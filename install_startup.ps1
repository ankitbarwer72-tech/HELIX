# Adds HELIX for the currently signed-in Windows user at every login.
# No administrator permission is required.
$ErrorActionPreference = 'Stop'

$exePath = Join-Path $PSScriptRoot 'dist\HELIX.exe'
if (-not (Test-Path -LiteralPath $exePath -PathType Leaf)) {
    throw "HELIX.exe was not found at $exePath. Run build_exe.ps1 first."
}

$resolvedExe = (Resolve-Path -LiteralPath $exePath).Path
$runKey = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run'
New-Item -Path $runKey -Force | Out-Null
Set-ItemProperty -Path $runKey -Name 'HELIX' -Value ('"{0}"' -f $resolvedExe)

Write-Host "HELIX will start automatically when you sign in to Windows."
