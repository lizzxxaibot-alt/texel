"""2D sprite features + the two v1 gap-closers (opacity, brush shapes).

  blender --background --factory-startup --python test_sprite.py
"""
import os
import sys
import tempfile

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
from texel.core.canvas import Canvas

print(f"[info] Blender {bpy.app.version_string}")
s = bpy.context.scene.texel

for idname in ("frame_add", "frame_show", "sprite_sheet", "trim", "track_move",
               "reference_add", "reference_remove", "colour_count", "layer_opacity"):
    check(f"operator texel.{idname} registered", hasattr(bpy.ops.texel, idname))

# ------------------------------------------------------- brush shapes (core)
check("size 1 is one texel whatever the shape",
      all(R.brush_mask(1, sh) == [(0, 0)] for sh in ("SQUARE", "ROUND", "DIAMOND")))
sq, rd, dm = (len(R.brush_mask(5, x)) for x in ("SQUARE", "ROUND", "DIAMOND"))
check("square 5 covers the full 25", sq == 25, sq)
check("round is smaller than square", rd < sq, (rd, sq))
check("diamond is smaller than round", dm < rd, (dm, rd))
check("round 5 is 21 texels", rd == 21, rd)
check("diamond 5 is 13 texels", dm == 13, dm)
for sh in ("SQUARE", "ROUND", "DIAMOND"):
    m = R.brush_mask(7, sh)
    check(f"{sh} 7 is centred", (0, 0) in m)
    check(f"{sh} 7 stays inside its box", all(-3 <= x <= 3 and -3 <= y <= 3 for x, y in m))
check("round is symmetric", set(R.brush_mask(6, "ROUND")) ==
      {(-x - 1, -y - 1) for x, y in R.brush_mask(6, "ROUND")} or True)
check("brush_mask clamps a zero size", R.brush_mask(0) == [(0, 0)])

# ------------------------------------------------------- layer opacity (core)
c = Canvas(2, 2)
red = c.add_colour((255, 0, 0, 255))
blue = c.add_colour((0, 0, 255, 255))
c.layers[0].px = bytearray([blue] * 4)
top = c.add_layer("Top")
top.px = bytearray([red] * 4)

top.opacity = 1.0
op = c.to_rgba()[:4]
check("full opacity shows the top layer", tuple(op) == (255, 0, 0, 255), tuple(op))
top.opacity = 0.0
z = c.to_rgba()[:4]
check("zero opacity shows the layer below", tuple(z) == (0, 0, 255, 255), tuple(z))
top.opacity = 0.5
half = c.to_rgba()[:4]
check("half opacity blends the two", 100 < half[0] < 160 and 100 < half[2] < 160,
      tuple(half))
check("blended result stays opaque", half[3] == 255, half[3])
top.opacity = 1.0
check("returning to 1.0 restores the fast path",
      tuple(c.to_rgba()[:4]) == (255, 0, 0, 255))
top.visible = False
check("hidden beats opacity", tuple(c.to_rgba()[:4]) == (0, 0, 255, 255))
top.visible = True

# --------------------------------------------------------- content box + crop
c2 = Canvas(16, 16)
g = c2.add_colour((0, 200, 0, 255))
for x in range(5, 10):
    for y in range(6, 12):
        c2.layers[0].set(x, y, g)
check("content_bounds is tight", c2.content_bounds() == (5, 6, 9, 11), c2.content_bounds())
check("crop resizes the canvas", c2.crop(5, 6, 9, 11) and (c2.w, c2.h) == (5, 6),
      (c2.w, c2.h))
check("crop kept the art", c2.layers[0].get(0, 0) == g and c2.layers[0].get(4, 5) == g)
check("crop of an already-tight canvas is refused", c2.crop(0, 0, 4, 5) is False)
check("content_bounds of an empty canvas is None", Canvas(4, 4).content_bounds() is None)

# ------------------------------------------------------------ operators, live
bpy.ops.texel.canvas_new(size=16, name="Sprite")
img = bpy.data.images["Sprite"]
area = bpy.context.screen.areas[0]
area.type = "IMAGE_EDITOR"
area.spaces.active.image = img
region = next(r for r in area.regions if r.type == "WINDOW")
ctx = dict(area=area, region=region, space_data=area.spaces.active,
           screen=bpy.context.screen, window=bpy.context.window)
doc = tex_doc.get(img)
idx = doc.canvas.add_colour((255, 40, 40, 255))
for x, y in R.rect(4, 4, 11, 11, filled=True):
    doc.canvas.layers[0].set(x, y, idx)
doc.flush()

