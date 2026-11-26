# Roadmap: LifeWeaver

LifeWeaver verantwortet optionale AI-Provider, MCP, Agenten, RAG,
Wissensgraph und persönliche Health-Twin-Funktionen. Alles ist geplant;
LifeLedger benötigt LifeWeaver nicht für den lokalen Kern. Anbieter werden
über providerneutrale Adapter eingebunden; gesundheitsbezogene Provider-Plugins
erhalten Daten nur über freigegebene VitaFabric-Verträge und unter expliziter
Einwilligung. Siehe
[Gesamt-Roadmap](project.md).

## Stufen

| Stufe | Ergebnis und Abhängigkeiten | Tests und Abnahme |
| --- | --- | --- |
| W0 – Grenzen und Gefahren | Zweckbestimmung und Nichtziele, Bedrohungsmodell, providerneutrale Provider-Plugin-Schnittstellen, MCP-Rollen, Identitäts-/Consent-Grenzen, Datenminimierung und lokale Ausführung per RFC/ADR spezifizieren. Keine Diagnose- oder Behandlungsempfehlungsfunktion voraussetzen. | Security-, Produkt- und Interoperabilitätsreview einschließlich Prompt-Injection, unzulässiger Tool-Aufrufe und Datenabfluss. |
| W1 – Lokale Verträge | Nach Daten- und Sicherheitsverträgen ein synthetisches, lokal ausführbares Test-Backend und providerneutrale Schnittstellen schaffen; keine Bindung an einen einzelnen Anbieter. | Vertrags- und Fehlertests mit mindestens zwei austauschbaren Testimplementierungen; lokal ohne Netzwerk, ohne Geheimnisse und ohne Gesundheitsdaten-Zugriff. |
| W2 – Freigegebener Datenzugriff und MCP | MCP-Client/Server im festgelegten Umfang; Daten nur über VitaFabric und durch Identity-&-Consent-Regeln explizit freigegeben. Einwilligungswiderruf und Datenminimierung von Beginn an berücksichtigen. | MCP-Kompatibilität, verweigerte und widerrufene Rechte, eingeschränkter Kontext, Tool-Berechtigungen, Audit und Offline-Betrieb testen. |
| W3 – Optionale Provider und Erweiterungen | Nach eigenen Reviews lokale Modelle und optional externe Provider anbinden. Externe Übertragung nur nach ausdrücklicher Freigabe und transparentem Hinweis; lokale Nutzung darf davon nicht abhängen. | Providerwechsel, Ausfall, Timeouts, kein stiller Cloud-Fallback, keine Datenübertragung ohne Zustimmung und Widerruf prüfen. |
| W4 – RAG, Agenten und Health Twin | Jede Fähigkeit separat spezifizieren und nach Risiko priorisieren; Speicherdauer, Herkunft und Rechte abgeleiteter Daten klären. | Tests für Quellenbezug, Zugriffsbeschränkung, Löschung/Widerruf, schädliche Eingaben, Halluzinationen und Fehlermeldungen; unabhängige Sicherheits- und Zweckbestimmungsprüfung. |

## Offene Fragen und Vorschläge

- Welcher konkrete lokale Nutzen rechtfertigt den ersten AI-Anwendungsfall,
  und welche Leistung ist auf welchen Geräten offline realistisch?
- Wie werden Einwilligung und Widerruf für Prompts, Kontext, Embeddings,
  Caches und eventuell bereits an Dritte übertragene Daten durchgesetzt?
- Welche MCP-Versionen, Tool-Rechte und Vertrauensgrenzen gelten? Wie werden
  untrusted Inhalte von Anweisungen und Tool-Freigaben getrennt?
- Wie gelten dieselben VitaFabric-, Consent- und Audit-Grenzen für mehrere
  Anwendungen und optionale Deployment-Szenarien, ohne lokalen Betrieb oder
  einen Providerwechsel von einem Cloud-Dienst abhängig zu machen?
- Wie werden Berechtigungen für Provider-Plugins unabhängig von
  Authentifizierung und Rollen begrenzt, angezeigt, geprüft und widerrufen?
- Welche Funktionen wären regulatorisch oder medizinisch problematisch?
  Wer prüft den Abstand zu Diagnose, Therapie und klinischer Entscheidung?
- Vorschlag: Zuerst eine klar begrenzte, quellengebundene Funktion mit
  synthetischen Daten evaluieren; keinen autonomen Agenten als Voraussetzung
  für den Produktkern einführen.
