# RFC 0004: Capability & Permission Model

- Status: Draft
- Type: Architecture RFC
- Owner: Platform Core
Depends On: RFC-0002 Platform Core Architecture  
Depends On: RFC-0003 Identity & Consent Framework  
Blocks: RFC-0006, RFC-0007, RFC-0009, RFC-0011

---

## 1. Zusammenfassung

Dieses RFC definiert das Capability- und Berechtigungsmodell der LifeLedger Plattform.

Während RFC-0003 beschreibt:

```text
Wer darf?
```

beschreibt dieses RFC:

```text
Was darf?
```

Capabilities sind die technische Grundlage für:

- Plugins
- Anwendungen
- Integrationen
- Provider
- AI-Komponenten
- APIs

Capabilities werden technisch erzwungen.

Sie sind keine UI-Hinweise.

Sie sind keine freiwilligen Deklarationen.

---

## 2. Ziele

### Ziele

```text
Least Privilege

Technische Durchsetzung

Explizite Rechte

Unabhängigkeit von UI

Auditierbarkeit

Plugin-Sicherheit
```

---

### Nichtziele

```text
Business Rollen

Familienbeziehungen

Consent Management

Authentifizierung
```

Diese Bereiche werden durch RFC-0003 geregelt.

---

## 3. Architekturprinzipien

### Default Deny

Jede Capability ist verboten.

Freigaben erfolgen explizit.

```text
Default = Deny
```

---

### Capability Based Security

Plugins erhalten niemals:

```text
Admin
PowerUser
Trusted
```

sondern konkrete Fähigkeiten.

---

### Consent + Capability

Zugriff benötigt beide Bedingungen.

```text
Capability vorhanden

UND

Consent vorhanden
```

---

## 4. Sicherheitsmodell

### Zugriffspfad

```text
Request

↓

Identity

↓

Consent

↓

Capability

↓

Resource Access
```

Alle Prüfungen sind verpflichtend.

---

### Beispiel

```text
Plugin

READ_MEDICATION

+

Consent

=

Zugriff erlaubt
```

---

```text
Plugin

READ_MEDICATION

ohne Consent

=

Zugriff verweigert
```

---

## 5. Capability Ebenen

Die Plattform verwendet vier Capability-Ebenen.

---

## 6. FHIR Capabilities

### Read

```text
READ_PATIENT

READ_OBSERVATION

READ_CONDITION

READ_MEDICATION

READ_ALLERGY

READ_DOCUMENT

READ_TIMELINE

READ_PROVENANCE
```

---

### Write

```text
WRITE_OBSERVATION

WRITE_DOCUMENT

WRITE_MEDICATION

WRITE_CONDITION
```

---

### Administrative Datenoperationen

```text
MERGE_RECORDS

DELETE_RECORDS

EXPORT_DATA
```

---

## 7. Plattform Capabilities

### Netzwerk

```text
NETWORK_ACCESS
```

Erlaubt:

```text
HTTP
HTTPS
Websocket
```

---

### Datei Zugriff

```text
LOCAL_STORAGE_READ

LOCAL_STORAGE_WRITE
```

---

### Kamera

```text
CAMERA_ACCESS
```

---

### Benachrichtigungen

```text
NOTIFICATION_ACCESS
```

---

### Hintergrundprozesse

```text
BACKGROUND_TASKS
```

---

## 8. KI Capabilities

### Lokale KI

```text
AI_LOCAL_MODEL
```

---

### Remote KI

```text
AI_REMOTE_PROVIDER
```

---

### Embeddings

```text
AI_EMBEDDING

READ_EMBEDDINGS
```

`AI_EMBEDDING` betrifft die Embedding-Funktion; `READ_EMBEDDINGS`
autorisiert das Lesen gespeicherter Embeddings. Auch dafür gelten Consent
und die VitaFabric-Datenverträge für Derived Data gemäß RFC-0013.

---

### RAG

```text
AI_RAG
```

---

### Agenten

```text
AI_AGENT
```

