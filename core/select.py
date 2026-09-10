"""Selection masks. A selection is a bytearray of 0/1, one byte per texel.

Every drawing op honours the mask when one is active. Kept as a flat bytearray
rather than a set of points: at 512x512 a set of tuples costs megabytes and
makes the per-texel test a hash lookup, while this is one index.
"""
from __future__ import annotations

from . import raster as R
from . import tools as T


class Selection:
    __slots__ = ("w", "h", "mask", "_count")

    def __init__(self, w: int, h: int, all_selected: bool = False):
        self.w, self.h = w, h
        self.mask = bytearray([1 if all_selected else 0]) * (w * h)
        self._count = w * h if all_selected else 0

    # ---- queries
    def __contains__(self, xy) -> bool:
        x, y = xy
        return 0 <= x < self.w and 0 <= y < self.h and bool(self.mask[y * self.w + x])

    def is_empty(self) -> bool:
        return self._count == 0

    def count(self) -> int:
        return self._count

    def bounds(self) -> tuple[int, int, int, int] | None:
        minx = miny = 1 << 30
        maxx = maxy = -1
        for y in range(self.h):
            row = self.mask[y * self.w:(y + 1) * self.w]
            if not any(row):
                continue
            miny = min(miny, y)
            maxy = max(maxy, y)
            for x, v in enumerate(row):
                if v:
                    if x < minx:
                        minx = x
                    if x > maxx:
                        maxx = x
        return None if maxx < 0 else (minx, miny, maxx, maxy)

    # ---- building
    def _recount(self) -> None:
        self._count = sum(self.mask)

    def clear(self) -> None:
        self.mask = bytearray(self.w * self.h)
        self._count = 0

    def select_all(self) -> None:
        self.mask = bytearray([1]) * (self.w * self.h)
        self._count = self.w * self.h

    def invert(self) -> None:
        self.mask = bytearray(1 - v for v in self.mask)
        self._count = self.w * self.h - self._count

    def add_points(self, pts) -> None:
        for x, y in pts:
            if 0 <= x < self.w and 0 <= y < self.h:
                self.mask[y * self.w + x] = 1
        self._recount()

    def remove_points(self, pts) -> None:
        for x, y in pts:
            if 0 <= x < self.w and 0 <= y < self.h:
                self.mask[y * self.w + x] = 0
        self._recount()

    def add_rect(self, x0: int, y0: int, x1: int, y1: int) -> None:
        self.add_points(R.rect(x0, y0, x1, y1, filled=True))

    def add_ellipse(self, cx: int, cy: int, rx: int, ry: int) -> None:
        self.add_points(R.ellipse(cx, cy, rx, ry, filled=True))

    def select_linked(self, layer, sx: int, sy: int, tolerance: int = 0) -> None:
        """Contiguous run of one index - the 'magic wand'."""
        get = lambda x, y: (layer.get(x, y),)
        pts = R.flood_fill(get, self.w, self.h, sx, sy, (-1,), tolerance, True)
        self.add_points(pts)

    def select_same_colour(self, layer, idx: int) -> None:
        """Every texel of one palette index, contiguous or not."""
        pts = [(x, y) for y in range(self.h) for x in range(self.w)
               if layer.get(x, y) == idx]
        self.add_points(pts)

    def grow(self, n: int = 1) -> None:
        """Dilate by n texels, 4-connected."""
        for _ in range(max(0, n)):
            add = []
            for y in range(self.h):
                for x in range(self.w):
                    if self.mask[y * self.w + x]:
                        continue
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.w and 0 <= ny < self.h and self.mask[ny * self.w + nx]:
                            add.append((x, y))
                            break
            if not add:
                break
            self.add_points(add)

    def shrink(self, n: int = 1) -> None:
        """Erode by n texels. Edge of canvas counts as outside."""
        for _ in range(max(0, n)):
            drop = []
            for y in range(self.h):
                for x in range(self.w):
                    if not self.mask[y * self.w + x]:
                        continue
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = x + dx, y + dy
                        if not (0 <= nx < self.w and 0 <= ny < self.h) or \
                           not self.mask[ny * self.w + nx]:
                            drop.append((x, y))
                            break
            if not drop:
                break
            self.remove_points(drop)

    def outline(self) -> list[tuple[int, int]]:
        """Texels on the selection border - what a marching-ants overlay draws."""
        out = []
        for y in range(self.h):
            for x in range(self.w):
                if not self.mask[y * self.w + x]:
                    continue
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if not (0 <= nx < self.w and 0 <= ny < self.h) or \
                       not self.mask[ny * self.w + nx]:
                        out.append((x, y))
                        break
        return out


