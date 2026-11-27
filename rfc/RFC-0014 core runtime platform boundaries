# RFC-0014: Core Runtime & Platform Boundaries

Status: Draft
Type: Architecture RFC

## Ziel

Dieses RFC definiert die endgültige Grenze zwischen:

- Platform Core
- VitaFabric
- LifeWeaver
- Applications
- Plugins

und beantwortet:

> Was gehört zwingend zur Plattform?
>
> Was darf Plugin sein?
>
> Was darf niemals Plugin sein?

---

## Platform Core

Immer Bestandteil der Plattform:

```text
Identity Service
Consent Service
Audit Service
Event Bus
Plugin Host
Secret Store
Policy Engine
Settings Service
```

Diese Komponenten dürfen niemals ersetzt werden.

---

## VitaFabric

Immer Bestandteil der Plattform:

```text
FHIR Model
Validation
Provenance
Data Contracts
Storage Abstraction
Connector Contracts
```

---

## LifeWeaver

Immer Bestandteil der Plattform:

```text
Provider Framework
RAG APIs
Embedding Management
MCP Integration
Twin APIs
```

---

## Erweiterbar durch Plugins

```text
Connectors
Integrations
Providers
Storage Backends
Dashboards
Applications
```

---

## Verbotene Plugin-Kandidaten

```text
Consent Engine
Identity
Audit
Capability Enforcement
FHIR Validation
Policy Engine
```

---

## Application Definition

Eine Application ist:

```text
Ein spezialisierter Plugin-Typ
```

mit:

```text
UI
Navigation
Workflows
Settings
```

aber ohne:

```text
eigene Datenbank
eigene Identität
eigene Consent Engine
```

---

## Architekturentscheidung

✅ Platform Core ist nicht austauschbar

✅ VitaFabric bleibt Single Source of Truth

✅ LifeWeaver bleibt optionale Plattformfunktion

✅ Applications sind spezialisierte Plugins

✅ Sicherheits- und Identitätsdienste sind niemals Plugins
