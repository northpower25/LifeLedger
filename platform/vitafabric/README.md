# VitaFabric

VitaFabric is the health-data interoperability and data platform within the
proposed LifeLedger Platform. It is intended to own health-data access,
connectors, FHIR R4 mapping, provenance, synchronization, data quality and
storage abstraction. It is the only health-data gateway: applications,
integrations, AI features and plugins must use its approved contracts and
must not access a database directly.

Connector and storage adapters are controlled VitaFabric extension points,
not a bypass around its FHIR, provenance, consent and security requirements.
This is a design placeholder: no endpoints, conformance claims, or integrations
exist yet.

Part of the LifeLedger Platform Architecture: LifeLedger, VitaFabric, and LifeWeaver.
