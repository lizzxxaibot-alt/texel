"""Exercise the parity + past-parity operators against live Blender data.

  blender --background --factory-startup --python test_features.py
"""
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
fails = []


def check(name, cond, detail=""):
    print(f"[{'ok  ' if cond else 'FAIL'}] {name}" + ("" if cond else f"  {detail}"))
    if not cond:
        fails.append(name)


import texel
texel.register()
from texel import tex_doc
from texel.core import raster as R

print(f"[info] Blender {bpy.app.version_string}")

ops = sorted(o for o in dir(bpy.ops.texel) if not o.startswith("_"))
print(f"[info] {len(ops)} operators registered")
check("more operators than the reference's 67", len(ops) > 67, len(ops))

# ------------------------------------------------------------------- a canvas
bpy.ops.texel.canvas_new(size=32, name="Feat")
img = bpy.data.images["Feat"]
doc = tex_doc.get(img)
red = doc.canvas.add_colour((255, 0, 0, 255))
for x, y in R.rect(4, 4, 12, 12, filled=True):
    doc.canvas.layers[0].set(x, y, red)
doc.flush()

# an Image Editor is needed for the canvas operators to poll true
area = bpy.context.screen.areas[0]
area.type = "IMAGE_EDITOR"
area.spaces.active.image = img
region = next(r for r in area.regions if r.type == "WINDOW")
ctx = {"area": area, "region": region, "space_data": area.spaces.active,
       "screen": bpy.context.screen, "window": bpy.context.window}

with bpy.context.temp_override(**ctx):
    # --------------------------------------------------------- selection
    check("select_all", bpy.ops.texel.select_all() == {"FINISHED"})
    check("select_all took the whole canvas", doc.canvas.selection.count() == 32 * 32,
          doc.canvas.selection.count())
    bpy.ops.texel.select_invert()
    check("invert emptied it", doc.canvas.selection.count() == 0)
    bpy.ops.texel.select_all()
    bpy.ops.texel.deselect()
    check("deselect clears", doc.canvas.selection.count() == 0)

    bpy.ops.texel.select_linked(x=5, y=5)
    check("select_linked found the red block", doc.canvas.selection.count() == 81,
          doc.canvas.selection.count())
    before = doc.canvas.selection.count()
    bpy.ops.texel.select_grow(amount=1)
    check("select_grow expanded", doc.canvas.selection.count() > before)

    # --------------------------------------------------------- clipboard
    check("copy", bpy.ops.texel.clipboard_copy() == {"FINISHED"})
    check("paste", bpy.ops.texel.clipboard_paste(x=20, y=20) == {"FINISHED"})
    check("pasted texels landed", doc.canvas.layers[doc.canvas.active].get(22, 22) != 0)
    check("cut", bpy.ops.texel.clipboard_cut() == {"FINISHED"})

    # -------------------------------------------------------- adjustments
    doc.canvas.selection.clear()
    before_pal = list(doc.canvas.palette)
    check("adjust brightness", bpy.ops.texel.adjust(op="BRIGHTNESS", amount=0.5) == {"FINISHED"})
    check("palette actually changed", doc.canvas.palette != before_pal)
    check("index 0 still transparent", doc.canvas.palette[0] == (0, 0, 0, 0))
    check("invert", bpy.ops.texel.adjust(op="INVERT") == {"FINISHED"})
    check("greyscale", bpy.ops.texel.adjust(op="GREYSCALE") == {"FINISHED"})

    # -------------------------------------------------------------- layers
    n = len(doc.canvas.layers)
    bpy.ops.texel.layer_duplicate()
    check("layer_duplicate", len(doc.canvas.layers) == n + 1, len(doc.canvas.layers))
    bpy.ops.texel.layer_group(name="G")
    check("layer_group tagged members", any(l.group == "G" for l in doc.canvas.layers))
    bpy.ops.texel.layer_ungroup(name="G")
    check("layer_ungroup", all(l.group is None for l in doc.canvas.layers))
    bpy.ops.texel.layer_merge_selected()
    check("merge_selected reduced the stack", len(doc.canvas.layers) < n + 1)

    # ------------------------------------------------------------ palette
    check("swatch_add", bpy.ops.texel.swatch_add() == {"FINISHED"})
    check("palette_sort", bpy.ops.texel.palette_sort(by="LUMA") == {"FINISHED"})
    check("palette_ramp", bpy.ops.texel.palette_ramp(steps=5) == {"FINISHED"})
    check("ramp added swatches", len(doc.canvas.palette) >= 6, len(doc.canvas.palette))

    # --------------------------------------------------------------- grid
    check("grid_add", bpy.ops.texel.grid_add(spacing=8) == {"FINISHED"})
    check("grid layer exists", any(l.name == "Pixel Grid" for l in doc.canvas.layers))
    check("grid is locked", next(l for l in doc.canvas.layers
                                 if l.name == "Pixel Grid").locked)
    check("grid_toggle", bpy.ops.texel.grid_toggle() == {"FINISHED"})

    # ----------------------------------------------------- past-parity tools
    check("outline_sprite", bpy.ops.texel.outline_sprite() == {"FINISHED"})
    check("check_tileable", bpy.ops.texel.check_tileable() == {"FINISHED"})
    check("tiling reported something", bool(bpy.context.scene.texel.status),
          bpy.context.scene.texel.status)
    print(f"[info] tiling: {bpy.context.scene.texel.status}")
    # The pass message used to read "Seamless: both edge pairs match exactly".
    # tile_seam_score never compares the edges for equality - it compares mean
    # colour distance across the wrap against the harshest interior transition -
    # so the sentence claimed a measurement that was not taken, and it said it
    # over a tile with a moss patch sliced flat at the edge (reproduced
    # 2026-09-23 by texel-support, and again 2026-09-24 here). A heuristic must
    # not report itself as a proof.
    _st = bpy.context.scene.texel.status
    check("the tiling pass does not claim the edges match exactly",
          "exactly" not in _st.lower(), _st)
    check("the tiling pass states it is a heuristic", "heuristic" in _st.lower(), _st)
    check("the tiling pass shows its numbers either way",
          any(ch.isdigit() for ch in _st), _st)
    check("flip", bpy.ops.texel.flip_canvas(axis="H") == {"FINISHED"})
    check("rotate", bpy.ops.texel.rotate_canvas() == {"FINISHED"})
    check("shift_wrap", bpy.ops.texel.shift_wrap(half=True) == {"FINISHED"})
    check("replace_colour", bpy.ops.texel.replace_colour(index=1) == {"FINISHED"})
    check("export_layers", bpy.ops.texel.export_layers() == {"FINISHED"})
    check("canvas_resize", bpy.ops.texel.canvas_resize(size=64) == {"FINISHED"})
    check("resize took effect", doc.canvas.w == 64 and tuple(img.size) == (64, 64),
          (doc.canvas.w, tuple(img.size)))

