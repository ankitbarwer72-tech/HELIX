# Removes only HELIX's current-user automatic startup entry.
$ErrorActionPreference = 'Stop'

$runKey = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run'
Remove-ItemProperty -Path $runKey -Name 'HELIX' -ErrorAction SilentlyContinue
Write-Host 'HELIX automatic startup removed.'
