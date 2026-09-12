#include "T7Simulation.h"
#include "Camera/CameraComponent.h"
#include "Camera/CameraActor.h"
#include "UnrealClient.h"
#include "Components/BoxComponent.h"
#include "Components/CapsuleComponent.h"
#include "Engine/Canvas.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "EngineUtils.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/PlayerController.h"
#include "Kismet/GameplayStatics.h"
#include "Kismet/KismetSystemLibrary.h"
#include "Dom/JsonObject.h"
#include "Misc/App.h"
#include "Misc/CommandLine.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "Serialization/JsonSerializer.h"

namespace {
TSharedPtr<FJsonObject> ReadJson(const FString& Name) {
    FString Text; TSharedPtr<FJsonObject> Object;
    if(!FFileHelper::LoadFileToString(Text,*(FPaths::ProjectContentDir()/TEXT("Data")/Name)) || !FJsonSerializer::Deserialize(TJsonReaderFactory<>::Create(Text),Object))
        UE_LOG(LogTemp,Fatal,TEXT("Missing or invalid T7 data: %s"),*Name);
    return Object;
}
// Matches GLTFCore ConversionUtilities.h; metres become centimetres exactly once.
FVector Convert(const TArray<TSharedPtr<FJsonValue>>& A) { return FVector(A[0]->AsNumber(),A[2]->AsNumber(),A[1]->AsNumber())*100; }
FQuat DoorRotation(const FT7Door& D,double F) { return FQuat(FVector::UpVector,-(D.Base+D.Swing*F)); }
FVector DoorCenter(const FT7Door& D,double F) { return D.Pivot+DoorRotation(D,F).RotateVector(D.LocalCenter); }
}

