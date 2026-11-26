# Gesamt-Roadmap

## Status und Ziel

Planungsvorschlag ohne Termine oder zugesagte Releases. Ausgangspunkt ist die
[Bestandsaufnahme](assessment.md): keine laufenden Dienste, keine produktiven
Daten und keine nachgewiesene Konformität. Die Reihenfolge beschreibt
Abhängigkeiten, nicht notwendig aufeinanderfolgende Kalenderphasen. Arbeit
ohne Abhängigkeit kann parallel stattfinden; jede Stufe benötigt ihre
genannten Nachweise.

## Verbindliche Leitplanken

Gesundheitsdaten passieren VitaFabric und werden in FHIR R4 modelliert;
Importe benötigen Quelle, Connector, Importzeitpunkt und ursprüngliche ID.
Zugriffe müssen Einwilligung beachten. Lokale Nutzung darf keine Cloud
voraussetzen; AI ist für den Kern optional. Sicherheitsvorgaben einschließlich
AES-256-GCM, Argon2, RBAC, Audit-Logging und MFA-Unterstützung sind in konkrete, überprüfbare
Spezifikationen umzusetzen. UI, Meldungen und Fehler sind lokalisierbar; Deutsch
und Englisch sind gemäß Produktdokumenten erste Zielsprachen. Architektur- und
Plugin-Vorschläge benötigen RFC, ADR und Review vor Umsetzung. Einzelheiten
und ungelöste Zielkonflikte werden nicht durch diese Roadmap entschieden.

## Stufen und Gates

| Stufe | Ergebnis und Abhängigkeit | Nachweis bzw. Gate |
| --- | --- | --- |
| 0 – Richtung und Schutz | Zielgruppe, erster Anwendungsfall, Bedrohungsmodell, System- und Vertrauensgrenzen, Sicherheits- und Einwilligungsmodell, lokale Laufzeit, FHIR- und Plugin-RFCs. Verantwortliche und Entscheidungspfade benennen. | Offene Blocker und Annahmen dokumentiert; betroffene Verantwortliche und Security/Interoperabilität prüfen; benötigte ADRs akzeptiert und Spezifikationen versioniert, bevor entsprechende Funktionen entstehen. |
| 1 – Entwicklungsgrundlage | Reproduzierbare lokale Entwicklungsumgebung und CI; synthetische Fixtures; Verträge und erste kleine funktionsfähige Einheiten in VitaFabric und LifeLedger. Auswahl des ersten Clients nach Stufe 0. | Build, Lint, Unit- und negative Vertragstests laufen lokal und in CI. Fehlende Einwilligung und ungültige Daten werden abgewiesen; keine echten Gesundheitsdaten. |
| 2 – Erster vertikaler Durchstich | Offline im gewählten Client einen begrenzten synthetischen Gesundheitsdatensatz über VitaFabric erfassen, validieren, geschützt speichern und in LifeLedger anzeigen. Verschlüsselung, Zugriffskontrolle, Audit und Herkunft gemäß freigegebenen Spezifikationen; AI nicht erforderlich. | Ende-zu-Ende-Test ohne Netzwerk; FHIR-Validierung, Berechtigungs- und Einwilligungs-Negativfälle, falscher Schlüssel, Neustart sowie Locale/Zeitzone. Gate erst nach Security- und Architekturreview der implementierten Datenpfade. |
| 3 – Belastbarer lokaler Kern | Lebenszyklus, Änderung und Löschung, verschlüsselte Sicherung/Wiederherstellung, Interoperabilität und zugängliche Bedienung ausbauen. Weitere Clients erst auf gemeinsamen Verträgen aufsetzen. | Integrations-, Migrations-, Wiederherstellungs-, Fehler- und Zugänglichkeitstests; interoperabler FHIR-Test gegen dokumentierte Profile. Wiederherstellung darf keine unverschlüsselten Backups voraussetzen. |
| 4 – Erweiterbarkeit und Integrationen | Freigegebene Plugin-Verträge und lokale Entwicklungswerkzeuge; synthetischer Referenz-Connector, anschließend eine nach Review ausgewählte optionale Integration. Abhängig von Stufen 0–3 und [Plugin-Roadmap](plugins.md). | Unabhängig entwickeltes Plugin gegen versioniertes SDK und Konformitätssuite; Consent-/Isolations-, Fehler-, Upgrade- und Offline-Tests. Gesundheitsdaten weiterhin ausschließlich über VitaFabric. |
| 5 – Optionale Intelligenz | LifeWeaver lokal und providerneutral; MCP und ggf. externe Provider nur über explizit freigegebene Grenzen. Abhängig von Daten-, Sicherheits- und Einwilligungsverträgen. | Tests für verweigerten/widerrufenen Zugriff, Datenminimierung, Providerwechsel, lokale Nutzung und MCP-Kompatibilität; Sicherheits- und Zweckbestimmungsreview vor Nutzerfreigabe. |
| 6 – Freigabe und nachhaltiger Ausbau | Erst nach vollständigem Scope- und Risikoreview: unterstützte Plattformen, Dokumentation, Support, sichere Updates und Betriebsmodell veröffentlichen. Danach weitere Produktbereiche und Integrationen inkrementell. | Dokumentierte Bedrohungs- und Datenschutzprüfung, externe Sicherheitsprüfung nach vereinbartem Umfang, behobene Freigabeblocker, Recovery-Übung, Barrierefreiheits- und Lokalisierungsprüfung, dokumentierte Restrisiken und explizite Freigabe. Kein Einsatz echter Daten vor diesem Gate. |

