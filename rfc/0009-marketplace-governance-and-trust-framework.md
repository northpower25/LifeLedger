# RFC 0009: Marketplace Governance & Trust Framework

- Status: Draft
- Type: Governance RFC
- Owner: Platform Governance
Depends On: RFC-0003 Identity & Consent Framework  
Depends On: RFC-0004 Capability & Permission Model  
Depends On: RFC-0006 Plugin Runtime & Isolation  
Depends On: RFC-0007 Application Framework

Blocks:
- Public Marketplace
- Verified Listings
- Official Listings
- Community Ecosystem

---

## 1. Zusammenfassung

Dieses RFC definiert Governance, Vertrauensmodell, Veröffentlichung, Review, Sperrung und Betrieb des LifeLedger Marketplace.

Der Marketplace dient der:

```text
Entdeckung

Verteilung

Dokumentation

Bewertung

Versionierung
```

von Erweiterungen.

Der Marketplace ist keine Sicherheitsgarantie.

Ein Marketplace-Eintrag ersetzt niemals:

```text
Capability Enforcement

Consent

Audit

Plugin Isolation
```

---

## 2. Ziele

### Ziele

```text
Offenes Ökosystem

Vertrauensmodell

Review-Prozesse

Missbrauchserkennung

Nachvollziehbarkeit

Betriebsfähigkeit
```

---

### Nichtziele

```text
App Store Monopol

Pflichtinstallation

Zwangssynchronisation

Cloudzwang

Sicherheitszertifizierung
```

---

## 3. Grundprinzipien

### Local First

Plugins müssen lokal installierbar bleiben.

Ein Marketplace darf niemals Voraussetzung sein.

---

### Security Through Architecture

Sicherheit entsteht durch:

```text
Runtime

Capabilities

Consent

Isolation
```

Nicht durch Marketplace-Badges.

---

### Transparenz

Alle Prüfungen müssen nachvollziehbar sein.

---

## 4. Marketplace Architektur

```text
Developer

↓

Package

↓

Marketplace

↓

Review

↓

Installation

↓

Local Runtime
```

---

## 5. Erweiterungstypen

Der Marketplace unterstützt alle Plattformtypen.

```text
Connector

Integration

Provider

Storage

UI

Application
```

---

## 6. Listing Kategorien

Es existieren drei Kategorien.

Die Stufen beschreiben Herkunft und Umfang der Prüfung, nicht die tatsächliche
Sicherheit: Community bedeutet nicht unsicher, Official nicht sicher.
Isolation und Capability- sowie Consent-Prüfungen gelten für alle Stufen.

---

## 7. Community

Niedrigste Vertrauensebene.

---

### Anforderungen

```text
Manifest

Signatur

Lizenz

Beschreibung
```

---

### Prüfung

Keine inhaltliche Prüfung.

---

### Vertrauensniveau

```text
Niedrig
```

---

## 8. Verified

Mittlere Vertrauensebene.

---

### Anforderungen

```text
Review

Build erfolgreich

Kompatibilität geprüft

Capabilities bewertet

Dokumentation vorhanden
```

---

### Prüfung und Sign-Off

Vor der Einstufung als Verified prüfen **mindestens zwei voneinander
unabhängige Reviewer** Manifest, Quell- und Build-Provenienz,
Capabilities/Datenflüsse, Dokumentation, Lizenz, Kompatibilität und die
veröffentlichten Tests. Mindestens ein Reviewer muss für Security oder
Plattform-Review zuständig sein. Autor, Paket-Publisher und direkte
Interessenkonflikte schließen eine Person als Reviewer für dieses Listing
aus.

Beide Reviewer geben ein dokumentiertes Sign-Off mit geprüfter Version,
Paket-Digest, Prüfumfang, offenen Einschränkungen und Datum. Eine Ablehnung
enthält konkrete Gründe und erforderliche Abhilfen; das Listing bleibt
Community oder wird nicht gelistet. Der Publisher kann Einspruch einlegen,
der von anderen Reviewern entschieden wird. Keine Antwort gilt nicht als
Freigabe.

Die Marketplace-Review verleiht keine Sicherheitszertifizierung und ersetzt
weder Capability-/Consent-Enforcement noch unabhängige Laufzeitisolation.

---

### Vertrauensniveau

```text
Mittel
```

---

## 9. Official

Höchste Vertrauensebene.

---

### Anforderungen

```text
Maintained by Project

Automatische Tests

Dokumentation

Security Review durch mindestens zwei unabhängige Reviewer

Review von Capabilities, Datenflüssen und Abhängigkeiten
```

Offizielle Erweiterungen müssen dieselben Signatur-, Digest- und
Schlüsselwiderrufsregeln wie Verified-Pakete erfüllen. Der Official-Status
beschreibt Projektverantwortung und Reviewumfang, keine Sicherheitsgarantie.

---

### Signatur

Projekt-Schlüssel.

---

### Vertrauensniveau

```text
Hoch
```

---

## 10. Kein Sicherheitszertifikat

Wichtige Regel:

```text
Official

≠

Sicher
```

---

```text
Verified

≠

Geprüft gegen alle Risiken
```

---

```text
Community

≠

Unsicher
```

---

## 11. Manifest Anforderungen

Pflichtfelder:

```text
Name

Version

Typ

Autor

Lizenz

Capabilities

Support URL
```

---

## 12. Provenienz

Jede Erweiterung besitzt:

```text
Publisher

Signatur

Build Hash

Release Historie
```

---

## 13. Paketverteilung

### Unterstützt

```text
Marketplace

Lokale Datei

Direktinstallation
```

---

### Nicht unterstützt

```text
Pflichtregistrierung

Cloud Konto Pflicht
```

