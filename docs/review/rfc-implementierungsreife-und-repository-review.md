# Review: Implementierungsreife der RFCs und Repository-Abgleich

**Stand:** 27.11.2026, Repository `main` bei Commit `7d8486a`.

**Ergebnis:** Die RFCs 0001–0019 liefern eine brauchbare Richtung und mehrere
konkrete Vorschläge, aber noch keine durchgehend widerspruchsfreien,
ausführbaren Verträge. Alle sind Drafts; [ADR-0002](../../adr/0002-platform-direction.md)
ist vorgeschlagen. Ein sicherer, vollständiger Produktaufbau oder die
Verarbeitung echter Gesundheitsdaten kann daraus noch nicht verantwortbar
gestartet werden. Spezifikationsarbeit, Architektur- und Machbarkeitsprototypen
mit synthetischen Daten sowie Entwicklungsumgebung und Tests sind möglich;
solche Prototypen belegen weder Security noch FHIR-Konformität.

Der Review ergänzt den [Konsistenzreview](rfc-consistency-review.md) und den
[Konsolidierungsplan](rfc-open-questions-resolution-V1.md): Deren umgesetzte
Vorschläge werden nicht erneut als vollständig ungeklärt dargestellt. Sie sind
jedoch weiterhin Drafts, und eine konkretisierte Richtung ersetzt keinen
vollständigen technischen Vertrag oder ein Review.

## Einordnung und Prioritäten

Bewertet wurden sämtliche nummerierten RFCs 0001–0019 sowie das Template,
die vorhandenen Reviews, ADRs, Roadmaps, Architektur-, Security- und
Governance-Dokumente, Komponenten- und Spezifikationsverzeichnisse und die
Repository-CI. Es gibt im geprüften Stand keine Produktimplementierung;
Verzeichnis-READMEs sind überwiegend Platzhalter.

- **A – vor dem ersten implementierten Offline-Durchstich:** Entscheidungen
  und ausführbare Verträge für dessen konkreten Daten-, Prozess- und
  Sicherheitsumfang. Einzelne isolierte synthetische Experimente dürfen
  vorher entstehen, aber nicht als vollständiger Durchstich gelten.
- **B – vor der jeweiligen optionalen Funktion:** Erweiterungen, Familie,
  Sync, KI und Marketplace müssen nicht alle vor dem lokalen Kern fertig sein;
  die zugehörigen Fragen blockieren aber ihre jeweilige Implementierung bzw.
  Freigabe. Die Abhängigkeit des Gesundheitsakten-Clients vom Plugin-Modell
  ist explizit zu entscheiden (RFC-0007).
- **C – vor produktivem Einsatz/echten Daten:** unabhängige Sicherheits-,
  Datenschutz- und ggf. Rechtsprüfung sowie die in der
  [Gesamt-Roadmap](../roadmap/project.md) definierten Release-Gates. A und B
  ersetzen diese Freigabe nicht.

Die Priorität bezeichnet den frühesten relevanten Entscheidungspunkt, keine
Annahme, dass ein RFC bereits beschlossen oder eine Funktion implementiert ist.
Empfohlene Speicherorte unten sind Vorschläge, keine zusätzlichen Architektur-
oder Governance-Entscheidungen.

## Übergreifende Klärungen vor dem ersten Durchstich

1. **Verbindlichkeit und Scope (A):** RFC-Status, Entscheidungsträger,
   Review- und Annahmekriterien sowie die Reihenfolge RFC → ADR →
   versionierte Spezifikation klären. Der erste Durchstich nennt ein
   Dokument, einen Datentyp und Backup; die erste Nutzerreise nennt zusätzlich
   Medikation und Timeline. Welche Teilmenge ist zuerst abnahmefähig, welche
   der sechs MVP-Ressourcen ist für sie erforderlich und gehört eine
   getestete Wiederherstellung bereits zum Backup-Gate?
   Belege: [RFC-0002 §13](../../rfc/0002-platform-core-architecture.md),
   [RFC-0007 §8](../../rfc/0007-application-framework.md),
   [Roadmap Stufen 2–3](../roadmap/project.md).
2. **End-to-End-Sicherheitsvertrag (A):** Ein konkretes Bedrohungsmodell und
   Sequenzdiagramme für Erstanlage, Import, Lesen, Widerruf, Neustart,
   Sicherung und Wiederherstellung beschließen: Akteure, Prozess- und
   Vertrauensgrenzen, Schlüsselbesitz, Identity-, Capability- und
   Consent-Prüfung, Auditerfolg/-ausfall und Ablehnungen. Insbesondere fehlen
   das Owner-/Erst-Consent-Bootstrapping und das Verhalten bei Ausfall eines
   Pflichtdienstes. Kein implizites Recht oder unsicherer Fallback.
