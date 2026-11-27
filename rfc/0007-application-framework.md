# RFC 0007: Application Framework

- Status: Draft
- Type: Architecture RFC
- Owner: LifeLedger Platform
Depends On: RFC-0002 Platform Core Architecture  
Depends On: RFC-0003 Identity & Consent Framework  
Depends On: RFC-0004 Capability & Permission Model  
Depends On: RFC-0005 Event Bus Architecture  
Depends On: RFC-0006 Plugin Runtime & Isolation

Blocks:
- RFC-0008 Family Model
- RFC-0011 AI Provider & Health Twin
- Referenzanwendungen
- Marketplace Apps

---

## 1. Zusammenfassung

Dieses RFC definiert das Anwendungsmodell der LifeLedger Plattform.

Die Plattform unterscheidet zukünftig zwischen:

```text
Plattform

und

Anwendungen
```

LifeLedger Health Record ist die erste Referenzanwendung.

Weitere Anwendungen dürfen unabhängig entstehen ohne Änderungen an:

```text
Core Runtime

Identity

Consent

VitaFabric

LifeWeaver
```

Die Plattform entwickelt sich dadurch vom Einzelprodukt zur erweiterbaren Gesundheitsdatenplattform. Die Notwendigkeit eines eigenständigen Application Frameworks ergibt sich direkt aus der Plattformvision, dem Plugin-Modell und der Trennung zwischen Plattform und Referenzanwendung.

---

## 2. Ziele

### Ziele

```text
Anwendungsunabhängigkeit

Erweiterbarkeit

Wiederverwendbare Plattformdienste

Pluginfähige Apps

Einheitliches Berechtigungssystem

Gemeinsame UI-Muster

Gemeinsame Datenbasis
```

---

### Nichtziele

```text
Eigene Gesundheitsdatenbanken

Eigene Authentifizierung

Direkte FHIR Implementierungen

Parallele Consent Modelle
```

---

## 3. Grundprinzipien

### Plattform First

Anwendungen sind Gäste der Plattform.

Nicht umgekehrt.

---

### Shared Services

Gemeinsame Plattformdienste:

```text
Identity

Consent

Audit

Notifications

Event Bus

Secrets

VitaFabric
```

---

### Data Through VitaFabric

Alle Gesundheitsdaten laufen über VitaFabric.

---

## 4. Definition einer Application

Erweiterbare Applications sind als spezialisierte Plugin-Typen mit UI,
Navigation, Workflows und Settings vorgesehen. Der integrierte Health Record
des ersten Slice ist die in [ADR-0003](../adr/0003-first-slice-application-boundary.md)
vorgeschlagene Ausnahme. In beiden Fällen gelten die Plattformprüfungen.

---

### Bestandteile

```text
UI

Navigation

Settings

Workflows

Capabilities
```

---

## 5. Was eine Application NICHT besitzt

Verboten:

```text
Eigene Gesundheitsdatenbank

Eigene Authentifizierung

Eigene Consent Engine

Eigene Audit Logs

Eigene Benutzerverwaltung
```

---

## 6. Application Architektur

```text
Application

├── UI
├── Routes
├── Settings
├── Workflows
├── Permissions
└── Platform Integrations
```

---

## 7. Datenfluss

Verpflichtender Pfad:

```text
Application

↓

Capabilities

↓

Consent

↓

VitaFabric

↓

FHIR
```

---

Nicht zulässig:

```text
Application

↓

Datenbank
```

---

## 8. Erste Referenzanwendungen

### Phase 1

```text
Health Record
```

## Health Record Execution Model

Der erste Health Record ist ein integrierter Anwendungsteil der lokalen
Distribution, kein externes oder isoliert auszuführendes Plugin. „Im Kern“
bezeichnet hier die gemeinsame Distribution, nicht die Verlagerung von
Produktlogik in den Platform Core. Zugriffe gehen weiterhin über Identity,
Consent, Capability, Policy und VitaFabric. Ein späterer Plugin-Pfad benötigt
eigene Verträge und Review; siehe ADR-0003.

## First User Journey