# ------------------------------------------------------------- density zones
area.type = "VIEW_3D"
bpy.ops.texel.add_cube(size=2, texture=64)
cube = bpy.context.active_object
check("add_cube made a textured cube", cube is not None and len(cube.material_slots) == 1)

r3d = next(r for r in area.regions if r.type == "WINDOW")
with bpy.context.temp_override(area=area, region=r3d, space_data=area.spaces.active):
    check("pixel_art_unwrap", bpy.ops.texel.pixel_art_unwrap(method="CUBE") == {"FINISHED"})
    print(f"[info] unwrap: {bpy.context.scene.texel.status}")

    check("detect_zones", bpy.ops.texel.detect_zones(buckets=2) == {"FINISHED"})
    print(f"[info] zones: {bpy.context.scene.texel.status}")

    # put half the faces in zone 2, then give that zone its own density
    import bmesh
    bpy.ops.object.mode_set(mode="OBJECT")
    bm = bmesh.new()
    bm.from_mesh(cube.data)
    lay = bm.faces.layers.int.get("texel_zone")
    check("zone attribute persisted on the mesh", lay is not None)
    for i, f in enumerate(bm.faces):
        f[lay] = 1 if i < 3 else 2
    bm.to_mesh(cube.data)
    bm.free()

    check("zone_apply", bpy.ops.texel.zone_apply(zone=2, density=8.0) == {"FINISHED"})
    check("zone_info", bpy.ops.texel.zone_info() == {"FINISHED"})
    status = bpy.context.scene.texel.status
    print(f"[info] zone summary: {status}")
    check("summary mentions both zones", "zone 1" in status and "zone 2" in status, status)
    check("the two zones ended at different densities",
          status.count("@") == 2 and
          status.split("@")[1].split("|")[0].strip() != status.split("@")[2].strip(),
          status)
    check("zone_select", bpy.ops.texel.zone_select(zone=2) == {"FINISHED"})
    check("zone_grid", bpy.ops.texel.zone_grid(zone=1) == {"FINISHED"})
    check("zones_clear", bpy.ops.texel.zones_clear() == {"FINISHED"})
    check("setup_viewport", bpy.ops.texel.setup_viewport() == {"FINISHED"})
    check("restore_viewport", bpy.ops.texel.restore_viewport() == {"FINISHED"})

