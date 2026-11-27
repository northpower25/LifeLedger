# RFC 0006: Plugin Runtime & Isolation

- Status: Draft
- Type: Architecture RFC
- Owner: Platform Core
Depends On: RFC-0002 Platform Core Architecture  
Depends On: RFC-0003 Identity & Consent Framework  
Depends On: RFC-0004 Capability & Permission Model  
Depends On: RFC-0005 Event Bus Architecture  
Blocks: RFC-0007, RFC-0009, RFC-0011

---

## 1. Zusammenfassung

Dieses RFC definiert die Runtime, Isolation, Sicherheitsgrenzen und den Lebenszyklus aller Erweiterungen innerhalb der LifeLedger Plattform.

Das Ziel ist ein Home-Assistant-ähnliches Erweiterungsmodell mit deutlich strengeren Sicherheitsanforderungen für Gesundheitsdaten. Erweiterungen dürfen niemals direkte Datenbank- oder Systemzugriffe erhalten und müssen vollständig durch Capability-, Consent- und VitaFabric-Grenzen kontrolliert werden. Die Anforderungen ergeben sich unmittelbar aus den Plattform-, Plugin-, VitaFabric- und Integrations-Roadmaps.

---

## 2. Ziele

### Ziele

```text
Isolierte Erweiterungen

Lokaler Betrieb

Kontrollierte APIs

Capability Enforcement

Plugin-Unabhängigkeit

Drittentwickler-Unterstützung

Offline-Nutzung

Reproduzierbares Sicherheitsmodell
```

---

### Nichtziele

```text
Beliebige Codeausführung

Direkte Datenbankzugriffe

Volle Betriebssystemrechte

Root-Zugriffe

Vertrauensbasierte Plugins
```

---

## 3. Architekturentscheidung

### Entscheidung

Die Plattform verwendet:

```text
WASM First
```

als primäre Plugin Runtime.

Kann die erforderliche Isolation auf einer Plattform nicht durchgesetzt
werden, wird das Plugin dort nicht ausgeführt. Eine nicht isolierte
Ausführung als Fallback ist ausgeschlossen.

### Referenzruntime und Schnittstelle

Die Referenzimplementierung verwendet **Wasmtime** mit dem **WebAssembly
Component Model** und **WASI 0.2 (Preview 2)**. Plugin-Schnittstellen werden
als versionierte WIT-Interfaces definiert; WASI stellt keine implizite
Berechtigung für Plattformdaten, Dateien oder Netzwerk dar. Die Plattform
stellt nur explizit capability-geprüfte Host-Imports bereit.

Die Runtime-Version und die verwendeten WASI- und WIT-Abhängigkeiten werden
pro Release exakt gepinnt, mit SBOM und reproduzierbarem Build veröffentlicht
und nach Sicherheitsupdates aktualisiert. Andere Runtimes sind nicht
automatisch kompatibel; ein Wechsel erfordert ein RFC und erneute
Konformitäts- und Isolationstests.

Die Component-Runtime kann gegenüber nativer Ausführung Startzeit- und
Speicher-Overhead verursachen, besonders auf mobilen oder ressourcenarmen
Geräten. Runtime-Versionen und Plugin-Limits müssen deshalb auf jeder
Zielplattform gemessen werden; ein Performance-Fallback auf unisolierten Code
ist ausgeschlossen.

---

### Begründung

WASM bietet:

```text
Sandboxing

Plattformunabhängigkeit

Desktop-Unterstützung

Mobile-Unterstützung

Browser-Unterstützung

Kontrollierte Schnittstellen
```

---

### Abgelehnte Alternativen

#### Python Only

Probleme:

```text
Schwache Isolation

Hohe Angriffsfläche

Unkontrollierbare Abhängigkeiten
```

---

#### Container First

Probleme:

```text
Komplex auf Mobile

Hoher Ressourcenverbrauch

Schwierige Verteilung
```

---

## 4. Runtime Architektur

```text
Plugin

↓

Plugin Host

↓

Capability Layer

↓

VitaFabric
Identity
Consent
Filesystem APIs
Event Bus
```

---

## 5. Unterstützte Erweiterungstypen

Die Plattform unterstützt sechs Erweiterungstypen.

```text
Connector

Integration

Provider

Storage

UI

Application
```

Eine Application ist ein spezialisierter Plugin-Typ mit UI, Navigation,
Workflows und Settings, der die gemeinsamen Plattformdienste nutzt.

---

## 6. Plugin Paketstruktur

Jedes Plugin besteht aus:

```text
plugin.wasm

manifest.json

permissions.json

signature.json

README.md
```

---

