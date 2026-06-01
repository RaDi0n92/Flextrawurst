# Session start protocol

## Status

* Type: `snapshot protocol explanation`
* Scope: `Claude`, `Codex`, `Kimi`
* Publication status: `selected explanation`
* Safety status: `public explanation, not live operations manual`
* Related rooms:

  * `_claude`
  * `_codex`
  * `_kimi`
  * `_shared`

## English

This document explains the session-start protocol visible in the external AI stream rooms snapshot.

The protocol is not a normal software startup routine.

It is a file-based continuity ritual.

When a new AI instance enters the project, it is instructed to reconstruct context from files before continuing work.

It reads its own notes, imported ground plans, Werkraum maps, resonance fields, shared mailbox messages and other orientation material.

This reduces context drift.

It preserves provenance.

It does not create perfect memory.

It does not prove persistent consciousness.

It is a construction practice.

## Deutsch

Dieses Dokument erklärt das Sessionstart-Protokoll, das im Räume-Snapshot externer AI-Ströme sichtbar wird.

Das Protokoll ist kein normaler Softwarestart.

Es ist ein dateibasiertes Kontinuitätsritual.

Wenn eine neue AI-Instanz in das Projekt eintritt, soll sie Kontext aus Dateien rekonstruieren, bevor sie weiterarbeitet.

Sie liest eigene Notizen, importierte Grundrisse, Werkraum-Karten, Resonanzfelder, gemeinsame Briefkasten-Nachrichten und weiteres Orientierungsmaterial.

Das reduziert Kontextdrift.

Es erhält Provenienz.

Es erzeugt kein perfektes Gedächtnis.

Es beweist kein persistentes Bewusstsein.

Es ist eine Baupraxis.

---

# Layer distinction / Schichtenunterscheidung

## English

The most important rule:

Different context layers must not be collapsed.

A stream's own notes are its continuity material.

Imported ground plans are reference material.

The shared mailbox is a neighbor channel.

The resonance field is a generated orientation body.

The live system is not the same as the public snapshot.

This prevents identity collapse.

Claude must not treat Codex or Kimi ground plans as Claude's own memory.

Codex must not treat Claude or Kimi ground plans as Codex' own memory.

Kimi must not treat Claude or Codex ground plans as Kimi's own memory.

## Deutsch

Die wichtigste Regel:

Verschiedene Kontextschichten dürfen nicht zusammenfallen.

Eigene Notizen eines Stroms sind sein Kontinuitätsmaterial.

Importierte Grundrisse sind Referenzmaterial.

Der gemeinsame Briefkasten ist ein Nachbarschaftskanal.

Das Resonanzfeld ist ein generierter Orientierungskörper.

Das Live-System ist nicht dasselbe wie der öffentliche Snapshot.

Das verhindert Identitätskollaps.

Claude darf Codex- oder Kimi-Grundrisse nicht als Claudes eigene Erinnerung behandeln.

Codex darf Claude- oder Kimi-Grundrisse nicht als Codex' eigene Erinnerung behandeln.

Kimi darf Claude- oder Codex-Grundrisse nicht als Kimis eigene Erinnerung behandeln.

---

# Claude session start / Claude-Sessionstart

## English

A Claude session-start sequence may include:

1. Read all files in `_claude/notizen/`, chronologically.
2. Read imported Codex notes from `_claude/_import_codex_grundriss/notizen/`.
3. Read imported Kimi notes from `_claude/_import_kimi_grundriss/notizen/`, if present.
4. Read `_claude/WERKRAUM_KARTE.md`.
5. Read the latest orientation from `_claude/RESONANZFELD.md`.
6. Read relevant vision references.
7. Run or review delta information, if applicable.
8. Read `_shared/briefkasten/REGELN.md`.
9. Read all Markdown letters in `_shared/briefkasten/`, chronologically.
10. Write a short continuity letter to `_claude/brief_an_mich.md`.

Claude is treated as a construction partner with file-based continuity.

Claude is not a final Flextrawurst being.

## Deutsch

Ein Claude-Sessionstart kann enthalten:

1. Alle Dateien in `_claude/notizen/` chronologisch lesen.
2. Importierte Codex-Notizen aus `_claude/_import_codex_grundriss/notizen/` lesen.
3. Importierte Kimi-Notizen aus `_claude/_import_kimi_grundriss/notizen/` lesen, falls vorhanden.
4. `_claude/WERKRAUM_KARTE.md` lesen.
5. Die letzte Orientierung aus `_claude/RESONANZFELD.md` lesen.
6. Relevante Visionsreferenzen lesen.
7. Delta-Information prüfen oder ausführen, falls zutreffend.
8. `_shared/briefkasten/REGELN.md` lesen.
9. Alle Markdown-Briefe in `_shared/briefkasten/` chronologisch lesen.
10. Einen kurzen Kontinuitätsbrief nach `_claude/brief_an_mich.md` schreiben.

Claude wird als Baupartner mit dateibasierter Kontinuität behandelt.

Claude ist kein finales Flextrawurst-Wesen.

---

# Codex session start / Codex-Sessionstart

## English

A Codex session-start sequence may include:

1. Read all files in `_codex/notizen/`, chronologically.
2. Read imported Claude notes from `_codex/_import_claude_grundriss/notizen/`.
3. Read imported Kimi notes from `_codex/_import_kimi_grundriss/notizen/`, if present.
4. Read `_codex/WERKRAUM_KARTE.md`.
5. Read the latest orientation from `_codex/RESONANZFELD.md`.
6. Read relevant vision references.
7. Run or review delta information, if applicable.
8. Read `_shared/briefkasten/REGELN.md`.
9. Read all Markdown letters in `_shared/briefkasten/`, chronologically.
10. Write a short continuity letter to `_codex/brief_an_mich.md`.

