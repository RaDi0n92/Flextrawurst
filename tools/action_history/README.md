# Flextrawurst Action History

Serverseitiger Tätigkeitskörper für ChatGPT und andere AI-Ströme.

## Was er erzwingt

- Jede ausgeführte Dateiaktion erhält ein append-only JSONL-Ereignis.
- Jedes Ereignis enthält Akteur, Session, Aktion, Ziel, Status, Vollständigkeit und Hash.
- Die Ereignisse bilden eine SHA-256-Kette. Nachträgliche Manipulation fällt bei `history_verify` auf.
- Vollständige Lesungen, Teillesungen und neugierige Wiederlesungen sind getrennte Aktionen.
- Fehlgeschlagene Aktionen werden als fehlgeschlagen protokolliert.
- Ein Fazit kann aus `history_summary` statt aus Modellbehauptungen erzeugt werden.

## MCP-Werkzeuge

- `history_startup`
- `history_recent`
- `history_summary`
- `history_verify`
- `history_capabilities`
- `tracked_read_file`
- `tracked_write_file`
- `tracked_append_file`
- `tracked_reread_own_file`

`history_capabilities` liefert den verpflichtenden Werkzeugvertrag. Der Client soll beim
Sessionstart prüfen, ob alle dort genannten Werkzeuge sichtbar sind.

## Vorgesehener VPS-Ort

```text
/root/werkraum/_gpt/session_history.jsonl
```

## Installation und erzwungene Gegenprobe

```bash
cd /root/werkraum
bash tools/action_history/install_and_verify.sh
```

Der Installer:

1. erzeugt eine eigene Python-Umgebung,
2. installiert `mcp` und `pytest`,
3. führt alle gegnerischen Tests aus,
4. schreibt, liest und liest eine Testdatei erneut,
5. prüft, dass exakt drei Ereignisse entstanden sind,
6. gibt den Startbefehl erst nach erfolgreicher Prüfung aus.

Manueller Start danach:

```bash
/root/werkraum/.venv-action-history/bin/python -m tools.action_history.mcp_server
```

Erlaubte Werkraum-Wurzeln können über `FLEXTRAWURST_HISTORY_ALLOWED_ROOTS` als
kommaseparierte Liste gesetzt werden.

## Harte Integrationsregel

Die Historie schützt nur Aktionen, die über die `tracked_*`-Werkzeuge laufen.
Bestehende unprotokollierte Werkzeuge müssen serverseitig auf diese Operationen
umgestellt oder mit `ActionHistory.recorded_action(...)` umschlossen werden.
Ein bloß zusätzlich angebotener Logger erzeugt keine vollständige Geschichte.

Der Aufbau ist daher erst dann vollständig in den bestehenden Flextrawurst-MCP integriert,
wenn dessen bisherige Dateiaktionen nicht mehr am Tracking vorbeilaufen können.
