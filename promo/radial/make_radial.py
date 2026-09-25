"""Build the radial-symmetry panels using the SHIPPED Texel code, not a mock.

Every texel in the output comes from texel/core/raster.py inside the live
0.2.1 zip: line() + pixel_perfect() rasterise the stroke, brush_mask() stamps
it, symmetry_points() does the repeats. PIL only writes the resulting texel
list out as pixels; nothing here is drawn with a PIL primitive.
"""
import sys, json, os
sys.path.insert(0, r"C:\Users\opule\AppData\Local\Temp\claude\z021\texel")
import core.raster as R
from PIL import Image

W = H = 64
SCALE = 9                     # nearest-neighbour, whole number, no resampling
OUT = r"C:\Users\opule\AppData\Local\Temp\claude\radial"

BG    = (22, 24, 30, 255)
GRID  = (33, 36, 44, 255)
INK   = (244, 233, 205, 255)   # the one authored stroke
ECHO  = (126, 200, 227, 255)   # its repeats

# A hand-authored drag path: the kind of flick you make drawing one petal.
# Nine anchor points in canvas space, nothing procedural about them.
PATH = [(32, 30), (35, 26), (38, 21), (40, 16), (40, 11),
        (38, 7), (35, 5), (33, 6), (32, 9)]

def stroke_texels(path, brush=2):
    pts = []
    for (x0, y0), (x1, y1) in zip(path, path[1:]):
        pts.extend(R.line(x0, y0, x1, y1))
    pts = R.pixel_perfect(pts)
    mask = R.brush_mask(brush, "SQUARE")
    out, seen = [], set()
    for x, y in pts:
        for mx, my in mask:
            p = (x + mx, y + my)
            if p in seen or not (0 <= p[0] < W and 0 <= p[1] < H):
                continue
            seen.add(p); out.append(p)
    return out

def render(base, full, name):
    img = Image.new("RGBA", (W, H), BG)
    px = img.load()
    for y in range(H):                      # canvas centre guides, 1px
        px[W // 2, y] = GRID
        px[y, H // 2] = GRID
    baseset = set(base)
    for x, y in full:
        px[x, y] = INK if (x, y) in baseset else ECHO
    big = img.resize((W * SCALE, H * SCALE), Image.NEAREST)
    path = os.path.join(OUT, name)
    big.save(path)
    return path

base = stroke_texels(PATH)
panels = {}
for name, kw in (("p1_stroke",  dict(segments=1)),
                 ("p2_radial8", dict(segments=8)),
                 ("p3_r8_mx",   dict(segments=8, mirror_x=True)),
                 ("p4_r16",     dict(segments=16))):
    full = R.symmetry_points(base, W, H, **kw)
    panels[name] = dict(count=len(full), path=render(base, full, name + ".png"), **kw)

panels["_base"] = dict(count=len(base))
print(json.dumps(panels, indent=2))
