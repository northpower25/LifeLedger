# RFC 0013: VitaFabric Data Contracts & FHIR Governance

- Status: Draft
- Type: Architecture RFC
- Owner: VitaFabric

Depends On:
- RFC-0002 Platform Core Architecture
- RFC-0003 Identity & Consent
- RFC-0004 Capability Model
- RFC-0005 Event Bus
- RFC-0010 Zero Knowledge Sync

Blocks:
- First Real Dataset
- Connector Framework
- Storage Framework
- Health Record Application
- External Integrations

---

## 1. Zusammenfassung

Dieses RFC definiert die verbindlichen Datenverträge
der Plattform.

VitaFabric ist das einzige autorisierte
Gesundheitsdaten-Gateway.

Alle Gesundheitsdaten passieren VitaFabric.

Keine Anwendung, Integration, KI-Komponente
oder Erweiterung darf Gesundheitsdaten
an VitaFabric vorbei lesen oder schreiben.

---

## 2. Ziele

### Ziele

```text
FHIR First

Datenkonsistenz

Provenienz

Interoperabilität

Versionsstabilität

Connector Unabhängigkeit
```

### Nichtziele

```text
FHIR Vollabdeckung

Beliebige Datenformate

Provider-spezifische Rohdaten
```

---

## 3. Architekturprinzipien

### Single Source of Truth

Alle Gesundheitsdaten leben logisch
in VitaFabric.

---

### Canonical Data Model

FHIR R4 ist das interne Referenzmodell.

---

### Provenance Required

Jeder Datensatz besitzt Herkunft.

---

### Validation First

Keine Daten ohne Validierung.

---

## 4. Erste unterstützte FHIR Ressourcen

MVP Umfang:

```text
Patient

Observation

Condition

MedicationStatement

AllergyIntolerance

DocumentReference
```

---

## MVP Resource Contract

Das MVP beschränkt kanonische FHIR-R4-Ressourcen auf `Patient`, `Observation`,
`Condition`, `MedicationStatement`, `AllergyIntolerance` und
`DocumentReference`; weitere Ressourcentypen sind nicht Teil dieses MVP.
Der erste Durchstich verwendet davon `Patient`, `Observation` und
`DocumentReference` als vorgeschlagene Teilmenge. Eine vollständige erste
Nutzerreise mit Medikation benötigt zusätzlich `MedicationStatement` und ist
nicht automatisch Teil dieses kleineren Durchstichs. Das Dokumentoriginal
bleibt separat geschützt und über die `DocumentReference` referenziert.
Provenienz ist verpflichtende VitaFabric-Metadaten und erfordert im MVP keine
zusätzliche FHIR-`Provenance`-Ressource. RFC-0015 beschreibt die noch zu
veröffentlichenden Profile und Fixtures; diese Liste allein ist kein Profil.

## 5. FHIR Version

Festgelegt:

```text
FHIR R4
```

Nicht:

```text
R4B

R5
```

für den Erstaufbau.

---

## 6. Canonical Storage Modell

Entscheidung:

```text
FHIR JSON
```

als kanonisches Format.

Dieses Format gilt für FHIR-Ressourcen. Zusätzlich verwaltet VitaFabric die
Datenklasse **Derived Data** für abgeleitete Daten, darunter Embeddings,
Knowledge Graph, AI Summaries und Derived Metadata. Diese Daten sind nicht
automatisch FHIR-Ressourcen; ihr Zugriff erfolgt ebenfalls ausschließlich
über VitaFabric und unterliegt Identity, Consent und Capabilities. Konkrete
Schemas folgen RFC-0011; Quellenbezug, Modell-/Indexversion, Widerruf,
Reindex und Löschlebenszyklus müssen die dort festgelegten Anforderungen
erfüllen.

---

Speicherung:

```text
FHIR JSON

+

Indexe

+

Materialisierte Views
```

---

## 7. Datenfluss

```text
Connector

↓

Mapping

↓

FHIR

↓

Validation

↓

Consent

↓

Storage
```

---

## 8. Import Modell

Jeder Import benötigt:

```text
Connector ID

Source ID

Import Timestamp

Data Origin

Version
```

---

## 9. Provenance

Pflichtfelder:

```text
Quelle

Zeitstempel (bei Import: Importzeitpunkt)

Connector

Original ID

Version

Transformationsschritte
```

Die Repräsentation dieser Felder bei manueller Eingabe ohne externen
Connector oder Original-ID ist noch festzulegen.

---

## 10. Datenqualität

Qualitätsstufen:

```text
RAW

VALIDATED

CORRECTED

REVIEWED
```

---

## 11. Validierung

FHIR Ressourcen werden geprüft gegen:

