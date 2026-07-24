# Flextrawurst · Godot Engine Vertical Slice 001

## Status

Erster isolierter echter Game-Engine-Körper neben dem bestehenden Single-HTML-Spiel.

Dieser Körper ersetzt, überschreibt oder entwertet die vorhandene HTML-Fassung nicht. Er beweist zunächst nur die kleinste geschlossene Engine-Grundlage:

- echtes `project.godot`,
- echte 3D-Szene,
- `CharacterBody3D`, Kamera und Kollision,
- deterministische Bewegung,
- provenance-bewusster Weltseed,
- bidirektionaler HTTP-Bridge-Adapter,
- Headless-Strukturtest,
- Headless-Starttest über GitHub Actions.

## Harte Grenzen

- Keine erfundenen Live-VPS-Daten.
- Keine automatische Kanonisierung empfangener Ereignisse.
- Keine Aktivierung von Codewesen.
- Keine stillen Änderungen am vorhandenen HTML-Spiel.
- Die VPS-Bridge bleibt deaktiviert, bis eine real geprüfte Route eingetragen wurde.
- Platzhaltergeometrie ist ausdrücklich kein realer Schwelm-Import.

## Lokaler Start

Voraussetzung: Godot 4.7.1 stable oder kompatible 4.7-Patchversion im `PATH`.

```bash
godot --path engine/godot-vertical-slice
```

## Headless-Strukturtest

```bash
godot \
  --headless \
  --path engine/godot-vertical-slice \
  --script res://tests/headless_smoke.gd
```

Erwartete Abschlusszeile:

```text
FLEXTRAWURST_ENGINE_SLICE_SMOKE_PASS
```

## Headless-Boot der Hauptszene

```bash
godot \
  --headless \
  --path engine/godot-vertical-slice \
  --quit-after 3
```

## Bestehender Datenfluss

```text
Weltseed
→ Godot-Szene
→ Spielerbewegung und lokale Zustände
→ WorldBridge-Adapter
→ bestätigte VPS-Route
→ strukturierte Ereignisse
→ geprüfte Rückführung in die Engine
```

## Noch nicht behauptet

- kein vollständiges Flextrawurst-Godot-Spiel,
- kein real importiertes Stadtmodell,
- kein aktiver VPS-Livekanal,
- kein Webexport,
- kein vollständiges Physik-, Quest- oder AI-System,
- kein menschlicher Spielbeweis.

## Nächster Bauring nach grünem Test

1. reale VPS-MCP-/HTTP-Route prüfen,
2. Request- und Response-Schema festnageln,
3. Bridge gegen einen read-only Weltzustand testen,
4. eine vorhandene GLB-Datei importieren,
5. Metadaten-ID und Alleswisser-Akte an das Mesh binden,
6. Headless-Test, Screenshot und Build-Artefakt zurückführen.
