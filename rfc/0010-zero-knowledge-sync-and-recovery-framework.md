# RFC 0010: Zero-Knowledge Sync & Recovery Framework

- Status: Draft
- Type: Security RFC
- Owner: Platform Security
Depends On: RFC-0002 Platform Core Architecture  
Depends On: RFC-0003 Identity & Consent Framework  
Depends On: RFC-0005 Event Bus Architecture  
Depends On: RFC-0008 Family & Delegation Model

Blocks:
- Local + Zero Knowledge Sync
- Multi Device Support
- Encrypted Backup
- Cross Device Synchronization
- Relay Infrastructure

---

## 1. Zusammenfassung

Dieses RFC definiert die optionale Zero-Knowledge-Synchronisierung der LifeLedger Plattform.

Der Synchronisationsdienst darf Daten speichern.

Der Synchronisationsdienst darf Daten übertragen.

Der Synchronisationsdienst darf Daten sichern.

Der Synchronisationsdienst darf jedoch niemals:

```text
Passwörter kennen

Entschlüsselungsschlüssel kennen

Gesundheitsdaten lesen

Health Profile entschlüsseln
```

können.

Zero-Knowledge-Sync ist eine optionale Erweiterung.

Der lokale Betrieb bleibt vollständig funktionsfähig und benötigt keinen Cloud-Dienst. Dies folgt den Plattformprinzipien der Roadmaps und Deployment-Szenarien.

---

## 2. Ziele

### Ziele

```text
Ende-zu-Ende Verschlüsselung

Mehrere Geräte

Recovery

Offline First

Zero Knowledge

Cloud Optional
```

---

### Nichtziele

```text
Cloud Pflicht

Serverseitige Entschlüsselung

Passwort Recovery durch Betreiber

Zentraler Schlüsseldienst
```

---

## 3. Grundprinzipien

### Local First

Alle Kernfunktionen funktionieren lokal.

---

### User Owns The Keys

Schlüssel gehören ausschließlich dem Nutzer.

---

### Zero Knowledge

Server besitzen keine Lesemöglichkeit.

---

### Verifizierbare Kryptographie

Keine proprietären Verfahren.

---

## 4. Architektur

```text
Device

↓

Encrypt

↓

Ciphertext

↓

Sync Service

↓

Ciphertext

↓

Authorized Device

↓

Decrypt
```

---

## 5. Datenklassen

### Synchronisierbar

```text
FHIR Daten

Dokumente

Timeline

Settings

Application Daten
```

---

### Nicht synchronisierbar

```text
Lokale Secrets

Recovery Seeds

Betriebssystemschlüssel
```

---

## 6. Schlüsselhierarchie

### Root Key

Höchste Vertrauensebene.

---

Abgeleitet aus:

```text
User Password

+

Recovery Secret
```

---

### Data Encryption Key

```text
DEK
```

verschlüsselt Daten.

---

### Device Key

```text
DK
```

identifiziert Geräte.

---

## 7. Kryptographische Anforderungen

Passwortableitung:

```text
Argon2id
```

---

Datenverschlüsselung:

```text
AES-256-GCM
```

oder

```text
XChaCha20-Poly1305
```

---

Hashing:

```text
SHA-256
```

---

## 8. Benutzerkonto Modell

Ein Benutzer kann besitzen:

```text
Mehrere Geräte
```

---

Beispiel:

```text
Desktop

Laptop

Smartphone

Tablet
```

---

## 9. Device Enrollment

Neue Geräte werden aktiv freigegeben.

---

### Standardverfahren

```text
QR Code Pairing
```

---

Ablauf:

```text
Bestehendes Gerät

↓

Pairing Token

↓

QR Code

↓

Neues Gerät

↓

Vertrauen hergestellt
```

---

## 10. Trusted Device Modell

Nur autorisierte Geräte dürfen:

```text
Synchronisieren

Entschlüsseln

Recovery durchführen
```

