#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "GameFramework/Character.h"
#include "GameFramework/GameModeBase.h"
#include "GameFramework/HUD.h"
#include "T7Simulation.generated.h"
class UBoxComponent;
class UCameraComponent;

USTRUCT()
struct FT7Door {
    GENERATED_BODY()
    FString Id, Opening, Label;
    FVector Pivot, LocalCenter, Extent;
    double Base=0, Swing=0, Fraction=0, Target=0;
    UPROPERTY() TObjectPtr<UBoxComponent> Collider;
    UPROPERTY() TObjectPtr<AActor> Visual;
};

UCLASS()
class DEPARTAMENTOT7_API AT7World : public AActor {
    GENERATED_BODY()
public:
    AT7World();
    virtual void BeginPlay() override;
    virtual void Tick(float DeltaSeconds) override;
    UPROPERTY() TArray<FT7Door> Doors;
    UPROPERTY() TArray<TObjectPtr<UBoxComponent>> Solids;
    FVector Spawn;
    FString Revision, Message;
    FT7Door* NearestDoor(const FVector& Position);
    void Interact(const FVector& Position);
    bool ResetVisitor(class AT7Visitor* Visitor);
    void PlaceDoor(FT7Door& Door, double Fraction);
private:
    double Accumulator=0;
    bool bValidate=false;
    bool bCapture=false;
    int32 CaptureIndex=-1, CaptureFrame=0, SafetyFrame=0;
    FVector SafetyStart;
    double SafetyDisplacement=0;
    UPROPERTY() TObjectPtr<class ACameraActor> EvidenceCamera;
    int32 RouteIndex=-1, Waypoint=0, SweepIndex=0, SweepPhase=0, TestFrame=0;
    float WaypointTime=0;
    double EyeMin=10000, EyeMax=-10000;
    TArray<TSharedPtr<class FJsonValue>> Routes, OpenRoutes;
    TArray<FVector> Path;
    TArray<TSharedPtr<class FJsonValue>> Results;
    void ValidateTick(float DeltaSeconds);
    void ValidationFinished(const FString& Error);
    void CaptureTick();
};

UCLASS()
class DEPARTAMENTOT7_API AT7Visitor : public ACharacter {
    GENERATED_BODY()
public:
    AT7Visitor();
    virtual void BeginPlay() override;
    virtual void Tick(float DeltaSeconds) override;
    virtual void SetupPlayerInputComponent(UInputComponent* Input) override;
    UPROPERTY(VisibleAnywhere) TObjectPtr<UCameraComponent> Camera;
    UPROPERTY() TObjectPtr<AT7World> Apartment;
    void Forward(float Value);
    void Right(float Value);
    void Yaw(float Value);
    void Pitch(float Value);
    void Use();
    void Pause();
    void Reset();
};

UCLASS()
class DEPARTAMENTOT7_API AT7HUD : public AHUD {
    GENERATED_BODY()
public: virtual void DrawHUD() override;
};

UCLASS()
class DEPARTAMENTOT7_API AT7GameMode : public AGameModeBase {
    GENERATED_BODY()
public: AT7GameMode();
};
