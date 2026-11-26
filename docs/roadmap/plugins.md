# Roadmap: Plugin- und Community-Ökosystem

Ein Home-Assistant-ähnliches Ökosystem ist ein Ziel, aber derzeit nicht
nachgewiesen: [plugins/](../../plugins/README.md) enthält nur einen Platzhalter.
Ein Plugin-Verzeichnis ist keine API, Sicherheitsgrenze oder Community-SDK.
Diese Roadmap ist ein Vorschlag; ein gemeinsamer RFC, ADRs und normative
Spezifikationen müssen die technischen Entscheidungen treffen.

## Erweiterungsgrenzen als Vorschlag

Unterschiedliche Erweiterungstypen sollen klar getrennte, versionierte
Verträge erhalten: Connectoren und FHIR-Mapping in VitaFabric; AI-Provider,
MCP und Agenten in LifeWeaver; gegebenenfalls LifeLedger-Oberflächen über
eigene, begrenzte Präsentationsverträge. Externe Integrationen orchestrieren
nur die freigegebenen Verträge und umgehen VitaFabric nicht. Die konkrete
Platzierung, Ausführung und Ownership bedarf eines ADRs.

Ein Plugin ist **nicht automatisch vertrauenswürdig**, auch nicht bei lokaler
Installation. Vorschlag für den RFC: deklarierte Fähigkeiten und Versionen,
minimale Berechtigungen, explizite Nutzerfreigabe, nachvollziehbare Herkunft,
Isolation und kontrollierte Kommunikation. Ob und wie Isolation auf den
gewählten Plattformen tatsächlich durchgesetzt werden kann, muss vor
Drittanbieter-Ausführung nachgewiesen werden. Ein Manifest allein ist keine
Sandbox. Keine versteckte Telemetrie, keine Cloud-Pflicht und kein direkter
Zugriff auf ungeschützte Gesundheitsdaten.

## Stufen

| Stufe | Ergebnis und Abhängigkeiten | Tests und Abnahme |
| --- | --- | --- |
| P0 – Ökosystem-RFC | Erweiterungstypen, Vertrauensgrenzen, erlaubte Fähigkeiten, Installation, Widerruf, Datenflüsse, Verantwortliche und Bedrohungsmodell spezifizieren; auf Gesamtstufe 0 abstimmen. | Community-, Datenschutz-, Security- und Architekturreview; ADRs akzeptieren und normative Verträge versionieren. |
| P1 – Minimaler Erweiterungspunkt | Nach Daten- und Sicherheitsverträgen eine Art von lokalem, synthetischem Connector sowie SDK/Fixtures, Fehlermodell und Beispiel erstellen. Keine produktiven Daten. | Kontrakt- und Kompatibilitätstests einschließlich unbekannter Versionen, fehlender Fähigkeiten, bösartiger Eingaben und Fehlerisolierung. |
| P2 – Drittanbieter-Nachweis | Unabhängige Entwickler erstellen anhand öffentlicher Anleitung ein Plugin ohne Änderungen am Kern; nachvollziehbarer lokaler Installations- und Deinstallationspfad. | Konformitätssuite und Security-Tests für Isolation, verweigerte/widerrufene Einwilligung, Netzwerk- und Dateizugriff, Herkunft, Updates und Deinstallation. Nachweis der tatsächlichen Durchsetzung, nicht nur deklarierter Rechte. |
| P3 – Erweiterter Lebenszyklus | Versionierung, Kompatibilitätsmatrix, Deprecation, signierte Integrität/Provenienz von Paketen, Sicherheitsmeldungen und Recovery nach ungeeignetem Update nach gemeinsamer Entscheidung. | Tests für Manipulation, inkompatible Versionen, Rollback, widerrufene Pakete, Offline-Installation und Abwärtskompatibilität; kein zentraler Cloud-Dienst als Pflicht. |
| P4 – Community-Skalierung | Weitere Erweiterungstypen und gegebenenfalls Verzeichnis/Discovery erst nach Governance- und Sicherheitsentscheidung; lokaler, transparenter Alternativpfad bleibt erforderlich. | Unabhängige Integrationen gegen veröffentlichte Versionen, Regressionssuite und dokumentierter Review-/Incident-Prozess. Ein Verzeichnis ist kein Sicherheitszertifikat. |

## Offene Fragen

- Welche Isolation ist auf Desktop, Mobile und Web tatsächlich verfügbar und
  wie werden Netzwerk, Dateien, Secrets, Ressourcenverbrauch und Plugin-zu-
  Plugin-Kommunikation technisch begrenzt? Was geschieht bei fehlender Isolation?
- Wer vergibt und widerruft Fähigkeiten; wie wirken sich Consent-Widerruf,
  Deinstallation und bereits exportierte Daten auf den Lebenszyklus aus?
- Wie werden SDK/API-Versionen, Protokolle, Kompatibilität, Migration und
  Supportdauer festgelegt? Wie wird ein Community-Plugin unabhängig getestet?
- Wie funktionieren Offline-Verteilung, Paketprüfung, Signaturschlüssel,
  Updates und ein möglicher Registry-Betrieb ohne Single Point of Failure?
- Welche Regeln gelten für Qualität, Malware-Meldungen, Zuständigkeit,
  De-Listing, Konflikte und langfristige Wartung? Welche Lizenzanforderungen
  gelten für Dritte unter Berücksichtigung von AGPL und fachlicher Rechtsprüfung?
- Wie werden Erweiterungs-UI, Fehler und Dokumentation übersetzt und
  barrierefrei gestaltet? Wie werden Quellen und Datenqualität angezeigt?
