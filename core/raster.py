"""Pixel rasterisation primitives.

Written from first principles (Bresenham 1965, midpoint ellipse, scanline fill).
Pure Python, no bpy, no numpy - so it runs in Blender, in tests, and anywhere else.

The one non-textbook piece is `pixel_perfect`: a plain Bresenham diagonal leaves
L-shaped corner pairs, which read as fat joints at 1px. Pixel artists remove the
corner pixel by hand. We do it in code.
"""
from __future__ import annotations

Point = tuple[int, int]


def line(x0: int, y0: int, x1: int, y1: int) -> list[Point]:
    """Bresenham line, endpoints inclusive."""
    pts: list[Point] = []
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        pts.append((x0, y0))
        if x0 == x1 and y0 == y1:
            return pts
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def pixel_perfect(pts: list[Point]) -> list[Point]:
    """Drop corner pixels from a freehand stroke.

    NOTE: this is for MOUSE-TRACED input, not for `line()` output. Our Bresenham
    steps diagonally already, so it emits no L-corners - verified in the tests.
    Freehand drags do emit them: the cursor is sampled per event, so a shallow
    drag lands as a staircase and the joints read fat at 1px.

    A pixel is a corner when the pixel before and the pixel after are each
    orthogonally adjacent to it but diagonal to each other - i.e. the three form
    an L. Removing the middle leaves a clean 1px diagonal, which is what a pixel
    artist would draw. Endpoints are never removed.
    """
    if len(pts) < 3:
        return list(pts)
    out: list[Point] = [pts[0]]
    i = 1
    while i < len(pts) - 1:
        px, py = out[-1]
        cx, cy = pts[i]
        nx, ny = pts[i + 1]
        prev_orth = (abs(cx - px) + abs(cy - py)) == 1
        next_orth = (abs(nx - cx) + abs(ny - cy)) == 1
        turns = (nx - cx) != (cx - px) and (ny - cy) != (cy - py)
        if prev_orth and next_orth and turns:
            i += 1          # skip the corner
            continue
        out.append((cx, cy))
        i += 1
    out.append(pts[-1])
    return out


def rect(x0: int, y0: int, x1: int, y1: int, filled: bool = False) -> list[Point]:
    lo_x, hi_x = (x0, x1) if x0 <= x1 else (x1, x0)
    lo_y, hi_y = (y0, y1) if y0 <= y1 else (y1, y0)
    if filled:
        return [(x, y) for y in range(lo_y, hi_y + 1) for x in range(lo_x, hi_x + 1)]
    pts = set()
    for x in range(lo_x, hi_x + 1):
        pts.add((x, lo_y)); pts.add((x, hi_y))
    for y in range(lo_y, hi_y + 1):
        pts.add((lo_x, y)); pts.add((hi_x, y))
    return sorted(pts)


def ellipse(cx: int, cy: int, rx: int, ry: int, filled: bool = False) -> list[Point]:
    """Midpoint ellipse from a centre and radii. Symmetric in all four quadrants.

    WARNING: this always spans an ODD 2r+1 texels per axis, because a centre
    texel exists. Do NOT reach it by converting a bounding box with
    `rx = (x1-x0)//2` - that loses a texel whenever the box is even, so a
    24-wide drag draws 23. For anything defined by two corners (every drag tool)
    use `ellipse_box`, which fills the box exactly at either parity.
    """
    if rx < 0 or ry < 0:
        return []
    if rx == 0 and ry == 0:
        return [(cx, cy)]
    pts: set[Point] = set()

    def plot(x: int, y: int) -> None:
        if filled:
            for xx in range(cx - x, cx + x + 1):
                pts.add((xx, cy + y)); pts.add((xx, cy - y))
        else:
            pts.add((cx + x, cy + y)); pts.add((cx - x, cy + y))
            pts.add((cx + x, cy - y)); pts.add((cx - x, cy - y))

    x, y = 0, ry
    rx2, ry2 = rx * rx, ry * ry
    # region 1: slope > -1
    d = ry2 - rx2 * ry + rx2 // 4
    dx, dy = 0, 2 * rx2 * y
    while dx < dy:
        plot(x, y)
        x += 1
        dx += 2 * ry2
        if d < 0:
            d += ry2 + dx
        else:
            y -= 1
            dy -= 2 * rx2
            d += ry2 + dx - dy
    # region 2: slope < -1
    d = int(ry2 * (x + 0.5) ** 2 + rx2 * (y - 1) ** 2 - rx2 * ry2)
    while y >= 0:
        plot(x, y)
        y -= 1
        dy -= 2 * rx2
        if d > 0:
            d += rx2 - dy
        else:
            x += 1
            dx += 2 * ry2
            d += rx2 - dy + dx
    return sorted(pts)