AT7World::AT7World() { PrimaryActorTick.bCanEverTick=true; RootComponent=CreateDefaultSubobject<USceneComponent>(TEXT("Root")); }
void AT7World::BeginPlay() {
    Super::BeginPlay(); auto Data=ReadJson(TEXT("departamento-t7.json"));
    Revision=Data->GetStringField(TEXT("revision"));Spawn=Convert(Data->GetArrayField(TEXT("spawn")));Spawn.Z=84;
    for(auto Value:Data->GetArrayField(TEXT("colliders"))) {
        auto C=Value->AsObject();FString Id=C->GetStringField(TEXT("id"));
        auto Box=NewObject<UBoxComponent>(this,FName(*Id));Box->SetupAttachment(RootComponent);Box->SetBoxExtent(Convert(C->GetArrayField(TEXT("size")))/2);
        Box->SetWorldLocation(Convert(C->GetArrayField(TEXT("center"))));Box->SetCollisionProfileName(TEXT("BlockAll"));Box->SetHiddenInGame(true);Box->RegisterComponent();AddInstanceComponent(Box);Solids.Add(Box);
    }
    for(auto Value:Data->GetArrayField(TEXT("doors"))) {
        auto C=Value->AsObject();FT7Door D;D.Id=C->GetStringField(TEXT("id"));D.Opening=C->GetStringField(TEXT("opening"));
        D.Label=D.Id;C->TryGetStringField(TEXT("label"),D.Label);D.Pivot=Convert(C->GetArrayField(TEXT("pivot")));D.LocalCenter=Convert(C->GetArrayField(TEXT("center_local")));D.Extent=Convert(C->GetArrayField(TEXT("size")))/2;
        D.Base=C->GetNumberField(TEXT("base_rotation_y"));D.Swing=C->GetNumberField(TEXT("swing_radians"));
        for(TActorIterator<AActor> It(GetWorld());It;++It)if(It->ActorHasTag(FName(*(D.Id+TEXT("_Pivot"))))){D.Visual=*It;break;}
        D.Collider=NewObject<UBoxComponent>(this,FName(*(D.Id+TEXT("_Collision"))));D.Collider->SetupAttachment(RootComponent);D.Collider->SetBoxExtent(D.Extent);D.Collider->SetMobility(EComponentMobility::Movable);D.Collider->SetCollisionProfileName(TEXT("BlockAllDynamic"));D.Collider->SetHiddenInGame(true);D.Collider->RegisterComponent();AddInstanceComponent(D.Collider);Doors.Add(D);PlaceDoor(Doors.Last(),0);
    }
    if(auto Visitor=Cast<AT7Visitor>(UGameplayStatics::GetPlayerCharacter(this,0)))ResetVisitor(Visitor);
    bValidate=FParse::Param(FCommandLine::Get(),TEXT("T7Validate"));
    bCapture=FParse::Param(FCommandLine::Get(),TEXT("T7Capture"));
    if(bValidate){Routes=ReadJson(TEXT("routes.json"))->GetArrayField(TEXT("paths"));OpenRoutes=ReadJson(TEXT("routes-open.json"))->GetArrayField(TEXT("paths"));FApp::SetUseFixedTimeStep(true);FApp::SetFixedDeltaTime(1.0/60.0);}
    if(bCapture)Routes=ReadJson(TEXT("routes.json"))->GetArrayField(TEXT("paths"));
}
void AT7World::PlaceDoor(FT7Door& D,double F) {
    D.Fraction=F;D.Collider->SetWorldLocationAndRotation(DoorCenter(D,F),DoorRotation(D,F),false,nullptr,ETeleportType::TeleportPhysics);
    if(D.Visual)D.Visual->SetActorLocationAndRotation(D.Pivot,DoorRotation(D,F),false,nullptr,ETeleportType::TeleportPhysics);
}
void AT7World::Tick(float DeltaSeconds) {
    Super::Tick(DeltaSeconds);Accumulator+=FMath::Min(DeltaSeconds,.1f);
    while(Accumulator>=1.0/60) {
        for(FT7Door& D:Doors) {
            if(FMath::Abs(D.Target-D.Fraction)<1.e-6)continue;
            double Next=FMath::FInterpConstantTo(D.Fraction,D.Target,1.0/60,1.1);
            FCollisionQueryParams Query;Query.AddIgnoredComponent(D.Collider.Get());
            for(auto B:Solids)if(B->GetName().StartsWith(D.Opening+TEXT("_")))Query.AddIgnoredComponent(B.Get());
            if(GetWorld()->OverlapBlockingTestByChannel(DoorCenter(D,Next),DoorRotation(D,Next),ECC_Pawn,FCollisionShape::MakeBox(D.Extent-FVector(.2)),Query)) {D.Target=D.Fraction;Message=TEXT("Hay un obstaculo junto a la puerta.");}
            else PlaceDoor(D,Next);
        }
        Accumulator-=1.0/60;
    }
    if(bValidate)ValidateTick(DeltaSeconds);
    if(bCapture)CaptureTick();
}
FT7Door* AT7World::NearestDoor(const FVector& Position) {
    FT7Door* Best=nullptr;double Distance=155;
    for(FT7Door& D:Doors){
        double V=FVector::Dist2D(Position,D.Pivot);if(V>=Distance)continue;
        FVector From(Position.X,Position.Y,110),To=DoorCenter(D,D.Fraction);To.Z=110;
        FCollisionQueryParams Query;Query.AddIgnoredActor(UGameplayStatics::GetPlayerCharacter(this,0));FHitResult Hit;
        if(GetWorld()->LineTraceSingleByChannel(Hit,From,To,ECC_Visibility,Query)&&Hit.GetComponent()!=D.Collider)continue;
        Distance=V;Best=&D;
    }
    return Best;
}
void AT7World::Interact(const FVector& Position){if(auto D=NearestDoor(Position)){D->Target=D->Target<.5?1:0;Message.Empty();}}
bool AT7World::ResetVisitor(AT7Visitor* V){
    FCollisionQueryParams Q;Q.AddIgnoredActor(V);
    if(GetWorld()->OverlapBlockingTestByChannel(Spawn,FQuat::Identity,ECC_Pawn,FCollisionShape::MakeCapsule(22,82),Q)){Message=TEXT("El acceso esta ocupado.");return false;}
    V->SetActorLocation(Spawn,false,nullptr,ETeleportType::TeleportPhysics);V->GetCharacterMovement()->StopMovementImmediately();if(V->GetController())V->GetController()->SetControlRotation(FRotator(0,180,0));return true;
}
void AT7World::ValidationFinished(const FString& Error){
    auto Report=MakeShared<FJsonObject>();Report->SetStringField(TEXT("revision"),Revision);Report->SetStringField(TEXT("error"),Error);Report->SetBoolField(TEXT("passed"),Error.IsEmpty());Report->SetNumberField(TEXT("eye_min_cm"),EyeMin);Report->SetNumberField(TEXT("eye_max_cm"),EyeMax);Report->SetArrayField(TEXT("routes"),Results);Report->SetNumberField(TEXT("door_sweeps_passed"),SweepIndex);Report->SetNumberField(TEXT("frames"),TestFrame);
    Report->SetNumberField(TEXT("active_player_door_displacement_cm"),SafetyDisplacement);
    FString Text;FJsonSerializer::Serialize(Report,TJsonWriterFactory<>::Create(&Text));FFileHelper::SaveStringToFile(Text,*(FPaths::ProjectSavedDir()/TEXT("t7-runtime-check.json")));
    UE_LOG(LogTemp,Display,TEXT("T7_VALIDATION_FINISHED %s"),*Error);bValidate=false;UKismetSystemLibrary::QuitGame(this,nullptr,EQuitPreference::Quit,false);
}
void AT7World::ValidateTick(float Dt){
    TestFrame++;auto V=Cast<AT7Visitor>(UGameplayStatics::GetPlayerCharacter(this,0));if(!V){if(TestFrame>120)ValidationFinished(TEXT("Visitor did not spawn"));return;}
    if(SweepIndex<Doors.Num()){
        V->SetActorLocation(FVector(1350,-300,84),false,nullptr,ETeleportType::TeleportPhysics);
        auto& D=Doors[SweepIndex];WaypointTime+=Dt;
        if(SweepPhase==0){D.Target=1;SweepPhase=1;WaypointTime=0;}
        if(SweepPhase==1&&D.Fraction>.999){D.Target=0;SweepPhase=2;WaypointTime=0;}
        if(SweepPhase==2&&D.Fraction<.001){SweepIndex++;SweepPhase=0;WaypointTime=0;}
        if(WaypointTime>2.5)ValidationFinished(TEXT("Door sweep blocked: ")+D.Id);
        return;
    }
    if(SafetyFrame<90){
        if(SafetyFrame==0){ResetVisitor(V);SafetyStart=V->GetActorLocation();Doors[0].Target=1;}
        SafetyDisplacement=FMath::Max(SafetyDisplacement,FVector::Dist2D(SafetyStart,V->GetActorLocation()));SafetyFrame++;
        if(SafetyFrame==90){if(Doors[0].Fraction>.999||SafetyDisplacement>.1){ValidationFinished(TEXT("Door failed active visitor safety"));return;}PlaceDoor(Doors[0],0);Doors[0].Target=0;}
        return;
    }
    if(Path.IsEmpty() || Waypoint>=Path.Num()){
        if(RouteIndex>=0){auto R=MakeShared<FJsonObject>();R->SetStringField(TEXT("room"),Routes[RouteIndex%Routes.Num()]->AsObject()->GetStringField(TEXT("room")));R->SetBoolField(TEXT("wardrobes_open"),RouteIndex>=Routes.Num());R->SetBoolField(TEXT("round_trip"),true);Results.Add(MakeShared<FJsonValueObject>(R));UE_LOG(LogTemp,Display,TEXT("T7_ROUTE_OK %d"),RouteIndex);}
        RouteIndex++;if(RouteIndex>=Routes.Num()*2){ValidationFinished(TEXT(""));return;}
        auto Route=(RouteIndex>=Routes.Num()?OpenRoutes:Routes)[RouteIndex%Routes.Num()]->AsObject();FString Room=Route->GetStringField(TEXT("room")),Opening;
        if(Room==TEXT("D3"))Opening=TEXT("O02");if(Room==TEXT("D1"))Opening=TEXT("O03");if(Room==TEXT("D2"))Opening=TEXT("O04");if(Room==TEXT("BATH")||Room==TEXT("SHOWER"))Opening=TEXT("O05");if(Room==TEXT("LOGIA"))Opening=TEXT("O06");if(Room==TEXT("CORRIDOR"))Opening=TEXT("O01");
        for(auto& D:Doors){double F=(D.Opening==Opening||(RouteIndex>=Routes.Num()&&D.Opening.Contains(TEXT("Wardrobe"))))?1:0;PlaceDoor(D,F);D.Target=F;}
        ResetVisitor(V);Path.Empty();for(auto P:Route->GetArrayField(TEXT("path"))){auto A=P->AsArray();Path.Add(FVector(A[0]->AsNumber()*100,A[1]->AsNumber()*100,0));}
        for(int32 I=Path.Num()-2;I>=0;I--){const FVector ReturnPoint=Path[I];Path.Add(ReturnPoint);}Waypoint=0;WaypointTime=0;
    }
    FVector P=V->GetActorLocation(),Difference=Path[Waypoint]-P;Difference.Z=0;
    if(Difference.Size()<5.5){Waypoint++;WaypointTime=0;return;}
    V->AddMovementInput(Difference.GetSafeNormal(),1);if(V->GetController())V->GetController()->SetControlRotation(Difference.Rotation());WaypointTime+=Dt;
    if(TestFrame>60){double Eye=V->Camera->GetComponentLocation().Z;EyeMin=FMath::Min(EyeMin,Eye);EyeMax=FMath::Max(EyeMax,Eye);if(Eye<157||Eye>163){ValidationFinished(TEXT("Eye height out of range"));return;}}
    if(WaypointTime>3)ValidationFinished(FString::Printf(TEXT("Route stuck %d waypoint %d at %.2f,%.2f"),RouteIndex,Waypoint,P.X,P.Y));
}

