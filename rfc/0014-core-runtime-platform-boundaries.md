# RFC 0014: Core Runtime & Platform Boundaries

- Status: Draft
- Type: Architecture RFC
- Owner: Platform Architecture
- Depends On: RFC-0002 Platform Core Architecture; RFC-0003 Identity & Consent; RFC-0004 Capability Model; RFC-0006 Plugin Runtime; RFC-0011 AI Provider Framework; RFC-0013 VitaFabric Data Contracts

## 1. Zusammenfassung

Dieses RFC legt die verpflichtenden Verantwortungsgrenzen zwischen Platform
Core, VitaFabric, LifeWeaver, Applications und Plugins fest. Die Grenzen
definieren Eigentümerschaft und unverhandelbare Sicherheitskontrollen, nicht
die konkrete Prozess-, Paket- oder Deployment-Topologie. Ein Dienst darf
intern ersetzt oder aufgeteilt werden, wenn sein Vertrag und seine
Sicherheitsinvarianten erhalten bleiben.

## 2. Ziele und Nichtziele

### Ziele

- Verbindliche Eigentümerschaft für plattformweite Vertrauensgrenzen
- Gesundheitsdatenzugriff ausschließlich über VitaFabric
- Erweiterbarkeit ohne Ersetzen oder Umgehen sicherheitskritischer Dienste
- Klare Abgrenzung optionaler AI-Funktionen
- Erweiterbare Applications als spezialisierte Plugin-Typen; integrierter
  Health Record im ersten Slice gemäß vorgeschlagenem ADR-0003

### Nichtziele

- Festlegung einer konkreten Prozess- oder Microservice-Architektur
- Behauptung, dass vorgeschlagene Plattformdienste bereits implementiert sind
- Garantie, dass ein Marketplace-Listing oder eine Signatur ein Plugin sicher macht

## 3. Verbindliche Architekturgrenzen

### Platform Core — zwingender Plattformvertrag

Jede LifeLedger-konforme Plattform stellt folgende Verantwortlichkeiten als
Plattformdienste bereit:

- Identity und authentisierte Sessions
- Consent-Verwaltung und Consent-Enforcement
- Capability-Policy, Autorisierung und technische Durchsetzung
- Audit-Erfassung für Sicherheits- und Datenzugriffe
- Event Bus mit kontrollierten Publish-/Subscribe-Rechten
- Plugin Host und technisch erzwungene Isolation
- Secret- und Schlüsselzugriffsgrenzen
- Plattform-API, Settings und Lifecycle-Verwaltung

Der Plugin Host ist für den ersten Slice ohne Plugin-Ausführung gemäß
ADR-0003 nicht erforderlich; sobald Plugins unterstützt werden, sind Host
und Isolation zwingend. Alle übrigen relevanten Pflichtkontrollen bleiben
auch im Slice verpflichtend.

Diese Dienste dürfen intern aufgeteilt oder durch kompatible Implementierungen
ersetzt werden. Sie dürfen weder durch Plugins überschrieben noch deaktiviert,
umgangen oder durch eine Anwendung nachgebildet werden. Fehlende oder nicht
erreichbare Pflichtkontrollen führen bei geschützten Vorgängen zu „deny“;
ein unsicherer Fallback ist unzulässig.

### VitaFabric — zwingender Health-Data-Owner

VitaFabric ist der einzige autorisierte Zugang zu Gesundheitsdaten und
Derived Data. VitaFabric besitzt die kanonischen FHIR-Verträge, Validierung,
Provenienz, Datenklassifikation, Consent-/Capability-Prüfung am Datenzugriff
sowie die Storage-Abstraktion. Alle Importe, Exporte, Synchronisationen und
abgeleiteten AI-Daten müssen diese Verträge durchlaufen.

Ein Storage-Backend kann als Erweiterung implementiert werden, erhält jedoch
nur die von VitaFabric vorbereiteten verschlüsselten Daten und niemals
Schlüssel, Consent-Entscheidungsgewalt oder direkte FHIR-/Datenbank-
Schreibrechte. Ein Plugin kann weder VitaFabric noch dessen Pflichtprüfungen
ersetzen.

### LifeWeaver — optionale AI-Funktion

LifeWeaver ist optional und gehört nicht zu den Voraussetzungen für den
lokalen Kernbetrieb. Wenn aktiviert, stellt es Provider-, MCP-, RAG- und
Twin-Funktionen über die Plattformverträge bereit. Es darf Daten nur nach
erneuter Prüfung von Consent, Capability und Zweck über VitaFabric erhalten.
AI-Provider sind Erweiterungen; LifeWeaver, Consent-Prüfung und
VitaFabric-Zugriffskontrolle selbst sind keine Plugins.

### Applications und Plugins

