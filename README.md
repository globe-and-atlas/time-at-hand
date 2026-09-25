> **Generated branch: Cardinal edition.** CloudPebble builds Cardinal from `watchface/` ([import](https://cloudpebble.repebble.com/ide/import/github/globe-and-atlas/time-at-hand/edition-four-points)). Don't edit here: change `main`, then run `python3 execution/publish_edition_branches.py --push`. Generated from main 521d1dc.

---
generated_by: "OpenAI Codex (GPT-6)"
timestamp: "2026-09-23"
---
# Time at Hand

A native Pebble Time 2 watchface experiment with a matching local preview and article evidence kit.

Five editions: Origin puts the full digital time along an hour hand; Vector places upright hour and minute numbers near their respective hand tips; Meridian adds a globe with calculated day/night shading beneath those two hands, now with configurable land and water colors. Cardinal adds four cardinal marks and fine black hands; Clarity removes orientation marks and uses a heavier black hour hand with an orange minute hand. Origin reduces to a single upright numeral at 3:00, 6:00, 9:00 and 12:00 for that minute. The other editions retain both numbers. The two-hand editions use a48px hour track and82px minute track, with upright tip numerals. The clock uses local time and 12-hour notation; AM/PM is intentionally not displayed.

Each offers 12 original pixel numeral fonts (Pixel, Retro, Modern, Classic), 64-color hand pickers, widths of 1–8 pixels, independent hour/minute label sizes, optional twelve-position tick marks, light/dark dial themes, center-pivot visibility, leading-zero formats, optional battery/Bluetooth status, and optional weekday/day/month/year combinations at the top or bottom with selectable date order. The four two-hand editions style each hand independently. Date typography stays constant. Defaults retain the original appearance with date hidden, ticks off, light dial and no battery indicator.

Hemisphere uses UTC plus the date for sunlight, independently of local daylight saving. Choose a manual city/coordinates or opt into phone location; the saved center works offline. The world-view default has no location marker. Coordinates change the globe view, not the watch time zone. See [Hemisphere design notes](knowledge/domain/hemisphere.md).

## Try it now

```bash
cd /Users/danielbally/Git/time-at-hand
python3 execution/preview.py
```

Open http://127.0.0.1:4286. Select an edition; adjust time, typography, hands and calendar. Browser preferences persist separately per edition. The dial stays visible while scrolling settings. PNGs use the same C renderer as the watch. The preview is not a physical reflectance simulation. Browser choices do not rewrite downloads: use each watchface's settings in the Pebble phone app after installation.

## Build and install

SDK installed for this session: Pebble CLI 5.0.40, SDK 4.33.1. Native target: Emery only (Pebble Time 2).

```bash
cd /Users/danielbally/Git/time-at-hand
python3 execution/build_editions.py
cd watchface
pebble install --emulator emery ../dist/vector.pbw
```

Installable outputs: `dist/origin.pbw`, `dist/vector.pbw`, `dist/meridian.pbw`, `dist/cardinal.pbw`, and `dist/clarity.pbw`. Each has its own UUID, so the five can coexist. The build script restores the source manifest and default build to Origin. Each preview edition links its matching download.

For the physical watch, open the current Pebble mobile app, enable Dev Connect from Devices, then authenticate personally. From `watchface/`:

```bash
pebble login
pebble install --cloudpebble ../dist/vector.pbw
```

The build needs no API key. Bundled Clay phone-side JavaScript provides offline settings; no custom phone app, hosted settings page, or preview server is needed on the wrist. No store submission is needed for sideloading. Official setup: https://developer.repebble.com/sdk/

## Verify

```bash
python3 execution/verify.py
python3 execution/verify_editions.py
python3 execution/verify_clear_points.py
python3 execution/verify_calendar.py
python3 execution/verify_styles.py
python3 execution/verify_hemisphere.py
node execution/verify_location.js
python3 execution/verify_preview.py
/Users/danielbally/.local/share/uv/tools/pebble-tool/bin/python3 execution/check_hemisphere_emulator.py
/Users/danielbally/.local/share/uv/tools/pebble-tool/bin/python3 execution/check_calendar_emulator.py
/Users/danielbally/.local/share/uv/tools/pebble-tool/bin/python3 execution/inspect_bundles.py
```

Host checks cover default preservation, 5,920 calendar-format cases, 17,280 styled time states, common display toggles, and the four date-order layouts. Emulator fixtures compare native pixels and persistent preferences, then rebuild the three live-clock bundles in finally. Emulator protocol issues are logged in knowledge/ERRORS.md. Reports/screenshots live in `.tmp/`, never committed. Do not distribute a PBW built with `TAH_TEST_MINUTE` set.

## Publishing
See [PUBLISH.md](PUBLISH.md) for the Pebble dashboard route, bundle choices and physical checks still needed before a public release. Nothing has been uploaded or published.

## Article

`article/draft.md` is a working draft about the experiment so far. `article/field-notes.md` holds provenance, evidence limits and questions for the physical trial. Neither is published. Hardware readability, battery measurements and wearer observations remain untested.

## CloudPebble

Each edition has its own importable branch. The links fill in the branch: CloudPebble's import form defaults an empty branch to `master`, which doesn't exist here.

| Edition | Branch | Import |
| --- | --- | --- |
| Origin | `main` | [Open in CloudPebble](https://cloudpebble.repebble.com/ide/import/github/globe-and-atlas/time-at-hand/main) |
| Vector | `edition-two-hands` | [Open in CloudPebble](https://cloudpebble.repebble.com/ide/import/github/globe-and-atlas/time-at-hand/edition-two-hands) |
| Meridian | `edition-meridian` | [Open in CloudPebble](https://cloudpebble.repebble.com/ide/import/github/globe-and-atlas/time-at-hand/edition-meridian) |
| Cardinal | `edition-four-points` | [Open in CloudPebble](https://cloudpebble.repebble.com/ide/import/github/globe-and-atlas/time-at-hand/edition-four-points) |
| Clarity | `edition-clear` | [Open in CloudPebble](https://cloudpebble.repebble.com/ide/import/github/globe-and-atlas/time-at-hand/edition-clear) |

The import form pre-fills the project name with the account name (`globe-and-atlas`), so rename it in the dialog.

How it works. CloudPebble finds `watchface/package.json`, imports only `.c`/`.h` files from `src/c` and `.js`/`.json` files from `src/pkjs`, and replaces our `wscript` with its own:
- Renderer fragments included by `face.c` use `.h` names (`face_colors.h`, `face_globe.h`), not `.inc`.
- The edition comes from `watchface/src/c/edition.h`: 0 on main. Locally, `build_editions.py` passes `-DTAH_EDITION` through our `wscript`, which takes precedence.
- The `edition-*` branches are generated. Each is main plus one commit setting that edition's manifest, phone settings and `edition.h`. **Don't edit them.** Change main, then:

```bash
python3 execution/build_editions.py                   # dist/ must match main
python3 execution/publish_edition_branches.py         # generate and verify each branch
python3 execution/publish_edition_branches.py --push  # then force-push the edition-* branches
```

Verification: `execution/cloudpebble.py` simulates CloudPebble's import (its file filter and its generated `wscript`, from coredevices/cloudpebble @ 08298a2). The publish script builds every branch that way and requires the same manifest identity, identical phone JS, and an app binary identical to the local `dist/` build apart from the CRC, timestamp and build ID.