check("shortcuts_restore", bpy.ops.texel.shortcuts_restore() == {"FINISHED"})
check("defaults really restored", bpy.context.scene.texel.tool == "PENCIL")


# ---- radial symmetry reaches the real stroke, not just the maths ------------
# core.raster.symmetry_points is tested headlessly; what that cannot show is
# whether the paint path reads scene.texel.symmetry at all. A property that is
# drawn, saved and ignored looks identical from outside.
#
# `_commit` is not reachable from a test: a registered Operator cannot be
# instantiated in Python (bpy_struct.__new__ raises), and an uncaught raise here
# makes Blender quit with status 0 and NO summary line - i.e. a silently
# skipped suite. That was reproduced while writing this. `stroke_points` is the
# module-level function `_commit` delegates to, and it takes the real property
# group.
from texel.tex_paint import stroke_points

st = bpy.context.scene.texel
st.mirror_x, st.mirror_y = False, False

st.symmetry = 1
check("symmetry off leaves one texel one texel",
      stroke_points(st, [(2, 8)], 17, 17) == [(2, 8)],
      stroke_points(st, [(2, 8)], 17, 17))

st.symmetry = 8
lit = stroke_points(st, [(2, 8)], 17, 17)
check("symmetry=8 turns one texel into eight", len(lit) == 8, lit)
# The check that used to sit here asked that all eight be the SAME distance
# from the centre, and it has failed since the hour it was written (2026-09-16,
# in the release that also reported itself green). It is unsatisfiable, not
# unmet: x^2 + y^2 = 36 has only the four axial integer solutions, so no grid
# point whatsoever lies at radius 6 on a diagonal. The rotation lands at
# (8+-4.243, 8+-4.243) and the nearest texel is (4, 4), radius 5.657.
#
# Snapping the diagonals out to (4, 5) to recover radius 6 would be WORSE art -
# it is 0.76 texels from the true rotation where (4, 4) is 0.34 - so the code is
# right and the assertion was wrong. What eight-fold symmetry does guarantee on
# a grid is below, and both halves discriminate: swapping round() for int() in
# symmetry_points breaks the invariance (it yields (3, 3) against (12, 3)) and
# pushes the radius error to 1.07.
CENTRE = 8.0


def _turned(pts):
    """The set rotated a quarter turn about the canvas centre."""
    return {(int(CENTRE - (y - CENTRE)), int(CENTRE + (x - CENTRE))) for x, y in pts}


def _flipped(pts):
    """The set reflected in the leading diagonal."""
    return {(int(CENTRE + (y - CENTRE)), int(CENTRE + (x - CENTRE))) for x, y in pts}


check("the eight are closed under a quarter turn", _turned(lit) == set(lit), sorted(lit))
check("the eight are closed under a diagonal flip", _flipped(lit) == set(lit), sorted(lit))
check("every one is the nearest texel to its true rotation",
      max(abs(((x - 8) ** 2 + (y - 8) ** 2) ** 0.5 - 6.0) for x, y in lit) <= 0.5 * 2 ** 0.5,
      sorted((round(((x - 8) ** 2 + (y - 8) ** 2) ** 0.5, 3), x, y) for x, y in lit))
check("the original texel is among them", (2, 8) in lit, sorted(lit))
check("the scene properties reach core.raster unchanged",
      lit == R.symmetry_points([(2, 8)], 17, 17, False, False, 8), lit)

st.mirror_x, st.symmetry = True, 4
check("radial 4 with Mirror X is eight-fold",
      len(stroke_points(st, [(3, 5)], 17, 17)) == 8,
      stroke_points(st, [(3, 5)], 17, 17))
st.mirror_x, st.symmetry = False, 1