Dokument importieren → Patient anlegen → Medikation anlegen → Timeline
anzeigen → Backup erstellen. Ein vor dem Patienten ausgewähltes Dokument
muss bis zur gültigen Zuordnung sicher behandelt werden; Art der temporären
Ablage und Abbruchverhalten sind noch offen. Alle Daten sind synthetisch.
Die Ressourcen sind `Patient`, `DocumentReference` und
`MedicationStatement`, nicht `Observation`. Details zu Dokumentformat,
Größe und Timeline-Sortierung stehen noch aus.

## Backup Scope

Das lokale Backup muss für die Wiederherstellung des Slice konsistent
Patient, MedicationStatement, DocumentReference, Dokumentoriginale,
Provenienz sowie die zur Wiederherstellung benötigten Identity-, Consent-,
Capability-, Audit- und Schema-/Versionsinformationen berücksichtigen.
Es ist verschlüsselt und darf keine Klartextschlüssel oder Credentials
enthalten. Backup und Restore unterliegen eigenen Zugriffsprüfungen; Wieder-
herstellung darf Widerrufe oder Löschungen nicht stillschweigend rückgängig
machen. Schlüssel-/Recovery-Verfahren, genaue Inhalte, atomare Konsistenz,
Aufbewahrung und Umgang mit einem älteren Stand sind noch festzulegen.
Ein erfolgreicher Restore ist vorgeschlagen, aber noch nicht als Abnahme
bestätigt.

---

### Phase 2

```text
Medication Manager

Emergency Profile
```

---

### Phase 3

```text
Family Health

Health Dashboard
```

---

### Phase 4

```text
Sleep Tracker

Nutrition Tracking

Fitness Analytics
```

---

## 9. Navigation

Die Plattform stellt globale Navigation bereit.

---

### Jede App erhält

```text
App Titel

Icon

Version

Capabilities

Settings
```

---

### Beispiel

```text
LifeLedger

├── Health Record
├── Medication Manager
├── Family Health
└── Settings
```

---

## 10. Routing

Anwendungen definieren eigene Routen.

---

Beispiel:

```text
/health

/medication

/family

/emergency
```

---

## 11. Capability Modell

Capabilities stammen ausschließlich aus RFC-0004.

Eine Anwendung definiert:

```text
Benötigte Capabilities
```

---

Beispiel

```json
{
  "requiredCapabilities": [
    "READ_PATIENT",
    "READ_DOCUMENT"
  ]
}
```

---

## 12. Consent Integration

Anwendungen dürfen Consent nicht direkt prüfen.

Die Plattform prüft:

```text
Identity

Consent

Capability
```

---

## 13. Event Bus Integration

Anwendungen kommunizieren über den Event Bus.

---

### Subscribe

```text
FHIR_CREATED

FHIR_UPDATED

CONSENT_REVOKED
```

---

### Publish

```text
WORKFLOW_STARTED

WORKFLOW_COMPLETED
```

---

## 14. Application Settings

Jede Anwendung besitzt:

```text
Lokale Einstellungen

Layout

Filter

Darstellung
```

---

Nicht zulässig:

```text
Authentication Settings

Consent Ownership

FHIR Core Config
```

---

## 15. Internationalisierung

Pflicht:

```text
Deutsch

Englisch
```

wie in den Produktzielen vorgesehen.

---

### Anforderungen

```text
i18n Ressourcen

Datumsformate

Zeitzonen

Lokalisierbare Fehler
```

---

## 16. Accessibility

Mindestanforderungen:

```text
Tastaturnavigation

Screen Reader Unterstützung

Kontrastanforderungen

Skalierbarkeit
```

---

Ziel:

```text
WCAG 2.2 AA
```

---

## 17. Marketplace Integration

Anwendungen sind Marketplace-fähig.

---

Verfügbare Kategorien:

```text
Community

Verified

Official
```

---

## 18. Application Lifecycle

### Installation

```text
Manifest prüfen

Capabilities prüfen

Registrieren
```

---

### Aktivierung

```text
Navigation registrieren

Events abonnieren

UI laden
```

---

### Update

```text
Kompatibilität prüfen

Migration ausführen
```

---

### Entfernung

```text
Routes entfernen

Subscriptions beenden

Settings löschen
```

### Dependency Management

