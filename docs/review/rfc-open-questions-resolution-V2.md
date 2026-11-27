# LifeLedger RFC Remediation Plan
# Arbeitsaufträge für GitHub Copilot
# Ziel: Implementierungsreife für den ersten Offline Vertical Slice

Bearbeitungsstand und weiterhin unerfüllte Startbedingungen:
[Offene Informationen für die erste Testversion](offene-informationen-erste-testversion.md).
Die folgenden Aufträge und die Definition of Done bleiben als ursprüngliche
Vorgaben erhalten; die RFC-Ergänzungen sind weiterhin Entwürfe.

Status: Architektur weitgehend geklärt
Ziel: Nach Abschluss dieses Backlogs soll die Implementierung des ersten
lauffähigen Prototyps beginnen können.

Referenzen:

- RFC-0001 bis RFC-0019
- Gesamt-Roadmap
- RFC Implementierungsreife Review

---

# PHASE A
# First Offline Vertical Slice Blocker

Diese Arbeiten müssen abgeschlossen sein bevor mit
der eigentlichen Plattformimplementierung begonnen wird.

---

# A-001
# RFC-0002 Platform Core Architecture

Priorität: Kritisch

## Problem

Core Runtime ist definiert.

Die tatsächliche Laufzeittopologie ist nicht definiert.

Unklar:

- Tauri ⇄ FastAPI
- IPC
- Startreihenfolge
- Shutdown
- Authentifizierung zwischen Prozessen

## Arbeitsauftrag

Neuen Abschnitt ergänzen:

```md
## Runtime Topology
```

Inhalt:

```text
Tauri Desktop Host

↓

Local IPC

↓

FastAPI Service

↓

VitaFabric

↓

SQLite
```

Zusätzlich:

```text
Startup Sequence

Shutdown Sequence

Failure Modes

Trust Boundaries
```

## Ergebnis

Implementierbare Runtime-Struktur.

---

# A-002
# RFC-0003 Identity & Consent

Priorität: Kritisch

## Problem

Consent besitzt kein Lebenszyklusmodell.

## Arbeitsauftrag

Neuen Abschnitt ergänzen:

```md
## Consent State Machine
```

Status:

```text
DRAFT
ACTIVE
REVOKED
EXPIRED
SUSPENDED
```

---

Zusätzlich:

```md
## Consent Ownership Rules
```

Festlegen:

```text
Wer erstellt Consent

Wer darf ändern

Wer darf widerrufen

Wer darf erneuern
```

---

# A-003
# RFC-0003 Identity & Consent

Priorität: Kritisch

## Problem

Bootstrap des ersten Benutzers fehlt.

## Arbeitsauftrag

Neuen Abschnitt ergänzen:

```md
## System Bootstrap
```

Definieren:

```text
Erster Owner

Erstes Gerät

Erste Sitzung

Erstes MFA Setup
```

---

# A-004
# RFC-0013 VitaFabric

Priorität: Kritisch

## Problem

FHIR Ressourcen vorgegeben

aber nicht verbindlich festgelegt.

## Arbeitsauftrag

Neuen Abschnitt ergänzen:

```md
## MVP Resource Contract
```

Festlegen:

```text
Patient

Observation

Condition

MedicationStatement

AllergyIntolerance

DocumentReference
```

Keine weiteren Ressourcen
für MVP.

---

# A-005
# RFC-0013 VitaFabric

Priorität: Kritisch

## Problem

Validierungsfehler unklar.

## Arbeitsauftrag

Neuen Abschnitt ergänzen:

```md
## Validation Failure Behaviour
```

Strategie:

```text
REJECT

WARN

QUARANTINE
```

Kein stilles Korrigieren.

---

# PHASE B
# Plattformverträge

---

# B-001
# RFC-0004 Capability Model

Priorität: Hoch

## Arbeitsauftrag

Neuen Abschnitt ergänzen:

```md
## Capability Evaluation Flow
```

Pfad:

```text
Identity

↓

Consent

↓

Capability

↓

Policy

↓

Resource Access
```

---

# B-002
# RFC-0004 Capability Model

Priorität: Hoch

## Arbeitsauftrag

Neuen Abschnitt ergänzen:

```md
## Capability Lifecycle
```

Zustände:

```text
Requested

Approved

Active

Revoked

Expired
```

---

# B-003
# RFC-0005 Event Bus

Priorität: Hoch

## Arbeitsauftrag

Neuen Abschnitt ergänzen:

```md
## Delivery Guarantees
```

Empfehlung:

```text
At Least Once
```

---

# B-004
# RFC-0005 Event Bus

Priorität: Hoch

## Arbeitsauftrag

Neuen Abschnitt ergänzen:

```md
## Event Retention
```

Definieren:

```text
Audit

Replay

Debugging

Sync
```

inkl.

```text
Retention
Deletion
Archiving
```

---

# PHASE C
# Plugin Framework

---

# C-001
# RFC-0006 Plugin Runtime

Priorität: Hoch

## Arbeitsauftrag

Neuen Abschnitt ergänzen:

```md
## WIT Interface Catalog
```

Mindestens:

```text
Filesystem API

Event API

Identity API

Consent API

VitaFabric API

Secret API

Network API
```

---

# C-002
# RFC-0006 Plugin Runtime

Priorität: Hoch

## Arbeitsauftrag

Neuen Abschnitt ergänzen:

```md
## Runtime Resource Limits
```

Definieren:

```text
RAM

CPU

Execution Time

Disk

Network

Concurrent Events
```

---

# C-003
# RFC-0019 Plugin APIs

Priorität: Hoch

## Arbeitsauftrag

RFC vollständig ausarbeiten.

Pflichtinhalte:

```text
Manifest Schema

Permission Schema

Package Format

WIT Contracts

Compatibility Rules

SDK Contracts

Compliance Suite
```

---

# PHASE D
# Family & Consent

---

# D-001
# RFC-0008 Family Model

Priorität: Mittel

## Arbeitsauftrag

Neuen Abschnitt ergänzen:

```md
## Guardian Verification
```

Definieren:

```text
Nachweis

Vormundschaft

Vertretung

Dokumentation
```

---

# D-002
# RFC-0008 Family Model

Priorität: Mittel

## Arbeitsauftrag

Neuen Abschnitt ergänzen:

```md
## Jurisdiction Model
```

Version 1:

```text
Deutschland

EU

International
```

---

# D-003
# RFC-0008 Family Model

Priorität: Mittel

## Arbeitsauftrag

Neuen Abschnitt ergänzen:

```md
## Age Transition Workflow
```

Ablauf:

```text
Minor

↓

Transition

↓

Adult Owner
```

---

# PHASE E
# AI

---

# E-001
# RFC-0011 AI Provider Framework

Priorität: Mittel

## Arbeitsauftrag

Neuen Abschnitt ergänzen:

```md
## Prompt Retention Policy
```

Regeln:

```text
Store

Encrypt

Delete

Audit
```

---

# E-002
# RFC-0011 AI Provider Framework

Priorität: Mittel

## Arbeitsauftrag

Neuen Abschnitt ergänzen:

```md
## Embedding Retention Policy
```

Regeln:

```text
Create

Rebuild

Delete

Purge
```

---

# E-003
# RFC-0011 AI Provider Framework

Priorität: Mittel

## Arbeitsauftrag

Neuen Abschnitt ergänzen:

```md
## Local AI Requirements
```

Definieren:

```text
RAM

CPU

GPU

Storage
```

---

# PHASE F
# Marketplace & Governance

---

# F-001
# RFC-0009 Marketplace

Priorität: Mittel

## Arbeitsauftrag

Neuen Abschnitt ergänzen:

```md
## Key Rotation
```

---

# F-002
# RFC-0009 Marketplace

Priorität: Mittel

## Arbeitsauftrag

Neuen Abschnitt ergänzen:

```md
## Offline Trust Behaviour
```

Behandeln:

```text
Expired Keys

Revoked Keys

Missing CRL

Offline Installation
```

---

# F-003
# RFC-0012 Governance

Priorität: Mittel

## Arbeitsauftrag

Neuen Abschnitt ergänzen:

```md
## Maintainer Succession Policy
```

---

# F-004
# RFC-0012 Governance

Priorität: Mittel

## Arbeitsauftrag

Neuen Abschnitt ergänzen:

```md
## Security Escalation Matrix
```

---

# PHASE G
# Spezifikationsebene

Diese RFCs müssen implementierungsfähig vorliegen.

---

# RFC-0015

FHIR Profiles & Terminology

Pflicht:

```text
FHIR Profiles

ValueSets

Terminologies

Validator Config

Test Fixtures
```

---

# RFC-0016

Platform API Standards

Pflicht:

```text
OpenAPI

Errors

Auth

Audit

Versioning
```

---

# RFC-0017

Event Schemas

Pflicht:

```text
JSON Schema

Registry

Compatibility Rules
```

---

# RFC-0018

Identity APIs

Pflicht:

```text
Identity Endpoints

Consent Endpoints

Household Endpoints

Emergency Endpoints
```

---

# RFC-0019

Plugin APIs

Pflicht:

```text
Manifest Schema

WIT Contracts

SDK Interface

Compliance Tests
```

---

# Definition of Done

Die erste Implementierungsphase darf beginnen wenn:

✅ RFC-0014 akzeptiert

✅ RFC-0015 vollständig

✅ RFC-0016 vollständig

✅ RFC-0017 vollständig

✅ RFC-0018 vollständig

✅ RFC-0019 vollständig

✅ Alle Phase-A Punkte umgesetzt

✅ Offene Blocker aus dem Implementierungsreview geschlossen

✅ Erster synthetischer Offline-Vertical-Slice definiert

✅ FHIR-MVP-Ressourcen festgelegt

✅ Security- und Consent-Flows spezifiziert

Danach kann mit dem ersten lauffähigen Prototypen begonnen werden:

```text
Tauri

↓

FastAPI

↓

VitaFabric

↓

SQLite

↓

Patient
Observation
DocumentReference

↓

Health Record App
```

unter Verwendung ausschließlich synthetischer Testdaten.
