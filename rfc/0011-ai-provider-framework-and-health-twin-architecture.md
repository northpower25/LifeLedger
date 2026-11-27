# RFC 0011: AI Provider Framework & Health Twin Architecture

- Status: Draft
- Type: Architecture RFC
- Owner: LifeWeaver
Depends On: RFC-0003 Identity & Consent Framework  
Depends On: RFC-0004 Capability Model  
Depends On: RFC-0005 Event Bus Architecture  
Depends On: RFC-0006 Plugin Runtime & Isolation  
Depends On: RFC-0010 Zero Knowledge Sync

Blocks:
- RAG
- MCP Integration
- Provider Plugins
- Health Twin
- Agent Runtime
- AI Marketplace

---

## 1. Zusammenfassung

Dieses RFC definiert:

```text
AI Provider Framework

MCP Integration

RAG Architektur

Embedding Verwaltung

Knowledge Twin

Health Twin

Predictive Twin
```

für LifeWeaver.

Der erste AI-Anwendungsfall ist die Zusammenfassung eines Dokuments.

LifeWeaver bleibt eine optionale Plattformfunktion.

Der lokale Kern von LifeLedger benötigt LifeWeaver nicht. Die Roadmaps definieren AI explizit als optionalen Teil der Plattform.

---

## 2. Ziele

### Ziele

```text
Providerneutralität

Lokale Modelle

Optionale Cloud Provider

RAG

MCP

Health Twin

Mehrere Provider
```

---

### Nichtziele

```text
Diagnose

Therapieempfehlung

Medizinische Entscheidungen

Klinische Bewertung
```

Diese Funktionen bleiben ausdrücklich außerhalb des Projektumfangs.

---

## 3. Grundprinzipien

### Provider Neutrality

Kein Provider darf fest eingebaut sein.

---

### AI Optional

Alle Kernfunktionen funktionieren ohne KI.

---

### Consent First

AI erhält niemals ungeprüft Daten.

---

### Local First

Lokale Modelle haben Vorrang.

---

### Explainability

Der Nutzer muss erkennen:

```text
Welche Daten verwendet wurden

Welcher Provider genutzt wurde

Welche Quellen eingeflossen sind
```

---

## 4. LifeWeaver Architektur

```text
Applications

↓

LifeWeaver

├── Provider Layer
├── MCP Layer
├── RAG Layer
├── Twin Layer
└── Consent Gateway

↓

VitaFabric
```

---

## 5. Provider Taxonomie

Es existieren drei Providerklassen.

---

## 6. Local Provider

Beispiele:

```text
Ollama

LM Studio

vLLM

llama.cpp
```

---

### Vorteile

```text
Keine Datenübertragung

Offline Betrieb

Volle Kontrolle
```

---

## 7. Remote Provider

Beispiele:

```text
OpenAI

Anthropic

Google

Mistral
```

---

### Voraussetzungen

```text
Explizite Zustimmung

Provider Plugin

Capability

Audit
```

---

## 8. Managed Provider

Zukünftige Option.

---

Beispiele:

```text
LifeLedger Managed AI
```

---

Erfordert separates Architekturreview.

---

## 9. Provider Plugins

Provider werden über Plugins angebunden.

---

Pflicht:

```text
Provider Interface
```

---

Beispiel:

```text
complete()

embed()

chat()

tool_call()
```

### OpenAI-kompatible API-Klassifikation

„OpenAI-kompatibel“ bezeichnet Protokoll-/API-Kompatibilität, nicht
Vertrauenswürdigkeit, Datenschutz oder identisches Modellverhalten. Ein
Adapter MUSS pro Provider und Modell deklarieren, welche Endpunkte und
Funktionen tatsächlich getestet sind; nicht unterstützte Felder dürfen nicht
still ignoriert werden. Basisschnittstellen sind Chat Completions und
Embeddings mit OpenAI-kompatiblen JSON-Request-/Response-Schemas. Streaming,
Tool Calls, strukturierte Ausgaben und provider-spezifische Endpunkte sind
optionale, einzeln zu deklarierende Erweiterungen.

| Klasse | Beispiele | Einordnung |
|---|---|---|
| Inference Server | vLLM, LM Studio | Lokal oder selbst betrieben; tatsächlicher Datenpfad hängt von Deployment und Konfiguration ab |
| Router/Gateway | OpenRouter, LiteLLM | Vermittelt an einen oder mehrere Provider; Datenübertragung und Unterauftragsverarbeiter sind pro Ziel zu prüfen |
| Cloud Provider | Anbieter mit OpenAI-kompatiblem Endpoint | Drittanbieter-Verarbeitung; erfordert Remote-Provider-Capability, zweckgebundene Zustimmung und Audit |

