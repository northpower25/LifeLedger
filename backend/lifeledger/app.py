"""FastAPI service for the synthetic-data-only offline vertical slice."""

import hashlib
import hmac
import json
import logging
import os
import secrets
import sqlite3
import tempfile
import threading
import time
import uuid
from datetime import datetime, timedelta, timezone
from html import escape
from pathlib import Path
from typing import Annotated, Any, Literal

import pyotp
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict, StringConstraints

from .crypto import (
    ARGON2_MEMORY_KIB,
    ARGON2_PARALLELISM,
    ARGON2_TIME_COST,
    b64decode,
    b64encode,
    decrypt_bytes,
    decrypt_json,
    derive_key,
    encrypt_bytes,
    encrypt_json,
    hash_password,
    new_data_key,
    new_salt,
    verify_password,
)
from .database import SCHEMA_VERSION, connect, connection, transaction

PASSWORD = Annotated[str, StringConstraints(min_length=12, max_length=256)]
NAME = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]
BACKUP_AAD = b"LifeLedger offline backup v1"
LOGGER = logging.getLogger(__name__)
MAX_DOCUMENT_BYTES = 10 * 1024 * 1024
MAX_BACKUP_DATABASE_BYTES = 64 * 1024 * 1024
SESSION_LIFETIME = timedelta(minutes=30)
CAPABILITIES = {
    "Patient": {"read": "READ_PATIENT", "write": "WRITE_PATIENT"},
    "DocumentReference": {
        "read": "READ_DOCUMENT",
        "write": "WRITE_DOCUMENT",
    },
    "MedicationStatement": {
        "read": "READ_MEDICATION",
        "write": "WRITE_MEDICATION",
    },
    "Backup": {"create": "CREATE_BACKUP", "restore": "RESTORE_BACKUP"},
}
TABLES: dict[str, tuple[str, str]] = {
    "Patient": ("patients", "resource_id"),
    "DocumentReference": ("document_references", "resource_id"),
    "MedicationStatement": ("medication_statements", "resource_id"),
}
RESOURCE_EVENTS = {
    "Patient": "fhir.created.v1",
    "DocumentReference": "fhir.created.v1",
    "MedicationStatement": "fhir.created.v1",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def default_database_path() -> Path:
    if os.name == "nt":
        local_app_data = os.environ.get("LOCALAPPDATA")
        base = Path(local_app_data) if local_app_data else Path.home() / "AppData" / "Local"
        return base / "LifeLedger" / "lifeledger.sqlite3"
    return Path.home() / ".local" / "share" / "LifeLedger" / "lifeledger.sqlite3"


def _seal(key: bytes, table: str, resource_id: str, payload: Any) -> bytes:
    return encrypt_json(key, payload, f"{table}:{resource_id}".encode())


def _open(key: bytes, table: str, resource_id: str, payload: bytes) -> Any:
    return decrypt_json(key, payload, f"{table}:{resource_id}".encode())


def _seal_resource(
    key: bytes, table: str, resource_id: str, resource: dict[str, Any]
) -> bytes:
    original_id = resource_id
    transformations: list[str] = []
    if resource["resourceType"] == "DocumentReference":
        attachment = resource["content"][0]["attachment"]
        original_id = attachment["hash"]
        transformations = ["base64_decode", "mime_signature_check"]
    envelope = {
        "resource": resource,
        "provenance": {
            "source": "MANUAL_ENTRY",
            "connector_id": None,
            "original_id": original_id,
            "recorded_at": utc_now(),
            "version": 1,
            "transformations": transformations,
        },
    }
    return _seal(key, table, resource_id, envelope)


def _open_resource(
    key: bytes, table: str, resource_id: str, payload: bytes
) -> dict[str, Any]:
    return _open(key, table, resource_id, payload)["resource"]


def _totp_step(secret: str, code: str, last_step: int | None) -> int | None:
    current_step = int(time.time() // 30)
    totp = pyotp.TOTP(secret)
    for candidate in range(current_step - 1, current_step + 2):
        if (last_step is None or candidate > last_step) and hmac.compare_digest(
            totp.at(candidate * 30), code
        ):
            return candidate
    return None


class OwnerSetup(BaseModel):
    model_config = ConfigDict(extra="forbid")
    display_name: NAME
    password: PASSWORD


class TotpConfirmation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    password: PASSWORD
    code: Annotated[str, StringConstraints(pattern=r"^\d{6}$")]


class SetupResume(BaseModel):
    model_config = ConfigDict(extra="forbid")
    password: PASSWORD


class UnlockRequest(TotpConfirmation):
    pass


class PatientCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: NAME
    synthetic: Literal[True]


class DocumentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    patient_id: str
    title: NAME
    content_type: Literal["application/pdf", "text/plain", "image/png"]
    content_base64: Annotated[str, StringConstraints(min_length=4, max_length=14_000_000)]
    synthetic: Literal[True]


class MedicationCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    patient_id: str
    medication_text: NAME
    status: Literal["active", "completed", "not-taken", "on-hold", "stopped", "unknown"] = "active"
    effective_datetime: datetime
    synthetic: Literal[True]


class BackupCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    passphrase: PASSWORD


class BackupRestore(BaseModel):
    model_config = ConfigDict(extra="forbid")
    passphrase: PASSWORD
    backup_base64: Annotated[str, StringConstraints(min_length=64, max_length=100_000_000)]


class OwnerStatusResponse(BaseModel):
    owner_exists: bool
    owner_confirmed: bool


class OwnerSetupResponse(BaseModel):
    owner_id: str
    totp_secret: str
    totp_uri: str
    status: Literal["pending_mfa_confirmation"]


class SessionResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"]
    expires_in: int


class FhirReference(BaseModel):
    reference: str


class FhirExtension(BaseModel):
    url: str
    valueBoolean: bool


class FhirHumanName(BaseModel):
    text: str


class FhirNarrative(BaseModel):
    status: Literal["generated"]
    div: str


class PatientResource(BaseModel):
    resourceType: Literal["Patient"]
    id: str
    active: bool
    name: list[FhirHumanName]
    extension: list[FhirExtension]
    text: FhirNarrative


class DocumentAttachment(BaseModel):
    contentType: Literal["application/pdf", "text/plain", "image/png"]
    title: str
    size: int
    hash: str
    data: str


class DocumentContent(BaseModel):
    attachment: DocumentAttachment


class DocumentReferenceResource(BaseModel):
    resourceType: Literal["DocumentReference"]
    id: str
    status: Literal["current"]
    subject: FhirReference
    date: datetime
    content: list[DocumentContent]
    extension: list[FhirExtension]


class MedicationConcept(BaseModel):
    text: str


class MedicationStatementResource(BaseModel):
    resourceType: Literal["MedicationStatement"]
    id: str
    status: Literal["active", "completed", "not-taken", "on-hold", "stopped", "unknown"]
    medicationCodeableConcept: MedicationConcept
    subject: FhirReference
    effectiveDateTime: datetime
    dateAsserted: datetime
    extension: list[FhirExtension]


class TimelineEntry(BaseModel):
    occurred_at: datetime
    resource_type: Literal["Patient", "DocumentReference", "MedicationStatement"]
    resource: PatientResource | DocumentReferenceResource | MedicationStatementResource


class BackupResponse(BaseModel):
    backup_base64: str
    sha256: str


class Session:
    def __init__(self, owner_id: str, key: bytes) -> None:
        self.owner_id = owner_id
        self.key = key
        self.expires_at = datetime.now(timezone.utc) + SESSION_LIFETIME


class SessionStore:
    def __init__(self) -> None:
        self._sessions: dict[str, Session] = {}
        self._lock = threading.Lock()

    def issue(self, owner_id: str, key: bytes) -> str:
        token = secrets.token_urlsafe(32)
        with self._lock:
            self._sessions.clear()
            self._sessions[token] = Session(owner_id, key)
        return token

    def resolve(self, token: str | None) -> Session:
        if not token:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "session_required")
        with self._lock:
            session = self._sessions.get(token)
            if session is None or session.expires_at <= datetime.now(timezone.utc):
                self._sessions.pop(token, None)
                raise HTTPException(status.HTTP_401_UNAUTHORIZED, "session_expired")
            return session

    def clear(self) -> None:
        with self._lock:
            self._sessions.clear()


def _password_valid(stored_hash: str, password: str) -> bool:
    return verify_password(stored_hash, password)


def _owner_row(connection: sqlite3.Connection) -> sqlite3.Row | None:
    return connection.execute(
        "SELECT * FROM identity_owner LIMIT 1"
    ).fetchone()


def _unlock_key(owner: sqlite3.Row, password: str) -> bytes | None:
    if not _password_valid(owner["password_hash"], password):
        return None
    wrap_key = derive_key(password, owner["kdf_salt"])
    try:
        return decrypt_bytes(
            wrap_key, owner["wrapped_key"], f"owner-key:{owner['owner_id']}".encode()
        )
    except (InvalidTag, ValueError):
        return None


def _audit(
    connection: sqlite3.Connection,
    owner_id: str,
    key: bytes,
    event_type: str,
    details: dict[str, Any],
) -> None:
    event_id = str(uuid.uuid4())
    occurred_at = utc_now()
    payload = _seal(key, "audit", event_id, {
        "actor": owner_id,
        "action": event_type,
        "result": "success",
        **details,
    })
    connection.execute(
        "INSERT INTO audit(event_id, owner_id, event_type, occurred_at, payload) "
        "VALUES (?, ?, ?, ?, ?)",
        (event_id, owner_id, event_type, occurred_at, payload),
    )


def _outbox(
    connection: sqlite3.Connection,
    owner_id: str,
    key: bytes,
    event_type: str,
    subject: str,
) -> None:
    event_id = str(uuid.uuid4())
    occurred_at = utc_now()
    payload = {
        "event_id": event_id,
        "event_type": event_type,
        "subject": subject,
    }
    connection.execute(
        "INSERT INTO event_outbox(event_id, owner_id, event_type, occurred_at, payload) "
        "VALUES (?, ?, ?, ?, ?)",
        (
            event_id,
            owner_id,
            event_type,
            occurred_at,
            _seal(key, "event_outbox", event_id, payload),
        ),
    )


def _authorize(
    connection: sqlite3.Connection,
    session: Session,
    resource_type: str,
    operation: str,
) -> None:
    required = CAPABILITIES.get(resource_type, {}).get(operation)
    if required is None:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "capability_denied")
    consent_rows = connection.execute(
        "SELECT consent_id, payload FROM consent WHERE owner_id = ? AND status = 'ACTIVE'",
        (session.owner_id,),
    ).fetchall()
    consent_allowed = False
    for row in consent_rows:
        payload = _open(session.key, "consent", row["consent_id"], row["payload"])
        if (
            resource_type in payload["resource_types"]
            and operation in payload["operations"]
        ):
            consent_allowed = True
            break
    grant_rows = connection.execute(
        "SELECT grant_id, payload FROM capability_grants "
        "WHERE owner_id = ? AND status = 'ACTIVE'",
        (session.owner_id,),
    ).fetchall()
    capability_allowed = any(
        required in _open(session.key, "capability_grants", row["grant_id"], row["payload"])["capabilities"]
        for row in grant_rows
    )
    if not consent_allowed or not capability_allowed:
        _audit(connection, session.owner_id, session.key, "ACCESS_DENIED", {
            "resource_type": resource_type,
            "operation": operation,
        })
        connection.commit()
        raise HTTPException(status.HTTP_403_FORBIDDEN, "consent_or_capability_denied")


