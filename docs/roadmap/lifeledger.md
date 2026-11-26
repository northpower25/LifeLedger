# Roadmap: LifeLedger

LifeLedger umfasst persönliche Gesundheitsakte, Timeline, Dokumente, Familie,
Medikamente und Clients. Diese Funktionen sind geplant, nicht implementiert.
Alle Gesundheitsdatenzugriffe laufen über VitaFabric; FHIR-Mapping, Connectoren
und AI-Provider gehören nicht in LifeLedger. Die
[Gesamt-Roadmap](project.md) definiert gemeinsame Gates.

## Stufen

| Stufe | Ergebnis und Abhängigkeiten | Tests und Abnahme |
| --- | --- | --- |
| L0 – Produkt- und Clientkonzept | Zielgruppe, erste Nutzerreise, Zugänglichkeit, Sprach- und Zeitzonenverhalten sowie Bedrohungsmodell definieren. Ersten Client und Technologieentscheidungen gemeinsam mit lokaler Laufzeit und VitaFabric-Vertrag per RFC/ADR klären. | Review anhand konkreter Akzeptanzfälle, einschließlich Offline, Hilfsmittel und Einwilligung. |
| L1 – Dünne lokale Anwendung | Ein Backend bzw. eine lokale Anwendung und ein ausgewählter Client nutzen versionierte VitaFabric-Verträge für einen synthetischen Datensatz; keine direkte Gesundheitsdatenbank oder Mapping-Logik im Client. | Unit- und Vertragstests; ungültige Eingaben und verweigerte Rechte sichtbar behandeln; lokalisierte Bedienung in Deutsch und Englisch prüfen. |
| L2 – Timeline-Durchstich | Nach freigegebenen Sicherheits- und Datenspezifikationen Erfassung, Lesen und Anzeige eines begrenzten FHIR-basierten Datentyps offline; Herkunft und Freigabestatus verständlich darstellen. | E2E über Client und VitaFabric, Offline-Neustart, Rollen-/Consent-Negativfälle, Zeitzonen und Barrierefreiheit. Sicherheits-Gate aus Stufe 2 der Gesamt-Roadmap. |
| L3 – Nutzbarer Kern | Dokumente, Medikations- und Familienfunktionen einzeln priorisieren; für jeden Bereich Datenmodell, Rechte und Risiken vor Implementierung spezifizieren. Geschützte Sicherung und Wiederherstellung über vereinbarte Datenverträge anbinden. | Pro Bereich FHIR-, Integrations-, Berechtigungs- und Migrationstests; Recovery- und Löschtests, inklusive gemeinsam genutzter Daten und Widerruf. |
| L4 – Weitere Clients | Web, Mobile und Desktop inkrementell ergänzen, nicht automatisch parallel; gemeinsame Verträge und konsistente Bedienung, lokale Laufzeit und plattformspezifische Sicherheitsgrenzen dokumentieren. | Für jeden Client Offline-, Installations-, Update-, Accessibility-, Lokalisierungs- und E2E-Tests auf den tatsächlich unterstützten Plattformen. |
| L5 – Erweiterte Abläufe | Notfallprofile, Datenfreigabe und optionale LifeWeaver-Funktionen erst nach eigener Risiko-, Einwilligungs- und Zweckbestimmungsprüfung. | Szenarien für minimale Freigabe, Ablehnung, Widerruf und Fehler; medizinische Fehlinterpretation und Datenabfluss in Review und Tests berücksichtigen. |

## Teilbereiche und offene Entscheidungen

- **Backend:** Läuft es lokal als Dienst, eingebettet oder in anderer Form?
  Wie werden Zugriff und Authentifizierung zwischen Prozessgrenzen geschützt?
  Die genannten Backend-Technologien sind noch nicht als ADR nachgewiesen.
- **Web:** Wie ist lokaler Betrieb ohne verpflichtenden Remote-Server und ohne
  unsichere Browser-Datenspeicherung möglich?
- **Mobile:** Welche Betriebssysteme, Offline-Grenzen, Schlüsselablage und
  Hintergrundausführung sind zuerst unterstützt? Die Architektur-Checkliste
  verlangt Flutter-Kompatibilität; ein begründetes Technologie-ADR fehlt.
- **Desktop:** Welche lokalen Zielplattformen, Update- und Schlüsselprozesse
  gelten? Tauri ist bisher Planung.
- **Produkt:** Welche Angaben gehören zum ersten Datensatz und wie werden
  Herkunft, Datenqualität und Fehler ohne medizinische Schlussfolgerung erklärt?
  Wie unterscheiden sich eigene Daten von Familien- oder Vertretungsdaten?
- **Inklusion:** Welche Accessibility-Zielnorm und Übersetzungsprozesse gelten?
  Sprachwechsel, Übersetzungen, Datumsformate, Zeitzonen und RTL sollen früh
  überprüft werden; der genaue RTL-Umfang ist zu entscheiden.

Vorschlag: Zuerst eine kleine vollständige Nutzerreise statt paralleler
Oberflächen entwickeln; Schnittstellenstabilität und Bedienbarkeit vor
zusätzlichen Datendomänen nachweisen.
