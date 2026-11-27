# RFC 0012: Sustainability, Governance & Operations

- Status: Draft
- Type: Governance RFC
- Owner: Project Governance
Depends On: RFC-0002 Platform Core Architecture  
Depends On: RFC-0009 Marketplace Governance  
Depends On: RFC-0010 Zero Knowledge Sync

Blocks:
- Public Release
- Managed Services
- Marketplace Operations
- Official Plugins
- Community Governance

---

## 1. Zusammenfassung

Dieses RFC definiert die langfristige Betriebs-, Governance- und Nachhaltigkeitsstrategie der LifeLedger Plattform.

Technisch kann eine Plattform funktionieren.

Projekte scheitern jedoch meist an:

```text
Finanzierung

Wartung

Moderation

Security

Dokumentation

Governance
```

Dieses RFC definiert deshalb die organisatorische Struktur hinter LifeLedger.

Das Ziel ist:

```text
Langfristige Wartbarkeit

Transparenz

Unabhängigkeit

Community-Beteiligung
```

ohne die Plattform von einem einzelnen Unternehmen oder Sponsor abhängig zu machen. Die Notwendigkeit dieser Regelungen wird in den Roadmaps und der Bestandsaufnahme ausdrücklich hervorgehoben.

---

## 2. Ziele

### Ziele

```text
Projektkontinuität

Nachhaltige Finanzierung

Offene Governance

Sicherheitsprozesse

Dokumentationspflege

Community-Beteiligung
```

---

### Nichtziele

```text
Kommerzielle Exklusivität

Verpflichtende Cloud-Abos

Closed Source Betrieb

Provider Lock-In
```

---

## 3. Grundprinzipien

### Local First

Lokale Nutzung bleibt dauerhaft möglich.

---

### Open Source First

Der Kern bleibt offen.

---

### Community Before Monetization

Geschäftsmodelle dürfen Kernprinzipien nicht gefährden.

---

### Security Before Growth

Sicherheit hat Vorrang vor Funktionserweiterungen.

---

## 4. Governance Modell

### Governance Ebenen

GitHub, RFC-Prozess und Maintainer-Modell bilden die vorgesehene
Arbeitsgrundlage. OpenCollective ist für die Finanzierungsphase gemäß §24
vorgesehen; daraus folgt keine bereits bestehende Organisation oder
Infrastruktur.

```text
Community

Contributors

Maintainers

Core Maintainers

Steering Committee
```

---

## 5. Community

Kann:

```text
Issues

RFCs

Pull Requests

Dokumentation
```

beitragen.

---

## 6. Contributors

Personen mit regelmäßigen Beiträgen.

---

Können:

```text
Reviews

Verbesserungen

Roadmap Feedback
```

leisten.

---

## 7. Maintainers

Verantwortlich für Komponenten.

---

Beispiele:

```text
LifeLedger

VitaFabric

LifeWeaver

Marketplace
```

---

## 8. Core Maintainers

Verantwortlich für:

```text
Architektur

RFC Freigaben

Breaking Changes
```

---

## 9. Steering Committee

Langfristige Projektführung.

---

Entscheidet:

```text
Strategie

Lizenzfragen

Governance

Finanzierung
```

---

## 10. Entscheidungssystem

### Technische Entscheidungen

```text
RFC Prozess
```

---

### Dauerhafte Entscheidungen

```text
ADR Prozess
```

---

### Konflikte

```text
Maintainer Vote
```

---

## 11. RFC Prozess

Vorschlag:

```text
Draft

↓

Discussion

↓

Review

↓

Accepted

↓

Implemented
```

---

## 12. Sicherheitsgovernance

### Security Team

Eigenständige Rolle.

---

Verantwortlich für:

```text
Vulnerabilities

Disclosure

Incident Response

Security Reviews
```

---

## 13. Security Meldungen

Unterstützte Kanäle:

```text
Security Email

GitHub Security Advisory

Responsible Disclosure
```

---

## 14. Incident Response

Ablauf:

```text
Meldung

↓

Analyse

↓

Priorisierung

↓

Fix

↓

Veröffentlichung
```

---

## 15. Marketplace Betrieb

