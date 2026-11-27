# Roadmap: Integrationen und Home Assistant

Integrationen verbinden externe Systeme mit den Plattformverträgen. Ein
Home-Assistant-Verzeichnis existiert, aber keine Integration. Connector-
Ausführung und FHIR-Mapping gehören zu VitaFabric; Integrationsteams
koordinieren Lebenszyklus und externe Kompatibilität, ohne Gesundheitsdaten-
Verarbeitung aus VitaFabric herauszulösen. Datenrichtung, API, Consent und
Identitätsgrenzen sind je Integration zu entscheiden.

## Stufen

| Stufe | Ergebnis und Abhängigkeiten | Tests und Abnahme |
| --- | --- | --- |
| I0 – Scope und Verträge | Bedarf und Richtung je Integration, Datenarten, Nutzer/Familienrollen, Einwilligung, lokale Verbindung und Bedrohungsmodell spezifizieren. Abhängig von Identity-&-Consent-, VitaFabric- und Plugin-Verträgen. | Architektur-/Security-Review; prüfen, dass kein Gesundheitsdatenpfad VitaFabric, FHIR, Herkunft oder Consent umgeht. |
| I1 – Synthetische Referenz | Unabhängig vom Hersteller ein lokaler Test-Connector mit synthetischer Quelle und dokumentierter Konformitätssuite; keine externen Konten erforderlich. | Fehler, unvollständige Daten, Herkunft, Dubletten, Consent-Widerruf und Netzwerkausfall automatisiert testen. |
| I2 – Erste optionale Integration | Nextcloud ist als erste externe Integration vor Home Assistant vorgesehen; Umfang und Datenrichtung benötigen ein eigenes Review. Datenminimierung und Nutzerfreigabe vor jeder Übertragung. | Ende-zu-Ende mit lokalen Testsystemen, Datenfluss in jeder freigegebenen Richtung, verweigerter/widerrufener Zugriff, Neustart, Fehler und Offline-Nutzung des Kerns. |
| I3 – Hersteller- und Community-Ausbau | Weitere Connectoren über dieselben versionierten Verträge, dokumentierte Kompatibilität und Supportverantwortung ergänzen. Optionale Cloud-Anbindung darf den lokalen Kern nicht abhängig machen. | Wiederverwendbare Konformitätssuite, Upgrade-/Regressionstests, Sicherheitsprüfung und dokumentierte Grenzen je Integration. |

## Home Assistant: vorab klären

- Welcher konkrete Nutzen und welche Datenrichtung sind gewünscht: Import,
  Export oder beides? Welche minimalen Daten und welche Freigaben sind nötig?
- Wie werden Identität, Transport, lokale Authentifizierung, Widerruf,
  Wiederverbindung und die tatsächlichen Vertrauensgrenzen beider Systeme
  geregelt? Wie wird Weitergabe an Dritte in Home Assistant kenntlich gemacht?
- Welche Plugin-Klasse beschreibt den Home-Assistant-Umfang am besten:
  externe Integration oder VitaFabric-Connector? Die Benennung darf keine
  direkte Gesundheitsdatenbank-Verbindung implizieren.
- Welche FHIR-Abbildung und Herkunft gelten für Sensorwerte, Zeitzonen,
  Einheiten und Korrekturen? Wie werden ungültige oder veraltete Werte behandelt?
- Wie werden Community-Wartung, Kompatibilität mit Home-Assistant-Versionen
  und sichere Veröffentlichung organisiert, ohne einen Hersteller zu bevorzugen?
- Wie unterscheiden sich lokaler Zugriff und optionale Relay- oder
  Sync-Szenarien bezüglich Metadaten, Consent und Vertrauensgrenzen? Kein
  Cloud-Dienst darf Voraussetzung für den lokalen Kern werden.

Vorschlag: Zuerst eine begrenzte, synthetische lokale Datenrichtung nach
freigegebenem Consent-Modell testen; bidirektionale Synchronisierung erst nach
separater Konflikt- und Risikobewertung.
