---
generated_by: "OpenAI Codex (GPT-6)"
timestamp: "2026-09-23"
---
# Run the prototype
From project root: `python3 execution/preview.py`, then open http://127.0.0.1:4286. Python standard library plus local C compiler required. Server is loopback-only and serves an explicit route allowlist.

Run `python3 execution/verify.py` after changing renderer. In `watchface/`, run `pebble build`, then `pebble install --emulator emery`. Run emulator image comparison with the Pebble tool environment's Python: `/Users/danielbally/.local/share/uv/tools/pebble-tool/bin/python3 execution/check_emulator.py`.

Physical install requires user's Pebble phone app. Enable Dev Connect under Devices, authenticate with the user's own account, then run `pebble login` and `pebble install --cloudpebble` from watchface/. Do not automate account credentials. No deployment or app-store publication required.

The app has no external data service, backend, runtime AI or secrets. Bundled Clay phone-side JavaScript provides offline configuration. Its preview server is development-only. Rebuild after code changes; restart preview to reload the compiled C library.

## Current two-edition workflow — 2026-09-23
- Build: `python3 execution/build_editions.py`; distributes two distinct UUIDs in dist/. Source manifest returns to Original.
- Regenerate font data/catalogs after changes: `python3 execution/generate_fonts.py`, then `python3 execution/generate_settings.py`.
- Verify: `python3 execution/verify_editions.py`, `python3 execution/verify_calendar.py`, `python3 execution/verify_styles.py`.
- Native comparison: Pebble environment python3 execution/check_calendar_emulator.py. It sends actual configuration messages and tests app restart persistence. Test-clock overrides stay in temporary emulator builds; finally rebuilds live distributables.
- Stop active emulator app before installing another UUID: `python3 execution/stop_emulator_app.py`. Installing alone can acknowledge transfer while prior watchface remains active. Avoid sending a second start while an install is transitioning. Emulator transport can time out on long batches; errors are not pixel evidence.
- `pebble clean` is needed after messageKeys change to regenerate SDK headers.
- Publish via current dashboard using the explicit PBWs: see PUBLISH.md. Do not run pebble publish from default source and expect Two Hands: it rebuilds Original.

2026-09-23 verification: 1,440 host minute checks passed; 8 native fixed-time emulator states matched pixel-exactly; restored live build matched local time. Independent verifier approved final build and download identity. The source-based browser was manually inspected.

Final settings delivery: 17 native pixel comparisons passed; both editions retained date/style settings across app restart. Final production Two Hands frame matched local clock. Bundle embedded UUIDs and preview download hashes matched. Independent final verifier approved. Paired-phone settings interaction and physical wear/battery remain untested.