Der Marketplace benötigt Betreiber.

---

Verantwortlich für:

```text
Moderation

Delisting

Signing

Review Prozesse
```

---

## 16. Signing Infrastructure

Official Plugins benötigen Projekt-Signaturen.

---

Verantwortung:

```text
Marketplace Team

Security Team
```

---

## 17. Relay Infrastruktur

Optionales Deployment.

---

Betrieb:

```text
Projekt

Community

Sponsoren
```

möglich.

---

Kein Relay wird vorausgesetzt.

---

## 18. Zero Knowledge Sync Betrieb

Optional.

---

Betreiber dürfen niemals besitzen:

```text
Schlüssel

Passwörter

Plaintext Daten
```

---

RFC-0010 bleibt verbindlich.

---

## 19. Dokumentation

Jede Plattformkomponente benötigt:

```text
README

Architekturdokumentation

RFC Referenzen

Beispiele
```

---

## 20. Übersetzungen

Geplante Hauptsprachen:

```text
Deutsch

Englisch
```

---

Spätere Sprachen:

```text
Französisch

Spanisch

Weitere Community Beiträge
```

---

## 21. Übersetzungsprozess

Empfohlen:

```text
Weblate
```

oder

```text
Crowdin
```

---

## 22. Accessibility

Projektziel:

```text
WCAG 2.2 AA
```

---

Verantwortlich:

```text
UI Maintainer

Application Maintainer
```

---

## 23. Lizenzmodell

Projektkern:

```text
AGPL-3.0
```

gemäß aktuellem Repository-Stand.

---

Plugins dürfen:

```text
Open Source

oder

Kompatibel lizenzierte Modelle
```

verwenden.

---

## 24. Finanzierung

Finanzierung erfolgt stufenweise.

---

### Phase 1

```text
Privates Projekt

Community Beiträge
```

---

### Phase 2

```text
GitHub Sponsors

OpenCollective
```

---

### Phase 3

```text
Managed Services

Hosting

Support
```

---

## 25. Ausgaben

Mögliche Kosten:

```text
Code Signing

Domains

Hosting

CI Infrastruktur

Security Audits

Dokumentation
```

---

## 26. Transparenz

Pflicht:

```text
Offene Finanzberichte

Sponsorenübersicht

Governance Dokumentation
```

---

## 27. Release Management

Jedes Release benötigt:

```text
Changelog

Tests

Sicherheitsprüfung

Versionsinformationen
```

---

## 28. Support Modell

### Community Support

```text
GitHub Discussions

Issues
```

---

### Maintainer Support

Best Effort.

---

### Kommerzieller Support

Später optional.

---

## 29. Nachhaltigkeitsrisiken

Risiken:

```text
Maintainer Burnout

Finanzierungsausfall

Sicherheitsaufwand

Dokumentationsschulden
```

---

## 30. Gegenmaßnahmen

```text
Transparente Prozesse

Geteilte Verantwortung

Automatisierung

Dokumentation

Öffentliche RFCs
```

---

## 31. Erfolgskennzahlen

Beispiele:

```text
Aktive Maintainer

Offene Security Issues

Dokumentationsabdeckung

Review Zeiten

Release Stabilität
```

---

## 32. Betriebsmodelle

Unterstützte Modelle:

```text
Community Betrieben

Stiftungsmodell

Verein

Unternehmen mit Community Governance
```

---

Keine Bindung an ein einzelnes Modell.

---

## 33. Maintainer Succession Process

Der Nachfolgeprozess gilt für Core Maintainer, Marketplace-Verantwortliche
und Security-Team-Mitglieder. Für jede kritische Rolle gibt es mindestens
eine benannte Vertretung, dokumentierte Aufgaben, offene Vorgänge,
Abhängigkeiten und eine Liste der benötigten Zugänge. Öffentliche
Übergabedokumentation enthält niemals Geheimnisse oder private Schlüssel.

### Geplanter Rückzug

Die ausscheidende Person kündigt den Rückzug an, übergibt offene Arbeiten und
Zuständigkeiten an die benannte Vertretung und lässt nicht mehr benötigte
Zugänge widerrufen. Neue Rechte werden nur nach dokumentierter Zustimmung der
für die Komponente zuständigen Maintainer erteilt.

