# Backend

The first offline slice has a FastAPI development service under
`lifeledger/`. It uses SQLite behind the VitaFabric access path and supports
only synthetic `Patient`, `DocumentReference`, and `MedicationStatement`
data. See the [implementation contract](../docs/implementation/first-offline-slice.md)
for fixed assumptions and security limitations.

From `backend/`, create a virtual environment and install the project:

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[test]"
LIFELEDGER_DEV_MODE=1 PYTHONPATH=. uvicorn lifeledger.app:app --host 127.0.0.1 --port 8765
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1` and set
`$env:LIFELEDGER_DEV_MODE = "1"`. Without the explicit development flag the
API rejects all requests unless started by its Tauri host with the private
IPC secret. The development API binds only to loopback. Do not expose it to a
network or use real health data.

Run backend tests from the repository root with:

```sh
PYTHONPATH=backend python -m pytest backend/tests
```

Regenerate the checked-in OpenAPI contract after changing routes or schemas:

```sh
PYTHONPATH=backend python backend/scripts/export_openapi.py
```