3. **Prüfbare Verträge (A):** Daten-, API-, Event- und Fehlerformate mit
   Versionen, synthetischen Beispielen und negativen Akzeptanzfällen
   festlegen. RFC-0015–0019 sind derzeit überwiegend Aufzählungen, keine
   ausführbaren Schemata. Interne REST-APIs und Plugin-WIT-Imports müssen
   gemeinsam spezifiziert werden, statt einen identischen Transport
   vorauszusetzen.
4. **Technische Machbarkeit und Kosten (A/B):** Tauri/FastAPI-Lebenszyklus
   und sichere lokale Kommunikation auf Windows, verschlüsselte SQLite-Daten
   inklusive Indizes/Dateien, HL7-Validator und Wasmtime auf den jeweils
   tatsächlich unterstützten Plattformen nachweisen. Budgets für Startzeit,
   RAM, Datenmenge, Validierung und Audit sowie Messgeräte und Abbruchkriterien
   fehlen. Sicherheitskontrollen dürfen für Performance nicht umgangen werden.
5. **Offline, Widerruf und Kopien (A für lokale Zugriffe; B für Sync/Exporte):**
   „sofort“ benötigt eine messbare lokale Grenze und Regeln für laufende
   Vorgänge. Ein offline Gerät oder bereits exportierter bzw. an Dritte
   übertragener Klartext kann nicht durch ein lokales Widerrufsereignis
   rückwirkend gelöscht werden. Nach Wiederverbindung müssen Sperren und
   Löschungen vor weiterer Verarbeitung greifen; Garantien, Fristen und
   Restrisiken sind pro Datenpfad festzulegen.

## Offene Punkte je RFC

### [RFC-0001 – Platform Direction](../../rfc/0001-platform-direction.md) — A/B

- **A:** Welche lokale Kernfunktion, Zielplattform und Nutzerreise sind
  verbindlich, und wer nimmt die Architektur gegenüber dem vorgeschlagenen
  ADR ab? Verantwortliche für Core und Durchsetzung müssen benannt werden.
- **B:** Für Relay, Zero-Knowledge-Sync und Managed Cloud jeweils Datenflüsse,
  Metadaten, Verantwortlichkeiten, Datenschutz-/Rechtsprüfung und ein
  separates Freigabe-Gate festlegen. Die Szenarien sind keine Freigabe.
- **Artefakt:** Entscheidungs- und Scope-Matrix in RFC/ADR und Roadmap; konkrete
  Grenzen in `specifications/security/` und `specifications/integrations/`.

### [RFC-0002 – Platform Core Architecture](../../rfc/0002-platform-core-architecture.md) — A

- Prozess-/Paketgrenzen, Startreihenfolge und Kommunikation zwischen Tauri,
  FastAPI, Core und VitaFabric festlegen; Authentisierung, Port-/IPC-Schutz,
  Dienstende, Updates und Fehlverhalten auf Windows beschreiben.
- Festlegen, welche zwingenden **Verträge** im ersten Slice tatsächlich
  ausgeführt werden müssen und ob der Plugin Host bereits benötigt wird.
  RFC-0014 lässt die Topologie offen; ein Platzhalter darf keine Isolation
  vortäuschen.
- §16 nennt RFC-0005 „Marketplace Governance“ und RFC-0006 „Deployment
  Modes“; tatsächlich behandeln sie Event Bus und Plugin Runtime. Folge-RFCs
  anhand des [Indexes](../../rfc/README.md) korrigieren.
- **Artefakt:** Kontext-/Sequenzdiagramme und überprüfbare Schnittstellen;
  Platzierung von Core-Implementierung und Tests entscheiden.

### [RFC-0003 – Identity & Consent](../../rfc/0003-identity-and-consent-framework.md) — A/B

- **A:** Identitäten für lokalen Owner und Gerät, Credential-/Session-
  Lebenszyklus, Erstfreigabe für eigene Daten, MFA-Bedeutung im Offline-Modus,
  Sperre, Recovery und Autorisierung definieren. Consent-Objekt um Aussteller,
  Betroffenen, Zweck, Operation, Ressource, Gültigkeit, Zustand, Version und
  Widerruf ergänzen; Zustandsübergänge und Änderungsrechte festlegen.
- **A/B:** Wer prüft welche Policy am tatsächlichen Zugriffspunkt? Atomarität
  bei gleichzeitigem Widerruf/Zugriff, Session-Invalidierung, Audit-Ausfall
  und offline Kopien spezifizieren. Familien- und Notfallverfahren inklusive
  rechtlicher Grenzen separat vor deren Implementierung klären.
