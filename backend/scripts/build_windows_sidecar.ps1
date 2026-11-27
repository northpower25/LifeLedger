$ErrorActionPreference = "Stop"

$backend = Split-Path -Parent $PSScriptRoot
$repository = Split-Path -Parent $backend
$binaries = Join-Path $repository "frontend-desktop/src-tauri/binaries"
$work = Join-Path $env:TEMP "lifeledger-pyinstaller"

Push-Location $backend
try {
    python -m pip install -e ".[package]"
    if ($LASTEXITCODE -ne 0) { throw "Installing sidecar dependencies failed ($LASTEXITCODE)." }
    python -m PyInstaller `
        --clean `
        --noconfirm `
        --onefile `
        --name lifeledger-api `
        --paths $backend `
        --add-data "lifeledger/schema.sql;lifeledger" `
        --distpath (Join-Path $work "dist") `
        --workpath (Join-Path $work "work") `
        --specpath $work `
        lifeledger/launcher.py
    if ($LASTEXITCODE -ne 0) { throw "Building the sidecar failed ($LASTEXITCODE)." }

    New-Item -ItemType Directory -Force -Path $binaries | Out-Null
    Copy-Item `
        (Join-Path $work "dist/lifeledger-api.exe") `
        (Join-Path $binaries "lifeledger-api-x86_64-pc-windows-msvc.exe") `
        -Force
}
finally {
    Pop-Location
}
