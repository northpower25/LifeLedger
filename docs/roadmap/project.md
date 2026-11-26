# Gesamt-Roadmap

## Status und Ziel

Planungsvorschlag ohne Termine oder zugesagte Releases. Ausgangspunkt ist die
[Bestandsaufnahme](assessment.md): keine laufenden Dienste, keine produktiven
Daten und keine nachgewiesene Konformität. Die Reihenfolge beschreibt
Abhängigkeiten, nicht notwendig aufeinanderfolgende Kalenderphasen. Arbeit
ohne Abhängigkeit kann parallel stattfinden; jede Stufe benötigt ihre
genannten Nachweise.

## Verbindliche Leitplanken

Gesundheitsdaten passieren VitaFabric und werden in FHIR R4 modelliert;
Importe benötigen Quelle, Connector, Importzeitpunkt und ursprüngliche ID.
Zugriffe müssen Einwilligung beachten. Lokale Nutzung darf keine Cloud
voraussetzen; AI ist für den Kern optional. Sicherheitsvorgaben einschließlich
AES-256-GCM, Argon2, RBAC, Audit-Logging und MFA-Unterstützung sind in konkrete, überprüfbare
Spezifikationen umzusetzen. UI, Meldungen und Fehler sind lokalisierbar; Deutsch
und Englisch sind gemäß Produktdokumenten erste Zielsprachen. Architektur- und
Plugin-Vorschläge benötigen RFC, ADR und Review vor Umsetzung. Einzelheiten
und ungelöste Zielkonflikte werden nicht durch diese Roadmap entschieden.

## Plattformperspektive und Deployment

Die Gesundheitsakte ist als erste Referenzanwendung einer erweiterbaren
Plattform vorgeschlagen. Draft [RFC-0002](../../rfc/RFC-0002%20Platform%20Core%20Architecture)
beschreibt einen Core Runtime mit Identity & Consent, Security Services,
Event Bus, Plugin Host, Secret Store und Audit Service. Er schlägt explizite,
technisch durchzusetzende Capabilities und WASM First als Plugin-Runtime vor;
der Core Runtime soll keine Geschäftslogik, Gesundheitsmodelle oder AI
enthalten. Diese Entscheidungen sind noch nicht angenommen oder implementiert.
Authentifizierung, Autorisierung und Consent sind getrennte Belange;
Ownership, Richtlinien, Verträge und Durchsetzung an den Datenzugriffen sind
vor Umsetzung zu reviewen. VitaFabric und LifeWeaver behalten ihre
verbindlichen Daten- bzw. AI-Verantwortungen. Der
[Plattform-RFC](../../rfc/0001-platform-direction.md) und der
[ADR](../../adr/0002-platform-direction.md) sind noch nicht angenommen.

| Szenario | Planung und zusätzliches Gate |
| --- | --- |
| Nur lokal | Grundlage für alle Kernfunktionen; Offline-E2E-Nachweis ab Stufe 2. |
| Lokal + Relay | Optional nach Bedrohungsmodell und Review von Metadaten, Identität, Remote-Zugriff und Einwilligung; keine Klartext-Gesundheitsdaten im Relay. |
| Lokal + Zero-Knowledge-Sync | Optional nach Spezifikation und Tests für Ende-zu-Ende-Verschlüsselung, Schlüsselverwaltung und -wiederherstellung, Metadaten, Konflikte, Widerruf und verschlüsselte Backups; Dienst erhält keine Entschlüsselungsschlüssel. |
| Managed Cloud | Nur als separat zu prüfende Option, nicht als Ersatz für lokale Funktion. Verarbeitung, Verantwortlichkeiten, Einwilligung, Datenstandort und Sicherheitsanforderungen benötigen vor Umsetzung und Freigabe eigenes Architektur-, Datenschutz- und Rechtsreview. |

Keines dieser Szenarien außer dem geplanten lokalen Kern ist Voraussetzung für
die erste Nutzerreise; keines ist bereits verfügbar. Reihenfolge und Aufwand
optionaler Szenarien sind nicht entschieden.

