# Documentation

`docs/` is the single source of truth for LifeLedger project documentation.
Authoritative technical standards and design specifications belong in
[`specifications/`](../specifications/), not here.

The proposed **LifeLedger Platform** has a personal health record as its first
reference application. Its component responsibilities remain distinct:
**LifeLedger** owns product experiences, **VitaFabric** owns health-data
integration and FHIR, and **LifeWeaver** owns optional AI, MCP and agents.
Draft [RFC-0002](../rfc/RFC-0002%20Platform%20Core%20Architecture) proposes a
shared Core Runtime with identity and consent, security services, an event bus,
plugin hosting, and capability-based access. It does not assign business
logic, health models, or AI to the Core Runtime. These capabilities remain
proposals, not implemented services or accepted architecture. Start with the
[repository overview](../README.md) and [architecture](architecture/README.md).
Documentation is design-stage guidance; it does not imply that an application
or platform implementation exists.
