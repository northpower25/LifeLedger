# Offene Informationen und Startfreigabe für die erste Testversion

**Stand:** 27.11.2026, Abgleich mit dem
[RFC-Backlog](LifeLedger%20RFC%20Backlog.md). **Ergebnis: Noch keine
Startfreigabe.** Die Slice-Richtung ist jetzt vorgegeben, aber mehrere
Backlog-Aufträge sind nur teilweise konkretisiert. Die RFCs bleiben Entwürfe,
keine angenommenen Entscheidungen oder ausführbaren Verträge. Diese Bewertung ersetzt nicht den
[ursprünglichen Review](rfc-implementierungsreife-und-repository-review.md),
sondern konkretisiert dessen verbleibende Punkte.

Das frühere [V2-Gate](rfc-open-questions-resolution-V2.md) verlangt zusätzlich
akzeptiertes RFC-0014 und vollständige RFCs 0015–0019; der Backlog nennt deren
Existenz und P0/P1, hebt das V2-Gate aber nicht ausdrücklich auf. Welches Gate
maßgeblich ist, muss entschieden werden. Isolierte Machbarkeitsversuche mit
synthetischen Daten erfüllen das strengere V2-Gate nicht.
Für echte Gesundheitsdaten, produktive Nutzung und externe Freigabe gelten
zusätzliche unabhängige Sicherheits-, Datenschutz- und Rechtsprüfungen. Bis
dahin ausschließlich synthetische Daten, auch für Logs, Dokumente, Backups und
Fixtures.

## Benötigte Entscheidungen des Projekteigentümers

Diese Punkte benötigen eine ausdrückliche Entscheidung oder benannte
Entscheidungsinstanz; technische Ausarbeitung allein kann sie nicht ersetzen.
Vorschläge sind keine Vorwegnahme einer Freigabe.

| Nr. | Benötigte Information / Entscheidung | Warum vor Start |
| --- | --- | --- |
| 1 | Wer entscheidet über RFCs und ADRs, prüft Security und erteilt die dokumentierte Startfreigabe? Gilt weiterhin das strengere V2-Gate? | Der Backlog benennt Zuständigkeiten auf Teamebene, aber keine Personen oder Annahme von RFC-0014 und ADR-0002/-0003. |
| 2 | Erfolgreichen Backup-Restore als Abnahmekriterium bestätigen; Dokumenttypen und maximale Größen festlegen. | Festgelegt sind Windows, Tauri/FastAPI/SQLite, Patient, DocumentReference, MedicationStatement und Timeline; Observation ist nicht Teil dieses Slice. Backup ist gefordert, Restore-Erfolg nicht ausdrücklich genannt. |
| 3 | Architektur- und Sicherheitsreview sowie Annahme der integrierten Health-Record-Ausnahme in ADR-0003/RFC-0014 klären. Ist RFC-0019 trotz ausgeschlossener Plugins nach dem maßgeblichen Gate vollständig erforderlich? | Die integrierte Ausführung ist vorgegeben, die frühere Plugin-only-Grenze und das V2-Gate sind nicht automatisch angenommen oder aufgehoben. |
| 4 | Was bedeutet verpflichtendes offline MFA für den ersten lokalen Owner: Faktoren, Setup-Zeitpunkt, Verlust und Recovery? Welche Bedienbarkeit und welches Verhalten bei verlorenen Faktoren sind gewünscht? | RFC-0003 fordert Erst-MFA, nennt aber keinen implementierbaren Faktor oder Recovery-Pfad. Keine implizite Abschwächung. |
| 5 | Welche konkreten Windows-Versionen und Referenzgeräte sowie akzeptablen Grenzen für Startzeit, RAM, Importgröße, Validierungsdauer und Backup-/Restore-Zeit gelten? | Tauri, FastAPI, Validator, Verschlüsselung, Audit und gegebenenfalls Wasmtime verursachen messbare Last. Ohne Messziele keine reproduzierbare Abnahme. |
| 6 | Welche Fristen und Verantwortlichen gelten für Audit, Events, Quarantäne und Backup, insbesondere Löschung und Wiederherstellung? | Datenschutz, Speicherbedarf und Löschgarantien hängen davon ab; Fristen dürfen nicht erfunden werden. |
| 7 | Wer übernimmt die fachliche und rechtliche Prüfung von Familien-/Guardian-Regeln und die Freigabe von Terminologielizenzen? | Rechtsordnungen und Lizenzrechte können nicht aus der technischen Architektur abgeleitet werden. Familienfunktionen gehören nicht zur festgelegten ersten Nutzerreise; sie dürfen ohne diese Prüfung nicht freigegeben werden. |

## Abgleich mit dem Backlog

„Teilweise“ bedeutet, dass der angeforderte Abschnitt existiert, aber die
geforderte Entscheidung oder eine ausführbare Konkretisierung noch fehlt.
Die Einträge sind keine Annahme der RFCs.