- **Artefakt:** Zustandsautomat, Zugriffsmatrix und Negativfälle in
  `specifications/security/`, API-Vertrag zusammen mit RFC-0018.

### [RFC-0004 – Capability & Permission Model](../../rfc/0004-capability-and-permission-model.md) — A/B

- **A:** Die vorhandenen Risikostufen und Beispiele in einen vollständigen,
  versionierten Katalog überführen: Subjekt, Ressource, Operation, Zweck,
  Scope, Aussteller, Grant-Lebenszyklus und Zuordnung pro API. Owner-Zugriffe
  und Zusammenspiel mit Consent/Rollen konkretisieren. Unbekannte
  Capabilities bleiben gesperrt.
- **B:** Netzwerkziele, Dateispeicher, AI und administrative Aktionen
  granular begrenzen; Prüfung und Widerruf laufender Aufrufe und Abonnements
  definieren. Klären, wie die Reviewpflichten der Risikostufen zu lokalen,
  nicht gelisteten Plugins passen, ohne Marketplace-Pflicht einzuführen.
- **Artefakt:** Capability-/Operation-Matrix mit zulässigen und verweigerten
  Beispielen, Auditdaten und Konformitätstests.

### [RFC-0005 – Event Bus](../../rfc/0005-event-bus-architecture.md) — A/B

- **A:** Festlegen, welche Ereignisse im Slice notwendig sind; atomare
  Speicherung von Datenänderung und Event, Zustellungsgarantie, Reihenfolge,
  Idempotenz, Retry/DLQ, Backpressure, Replay und Wiederanlauf spezifizieren.
  Widerruf darf nicht von einer verspäteten Event-Zustellung abhängen.
- **B:** Event-Zugriff pro Producer/Consumer und Profil, Reautorisierung beim
  Replay, Aufbewahrung, Löschung sowie Schutz opaker, dennoch potenziell
  personenbezogener IDs festlegen. Prioritäten und Ressourcenlimits messbar
  machen.
- §6 nennt ASCII-Segmente mit Punkttrennung, verwendet aber Namen wie
  `role_granted`; das zulässige Zeichenformat einschließlich Unterstrich
  präzisieren. Zuständigkeit für alle Kategorien, etwa `plugin`, `sync` und
  `application`, vollständig zuordnen.
- **Artefakt:** Event-Registry und transportneutrale Schemas mit RFC-0017;
  Crash-, Duplikat-, Widerrufs- und Replay-Tests.

### [RFC-0006 – Plugin Runtime & Isolation](../../rfc/0006-plugin-runtime-and-isolation.md) — B

- Wasmtime, Component Model und WASI 0.2 sind vorgeschlagen; konkrete
  Versionen, Build-/Einbettungsmodell und tatsächliche Unterstützung je
  Desktop-, Mobile- und ggf. Browser-Ziel nachweisen. Fehlende Isolation
  bleibt ein Ausführungsstopp, kein nativer Fallback.
- WIT-Imports, Manifest-/Paketformat, Signaturvertrauen, Limits und
  Fehlermodell definieren. Netzwerkproxy braucht Regeln für Ziele,
  Weiterleitungen, DNS/Rebinding, Datenabfluss und Widerruf; Secret-API
  braucht ein konkretes Nutzungsmodell ohne Secret-Offenlegung.
- CPU-/RAM-/Zeitlimits, Startkosten und Plugin-Abstürze pro Plattform messen;
  Grenzen und Verhalten bei Überschreitung mit Negativtests belegen.
- **Artefakt:** WIT, Paket- und Sandbox-Spezifikation samt synthetischem
  Referenz-Connector und Isolationstests; RFC-0019 als Vertrag vervollständigen.

### [RFC-0007 – Application Framework](../../rfc/0007-application-framework.md) — A/B

- **A:** Der Health Record ist laut §4 eine spezialisierte Plugin-Anwendung,
  während [Roadmap Stufe 4](../roadmap/project.md) Erweiterbarkeit erst nach
  dem lokalen Kern vorsieht. Entscheiden, ob die Referenzanwendung von Beginn
  an durch die isolierte Plugin Runtime läuft oder ein ausdrücklich
  spezifizierter, sicherer erster Host-/UI-Pfad zulässig ist; dabei RFC-0006,
  RFC-0014 und die Roadmap gemeinsam aktualisieren.
- **A:** Dokumentformat/-größe, Medikation, Timeline-Sortierung, Fehler,
  Backup/Restore und Abnahmekriterien für die erste Nutzerreise festlegen.
  Deutsch/Englisch, WCAG-Ziel, Zeitzonen und Profile-Auswahl prüfbar machen.
