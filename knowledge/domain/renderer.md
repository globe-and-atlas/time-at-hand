---
generated_by: "OpenAI Codex (GPT-6)"
timestamp: "2026-09-23"
---
# Renderer
The original C renderer is shared by the host preview and native Emery build. Generated `trig.h` provides half-degree sine values to avoid divergent platform math. Native SDK defines PBL_PLATFORM_EMERY, not PBL_PLATFORM; initial guard mistake was replaced with the shared table.

Minute-resolution hour angle is `(hour % 12) * 30 + minute * 0.5`. Only minute zero with hour divisible by three becomes a numeral. Numeral state omits pivot and amber accents so only the requested digit(s) appear. Full-time text flips on the left half. Custom 5x7 glyphs are original data, no external font license dependency.

Background is true white, ink black, accent ChromeYellow. The screen cannot reproduce the subtle paper texture shown in concept renders. Browser palette matches the uncorrected SDK colors, not physical reflectance.

Eight native fixture screenshots matched host pixels exactly. Emulator clock injection is unreliable on Emery; fixed-time compiler fixtures avoid that limitation. The default build omits TAH_TEST_MINUTE and uses localtime.

## Two Hands and settings — 2026-09-23
Two Hands uses hour radius40 and minute radius82; 3× hour glyphs and 2× minute glyphs remain upright. Hour angle includes fractional minutes; minute angle is six degrees per minute. Label clearance masks prevent crossing strokes. Minimum label-rectangle separation is 11px at default geometry across 720 minutes.

Calendar mask bits: weekday1, day2, month4, year8. Position0 top,1 bottom. English uppercase abbreviated names. Date glyph rows4–17 or210–223; dial occupies rows22–205. Date off preserves original pixels. Native date refresh uses localtime on minute ticks.

Twelve original numeral glyph sets are generated from execution/generate_fonts.py into fonts.h, in four groups. Calendar glyphs stay consistent. Selectable hand widths1–8 use half-open stroke spans for distinct even widths; automatic defaults preserve pre-change optical stroke weights. Eight foreground colors use native 2-bit channel values. Labels/pivot remain black. Renderer is serial (style state is internal); preview uses serial HTTPServer.

Clay1.1.0 provides per-edition phone settings. Native AppMessage settings persist with app UUID isolation. Preview uses separate browser localStorage keys per edition; downloads remain generic configurable builds.

## 0.1.1 hand geometry controls — 2026-09-24
The point release keeps the five product names Origin, Vector, Meridian, Cardinal and Clarity, and preserves all UUIDs. Hand width settings accept 1–8 pixels; zero retains the edition optical default. Hour and minute tip labels have independent Small, Medium and Large choices, mapped to 2×, 3× and 4× glyph scales; zero retains the existing hour 3× and minute 2× defaults. Twelve 3×3 outer tick marks are optional and default off. Legacy five-element preview style arrays migrate by appending three default values, and legacy native persistence keys remain unchanged. Host style, label-edge, edition and hemisphere suites pass after the API extension; `verify_incremental.py` remains blocked by its pre-`edition.h` historical fixture.
