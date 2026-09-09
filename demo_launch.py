"""Open Blender with Texel loaded and a scene ready to paint on.

Not shipped to customers - this is the try-it-now harness. It registers the
add-on straight from the working tree (no install step), builds a textured cube,
splits the window so the canvas and the model are both visible, and leaves you
in the Texel sidebar tab.
"""
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import texel
texel.register()

# ---------------------------------------------------------------- clean scene
bpy.ops.wm.read_factory_settings(use_empty=True)

SIZE = 64
img = bpy.data.images.new("Texel Canvas", SIZE, SIZE, alpha=True)
img.pixels.foreach_set([0.0] * (SIZE * SIZE * 4))
img.update()

from texel import tex_doc
from texel.core import raster as R

doc = tex_doc.get(img)
# a faint grid so the canvas is not an intimidating void, and you can see the
# texel size immediately
faint = doc.canvas.add_colour((44, 44, 52, 255))
for n in range(0, SIZE, 8):
    for x, y in R.line(n, 0, n, SIZE - 1):
        doc.canvas.layers[0].set(x, y, faint)
    for x, y in R.line(0, n, SIZE - 1, n):
        doc.canvas.layers[0].set(x, y, faint)
doc.flush()

# ---------------------------------------------------------------- the model
bpy.ops.mesh.primitive_cube_add(size=2)
cube = bpy.context.active_object
cube.name = "Paint Me"
bpy.ops.object.shade_flat()

mat = bpy.data.materials.new("TexelDemo")
mat.use_nodes = True
nt = mat.node_tree
tex = nt.nodes.new("ShaderNodeTexImage")
tex.image = img
tex.interpolation = "Closest"          # pixels stay pixels
nt.links.new(tex.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"])
cube.data.materials.append(mat)

# a starting palette so there is something in the swatch grid
for rgba in ((242, 230, 200, 255), (255, 156, 63, 255), (231, 178, 58, 255),
             (96, 158, 84, 255), (58, 106, 66, 255), (132, 132, 140, 255),
             (122, 88, 58, 255), (20, 19, 23, 255)):
    doc.canvas.add_colour(rgba)
bpy.context.scene.texel.colour = (1.0, 0.61, 0.25, 1.0)

# ---------------------------------------------------------------- the layout
# split the main area so you see the flat canvas and the model at once
for window in bpy.context.window_manager.windows:
    screen = window.screen
    areas = [a for a in screen.areas if a.type == "VIEW_3D"]
    if not areas:
        continue
    v3d = areas[0]
    with bpy.context.temp_override(window=window, screen=screen, area=v3d):
        bpy.ops.screen.area_split(direction="VERTICAL", factor=0.42)
    left = min((a for a in screen.areas if a.type == "VIEW_3D"),
               key=lambda a: a.x)
    left.type = "IMAGE_EDITOR"
    left.spaces.active.image = img
    break

# open the N sidebar in both editors, on the Texel tab
for area in bpy.context.screen.areas:
    if area.type in {"IMAGE_EDITOR", "VIEW_3D"}:
        for space in area.spaces:
            if hasattr(space, "show_region_ui"):
                space.show_region_ui = True

print("=" * 62)
print("  TEXEL demo is open.")
print("  Left  = the 64x64 canvas.   Right = the cube it textures.")
print("  Press N for the sidebar, pick the 'Texel' tab, hit Paint.")
print("  Try a shallow freehand diagonal with Pixel Perfect ON, then OFF.")
print("=" * 62)
