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
| `plugins/` | Plugin maintainers own extension contracts, compatibility expectations, and plugin trust boundaries in coordination with security owners. |
| `integrations/` | Integration maintainers own external-system connectors and their lifecycle, data exchange, and compatibility. |
| Security (`docs/security/`, `specifications/security/`, and `SECURITY.md`) | Security maintainers coordinate threat modeling, security requirements, vulnerability handling, and cross-component review. |
| Roadmap (`docs/roadmap/`) | Roadmap maintainers coordinate priorities and communicate proposals; changes with architectural impact follow the RFC and ADR processes. |

## Cross-area changes

Changes spanning multiple ownership areas require review from each affected
owner. Security-sensitive changes require security review; standards or
interoperability changes require VitaFabric and specification review. Where no
specialized owner has been assigned, repository maintainers provide the
interim review and record significant decisions through an ADR or RFC.

Owners are expected to keep their area documentation current, identify
privacy, safety, and interoperability impacts, and avoid representing planned
capabilities as implemented.
