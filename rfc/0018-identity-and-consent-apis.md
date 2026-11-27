# RFC 0018: Identity & Consent APIs

- Status: Draft
- Owner: Platform Identity & Consent (Rolle, Person noch zu benennen)
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

## Identity Endpoints

Vorschlag für lokale HTTP-Operationen unter `/api/v1/`; alle außer Bootstrap
erfordern eine Sitzung und jeweils explizite Policy. Die genaue
Authentisierung und Request-/Response-Schemas sind vor Umsetzung in
RFC-0016/OpenAPI festzulegen.

| Operation | Vorgeschlagene Route | Einschränkung |
| --- | --- | --- |
| Bootstrap Owner und Gerät | `POST /bootstrap` | nur bei noch nicht initialisiertem Store, atomar |
| Sitzung öffnen / schließen | `POST /sessions`, `DELETE /sessions/current` | kein Credential in URL oder Log |
| Benutzer lesen / ändern / deaktivieren | `GET`, `PATCH`, `POST /users/{id}/disable` | nur nach passender Capability und Policy |

## Consent Endpoints

| Operation | Vorgeschlagene Route | Einschränkung |
| --- | --- | --- |
| Entwurf erstellen / listen | `POST`, `GET /consents` | Owner bzw. zulässiger Vertreter, profilgebunden |
| Freigeben / ändern | `POST /consents/{id}/activate`, `PATCH /consents/{id}` | ausdrückliche Zustimmung; Version prüfen |
| Widerrufen / erneuern | `POST /consents/{id}/revoke`, `POST /consents/{id}/renew` | Widerruf unmittelbar am Datenzugriff; Erneuerung als neuer Consent |

`checkConsent` ist eine interne Policy-Schnittstelle, kein allgemein
zugänglicher Endpoint; ihr Ergebnis ist keine übertragbare dauerhafte
Zugriffsgarantie. Zustandswechsel folgen RFC-0003, Änderungen sind
versionskontrolliert, wiederholte Requests benötigen definierte
Idempotenzsemantik. Audit gilt auch bei Verweigerung; Audit-Ausfall blockiert
den geschützten Zugriff.

## Household und Emergency Endpoints

Die genannten Household- und Emergency-Operationen sind Funktionswünsche,
keine freigegebenen öffentlichen Endpoints. Vor ihrer Implementierung
benötigen sie das Guardian-/Jurisdiktionsmodell aus RFC-0008, konkrete
Zustandsautomaten, Identitäts- und Policy-Prüfung, Offline-Verhalten,
Zustimmung, Ablauf, Missbrauchsschutz, Audit und verifizierte Schemas.
Ein `approveEmergencyAccess` ist ohne diese Regeln nicht implementierungsreif.

## Negative Akzeptanzfälle

Unauthentisierter Zugriff → 401; fehlender Scope → 403, bei Gefahr einer
Existenzoffenlegung stattdessen 404; abgelaufener bzw. widerrufener Consent → deny;
gleichzeitiger Widerruf und Schreibzugriff wird am Zugriffspunkt
serialisiert; fehlgeschlagene Auditpersistenz → kein geschützter Erfolg.
Konkrete Fehlercodes und Payloads sind noch zu veröffentlichen.