void AT7World::CaptureTick(){
    auto PC=UGameplayStatics::GetPlayerController(this,0);if(!PC)return;
    CaptureFrame++;
    if(CaptureFrame==1){
        CaptureIndex++;if(CaptureIndex>=Routes.Num()+2){UE_LOG(LogTemp,Display,TEXT("T7_CAPTURES_OK"));bCapture=false;UKismetSystemLibrary::QuitGame(this,PC,EQuitPreference::Quit,false);return;}
        if(!EvidenceCamera)EvidenceCamera=GetWorld()->SpawnActor<ACameraActor>();
        PC->SetViewTarget(EvidenceCamera);auto Camera=EvidenceCamera->GetCameraComponent();
        const bool Inspect=CaptureIndex<2;
        for(TActorIterator<AActor> It(GetWorld());It;++It)if(It->ActorHasTag(TEXT("inspection_hide")))It->SetActorHiddenInGame(Inspect);
        Camera->SetProjectionMode(Inspect?ECameraProjectionMode::Orthographic:ECameraProjectionMode::Perspective);Camera->SetOrthoWidth(CaptureIndex==1?1450:2300);Camera->SetFieldOfView(75);
        if(CaptureIndex==0){FVector P(-800,1200,1400),T(630,-180,100);EvidenceCamera->SetActorLocationAndRotation(P,(T-P).Rotation());}
        else if(CaptureIndex==1)EvidenceCamera->SetActorLocationAndRotation(FVector(630,-180,2500),FRotator(-90,-90,0));
        else{
            auto R=Routes[CaptureIndex-2]->AsObject();auto A=R->GetArrayField(TEXT("path")).Last()->AsArray();FString Room=R->GetStringField(TEXT("room"));FVector P(A[0]->AsNumber()*100,A[1]->AsNumber()*100,160),Target=P+FVector(-100,0,-35);
            const auto InventoryData=ReadJson(TEXT("departamento-t7.json"));
            for(auto Value:InventoryData->GetArrayField(TEXT("inventory"))){auto Item=Value->AsObject();if(Item->GetStringField(TEXT("room"))==Room){auto Center=Item->GetArrayField(TEXT("center"));Target=FVector(Center[0]->AsNumber()*100,-Center[1]->AsNumber()*100,85);break;}}
            if(Room==TEXT("SHOWER"))Target=P+FVector(0,-200,-35);
            EvidenceCamera->SetActorLocationAndRotation(P,(Target-P).Rotation());
        }
    }
    if(CaptureFrame==120){FString Name=CaptureIndex==0?TEXT("isometrica"):CaptureIndex==1?TEXT("planta"):Routes[CaptureIndex-2]->AsObject()->GetStringField(TEXT("room"));FScreenshotRequest::RequestScreenshot(FPaths::ProjectSavedDir()/TEXT("T7Captures")/(Name+TEXT(".png")),false,false);}
    if(CaptureFrame>=150)CaptureFrame=0;
}

