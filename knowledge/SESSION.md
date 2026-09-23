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
