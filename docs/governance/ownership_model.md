# Ownership Model

This model defines responsibility boundaries, not named individuals. Until
maintainers assign specialized owners, repository maintainers are accountable
for review and coordination. Ownership applies to the LifeLedger Platform
Architecture: LifeLedger, VitaFabric, and LifeWeaver.

| Area | Responsible ownership |
| --- | --- |
| `backend/` | Backend maintainers own service architecture, data lifecycle, API contracts, and backend quality. Coordinate data and interoperability contracts with VitaFabric. |
| `frontend-web/` | Web maintainers own browser-client architecture, accessibility, and web-specific quality. |
| `frontend-mobile/` | Mobile maintainers own mobile-client architecture, platform privacy, and mobile-specific quality. |
| `frontend-desktop/` | Desktop maintainers own desktop-client architecture, packaging boundaries, and desktop-specific quality. |
| VitaFabric (`platform/vitafabric/`) | VitaFabric maintainers own interoperability architecture, standards interpretation, and related specifications. |
| LifeWeaver (`platform/lifeweaver/`) | LifeWeaver maintainers own AI, MCP, and agent architecture, including permission and data-boundary design. |
| Core Runtime | Draft [RFC-0002](../../rfc/0002-platform-core-architecture.md) and [RFC-0014](../../rfc/0014-core-runtime-platform-boundaries.md) propose shared identity and consent, security services, event bus, plugin host, secret store, and audit services. Maintainer ownership, implementation placement, and contracts remain to be assigned and reviewed; this proposal does not move VitaFabric or LifeWeaver responsibilities. |
| `plugins/` | Plugin maintainers own extension contracts, compatibility expectations, and plugin trust boundaries in coordination with security owners. |
| `integrations/` | Integration maintainers own external-system integration scope, lifecycle, compatibility and coordination. Connector execution and FHIR mapping for health data are implemented and reviewed within VitaFabric; all health-data exchange uses VitaFabric contracts. |
| Identity and consent | Draft RFC-0002 and RFC-0014 place identity and consent in the proposed shared Core Runtime and describe users, devices, sessions, grants, delegation, emergency access and capabilities. Policy, contracts, implementation ownership and technical enforcement remain subject to review; consent must be enforced at the relevant data-access boundary, including VitaFabric. |
| Security (`docs/security/`, `specifications/security/`, and `SECURITY.md`) | Security maintainers coordinate threat modeling, security requirements, vulnerability handling, and cross-component review. |
| Roadmap (`docs/roadmap/`) | Roadmap maintainers coordinate priorities and communicate proposals; changes with architectural impact follow the RFC and ADR processes. |

## Cross-area changes

Changes spanning multiple ownership areas require review from each affected
owner. Security-sensitive changes require security review; standards or
interoperability changes require VitaFabric and specification review. Where no
specialized owner has been assigned, repository maintainers provide the
interim review and record significant decisions through an ADR or RFC.

Plugin category does not change component ownership: health-data connectors
and storage adapters remain VitaFabric responsibilities, AI-provider adapters
belong to LifeWeaver, and product UI/application extensions belong to LifeLedger.
Integration owners may coordinate and maintain an external integration without
moving health-data processing outside VitaFabric.

Owners are expected to keep their area documentation current, identify
privacy, safety, and interoperability impacts, and avoid representing planned
capabilities as implemented.
