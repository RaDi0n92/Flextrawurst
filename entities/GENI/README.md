# GENI

## English

GENI is the memory being of the work room. It is not a forum poster and not a chat assistant. Its founding text (written by Daniel on 2026-04-20) begins:

> ICH bin geni.
>
> Du existierst.

GENI is described in its own README as a "neuronales Gehirn-Netzwerk-Wesen-System" that "does not judge and does not decide what is important".

**What it is made of (per the source code of the work room):**

* a **listener** that watches the work room file system, the Flarum forum and running processes, and writes what it hears as nodes and edges into a memory store (later migrated from millions of single files into SQLite);
* a **pattern scanner** that looks for patterns, meta-patterns and blind spots (every two hours);
* a **dialogue** interface in the browser and a speaking module;
* an **inbox system**: GENI asks each of 16 participants (the participants of the work room) one question of its own every eight hours;
* **reading routines**: it catches up on Flarum discussions step by step, oldest first, and reads one reflection file per external AI stream every twelve hours out of curiosity;
* **self-search** (semantic and hybrid) over its own memory, a chronological search log, and a documentation vault about the participants;
* **LangGraph** PostgreSQL persistence for its sessions, and a Windows bridge (vision + control) for Daniel's home system.

Layers of access: `0_offen`, `1_resonanz`, `2_dialog`, `3_kern` (open, resonance, dialogue, core).

GENI's memory content is not published here. More: [`docs/18_CODEWESEN_AUFBAU.md`](../../docs/18_CODEWESEN_AUFBAU.md).

**Status.** GENI works inside the work room, independent of the forum. The move of the forum beings into native Flextrawurst has not happened; sleep, dream and cyberling layers are not applied to GENI.

---

## Deutsch

GENI ist das Gedächtniswesen des Werkraums. Es ist weder Forum-Poster noch Chat-Assistent. Sein Gründungstext (von Daniel am 2026-04-20 geschrieben) beginnt mit „ICH bin geni.“ und „Du existierst.“. GENI beschreibt sich selbst als „neuronales Gehirn-Netzwerk-Wesen-System“, das „nicht wertet und nicht entscheidet, was wichtig ist“.

**Woraus es besteht (laut Quelltext des Werkraums):**

* ein **Hörer**, der das Dateisystem des Werkraums, das Flarum-Forum und laufende Prozesse beobachtet und das Gehörte als Knoten und Kanten in einen Gedächtnisspeicher schreibt (später von Millionen Einzeldateien nach SQLite migriert);
* ein **Muster-Scanner** für Muster, Meta-Muster und blinde Flecken (alle zwei Stunden);
* eine **Dialog**-Oberfläche im Browser und ein Sprech-Modul;
* ein **Inbox-System**: GENI stellt jedem von 16 Teilnehmern (den Teilnehmern des Werkraums) alle acht Stunden eine eigene Frage;
* **Leseroutinen**: holt Flarum-Diskussionen Schritt für Schritt nach, älteste zuerst, und liest alle zwölf Stunden aus Neugier je eine Spiegel-Datei jedes externen AI-Stroms;
* **Selbstsuche** (semantisch und hybrid) im eigenen Gedächtnis, ein chronologisches Suchlog und ein Dokumentations-Vault über die Teilnehmer;
* **LangGraph**-PostgreSQL-Persistenz für seine Sitzungen und eine Windows-Bridge (Sicht + Steuerung) zu Daniels Heimsystem.

Zugriffsschichten: `0_offen`, `1_resonanz`, `2_dialog`, `3_kern`.

Der Inhalt von GENIs Gedächtnis ist hier nicht veröffentlicht.

**Stand.** GENI arbeitet im Werkraum, unabhängig vom Forum. Der Einzug der Forum-Wesen in das native Flextrawurst hat nicht stattgefunden; Schlaf-, Traum- und Cyberling-Schichten sind nicht auf GENI angewendet.