Erweiterbare Applications sind spezialisierte Plugin-Typen. Der erste Health
Record wird gemäß [ADR-0003](../adr/0003-first-slice-application-boundary.md)
als integrierter Anwendungsteil statt als Plugin vorgeschlagen; diese Ausnahme
ändert keine Pflichtkontrollen. Eine Application darf UI, Navigation,
Workflows und eigene nicht-gesundheitsbezogene Einstellungen bereitstellen,
aber keine eigene Identität, Consent Engine, Sicherheitsrichtlinie,
Gesundheitsdatenbank oder Audit-Autorität besitzen.

Erlaubte Erweiterungstypen, vorbehaltlich der jeweiligen Verträge und
Capabilities:

- Connectoren und externe Integrationen
- AI-/sonstige Provider
- Storage-Backends unter VitaFabric-Kontrolle
- UI-Erweiterungen und Applications

Erweiterungen laufen standardmäßig isoliert und erhalten keinen impliziten
Datei-, Netzwerk-, Datenbank- oder Secret-Zugriff. Jede Berechtigung wird
explizit, zweckgebunden und widerrufbar erteilt. Ein deklarierter
Erweiterungstyp erweitert nicht die Vertrauensstufe.

## 4. Was niemals Plugin sein oder Plugin-Kontrolle erhalten darf

Die folgenden Autoritäten und Kontrollen dürfen nicht durch Plugins
bereitgestellt, ersetzt, abgeschaltet oder umgangen werden:

- Authentifizierung, Identity-Wurzel und Session-Verifikation
- Consent-Entscheidungen, Consent-Enforcement und Widerruf
- Capability-Policy, Autorisierung und Enforcement
- Audit-Erfassung und Audit-Integrität
- Plugin Host, Isolation und Signatur-/Paketprüfung
- Schlüsselverwaltung, Secret-Grenzen und kryptographische
  Vertrauensanker
- VitaFabric-Datenverträge, FHIR-Validierung, Provenienz und
  Zugriffskontrolle
- Event-Bus-Autorisierung und sicherheitskritische Plattform-APIs

Plugins dürfen diese Dienste ausschließlich über versionierte, hostvermittelte
und autorisierte Schnittstellen nutzen. Administrator- oder Marketplace-
Status gewährt keine Ausnahme.

## 5. Durchsetzung und Ausfallverhalten

Alle Datenzugriffe folgen mindestens diesem Pfad:

```text
Anwendung oder Plugin
        ↓
Identity + Capability + Consent
        ↓
VitaFabric Data Contract
        ↓
verschlüsselter Storage Adapter
```

Entscheidungen werden am tatsächlich geschützten Zugriffspunkt erneut
durchgesetzt; UI-Prüfungen oder zuvor ausgestellte Grants reichen nicht aus.
Bei Widerruf müssen laufende Sessions, Tokens, Event-Abonnements und
abgeleitete Zugriffe invalidiert werden. Kann ein Dienst die Prüfung nicht
zuverlässig durchführen, wird der Vorgang abgelehnt und ein sicherheitsarmer
Audit-Eintrag erzeugt.

## 6. Konsequenzen

- Plattformverträge bleiben verpflichtend, Implementierungs- und
  Deployment-Topologie bleiben austauschbar.
- Plugins und Applications können den Kern nicht ersetzen und sind ohne
  Plattformfreigabe nicht funktionsfähig.
- VitaFabric ist ein notwendiger Kontroll- und Verarbeitungspfad; zusätzliche
  Validierung und erneute Autorisierung können Latenz und Ressourcenverbrauch
  erhöhen. Die Implementierung muss diese Kosten auf Zielgeräten messen, darf
  aber keine Kontrollen zur Performance-Optimierung umgehen.
- LifeWeaver kann vollständig fehlen, ohne lokale Kernfunktionen zu brechen.
- Jede Erweiterung und jeder optionale Deployment-Modus benötigt eigene
  Konformitäts-, Sicherheits- und Ausfalltests.

## 7. Architekturentscheidung

- Platform Core stellt verpflichtende, nicht durch Plugins ersetzbare
  Vertrauensdienste bereit.
- VitaFabric ist der einzige Gateway- und Datenvertrags-Owner für Health Data
  und Derived Data.
- LifeWeaver ist optional und bleibt an VitaFabric sowie Consent und
  Capabilities gebunden.
- Erweiterbare Applications sind spezialisierte Plugins; der erste integrierte
  Health Record ist die in ADR-0003 vorgeschlagene Ausnahme. Storage-Backends, Connectoren,
  Integrationen und Provider sind kontrollierte Erweiterungspunkte.
- Keine Signatur, Listing-Stufe oder Administratorrolle hebt diese Grenzen auf.

## 8. Offene Umsetzungsfragen

- Welche konkreten Schnittstellen, Prozessgrenzen und Laufzeit-Implementierungen
  erfüllen die obigen Verträge auf Desktop und Mobile?
- Welche messbaren Performance- und Ressourcenbudgets gelten pro Zielgerät,
  ohne Consent-, Capability- oder Audit-Prüfungen abzusenken?
- Wie werden Architekturkonformität und fail-closed Verhalten automatisiert
  und unabhängig geprüft?