---

## 14. Signaturmodell

### Community

```text
Self Signed
```

---

### Verified

```text
Zwei unabhängige Reviewer
```

Der Signaturworkflow ist: Paket bauen, Digest des finalen Artefakts
berechnen, Digest und Prüfergebnisse von zwei unabhängigen Reviewern
freigeben lassen und erst danach den Digest mit dem geschützten
Marketplace-Signaturschlüssel signieren. Signaturen binden exakt an Paket,
Version und Digest; Änderungen nach Freigabe erfordern eine neue Prüfung.
Private Signaturschlüssel sind zugriffsbeschränkt, offline oder in einem
Hardware-Sicherheitsmodul verwahrt und mit dokumentiertem Rotations- und
Widerrufsverfahren zu betreiben. Ein Signaturstatus beweist Herkunft und
Integrität, nicht Harmlosigkeit.

---

### Official

```text
Project Signed
```

---

## 15. Review Prozess

### Community

Automatische Prüfung.

---

### Verified

Manuelle Prüfung gemäß §8 mit zwei unabhängigen Reviewern.

---

Prüfung umfasst:

```text
Manifest

Capabilities

Dokumentation

Build
```

---

### Official

Zusätzliche Prüfungen:

```text
Code Review

Security Review

Regression Tests
```

---

## 16. Delisting

Marketplace Einträge können entfernt werden.

---

### Gründe

```text
Malware

Datendiebstahl

Identitätsmissbrauch

Lizenzverstöße

Schwere Sicherheitsmängel
```

---

## 17. Soft Delisting

Eintrag bleibt sichtbar.

---

Status:

```text
Deprecated
```

---

### Gründe

```text
Keine Wartung

Veraltete APIs

Inkompatibilität
```

---

## 18. Hard Delisting

Eintrag wird entfernt.

---

### Gründe

```text
Malware

Kompromittierung

Missbrauch
```

---

## 19. Appeals

Entwickler dürfen Einspruch einlegen.

---

Ablauf:

```text
Issue

↓

Review

↓

Maintainer Entscheidung
```

---

## 20. Incident Management

Marketplace benötigt Security Workflow.

---

### Meldung

```text
Security Report
```

---

### Bewertung

```text
Triaging
```

---

### Maßnahmen

```text
Warnung

Delisting

Signaturwiderruf
```

---

## 21. Signaturwiderruf

Projekt muss kompromittierte Pakete sperren können.

---

Beispiel:

```text
Revoked Signature List
```

---

## 22. Kompatibilität

Jedes Listing enthält:

```text
Min Version

Max Version

Kompatibilitätsstatus
```

---

## 23. Updates

Pflicht:

```text
Versionshistorie

Changelog

Kompatibilitätsprüfung
```

Verified-Listings werden mindestens alle zwölf Monate sowie bei jeder
Änderung an Capabilities, Datenflüssen, Abhängigkeiten, Build-Prozess oder
Signaturschlüssel rezertifiziert. Ein Minor-/Major-Release erhält erst nach
erneuter Prüfung den Verified-Status; reine Patch-Releases dürfen nur dann
automatisiert übernommen werden, wenn der verifizierte Build-Prozess und
Digestvergleich unverändert bleiben. Bei ausbleibender Rezertifizierung
wird das Listing auf Community herabgestuft und klar gekennzeichnet.

---

## 24. Bewertungen

Optional.

---

Erlaubt:

```text
Sterne

Feedback

Nutzungshinweise
```

---

Nicht erlaubt:

```text
Vertrauensersatz

Sicherheitsversprechen
```

---

## 25. Governance

### Verantwortlich

```text
Marketplace Maintainer Team
```

---

Aufgaben:

```text
Review

Moderation

Policies

Delisting
```

---

## 26. Community Governance

Community kann Vorschläge einbringen.

---

Geeignete Formate:

```text
RFC

Issue

Discussion

Proposal
```

---

## 27. Lizenzanforderungen

Pflicht:

```text
Klare Lizenzangabe
```

---

Bevorzugt:

```text
AGPL

MIT

Apache 2.0
```

---

Unklare Lizenzen:

```text
Kein Listing
```

---

## 28. Dokumentation

Jedes Listing benötigt:

```text
Beschreibung

Installation

Capabilities

Datennutzung

Support Informationen
```

---

## 29. Accessibility

Marketplace Informationen müssen unterstützen:

```text
Screen Reader

Keyboard Navigation

Mehrsprachigkeit
```

---

## 30. Audit Anforderungen

Marketplace Aktionen protokollieren:

```text
Listing

Freigabe

Delisting

Signaturwiderruf

Review
```

---

## 31. Offline Strategie

Pflicht:

```text
Lokale Installation

Marketplace unabhängiger Betrieb
```

---

Marketplace muss vollständig optional bleiben.

---

## 32. Nachhaltigkeit

Langfristig benötigt der Marketplace:

```text
Hosting

Code Signing

Security Reviews

Moderation
```

Diese Kosten müssen transparent finanziert werden. Die Betriebs- und Nachhaltigkeitsfragen werden auch in der Bestandsaufnahme als offene Governance-Themen beschrieben.

---

## 33. Architekturentscheidung

Dieses RFC legt fest:

✅ Drei Vertrauensebenen

✅ Community Listings

✅ Verified Listings

✅ Official Listings

✅ Lokale Installation bleibt möglich

✅ Kein Sicherheitsversprechen durch Badges

✅ Review Prozess

✅ Delisting Prozess

✅ Incident Management

✅ Signaturwiderruf

✅ Transparente Governance

✅ Marketplace bleibt optional

✅ Local-First Prinzip