## Übergreifende Teststrategie

Ab der ersten ausführbaren Komponente gehört zu jeder Änderung eine passende
automatisierte Prüfung: Unit-Tests, komponentenübergreifende Vertragstests und
gezielte Ende-zu-Ende-Tests. Sicherheits- und Einwilligungsfälle testen auch
Verweigerung, Widerruf, Fehler und Umgehungsversuche; FHIR-Fälle sowohl gültige
als auch ungültige Beispiele. Testdaten sind synthetisch und enthalten weder
Geheimnisse noch echte Gesundheitsdaten. Plugin-Suite und Regressionstests
laufen mit unterstützten Vertragsversionen. Tests, Tooling und Freigabeergebnisse
werden mit konkreten Kommandos dokumentiert, sobald sie existieren.

## Koordination

- [LifeLedger](lifeledger.md): Produktabläufe, Backend und Web-, Mobile- und Desktop-Clients.
- [VitaFabric](vitafabric.md): Datenzugang, FHIR, Provenienz, Speicherung und Connectoren.
- [LifeWeaver](lifeweaver.md): optionale AI, Agenten und MCP.
- [Plugins](plugins.md): herstellerneutrale Community-Verträge und Vertrauensmodell.
- [Integrationen](integrations.md): externe Systeme einschließlich Home Assistant.

## Vor Entwicklung zu entscheiden

1. Wer ist die erste Zielgruppe und welcher konkrete lokale Arbeitsablauf
   definiert den kleinsten wertvollen Durchstich?
2. Welches Gerät und welcher Client werden zuerst unterstützt, und welches
   lokale Laufzeit- und Speichermodell ist dafür praktikabel?
3. Wie werden Rollen, persönliche und familiäre Daten, Einwilligung und
   Widerruf rechtlich und technisch modelliert? Wer gibt das Modell frei?
4. Welche FHIR-R4-Ressourcen, Profile und Datenarten gelten zuerst, und wie
   werden manuelle Eingaben und Dokumente mit Herkunft erfasst?
5. Welche Sicherheits- und regulatorischen Voraussetzungen gelten vor einem
   Einsatz mit realen Daten? Wer verantwortet Freigabe und Incident Response?
6. Wie werden Community-Entscheidungen, Finanzierung, Wartung und Übersetzungen
   langfristig getragen?
