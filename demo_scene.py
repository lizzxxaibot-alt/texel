"""Render the hero shot for the store page - a real one.

Builds a low-poly scene, paints its texture THROUGH TEXEL'S OWN CORE, applies it
with nearest-neighbour filtering, and renders. Nothing here is mocked: if the
add-on could not paint, this image could not exist.

  blender --background --factory-startup --python demo_scene.py
"""
import math
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from core import raster as R
from core.canvas import Canvas

OUT = os.path.join(HERE, "shots")
os.makedirs(OUT, exist_ok=True)
SIZE = 64

# ---------------------------------------------------------------- clean slate
bpy.ops.wm.read_factory_settings(use_empty=True)

# ---------------------------------------------------------------- the texture
c = Canvas(SIZE, SIZE)
GRASS_D = c.add_colour((58, 106, 66, 255))
GRASS_L = c.add_colour((96, 158, 84, 255))
DIRT = c.add_colour((122, 88, 58, 255))
STONE = c.add_colour((132, 132, 140, 255))
STONE_L = c.add_colour((176, 176, 184, 255))
EMBER = c.add_colour((255, 156, 63, 255))
CREAM = c.add_colour((242, 230, 200, 255))

L = c.layers[0]
for x, y in R.rect(0, 0, SIZE - 1, SIZE - 1, filled=True):
    L.set(x, y, GRASS_D)

def motif(ox, oy):
    """One 32x32 tile: a stone path, a grass tuft, an ember rune. Drawn so the
    cube reads as pixel art from any angle instead of as a checker field."""
    for x, y in R.ellipse(ox + 9, oy + 20, 6, 4, filled=True):
        L.set(x, y, STONE)
    for x, y in R.ellipse(ox + 9, oy + 20, 6, 4):
        L.set(x, y, STONE_L)
    for x, y in R.ellipse(ox + 22, oy + 24, 4, 3, filled=True):
        L.set(x, y, DIRT)
    # grass tufts: short vertical strokes, the way a pixel artist marks ground
    for i, (tx, ty) in enumerate(((4, 6), (13, 4), (21, 8), (27, 13), (6, 27))):
        for x, y in R.line(ox + tx, oy + ty, ox + tx, oy + ty - 3):
            L.set(x, y, GRASS_L)
        L.set(ox + tx - 1, oy + ty - 2, GRASS_L)
        L.set(ox + tx + 1, oy + ty - 2 - (i % 2), GRASS_L)
    # the ember rune - a pixel-perfect diagonal, the marquee feature, on show
    for x, y in R.pixel_perfect(R.line(ox + 18, oy + 5, ox + 28, oy + 10)):
        L.set(x, y, EMBER)
    for x, y in R.rect(ox + 17, oy + 15, ox + 21, oy + 19):
        L.set(x, y, CREAM)

for ox in (0, 32):
    for oy in (0, 32):
        motif(ox, oy)

img = bpy.data.images.new("TexelDemo", SIZE, SIZE, alpha=True)
img.pixels.foreach_set(c.to_blender_floats())
img.update()
img.filepath_raw = os.path.join(OUT, "texture_64.png")
img.file_format = "PNG"
img.save()
print(f"[ok] texture written: {img.filepath_raw}")

# ---------------------------------------------------------------- the model
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
cube = bpy.context.active_object
cube.name = "Block"
bpy.ops.object.shade_flat()

mat = bpy.data.materials.new("TexelDemoMat")
mat.use_nodes = True
nt = mat.node_tree
bsdf = nt.nodes["Principled BSDF"]
tex = nt.nodes.new("ShaderNodeTexImage")
tex.image = img
tex.interpolation = "Closest"          # nearest-neighbour: pixels stay pixels
tex.location = (-400, 200)
nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
bsdf.inputs["Roughness"].default_value = 0.85
bsdf.inputs["Specular IOR Level"].default_value = 0.1
cube.data.materials.append(mat)

# ---------------------------------------------------------------- staging
bpy.ops.mesh.primitive_cube_add(size=1.2, location=(-1.75, -0.6, -0.4))
small = bpy.context.active_object
bpy.ops.object.shade_flat()
small.rotation_euler = (0, 0, math.radians(31))
small.data.materials.append(mat)

bpy.ops.mesh.primitive_plane_add(size=24, location=(0, 0, -1.001))
floor = bpy.context.active_object
fm = bpy.data.materials.new("Floor")
fm.use_nodes = True
fm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.055, 0.05, 0.062, 1)
fm.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.95
floor.data.materials.append(fm)

cam_data = bpy.data.cameras.new("Cam")
cam_data.lens = 58
cam = bpy.data.objects.new("Cam", cam_data)
bpy.context.collection.objects.link(cam)
cam.location = (5.1, -5.6, 3.9)
cam.rotation_euler = (math.radians(58), 0, math.radians(43))
bpy.context.scene.camera = cam

key = bpy.data.lights.new("Key", "AREA")
key.energy = 900
key.size = 6
ko = bpy.data.objects.new("Key", key)
bpy.context.collection.objects.link(ko)
ko.location = (5, -4, 7)
ko.rotation_euler = (math.radians(38), 0, math.radians(40))

rim = bpy.data.lights.new("Rim", "AREA")
rim.energy = 320
rim.size = 4
rim.color = (1.0, 0.63, 0.28)          # ember rim, matching the brand
ro = bpy.data.objects.new("Rim", rim)
bpy.context.collection.objects.link(ro)
ro.location = (-5, 3.5, 3)
ro.rotation_euler = (math.radians(66), 0, math.radians(-125))

world = bpy.data.worlds.new("W")
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.02, 0.02, 0.025, 1)
bpy.context.scene.world = world

# ---------------------------------------------------------------- render
sc = bpy.context.scene
sc.render.engine = "CYCLES"
try:
    sc.cycles.device = "GPU"
    prefs = bpy.context.preferences.addons["cycles"].preferences
    prefs.compute_device_type = "OPTIX"
    prefs.get_devices()
    for d in prefs.devices:
        d.use = True
except Exception as e:
    print(f"[warn] GPU unavailable, falling back to CPU: {e}")
    sc.cycles.device = "CPU"
sc.cycles.samples = 256
sc.cycles.use_denoising = True
sc.render.resolution_x = 1400
sc.render.resolution_y = 1120
sc.render.film_transparent = False
sc.render.filepath = os.path.join(OUT, "hero")
sc.render.image_settings.file_format = "PNG"

import time
t0 = time.perf_counter()
bpy.ops.render.render(write_still=True)
print(f"[ok] hero rendered in {time.perf_counter() - t0:.1f}s -> {sc.render.filepath}.png")