Klassifiziert wird nach tatsächlichem Deployment und Datenempfänger, nicht
nur nach Produktname oder API-Format. Die Kompatibilitätskennzeichnung
erlaubt keine automatische Provider-Auswahl oder stillen Fallback.

---

## 10. Capability Anforderungen

Lokale Modelle:

```text
AI_LOCAL_MODEL
```

---

Remote Modelle:

```text
AI_REMOTE_PROVIDER
```

---

RAG:

```text
AI_RAG
```

---

Agenten:

```text
AI_AGENT
```

---

## 11. MCP Architektur

MCP wird als standardisierte Tool-Schicht betrachtet.

---

### Rollen

```text
MCP Client

MCP Server
```

---

### Toolzugriff

Nur über:

```text
Capabilities

Consent

Audit
```

---

## 12. Tool Isolation

MCP Tools dürfen niemals:

```text
Consent umgehen

Capabilities umgehen

VitaFabric umgehen
```

---

## 13. RAG Architektur

### Ziel

Quellengebundene Antworten.

---

### Datenquellen

```text
FHIR Ressourcen

Dokumente

Timeline

Freigegebene Daten
```

---

## 14. Embedding Modell

Embedding Speicherung erfolgt getrennt.

Embeddings gehören zur VitaFabric-Datenklasse Derived Data gemäß RFC-0013,
ebenso Knowledge Graph, AI Summaries und Derived Metadata. Sie sind von
FHIR-Datensätzen getrennt, umgehen aber nicht VitaFabric, Consent oder
Capability Enforcement.

---

```text
Embeddings

≠

FHIR Datensatz
```

---

## 15. Embedding Speicher

MVP:

```text
Lokal

Verschlüsselt
```

Nicht:

```text
automatisch in Cloud
```

### Metadaten

Embeddings und weitere Derived Data werden ausschließlich über VitaFabric
verwaltet. Für jedes Objekt werden Quell-IDs und Quellversionen, Modell- und
Indexversion, Erstellungszeitpunkt, Consent-Kontext sowie Speicherorte
nachvollziehbar geführt.

---

## 16. Embedding Widerruf und Löschprotokoll

#### Soft Delete

Bei Consent-Widerruf, Quellenlöschung, Profil-Löschung oder explizitem
Löschauftrag wird der Zugriff sofort gesperrt. Die betroffenen Embeddings
werden als „zur Löschung vorgemerkt“ markiert und dürfen weder für Suche,
RAG, Training noch Export verwendet werden. Nur opake Löschmetadaten und
Tombstones dürfen zur Verteilung des Löschauftrags verbleiben.

#### Hard Delete und Retention

Ein Purge-Job entfernt innerhalb von 24 Stunden Embeddings, Vektorindex-
Einträge, abgeleitete Caches und Replikate aus allen online verfügbaren
Stores. Verschlüsselte Backups dürfen die Daten höchstens 30 Tage enthalten;
für jedes Objekt ist, soweit technisch möglich, ein eigener Backup-
Verschlüsselungsschlüssel vorzusehen, der bei Widerruf oder Löschauftrag
sofort kryptografisch vernichtet wird. Enthalten nicht selektiv löschbare
Backups noch verschlüsselte Kopien, bleiben diese bis zur Rotation/Expiration
unzugänglich und dürfen nicht wiederhergestellt werden, ohne den Tombstone
erneut anzuwenden. Bei Profil-/Kontolöschung werden ausschließlich dafür
genutzte Backup-Schlüssel sofort kryptografisch vernichtet.
Audit- und Sync-Tombstones dürfen keine Embedding-Inhalte oder rückführbaren
Gesundheitsdaten enthalten und werden nach der festgelegten Audit- bzw.
Tombstone-Retention entfernt.

`EMBEDDING_PURGED` wird erst nach bestätigtem Purge aller registrierten
Online-Stores publiziert und enthält nur opake Objekt-IDs, Modell-/Index-
Versionen, Status und Zeit. Fehler oder offline Stores bleiben als ausstehend
sichtbar und werden erneut bearbeitet; der Status darf keinen erfolgreichen
Purge vortäuschen.

#### Reindex

Nach Modell-, Index- oder Schemawechsel werden Embeddings aus der autoritativen
VitaFabric-Quelle neu aufgebaut. Vor Reindex werden Consent und Capability
erneut geprüft. Widerrufene oder gelöschte Quellen werden nicht regeneriert.
Während eines Reindex bleibt die bisherige gültige Indexversion verfügbar,
bis die neue Version validiert und atomar aktiviert wurde; betroffene
Löschungen sind davon ausgenommen und bleiben sofort gesperrt.

---

---

## 17. Quellenmodell

