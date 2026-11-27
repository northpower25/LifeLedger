# RFC 0019: Plugin APIs & SDK Contracts

- Status: Draft
- Owner: Plugin Platform / SDK (Rolle, Person noch zu benennen)
- Depends On: [RFC-0006 Plugin Runtime & Isolation](0006-plugin-runtime-and-isolation.md), [RFC-0007 Application Framework](0007-application-framework.md), [RFC-0009 Marketplace Governance](0009-marketplace-governance-and-trust-framework.md)

## Ziel

Normierung aller Plugin APIs.

---

## APIs

```text
Filesystem API

Event API

VitaFabric API

Identity API

Consent API

Secret API

Network API
```

---

## Plugin Manifest

Verbindliches Schema.

---

## SDK

Pflicht:

```text
Test Fixtures

Capability Tests

Compliance Suite
```

---

## Kompatibilität

Plugin muss angeben:

```text
min_version
max_version
```

---

## Marketplace-Listingstufe

Für die Listingstufen Community, Verified und Official gelten die Prüf- und
Signaturregeln aus RFC-0009. Die Stufen sind keine Zertifizierung und keine
Sicherheitsgarantie; sie ersetzen weder Isolation noch Consent- und
Capability-Enforcement.

## Manifest Schema und Permission Schema

Vorgesehen sind ein versioniertes `manifest.json` mit Paket-ID, Name,
Version, Erweiterungstyp, Entry-Component, Plattform-/WIT-
Kompatibilitätsbereich und Paket-Digest sowie ein `permissions.json` mit
expliziten Capability-IDs, Operationen, Scopes und Zwecken. Der Host
verweigert unbekannte Felder mit sicherheitsrelevanter Bedeutung,
unbekannte Capabilities und fehlende Pflichtwerte. Die Beispiele in
RFC-0004 und RFC-0006 sind illustrative Skizzen, keine gültigen Manifeste.
Ein maschinenlesbares JSON-Schema und konkrete Feldsemantik fehlen noch.

## Package Format

Das Paket enthält `plugin.wasm` als Component, Manifest, Permissions,
`signature.json` und README gemäß RFC-0006. Die Signatur muss den Digest
einer eindeutig definierten kanonischen Paketrepräsentation einschließlich
Manifest und Permissions binden; das Signaturdokument selbst darf nicht
zirkulär in den signierten Digest eingehen. Archivformat, Normalisierung,
Pfad-/Symlinkschutz, Größenlimits, Signaturalgorithmus und Trust-Bootstrap
sind noch festzulegen. Kein Paket wird vor erfolgreicher Integritäts-,
Kompatibilitäts-, Policy- und Isolationsprüfung aktiviert.

## WIT Contracts

Der Katalog in RFC-0006 umfasst Filesystem, Event, Identity, Consent,
VitaFabric, Secret und Network. Der Host prüft für jeden Import die aktuelle
Capability und gegebenenfalls Consent; Secrets bleiben hinter opaken Handles.
Network-Ziele, Redirects und DNS müssen vom Proxy geprüft werden.
Versionierte WIT-Definitionen mit Typen, Fehlern, Lifetime und Beispielen
fehlen; ein REST-Vertrag ist kein Ersatz für WIT.

## Compatibility Rules und SDK Contracts

Plugin und Host müssen für Platform API, Component ABI und jedes verwendete
WIT-Interface kompatible Versionen deklarieren; außerhalb des Bereichs wird
die Aktivierung verweigert. `min_version` und `max_version` sind bis zur
Festlegung der genauen Intervallsemantik nicht ausreichend. Breaking Changes
benötigen neue Major-Versionen, Migration und dokumentierte
Unterstützungsfristen. SDK-Sprachen, Generatorversionen und konkrete
asynchrone Fehler-/Cancellation-Semantik sind offen.

## Compliance Suite

Vor Freigabe sind unabhängig ausführbare synthetische Tests für Manifest und
Signatur, ungültige Versionen, verweigerte Capabilities und Consent,
Widerruf während eines Aufrufs, isoliertes Dateisystem, Netzwerkumgehung,
Secret-Leaks, Ressourcenlimits, Event-Duplikate und Host-Absturz erforderlich.
Fixtures, Referenz-SDK und WIT-Dateien sind noch nicht implementiert.
Listing oder bestandene Suite ersetzt keine kontinuierliche Isolation.