### Erweiterungen und Marketplace

Die Vision und RFC-0002 schlagen sechs Plugin-Typen vor: Connector,
Integration, Provider, Storage, UI und Application. Sie sind nach
Zuständigkeit zu trennen:
VitaFabric verantwortet Gesundheitsdaten-Connectoren, FHIR und kontrollierte
Storage-Adapter; LifeWeaver optionale AI-Provider; LifeLedger UI- und
Produktanwendungen. Integrationen dürfen keine Gesundheitsdaten direkt
speichern oder an VitaFabric vorbei übertragen. Eine Marketplace-Oberfläche
mit Community-, Verified- und Official-Listings ist eine Option für eine
spätere Ausbaustufe, keine Registry-/Cloud-Pflicht und keine Sicherheits- oder
Consent-Garantie. Community-, Verified- und Official-Einstufungen benötigen
vorher Kriterien, Governance und Umsetzungsnachweise. Storage-Adapter erhalten
laut RFC-0002 nur verschlüsselte Daten, niemals Klartext oder Schlüssel.

## Stufen und Gates

| Stufe | Ergebnis und Abhängigkeit | Nachweis bzw. Gate |
| --- | --- | --- |
| 0 – Richtung und Schutz | Zielgruppe, erste Referenzanwendung, Plattformgrenzen und Verantwortlichkeiten für Core Runtime, Identity & Consent, Sicherheit und Plugins; Bedrohungsmodell, Rollen-/Consent-Modell, lokale Laufzeit, Deployment-Szenarien sowie FHIR- und Plugin-Verträge. | Authentifizierung, Autorisierung, Consent, Notfallzugriff und Widerruf getrennt spezifiziert; Datenzugriffsgrenzen, Annahmen und Blocker geprüft; benötigte ADRs akzeptiert und Spezifikationen versioniert, bevor entsprechende Funktionen entstehen. |
| 1 – Entwicklungsgrundlage | Reproduzierbare lokale Entwicklungsumgebung und CI; synthetische Fixtures; Verträge und kleine, testbare Einheiten für VitaFabric, LifeLedger und die spezifizierten Identitäts-/Consent-Grenzen. Auswahl des ersten Clients nach Stufe 0. | Build, Lint, Unit- und negative Vertragstests laufen lokal und in CI. Fehlende Consent-Freigabe, widerrufene Rechte und ungültige Daten werden abgewiesen; keine echten Gesundheitsdaten. |
| 2 – Erster vertikaler Durchstich | Offline im gewählten Client einen begrenzten synthetischen Gesundheitsdatensatz über VitaFabric erfassen, validieren, geschützt speichern und in der Referenzanwendung anzeigen. Identität, Rollen, Consent, Verschlüsselung, Zugriffskontrolle, Audit und Herkunft gemäß freigegebenen Spezifikationen; AI nicht erforderlich. | Ende-zu-Ende-Test ohne Netzwerk; FHIR-Validierung, Berechtigungs-, Notfallzugriffs- und Einwilligungs-Negativfälle, Widerruf, falscher Schlüssel, Neustart sowie Locale/Zeitzone. Gate erst nach Security- und Architekturreview der implementierten Datenpfade. |
| 3 – Belastbarer lokaler Kern | Lebenszyklus, Änderung und Löschung, verschlüsselte lokale Sicherung/Wiederherstellung, Interoperabilität und zugängliche Bedienung ausbauen. Weitere Clients erst auf gemeinsamen Verträgen aufsetzen; optionale Deployment-Szenarien getrennt prüfen. | Integrations-, Migrations-, Wiederherstellungs-, Fehler- und Zugänglichkeitstests; interoperabler FHIR-Test gegen dokumentierte Profile. Wiederherstellung darf keine unverschlüsselten Backups voraussetzen. |
| 4 – Erweiterbarkeit und Integrationen | Freigegebene Plugin-Verträge und lokale Entwicklungswerkzeuge; synthetischer Referenz-Connector, anschließend eine nach Review ausgewählte optionale Integration. Abhängig von Stufen 0–3 und [Plugin-Roadmap](plugins.md). | Unabhängig entwickeltes Plugin gegen versioniertes SDK und Konformitätssuite; Consent-/Isolations-, Fehler-, Upgrade- und Offline-Tests. Gesundheitsdaten weiterhin ausschließlich über VitaFabric. |
| 5 – Optionale Intelligenz | LifeWeaver lokal und providerneutral; MCP und ggf. externe Provider nur über explizit freigegebene Grenzen. Abhängig von Daten-, Sicherheits- und Einwilligungsverträgen. | Tests für verweigerten/widerrufenen Zugriff, Datenminimierung, Providerwechsel, lokale Nutzung und MCP-Kompatibilität; Sicherheits- und Zweckbestimmungsreview vor Nutzerfreigabe. |
| 6 – Freigabe und nachhaltiger Ausbau | Erst nach vollständigem Scope- und Risikoreview: unterstützte Plattformen, Dokumentation, Support, sichere Updates und Betriebsmodell veröffentlichen. Danach weitere Produktbereiche und Integrationen inkrementell. | Dokumentierte Bedrohungs- und Datenschutzprüfung, externe Sicherheitsprüfung nach vereinbartem Umfang, behobene Freigabeblocker, Recovery-Übung, Barrierefreiheits- und Lokalisierungsprüfung, dokumentierte Restrisiken und explizite Freigabe. Kein Einsatz echter Daten vor diesem Gate. |