- **B:** UI-Rendering und Isolation, App-zu-App-Abhängigkeiten trotz Verbots
  direkter Plugin-Kommunikation, Manifest/Lockfile, Upgrade-Transaktion,
  Backup und Rollback einschließlich Absturzfällen spezifizieren.
- **Artefakt:** User-Flow und Akzeptanzfälle; später UI-/WIT- und
  Lifecycle-Vertrag mit Versionsmatrix.

### [RFC-0008 – Family & Delegation](../../rfc/0008-family-and-delegation-model.md) — B

- Das bestehende Rollenmodell aus RFC-0003 nicht neu definieren, sondern
  Identitätsnachweis, Guardian-Nachweis, Delegationskette, Scope-Verengung,
  optionale Proxy-Weiterdelegation und Entzug durch zuständige Akteure
  operationalisieren.
- Bei Minderjährigen Profil-Owner versus handelnde Person, Volljährigkeits-
  übergang und jurisdiktionsabhängige Rechte klären; nicht voraussetzen,
  dass eine Softwareentscheidung rechtliche Vertretung beweist.
- Emergency-Bundle und Zugriffsvoraussetzungen vereinheitlichen: §11 nennt
  zusätzlich Geburtsdatum gegenüber RFC-0003 §10. Offline-Verfügbarkeit,
  Zustimmung, Audit und Risiken bei Gerätesperre beschreiben.
- **Artefakt:** Familien-/Delegations-Zustandsmodell, Rechte- und
  Jurisdiktionsmatrix sowie Missbrauchs- und Widerrufstests.

### [RFC-0009 – Marketplace Governance & Trust](../../rfc/0009-marketplace-governance-and-trust-framework.md) — B

- Zwei unabhängige Reviews und Digest-Signatur sind vorgeschlagen. Vor
  Umsetzung Schlüsselhierarchie, Signaturformat, Trust Bootstrap, Widerrufs-
  und Offline-Verhalten, Gültigkeit, Rotation und Kompromittierungsfall
  festlegen; insbesondere Folgen veralteter Sperrlisten transparent machen.
- §23 erlaubt Patch-Releases bei „unverändertem Digestvergleich“
  automatisiert: Ein geändertes Paket hat grundsätzlich einen anderen Digest.
  Definieren, welche reproduzierbaren Vergleiche, Prüfungen und neuen
  Signaturen einen Patch tatsächlich freigeben.
- Betreiber, Quorum, Fristen, Einspruch, Delisting und Vertrauensstatus
  installierter Offline-Pakete festlegen; unabhängig von Nutzer-Consent.
- **Artefakt:** Signatur-/Release-Protokoll und Governance-Runbooks; keine
  Aussage, dass ein Listing Sicherheit garantiert.

### [RFC-0010 – Zero-Knowledge Sync & Recovery](../../rfc/0010-zero-knowledge-sync-and-recovery-framework.md) — B

- Der FHIR-Konfliktworkflow ist bereits beschrieben; kausale
  Versionsrepräsentation, Protokoll, Integritäts-/Replay-Schutz,
  Gerätewiderruf, Pairing-Authentisierung und Verhalten nicht erreichbarer
  Geräte einschließlich Tombstone-Retention fehlen weiterhin.
- Schlüsselhierarchie präzisieren: Erzeugung und Wrapping von Root-/Daten-/
  Geräteschlüsseln, Passwortwechsel, Recovery mit Schlüssel **oder**
  autorisiertem Gerät, Rotation und Verlust. Die Formulierung
  „User Password + Recovery Secret“ allein erklärt diese Alternativen nicht.
  Recovery-Kontakte ohne Datenzugriff benötigen ein überprüfbares Verfahren.
- §16 bezeichnet verschlüsseltes Backup als optional, §30 verbietet
  unverschlüsselte Backups; mit Roadmap und erstem lokalen Backup klären,
  welche Sicherungen verpflichtend verschlüsselt sind.
- **Artefakt:** unabhängig geprüftes Kryptoprotokoll und Bedrohungsmodell,
  Testvektoren, Offline-/Konflikt-/Restore-Tests; Aussagen zu Metadaten und
  nicht rückholbaren Kopien dokumentieren.

### [RFC-0011 – AI Provider & Health Twin](../../rfc/0011-ai-provider-framework-and-health-twin-architecture.md) — B/C

- Für Dokumentzusammenfassung Eingabegrenzen, Quellen-/Versionsbezug,
  Qualitäts- und Sicherheitskriterien, Prompt-Injection-Abwehr,
  Tool-Berechtigungen, Provider-Timeouts und keine stillen Cloud-Fallbacks
  definieren. „Lokal“ anhand des tatsächlichen Datenpfads prüfen.
