# RFC 0017: Event Schemas & Messaging Contracts

- Status: Draft
- Depends On: [RFC-0005 Event Bus Architecture](0005-event-bus-architecture.md)

## Ziel

Normierung aller Events.

---

## Event Format

RFC-0005 ist die normative Quelle für Event-Kategorien, Namen, Routing und
Sicherheitsanforderungen. Dieses RFC definiert die Schema-Kompatibilität. Der
serialisierte Event-Envelope verwendet `event_category`, `event_name` und
`event_version` als Ganzzahl; `event_type` folgt dem Format
`<category>.<name>.v<version>`.

```json
{
  "event_id": "",
  "event_category": "fhir",
  "event_name": "created",
  "event_version": 1,
  "event_type": "fhir.created.v1",
  "timestamp": ""
}
```

---

## Kategorien

```text
identity
consent
household
fhir
import
sync
plugin
security
ai
application
```

---

## Versionierung

```text
fhir.created.v1
fhir.created.v2
```

---

## Compatibility

Ein Consumer muss für jeden abonnierten Eventtyp die aktuelle und die
vorherige unterstützte Schema-Version (`n` und `n-1`) verarbeiten können.
Unbekannte oder nicht unterstützte Versionen werden sicher abgelehnt oder in
die Dead-Letter-Queue geleitet; sie dürfen nicht still ignoriert werden.
Inkompatible Änderungen erhöhen die Event-Version. Diese Kompatibilitätsregel
ändert weder die Kategorie-/Namenskonvention noch die Ownership aus RFC-0005.
