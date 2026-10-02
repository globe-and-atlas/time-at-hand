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
