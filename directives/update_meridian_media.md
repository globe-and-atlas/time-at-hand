---
generated_by: "OpenAI Codex (GPT-6.1-sol)"
timestamp: "2026-10-19"
---
# Update Meridian Earth media

Goal: show the existing colored Earth controls in Meridian's native Emery listing screenshots and first-position animated GIF.

Inputs: the current C renderer, Meridian color controls, the existing promo suite, and the authenticated RePebble Meridian listing.

Execution: `execution/generate_promo_suite.py` renders the media; `execution/verify_promo_suite.py` validates the generated files; the RePebble listing editor receives the updated Meridian images.

Outputs: `assets/promo-suite/meridian/store/` images and GIF; updated public Meridian listing screenshots.

Safety: preserve other edition media, the current Meridian PBW and listing visibility. Keep credentials and temporary captures outside Git.

## Validation Contract

- Meridian signature screenshot is 200×228.
- Meridian calendar screenshot is 200×228.
- Meridian night screenshot is 200×228.
- Meridian detail screenshot is 200×228.
- Each of those four screenshots contains a visible colored Earth.
- Meridian's animated GIF is 200×228.
- Meridian's animated GIF contains at least three distinct Earth color palettes.
- Each GIF frame comes from the native C renderer.
- The GIF is the first Emery screenshot on the public listing.
- The public search card animates the new colored Earth GIF.
- Other watchface listing media stays unchanged.
- An independent verifier approves the final local media.

## 2026-10-19 — Grayscale and minute-hand examples

Goal: make the default black-and-white Earth and independent minute-hand colors visible in Meridian's current five-slot Emery media set.

Execution: regenerate with `execution/generate_promo_suite.py`; validate with `execution/verify_promo_suite.py`; replace Meridian listing media in the RePebble dashboard.

Outputs: native 200×228 Meridian store images, first-slot GIF, and the updated public listing.

Safety: keep other edition media and Meridian's PBW unchanged; do not commit credentials or `.tmp/` captures.

### Validation Contract

- One published static screenshot shows the default grayscale Earth.
- Three published static screenshots show colored Earth palettes.
- At least two published static screenshots show a minute hand colored differently from the hour hand.
- The first-slot 200×228 GIF includes a grayscale Earth segment.
- The first-slot GIF includes at least three distinct colored Earth palettes.
- The GIF includes a minute-hand color distinct from the hour hand in at least one segment.
- Native C renderer output matches each store screenshot.
- Native C renderer output matches sampled GIF frames.
- The public search card uses the updated first-slot GIF.
- Meridian remains Listed with release 0.1.8.
- Other face listing media remains unchanged.
- A fresh verifier approves the final local media.
