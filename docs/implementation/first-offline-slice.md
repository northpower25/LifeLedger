# First Offline Vertical Slice

Status: implementation contract and backlog; synthetic test data only.
This document implements the frozen scope in RFC-0001 through RFC-0014. It
does not create or propose another RFC and does not reopen frozen architecture.
The machine-readable API contract is
[`openapi.json`](openapi.json); the executable database schema is
[`backend/lifeledger/schema.sql`](../../backend/lifeledger/schema.sql).
The Windows build and acceptance procedure, including a results form, is in
[`windows-testprotokoll.md`](windows-testprotokoll.md).

## Frozen scope

Windows desktop, Tauri, local FastAPI, SQLite behind VitaFabric, and the
integrated Health Record. The journey is local Owner setup/unlock, Patient
creation, DocumentReference import, MedicationStatement creation, timeline,
encrypted backup and restore. Only FHIR R4 `Patient`, `DocumentReference` and
`MedicationStatement` are accepted. All data, including documents, fixtures,
logs and backups, must be synthetic.

Plugins, marketplace, AI, synchronization, family, Home Assistant,
connectors, external integrations, other FHIR resource types, cloud services
and real health data are excluded. The Health Record is integrated in the
desktop distribution, not implemented as a plugin.

## Fixed implementation assumptions

These are bounded choices for this test slice, not questions or changes to
architecture:

| Area | Assumption |
| --- | --- |
| Owner | Exactly one local Primary Owner per database. Owner setup is one-time; setup can be resumed with the chosen password if the process exits before MFA confirmation. |
| MFA | Offline TOTP (RFC 6238), 6 digits, 30-second period; accept current step plus/minus one step for clock skew and reject reuse of an already accepted TOTP step. Password plus TOTP is required for every unlock. |
| Recovery | A backup can be recovered from the start screen only into an empty local database, using the separate backup passphrase. The restored Owner password and TOTP are still required to unlock; no password or TOTP reset/recovery is implemented. A populated database is never overwritten by this recovery path. |
| Password KDF | Argon2id, time cost 3, memory 65,536 KiB, parallelism 1, 32-byte derived key, random 16-byte salt. |
| Data encryption | AES-256-GCM; random 96-bit nonce per encrypted value; table and opaque row ID are authenticated associated data. A random 256-bit data key is wrapped by the Argon2id-derived password key. |
| Storage encryption boundary | Every FHIR resource, document body, consent, capability grant, audit payload and outbox payload is encrypted. SQLite schema, opaque IDs, row relationships, timestamps, status, event names, Argon2 password verifier and KDF salt remain visible as operational metadata. The test slice does not claim whole-file/SQLCipher encryption or protection against a process running as the same Windows user. |
| Session | Random bearer token held in process memory for 30 minutes. Lock, process exit, restore, or expiry invalidates it. |
| Consent and capabilities | Owner setup grants active, self-owned `health_record` consent for read/write on exactly the three allowed resource types, plus create/restore of backups. Explicit capabilities cover those operations. Both are checked at VitaFabric on each operation. Consent revoke is synchronous and fail-closed. |
| FHIR | FHIR R4 JSON with structural checks for these three resource types and local required-field/reference checks. The current slice does not claim full HL7 validator/profile conformance. |
| Documents | PDF, UTF-8 plain text, or PNG only; 10 MiB maximum. MIME signatures/encoding are checked. Document bytes are stored inside the encrypted DocumentReference payload. |
| Synthetic data | Create/import requests require `synthetic: true`; this is an explicit caller assertion, not an automated detector. Never use real records or upload user documents during development/testing. |
| Timeline | Descending local record-creation timestamp; timestamps are stored as UTC ISO-8601 metadata. Medication effective time remains inside its encrypted FHIR resource. |
| Backup | User supplies a separate passphrase (minimum 12 characters). The SQLite online-backup API snapshots a consistent database image up to 64 MiB; the full image is wrapped in an Argon2id-derived AES-256-GCM envelope. The desktop validates the backup, warns about data loss and requires the current Owner password and fresh TOTP before replacing the local database, including with another Owner's backup. A separate current-Owner backup can be saved first to a new file without overwriting existing files. Start-screen recovery requires an empty database and does not create an authenticated session. Restored Owner credentials are required to unlock. The legacy same-Owner restore endpoint remains supported. |
| Retention | No automatic purge/retention job in the test slice. User can remove the local test database only after closing the application. Do not rely on this prototype for records requiring retention or deletion guarantees. |
| Network | Packaged API binds to a random loopback port and uses per-launch TLS. The Tauri host generates an ephemeral self-signed certificate, pins it for every HTTPS request, and pipes the certificate, private key and IPC secret to the child over stdin. The API secret and request data are sent only inside the pinned TLS channel. Direct browser API access is allowed only with the explicit `LIFELEDGER_DEV_MODE=1` development flag. Windows lifecycle and same-user-process isolation remain unverified. |

