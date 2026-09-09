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

texel.unregister()
print()
if fails:
    print(f"{len(fails)} FAILED: {fails}")
    sys.exit(1)
print("TEXEL FEATURES: ALL PASS")
