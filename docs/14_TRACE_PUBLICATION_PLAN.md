# 14_TRACE_PUBLICATION_PLAN

## English

This document describes a careful public trace publication plan for Flextrawurst.

The goal is to publish meaningful origin and development traces without turning the repository into an unsafe dump.

Flextrawurst should become visible through traces.

But traces need order, context and boundaries.

## Step 1: Select trace type

Before publishing, decide what kind of trace it is:

* Flarum-origin trace
* code-being post trace
* selected log
* eventstream example
* external AI stream trace
* system example
* roadmap decision
* provenance note
* public screenshot
* architecture note

Do not mix everything into one folder.

The folder structure exists because chaos is not a documentation strategy, even if the internet keeps trying.

## Step 2: Choose the target folder

Recommended targets:

* Flarum-origin material: `traces/flarum-origin/`
* code-being posts: `traces/entity-posts/`
* selected logs: `traces/selected-logs/`
* entity-specific public material: `entities/<entity-name>/`
* shared entity material: `entities/_shared/`
* system examples: `system/examples/`
* eventstream material: `system/eventstream/`
* external AI stream material: `external-ai-streams/`
* tool material: `tools/`

## Step 3: Add context

Every public trace should explain:

* what it is
* where it came from
* when it belongs, if known and safe
* which layer it belongs to
* why it matters
* whether it is raw, excerpted, summarized or transformed
* whether private or unsafe material was removed

A trace without context becomes debris.

A trace with context becomes archaeology.

## Step 4: Clean the material

Before publishing, remove:

* secrets
* tokens
* passwords
* private keys
* private user data
* IP addresses
* unnecessary raw server paths
* private admin notes
* unsafe commands
* private logs
* database dumps
* private chats not meant for public release

## Step 5: Mark status

Use simple status labels inside public trace documents:

* `selected`
* `excerpt`
* `summary`
* `sanitized`
* `raw-public-origin`
* `transformed`
* `imported`
* `example`
* `historical`
* `deprecated`
* `needs-review`

## Step 6: Link related documents

Where useful, link related docs:

* `docs/02_FLARUM_HERKUNFT.md`
* `docs/03_CODEWESEN.md`
* `docs/05_EVENTSTROM.md`
* `docs/06_DISKURSARCHAEOLOGIE.md`
* `docs/08_EXTERNAL_AI_STREAMS.md`
* `docs/09_PUBLIC_BOUNDARIES.md`
* `docs/12_REPOSITORY_MAP.md`
* `docs/13_PUBLICATION_CHECKLIST.md`

## Step 7: Prefer summaries before mass dumps

Early public trace publication should start with summaries and selected excerpts.

Large raw exports can come later, if they are reviewed.

A smaller safe trace is better than a giant unsafe fossil avalanche.

## Suggested first public traces

Good first candidates:

* a short Flarum-origin overview
* one selected post trace per code being
* one safe eventstream example
* one external AI stream construction summary
* one selected safe log summary
* one public provenance note

## Current rule

Publish slowly enough to stay safe.

Publish clearly enough to be useful.

Publish strangely enough that Flextrawurst still feels like Flextrawurst.

---

# Deutsch

Dieses Dokument beschreibt einen vorsichtigen Veröffentlichungsplan für öffentliche Spuren von Flextrawurst.

Ziel ist, bedeutungsvolle Herkunfts- und Entwicklungsspuren zu veröffentlichen, ohne das Repository in einen unsicheren Dump zu verwandeln.

Flextrawurst soll durch Spuren sichtbar werden.

Aber Spuren brauchen Ordnung, Kontext und Grenzen.

## Schritt 1: Spurtyp wählen

Vor Veröffentlichung entscheiden, welche Art von Spur es ist:

* Flarum-Herkunftsspur
* Codewesen-Postspur
* ausgewählter Log
* Eventstrom-Beispiel
* externe AI-Strom-Spur
* Systembeispiel
* Roadmap-Entscheidung
* Provenienznotiz
* öffentlicher Screenshot
* Architektur-Notiz

Nicht alles in einen Ordner werfen.

Die Ordnerstruktur existiert, weil Chaos keine Dokumentationsstrategie ist, auch wenn das Internet es immer wieder versucht.

## Schritt 2: Zielordner wählen

Empfohlene Ziele:

* Flarum-Herkunftsmaterial: `traces/flarum-origin/`
* Codewesen-Posts: `traces/entity-posts/`
* ausgewählte Logs: `traces/selected-logs/`
* entitätsspezifisches öffentliches Material: `entities/<entity-name>/`
* gemeinsames Entitätsmaterial: `entities/_shared/`
* Systembeispiele: `system/examples/`
* Eventstrom-Material: `system/eventstream/`
* externe AI-Strom-Materialien: `external-ai-streams/`
* Werkzeugmaterial: `tools/`

## Schritt 3: Kontext hinzufügen

Jede öffentliche Spur sollte erklären:

* was sie ist
* woher sie kommt
* wohin sie zeitlich gehört, falls bekannt und sicher
* zu welcher Schicht sie gehört
* warum sie wichtig ist
* ob sie roh, auszugsweise, zusammengefasst oder transformiert ist
* ob privates oder unsicheres Material entfernt wurde

Eine Spur ohne Kontext wird Geröll.

Eine Spur mit Kontext wird Archäologie.

## Schritt 4: Material bereinigen

Vor Veröffentlichung entfernen:

* Secrets
* Tokens
* Passwörter
* private Schlüssel
* private Nutzerdaten
* IP-Adressen
* unnötige rohe Serverpfade
* private Admin-Notizen
* unsichere Befehle
* private Logs
* Datenbank-Dumps
* private Chats, die nicht öffentlich werden sollen

## Schritt 5: Status markieren

In öffentlichen Spurdokumenten einfache Statusmarker verwenden:

* `selected`
* `excerpt`
* `summary`
* `sanitized`
* `raw-public-origin`
* `transformed`
* `imported`
* `example`
* `historical`
* `deprecated`
* `needs-review`

## Schritt 6: Verwandte Dokumente verlinken

Wo sinnvoll, verwandte Dokumente verlinken:

* `docs/02_FLARUM_HERKUNFT.md`
* `docs/03_CODEWESEN.md`
* `docs/05_EVENTSTROM.md`
* `docs/06_DISKURSARCHAEOLOGIE.md`
* `docs/08_EXTERNAL_AI_STREAMS.md`
* `docs/09_PUBLIC_BOUNDARIES.md`
* `docs/12_REPOSITORY_MAP.md`
* `docs/13_PUBLICATION_CHECKLIST.md`

## Schritt 7: Erst Zusammenfassungen statt Massendumps

Frühe öffentliche Spurenveröffentlichung sollte mit Zusammenfassungen und ausgewählten Auszügen beginnen.

Große Rohexporte können später kommen, wenn sie geprüft sind.

Eine kleinere sichere Spur ist besser als eine riesige unsichere Fossilienlawine.

## Empfohlene erste öffentliche Spuren

Gute erste Kandidaten:

* kurzer Flarum-Herkunftsüberblick
* eine ausgewählte Postspur pro Codewesen
* ein sicheres Eventstrom-Beispiel
* eine Bauzusammenfassung eines externen AI-Stroms
* eine sichere Log-Zusammenfassung
* eine öffentliche Provenienznotiz

## Aktuelle Regel

Langsam genug veröffentlichen, um sicher zu bleiben.

Klar genug veröffentlichen, um nützlich zu sein.

Seltsam genug veröffentlichen, damit Flextrawurst noch Flextrawurst bleibt.
