---
generated_by: "OpenAI Codex (GPT-6)"
timestamp: "2026-09-23"
---
# Time at Hand release notes

## 0.1.8 · Vector, Meridian and Cardinal build fix

- 0.1.7 of Vector, Meridian and Cardinal was built as Origin by mistake (the local build script defaulted
  to edition 0 over each edition branch's edition.h). 0.1.8 restores each edition's own face, with the
  0.1.7 settings: 24-hour hour numbers and custom numeral color.

## 0.1.7 · 24-hour numbers and numeral color (all editions)

- New Hour numbers setting: 12-hour (1 to 12, the default), 24-hour (0 to 23), or follow the watch setting.
- New Custom numeral color: turn it on and pick any of the 64 Pebble colors for the time numerals. Off keeps the automatic black numerals, which turn white on the dark dial.
- Hands, ticks, pivot and date keep their own colors.

## Meridian 0.1.6 · Mac stipple globe texture

- Replaces the experimental low-poly globe treatment with a coarse Classic Mac-style land stipple.
- Renames the Meridian control to Globe texture, with Off, Subtle dots, and Mac stipple options.
- Keeps Subtle dots as the default Meridian texture.
- Preserves custom land/water color controls, saved location, daylight/night overlay, UUID, and existing visual defaults.

Upload this as version 0.1.6 to the existing Meridian dashboard listing.

## Meridian 0.1.5 · globe textures and settings-transfer fix

- Adds Meridian globe texture modes: Off, Subtle dots, and Mac stipple.
- Keeps Subtle dotted as the default Meridian globe look.
- Adds a Meridian-only custom globe color toggle, with water and land color pickers enabled only when custom colors are on.
- Fixes Meridian phone settings not transferring to the watch after the settings payload grew.
- Enlarges AppMessage buffers so the full Meridian settings payload can be delivered reliably.
- Preserves saved location, daylight/night overlay, UUID, and existing visual defaults.

Upload this as version 0.1.5 to the existing Meridian dashboard listing.

## 0.1.2 point release · shared dial and status settings

- All five faces now share light/dark dial theme controls.
- Center pivot visibility can be turned off for a cleaner dial.
- Hour and minute leading-zero formats can be set from the phone app and preview.
- Date order can be changed between weekday-first, day-first, month-first, and ISO-style layouts.
- Optional battery status can be hidden, shown as a percent, shown as a thin bar, or shown only when low.
- Optional Bluetooth disconnect marker adds a small `x` when the phone connection drops.
- Meridian adds land and water color pickers for the globe while preserving its daylight overlay.

Upload this as version 0.1.2 to each existing dashboard listing. The five app identities, names, UUIDs, and direct links remain unchanged.

## 0.1.1 point release · renamed collection and expanded controls

- The five-face series is now named **Origin**, **Vector**, **Meridian**, **Cardinal**, and **Clarity**. UUIDs and existing app links remain unchanged.
- Hand widths now offer 1–8 pixels, while preserving each edition's optical default.
- Hour and minute hand-number labels have independent Small, Medium, and Large size choices.
- Optional twelve-position tick marks can be enabled per face; the default remains off.
- Preview, Clay settings, CloudPebble branches, and phone-preview listings use the same controls and names.

Existing releases remain installable. Upload this as version 0.1.1 to each existing dashboard listing rather than creating new app identities.

## 0.1.0 prototype · unpublished

A globe beneath the hands, with daylight moving across its surface. The hour and minute stay upright near the ends of their own hands.

- Calculated day/night shading follows UTC and the season.
- Darker land, night texture, and globe outline improve contrast on the watch.
- The clock follows your watch's local time, including its daylight-saving setting.
- Center the globe on a city, custom coordinates, or optional phone location.
- Keep the saved globe view when the phone is unavailable.
- Choose from 12 numeral fonts, 64-color hand pickers, and the original five hand-width choices.
- Show any combination of weekday, day, month, and year at the top or bottom.

For Pebble Time 2 (Emery). This is a prototype for sideloading, not a store release. The map is simplified; shading shows geometric day/night, not weather or exact sunrise times. Physical wrist readability, phone permissions, and battery life still need testing. Manual globe location does not change the watch's time zone.

## Clarity and Cardinal · 0.1.0 prototypes

- Clarity: a heavy black hour hand, orange minute hand, and upright numbers at their tips.
- Cardinal: fine black hands with upright tip numbers.
- Cardinal includes four small cardinal marks for orientation; Clarity removes them for a cleaner dial.
- Both include 12 numeral fonts, independent hand color/width controls, and optional date combinations at the top or bottom.
- Separate app identities preserve each edition’s settings. For Pebble Time 2; not published to the store.

Proportion refinement: Vector, Meridian, Cardinal and Clarity move the hour hand and its numeral20% farther from the center. The shorter hour reach remains distinct from the minute hand. Origin retains its full-time hand.