---

## 11. Synchronisationsobjekte

Jedes Objekt besitzt:

```text
Object ID

Version

Timestamp

Ciphertext

Hash
```

---

## 12. Konfliktbehandlung

Konflikte sind erwartbar.

---

### Beispiele

```text
Zwei Geräte

ändern denselben Datensatz
```

---

## 13. Konfliktstrategie

Last Writer Wins (LWW) ist ausschließlich zulässig für:

```text
Settings

UI-Daten

Preferences
```

Für andere Datenklassen ist Last Writer Wins damit nicht freigegeben.

---

### FHIR Conflict Resolution Workflow

Jede Änderung trägt eine Objekt-ID, Elternversion bzw. kausale
Versionsreferenz, Geräte-ID, monotone lokale Sequenz und Provenienz.
Zeitstempel dienen der Anzeige, niemals als alleinige Konfliktpriorität.
Wiederholte Übertragung derselben Operation ist idempotent.

1. **Kein Konflikt:** Eine Änderung, die auf der aktuellen Version basiert,
   wird übernommen.
2. **Unabhängige Änderungen:** Nur Felder/Elemente, die durch ein
   versioniertes Ressourcenschema als unabhängig und mergebar definiert sind,
   dürfen automatisch zusammengeführt werden. Provenienz beider Änderungen
   bleibt erhalten. FHIR-Arrays, klinische Werte und unbekannte Extensions
   werden nicht pauschal feldweise gemergt.
3. **Nicht mergebare Änderungen:** Beide Versionen bleiben als verschlüsselte
   Konfliktvarianten erhalten; keine Seite überschreibt die andere.
4. **Löschung gegen Änderung:** Ein bestätigter Lösch-Tombstone gewinnt
   standardmäßig gegen eine nebenläufige Änderung. Die Ressource wird auf
   allen Geräten verborgen und nicht weiter verarbeitet. Eine Wiederherstellung
   ist nur als explizite, auditierte Nutzeraktion mit neuer Ressourcenversion
   möglich; Synchronisation allein darf keine gelöschten Daten wiederbeleben.
   Der Tombstone wird bis zur Bestätigung aller autorisierten Geräte und danach
   entsprechend der festgelegten Tombstone-Retention weitergeführt.
5. **Konkurrierende Löschungen:** Werden idempotent zu einem Tombstone
   zusammengefasst. Ein späterer Restore ist eine neue, separat autorisierte
   Operation.

**Konfliktpriorität:** Consent- oder Gerätewiderruf sperrt Verarbeitung zuerst;
danach gilt Lösch-Tombstone vor Update; danach kausale Nachfolge; danach
deterministischer Merge nur für ausdrücklich freigegebene Felder. Es gibt
keinen Zeitstempel- oder Geräteprioritäts-Sieg für konkurrierende klinische
Änderungen.

**Manueller Review und UI:** Der Nutzer sieht Ressourcentyp, betroffene
Felder, Quelle/Gerät, Zeit und beide Werte sowie die Optionen „Version A
behalten“, „Version B behalten“ oder „sicher zusammenführen“, sofern ein
validierter Merge verfügbar ist. Bei Löschung gegen Änderung ist standardmäßig
„gelöscht lassen“ ausgewählt. Bis zur Entscheidung bleiben konkurrierende
Versionen lokal verschlüsselt, als Konflikt markiert und für Export, RAG,
Embedding-Erzeugung und nachgelagerte Workflows gesperrt. Eine Auflösung
erzeugt eine neue Version mit Provenienz und Audit-Eintrag; ohne verfügbaren
Owner wird der Konflikt nicht automatisch aufgelöst.

---

## 14. Synchronisationsmodell

### Push

```text
Client → Sync Service
```

---

### Pull

```text
Client ← Sync Service
```

---

### Hybrid

Festgelegt als Sync-Architektur.

```text
Push + Pull
```

