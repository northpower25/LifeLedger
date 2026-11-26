# LifeLedger

**Your Health. Your Data. Your Timeline.**

LifeLedger is a planned local-first, privacy-first personal health platform.
This repository is an architectural foundation, not a working product. It does
not yet provide applications, services, deployments, FHIR conformance, AI
capabilities, or a security guarantee. Do not use it to store real health data
or make medical decisions.

## LifeLedger Platform Architecture

The platform has three first-class parts:

- **LifeLedger** is the personal health record platform.
- **VitaFabric** is the interoperability platform for health data exchange,
  including planned FHIR standards support.
- **LifeWeaver** is the AI, Model Context Protocol (MCP), and agent platform.

The architecture is design intent, not a statement of implemented features.

## Repository layout

| Path | Purpose |
| --- | --- |
| `.github/` | Repository templates and workflows |
| `backend/` | Planned backend services |
| `frontend-web/` | Planned web client |
| `frontend-mobile/` | Planned mobile client |
| `frontend-desktop/` | Planned desktop client |
| `platform/vitafabric/` | VitaFabric platform |
| `platform/lifeweaver/` | LifeWeaver platform |
| `plugins/` | Future extension ecosystem |
| `integrations/` | External integrations, including Home Assistant |
| `docs/` | Project documentation and guidance |
| `specifications/` | Authoritative technical standards and design specifications |
| `tests/` | Cross-component test organization |
| `tools/` | Reserved for future developer tooling |
| `docker/`, `kubernetes/` | Reserved deployment configuration locations |
| `infrastructure/` | Infrastructure and operational architecture |
| `branding/` | Brand identity resources |
| `assets/` | Shared diagrams, images, screenshots, and presentations |
| `adr/`, `rfc/` | Architecture decisions and community proposals |

See the [architecture overview](docs/architecture/README.md), the
[repository migration report](docs/architecture/repository_migration_report.md),
and [CONTRIBUTING](CONTRIBUTING.md) to learn more.

## Get involved

There are no runnable services or installation instructions yet. Proposed
direction and decisions are documented through [ADRs](adr/) and [RFCs](rfc/).
See [governance](docs/governance/README.md) for decision-making and
[SECURITY](SECURITY.md) for private vulnerability reporting.

## License

LifeLedger is licensed under the [GNU Affero General Public License v3.0 only](LICENSE).
