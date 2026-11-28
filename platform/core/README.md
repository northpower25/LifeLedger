# Platform Core

The first local implementation responsibilities are Owner identity/session,
offline TOTP, consent, capability checks and audit. Their test-slice
implementation currently lives in the FastAPI composition under
`backend/lifeledger/`; health-resource storage and access remain behind
VitaFabric.

This is not a production security boundary until the Windows host/service
channel is mutually authenticated and the same-user threat model has been
tested. See the [slice implementation contract](../../docs/implementation/first-offline-slice.md).
