"""End-to-end add-on test. Loads Texel as a real package, registers it, and
exercises the operators against a live mesh.

  blender --background --factory-startup --python test_addon.py
"""
import math
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))          # parent, so `import texel` works

fails = []


def check(name, cond, detail=""):
    if cond:
        print(f"[ok]   {name}")
    else:
        print(f"[FAIL] {name}  {detail}")
        fails.append(name)


print(f"[info] Blender {bpy.app.version_string}")

# ---------------------------------------------------------------- register
import texel
texel.register()
check("add-on registers cleanly", True)
check("scene.texel property exists", hasattr(bpy.context.scene, "texel"))

s = bpy.context.scene.texel
check("default tool is PENCIL", s.tool == "PENCIL", s.tool)
check("pixel perfect defaults ON", s.pixel_perfect is True)

# every operator the UI references must actually exist, or panels raise at draw
for idname in ("texel.paint", "texel.canvas_new", "texel.layer_add",
               "texel.layer_remove", "texel.layer_merge_down", "texel.layer_select",
               "texel.layer_toggle", "texel.density_detect", "texel.density_apply",
               "texel.snap_uvs", "texel.palette_load", "texel.palette_save",
               "texel.palette_from_image", "texel.palette_lospec", "texel.swatch_use"):
    mod, op = idname.split(".")
    check(f"operator {idname} registered", hasattr(getattr(bpy.ops, mod), op))

# ---------------------------------------------------------------- canvas op
bpy.ops.texel.canvas_new(size=32, name="TestCanvas")
img = bpy.data.images.get("TestCanvas")
check("canvas_new made an image", img is not None and tuple(img.size) == (32, 32),
      tuple(img.size) if img else None)

from texel import tex_doc
doc = tex_doc.get(img)
check("a Doc was bound to the image", doc is not None and doc.canvas.w == 32)

# paint through the core and flush, the same path the modal operator uses
from texel.core import raster as R
idx = doc.canvas.add_colour((255, 0, 0, 255))
for x, y in R.line(2, 2, 29, 29):
    doc.canvas.layers[0].set(x, y, idx)
check("flush reports success", doc.flush() is True)

buf = [0.0] * (32 * 32 * 4)
img.pixels.foreach_get(buf)
o = ((32 - 1 - 2) * 32 + 2) * 4                    # image (2,2) -> bpy bottom-up
check("painted texel is live in the image",
      tuple(round(v * 255) for v in buf[o:o + 4]) == (255, 0, 0, 255),
      tuple(round(v * 255) for v in buf[o:o + 4]))

# ---------------------------------------------------------------- round trip
doc.load_from_image()
check("load_from_image recovered the stroke",
      doc.canvas.layers[0].get(2, 2) != 0, doc.canvas.layers[0].get(2, 2))
check("load_from_image built a palette", len(doc.canvas.palette) >= 2,
      len(doc.canvas.palette))
check("transparent stays transparent on load", doc.canvas.layers[0].get(20, 2) == 0)

# ---------------------------------------------------------------- density
bpy.ops.mesh.primitive_cube_add(size=2)            # 2m cube -> 4 sq units / face
cube = bpy.context.active_object
mat = bpy.data.materials.new("M")
mat.use_nodes = True
tex = mat.node_tree.nodes.new("ShaderNodeTexImage")
tex.image = bpy.data.images.new("CubeTex", 64, 64, alpha=True)
cube.data.materials.append(mat)
check("cube has a UV map", len(cube.data.uv_layers) > 0)

r = bpy.ops.texel.density_detect()
check("density_detect ran", r == {"FINISHED"}, r)
detected = bpy.context.scene.texel.target_density
check("detected a positive density", detected > 0, detected)
print(f"[info] cube default density: {detected:.2f} px/unit  |  {bpy.context.scene.texel.status}")

bpy.context.scene.texel.target_density = 16.0
r = bpy.ops.texel.density_apply()
check("density_apply ran", r == {"FINISHED"}, r)
bpy.ops.texel.density_detect()
after = bpy.context.scene.texel.target_density
check("apply actually moved density to the target",
      math.isclose(after, 16.0, rel_tol=0.02), f"asked 16.0, measured {after:.3f}")

r = bpy.ops.texel.snap_uvs()
check("snap_uvs ran", r == {"FINISHED"}, r)
uvs = cube.data.uv_layers.active.data
on_grid = all(
    math.isclose(uv.uv[0] * 64, round(uv.uv[0] * 64), abs_tol=1e-4) and
    math.isclose(uv.uv[1] * 64, round(uv.uv[1] * 64), abs_tol=1e-4)
    for uv in uvs)
check("every UV landed on a texel corner", on_grid)

# ---------------------------------------------------------------- layers
before = len(doc.canvas.layers)
doc.canvas.add_layer("Second")
check("layer added", len(doc.canvas.layers) == before + 1)
doc.canvas.layers[doc.canvas.active].set(5, 5, idx)
check("merge_down folds the layer away",
      doc.canvas.merge_down(doc.canvas.active) and len(doc.canvas.layers) == before)
check("merged pixel survived", doc.canvas.layers[0].get(5, 5) == idx)

# ---------------------------------------------------------------- unregister
texel.unregister()
check("unregisters without error", True)
check("scene property removed", not hasattr(bpy.types.Scene, "texel"))

print()
if fails:
    print(f"{len(fails)} FAILED: {fails}")
    sys.exit(1)
print("TEXEL ADDON: ALL PASS")
