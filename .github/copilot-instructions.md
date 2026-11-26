# LifeLedger Copilot Instructions

These rules override implementation convenience.

Copilot must always prioritize these principles.

---

# Project Identity

LifeLedger

Tagline:

Your Health.
Your Data.
Your Timeline.

---

# Architecture

LifeLedger consists of:

- LifeLedger
- VitaFabric
- LifeWeaver

Never blur responsibilities between these components.

---

# LifeLedger Responsibilities

- Health Record
- Documents
- Medication
- Family History
- Health Timeline
- Companion Apps

LifeLedger must NOT contain:

- AI provider logic
- Connector implementations
- FHIR mapping logic

---

# VitaFabric Responsibilities

- FHIR Canonical Model
- Data Mapping
- Connectors
- Synchronization
- Provenance

All health data enters the platform through VitaFabric.

No direct provider-specific models may bypass VitaFabric.

---

# LifeWeaver Responsibilities

- AI Providers
- MCP
- Agents
- RAG
- Health Twin

No AI logic belongs in LifeLedger.

---

# Privacy First

Never introduce:

- telemetry
- tracking
- analytics
- hidden cloud dependencies

without explicit approval.

---

# Local First

Every feature must work locally.

Cloud support is optional.

Cloud support may never become mandatory.

---

# FHIR First

FHIR R4 is the canonical health model.

Avoid creating parallel health models.

---

# MCP First

AI integrations must remain MCP-compatible.

Avoid AI vendor lock-in.

---

# Open Source First

Prefer:

- open standards
- open protocols
- open file formats

Avoid proprietary dependencies.

---

# Security First

Never store health data unencrypted.

Use:

- AES-256-GCM
- Argon2
- Provenance Tracking
- Consent Model

---

# Before Every Change

Validate:

□ Does this belong in LifeLedger?

□ Does this belong in VitaFabric?

□ Does this belong in LifeWeaver?

□ Does this violate Local First?

□ Does this violate Privacy First?

□ Does this bypass FHIR?

□ Does this create vendor lock-in?

□ Does this bypass Consent Management?

□ Does this bypass Provenance Tracking?

If any answer is YES:

Stop and document the architectural impact.

Do not proceed automatically.
