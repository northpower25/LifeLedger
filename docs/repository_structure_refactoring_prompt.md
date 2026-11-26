# LifeLedger Repository Structure Refactoring Prompt

You are a Principal Software Architect, Open Source Program Manager and Repository Governance Specialist.

IMPORTANT:

Do not generate backend code.
Do not generate frontend code.
Do not generate Flutter code.
Do not generate Tauri code.
Do not generate Home Assistant code.
Do not generate AI implementations.

At this stage only perform repository structure refactoring and repository architecture cleanup.

---

# Context

The current LifeLedger repository evolved through multiple planning iterations.

Several directory structures have become redundant and contradictory.

The goal is to establish a single authoritative repository structure before architecture documentation and implementation continue.

---

# Project Architecture

LifeLedger consists of:

## LifeLedger

Personal Health Record Platform

Responsibilities:

- Personal Health Record
- Medical Documents
- Medication Management
- Family Health
- Emergency Profiles
- Companion Apps
- Home Assistant Integration

---

## VitaFabric

FHIR-based Data Integration Layer

Responsibilities:

- FHIR Canonical Model
- Connector Framework
- Synchronization
- Provenance
- Data Quality
- Storage Abstraction

---

## LifeWeaver

AI and Agent Framework

Responsibilities:

- MCP
- Agents
- AI Providers
- RAG
- Knowledge Graph
- Personal Health Twin

---

# Repository Refactoring Goals

Audit the current repository structure.

Identify:

- duplicate directories
- overlapping responsibilities
- misplaced files
- conflicting ownership boundaries

Generate a migration plan.

Generate updated repository documentation.

Do not implement software.

---

# Directories To Remove

Remove the following root-level directories if they only contain documentation:

architecture/

security/

roadmap/

research/

community/

These should be moved under:

docs/

---

# Modules Refactoring

Remove:

modules/

Reason:

VitaFabric and LifeWeaver are first-class platform components.

They must not appear as generic modules.

Replace with:

platform/

    vitafabric/

    lifeweaver/

---

# Home Assistant Refactoring

Remove:

homeassistant/

Create:

integrations/

    homeassistant/

Reason:

Future integrations may include:

- Nextcloud
- Matrix
- OpenWebUI
- Research Platforms
- Clinical Systems

Home Assistant is an integration, not a core subsystem.

---

# Plugin Refactoring

Remove separate root-level directories:

wearables/

storage/

ai/

medical/

documents/

These create duplicated responsibilities.

Create:

plugins/

    connectors/

    storage/

    ai/

    medical/

    documents/

---

# Documentation Consolidation

Create a single source of truth:

docs/

Move all architecture-related documents under:

docs/architecture/

Move all governance-related documents under:

docs/governance/

Move all security-related documents under:

docs/security/

Move all roadmap-related documents under:

docs/roadmap/

Move all research-related documents under:

docs/research/

Move all community-related documents under:

docs/community/

---

# Specifications Layer

Create a new repository area:

specifications/

Purpose:

Authoritative system specifications.

Structure:

specifications/

    fhir/

    mcp/

    agents/

    connectors/

    storage/

    security/

    mobile/

    homeassistant/

---

# Branding Layer

Create:

branding/

    logos/

    icons/

    colors/

    fonts/

    press-kit/

---

# Final Target Structure

lifeledger/

.github/

docs/

    architecture/

    governance/

    security/

    roadmap/

    research/

    community/

    product/

    fhir/

    mcp/

    agents/

    integrations/

    mobile/

specifications/

    fhir/

    mcp/

    agents/

    connectors/

    storage/

    security/

    mobile/

    integrations/

platform/

    vitafabric/

    lifeweaver/

backend/

frontend-web/

frontend-mobile/

frontend-desktop/

plugins/

    connectors/

    storage/

    ai/

    medical/

    documents/

integrations/

    homeassistant/

tests/

tools/

examples/

docker/

kubernetes/

infrastructure/

branding/

assets/

---

# Produce

Generate:

1. Repository refactoring report
2. Directory migration plan
3. Updated repository tree
4. Ownership model per directory
5. Documentation ownership matrix
6. Repository governance impact
7. Future scalability assessment

Do not generate application code.

Repository architecture only.
