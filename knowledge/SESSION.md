---
generated_by: "OpenAI Codex (GPT-6)"
timestamp: "2026-09-23"
---
# Last Known State
Agent: OpenAI Codex
Handoff-from: OpenAI Codex
Handoff-type: continuation
Goal: implement selected Meridian Hemisphere third edition.
Status: implemented; independent verifier approved. Physical trial remains open.

Project: /Users/danielbally/Git/time-as-hand
Preview: http://127.0.0.1:4286 (third edition selected).
Builds: dist/time-as-hand-original.pbw; dist/time-as-hand-two-hands.pbw; dist/meridian-hemisphere.pbw.
Source manifest/default build: Original, production live clock. Three embedded UUID/download hashes verified.
Hemisphere: location-centered low-resolution globe, seasonal UTC night shading, two numbered hands, existing date/font/color/width controls, opt-in coarse phone coordinates and remembered offline view.
Evidence: .tmp/hemisphere-verification.json; hemisphere-emulator-verification.json (five zero-difference cases); existing style/calendar regression reports. Phone sandbox tests pass. See procedural/verify_hemisphere.md for commands and limitations.
Native findings: static allocation limit required heap pixel buffer; linked atan2f produced invalid longitudes and was replaced; empty phone settings must not overwrite native location. UTC/local mismatch in emulator was not established as a gmtime bug; final tests use explicit UTC process environment.
Documentation: README.md, RELEASE_NOTES.md, PUBLISH.md, article/field-notes.md, domain/hemisphere.md updated. Store screenshots: assets/store/meridian/. No publishing, commits or pushes.
Next: physical paired-phone settings/permission checks, non-UTC/DST watch behavior, wrist reading and battery trial.
Closing audit: the chosen visual concept is now a working third prototype. Article notes capture measured failures and evidence boundaries; more feature expansion should wait for wear-test results.

## Checkpoint Log

- 2026-09-23 12:42 — commit: Initial commit: Time as Hand watchface, preview and verification kit
- 2026-09-23 — review fixes: blank custom coordinates rejected (pkjs), structural Meridian detection (pkjs), preview 404 ordering; tests added/extended (verify_location.js, verify_preview.py) and shown to fail on old code; dist/ rebuilt, inspect_bundles + host suites pass. Emulator suites not re-run (C unchanged). Independent verifier: APPROVED (fresh subagent; noted weak edition-detection test, since strengthened with nested-config fixture).
- 2026-09-23 12:48 — commit: Fix blank custom coordinates, structural Meridian detection, preview 404 | README.md,execution/preview.py,execution/verify_location.js,execution/verify_preview.py,knowledge/DECISIONS.md
- 2026-09-23 — halo: glyph-shaped numeral halo (r=scale) + white graticule over land in globe.inc; verify_hemisphere.py rewritten to derive the halo independently (fails on old rectangle and on r=1 mutant); host suites pass; rebuilt; native emulator 5/5 zero-diff after pebble wipe; store screenshots refreshed. Independent verifier: first pass rejected (test missed an over-large halo); test strengthened with cross-frame consensus check, mutant table re-verified, APPROVED.
