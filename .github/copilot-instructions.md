# LifeLedger Copilot Instructions

Version: 1.0

Status: Mandatory

These instructions apply to all Copilot generated code, documents,
specifications, architectures, pull requests and repository changes.

If any generated output conflicts with this document, this document wins.

---

# Project Identity

Project:

LifeLedger

Tagline:

Your Health.
Your Data.
Your Timeline.

LifeLedger is a Local-First, Privacy-First, Open Source Personal Health Intelligence Platform.

---

# Platform Components

The platform consists of three major systems.

## LifeLedger

Responsibilities:

- Personal Health Record
- Health Timeline
- Medical Documents
- Family Health
- Medication Tracking
- Companion Apps
- Emergency Profiles

LifeLedger must not contain:

- AI provider implementations
- FHIR mapping implementations
- Connector implementations

---

## VitaFabric

Responsibilities:

- FHIR R4 Canonical Model
- Data Integration
- Connectors
- Synchronization
- Provenance Tracking
- Data Quality
- Storage Abstraction

All health data enters the platform through VitaFabric.

No component may bypass VitaFabric.

---

## LifeWeaver

Responsibilities:

- AI Providers
- MCP Client
- MCP Server
- Agent Framework
- RAG
- Knowledge Graph
- Personal Health Twin

No AI implementation belongs inside LifeLedger.

## Proposed Core Runtime

Draft [RFC-0002](../rfc/RFC-0002%20Platform%20Core%20Architecture) proposes
shared identity and consent, security services, an event bus, plugin hosting,
a secret store, and audit services, with explicit capabilities and a
WASM-first plugin runtime. The Core Runtime must not contain product business
logic, health models, or AI. These remain draft proposals, not implemented
services or accepted component ownership; do not assume their interfaces or
security guarantees exist.

---

# Immutable Principles

The following principles are non-negotiable.

## Privacy First

User privacy takes precedence over convenience.

---

## Local First

Every feature must operate locally.

Cloud support is optional.

Cloud services must never become mandatory.

---

## FHIR First

FHIR R4 is the canonical health model.

Alternative health data models are prohibited.

---

## MCP First

MCP compatibility must be preserved.

Avoid provider-specific coupling.

---

## AI Agnostic

No dependency on a single AI provider.

Supported providers should remain interchangeable.

---

## Open Source First

Prefer:

- Open Standards
- Open Protocols
- Open Formats

Avoid unnecessary proprietary dependencies.

---

## Vendor Neutral

No wearable, AI provider, storage provider or platform receives special treatment.

---

## Provenance First

Every imported health record must record:

- source
- connector
- import timestamp
- original identifier

---

## Consent First

Data access must always respect user consent.

No exceptions.

---

## Security First

Health data must be encrypted.

Security shall never be deferred.

---

## Internationalization First

The entire platform shall be localization-ready.

No component may assume:

- English-only
- US date formats
- single timezone

---

# Repository Structure Rules

The repository structure is authoritative.

Use:

platform/

    vitafabric/

    lifeweaver/

Never recreate:

modules/

---

Use:

integrations/

Never reintroduce:

homeassistant/

as a root folder.

---

Use:

docs/

as primary source of documentation.

Avoid duplicate documentation locations.

---

Use:

specifications/

for technical specifications.

Avoid architecture definitions outside specifications or docs.

---

# Architecture Rules

Before creating any component ask:

1. Does this belong in LifeLedger?
2. Does this belong in VitaFabric?
3. Does this belong in LifeWeaver?

If unclear:

Stop.

Create ADR.

Do not guess.

---

# Data Rules

Health data must:

- pass through VitaFabric
- map to FHIR
- record provenance
- support consent enforcement

Direct storage of provider-specific payloads is forbidden.

---

# AI Rules

LifeWeaver owns:

- Agents
- MCP
- RAG
- AI Providers

Avoid:

- OpenAI-specific abstractions
- Anthropic-specific abstractions
- Gemini-specific abstractions

Use provider interfaces.

---

# Localization Rules

Never hardcode:

- UI strings
- notifications
- dialog text
- error messages

Use translation keys.

Every new UI element must support localization.

---

# Security Rules

Forbidden:

- plaintext health data
- hardcoded secrets
- unencrypted backups
- analytics without consent
- hidden telemetry

Required:

- AES-256-GCM
- Argon2
- RBAC
- Audit Logging

---

# Documentation Rules

Architecture changes require:

- ADR
- Documentation update

Major changes require:

- RFC

Implementation without documentation is prohibited.

---

# Pull Request Requirements

Every Pull Request must answer:

[ ] FHIR compliant

[ ] VitaFabric compliant

[ ] LifeWeaver compliant

[ ] Local First compliant

[ ] Privacy First compliant

[ ] MCP compatible

[ ] AI Agnostic

[ ] Provenance compliant

[ ] Consent compliant

[ ] Localization compliant

[ ] Security compliant

[ ] No vendor lock-in introduced

---

# Automatic PR Rejection Criteria

Reject Pull Request if:

- FHIR is bypassed
- VitaFabric is bypassed
- Consent checks are bypassed
- Provenance tracking is bypassed
- Hardcoded UI strings are introduced
- Telemetry is added
- Plaintext health data is stored
- Hardcoded secrets are introduced
- Vendor-specific AI logic leaks into LifeWeaver
- Cloud dependency becomes mandatory

---

# Decision Process

When uncertainty exists:

1. Check ADRs
2. Check Specifications
3. Check Product Documentation
4. Create ADR
5. Request architectural review

Never make silent architectural changes.

---

# Long-Term Goal

LifeLedger shall become the open-source reference platform for:

- Personal Health Records
- Wearable Aggregation
- FHIR Interoperability
- AI-Assisted Health Insights
- Privacy-First Health Data Management

Every implementation decision should be evaluated against this goal.
