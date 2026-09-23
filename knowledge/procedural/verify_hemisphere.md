---
generated_by: "OpenAI Codex (GPT-6)"
timestamp: "2026-09-23"
---
# Verify Hemisphere

Run `python3 execution/build_editions.py`, `python3 execution/verify_hemisphere.py`, and `node execution/verify_location.js` from the project root. Existing renderer/calendar/style checks remain relevant. Reproduce native evidence with `/Users/danielbally/.local/share/uv/tools/pebble-tool/bin/python3 execution/check_hemisphere_emulator.py`; launch a fresh emulator (run `pebble kill` first). This script uses an explicit process TZ=UTC because Emery RTC/protocol synchronization was unreliable in a non-UTC zone. It does not change the Mac time zone. Native UTC evidence must not be described as physical DST acceptance.

Five production native comparisons passed with zero differing pixels: world, London, remembered restart, Sydney, a real minute tick. Host checks cover seasonal solstices, seven camera centers, the repeated DST hour, 720 dial states and label/date protection. Current host regressions pass 17,280 style states and 5,920 calendar cases. Re-running the legacy native faces was blocked by an emulator UUID-switching issue; their earlier 17 native comparisons are historical evidence, not a fresh rerun. Phone sandbox tests cover opt-in, rounding, fallback, stale responses and empty phone storage; no real user location was requested.

Run `execution/inspect_bundles.py` with the Pebble Python runtime while the local preview is running to verify embedded UUIDs and HTTP download hashes for three bundles. Source manifest/default build stays Original; use dist/meridian-hemisphere.pbw explicitly. Build script retains .tmp/meridian.elf for fault diagnosis. Transient logs and test reports stay in .tmp/.

Browser observed: edition switching retains independent controls; London updates the globe; date fields appear below; reload retains location; a spring DST gap normalizes forward; live view shows America/Chicago local time and a separate UTC solar instant. Browser geolocation was not granted or called. Ambiguous autumn manual time selects the first occurrence; live mode uses the actual instant.

Independent review: verify_hemisphere approved the prototype against the stated contract after inspecting source and native evidence. Final store screenshots in assets/store/meridian/ are emulator captures, not hardware photos. Paired-phone permissions, non-UTC hardware behavior, wrist readability, battery and publication remain open.
