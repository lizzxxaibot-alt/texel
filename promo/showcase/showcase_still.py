"""Headless: crates wearing a 64x64 pixel texture, then Texel 0.2.5's own
Build Showcase + Render Showcase (Still). Shipped zip only, factory startup.
  blender -b --factory-startup --python showcase_still.py -- <tz> <out> <PRESET>
"""
import sys, os, math
import bpy

tz, out, preset = sys.argv[sys.argv.index("--") + 1:][:3]
sys.path.insert(0, tz)
import texel
texel.register()
from texel.core.tools import make_ramp

for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)

S = 64
img = bpy.data.images.new("crate64", S, S, alpha=True)
wood = make_ramp((176, 124, 76, 255), 5)          # Texel's own ramp builder
px = [0.0] * (S * S * 4)
def put(x, y, c):
    i = ((S - 1 - y) * S + x) * 4
    px[i:i + 4] = [v / 255 for v in c]
for y in range(S):
    for x in range(S):
        plank = (y // 8)
        c = wood[2] if plank % 2 else wood[3]
        if y % 8 == 0: c = wood[1]
        if y % 8 == 1: c = wood[4]
        joint = (x + plank * 23) % 32            # staggered plank ends
        if joint == 0: c = wood[0]
        if joint == 1 and y % 8 > 1: c = wood[4]
        if (x * 7 + y * 13 + plank) % 41 == 0 and y % 8 > 2: c = wood[1]  # grain
        put(x, y, c)
img.pixels[:] = px
img.filepath_raw = os.path.join(out, "crate64.png"); img.file_format = "PNG"; img.save()

mat = bpy.data.materials.new("Crate"); mat.use_nodes = True
nt = mat.node_tree
tex = nt.nodes.new("ShaderNodeTexImage"); tex.image = img
tex.interpolation = "Linear"          # left wrong on purpose: Build fixes it
nt.links.new(tex.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"])
for loc, sc in (((0, 0, 0), (3.0, 3.0, 0.4)), ((-0.9, 0.6, 0.7), (0.9,) * 3),
                ((1.0, -0.3, 0.6), (0.7,) * 3)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.view_layer.objects.active
    o.scale = sc
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(mat)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.cube_project(cube_size=1.0)
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.context.scene.texel.target_density = 32.0
    print("DENSITY", o.name, bpy.ops.texel.density_apply())

s = bpy.context.scene.texel
s.showcase_preset = preset
s.showcase_move = "STILL"
s.showcase_samples = 64
s.showcase_width, s.showcase_height = 1280, 720
s.showcase_output = out + os.sep
print("BUILD", bpy.ops.texel.showcase_setup())
print("INTERP_AFTER_BUILD", tex.interpolation)
print("COLLECTION", [o.name for o in bpy.data.collections["Texel Showcase"].objects])
print("RENDER", bpy.ops.texel.showcase_render())
print("STATUS", s.status)
os.replace(os.path.join(out, "showcase_0000.png"), os.path.join(out, f"showcase_{preset}.png"))

# ---- BEFORE: the same camera, with the rig removed and Blender's defaults back
for n in ("Texel Key", "Texel Rim", "Texel Haze", "Texel Ground"):
    bpy.data.objects.remove(bpy.data.objects[n], do_unlink=True)
tex.interpolation = "Linear"                       # Blender's default
w = bpy.data.worlds.new("Default"); w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.05, 0.05, 0.05, 1)
w.node_tree.nodes["Background"].inputs[1].default_value = 1.0
sc = bpy.context.scene; sc.world = w
bpy.ops.object.light_add(type="POINT", location=(4.08, 1.01, 5.9))   # factory light
bpy.context.view_layer.objects.active.data.energy = 1000
sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "None"
sc.render.filepath = os.path.join(out, "showcase_BEFORE")
bpy.ops.render.render(write_still=True)
print("BEFORE done", tex.interpolation)
