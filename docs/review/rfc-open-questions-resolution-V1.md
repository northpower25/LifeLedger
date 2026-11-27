# RFC Konsolidierungs- und Änderungsplan

Status: Nach Architekturreview RFC-0003 bis RFC-0013

---

# Phase 1 – Blocking Issues

Diese Punkte sollten vor Beginn einer eigentlichen Implementierung erledigt werden.

---

## RFC-0014 Core Runtime & Platform Boundaries

Neu erstellen.

Ziel:

Zentrale Klärung:

- Platform Core
- VitaFabric
- LifeWeaver
- Applications
- Plugins

Festlegen:

Was MUSS Plattform sein?

Was DARF Plugin sein?

Was DARF NIEMALS Plugin sein?

---

## RFC-0009 Marketplace Governance

Abschnitt:

Verified Listings

Arbeitsauftrag:

Sign-Off Verfahren definieren.

Ergänzen:

- Anzahl Reviewer
- Ablehnungsprozess
- Rezertifizierung
- Signaturworkflow

---

## RFC-0010 Zero Knowledge Sync

Abschnitt:

Conflict Resolution Workflow

Arbeitsauftrag:

Konfliktmodell fertig spezifizieren.

Fehlend:

- Delete vs Update
- Merge-Regeln
- Konfliktpriorität
- Manueller Review
- UI-Verhalten

---

## RFC-0011 AI Provider Framework

Abschnitt:

Embedding Management

Arbeitsauftrag:

Löschprotokoll definieren.

Fehlend:

- Soft Delete
- Hard Delete
- Embedding Reindex
- Retention

---

# Phase 2 – Implementierungsreife

---

## RFC-0006 Plugin Runtime

Arbeitsauftrag:

WASM Runtime konkretisieren.

Festlegen:

- Wasmtime oder Wasmer
- WASI Version
- Component Model
- Sandboxing Grenzen

---

## RFC-0007 Application Framework

Arbeitsauftrag:

App Abhängigkeiten ergänzen.

Fehlend:

- Dependency Management
- App Migration
- Upgrade Strategy
- Compatibility Matrix

---

## RFC-0012 Governance

Arbeitsauftrag:

Maintainer Succession ergänzen.

Fehlend:

- Ausfall Core Maintainer
- Schlüsselübergabe
- Marketplace Vertretung
- Security Team Vertretung

---

# Phase 3 – Dokumentationsqualität

---

## RFC-0004 Capability Model

Arbeitsauftrag:

Capability Risk Levels operationalisieren.

Derzeit:

```text
Niedrig
Mittel
Hoch
Kritisch
```

Fehlend:

- Genehmigungsprozess
- Reviewprozess
- Auditpflicht je Stufe

---

## RFC-0005 Event Bus

Arbeitsauftrag:

Event Naming Convention.

Neues Kapitel:

```text
EVENT_CATEGORY

EVENT_NAME

EVENT_VERSION
```

---

## RFC-0011 AI Provider Framework

Arbeitsauftrag:

OpenAI-kompatible APIs formalisieren.

Beispiele:

```text
OpenRouter

LM Studio

vLLM

LiteLLM
```

Klassifikation definieren.