## Übergreifende Teststrategie

Ab der ersten ausführbaren Komponente gehört zu jeder Änderung eine passende
automatisierte Prüfung: Unit-Tests, komponentenübergreifende Vertragstests und
gezielte Ende-zu-Ende-Tests. Sicherheits- und Einwilligungsfälle testen auch
Verweigerung, Widerruf, Fehler und Umgehungsversuche; FHIR-Fälle sowohl gültige
als auch ungültige Beispiele. Testdaten sind synthetisch und enthalten weder
Geheimnisse noch echte Gesundheitsdaten. Plugin-Suite und Regressionstests
laufen mit unterstützten Vertragsversionen. Tests, Tooling und Freigabeergebnisse
werden mit konkreten Kommandos dokumentiert, sobald sie existieren.

## Koordination

- [LifeLedger](lifeledger.md): Produktabläufe, Backend und Web-, Mobile- und Desktop-Clients.
- [VitaFabric](vitafabric.md): Datenzugang, FHIR, Provenienz, Speicherung und Connectoren.
- [LifeWeaver](lifeweaver.md): optionale AI, Agenten und MCP.
- [Plugins](plugins.md): herstellerneutrale Community-Verträge und Vertrauensmodell.
- [Integrationen](integrations.md): externe Systeme einschließlich Home Assistant.

## Getroffene Architekturentscheidungen für den ersten Durchstich

## Getroffene Architekturentscheidungen für den ersten Durchstich

Die folgenden Entscheidungen gelten als Arbeitsgrundlage für die Architektur-, Spezifikations- und Prototypenphase.

### Zielgruppe und erster Anwendungsfall

Die erste Zielgruppe sind Privatpersonen und Familien mit Interesse an einer langfristigen, lokalen Gesundheitsdatenverwaltung.

Der erste wertvolle Durchstich besteht aus:

1. Installation von LifeLedger auf einem lokalen Gerät
2. Import eines synthetischen oder realen Gesundheitsdatensatzes
3. Import eines medizinischen Dokuments
4. Darstellung aller Daten in einer gemeinsamen Timeline
5. Lokale verschlüsselte Speicherung
6. Lokale Sicherung und Wiederherstellung

Die persönliche Gesundheitsakte dient als erste Referenzanwendung der Plattform.

---

### Erstes Zielsystem

Unterstützt wird zunächst:

```text
Desktop
  └─ Windows
```

Weitere Plattformen folgen nach erfolgreichem Abschluss des ersten vertikalen Durchstichs.

Die erste Client-Anwendung basiert auf:

```text
Tauri Desktop
```