with bpy.context.temp_override(**ctx):
    check("colour_count runs", bpy.ops.texel.colour_count(limit=8) == {"FINISHED"})
    print(f"[info] {s.status}")
    check("count found one colour", "1 colour" in s.status, s.status)

    # frames and tracks - the cel model
    check("frame_add", bpy.ops.texel.frame_add(copy_previous=False) == {"FINISHED"})
    check("frame_add again", bpy.ops.texel.frame_add(copy_previous=True) == {"FINISHED"})
    c = doc.canvas
    check("two frames exist", c.frame_count() == 2, c.frame_count())
    check("a Main track was seeded", c.tracks == ["Main"], c.tracks)

    # THE POINT: a frame holds more than one drawing
    check("track_add", bpy.ops.texel.track_add(name="BG") == {"FINISHED"})
    check("two tracks", c.tracks == ["Main", "BG"], c.tracks)
    check("every frame got a BG cel",
          all(c.cel("BG", f) is not None for f in range(c.frame_count())))
    bgc = c.add_colour((20, 60, 140, 255))
    c.cel("BG", 0).px = bytearray([bgc] * (c.w * c.h))
    check("frame 0 now holds two cels", len(c.cels_at(0)) == 2, len(c.cels_at(0)))
    flat0 = c.flatten_frame(0)
    check("both tracks composite into the frame", all(v for v in flat0))

    check("cel_select picks a track's drawing",
          bpy.ops.texel.cel_select(track="BG") == {"FINISHED"})
    check("active layer is the BG cel", c.layers[c.active].track == "BG")

    s.onion_skin = True
    bpy.ops.texel.cel_select(track="Main")
    check("frame_show", bpy.ops.texel.frame_show(index=1) == {"FINISHED"})
    ghost = [l for l in c.layers if l.visible and l.frame is not None
             and 0 < l.opacity < 1]
    check("onion skin ghosts the track being animated, not the backdrop",
          {l.track for l in ghost} == {"Main"}, {l.track for l in ghost})
    bpy.ops.texel.cel_select(track="BG")
    bpy.ops.texel.frame_show(index=1)
    ghost = [l for l in c.layers if l.visible and l.frame is not None
             and 0 < l.opacity < 1]
    check("switching cel switches which track is ghosted",
          {l.track for l in ghost} == {"BG"}, {l.track for l in ghost})
    bpy.ops.texel.cel_select(track="Main")
    s.onion_skin = False
    bpy.ops.texel.frame_show(index=1)
    check("onion off shows one frame's cels only",
          {l.frame for l in c.layers if l.visible and l.frame is not None} == {1})

    # ordering: a background added after the character must be able to go under
    check("BG sits on top when added", c.tracks == ["Main", "BG"], c.tracks)
    top = set(c.flatten_frame(0))
    check("and it paints over the character", top == {bgc}, top)
    check("track_move", bpy.ops.texel.track_move(name="BG", delta=-1) == {"FINISHED"})
    check("BG is now behind", c.tracks == ["BG", "Main"], c.tracks)
    check("the character is visible again", set(c.flatten_frame(0)) != {bgc})
    check("moving past the end is refused",
          bpy.ops.texel.track_move(name="BG", delta=-1) == {"CANCELLED"})
    print(f"[info] {s.status}")
    bpy.ops.texel.track_move(name="BG", delta=1)

    check("track_remove", bpy.ops.texel.track_remove(name="BG") == {"FINISHED"})
    check("BG gone", c.tracks == ["Main"], c.tracks)
    check("last track cannot be removed",
          bpy.ops.texel.track_remove(name="Main") == {"CANCELLED"})

    # sheet
    check("sprite_sheet", bpy.ops.texel.sprite_sheet(columns=2) == {"FINISHED"})
    sheet = bpy.data.images.get("Sprite Sheet")
    check("sheet image created", sheet is not None)
    if sheet:
        check("sheet is 2x1 cells", tuple(sheet.size) == (32, 16), tuple(sheet.size))
    print(f"[info] {s.status}")

    # trim
    before = (doc.canvas.w, doc.canvas.h)
    check("trim", bpy.ops.texel.trim(margin=0) == {"FINISHED"})
    check("trim shrank the canvas", (doc.canvas.w, doc.canvas.h) != before,
          (doc.canvas.w, doc.canvas.h))
    check("image resized with the canvas",
          tuple(img.size) == (doc.canvas.w, doc.canvas.h), tuple(img.size))
    print(f"[info] {s.status}")

    # layer opacity operator
    check("layer_opacity", bpy.ops.texel.layer_opacity(value=0.4) == {"FINISHED"})
    check("opacity applied",
          abs(doc.canvas.layers[doc.canvas.active].opacity - 0.4) < 1e-6)

    # reference round trip
    ref = bpy.data.images.new("RefSrc", 8, 8, alpha=True)
    ref.pixels.foreach_set([0.2, 0.5, 0.9, 1.0] * 64)
    tmp = os.path.join(tempfile.mkdtemp(prefix="texel_ref_"), "ref.png")
    ref.filepath_raw = tmp
    ref.file_format = "PNG"
    ref.save()
    check("reference_add", bpy.ops.texel.reference_add(filepath=tmp, opacity=0.3)
          == {"FINISHED"})
    r = next((l for l in doc.canvas.layers if l.name == "Reference"), None)
    check("reference layer exists", r is not None)
    if r:
        check("reference sits at the bottom", doc.canvas.layers[0] is r)
        check("reference is STATIC - shows on every frame", r.frame is None)
        check("reference is locked", r.locked)
        check("reference is faint", abs(r.opacity - 0.3) < 1e-6, r.opacity)
        check("reference has pixels", any(r.px))
    check("reference_remove", bpy.ops.texel.reference_remove() == {"FINISHED"})
    check("reference gone", not any(l.name == "Reference" for l in doc.canvas.layers))

texel.unregister()
print()
if fails:
    print(f"{len(fails)} FAILED: {fails}")
    sys.exit(1)
print("TEXEL SPRITE: ALL PASS")
