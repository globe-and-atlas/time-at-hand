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

    # Split editions: the hour number near the short hand follows the 24-hour setting too.
    class Num(ctypes.Structure):
        _fields_ = [("x", ctypes.c_int), ("y", ctypes.c_int), ("width", ctypes.c_int),
                    ("height", ctypes.c_int), ("scale", ctypes.c_int), ("text", ctypes.c_char * 3)]
    lib.face_split_layout.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(Num)]
    nums = (Num * 2)()
    for h, want12, want24 in [(0, b"12", b"0"), (9, b"9", b"9"), (15, b"3", b"15"), (23, b"11", b"23")]:
        lib.face_clock_style(0, 1); lib.face_split_layout(h, 30, nums)
        assert nums[0].text == want12, (h, nums[0].text)
        lib.face_clock_style(1, 1); lib.face_split_layout(h, 30, nums)
        assert nums[0].text == want24, (h, nums[0].text)
    for edition in range(1, 5):
        lib.face_clock_style(0, 1); twelve = full(lib, 15, 30, edition)
        lib.face_clock_style(1, 1); assert full(lib, 15, 30, edition) != twelve, edition

    # Origin, Large hour labels in 24-hour mode: nothing is clipped. The face keeps labels 3 px from
    # the edge (clamp_label_start); the 6 px margin in verify.py applies to the default sizes.
    lib.face_clock_style(1, 1)
    for t in range(780, 1440):
        h, m = divmod(t, 60)
        buf = (ctypes.c_uint8 * (W * H))()
        lib.face_render_full(h, m, 0, 2026, 10, 1, 4, 0, 0, 0, -1, -1, 0, 0, 3, 0, 0, 0, 0, 1, 0, 1, buf)
        px = bytes(buf)
        assert not any(px[:W * 3] + px[-W * 3:]), (h, m)
        assert all(not any(px[y * W:y * W + 3] + px[y * W + W - 3:(y + 1) * W]) for y in range(H)), (h, m)

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
