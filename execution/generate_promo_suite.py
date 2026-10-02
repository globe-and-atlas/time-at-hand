#!/usr/bin/env python3
"""Reproducible G&A promotional assets, using unmodified native C face pixels."""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from io import BytesIO
from pathlib import Path
import hashlib
import html
import json
import shutil
import subprocess
import zipfile

from PIL import Image, ImageDraw, ImageFont
from preview import ROOT, frame, load_renderer, png

OUT = ROOT / 'assets/promo-suite'
TMP = ROOT / '.tmp/promo-suite'
PAPER = '#f1eee5'
INK = '#172824'
MUTED = '#53655c'
GRID = '#dedfd3'
FONTS = Path('/System/Library/Fonts/Supplemental')
SPECS = [
    dict(id=0, slug='origin', name='Origin', accent='#b74826', hook='Time is the hand.', sub='One hand. A different way to read time.'),
    dict(id=1, slug='vector', name='Vector', accent='#286858', hook='Follow the numbers.', sub='Hour and minute labels ride their hands.'),
    dict(id=2, slug='meridian', name='Meridian', accent='#335f8a', hook='Wear the day. And night.', sub='A small globe. A changing line of light.'),
    dict(id=3, slug='cardinal', name='Cardinal', accent='#885231', hook='Find your bearings.', sub='Four points. Just enough structure.'),
]


def font(size: int, mono: bool = False):
    return ImageFont.truetype(str(FONTS / ('Courier New.ttf' if mono else 'DIN Alternate Bold.ttf')), size)


