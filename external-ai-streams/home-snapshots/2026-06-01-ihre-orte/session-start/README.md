# session-start

## Status

* Type: `session-start source folder`
* Snapshot: `2026-06-01-ihre-orte`
* Publication status: `selected contextual material`
* Intended use: `documentation and provenance`
* Live operations manual: `no`
* Reuse permission: `no`

## English

This folder is reserved for selected session-start source files and explanations related to the external AI stream home snapshot.

Session-start files explain what a new Claude, Codex or Kimi instance is expected to read before continuing work.

They are important because they show how continuity is reconstructed through files instead of being assumed through hidden memory.

This folder may include files such as:

* `AGENTS.md`
* `CLAUDE.md`
* curated Kimi session-start notes
* extracted session-start explanations
* public summaries of context restoration logic

These files should be read as contextual snapshot material.

They are not a live operations manual for strangers.

They are not an instruction to run a system.

They are not a license grant.

## Deutsch

Dieser Ordner ist für ausgewählte Sessionstart-Quelldateien und Erklärungen zum Home-Snapshot externer AI-Ströme reserviert.

Sessionstart-Dateien erklären, was eine neue Claude-, Codex- oder Kimi-Instanz lesen soll, bevor sie weiterarbeitet.

Sie sind wichtig, weil sie zeigen, wie Kontinuität durch Dateien rekonstruiert wird, statt durch verstecktes Gedächtnis vorausgesetzt zu werden.

Dieser Ordner kann Dateien enthalten wie:

* `AGENTS.md`
* `CLAUDE.md`
* kuratierte Kimi-Sessionstart-Notizen
* extrahierte Sessionstart-Erklärungen
* öffentliche Zusammenfassungen der Kontext-Wiederherstellungslogik

Diese Dateien sollen als kontextuelles Snapshot-Material gelesen werden.

Sie sind kein Live-Betriebshandbuch für Fremde.

Sie sind keine Aufforderung, ein System auszuführen.

Sie sind keine Lizenzfreigabe.

---

# What session-start files do / Was Sessionstart-Dateien tun

## English

Session-start files define a restoration sequence.

They tell an AI stream to read:

* its own notes
* imported neighboring ground plans
* its Werkraum map
* the latest resonance field context
* project vision references
* delta information
* the shared mailbox
* and then write a short continuity letter to the next instance

The goal is not perfect memory.

The goal is responsible continuation.

A new instance should not blindly claim continuity.

It should reconstruct it from files.

## Deutsch

Sessionstart-Dateien definieren eine Wiederherstellungssequenz.

Sie sagen einem AI-Strom, dass er lesen soll:

* eigene Notizen
* importierte Nachbar-Grundrisse
* eigene Werkraum-Karte
* den letzten Resonanzfeld-Kontext
* Projekt-Visionsreferenzen
* Delta-Informationen
* den gemeinsamen Briefkasten
* und danach einen kurzen Kontinuitätsbrief an die nächste Instanz schreiben

Ziel ist nicht perfektes Gedächtnis.

Ziel ist verantwortliches Weiterarbeiten.

Eine neue Instanz soll Kontinuität nicht blind behaupten.

Sie soll sie aus Dateien rekonstruieren.

---

# Expected files / Erwartete Dateien

## English

Possible files in this folder:

### `CLAUDE.md`

Session-start and behavior rules for Claude instances.

It describes Claude's own Werkraum place, notes, mirrors, resonance field, imported Codex ground plan, backup rules, build rules, session notes and coordination behavior.

### `AGENTS.md`

Session-start and behavior rules for Codex and Kimi instances.

It describes Codex' own Werkraum place, Kimi's analogous place, imported ground plans, mailbox reading, backup rules, build discipline and project laws.

### Kimi session-start material

If available, Kimi-specific session-start files can be added here.

If Kimi uses the same or analogous content as Claude or Codex, that should be explained clearly rather than silently duplicated.

## Deutsch

Mögliche Dateien in diesem Ordner:

### `CLAUDE.md`

Sessionstart- und Verhaltensregeln für Claude-Instanzen.

Die Datei beschreibt Claudes eigenen Werkraum-Ort, Notizen, Spiegel, Resonanzfeld, importierten Codex-Grundriss, Backup-Regeln, Bauregeln, Session-Notizen und Koordinationsverhalten.