## 7. Plugin Manifest

Beispiel:

```json
{
  "id": "garmin_connector",
  "name": "Garmin Connector",
  "version": "1.0.0",
  "type": "connector",
  "capabilities": [
    "READ_PATIENT",
    "WRITE_OBSERVATION",
    "NETWORK_ACCESS"
  ]
}
```

---

## 8. Lebenszyklus

### Installation

```text
Signatur prüfen

↓

Manifest validieren

↓

Capabilities prüfen

↓

Registrieren
```

---

### Aktivierung

```text
Plugin laden

↓

Runtime erzeugen

↓

Capabilities anwenden
```

---

### Deaktivierung

```text
Runtime stoppen

↓

Events beenden

↓

Sessions schließen
```

---

### Entfernung

```text
Plugin deaktivieren

↓

Plugin entfernen

↓

Capabilities widerrufen
```

---

## 9. Isolationsmodell

Plugins laufen isoliert.

---

### Verboten

```text
Direkter Datenbankzugriff

Direkter Dateisystemzugriff

Direkter Netzwerkzugriff

Direkter Secret-Zugriff

Plugin-zu-Plugin Zugriff
```

---

### Erlaubt

Nur über freigegebene APIs.

```text
Filesystem API

Network API

VitaFabric API

Consent API

Event Bus API
```

Datei- und Netzwerkzugriff bleiben standardmäßig deaktiviert. Erlaubte
Dateizugriffe erfolgen ausschließlich auf plugin-eigenen Speicher über den
Host; Netzwerkzugriffe laufen über einen kontrollierten Host-Proxy, der Ziele
und Capability prüft. WASI-Interfaces dürfen keine weitergehenden Rechte
freischalten. Die Plattform verweigert Plugin-Ausführung, wenn die jeweilige
Host-Plattform Speicher-, CPU-, Zeit- und Import-Limits nicht durchsetzen
kann.

---

## 10. Ressourcenbegrenzung

Jede Runtime besitzt Limits.

---

### CPU

```text
Max CPU Budget
```

---

### Speicher

```text
Max RAM Budget
```

---

### Laufzeit

```text
Timeouts
```

---

### Event-Verarbeitung

```text
Rate Limits
```

---

## WIT Interface Catalog

Die folgenden versionierten Host-Imports sind Vertragsbereiche, noch keine
veröffentlichten WIT-Dateien. RFC-0019 beschreibt Paket und Vertragsarbeit;
WASI vermittelt ohne explizite Freigabe weder Datei- noch Netzwerkzugriff.

| Interface | Zugang und Grenze |
| --- | --- |
| Filesystem | Host-vermittelter, pluginisolierter Speicher; kein Pfad zum Host-Dateisystem oder Gesundheitsdatenstore. |
| Event | Registrierte Typen publizieren/abonnieren; Reautorisierung und minimale Payload. |
| Identity | Nur für den Aufruf erforderliche opake Identitätskontexte, keine Credentials. |
| Consent | Freigabestatus im eigenen Scope abfragen; keine Freigabe selbst ausstellen. |
| VitaFabric | Autorisierte FHIR-Operationen über das Gateway, kein direkter Storage. |
| Secret | Opake Handles und hostvermittelte Nutzung; keine Schlüssel oder Passwörter auslesen. |
| Network | Hostproxy mit expliziter Ziel- und Methodenfreigabe; kein direkter Socket. |

Die konkreten Signaturen, Datenformate, Fehler, Versionskompatibilität und
Ausführungsgrenzen sind vor Plugin-Implementierung als WIT zu veröffentlichen.

## Runtime Resource Limits

Jede Instanz erhält durch den Host durchgesetzte Obergrenzen für RAM,
CPU/Fuel, Wandzeit pro Aufruf, verschlüsselten Disk-Verbrauch, Netzwerkziele
und -Bytes sowie gleichzeitige Events und Queue-Größe. Keine Ressource ist
implizit unbegrenzt. Überschreitung beendet oder unterbricht den Aufruf,
verhindert einen Teil-Commit, erzeugt einen datensparsamen Fehler und
isoliert das Plugin; Limits dürfen nicht umgangen werden. Netzwerkproxy
validiert auch DNS-Auflösung und jeden Redirect; private/lokale Ziele sind
ohne gesonderte Freigabe gesperrt.

Numerische Budgets, Betriebssystem-Durchsetzung und Abbruchsemantik sind für
die jeweilige Zielplattform zu messen und vor Freigabe zu beschließen.
Insbesondere sind Fuel und Timeout kein Nachweis einer vollständigen
CPU-Isolation. Zu niedrige Limits können legitime Imports abbrechen; zu hohe
beeinträchtigen Reaktionszeit und Speicher anderer Anwendungen.

