# RFC 0015: FHIR Profiles & Terminology Governance

- Status: Draft
- Owner: VitaFabric / FHIR Governance (Rolle, Person noch zu benennen)
- Depends On: [RFC-0013 VitaFabric Data Contracts & FHIR Governance](0013-vitafabric-data-contracts-and-fhir-governance.md)

## Ziel

Normierung von:

- Ressourcen
- Profilen
- Terminologien
- Validierung

---

## MVP Ressourcen

```text
Patient
Observation
Condition
MedicationStatement
AllergyIntolerance
DocumentReference
```

---

## Profilklassen

```text
Core Profile
Experimental Profile
Community Profile
```

---

## Terminologien

MVP:

```text
SNOMED CT
LOINC
UCUM
```

Die Nutzung dieser Code-Systeme und konkrete Bindungen sind noch nicht
beschlossen; offline verfügbare Versionen und Lizenzrechte müssen je System
geprüft werden. Ein nicht erreichbarer Terminologieserver darf eine
verpflichtende Prüfung nicht stillschweigend erfolgreich machen.

---

## Validator

Referenz:

```text
HL7 FHIR Validator
```

---

## Pflichtfelder

Patient:

```text
id
identifier
name
birthDate
```

Observation:

```text
code
status
effective[x] nach gewähltem Profil
value[x] oder begründetes dataAbsentReason nach gewähltem Profil
```

---

## Versionsstrategie

```text
FHIR R4

R4B später

R5 später
```

## FHIR Profiles

Für jeden der sechs MVP-Typen wird ein eigenes versioniertes R4-Core-Profil
mit kanonischer URL, Basisprofil, Kardinalitäten, Datentypen, Invarianten,
Referenzzielen und zulässigen Erweiterungen benötigt. Die obigen Felder sind
Profilvorschläge, nicht die Behauptung, sie seien alle durch FHIR R4 selbst
verpflichtend. Für `Observation` sind `value[x]` und `dataAbsentReason`
FHIR-Alternativen; die konkrete Auswahl und Zeitanforderung bedürfen der
Profilentscheidung. `DocumentReference` muss auf ein geschütztes Original
verweisen; MIME-Typ, Größe, Integrität und Profil-Referenzen sind festzulegen.
Die verbleibenden drei Typen gehören zum MVP-Katalog, müssen aber nicht im
ersten Durchstich implementiert werden.

## ValueSets und Terminologies

Jede Coding-Bindung benennt ValueSet-URL, Version, Binding Strength und
Offline-Verhalten. Unbekannte Codes bei required-Bindung werden nicht
stillschweigend akzeptiert; bei fehlendem Offline-Nachweis gilt der
Validierungspfad aus RFC-0013. Proprietäre oder lizenzpflichtige
Terminologiepakete dürfen nicht ohne Nutzungsrecht gebündelt werden. Ein
konkreter Satz von Codes und ValueSets fehlt weiterhin.

## Validator Config und Test Fixtures

Vor Implementierungsstart müssen unter `specifications/fhir/` versionierte
StructureDefinitions, ValueSets und Validator-Konfiguration einschließlich
exakter FHIR-R4-, HL7-Validator- und Paketversion, Offline-Paketen sowie
Schweregradzuordnung bereitstehen. Für jeden verwendeten Typ sind
synthetische gültige und ungültige Fixtures mit erwarteten Ergebnissen
erforderlich: fehlendes Pflichtfeld, ungültiger Code, falscher Referenztyp,
`Observation.value[x]`/`dataAbsentReason` und ungültige Dokumentreferenz.
Die Dateien und Lizenzprüfung sind noch nicht vorhanden; ein RFC-Beispiel
ersetzt keinen ausführbaren Validatorvertrag.

## Governance

Core-Profile werden versioniert und vor Nutzung unabhängig geprüft;
inkompatible Änderungen benötigen eine neue Version und einen
Migrationsvertrag. Experimental- und Community-Profile dürfen Core-Regeln
nicht abschwächen und gelangen nicht ohne Freigabe in den kanonischen
Bestand. Owner, Reviewverfahren und Kompatibilitätszeitraum sind zu benennen.