These assumptions keep the implementation bounded but have consequences:
the SQLite file leaks timing and access-pattern metadata; a same-user process
may interfere with loopback service startup; the session token is a bearer
secret; TOTP depends on a reasonably correct local clock; and restore
overwrites the current local state. A 10 MiB document is Base64 encoded and
copied through the WebView, Tauri IPC, FastAPI request and encrypted SQLite
payload; this increases peak memory and import latency. These limitations
must remain visible in the test UI and must not be represented as production
security clearance.

## Deliverable 1: implementation backlog

Effort is relative engineering effort, not a calendar estimate:
S = 1–2 days, M = 3–5 days, L = 6–10 days. Tasks with unmet technical or
platform prerequisites are not complete.

| ID | Priority | Task | Status | Effort | Dependencies | Acceptance |
| --- | --- | --- | --- | --- | --- | --- |
| B1 | P0 | Implement encrypted local identity, Argon2id key derivation, TOTP setup/unlock, in-memory sessions | Implemented; needs Windows validation | M | None | First Owner setup is atomic/resumable; incorrect password/code denied; database contains no plaintext FHIR/document payload. |
| B2 | P0 | Implement SQLite schema, VitaFabric repository boundary, consent/capability enforcement, encrypted audit/outbox | Implemented in API; Windows authority boundary pending | M | B1 | Every data operation is checked at the gateway; writes/audit/outbox commit atomically; revoked consent immediately denies. |
| B3 | P0 | Implement Patient and MedicationStatement create/read plus Patient-linked document import and validation | Implemented with bounded local validation | M | B2 | Only the three allowed resource types can persist; invalid references, MIME/content mismatch and >10 MiB documents are rejected. |
| B4 | P0 | Implement timeline API/view and document retrieval | Implemented; desktop journey needs Windows test | S | B3 | Timeline shows allowed records for the selected Patient, newest first; access is audited. |
| B5 | P0 | Implement encrypted backup/restore and recovery tests | Implemented; Windows restore test pending | M | B2 | Wrong passphrase, modified ciphertext, unsupported schema and corrupt SQLite are rejected without replacing the active database; valid restore reinstates the synthetic fixture set. |
| B6 | P0 | Build Tauri Windows shell and integrated Health Record journey | Windows CI built sidecar, desktop EXE, MSI and NSIS; manual journey pending | L | B1–B5 | Windows app starts the local service, completes Owner → Patient → document → medication → timeline → backup/restore without network. |
| B7 | P0 | Verify/package the Windows IPC and service lifecycle | Per-launch pinned TLS implemented and Windows-compiled; runtime verification pending | L | B6 | Untrusted loopback listeners cannot receive API requests or credentials; no unauthenticated local HTTP fallback; safe startup/shutdown, packaged offline dependencies, and Windows-specific negative tests pass. Same-user process isolation is not claimed. |
| B8 | P0 | Run integration/offline/negative tests and dependency/license review | Backend tests pass on Linux and Windows CI; interactive Windows acceptance pending | M | B1–B7 | Acceptance suite passes on a clean Windows reference machine with networking disabled; only synthetic fixtures used. |
| B9 | P1 | Add signed release packaging and upgrade/migration verification | Not started | M | B8 | Signed installer and upgrade do not expose, reset or corrupt local data. Not required for the first internal test build. |

## Deliverable 2: repository structure

