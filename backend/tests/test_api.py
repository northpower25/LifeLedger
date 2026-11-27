import base64
import json
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path

import pyotp
from fastapi.testclient import TestClient

from lifeledger.app import create_app


PASSWORD = "synthetic-owner-password-1"
BACKUP_PASSWORD = "synthetic-backup-password-1"


def create_client(tmp_path):
    database = tmp_path / "lifeledger.sqlite3"
    client = TestClient(create_app(database, dev_api=True))
    setup = client.post(
        "/api/v1/owner/setup",
        json={"display_name": "Synthetic Owner", "password": PASSWORD},
    )
    assert setup.status_code == 201
    secret = setup.json()["totp_secret"]
    confirmation_code = pyotp.TOTP(secret).now()
    confirmation = client.post(
        "/api/v1/owner/setup/confirm",
        json={"password": PASSWORD, "code": confirmation_code},
    )
    assert confirmation.status_code == 200
    client.headers["Authorization"] = (
        f"Bearer {confirmation.json()['access_token']}"
    )
    return client, database, secret, confirmation_code


def test_offline_health_record_journey_and_encrypted_backup_restore(tmp_path):
    client, database, totp_secret, _ = create_client(tmp_path)

    patient_response = client.post(
        "/api/v1/patients",
        json={"name": "Synthetic Patient Marker", "synthetic": True},
    )
    assert patient_response.status_code == 201
    patient = patient_response.json()
    patient_id = patient["id"]

    pdf = b"%PDF-1.7\nsynthetic document marker\n"
    document_response = client.post(
        f"/api/v1/patients/{patient_id}/documents",
        json={
            "patient_id": patient_id,
            "title": "Synthetic document",
            "content_type": "application/pdf",
            "content_base64": base64.b64encode(pdf).decode(),
            "synthetic": True,
        },
    )
    assert document_response.status_code == 201
    document = document_response.json()

    medication_response = client.post(
        f"/api/v1/patients/{patient_id}/medication-statements",
        json={
            "patient_id": patient_id,
            "medication_text": "Synthetic medication",
            "effective_datetime": datetime.now(timezone.utc).isoformat(),
            "synthetic": True,
        },
    )
    assert medication_response.status_code == 201
    medication = medication_response.json()

    timeline = client.get(f"/api/v1/patients/{patient_id}/timeline")
    assert timeline.status_code == 200
    assert {item["resource_type"] for item in timeline.json()} == {
        "Patient",
        "DocumentReference",
        "MedicationStatement",
    }

    backup_response = client.post(
        "/api/v1/backup", json={"passphrase": BACKUP_PASSWORD}
    )
    assert backup_response.status_code == 200
    backup = backup_response.json()["backup_base64"]
    assert b"Synthetic Patient Marker" not in base64.b64decode(backup)

    later_patient = client.post(
        "/api/v1/patients",
        json={"name": "Must disappear after restore", "synthetic": True},
    )
    assert later_patient.status_code == 201
    wrong_passphrase = client.post(
        "/api/v1/backup/restore",
        json={"passphrase": "wrong-backup-passphrase", "backup_base64": backup},
    )
    assert wrong_passphrase.status_code == 422
    assert len(client.get("/api/v1/patients").json()) == 2

    restore = client.post(
        "/api/v1/backup/restore",
        json={"passphrase": BACKUP_PASSWORD, "backup_base64": backup},
    )
    assert restore.status_code == 204, restore.text
    assert client.get("/api/v1/patients").status_code == 401

    unlocked = client.post(
        "/api/v1/owner/unlock",
        json={
            "password": PASSWORD,
            "code": pyotp.TOTP(totp_secret).at((int(time.time() // 30) + 1) * 30),
        },
    )
    assert unlocked.status_code == 200
    client.headers["Authorization"] = f"Bearer {unlocked.json()['access_token']}"
    listed = client.get("/api/v1/patients")
    assert listed.status_code == 200
    assert [item["id"] for item in listed.json()] == [patient_id]
    assert client.get(
        f"/api/v1/patients/{patient_id}/documents"
    ).json()[0]["id"] == document["id"]
    assert client.get(
        f"/api/v1/patients/{patient_id}/medication-statements"
    ).json()[0]["id"] == medication["id"]
    assert database.exists()
    assert b"Synthetic Patient Marker" not in database.read_bytes()
    with sqlite3.connect(database) as connection:
        assert connection.execute("SELECT COUNT(*) FROM event_outbox").fetchone()[0] == 6
        assert connection.execute("SELECT COUNT(*) FROM audit").fetchone()[0] >= 5
    assert client.post("/api/v1/owner/lock").status_code == 204
    assert client.get("/api/v1/patients").status_code == 401

def test_wrong_mfa_consent_revocation_and_document_validation_fail_closed(tmp_path):
    client, _, _, _ = create_client(tmp_path)
    invalid_unlock = client.post(
        "/api/v1/owner/unlock",
        json={"password": PASSWORD, "code": "000000"},
    )
    assert invalid_unlock.status_code == 401

    patient = client.post(
        "/api/v1/patients",
        json={"name": "Another synthetic patient", "synthetic": True},
    ).json()
    bad_document = client.post(
        f"/api/v1/patients/{patient['id']}/documents",
        json={
            "patient_id": patient["id"],
            "title": "Mismatched PDF",
            "content_type": "application/pdf",
            "content_base64": base64.b64encode(b"not a PDF").decode(),
            "synthetic": True,
        },
    )
    assert bad_document.status_code == 422

    assert client.post("/api/v1/consent/revoke").status_code == 204
    denied = client.get("/api/v1/patients")
    assert denied.status_code == 403
    denied_backup = client.post(
        "/api/v1/backup", json={"passphrase": BACKUP_PASSWORD}
    )
    assert denied_backup.status_code == 403


def test_setup_cannot_create_a_second_owner_and_bad_backup_is_rejected(tmp_path):
    client, _, _, setup_code = create_client(tmp_path)
    second_setup = client.post(
        "/api/v1/owner/setup",
        json={"display_name": "Another owner", "password": PASSWORD},
    )
    assert second_setup.status_code == 409
    replayed_code = client.post(
        "/api/v1/owner/unlock",
        json={"password": PASSWORD, "code": setup_code},
    )
    assert replayed_code.status_code == 401
    bad_restore = client.post(
        "/api/v1/backup/restore",
        json={
            "passphrase": BACKUP_PASSWORD,
            "backup_base64": base64.b64encode(b"not a backup").decode(),
        },
    )
    assert bad_restore.status_code == 422


def test_packaged_api_requires_the_private_host_channel(tmp_path):
    protected = TestClient(
        create_app(tmp_path / "protected.sqlite3", ipc_secret=b"x" * 32)
    )
    assert protected.get("/api/v1/health").status_code == 403
    assert protected.get(
        "/api/v1/health", headers={"X-LifeLedger-IPC": "wrong"}
    ).status_code == 403
    authorized = protected.get(
        "/api/v1/health",
        headers={"X-LifeLedger-IPC": (b"x" * 32).hex()},
    )
    assert authorized.status_code == 200
    assert authorized.json()["pid"] > 0

    locked_down = TestClient(create_app())
    assert locked_down.get("/api/v1/health").status_code == 503


def test_checked_in_openapi_contract_matches_fastapi():
    repository = Path(__file__).resolve().parents[2]
    saved_contract = json.loads(
        (repository / "docs/implementation/openapi.json").read_text(
            encoding="utf-8"
        )
    )
    generated_contract = create_app().openapi()
    assert saved_contract == generated_contract
    assert saved_contract["openapi"] == "3.1.0"
    assert "/api/v1/backup/restore" in saved_contract["paths"]
    assert "HTTPBearer" in saved_contract["components"]["securitySchemes"]
