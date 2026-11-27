# RFC 0002: Platform Core Architecture

- Status: Draft
- Type: Architecture RFC
- Owner: Platform Core
- Related Documents:

- ADR-0002 Platform Direction
- RFC-0001 Platform Direction
- VitaFabric Roadmap
- LifeLedger Roadmap
- Plugin Ecosystem Roadmap

---

## 1. Zusammenfassung

LifeLedger soll nicht ausschließlich eine persönliche Gesundheitsakte sein.

LifeLedger soll eine erweiterbare, lokale und datenschutzorientierte Plattform für persönliche Gesundheitsdaten werden.

Die Gesundheitsakte ist die erste Referenzanwendung der Plattform.

Die erste Zielgruppe umfasst Privatpersonen, Familien und Health Power User.

Dieses RFC definiert:

- Platform Core Runtime
- Identity & Consent Layer
- Capability Model
- Event Bus
- Plugin Runtime
- Application Model
- Grundlegende Systemgrenzen

und legt fest, welche Komponenten zwingender Bestandteil der Plattform sind und welche durch Erweiterungen realisiert werden können. Dies entspricht der vorgeschlagenen Plattformvision und den in den Roadmaps beschriebenen Vertrauensgrenzen. 

---

## 2. Ziele

### Ziele

- Local-First Betrieb
- Erweiterbarkeit ähnlich Home Assistant
- Zentrale Gesundheitsdatenkontrolle über VitaFabric
- Trennung von Daten, Anwendungen und Integrationen
- Plattformübergreifende Nutzbarkeit
- Sichere Rechteverwaltung
- Sichere Plugin-Architektur
- Optionale Cloud-Komponenten

### Nichtziele

- Medizinische Diagnosen
- Therapieempfehlungen
- Klinische Entscheidungsunterstützung
- Cloud-Pflicht
- Direkter Datenbankzugriff durch Plugins

---

## 3. Plattformarchitektur

### Zielstruktur

```text
LifeLedger Platform

├── Core Runtime
├── Identity & Consent
├── Security Services
├── Event Bus
├── Plugin Host

├── VitaFabric
│   └── Data Layer

├── LifeWeaver
│   └── AI Layer

└── Applications
    ├── Health Record
    ├── Family Health
    ├── Medication Manager
    └── weitere Apps
```

---

## 4. Core Runtime

### Zweck

Der Core Runtime stellt die minimal notwendige Plattform bereit.

Er enthält keine Geschäftslogik.

Er enthält keine Gesundheitsmodelle.

Er enthält keine KI.

### Bestandteile

#### Identity Service

Verantwortlich für:

```text
Benutzer
Geräte
Authentifizierung
Sessions
```

---

#### Consent Service

Verantwortlich für:

```text
Freigaben
Widerruf
Vertretungen
Notfallzugriffe
Familienbeziehungen
```

---

#### Plugin Host

Verantwortlich für:

```text
Plugin-Lifecycle
Plugin-Registrierung
Plugin-Start
Plugin-Stop
Plugin-Update
```

---

#### Event Bus

Verantwortlich für:

```text
Interne Kommunikation
Events
Subscriptions
```

---

#### Secret Store

Verantwortlich für:

```text
API Keys
Access Tokens
Provider Credentials
```

---

#### Audit Service

Verantwortlich für:

```text
Audit Events
Sicherheitsereignisse
Datenzugriffe
Einwilligungen
```

---

## 5. Plattformgrenzen

RFC-0014 ist die maßgebliche Quelle der Komponentenverantwortung und
Abgrenzung zwischen Plattform, VitaFabric, LifeWeaver und Erweiterungen. Die
folgenden Listen fassen den Vertrag zusammen; sie legen keine monolithische
Implementierung fest.

### Zwingende Plattformverträge

```text
Core Runtime
Identity
Consent
Audit
Event Bus
Plugin Host
VitaFabric
```

LifeWeaver ist eine optionale Plattformfunktion und für den lokalen Kernbetrieb
nicht erforderlich. VitaFabric bleibt der einzige autorisierte
Gesundheitsdatenzugriff und kann nicht durch ein Plugin ersetzt werden.

---

### Darf Plugin sein

```text
Connectoren
Integrationen
Provider
Storage Adapter
Dashboards
Anwendungen
```

---

### Darf niemals Plugin sein

