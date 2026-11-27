# RFC Konsolidierungs- und Änderungsplan

Status: Review-Aufträge in den RFC-Drafts konsolidiert (2026-11-27)

Die folgenden Punkte dienten als Arbeitsaufträge für die Überarbeitung. Die
Entscheidungen sind in den genannten RFCs als Vorschläge konkretisiert; die
RFCs bleiben Drafts und sind weder angenommene Architektur noch Nachweis einer
Implementierung. Insbesondere Quoren, Fristen und Retentionswerte bedürfen
vor produktivem Betrieb der Governance-, Sicherheits- und Datenschutzprüfung.

---

# Phase 1 – Blocking Issues

Diese Punkte sollten vor Beginn einer eigentlichen Implementierung erledigt werden.

---

## RFC-0014 Core Runtime & Platform Boundaries

Grenzen in RFC-0014 konkretisiert.

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

Ergebnis: verpflichtende, intern austauschbare Core-Verträge; VitaFabric als
einziger Health-Data-Gateway-Owner; LifeWeaver optional; Applications als
spezialisierte Plugins; nicht umgehbare Identity-, Consent-, Capability-,
Audit-, Schlüssel- und Datenvertragskontrollen.

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

Ergebnis: zwei unabhängige Reviewer, dokumentierte Ablehnung und Einspruch,
Rezertifizierung spätestens nach zwölf Monaten bzw. bei sicherheits- oder
vertrauensrelevanten Änderungen und Signatur des freigegebenen Paket-Digests.

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

Ergebnis: kausale Versionierung ohne Zeitstempelpriorität, begrenzter Merge
nur für explizit unabhängige Felder, Tombstone vor nebenläufigem Update,
manuelle Auflösung samt gesperrtem Konfliktzustand und Audit.

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

Ergebnis: sofortige Zugriffssperre beim Soft Delete, Online-Purge innerhalb
24 Stunden, Backup-Retention höchstens 30 Tage, expliziter Reindex aus
autoritativen VitaFabric-Quellen und Statusereignis erst nach bestätigtem
Purge der registrierten Online-Stores.

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

Ergebnis: Wasmtime, WebAssembly Component Model und WASI 0.2 (Preview 2);
versionierte WIT-Schnittstellen, gepinnte Runtime-Abhängigkeiten und
fail-closed Ausführung ohne Umgehungs-Fallback.

---

## RFC-0007 Application Framework

Arbeitsauftrag:

App Abhängigkeiten ergänzen.

Fehlend:

- Dependency Management
- App Migration
- Upgrade Strategy
- Compatibility Matrix

Ergebnis: deklarative Abhängigkeiten und Digest-Lockfile, offlinefähige
Staging-Migrationen, atomare Upgrades mit Rollback und Kompatibilitätsprüfung
für Manifest, Platform API, ABI und App-Datenschema.

---

## RFC-0012 Governance

Arbeitsauftrag:

Maintainer Succession ergänzen.

Fehlend:

- Ausfall Core Maintainer
- Schlüsselübergabe
- Marketplace Vertretung
- Security Team Vertretung

Ergebnis: benannte Stellvertretungen für Core-, Marketplace- und
Security-Rollen, befristete Ausfallvertretung mit Mehrpersonenquorum und
kontrollierter Schlüsselrotation. Fristen und Quoren bleiben vor Betrieb
governancepflichtig.

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

Ergebnis: Mindestfreigabe, Review und Audit für jede Risikostufe; Default
Deny, Höherstufung nach größtem Schadenspotenzial und unabhängige Reviews bei
hohen bzw. kritischen Capabilities.

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

Ergebnis: versioniertes `<category>.<name>.v<version>`-Routing, registrierte
Kategorien/Owner, inkompatible Schemaänderung nur mit neuer Event-Version.

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

Ergebnis: Trennung zwischen Inference Server, Router/Gateway und Cloud
Provider; API-Kompatibilität wird pro Modell und Endpoint deklariert und
begründet keine Vertrauens- oder Sicherheitsstufe.