| Auftrag | Stand und verbleibende Arbeit |
| --- | --- |
| RFC1-01/02 | Umfang und Teamrollen in RFC-0001 übernommen; konkrete Personen und Freigabeinstanzen fehlen. |
| RFC2-01/02/03 | Topologie, Vertrauensgrenzen und korrekte Folgereferenzen in RFC-0002 dokumentiert; IPC, Authentisierung, Packaging und Schutz gegen Prozesse desselben Nutzers offen. |
| RFC3-01/03 | Zustandsautomat und Consent-Felder in RFC-0003 dokumentiert; ausführbares Schema und Schnittstellen fehlen. |
| RFC3-02/04 | Bootstrap-Reihenfolge und Widerrufsverhalten dokumentiert; Recovery-Key-Verfahren, MFA und Abbruchgrenzen fehlen. |
| RFC4-01–03 | Prüfreihenfolge, Lifecycle und Owner-Regeln in RFC-0004 dokumentiert; vollständige Policy-/Capability-Matrix fehlt. |
| RFC5-01/03 | At-least-once und sechs Slice-Events in RFC-0005 festgelegt; Schemas, Consumer und Betriebsparameter fehlen. |
| RFC5-02 | Kategorien und Grundregeln dokumentiert; Aufbewahrungsfristen, Archivierung und Löschung sind nicht entschieden. |
| RFC6-01–03 | WIT-Katalog, Budgetprinzipien und Host-Matrix in RFC-0006 dokumentiert; echte WIT-Definitionen, Zahlen und Plattformnachweise fehlen. Plugins sind nicht im Slice. |
| RFC7-01–03 | Integrierter Health Record, Nutzerreise und Backup-Scope in RFC-0007 dokumentiert; ADR-0003 ist proposed, Restore- und Schlüsselvertrag offen. |
| RFC8-01–03 | Guardian-Prüfung und Altersübergang in RFC-0008 skizziert, Notfallfelder mit RFC-0003 harmonisiert; Rechtsprüfung und konkrete Verfahren fehlen. |
| RFC9-01–03 | Rotation und Offline-Verhalten in RFC-0009 skizziert; jede Paketänderung erfordert neuen Digest und neue Signatur. Trust-Bootstrap und Offline-Weiterbetrieb bleiben offen. |
| RFC-0015–0019 | Alle existieren als Entwürfe; Existenz erfüllt das Backlog-Kriterium, nicht die Vollständigkeit des V2-Gates. |
| P2: RFC-0010–0012 | Nicht Gegenstand der P0/P1-Startbedingung; Sync/AI bleiben außerhalb des Slice. Betriebsverantwortliche und Auditfristen bleiben auch für den lokalen Kern zu klären. |

## Vor Programmierung zu erstellende und zu prüfende Artefakte

Diese Aufgaben können nach den Entscheidungen technisch ausgearbeitet werden;
sie sind nicht sämtlich zusätzliche Fragen an den Projekteigentümer. Die
Reviewenden und die Abnahmekriterien müssen aber benannt sein.

1. **End-to-End-Sicherheits- und Bedrohungsmodell:** Sequenzen für
   Bootstrap/MFA, Unlock, Import, Lesen, Widerruf, Neustart, Backup und
   Restore; Angreifer und Same-User-Grenze, Audit-Ausfall, gleichzeitiger
   Widerruf und Zugriff sowie Folgen bereits ausgelieferter Daten.
2. **Lokale Runtime und Storage:** verbindlicher Windows-IPC-Mechanismus mit
   gegenseitiger Prozessauthentisierung und Mehrfachstartschutz; exakte
   Tauri-/FastAPI-Paketierung, sichere Kanalübergabe und Update-/Shutdown-
   Semantik. Verschlüsselungsverfahren und Schlüsselhierarchie für SQLite,
   WAL, Indizes, temporäre Dateien, Dokumente und Backups; Argon2-Parameter,
   AES-256-GCM-Nonce-/Integritätsmanagement, Passwortwechsel, Recovery,
   Transaktions- und Restore-Verhalten. Kein unverschlüsselter Fallback.
3. **Slice-Datenvertrag:** R4-Profile und erlaubte Felder, Referenzen,
   Versionierung, Dokumentoriginal, MIME-/Größen- und Integritätsprüfung;
   Provenienz einschließlich `MANUAL_ENTRY`, Quell-ID und Transformationen;
   Offline-Terminologie, exakt gepinnter HL7-Validator samt Paketen,
   Fehlerzuordnung und lauffähige positive/negative Fixtures.
4. **API und Zugriff:** OpenAPI 3.1 mit Request-/Response-Schemas,
   Authentisierung, vollständiger Capability-/Consent-/Policy-Matrix für
   Owner, Ressourcen, Import, Backup und gegebenenfalls Restore; Fehler, Idempotenz,
   Concurrency und Audit. Die Skizzen in RFC-0016/-0018 sind noch keine
   ausführbaren Schemata.
5. **Events und Audit:** tatsächliche Slice-Eventtypen, Registry und
   JSON-Schemas, Atomarität von Änderung/Audit/Outbox, Deduplizierung,
   Reihenfolge, Wiederanlauf, DLQ und sichere Retention samt Lösch-/
   Restore-Strategie. Widerruf darf nicht von einem Event abhängen.