```text
backend/
  pyproject.toml
  lifeledger/
    app.py                 # FastAPI routes and local composition root
    crypto.py              # Argon2id, AES-256-GCM, encrypted payloads
    database.py            # SQLite connections and transactions
    schema.sql             # versioned local schema
  tests/                   # API and backend tests
frontend-desktop/
  package.json
  src/
    App.tsx                 # localized Health Record screens
    api.ts                  # typed API client
    i18n.ts                 # German/English message catalog
  src-tauri/
    Cargo.toml
    tauri.conf.json
    src/main.rs             # Windows host, service lifecycle and IPC boundary
platform/
  core/
    README.md               # identity, session, consent, capability, audit ownership
  vitafabric/
    README.md               # FHIR validation, provenance, repository gateway
tests/
  integration/              # API, storage, lifecycle, backup/restore
  offline/                  # network-disabled end-to-end checks
  fixtures/synthetic/       # synthetic JSON and document fixtures only
backend/scripts/
  build_windows_sidecar.ps1 # offline API executable build
  export_openapi.py         # static OpenAPI contract generator
```

Core and VitaFabric may share one local process in this slice but retain
separate modules and authority boundaries. Only VitaFabric code may call the
health-resource repository methods.

## Deliverable 3: API definitions

All paths are under `/api/v1`; request/response fields and error responses are
specified in OpenAPI. Authorization is `Authorization: Bearer <session>`.

| Operation | Endpoint | Purpose |
| --- | --- | --- |
| Owner status | `GET /owner/status` | Report whether setup exists and is confirmed; no profile data. |
| Owner setup | `POST /owner/setup` | Create the single local Owner and initial self-consent/capabilities; return the TOTP secret once. |
| Resume setup | `POST /owner/setup/resume` | Recover pending TOTP secret after interrupted setup, after password verification. |
| Confirm MFA | `POST /owner/setup/confirm` | Confirm TOTP and issue the first in-memory session. |
| Unlock | `POST /owner/unlock` | Verify password and TOTP; issue a 30-minute session. |
| Lock | `POST /owner/lock` | Audit and invalidate the current session. |
| Patient | `POST /patients`, `GET /patients` | Create/list synthetic FHIR Patient resources. |
| DocumentReference | `POST /patients/{patient_id}/documents`, `GET /patients/{patient_id}/documents` | Import/list synthetic patient-linked document resources and original bytes. |
| MedicationStatement | `POST /patients/{patient_id}/medication-statements`, `GET /patients/{patient_id}/medication-statements` | Create/list synthetic patient-linked medication resources. |
| Timeline | `GET /patients/{patient_id}/timeline` | Return Patient, documents and medications, newest first. |
| Consent | `POST /consent/revoke` | Revoke the local Owner's active health-record consent synchronously. |
| Backup | `POST /backup` | Create a passphrase-protected encrypted backup envelope. |
| Restore | `POST /backup/restore` | Validate and restore the encrypted backup; expires all sessions. |
| Recovery | `POST /backup/recover` | Recover into an empty local database using the backup passphrase; unlock afterwards with the restored Owner credentials. Protected by the local IPC channel, not an Owner session. |
| Validate | `POST /backup/validate` | Validate the backup and its schema before the replacement confirmation, with an authorized Owner session. |
| Replace | `POST /backup/replace` | Require an authorized session, backup passphrase, current Owner password and fresh TOTP; transactionally replace the local database and invalidate local sessions. |
| Readiness | `GET /health` | Report local service readiness without exposing health data. |

Start-screen recovery and cross-Owner replacement cannot write an encrypted `BACKUP_RESTORED` audit event:
the Owner data key is unavailable until a subsequent unlock. The restored
database retains the audit records included in the backup; the later unlock
is audited normally. Recovery decrypts the database image in memory, so large
backups increase peak memory usage.

Replacement holds a SQLite write transaction; failed imports roll back. Backup
validation and replacement each decrypt and check the backup, adding latency
and memory usage. A backup saved before replacement is a snapshot: changes
made afterward are not included. Close other application instances before
replacement; cross-process session invalidation and same-user isolation are
not guaranteed. The desktop requires a new destination filename for every
backup and never overwrites an existing file.

## Deliverable 4: SQLite schema

