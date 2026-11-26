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

## Plattformperspektive und Deployment

Die Gesundheitsakte ist als erste Referenzanwendung einer erweiterbaren
Plattform vorgeschlagen. Draft [RFC-0002](../../rfc/RFC-0002%20Platform%20Core%20Architecture)
beschreibt einen Core Runtime mit Identity & Consent, Security Services,
Event Bus, Plugin Host, Secret Store und Audit Service. Er schlägt explizite,
technisch durchzusetzende Capabilities und WASM First als Plugin-Runtime vor;
der Core Runtime soll keine Geschäftslogik, Gesundheitsmodelle oder AI
enthalten. Diese Entscheidungen sind noch nicht angenommen oder implementiert.
Authentifizierung, Autorisierung und Consent sind getrennte Belange;
Ownership, Richtlinien, Verträge und Durchsetzung an den Datenzugriffen sind
vor Umsetzung zu reviewen. VitaFabric und LifeWeaver behalten ihre
verbindlichen Daten- bzw. AI-Verantwortungen. Der
[Plattform-RFC](../../rfc/0001-platform-direction.md) und der
[ADR](../../adr/0002-platform-direction.md) sind noch nicht angenommen.

| Szenario | Planung und zusätzliches Gate |
| --- | --- |
| Nur lokal | Grundlage für alle Kernfunktionen; Offline-E2E-Nachweis ab Stufe 2. |
| Lokal + Relay | Optional nach Bedrohungsmodell und Review von Metadaten, Identität, Remote-Zugriff und Einwilligung; keine Klartext-Gesundheitsdaten im Relay. |
| Lokal + Zero-Knowledge-Sync | Optional nach Spezifikation und Tests für Ende-zu-Ende-Verschlüsselung, Schlüsselverwaltung und -wiederherstellung, Metadaten, Konflikte, Widerruf und verschlüsselte Backups; Dienst erhält keine Entschlüsselungsschlüssel. |
| Managed Cloud | Nur als separat zu prüfende Option, nicht als Ersatz für lokale Funktion. Verarbeitung, Verantwortlichkeiten, Einwilligung, Datenstandort und Sicherheitsanforderungen benötigen vor Umsetzung und Freigabe eigenes Architektur-, Datenschutz- und Rechtsreview. |

Keines dieser Szenarien außer dem geplanten lokalen Kern ist Voraussetzung für
die erste Nutzerreise; keines ist bereits verfügbar. Reihenfolge und Aufwand
optionaler Szenarien sind nicht entschieden.

### Erweiterungen und Marketplace

Die Vision und RFC-0002 schlagen sechs Plugin-Typen vor: Connector,
Integration, Provider, Storage, UI und Application. Sie sind nach
Zuständigkeit zu trennen:
VitaFabric verantwortet Gesundheitsdaten-Connectoren, FHIR und kontrollierte
Storage-Adapter; LifeWeaver optionale AI-Provider; LifeLedger UI- und
Produktanwendungen. Integrationen dürfen keine Gesundheitsdaten direkt
speichern oder an VitaFabric vorbei übertragen. Eine Marketplace-Oberfläche
mit Community-, Verified- und Official-Listings ist eine Option für eine
spätere Ausbaustufe, keine Registry-/Cloud-Pflicht und keine Sicherheits- oder
Consent-Garantie. Community-, Verified- und Official-Einstufungen benötigen
vorher Kriterien, Governance und Umsetzungsnachweise. Storage-Adapter erhalten
laut RFC-0002 nur verschlüsselte Daten, niemals Klartext oder Schlüssel.

## Stufen und Gates

| Stufe | Ergebnis und Abhängigkeit | Nachweis bzw. Gate |
| --- | --- | --- |
| 0 – Richtung und Schutz | Zielgruppe, erste Referenzanwendung, Plattformgrenzen und Verantwortlichkeiten für Core Runtime, Identity & Consent, Sicherheit und Plugins; Bedrohungsmodell, Rollen-/Consent-Modell, lokale Laufzeit, Deployment-Szenarien sowie FHIR- und Plugin-Verträge. | Authentifizierung, Autorisierung, Consent, Notfallzugriff und Widerruf getrennt spezifiziert; Datenzugriffsgrenzen, Annahmen und Blocker geprüft; benötigte ADRs akzeptiert und Spezifikationen versioniert, bevor entsprechende Funktionen entstehen. |
| 1 – Entwicklungsgrundlage | Reproduzierbare lokale Entwicklungsumgebung und CI; synthetische Fixtures; Verträge und kleine, testbare Einheiten für VitaFabric, LifeLedger und die spezifizierten Identitäts-/Consent-Grenzen. Auswahl des ersten Clients nach Stufe 0. | Build, Lint, Unit- und negative Vertragstests laufen lokal und in CI. Fehlende Consent-Freigabe, widerrufene Rechte und ungültige Daten werden abgewiesen; keine echten Gesundheitsdaten. |
| 2 – Erster vertikaler Durchstich | Offline im gewählten Client einen begrenzten synthetischen Gesundheitsdatensatz über VitaFabric erfassen, validieren, geschützt speichern und in der Referenzanwendung anzeigen. Identität, Rollen, Consent, Verschlüsselung, Zugriffskontrolle, Audit und Herkunft gemäß freigegebenen Spezifikationen; AI nicht erforderlich. | Ende-zu-Ende-Test ohne Netzwerk; FHIR-Validierung, Berechtigungs-, Notfallzugriffs- und Einwilligungs-Negativfälle, Widerruf, falscher Schlüssel, Neustart sowie Locale/Zeitzone. Gate erst nach Security- und Architekturreview der implementierten Datenpfade. |
| 3 – Belastbarer lokaler Kern | Lebenszyklus, Änderung und Löschung, verschlüsselte lokale Sicherung/Wiederherstellung, Interoperabilität und zugängliche Bedienung ausbauen. Weitere Clients erst auf gemeinsamen Verträgen aufsetzen; optionale Deployment-Szenarien getrennt prüfen. | Integrations-, Migrations-, Wiederherstellungs-, Fehler- und Zugänglichkeitstests; interoperabler FHIR-Test gegen dokumentierte Profile. Wiederherstellung darf keine unverschlüsselten Backups voraussetzen. |
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
3. Wie werden Nutzer, Familienmitglieder, Vertreter, Rollen, Notfallzugriff,
   Einwilligung und Widerruf rechtlich und technisch modelliert? Wer gibt das
   Modell frei und darf welche Freigaben erteilen?
4. Welche FHIR-R4-Ressourcen, Profile und Datenarten gelten zuerst, und wie
   werden manuelle Eingaben und Dokumente mit Herkunft erfasst?
5. Welche Sicherheits- und regulatorischen Voraussetzungen gelten vor einem
   Einsatz mit realen Daten? Wer verantwortet Freigabe und Incident Response?
6. Wie werden Community-Entscheidungen, Finanzierung, Wartung und Übersetzungen
   langfristig getragen?
7. Welche gemeinsamen Fähigkeiten und Vertrauensgrenzen braucht die Plattform
   tatsächlich, und wo liegen deren Ownership und technische Durchsetzung?
8. Welche Kriterien, Verantwortlichen und Einspruchswege sollen Community-,
   Verified- und Official-Marketplace-Listings definieren?
9. Welche optionalen Deployment-Szenarien sind mit lokalen Alternativen,
    Einwilligung, Schlüsselbesitz und regulatorischen Pflichten vereinbar?
