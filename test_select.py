"""Selection, clipboard, adjustments and layer groups.  py -3 test_select.py"""
import sys

from core.canvas import Canvas, Layer
from core.select import Clip, Selection
from core import adjust as A

fails = []


def check(n, c, d=""):
    print(f"[{'ok  ' if c else 'FAIL'}] {n}" + ("" if c else f"  {d}"))
    if not c:
        fails.append(n)


# ------------------------------------------------------------------ selection
s = Selection(8, 8)
check("starts empty", s.is_empty() and s.count() == 0)
check("empty has no bounds", s.bounds() is None)

s.add_rect(2, 2, 4, 5)
check("rect selects w*h texels", s.count() == 3 * 4, s.count())
check("membership works", (3, 3) in s and (0, 0) not in s)
check("bounds are tight", s.bounds() == (2, 2, 4, 5), s.bounds())
check("out-of-range membership is False", (99, 0) not in s)

s.invert()
check("invert flips the count", s.count() == 64 - 12, s.count())
check("invert flips membership", (0, 0) in s and (3, 3) not in s)

s.select_all()
check("select_all takes everything", s.count() == 64)
s.clear()
check("clear empties it", s.is_empty())

# grow / shrink
s.add_rect(3, 3, 4, 4)
before = s.count()
s.grow(1)
check("grow adds a 4-connected ring", s.count() == before + 8, f"{before} -> {s.count()}")
s.shrink(1)
check("shrink undoes grow", s.count() == before, s.count())
s.clear()
s.add_rect(0, 0, 0, 0)
s.shrink(1)
check("shrink can empty a selection", s.is_empty())

# magic wand on a real layer
c = Canvas(8, 8)
red = c.add_colour((255, 0, 0, 255))
blue = c.add_colour((0, 0, 255, 255))
L = c.layers[0]
for x in range(4):
    for y in range(8):
        L.set(x, y, red)
for x in range(4, 8):
    for y in range(8):
        L.set(x, y, blue)
s2 = Selection(8, 8)
s2.select_linked(L, 0, 0)
check("select_linked grabs the connected run", s2.count() == 32, s2.count())
check("select_linked stops at the colour boundary", (4, 0) not in s2)
s3 = Selection(8, 8)
s3.select_same_colour(L, blue)
check("select_same_colour grabs every match", s3.count() == 32, s3.count())
check("outline is the border only", 0 < len(s2.outline()) < s2.count(), len(s2.outline()))

# ------------------------------------------------------------------ clipboard
sel = Selection(8, 8)
sel.add_rect(0, 0, 1, 1)
clip = Clip.from_layer(L, sel, c.palette)
check("clip takes the selection size", (clip.w, clip.h) == (2, 2), (clip.w, clip.h))
check("clip carries the palette", clip.palette == c.palette)

c2 = Canvas(8, 8)                       # different document, empty palette
n = clip.paste_into(c2, c2.layers[0], 5, 5)
check("paste writes the texels", n == 4, n)
check("paste remaps into the target palette",
      c2.palette[c2.layers[0].get(5, 5)] == (255, 0, 0, 255),
      c2.palette[c2.layers[0].get(5, 5)])
check("paste did not corrupt index 0", c2.palette[0] == (0, 0, 0, 0))
check("paste is offset correctly", c2.layers[0].get(4, 4) == 0)

empty = Clip.from_layer(Layer("e", 4, 4), None, c.palette)
check("clip of an empty layer is None", empty is None)

# ----------------------------------------------------------------- adjustments
pal = [(0, 0, 0, 0), (100, 150, 200, 255)]
br = A.apply_to_palette(pal, "BRIGHTNESS", 0.5)
check("brightness lightens", br[1][0] > 100 and br[1][2] > 200, br[1])
check("brightness never moves index 0", br[0] == (0, 0, 0, 0))
dk = A.apply_to_palette(pal, "BRIGHTNESS", -0.5)
check("negative brightness darkens", dk[1][0] < 100, dk[1])
check("brightness +1 is white", A.apply_to_palette(pal, "BRIGHTNESS", 1.0)[1][:3] == (255, 255, 255))
check("brightness -1 is black", A.apply_to_palette(pal, "BRIGHTNESS", -1.0)[1][:3] == (0, 0, 0))

inv = A.apply_to_palette(pal, "INVERT")
check("invert flips channels", inv[1][:3] == (155, 105, 55), inv[1])
grey = A.apply_to_palette(pal, "GREYSCALE")
check("greyscale is neutral", grey[1][0] == grey[1][1] == grey[1][2], grey[1])
check("greyscale uses luma weighting, not a naive mean",
      grey[1][0] != round((100 + 150 + 200) / 3), grey[1][0])

