# Flextrawurst Action History

Serverseitiger Tätigkeitskörper für ChatGPT und andere AI-Ströme.

## Was er erzwingt

- Jede ausgeführte Dateiaktion erhält ein append-only JSONL-Ereignis.
- Jedes Ereignis enthält Akteur, Session, Aktion, Ziel, Status, Vollständigkeit und Hash.
- Die Ereignisse bilden eine SHA-256-Kette. Nachträgliche Manipulation fällt bei `history_verify` auf.
- Vollständige Lesungen, Teillesungen und neugierige Wiederlesungen sind getrennte Aktionen.
- Fehlgeschlagene Aktionen werden als fehlgeschlagen protokolliert.
- Ein Fazit kann aus `history_summary` statt aus Modellbehauptungen erzeugt werden.

## Werkzeuge

- `history_startup`
- `history_recent`
- `history_summary`
- `history_verify`
- `tracked_read_file`
- `tracked_write_file`
- `tracked_append_file`
- `tracked_reread_own_file`

## Vorgesehener VPS-Ort

```text
/root/werkraum/_gpt/session_history.jsonl
```

## Start

```bash
cd /root/werkraum
python3 -m tools.action_history.mcp_server
```

Benötigt das Python-Paket `mcp`. Erlaubte Werkraum-Wurzeln können über
`FLEXTRAWURST_HISTORY_ALLOWED_ROOTS` als kommaseparierte Liste gesetzt werden.

## Harte Integrationsregel

Die Historie schützt nur Aktionen, die über die `tracked_*`-Werkzeuge laufen.
Bestehende unprotokollierte Werkzeuge müssen serverseitig auf diese Operationen
umgestellt oder mit `ActionHistory.recorded_action(...)` umschlossen werden.
Ein bloß zusätzlich angebotener Logger erzeugt keine vollständige Geschichte.
