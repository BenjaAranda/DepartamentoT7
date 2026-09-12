param([ValidateSet('build','import','check','capture','play')][string]$Action='play')
$ErrorActionPreference='Stop'
$t7Project=Join-Path $PSScriptRoot 'T7/DepartamentoT7.uproject'
$t7Engine=Join-Path $env:ProgramFiles 'Epic Games/UE_5.8/Engine'
$t7Editor=Join-Path $t7Engine 'Binaries/Win64/UnrealEditor-Cmd.exe'
if($Action -eq 'build'){
    & (Join-Path $t7Engine 'Build/BatchFiles/Build.bat') DepartamentoT7Editor Win64 Development "-Project=$t7Project" -WaitMutex -NoHotReloadFromIDE -MaxParallelActions=6
    exit $LASTEXITCODE
}
if($Action -eq 'import'){
    & $t7Editor $t7Project '-run=pythonscript' ('-script='+ (Join-Path $PSScriptRoot 'scripts/import-apartment.py')) -unattended -NullRHI -NoSound
    if($LASTEXITCODE -ne 0){exit $LASTEXITCODE}
    & $t7Editor $t7Project '-run=pythonscript' ('-script='+ (Join-Path $PSScriptRoot 'scripts/prepare-evidence.py')) -unattended -NullRHI -NoSound
}elseif($Action -eq 'check'){
    & $t7Editor $t7Project '-run=pythonscript' ('-script='+ (Join-Path $PSScriptRoot 'scripts/prepare-evidence.py')) -unattended -NullRHI -NoSound
    if($LASTEXITCODE -ne 0){exit $LASTEXITCODE}
    & $t7Editor $t7Project /Game/T7/Apartment -game -T7Validate -unattended -NullRHI -NoSound
}elseif($Action -eq 'capture'){
    & $t7Editor $t7Project /Game/T7/Apartment -game -T7Capture -unattended -RenderOffscreen -ResX=1280 -ResY=720 -ForceRes -NoSound
}else{
    & $t7Editor $t7Project /Game/T7/Apartment -game -windowed -ResX=1280 -ResY=720
}
exit $LASTEXITCODE
