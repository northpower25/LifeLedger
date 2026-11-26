# LifeLedger Platform Architecture

LifeLedger is in the design stage. The proposed product is a local-first
personal health platform, with the personal health record as its first
reference application. This platform framing is a proposal, not an implemented
architecture.

## Proposed platform direction

The [platform vision](https://github.com/northpower25/LifeLedger/blob/main/docs/concept)
proposes the following conceptual model:

```text
LifeLedger Platform
├── Shared platform capabilities (runtime, security, identity and consent)
├── VitaFabric — health-data gateway, FHIR and storage abstraction
├── LifeWeaver — optional AI, MCP and agent services
├── Secure extension framework
└── Applications — personal health record first, then other apps
```

Draft [RFC-0002](../../rfc/RFC-0002%20Platform%20Core%20Architecture) proposes
that the shared Core Runtime provide identity and consent, security services,
an event bus, a plugin host, a secret store and audit services. It contains no
business logic, health models or AI. The runtime's service contracts and
implementation ownership remain subject to review; no such services are
implemented or accepted by this draft.

The proposal does not merge or reassign component responsibilities: LifeLedger
owns product experiences and applications; VitaFabric owns health-data
integration, FHIR mapping, provenance and storage abstraction; LifeWeaver owns
AI providers, agents and MCP. VitaFabric remains a required platform component.
Every health-data operation must pass through VitaFabric and respect consent;
applications have no separate health-data database, and plugins must not
access a database directly.

The proposed capability model grants no implicit plugin rights: requested
capabilities must be explicitly granted and technically enforced. Consent
enforcement, audit, authentication, the FHIR core model and capability
enforcement are platform responsibilities, not plugins. The RFC proposes a
WASM-first plugin runtime, with a Python connector runtime only as a possible
later extension. These are draft choices, not implemented runtime guarantees.

The proposal names connector, integration, provider, storage, UI and
application plugins. Their contracts and responsibility boundaries are not yet
specified: connectors and health-data storage adapters belong within
VitaFabric's controlled interfaces; provider adapters belong to LifeWeaver;
presentation and application extensions belong to LifeLedger. Any extension
that handles health data must use VitaFabric contracts. The proposed
Marketplace distinguishes proposed Community, Verified and Official
categories; governance and review criteria remain open, and labels must not
imply a security guarantee or replace user consent. The
[platform-direction RFC](../../rfc/0001-platform-direction.md) and
[proposed ADR](../../adr/0002-platform-direction.md) seek review before these
boundaries or choices are accepted. RFC-0002 also proposes that storage
adapters receive encrypted data only, never plaintext or keys.

## Proposed deployment modes

| Mode | Intended behavior and open boundaries |
| --- | --- |
| Local only | Core functionality operates locally without cloud services. |
| Local + relay | Optional push events, notifications, device discovery or remote-access relay; no plaintext health data in the relay. Event and connection metadata can still be sensitive and requires minimization and review. |
| Local + zero-knowledge sync | Optional encrypted synchronization and backups; the service must not receive decryption keys. Key recovery, metadata exposure, deletion and conflict handling remain open. |
| Managed cloud | A separately reviewed optional proposal where a service may process health data. It must not replace the local alternative or weaken consent, encryption, FHIR or other project requirements; feasibility and compliance are not established. |

These are design scenarios, not available deployment options or guarantees.
The [overall roadmap](../roadmap/project.md) sets evidence gates for each.

Client applications and backend services will support the LifeLedger
experience. Integrations and plugins will extend the platform only through
versioned contracts and trust boundaries defined before implementation.
Home Assistant is a proposed integration under `integrations/`, not an
exception to VitaFabric's data boundary.

Local-first synchronization, data ownership, consent, encryption, identity,
deployment topology, trust boundaries, and interoperability require further
design. Record decisions in [ADRs](../../adr/) and use [RFCs](../../rfc/) for
proposals that need community review. See the [security documentation](../security/)
and the [repository migration report](repository_migration_report.md).
