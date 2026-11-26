# RFC 0001: Platform direction and deployment scenarios

See the related [draft RFC-0002: Platform Core Architecture](RFC-0002%20Platform%20Core%20Architecture)
for the proposed Core Runtime, capability, event-bus, plugin-runtime, and
application model. Its draft status does not make those proposals accepted
architecture.

- Status: draft
- Author(s): To be assigned
- Date: 2026-11-26
- Related issues or ADRs: [ADR 0002](../adr/0002-platform-direction.md)

## Summary

Propose LifeLedger Platform as an umbrella for reusable capabilities and
applications, with the personal health record as a first reference application.
The [source vision](https://github.com/northpower25/LifeLedger/blob/main/docs/concept)
also proposes four deployment scenarios. This RFC is not an accepted design,
and does not claim that any capability exists.

## Motivation and goals

Make application and extension boundaries explicit while retaining a useful,
offline local core. Enable independent applications and integrations only
through reviewed, versioned contracts. Avoid treating a directory, registry,
or plugin manifest as evidence of a working platform or security boundary.

## Proposal

LifeLedger continues to own product experiences; VitaFabric owns health-data
integration, FHIR mapping, provenance and storage abstraction; LifeWeaver owns
AI, agents and MCP. All health data passes through VitaFabric and all access
respects consent. The platform framing does not transfer these responsibilities.

Design a shared runtime, security framework and **Identity & Consent** layer.
The proposed layer covers users, family members, delegates, grants, roles,
emergency access, plugin permissions, AI permissions and sync permissions.
Authentication, authorization and consent are distinct concerns; a role or
identity alone does not grant health-data access. Exact policy, ownership,
interfaces and enforcement boundaries require review and normative
specifications. Consent must be checked at the relevant data-access boundary,
including by VitaFabric; denial or revocation must not be bypassed by an app,
plugin, AI feature or storage adapter.

The proposed plugin types are connector, integration, provider, storage, UI
and application. Their component boundaries are:

- Connectors and health-data storage adapters are controlled VitaFabric
  responsibilities. Health data follows a VitaFabric contract, FHIR R4 model
  and controlled storage abstraction; extensions never connect directly to a
  database.
- External integrations use approved platform APIs; health data still passes
  through VitaFabric.
- Provider adapters belong to LifeWeaver and remain optional and
  provider-neutral.
- UI and application extensions belong to LifeLedger and use versioned
  platform APIs.

An extension is untrusted by default. A future contract should define a
manifest, least-privilege capabilities, explicit consent and revocation,
package integrity/signature, provenance and technically enforced isolation.
A signature or marketplace listing is not a security guarantee. The proposed
Marketplace may distinguish Community, Verified and Official listings, but
criteria and governance are open; it is optional, and neither discovery nor
local installation may require a central service.

Evaluate local-only operation first. Optional local-plus-relay and
local-plus-zero-knowledge-sync scenarios must not make cloud mandatory. Relay
must not hold plaintext health data; zero-knowledge sync must not receive
decryption keys. Managed cloud processing is a separate, optional proposal,
not an approved exception to local operation, consent or encryption. See the
[roadmap](../docs/roadmap/project.md) for scenario-specific gates.

## Alternatives

- Retain the health-record-first framing: simpler initially, but reusable
  contracts and extension boundaries could remain implicit.
- Make a central registry or cloud service mandatory: rejected as incompatible
  with local-first operation.
- Fix deployment, shared-service ownership and plugin contracts now:
  premature without reviewed data flows, threat models and implementation
  constraints.

## Privacy, security, and interoperability

Before implementation, model identities, roles, explicit consent and
revocation across applications, plugins, caches, exports and remote copies.
Define enforcement, audit, key management and recovery, threat boundaries,
metadata minimization and failure behavior. A relay can expose sensitive
metadata even when it stores no plaintext health data. Zero-knowledge claims
require a reviewed key and recovery design, not encryption alone. Managed
processing requires separate legal, privacy and security review and must meet
all applicable project constraints.

FHIR R4 and provenance remain mandatory for health data; MCP and
provider-neutral interfaces remain LifeWeaver responsibilities. No extension
or deployment mode may bypass VitaFabric or consent. Storage backends must
preserve the required encryption, audit and recovery controls, and remain
replaceable without tying the platform to a vendor.

## Rollout and compatibility

Review this RFC and its proposed ADR before accepting architectural changes.
Specify and test a synthetic offline vertical slice first, then prove plugin
contracts and isolation. Each optional deployment scenario requires its own
design, review and evidence before implementation or release. No real health
data before the existing release gate.

## Open questions

- Which user journey and client define the first reference application?
- Who owns and enforces the shared runtime, security, Identity & Consent,
  plugin-host and trust-boundary contracts?
- How are consent, identity, roles and revocation applied across applications
  and devices, including data already exported or synchronized?
- How are keys recovered without disclosing them to a sync service, and what
  metadata is exposed? How are sync conflicts and deletion handled?
- Can managed processing satisfy all project requirements and applicable law?
  Who is responsible for operations, data location and incident response?
- What governance and evidence distinguish Community, Verified and Official
  Marketplace listings without implying certification or guaranteed safety?
- Which storage adapters are required for local operation, and what interfaces
  keep them under VitaFabric's FHIR, provenance, consent and security controls?
- What accessibility and localization requirements apply to third-party apps,
  extensions and Marketplace listings?

## Outcome

Pending community, architecture, security and privacy review. The source
vision informs the proposal; this RFC makes open ownership, implementation,
policy and deployment questions explicit rather than treating its suggestions
as accepted architecture.
