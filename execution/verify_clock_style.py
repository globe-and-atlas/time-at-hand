#!/usr/bin/env python3
"""Clock style checks: 24-hour hour labels and custom numeral colour, against the shared C renderer."""
import ctypes
from preview import load_renderer, W, H

CUSTOM = 10 + 3 * 16  # palette index for pure red (r=3, g=0, b=0)


def full(lib, h, m, edition, theme=0):
    buf = (ctypes.c_uint8 * (W * H))()
    # font, colours, widths and sizes at edition defaults; no ticks; hour/minute formats 0/1; pivot on
    lib.face_render_full(h, m, edition, 2026, 10, 1, 4, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 1, theme, 1, buf)
    return bytes(buf)


def verify():
    lib = load_renderer()
    lib.face_clock_style.argtypes = [ctypes.c_int, ctypes.c_int]
    label = ctypes.create_string_buffer(6)

    lib.face_clock_style(1, 1)
    for t in range(1440):
        h, m = divmod(t, 60)
        lib.face_label(h, m, label)
        expected = str(h) if m == 0 and h % 3 == 0 else f"{h}:{m:02}"
        assert label.value.decode() == expected, (h, m, label.value)

    lib.face_clock_style(0, 1)  # back to the defaults: 12-hour labels
    lib.face_label(15, 30, label)
    assert label.value == b"3:30"
    lib.face_label(0, 0, label)
    assert label.value == b"12"

    for edition in range(5):
        lib.face_clock_style(0, 1)
        default = full(lib, 10, 10, edition)
        assert CUSTOM not in default
        lib.face_clock_style(0, CUSTOM)
        custom = full(lib, 10, 10, edition)
        assert CUSTOM in custom, edition
        # Only numeral pixels move: every changed pixel was automatic ink (1) and is now the custom colour.
        changed = [(a, b) for a, b in zip(default, custom) if a != b]
        assert changed and all(a == 1 and b == CUSTOM for a, b in changed), edition
        # The dark dial inverts automatic ink but leaves a custom numeral colour alone.
        if edition != 2:
            assert CUSTOM in full(lib, 10, 10, edition, theme=1)

    lib.face_clock_style(0, 99)  # out of range falls back to automatic
    assert CUSTOM not in full(lib, 10, 10, 0)
    lib.face_clock_style(0, 1)
    print("clock style: 24-hour labels for 1440 minutes; numeral colour across 5 editions; PASS")


if __name__ == "__main__":
    verify()
