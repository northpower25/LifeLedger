# RFC Konsistenzreview (RFC-0003 bis RFC-0013)

Die folgenden Konsolidierungsentscheidungen wurden in den RFC-Drafts
berücksichtigt. Sie nehmen die RFCs nicht an und belegen keine Implementierung.

## Priorität P1

### RFC-0003 ↔ RFC-0008

Problem:

Rollen werden doppelt definiert.

Festlegung:

RFC-0003 ist normative Quelle.

RFC-0008 referenziert diese Rollen nur.

Aktion:

Rollenbeschreibungen aus RFC-0008 entfernen.

---

### RFC-0006 ↔ RFC-0007

Problem:

Application wird gleichzeitig als Plugin-Typ
und als eigenständiges Modell beschrieben.

Festlegung:

Application = spezialisierter Plugin-Typ.

Aktion:

In beiden RFCs identisch formulieren.

---

### RFC-0010 ↔ RFC-0013

Problem:

Last Writer Wins kollidiert mit FHIR Governance.

Festlegung:

LWW nur für:

- Settings
- UI Daten
- Preferences

FHIR:

```text
Conflict Resolution Workflow
```

---

### RFC-0011 ↔ RFC-0013

Problem:

Embeddings liegen außerhalb des VitaFabric Modells.

Festlegung:

Neue VitaFabric Datenklasse:

```text
Derived Data
```

umfasst:

```text
Embeddings
Knowledge Graph
AI Summaries
Derived Metadata
```

---

## Priorität P2

### RFC-0005

Neue Events ergänzen:

```text
ROLE_GRANTED
ROLE_REVOKED
PROVIDER_CONSENT_GRANTED
PROVIDER_CONSENT_REVOKED
EMBEDDING_PURGED
```

---

### RFC-0004

Neue Capabilities ergänzen:

```text
READ_PROVENANCE
READ_EMBEDDINGS
MANAGE_CONSENT
MANAGE_HOUSEHOLD
```

---

### RFC-0012

Governance um ergänzen:

```text
Maintainer Succession Process
```

---

## Priorität P3

### RFC-0009

Trust Levels präzisieren:

Community ≠ Unsicher

Official ≠ Sicher

---

### RFC-0011

Regulatorischen Abschnitt ergänzen:

```text
EU AI Act
MDR
Clinical Decision Support
```
