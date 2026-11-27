# LifeLedger RFC Backlog
# Konkrete Änderungsaufträge zur Schließung offener Entscheidungen
# Übergabedokument für GitHub Copilot

Status: Vor erstem implementierten Offline Vertical Slice

Ziel:
Nach Umsetzung aller P0- und P1-Arbeitsaufträge sollen die RFCs
ausreichend konkret sein, um mit der technischen Implementierung
des ersten Windows-Offline-Durchstichs zu beginnen.

Referenzen:

- RFC-0001 bis RFC-0019
- Gesamt-Roadmap
- Repository Review
- Implementierungsreife Review

---

# P0
# Blocker für den ersten Vertical Slice

Diese Punkte müssen vor Beginn der eigentlichen Implementierung
abgeschlossen werden.

---

# RFC-0001 Platform Direction

## Änderungsauftrag RFC1-01

Abschnitt ergänzen:

```md
## Approved First Vertical Slice
```

Festlegung:

```text
Zielgruppe:
Health Power User

Client:
Windows Desktop

Technologie:
Tauri + FastAPI

Speicher:
SQLite

FHIR Ressourcen:
Patient
MedicationStatement
DocumentReference

Daten:
nur synthetisch
```

---

## Änderungsauftrag RFC1-02

Abschnitt ergänzen:

```md
## Platform Ownership
```

Festlegen:

```text
Platform Core
→ Core Maintainer Team

VitaFabric
→ Data Team

LifeWeaver
→ AI Team

Marketplace
→ Governance Team
```

---

# RFC-0002 Platform Core Architecture

## Änderungsauftrag RFC2-01

Neuen Abschnitt hinzufügen:

```md
## Runtime Topology
```

Verbindliche Architektur:

```text
Tauri
↓
Local IPC
↓
FastAPI
↓
Platform Core
↓
VitaFabric
↓
SQLite
```

---

## Änderungsauftrag RFC2-02

Neuen Abschnitt hinzufügen:

```md
## Process Trust Boundaries
```

Definieren:

```text
UI Process

Backend Process

Plugin Runtime

Storage Layer
```

inkl.

```text
Trust Level
Authentication
Communication Path
```

---

## Änderungsauftrag RFC2-03

Folge-RFC Referenzen korrigieren.

Aktuell:

```text
RFC-0005 Marketplace Governance
RFC-0006 Deployment Modes
```

stimmen nicht mit RFC Nummern überein.

---

# RFC-0003 Identity & Consent

## Änderungsauftrag RFC3-01

Neuen Abschnitt erstellen:

```md
## Consent State Machine
```

Status:

```text
DRAFT
ACTIVE
SUSPENDED
EXPIRED
REVOKED
```

inkl.

```text
Zustandsübergänge
```

---

## Änderungsauftrag RFC3-02

Neuen Abschnitt:

```md
## Bootstrap Ownership
```

Festlegen:

```text
First Start

↓

Owner Creation

↓

Recovery Key

↓

Initial Device

↓

Initial Consent Context
```

---

## Änderungsauftrag RFC3-03

Consent Objekt erweitern.

Zusätzliche Felder:

```json
{
  "purpose": "",
  "operation": "",
  "resource": "",
  "version": "",
  "status": ""
}
```

---

## Änderungsauftrag RFC3-04

Neuer Abschnitt:

```md
## Session Revocation Behaviour
```

Verhalten bei:

```text
Consent Revoked

Active Session

Running Export

Running AI Request
```

---

# RFC-0004 Capability Model

## Änderungsauftrag RFC4-01

Neuer Abschnitt:

```md
## Capability Evaluation Algorithm
```

Workflow:

```text
Identity
↓
Consent
↓
Capability
↓
Policy
↓
Resource
```

---

## Änderungsauftrag RFC4-02

Neuer Abschnitt:

```md
## Capability Lifecycle
```

```text
Requested
Approved
Active
Revoked
Expired
```

---

## Änderungsauftrag RFC4-03

Neue Spezifikation:

```md
## Owner Access Rules
```

Owner darf nicht automatisch
Capabilities umgehen.

Festlegen:

```text
Owner
+
Capability
+
Consent
```

---

# RFC-0005 Event Bus

## Änderungsauftrag RFC5-01

Neuen Abschnitt:

```md
## Delivery Guarantees
```

Festlegung:

```text
At Least Once
```

---

## Änderungsauftrag RFC5-02

Neuen Abschnitt:

