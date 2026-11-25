# Architecture

LifeLedger is in the design stage. The following is a starting point for
discussion, not an implemented architecture:

- Client applications provide access to personal health records.
- Backend services manage application behavior and persistence.
- VitaFabric handles integration and FHIR R4 exchange.
- LifeWeaver provides an AI-agnostic interface for models, MCP, and agents.
- Plugins and Home Assistant integrations extend the platform.
- PostgreSQL/TimescaleDB and OpenSearch are intended storage and search technologies.

Local-first synchronization, data ownership, consent, encryption, identity,
deployment topology, trust boundaries, and interoperability are unresolved.
Document decisions in [ADRs](../adr/) and use [RFCs](../rfc/) for proposals
that need community review. Assess health data and AI data flows before
implementation; see [security](../security/).
