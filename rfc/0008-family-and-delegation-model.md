# RFC 0008: Family & Delegation Model

- Status: Draft
- Type: Architecture RFC
- Owner: Identity & Consent Domain
Depends On: RFC-0002 Platform Core Architecture  
Depends On: RFC-0003 Identity & Consent Framework  
Depends On: RFC-0004 Capability & Permission Model  
Depends On: RFC-0007 Application Framework

Blocks:
- Emergency Access
- Family Health Application
- Pediatric Records
- Caregiver Workflows
- Shared Household Features

---

## 1. Zusammenfassung

Dieses RFC definiert das Familien-, Vertretungs- und Delegationsmodell der LifeLedger Plattform.

Ziel ist die sichere Verwaltung von:

```text
Kindern

Partnern

Angehörigen

Pflegebedürftigen Personen

Vertretungen

Notfallkontakten
```

ohne die Eigentumsrechte an Gesundheitsdaten aufzuweichen.

Das Modell muss sowohl lokale Einzelnutzer-Szenarien als auch Haushalte mit mehreren Personen unterstützen.

---

## 2. Ziele

### Ziele

```text
Familienunterstützung

Minderjährige

Pflegebedürftige Personen

Vertretungen

Notfallzugriffe

Widerrufbare Freigaben

Auditierbarkeit
```

---

### Nichtziele

```text
Klinisches Rollenmodell

Krankenhaus-Workflows

Versicherungsrollen

Organisationshierarchien
```

---

## 3. Architekturprinzipien

### Ownership First

Jedes Gesundheitsprofil besitzt genau einen Owner.

---

### Delegation statt Besitzübertragung

Freigaben übertragen niemals Besitz.

---

### Minimale Berechtigungen

Jeder Zugriff erfolgt:

```text
so wenig wie möglich
so viel wie nötig
```

---

### Widerrufbarkeit

Jede Delegation muss widerrufbar sein.

---

### Auditpflicht

Jeder Zugriff wird protokolliert.

---

## 4. Grundlegende Begriffe

### User

Technische Identität.

---

### Health Profile

Gesundheitsprofil.

Beinhaltet:

```text
FHIR Ressourcen

Dokumente

Historie

Freigaben
```

---

### Household

Logische Gruppe.

Beispiel:

```text
Eltern

Kinder

Pflegebedürftige Angehörige
```

---

## 5. Rollen und Zuständigkeit

RFC-0003 §6 ist die normative und alleinige Quelle für Definition, Rechte
und Grenzen von Primary Owner, Guardian, Caregiver, Proxy und Emergency
Contact. Dieses RFC wendet diese Rollen auf Haushalte und Delegationen an,
ändert oder wiederholt ihre Rechte aber nicht. Ein Household oder eine
Beziehung allein erteilt keine Capability und keine Einwilligung.

---

## 6. Dependent

Abhängige Person.

Typische Beispiele:

```text
Kinder

Betreute Personen

Pflegebedürftige Personen
```

---

Dependent ist keine Berechtigung.

Dependent beschreibt nur die Beziehung.

---

## 7. Household Modell

```text
Household

├── Owner
├── Guardian
├── Caregiver
├── Proxy
├── Emergency Contact
└── Dependents
```

---

## 8. Delegationsmodell

### Direkte Delegation

```text
Owner

↓

Caregiver
```

---

### Guardian Delegation

```text
Guardian

↓

Caregiver
```

---

### Proxy Delegation

Standardmäßig verboten.

Kann optional erlaubt werden.

---

## 9. Freigabebereiche

Freigaben erfolgen nicht global.

---

### Dokumente

```text
DOCUMENT_ACCESS
```

---

### Medikamente

```text
MEDICATION_ACCESS
```

---

### Allergien

```text
ALLERGY_ACCESS
```

---

### Beobachtungen

```text
OBSERVATION_ACCESS
```

---

### Notfallprofil

```text
EMERGENCY_ACCESS
```

---

## 10. Zeitbasierte Freigaben

Unterstützt:

```text
Ablaufdatum

Zeitfenster

Temporäre Berechtigung
```

---

Beispiel:

```text
Caregiver

gültig für

30 Tage
```

---

## 11. Notfallmodell

### Emergency Profile

Separater minimaler Datensatz.

Enthält:

```text
Name

Geburtsdatum

Blutgruppe

Allergien

Medikationen

Notfallkontakte
```

---

## 12. Emergency Access Workflow

```text
Notfallanfrage

↓

Protokollierung

↓

Emergency Access

↓

Audit Event
```

---

## 13. Minderjährige

### Standard

```text
Owner = Kind

Guardian = Eltern
```

---

### Zugriff

Die Anwendung der Guardian-Rolle richtet sich nach RFC-0003 und den
rechtlich zulässigen Vertretungsbefugnissen. Das Kind besitzt die
Profilidentität.