```text
Identity und Authentifizierung
Consent Entscheidung und Enforcement
Audit Integrität
Capability Policy und Enforcement
Plugin Host und Isolation
Secret-/Schlüsselgrenzen
VitaFabric Verträge, FHIR Validierung und Zugriffskontrolle
```

---

## 6. Identity & Consent Modell

### Benutzerrollen

#### Primary Owner

Besitzer eines Gesundheitsprofils.

Darf:

```text
lesen
schreiben
delegieren
widerrufen
```

---

#### Guardian

Gesetzlicher Vertreter.

Darf:

```text
lesen
schreiben
freigeben
widerrufen
```

---

#### Caregiver

Pflegeperson.

Darf:

```text
lesen
teilweise schreiben
keine Besitzrechte
```

---

#### Proxy

Bevollmächtigter Vertreter.

Beispiel:

```text
Vorsorgevollmacht
```

---

#### Emergency Contact

Darf ausschließlich:

```text
vordefinierte Notfalldaten lesen
```

---

## 7. Capability Modell

### Grundprinzip

Kein Plugin erhält implizite Rechte.

Alle Fähigkeiten müssen explizit angefordert werden.

---

### Gesundheitsdaten

```text
READ_PATIENT
READ_OBSERVATION
READ_CONDITION
READ_DOCUMENT
READ_MEDICATION
```

---

### Schreibrechte

```text
WRITE_OBSERVATION
WRITE_DOCUMENT
WRITE_MEDICATION
```

---

### Systemrechte

```text
NETWORK_ACCESS
LOCAL_STORAGE
NOTIFICATION_ACCESS
CAMERA_ACCESS
```

---

### KI Rechte

```text
AI_LOCAL_MODEL
AI_REMOTE_PROVIDER
AI_RAG
AI_EMBEDDING
AI_AGENT
```

---

### Administrative Rechte

```text
USER_MANAGEMENT
EMERGENCY_ACCESS
PLUGIN_INSTALL
PLUGIN_SIGN
```

---

## 8. Event Bus

### Ziel

Lose Kopplung aller Komponenten.

---

### Standard Events

```text
FHIR_CREATED
FHIR_UPDATED
FHIR_DELETED

CONSENT_GRANTED
CONSENT_REVOKED

PLUGIN_INSTALLED
PLUGIN_REMOVED

USER_CREATED
USER_REMOVED
```

---

### Beispiel

```text
Observation gespeichert

↓

FHIR_CREATED

↓

Event Bus

↓

Abonnierte Plugins
```

---

## 9. VitaFabric Regeln

### Verbindliche Regel

Alle Gesundheitsdaten passieren VitaFabric.

```text
Plugin
↓
VitaFabric API
↓
FHIR Modell
↓
Storage
```

---

### Verboten

```text
Plugin
↓
Datenbank
```

---

### Storage Plugins

Storage Adapter erhalten:

```text
verschlüsselte Daten
```

Storage Adapter erhalten niemals:

```text
Klartextdaten
Schlüssel
FHIR Ownership Kontrolle
```

---

## 10. Plugin Runtime

### Entscheidung

WASM First

```text
WebAssembly Runtime
```

wird Standard.

Gründe:

- Plattformunabhängig
- Sandboxing
- Mobile geeignet
- Desktop geeignet
- Browser geeignet

---

### Spätere Erweiterungen

Optional:

```text
Python Connector Runtime
```

für Datenimporte.

Kann die geforderte Isolation nicht durchgesetzt werden, wird ein Plugin
nicht ausgeführt; ein unisolierter Fallback ist ausgeschlossen (RFC-0006).

---

## 11. Plugin-Signierung

### Community

```text
Self Signed
```

---

### Verified

```text
Maintainer Sign-Off
```

Das konkrete Signatur- und Prüfverfahren bleibt zu spezifizieren.

---

### Official

```text
LifeLedger Signing Key
```

---

## 12. Marketplace

### Kategorien

#### Community

Keine Prüfung.

---

#### Verified

Review durchgeführt.

---

#### Official

Projektverantwortung übernommen.

---

### Wichtige Regel

Marketplace ist:

```text
Discovery
```

nicht

```text
Sicherheitsgarantie
```

---

## 13. Application Model

### Grundsatz