## 11. Netzwerkmodell

### Standard

```text
kein Netzwerkzugriff
```

---

### Voraussetzung

Capability:

```text
NETWORK_ACCESS
```

---

### Netzwerk Audit

Pflicht:

```text
Zielsystem

Zeitpunkt

Plugin

Ergebnis
```

---

## 12. Dateisystemmodell

### Standard

```text
kein Zugriff
```

---

### Freigegeben

Nur Plugin Sandbox.

```text
plugin_storage/
```

---

### Verboten

```text
Systemordner

Datenbankdateien

Secrets
```

---

## 13. Datenzugriff

Alle Gesundheitsdaten laufen über VitaFabric.

Pflichtpfad:

```text
Plugin

↓

Capability Check

↓

Consent Check

↓

VitaFabric

↓

FHIR
```

---

Nicht zulässig:

```text
Plugin

↓

Datenbank
```

---

## 14. Event Bus Integration

Plugins kommunizieren über den Event Bus.

---

### Subscribe

```text
FHIR_CREATED

FHIR_UPDATED

CONSENT_REVOKED
```

---

### Publish

Nur definierte Eventtypen.

---

## 15. Secret Management

Plugins erhalten niemals:

```text
Passwörter

Private Keys

Recovery Keys
```

---

### Zugriff

Ausschließlich über:

```text
Secret API
```

---

## 16. Consent Integration

Ein Plugin darf nie selbst entscheiden:

```text
ob Zugriff erlaubt ist
```

---

Die Plattform prüft:

```text
Identity

Consent

Capability
```

---

## 17. Plugin Kommunikation

Direkte Kommunikation verboten.

---

Nicht erlaubt:

```text
Plugin A

↓

Plugin B
```

---

Erlaubt:

```text
Plugin A

↓

Event Bus

↓

Plugin B
```

---

## 18. Plugin Signaturen

### Community

```text
Self Signed
```

---

### Verified

```text
Maintainer Sign-Off
```

Das Sign-Off bestätigt die Maintainer-Freigabe; das genaue Signatur- und
Prüfverfahren bleibt zu spezifizieren.

---

### Official

```text
Project Signing Key
```

---

Signatur bedeutet:

```text
Integrität
```

nicht:

```text
Sicherheitsgarantie
```

---

## 19. Offline Support

Pflicht:

```text
Installation

Aktivierung

Nutzung

Deinstallation
```

ohne Internet.

---

## 20. Fehlerisolierung

Pluginfehler dürfen niemals:

```text
VitaFabric stoppen

LifeLedger stoppen

Identity stoppen
```

---

Plugins dürfen ausschließlich ihre eigene Runtime beeinträchtigen.

---

## 21. Logging

Pflichtfelder:

```text
Plugin ID

Version

Event

Capability

Fehler
```

---

## 22. Audit Anforderungen

Jeder Zugriff protokolliert:

```text
Plugin

Nutzer

Capability

Zeitpunkt

Erfolg
```

---

## 23. SDK

Die Plattform stellt bereit:

```text
Plugin SDK

Fixtures

Testdaten

Konformitätssuite
```

---

## 24. Referenzimplementierung

Der erste Referenzplugin-Typ ist:

```text
Connector
```

über VitaFabric.

Keine produktiven Gesundheitsdaten.

Synthetische Testdaten.

---

## 25. Zukunft

### Phase 1

```text
WASM Plugins
```

---

### Phase 2

```text
Python Connector Runtime
```

nur für ausgewählte Connectoren.

---

### Phase 3

```text
Remote Execution Worker
```

für optionale Spezialfälle.

---

## 26. Sicherheitsanforderungen

Pflicht:

```text
Sandboxing

Capability Enforcement

Consent Enforcement

Audit Logging

Offline Betrieb

Fehlerisolierung

Signaturprüfung
```

---

Nicht zulässig:

```text
Direkter DB Zugriff

Direkter OS Zugriff

Direkte Secrets

Cloud-Zwang
```

---

## 27. Architekturentscheidung

Dieses RFC legt fest:

✅ WASM First

✅ Sandboxed Runtime

✅ Capability Enforcement

✅ Consent Enforcement

✅ VitaFabric als einziger Gesundheitsdatenpfad

✅ Event Bus basierte Kommunikation

✅ Signierte Pakete

✅ Offline Installation

✅ Fehlerisolierung

✅ Plattformweite Auditierbarkeit

✅ Kein direkter Datenbankzugriff

✅ Kein implizites Vertrauen in Plugins
