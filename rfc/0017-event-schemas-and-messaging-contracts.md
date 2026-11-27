# RFC 0017: Event Schemas & Messaging Contracts

- Status: Draft
- Owner: Platform Event Bus (Rolle, Person noch zu benennen)
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
  "timestamp": "2027-01-01T10:00:00Z",
  "source": "vitafabric",
  "subject": "opaque-resource-id"
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
backup
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

## JSON Schema und Registry

Der Envelope enthält verpflichtend `event_id`, `event_category`,
`event_name`, positive ganzzahlige `event_version`, abgeleiteten
`event_type`, UTC-`timestamp`, `source` und opakes `subject`, entsprechend
RFC-0005. Event-ID ist stabil über Wiederholungen, Typ und Quellfelder müssen
übereinstimmen. Payload und zusätzliche Felder müssen pro registriertem Typ
explizit spezifiziert werden und dürfen keine Gesundheitsinhalte oder
Geheimnisse transportieren. Die Registry ordnet Typ, Version, Owner,
JSON-Schema, Producer, berechtigte Consumer und Retentionzweck zu.

Vor Nutzung sind maschinenlesbare JSON-Schemas mit festgelegtem Dialekt,
Formatprüfung und synthetischen Positiv-/Negativfixtures unter
`specifications/` zu veröffentlichen. Die obige Illustration ist kein Schema;
das konkrete ID-Format und Pflicht-Korrelationsfelder sind noch zu beschließen.
Die sechs Slice-Eventtypen sind in RFC-0005 benannt, ihre ausführbaren Schemas
und Producer-/Consumer-Verträge fehlen.

## Compatibility Rules

Bei Version 1 existiert kein `n-1`; ein Consumer unterstützt v1. Ab v2
unterstützt er die aktuelle und unmittelbar vorherige veröffentlichte
Version, solange diese für Replay innerhalb der Retention freigegeben ist.
Versionsnummern werden nicht übersprungen; eine Entfernung alter Versionen
benötigt einen dokumentierten Migrations- oder Replayplan. Unbekannte
Versionen werden abgelehnt oder sichtbar in die DLQ geleitet.
Zustellung, Deduplizierung und Retention folgen RFC-0005.
