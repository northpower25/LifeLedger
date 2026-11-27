# RFC-0017: Event Schemas & Messaging Contracts

Status: Draft

## Ziel

Normierung aller Events.

---

## Event Format

```json
{
  "event_id": "",
  "event_type": "",
  "version": "",
  "timestamp": ""
}
```

---

## Kategorien

```text
IDENTITY

CONSENT

FHIR

PLUGIN

SYNC

AI

SECURITY
```

---

## Versionierung

```text
FHIR_CREATED.v1
FHIR_CREATED.v2
```

---

## Compatibility

Consumer müssen:

```text
n
n-1
```

unterstützen.