class Clip:
    """Clipboard contents: an indexed patch plus the palette it came from.

    Carrying the palette matters - pasting into a document with a different
    palette must not silently remap colours to whatever index happens to match.
    """
    __slots__ = ("w", "h", "px", "palette")

    def __init__(self, w: int, h: int, px: bytearray, palette: list):
        self.w, self.h, self.px, self.palette = w, h, px, list(palette)

    @classmethod
    def from_layer(cls, layer, sel: "Selection | None", palette) -> "Clip | None":
        """Copy the selected region, or the layer's tight bounds if unselected."""
        box = sel.bounds() if (sel and not sel.is_empty()) else layer.bounds()
        if box is None:
            return None
        x0, y0, x1, y1 = box
        w, h = x1 - x0 + 1, y1 - y0 + 1
        px = bytearray(w * h)
        for y in range(h):
            for x in range(w):
                sx, sy = x0 + x, y0 + y
                if sel and not sel.is_empty() and (sx, sy) not in sel:
                    continue
                px[y * w + x] = layer.get(sx, sy)
        return cls(w, h, px, palette)

    def paste_into(self, canvas, layer, ox: int, oy: int, transparent_skips=True) -> int:
        """Paste at (ox, oy), remapping colours through the target palette."""
        remap = {0: 0}
        for i, rgba in enumerate(self.palette):
            if i == 0:
                continue
            remap[i] = canvas.add_colour(rgba)
        n = 0
        for y in range(self.h):
            for x in range(self.w):
                v = self.px[y * self.w + x]
                if v == 0 and transparent_skips:
                    continue
                if layer.set(ox + x, oy + y, remap.get(v, 0)):
                    n += 1
        return n


TRANSFORMS = ("FLIP_H", "FLIP_V", "ROT_CW", "ROT_CCW", "SCALE")


def transform_region(layer, sel: "Selection | None", mode: str,
                     factor: float = 1.0) -> tuple[int, int, int] | None:
    """Flip, rotate or scale the selected region in place. Returns (n, w, h).

    Two decisions worth stating, because both are visible to the user:

    **The result is centred on the box it replaced.** Anchoring at the box's
    corner instead makes a rotated sprite walk across the canvas every time you
    press the button, and a scale-down leave the art pinned to one corner of the
    hole it came from.

    **The mask is transformed too**, not reset to the new bounding box. A magic
    wand selection that survives a flip as a rectangle is not the same selection,
    and the next operation would spill outside the shape.

    Nothing is written where the transformed patch is transparent, so rotating a
    round selection does not blank the square of canvas around it - the source
    texels are cleared first, which is the only erasing this does.
    """
    box = sel.bounds() if (sel and not sel.is_empty()) else layer.bounds()
    if box is None:
        return None
    x0, y0, x1, y1 = box
    w, h = x1 - x0 + 1, y1 - y0 + 1
    masked = bool(sel and not sel.is_empty())

    px = bytearray(w * h)
    mask = bytearray(w * h)
    for y in range(h):
        for x in range(w):
            sx, sy = x0 + x, y0 + y
            if masked and (sx, sy) not in sel:
                continue
            mask[y * w + x] = 1
            px[y * w + x] = layer.get(sx, sy)

    if mode == "FLIP_H":
        px, mask, nw, nh = T.flip(px, w, h, True), T.flip(mask, w, h, True), w, h
    elif mode == "FLIP_V":
        px, mask, nw, nh = T.flip(px, w, h, False), T.flip(mask, w, h, False), w, h
    elif mode in ("ROT_CW", "ROT_CCW"):
        cw = mode == "ROT_CW"
        px, nw, nh = T.rotate90(px, w, h, cw)
        mask, _nw, _nh = T.rotate90(mask, w, h, cw)
    elif mode == "SCALE":
        nw, nh = max(1, round(w * factor)), max(1, round(h * factor))
        px = T.scale_nearest(px, w, h, nw, nh)
        mask = T.scale_nearest(mask, w, h, nw, nh)
    else:
        raise ValueError(f"unknown transform {mode!r}")

    for y in range(h):
        for x in range(w):
            sx, sy = x0 + x, y0 + y
            if masked and (sx, sy) not in sel:
                continue
            layer.set(sx, sy, 0)

    ox, oy = x0 + (w - nw) // 2, y0 + (h - nh) // 2
    n = 0
    pts = []
    for y in range(nh):
        for x in range(nw):
            if not mask[y * nw + x]:
                continue
            pts.append((ox + x, oy + y))
            v = px[y * nw + x]
            if v and layer.set(ox + x, oy + y, v):
                n += 1
    if sel is not None:
        sel.clear()
        sel.add_points(pts)
    return n, nw, nh