Jede Antwort enthält:

```text
Quelle

Referenz

Zeitpunkt
```

---

Beispiel:

```text
Dokument A

Observation B

Medication C
```

---

## 18. Knowledge Twin

Erste Umsetzungsstufe.

---

Kann:

```text
Suchen

Zusammenfassen

Verknüpfen

Erklären
```

---

Darf nicht:

```text
Diagnostizieren
```

---

## 19. Health Twin

Zweite Ausbaustufe.

---

Kann:

```text
Zeitreihen analysieren

Korrelationen erkennen

Veränderungen darstellen
```

---

Beispiele:

```text
Gewicht

Blutdruck

Aktivität
```

---

## 20. Predictive Twin

Dritte Ausbaustufe.

---

Kann:

```text
Trends schätzen

Risiken berechnen

Prognosen erzeugen
```

---

Erfordert separate regulatorische Prüfung.

---

## 21. AI Agenten

Agenten sind optional.

---

Agenten dürfen:

```text
Lesen

Zusammenfassen

Arbeiten koordinieren
```

---

Agenten dürfen nicht:

```text
Freigaben ändern

Consent vergeben

Rollen ändern
```

---

## 22. Datenübertragung

Remote Provider erhalten nur:

```text
freigegebene Daten
```

---

Nie:

```text
gesamtes Profil
```

---

## 23. Consent Modell

Vor jeder Übertragung:

```text
Consent Check
```

---

Nutzer müssen sehen:

```text
Welche Daten

Welcher Provider

Welcher Zweck
```

---

## 24. Audit Anforderungen

Audit speichern:

```text
Provider

Prompt

Datenmenge

Zeitpunkt

Antwortstatus
```

---

Keine Speicherung von Geheimnissen.

---

## 25. Event Bus Integration

Events nach RFC-0005.

---

Beispiele:

```text
AI_REQUEST

AI_RESPONSE

PROVIDER_CONSENT_GRANTED

PROVIDER_CONSENT_REVOKED

EMBEDDING_CREATED

EMBEDDING_DELETED

EMBEDDING_PURGED

PROVIDER_CHANGED
```

---

## 26. Health Data Protection

Pflicht:

```text
Consent

Capability

Audit

Data Minimization
```

---

## 27. Halluzinationen

System muss deutlich kennzeichnen:

```text
KI Antwort

≠

medizinische Tatsache
```

---

## 28. Benutzeroberfläche

Nutzer müssen erkennen:

```text
Quelle

Provider

Vertrauensniveau

Lokales Modell oder Cloud Modell
```

---

## 29. Sicherheitsanforderungen

Pflicht:

```text
Provider Isolation

Consent Enforcement

Capability Enforcement

Audit Logging

Data Minimization
```

---

## 30. Nicht zulässig

```text
Diagnose Automatisierung

Therapievorschläge

Versteckte Cloud Nutzung

Stiller Provider Wechsel

Nicht dokumentierte Datenübertragung
```

---

## 31. Entwicklungsreihenfolge

Die Twin-Ausbaustufen sind unabhängig von der Reihenfolge einzelner
Provider- und RAG-Funktionen:

```text
Phase 1: Knowledge Twin
Phase 2: Health Twin
Phase 3: Predictive Twin
```

Der erste Anwendungsfall ist die Dokumentenzusammenfassung. Lokale Provider
haben Vorrang; Remote Provider bleiben optional und erfordern vor einer
Übertragung eine ausdrückliche Zustimmung. Die Freigabe jeder Ausbaustufe
setzt deren Sicherheits- und Zweckbestimmungsprüfung voraus.

---

### Regulatorische Einordnung

EU AI Act, EU-Medizinprodukteverordnung (MDR) und Anforderungen an Clinical
Decision Support sind anhand der konkreten Zweckbestimmung, Funktionen und
Einsatzorte vor einer Freigabe fachlich und rechtlich zu prüfen. Dieses RFC
stellt weder eine rechtliche Einordnung noch eine Konformitäts- oder
Zulassungsbehauptung dar. Diagnose, Therapieempfehlung und medizinische
Entscheidungen bleiben gemäß §2 und §30 ausgeschlossen.

---

## 32. Architekturentscheidung

Dieses RFC legt fest:

✅ Providerneutrale Architektur

✅ Lokale Modelle zuerst

✅ MCP Unterstützung

✅ RAG Unterstützung

✅ Quellengebundene Antworten

✅ Knowledge Twin als erste Ausbaustufe

✅ Health Twin als zweite Ausbaustufe

✅ Predictive Twin separat bewertet

✅ Consent First

✅ Audit Pflicht

✅ Embedding Widerruf

✅ Kein AI-Zwang für Kernfunktionen