```md
## Event Retention
```

Definieren:

```text
Normal Events
Audit Events
Sync Events
Security Events
```

inkl.

```text
Retention
Archive
Delete
```

---

## Änderungsauftrag RFC5-03

Neuen Abschnitt:

```md
## Slice Event Set
```

Erster Durchstich:

```text
FHIR_CREATED
FHIR_UPDATED

CONSENT_GRANTED
CONSENT_REVOKED

USER_CREATED

BACKUP_CREATED
```

---

# P1
# Implementierungsblocker

---

# RFC-0006 Plugin Runtime

## Änderungsauftrag RFC6-01

Neuer Abschnitt:

```md
## WIT Interface Catalog
```

Definieren:

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

## Änderungsauftrag RFC6-02

Neue Spezifikation:

```md
## Resource Budget Policy
```

Festlegen:

```text
RAM

CPU

Disk

Network

Execution Time
```

---

## Änderungsauftrag RFC6-03

Neuer Abschnitt:

```md
## Host Compatibility Matrix
```

Für:

```text
Windows

Linux

macOS

Android

iOS
```

---

# RFC-0007 Application Framework

## Änderungsauftrag RFC7-01

Explizite Entscheidung ergänzen:

```md
## Health Record Execution Model
```

Festlegung MVP:

```text
Health Record

läuft im Kern

nicht als externes Plugin
```

---

## Änderungsauftrag RFC7-02

Neuer Abschnitt:

```md
## First User Journey
```

Ablauf:

```text
Import Document

↓

Create Patient

↓

Create Medication

↓

Timeline View

↓

Backup
```

---

## Änderungsauftrag RFC7-03

Backup fest definieren:

```md
## Backup Scope
```

---

# RFC-0008 Family Model

## Änderungsauftrag RFC8-01

Neuer Abschnitt:

```md
## Guardian Verification
```

---

## Änderungsauftrag RFC8-02

Neuer Abschnitt:

```md
## Age Transition Workflow
```

---

## Änderungsauftrag RFC8-03

Emergency Profile harmonisieren.

RFC-0003 und RFC-0008
müssen identische Felder definieren.

---

# RFC-0009 Marketplace

## Änderungsauftrag RFC9-01

Neuer Abschnitt:

```md
## Key Rotation
```

---

## Änderungsauftrag RFC9-02

Neuer Abschnitt:

```md
## Offline Trust Behaviour
```

---

## Änderungsauftrag RFC9-03

Patch Release Regel korrigieren.

Der derzeitige Digest-Text
ist technisch widersprüchlich.

Neue Regel:

```text
Jede Paketänderung

→ neuer Digest

→ neue Signatur
```

---

# P2
# Vor Erweiterungen

---

# RFC-0010 Zero Knowledge Sync

Bearbeiten erst nach lokalem Kern.

Ergänzen:

```text
Pairing Protocol

Tombstone Retention

Device Revocation

Key Rotation
```

---

# RFC-0011 LifeWeaver

Bearbeiten erst nach lokalem Kern.

Ergänzen:

```text
Prompt Retention

Embedding Retention

Provider Timeout Rules

Prompt Injection Mitigation
```

---

# RFC-0012 Governance

Ergänzen:

```text
Maintainer Succession

Security Escalation Matrix

Audit Retention
```

---

# Definition of Ready für Implementierung

Die eigentliche Entwicklung darf starten wenn:

✅ RFC-0001 aktualisiert

✅ RFC-0002 aktualisiert

✅ RFC-0003 aktualisiert

✅ RFC-0004 aktualisiert

✅ RFC-0005 aktualisiert

✅ RFC-0006 erweitert

✅ RFC-0007 konkretisiert

✅ RFC-0008 harmonisiert

✅ RFC-0009 korrigiert

✅ RFC-0015 existiert

✅ RFC-0016 existiert

✅ RFC-0017 existiert

✅ RFC-0018 existiert

✅ RFC-0019 existiert

---

# Ergebnis

Nach Abschluss dieser Änderungen kann der erste technische Vertical Slice begonnen werden:

```text
Windows Desktop

↓

Tauri

↓

FastAPI

↓

SQLite

↓

VitaFabric

↓

Patient

↓

DocumentReference

↓

MedicationStatement

↓

Health Record

↓

Backup
```

Nur synthetische Daten.

Keine Integrationen.

Keine Plugins.

Keine AI.

Keine Synchronisierung.