---

## 15. Offline Support

Pflicht:

```text
Arbeiten ohne Verbindung
```

---

Synchronisation erfolgt später.

---

## 16. Backup Modell

### Lokales Backup

Pflicht.

---

### Verschlüsseltes Backup

Optional.

---

Backup enthält:

```text
Ciphertext

Metadaten

Versionen
```

---

## 17. Recovery Modell

Kritischer Bestandteil.

---

## 18. Recovery Key

Bei Einrichtung erzeugt:

```text
Recovery Key
```

---

Beispiel:

```text
24 Wörter
```

ähnlich:

```text
Signal

1Password

Bitwarden
```

---

## 19. Trusted Recovery Contact

Optional.

---

Beispiel:

```text
Partner

Familienmitglied

Guardian
```

---

Kann Recovery unterstützen.

---

Hat keinen Zugriff auf Daten.

---

## 20. Schlüsselverlust

### Ohne Recovery Key

und

### Ohne autorisiertes Gerät

---

Ergebnis:

```text
Daten gelten als verloren
```

---

Dies ist bewusstes Zero-Knowledge Verhalten.

---

## 21. Metadatenmodell

Zero Knowledge bedeutet nicht:

```text
Keine Metadaten
```

---

Mögliche Metadaten:

```text
Objektgröße

Versionsnummer

Zeitpunkt

Geräte-ID
```

---

## 22. Metadatenminimierung

Pflicht:

```text
Keine FHIR Inhalte

Keine Dokumententitel

Keine Medikationsnamen
```

---

## 23. Consent Integration

Synchronisation erzeugt keine Sonderrechte.

---

Pflichtpfad:

```text
Identity

↓

Consent

↓

Capability

↓

Data Access
```

---

## 24. Family Modell Integration

Gemäß RFC-0008.

---

Freigaben werden synchronisiert.

---

Besitzrechte werden nicht verändert.

---

## 25. Event Bus Integration

Gemäß RFC-0005.

Events:

```text
SYNC_STARTED

SYNC_COMPLETED

SYNC_FAILED

SYNC_CONFLICT

DEVICE_ADDED

DEVICE_REMOVED
```

---

## 26. Relay Service

Optional.

---

Darf verwalten:

```text
Routing

Push Events

Notifications
```

---

Darf niemals besitzen:

```text
Plaintext

Keys

Passwords
```

---

## 27. Managed Cloud

Separates Deployment-Modell.

Nicht Bestandteil dieses RFC.

Für Managed Cloud ist ein zusätzliches Review erforderlich.

---

## 28. Audit Anforderungen

Protokollieren:

```text
Device Enrollment

Recovery

Sync

Revocation

Conflict Resolution
```

---

## 29. Sicherheitsanforderungen

Pflicht:

```text
Ende zu Ende Verschlüsselung

Device Trust

Recovery Verfahren

Metadatenminimierung

Offline Betrieb

Key Rotation
```

---

## 30. Nicht zulässig

```text
Master Keys beim Betreiber

Passwort Recovery durch Cloud

Unverschlüsselte Backups

Cloud Pflicht
```

---

## 31. Zukünftige Erweiterungen

### Phase 1

```text
Single User Sync
```

---

### Phase 2

```text
Family Sync
```

---

### Phase 3

```text
Cross Household Sharing
```

---

### Phase 4

```text
Federated Sync Nodes
```

---

## 32. Architekturentscheidung

Dieses RFC legt fest:

✅ Zero Knowledge Architektur

✅ User Owns The Keys

✅ Ende-zu-Ende Verschlüsselung

✅ QR Device Pairing

✅ Recovery Key

✅ Trusted Recovery Contacts

✅ Lokaler Betrieb bleibt möglich

✅ Metadatenminimierung

✅ Offline First

✅ Konfliktlösung

✅ Device Trust Modell

✅ Kein Betreiberzugriff auf Inhalte
