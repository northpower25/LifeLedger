CREATE TABLE IF NOT EXISTS metadata (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS identity_owner (
    owner_id TEXT PRIMARY KEY,
    password_hash TEXT NOT NULL,
    kdf_salt BLOB NOT NULL,
    wrapped_key BLOB NOT NULL,
    totp_ciphertext BLOB NOT NULL,
    confirmed INTEGER NOT NULL CHECK (confirmed IN (0, 1)),
    last_totp_step INTEGER
);
CREATE TABLE IF NOT EXISTS patients (
    resource_id TEXT PRIMARY KEY,
    owner_id TEXT NOT NULL REFERENCES identity_owner(owner_id),
    created_at TEXT NOT NULL,
    payload BLOB NOT NULL
);
CREATE TABLE IF NOT EXISTS document_references (
    resource_id TEXT PRIMARY KEY,
    owner_id TEXT NOT NULL REFERENCES identity_owner(owner_id),
    patient_id TEXT NOT NULL REFERENCES patients(resource_id),
    created_at TEXT NOT NULL,
    payload BLOB NOT NULL
);
CREATE TABLE IF NOT EXISTS medication_statements (
    resource_id TEXT PRIMARY KEY,
    owner_id TEXT NOT NULL REFERENCES identity_owner(owner_id),
    patient_id TEXT NOT NULL REFERENCES patients(resource_id),
    created_at TEXT NOT NULL,
    payload BLOB NOT NULL
);
CREATE TABLE IF NOT EXISTS consent (
    consent_id TEXT PRIMARY KEY,
    owner_id TEXT NOT NULL REFERENCES identity_owner(owner_id),
    status TEXT NOT NULL CHECK (status IN ('ACTIVE', 'REVOKED')),
    payload BLOB NOT NULL
);
CREATE TABLE IF NOT EXISTS capability_grants (
    grant_id TEXT PRIMARY KEY,
    owner_id TEXT NOT NULL REFERENCES identity_owner(owner_id),
    status TEXT NOT NULL CHECK (status IN ('ACTIVE', 'REVOKED')),
    payload BLOB NOT NULL
);
CREATE TABLE IF NOT EXISTS audit (
    event_id TEXT PRIMARY KEY,
    owner_id TEXT NOT NULL REFERENCES identity_owner(owner_id),
    event_type TEXT NOT NULL,
    occurred_at TEXT NOT NULL,
    payload BLOB NOT NULL
);
CREATE TABLE IF NOT EXISTS event_outbox (
    event_id TEXT PRIMARY KEY,
    owner_id TEXT NOT NULL REFERENCES identity_owner(owner_id),
    event_type TEXT NOT NULL,
    occurred_at TEXT NOT NULL,
    payload BLOB NOT NULL,
    delivered INTEGER NOT NULL DEFAULT 0 CHECK (delivered IN (0, 1))
);
CREATE INDEX IF NOT EXISTS idx_patients_owner_time
    ON patients(owner_id, created_at);
CREATE INDEX IF NOT EXISTS idx_documents_owner_time
    ON document_references(owner_id, created_at);
CREATE INDEX IF NOT EXISTS idx_medications_owner_time
    ON medication_statements(owner_id, created_at);
CREATE INDEX IF NOT EXISTS idx_audit_owner_time
    ON audit(owner_id, occurred_at);
CREATE INDEX IF NOT EXISTS idx_outbox_delivery
    ON event_outbox(delivered, occurred_at);