hue = A.apply_to_palette(pal, "HUE", 180)
check("hue shift changes the colour", hue[1][:3] != (100, 150, 200), hue[1])
check("hue shift 360 is a no-op",
      A.apply_to_palette(pal, "HUE", 360)[1][:3] == (100, 150, 200))
check("alpha survives every op", all(
    A.apply_to_palette(pal, op, 0.3)[1][3] == 255 for op in A.OPS))

post = A.apply_to_palette(pal, "POSTERIZE", 2)
check("posterize snaps to endpoints", set(post[1][:3]) <= {0, 255}, post[1])

only = A.apply_to_palette([(0, 0, 0, 0), (10, 10, 10, 255), (20, 20, 20, 255)],
                          "INVERT", only={1})
check("scoped adjustment leaves other indices alone",
      only[1][:3] == (245, 245, 245) and only[2][:3] == (20, 20, 20), only)

used = A.indices_in(L)
check("indices_in finds the used colours", used == {red, blue}, used)
try:
    A.apply_to_palette(pal, "NOPE")
    check("unknown op raises", False)
except ValueError:
    check("unknown op raises", True)

# ---------------------------------------------------------------- layer groups
c3 = Canvas(4, 4)
c3.add_layer("B")
c3.add_layer("C")
check("duplicate_layer inserts a copy", c3.duplicate_layer(0) is not None and len(c3.layers) == 4)
check("duplicate is independent",
      c3.layers[1].px is not c3.layers[0].px)
check("group_layers tags members", c3.group_layers([0, 1], "Base"))
check("group_members finds them", c3.group_members("Base") == [0, 1], c3.group_members("Base"))
check("group visibility toggles members", c3.set_group_visible("Base", False) == 2
      and not c3.layers[0].visible)
check("ungroup clears the tag", c3.ungroup("Base") == 2 and c3.layers[0].group is None)
check("group of nothing is refused", c3.group_layers([], "X") is False)

n0 = len(c3.layers)
c3.layers[1].set(1, 1, 1)
check("merge_indices folds several layers", c3.merge_indices([0, 1]))
check("merge_indices removed the extras", len(c3.layers) == n0 - 1, len(c3.layers))
check("merge_indices kept the pixel", c3.layers[0].get(1, 1) == 1)
check("merge_indices needs 2+ layers", c3.merge_indices([0]) is False)


# ------------------------------------------------------------- past-parity tools
from core import tools as T
from core.canvas import Canvas as _C
print()

# outline: a 2x2 opaque block in an 6x6 layer has an 8-texel 4-connected ring
lay = Layer("o", 6, 6)
for x in (2, 3):
    for y in (2, 3):
        lay.set(x, y, 1)
ring = T.outline_points(lay)
check("outline rings the shape", len(ring) == 8, len(ring))
check("outline is transparent texels only", all(lay.get(x, y) == 0 for x, y in ring))
check("outline with diagonals is larger", len(T.outline_points(lay, True)) == 12,
      len(T.outline_points(lay, True)))
check("outline of an empty layer is empty", T.outline_points(Layer("e", 4, 4)) == [])

# shift with wrap
px = bytearray([1, 2, 3, 4])
sh = T.shift_wrap(px, 2, 2, 1, 0)
check("shift wraps horizontally", list(sh) == [2, 1, 4, 3], list(sh))
check("shift by full width is a no-op", list(T.shift_wrap(px, 2, 2, 2, 0)) == list(px))
check("shift by zero is a no-op", list(T.shift_wrap(px, 2, 2, 0, 0)) == list(px))