- §24 verlangt Audit des „Prompt“, RFC-0004 §17 verbietet Gesundheitsinhalte
  im Audit. Festlegen, ob nur datensparsame Metadaten/Referenzen oder ein
  separat geschütztes, zustimmungsgebundenes Prompt-Protokoll zulässig sind;
  keine Gesundheitsinhalte stillschweigend ins Audit schreiben.
- Für bestehende 24-Stunden-/30-Tage-Vorschläge den Beginn der Fristen,
  Offline-Stores, Fehlereskalation, Backup-Schlüssel, Löschbelege und
  Restore-Reihenfolge operationalisieren. Widerruf bei externen Providern
  kann bereits übertragene Daten nicht technisch zurückholen.
- **C:** Abgrenzung von Vorhersagen/Risikoberechnungen zu ausgeschlossener
  Diagnose und Therapie sowie konkrete regulatorische Zweckbestimmung vor
  Freigabe prüfen.
- **Artefakt:** Provider-/MCP-Vertrag, Datenfluss- und Retention-Matrix,
  Sicherheits- und Zweckbestimmungsreview.

### [RFC-0012 – Sustainability, Governance & Operations](../../rfc/0012-sustainability-governance-and-operations.md) — A/B/C

- **A:** Verantwortliche, Entscheidungsbefugnis und Annahmeverfahren für RFCs,
  ADRs und sicherheitskritische Verträge sowie Stellvertretung für das
  heutige Maintainer-Modell festlegen.
- **B/C:** Vorgeschlagene Quoren, 14-/90-Tage-Regeln, Signing-/Incident- und
  Finanzierungsprozesse vor Betrieb bestätigen; bei zu kleiner Maintainerzahl
  realisierbares Verfahren klären, ohne Vier-Augen-Anforderungen still
  abzuschwächen.
- Audit- und Tombstone-Aufbewahrung, Löschung, Zugriff, Integrität,
  Speichergrenzen und Ausfallverhalten fehlen trotz Verweis aus RFC-0004 und
  RFC-0011. Operative Fristen und Zuständigkeit konkretisieren.
- **Artefakt:** Governance-Beschlüsse, Security-/Release-Runbooks und
  datensparsame Audit-/Retention-Spezifikation.

### [RFC-0013 – VitaFabric Data Contracts](../../rfc/0013-vitafabric-data-contracts-and-fhir-governance.md) — A/B

- **A:** Minimalen Import-/Lese-/Schreibvertrag für den gewählten Slice,
  FHIR-Profile und Validator-Integration, Provenienz für manuelle Eingaben,
  ID-/Versionsmodell und Validierungsfehler festlegen. Dokumentoriginal,
  MIME-Typ, Größenlimit, Integrität und verschlüsselte Ablage spezifizieren.
- **A:** Datenbankschema bzw. verschlüsselte Objekte, Schlüsselgrenzen,
  Indizes/materialisierte Views, Transaktionen, Audit und Backup samt Restore
  definieren. Wenn Adapter ausschließlich Ciphertext erhalten, muss
  insbesondere Suche/Indexierung ohne unbeabsichtigte Klartext-Lecks erklärt
  werden.
- **B:** Connector-Idempotenz, Mapping-Versionen, Export-/Löschsemantik und
  Derived-Data-Schemas samt Konflikten ergänzen. Keine aus RFC-0010/-0011
  fehlenden Detailverträge als bereits vorhanden ausgeben.
- **Artefakt:** versionierte FHIR-/Storage-/Provenienzverträge in
  `specifications/`, synthetische positive und negative Fixtures.

### [RFC-0014 – Core Runtime & Platform Boundaries](../../rfc/0014-core-runtime-platform-boundaries.md) — A

- Die Zuständigkeitsgrenzen und Fail-closed-Richtung sind beschrieben, aber
  ausführbare Prozessgrenzen, Host-/VitaFabric-Schnittstellen und
  Durchsetzungsorte fehlen. Festlegen, wie die VitaFabric-Prüfung auch bei
  internem Aufruf nicht umgangen wird und wie Audit-Ausfälle behandelt
  werden, ohne einen erfolgreichen Zugriff zu suggerieren.
- Die Abgrenzung zwischen austauschbarer interner Implementierung und
  verbotener Plugin-Kontrolle anhand konkreter Komponenten und Verträge
  verifizieren; Entscheidung zur Referenzanwendung mit RFC-0007 abstimmen.
- **Artefakt:** Verantwortlichkeits- und Trust-Boundary-Diagramm,
  Architekturtests, messbare Budgets und Ausfalltests.

### [RFC-0015 – FHIR Profiles & Terminology](../../rfc/0015-fhir-profiles-and-terminology-governance.md) — A/B

