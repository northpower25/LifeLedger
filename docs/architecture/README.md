# LifeLedger Platform Architecture

LifeLedger is in the design stage. The target platform is organized around
three first-class components: LifeLedger, the personal health record platform;
VitaFabric, the interoperability platform; and LifeWeaver, the AI, MCP, and
agent platform. This is a starting point for discussion, not an implemented
architecture.

Client applications and backend services will support the LifeLedger
experience. Integrations and plugins will extend the platform through
specifications and trust boundaries that are defined before implementation.
Home Assistant is an integration under `integrations/`.

Local-first synchronization, data ownership, consent, encryption, identity,
deployment topology, trust boundaries, and interoperability require further
design. Record decisions in [ADRs](../../adr/) and use [RFCs](../../rfc/) for
proposals that need community review. See the [security documentation](../security/)
and the [repository migration report](repository_migration_report.md).
