"""Radial card panels, round 2: 1x output for integer CSS scaling.

Same stroke and same calls as make_radial.py, but core.raster is imported
straight out of the SHIPPED zip (zipimport), so the panels are the live
product's output, not a working-tree copy. Panels are written at 64x64, 1x;
the card scales them by a whole number with image-rendering:pixelated.
Asserts the counts the card prints, so the card cannot drift from the code.
"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
ZIP = os.path.join(HERE, "..", "..", "dist", "shipped", "texel-0.2.2-SHIPPED-2026-09-30.zip")
sys.path.insert(0, os.path.join(os.path.abspath(ZIP), "texel"))
import core.raster as R
from PIL import Image

W = H = 64
BG, GRID = (13, 12, 16, 255), (66, 64, 74, 255)
INK, ECHO = (242, 230, 200, 255), (126, 200, 227, 255)
PATH = [(32, 30), (35, 26), (38, 21), (40, 16), (40, 11),
        (38, 7), (35, 5), (33, 6), (32, 9)]

def stroke_texels(path, brush=2):
    pts = []
    for (x0, y0), (x1, y1) in zip(path, path[1:]):
        pts.extend(R.line(x0, y0, x1, y1))
    pts = R.pixel_perfect(pts)
    out, seen = [], set()
    for x, y in pts:
        for mx, my in R.brush_mask(brush, "SQUARE"):
            p = (x + mx, y + my)
            if p in seen or not (0 <= p[0] < W and 0 <= p[1] < H):
                continue
            seen.add(p); out.append(p)
    return out

base = stroke_texels(PATH)
counts = {}
for name, kw in (("r2_p1", dict(segments=1)), ("r2_p2", dict(segments=8)),
                 ("r2_p3", dict(segments=8, mirror_x=True))):
    full = R.symmetry_points(base, W, H, **kw)
    img = Image.new("RGBA", (W, H), BG); px = img.load()
    for i in range(W):
        px[W // 2, i] = GRID; px[i, H // 2] = GRID
    for x, y in full:            # echoes first, the authored stroke last
        px[x, y] = ECHO
    for x, y in base:
        px[x, y] = INK
    img.save(os.path.join(HERE, name + ".png"))
    counts[name] = len(full)
assert len(base) == 80 and counts == {"r2_p1": 80, "r2_p2": 576, "r2_p3": 984}, counts
print(json.dumps(counts))