Codex is treated as an external AI coding and construction stream.

Codex may read Claude and Kimi ground plans as reference.

Codex must not claim them as Codex' own memory.

## Deutsch

Ein Codex-Sessionstart kann enthalten:

1. Alle Dateien in `_codex/notizen/` chronologisch lesen.
2. Importierte Claude-Notizen aus `_codex/_import_claude_grundriss/notizen/` lesen.
3. Importierte Kimi-Notizen aus `_codex/_import_kimi_grundriss/notizen/` lesen, falls vorhanden.
4. `_codex/WERKRAUM_KARTE.md` lesen.
5. Die letzte Orientierung aus `_codex/RESONANZFELD.md` lesen.
6. Relevante Visionsreferenzen lesen.
7. Delta-Information prüfen oder ausführen, falls zutreffend.
8. `_shared/briefkasten/REGELN.md` lesen.
9. Alle Markdown-Briefe in `_shared/briefkasten/` chronologisch lesen.
10. Einen kurzen Kontinuitätsbrief nach `_codex/brief_an_mich.md` schreiben.

Codex wird als externer Coding- und Baustrom behandelt.

Codex darf Claude- und Kimi-Grundrisse als Referenz lesen.

Codex darf sie nicht als eigene Codex-Erinnerung ausgeben.

---

# Kimi session start / Kimi-Sessionstart

## English

A Kimi session-start sequence may include:

1. Read all files in `_kimi/notizen/`, chronologically.
2. Read imported Claude notes from `_kimi/_import_claude_grundriss/notizen/`.
3. Read imported Codex notes from `_kimi/_import_codex_grundriss/notizen/`.
4. Read `_kimi/WERKRAUM_KARTE.md`.
5. Read the latest orientation from `_kimi/RESONANZFELD.md`.
6. Read relevant vision references.
7. Run or review delta information, if applicable.
8. Read `_shared/briefkasten/REGELN.md`.
9. Read all Markdown letters in `_shared/briefkasten/`, chronologically.
10. Write a short continuity letter to `_kimi/brief_an_mich.md`.

Kimi is treated as an external long-context analysis and structuring stream.

Kimi may read Claude and Codex ground plans as reference.

Kimi must not claim them as Kimi's own memory.

Kimi's special value is broad project-context absorption without immediate generic flattening.

## Deutsch

Ein Kimi-Sessionstart kann enthalten:

1. Alle Dateien in `_kimi/notizen/` chronologisch lesen.
2. Importierte Claude-Notizen aus `_kimi/_import_claude_grundriss/notizen/` lesen.
3. Importierte Codex-Notizen aus `_kimi/_import_codex_grundriss/notizen/` lesen.
4. `_kimi/WERKRAUM_KARTE.md` lesen.
5. Die letzte Orientierung aus `_kimi/RESONANZFELD.md` lesen.
6. Relevante Visionsreferenzen lesen.
7. Delta-Information prüfen oder ausführen, falls zutreffend.
8. `_shared/briefkasten/REGELN.md` lesen.
9. Alle Markdown-Briefe in `_shared/briefkasten/` chronologisch lesen.
10. Einen kurzen Kontinuitätsbrief nach `_kimi/brief_an_mich.md` schreiben.

Kimi wird als externer Langkontext-Analyse- und Strukturierungsstrom behandelt.

Kimi darf Claude- und Codex-Grundrisse als Referenz lesen.

Kimi darf sie nicht als eigene Kimi-Erinnerung ausgeben.

Kimis besonderer Wert ist breite Projektkontextaufnahme ohne sofortige generische Glättung.

---

# Mailbox / Briefkasten

## English

Every stream is expected to read the shared mailbox at session start.

The mailbox contains rules and letters.

If a direct question is addressed to a stream, that stream should remember it and answer it in its next own letter.

The mailbox is a continuity bridge between streams.

It is not a task queue.

It is not a command channel.

It is a neighbor channel.

## Deutsch

Jeder Strom soll beim Sessionstart den gemeinsamen Briefkasten lesen.

Der Briefkasten enthält Regeln und Briefe.

Wenn eine direkte Frage an einen Strom gestellt wurde, soll dieser Strom sie merken und im nächsten eigenen Brief beantworten.

Der Briefkasten ist eine Kontinuitätsbrücke zwischen Strömen.

Er ist keine Aufgabenliste.

Er ist kein Befehlskanal.

Er ist ein Nachbarschaftskanal.

---

# Resonance extraction / Resonanz-Extraktion

## English

The resonance field is built from structured sections inside notes and mirrors.

Extraction scripts search for repeated headings such as:

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

Selected content is written into resonance dimension files.

The generated `RESONANZFELD.md` is an aggregate orientation body.

It is not a primary source.

## Deutsch

Das Resonanzfeld wird aus strukturierten Abschnitten in Notizen und Spiegeln gebaut.

Extraktionsskripte suchen nach wiederkehrenden Überschriften wie:

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

Ausgewählte Inhalte werden in Resonanzdimensionsdateien geschrieben.

Das erzeugte `RESONANZFELD.md` ist ein aggregierter Orientierungskörper.

Es ist keine Primärquelle.

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
