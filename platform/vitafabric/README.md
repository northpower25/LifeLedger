# VitaFabric

VitaFabric is the health-data interoperability and data platform within the
proposed LifeLedger Platform. It is intended to own health-data access,
connectors, FHIR R4 mapping, provenance, synchronization, data quality and
storage abstraction. It is the only health-data gateway: applications,
integrations, AI features and plugins must use its approved contracts and
must not access a database directly.

Connector and storage adapters are controlled VitaFabric extension points,
not a bypass around its FHIR, provenance, consent and security requirements.
The first offline-slice gateway is implemented in the local FastAPI service
under `backend/lifeledger/`: it owns the three allowed FHIR R4 resource paths,
validation, provenance, Consent/Capability checks, encrypted SQLite payload
storage and timeline reads. This is a narrow synthetic-data implementation,
not a full FHIR profile or HL7-validator conformance claim. No other component
may access the SQLite health-resource tables directly.

The Windows packaging and IPC boundary are not yet verified. See the
[implementation contract](../../docs/implementation/first-offline-slice.md)
for the exact limits and acceptance plan.

Part of the LifeLedger Platform Architecture: LifeLedger, VitaFabric, and LifeWeaver.
