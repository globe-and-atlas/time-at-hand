---
generated_by: "OpenAI Codex (GPT-6)"
timestamp: "2026-09-27"
---
# Prepare promotional assets

`python3 execution/generate_promo_suite.py` creates `assets/promo-suite/` plus `assets/pebble-promo-suite.zip`. Requires existing Pillow, cc, ffmpeg and local macOS DIN Alternate/Courier New fonts. No dependencies were installed. Intermediates stay in `.tmp/promo-suite/`.

Scope is Origin, Vector, Meridian and Cardinal; exclude retired Clarity. The generator calls the current C renderer through execution/preview.py. Screenshots are 200x228 Emery, without frames. Promotional artwork uses an abstract rectangular display frame, not a simulated device photo.

Per edition: five PNG screenshot variants; three square thumbnails (48/144/512); 720x320 banner; 1200x630 article image; 1080 square; 1080x1350 portrait; 1080x1920 story; native GIF; 600-square promotional GIF; square and vertical MP4. Also creates suite contact sheet, article cover, index.html gallery, README usage guide and SHA-256 manifest. Total: 54 PNG, eight GIF, eight MP4.

`python3 execution/verify_promo_suite.py` checks screenshot pixels, decoded native GIF pixels, file hashes, dimensions, video format/duration, gallery link targets and ZIP integrity. Animation frames are discrete accelerated time: 12 hours for Origin/Vector/Cardinal, 24 hours for Meridian in 12 seconds. Meridian ties Chicago local time to UTC-5 for September 23, 2026; globe center stays fixed while solar shading changes.

Inspect the sheet, square, banner and portrait outputs before shipping. Do not let square-card subtitles overlap the display rim. Store PNGs match renderer pixels, but the host path omits separate battery/Bluetooth overlays. No hardware capture or browser playback is implied.

The official archived Pebble submission guide allows five PNG/GIF/animated GIF screenshots per platform. A native GIF replaces a PNG slot; it does not add a sixth. Current authenticated dashboard thumbnail/banner dimensions and file size caps remain unverified. GIF/MP4 promotion should disclose accelerated time. No asset upload, release update, or remote publishing was part of creation.

The native browser bridge was unavailable during review; rely on recorded file/frame checks only until live playback/upload can be observed.

## 2026-09-27 Current dashboard checks
Authenticated editor inspected for Origin: screenshots must be 200x228, banner 720x320; small icon recommended 80x80, large icon recommended 144x144. Generator now includes 80px thumbnails (58 PNGs in total; GIF/MP4 counts unchanged). This supersedes the older unverified-dimensions note above; file size limits remain unverified.

Browser connection now works. Extension fileChooser.setFiles requires ChatGPT extension Allow access to file URLs. Do not toggle security-sensitive extension permissions without user confirmation. Native picker fallback can be interrupted when another task/user changes Chrome's foreground tab; preserve the editor and request the supported upload permission instead of repeatedly competing for focus.

## 2026-09-27 Successful dashboard upload
Origin, Vector, Meridian and Cardinal saved successfully. Each retained its existing signature PNG, added timelapse-200x228.gif, 02-calendar.png and 03-night.png. Fourth addition was 04-custom.png for Origin/Vector/Cardinal, 05-detail.png (Mac stipple) for Meridian. Each received banner-720x320.png, thumbnail-80.png and thumbnail-144.png. Total newly uploaded: 28 files. MP4/social cards are external-promotion assets and were not submitted to the dashboard.

Descriptions retain original copy plus: Preview animation is an accelerated time-lapse; the watch updates once per minute. Reopened all four editors after save and verified five screenshot server URLs, 720x320 banner, 80px and 144px icons. Meridian's public page displayed the new banner and five screenshots. Proof: .tmp/upload-proof/meridian-public.png. Listed visibility was preserved; no PBW/release edits.

After enabling extension file-URL access, the old browser binding still reported permission errors. A fresh inventory showed the same Chrome extension instance with a new browser connection ID; binding that refreshed connection fixed uploads. Keep a dedicated verification tab when the user is navigating elsewhere. A save wait timeout did not mean failure: fresh dashboard state showed the new icon; reopening the editor confirmed persistence.
## 2026-10-17 — Search preview ordering

Repebble search cards use the first screenshot for the selected platform. Cardinal, Meridian, Vector, and Origin have their 200×228 time-lapse GIF first in the Emery screenshot list as of 2026-10-17. The four static screenshots remain after it. Verify the public search card `img` URL ends in `.gif` after editing.

## 2026-10-19 — Meridian colored Earth media

Set Meridian land/water colors in `MERIDIAN_PALETTES` in `execution/generate_promo_suite.py`; store stills use four palettes and the 48-frame native GIF changes palette every 12 frames. Run `python3 execution/generate_promo_suite.py` followed by `python3 execution/verify_promo_suite.py`. Four sampled GIF frames (0, 12, 24, 36) show distinct palettes at 200×228. Keep listing copy explicit that palette changes are preview examples and watch colors remain chosen until the wearer changes them.

For a media-only dashboard update, open Meridian's Edit Listing form, remove the five current Emery screenshot entries in the form, then use the multiple-file screenshot input for the new GIF followed by four PNGs. Start `waitForEvent('filechooser')` before clicking the input and await it after the click. Save once; a return to the dashboard is not enough by itself. Reopen the editor and check five persisted screenshot URLs, `.gif` first, plus description, visibility, and release version. The public app/search views can lag behind the saved dashboard state; check them separately.

The 2026-10-19 upload also replaced the 720×320 banner and 80/144px icons. The public search card loaded the new GIF URL before the detail page did; a later detail-page reload showed the new screenshot URLs. Asset propagation is independent of version changes: release 0.1.8 stayed in place.

For visual proof after a public-page reload, request a fresh accessibility tree before using a screenshot container index for scrolling; indices from before the reload are stale. The public detail-page screenshot row showed the colored GIF and PNGs on 2026-10-19 (`.tmp/meridian-live-colored.png`).

## 2026-10-19 — Meridian grayscale and minute-hand examples

Meridian's store set now starts with a 48-frame, 200×228 GIF: blue/green, teal/sand, the original black-and-white globe, indigo/sage, and blue/tan. The static order after the GIF is grayscale signature, teal/sand calendar with a purple minute hand, indigo/sage night with a white minute hand, and blue/tan detail with a purple minute hand. Minute width is 3px in colored examples so it reads at native resolution. The grayscale still uses the watch's default palette and hands. The Meridian night media time is 10:15 so the two hands separate visually.

Regenerate with `python3 execution/generate_promo_suite.py` and validate with `python3 execution/verify_promo_suite.py`. `meridian_style(frame_index)` supplies the GIF palette; store stills use the same style table. The verifier compares native C renderer pixels, decoded GIF frames, sizes, hashes, gallery links, and ZIP contents. Keep the preview disclosure in listing copy: the animation accelerates time and cycles through sample settings; the watch updates once per minute with the wearer's chosen settings.

The authenticated Meridian edit form was saved with five new Emery screenshots, banner, and 80/144px icons. Reopening the editor showed five new screenshot URLs with `.gif` first. The public search card and detail page later loaded that new GIF URL; the detail page served the same four static image URLs. Listed visibility and PBW release 0.1.8 stayed unchanged. Live page proof: `.tmp/meridian-gray-live.png`. This was media and listing-copy work, with no watchface C or PBW edit.