Für spätere Erweiterungen ist eine Application als spezialisierter Plugin-Typ
vorgesehen. Der erste Health Record wird dagegen als integrierter Anwendungsteil
ohne externes Plugin ausgeführt; die Änderung der bisherigen Grenze ist in
[ADR-0003](../adr/0003-first-slice-application-boundary.md) vorgeschlagen.
Auch er nutzt die gemeinsamen Plattformdienste.

Anwendungen besitzen keine eigene Datenbank.

---

Anwendungen bestehen aus:

```text
UI
Workflows
Settings
Capabilities
```

---

Alle Gesundheitsdaten stammen aus:

```text
VitaFabric
```

---

### Erster Client und Durchstich

Geplant sind ein lokaler FastAPI-Dienst eingebettet in Tauri für den
Desktop-Client und Flutter für Mobile. Desktop beginnt mit Windows; Linux
und macOS folgen. Der erste Durchstich umfasst Patient, DocumentReference und
MedicationStatement, Dokumentimport, Timeline und Backup (RFC-0007); nur
synthetische Daten sind zugelassen. Observation gehört nicht zum Slice.
Vor der Freigabe für echte Gesundheitsdaten gelten die Sicherheits-Gates der
Roadmap.

Die vorgeschlagene lokale Laufzeittopologie und ihre offenen Nachweise stehen
in „Runtime Topology“ unten.

Als erste externe Integration ist Nextcloud vor Home Assistant vorgesehen;
der lokale Kern benötigt keine dieser Integrationen. Datenrichtung und
Vertrauensgrenzen bleiben integrationsspezifisch zu klären.

---

## 14. Deployment Modelle

Die geplante Reihenfolge ist Mode 1 → Mode 2 → Mode 3 → Mode 4.
Optionale Modi benötigen jeweils ein eigenes Review und machen den lokalen
Kern nicht von einem Cloud-Dienst abhängig.

### Mode 1

Local Only

```text
Standard
```

---

### Mode 2

Local + Relay

Zweck:

```text
Remote Access
Notifications
Discovery
```

---

### Mode 3

Local + Zero Knowledge Sync

Cloud speichert:

```text
verschlüsselte Daten
```

Cloud erhält niemals:

```text
Schlüssel
Passwörter
Klartext
```

---

### Mode 4

Managed Cloud

Optional.

Separates Datenschutz- und Sicherheitsreview erforderlich.

---

## 15. Sicherheitsprinzipien

### Zero Trust

Plugins sind niemals automatisch vertrauenswürdig.

---

### Least Privilege

Plugins erhalten nur notwendige Rechte.

---

### Auditability

Jede Freigabe muss nachvollziehbar sein.

---

### Local First

Jede Kernfunktion muss lokal lauffähig sein.

---

### Consent First

Kein Zugriff auf Gesundheitsdaten ohne Freigabe.

---

## 16. Offene Nachfolge-RFCs

Dieses RFC erzeugt folgende Folgedokumente:

```text
RFC-0003 Identity & Consent

RFC-0004 Capability Model

RFC-0005 Event Bus

RFC-0006 Plugin Runtime

RFC-0007 Application Model

RFC-0008 Family Model

RFC-0009 Marketplace Governance
```

---

## Runtime Topology

Für den ersten Windows-Offline-Durchstich wird folgende Topologie
vorgeschlagen; RFC-0014 definiert weiterhin die Verantwortungsgrenzen, nicht
die Prozessaufteilung:

```text
Tauri Desktop Host → lokales IPC → FastAPI + Core → VitaFabric → SQLite
```

Core und VitaFabric können im selben lokalen Dienst laufen, bleiben aber
getrennte Verantwortlichkeiten; die SQLite-Schnittstelle ist ausschließlich
über VitaFabric für Gesundheitsdaten erreichbar. SQLite und alle zugehörigen
Dateien, Indizes, temporären Dateien und Backups müssen vor Speicherung
geschützt sein. Normales SQLite allein bietet keine Verschlüsselung.
Eine genaue Verschlüsselungs- und Schlüsselarchitektur ist noch offen.

### Startup Sequence

1. Tauri startet genau einen eigenen Dienst und übergibt ihm einen
   kurzlebiges, zufällig erzeugtes IPC-Authentisierungsgeheimnis über einen geschützten
   lokalen Kanal, nicht über URL, Kommandozeile, Log oder Umgebungsvariable.
