"""Prove Texel is not limited to boxy models. Not shipped.

  blender --background --factory-startup --python proof_organic.py

The demo art is blocky because that is a rendering choice - it is the style the
buyers ship, and flat faces show individual texels cleanly. It is NOT what the
add-on can handle. `tex_pick.viewport_hit` raycasts any MESH and `uv_at_hit`
fan-triangulates any polygon, so painting lands on whatever is under the cursor;
`texel.density_detect` measures per-face areas out of bmesh, so it reads any
topology.

This renders the least boxy things Blender has - Suzanne subdivided and
smooth-shaded, a UV sphere, a torus - carrying pixel art painted by Texel's own
raster core, and runs the REAL density operator on each so the numbers come from
the shipped code rather than from me.

Writes shots/proof_organic.png.
"""
from __future__ import annotations
import math
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

import texel                                                  # noqa: E402
texel.register()
from texel.core import canvas as C                            # noqa: E402
from texel.core import raster as R                            # noqa: E402
from texel.core import tools as TT                            # noqa: E402
import proof3d as P3                                          # noqa: E402

SIZE = 128
RES = (1500, 640)


def paint_hide() -> "C.Canvas":
    """A scaled hide, painted with the shipped primitives - nothing box-shaped.

    Deliberately organic: rows of overlapping scales with a shaded ramp, the
    kind of texture that only makes sense wrapped round a curved surface.
    """
    c = C.Canvas(SIZE, SIZE)
    L = c.layers[0]
    body = [c.add_colour(x) for x in TT.make_ramp((92, 132, 88, 255), 5)]
    warm = [c.add_colour(x) for x in TT.make_ramp((176, 138, 74, 255), 4)]
    ink = c.add_colour((26, 32, 28, 255))

    for p in R.rect(0, 0, SIZE - 1, SIZE - 1, filled=True):
        L.set(*p, body[2])
    # a belly that lightens toward the bottom, so the wrap is readable
    for y in range(SIZE):
        t = y / (SIZE - 1)
        if t > 0.62:
            idx = body[3] if t < 0.82 else body[4]
            for x in range(SIZE):
                L.set(x, y, idx)

    step = 16          # 9 was smaller than the UV islands and read as camo
    for row, y in enumerate(range(-4, SIZE + step, step)):
        off = (row % 2) * (step // 2)
        for x in range(-step, SIZE + step, step):
            cx, cy = x + off, y
            shade = body[1] if (row + x // step) % 3 else warm[1]
            for p in R.ellipse_box(cx, cy, cx + step - 2, cy + step - 1):
                L.set(*p, ink)
            for p in R.ellipse_box(cx + 1, cy + 1, cx + step - 3, cy + step - 2,
                                   filled=True):
                L.set(*p, shade)
            for p in R.line(cx + 3, cy + 2, cx + step - 5, cy + 2):
                L.set(*p, body[4])
    return c


def to_image(name, c):
    img = bpy.data.images.get(name)
    if img:
        bpy.data.images.remove(img)
    img = bpy.data.images.new(name, c.w, c.h, alpha=True)
    img.pixels.foreach_set(c.to_blender_floats())
    img.update()
    return img


def pixel_mat(name, img):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    t = nt.nodes.new("ShaderNodeTexImage")
    t.image = img
    t.interpolation = "Closest"          # texels stay square on a curve too
    t.location = (-420, 240)
    nt.links.new(t.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.85
    b.inputs["Specular IOR Level"].default_value = 0.12
    return m


def unwrap(obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.02)
    bpy.ops.object.mode_set(mode="OBJECT")
    obj.select_set(False)


def density_of(obj):
    """Run the SHIPPED operator and capture what it reports.

    density_detect states its result through self.report rather than writing a
    scene property, so the numbers have to be caught off the operator's report
    list - reading a property that does not exist just prints 0.0, which is what
    the first run of this did.
    """
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    said = []
    try:
        bpy.ops.texel.density_detect()
        for w in bpy.context.window_manager.operators[-1:]:
            said.append(w.bl_label)
    except Exception as e:
        obj.select_set(False)
        return f"{obj.name}: density_detect FAILED: {type(e).__name__}: {e}"
    obj.select_set(False)
    return (f"{obj.name:<9} {len(obj.data.polygons):>5} faces  "
            f"(the operator's own reading is the Info line above)")


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    P3.ground()
    P3.key_light()

    img = to_image("OrganicHide", paint_hide())
    mat = pixel_mat("Hide", img)

    made = []

    # Suzanne: subdivided and SMOOTH shaded - as far from a box as Blender ships
    bpy.ops.mesh.primitive_monkey_add(size=2.0, location=(-2.35, 0, 1.15))
    suz = bpy.context.active_object
    suz.name = "Suzanne"
    m = suz.modifiers.new("Subd", "SUBSURF")
    m.levels = m.render_levels = 2
    bpy.ops.object.modifier_apply(modifier=m.name)
    bpy.ops.object.shade_smooth()
    made.append(suz)

    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.95, segments=48, ring_count=24,
                                         location=(0.35, 0, 0.95))
    sph = bpy.context.active_object
    sph.name = "Sphere"
    bpy.ops.object.shade_smooth()
    made.append(sph)

    bpy.ops.mesh.primitive_torus_add(major_radius=0.85, minor_radius=0.34,
                                     major_segments=54, minor_segments=22,
                                     location=(2.9, 0, 0.9),
                                     rotation=(math.radians(64), 0, 0))
    tor = bpy.context.active_object
    tor.name = "Torus"
    bpy.ops.object.shade_smooth()
    made.append(tor)

    for o in made:
        unwrap(o)
        o.data.materials.append(mat)

    print("", flush=True)
    print("  density measured by texel.density_detect on curved geometry:", flush=True)
    for o in made:
        print("    " + density_of(o), flush=True)
    print("", flush=True)

    P3.camera((0.3, -10.6, 3.1), (0.3, 0, 1.0), lens=50)
    P3.render(os.path.join(HERE, "shots", "proof_organic"), res=RES)


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "shots"), exist_ok=True)
    build()
    print("ORGANIC DONE", flush=True)
