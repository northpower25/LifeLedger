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

The Tauri host starts the packaged API child and sends a per-run IPC secret
and ephemeral TLS keypair through stdin. It pins the generated certificate and
uses HTTPS for readiness and every proxied API call, so a loopback listener
without that key cannot receive credentials or API requests. Windows CI builds
the sidecar as a directory containing its runtime dependencies, and bundles
it with the desktop application in the MSI and NSIS installers. The desktop
executable alone is not a standalone distribution. Install, service
lifecycle, offline behavior, and runtime TLS still require manual Windows
testing. Isolation from another process running as the same user is not
claimed. Do not use real health data.

For Windows build, offline acceptance steps and a results form, see the
[Windows test protocol](../docs/implementation/windows-testprotokoll.md).
