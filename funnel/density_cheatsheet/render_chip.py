"""Render the cover chip: ONE textured cube, alone, on a transparent film.

  blender --background --factory-startup --python funnel/density_cheatsheet/render_chip.py

Why a render and not a crop. The chip started as a crop of promo/density/
after.png, which is the THREE-cube measurement scene (3.2 m wall, 1.0 m, 0.38 m
cap - see density_shot.py). Round 3 of the design-critic loop traced the crop
rectangle back to that source and found an opaque slice of the 3.2 m wall
surviving behind the crate: the hero image of a sheet about sizing each object
correctly was fusing the 16 px reference and the 128 px reference into one
indistinct silhouette. Keying cannot fix that - the wall is not the backdrop.

So the object is rendered alone. Same tile, same Closest interpolation, same
nearest-neighbour discipline as the product; film transparency means there is
no backdrop to key and no fringe to erode.
"""
import math
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(bpy.data.filepath or __file__))
if "--" in sys.argv:
    HERE = sys.argv[sys.argv.index("--") + 1]
TEXEL = os.path.dirname(os.path.dirname(HERE))
TILE = os.path.join(TEXEL, "store", "tile_blockwall_32.png")
OUT = os.path.join(HERE, "chip_render.png")

for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)

# --- the object: one default cube, the same 1.0 m prop from the density scene
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
cube = bpy.context.active_object
cube.rotation_euler = (0, 0, math.radians(28))

img = bpy.data.images.load(TILE)
mat = bpy.data.materials.new("Pixel")
mat.use_nodes = True
nt = mat.node_tree
bsdf = nt.nodes["Principled BSDF"]
tex = nt.nodes.new("ShaderNodeTexImage")
tex.image = img
tex.interpolation = "Closest"            # the whole point; never Linear
tex.location = (-400, 200)
nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
bsdf.inputs["Roughness"].default_value = 0.92
bsdf.inputs["Specular IOR Level"].default_value = 0.18
cube.data.materials.append(mat)

# --- lighting: a warm key and a cool fill, so the cube reads as lit geometry
# rather than as a flat sprite. Matches the ember/charcoal card it sits on.
key = bpy.data.lights.new("Key", "AREA")
key.energy, key.size = 340.0, 3.4
key.color = (1.0, 0.86, 0.68)
ko = bpy.data.objects.new("Key", key)
ko.location = (2.9, -2.6, 3.3)
ko.rotation_euler = (math.radians(45), 0, math.radians(46))
bpy.context.collection.objects.link(ko)

fill = bpy.data.lights.new("Fill", "AREA")
fill.energy, fill.size = 70.0, 4.0
fill.color = (0.66, 0.74, 1.0)
fo = bpy.data.objects.new("Fill", fill)
fo.location = (-3.1, -1.9, 1.1)
fo.rotation_euler = (math.radians(78), 0, math.radians(-58))
bpy.context.collection.objects.link(fo)

# --- camera: three-quarter, orthographic so the cube fills the square frame
# predictably and no perspective skews the texel grid.
cam_d = bpy.data.cameras.new("Cam")
cam_d.type = "ORTHO"
cam_d.ortho_scale = 1.95            # cube + margin; 1.72 clipped its top edge
cam = bpy.data.objects.new("Cam", cam_d)
cam.location = (2.6, -2.6, 2.0)
bpy.context.collection.objects.link(cam)
bpy.context.scene.camera = cam

# Aim it rather than trusting hand-set Euler angles - the first pass put the
# cube 80px above centre because the angles only approximated "looking at the
# origin". A TRACK_TO on an empty at the origin cannot be approximately right.
target = bpy.data.objects.new("Target", None)
target.location = (0, 0, 0)
bpy.context.collection.objects.link(target)
con = cam.constraints.new("TRACK_TO")
con.target = target
con.track_axis = "TRACK_NEGATIVE_Z"
con.up_axis = "UP_Y"

sc = bpy.context.scene
sc.render.engine = "CYCLES"
sc.cycles.samples = 256
sc.cycles.use_denoising = True
sc.render.film_transparent = True                 # no backdrop, so nothing to key
sc.render.resolution_x = sc.render.resolution_y = 624       # 2x the 312 chip
sc.render.image_settings.file_format = "PNG"
sc.render.image_settings.color_mode = "RGBA"
sc.render.filepath = OUT
sc.view_settings.view_transform = "Standard"      # Filmic would mute the palette

try:
    sc.cycles.device = "GPU"
    prefs = bpy.context.preferences.addons["cycles"].preferences
    prefs.get_devices()
    for dev in prefs.devices:
        dev.use = dev.type != "CPU"
except Exception as exc:                                    # CPU is fine, just slower
    print("chip: GPU unavailable (%s), rendering on CPU" % exc)

bpy.ops.render.render(write_still=True)
print("chip: wrote", OUT)
