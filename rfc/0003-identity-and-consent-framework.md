# RFC 0003: Identity & Consent Framework

- Status: Draft
- Type: Architecture RFC
- Owner: Platform Core
Depends On: RFC-0002 Platform Core Architecture  
Blocks: RFC-0004, RFC-0006, RFC-0008, RFC-0010

---

## 1. Zusammenfassung

Dieses RFC definiert das zentrale Identity- und Consent-Modell der LifeLedger-Plattform.

Es legt fest:

- Benutzeridentitäten
- Familienbeziehungen
- Vertretungsmodelle
- Einwilligungen
- Berechtigungsdelegation
- Widerruf
- Notfallzugriffe
- Auditierbarkeit

Alle Datenzugriffe innerhalb von LifeLedger, VitaFabric, LifeWeaver und Plugins müssen dieses Modell verwenden. Gesundheitsdaten dürfen niemals außerhalb dieses Modells freigegeben werden. Die Notwendigkeit eines gemeinsamen Identity-&-Consent-Layers ergibt sich direkt aus der Plattformvision, den Roadmaps und den gemeinsamen Plattformfähigkeiten.

---

## 2. Ziele

### Ziele

```text
Nachvollziehbare Datenfreigaben

Familienmodelle

Notfallzugriffe

Delegationsmodelle

Widerrufbarkeit

Auditierbarkeit

Plugin-Integrierbarkeit
```

### Nichtziele

```text
Externe Identitätsprovider im MVP

Single Sign-On Systeme

Klinische Rollenmodelle

Krankenhaus-Berechtigungssysteme
```

---

## 3. Grundprinzipien

### Ownership First

Jeder Gesundheitsdatensatz besitzt genau einen Owner.

---

### Consent First

Kein Zugriff ohne gültige Einwilligung.

---

### Least Privilege

Freigaben müssen minimal sein.

---

### Revocable Access

Jede Freigabe muss widerrufbar sein.

---

### Audit Required

Jede Freigabe wird protokolliert.

---

## 4. Identitätsmodell

### User

Basisobjekt.

```text
User
├── UserID
├── Profile
├── Devices
├── Credentials
└── Settings
```

---

### Health Profile

Gesundheitsdaten gehören einem Profil.

```text
HealthProfile
├── ProfileID
├── Owner
├── Household
└── Resources
```

---

## 5. Household Modell

### Household

Verwaltet Familienbeziehungen.

```text
Household
├── Members
├── Guardians
├── Caregivers
├── Proxies
└── EmergencyContacts
```

---

## 6. Rollenmodell

Dieses RFC ist die maßgebliche Quelle für die Definitionen der folgenden
Rollen. RFC-0008 beschreibt deren Anwendung im Familien- und
Delegationsmodell und definiert die Rollen nicht erneut.

### Primary Owner

Besitzer eines Gesundheitsprofils.

Darf:

```text
lesen
schreiben
löschen
delegieren
freigeben
widerrufen
exportieren
```

---

### Guardian

Gesetzlicher Vertreter.

Beispiele:

```text
Eltern
Vormund
```

Darf:

```text
lesen
schreiben
freigeben
widerrufen
```

Die Guardian-Befugnisse enden bei Entzug, Volljährigkeit oder Widerruf,
soweit rechtlich zulässig.

---

### Caregiver

Pflegeperson.

Beispiele:

```text
Pflegedienst
Angehörige
```

Darf:

```text
lesen
teilweise schreiben
```

Nicht erlaubt:

```text
Besitz übertragen
Freigaben vergeben
Neue Vertreter ernennen
Notfalldefinition ändern
```

---

### Proxy

Bevollmächtigter Vertreter.

Beispiele:

```text
Vorsorgevollmacht
gesetzliche Vertretung
```

Die Rechte werden individuell vergeben und können dieselben Rechte wie beim
Owner umfassen.

---

### Emergency Contact

Darf ausschließlich Notfallinformationen im Emergency Profile einsehen.

Kein Zugriff auf das volle Gesundheitsprofil, Dokumentenarchiv oder die
Historie.

---

## 7. Consent Modell

### Consent Object

Jede Freigabe wird als Consent gespeichert.

```json
{
  "id": "consent_001",
  "owner": "user_123",
  "grantee": "user_456",
  "scope": [
    "Medication",
    "Allergies"
  ],
  "expires": null
}
```

---

## 8. Scope-Modell

Nicht:

```text
Vollzugriff
```

sondern:

```text
Dokumente
Medikationen
Allergien
Timeline
Observations
Notfallprofil
```

einzeln.

---

## 9. Delegation

Delegationsfähig:

```text
Owner
Guardian
Proxy
```

Nicht delegationsfähig:

```text
Caregiver
Emergency Contact
```

---

## 10. Notfallzugriff

### Emergency Bundle

Separater Datensatz.

Enthält:

```text
Name
Allergien
Medikationen
Blutgruppe
Notfallkontakte
```

---

### Emergency Access Workflow

```text
Anfrage

↓

Protokollierung

↓

Zugriff auf Emergency Bundle

↓

Audit Event
```

---

## 11. Widerrufsmodell

Widerruf muss sofort wirken.

---

### Widerruf betrifft

```text
aktive Sessions

Plugin Berechtigungen

API Tokens

Provider Freigaben
```

---

## 12. Audit Anforderungen

Jeder Zugriff erzeugt:

```text
Zeitpunkt
Akteur
Aktion
Ressource
Ergebnis
```

---

## 13. Plugin Integration

Plugins sehen niemals Rollen.

Plugins erhalten ausschließlich:

```text
Capabilities
Consent Result
```

---

## 14. API Anforderungen

Identity API

```text
createUser
updateUser
disableUser
```

Consent API

```text
grantConsent
revokeConsent
checkConsent
```

Emergency API

```text
requestEmergencyAccess
```

---

## 15. Sicherheitsanforderungen

Pflicht:

```text
MFA Unterstützung

Audit Logging

Session Management

Recovery Verfahren
```

---

## 16. Architekturentscheidung

Dieses RFC legt fest:

✅ Consent First

✅ Household Modell

✅ Guardian/Caregiver/Proxy Rollen

✅ Widerrufbarkeit

✅ Audit Pflicht

✅ Emergency Bundle

✅ Ressourcenbasierte Freigaben

✅ Plattformweites Modell