# tiling score
seam = bytearray([1, 1, 1, 1])
r = T.tile_seam_score(seam, 2, 2)
check("uniform texture is seamless", r["seamless"] and r["score"] == 100.0, r)
# A genuine seam: a gradient that does not wrap. The same NUMBER of texels
# change at the wrap as at any interior step, but the colour jump is 6x larger -
# which is exactly the case a count-based metric cannot see.
_GREY = [(0, 0, 0, 0)] + [(v * 36, v * 36, v * 36, 255) for v in range(8)]
_W = 16
grad = bytearray(1 + (x * 7) // _W for _y in range(_W) for x in range(_W))
r2 = T.tile_seam_score(grad, _W, _W, _GREY)
check("a non-wrapping gradient is flagged", not r2["seamless"], r2)
check("its score drops well below 100", r2["score"] < 60, r2["score"])
check("it reports the wrap is harsher than the interior",
      r2["h_wrap"] > r2["h_worst"] * 2, (r2["h_wrap"], r2["h_worst"]))
# and the wrapping version of the same gradient must pass
wrapped = bytearray(1 + min((x * 14) // _W, 14 - (x * 14) // _W)
                    for _y in range(_W) for x in range(_W))
check("the wrapping version passes", T.tile_seam_score(wrapped, _W, _W, _GREY)["seamless"])
check("stripes tile even though every edge differs",
      T.tile_seam_score(bytearray((1 if (x // 2) % 2 == 0 else 6)
                                  for _y in range(_W) for x in range(_W)),
                        _W, _W, _GREY)["seamless"])

# flip / rotate
f = T.flip(bytearray([1, 2, 3, 4]), 2, 2, horizontal=True)
check("horizontal flip mirrors rows", list(f) == [2, 1, 4, 3], list(f))
v = T.flip(bytearray([1, 2, 3, 4]), 2, 2, horizontal=False)
check("vertical flip mirrors columns", list(v) == [3, 4, 1, 2], list(v))
rot, rw, rh = T.rotate90(bytearray([1, 2, 3, 4]), 2, 2, clockwise=True)
check("rotate 90 moves corners", list(rot) == [3, 1, 4, 2], list(rot))
r4 = bytearray([1, 2, 3, 4])
for _ in range(4):
    r4, _w, _h = T.rotate90(r4, 2, 2, True)
check("four rotations return the original", list(r4) == [1, 2, 3, 4], list(r4))

# ramp
ramp = T.make_ramp((180, 60, 60, 255), steps=5)
check("ramp has the asked-for steps", len(ramp) == 5, len(ramp))
lum = [0.2126 * r + 0.7152 * g + 0.0722 * b for r, g, b, _a in ramp]
check("ramp runs dark to light", lum == sorted(lum), [round(x) for x in lum])
check("ramp is not a grey fade (hue actually shifts)",
      len({(r, g, b) for r, g, b, _a in ramp}) == 5)
check("ramp keeps alpha", all(a == 255 for *_c, a in ramp))
check("ramp clamps step count", len(T.make_ramp((1, 2, 3, 255), steps=99)) <= 16)
# regression: a ramp from black used to collapse to one colour (v=0 scales to 0)
for _nm, _base in (("black", (0,0,0,255)), ("white", (255,255,255,255)),
                   ("navy", (12,14,40,255))):
    _r = T.make_ramp(_base, 5)
    check(f"ramp from {_nm} gives 5 distinct colours",
          len({(a,b,c) for a,b,c,_d in _r}) == 5, _r)
    _l = [0.2126*a+0.7152*b+0.0722*c for a,b,c,_d in _r]
    check(f"ramp from {_nm} still runs dark to light", _l == sorted(_l))

# ------------------------------------------------- v0.2 selection transforms
print()

# scale_nearest: the only correct filter on an indexed buffer
src = bytearray([1, 2, 3, 4])
check("scale to the same size is a no-op", list(T.scale_nearest(src, 2, 2, 2, 2)) == [1, 2, 3, 4])
up = T.scale_nearest(src, 2, 2, 4, 4)
check("2x upscale turns each texel into a 2x2 block",
      list(up) == [1, 1, 2, 2, 1, 1, 2, 2, 3, 3, 4, 4, 3, 3, 4, 4], list(up))
check("upscale invents no index outside the source",
      set(up) <= set(src))
# corner sampling would return [1, 3]; centre sampling is half a destination
# texel to the right, and a corner-biased downscale shifts the whole image
check("downscale samples texel centres, not corners",
      list(T.scale_nearest(bytearray([1, 2, 3, 4]), 4, 1, 2, 1)) == [2, 4],
      list(T.scale_nearest(bytearray([1, 2, 3, 4]), 4, 1, 2, 1)))
check("downscale to one texel keeps a real index",
      list(T.scale_nearest(src, 2, 2, 1, 1)) == [4], list(T.scale_nearest(src, 2, 2, 1, 1)))
check("a zero size is clamped to one texel", len(T.scale_nearest(src, 2, 2, 0, 0)) == 1)
check("3x upscale of one texel is 9 of it",
      list(T.scale_nearest(bytearray([7]), 1, 1, 3, 3)) == [7] * 9)

# transform_region: flip with no selection uses the layer's own bounds
from core.select import TRANSFORMS, transform_region
L2 = Layer("t", 6, 6)
L2.set(1, 1, 1)
L2.set(2, 1, 2)
r = transform_region(L2, None, "FLIP_H")
check("flip returns (written, w, h)", r == (2, 2, 1), r)
check("flip with no selection mirrors the layer's content bounds",
      (L2.get(1, 1), L2.get(2, 1)) == (2, 1), (L2.get(1, 1), L2.get(2, 1)))

# rotate: a vertical bar becomes a horizontal one, centred on the box it left
L3 = Layer("t", 6, 6)
for i, y in enumerate((1, 2, 3)):
    L3.set(2, y, i + 1)
sel3 = Selection(6, 6)
sel3.add_rect(2, 1, 2, 3)
r = transform_region(L3, sel3, "ROT_CW")
check("rotating a 1x3 gives a 3x1", r == (3, 3, 1), r)
check("rotate CW reverses the bar",
      [L3.get(x, 2) for x in (1, 2, 3)] == [3, 2, 1], [L3.get(x, 2) for x in (1, 2, 3)])
check("the rotated result is centred on the box it replaced",
      L3.get(2, 1) == 0 and L3.get(2, 3) == 0)
check("the selection follows the rotation", sel3.bounds() == (1, 2, 3, 2), sel3.bounds())
transform_region(L3, sel3, "ROT_CCW")
check("CW then CCW restores the texels",
      [L3.get(2, y) for y in (1, 2, 3)] == [1, 2, 3], [L3.get(2, y) for y in (1, 2, 3)])
check("CW then CCW restores the selection", sel3.bounds() == (2, 1, 2, 3), sel3.bounds())

L3b = Layer("t", 6, 6)
L3b.set(1, 1, 5)
L3b.set(2, 1, 6)
transform_region(L3b, None, "FLIP_V")
check("vertical flip of a single row leaves it in place",
      (L3b.get(1, 1), L3b.get(2, 1)) == (5, 6))

# scale: a 2x2 patch at 2x covers 4x4 and the selection grows with it
L4 = Layer("t", 8, 8)
for i, (x, y) in enumerate(((2, 2), (3, 2), (2, 3), (3, 3))):
    L4.set(x, y, i + 1)
sel4 = Selection(8, 8)
sel4.add_rect(2, 2, 3, 3)
r = transform_region(L4, sel4, "SCALE", 2.0)
check("2x scale writes 16 texels over a 4x4 box", r == (16, 4, 4), r)
check("the scaled block is centred on the old box",
      (L4.get(1, 1), L4.get(4, 1), L4.get(1, 4), L4.get(4, 4)) == (1, 2, 3, 4),
      (L4.get(1, 1), L4.get(4, 1), L4.get(1, 4), L4.get(4, 4)))
check("scale takes the selection with it", sel4.count() == 16, sel4.count())
r = transform_region(L4, sel4, "SCALE", 0.5)
check("scaling back down returns a 2x2", r == (4, 2, 2), r)
check("the round trip restores the art",
      [L4.get(x, y) for x, y in ((2, 2), (3, 2), (2, 3), (3, 3))] == [1, 2, 3, 4],
      [L4.get(x, y) for x, y in ((2, 2), (3, 2), (2, 3), (3, 3))])

# the MASK is transformed, not reset to a bounding box - an L stays an L
L5 = Layer("t", 6, 6)
L5.set(2, 2, 1)
L5.set(3, 2, 2)
sel5 = Selection(6, 6)
sel5.add_points([(2, 2), (3, 2), (2, 3)])       # (2,3) is selected but transparent
n5, _w5, _h5 = transform_region(L5, sel5, "FLIP_H")
check("a transparent selected texel is carried but not counted", n5 == 2, n5)
check("the flipped mask mirrors the shape, it does not become a rectangle",
      (3, 3) in sel5 and (2, 3) not in sel5, sorted(
          (x, y) for y in range(6) for x in range(6) if (x, y) in sel5))
check("the flip moved the art", (L5.get(2, 2), L5.get(3, 2)) == (2, 1),
      (L5.get(2, 2), L5.get(3, 2)))

check("an empty layer has nothing to transform",
      transform_region(Layer("e", 4, 4), None, "FLIP_H") is None)
check("an empty selection falls back to the layer",
      transform_region(L5, Selection(6, 6), "FLIP_H") is not None)

L6 = Layer("t", 4, 4)
L6.set(1, 1, 3)
before6 = bytes(L6.px)
L6.locked = True
check("a locked layer is not transformed",
      transform_region(L6, None, "FLIP_H")[0] == 0 and bytes(L6.px) == before6)

try:
    transform_region(L2, None, "SPIN")
    check("an unknown transform raises", False)
except ValueError:
    check("an unknown transform raises", True)

check("every transform mode is reachable",
      set(TRANSFORMS) == {"FLIP_H", "FLIP_V", "ROT_CW", "ROT_CCW", "SCALE"})

print()
if fails:
    print(f"{len(fails)} FAILED: {fails}")
    sys.exit(1)
print("SELECT / CLIP / ADJUST / GROUPS / TOOLS: ALL PASS")
