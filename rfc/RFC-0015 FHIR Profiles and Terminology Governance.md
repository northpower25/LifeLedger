# RFC-0015: FHIR Profiles & Terminology Governance

Status: Draft

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

optional.

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
effectiveDateTime
value
```

---

## Versionsstrategie

```text
FHIR R4

R4B später

R5 später
```
