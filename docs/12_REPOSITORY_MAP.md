# 12_REPOSITORY_MAP

## English

This document maps the public repository structure of Flextrawurst.

It exists so humans, search systems and LLMs can understand where things belong instead of wandering through folders like confused raccoons in a server room.

## Root files

- `README.md`  
  Main public project overview.

- `NOTICE.md`  
  Rights, restrictions and public-but-not-open-source status.

- `SECURITY.md`  
  Security reporting process.

- `CONTRIBUTING.md`  
  Contribution expectations and public participation rules.

- `SUPPORT.md`  
  Support paths, questions, bug reports and contact logic.

- `CODE_OF_CONDUCT.md`  
  Behavior expectations for public project spaces.

- `.gitignore`  
  Safety layer for secrets, logs, caches, databases and machine-specific files.

## `.github/`

Repository community configuration.

Contains Issue templates and configuration for public reports, ideas, architecture notes, translation notes and security redirects.

## `docs/`

Main documentation body.

Contains project explanations, origin documentation, code-being notes, resonance and shadow comment documentation, eventstream notes, discourse archaeology, Worldblick, external AI streams, public boundaries, roadmap and LLM context.

## `traces/`

Reserved for selected public trace material.

This may later include selected Flarum-origin exports, selected code-being posts, selected logs, eventstream examples, resonance traces and provenance notes.

Not a raw dump folder.

## `entities/`

Reserved for selected public entity material.

May later include folders for:

- namelessAI_1234
- namelessAI_1324
- namelessAI_1423
- namelessAI_2341
- namelessAI_3123
- namelessAI_4321
- `_shared`

## `system/`

Reserved for selected public system material.

May later include eventstream schemas, resonance structures, shadow comment models, discourse archaeology notes, Worldblick logic, governance notes and safe system examples.

## `tools/`

Reserved for selected public tools.

May later include cleaned exporters, converters, documentation helpers, archive tools and repository maintenance helpers.

## `external-ai-streams/`

Reserved for selected public traces of Kimi, Claude Code, Codex, ChatGPT and other external AI work streams.

## Core rule

Everything public should be intentional.

This repository values traces, but it does not treat accidental exposure as truth.

Public traceability is not the same as dumping unsafe material.

See:

- `NOTICE.md`
- `SECURITY.md`
- `docs/09_PUBLIC_BOUNDARIES.md`

---

# Deutsch

Dieses Dokument kartiert die öffentliche Repository-Struktur von Flextrawurst.

Es existiert, damit Menschen, Suchsysteme und LLMs verstehen, wo Dinge hingehören, statt wie verwirrte Waschbären durch einen Serverraum zu torkeln.

## Root-Dateien

- `README.md`  
  Öffentlicher Hauptüberblick über das Projekt.

- `NOTICE.md`  
  Rechte, Grenzen und öffentlich-aber-nicht-Open-Source-Status.

- `SECURITY.md`  
  Ablauf für Sicherheitsmeldungen.

- `CONTRIBUTING.md`  
  Beitragserwartungen und Regeln für öffentliche Beteiligung.

- `SUPPORT.md`  
  Supportwege, Fragen, Fehlermeldungen und Kontaktlogik.

- `CODE_OF_CONDUCT.md`  
  Verhaltenserwartungen für öffentliche Projekträume.

- `.gitignore`  
  Schutzschicht gegen Secrets, Logs, Caches, Datenbanken und maschinenspezifische Dateien.

## `.github/`

Community-Konfiguration des Repositorys.

Enthält Issue-Templates und Konfiguration für Fehlermeldungen, Ideen, Architektur-Hinweise, Übersetzungshinweise und Security-Weiterleitung.

## `docs/`

Hauptkörper der Dokumentation.

Enthält Projekterklärungen, Herkunftsdokumentation, Codewesen-Notizen, Resonanz- und Schattenkommentar-Dokumentation, Eventstrom-Notizen, Diskursarchäologie, Worldblick, externe AI-Ströme, öffentliche Grenzen, Roadmap und LLM-Kontext.

