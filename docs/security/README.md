# Security

Detailed security architecture and operational guidance are not yet
specified. Draft [RFC-0002](../../rfc/RFC-0002%20Platform%20Core%20Architecture)
proposes Core Runtime security services, identity and consent, audit, a
capability model, and a plugin host; these are not implemented or accepted
controls. Threat models must cover sensitive local health data, family/delegate
and emergency access, storage and sync, integrations, every plugin type,
Marketplace distribution, event subscriptions, secrets, and AI data flows.
Authentication, authorization and consent must be distinguished and enforced
at the relevant data boundaries, including VitaFabric.

No plugin is trusted by default. Manifests, capabilities, signatures,
Marketplace listings or installation consent do not by themselves prove
isolation or safety. Define and test enforceable controls before running
third-party code; do not allow direct database access or unapproved data
sharing. See the [security roadmap](../roadmap/project.md) and report
vulnerabilities according to [SECURITY.md](../../SECURITY.md).

Part of the LifeLedger Platform Architecture: LifeLedger, VitaFabric, and LifeWeaver.
