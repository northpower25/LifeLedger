# Repository Migration Report

## Old structure

The repository previously grouped the VitaFabric and LifeWeaver platforms in
an intermediary collection, kept Home Assistant at the root, and separated architecture,
governance, security, and roadmap documentation into root-level folders.
Specifications, brand resources, shared assets, and future developer tooling
did not have dedicated locations.

## New structure

- `platform/vitafabric/` and `platform/lifeweaver/` are first-class platform
  locations.
- `integrations/homeassistant/` contains the Home Assistant integration.
- `docs/architecture/`, `docs/governance/`, `docs/security/`, and
  `docs/roadmap/` hold their respective documentation; research, community,
  product, FHIR, MCP, agents, mobile, and integrations documentation also have
  dedicated locations.
- `specifications/` is the authoritative home for technical standards and
  design, organized by FHIR, MCP, agents, connectors, storage, security,
  mobile, and integrations.
- `branding/`, `assets/`, and `tools/` reserve locations for their respective
  resources without introducing implementations.
- `docker/` and `kubernetes/` are reserved root locations alongside the
  existing application, infrastructure, tests, plugins, ADR, and RFC areas.

## Rationale

The layout makes the platform boundaries explicit: LifeLedger is the product
platform, with VitaFabric and LifeWeaver as first-class platform components;
Home Assistant is an integration rather than a platform module. A single
documentation tree is distinct from authoritative technical specifications,
and future resource categories are discoverable without implying that they
already contain software.

## Impact

Existing placeholder documentation was moved with its component and updated
for its new location. README links now use the consolidated documentation
paths. This is a repository-only migration: it adds no application,
backend, frontend, Flutter, AI, Home Assistant, deployment, or developer-tool
implementation. Consumers of the former paths must use the new locations.

## Future benefits

The structure supports independent ownership and growth of the LifeLedger,
VitaFabric, and LifeWeaver platforms; clearer integration boundaries; easier
navigation for contributors; and a stable separation between explanatory
documentation and normative specifications. Dedicated asset, branding,
deployment, infrastructure, and tooling locations provide room to grow while
keeping this bootstrap repository implementation-free.
