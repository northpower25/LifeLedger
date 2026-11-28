# Status des ersten Offline-Slices

**Stand:** 27.11.2026. Die vom Projekteigentümer erteilte
Implementation-Mandate ersetzt die früheren Startfragen und Review-Gates:
RFC-0001 bis RFC-0014, Gesamt-Roadmap und Repository Review gelten für
diesen Slice als ausreichend. Es werden keine neuen RFCs oder offenen
Architekturfragen erstellt. Fehlende Implementierungsdetails sind als feste,
begrenzte Annahmen im
[Implementation Contract](../implementation/first-offline-slice.md)
dokumentiert.

## Eingefrorener Umfang

Windows Desktop mit Tauri, lokalem FastAPI-Dienst, SQLite hinter VitaFabric
und integriertem Health Record. Der Slice umfasst den ersten lokalen Owner,
Patient, DocumentReference samt Dokumentoriginal, MedicationStatement,
Timeline, verschlüsseltes Backup und Restore. Zulässig sind ausschließlich
synthetische Daten und die drei FHIR-R4-Ressourcen `Patient`,
`DocumentReference` und `MedicationStatement`.

Plugins, Marketplace, AI, Sync, Family Features, Home Assistant und externe
Integrationen gehören nicht zum Slice und blockieren ihn nicht.

## Implementierungsstand

- **Vorhanden:** FastAPI-API, lokale SQLite-Schema/Migrationserstversion,
  Argon2id und AES-256-GCM-Payload-Verschlüsselung, TOTP-Owner-Setup/Unlock,
  Consent-/Capability-Prüfung, VitaFabric-Ressourcenpfad, synthetische
  FHIR-Datensätze, Dokumentimport, Timeline, verschlüsselter Backup/Restore,
  OpenAPI 3.1 und Backend-Integrationstests. Der Windows-CI-Lauf hat die
  Sidecar-Paketierung, Backendtests, Tauri-EXE sowie MSI- und NSIS-Installer
  erfolgreich erstellt.
- **Teilweise vorhanden:** Tauri- und TypeScript-UI mit den Slice-Formularen,
  Lokalisierung, Sidecar-Start und API-Proxy. Der installierte Windows-
  Laufzeitstart und die vollständige Offline-Journey sind noch nicht manuell
  nachgewiesen.
- **Noch erforderlich für Definition of Done:** installierte Windows-App
  starten/beenden, Offline-Flows inklusive Backup/Restore durchspielen und
  TLS-IPC auf Windows prüfen. Eine Same-User-Isolationsgrenze wird nicht
  behauptet.

Der erfolgreiche Windows-Build lief für Commit `56279b3` in
[GitHub Actions Run 46139999458](https://github.com/northpower25/LifeLedger/actions/runs/46139999458).
Das unsignierte interne Build-Artefakt heißt
`LifeLedger-windows-internal-test` und enthält EXE sowie MSI/NSIS-Installer.
Es ist ein Buildnachweis, kein Nachweis der Installation, des Offline-
Laufzeitverhaltens oder der manuellen IPC-Abnahme.

## Fest dokumentierte Einschränkungen

Die aktuelle Backend-Implementierung ist ein lokaler Testpfad, keine Freigabe
für echte Gesundheitsdaten. SQLite-FHIR-Payloads, Dokumentbytes, Consent-
Scopes, Capability-Grants, Audit-Details und Outbox-Payloads sind
AEAD-verschlüsselt; Tabellenstruktur, opake Beziehungen, Status, Eventtypen
und Zeitstempel bleiben als Metadaten sichtbar. Whole-file/SQLCipher-
Verschlüsselung ist nicht umgesetzt. Die Tauri-UI kann den Dienst nicht direkt
ansprechen: der Host startet einen Sidecar und übergibt IPC-Geheimnis sowie
ephemeres TLS-Zertifikat und -Schlüssel über stdin. Er pinnt das Zertifikat
und sendet Health- und API-Aufrufe ausschließlich über HTTPS.

Eine Quellcode-Prüfung identifizierte ein Port-Race, bei dem ein fremder
Loopback-Listener den bisherigen unverschlüsselten Health-Handshake hätte
abfangen können. Die Implementierung wurde daraufhin auf per-Start
zertifikat-gepinntes TLS umgestellt: ein Listener ohne den privaten Schlüssel
kann den TLS-Handshake nicht abschließen, bevor Host-Anfragen oder
Anmeldedaten gesendet werden. Backend-Tests decken den HTTPS-Pfad und die Ablehnung nicht vertrauenswürdiger
Zertifikate ab; Windows-Build und Sidecar-Paketierung sind in CI erfolgreich.
Der Windows-Laufzeittest steht noch aus; Same-User-Prozessisolation wird nicht
behauptet oder durch diese TLS-Änderung hergestellt.

Siehe [Implementation Backlog, Annahmen, API, Schema und Testplan](../implementation/first-offline-slice.md)
und [OpenAPI Contract](../implementation/openapi.json).
