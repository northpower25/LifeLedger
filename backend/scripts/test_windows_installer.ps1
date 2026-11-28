$ErrorActionPreference = "Stop"

$repository = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$bundle = Join-Path $repository "frontend-desktop/src-tauri/target/release/bundle/msi"
$installers = @(Get-ChildItem $bundle -Filter "*.msi")
if ($installers.Count -ne 1) { throw "Expected one MSI, found $($installers.Count)." }

$install = Start-Process msiexec.exe -ArgumentList @(
    "/i", "`"$($installers[0].FullName)`"", "/qn", "/norestart"
) -Wait -PassThru
if ($install.ExitCode -ne 0) { throw "MSI installation failed ($($install.ExitCode))." }

$desktop = Join-Path $env:ProgramFiles "LifeLedger/lifeledger-desktop.exe"
$sidecar = Join-Path $env:ProgramFiles "LifeLedger/lifeledger-api/lifeledger-api.exe"
if (!(Test-Path $desktop) -or !(Test-Path $sidecar)) {
    throw "Installed desktop or sidecar is missing."
}

$env:LIFELEDGER_DATABASE = Join-Path $env:RUNNER_TEMP "lifeledger-smoke-$([guid]::NewGuid()).sqlite3"
Remove-Item Env:LIFELEDGER_API_BIN -ErrorAction SilentlyContinue
Remove-Item Env:LIFELEDGER_DEV_MODE -ErrorAction SilentlyContinue
$errorLog = Join-Path $env:RUNNER_TEMP "lifeledger-smoke-stderr.log"
$app = Start-Process $desktop -RedirectStandardError $errorLog -PassThru
$apiProcessId = $null
try {
    $deadline = (Get-Date).AddSeconds(45)
    while ((Get-Date) -lt $deadline) {
        $app.Refresh()
        if ($app.HasExited) { throw "Desktop exited during startup ($($app.ExitCode))." }
        $api = @(Get-CimInstance Win32_Process -Filter "ParentProcessId = $($app.Id)" |
            Where-Object { $_.Name -eq "lifeledger-api.exe" })
        if ($api.Count -eq 1) { $apiProcessId = $api[0].ProcessId }
        if ($apiProcessId -and (Test-Path $env:LIFELEDGER_DATABASE) -and $app.MainWindowHandle -ne 0) {
            break
        }
        Start-Sleep -Milliseconds 500
    }
    if (!$apiProcessId -or !(Test-Path $env:LIFELEDGER_DATABASE) -or $app.MainWindowHandle -eq 0) {
        throw "Installed app did not complete startup and owner-status request."
    }
    if (!$app.CloseMainWindow()) { throw "Could not close the desktop window." }
    if (!$app.WaitForExit(15000)) { throw "Desktop did not exit after closing its window." }
    $apiHandle = Get-Process -Id $apiProcessId -ErrorAction SilentlyContinue
    if ($apiHandle -and !$apiHandle.WaitForExit(10000)) {
        throw "API process remained running after desktop shutdown."
    }
}
catch {
    if (Test-Path $errorLog) { Get-Content $errorLog }
    throw
}
finally {
    if (!$app.HasExited) { Stop-Process -Id $app.Id -ErrorAction SilentlyContinue }
    if ($apiProcessId) { Stop-Process -Id $apiProcessId -ErrorAction SilentlyContinue }
}