---

### Lokales Speicher- und Laufzeitmodell

Die Standardinstallation verwendet:

```text
SQLite
```

als lokale persistente Datenbank.

Die Daten werden durch VitaFabric verschlüsselt gespeichert.

Storage-Adapter erhalten niemals unverschlüsselte Gesundheitsdaten.

PostgreSQL, Cloud-Speicher oder andere Storage-Systeme sind spätere optionale Erweiterungen.

---

### Identität, Rollen und Einwilligung

Die Plattform verwendet folgende Rollen:

```text
Primary Owner
Guardian
Caregiver
Proxy
Emergency Contact
```

Nur Primary Owner, Guardian und Proxy dürfen Berechtigungen delegieren.

Freigaben werden ressourcenbasiert vergeben und können jederzeit widerrufen werden.

Authentifizierung, Autorisierung und Einwilligung werden als unabhängige Komponenten des Identity-&-Consent-Layers behandelt.

---

### Erste FHIR-Ressourcen

Der MVP unterstützt zunächst:

```text
Patient
Observation
Condition
MedicationStatement
AllergyIntolerance
DocumentReference
```

Weitere Ressourcen werden erst nach erfolgreichem MVP ergänzt.

---

### Herkunft und Provenienz

Jeder Datensatz muss mindestens folgende Informationen besitzen:

```text
Quelle
Connector
Importzeitpunkt
Original-ID
Version
```

Dokumente werden grundsätzlich über DocumentReference modelliert.

---

### Sicherheitsvoraussetzungen für reale Daten

Vor Verarbeitung realer Gesundheitsdaten müssen mindestens folgende Anforderungen erfüllt sein:

```text
AES-256-GCM
Argon2
Audit Logging
Consent Management
Backup & Recovery
MFA-Unterstützung
Incident Response Prozess
Security Disclosure Prozess
```

Ein Security-Maintainer-Team verantwortet Freigaben und Incident-Management.

---

### Community und Finanzierung

Phase 1:

```text
Community
GitHub
AGPL
```

Phase 2:

```text
GitHub Sponsors
OpenCollective
```

Phase 3:

```text
Managed Cloud Services
Marketplace Infrastruktur
Relay Services
```

Übersetzungen erfolgen über eine Community-Plattform wie Weblate oder Crowdin.

---

### Gemeinsame Plattformfähigkeiten

Zum verpflichtenden Plattformkern gehören:

```text
Identity Service
Consent Service
Plugin Host
Event Bus
Secret Store
Audit Service
VitaFabric
```

Nicht zum Plattformkern gehören:

```text
Connectoren
Integrationen
Provider
Anwendungen
Dashboards
```

Diese werden über das Erweiterungsmodell bereitgestellt.

---

### Marketplace Governance

Marketplace-Kategorien:

```text
Community
Verified
Official
```

Community:
- Keine Projektprüfung

Verified:
- Maintainer Review
- Grundlegende Tests

Official:
- Offiziell durch das Projekt betreut
- Signiert mit Projekt-Schlüsseln

Marketplace-Listings stellen keine Sicherheitszertifizierung dar.

---

### Deployment-Szenarien

Der lokale Betrieb ist verpflichtende Grundlage aller Kernfunktionen.

Unterstützte Szenarien:

```text
Local Only
Local + Relay
Local + Zero-Knowledge Sync
Managed Cloud
```

Dabei gilt:

- Kein Szenario darf lokalen Betrieb ersetzen
- Benutzer behalten die Kontrolle über ihre Schlüssel
- Cloud-Komponenten bleiben optional
- Zero-Knowledge Sync darf keine Entschlüsselungsschlüssel besitzen

---

### Offene Restfragen

Nach den bisherigen Architekturentscheidungen verbleiben insbesondere folgende Themen:

- Detaillierte Capability-Matrix
- Konkrete WASM Plugin Runtime
- Family Data Model
- Event Bus Spezifikation
- Marketplace Governance Details
- Zero-Knowledge Recovery Verfahren
- Health-Twin Architektur
