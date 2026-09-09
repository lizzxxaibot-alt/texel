"""Every error path and edge case the happy-path suites never reach.

Written to close the 37 uncovered lines found by `coverage`. These are the
branches that only fire on malformed input, full palettes, locked layers and
degenerate geometry - i.e. the ones that break in front of a customer.

  py -3 test_edges.py
"""
import sys

from core import adjust as A
from core import palette as P
from core import raster as R
from core import tools as T
from core import uvmap as U
from core.canvas import Canvas, Layer, MAX_COLOURS
from core.select import Clip, Selection

fails = []


def check(n, c, d=""):
    print(f"[{'ok  ' if c else 'FAIL'}] {n}" + ("" if c else f"  {d}"))
    if not c:
        fails.append(n)


# ------------------------------------------------------------------ canvas
c = Canvas(4, 4)
lay = c.layers[0]
idx = c.add_colour((1, 2, 3, 255))
lay.set(1, 1, idx)
lay.clear()
check("Layer.clear wipes every texel", lay.get(1, 1) == 0 and not any(lay.px))

full = Canvas(2, 2)
for i in range(MAX_COLOURS):
    full.add_colour((i % 256, (i * 7) % 256, (i * 13) % 256, 255))
try:
    full.add_colour((99, 98, 97, 96))
    check("palette refuses to overflow", False, len(full.palette))
except ValueError as e:
    check("palette refuses to overflow", "full" in str(e), str(e))

for bad in (0, -1, 999):
    try:
        c.replace_colour(bad, (1, 1, 1, 255))
        check(f"replace_colour rejects index {bad}", False)
    except IndexError:
        check(f"replace_colour rejects index {bad}", True)

check("duplicate_layer rejects a bad index", c.duplicate_layer(99) is None)
check("duplicate_layer rejects a negative index", c.duplicate_layer(-1) is None)

lk = Canvas(4, 4)
lk.add_layer("B")
lk.layers[0].locked = True
check("merge_indices refuses a locked target", lk.merge_indices([0, 1]) is False)
check("merge_down refuses a locked layer below", lk.merge_down(1) is False)
check("merge_indices rejects out-of-range indices", lk.merge_indices([5, 9]) is False)
check("move_layer rejects a bad destination", lk.move_layer(0, 99) is False)
check("remove_layer rejects a bad index", lk.remove_layer(99) is False)

# ------------------------------------------------------------------ raster
check("pixel_perfect passes through 0 points", R.pixel_perfect([]) == [])
check("pixel_perfect passes through 1 point", R.pixel_perfect([(1, 1)]) == [(1, 1)])
check("pixel_perfect passes through 2 points",
      R.pixel_perfect([(0, 0), (5, 5)]) == [(0, 0), (5, 5)])

check("ellipse rejects a negative radius", R.ellipse(5, 5, -1, 3) == [])
check("ellipse r=0 in one axis still draws", len(R.ellipse(5, 5, 4, 0)) > 0)
# region-2 branch: a tall, narrow ellipse spends most of its walk there
tall = R.ellipse(20, 20, 2, 14)
check("tall ellipse exercises the steep region", len(tall) > 20, len(tall))
check("tall ellipse spans its full height",
      min(y for _x, y in tall) == 6 and max(y for _x, y in tall) == 34)

# ellipse_box tip-finishing: a 1-texel-tall box is as flat as it gets
flat = R.ellipse_box(0, 0, 20, 1)
check("flat ellipse_box fills its width",
      min(x for x, _ in flat) == 0 and max(x for x, _ in flat) == 20)
thin = R.ellipse_box(0, 0, 20, 2)
check("2-tall ellipse_box fills its box",
      min(y for _, y in thin) == 0 and max(y for _, y in thin) == 2,
      (min(y for _, y in thin), max(y for _, y in thin)))
check("ellipse_box degenerate line box", len(R.ellipse_box(0, 0, 9, 0)) == 10)
# regression: narrow ellipses used to lose their tips (2x21 box drew rows 1..19)
for _b in ((0,0,1,20), (0,0,2,20), (0,0,1,3), (5,5,6,30), (0,0,20,1), (0,0,20,2), (3,3,4,4)):
    _e = R.ellipse_box(*_b)
    _xs = [x for x, _ in _e]; _ys = [y for _, y in _e]
    check(f"narrow ellipse_box {_b} fills its box",
          (min(_xs), max(_xs), min(_ys), max(_ys)) == (_b[0], _b[2], _b[1], _b[3]),
          (min(_xs), max(_xs), min(_ys), max(_ys)))
# every input value must still yield a spanning ramp (no dead guard needed)
for _v in (0, 36, 101, 128, 200, 255):
    _r = T.make_ramp((_v, _v, _v, 255), 5)
    check(f"ramp from grey {_v} gives 5 distinct steps",
          len({(a,b,c) for a,b,c,_d in _r}) == 5, _r)

# flood fill with tolerance
grid = [[(10, 10, 10, 255)] * 6 for _ in range(6)]
grid[0][3] = (14, 14, 14, 255)          # within tolerance 8
grid[0][4] = (200, 0, 0, 255)           # outside it
got = R.flood_fill(lambda x, y: grid[y][x], 6, 6, 0, 0, (0, 0, 255, 255), tolerance=8)
check("tolerance absorbs a near colour", (3, 0) in got, sorted(got)[:6])
check("tolerance still stops at a far colour", (4, 0) not in got)

