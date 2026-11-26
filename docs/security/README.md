# Security

Security architecture and operational guidance are not yet specified.
Threat models must cover sensitive local health data, identity and consent,
family/delegate and emergency access, storage and sync, integrations, every
plugin type, Marketplace distribution, and AI data flows. Authentication,
authorization and consent must be distinguished and enforced at the relevant
data boundaries, including VitaFabric.

No plugin is trusted by default. Manifests, capabilities, signatures,
Marketplace listings or installation consent do not by themselves prove
isolation or safety. Define and test enforceable controls before running
third-party code; do not allow direct database access or unapproved data
sharing. See the [security roadmap](../roadmap/project.md) and report
vulnerabilities according to [SECURITY.md](../../SECURITY.md).

Part of the LifeLedger Platform Architecture: LifeLedger, VitaFabric, and LifeWeaver.
