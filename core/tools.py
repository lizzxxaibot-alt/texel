"""Pixel-art operations that go past the reference feature set.

The tileability check is the one worth pointing at: a texture painted on a 3D
model is nearly always meant to tile, and nothing in the reference tells you
whether yours does. Here it is a measurement, not an eyeball.
"""
from __future__ import annotations

import colorsys

RGBA = tuple[int, int, int, int]


def outline_points(layer, diagonal: bool = False) -> list[tuple[int, int]]:
    """Transparent texels that touch an opaque one - a sprite outline ring."""
    offs = ((1, 0), (-1, 0), (0, 1), (0, -1))
    if diagonal:
        offs = offs + ((1, 1), (1, -1), (-1, 1), (-1, -1))
    out = []
    for y in range(layer.h):
        for x in range(layer.w):
            if layer.get(x, y):
                continue
            for dx, dy in offs:
                if layer.get(x + dx, y + dy):
                    out.append((x, y))
                    break
    return out


def shift_wrap(px: bytearray, w: int, h: int, dx: int, dy: int) -> bytearray:
    """Offset with wraparound. Shifting by half is how you find a tiling seam."""
    out = bytearray(w * h)
    dx %= w
    dy %= h
    for y in range(h):
        ny = (y + dy) % h
        row = px[y * w:(y + 1) * w]
        out[ny * w:(ny + 1) * w] = row[-dx:] + row[:-dx] if dx else row
    return out


def tile_seam_score(px: bytearray, w: int, h: int, palette=None) -> dict:
    """Is the wrap boundary more abrupt than the texture's own internal edges?

    HONEST SCOPE: a heuristic, not a proof. Whether a seam "reads" is perceptual.
    What this reliably catches is the common failure - an edge that changes far
    harder than anything inside the texture.

    Three rejected approaches, recorded so they are not retried:
      * "left column == right column" - a seamless tile does not need identical
        edges, and a duplicated edge column would pass while showing a doubled line.
      * "wrap difference vs MEAN interior difference" - regular stripes change at
        every stripe boundary, so mean and wrap are both high, yet they tile fine.
      * "COUNT of differing texels vs worst interior" - blind to magnitude. A
        non-wrapping gradient jumps 7->1 at the wrap; the same NUMBER of texels
        change as at any interior step, but the colour distance is six times
        larger. Counting cannot see that.

    So we measure mean COLOUR distance across the boundary and compare it to the
    harshest interior transition. Pass `palette` for that; without it we fall back
    to index distance, which is weaker and says so in the result.
    """
    if w < 2 or h < 2:
        return {"score": 100.0, "seamless": True, "h_wrap": 0.0, "h_worst": 0.0,
                "v_wrap": 0.0, "v_worst": 0.0, "by_colour": palette is not None}

    if palette:
        def dist(i, j):
            if i == j:
                return 0.0
            a = palette[i] if i < len(palette) else (0, 0, 0, 0)
            b = palette[j] if j < len(palette) else (0, 0, 0, 0)
            if a[3] == 0 or b[3] == 0:          # transparent vs opaque is a full edge
                return 0.0 if a[3] == b[3] else 255.0
            return max(abs(a[0] - b[0]), abs(a[1] - b[1]), abs(a[2] - b[2]))
    else:
        def dist(i, j):
            return 0.0 if i == j else 255.0

    col = lambda x: [px[y * w + x] for y in range(h)]
    row = lambda y: list(px[y * w:(y + 1) * w])

    def edge(a, b):
        return sum(dist(p, q) for p, q in zip(a, b)) / len(a)

    h_wrap = edge(col(w - 1), col(0))
    h_worst = max((edge(col(x), col(x + 1)) for x in range(w - 1)), default=0.0)
    v_wrap = edge(row(h - 1), row(0))
    v_worst = max((edge(row(y), row(y + 1)) for y in range(h - 1)), default=0.0)

    # 10% slack: a wrap marginally harsher than the interior is not a seam
    eh = max(0.0, h_wrap - h_worst * 1.1) / 255.0
    ev = max(0.0, v_wrap - v_worst * 1.1) / 255.0
    return {"score": round(100.0 * (1.0 - max(eh, ev)), 1),
            "seamless": max(eh, ev) < 0.01,
            "h_wrap": round(h_wrap, 1), "h_worst": round(h_worst, 1),
            "v_wrap": round(v_wrap, 1), "v_worst": round(v_worst, 1),
            "by_colour": palette is not None}


def flip(px: bytearray, w: int, h: int, horizontal: bool = True) -> bytearray:
    out = bytearray(w * h)
    for y in range(h):
        row = px[y * w:(y + 1) * w]
        if horizontal:
            row = row[::-1]
        ty = y if horizontal else h - 1 - y
        out[ty * w:(ty + 1) * w] = row
    return out


def rotate90(px: bytearray, w: int, h: int, clockwise: bool = True):
    """Returns (new_px, new_w, new_h). Square canvases keep their size."""
    out = bytearray(w * h)
    nw, nh = h, w
    for y in range(h):
        for x in range(w):
            v = px[y * w + x]
            if clockwise:
                nx, ny = h - 1 - y, x
            else:
                nx, ny = y, w - 1 - x
            out[ny * nw + nx] = v
    return out, nw, nh


def make_ramp(base: RGBA, steps: int = 5, hue_shift: float = -12.0,
              sat_boost: float = 0.18) -> list[RGBA]:
    """Build a shading ramp from one colour.

    Naive ramps just darken toward black, which looks muddy. Real pixel artists
    shift hue toward blue in shadow and toward yellow in light, and push
    saturation in the midtones. That is what this does.
    """
    steps = max(2, min(16, steps))
    r, g, b, a = base
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)

    # Guarantee a real value span. Scaling v directly collapses the ramp for
    # black (v=0 -> every step identical) and clips it for white. Instead pick
    # explicit endpoints around v with a minimum spread, so a ramp from ANY
    # input colour is still a ramp.
    MIN_SPAN = 0.42
    hi = min(1.0, max(v * 1.25, 0.05 + MIN_SPAN))
    lo = max(0.05, min(v * 0.40, hi - MIN_SPAN))   # derive lo FROM hi, so the
    #                                                span is >= MIN_SPAN by
    #                                                construction and needs no
    #                                                after-the-fact correction

    out: list[RGBA] = []
    for i in range(steps):
        t = i / (steps - 1)                 # 0 = darkest, 1 = lightest
        nv = lo + (hi - lo) * t
        curve = 1.0 - abs(t - 0.5) * 2.0    # peak saturation in the midtones
        ns = max(0.0, min(1.0, s * (1.0 + sat_boost * curve)))
        nh = (h + (hue_shift / 360.0) * (0.5 - t) * 2.0) % 1.0
        nr, ng, nb = colorsys.hsv_to_rgb(nh, ns, nv)
        out.append((round(nr * 255), round(ng * 255), round(nb * 255), a))
    return out