# ----------------------------------------------------------------- palette
check("malformed 6-digit hex is dropped", P.parse_hex("zzzzzz") == [])
check("malformed 8-digit hex is dropped", P.parse_hex("zzzzzzzz") == [])
check("malformed 3-digit hex is dropped", P.parse_hex("zzz") == [])
check("odd-length hex is dropped", P.parse_hex("#ffff") == [])
name, cols = P.parse_gpl("GIMP Palette\nName: X\nnot a number here\n255 0 0\n")
check("gpl skips a non-numeric row", cols == [(255, 0, 0, 255)], cols)
check("gpl skips out-of-range channels",
      P.parse_gpl("GIMP Palette\n999 0 0\n1 2 3\n")[1] == [(1, 2, 3, 255)])
check("gpl with no Name still parses", P.parse_gpl("GIMP Palette\n1 2 3\n")[0] == "Palette")
n3, c3 = P.parse("ff0000\n00ff00", r"C:\stuff\my palette.hex")
check("parse() falls back to hex and names from the file", n3 == "my palette", n3)
check("parse() fallback keeps the colours", len(c3) == 2, c3)
check("parse() of an extensionless path still names something",
      P.parse("ff0000", "noext")[0] == "noext")
check("empty text parses to nothing", P.parse("", "x.hex")[1] == [])

# ---------------------------------------------------------------- selection
sl = Selection(16, 16)
sl.add_ellipse(8, 8, 5, 3)
check("add_ellipse selects an elliptical area", 0 < sl.count() < 256, sl.count())
check("add_ellipse is centred", (8, 8) in sl)

full_sel = Selection(4, 4, all_selected=True)
before = full_sel.count()
full_sel.grow(3)                          # already everything: must stop early
check("grow stops when nothing can be added", full_sel.count() == before, full_sel.count())
empty_sel = Selection(4, 4)
empty_sel.shrink(3)                       # already nothing: must stop early
check("shrink stops when nothing can be removed", empty_sel.is_empty())

# Clip skipping unselected texels inside the bounding box
cc = Canvas(8, 8)
red = cc.add_colour((255, 0, 0, 255))
for x in range(8):
    for y in range(8):
        cc.layers[0].set(x, y, red)
diag = Selection(8, 8)
diag.add_points([(0, 0), (3, 3)])         # bbox is 4x4 but only 2 texels selected
clip = Clip.from_layer(cc.layers[0], diag, cc.palette)
check("clip covers the selection bbox", (clip.w, clip.h) == (4, 4), (clip.w, clip.h))
check("clip skips texels outside the selection",
      sum(1 for v in clip.px if v) == 2, sum(1 for v in clip.px if v))

dst = Canvas(8, 8)
dst.layers[0].locked = True
check("paste into a locked layer writes nothing",
      clip.paste_into(dst, dst.layers[0], 0, 0) == 0)

# ------------------------------------------------------------------- tools
check("tile score on a 1x1 canvas is seamless", T.tile_seam_score(bytearray([1]), 1, 1)["seamless"])
# no palette -> index fallback, which the result flags as weaker
_np = T.tile_seam_score(bytearray([1, 2, 1, 2]), 2, 2)
check("works without a palette", _np["by_colour"] is False, _np)
check("index fallback still returns a score", 0 <= _np["score"] <= 100, _np["score"])
# transparent vs opaque across the wrap is a full-strength edge
_pal2 = [(0, 0, 0, 0), (200, 200, 200, 255)]
_tr = T.tile_seam_score(bytearray([1, 1, 1, 0]), 2, 2, _pal2)
check("transparent/opaque boundary is measured", _tr["h_wrap"] > 0 or _tr["v_wrap"] > 0, _tr)
check("tile score on a 1-wide canvas is seamless",
      T.tile_seam_score(bytearray([1, 2]), 1, 2)["seamless"])
ccw, _w, _h = T.rotate90(bytearray([1, 2, 3, 4]), 2, 2, clockwise=False)
check("counter-clockwise rotate", list(ccw) == [2, 4, 1, 3], list(ccw))
cw, _w, _h = T.rotate90(bytearray([1, 2, 3, 4]), 2, 2, clockwise=True)
check("cw and ccw are different", list(cw) != list(ccw))
white_ramp = T.make_ramp((255, 255, 255, 255), 5)
check("ramp from white hits the value ceiling and still spans",
      len({(r, g, b) for r, g, b, _a in white_ramp}) == 5, white_ramp)

# ------------------------------------------------------------------- uvmap
check("uv_scale_for_density guards zero area", U.uv_scale_for_density(32.0, 0.0, 64) == 1.0)
check("uv_scale_for_density guards zero texture", U.uv_scale_for_density(32.0, 1.0, 0) == 1.0)
check("uv_scale_for_density guards zero target", U.uv_scale_for_density(0.0, 1.0, 64) == 1.0)

# ----------------------------------------------------------------- adjust
sel2 = Selection(8, 8)
sel2.add_rect(0, 0, 1, 1)
used = A.indices_in(cc.layers[0], sel2)
check("indices_in honours the selection", used == {red}, used)
check("indices_in on an empty region returns nothing",
      A.indices_in(Layer("e", 4, 4)) == set())

print()
if fails:
    print(f"{len(fails)} FAILED: {fails}")
    sys.exit(1)
print("EDGE CASES: ALL PASS")