- **A:** Für die im Slice genutzten Ressourcen echte versionierte FHIR-R4-
  Profile und Beispiele veröffentlichen: Kardinalitäten, Datentypen,
  Invarianten, Referenzen, Erweiterungen, Terminologie-Bindungen und Verhalten
  bei unbekannten Codes. `Observation.value` ist eine FHIR-Auswahl
  (`value[x]`); Form, Kardinalität und ggf. absent reason sind zu definieren.
- Genaue Validator-/FHIR-Paketversion, Offline-Terminologieprüfung,
  Lizenz-/Verfügbarkeit von SNOMED CT, LOINC und UCUM sowie Fehler- und
  Warnungsbehandlung klären. „optional“ präzisieren: Nutzung und Bindungen
  dürfen nicht widersprüchlich sein.
- **B:** Governance, Herausgabe, Migration und Kompatibilität der Core-,
  Experimental- und Community-Profile festlegen.
- **Artefakt:** Profile, ValueSets/Bindings, Validator-Konfiguration und
  gültige/ungültige Testvektoren in `specifications/fhir/`.

### [RFC-0016 – Platform API Contract Standards](../../rfc/0016-platform-api-contract-standards.md) — A

- REST/OpenAPI 3.1 und `/api/v1/` sind Vorgaben, aber Endpunkte, Auth,
  Autorisierung pro Operation, Request-/Response-Schemas, Statuscodes,
  Fehlertaxonomie, Pagination, Idempotenz und Kompatibilitätsregeln fehlen.
  Locale und keine sensitiven Daten in Fehlern/Logs berücksichtigen.
- Audit nicht auf mutierende HTTP-Methoden begrenzen: RFC-0003 §12 verlangt
  auch Audit für lesende Gesundheitsdatenzugriffe. Verhalten bei
  Audit-/Policy-Ausfall und parallelem Widerruf spezifizieren.
- Geltungsbereich für lokale HTTP-APIs, interne Funktionsaufrufe und
  WIT-Plugin-Schnittstellen festlegen; REST nicht unbesehen auf alle
  Prozessgrenzen übertragen.
- **Artefakt:** versioniertes OpenAPI-Dokument und Policy-Matrix mit
  Vertrags- und Negativtests.

### [RFC-0017 – Event Schemas & Messaging](../../rfc/0017-event-schemas-and-messaging-contracts.md) — A/B

- Das Envelope-Beispiel enthält gegenüber RFC-0005 §5 kein `source` und kein
  `subject`. Pflicht-/optionale Felder, Datentypen, IDs, Zeitformat,
  Korrelation, Payload und Schema-Validierung je Event verbindlich
  vereinheitlichen; Beispiele sind noch kein Schema.
- Für die `n`/`n-1`-Regel klären, was bei Version 1, Versionssprüngen,
  nicht unterstützten Versionen und Lebensdauer alter Events gilt; Migration,
  Replay und DLQ mit RFC-0005 abstimmen.
- **Artefakt:** Event-Registry und maschinenprüfbare Schemas/Fixtures mit
  Kompatibilitäts-, Datenschutz- und Replay-Tests.

### [RFC-0018 – Identity & Consent APIs](../../rfc/0018-identity-and-consent-apis.md) — A/B

- **A:** Für den lokalen Owner-Pfad Operationen als konkrete RFC-0016-API
  mit Datenmodellen, Authentisierung, Berechtigungsregeln, Fehlercodes,
  Idempotenz und Audit definieren. RFC-0003 nennt `checkConsent`, hier fehlt
  diese Operation: entscheiden, ob sie eine interne Policy-Schnittstelle
  oder externe API ist und wer sie aufrufen darf.
- **B:** Household-/Emergency-Abläufe, Rollenprüfung, Zustimmung,
  Ablauf/Widerruf, Race Conditions und Ausfallfälle für Delegierte und
  Geräte konkretisieren; `approveEmergencyAccess` nicht als bereits
  spezifizierten Workflow voraussetzen.
- **Artefakt:** OpenAPI und Zustandsautomaten mit Verweigerungs-,
  Widerrufs- und Audit-Negativfällen.

### [RFC-0019 – Plugin APIs & SDK](../../rfc/0019-plugin-apis-and-sdk-contracts.md) — B

- Ein „verbindliches Schema“ wird angekündigt, aber nicht bereitgestellt.
  Manifest, `permissions.json`, Paket, Signatur, API-/WIT-Versionen,
  Capability-Scopes und Kompatibilitätsbereiche maschinenlesbar definieren.
  Beispiele in RFC-0004/-0006/-0007 darauf abstimmen.