---

## 9. Administrative Capabilities

### Consent und Household

```text
MANAGE_CONSENT

MANAGE_HOUSEHOLD
```

Diese Capabilities ersetzen weder eine gültige Einwilligung noch die
Prüfung der jeweiligen Identität und Vertretungsbefugnis.

---

### Benutzerverwaltung

```text
USER_MANAGEMENT
```

---

### Plugin Installation

```text
PLUGIN_INSTALL
```

---

### Plugin Signierung

```text
PLUGIN_SIGN
```

---

### Audit Zugriff

```text
AUDIT_VIEW
```

---

### Notfallzugriff

```text
EMERGENCY_ACCESS
```

---

## 10. Capability Bundles

Zur Vereinfachung dürfen Bundles definiert werden.

---

### Health Viewer

```text
READ_PATIENT
READ_OBSERVATION
READ_DOCUMENT
```

---

### Import Connector

```text
WRITE_OBSERVATION
READ_PATIENT
NETWORK_ACCESS
```

---

### AI Assistant

```text
READ_DOCUMENT
AI_LOCAL_MODEL
AI_RAG
```

---

Bundles erzeugen keine Sonderrechte.

Sie aggregieren Fähigkeiten.

---

## 11. Plugin Manifest

Jedes Plugin muss Capabilities deklarieren.

Beispiel:

```json
{
  "id": "garmin_connector",
  "capabilities": [
    "READ_PATIENT",
    "WRITE_OBSERVATION",
    "NETWORK_ACCESS"
  ]
}
```

---

## 12. Capability Review

### Community

Selbstdeklaration.

Keine Prüfung.

---

### Verified

Review durch Maintainer.

---

### Official

Pflichtprüfung.

Die Prüfungstiefe folgt der höchsten Capability-Risikostufe aus §17.
Capabilities der Stufen Hoch und Kritisch benötigen dokumentierte
Sicherheitsprüfung; Kritisch erfordert zusätzlich zwei unabhängige Reviewer.
Eine Community-Selbstauskunft oder Marketplace-Einstufung vergibt niemals
selbst einen Grant und ersetzt nicht die explizite Nutzerfreigabe oder das
Host Enforcement.

---

## 13. Durchsetzung

### Host Enforcement

Capabilities werden nicht durch Plugins geprüft.

Sie werden durch den Plattformhost geprüft.

---

### Beispiel

Nicht erlaubt:

```text
Plugin

↓

Dateizugriff
```

---

Erlaubt:

```text
Plugin

↓

Capability Check

↓

Filesystem API

↓

Zugriff
```

---

## 14. Capability APIs

Jede Plattform-API muss definieren:

```text
Benötigte Capability
```

Beispiel:

```text
getObservation()

→ READ_OBSERVATION
```

---

```text
storeMedication()

→ WRITE_MEDICATION
```

---

## 15. Revocation

Capabilities können widerrufen werden.

---

### Folgen

```text
Plugin Neustart

Session Invalidierung

Token Invalidierung
```

---

## 16. Audit Anforderungen

Jede Nutzung protokolliert:

```text
Plugin
User
Capability
Resource
Zeitpunkt
Ergebnis
```

---

## 17. Capability Risk Levels

Das Risiko wird für jede Capability anhand der Sensitivität der erreichbaren
Daten, des möglichen Schadens, der Reichweite und der Umkehrbarkeit einer
Aktion bewertet. Die höchste zutreffende Stufe gilt. Bundles erben die höchste
Stufe ihrer enthaltenen Capabilities; sie dürfen eine Einstufung nicht
absenken.

