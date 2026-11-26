# Bestandsaufnahme: Umsetzungsreife

Stand: Repository-Inhalt bei Erstellung dieser Roadmap. Die Bewertung betrifft
den eingecheckten Stand, nicht externe Planungen oder künftige Zusagen. Das
Repository ist ein Architektur-Grundgerüst, kein lauffähiges Produkt. Es ist
noch nicht ausreichend spezifiziert, um eine vollständige Implementierung oder
die Verarbeitung echter Gesundheitsdaten sicher zu beginnen. Vorbereitende
Spezifikations-, Prototyp- und Testarbeiten mit synthetischen Daten sind möglich.

## Befunde und Handlungsbedarf

| Bereich | Befund und Beleg | Vor Umsetzung klären bzw. erstellen |
| --- | --- | --- |
| Produkt und Umfang | [Vision](../product/Vision.md), [Personas](../product/Personas.md) und [Nichtziele](../product/NonGoals.md) beschreiben die Richtung, aber keine priorisierten Nutzerabläufe oder Abnahmekriterien. | Erste Zielgruppe, unterstützte Datentypen, lokales Installationsziel und Grenzen des ersten vertikalen Durchstichs festlegen. Medizinische Zweckbestimmung und regulatorische Prüfung vor erweiterten Funktionen klären. |
| Architektur und Verantwortung | [Architektur](../architecture/README.md) nennt die drei Systeme, aber noch keine Verträge, Datenflüsse, Laufzeit- oder Vertrauensgrenzen. [ADR 0001](../../adr/0001-project-principles.md) enthält Prinzipien, keine konkreten Schnittstellen. | RFC, Bedrohungsmodell und ADRs für Grenzen, Identität, Datenzugriff, Deployment und Erweiterungen; danach versionierte Spezifikationen. |
| Plattformfähigkeiten | Das Konzept schlägt einen Core Runtime, Identity & Consent, Plugin Host, Security Layer, Sync und Marketplace unter einer Plattform vor. Die Zuständigkeiten und Verträge dieser gemeinsam genutzten Fähigkeiten sind nicht beschlossen oder implementiert. | Plattform-RFC/ADR prüfen; Identität, Zustimmung, Rollen, Notfallzugriff und Rechtevergabe als getrennte, testbare Verantwortlichkeiten definieren. Keine Marketplace-Kennzeichnung oder Plugin-Manifest als Sicherheitsnachweis behandeln. |
| FHIR und Daten | Die Verzeichnisse unter [specifications](../../specifications/) sind überwiegend Platzhalter; Profile, Ressourcen, Validierung, Provenienz und Fehlerbehandlung sind nicht spezifiziert. | VitaFabric-Verträge für FHIR R4, Import, manuelle Eingaben, Dokumente, Datenqualität und Herkunft definieren; erst dann erste Datenflüsse implementieren. |
| Schutz und Einwilligung | [Sicherheit](../security/README.md) ist ein Platzhalter; Schlüsselverwaltung, Rollen, Einwilligung, Widerruf, Audit, Sicherung und Wiederherstellung sind ungeklärt. | Bedrohungsmodell und testbare Sicherheits- und Einwilligungsspezifikationen vor Datenverarbeitung und Plugin-Ausführung erstellen; echte Gesundheitsdaten bis zur entsprechenden Freigabe ausschließen. |
| Lokalbetrieb und Technologien | [Backend](../../backend/README.md) nennt Python/FastAPI und PostgreSQL/TimescaleDB; [Mobile](../../frontend-mobile/README.md) Flutter, Desktop Tauri, Web React/TypeScript/Tailwind. Das sind Platzhalter, keine dokumentierten Technologieentscheidungen oder lauffähigen Setups. PostgreSQL im Backend belegt für sich keinen einfachen Offline-Einzelgerätebetrieb. | Anforderungen und Alternativen für lokale Laufzeit, Speicher, Zielplattformen und Betriebsaufwand vergleichen; Auswahl und Migrationspfad per ADR dokumentieren. Keine Cloud voraussetzen. |
| Erweiterbarkeit | [Plugins](../../plugins/README.md), [Connector-Spezifikation](../../specifications/connectors/README.md) und [Integrationen](../../integrations/homeassistant/README.md) sind noch keine ausführbaren Verträge. Sechs Plugin-Typen und Marketplace-Kennzeichnungen sind vorgeschlagen, nicht implementiert oder freigegeben. | Plugin-RFC mit getrennten VitaFabric-/LifeWeaver-/LifeLedger-Verträgen, technisch erzwungenen Fähigkeiten, Consent, Isolation, Provenienz und Konformität; synthetischen unabhängigen Nachweis erbringen. Siehe [Plugin-Roadmap](plugins.md). |
| AI und MCP | [LifeWeaver](../../platform/lifeweaver/README.md), [MCP](../../specifications/mcp/README.md) und Agenten-Spezifikationen beschreiben keine ausführbaren Verträge oder Sicherheitsgrenzen. | Lokale providerneutrale Schnittstellen, Datenfreigabe, MCP-Versionierung, Risiken und Widerruf spezifizieren; AI bleibt für den Kern optional. |
| Qualität und Betrieb | [tests](../../tests/README.md) ist ein Platzhalter. Die [CI](../../.github/workflows/repository.yml) prüft lediglich vorhandene Bootstrap-Dateien; es gibt keine Produkt-, Sicherheits- oder FHIR-Tests. [SECURITY.md](../../SECURITY.md) nennt noch keine unterstützten Releases oder garantierten Reaktionszeiten. | Teststrategie, ausführbare CI, Release- und Supportprozess sowie Sicherheitsprüfung schrittweise etablieren; keine Konformität oder Produktionsreife aus dem Strukturcheck ableiten. |
| Internationalisierung und Barrierefreiheit | Produktdokumente fordern Deutsch und Englisch auch für Dokumentation, aber der aktuelle Bestand ist überwiegend englisch; die [mobile Strategie](../mobile/Multilanguage_Strategy.md) ist nur eine Stichwortliste. Ein Barrierefreiheitsstandard fehlt. | Übersetzungsumfang und Pflegeprozess, Ressourcen und Sprachwechsel, Locale/Zeitzonen sowie zugängliche Bedienung für alle Clients spezifizieren und testen. |
| Community und Lizenz | [Governance](../governance/README.md) legt zunächst Maintainer-Verantwortung fest; [USP](../product/USP.md) formuliert Community-Governance als Ziel. Die Plugin-Lizenz- und Verteilungspraxis ist nicht beschrieben; das Repository steht unter [AGPL-3.0-only](../../LICENSE). | Ziel-Governance nicht mit bereits umgesetzter Mitbestimmung verwechseln. Lizenzierung, Distribution, Review, Support und Sicherheitsmeldungen für Drittanbieter mit fachlicher Rechtsprüfung klären. |
| Dokumentationspflege | Die [Repository-Baumdarstellung](../tree.md) ist nicht aktuell: Unter anderem fehlen ADR 0001, Produktdokumente und die neuen Roadmaps. | Automatisch erzeugte oder überprüfte Bestandsübersicht und Pflegeverantwortung vereinbaren; den Baum bis dahin nicht als vollständiges Inventar verwenden. |