def _record_resource(
    connection: sqlite3.Connection,
    session: Session,
    resource_type: str,
    resource_id: str,
    patient_id: str | None,
    resource: dict[str, Any],
) -> None:
    table, _ = TABLES[resource_type]
    created_at = utc_now()
    payload = _seal_resource(session.key, table, resource_id, resource)
    if resource_type == "Patient":
        connection.execute(
            "INSERT INTO patients(resource_id, owner_id, created_at, payload) "
            "VALUES (?, ?, ?, ?)",
            (resource_id, session.owner_id, created_at, payload),
        )
    else:
        if patient_id is None:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "patient_required")
        exists = connection.execute(
            "SELECT 1 FROM patients WHERE resource_id = ? AND owner_id = ?",
            (patient_id, session.owner_id),
        ).fetchone()
        if exists is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "patient_not_found")
        target = (
            "document_references"
            if resource_type == "DocumentReference"
            else "medication_statements"
        )
        connection.execute(
            f"INSERT INTO {target}(resource_id, owner_id, patient_id, created_at, payload) "
            "VALUES (?, ?, ?, ?, ?)",
            (resource_id, session.owner_id, patient_id, created_at, payload),
        )
    _audit(connection, session.owner_id, session.key, "FHIR_CREATED", {
        "resource_type": resource_type,
        "resource_id": resource_id,
    })
    _outbox(
        connection,
        session.owner_id,
        session.key,
        RESOURCE_EVENTS[resource_type],
        resource_id,
    )