- RFC-0006 nennt einen kontrollierten Netzwerkproxy, RFC-0019 listet keine
  Network API; entscheiden und Host-Funktionen einschließlich VitaFabric,
  Events, Filesystem und Secrets vollständig spezifizieren. Welche Identity-/
  Consent-Information ein Plugin sehen darf, datensparsam festlegen.
- SDK-Sprachen, Fehler, Rückwärtskompatibilität, Fixtures und unabhängig
  ausführbare Konformitätstests festlegen; Offline-Installation und
  Signaturwiderruf mit RFC-0009 abstimmen.
- **Artefakt:** WIT, Manifest-/Paket-Schema, Referenz-SDK und
  Konformitätssuite nach tatsächlicher Plattformfreigabe.

### [RFC-0000 – Template](../../rfc/0000-template.md) — A

Das Template ist kein Produkt-RFC. Status, Alternativen, Sicherheits-/
Datenschutzfolgen, Kompatibilität und offene Fragen sind bereits vorgesehen.
Für zukünftige RFCs sollten Owner, Abhängigkeiten und prüfbare
Abnahmekriterien ausdrücklich ergänzt und einheitlich ausgefüllt werden.
Bestehende RFCs 0015–0019 nennen beispielsweise keinen Owner.

## Repository- und Dokumentationsabgleich

Die Struktur bildet VitaFabric, LifeWeaver, Clients, Plugins, Integrationen,
RFCs und Spezifikationen grundsätzlich ab. Sie ist jedoch ein **Gerüst**:
Die meisten Verzeichnisse enthalten nur README-Platzhalter; es existieren
keine ausführbaren Produktverträge, FHIR-Profile oder Produkt-Tests. Der
[CI-Workflow](../../.github/workflows/repository.yml) prüft lediglich
Bootstrap-Dateien und Verzeichnisse, nicht RFC-Konformität oder Software.
Die [strukturelle Validierung](../architecture/repository_validation.md)
ist ein historischer Strukturbericht und kein Nachweis implementierter
Architektur.

| Bereich / Bestand | Erforderliche Anpassung |
| --- | --- |
| Core Runtime | `backend/` existiert, aber kein zugeordneter Core-Bereich für Identity, Consent, Capability, Audit, Event Bus, Secret Store und Plugin Host. Nach Entscheidung zur Topologie in `backend/` oder einem ausdrücklich gewählten Core-Pfad platzieren; Grenzen zu `platform/vitafabric/` dokumentieren, keine vorschnelle Umstrukturierung als Implementierung ausgeben. |
| `specifications/` | Bestehende Bereiche `fhir/`, `security/`, `storage/`, `connectors/`, `integrations/`, `mcp/` nutzen; geprüfte Profile, Daten-/Sicherheits-/Storageverträge ergänzen. Für API, Events, Identity/Consent und Plugin/WIT fehlen erkennbare eigene Vertragsorte: dort oder in abgestimmten Unterverzeichnissen versionierte Schemas und einen Index anlegen. Entwurfsstatus von angenommenen Normen trennen. |
| `frontend-desktop/`, `backend/` | [Backend-README](../../backend/README.md) nennt PostgreSQL/TimescaleDB, die [Gesamt-Roadmap](../roadmap/project.md) SQLite für den ersten lokalen Durchstich. README als spätere Option gegenüber geplanter lokaler SQLite-Nutzung präzisieren; Tauri/FastAPI-Verhältnis und sicheren Prozesspfad nach Entscheidung dokumentieren. |
| `platform/vitafabric/` | FHIR, Provenienz, Import, verschlüsselte Storage-Abstraktion, Derived Data und Grenzen zu Adaptern in Verträgen und späteren Komponenten sichtbar machen. Klarstellen, dass `DocumentReference` und verschlüsselte Originaldatei gemeinsam verwaltet werden müssen. |
| `plugins/`, `platform/lifeweaver/` | Plugin-README und [Plugin-Roadmap](../roadmap/plugins.md) bezeichnen Marketplace-Kriterien überwiegend als unentschieden; RFC-0009 enthält bereits konkrete **Draft**-Vorschläge. Auf diese verweisen und verbleibende Betriebs-/Implementierungsfragen unterscheiden. In der Plugin-Roadmap wird zudem das FHIR-Kernmodell dem Core zugeordnet; nach RFC-0014 gehört es VitaFabric. |
| `integrations/` | Nextcloud ist als erste externe Integration vor Home Assistant vorgesehen, aber noch ohne Integrationsverzeichnis oder Vertrag. Nach Scope-Entscheidung gezielt einen Ort und `specifications/integrations/`-Vertrag ergänzen; Home Assistant bleibt optional und ohne direkten Datenbankzugriff. |
| `docs/architecture/README.md`, `docs/roadmap/project.md` | RFC-0014 sowie inzwischen präzisierte Entwürfe zu Isolation, Marketplace und FHIR-Konflikten referenzieren. Aussagen wie vollständig offene Reviewkriterien oder völlig offene Konfliktbehandlung durch „als Draft vorgeschlagen, Einzelheiten offen“ ersetzen. Die Restfragen der Gesamt-Roadmap nennen eine konkrete WASM-Runtime als offen, obwohl RFC-0006 Wasmtime/WASI 0.2 vorschlägt; offene Plattformnachweise und Versionen benennen. |
| `docs/roadmap/assessment.md` | Historischen Stand kennzeichnen bzw. aktualisieren: erste Nutzerreise/Zielgruppe und WCAG 2.2 AA sind inzwischen vorgeschlagen, auch wenn Abnahmedetails offen bleiben. Keine veralteten Aussagen als aktuelle Implementierungslücken formulieren. |
| `.github/architecture_checklist.md` | „Reject if custom health models are introduced“ gegen RFC-0013 Derived Data abgrenzen: FHIR bleibt kanonisch für FHIR-Ressourcen, Derived Data sind nicht automatisch FHIR. Anwendbarkeit von Checklistenfragen klären, ohne Pflichtkontrollen abzuschwächen. |
| `docs/mobile/Multilanguage_Strategy.md`, `docs/governance/`, `docs/security/` | Stichwortlisten zu Sprachumfang, Accessibility und technischem Security-Modell später um konkrete, versionierte Anforderungen ergänzen. Bestehendes Maintainer-Modell und vorgeschlagene Governance-/Succession-Regeln aus RFC-0012 als unterschiedliche Reifegrade darstellen. |
| `docs/tree.md`, `docs/README.md`, `rfc/README.md` | Baum ist veraltet und zeigt weder aktuelle RFCs noch zahlreiche Dokumente. Aktualisieren oder automatisiert generieren und Pflegeverantwortung festlegen. Historische Reviews als zeitgebundene Ergebnisse belassen und auf die neue Bewertung verweisen; der RFC-Index verlinkt diesen Review. |
| `tests/`, `tools/`, `.github/workflows/` | Mit den ersten Verträgen synthetische Fixtures, Schema-/Link-/Konsistenzprüfungen, Unit-, Integrations-, Offline- und Sicherheits-Negativtests ergänzen. Je Komponente Tests nahe am Code, übergreifende End-to-End-Tests unter `tests/`; erst tatsächlich vorhandene Prüfungen in CI behaupten. |