# ---------------------------------------------------------- dither brush mode
# Same reason as above: `commit_stroke` is the module-level body of `_commit`,
# so this drives the real write path - scene properties in, layer texels out -
# rather than re-testing core.raster.dither_hit, which test_raster.py owns.
from texel.tex_paint import commit_stroke

check("dither defaults OFF, so existing strokes are unchanged", st.dither == "OFF", st.dither)
check("the brush offers every core pattern",
      {i.identifier for i in st.bl_rna.properties["dither"].enum_items}
      == {"OFF", "CHECKER", "QUARTER", "THREE", "BAYER"})

bpy.ops.texel.canvas_new(size=16, name="Dith")
dimg = bpy.data.images["Dith"]
ddoc = tex_doc.get(dimg)
dl = ddoc.canvas.layers[0]
blue = ddoc.canvas.add_colour((0, 0, 255, 255))
green = ddoc.canvas.add_colour((0, 255, 0, 255))
box = R.rect(2, 2, 9, 9, filled=True)


def _painted(idx):
    return {(x, y) for y in range(16) for x in range(16) if dl.get(x, y) == idx}


st.brush_size, st.dither = 1, "OFF"
commit_stroke(ddoc, st, box, blue)
check("dither OFF paints the whole stroke", _painted(blue) == set(box), len(_painted(blue)))

st.dither = "CHECKER"
commit_stroke(ddoc, st, box, green)
g = _painted(green)
check("CHECKER paints exactly half the stroke", len(g) == 32, len(g))
check("CHECKER lands on the canvas grid", all((x + y) % 2 == 0 for x, y in g), sorted(g))
check("the skipped texels keep what was under them",
      _painted(blue) == set(box) - g, len(_painted(blue)))

# two overlapping strokes must agree - the grid is the canvas's, not the stroke's
st.dither = "BAYER"
st.dither_level = 4
commit_stroke(ddoc, st, R.rect(0, 0, 7, 7, filled=True), 0)
commit_stroke(ddoc, st, R.rect(3, 5, 10, 12, filled=True), 0)   # offset not a multiple of 4
cleared = {(x, y) for y in range(16) for x in range(16) if dl.get(x, y) == 0}
check("overlapping Bayer strokes share one grid",
      all(R.dither_hit("BAYER", x, y, 4) for x, y in cleared if 2 <= x <= 9 and 2 <= y <= 9),
      sorted(cleared))

# a wide brush is dithered per stamped texel, not per stroke point
dl.px = bytearray(len(dl.px))
st.brush_size, st.brush_shape, st.dither = 4, "SQUARE", "QUARTER"
commit_stroke(ddoc, st, [(6, 6)], blue)
b = _painted(blue)
check("a 4px QUARTER stamp paints 4 of its 16 texels", len(b) == 4, sorted(b))
check("they are the QUARTER texels", all(x % 2 == 0 and y % 2 == 0 for x, y in b), sorted(b))
st.brush_size, st.dither = 1, "OFF"

def _rgba(x, y):                                   # bpy is bottom-up
    i = ((15 - y) * 16 + x) * 4
    return tuple(round(v * 255) for v in dimg.pixels[i:i + 4])


check("the dithered stroke reaches the image",
      _rgba(6, 6) == (0, 0, 255, 255) and _rgba(5, 6)[3] == 0,
      (_rgba(6, 6), _rgba(5, 6)))

# ------------------------------------------------------------- tablet pressure
# A mouse reads 1.0, so this is the plumbing a tablet drives, not its feel.
check("pressure defaults OFF, so existing strokes are unchanged", st.use_pressure is False)
st.brush_size = 7
dl.px = bytearray(len(dl.px))
commit_stroke(ddoc, st, [(8, 8)], blue, 0.2)
check("with Pressure off the brush ignores a light press",
      len(_painted(blue)) == 49, len(_painted(blue)))
st.use_pressure = True
for _p, _n in ((1.0, 49), (0.5, 16), (0.0, 1)):
    dl.px = bytearray(len(dl.px))
    commit_stroke(ddoc, st, [(8, 8)], blue, _p)
    check(f"with Pressure on, {_p} pressure on a 7 stamps {_n} texels",
          len(_painted(blue)) == _n, len(_painted(blue)))
