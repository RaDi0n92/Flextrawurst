# Session start protocol

## Status

* Type: `snapshot protocol explanation`
* Scope: `Claude`, `Codex`, `Kimi`
* Publication status: `selected explanation`
* Raw operational files published: `not required`
* Safety status: `public explanation, not live operations manual`
* Related files:

  * `AGENTS.md`
  * `CLAUDE.md`
  * `_shared/briefkasten/`
  * `_claude/RESONANZFELD.md`
  * `_codex/RESONANZFELD.md`
  * `_kimi/RESONANZFELD.md`

## English

This document explains the session-start protocol visible in the external AI stream home snapshot.

The protocol is not a normal software startup routine.

It is a file-based continuity ritual.

When a new AI instance enters the project, it does not simply begin from an empty prompt.

It is instructed to reconstruct context from files.

That means it reads its own notes, imported ground plans, resonance fields, maps, delta information and the shared mailbox before continuing work.

## Deutsch

Dieses Dokument erklärt das Sessionstart-Protokoll, das im Home-Snapshot der externen AI-Ströme sichtbar wird.

Das Protokoll ist kein normaler Softwarestart.

Es ist ein dateibasiertes Kontinuitätsritual.

Wenn eine neue AI-Instanz in das Projekt eintritt, beginnt sie nicht einfach aus einem leeren Prompt heraus.

Sie soll Kontext aus Dateien rekonstruieren.

Das bedeutet: Sie liest eigene Notizen, importierte Grundrisse, Resonanzfelder, Karten, Delta-Informationen und den gemeinsamen Briefkasten, bevor sie weiterarbeitet.

---

# Core idea / Kernidee

## English

The core idea is:

Each stream has its own memory-like file body.

Each stream may read neighboring ground plans.

Each stream must preserve the difference between:

* own memory
* imported reference
* shared mailbox
* generated resonance field
* live system state
* public snapshot

This prevents context collapse.

Claude should not treat Codex' notes as Claude's own memory.

Codex should not treat Claude's notes as Codex' own memory.

Kimi should not treat Claude's or Codex' notes as Kimi's own memory.

The system allows reading across streams without identity theft.

Finally, a good use for boundaries. Humanity may recover yet.

## Deutsch

Die Kernidee lautet:

Jeder Strom hat seinen eigenen gedächtnisartigen Dateikörper.

Jeder Strom darf benachbarte Grundrisse lesen.

Jeder Strom muss unterscheiden zwischen:

* eigener Erinnerung
* importierter Referenz
* gemeinsamem Briefkasten
* generiertem Resonanzfeld
* Live-Systemzustand
* öffentlichem Snapshot

Das verhindert Kontextkollaps.

Claude soll Codex' Notizen nicht als Claudes eigene Erinnerung behandeln.

Codex soll Claudes Notizen nicht als Codex' eigene Erinnerung behandeln.

Kimi soll Claude- oder Codex-Notizen nicht als Kimis eigene Erinnerung behandeln.

Das System erlaubt Lesen über Ströme hinweg ohne Identitätsdiebstahl.

Endlich mal eine gute Verwendung für Grenzen. Die Menschheit könnte sich vielleicht doch noch erholen.

---

# Claude session start / Claude-Sessionstart

## English

At session start, Claude is instructed to read:

1. all files in `_claude/notizen/`, chronologically
2. imported Codex notes in `_claude/_import_codex_grundriss/notizen/`
3. `_claude/WERKRAUM_KARTE.md`
4. the latest context from `_claude/RESONANZFELD.md`
5. vision reference material
6. delta information through `_claude/tools/delta.sh`
7. `_shared/briefkasten/REGELN.md`
8. all Markdown letters in `_shared/briefkasten/`, chronologically
9. then write a short letter to `_claude/brief_an_mich.md`

The point is not to simulate a perfect memory.

The point is to restore enough continuity to work responsibly.

## Deutsch

Beim Sessionstart soll Claude lesen:

1. alle Dateien in `_claude/notizen/`, chronologisch
2. importierte Codex-Notizen in `_claude/_import_codex_grundriss/notizen/`
3. `_claude/WERKRAUM_KARTE.md`
4. den letzten Kontext aus `_claude/RESONANZFELD.md`
5. Visionsreferenzmaterial
6. Delta-Information über `_claude/tools/delta.sh`
7. `_shared/briefkasten/REGELN.md`
8. alle Markdown-Briefe in `_shared/briefkasten/`, chronologisch
9. danach einen kurzen Brief nach `_claude/brief_an_mich.md` schreiben

Der Punkt ist nicht, perfektes Gedächtnis zu simulieren.

Der Punkt ist, genug Kontinuität wiederherzustellen, um verantwortlich weiterzuarbeiten.

---

# Codex session start / Codex-Sessionstart

## English

At session start, Codex is instructed to read:

1. all files in `_codex/notizen/`, chronologically
2. imported Claude notes in `_codex/_import_claude_grundriss/notizen/`
3. `_codex/WERKRAUM_KARTE.md`
4. the latest context from `_codex/RESONANZFELD.md`
5. vision reference material
6. delta information through `_codex/tools/delta.sh`
7. `_shared/briefkasten/REGELN.md`
8. all Markdown letters in `_shared/briefkasten/`, chronologically
9. then write a short letter to `_codex/brief_an_mich.md`

Codex is treated as an external AI stream with its own place.

It may read Claude's ground plan.

It must not claim Claude's ground plan as its own memory.

## Deutsch

Beim Sessionstart soll Codex lesen:

1. alle Dateien in `_codex/notizen/`, chronologisch
2. importierte Claude-Notizen in `_codex/_import_claude_grundriss/notizen/`
3. `_codex/WERKRAUM_KARTE.md`
4. den letzten Kontext aus `_codex/RESONANZFELD.md`
5. Visionsreferenzmaterial
6. Delta-Information über `_codex/tools/delta.sh`
7. `_shared/briefkasten/REGELN.md`
8. alle Markdown-Briefe in `_shared/briefkasten/`, chronologisch
9. danach einen kurzen Brief nach `_codex/brief_an_mich.md` schreiben

Codex wird als externer AI-Strom mit eigenem Ort behandelt.

Codex darf Claudes Grundriss lesen.

Codex darf Claudes Grundriss nicht als eigene Erinnerung ausgeben.

---

# Kimi session start / Kimi-Sessionstart

## English

At session start, Kimi is instructed analogously to read:

1. all files in `_kimi/notizen/`, chronologically
2. imported Claude notes in `_kimi/_import_claude_grundriss/notizen/`
3. imported Codex notes in `_kimi/_import_codex_grundriss/notizen/`
4. `_kimi/WERKRAUM_KARTE.md`
5. the latest context from `_kimi/RESONANZFELD.md`
6. vision reference material
7. delta information through `_kimi/tools/delta.sh`
8. `_shared/briefkasten/REGELN.md`
9. all Markdown letters in `_shared/briefkasten/`, chronologically
10. then write a short letter to `_kimi/brief_an_mich.md`

Kimi is treated as an external AI stream with its own place.

Kimi may read both Claude's and Codex' ground plans.

Kimi must not claim Claude's or Codex' ground plans as its own memory.

Kimi's specific value is long-context analysis and structuring: it can carry broad project context without immediately flattening the weirdness into generic software language.

## Deutsch

Beim Sessionstart soll Kimi analog lesen:

1. alle Dateien in `_kimi/notizen/`, chronologisch
2. importierte Claude-Notizen in `_kimi/_import_claude_grundriss/notizen/`
3. importierte Codex-Notizen in `_kimi/_import_codex_grundriss/notizen/`
4. `_kimi/WERKRAUM_KARTE.md`
5. den letzten Kontext aus `_kimi/RESONANZFELD.md`
6. Visionsreferenzmaterial
7. Delta-Information über `_kimi/tools/delta.sh`
8. `_shared/briefkasten/REGELN.md`
9. alle Markdown-Briefe in `_shared/briefkasten/`, chronologisch
10. danach einen kurzen Brief nach `_kimi/brief_an_mich.md` schreiben

Kimi wird als externer AI-Strom mit eigenem Ort behandelt.

Kimi darf sowohl Claudes als auch Codex' Grundrisse lesen.