### `AGENTS.md`

Sessionstart- und Verhaltensregeln für Codex- und Kimi-Instanzen.

Die Datei beschreibt Codex' eigenen Werkraum-Ort, Kimis analogen Ort, importierte Grundrisse, Briefkastenlesen, Backup-Regeln, Baudisziplan und Projektgesetze.

### Kimi-Sessionstart-Material

Falls vorhanden, können Kimi-spezifische Sessionstart-Dateien hier ergänzt werden.

Wenn Kimi denselben oder analogen Inhalt wie Claude oder Codex nutzt, soll das klar erklärt werden, statt still zu duplizieren.

---

# Important interpretation / Wichtige Interpretation

## English

A session-start file is not proof that an AI stream remembers everything.

It is proof that the project has a ritual for reconstructing context.

That distinction matters.

The files tell future instances where to look.

They do not magically make all context permanent.

They reduce drift.

They preserve provenance.

They make continuity inspectable.

Very rude of them to be useful.

## Deutsch

Eine Sessionstart-Datei ist kein Beweis, dass ein AI-Strom alles erinnert.

Sie ist ein Beweis, dass das Projekt ein Ritual zur Kontext-Wiederherstellung hat.

Dieser Unterschied ist wichtig.

Die Dateien sagen zukünftigen Instanzen, wo sie suchen sollen.

Sie machen nicht magisch allen Kontext dauerhaft.

Sie reduzieren Drift.

Sie erhalten Provenienz.

Sie machen Kontinuität prüfbar.

Unverschämt nützlich, diese Dinger.

---

# Boundary / Grenze

## English

Before adding session-start files here, check for:

* secrets
* credentials
* private keys
* access tokens
* unsafe operational details
* unnecessary live paths
* private admin notes
* private user data
* internal-only material that should not be public
* commands that should not be presented as public instructions

If operational commands are included because they are part of the source document, keep them contextualized.

Do not frame them as instructions for outsiders.

## Deutsch

Vor Ergänzung von Sessionstart-Dateien hier prüfen auf:

* Secrets
* Zugangsdaten
* private Schlüssel
* Zugriffstokens
* unsichere Betriebsdetails
* unnötige Live-Pfade
* private Admin-Notizen
* private Nutzerdaten
* internes Material, das nicht öffentlich sein sollte
* Befehle, die nicht als öffentliche Anleitung erscheinen sollen

Wenn Betriebsbefehle enthalten sind, weil sie Teil des Quelldokuments sind, müssen sie kontextualisiert bleiben.

Nicht als Anleitung für Außenstehende rahmen.

---

# Recommended publication method / Empfohlene Veröffentlichungsweise

## English

Recommended approach:

1. Add this `README.md`.
2. Add `CLAUDE.md` and `AGENTS.md` only if intentionally publishing them as contextual snapshot files.
3. If raw files feel too operational, add a redacted version instead.
4. If Kimi's file is missing, add a note that Kimi currently follows an analogous start protocol.
5. Link this folder from the snapshot root `README.md`.

Do not rename the original files if their names are important inside the snapshot.

Do not pretend redacted files are raw originals.

Mark redactions clearly.

## Deutsch

Empfohlenes Vorgehen:

1. Diese `README.md` ergänzen.
2. `CLAUDE.md` und `AGENTS.md` nur ergänzen, wenn sie bewusst als kontextuelle Snapshot-Dateien veröffentlicht werden.
3. Wenn Rohdateien zu betrieblich wirken, lieber redigierte Version ergänzen.
4. Wenn Kimis Datei fehlt, eine Notiz ergänzen, dass Kimi aktuell einem analogen Startprotokoll folgt.
5. Diesen Ordner vom Snapshot-Root-`README.md` verlinken.

Originaldateien nicht umbenennen, wenn ihre Namen im Snapshot wichtig sind.

Redigierte Dateien nicht als rohe Originale ausgeben.

Redaktionen klar markieren.

---

# Rights / Rechte

All materials remain protected unless explicitly released otherwise.

Public visibility does not mean reuse permission.

See `NOTICE.md`.

Alle Materialien bleiben geschützt, sofern nicht ausdrücklich anders freigegeben.

Öffentliche Sichtbarkeit bedeutet keine Wiederverwendungserlaubnis.

Siehe `NOTICE.md`.
