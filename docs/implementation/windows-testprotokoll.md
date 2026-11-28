# Windows-Testprotokoll: erster Offline-Slice

**Status: Windows-CI-Build bestanden; interaktive Windows-Abnahme nicht
durchgeführt.** Der CI-Lauf für Commit `56279b3` hat Sidecar, Desktop-EXE und
MSI/NSIS-Installer gebaut; Actions Run
[46139999458](https://github.com/northpower25/LifeLedger/actions/runs/46139999458),
Artefakt `LifeLedger-windows-internal-test`. Nur für eine isolierte
Testumgebung und ausschließlich synthetische Daten. Der Build ist unsigniert
und keine Freigabe für echte Gesundheitsdaten. Die interaktiven Tests müssen
mit dem exakt im Formular notierten Commit durchgeführt werden. Ein
erfolgreicher Funktionstest beweist keine Same-User-Isolation oder
Produktionssicherheit.

## Vorbereitung und Build

1. Windows 10/11 x64 (möglichst saubere VM), WebView2 Runtime, Python 3.12,
   Node.js 22, Rust mit `x86_64-pc-windows-msvc` sowie Visual Studio C++ Build
   Tools installieren. Für Setup, Paketdownloads und Installer-Build ist
   Internetzugang erforderlich. Der eigentliche Offline-Test erfolgt erst
   nach Installation und Deaktivierung aller Netzwerkadapter.
2. Repository einschließlich des PR-Branches auschecken. In PowerShell im
   Repositoryverzeichnis ausführen:

   ```powershell
   git rev-parse HEAD
   py -3.12 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -e "./backend[test]"
   python -m pytest backend/tests -q
   .\backend\scripts\build_windows_sidecar.ps1
   Push-Location frontend-desktop
   npm ci
   npm run tauri build
   Pop-Location
   ```

   Jeder Schritt muss erfolgreich enden; bei einem Fehler abbrechen und die
   Fehlermeldung im Formular notieren. Der Sidecar liegt unter
   `frontend-desktop/src-tauri/binaries/lifeledger-api/lifeledger-api.exe`
   mit den zugehörigen Laufzeitdateien im selben Verzeichnis,
   die Installer unter `frontend-desktop/src-tauri/target/release/bundle/`.
   Alternativ kann ein erfolgreiches Windows-Actions-Artefakt desselben
   Commits verwendet werden. Ein erfolgreicher Build ersetzt die folgenden
   interaktiven Tests nicht.
3. Einen erzeugten Installer installieren. Für einen isolierten Erststart eine
   neue Windows-Testbenutzerumgebung verwenden. Standard-Datenbank:
   `%LOCALAPPDATA%\LifeLedger\lifeledger.sqlite3`. Keine bestehende Datenbank
   löschen oder überschreiben. Das Restore ersetzt den aktuellen Datenbestand.
4. Lokal eine UTF-8-Textdatei `synthetisch.txt` mit dem Inhalt
   `SYNTHETISCHES TESTDOKUMENT 123` anlegen. Einen offlinefähigen
   TOTP-Authenticator bereithalten und die Windows-Uhr überprüfen. Passwörter
   und TOTP-Schlüssel niemals im Protokoll oder in Screenshots festhalten.
5. Netzwerkkonnektivität vorübergehend deaktivieren (alle Adapter, auch VPN).
   Sicherstellen, dass auch WLAN und Mobilfunk aus sind. Erst danach die
   installierte Anwendung starten. Die Tests W01–W10 offline durchführen.

## Tests

Ergebnis jeweils **bestanden**, **fehlgeschlagen** oder **nicht durchgeführt**
eintragen. Bei Abweichungen Schritte, Zeitpunkt und bereinigte Fehlermeldung
festhalten; keine Geheimnisse, Tokens oder personenbezogenen Daten teilen.

| ID | Durchführung | Erwartetes Ergebnis |
| --- | --- | --- |
| W01 Start | App starten; im Task-Manager den Prozess `lifeledger-api.exe` suchen. | UI mit Hinweis auf synthetische Daten erscheint; ein API-Prozess läuft. |
| W02 Owner | Owner mit Testnamen und Passwort (mindestens 12 Zeichen) anlegen; QR-Code im Authenticator scannen oder den angezeigten TOTP-Schlüssel manuell erfassen und aktuellen Code bestätigen. Auch Wiederaufnahme einer unterbrochenen Einrichtung prüfen. | Einrichtung erfolgreich, Patient-Bereich erscheint; QR-Code und manueller Schlüssel richten denselben TOTP-Zugang ein. |
| W03 Daten | Patient `Testperson Alpha` anlegen, auswählen, `synthetisch.txt` unter Titel `Testdokument 123` importieren, Medikation `Testmedikation 123` anlegen. | Timeline zeigt Patient, DocumentReference und MedicationStatement mit den Testbezeichnungen. |
| W04 Backup | Separate Test-Passphrase mit mindestens 12 Zeichen eingeben und verschlüsseltes Backup erstellen. Im Speicherdialog neuen Dateinamen wählen; danach erneut denselben Dateinamen wählen und den Dialog zusätzlich abbrechen. | Datei ist vorhanden und nicht leer; Speicherort wird bestätigt. Eine vorhandene Datei wird nicht überschrieben; bei Abbruch wird nichts gespeichert. |
| W05 Veränderung | Nach dem Backup `Testperson Beta` anlegen. | Beide Testpersonen sind auswählbar. |
| W06 Negativ-Restore | Backup mit falscher Passphrase und anschließend mit falschem Owner-Passwort oder bereits verwendetem TOTP-Code wiederherstellen. | Fehlermeldung; beide Testpersonen bleiben erhalten. |
| W07 Restore | Korrekte Backup-Passphrase eingeben, Warnung prüfen, optional aktuelle Daten in eine neue Datei sichern. Ersetzen bestätigen und Owner-Passwort sowie frischen TOTP-Code eingeben; nach Restore erneut entsperren. | Erneute Anmeldung erforderlich; Alpha und dessen drei Timeline-Einträge vorhanden, Beta fehlt. |
| W08 Sperren | `Sperren` wählen und mit Passwort und frischem TOTP-Code wieder entsperren. | Geschützte Daten verschwinden und erscheinen erst nach erfolgreicher Anmeldung. |
| W09 Negativ-Anmeldung | Nach Sperren falsches Passwort bzw. falschen TOTP-Code verwenden; anschließend mit gültigen Daten anmelden. | Falsche Daten werden abgelehnt; gültige Anmeldung funktioniert mit einem noch nicht verwendeten TOTP-Code. |
| W10 Beenden/Neustart | App schließen; Prozessliste prüfen; neu starten und anmelden. | Sidecar endet ebenfalls; erneuter Start und persistierte Daten funktionieren offline. |
| W11 Mehrfachstart | Bei laufender App ein zweites Exemplar starten; Prozesse, Meldungen und Datenbestand beobachten. | Keine konkurrierenden Instanzen/Seiteneffekte; ansonsten als Fehler bzw. offene Sicherheitsgrenze dokumentieren. |
| W12 IPC-Basistest | Bei laufender App deren Sidecar-PID und lokalen TCP-Port ermitteln. Plain-HTTP-Anfrage ohne Geheimnis versuchen, danach eine HTTPS-Anfrage ohne IPC-Header senden. | HTTP wird nicht verwendet; HTTPS ohne Vertrauen zum ephemeren Zertifikat scheitert im TLS-Handshake. Selbst bei manuell akzeptiertem Zertifikat wird eine Anfrage ohne IPC-Header mit HTTP 403 abgewiesen. Kein Testbeweis für Same-User-Isolation. |
| W13 Dokumentgrenze | Unterstützte synthetische Textdatei über 10 MiB bzw. ungültige PDF-Datei importieren. | Import wird abgewiesen und kein neuer Timeline-Eintrag erzeugt. |
| W14 Wiederherstellung ohne Owner | In einem separaten, frischen Windows-Testprofil die App starten und auf dem Startbildschirm das Backup aus W04 mit falscher, danach richtiger Backup-Passphrase auswählen. Mit dem ursprünglichen Owner-Passwort und einem frischen TOTP-Code entsperren. | Falsche Passphrase wird abgewiesen; korrektes Backup wird wiederhergestellt und Alpha erscheint nach Entsperrung. Ein bereits vorhandener Owner wird nicht überschrieben. |
| W15 Anderer Owner | Im separaten Testprofil neuen Owner anlegen und Daten erfassen. Backup aus W04 wählen, Warnung prüfen, aktuelles Backup unter neuem Namen erstellen und mit aktuellem Owner-Passwort und frischem TOTP ersetzen. | Ursprüngliche Backup-Datei unverändert; nach Ersetzen Anmeldung mit ursprünglichem Owner und dessen TOTP möglich; separat gespeichertes Backup bleibt vorhanden. Abbruch verändert nichts. |
| W16 Backup-Verlauf | Bei neuem Owner Hinweis auf fehlendes Backup prüfen; Backup speichern, Sperren/Entsperren und App-Neustart durchführen. Ein weiteres Backup innerhalb derselben Minute mit demselben Namen versuchen; danach mit neuem Namen speichern. | Lokaler Name enthält Datum und Uhrzeit. Der Verlauf zeigt erfolgreiche Speicherungen mit Datum und Pfad auch nach Neustart; die vorhandene Datei wird nicht überschrieben und der fehlgeschlagene Versuch nicht erfasst. |
| W17 Erinnerung und Restore | In isolierter Testumgebung Systemzeit kontrolliert um mehr als 14 Tage vorstellen; TOTP-Uhr beachten. Danach ein älteres Backup wiederherstellen und Verlauf vergleichen. | Nach über 14 Tagen erscheint der Hinweis mit Tageszahl. Nach Restore entspricht der Verlauf dem Snapshot vor dem Speichern der wiederhergestellten Datei; spätere Einträge fehlen. Systemzeit anschließend zurückstellen. |

Für W12 im separaten PowerShell-Fenster (nicht im Entwicklungsmodus starten;
`LIFELEDGER_DEV_MODE` darf nicht gesetzt sein):

```powershell
Get-Process lifeledger-api
Get-NetTCPConnection -State Listen -OwningProcess <PID>
try {
  Invoke-WebRequest "http://127.0.0.1:<Port>/api/v1/health" -UseBasicParsing
} catch {
  "Plain HTTP rejected: $($_.Exception.Message)"
}
```

PID und Port durch tatsächlich ermittelte Werte ersetzen. Eine HTTPS-Anfrage
mit Standard-Zertifikatsprüfung muss wegen des selbstsignierten, nicht
installierten Zertifikats ebenfalls scheitern. Die Tauri-Anwendung selbst
validiert mit ihrem angehefteten Zertifikat. W12 prüft nicht die Isolation
gegen einen Prozess desselben Windows-Benutzers. Scheitert W11 oder der
HTTPS-Start, bleibt das IPC-Gate offen. Erst nach allen Tests Netzwerkadapter
wieder aktivieren.

## Auszufüllendes Formular

```text
Tester/in (optional):                 Datum:
Commit-SHA / PR:
Windows-Version / Architektur:
VM oder Gerät / frisches Benutzerprofil:
Buildquelle (lokal / Actions) / Installer-Typ:
Python / Node / Rust:
Build Sidecar:      bestanden / fehlgeschlagen / nicht durchgeführt
Build Installer:    bestanden / fehlgeschlagen / nicht durchgeführt
Backend-Tests:      bestanden / fehlgeschlagen / nicht durchgeführt
Netzwerk für W01–W10 deaktiviert und geprüft: ja / nein

W01:                W02:                W03:
W04:                W05:                W06:
W07:                W08:                W09:
W10:                W11:                W12:
W13:                W14:                W15:

Abweichungen / bereinigte Fehlermeldungen:
Nicht durchgeführte Schritte und Grund:
Gesamtergebnis: bestanden / fehlgeschlagen / nicht vollständig
Bestätigung: Nur synthetische Daten verwendet: ja / nein
```

**Gesamtergebnis bestanden** nur, wenn Build und alle Tests bestanden und
W01–W10 tatsächlich offline durchgeführt wurden. Auch dann bleibt die
Windows-IPC-Sicherheitsprüfung separat offen, bis Same-User-Grenze,
gegenseitige Authentisierung und Startup-Race fachlich verifiziert sind.
Die frühere Port-Race-Schwachstelle wurde durch zertifikat-gepinntes TLS
adressiert; die Windows-Laufzeitprüfung bleibt ausstehend. Die
[Implementierungsgrenzen](../review/offene-informationen-erste-testversion.md)
beschreiben den verbleibenden Same-User-Vorbehalt.