AT7Visitor::AT7Visitor(){
    PrimaryActorTick.bCanEverTick=true;GetCapsuleComponent()->InitCapsuleSize(22,82);BaseEyeHeight=78;
    Camera=CreateDefaultSubobject<UCameraComponent>(TEXT("Eye"));Camera->SetupAttachment(GetCapsuleComponent());Camera->SetRelativeLocation(FVector(0,0,78));Camera->bUsePawnControlRotation=true;
    GetCharacterMovement()->MaxWalkSpeed=160;GetCharacterMovement()->MaxStepHeight=5;GetCharacterMovement()->BrakingDecelerationWalking=2000;GetCharacterMovement()->MaxAcceleration=1800;GetCharacterMovement()->bOrientRotationToMovement=false;
}
void AT7Visitor::BeginPlay(){Super::BeginPlay();for(TActorIterator<AT7World> It(GetWorld());It;++It){Apartment=*It;break;}if(Apartment&&Apartment->HasActorBegunPlay())Apartment->ResetVisitor(this);}
void AT7Visitor::Tick(float Dt){Super::Tick(Dt);auto Move=GetCharacterMovement();if(Move->IsMovingOnGround())Camera->SetRelativeLocation(FVector(0,0,160-GetCapsuleComponent()->GetScaledCapsuleHalfHeight()-Move->CurrentFloor.FloorDist));}
void AT7Visitor::SetupPlayerInputComponent(UInputComponent* Input){
    Super::SetupPlayerInputComponent(Input);Input->BindAxis(TEXT("Forward"),this,&AT7Visitor::Forward);Input->BindAxis(TEXT("Right"),this,&AT7Visitor::Right);Input->BindAxis(TEXT("Yaw"),this,&AT7Visitor::Yaw);Input->BindAxis(TEXT("Pitch"),this,&AT7Visitor::Pitch);
    Input->BindAction(TEXT("Use"),IE_Pressed,this,&AT7Visitor::Use);Input->BindAction(TEXT("Reset"),IE_Pressed,this,&AT7Visitor::Reset);auto& Binding=Input->BindAction(TEXT("Pause"),IE_Pressed,this,&AT7Visitor::Pause);Binding.bExecuteWhenPaused=true;
}
void AT7Visitor::Forward(float V){if(Controller)AddMovementInput(FRotator(0,Controller->GetControlRotation().Yaw,0).Vector(),V);}
void AT7Visitor::Right(float V){if(Controller)AddMovementInput(FRotationMatrix(FRotator(0,Controller->GetControlRotation().Yaw,0)).GetUnitAxis(EAxis::Y),V);}
void AT7Visitor::Yaw(float V){AddControllerYawInput(V*.7f);}
void AT7Visitor::Pitch(float V){AddControllerPitchInput(V*.7f);}
void AT7Visitor::Use(){if(Apartment)Apartment->Interact(GetActorLocation());}
void AT7Visitor::Reset(){if(Apartment)Apartment->ResetVisitor(this);}
void AT7Visitor::Pause(){if(auto PC=Cast<APlayerController>(Controller)){bool P=!UGameplayStatics::IsGamePaused(this);PC->SetPause(P);PC->bShowMouseCursor=P;}}
void AT7HUD::DrawHUD(){
    Super::DrawHUD();if(!Canvas||FParse::Param(FCommandLine::Get(),TEXT("T7Capture")))return;DrawRect(FLinearColor(0.035f,.07f,.09f,.85f),18,18,520,77);DrawText(TEXT("DepartamentoT7 | Los Altos de Algarrobo"),FLinearColor::White,32,28,nullptr,1.25f);
    DrawText(TEXT("W A S D: caminar   Raton: mirar   E: puerta   Esc: pausa   R: acceso"),FLinearColor(.8f,.87f,.9f),32,61,nullptr,1);
    if(auto V=Cast<AT7Visitor>(GetOwningPawn()))if(V->Apartment){FString Text=V->Apartment->Message;if(Text.IsEmpty())if(auto D=V->Apartment->NearestDoor(V->GetActorLocation()))Text=TEXT("E | ")+D->Label;DrawText(Text,FLinearColor::White,32,Canvas->SizeY-50,nullptr,1.2f);}
    DrawText(TEXT("+"),FLinearColor::White,Canvas->SizeX/2,Canvas->SizeY/2,nullptr,1);
}
AT7GameMode::AT7GameMode(){DefaultPawnClass=AT7Visitor::StaticClass();HUDClass=AT7HUD::StaticClass();}
