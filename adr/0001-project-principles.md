# ADR-0001

# Immutable Project Principles

Status

Accepted

---

# Context

LifeLedger is intended to be a multi-decade open-source project.

Architectural drift must be minimized.

Core principles are therefore declared immutable.

---

# Decision

The following principles shall govern all future decisions.

---

## Privacy First

User privacy takes precedence over convenience.

---

## Local First

All functionality must work without cloud services.

Cloud services are optional.

---

## FHIR First

FHIR R4 is the canonical health data model.

Provider-specific models may not bypass FHIR.

---

## MCP First

AI integrations shall support MCP.

Avoid vendor lock-in.

---

## AI Agnostic

LifeLedger shall not depend on a single AI provider.

---

## Open Source First

Preference is given to open standards.

---

## Vendor Neutral

No manufacturer shall receive privileged support.

---

## Provenance First

All health data must record origin.

---

## Consent First

Every data sharing action requires explicit user consent.

---

## Security First

Health data must be encrypted.

---

## Internationalization First

The platform must support multilingual usage.

No component shall assume English-only usage.

---

# Consequences

Features violating these principles must:

- justify the exception
- create an ADR
- undergo architecture review

Default outcome:

Reject implementation.
