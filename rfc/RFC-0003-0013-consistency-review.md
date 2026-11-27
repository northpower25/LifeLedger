# Konsistenzprüfung RFC-0003–RFC-0013

Die geprüften RFCs sind Entwürfe. Diese Übersicht trennt uneinheitliche Bezeichnungen und nicht abgestimmte Verträge von möglichen Widersprüchen, die wegen fehlender Definitionen noch nicht abschließend beurteilt werden können. Abschnittsnummern beziehen sich jeweils auf die nummerierten Abschnitte des genannten RFC.

## Nicht abgestimmte Verträge

### RFC-0003 §7 und RFC-0008 §13: Bezeichnungen für Freigabebereiche

RFC-0003 verwendet im Consent-Beispiel Ressourcenkategorien wie `Medication` und `Allergies`; RFC-0008 nennt `MEDICATION_ACCESS` und `ALLERGY_ACCESS` für entsprechende Freigabebereiche. Es fehlt eine verbindliche Zuordnung: Sind dies unterschiedliche Repräsentationen, Consent-Scopes oder Capabilities? Die Beispiele allein belegen keine gegensätzliche Zugriffsentscheidung.

### RFC-0004 §§6–9, 14 und RFC-0005 §22: Event-Berechtigungen

RFC-0005 nennt `CONSENT_MANAGEMENT` als Beispiel für die Berechtigung zu `CONSENT_REVOKED`; dieser Bezeichner ist im Capability-Katalog von RFC-0004 nicht aufgeführt. Zudem unterscheidet RFC-0005 nicht konkret zwischen Rechten zum Veröffentlichen und zum Konsumieren. Der Katalog und der Event-Vertrag sollten abgestimmt werden; es ist nicht festgelegt, dass der Katalog abschließend ist.

## Mögliche Widersprüche und unklare Grenzen

### RFC-0003 §§4, 7 und RFC-0008 §§4–6, 17: Consent-Subjekt und Familienvertretung

RFC-0003 ordnet Gesundheitsdaten einem `HealthProfile` zu, verwendet im Consent-Beispiel aber eine User-ID als `owner`. RFC-0008 bezeichnet bei Minderjährigen das Kind als Owner und die Sorgeberechtigten als Guardian. Offen ist, ob der Consent einem Nutzer oder Profil zugeordnet wird und wie die Vertretung im Namen des Profils handelt. Ein direkter Rollenwiderspruch ist damit nicht belegt.

### RFC-0003 §§6, 9 und RFC-0008 §§6, 12: Delegationsumfang

RFC-0003 nennt Owner, Guardian und Proxy als delegationsfähig. RFC-0008 beschreibt Guardian-zu-Caregiver-Delegation und lässt Proxy-Delegation optional. Zu klären ist, unter welchen Bedingungen eine Weiterdelegation zulässig ist und wie Scope, Ablauf und Widerruf der ursprünglichen Befugnis sie begrenzen.

### RFC-0004 §4 und RFC-0008 §24: Rolle im Autorisierungspfad

RFC-0004 nennt `Identity → Consent → Capability → Resource Access`, RFC-0008 dagegen `Role → Consent → Capability → VitaFabric → FHIR`. Es fehlt die Festlegung, ob die Rolle Teil des Identitätskontexts oder eine zusätzliche Prüfung ist und wie beide Pfade zusammengehören.

### RFC-0003 §11 und RFC-0005 §§17–18, 22–25: Widerruf und Event-Replay

RFC-0003 verlangt einen sofortigen Widerruf aktiver Sitzungen, Plugin-Berechtigungen und Tokens. RFC-0005 sieht Event-Persistenz, Replay und ein `CONSENT_REVOKED`-Event vor. Nicht geregelt ist, wie Warteschlangen und Replay nach einem Widerruf erneut autorisiert werden. Ohne diese Regel können zuvor erlaubte Zugriffe mit veralteten Entscheidungen fortgesetzt werden.