## Spannungen und Präzisierungen

- Die vollständige [Plattformvision](https://github.com/northpower25/LifeLedger/blob/main/docs/concept)
  schlägt die Gesundheitsakte als erste Referenzanwendung, Identity & Consent,
  sechs Plugin-Typen, einen Marketplace mit Community/Verified/Official-Listings
  und vier Deployment-Modi vor. Diese Fähigkeiten und Labels sind nicht
  implementiert oder beschlossen. Insbesondere definieren die Beispiele keine
  Berechtigungsrichtlinie, Isolation oder Sicherheitsgarantie. Der
  [RFC](../../rfc/0001-platform-direction.md) und das
  [ADR](../../adr/0002-platform-direction.md) erfassen die Vorschläge und
  offenen Fragen zur Prüfung.
- Integrations-Ownership betrifft Koordination und Lebenszyklus, nicht die
  Implementierungsgrenze: Connector-Ausführung, FHIR-Mapping und
  Gesundheitsdatenzugriff gehören zu VitaFabric. Jeder Plugin-Typ braucht
  dieselbe klare Verantwortungsgrenze; Implementierungen dürfen keine
  Gesundheitsdaten an VitaFabric vorbei speichern oder verarbeiten.
- Die Vision nennt einen Health Twin und AI-Insights, die
  [Nichtziele](../product/NonGoals.md) schließen Diagnose, Therapieempfehlung
  und klinische Entscheidungen aus. Funktionsgrenzen, Kommunikation und
  regulatorische Bewertung müssen vor solchen Funktionen geklärt werden;
  ein Hinweistext allein ist keine Sicherheitsmaßnahme.
- Die [Strukturprüfung](../architecture/repository_validation.md) bewertet
  Verzeichnisse und Dokumentation nach der Migration, nicht die Vollständigkeit
  oder Umsetzung der Architektur. Insbesondere belegt „Future growth is
  supported“ keine technische Plugin-Fähigkeit.
- Die vier vorgeschlagenen Modi (Local Only, Local + Relay, Local +
  Zero-Knowledge Sync und Managed Cloud) sind Szenarien, keine Produkte oder
  genehmigten Verarbeitungsweisen. Relay-Metadaten bleiben sensibel;
  Zero-Knowledge benötigt überprüfte Schlüssel- und Wiederherstellungsverfahren;
  Managed Cloud bedarf eigenständiger Prüfung. Kein externes Plugin oder
  Modell darf Voraussetzung für eine lokale Kernfunktion sein.
- Die verbindliche [Architektur-Checkliste](../../.github/architecture_checklist.md)
  verlangt Flutter-Kompatibilität für Companion-Apps und MFA-Unterstützung;
  ein ADR zur Mobile-Technologiewahl bzw. ein MFA-Konzept fehlt. Die Checkliste
  fordert zugleich für jede Änderung Antworten auf nicht immer anwendbare
  Fragen. Anwendbarkeit und Technologieentscheidung müssen geklärt werden;
  fehlende Konzepte setzen bestehende Anforderungen nicht außer Kraft.

## Ergebnis für die Planung

Die Plattformvision ist konzeptionell breiter als der aktuelle
Komponentenrahmen; ein erweiterbares System ist **noch nicht nachgewiesen**.
Priorität haben Ownership und testbare Verträge für Identity & Consent,
VitaFabric-Datenpfade und jeden Plugin-Typ sowie ein kleiner, offline
testbarer vertikaler Durchstich. Die [Gesamt-Roadmap](project.md) führt die
Abhängigkeiten und Freigaben zusammen; die Komponenten-Roadmaps enthalten
ihre offenen Fragen.