def create_app(
    database_path: str | Path | None = None,
    *,
    ipc_secret: bytes | None = None,
    dev_api: bool = False,
) -> FastAPI:
    configured_path = database_path or os.environ.get(
        "LIFELEDGER_DATABASE",
        str(default_database_path()),
    )
    db_path = Path(configured_path)
    sessions = SessionStore()
    app = FastAPI(
        title="LifeLedger Offline Slice API",
        version="1.0.0",
        description=(
            "Local-only API for synthetic Patient, DocumentReference and "
            "MedicationStatement data."
        ),
    )
    app.state.database_path = db_path
    app.state.sessions = sessions
    app.state.ipc_secret = ipc_secret
    app.state.dev_api = (
        ipc_secret is None
        and (
            dev_api
            or os.environ.get("LIFELEDGER_DEV_MODE") == "1"
        )
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "tauri://localhost",
            "http://tauri.localhost",
            "http://localhost:1420",
        ],
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["Authorization", "Content-Type"],
    )

    @app.middleware("http")
    async def require_tauri_ipc(request: Request, call_next):
        if app.state.ipc_secret is not None:
            supplied = request.headers.get("X-LifeLedger-IPC", "").encode()
            expected = app.state.ipc_secret.hex().encode()
            if not hmac.compare_digest(supplied, expected):
                return Response(status_code=status.HTTP_403_FORBIDDEN)
        elif not app.state.dev_api:
            return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
        return await call_next(request)

    bearer = HTTPBearer(auto_error=False)

    def get_session(
        credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
    ) -> Session:
        if credentials is None or credentials.scheme.lower() != "bearer":
            return sessions.resolve(None)
        return sessions.resolve(credentials.credentials)

    SessionDependency = Annotated[Session, Depends(get_session)]

    @app.get("/api/v1/health", tags=["System"])
    def health() -> dict[str, str | int]:
        return {"status": "ok", "mode": "offline", "pid": os.getpid()}

    @app.get(
        "/api/v1/owner/status",
        response_model=OwnerStatusResponse,
        tags=["Owner"],
    )
    def owner_status() -> OwnerStatusResponse:
        with connection(db_path) as db:
            owner = _owner_row(db)
        return OwnerStatusResponse(
            owner_exists=owner is not None,
            owner_confirmed=bool(owner["confirmed"]) if owner else False,
        )

    @app.post(
        "/api/v1/owner/setup",
        status_code=status.HTTP_201_CREATED,
        response_model=OwnerSetupResponse,
        tags=["Owner"],
    )
    def setup_owner(request: OwnerSetup) -> OwnerSetupResponse:
        with transaction(db_path) as connection:
            if _owner_row(connection) is not None:
                raise HTTPException(status.HTTP_409_CONFLICT, "owner_already_exists")
            owner_id = str(uuid.uuid4())
            salt = new_salt()
            data_key = new_data_key()
            wrapping_key = derive_key(request.password, salt)
            wrapped_key = encrypt_bytes(
                wrapping_key, data_key, f"owner-key:{owner_id}".encode()
            )
            totp_secret = pyotp.random_base32()
            totp_ciphertext = encrypt_bytes(
                data_key, totp_secret.encode(), f"owner-totp:{owner_id}".encode()
            )
            connection.execute(
                "INSERT INTO identity_owner(owner_id, password_hash, kdf_salt, "
                "wrapped_key, totp_ciphertext, confirmed, last_totp_step) "
                "VALUES (?, ?, ?, ?, ?, 0, NULL)",
                (
                    owner_id,
                    hash_password(request.password),
                    salt,
                    wrapped_key,
                    totp_ciphertext,
                ),
            )
            consent_id = str(uuid.uuid4())
            consent_payload = {
                "owner_id": owner_id,
                "resource_types": [
                    "Patient",
                    "DocumentReference",
                    "MedicationStatement",
                    "Backup",
                ],
                "operations": ["read", "write", "create", "restore"],
                "purpose": "health_record",
            }
            connection.execute(
                "INSERT INTO consent(consent_id, owner_id, status, payload) "
                "VALUES (?, ?, 'ACTIVE', ?)",
                (
                    consent_id,
                    owner_id,
                    _seal(data_key, "consent", consent_id, consent_payload),
                ),
            )
            grant_id = str(uuid.uuid4())
            capability_payload = {
                "owner_id": owner_id,
                "capabilities": [
                    "READ_PATIENT",
                    "WRITE_PATIENT",
                    "READ_DOCUMENT",
                    "WRITE_DOCUMENT",
                    "READ_MEDICATION",
                    "WRITE_MEDICATION",
                    "CREATE_BACKUP",
                    "RESTORE_BACKUP",
                ],
            }
            connection.execute(
                "INSERT INTO capability_grants(grant_id, owner_id, status, payload) "
                "VALUES (?, ?, 'ACTIVE', ?)",
                (
                    grant_id,
                    owner_id,
                    _seal(data_key, "capability_grants", grant_id, capability_payload),
                ),
            )
            _audit(connection, owner_id, data_key, "OWNER_CREATED", {
                "display_name": request.display_name,
            })
            _outbox(connection, owner_id, data_key, "identity.user_created.v1", owner_id)
            _outbox(connection, owner_id, data_key, "consent.granted.v1", consent_id)
        return OwnerSetupResponse(
            owner_id=owner_id,
            totp_secret=totp_secret,
            totp_uri=pyotp.TOTP(totp_secret).provisioning_uri(
                name=request.display_name, issuer_name="LifeLedger"
            ),
            status="pending_mfa_confirmation",
        )

    @app.post("/api/v1/owner/setup/resume", tags=["Owner"])
    def resume_owner_setup(request: SetupResume) -> dict[str, str]:
        with transaction(db_path) as db:
            owner = _owner_row(db)
            if owner is None or owner["confirmed"]:
                raise HTTPException(status.HTTP_404_NOT_FOUND, "pending_setup_not_found")
            data_key = _unlock_key(owner, request.password)
            if data_key is None:
                raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid_credentials")
            secret = decrypt_bytes(
                data_key,
                owner["totp_ciphertext"],
                f"owner-totp:{owner['owner_id']}".encode(),
            ).decode()
            _audit(db, owner["owner_id"], data_key, "OWNER_SETUP_RESUMED", {})
        return {"totp_secret": secret}

    @app.post(
        "/api/v1/owner/setup/confirm",
        response_model=SessionResponse,
        tags=["Owner"],
    )
    def confirm_owner(request: TotpConfirmation) -> SessionResponse:
        with transaction(db_path) as connection:
            owner = _owner_row(connection)
            if owner is None or owner["confirmed"]:
                raise HTTPException(status.HTTP_404_NOT_FOUND, "pending_setup_not_found")
            data_key = _unlock_key(owner, request.password)
            if data_key is None:
                raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid_credentials")
            secret = decrypt_bytes(
                data_key,
                owner["totp_ciphertext"],
                f"owner-totp:{owner['owner_id']}".encode(),
            ).decode()
            step = _totp_step(secret, request.code, owner["last_totp_step"])
            if step is None:
                raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid_mfa_code")
            connection.execute(
                "UPDATE identity_owner SET confirmed = 1, last_totp_step = ? "
                "WHERE owner_id = ?",
                (step, owner["owner_id"]),
            )
            _audit(connection, owner["owner_id"], data_key, "OWNER_MFA_CONFIRMED", {})
        return SessionResponse(
            access_token=sessions.issue(owner["owner_id"], data_key),
            token_type="bearer",
            expires_in=int(SESSION_LIFETIME.total_seconds()),
        )

    @app.post("/api/v1/owner/unlock", response_model=SessionResponse, tags=["Owner"])
    def unlock_owner(request: UnlockRequest) -> SessionResponse:
        with transaction(db_path) as connection:
            owner = _owner_row(connection)
            if owner is None or not owner["confirmed"]:
                raise HTTPException(status.HTTP_409_CONFLICT, "owner_setup_required")
            data_key = _unlock_key(owner, request.password)
            if data_key is None:
                raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid_credentials")
            secret = decrypt_bytes(
                data_key,
                owner["totp_ciphertext"],
                f"owner-totp:{owner['owner_id']}".encode(),
            ).decode()
            step = _totp_step(secret, request.code, owner["last_totp_step"])
            if step is None:
                raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid_mfa_code")
            connection.execute(
                "UPDATE identity_owner SET last_totp_step = ? WHERE owner_id = ?",
                (step, owner["owner_id"]),
            )
            _audit(connection, owner["owner_id"], data_key, "OWNER_UNLOCKED", {})
        return SessionResponse(
            access_token=sessions.issue(owner["owner_id"], data_key),
            token_type="bearer",
            expires_in=int(SESSION_LIFETIME.total_seconds()),
        )

    @app.post("/api/v1/owner/lock", status_code=status.HTTP_204_NO_CONTENT, tags=["Owner"])
    def lock_owner(session: SessionDependency) -> Response:
        with transaction(db_path) as db:
            _audit(db, session.owner_id, session.key, "OWNER_LOCKED", {})
        sessions.clear()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @app.post(
        "/api/v1/patients",
        status_code=status.HTTP_201_CREATED,
        response_model=PatientResource,
        tags=["Patient"],
    )
    def create_patient(
        request: PatientCreate, session: SessionDependency
    ) -> dict[str, Any]:
        patient_id = str(uuid.uuid4())
        resource = {
            "resourceType": "Patient",
            "id": patient_id,
            "active": True,
            "name": [{"text": request.name}],
            "extension": [{"url": "urn:lifeledger:synthetic-data", "valueBoolean": True}],
            "text": {"status": "generated", "div": f"<div>{escape(request.name)}</div>"},
        }
        with transaction(db_path) as connection:
            _authorize(connection, session, "Patient", "write")
            _record_resource(connection, session, "Patient", patient_id, None, resource)
        return resource

    @app.get("/api/v1/patients", response_model=list[PatientResource], tags=["Patient"])
    def list_patients(session: SessionDependency) -> list[dict[str, Any]]:
        with transaction(db_path) as connection:
            _authorize(connection, session, "Patient", "read")
            rows = connection.execute(
                "SELECT resource_id, payload FROM patients WHERE owner_id = ? ORDER BY created_at",
                (session.owner_id,),
            ).fetchall()
            for row in rows:
                _audit(connection, session.owner_id, session.key, "FHIR_READ", {
                    "resource_type": "Patient",
                    "resource_id": row["resource_id"],
                })
            return [
                _open_resource(session.key, "patients", row["resource_id"], row["payload"])
                for row in rows
            ]

    @app.post(
        "/api/v1/patients/{patient_id}/documents",
        status_code=status.HTTP_201_CREATED,
        response_model=DocumentReferenceResource,
        tags=["DocumentReference"],
    )
    def import_document(
        patient_id: str, request: DocumentCreate, session: SessionDependency
    ) -> dict[str, Any]:
        if request.patient_id != patient_id:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "patient_id_mismatch")
        try:
            content = b64decode(request.content_base64)
        except ValueError as exc:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "invalid_base64") from exc
        if not content or len(content) > MAX_DOCUMENT_BYTES:
            raise HTTPException(status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, "document_size_out_of_range")
        if request.content_type == "application/pdf" and not content.startswith(b"%PDF-"):
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "document_type_mismatch")
        if request.content_type == "image/png" and not content.startswith(b"\x89PNG\r\n\x1a\n"):
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "document_type_mismatch")
        if request.content_type == "text/plain":
            try:
                content.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "document_type_mismatch") from exc
        document_id = str(uuid.uuid4())
        now = utc_now()
        resource = {
            "resourceType": "DocumentReference",
            "id": document_id,
            "status": "current",
            "subject": {"reference": f"Patient/{patient_id}"},
            "date": now,
            "content": [{
                "attachment": {
                    "contentType": request.content_type,
                    "title": request.title,
                    "size": len(content),
                    "hash": b64encode(hashlib.sha256(content).digest()),
                    "data": b64encode(content),
                }
            }],
            "extension": [{"url": "urn:lifeledger:synthetic-data", "valueBoolean": True}],
        }
        with transaction(db_path) as connection:
            _authorize(connection, session, "DocumentReference", "write")
            _record_resource(
                connection, session, "DocumentReference", document_id, patient_id, resource
            )
        return resource

    @app.get(
        "/api/v1/patients/{patient_id}/documents",
        response_model=list[DocumentReferenceResource],
        tags=["DocumentReference"],
    )
    def list_documents(patient_id: str, session: SessionDependency) -> list[dict[str, Any]]:
        with transaction(db_path) as connection:
            _authorize(connection, session, "DocumentReference", "read")
            rows = connection.execute(
                "SELECT resource_id, payload FROM document_references "
                "WHERE owner_id = ? AND patient_id = ? ORDER BY created_at",
                (session.owner_id, patient_id),
            ).fetchall()
            for row in rows:
                _audit(connection, session.owner_id, session.key, "FHIR_READ", {
                    "resource_type": "DocumentReference",
                    "resource_id": row["resource_id"],
                })
            return [
                _open_resource(session.key, "document_references", row["resource_id"], row["payload"])
                for row in rows
            ]

    @app.post(
        "/api/v1/patients/{patient_id}/medication-statements",
        status_code=status.HTTP_201_CREATED,
        response_model=MedicationStatementResource,
        tags=["MedicationStatement"],
    )
    def create_medication(
        patient_id: str, request: MedicationCreate, session: SessionDependency
    ) -> dict[str, Any]:
        if request.patient_id != patient_id:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "patient_id_mismatch")
        if request.effective_datetime.tzinfo is None:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "timezone_required")
        medication_id = str(uuid.uuid4())
        effective = request.effective_datetime.astimezone(timezone.utc).isoformat()
        resource = {
            "resourceType": "MedicationStatement",
            "id": medication_id,
            "status": request.status,
            "medicationCodeableConcept": {"text": request.medication_text},
            "subject": {"reference": f"Patient/{patient_id}"},
            "effectiveDateTime": effective,
            "dateAsserted": utc_now(),
            "extension": [{"url": "urn:lifeledger:synthetic-data", "valueBoolean": True}],
        }
        with transaction(db_path) as connection:
            _authorize(connection, session, "MedicationStatement", "write")
            _record_resource(
                connection,
                session,
                "MedicationStatement",
                medication_id,
                patient_id,
                resource,
            )
        return resource

    @app.get(
        "/api/v1/patients/{patient_id}/medication-statements",
        response_model=list[MedicationStatementResource],
        tags=["MedicationStatement"],
    )
    def list_medications(patient_id: str, session: SessionDependency) -> list[dict[str, Any]]:
        with transaction(db_path) as connection:
            _authorize(connection, session, "MedicationStatement", "read")
            rows = connection.execute(
                "SELECT resource_id, payload FROM medication_statements "
                "WHERE owner_id = ? AND patient_id = ? ORDER BY created_at",
                (session.owner_id, patient_id),
            ).fetchall()
            for row in rows:
                _audit(connection, session.owner_id, session.key, "FHIR_READ", {
                    "resource_type": "MedicationStatement",
                    "resource_id": row["resource_id"],
                })
            return [
            _open_resource(session.key, "medication_statements", row["resource_id"], row["payload"])
                for row in rows
            ]

    @app.get(
        "/api/v1/patients/{patient_id}/timeline",
        response_model=list[TimelineEntry],
        tags=["Timeline"],
    )
    def timeline(patient_id: str, session: SessionDependency) -> list[dict[str, Any]]:
        with transaction(db_path) as connection:
            for resource_type in ("Patient", "DocumentReference", "MedicationStatement"):
                _authorize(connection, session, resource_type, "read")
            patient = connection.execute(
                "SELECT resource_id, created_at, payload FROM patients "
                "WHERE owner_id = ? AND resource_id = ?",
                (session.owner_id, patient_id),
            ).fetchone()
            if patient is None:
                raise HTTPException(status.HTTP_404_NOT_FOUND, "patient_not_found")
            records = [{
                "occurred_at": patient["created_at"],
                "resource_type": "Patient",
                "resource": _open_resource(session.key, "patients", patient_id, patient["payload"]),
            }]
            for resource_type, table in (
                ("DocumentReference", "document_references"),
                ("MedicationStatement", "medication_statements"),
            ):
                rows = connection.execute(
                    f"SELECT resource_id, created_at, payload FROM {table} "
                    "WHERE owner_id = ? AND patient_id = ?",
                    (session.owner_id, patient_id),
                ).fetchall()
                for row in rows:
                    _audit(connection, session.owner_id, session.key, "FHIR_READ", {
                        "resource_type": resource_type,
                        "resource_id": row["resource_id"],
                    })
                records.extend({
                    "occurred_at": row["created_at"],
                    "resource_type": resource_type,
                    "resource": _open_resource(session.key, table, row["resource_id"], row["payload"]),
                } for row in rows)
            _audit(connection, session.owner_id, session.key, "TIMELINE_READ", {
                "patient_id": patient_id,
            })
            return sorted(records, key=lambda record: record["occurred_at"], reverse=True)

    @app.post("/api/v1/consent/revoke", status_code=status.HTTP_204_NO_CONTENT, tags=["Consent"])
    def revoke_consent(session: SessionDependency) -> Response:
        with transaction(db_path) as connection:
            rows = connection.execute(
                "SELECT consent_id FROM consent WHERE owner_id = ? AND status = 'ACTIVE'",
                (session.owner_id,),
            ).fetchall()
            connection.execute(
                "UPDATE consent SET status = 'REVOKED' WHERE owner_id = ?",
                (session.owner_id,),
            )
            _audit(connection, session.owner_id, session.key, "CONSENT_REVOKED", {
                "consent_ids": [row["consent_id"] for row in rows],
            })
            _outbox(
                connection,
                session.owner_id,
                session.key,
                "consent.revoked.v1",
                session.owner_id,
            )
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @app.post(
        "/api/v1/backup",
        response_model=BackupResponse,
        tags=["Backup"],
    )
    def create_backup(
        request: BackupCreate, session: SessionDependency
    ) -> dict[str, str]:
        with transaction(db_path) as connection:
            _authorize(connection, session, "Backup", "create")
            _audit(connection, session.owner_id, session.key, "BACKUP_CREATED", {})
            _outbox(
                connection,
                session.owner_id,
                session.key,
                "backup.created.v1",
                session.owner_id,
            )
        source = sqlite3.connect(db_path)
        destination = sqlite3.connect(":memory:")
        try:
            source.backup(destination)
            raw = destination.serialize()
        finally:
            destination.close()
            source.close()
        if len(raw) > MAX_BACKUP_DATABASE_BYTES:
            raise HTTPException(
                status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, "backup_size_out_of_range"
            )
        salt = new_salt()
        backup_key = derive_key(request.passphrase, salt)
        nonce = os.urandom(12)
        ciphertext = AESGCM(backup_key).encrypt(nonce, raw, BACKUP_AAD)
        envelope = {
            "format": "lifledger-backup",
            "version": 1,
            "kdf": {
                "name": "Argon2id",
                "time_cost": ARGON2_TIME_COST,
                "memory_kib": ARGON2_MEMORY_KIB,
                "parallelism": ARGON2_PARALLELISM,
                "salt": b64encode(salt),
            },
            "cipher": {"name": "AES-256-GCM", "nonce": b64encode(nonce)},
            "ciphertext": b64encode(ciphertext),
        }
        packed = json.dumps(envelope, separators=(",", ":"), sort_keys=True).encode()
        return {"backup_base64": b64encode(packed), "sha256": hashlib.sha256(packed).hexdigest()}

    @app.post("/api/v1/backup/restore", status_code=status.HTTP_204_NO_CONTENT, tags=["Backup"])
    def restore_backup(request: BackupRestore, session: SessionDependency) -> Response:
        with transaction(db_path) as db:
            _authorize(db, session, "Backup", "restore")
        try:
            envelope = json.loads(b64decode(request.backup_base64))
            if not isinstance(envelope, dict):
                raise ValueError("invalid backup envelope")
            kdf = envelope.get("kdf")
            cipher = envelope.get("cipher")
            if not isinstance(kdf, dict) or not isinstance(cipher, dict):
                raise ValueError("invalid backup parameters")
            if envelope.get("format") != "lifledger-backup" or envelope.get("version") != 1:
                raise ValueError("unsupported backup")
            if kdf.get("name") != "Argon2id":
                raise ValueError("unsupported kdf")
            if (
                kdf.get("time_cost") != ARGON2_TIME_COST
                or kdf.get("memory_kib") != ARGON2_MEMORY_KIB
                or kdf.get("parallelism") != ARGON2_PARALLELISM
            ):
                raise ValueError("unsupported kdf parameters")
            if cipher.get("name") != "AES-256-GCM":
                raise ValueError("unsupported cipher")
            salt = b64decode(kdf["salt"])
            nonce = b64decode(cipher["nonce"])
            if len(salt) != 16 or len(nonce) != 12:
                raise ValueError("invalid backup parameters")
            backup_key = derive_key(
                request.passphrase, salt
            )
            plaintext = AESGCM(backup_key).decrypt(
                nonce,
                b64decode(envelope["ciphertext"]),
                BACKUP_AAD,
            )
        except (ValueError, KeyError, TypeError, json.JSONDecodeError, InvalidTag) as exc:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "invalid_backup") from exc
        fd, temporary_name = tempfile.mkstemp(
            prefix="lifledger-restore-", suffix=".sqlite3", dir=db_path.parent
        )
        os.close(fd)
        temporary_path = Path(temporary_name)
        replacement_path = db_path.with_suffix(db_path.suffix + ".previous")
        try:
            if len(plaintext) > MAX_BACKUP_DATABASE_BYTES:
                raise ValueError("backup exceeds size limit")
            temporary_path.write_bytes(plaintext)
            restored = sqlite3.connect(
                f"{temporary_path.as_uri()}?mode=ro", uri=True
            )
            restored.row_factory = sqlite3.Row
            try:
                check = restored.execute("PRAGMA integrity_check").fetchone()[0]
                version = restored.execute(
                    "SELECT value FROM metadata WHERE key = 'schema_version'"
                ).fetchone()
                restored_owner = _owner_row(restored)
                tables = {
                    row["name"]
                    for row in restored.execute(
                        "SELECT name FROM sqlite_master WHERE type = 'table'"
                    )
                }
                if (
                    check != "ok"
                    or version is None
                    or version["value"] != SCHEMA_VERSION
                    or restored_owner is None
                    or restored_owner["owner_id"] != session.owner_id
                    or not restored_owner["confirmed"]
                    or not {
                        "identity_owner",
                        "patients",
                        "document_references",
                        "medication_statements",
                        "consent",
                        "capability_grants",
                        "audit",
                        "event_outbox",
                        "metadata",
                    }.issubset(tables)
                ):
                    raise ValueError("backup database validation failed")
            finally:
                restored.close()
            with connection(db_path) as current:
                check = current.execute("PRAGMA integrity_check").fetchone()[0]
                if check != "ok":
                    raise HTTPException(status.HTTP_409_CONFLICT, "current_database_invalid")
            os.replace(db_path, replacement_path)
            try:
                os.replace(temporary_path, db_path)
                with transaction(db_path) as restored:
                    _audit(restored, session.owner_id, session.key, "BACKUP_RESTORED", {})
            except Exception:
                if db_path.exists():
                    db_path.unlink()
                os.replace(replacement_path, db_path)
                raise
            replacement_path.unlink(missing_ok=True)
            sessions.clear()
        except HTTPException:
            raise
        except (OSError, sqlite3.Error, ValueError) as exc:
            LOGGER.exception("Backup restore failed")
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "backup_restore_failed") from exc
        finally:
            temporary_path.unlink(missing_ok=True)
            replacement_path.unlink(missing_ok=True)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @app.get("/api/v1/openapi.json", include_in_schema=False)
    def openapi_json() -> dict[str, Any]:
        return app.openapi()

    return app


app = create_app()


def run() -> None:
    import argparse
    import sys

    import uvicorn

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=int(os.environ.get("LIFELEDGER_PORT", "8765")))
    parser.add_argument("--ipc-stdin", action="store_true")
    arguments = parser.parse_args()
    if arguments.ipc_stdin:
        secret_hex = sys.stdin.buffer.readline(129).strip()
        try:
            secret = bytes.fromhex(secret_hex.decode("ascii"))
        except (UnicodeDecodeError, ValueError) as exc:
            raise RuntimeError("Invalid host IPC initialization") from exc
        if len(secret) != 32:
            raise RuntimeError("Invalid host IPC initialization")
        app.state.ipc_secret = secret
        app.state.dev_api = False
    elif os.environ.get("LIFELEDGER_DEV_MODE") != "1":
        raise RuntimeError("Use the Tauri host to start the protected API service")
    uvicorn.run(
        "lifeledger.app:app",
        host="127.0.0.1",
        port=arguments.port,
        reload=False,
        log_level="info",
    )


if __name__ == "__main__":
    run()