The canonical executable schema is `backend/lifeledger/schema.sql`:

| Table | Contents | At-rest treatment |
| --- | --- | --- |
| `identity_owner` | Owner ID, Argon2 password verifier/salt, wrapped data key, encrypted TOTP secret, setup state | Password verifier and salt are visible; TOTP and data key are encrypted. |
| `patients` | Opaque resource/owner IDs, created-at index, encrypted FHIR JSON | FHIR payload AES-256-GCM. |
| `document_references` | Opaque resource/owner/Patient IDs, created-at index, encrypted FHIR JSON including original bytes | Entire DocumentReference payload AES-256-GCM. |
| `medication_statements` | Opaque resource/owner/Patient IDs, created-at index, encrypted FHIR JSON | FHIR payload AES-256-GCM. |
| `consent` | Opaque consent/owner IDs, active/revoked status, encrypted scope and purpose | Scope/purpose AES-256-GCM; status visible for synchronous checks. |
| `capability_grants` | Opaque grant/owner IDs, active/revoked status, encrypted capability set | Capability set AES-256-GCM. |
| `audit` | Opaque event/owner IDs, event type and timestamp, encrypted details | Details AES-256-GCM; event type and timestamp visible. |
| `event_outbox` | Opaque event/owner IDs, event type/timestamp, encrypted envelope, delivery bit | Envelope AES-256-GCM; routing metadata visible. |
| `metadata` | Schema version | Non-sensitive. |

The database has no plaintext column for names, medication labels, document
content or FHIR JSON. Database-file encryption and complete metadata hiding are
not implemented by this slice.

## Deliverable 6: test plan

### Unit

- Argon2id derives a stable key only for identical password/salt/parameters;
  distinct salts differ; password verification rejects wrong passwords.
- AES-GCM encrypt/decrypt round-trip; wrong key, changed nonce/ciphertext or
  changed associated-data ID fails authentication.
- FHIR resource builders enforce only the three allowed types, required
  references and synthetic marker.
- Document parser rejects invalid Base64, unsupported MIME, bad PDF/PNG
  signatures, invalid UTF-8 and files over 10 MiB.
- Timeline sorts by UTC creation timestamp and never mixes Patient IDs.

### Integration

- Owner bootstrap → MFA confirmation → unlock → create Patient → import
  document → create MedicationStatement → timeline read.
- Verify database transactions atomically include resource, audit and outbox.
- Revoke consent, then prove all resource, timeline and backup operations fail
  closed; verify no change is committed.
- Backup/restore to the same Owner and verify all synthetic resources,
  originals, consent, capability, audit and schema version are present.
- Recover into an empty database without a session; verify wrong passphrases
  and populated databases are rejected and original Owner MFA is still required.
- Inject failure during restore and prove original DB remains readable.

### Offline

- On a clean Windows VM, disable network adapters before launching the
  packaged app; complete setup, CRUD, timeline, backup and restore.
- Verify packaged Python/runtime dependencies and validator assets need no
  network access.
- Confirm service binds only to loopback and stops with the Tauri host.
- Repeat restart, interrupted setup, process termination during a write and
  process termination during backup.

### Negative and security

- Missing/expired token, wrong password, wrong TOTP, revoked consent and
  missing capability are denied.
- Foreign/unknown Patient reference, unsupported resource, malformed FHIR,
  MIME mismatch and oversized document are rejected.
- Modified backup, wrong passphrase, unsupported version, invalid SQLite and
  another Owner's backup are rejected without replacing current data.
- Ensure plaintext markers from all synthetic records/documents are absent
  from SQLite and backup files; ensure logs contain no payload, password,
  TOTP secret, bearer token or encryption key.
- Test repeated concurrent Owner setup, concurrent revoke/write, duplicate
  requests and SQLite busy/error paths.

Windows IPC and service lifecycle remain acceptance gates: the packaged
Tauri-to-service channel pins a per-launch TLS certificate before sending
the IPC secret or API requests. This prevents a different local process from
impersonating the sidecar merely by winning the loopback-port race. Windows
verification is still required, and this design does not claim isolation from
another process running as the same Windows user. The loopback-only
development API is not a substitute for the packaged channel.
