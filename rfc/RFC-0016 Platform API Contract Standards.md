# RFC-0016: Platform API Contract Standards

Status: Draft

## Ziel

Einheitliche APIs für:

- Identity
- Consent
- VitaFabric
- Event Bus
- Applications

---

## API Regeln

Pflicht:

```text
REST
OpenAPI 3.1
JSON
Versionierung
```

---

## URL Schema

```text
/api/v1/
```

---

## Fehlerformat

```json
{
  "error": {
    "code": "CONSENT_DENIED",
    "message": "..."
  }
}
```

---

## Versionierung

```text
v1
v2
v3
```

keine stillen Breaking Changes.

---

## Audit Pflicht

Alle mutierenden APIs:

```text
POST
PUT
PATCH
DELETE
```

müssen Audit Events erzeugen.
