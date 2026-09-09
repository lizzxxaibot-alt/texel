"""Showcase feature test - it must build a rig, render, and clean up after itself.

  blender --background --factory-startup --python test_showcase.py
"""
import math
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
from texel.tex_showcase import COLLECTION, PRESETS, subject_bounds

print(f"[info] Blender {bpy.app.version_string}")
s = bpy.context.scene.texel

for idname in ("showcase_setup", "showcase_render", "showcase_clear"):
    check(f"operator texel.{idname} registered", hasattr(bpy.ops.texel, idname))
check("six lighting presets", len(PRESETS) == 6, len(PRESETS))

# --- refuses to build with nothing to show.
# --factory-startup ships a default Cube, so the scene must be emptied first.
for _o in list(bpy.data.objects):
    bpy.data.objects.remove(_o, do_unlink=True)
check("setup refuses an empty scene",
      bpy.ops.texel.showcase_setup() == {"CANCELLED"})

# --- a subject with a texture whose filtering is deliberately WRONG
bpy.ops.mesh.primitive_cube_add(size=2)
cube = bpy.context.active_object
img = bpy.data.images.new("Art", 32, 32, alpha=True)
img.pixels.foreach_set([0.6, 0.3, 0.2, 1.0] * (32 * 32))
mat = bpy.data.materials.new("M")
mat.use_nodes = True
tex = mat.node_tree.nodes.new("ShaderNodeTexImage")
tex.image = img
tex.interpolation = "Linear"            # the classic pixel-art mistake
mat.node_tree.links.new(tex.outputs["Color"],
                        mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"])
cube.data.materials.append(mat)

b = subject_bounds(bpy.context)
check("subject_bounds finds the mesh", b is not None)
centre, radius, lo, hi = b
check("bounds centred on the cube", all(abs(c) < 1e-6 for c in centre), centre)
check("radius covers the cube", abs(radius - 1.0) < 1e-6, radius)

# --- build
s.showcase_preset = "GOLDEN"
s.showcase_move = "ARC"
check("setup succeeds", bpy.ops.texel.showcase_setup() == {"FINISHED"})
col = bpy.data.collections.get(COLLECTION)
check("showcase collection created", col is not None)
names = {o.name for o in col.objects}
check("camera built", "Texel Camera" in names, names)
check("key light built", "Texel Key" in names)
check("rim light built", "Texel Rim" in names)
check("focus target built", "Texel Focus" in names)
check("bounded haze built, not a world volume", "Texel Haze" in names, names)
check("scene camera is ours", bpy.context.scene.camera.name == "Texel Camera")

# the whole point: filtering is corrected for the user
check("texture filtering forced to Closest", tex.interpolation == "Closest",
      tex.interpolation)
check("engine set to Cycles", bpy.context.scene.render.engine == "CYCLES")
check("resolution applied", (bpy.context.scene.render.resolution_x,
                             bpy.context.scene.render.resolution_y) ==
      (s.showcase_width, s.showcase_height))

# haze must be a MESH volume, never a world volume - a world volume attenuates
# light across infinite space and drops a lit scene to near black
haze = bpy.data.objects["Texel Haze"]
check("haze is a mesh object", haze.type == "MESH")
wnt = bpy.context.scene.world.node_tree
check("world has NO volume attached",
      not wnt.nodes["World Output"].inputs["Volume"].is_linked)

# --- camera actually moves along the path
from texel.tex_showcase import _place
cam = bpy.data.objects["Texel Camera"]
pos = []
for t in (0.0, 0.5, 1.0):
    _place(cam, centre, radius, "ARC", t)
    pos.append(tuple(round(v, 4) for v in cam.location))
check("arc moves the camera", len(set(pos)) == 3, pos)
d0 = math.dist(pos[0], centre)
d2 = math.dist(pos[2], centre)
check("arc closes in on the subject", d2 < d0, (round(d0, 2), round(d2, 2)))
_place(cam, centre, radius, "ORBIT", 0.0)
a = tuple(cam.location)
_place(cam, centre, radius, "ORBIT", 0.5)
bpos = tuple(cam.location)
check("orbit keeps a constant radius",
      abs(math.dist(a, centre) - math.dist(bpos, centre)) < 1e-4)
_place(cam, centre, radius, "STILL", 0.0)
st = tuple(cam.location)
_place(cam, centre, radius, "STILL", 1.0)
check("still does not move", st == tuple(cam.location))

# --- every preset must build without error
for key in PRESETS:
    s.showcase_preset = key
    r = bpy.ops.texel.showcase_setup()
    check(f"preset {key} builds", r == {"FINISHED"}, r)
check("STUDIO has no haze (fog density 0)",
      "Texel Haze" not in {o.name for o in bpy.data.collections[COLLECTION].objects})

# --- render a still, cheaply
s.showcase_preset = "STUDIO"
s.showcase_move = "STILL"
s.showcase_samples = 4
s.showcase_width = s.showcase_height = 160
tmp = tempfile.mkdtemp(prefix="texel_show_")
s.showcase_output = tmp
bpy.ops.texel.showcase_setup()
check("render still succeeds", bpy.ops.texel.showcase_render() == {"FINISHED"})
pngs = [f for f in os.listdir(tmp) if f.endswith(".png")]
check("a PNG was written", len(pngs) == 1, pngs)

# --- render a 3-frame move
s.showcase_move = "ORBIT"
s.showcase_frames = 3
bpy.ops.texel.showcase_setup()
check("render sequence succeeds", bpy.ops.texel.showcase_render() == {"FINISHED"})
pngs = sorted(f for f in os.listdir(tmp) if f.endswith(".png"))
check("three frames written", len(pngs) >= 3, pngs)
print(f"[info] status: {s.status}")

# --- cleanup must remove the rig and leave the art alone
check("clear succeeds", bpy.ops.texel.showcase_clear() == {"FINISHED"})
check("collection removed", bpy.data.collections.get(COLLECTION) is None)
check("the user's cube survived", bpy.data.objects.get("Cube") is not None)
check("clear on an absent rig is harmless",
      bpy.ops.texel.showcase_clear() == {"FINISHED"})

import shutil
shutil.rmtree(tmp, ignore_errors=True)
texel.unregister()

print()
if fails:
    print(f"{len(fails)} FAILED: {fails}")
    sys.exit(1)
print("TEXEL SHOWCASE: ALL PASS")