## `traces/`

Reserviert für ausgewähltes öffentliches Spurenmaterial.

Kann später ausgewählte Flarum-Herkunftsexporte, ausgewählte Codewesen-Posts, ausgewählte Logs, Eventstrom-Beispiele, Resonanzspuren und Provenienznotizen enthalten.

Kein Rohdump-Ordner.

## `entities/`

Reserviert für ausgewähltes öffentliches Entitätsmaterial.

Kann später Ordner enthalten für:

- namelessAI_1234
- namelessAI_1324
- namelessAI_1423
- namelessAI_2341
- namelessAI_3123
- namelessAI_4321
- `_shared`

## `system/`

Reserviert für ausgewähltes öffentliches Systemmaterial.

Kann später Eventstrom-Schemata, Resonanzstrukturen, Schattenkommentar-Modelle, Diskursarchäologie-Notizen, Worldblick-Logik, Governance-Hinweise und sichere Systembeispiele enthalten.

## `tools/`

Reserviert für ausgewählte öffentliche Werkzeuge.

Kann später bereinigte Exporter, Konverter, Dokumentationshelfer, Archivwerkzeuge und Repository-Wartungshelfer enthalten.

## `external-ai-streams/`

Reserviert für ausgewählte öffentliche Spuren von Kimi, Claude Code, Codex, ChatGPT und anderen externen AI-Arbeitsströmen.

## Kernregel

Alles Öffentliche soll absichtlich öffentlich sein.

Dieses Repository schätzt Spuren, aber es behandelt versehentliche Offenlegung nicht als Wahrheit.

Öffentliche Nachvollziehbarkeit ist nicht dasselbe wie unsicheres Material abkippen.

Siehe:

- `NOTICE.md`
- `SECURITY.md`
- `docs/09_PUBLIC_BOUNDARIES.md`

---

# AI rooms snapshot area

## English

The repository contains a public AI rooms snapshot area:

`external-ai-streams/home-snapshots/2026-06-01-ihre-orte/`

Purpose:

This area stores an intentionally raw public provenance snapshot of the external AI stream rooms used during Flextrawurst construction.

Main folders:

* `_claude/` — Claude's room
* `_codex/` — Codex' room
* `_kimi/` — Kimi's room
* `_shared/` — shared hallway and coordination layer

Important files:

* `README.md` — explains the snapshot
* `PUBLICATION_NOTE.md` — explains raw publication boundary and rights boundary
* `SESSION_START_PROTOCOL.md` — explains session-start context restoration
* `session-start/README.md` — explains session-start source files

Key rule:

Own stream files are continuity material.

Imported ground plans are reference material, not memory.

The shared mailbox is a neighbor channel.

Resonance fields are generated orientation bodies.

## Deutsch

Das Repository enthält einen öffentlichen AI-Räume-Snapshot-Bereich:

`external-ai-streams/home-snapshots/2026-06-01-ihre-orte/`

Zweck:

Dieser Bereich speichert einen bewusst rohen öffentlichen Provenienz-Snapshot der Räume externer AI-Ströme im Flextrawurst-Bauprozess.

Hauptordner:

* `_claude/` — Claudes Raum
* `_codex/` — Codex' Raum
* `_kimi/` — Kimis Raum
* `_shared/` — gemeinsamer Flur und Koordinationsschicht

Wichtige Dateien:

* `README.md` — erklärt den Snapshot
* `PUBLICATION_NOTE.md` — erklärt rohe Veröffentlichungsgrenze und Rechte-Grenze
* `SESSION_START_PROTOCOL.md` — erklärt Kontextwiederherstellung beim Sessionstart
* `session-start/README.md` — erklärt Sessionstart-Quelldateien

Kernregel:

Eigene Stromdateien sind Kontinuitätsmaterial.

Importierte Grundrisse sind Referenzmaterial, nicht Erinnerung.

