# RFC 0019: Plugin APIs & SDK Contracts

- Status: Draft
- Depends On: [RFC-0006 Plugin Runtime & Isolation](0006-plugin-runtime-and-isolation.md), [RFC-0007 Application Framework](0007-application-framework.md), [RFC-0009 Marketplace Governance](0009-marketplace-governance-and-trust-framework.md)

## Ziel

Normierung aller Plugin APIs.

---

## APIs

```text
Filesystem API

Event API

VitaFabric API

Identity API

Consent API

Secret API
```

---

## Plugin Manifest

Verbindliches Schema.

---

## SDK

Pflicht:

```text
Test Fixtures

Capability Tests

Compliance Suite
```

---

## Kompatibilität

Plugin muss angeben:

```text
min_version
max_version
```

---

## Marketplace-Listingstufe

Für die Listingstufen Community, Verified und Official gelten die Prüf- und
Signaturregeln aus RFC-0009. Die Stufen sind keine Zertifizierung und keine
Sicherheitsgarantie; sie ersetzen weder Isolation noch Consent- und
Capability-Enforcement.