```text
Schema

Profile

Business Rules
```

Als Validator ist der HL7 FHIR Validator vorgesehen. Version, Profile,
Terminologien und die Integration in den lokalen Datenpfad sind noch
festzulegen. Laufzeit-, Speicher- und Startzeitkosten auf den unterstützten
Geräten sind vor der Produktfreigabe zu prüfen.

## Validation Failure Behaviour

* `REJECT`: ungültiges JSON, nicht unterstützter Typ, fehlende Pflichtwerte,
  gebrochene Referenz oder Verletzung einer verpflichtenden Profilregel.
  Keine kanonische Änderung; ein datensparsam protokollierter Fehler wird
  zurückgegeben.
* `WARN`: ausschließlich nicht-blockierende, ausdrücklich im versionierten
  Profil registrierte Warnungen. Speicherung nur nach expliziter Bestätigung;
  Warnung und Validatorversion werden dem Vorgang zugeordnet.
* `QUARANTINE`: bei Import, dessen Prüfung wegen fehlender Terminologie oder
  unbestimmter Herkunft nicht abgeschlossen werden kann. Verschlüsselt,
  getrennt vom kanonischen Bestand, nicht für regulären Zugriff freigegeben;
  prüfberechtigte Person entscheidet über erneute Prüfung oder Löschung.
  Quarantäne darf das Verbot der Ablage providerspezifischer Rohdaten nicht
  umgehen; zulässige Datenform und Schutz bedürfen eines separaten Vertrags.

Kein stilles Korrigieren. Quarantäne ist kein Fallback bei Ausfall von
Verschlüsselung, Consent, Capability oder Audit: dann wird abgelehnt.
Offline-Terminologie, Quarantänefristen, Größenlimits und konkrete Zuordnung
der Validatorbefunde sind noch festzulegen. Für den ersten Slice ist ein
reiner Reject-Pfad zulässig, sofern Warnung und Quarantäne nicht als
implementiert behauptet werden.

---

## 12. Dokumentenmodell

Dokumente werden als:

```text
DocumentReference
```

modelliert.

---

Originaldatei bleibt erhalten.

---

## 13. Manueller Dateneintrag

Manuelle Daten sind erlaubt.

---

Pflicht:

```text
Provenance:
MANUAL_ENTRY
```

---

## 14. Connector Verträge

Connectoren erhalten:

```text
Import APIs
```

---

Connectoren erhalten niemals:

```text
Database Access
```

---

## 15. Storage Verträge

VitaFabric ist für die Verschlüsselung vor Übergabe an einen Storage-Adapter
verantwortlich. Ein Storage-Plugin übernimmt diese Verschlüsselung nicht und
erhält keine Schlüssel.

Storage Adapter erhalten:

```text
verschlüsselte Daten
```

---

Storage Adapter sehen niemals:

```text
FHIR Ownership

Consent

Klartextprofile
```

---

## 16. Event Integration

FHIR Events gemäß RFC-0005.

```text
FHIR_CREATED

FHIR_UPDATED

FHIR_DELETED
```

---

## 17. Consent Durchsetzung

Jeder Zugriff prüft:

```text
Identity

Consent

Capability
```

---

## 18. Versionierung

Jeder Ressourcentyp besitzt:

```text
Contract Version

Migration Strategy

Backward Compatibility
```

---

## 19. Synchronisation

RFC-0010 bleibt maßgeblich.

Last Writer Wins ist nur für Settings, UI-Daten und Preferences zulässig;
FHIR-Ressourcen durchlaufen den Conflict Resolution Workflow aus RFC-0010.
Ein konkretes Verfahren für andere Datenklassen, insbesondere Derived Data,
ist noch festzulegen.

Derived Data dürfen bei einem Konflikt nicht unabhängig von ihrer autoritativen
Quelle wiederhergestellt werden. Consent-Widerruf und Lösch-Tombstones sperren
abgeleitete Zugriffe sofort; Reindex und Wiederherstellung folgen RFC-0011.

---

VitaFabric liefert:

```text
Objekte

Versionen

Konfliktinformationen
```

---

## 20. Export

Unterstützt:

```text
FHIR Bundle

FHIR NDJSON

JSON Export
```

---

## 21. Sicherheitsanforderungen

Pflicht:

```text
Audit

Encryption

Validation

Consent Enforcement

Capability Enforcement
```

---

## 22. Architekturentscheidung

✅ FHIR R4 Canonical Model

✅ VitaFabric als Single Data Gateway

✅ Provenance Pflicht

✅ Validation Pflicht

✅ Canonical JSON Storage

✅ Keine Direktzugriffe

✅ FHIR First

✅ Connector Isolation

✅ Storage Isolation

✅ Contract Versionierung
