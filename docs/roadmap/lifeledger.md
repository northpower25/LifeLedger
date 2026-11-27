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
Freigaben unterstützen. Draft [RFC-0002](../../rfc/0002-platform-core-architecture.md)
ordnet Identity & Consent dem vorgeschlagenen Core Runtime zu; Richtlinien,
Verträge und technische Durchsetzung stehen noch zur Review. Die
Plattformneuausrichtung ist Gegenstand der
[RFCs](../../rfc/0001-platform-direction.md), keine akzeptierte Architektur.

## Stufen

| Stufe | Ergebnis und Abhängigkeiten | Tests und Abnahme |
| --- | --- | --- |
| L0 – Produkt- und Clientkonzept | Festgelegte Zielgruppe, erste Nutzerreise und Client-Technologien konkretisieren; Identitäts-/Consent-Anforderungen, Zugänglichkeit, Sprach- und Zeitzonenverhalten sowie Bedrohungsmodell und VitaFabric-Vertrag per RFC/ADR klären. | Review anhand konkreter Akzeptanzfälle, einschließlich Offline, Hilfsmittel, Familien-/Vertretungsrollen, Notfallzugriff und Consent-Widerruf. |
| L1 – Dünne lokale Anwendung | Ein Backend bzw. eine lokale Anwendung und ein ausgewählter Client nutzen versionierte VitaFabric-Verträge und die spezifizierten Identity-/Consent-Verträge für einen synthetischen Datensatz; keine direkte Gesundheitsdatenbank oder Mapping-Logik im Client. | Unit- und Vertragstests; ungültige Eingaben, fehlende/widerrufene Freigaben und abgelehnte Rechte sichtbar behandeln; lokalisierte Bedienung in Deutsch und Englisch prüfen. |
| L2 – Erster Offline-Durchstich | Nach geklärten Startbedingungen Patient, DocumentReference und MedicationStatement mit Dokumentimport, Timeline und Backup auf Windows offline erproben; Herkunft und Freigabestatus verständlich darstellen. Nur synthetische Daten. | E2E über Client, Identity/Consent und VitaFabric, Offline-Neustart, Consent-Negativfälle, Widerruf, Zeitzonen und Barrierefreiheit. Backup-Restore als Abnahmekriterium noch bestätigen. |
| L3 – Nutzbarer Kern | Ersten Durchstich um belastbare Datenverträge, Bedienbarkeit und Wiederherstellung erweitern; Familienfunktionen separat priorisieren. | Pro Bereich FHIR-, Integrations-, Berechtigungs- und Migrationstests; Recovery- und Löschtests, inklusive gemeinsam genutzter Daten und Widerruf. |
| L4 – Weitere Clients | Web, Mobile und Desktop inkrementell ergänzen, nicht automatisch parallel; gemeinsame Verträge und konsistente Bedienung, lokale Laufzeit und plattformspezifische Sicherheitsgrenzen dokumentieren. | Für jeden Client Offline-, Installations-, Update-, Accessibility-, Lokalisierungs- und E2E-Tests auf den tatsächlich unterstützten Plattformen. |
| L5 – Erweiterte Abläufe | Notfallprofile, Datenfreigabe und optionale LifeWeaver-Funktionen erst nach eigener Risiko-, Einwilligungs- und Zweckbestimmungsprüfung. | Szenarien für minimale Freigabe, Ablehnung, Widerruf und Fehler; medizinische Fehlinterpretation und Datenabfluss in Review und Tests berücksichtigen. |

## Teilbereiche und offene Entscheidungen

- **Backend:** Vorgesehen ist ein lokaler FastAPI-Dienst eingebettet in
  Tauri. Wie werden dessen Lebenszyklus, Zugriff und Authentifizierung
  zwischen Prozessgrenzen geschützt? Ein akzeptiertes ADR fehlt.
- **Web:** Wie ist lokaler Betrieb ohne verpflichtenden Remote-Server und ohne
  unsichere Browser-Datenspeicherung möglich?
- **Mobile:** Welche Betriebssysteme, Offline-Grenzen, Schlüsselablage und
  Hintergrundausführung sind zuerst unterstützt? Flutter ist vorgesehen;
  ein akzeptiertes Technologie-ADR fehlt.
- **Desktop:** Tauri und Windows First sind vorgesehen, danach Linux und
  macOS. Welche Update- und Schlüsselprozesse gelten?
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

Die erste Nutzerreise umfasst Arztbriefimport, Medikationserfassung, Timeline
und Backup. Schnittstellenstabilität und Bedienbarkeit sollen vor zusätzlichen
Datendomänen nachgewiesen werden.
