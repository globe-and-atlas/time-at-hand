#!/usr/bin/env python3
"""Generate listing-ready renderer PNGs for the five public editions."""
from __future__ import annotations

from datetime import date, datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from preview import ROOT, W, H, frame, load_renderer, png

EDITIONS = [
    (0, "origin", "Origin"),
    (1, "vector", "Vector"),
    (2, "meridian", "Meridian"),
    (3, "cardinal", "Cardinal"),
    (4, "clarity", "Clarity"),
]

CASES = [
    ("default", "Default", dict(h=10, m=10, mask=0, position=0, calendar=date(2026, 9, 23))),
    ("calendar", "Calendar", dict(h=3, m=30, mask=15, position=1, calendar=date(2026, 9, 23), font=3)),
    ("dark", "Dark", dict(h=8, m=45, mask=3, position=0, calendar=date(2026, 12, 21), theme=1, ticks=0, battery_mode=0)),
]


def render_case(lib, edition: int, case: dict) -> bytes:
    values = dict(case)
    h = values.pop("h")
    m = values.pop("m")
    values.pop("battery_mode", None)
    if edition == 2:
        values.setdefault("utc", datetime(2026, 9, 23, 17, 10, tzinfo=timezone.utc).timestamp())
        values.setdefault("lat", 41.9)
        values.setdefault("lon", -87.6)
        values.setdefault("marker", 1)
    return frame(lib, h, m, edition, **values)


def write_png(path: Path, pixels: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(png(pixels))
    with Image.open(path) as image:
        assert image.size == (W, H), path


def make_contact_sheet(files: list[tuple[str, str, Path]], target: Path) -> None:
    scale = 2
    label_h = 38
    margin = 24
    gap = 18
    cols = 3
    rows = 5
    sheet = Image.new("RGB", (margin * 2 + cols * W * scale + (cols - 1) * gap,
                              margin * 2 + rows * (H * scale + label_h) + (rows - 1) * gap),
                      (241, 239, 231))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    for index, (edition, label, path) in enumerate(files):
        col = index % cols
        row = index // cols
        x = margin + col * (W * scale + gap)
        y = margin + row * (H * scale + label_h + gap)
        with Image.open(path) as image:
            image = image.convert("RGB").resize((W * scale, H * scale), Image.Resampling.NEAREST)
        sheet.paste(image, (x, y + label_h))
        draw.text((x, y), f"{edition} · {label}", fill=(36, 38, 34), font=font)
    target.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(target)


def main() -> None:
    lib = load_renderer()
    output = ROOT / "assets" / "listing-images"
    generated: list[tuple[str, str, Path]] = []
    for edition, slug, name in EDITIONS:
        for case_slug, label, case in CASES:
            target = output / slug / f"{case_slug}.png"
            write_png(target, render_case(lib, edition, case))
            generated.append((name, label, target))
            print(target)
        preview = output / slug / "emery_preview.png"
        write_png(preview, render_case(lib, edition, CASES[0][2]))
    make_contact_sheet(generated, output / "contact-sheet.png")
    print(output / "contact-sheet.png")


if __name__ == "__main__":
    main()