commit_stroke(ddoc, st, [(8, 8)], 0, 0.5)
check("the eraser narrows with pressure too", len(_painted(blue)) == 0, len(_painted(blue)))
check("pressure leaves the Size setting alone", st.brush_size == 7, st.brush_size)
st.brush_size, st.use_pressure = 1, False

# -------------------------------------------------------------- custom stamps
# Until 0.2.4 "Brush From Selection" saved into a module dict that nothing ever
# painted from. These drive the operator and the real write path end to end.
from texel.core.select import Selection
from texel.tex_paint import saved_stamp

bpy.ops.texel.canvas_new(size=16, name="Stmp")
simg = bpy.data.images["Stmp"]
sdoc = tex_doc.get(simg)
sl = sdoc.canvas.layers[0]
PINK, TEAL = (255, 0, 128, 255), (0, 128, 128, 255)
sl.set(1, 1, sdoc.canvas.add_colour(PINK))
sl.set(2, 1, sdoc.canvas.add_colour(TEAL))
sl.set(1, 2, sdoc.canvas.add_colour(TEAL))           # (2, 2) stays clear
mark = sdoc.canvas.add_colour((9, 9, 9, 255))
area.type = "IMAGE_EDITOR"                  # the viewport checks above left it 3D
area.spaces.active.image = simg
ctx = {"area": area, "region": next(r for r in area.regions if r.type == "WINDOW"),
       "space_data": area.spaces.active, "screen": bpy.context.screen,
       "window": bpy.context.window}
st.tool, st.brush_size, st.dither = "PENCIL", 1, "OFF"
with bpy.context.temp_override(**ctx):
    sdoc.canvas.selection = None
    check("saving a stamp with no selection is refused",
          bpy.ops.texel.custom_brush_add(name="none") == {"CANCELLED"})
    sdoc.canvas.selection = Selection(16, 16)
    sdoc.canvas.selection.add_rect(8, 8, 9, 9)
    check("saving a selection with nothing painted in it is refused",
          bpy.ops.texel.custom_brush_add(name="none") == {"CANCELLED"})
    sdoc.canvas.selection = Selection(16, 16)
    sdoc.canvas.selection.add_rect(1, 1, 2, 2)
    check("save stamp", bpy.ops.texel.custom_brush_add(name="leaf") == {"FINISHED"})
check("the stamp is stored on the scene", "leaf" in st.stamps and "none" not in st.stamps,
      [i.name for i in st.stamps])
check("saving switches the brush to the stamp", (st.brush_shape, st.stamp) == ("STAMP", "leaf"),
      (st.brush_shape, st.stamp))

sl.px = bytearray(len(sl.px))
sl.set(8, 8, mark)
commit_stroke(sdoc, st, [(8, 8)], 1)
check("the stamp paints its own colours, centred like a brush",
      [sdoc.canvas.palette[sl.get(x, y)] for x, y in ((7, 7), (8, 7), (7, 8))] == [PINK, TEAL, TEAL],
      [sl.get(x, y) for x, y in ((7, 7), (8, 7), (7, 8))])
check("its transparent texels leave the canvas alone", sl.get(8, 8) == mark, sl.get(8, 8))
check("it paints nothing outside its box",
      sum(1 for v in sl.px if v) == 4, sum(1 for v in sl.px if v))

commit_stroke(sdoc, st, [(8, 8)], 0)
check("the eraser rubs out the stamp's footprint only",
      [sl.get(x, y) for x, y in ((7, 7), (8, 7), (7, 8), (8, 8))] == [0, 0, 0, mark],
      [sl.get(x, y) for x, y in ((7, 7), (8, 7), (7, 8), (8, 8))])

dl.px = bytearray(len(dl.px))
commit_stroke(ddoc, st, [(4, 4)], 1)
check("a stamp carries its colours into another canvas's palette",
      ddoc.canvas.palette[dl.get(3, 3)] == PINK and ddoc.canvas.palette[dl.get(4, 3)] == TEAL,
      (dl.get(3, 3), dl.get(4, 3), ddoc.canvas.palette))

st.dither = "CHECKER"
sl.px = bytearray(len(sl.px))
commit_stroke(sdoc, st, [(8, 8)], 1)
check("dither applies to a stamp per texel",
      sl.get(8, 7) == 0 and sl.get(7, 7) != 0 and sl.get(7, 8) == 0,
      (sl.get(7, 7), sl.get(8, 7), sl.get(7, 8)))
