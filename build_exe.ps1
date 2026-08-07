# Builds a portable HELIX.exe with the bundled offline Vosk language model.
# Run from PowerShell: .\build_exe.ps1
$ErrorActionPreference = 'Stop'

$userPython = Join-Path $env:LocalAppData 'Programs\Python\Python313\python.exe'
if (Test-Path -LiteralPath $userPython -PathType Leaf) {
    # Prefer the supported version even if another version is the Windows default.
    $pythonCommand = Get-Item -LiteralPath $userPython
} else {
    $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
    if (-not $pythonCommand) {
        $pythonCommand = Get-Command py -ErrorAction SilentlyContinue
    }
}
if (-not $pythonCommand) {
    throw 'Python 3.11-3.13 was not found. Install it from python.org, select "Add Python to PATH", then run this script again.'
}

$pythonPath = $pythonCommand.Path
if (-not $pythonPath) {
    $pythonPath = $pythonCommand.FullName
}
$pythonVersion = & $pythonPath --version 2>&1
if ($pythonVersion -notmatch 'Python 3\.(11|12|13)\.') {
    throw "HELIX packaging needs Python 3.11, 3.12, or 3.13. Detected: $pythonVersion"
}

& $pythonPath -m pip install --upgrade pip
& $pythonPath -m pip install -r requirements.txt
& $pythonPath -m PyInstaller --noconfirm --clean --onefile --name HELIX `
    --noconsole `
    --add-data "assets;assets" src\main.py

& $pythonPath -m PyInstaller --noconfirm --clean --onefile --name HELIX-ENROLL `
    --console `
    --add-data "assets;assets" src\enroll_owner.py

& powershell -ExecutionPolicy Bypass -File "$PSScriptRoot\install_startup.ps1"
Write-Host "Built and added to startup: $PWD\dist\HELIX.exe"