def save(image: Image.Image, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    image.convert('RGB').save(path)


def face_image(lib, spec, h=10, m=10, **options):
    settings = dict(calendar=date(2026, 9, 23))
    if spec['id'] == 2:
        settings.update(lat=41.9, lon=-87.6, marker=1,
                        utc=(datetime(2026, 9, 23, h, m, tzinfo=timezone.utc)+timedelta(hours=5)).timestamp())
    settings.update(options)
    return Image.open(BytesIO(png(frame(lib, h, m, spec['id'], **settings)))).convert('RGB')


def background(size):
    image = Image.new('RGB', size, PAPER)
    d = ImageDraw.Draw(image)
    w, h = size
    for x in range(0, w, 40):
        d.line((x, 0, x, h), fill=GRID)
    for y in range(0, h, 40):
        d.line((0, y, w, y), fill=GRID)
    return image


def dial(image, screen, x, y, scale):
    """Abstract display frame, deliberately not a product photograph."""
    d = ImageDraw.Draw(image)
    w, h = round(200 * scale), round(228 * scale)
    rim = max(5, round(scale * 5))
    d.rounded_rectangle((x-rim+5, y-rim+7, x+w+rim+5, y+h+rim+7), radius=rim*2, fill='#c3c7b9')
    d.rounded_rectangle((x-rim, y-rim, x+w+rim, y+h+rim), radius=rim*2, fill=INK)
    image.paste(screen.resize((w, h), Image.Resampling.NEAREST), (x, y))


def layout(spec, screen, size, motion=False):
    im = background(size)
    d = ImageDraw.Draw(im)
    w, h = size
    compact = w == 600
    margin = 26 if w <= 720 else 56
    small = 12 if w <= 720 else 21
    d.text((margin, margin), 'G&A  /  GLOBE AND ATLAS', font=font(small, True), fill=INK)
    d.text((w-margin, margin), f"0{spec['id']+1}", anchor='ra', font=font(small, True), fill=spec['accent'])
    if w > h:
        scale = 1 if h == 320 else 2
        x, y = w - margin - 200*scale - 12, (h - 228*scale)//2
        d.text((margin, 78 if h==320 else 138), spec['name'], font=font(53 if h==320 else 94), fill=INK)
        d.text((margin, 147 if h==320 else 256), spec['hook'], font=font(22 if h==320 else 34), fill=spec['accent'])
        d.text((margin, h-65), 'WATCHFACE / PEBBLE TIME 2', font=font(small, True), fill=INK)
        dial(im, screen, x, y, scale)
    else:
        scale = 2 if compact else 3
        title_y = 56 if compact else 100
        title_size = 56 if compact else 108
        d.text((margin, title_y), spec['name'], font=font(title_size), fill=INK)
        # Square animations prioritize the readable display over extra copy.
        if compact:
            dial(im, screen, 150, 149, 1.5)
            d.text((300, 510), spec['hook'], anchor='ma', font=font(28), fill=spec['accent'])
        else:
            y = (278 if h == 1080 else 260) if h <= 1350 else 460
            dial(im, screen, (w-200*scale)//2, y, scale)
            if h >= 1350:
                d.text((w//2, y+228*scale+90), spec['hook'], anchor='ma', font=font(47), fill=spec['accent'])
                d.text((w//2, y+228*scale+153), spec['sub'], anchor='ma', font=font(26), fill=INK)
            else:
                d.text((margin, 220), spec['hook'], font=font(32), fill=spec['accent'])
        footer = 'TIME-LAPSE / PEBBLE TIME 2' if motion else 'WATCHFACE / PEBBLE TIME 2'
        d.line((margin, h-margin-36, w-margin, h-margin-36), fill=INK, width=1)
        d.text((margin, h-margin-20), footer, font=font(small, True), fill=INK)
    return im


def thumbnail(screen, size):
    im = Image.new('RGB', (size, size), PAPER)
    # Largest complete face possible, no crop, no text competing with the dial.
    height = int(size * .90)
    width = round(height * 200 / 228)
    im.paste(screen.resize((width, height), Image.Resampling.NEAREST), ((size-width)//2, (size-height)//2))
    return im


def video(frames, target, work):
    work.mkdir(parents=True, exist_ok=True)
    for i, image in enumerate(frames):
        save(image, work / f'{i:03d}.png')
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-framerate', '4',
                    '-i', str(work/'%03d.png'), '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p',
                    '-vf', 'fps=24', '-movflags', '+faststart', str(target)], check=True)


def main():
    if not shutil.which('ffmpeg'):
        raise SystemExit('ffmpeg is required before asset generation.')
    OUT.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    lib = load_renderer()
    records = []
    heroes = []
    gallery = []
    for spec in SPECS:
        directory = OUT / spec['slug']
        store = directory / 'store'
        promo = directory / 'promotion'
        store.mkdir(parents=True, exist_ok=True)
        promo.mkdir(parents=True, exist_ok=True)
        configs = [
            ('01-signature', dict()),
            ('02-calendar', dict(mask=3, position=1, h=3, m=30)),
            ('03-night', dict(h=8, m=45, theme=1, color=2, minute_color=2)),
            ('04-custom', dict(h=1, m=50, color=6, minute_color=8, width=5, minute_width=3, font=3)),
            ('05-detail', dict(h=3, m=0) if spec['id']==0 else
             dict(h=10, m=10, wireframe=2) if spec['id']==2 else
             dict(h=10, m=10, ticks=1, hour_label_size=3, minute_label_size=2)),
        ]
        for name, config in configs:
            image = face_image(lib, spec, **config)
            save(image, store/f'{name}.png')
            records.append(dict(path=f"{spec['slug']}/store/{name}.png", edition=spec['id'], config=config,
                                sha256=hashlib.sha256(image.tobytes()).hexdigest()))
        hero = face_image(lib, spec)
        heroes.append(hero)
        for size in (48, 80, 144, 512):
            save(thumbnail(hero, size), store/f'thumbnail-{size}.png')
        for filename, size in [('banner-720x320', (720,320)), ('cover-1200x630', (1200,630)),
                               ('square-1080', (1080,1080)), ('portrait-1080x1350', (1080,1350)),
                               ('story-1080x1920', (1080,1920))]:
            save(layout(spec, hero, size), (store if filename.startswith('banner') else promo)/f'{filename}.png')
        native_frames = []
        for i in range(48):
            # Minute-stepped acceleration; never fabricate continuous hand physics.
            minutes = 600 + i*(30 if spec['id']==2 else 15)
            instant = datetime(2026,9,23,15,0,tzinfo=timezone.utc) + timedelta(minutes=i*30)
            opts = dict(utc=instant.timestamp()) if spec['id']==2 else {}
            native_frames.append(face_image(lib, spec, h=(minutes//60)%24, m=minutes%60, **opts))
        native_frames[0].save(store/'timelapse-200x228.gif', save_all=True, append_images=native_frames[1:], duration=250, loop=0, disposal=2)
        gif_frames = [layout(spec, f, (600,600), True) for f in native_frames]
        gif_frames[0].save(promo/'timelapse-600.gif', save_all=True, append_images=gif_frames[1:], duration=250, loop=0, disposal=2)
        for name, size in [('square', (1080,1080)), ('vertical', (1080,1920))]:
            video([layout(spec, f, size, True) for f in native_frames], promo/f'timelapse-{name}.mp4', TMP/spec['slug']/name)
        gallery.append(f'''<section id="{spec['slug']}"><header><span>0{spec['id']+1}</span><h2>{spec['name']}</h2><p>{spec['hook']}</p></header>
<div class="edition"><video controls loop muted playsinline preload="none" poster="{spec['slug']}/promotion/square-1080.png"><source src="{spec['slug']}/promotion/timelapse-square.mp4" type="video/mp4"></video><div><h3>The listing</h3><div class="screens">'''+''.join(f'<a href="{spec["slug"]}/store/{name}.png"><img alt="{spec["name"]}: {html.escape(name)}" src="{spec["slug"]}/store/{name}.png"></a>' for name,_ in configs)+f'''</div><p>200 × 228. Unframed. Current C renderer.</p><p><a href="{spec['slug']}/store/banner-720x320.png">Listing banner</a> · <a href="{spec['slug']}/store/thumbnail-144.png">Thumbnail</a> · <a href="{spec['slug']}/store/timelapse-200x228.gif">Native GIF</a></p><h3>Share it</h3><p><a href="{spec['slug']}/promotion/cover-1200x630.png">Article cover</a> · <a href="{spec['slug']}/promotion/portrait-1080x1350.png">Portrait</a> · <a href="{spec['slug']}/promotion/story-1080x1920.png">Story</a></p><p><a href="{spec['slug']}/promotion/timelapse-600.gif">Social GIF</a> · <a href="{spec['slug']}/promotion/timelapse-square.mp4">Square MP4</a> · <a href="{spec['slug']}/promotion/timelapse-vertical.mp4">Vertical MP4</a></p></div></div></section>''')
        print(f"Created {spec['name']}", flush=True)
    sheet = background((1600,1100))
    d = ImageDraw.Draw(sheet)
    d.text((55,45), 'Four ways to find your time.', font=font(66), fill=INK)
    d.text((57,133), 'GLOBE AND ATLAS  /  PEBBLE TIME 2', font=font(24, True), fill=MUTED)
    for i,(spec,hero) in enumerate(zip(SPECS, heroes)):
        x=65+i*390
        d.text((x,210), f"0{i+1} / {spec['name']}", font=font(36), fill=spec['accent'])
        # Full screen shown at 1:1 plus customized companion below, no cropping.
        dial(sheet, hero, x+65, 295, 1)
        d.text((x,569), spec['hook'], font=font(25), fill=INK)
        for j,case in enumerate(['02-calendar','03-night','05-detail']):
            with Image.open(OUT/spec['slug']/'store'/f'{case}.png') as im:
                sheet.paste(im.resize((100,114),Image.Resampling.NEAREST), (x+j*112,645))
        d.text((x,783), 'CALENDAR / NIGHT / DETAIL', font=font(16,True), fill=MUTED)
    d.line((55,910,1545,910),fill=INK)
    d.text((55,950),'Actual face renderer. Your colors, your typography, your time.',font=font(31),fill=INK)
    save(sheet, OUT/'contact-sheet.png')
    # Article-wide suite card, distinct from the detailed contact sheet.
    suite=background((1600,900));d=ImageDraw.Draw(suite)
    d.text((60,48),'G&A / TIME STUDIES',font=font(24,True),fill=INK)
    d.text((60,114),'Four ways to find your time.',font=font(72),fill=INK)
    for i,(spec,hero) in enumerate(zip(SPECS,heroes)):
        x=95+i*390
        dial(suite,hero,x+35,325,1)
        d.text((x,615),spec['name'],font=font(41),fill=spec['accent'])
    d.text((60,802),'ORIGIN / VECTOR / MERIDIAN / CARDINAL',font=font(23,True),fill=INK)
    save(suite,OUT/'suite-cover-1600x900.png')
    css='''*{box-sizing:border-box}body{margin:0;background:#f1eee5;color:#172824;font:18px Georgia,serif}main{max-width:1400px;margin:auto;padding:48px}h1{font-size:clamp(40px,6vw,80px);font-weight:400;line-height:1.05;max-width:850px}h2{font-size:44px;margin:0}h3{font:20px monospace}a{color:#286858;text-underline-offset:4px}a:focus-visible{outline:3px solid #b74826}nav{display:flex;flex-wrap:wrap;gap:24px}section{border-top:1px solid #718077;padding:40px 0;margin-top:48px}header{display:flex;align-items:baseline;gap:24px;flex-wrap:wrap}.edition{display:grid;grid-template-columns:1fr 1fr;gap:40px;margin-top:24px}video{width:100%;height:auto}.screens{display:flex;flex-wrap:wrap;gap:12px}.screens img{width:100px;height:114px;image-rendering:pixelated}p{line-height:1.6}.note{max-width:900px} @media(max-width:800px){main{padding:24px}.edition{grid-template-columns:1fr}}'''
    (OUT/'index.html').write_text(f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>G&A — Time studies</title><style>{css}</style><main><p>GLOBE AND ATLAS / ASSET LIBRARY</p><h1>Four ways to find your time.</h1><p>Origin. Vector. Meridian. Cardinal.</p><nav>'''+''.join(f'<a href="#{s["slug"]}">{s["name"]}</a>' for s in SPECS)+'''<a href="contact-sheet.png">Contact sheet</a><a href="../pebble-promo-suite.zip">Download ZIP</a></nav><p class="note">Animations are accelerated time-lapses, not real-time smooth sweeps. Images use the current watchface C renderer; they are not device photographs. Videos play only when you press play.</p>'''+''.join(gallery)+'''<footer><p>Prepared for Pebble Time 2 / Emery. Current dashboard field limits still require confirmation. Store screenshots stay unframed; promotional artwork uses an abstract display frame.</p></footer></main></html>''')
    instructions='''---
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
| store/thumbnail-{48,80,144,512}.png | Complete dial on square paper ground; dashboard recommends 80 small and 144 large |
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
'''
    (OUT/'README.md').write_text(instructions)
    files=[]
    for path in sorted(OUT.rglob('*')):
        if path.is_file() and path.name not in ('manifest.json','verification.json'):
            files.append(dict(path=str(path.relative_to(OUT)),bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    (OUT/'manifest.json').write_text(json.dumps(dict(editions=[s['slug'] for s in SPECS],screenshots=records,files=files),indent=2)+'\n')
    with zipfile.ZipFile(ROOT/'assets/pebble-promo-suite.zip','w',zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(OUT.rglob('*')):
            if path.is_file(): archive.write(path,Path('promo-suite')/path.relative_to(OUT))
    print(f'Created {len(files)} assets/documents plus manifest and ZIP: {OUT}')


if __name__ == '__main__':
    main()
