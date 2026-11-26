# Roadmap: VitaFabric

VitaFabric verantwortet den Zugang zu Gesundheitsdaten, FHIR-R4-Modellierung,
Connectoren, Synchronisierung, Provenienz, Datenqualität und
Speicherabstraktion. Es gibt noch keine Implementierung oder
FHIR-Konformitätsbehauptung. Siehe [Gesamt-Roadmap](project.md).

## Stufen

| Stufe | Ergebnis und Abhängigkeiten | Tests und Abnahme |
| --- | --- | --- |
| V0 – Daten- und Vertrauensverträge | RFC/ADRs für lokale Datenflüsse, FHIR-R4-Ressourcen und Profile, Identität, Consent-Durchsetzung, Speicher, Schlüssel, Audit und Provenienz; Schnittstelle zu LifeLedger, LifeWeaver und Plugins spezifizieren. | Review mit synthetischen Beispielen, Fehlerfällen und nachvollziehbarem Mapping; Quelle, Connector, Importzeitpunkt und Original-ID für jeden Import nachweisbar vorsehen. |
| V1 – Minimaler FHIR-Pfad | Ersten ausgewählten Datentyp validieren und über versionierten Vertrag bereitstellen; auch manuelle Eingaben passieren VitaFabric. Verschlüsselte Persistenz und Zugriffsschutz entsprechend freigegebenen Vorgaben. | Unit- und Vertragstests für gültiges/ungültiges FHIR, fehlende Herkunft, doppelte IDs, verweigerten Zugriff und Speicherfehler. |
| V2 – Vertikaler Offline-Pfad | Zusammen mit LifeLedger den synthetischen End-to-End-Durchstich aus Gesamtstufe 2 liefern. | Offline-, FHIR-Profil-, Consent-, Audit-, Schlüssel- und Neustarttests; ungeprüfte oder unzulässige Datensätze gelangen nicht in den lesbaren Bestand. |
| V3 – Lebenszyklus und Qualität | Nach Spezifikation Korrektur, Löschung, Versionierung, verschlüsselte Sicherung/Recovery und Datenqualitätsmeldungen ergänzen. | Migration, Integrität, Fehler beim Wiederherstellen, Rechteentzug und Datenqualitätsfälle testen; keine provider-spezifischen Rohdaten direkt speichern. |
| V4 – Connector- und Sync-Verträge | Sichere Erweiterungspunkte, synthetischen Referenz-Connector und später optional externe Integration entwickeln; Abhängigkeit: freigegebene [Plugin-Verträge](plugins.md). Synchronisierung und Konfliktlösung separat entscheiden. | Konformitätssuite für Mapping, Validierung, Herkunft, idempotenten Import, Abbruch, Konflikte, Widerruf und Ausfälle; Offline-Verhalten testen. |
| V5 – Interoperabilität erweitern | Weitere Ressourcen/Profile und standardisierte Exporte auf Grundlage konkreter Nutzerfälle und Kompatibilitätsregeln. | FHIR-Validierung gegen dokumentierte Profile, Roundtrip- und Regressionstests sowie unabhängige Interoperabilitätsprüfung vor entsprechenden Aussagen. |

## Offene Fragen und Vorschläge

- Welche Ressourcen, Profile, Terminologien, Versionen und Validatoren gelten
  für den ersten Anwendungsfall? Wie werden fehlende bzw. unzulässige Werte
  behandelt, ohne sie stillschweigend zu verändern?
- Wie wird Provenienz bei manueller Eingabe, Korrektur, Zusammenführung und
  Löschung modelliert? Importherkunft ist obligatorisch; weitergehende Regeln
  benötigen Spezifikation.
- Welche lokalen Speicher- und Schlüsselmodelle erfüllen AES-256-GCM, Argon2,
  RBAC, Audit und sichere Wiederherstellung auf den gewählten Geräten?
- Wo und wie werden Einwilligung, Rollen und Widerruf durchgesetzt, auch bei
  Caches, Exporten und bereits synchronisierten Kopien?
- Wie werden Synchronisierungskonflikte, Schema-Upgrades und unvollständige
  Importe nachvollziehbar und ohne Datenverlust behandelt?
- Vorschlag: Ein FHIR-Beispieldatensatz mit vollständiger Herkunft als
  gemeinsames Vertragsfixture für Clients, Connectoren und LifeWeaver.
