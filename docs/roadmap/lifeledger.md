# Roadmap: LifeLedger

LifeLedger umfasst persönliche Gesundheitsakte, Timeline, Dokumente, Familie,
Medikamente und Clients. Diese Funktionen sind geplant, nicht implementiert.
Alle Gesundheitsdatenzugriffe laufen über VitaFabric; FHIR-Mapping, Connectoren
und AI-Provider gehören nicht in LifeLedger. Die
[Gesamt-Roadmap](project.md) definiert gemeinsame Gates.
Die persönliche Gesundheitsakte ist als erste Plattform-Referenzanwendung
vorgesehen; weitere Anwendungen sind erst nach bestätigten Verträgen und
Nutzerbedarf zu priorisieren. Gemeinsame Identitäts- und Consent-Funktionen
sollen Nutzer, Familienmitglieder, Vertreter und app-/pluginbezogene
Freigaben unterstützen; Zuständigkeit, Richtlinien und technische Durchsetzung
stehen noch zur Entscheidung. Die Plattformneuausrichtung ist Gegenstand des
[RFCs](../../rfc/0001-platform-direction.md), keine akzeptierte Architektur.

## Stufen

| Stufe | Ergebnis und Abhängigkeiten | Tests und Abnahme |
| --- | --- | --- |
| L0 – Produkt- und Clientkonzept | Zielgruppe, erste Nutzerreise, Identitäts-/Consent-Anforderungen, Zugänglichkeit, Sprach- und Zeitzonenverhalten sowie Bedrohungsmodell definieren. Ersten Client und Technologieentscheidungen gemeinsam mit lokaler Laufzeit und VitaFabric-Vertrag per RFC/ADR klären. | Review anhand konkreter Akzeptanzfälle, einschließlich Offline, Hilfsmittel, Familien-/Vertretungsrollen, Notfallzugriff und Consent-Widerruf. |
| L1 – Dünne lokale Anwendung | Ein Backend bzw. eine lokale Anwendung und ein ausgewählter Client nutzen versionierte VitaFabric-Verträge und die spezifizierten Identity-/Consent-Verträge für einen synthetischen Datensatz; keine direkte Gesundheitsdatenbank oder Mapping-Logik im Client. | Unit- und Vertragstests; ungültige Eingaben, fehlende/widerrufene Freigaben und abgelehnte Rechte sichtbar behandeln; lokalisierte Bedienung in Deutsch und Englisch prüfen. |
| L2 – Timeline-Durchstich | Nach freigegebenen Sicherheits- und Datenspezifikationen Erfassung, Lesen und Anzeige eines begrenzten FHIR-basierten Datentyps offline; Herkunft, Datenzugriff und Freigabestatus verständlich darstellen. | E2E über Client, Identity/Consent und VitaFabric, Offline-Neustart, Rollen-/Consent-Negativfälle, Widerruf, Zeitzonen und Barrierefreiheit. Sicherheits-Gate aus Stufe 2 der Gesamt-Roadmap. |
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
- **Identität und Consent:** Wie werden Konten, Familienmitglieder, Vertreter,
  Rollen, Freigaben und Notfallzugriff getrennt modelliert? Welche Oberfläche
  lässt Nutzer Rechte pro App oder Plugin nachvollziehen und widerrufen?
- **Referenzanwendung:** Welche Abläufe gehören zur ersten Anwendung und welche
  wiederverwendbaren Fähigkeiten müssen über gemeinsame Verträge bereitstehen?
  Wie bleiben Ablehnung und Widerruf in allen Anwendungen verständlich?
- **Inklusion:** Welche Accessibility-Zielnorm und Übersetzungsprozesse gelten?
  Sprachwechsel, Übersetzungen, Datumsformate, Zeitzonen und RTL sollen früh
  überprüft werden; der genaue RTL-Umfang ist zu entscheiden.

Vorschlag: Zuerst eine kleine vollständige Nutzerreise statt paralleler
Oberflächen entwickeln; Schnittstellenstabilität und Bedienbarkeit vor
zusätzlichen Datendomänen nachweisen.
