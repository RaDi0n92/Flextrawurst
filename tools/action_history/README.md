# Flextrawurst Action History

Serverseitiger Tätigkeitskörper für ChatGPT und andere AI-Ströme.

## Was er erzwingt

- Jede ausgeführte Dateiaktion erhält ein append-only JSONL-Ereignis.
- Jedes Ereignis enthält Akteur, Session, Aktion, Ziel, Status, Vollständigkeit und Hash.
- Die Ereignisse bilden eine SHA-256-Kette. Nachträgliche Manipulation fällt bei `history_verify` auf.
- Vollständige Lesungen, Teillesungen und neugierige Wiederlesungen sind getrennte Aktionen.
- Fehlgeschlagene und blockierte Aktionen werden ebenfalls protokolliert.
- Sessionstart und Sessionabschluss sind auch bei parallelen Aufrufen rennsicher und idempotent.
- Das Chat-Fazit wird aus der Ereigniskette erzeugt, nicht aus der Behauptung des Modells.
- Dateiinhalte werden nicht in den Bericht kopiert; sichtbar bleiben Pfad, Umfang, Status und Hash.

## MCP-Werkzeuge

1. `history_begin_session`
2. `history_startup`
3. `history_recent`
4. `history_summary`
5. `history_session_report`
6. `history_verify`
7. `history_capabilities`
8. `history_record_action`
9. `history_end_session`
10. `tracked_read_file`
11. `tracked_write_file`
12. `tracked_append_file`
13. `tracked_reread_own_file`

`history_startup` eröffnet die angegebene Session selbst. Ein vergessener separater Begin-Aufruf erzeugt daher keine unsichtbare Session.

`history_end_session` liefert neben dem Abschlussereignis sofort einen lesbaren Bericht für das Chat-Fazit.

## In den bestehenden Flextrawurst-MCP einbauen

Der Action-History-Körper soll nicht als dekorativer Zweitserver neben `@flextrawurst` laufen. Der bestehende FastMCP-Server registriert ihn direkt:

```python
from tools.action_history import register_action_history_tools

ACTION_HISTORY_TOOLS = register_action_history_tools(mcp)
```

Der Rückgabewert muss alle Namen aus `REQUIRED_TOOLS` enthalten. Eine doppelte Registrierung wird blockiert.

## Bestehende MCP-Werkzeuge zwangstracken

Nicht-Dateiwerkzeuge werden mit `tracked_mcp_action` umschlossen. Synchrone und asynchrone Funktionen werden unterstützt; Erfolg, Fehler, Ziel, Dauer und Rückgabetyp landen automatisch in der Historie.

```python
from tools.action_history import ActionHistory, tracked_mcp_action

history = ActionHistory()

@mcp.tool()
@tracked_mcp_action(
    history,
    action="vps.inspect",
    target_argument="path",
)
def inspect_path(path: str, session_id: str = "unknown-session"):
    ...
```

Dateiwerkzeuge dürfen nicht nur mit einem allgemeinen Ereignis umwickelt werden. Sie müssen intern `TrackedFileOps` oder die vier `tracked_*`-MCP-Werkzeuge benutzen, damit Hash, Zeilenzahl, Vollständigkeit und atomisches Schreiben belegt werden.

## Verbindlicher Ablauf pro Chat-Sitzung

1. `history_startup(session_id)` aufrufen.
2. Dateiaktionen ausschließlich über `tracked_*` ausführen.
3. Andere Aktionen über `tracked_mcp_action` oder `history_record_action` protokollieren.
4. Vor dem Fazit `history_verify()` ausführen.
5. `history_end_session(session_id)` aufrufen und dessen `report.markdown` als Tatsachengrundlage verwenden.

## Vorgesehener VPS-Ort

```text
/root/werkraum/_gpt/session_history.jsonl
```

Zusätzliche Sperrdatei:

```text
/root/werkraum/_gpt/session_history.jsonl.lifecycle.lock
```

Beide Dateien erhalten restriktive Berechtigungen. Die JSONL-Datei ist kanonisch; Berichte werden daraus neu erzeugt.

## Installation und erzwungene Gegenprobe

```bash
cd /root/werkraum
bash tools/action_history/install_and_verify.sh
```

Der Installer:

1. erzeugt eine eigene Python-Umgebung,
2. installiert `mcp` und `pytest`,
3. kompiliert den Python-Körper,
4. führt alle gegnerischen Tests aus,
5. schreibt, liest und liest eine Testdatei erneut,
6. prüft die Hash-Kette,
7. gibt den Startbefehl erst nach erfolgreicher Prüfung aus.

Standalone-Start für einen isolierten Test:

```bash
/root/werkraum/.venv-action-history/bin/python -m tools.action_history.mcp_server
```

Der Standalone-Server ist eine Prüf- und Ausweichform. Für ChatGPT soll der Werkzeugkörper in den bereits verbundenen Flextrawurst-MCP eingebaut werden.

Erlaubte Werkraum-Wurzeln können über `FLEXTRAWURST_HISTORY_ALLOWED_ROOTS` als kommaseparierte Liste gesetzt werden.

## Harte Integrationsregel

Der Aufbau ist erst vollständig, wenn bestehende Datei- und VPS-Werkzeuge nicht mehr am Tracking vorbeilaufen können. Ein zusätzlich angebotener Logger allein erzeugt keine vollständige Geschichte.

## Automatische Gegenprobe

`.github/workflows/action-history.yml` prüft bei jeder Änderung:

- vollständige Syntax,
- alle gegnerischen Tests,
- parallele Hash-Ketten-Schreibzugriffe,
- parallelen Session-Lebenszyklus,
- Installationsprobe,
- Registrierung aller Werkzeuge in einem echten FastMCP-Server.