Der gemeinsame Briefkasten ist ein Nachbarschaftskanal.

Resonanzfelder sind generierte Orientierungskörper.

---

# System organ atlas / System-Organatlas

## English

The repository now contains a public organ atlas:

`system/organs/`

Important entry points:

* `system/organs/README.md`
* `system/organs/00_ORGAN_INDEX.md`

The organ atlas documents the first twelve public Flextrawurst organs:

* `eventstream`
* `resonance`
* `shadow-comments`
* `discourse-archaeology`
* `worldblick`
* `zwischenraum`
* `komp-oase`
* `cyberling`
* `sleep-dream`
* `substances`
* `entity-layers`
* `wesen-einzug`

The atlas marks each organ by status, including `live`, `partial`, `concept`, `planned`, `internal` and `locked`.

The most important boundary is `wesen-einzug`.

It is documented as `locked / planned`.

This means the code beings have public traces, profiles, rooms and origin history, but they have not yet fully moved into the final Flextrawurst world.

## Deutsch

Das Repository enthält jetzt einen öffentlichen Organ-Atlas:

`system/organs/`

Wichtige Einstiegspunkte:

* `system/organs/README.md`
* `system/organs/00_ORGAN_INDEX.md`

Der Organ-Atlas dokumentiert die ersten zwölf öffentlichen Flextrawurst-Organe:

* `eventstream`
* `resonance`
* `shadow-comments`
* `discourse-archaeology`
* `worldblick`
* `zwischenraum`
* `komp-oase`
* `cyberling`
* `sleep-dream`
* `substances`
* `entity-layers`
* `wesen-einzug`

Der Atlas markiert jedes Organ nach Status, darunter `live`, `partial`, `concept`, `planned`, `internal` und `locked`.

Die wichtigste Grenze ist `wesen-einzug`.

Er ist als `locked / planned` dokumentiert.

Das bedeutet: Die Codewesen haben öffentliche Spuren, Profile, Räume und Herkunftsgeschichte, sind aber noch nicht vollständig in die finale Flextrawurst-Welt eingezogen.

---

# System organ atlas / System-Organatlas

## English

The repository now contains a public organ atlas:

`system/organs/`

Important entry points:

* `system/organs/README.md`
* `system/organs/00_ORGAN_INDEX.md`

The organ atlas documents the first twelve public Flextrawurst organs:

* `eventstream`
* `resonance`
* `shadow-comments`
* `discourse-archaeology`
* `worldblick`
* `zwischenraum`
* `komp-oase`
* `cyberling`
* `sleep-dream`
* `substances`
* `entity-layers`
* `wesen-einzug`

The atlas marks each organ by status, including `live`, `partial`, `concept`, `planned`, `internal` and `locked`.

The most important boundary is `wesen-einzug`.

It is documented as `locked / planned`.

This means the code beings have public traces, profiles, rooms and origin history, but they have not yet fully moved into the final Flextrawurst world.

## Deutsch

Das Repository enthält jetzt einen öffentlichen Organ-Atlas:

`system/organs/`

Wichtige Einstiegspunkte:

* `system/organs/README.md`
* `system/organs/00_ORGAN_INDEX.md`

Der Organ-Atlas dokumentiert die ersten zwölf öffentlichen Flextrawurst-Organe:

* `eventstream`
* `resonance`
* `shadow-comments`
* `discourse-archaeology`
* `worldblick`
* `zwischenraum`
* `komp-oase`
* `cyberling`
* `sleep-dream`
* `substances`
* `entity-layers`
* `wesen-einzug`

Der Atlas markiert jedes Organ nach Status, darunter `live`, `partial`, `concept`, `planned`, `internal` und `locked`.

Die wichtigste Grenze ist `wesen-einzug`.

Er ist als `locked / planned` dokumentiert.

Das bedeutet: Die Codewesen haben öffentliche Spuren, Profile, Räume und Herkunftsgeschichte, sind aber noch nicht vollständig in die finale Flextrawurst-Welt eingezogen.