st.dither = "OFF"

st.tool = "FILL"
sl.px = bytearray(len(sl.px))
commit_stroke(sdoc, st, [(8, 8)], mark)
check("fill keeps the plain brush instead of smearing the stamp",
      sum(1 for v in sl.px if v) == 1 and sl.get(8, 8) == mark, sum(1 for v in sl.px if v))
st.tool = "PENCIL"

bad = st.stamps.add()
bad.name, bad.data = "bad", "{oops"
st.stamp = "bad"
check("a damaged saved stamp reads as no stamp", saved_stamp(st) is None)
sl.px = bytearray(len(sl.px))
commit_stroke(sdoc, st, [(8, 8)], mark)
check("and the brush falls back to a plain texel rather than raising",
      sum(1 for v in sl.px if v) == 1 and sl.get(8, 8) == mark, sum(1 for v in sl.px if v))

st.stamp = "leaf"
with bpy.context.temp_override(**ctx):
    check("removing a stamp that does not exist is refused",
          bpy.ops.texel.custom_brush_remove(name="ghost") == {"CANCELLED"})
    check("remove the selected stamp", bpy.ops.texel.custom_brush_remove() == {"FINISHED"})
    check("the next stamp becomes selected", (st.stamp, st.brush_shape) == ("bad", "STAMP"),
          (st.stamp, st.brush_shape))
    bpy.ops.texel.custom_brush_remove(name="bad")
check("removing the last stamp puts the brush back to Square",
      (len(st.stamps), st.stamp, st.brush_shape) == (0, "", "SQUARE"),
      (len(st.stamps), st.stamp, st.brush_shape))

# ------------------------------------------- paint mode stays on (0.2.7, T-028)
# The first stranger to use Texel had to press Texel Paint before every stroke:
# the operator ended on the first mouse release. It is a mode now. This drives
# the REAL invoke/modal code with synthetic events, the harness texel-support
# used to reproduce the bug (repro/paint_per_stroke_20261103/); the texel
# lookup is replaced because background mode has no viewport to raycast into.
from texel import tex_paint as TP

pimg = bpy.data.images.new("ModeCanvas", 16, 16, alpha=True)
pimg.pixels.foreach_set([0.0] * 16 * 16 * 4)
pdoc = tex_doc.get(pimg)


class _Ev:
    def __init__(s, t, v="NOTHING", x=0, y=0):
        s.type, s.value, s.x, s.y, s.pressure = t, v, x, y, 1.0
        s.mouse_x, s.mouse_y = x, y


class _Region:
    def __init__(s, t, x, y, w, h):
        s.type, s.x, s.y, s.width, s.height = t, x, y, w, h


class _Area:
    def __init__(s, ptr):
        s.ptr, s.type, s.header = ptr, "IMAGE_EDITOR", None
        s.regions = [_Region("WINDOW", 0, 0, 400, 300), _Region("UI", 300, 0, 100, 300),
                     _Region("HEADER", 0, 280, 400, 20), _Region("TOOLS", 0, 0, 1, 300)]
    def as_pointer(s): return s.ptr
    def header_text_set(s, t): s.header = t
    def tag_redraw(s): pass


class _WM:
    handlers = 0
    def modal_handler_add(s, op): _WM.handlers += 1


class _Sp:
    type = "IMAGE_EDITOR"
    image = pimg


area_a, area_b = _Area(1), _Area(2)


class _Screen:
    areas = [area_a, area_b]


class _Ctx:
    space_data = _Sp(); scene = bpy.context.scene; window_manager = _WM()
    active_object = None; screen = _Screen(); area = area_a


class _Op:    # the operator's own methods; a bpy_struct cannot be built by hand
    def report(s, *a): s.reports.append(a)
for _k, _v in TP.TEXEL_OT_paint.__dict__.items():
    if callable(_v) and not _k.startswith("__") and _k not in ("poll", "report"):
        setattr(_Op, _k, _v)
# x < 0 stands for "over the sidebar", where there is no texel
_Op._texel = lambda s, ctx, ev: (ev.x, ev.y) if 0 <= ev.x < 16 else None
_pushes = []
_Op._push = lambda s: _pushes.append(1)

