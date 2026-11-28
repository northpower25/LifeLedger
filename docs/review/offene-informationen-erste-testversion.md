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
  OpenAPI 3.1 und Backend-Integrationstests.
- **Teilweise vorhanden:** Tauri- und TypeScript-UI mit den Slice-Formularen,
  Lokalisierung, Sidecar-Start und API-Proxy. Der Windows-Service-Start und
  die vollständige Tauri-zu-FastAPI-Integration sind nicht nachgewiesen.
- **Noch erforderlich für Definition of Done:** überprüfte Windows-IPC-
  Authentisierung und Same-User-Grenze, FastAPI-Paketierung und
  Lebenszyklussteuerung als Tauri-Service, Windows-Installer sowie Offline-
  und Negativabnahme auf Windows.

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
Anmeldedaten gesendet werden. Backend-Tests decken den HTTPS-Pfad und die
Ablehnung nicht vertrauenswürdiger Zertifikate ab. Ein Windows-Build und
Windows-Laufzeittest stehen noch aus; Same-User-Prozessisolation wird nicht
behauptet oder durch diese TLS-Änderung hergestellt.

Siehe [Implementation Backlog, Annahmen, API, Schema und Testplan](../implementation/first-offline-slice.md)
und [OpenAPI Contract](../implementation/openapi.json).
