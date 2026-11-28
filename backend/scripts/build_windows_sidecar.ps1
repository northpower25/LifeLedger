$ErrorActionPreference = "Stop"

$backend = Split-Path -Parent $PSScriptRoot
$repository = Split-Path -Parent $backend
$binaries = Join-Path $repository "frontend-desktop/src-tauri/binaries"
$work = Join-Path $env:TEMP "lifeledger-pyinstaller"
$schema = Join-Path $backend "lifeledger/schema.sql"

Push-Location $backend
try {
    python -m pip install -e ".[package]"
    if ($LASTEXITCODE -ne 0) { throw "Installing sidecar dependencies failed ($LASTEXITCODE)." }
    python -m PyInstaller `
        --clean `
        --noconfirm `
        --onedir `
        --name lifeledger-api `
        --paths $backend `
        --add-data "$schema;lifeledger" `
        --distpath $binaries `
        --workpath (Join-Path $work "work") `
        --specpath $work `
        lifeledger/launcher.py
    if ($LASTEXITCODE -ne 0) { throw "Building the sidecar failed ($LASTEXITCODE)." }
}
finally {
    Pop-Location
}
