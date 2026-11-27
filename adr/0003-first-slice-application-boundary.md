# ADR 0003: First-slice application boundary

- Status: proposed
- Date: 2026-11-27
- Decision makers: pending architecture and security review
- Related issues or RFCs: [RFC-0002](../rfc/0002-platform-core-architecture.md), [RFC-0007](../rfc/0007-application-framework.md), [RFC-0014](../rfc/0014-core-runtime-platform-boundaries.md), [backlog](../docs/review/LifeLedger%20RFC%20Backlog.md)

## Context

The project owner's first-slice direction calls for an integrated Health Record
without external plugins. The existing drafts describe every application as a
plugin. The exception changes an architectural boundary and must not silently
weaken the separation between product logic and platform security services.

## Decision

Proposed: ship the first Windows Health Record as a built-in application in
the local distribution, not as an external or WASM plugin. Product UI and
workflow logic remain LifeLedger responsibilities, not Platform Core
business logic. Identity, consent, capability, policy and audit enforcement
remain mandatory, and all health data passes through VitaFabric. No external
plugin runtime is required by this slice. Later plugin applications still
require reviewed contracts and isolation.

The backlog determines the requested direction; this proposed ADR does not
itself accept RFC-0014 or authorize implementation.

## Alternatives considered

Require the Health Record to be an isolated WASM plugin immediately: preserves
the original application model, but requires the unfinished plugin contracts
and runtime before the local journey can be tested. Put Health Record business
logic in Platform Core: rejected because it breaks component boundaries.

## Consequences

The built-in path avoids plugin-runtime overhead and dependency for the slice,
but does not provide plugin isolation between the application and host.
Process compromise can therefore affect the integrated application and
backend; the local IPC threat model and mandatory controls need review.
Building a later plugin path may require migration and separate compatibility
testing. This decision does not relax encryption, provenance, FHIR, local-first
operation, consent or audit requirements.