pctx = _Ctx()
ps = pctx.scene.texel
ps.tool, ps.colour, ps.brush_shape, ps.dither = "PENCIL", (1, 0, 0, 1), "SQUARE", "OFF"
ps.brush_size, ps.mirror_x, ps.mirror_y, ps.symmetry = 1, False, False, 1
ps.use_pressure = False
plit = lambda: sum(1 for v in pdoc.canvas.flatten() if v)


def drag(op, y, x0, x1):
    out = [op.modal(pctx, _Ev("LEFTMOUSE", "PRESS", x0, y))]
    for x in range(x0 + 1, x1 + 1):
        out.append(op.modal(pctx, _Ev("MOUSEMOVE", "NOTHING", x, y)))
    out.append(op.modal(pctx, _Ev("LEFTMOUSE", "RELEASE", x1, y)))
    return out


mop = _Op(); mop.reports = []
check("Texel Paint enters the mode even with the cursor over the sidebar",
      mop.invoke(pctx, _Ev("LEFTMOUSE", "PRESS", -5, 2)) == {"RUNNING_MODAL"}, mop.reports)
check("the mode is on for this editor only",
      TP.paint_mode_on(area_a) and not TP.paint_mode_on(area_b))
check("the header says how to leave it", area_a.header == TP.HINT, area_a.header)
check("entering paints nothing", plit() == 0, plit())
check("a mouse move with no button held paints nothing",
      mop.modal(pctx, _Ev("MOUSEMOVE", "NOTHING", 3, 3)) == {"PASS_THROUGH"} and plit() == 0)
r1 = drag(mop, 2, 1, 7)
check("stroke 1 paints 7 texels and the mode stays on",
      plit() == 7 and all(r == {"RUNNING_MODAL"} for r in r1), (plit(), r1))
r2 = drag(mop, 5, 1, 5)
check("stroke 2 paints with the mouse alone, no second press of Texel Paint",
      plit() == 12 and all(r == {"RUNNING_MODAL"} for r in r2), (plit(), r2))
check("one undo step per drag", len(_pushes) == 2, len(_pushes))
check("a click off the canvas passes through to the sidebar",
      mop.modal(pctx, _Ev("LEFTMOUSE", "PRESS", -5, 5)) == {"PASS_THROUGH"} and plit() == 12)
check("navigation passes through",
      all(mop.modal(pctx, _Ev(t, "PRESS", 3, 3)) == {"PASS_THROUGH"}
          for t in ("MIDDLEMOUSE", "WHEELUPMOUSE", "B", "RIGHTMOUSE")))
ps.tool = "LINE"
mop.modal(pctx, _Ev("LEFTMOUSE", "PRESS", 1, 9))
mop.modal(pctx, _Ev("MOUSEMOVE", "NOTHING", 9, 9))
check("a line previews while dragging", plit() == 21, plit())
check("right-click mid-drag drops the shape and keeps the mode",
      mop.modal(pctx, _Ev("RIGHTMOUSE", "PRESS", 9, 9)) == {"RUNNING_MODAL"}
      and plit() == 12 and len(_pushes) == 2, (plit(), len(_pushes)))
ps.tool = "FILL"
check("a fill is one click, one undo step, and the mode stays on",
      mop.modal(pctx, _Ev("LEFTMOUSE", "PRESS", 0, 15)) == {"RUNNING_MODAL"}
      and plit() == 256 and len(_pushes) == 3, (plit(), len(_pushes)))
ps.tool = "PENCIL"
mop2 = _Op(); mop2.reports = []
check("pressing Texel Paint again in the same editor leaves the mode",
      mop2.invoke(pctx, _Ev("D", "PRESS", 3, 3)) == {"CANCELLED"} and not TP.paint_mode_on())
check("the running mode exits on its next event and clears the header",
      mop.modal(pctx, _Ev("MOUSEMOVE", "NOTHING", 3, 3)) == {"FINISHED"} and area_a.header is None,
      area_a.header)
mop.invoke(pctx, _Ev("D", "PRESS", 3, 3))
pctx.area = area_b
mop3 = _Op(); mop3.reports = []
check("Texel Paint in another editor moves the mode there",
      mop3.invoke(pctx, _Ev("D", "PRESS", 3, 3)) == {"RUNNING_MODAL"}
      and TP.paint_mode_on(area_b) and not TP.paint_mode_on(area_a))