| Stufe | Mindestfreigabe | Review vor Freigabe | Audit |
|---|---|---|---|
| Niedrig | Nutzerfreigabe pro Plugin oder App | Automatisierte Manifest- und Kompatibilitätsprüfung | Installation, Freigabe und Nutzung |
| Mittel | Explizite Nutzerfreigabe mit Zweck und Datenumfang | Maintainer-Review bei Marketplace-Listing; erneute Prüfung bei Scope-Änderung | Jede Ressourcennutzung mit Ergebnis |
| Hoch | Explizite, widerrufbare Nutzerfreigabe je Datenkategorie und Empfänger | Sicherheitsreview und Review durch zwei voneinander unabhängige Reviewer für Verified/Official Listings | Jede Nutzung, jeder Export und jede Änderung mit Akteur, Scope, Zeit und Ergebnis |
| Kritisch | Schrittweise Nutzerbestätigung je Vorgang; keine unbeaufsichtigte oder gebündelte Freigabe | Sicherheits- und Governance-Freigabe durch zwei unabhängige Reviewer; kritische Fähigkeit standardmäßig nicht an Drittanbieter-Erweiterungen vergeben | Unveränderlicher Audit-Eintrag, einschließlich Ablehnung und Widerruf |

| Capability-Beispiel | Mindeststufe |
|---|---|
| `NOTIFICATION_ACCESS` | Niedrig |
| `READ_DOCUMENT`, `READ_OBSERVATION`, `READ_EMBEDDINGS` | Hoch |
| `WRITE_OBSERVATION`, `EXPORT_DATA` | Hoch |
| `READ_PATIENT`, `AI_REMOTE_PROVIDER`, `MANAGE_HOUSEHOLD` | Hoch |
| `DELETE_RECORDS`, `MANAGE_CONSENT`, `EMERGENCY_ACCESS`, `USER_MANAGEMENT`, `PLUGIN_SIGN` | Kritisch |

Die Beispiele sind Mindeststufen. Ein konkreter Anwendungsfall darf höher,
aber nicht niedriger eingestuft werden. Unbekannte oder nicht bewertete
Capabilities bleiben gesperrt. Eine Nutzerfreigabe ersetzt weder Consent
gemäß RFC-0003 noch Host Enforcement oder die unabhängige Sicherheitsprüfung.

### Genehmigungs- und Reviewprozess

1. Der Capability-Eigentümer dokumentiert Datenklasse, Zweck, Empfänger,
   Reichweite, Widerruf und Schadensauswirkung.
2. Der Host prüft die Einstufung und verweigert nicht katalogisierte
   Capabilities (Default Deny).
3. Die Freigabe erfordert mindestens die oben angegebene Nutzerbestätigung.
   Für Marketplace-Einstufungen gelten zusätzlich die unabhängigen Reviews
   aus RFC-0009.
4. Scope- oder Verhaltensänderungen lösen eine Neubewertung aus. Beim
   Entfernen einer Capability werden aktive Grants und Tokens widerrufen.

Der Audit-Eintrag enthält mindestens Capability-ID, Erweiterungs- und
Nutzer-ID, Ressourcenkategorie, Entscheidung, Reviewer/Freigebenden und
Zeitpunkt. Audit-Datensätze dürfen keine Gesundheitsinhalte oder Geheimnisse
enthalten. Aufbewahrung und Zugriff auf Auditdaten folgen RFC-0012 und den
geltenden Datenschutzanforderungen.

---

## 18. Sicherheitsanforderungen

Pflicht:

```text
Host Enforcement

Audit Logging

Revocation

Consent Integration

Least Privilege
```

---

Nicht zulässig:

```text
Capability nur im Frontend prüfen

Capability im Plugin prüfen

Capability deklarieren aber nicht erzwingen
```

---

## 19. Migrationsstrategie

V1:

```text
statische Capability Listen
```

---

V2:

```text
Capability Bundles
```

---

V3:

```text
Kontextabhängige Capabilities
```

---

## 20. Architekturentscheidung

Dieses RFC legt fest:

✅ Default Deny

✅ Capability Based Security

✅ Consent + Capability erforderlich

✅ Vier Capability Ebenen

✅ Host Enforcement

✅ Audit Pflicht

✅ Plugin Manifest Pflicht

✅ Capability Revocation

✅ Bundle Unterstützung

✅ Plattformweite Durchsetzung
