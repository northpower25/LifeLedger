# Roadmap: Plugin- und Community-Ökosystem

Ein Home-Assistant-ähnliches Ökosystem ist ein Ziel, aber derzeit nicht
nachgewiesen: [plugins/](../../plugins/README.md) dokumentiert Vorschläge,
aber keine ausführbaren Verträge. Ein Plugin-Verzeichnis ist keine API,
Sicherheitsgrenze oder Community-SDK.
Diese Roadmap ist ein Vorschlag; ein gemeinsamer RFC, ADRs und normative
Spezifikationen müssen die technischen Entscheidungen treffen.

## Erweiterungsgrenzen als Vorschlag

Die [Plattformvision](https://github.com/northpower25/LifeLedger/blob/main/docs/concept)
schlägt sechs Erweiterungstypen vor. Sie benötigen klar getrennte,
versionierte Verträge und ändern nicht die verbindlichen
Komponentenverantwortungen:

| Typ | Vorgeschlagene Rolle und Grenze |
| --- | --- |
| Connector | VitaFabric-owned; externe Gesundheitsquellen wie Garmin, Fitbit, Oura oder Apple Health über VitaFabric importieren, FHIR abbilden und Herkunft erfassen. Beispiele, keine ausgewählten Integrationen. |
| Integration | Externe Systeme wie Home Assistant, Matrix, Nextcloud oder Open WebUI anbinden; sobald Gesundheitsdaten fließen, ausschließlich über VitaFabric. Datenrichtung und Rechte je Integration festlegen. |
| Provider | LifeWeaver-owned, providerneutral und optional. Adapter für lokale oder externe Modelle (z. B. Ollama oder externe Provider); keine provider-spezifische AI-Logik in LifeLedger und keine Übertragung ohne ausdrückliche Freigabe. |
| Storage | VitaFabric-interne Storage-Abstraktion für lokale oder externe Backends, etwa SQLite, PostgreSQL, OneDrive, S3 oder Nextcloud. Beispiele, keine ausgewählten Anbieter. Kein Storage-Plugin erhält direkten, unkontrollierten Datenbankzugriff; Cloud-Backends benötigen separates Review. |
| UI | LifeLedger-owned Präsentations-Erweiterungen wie Dashboards, Widgets und Ansichten mit eingeschränkten UI-Verträgen; Datenzugriff nur über genehmigte Plattform-APIs. |
| Application | Unabhängige Apps wie Medication Manager, Schlaftagebuch, Ernährungstracker oder Sportanalyse über versionierte Plattform-APIs; Gesundheitsdatenzugriff immer über VitaFabric und Consent. |

Das ist eine vorgeschlagene Taxonomie, kein freigegebener Vertrag. Insbesondere
ist der Datenpfad für Gesundheitsdaten fest: Plugin oder Anwendung ->
VitaFabric-Vertrag → FHIR-R4-Modell → kontrollierte Speicherabstraktion.
Direkter Datenbankzugriff durch Erweiterungen ist ausgeschlossen.

Draft [RFC-0002](../../rfc/RFC-0002%20Platform%20Core%20Architecture)
schlägt WASM First als Standard-Laufzeit vor; eine Python Connector Runtime
ist nur als spätere optionale Erweiterung genannt. Es ordnet Identity &
Consent, Audit, Authentifizierung, FHIR-Kernmodell und Capability Enforcement
dem Core Runtime zu, nicht Plugins. Storage-Adapter erhalten nur
verschlüsselte Daten, niemals Klartext oder Schlüssel. Das sind Draft-Vorgaben,
keine bereits implementierten Eigenschaften.

Ein Plugin ist **nicht automatisch vertrauenswürdig**, auch nicht bei lokaler
Installation. Der RFC-Entwurf schlägt signierte Pakete und Manifeste mit
Versionen, Capabilities, minimalen Rechten, expliziter Consent-Freigabe,
Widerruf, Provenienz, Isolation und kontrollierter Kommunikation. Signatur
weist allenfalls Integrität/Quelle nach und ist keine Sicherheitsbewertung;
Capabilities sind nur wirksam, wenn sie technisch erzwungen werden. Ob und
wie Isolation auf unterstützten Plattformen nachweisbar ist, muss vor
Drittanbieter-Ausführung geklärt sein. RFC-0002 schlägt Community
(self-signed), Verified (Maintainer-Review) und Official (LifeLedger-Signatur)
als Vertrauenseinstufungen für Pakete vor, nicht als Sicherheitsgarantie.
Keine versteckte Telemetrie, keine Cloud-Pflicht und kein direkter Zugriff auf
ungeschützte Gesundheitsdaten.

### Marketplace

Die Vision schlägt einen **Marketplace** statt einer bloßen Registry vor,
gegebenenfalls mit Community-, Verified- und Official-Listings. Noch offen
sind Governance, Kriterien, Betreiber, Einspruch/Widerruf und die Bedeutung
jeder Kennzeichnung. Kein Listing oder Badge darf eine Sicherheitsgarantie
oder Nutzer-Consent suggerieren. Discovery und Distribution müssen optional
bleiben; lokale Installation und Betrieb dürfen keinen zentralen Marketplace
voraussetzen.

## Stufen

| Stufe | Ergebnis und Abhängigkeiten | Tests und Abnahme |
| --- | --- | --- |
| P0 – Ökosystem-RFC | Sechs Erweiterungstypen, ihre Ownership, VitaFabric-Datenpfad, Vertrauensgrenzen, erlaubte Fähigkeiten, Signatur/Provenienz, Installation, Consent/Widerruf, Marketplace-Governance und Bedrohungsmodell spezifizieren; auf Gesamtstufe 0 abstimmen. | Community-, Datenschutz-, Security- und Architekturreview; ADRs akzeptieren und normative Verträge versionieren. |
| P1 – Minimaler Erweiterungspunkt | Nach Daten- und Sicherheitsverträgen einen VitaFabric-Connector mit synthetischen Daten sowie SDK/Fixtures, Fehlermodell und Beispiel erstellen. Keine produktiven Daten. | Kontrakt- und Kompatibilitätstests einschließlich unbekannter Versionen, fehlender Fähigkeiten, bösartiger Eingaben und Fehlerisolierung; nachweisen, dass kein direkter Datenbankpfad besteht. |
| P2 – Drittanbieter-Nachweis | Unabhängige Entwickler erstellen anhand öffentlicher Anleitung ein Plugin ohne Änderungen am Kern; nachvollziehbarer lokaler Installations- und Deinstallationspfad. | Konformitätssuite und Security-Tests für Isolation, verweigerte/widerrufene Einwilligung, Netzwerk- und Dateizugriff, Herkunft, Updates und Deinstallation. Nachweis der tatsächlichen Durchsetzung, nicht nur deklarierter Rechte. |
| P3 – Erweiterter Lebenszyklus | Versionierung, Kompatibilitätsmatrix, Deprecation, signierte Integrität/Provenienz von Paketen, Sicherheitsmeldungen und Recovery nach ungeeignetem Update nach gemeinsamer Entscheidung. | Tests für Manipulation, inkompatible Versionen, Rollback, widerrufene Pakete, Offline-Installation und Abwärtskompatibilität; kein zentraler Cloud-Dienst als Pflicht. |
| P4 – Community-Skalierung | Nach Nachweisen für die Connector-Klasse weitere Typen inkrementell freigeben. Marketplace mit Community/Verified/Official-Listings nur nach Governance-, Kriterien- und Sicherheitsentscheidung; lokaler, transparenter Alternativpfad bleibt erforderlich. | Unabhängige Erweiterungen gegen veröffentlichte Versionen, Regressionssuite und dokumentierter Review-/Incident-Prozess. Marketplace-Listing ist kein Sicherheitszertifikat und keine Consent-Freigabe. |

## Offene Fragen

- Welche Isolation ist auf Desktop, Mobile und Web tatsächlich verfügbar und
  wie werden Netzwerk, Dateien, Secrets, Ressourcenverbrauch und Plugin-zu-
  Plugin-Kommunikation technisch begrenzt? Was geschieht bei fehlender Isolation?
- Wer vergibt und widerruft Fähigkeiten; wie wirken sich Consent-Widerruf,
  Deinstallation und bereits exportierte Daten auf den Lebenszyklus aus?
- Wie werden SDK/API-Versionen, Protokolle, Kompatibilität, Migration und
  Supportdauer festgelegt? Wie wird ein Community-Plugin unabhängig getestet?
- Wie funktionieren Offline-Verteilung, Paketprüfung, Signaturschlüssel und
  Updates eines optionalen Marketplace ohne Single Point of Failure?
- Welche überprüfbaren Kriterien trennen Community-, Verified- und
  Official-Listings, wer entscheidet darüber und wie werden Beschwerden oder
  widerrufene Listings behandelt?
- Welche Storage-Backends sind lokal und ohne Providerbindung praktikabel?
  Wie verhindern Schnittstellen, dass ein Storage-Adapter Consent- oder
  VitaFabric-Prüfungen umgeht?
- Welche Regeln gelten für Qualität, Malware-Meldungen, Zuständigkeit,
  De-Listing, Konflikte und langfristige Wartung? Welche Lizenzanforderungen
  gelten für Dritte unter Berücksichtigung von AGPL und fachlicher Rechtsprüfung?
- Wie werden Erweiterungs-UI, Fehler und Dokumentation übersetzt und
  barrierefrei gestaltet? Wie werden Quellen und Datenqualität angezeigt?
