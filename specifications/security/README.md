# Security Specifications

Authoritative security and privacy requirements belong here. Operational
vulnerability reporting guidance remains in the root `SECURITY.md`.

Draft [RFC-0002](../../rfc/0002-platform-core-architecture.md) proposes
Core Runtime security services, Identity & Consent, audit logging, explicit
capabilities, and a sandboxed plugin host. Normative specifications must define
their policies, interfaces, failure behavior, and verifiable enforcement
before implementation; the RFC draft itself is not a security control.
Health-data access remains mediated by VitaFabric, and storage adapters must
not receive plaintext health data or keys.

Part of the LifeLedger Platform Architecture: LifeLedger, VitaFabric, and LifeWeaver.