6. **Plugin-Vertrag gemäß V2, falls dieses Gate weiter gilt:** maschinenlesbare Manifest-/Permission-Schemas,
   eindeutiges Paket- und Signaturformat, vollständige versionierte WIT-
   Definitionen, Host-Fehler, Ressourcenlimits, SDK-Vertrag und unabhängig
   ausführbare Compliance-Fixtures. Vorliegende Tabellen sind keine WIT-
   Schnittstellen und keine Compliance-Suite. Auch falls der Slice keine
   Plugins ausführt, fordert V2 ausdrücklich ein vollständiges RFC-0019.
7. **Abnahme und Machbarkeit:** synthetische Ende-zu-Ende-Fälle für Setup,
   Import, ungültige Daten, Lesen, verweigerten und widerrufenen Zugriff,
   Audit-/Policy-Ausfall, parallelen Widerruf, falsches Credential, Neustart,
   Offline-Betrieb und, falls bestätigt, Backup-Restore. Messverfahren und Schwellen aus Nr. 5
   dokumentieren; technisch relevante Abhängigkeiten und deren Lizenzen
   inklusive Windows-Verfügbarkeit prüfen.

## Abgleich mit den V2-Arbeitsaufträgen

| Auftrag | Bearbeiteter Entwurf | Rest bis zum V2-Gate |
| --- | --- | --- |
| A-001 | [RFC-0002](../../rfc/0002-platform-core-architecture.md): Topologie, Start, Ende, Fehler, Grenzen | IPC- und Storage-Technik, Bedrohungsmodell und Nachweis fehlen. |
| A-002–003 | [RFC-0003](../../rfc/0003-identity-and-consent-framework.md): Consent-Automat, Zuständigkeit, Bootstrap | MFA, Recovery, konkrete API-/Policy- und Race-Verträge fehlen. |
| A-004–005 | [RFC-0013](../../rfc/0013-vitafabric-data-contracts-and-fhir-governance.md): sechs Typen, Reject/Warn/Quarantine | Profile, Validator, Fehlerzuordnung und Quarantäneparameter fehlen. |
| B-001–004 | [RFC-0004](../../rfc/0004-capability-and-permission-model.md), [RFC-0005](../../rfc/0005-event-bus-architecture.md): Prüfung, Lebenszyklus, Zustellung, Retention | konkrete Kataloge, Eventschemas, Fristen und Limits fehlen. |
| C-001–003 | [RFC-0006](../../rfc/0006-plugin-runtime-and-isolation.md), [RFC-0019](../../rfc/0019-plugin-apis-and-sdk-contracts.md): WIT-Katalog, Limits und Paket-/SDK-Rahmen | WIT, ausführbare Schemas, Limits und Compliance-Suite fehlen; RFC-0019 ist nicht vollständig. |
| D-001–003 | [RFC-0008](../../rfc/0008-family-and-delegation-model.md): Prüfung, Rechtsräume und Übergang | konkrete rechtliche Regeln und verifizierbares Verfahren fehlen. |
| E-001–003 | [RFC-0011](../../rfc/0011-ai-provider-framework-and-health-twin-architecture.md): Retention und lokale Voraussetzungen | Modell, Ressourcenwerte, Provider- und Löschverträge fehlen. |
| F-001–004 | [RFC-0009](../../rfc/0009-marketplace-governance-and-trust-framework.md), [RFC-0012](../../rfc/0012-sustainability-governance-and-operations.md): Rotation, Offline-Vertrauen, Nachfolge und Eskalation | Schlüsselprotokoll, Verantwortliche, Quoren und Betriebsfristen fehlen. |
| G | [RFC-0015](../../rfc/0015-fhir-profiles-and-terminology-governance.md) bis [RFC-0019](../../rfc/0019-plugin-apis-and-sdk-contracts.md): Vertragsrahmen und Negativfälle | Profile, OpenAPI, Event-/Manifest-Schemas, WIT und Fixtures fehlen. Keiner dieser RFCs ist nach V2 vollständig. |

**Schlussfolgerung:** Die Planungsbreite deckt die verlangten Themen jetzt
als Entwurf ab, die Planungstiefe reicht für den verlangten Start noch nicht.
Insbesondere sind RFC-0014 nicht akzeptiert, RFC-0015–0019 nicht vollständig,
Phase A nicht abgeschlossen und die Review-Blocker nicht geschlossen. Der
synthetische Slice ist in seinem Produktumfang festgelegt; Security-/Consent-Flows
sind aber nicht abschließend beschlossen und ausführbar spezifiziert. Diese Punkte
dürfen nicht als erledigt markiert werden.

Erneute Zugriffskontrolle, Offline-Validierung, Verschlüsselung, Audit und
Isolation kosten Zeit und Speicher; kurze Retention oder strenge Offline-
Sperrlisten können Wiederherstellung bzw. Verfügbarkeit einschränken.
Grenzwerte sind zu messen, ohne Pflichtkontrollen abzuschalten.