## Empfohlene Reihenfolge und Abnahme

1. **A:** Scope und Verantwortliche bestätigen; Widersprüche aus RFC-0002,
   -0007, -0010, -0011, -0016 und -0017 auflösen. Das erste Daten- und
   Bedrohungsmodell samt Benutzerreise und messbaren Akzeptanzfällen
   verabschieden.
2. **A:** Versionierte Minimalverträge für Identity/Consent/Capabilities,
   VitaFabric/FHIR, verschlüsselten lokalen Speicher, Backup/Restore, Audit
   und ggf. tatsächlich benötigte Events erarbeiten. Für den gewählten
   Client Prozessgrenzen und Budgets festlegen; synthetische Fixtures und
   Negativfälle bereitstellen.
3. **A:** Einen begrenzten Windows-Offline-Durchstich implementieren und
   unabhängig prüfen: gültige/ungültige Daten, verweigerte/widerrufene
   Rechte, Audit-Ausfall, Neustart, falscher Schlüssel, Backup/Restore und
   Netzwerkabwesenheit. Umfang und App-/Plugin-Host-Entscheidung aus Schritt 1
   sind Voraussetzung.
4. **B:** Plugin-, Familien-, Sync-, Marketplace- und AI-Verträge jeweils vor
   ihrer Funktion spezifizieren und getrennt prüfen; nicht alle sind
   Voraussetzung für Experimente oder den lokalen Kern.
5. **C:** Vor echten Gesundheitsdaten sämtliche einschlägigen Release-Gates,
   externe Sicherheitsprüfung, Datenschutz-/Rechtsprüfung, Recovery-Übung
   und dokumentierte Freigabe gemäß Gesamt-Roadmap erfüllen.

**Nebenwirkungen und Zielkonflikte:** Erneute Autorisierung, vollständige
Validierung, Audit und Isolation kosten CPU, Speicher und Startzeit; lokale
Offline-Verfügbarkeit kann mit aktueller Widerrufsinformation kollidieren.
Verschlüsselte Indizes und selektive Backup-Löschung erhöhen Komplexität und
Speicherbedarf. Messungen und explizite Restrisiken sind notwendig; keine
dieser Kosten rechtfertigt das Umgehen von Sicherheitsgrenzen.