Eine Application deklariert direkte Abhängigkeiten auf versionierte
Plattform-APIs und andere Applications. Abhängigkeiten müssen im Manifest
aufgelistet und gegen einen veröffentlichten Kompatibilitätsbereich geprüft
werden. Die Installation erzeugt ein Lockfile mit exakten Versionen und
Paket-Digests; Laufzeitauflösung, transitive Zyklen und stiller Download
fehlender Abhängigkeiten sind verboten. Optionale Abhängigkeiten müssen
explizit gekennzeichnet sein und dürfen den sicheren Start ohne das Feature
nicht verhindern.

### Migration und Upgrade

Jede persistente Application-Einstellung erhält eine Schema-Version.
Migrationen sind versioniert, deterministisch, idempotent und werden lokal
vor Aktivierung des neuen Pakets ausgeführt. Vor Migration oder Upgrade wird
ein wiederherstellbarer Zustand gesichert. Schlägt Vorprüfung, Migration oder
Health Check fehl, bleiben die alte Version und ihre Daten aktiv; ein
automatischer Fallback auf eine nicht geprüfte Version ist ausgeschlossen.
Eine Datenmigration wird erst nach erfolgreicher Validierung atomar
übernommen. Rollback umfasst Paket, Manifest und Application-eigene
Einstellungen; Plattformdaten bleiben VitaFabric zugeordnet und werden nicht
durch App-Migrationen verändert.

### Upgrade-Strategie und Kompatibilitätsmatrix

Ein Upgrade durchläuft: Signatur- und Digest-Prüfung, Abhängigkeits- und
Kompatibilitätsprüfung, Backup, Migration im isolierten Staging, Health
Check, atomare Aktivierung. Ohne Netzwerk muss ein bereits bezogenes,
verifiziertes Paket installierbar und rückrollbar bleiben.

| Schnittstelle | Manifest deklariert | Upgrade-Regel |
|---|---|---|
| Application Manifest | Manifest-Schema-Version | Unbekannte Major-Version ablehnen |
| Platform API | unterstützter API-Bereich | Nur tatsächlich unterstützte Version aktivieren |
| Plugin ABI/WIT | ABI-Version | Inkompatible ABI erfordert neues Paket |
| App-Daten | eigene Schema-Version | Migration vor Aktivierung; Rollback muss möglich sein |

Die konkrete API-Unterstützungsmatrix wird pro Plattformrelease veröffentlicht.
Ein Release darf nur Applications als kompatibel markieren, für die
Konformitätstests mit dem deklarierten API-Bereich bestanden wurden.

---

## 19. Versionsmodell

Jede Anwendung besitzt:

```text
App Version

Manifest Version

API Compatibility Version
```

---

## 20. App Manifest

Beispiel:

```json
{
  "id": "medication_manager",
  "name": "Medication Manager",
  "version": "1.0.0",
  "type": "application",
  "capabilities": [
    "READ_MEDICATION",
    "WRITE_MEDICATION"
  ]
}
```

---

## 21. Familienfähigkeit

Anwendungen müssen mehrbenutzerfähig sein.

Vorbereitung für RFC-0008.

---

Unterstützte Bereiche:

```text
Owner

Guardian

Caregiver

Proxy
```

---

## 22. Health-Twin Integration

Anwendungen dürfen optionale LifeWeaver Funktionen nutzen.

---

Voraussetzungen:

```text
Consent

Capability

Provider Freigabe
```

---

## 23. Sicherheitsanforderungen

Pflicht:

```text
Capability Enforcement

Consent Enforcement

Audit Logging

Keine Direktzugriffe

Event Bus Integration
```

---

## 24. Testanforderungen

Jede Anwendung benötigt:

```text
Unit Tests

UI Tests

Capability Tests

Consent Tests

Localization Tests
```

---

## 25. Architekturentscheidung

Dieses RFC legt fest:

✅ Anwendungen sind Erweiterungen der Plattform

✅ Health Record ist Referenzanwendung

✅ Keine eigene Gesundheitsdatenbank

✅ Keine eigene Authentifizierung

✅ Plattformnavigation

✅ Plattformfähigkeiten

✅ Event Bus Integration

✅ Marketplace Unterstützung

✅ Gemeinsame Consent Engine

✅ Gemeinsame VitaFabric Nutzung

✅ Mehrbenutzerfähigkeit

✅ Lokalisierungspflicht