### RFC-0008 §§20–21 und RFC-0010 §§5–6, 23–24: Widerruf bei Offline-Synchronisation

RFC-0008 fordert sofortigen Widerruf und Audit; RFC-0010 sieht die Synchronisation von Freigaben zwischen Geräten vor. Ein getrenntes Gerät kann einen externen Widerruf nicht sofort empfangen. Festzulegen sind die tatsächlich erreichbare Wirkung und das Verhalten bei Offline-Zugriff sowie Wiederverbindung. Eine restriktivere Offline-Regel kann die lokale Verfügbarkeit beeinträchtigen; bereits offengelegte Daten lassen sich nicht zurückrufen.

### RFC-0004 §§3–4 und RFC-0013 §§3, 7, 17: Autorisierung des FHIR-Imports

RFC-0004 verlangt Consent und Capability für Ressourcenzugriffe. RFC-0013 zeigt den Importpfad `Mapping → FHIR → Validation → Consent → Storage` und fordert in §17 zusätzlich eine Capability-Prüfung für jeden Zugriff. Im Importpfad fehlt eine explizite Capability-Prüfung. Zu klären ist, an welcher Stelle sie erfolgt und welche Einwilligung für die Speicherung erforderlich ist; eine Ausnahme ist nicht festgelegt.

### RFC-0006 §§9, 11, 15: Technische Isolationsgrenzen

RFC-0006 verbietet direkten Netzwerk- und Secret-Zugriff, erlaubt jedoch Zugriff über freigegebene APIs und setzt für das Netzwerk `NETWORK_ACCESS` voraus. Dies ist nicht zwingend widersprüchlich: Die APIs können vermittelten Zugriff ermöglichen. Offen bleiben die technische Durchsetzung dieser Grenze und die sichere Verwendung von Zugangsdaten über die Secret API.

## Übergreifende Vollständigkeitslücken

- **Autorisierungs- und Consent-Schema:** Kanonische Felder für Nutzer bzw. Profil, Ressource, Aktion, Zweck, Ablauf, Delegation und Widerruf sowie die Zuordnung zwischen Scopes und Capabilities fehlen. Relevant: RFC-0003 §§4–9, RFC-0004 §§4–14, RFC-0008 §§12–14.
- **Event-Datenvertrag:** Konkrete versionierte Event-Schemas sowie Regeln für Payloads bzw. Referenzen, Datenschutz und Zugriff auf persistierte Events und Replay fehlen. Relevant: RFC-0005 §§5, 17–22, 25–28; RFC-0003 §11; RFC-0013 §16.
- **Paketvertrag für Anwendungen und Plugins:** Maschinenprüfbare Manifeste, API-Kompatibilität, Signaturprüfung und durchgängige Installations-, Update- und Rollback-Semantik sind nicht spezifiziert. Relevant: RFC-0006 §§6–8, 18, 23; RFC-0007 §§18–20; RFC-0009 §§11–15, 22–23.
- **Zero-Knowledge-Protokoll:** Schlüsselerzeugung und -schutz, Geräteaufnahme und -widerruf, Rotation, Wiederherstellung und verschlüsselte Konfliktauflösung benötigen konkrete Protokolle. Relevant: RFC-0010 §§6–13, 18–20, 29.
- **FHIR-Datenverträge:** Konkrete Profile, Terminologie-Bindungen, Provenienzrepräsentation, Qualitätszustandsübergänge und Migrationsartefakte fehlen. Relevant: RFC-0013 §§4–11, 18–20.
- **Governance und Betrieb:** Entscheidungsrechte, Verantwortlichkeiten und überprüfbare Verfahren für Sicherheitsvorfälle, Signaturschlüssel, Releases und Nachfolge sind nicht durchgängig festgelegt. Relevant: RFC-0012 §§8–16, 24–33; RFC-0009 §§19–21, 25, 30–32.