### Ausfall oder Nichterreichbarkeit

Bei längerem Ausfall übernehmen die benannten Vertretungen die Tagesarbeit,
aber keine dauerhafte Governance- oder Schlüsselinhaberschaft. Nach 14
Kalendertagen ohne bestätigte Erreichbarkeit können mindestens zwei
unabhängige Core Maintainer gemeinsam eine befristete Vertretung für höchstens
90 Tage einsetzen. Eine Verlängerung oder dauerhafte Nachfolge erfordert
öffentliche Begründung und dokumentierte Zustimmung der verbleibenden
Core-Maintainer-Mehrheit; bei fehlendem Quorum bleibt die Änderung blockiert
und wird nicht durch Einzelentscheidung freigegeben.

Marketplace- und Security-Team-Vertretungen müssen jeweils aus dem
entsprechenden Bereich kommen. Die Marketplace-Vertretung darf keine
Sicherheitsmeldung eigenständig schließen; die Security-Vertretung darf
keine Paketfreigabe allein signieren.

### Zugänge und Schlüssel

Konten, Tokens und Rollen werden personenbezogen vergeben, inventarisiert und
bei Ausscheiden oder Kompromittierung unverzüglich widerrufen. Signing Keys
werden nicht übertragen: Bei notwendigem Wechsel wird ein neuer Schlüssel
unter Vier-Augen-Kontrolle erzeugt, veröffentlicht und der alte widerrufen.
Recovery, Rotation, Widerruf und neue Vertrauensanker werden nachvollziehbar
protokolliert. Keine Person darf allein gleichzeitig den Build, die
Marketplace-Freigabe und die finale Projektsignatur kontrollieren.

Fristen und Quoren dieses Prozesses sind Governance-Vorschläge und müssen vor
einem produktiven Marketplace- oder Release-Betrieb durch die zuständige
Projektgovernance bestätigt werden.

---

## Maintainer Succession Policy

Der Prozess in §33 ist der geltende Entwurf für Übergabe, Ausfallvertretung,
Quorum und Schlüsselrotation. Vor Betriebsaufnahme müssen konkrete
Rolleninhaber und unabhängige Vertretungen benannt und ein getesteter
Zugangs- und Incident-Übergabeplan hinterlegt werden. Fehlt das vorgeschlagene
Quorum, werden privilegierte Freigaben ausgesetzt statt ein Vier-Augen-Prinzip
zu fingieren. Die Fristen und Quoren bedürfen der Governance-Annahme.

## Security Escalation Matrix

| Ereignis | Erstzuständigkeit | Eskalation und Begrenzung |
| --- | --- | --- |
| Verdacht auf Schwachstelle | Security-Team über den privaten Meldekanal in `SECURITY.md` | vertrauliche Triage, keine öffentliche Offenlegung vor abgestimmter Koordination |
| Schlüsselkompromittierung | Security und Signing-Verantwortliche | Signierung stoppen, Schlüssel widerrufen/rotieren, Maintainer informieren |
| Aktive Ausnutzung oder Datenabfluss | Security und zuständige Betriebsverantwortliche | betroffene Funktion isolieren, Belege sichern, Incident und gegebenenfalls Meldepflichten prüfen |
| Kein Security-Ansprechpartner erreichbar | benannte Security-Vertretung | privilegierte Releases pausieren; keine einseitige Freigabe |

Konkrete Personen, gesicherte Kommunikationswege, Schweregrade,
Reaktionsfristen und rechtliche Meldewege müssen vor Betrieb beschlossen und
geübt werden. Keine Zusage einer bereits existierenden Bereitschaft.

## 34. Architekturentscheidung

Dieses RFC legt fest:

✅ Open Source First

✅ Local First

✅ RFC basierte Governance

✅ Maintainer Modell

✅ Security Team

✅ Marketplace Betrieb

✅ Signing Infrastruktur

✅ Community Finanzierung

✅ Mehrsprachigkeit

✅ Accessibility Ziele

✅ Transparente Finanzen

✅ Nachhaltiger Projektbetrieb
