---
generated_by: "OpenAI Codex (GPT-6)"
timestamp: "2026-09-27"
---
# G&A Pebble promotional suite

Scope: Origin, Vector, Meridian, Cardinal. Clarity is retired.

Open index.html for a playable gallery. Start with contact-sheet.png to choose the listing order. suite-cover-1600x900.png is the collection-wide article image.

## Per-face assets

| Asset | Use |
|---|---|
| store/01-signature.png | Lead screenshot; authentic default appearance |
| store/02-calendar.png | Calendar example |
| store/03-night.png | Dark theme example |
| store/04-custom.png | Color, line width and font example |
| store/05-detail.png | Origin exact-hour numeral; Meridian Mac stipple; Vector/Cardinal larger labels and ticks |
| store/thumbnail-{48,144,512}.png | Complete dial on square paper ground; choose the size requested by the dashboard |
| store/banner-720x320.png | Listing banner candidate, established legacy size |
| store/timelapse-200x228.gif | Animated screenshot alternative; replace a PNG, do not add a sixth slot |
| promotion/cover-1200x630.png | Article/social link cover |
| promotion/square-1080.png | Square post |
| promotion/portrait-1080x1350.png | Portrait post |
| promotion/story-1080x1920.png | Story still |
| promotion/timelapse-600.gif | Lightweight labelled social animation |
| promotion/timelapse-square.mp4 | 1080 square, 12-second silent video |
| promotion/timelapse-vertical.mp4 | 1080x1920, 12-second silent video |

## Suggested launch order

Lead with Meridian's day/night animation as the most visually distinctive image. Follow with Origin to explain the time-as-hand idea. Use Vector and Cardinal to show the quieter alternatives. Test static versus animation engagement rather than assuming motion guarantees attention.

Suggested captions:
- Origin: Time is the hand. A different way to read your Pebble.
- Vector: Follow the numbers. Hour and minute labels, right where you need them.
- Meridian: Wear the day. And night. A tiny globe with solar day/night shading.
- Cardinal: Find your bearings. Four points and room to breathe.

Append to animated posts: "Accelerated time-lapse; watch updates by the minute."

## Accuracy and upload boundaries

The images are generated from the current local C renderer at native 200x228 Emery resolution, not captured from hardware. Calendar/date and style variants are explicitly selected examples, not new defaults. Host previews omit the separate battery/Bluetooth status overlay. No untested battery claims, weather, live satellite imagery, continuous sweeping or gravity behavior are advertised.

Each animation contains 48 frames at 250 ms per frame. Origin/Vector/Cardinal advance 15 watch minutes per frame over a 12-hour loop. Meridian advances 30 watch minutes per frame over a 24-hour loop; local Chicago time and UTC are paired for September 23, 2026 (UTC-5), with a fixed location-centered globe and changing solar shadow. Repeating the Meridian clip resets the date rather than demonstrating continuous multi-day evolution. The native GIF has no marketing text overlay, so disclose the time-lapse in listing copy.

Official guide: https://developer.rebble.io/guides/appstore-publishing/preparing-a-submission/ allows up to five screenshots per platform in PNG/GIF/animated GIF. https://developer.rebble.io/guides/appstore-publishing/appstore-assets/ says listing screenshots must be unframed. Current authenticated dashboard dimensions/file limits were not accessible; 720x320 banners and square thumbnail sizes are prepared candidates, not verified current field requirements. No uploads, release changes or publication are included. MP4s are for external promotion, not assumed dashboard inputs.

Rebuild: `python3 execution/generate_promo_suite.py`
Verify: `python3 execution/verify_promo_suite.py`
Requires Pillow, a C compiler, macOS DIN Alternate/Courier New fonts and ffmpeg. Fonts are rasterized, not redistributed. Intermediate video frames live in .tmp/promo-suite/.