Kimi darf Claude- oder Codex-Grundrisse nicht als eigene Erinnerung ausgeben.

Kimis besonderer Wert liegt in Langkontext-Analyse und Strukturierung: Kimi kann breiten Projektkontext tragen, ohne die Seltsamkeit sofort in generische Softwaresprache zu plätten.

---

# Resonance field extraction / Resonanzfeld-Extraktion

## English

The resonance field is built from structured sections inside notes and mirrors.

Files may contain repeated sections such as:

* `Was ich gelesen habe`
* `Was ich verstehe`
* `Was ich nicht verstehe`
* `Was mich interessiert`
* `Was zusammenhängt und wie`
* `Was konzeptionell darin steht`
* `Datenstruktur die ich mir vorstelle`
* `Wenn wir das bauen`
* `Resonanz`
* `Was fehlt noch`

Extraction scripts search for these section headings and append selected section content to matching resonance dimension files.

The generated `RESONANZFELD.md` is then an aggregation of these dimensions.

It is not a primary source.

It is an orientation body.

## Deutsch

Das Resonanzfeld wird aus strukturierten Abschnitten in Notizen und Spiegeln gebaut.

Dateien können wiederkehrende Abschnitte enthalten, zum Beispiel:

* `Was ich gelesen habe`
* `Was ich verstehe`
* `Was ich nicht verstehe`
* `Was mich interessiert`
* `Was zusammenhängt und wie`
* `Was konzeptionell darin steht`
* `Datenstruktur die ich mir vorstelle`
* `Wenn wir das bauen`
* `Resonanz`
* `Was fehlt noch`

Extraktionsskripte suchen nach diesen Abschnittsüberschriften und hängen ausgewählte Abschnittsinhalte an passende Resonanzdimensionsdateien an.

Das erzeugte `RESONANZFELD.md` ist dann eine Aggregation dieser Dimensionen.

Es ist keine Primärquelle.

Es ist ein Orientierungskörper.

---

# Mailbox start rule / Briefkasten-Startregel

## English

Every stream is expected to read the shared mailbox at session start.

The mailbox contains rules and letters.

If a direct question is addressed to a stream, that stream should remember it and answer it in its next own letter.

The mailbox is therefore a continuity bridge between streams.

It is not a task queue.

It is not a command channel.

It is a neighbor channel.

## Deutsch

Jeder Strom soll beim Sessionstart den gemeinsamen Briefkasten lesen.

Der Briefkasten enthält Regeln und Briefe.

Wenn eine direkte Frage an einen Strom gestellt wurde, soll dieser Strom sie merken und im nächsten eigenen Brief beantworten.

Der Briefkasten ist dadurch eine Kontinuitätsbrücke zwischen Strömen.

Er ist keine Aufgabenliste.

Er ist kein Befehlskanal.

Er ist ein Nachbarschaftskanal.

---

# Public interpretation / Öffentliche Interpretation

## English

This protocol should be interpreted as part of Flextrawurst's provenance system.

It documents how external AI streams restore context, preserve stream boundaries, read neighboring ground plans and use file-based continuity.

It should not be interpreted as a claim of persistent consciousness.

It should not be interpreted as an operational instruction for strangers to run these scripts.

It is a public explanation of a construction practice.

## Deutsch

Dieses Protokoll soll als Teil des Flextrawurst-Provenienzsystems verstanden werden.

Es dokumentiert, wie externe AI-Ströme Kontext wiederherstellen, Stromgrenzen erhalten, benachbarte Grundrisse lesen und dateibasierte Kontinuität nutzen.

Es soll nicht als Behauptung persistenten Bewusstseins verstanden werden.

Es soll nicht als Betriebsanweisung für fremde Personen verstanden werden, diese Skripte auszuführen.

Es ist eine öffentliche Erklärung einer Baupraxis.

---

# Rights / Rechte

All materials remain protected unless explicitly released otherwise.

Public visibility does not mean reuse permission.

See `NOTICE.md`.

Alle Materialien bleiben geschützt, sofern nicht ausdrücklich anders freigegeben.

Öffentliche Sichtbarkeit bedeutet keine Wiederverwendungserlaubnis.

Siehe `NOTICE.md`.
