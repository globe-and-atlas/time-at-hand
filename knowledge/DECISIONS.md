---
generated_by: "OpenAI Codex (GPT-6)"
timestamp: "2026-09-23"
---
# Decisions

## Initial Decision

- Template profile: `dashboard-static`
- Deploy target: `local-only`
- Runtime: `static`

## 2026-09-23 — Portable native renderer
Use one C renderer for preview and native Emery target. Rejected separate browser drawing implementation because it could hide native geometry bugs. Chose minute-resolution updates, 12-hour text, one-minute cardinal state and left-side text flip. Hardware acceptance remains separate.

## 2026-09-23 — Editions and personalization
- Keep distinct UUIDs for Original and Two Hands so each can coexist and retain settings independently.
- Twelve original 5×7 numeral glyph sets preserve layout bounds; date uses a consistent small typeface. No external font assets.
- Hand styling retains optical defaults, supports eight Pebble-native foreground colors and explicit widths1–5. Time labels stay black.
- Bundle Clay1.1.0 configuration rather than hosting a settings page. Browser preferences demonstrate the feature but do not mutate PBWs.
- Use developer dashboard uploads of explicit PBWs for first store release; CLI publish rebuilds the default source edition.

## 2026-09-23 — Hemisphere third edition
User selected concept06 with night/day shading. Keep existing editions separate; add G&A Meridian with its own UUID. Use a bundled low-resolution land mask plus an analytic shadow instead of cached rotation images or network imagery. UTC drives sunlight; the watch OS drives local civil time. Optional phone coordinates affect the camera only. Retain native location when an empty phone sandbox reconnects. See domain/hemisphere.md for sources and limitations.
