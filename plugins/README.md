# Plugin ecosystem

The platform vision proposes a secure extension ecosystem for applications,
integrations and optional AI capabilities. Draft
[RFC-0002](../rfc/0002-platform-core-architecture.md) proposes a
WASM-first plugin runtime (with a possible later Python connector runtime),
but no plugin API, runtime, marketplace, or security boundary is implemented
or accepted yet.

The following plugin types are proposals; ownership follows the platform's
existing component responsibilities:

| Proposed type | Responsibility boundary |
| --- | --- |
| Connector | VitaFabric owns connector execution, FHIR mapping, provenance and health-data exchange (for example, wearable or health-app sources). |
| Integration | Connects external systems through approved platform APIs; any health data must pass through VitaFabric. |
| Provider | LifeWeaver owns provider-neutral AI adapters for local or external models. A provider must not become a dependency of the LifeLedger core. |
| Storage | Storage adapters are controlled VitaFabric storage abstractions (illustrative backends include SQLite, PostgreSQL, OneDrive, S3 and Nextcloud), not extensions with direct database access. Any cloud storage option requires separate privacy and security review. |
| UI | LifeLedger presentation extensions, such as dashboards, widgets and views, use approved UI contracts and access data only through platform APIs. |
| Application | Independent applications, such as medication, sleep, nutrition or sports-analysis apps, use versioned platform APIs; health data still passes through VitaFabric and consent enforcement. |

Every extension is untrusted by default. A future contract is expected to
cover a manifest, declared capabilities, least privilege, explicit consent,
revocation, package integrity/signature, provenance and enforceable isolation.
A manifest or signature alone is not a security guarantee; each control must
be demonstrated on supported platforms before third-party extensions run.

A possible Marketplace may provide discovery and distribution, with proposed
Community, Verified and Official listings. The meanings, governance and
verification process are undecided; no listing label can promise safety or
replace user review and consent. Local installation and core functionality
must not depend on a central Marketplace.

See the [plugin roadmap](../docs/roadmap/plugins.md) and
[platform-direction RFC](../rfc/0001-platform-direction.md).
RFC-0002 additionally proposes that plugins request explicit capabilities,
with no implicit rights; Consent Enforcement, Audit, authentication, the
FHIR core model and Capability Enforcement remain platform responsibilities
and cannot be delegated to plugins. Applications have no separate health-data
database, and storage adapters must never receive plaintext health data or
keys. These are draft requirements pending review and implementation.
