# RFC 0016: Platform API Contract Standards

- Status: Draft
- Owner: Platform API (Rolle, Person noch zu benennen)
- Depends On: [RFC-0002 Platform Core Architecture](0002-platform-core-architecture.md), [RFC-0007 Application Framework](0007-application-framework.md)

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

Alle mutierenden APIs sowie lesende Zugriffe auf Gesundheitsdaten:

```text
POST
PUT
PATCH
DELETE
GET (geschützte Gesundheitsdaten)
```

müssen Audit Events erzeugen.

## OpenAPI und Transportgrenzen

`/api/v1/` gilt für lokale HTTP-Schnittstellen zwischen vertrauensgetrennten
Prozessen. OpenAPI 3.1 beschreibt deren Requests, Responses,
Authentisierung, Fehler und Versionsstand. Interne Funktionsaufrufe und
Plugin-WIT sind nicht automatisch HTTP; sie erfüllen dieselben Policy- und
Audit-Invarianten mit eigenen Verträgen. Vor Umsetzung muss ein
maschinenlesbares OpenAPI-Dokument einschließlich der in RFC-0018 genannten
Operationen und einer Policy-Matrix veröffentlicht werden.

## Auth und Fehler

Jede geschützte Anfrage benötigt eine gültige Sitzung und wird zusätzlich
nach Consent, Capability und Policy geprüft. Das Host-/Service-IPC benötigt
eigene gegenseitige Authentisierung (RFC-0002); ein Browser-Origin oder
Loopback allein ist keine Identität. Fehler enthalten einen stabilen
maschinenlesbaren `code`, einen lokalisierbaren Schlüssel und eine opake
Korrelations-ID, aber keine Gesundheitsdaten, Zugangsdaten oder Stacktraces.

| HTTP | Bedeutung |
| --- | --- |
| 400 / 422 | fehlerhafte Anfrage / Validierung fehlgeschlagen |
| 401 / 403 | keine gültige Sitzung / Consent oder Policy verweigert |
| 404 | nicht verfügbar; keine unautorisierte Existenzoffenlegung |
| 409 | Versions- oder Zustandskonflikt |
| 429 | Rate-/Ressourcenlimit |
| 500 / 503 | interner Fehler / Pflichtdienst nicht verfügbar |

Fehlerdetails, Statuscodes je Operation, Pagination, Idempotenz und
Konkurrenzkontrolle sind im OpenAPI-Vertrag pro Endpoint auszuweisen.
Zeitpunkte sind mit Zeitzone zu übertragen; Oberflächentexte werden
lokalisiert.

## Audit und Versioning

Geschützte Lesezugriffe und Mutationen werden mit Actor, Zweck,
Ressourcenkategorie, Entscheidung, Zeit und opaker Korrelations-ID
protokolliert, ohne Gesundheitsinhalt. Erfolgreiche Mutationen und Audit
werden atomar gespeichert; bei nicht verfügbarem Pflicht-Audit kein Zugriff.
Breaking Changes benötigen eine neue API-Major-Version; unterstützte
Übergangsfristen, Deprecation und Schema-Kompatibilität müssen vor
Veröffentlichung festgelegt werden. Dieses RFC allein ist kein OpenAPI-Artefakt.
