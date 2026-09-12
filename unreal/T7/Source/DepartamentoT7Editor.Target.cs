using UnrealBuildTool;
public class DepartamentoT7EditorTarget : TargetRules {
    public DepartamentoT7EditorTarget(TargetInfo Target) : base(Target) {
        Type=TargetType.Editor; DefaultBuildSettings=BuildSettingsVersion.V7;
        IncludeOrderVersion=EngineIncludeOrderVersion.Unreal5_8;
        ExtraModuleNames.Add("DepartamentoT7");
    }
}