---

### Volljährigkeit

System muss unterstützen:

```text
Rollenübergang

Besitzübernahme
```

---

## Guardian Verification

Eine behauptete Guardian-Beziehung gewährt allein keinen Zugriff. Vor einer
Vertretungsfreigabe müssen Identität der handelnden Person, betroffenes
Profil, Art, Umfang und Gültigkeit der Vertretung anhand geeigneter Nachweise
und des anwendbaren Rechts geprüft werden. Der prüfende Prozess dokumentiert
Entscheidung, Zuständigkeit, Zeitpunkt, Gültigkeit und Nachweisreferenz;
Originalnachweise sind nur soweit erforderlich separat verschlüsselt
aufzubewahren. Entzug oder Ablauf sperrt abgeleitete Zugriffe. Ein lokal
eingegebenes Dokument ist kein automatischer Rechtsnachweis.

## Jurisdiction Model

Version 1 unterscheidet Deutschland, übrige EU und international als
Prüfbereiche, nicht als einheitliche Rechtsregeln. Land, relevante
Rechtsordnung, Regelversion, Prüfer und Zeitpunkt müssen explizit erfasst
werden; EU-Mitgliedschaft ersetzt keine Prüfung des nationalen Rechts.
Unbekannte oder konfligierende Zuständigkeit führt zu manueller Prüfung und
keiner automatischen Freigabe. Rechtsgrundlagen, Nachweise und Prüfinstanz
sind vor Familienfunktionen durch qualifizierte Stellen festzulegen.

## Age Transition Workflow

`Minor` → `Transition` → `Adult Owner`: Bei Erreichen der nach geprüfter
Rechtsordnung maßgeblichen Schwelle beginnt eine überprüfte Übergangsphase.
Das Profil bleibt beim Betroffenen; bestehende Guardian-Grants werden
gesperrt und nicht automatisch in Erwachsenenfreigaben umgewandelt. Nach
Identitätsprüfung und sicherem Bootstrap entscheidet der erwachsene Owner
über neue, begrenzte Grants. Ausnahmen durch fortbestehende gesetzliche
Vertretung benötigen unabhängige Prüfung. Benachrichtigung, gescheiterte
Identitätsprüfung und Offline-Geräte dürfen keine stillschweigende
Rechteausweitung auslösen.

## 14. Trennung von Daten

Jeder Nutzer besitzt:

```text
Eigenes Profil

Eigene Berechtigungen

Eigenes Audit
```

---

Nicht erlaubt:

```text
Gemeinsame Gesundheitsdatenbank
ohne Zuordnung
```

---

## 15. User Interface Anforderungen

Nutzer müssen erkennen:

```text
Wer Zugriff hat

Worauf Zugriff besteht

Warum Zugriff besteht

Wann Zugriff endet
```

---

## 16. Widerruf

Jeder Widerruf muss sofort wirken.

---

Betroffen:

```text
Sessions

API Tokens

Apps

Plugins
```

---

## 17. Audit Anforderungen

Jeder Zugriff speichert:

```text
Akteur

Zielprofil

Rolle

Zeitpunkt

Aktion

Ergebnis
```

---

## 18. Event Bus Integration

Events gemäß RFC-0005.

Beispiele:

```text
MEMBER_ADDED

ROLE_GRANTED

ROLE_REVOKED

EMERGENCY_ACCESS_GRANTED

EMERGENCY_ACCESS_USED
```

---

## 19. Application Integration

Alle Anwendungen müssen Family-Awareness unterstützen.

Beispiele:

```text
Health Record

Family Health

Medication Manager
```

---

## 20. VitaFabric Integration

Familienrollen umgehen niemals VitaFabric.

Pflichtpfad:

```text
Role

↓

Consent

↓

Capability

↓

VitaFabric

↓

FHIR Daten
```

---

## 21. Sicherheitsanforderungen

Pflicht:

```text
Explizite Delegation

Widerrufbarkeit

Audit Logging

Consent Enforcement

Least Privilege
```

---

Nicht zulässig:

```text
Implizite Familienrechte

Automatische Vollzugriffe

Unsichtbare Freigaben
```

---

## 22. Zukunftserweiterungen

Spätere Erweiterungen:

```text
Professionelle Pflege

Betreuungsorganisationen

Mehrgenerationenhaushalte

Juristische Vollmachten
```

---

## 23. Architekturentscheidung

Dieses RFC legt fest:

✅ Household Modell

✅ Rollen gemäß RFC-0003

✅ Ressourcenbasierte Freigaben

✅ Zeitbasierte Berechtigungen

✅ Minderjährigenmodell

✅ Volljährigkeitsübergang

✅ Auditpflicht

✅ Sofortiger Widerruf

✅ VitaFabric Enforcement