def ellipse_box(x0: int, y0: int, x1: int, y1: int, filled: bool = False) -> list[Point]:
    """Ellipse that exactly fills the bounding box, at any parity.

    Integer midpoint ellipse over a rectangle (the Bresenham/Zingl formulation).
    Two reasons it is done this way rather than centre+radius with floats:

    1. Parity. An even-width box has no single centre column, so `rx=(x1-x0)//2`
       loses a texel and a 24-wide drag draws 23. Stepping the box edges inward
       from both sides handles even and odd identically.
    2. Smoothness. Rounding each row independently gives step sizes that jump
       around (3,1,2,0,...) and the shoulder visibly wobbles. Carrying one
       integer error term makes the steps monotonically ease (2,2,1,1,...),
       which is what a hand-drawn pixel ellipse looks like.
    """
    if x1 < x0:
        x0, x1 = x1, x0
    if y1 < y0:
        y0, y1 = y1, y0

    a = x1 - x0
    b = y1 - y0
    if a <= 0 or b <= 0:                       # a line or a dot
        return rect(x0, y0, x1, y1, filled=True)

    b1 = b & 1                                 # 1 when the box height is even
    dx = 4 * (1 - a) * b * b
    dy = 4 * (b1 + 1) * a * a
    err = dx + dy + b1 * a * a

    lo, hi = x0, x1
    ty = y0 + (b + 1) // 2                     # top edge of the two centre rows
    by = ty - b1                               # bottom edge (same row when odd)
    aa = 8 * a * a
    bb = 8 * b * b

    pts: set[Point] = set()
    while lo <= hi:
        pts.add((hi, ty)); pts.add((lo, ty))
        pts.add((lo, by)); pts.add((hi, by))
        e2 = 2 * err
        if e2 <= dy:
            ty += 1
            by -= 1
            dy += aa
            err += dy
        if e2 >= dx or 2 * err > dy:
            lo += 1
            hi -= 1
            dx += bb
            err += dx
    # Finish the tips of narrow ellipses (a <= 2), where the main loop stops
    # before reaching the box edges. The bound is <= b, not < b: with < b the
    # final iteration is skipped and a 2x21 box draws rows 1..19 instead of 0..20.
    while ty - by <= b:
        pts.add((lo - 1, ty)); pts.add((hi + 1, ty))
        pts.add((lo - 1, by)); pts.add((hi + 1, by))
        ty += 1
        by -= 1

    if not filled:
        return sorted(pts)

    spans: dict[int, list[int]] = {}
    for x, y in pts:
        r = spans.setdefault(y, [x, x])
        if x < r[0]:
            r[0] = x
        if x > r[1]:
            r[1] = x
    out: set[Point] = set()
    for y, (a0, a1) in spans.items():
        for x in range(a0, a1 + 1):
            out.add((x, y))
    return sorted(out)


def brush_mask(size: int, shape: str = "SQUARE") -> list[Point]:
    """Offsets a brush stamps, relative to the cursor texel.

    Square is the honest default at 1px and stays useful for hard edges. Round
    is what you want above about 3 texels - a square brush that size leaves
    visibly boxy corners on a curve. Diamond is the 45-degree cousin, handy for
    isometric work where every edge runs on the diagonal.
    """
    size = max(1, int(size))
    if size == 1:
        return [(0, 0)]
    half = size // 2
    lo, hi = -half, -half + size - 1
    pts: list[Point] = []
    r = (size - 1) / 2.0
    c = lo + r
    for y in range(lo, hi + 1):
        for x in range(lo, hi + 1):
            if shape == "ROUND":
                # +0.25 so an odd-sized round brush keeps its corners square-ish
                # instead of losing a texel off each cardinal point
                if (x - c) ** 2 + (y - c) ** 2 > (r + 0.25) ** 2:
                    continue
            elif shape == "DIAMOND":
                if abs(x - c) + abs(y - c) > r + 0.25:
                    continue
            pts.append((x, y))
    return pts


def flood_fill(get_px, w: int, h: int, sx: int, sy: int, target, tolerance: int = 0,
               contiguous: bool = True) -> list[Point]:
    """Scanline flood fill. `get_px(x, y)` returns an RGBA tuple of 0-255 ints.

    Iterative, not recursive - a 4096x4096 canvas would blow the Python stack.
    """
    if not (0 <= sx < w and 0 <= sy < h):
        return []
    seed = get_px(sx, sy)

    def match(c) -> bool:
        if tolerance == 0:
            return c == seed
        return all(abs(a - b) <= tolerance for a, b in zip(c, seed))

    if match(target) and tolerance == 0:
        return []                       # already that colour: nothing to do

    if not contiguous:                  # global replace, ignores connectivity
        return [(x, y) for y in range(h) for x in range(w) if match(get_px(x, y))]

    seen = bytearray(w * h)
    out: list[Point] = []
    stack = [(sx, sy)]
    while stack:
        x, y = stack.pop()
        if seen[y * w + x] or not match(get_px(x, y)):
            continue
        x0 = x
        while x0 > 0 and not seen[y * w + x0 - 1] and match(get_px(x0 - 1, y)):
            x0 -= 1
        x1 = x
        while x1 < w - 1 and not seen[y * w + x1 + 1] and match(get_px(x1 + 1, y)):
            x1 += 1
        for xx in range(x0, x1 + 1):
            seen[y * w + xx] = 1
            out.append((xx, y))
            for ny in (y - 1, y + 1):
                if 0 <= ny < h and not seen[ny * w + xx] and match(get_px(xx, ny)):
                    stack.append((xx, ny))
    return out