check("the old editor's mode exits without switching the new one off",
      mop.modal(pctx, _Ev("MOUSEMOVE", "NOTHING", 3, 3)) == {"FINISHED"}
      and TP.paint_mode_on(area_b))
mop3.modal(pctx, _Ev("LEFTMOUSE", "PRESS", 2, 0))
check("Esc mid-stroke keeps the stroke and leaves the mode",
      mop3.modal(pctx, _Ev("ESC", "PRESS", 2, 0)) == {"FINISHED"}
      and not TP.paint_mode_on() and area_b.header is None and len(_pushes) == 4,
      len(_pushes))
mop3.invoke(pctx, _Ev("D", "PRESS", 3, 3))
mop3.cancel(pctx)
check("Blender removing the handler (a file load) clears the mode", not TP.paint_mode_on())
pctx.area = area_a

# the hit test the mode uses: on the main region, and not under a panel that
# overlaps it - a click on a sidebar button must not paint the texel beneath
win = area_a.regions[0]
check("over_canvas: the middle of the editor is canvas", TP.over_canvas(area_a, win, 150, 150))
check("over_canvas: an overlapping sidebar is not", not TP.over_canvas(area_a, win, 350, 150))
check("over_canvas: the header is not", not TP.over_canvas(area_a, win, 150, 290))
check("over_canvas: a collapsed 1 px toolbar does not block", TP.over_canvas(area_a, win, 0, 150))
check("over_canvas: outside the editor is not", not TP.over_canvas(area_a, win, 450, 150))

# the hidden-track fix, through the real Export Sprite Sheet operator: the
# regression case @wenvikstudios proposed (ROADMAP v0.2.7). Two frames; export
# Base alone; add Torch and Glow, hide them with the eye, step a frame (which
# used to switch them back on); export again. The sheets must match exactly.
bpy.ops.texel.canvas_new(size=8, name="Tracks")
timg = bpy.data.images["Tracks"]
tdoc = tex_doc.get(timg)
with bpy.context.temp_override(**ctx):
    ctx_space = bpy.context.space_data
    ctx_space.image = timg
    bpy.ops.texel.frame_add()
    bpy.ops.texel.frame_add()
    tc = tdoc.canvas
    base = tc.add_colour((90, 60, 30, 255))
    for f in range(2):
        tc.cel(tc.tracks[0], f).set(1 + f, 2, base)

    def sheet_px():
        bpy.ops.texel.sprite_sheet(columns=0)
        sh = bpy.data.images[f"{tdoc.image_name} Sheet"]
        return list(sh.pixels)

    alone = sheet_px()
    fire = tc.add_colour((255, 140, 0, 255))
    for name in ("Torch", "Glow"):
        bpy.ops.texel.track_add(name=name)
        for f in range(2):
            tc.cel(name, f).set(1 + f, 2, fire)
            tc.cel(name, f).set(7, 7 - f, fire)
    check("shown effect tracks change the sheet", sheet_px() != alone)
    for name in ("Torch", "Glow"):
        cel = tc.cel(name, 0)
        bpy.ops.texel.layer_toggle(index=tc.layers.index(cel))
    check("the eye on one cel hides the whole track",
          tc.track_hidden("Torch") and tc.track_hidden("Glow")
          and not any(l.visible for l in tc.layers if l.track in ("Torch", "Glow")))
    bpy.ops.texel.frame_show(index=1)
    check("a frame step does not switch a hidden track back on",
          not any(l.visible for l in tc.layers if l.track in ("Torch", "Glow")))
    check("REGRESSION CASE: Base alone == Base + hidden Torch and Glow, pixel for pixel",
          sheet_px() == alone)
    bpy.ops.texel.layer_toggle(index=tc.layers.index(tc.cel("Glow", 0)))
    check("the eye again shows the track", not tc.track_hidden("Glow")
          and sheet_px() != alone)
    st_layer = tc.add_layer("Static")
    st_layer.frame = st_layer.track = None
    bpy.ops.texel.layer_toggle(index=tc.layers.index(st_layer))
    check("a static layer's eye still toggles just that layer",
          not st_layer.visible and not tc.track_hidden("Static"))

texel.unregister()
print()
if fails:
    print(f"{len(fails)} FAILED: {fails}")
    sys.exit(1)
print("TEXEL FEATURES: ALL PASS")
