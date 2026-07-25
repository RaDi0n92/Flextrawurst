# Flextrawurst Game Source Ingress

Dieser Körper zieht die zehn ausgewählten Originalarchive kollisionssicher in
`/root/werkraum/engine/flextrawurst-game/` ein.

Er prüft vor jeder Änderung Dateigröße, SHA-256, ZIP-Integrität und beim
333-MD-Körper die exakte Anzahl von 333 Markdown-Dateien. Bestehende identische
Dateien werden übersprungen. Abweichende bestehende Dateien führen zu einem
harten Abbruch statt zu Überschreiben oder stiller Vermischung.

Standardablauf auf dem VPS:

```bash
python3 -m tools.game_source_ingress.ingest
python3 -m tools.game_source_ingress.ingest --apply
```

Die Archive werden unverändert unter `sources/original_archives/` bewahrt und
zusätzlich in getrennte Herkunftsbereiche extrahiert. Der Lauf erzeugt
`SOURCE_INGRESS_REPORT.json` und ergänzt `GAME_MANIFEST.json` um einen
`source_ingress`-Knoten. Vor dieser Ergänzung wird ein datierter Backupkörper
angelegt.
