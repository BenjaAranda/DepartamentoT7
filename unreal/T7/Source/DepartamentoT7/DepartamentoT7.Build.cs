using UnrealBuildTool;
public class DepartamentoT7 : ModuleRules {
    public DepartamentoT7(ReadOnlyTargetRules Target) : base(Target) {
        PCHUsage=PCHUsageMode.UseExplicitOrSharedPCHs;
        PublicDependencyModuleNames.AddRange(new[]{"Core","CoreUObject","Engine","InputCore","Json","JsonUtilities"});
    }
}
