# LifeLedger

**Your Health. Your Data. Your Timeline.**

LifeLedger is a planned local-first, privacy-first personal health platform. It
aims to help people keep and understand their health records while retaining
control over their data.

This repository is an early project bootstrap, not a working product. No
application, deployment, FHIR implementation, AI integration, or security
guarantee is provided yet. Do not use it to store real health data or make
medical decisions.

## Platform

- **LifeLedger**: the personal health record platform.
- **VitaFabric**: the planned FHIR R4 interoperability and data integration layer.
- **LifeWeaver**: the planned AI, Model Context Protocol (MCP), and agent framework.

## Principles

- **Local first:** design for local ownership and useful offline operation.
- **Privacy first:** minimize collection and disclosure of sensitive data.
- **Open source:** licensed under AGPL-3.0-only; see [LICENSE](LICENSE).
- **Interoperable:** target FHIR R4 for health data exchange.
- **AI agnostic:** support multiple models and providers rather than depending
  on a single vendor; use MCP where appropriate.

These are design goals, not claims about implemented capabilities.

## Repository map

| Path | Intended purpose |
| --- | --- |
| [backend](backend/) | Python/FastAPI services, PostgreSQL and TimescaleDB |
| [frontend-web](frontend-web/) | React, TypeScript and Tailwind web client |
| [frontend-mobile](frontend-mobile/) | Flutter mobile client |
| [frontend-desktop](frontend-desktop/) | Tauri desktop client |
| [modules/vitafabric](modules/vitafabric/) | FHIR R4 and integration layer |
| [modules/lifeweaver](modules/lifeweaver/) | AI, MCP and agent framework |
| [plugins](plugins/) | Extension points and plugins |
| [homeassistant](homeassistant/) | Home Assistant integration |
| [infrastructure](infrastructure/) | Deployment and operational configuration, including OpenSearch |
| [tests](tests/) | Cross-component tests |
| [docs](docs/) | Project and user documentation |
| [architecture](architecture/) | Architecture overview and design placeholders |
| [adr](adr/) | Architecture decision records |
| [rfc](rfc/) | Requests for comments |
| [roadmap](roadmap/) | Proposed project milestones |
| [governance](governance/) | Project decision-making |
| [security](security/) | Security design and resources |

## Get involved

There are no runnable services or installation instructions yet. See the
[roadmap](roadmap/README.md) for proposed work, [CONTRIBUTING](CONTRIBUTING.md)
to contribute, [governance](governance/README.md) for decisions, and
[SECURITY](SECURITY.md) for private vulnerability reporting.

## License

LifeLedger is licensed under the [GNU Affero General Public License v3.0 only](LICENSE).