2. Der Dienst bindet ausschließlich an den freigegebenen lokalen Endpunkt,
   validiert Host/Origin und authentisiert jede Anfrage; er akzeptiert keine
   externe Netzwerkverbindung. Der Host prüft die Identität des Dienstes.
3. Nach Bereitschaft von Identity, Policy, Audit und VitaFabric erfolgt
   die Owner-Entsperrung und Einrichtung einer eigenen Benutzersitzung; vor
   erfolgreicher Prüfung bleiben Daten gesperrt.
   Ein bereits belegter Endpunkt oder fehlgeschlagene Gegenprüfung führt zum
   Abbruch, nicht zu einem Vertrauen auf einen fremden Dienst.

### Shutdown Sequence

Neue Anfragen stoppen, laufende Transaktionen abschließen oder rückrollen,
Audit und Änderungen dauerhaft sichern, Sitzungen und Schlüssel im Speicher
invalidieren und den eigenen Dienst beenden. Bei Absturz erfolgt beim
Neustart Recovery vor neuer Datenfreigabe. Bereits exportierte Daten werden
durch den Shutdown nicht zurückgerufen.

### Process Trust Boundaries

| Bereich | Vertrauensniveau und Authentisierung | Kommunikationsweg |
| --- | --- | --- |
| Tauri-UI/Host | Client-Eingaben nicht vertrauenswürdig; Owner-Sitzung und gegenseitige Prozessprüfung erforderlich. | Ausschließlich authentisiertes lokales IPC zum eigenen Backend. |
| FastAPI/Core und VitaFabric | Vertrauenswürdige Durchsetzungsinstanzen, aber kein implizites Recht für Aufrufer; Identity, Consent, Capability und Policy am geschützten Zugriff prüfen. | Lokale interne Aufrufe; Gesundheitsdaten ausschließlich über VitaFabric. |
| Plugin Runtime | Plugins nicht vertrauenswürdig; Host prüft Identität, Signatur und Berechtigungen. Im Slice nicht ausgeführt. | Nur isolierte, hostvermittelte Schnittstellen; kein direkter Storage. |
| Storage Layer | Daten und Dateien gelten als manipulierbar; Integrität und Verschlüsselung prüfen, keine eigene Autorisierungsentscheidung. | Zugriff auf Gesundheitsdaten ausschließlich über VitaFabric und dessen Storage-Abstraktion. |

Der konkrete Mechanismus für IPC, Prozessidentität und Schutz gegen Prozesse
mit denselben Benutzerrechten ist offen; diese Tabelle behauptet keine bereits
durchgesetzte Isolation.

### Failure Modes

UI, Host, Dienst, Dateisystem und externe Prozesse sind getrennte
Vertrauensbereiche; ein anderer Prozess desselben Nutzers ist nicht
automatisch vertrauenswürdig. Audit-, Policy-, Validierungs-, Schlüssel- oder
Speicherfehler verhindern den geschützten Zugriff; ein schreibender Vorgang
gilt erst nach atomarer Speicherung von Änderung und Audit als erfolgreich.
Ein Audit-Ausfall darf keinen Erfolg vortäuschen. Zugriffskontrolle erfolgt
auch bei internen Aufrufen am VitaFabric-Gateway.

Die konkrete Windows-IPC-Technik, beidseitige Authentisierung, Schutz gegen
lokale Mitbenutzer und Schadsoftware mit gleichen Rechten, Packaging,
Mehrfachstarts und Prozessüberwachung sind nicht entschieden. Eine lokale
HTTP-Loopback-Adresse ist für sich keine Authentisierung. Diese Punkte,
das Bedrohungsmodell und Messbudgets benötigen vor Implementierungsstart
einen geprüften Vertrag; siehe [Startfragen](../docs/review/offene-informationen-erste-testversion.md).

---

## 17. Architekturentscheidung

Dieses RFC legt folgende vorläufige Entscheidungen fest:

✅ Gesundheitsakte = Referenzanwendung

✅ VitaFabric = zentrales Gesundheitsdaten-Gateway

✅ WASM First Plugin Runtime

✅ Event Bus als Kernbestandteil

✅ Capability basiertes Sicherheitsmodell

✅ Local First als Standard

✅ Consent als eigenständige Plattformfunktion

✅ Anwendungen besitzen keine eigene Gesundheitsdatenbank

✅ Marketplace ist optional

✅ Storage Adapter erhalten niemals Klartextdaten
