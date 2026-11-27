# RFC 0018: Identity & Consent APIs

- Status: Draft
- Depends On: [RFC-0003 Identity & Consent Framework](0003-identity-and-consent-framework.md), [RFC-0004 Capability & Permission Model](0004-capability-and-permission-model.md)

## Ziel

Normierung der Identity APIs.

---

## Identity APIs

```text
createUser
updateUser
disableUser
getUser
```

---

## Consent APIs

```text
grantConsent
updateConsent
revokeConsent
listConsents
```

---

## Household APIs

```text
addMember
removeMember
assignRole
revokeRole
```

---

## Emergency APIs

```text
requestEmergencyAccess
approveEmergencyAccess
auditEmergencyAccess
```

---

## Audit Integration

Pflicht.

