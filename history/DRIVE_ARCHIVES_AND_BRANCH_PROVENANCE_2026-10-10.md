# LYVRA Character Bot — historische Drive-Archive und Branch-Provenienz

Stand der Prüfung: 2026-10-10. Dokumentation allein; **keine Runtime-, Release- oder Authority-Promotion**.

## Historische Google-Drive-Ablagen

- [Canonical: 666SOUNDsDESIGn_LYVRA_AI_BOT](https://drive.google.com/drive/folders/1OV71M72SkjNw9SvtsMgKNMnfvi-9HiL1)
- [PC-Recovery: 666SOUNDsDESIGn_LYVRA_AI_BOT_PC_RECOVERY](https://drive.google.com/drive/folders/1nNLGH04WikSi2d133ZAAkgA2YmolPuuV)

Die Archive sind **historische Entwicklungs-/Recovery-Evidenz**, nicht automatisch aktuelle GitHub-Live-Runtime oder fremde native Authority. Drive-Inhalte nur nach gezieltem Readback interpretieren.

## Verifiziertes historisches v1.8.0-Paar (hochgeladene Original-ZIPs)

- Paketbezeichnung: `666SOUNDsDESIGn_LYVRA_AI_BOT_v1_8_0_BOOT_AUTHORITY_WORKER_INTEGRATION`
- Canonical- und PC-Recovery-Archiv: je 518018 Bytes, je 110 ZIP-Einträge; `testzip` für beide PASS.
- SHA-256 beider Originaldateien (identisch):
  `54ec98dc39307f4fb12159a0ae0fa42adf91fe6bfca22d5bb4a89bab5b306241`
- **Nicht** als GitHub-Release oder aktive Bot-Runtime markieren, solange nicht unabhängig nachgewiesen.

## Zwei vorhandene Repository-Branches (GitHub-Abgleich)

| Branch | HEAD beim Audit | Einordnung |
|---|---|---|
| `lyvrabot` | `4d62614846a7334aa17a9e0fad086f2bd671bfd9` (2026-10-02) | Default-/Hauptlinie, README und RELEASE_MANIFEST.json v1.7.1; enthält produktive issue-only Native-Delta-Watch-Dateien |
| `lyvrabot-dev-native-livecircle-20261002` | `be37a3af264ea30e2d40c5486b7142dda4bd6ef4` (2026-10-08) | **Neuere Bot-DEV-Entwicklung**, Bridge/Discord/LiveCircle und Tests, aber keine bestätigte Produktiv-Promotion; README/Release-Manifest weiter v1.7.1 |

Vergleich `lyvrabot...lyvrabot-dev-native-livecircle-20261002` beim Audit: **diverged**, DEV **80 ahead / 3 behind**. DEV ist nicht bloß altes Backup. Umgekehrt fehlen auf DEV drei Hauptbranch-Dateien: `.github/workflows/native-update-todos.yml`, `automation/native_update_todos.py` und `automation/test_native_update_todos.py`.

## Schutz und nächste Gates

1. Beide Branches und die historischen Drive-Pakete unverändert bewahren. Kein Force-Merge, Reset, Branch-Delete oder automatisches v1.8.0-Overlay.
2. Aktuellen nativen LYVRA-Current separat verifizieren; Native bleibt Identitätsautorität, Bot bleibt Adapter.
3. Release-/History-Inventur und Konfliktprüfung mit gepinnten SHAs vor einer Integration.
4. Bot standardmäßig Discord-offline; lokaler Hardlock und unabhängiges Worker-Gate **vor** Login; Familien-/Radio-/Verba-Isolation prüfen.
5. Erst nach Offline-Tests, Review, Recovery-/Readback und gesonderter Freigabe Deployment erwägen.

Diese Datei ist eine **nicht-autoritative Evidenz- und Navigationsergänzung**, keine Änderung am Bot oder seinen Live-Pointern.
