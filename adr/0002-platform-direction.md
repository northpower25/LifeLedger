# ADR 0002: Platform framing and deployment scenarios

- Status: proposed
- Date: 2026-11-26
- Decision makers: pending architecture and community review
- Related issues or RFCs: [RFC 0001](../rfc/0001-platform-direction.md),
  [RFC-0002](../rfc/0002-platform-core-architecture.md)

## Context

The platform vision proposes a reusable platform, a first health-record
reference application, a shared Identity & Consent layer, six plugin types,
a Marketplace and several deployment scenarios. Existing principles and
component responsibilities remain binding; detailed contracts, policy,
service placement and the feasibility of optional cloud processing have not
been established.

## Decision

Proposed, not yet accepted: use LifeLedger Platform as an umbrella framing,
with the personal health record as its first reference application. Retain
LifeLedger, VitaFabric and LifeWeaver responsibilities. Treat Identity &
Consent as a shared cross-cutting platform capability covering user, family
and delegate identity, grants, roles, emergency access and application,
plugin, AI and sync permissions. Separate authentication from authorization
and consent; access decisions must be enforced at data boundaries, including
VitaFabric. Define the policy and ownership before implementation.

Adopt connector, integration, provider, storage, UI and application as
proposed plugin categories, not as pre-approved contracts. Health-data
connectors and storage adapters remain under VitaFabric; AI-provider adapters
under LifeWeaver; UI and application experiences under LifeLedger. No
extension has direct database access. A possible Marketplace may use
Community, Verified and Official listing classes only after governance and
evidence criteria are agreed; listings do not imply safety or consent.

Draft RFC-0002 further proposes a Core Runtime containing identity and consent,
security services, an event bus, a plugin host, a secret store and audit
services. It proposes explicit capabilities and a WASM-first plugin runtime.
These remain draft choices pending review; normative contracts and
implementation ownership are not established. Design shared capabilities and
optional deployment scenarios through reviewed RFCs and versioned
specifications rather than assuming implementation. Local operation remains
mandatory; no deployment mode may bypass consent, VitaFabric, FHIR or the
other accepted principles in
[ADR 0001](0001-project-principles.md).

## Alternatives considered

Retain the health-record-first framing; require central cloud or a mandatory
registry; or decide service placement before data and trust boundaries are
known. The RFC describes trade-offs. Mandatory central services conflict with
local operation; other alternatives remain open for review.

## Consequences

The platform framing can guide a reference application and independently
testable extension contracts, but creates work to define Identity & Consent
policy, ownership, isolation, privacy, security and interoperability. Optional
relay, zero-knowledge sync, Marketplace and managed cloud need separate
threat models, approvals and evidence; this proposal neither authorizes cloud
processing nor changes existing requirements. No implementation or
production readiness is implied.
