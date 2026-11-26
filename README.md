# LifeLedger

**Your Health. Your Data. Your Timeline.**

LifeLedger is a planned local-first, privacy-first personal health platform.
This repository is an architectural foundation, not a working product. It does
not yet provide applications, services, deployments, FHIR conformance, AI
capabilities, or a security guarantee. Do not use it to store real health data
or make medical decisions.

## LifeLedger Platform Architecture

LifeLedger is envisioned as a local-first personal health platform. The
personal health record is its first reference application; applications,
integrations and AI capabilities are intended to use shared, secure platform
contracts rather than access data stores directly.

The platform's component responsibilities remain distinct:

- **LifeLedger** owns the health-record product experience and applications.
- **VitaFabric** owns health-data integration, FHIR mapping, provenance and
  storage abstraction. Health data must pass through VitaFabric.
- **LifeWeaver** owns optional AI providers, MCP and agents.

The [draft RFC-0002](rfc/RFC-0002%20Platform%20Core%20Architecture) proposes a
Core Runtime for shared identity and consent, security services, an event bus,
and plugin hosting, with capability-based access and a WASM-first plugin
runtime. The Core Runtime is not intended to contain business logic, health
models, or AI. These remain proposals under review, not implemented services
or accepted component assignments; the [platform proposal](rfc/0001-platform-direction.md)
and [architecture overview](docs/architecture/README.md) describe their status.

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

See the [platform vision](https://github.com/northpower25/LifeLedger/blob/main/docs/concept),
the [architecture overview](docs/architecture/README.md), the
[repository migration report](docs/architecture/repository_migration_report.md),
the [assessment and roadmaps](docs/roadmap/README.md), and
[CONTRIBUTING](CONTRIBUTING.md) to learn more.

## Get involved

There are no runnable services or installation instructions yet. Proposed
direction and decisions are documented through [ADRs](adr/) and [RFCs](rfc/).
See [governance](docs/governance/README.md) for decision-making and
[SECURITY](SECURITY.md) for private vulnerability reporting.

## License

LifeLedger is licensed under the [GNU Affero General Public License v3.0 only](LICENSE).
