# Desktop frontend

The first Tauri 2 and React shell is under `src/` and `src-tauri/`. It provides
the synthetic-data Owner/MFA and Health Record screens. Packaged UI requests
are proxied through Rust Tauri commands; the API is never called directly by
the WebView.

On Windows, build the local API sidecar, then start the desktop shell:

```powershell
..\backend\scripts\build_windows_sidecar.ps1
npm install
npm run build
npm run tauri dev
```

The Tauri host starts the packaged API child, sends a random per-run IPC
secret through stdin, proxies API calls over Tauri commands, and validates the
child PID during readiness. The current loopback channel and PID check are not
a verified Windows named-pipe or same-user-process isolation boundary. The
Windows installer, startup race, shutdown, and offline behavior still require
Windows testing. Do not use real health data.

For Windows build, offline acceptance steps and a results form, see the
[Windows test protocol](../docs/implementation/windows-testprotokoll.md).
