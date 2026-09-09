"""Colour adjustments.

On an indexed canvas an adjustment is a PALETTE operation, not a pixel one:
change the 12 palette entries and all 260,000 texels change with them. That is
the whole point of indexed, and it is why these are instant at any canvas size.

Hue/saturation go through HSV; brightness/contrast are linear in 0-255 space,
which is what a pixel artist expects (a perceptual curve would smear ramps).
"""
from __future__ import annotations

import colorsys

RGBA = tuple[int, int, int, int]


def _clamp(v: float) -> int:
    return max(0, min(255, round(v)))


def brightness(rgba: RGBA, amount: float) -> RGBA:
    """amount in -1..1. -1 is black, +1 is white."""
    r, g, b, a = rgba
    if amount >= 0:
        k = amount
        return (_clamp(r + (255 - r) * k), _clamp(g + (255 - g) * k),
                _clamp(b + (255 - b) * k), a)
    k = 1.0 + amount
    return (_clamp(r * k), _clamp(g * k), _clamp(b * k), a)


def contrast(rgba: RGBA, amount: float) -> RGBA:
    """amount in -1..1, pivoting on mid grey."""
    r, g, b, a = rgba
    k = 1.0 + amount
    return (_clamp((r - 128) * k + 128), _clamp((g - 128) * k + 128),
            _clamp((b - 128) * k + 128), a)


def hue_shift(rgba: RGBA, degrees: float) -> RGBA:
    r, g, b, a = rgba
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    h = (h + degrees / 360.0) % 1.0
    nr, ng, nb = colorsys.hsv_to_rgb(h, s, v)
    return (_clamp(nr * 255), _clamp(ng * 255), _clamp(nb * 255), a)


def saturation(rgba: RGBA, amount: float) -> RGBA:
    """amount in -1..1. -1 is greyscale, +1 is fully saturated."""
    r, g, b, a = rgba
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    s = max(0.0, min(1.0, s * (1.0 + amount) if amount >= 0 else s * (1.0 + amount)))
    nr, ng, nb = colorsys.hsv_to_rgb(h, s, v)
    return (_clamp(nr * 255), _clamp(ng * 255), _clamp(nb * 255), a)


def posterize(rgba: RGBA, levels: int) -> RGBA:
    """Quantise each channel to `levels` steps. 2-8 is the useful range."""
    levels = max(2, min(255, int(levels)))
    step = 255.0 / (levels - 1)
    r, g, b, a = rgba
    return (_clamp(round(r / step) * step), _clamp(round(g / step) * step),
            _clamp(round(b / step) * step), a)


def greyscale(rgba: RGBA) -> RGBA:
    """Rec. 709 luma - the weighting that matches how the eye reads brightness."""
    r, g, b, a = rgba
    y = _clamp(0.2126 * r + 0.7152 * g + 0.0722 * b)
    return (y, y, y, a)


def invert(rgba: RGBA) -> RGBA:
    r, g, b, a = rgba
    return (255 - r, 255 - g, 255 - b, a)


OPS = {
    "BRIGHTNESS": (brightness, True),
    "CONTRAST": (contrast, True),
    "HUE": (hue_shift, True),
    "SATURATION": (saturation, True),
    "POSTERIZE": (posterize, True),
    "GREYSCALE": (greyscale, False),
    "INVERT": (invert, False),
}


def apply_to_palette(palette: list[RGBA], op: str, amount: float = 0.0,
                     only: set[int] | None = None) -> list[RGBA]:
    """Return a new palette with `op` applied. Index 0 (transparent) never moves.

    `only` restricts the change to those indices, which is how an adjustment
    scoped to a selection works: we collect the indices the selection uses and
    pass them in.
    """
    fn, takes_amount = OPS.get(op, (None, False))
    if fn is None:
        raise ValueError(f"unknown adjustment: {op}")
    out = list(palette)
    for i, rgba in enumerate(palette):
        if i == 0:
            continue                      # transparent stays transparent
        if only is not None and i not in only:
            continue
        out[i] = fn(rgba, amount) if takes_amount else fn(rgba)
    return out


def indices_in(layer, sel=None) -> set[int]:
    """Which palette indices a layer (optionally within a selection) actually uses."""
    used: set[int] = set()
    for y in range(layer.h):
        for x in range(layer.w):
            if sel is not None and not sel.is_empty() and (x, y) not in sel:
                continue
            v = layer.get(x, y)
            if v:
                used.add(v)
    return used
