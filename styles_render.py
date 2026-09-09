"""Render one character per art style, each on transparency. Not shipped.

  blender --background --factory-startup --python styles_render.py -- <style>
  blender --background --factory-startup --python styles_render.py        (all)

Each style renders alone, framed from its own published height, on a transparent
background, so the labelled comparison sheet can be laid out in HTML afterwards
rather than fought with inside Blender. Writes shots/style_<name>.png.

The point of the set: Texel does not care what the geometry is. Showing one
style implies it only does that style, which is the objection the blocky demos
kept raising.
"""
from __future__ import annotations
import math
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import models3d as M                                          # noqa: E402
import proof3d as P3                                          # noqa: E402

RES = (760, 1000)
SAMPLES = 260


def light():
    """Softer and more even than the prop lighting: these are compared side by
    side, so a dramatic key would read as a style difference rather than a
    lighting one."""
    for name, loc, energy, size, col in (
            ("Key",  (-3.4, -4.2, 5.6), 320, 4.2, (1.0, 0.95, 0.88)),
            ("Fill", (4.2, -3.4, 2.8), 130, 5.0, (0.70, 0.79, 1.0)),
            ("Rim",  (1.4, 4.6, 4.2), 280, 2.6, (1.0, 0.74, 0.44))):
        d = bpy.data.lights.new(name, "AREA")
        d.energy, d.size, d.color = energy, size, col
        o = bpy.data.objects.new(name, d)
        o.location = loc
        o.visible_camera = False
        bpy.context.collection.objects.link(o)
        P3.aim(o, (0, 0, 0.9))


def torch_in_hand(ch, scale=0.85):
    """Same prop for every style, so the comparison is about the character."""
    if "texel_hand" not in ch.keys():
        return
    hx, hy, hz = ch["texel_hand"]
    t = M.prop("torch")
    t.parent = ch
    t.location = (hx, hy, hz - 0.34)
    fl = M.flame("Flame", scale=scale)
    fl.parent = ch
    fl.location = (hx, hy, hz + 0.70)
    li = bpy.data.lights.new("Fire", "POINT")
    li.energy, li.color, li.shadow_soft_size = 150, (1.0, 0.62, 0.28), 0.28
    lo = bpy.data.objects.new("Fire", li)
    lo.parent = ch
    lo.location = (hx, hy, hz + 0.78)
    bpy.context.collection.objects.link(lo)


def shot(name, builder, turn=22, lift=0.0, pad=1.45):
    """Build one style and frame it from its own height, on transparency."""
    P3.reset()
    light()
    ch = builder()
    ch.rotation_euler = (0, 0, math.radians(turn))
    torch_in_hand(ch)

    # frame from the object's real bounds, not a guessed camera position - the
    # styles are different heights and a fixed camera crops some and shrinks
    # others, which would read as a style difference
    bpy.context.view_layer.update()
    zs, xs = [], []
    for o in bpy.data.objects:
        if o.type != "MESH":
            continue
        for c in o.bound_box:
            w = o.matrix_world @ __import__("mathutils").Vector(c)
            zs.append(w.z); xs.append(w.x)
    top, bot = max(zs), min(zs)
    height = max(top - bot, 0.4) * pad
    mid = (top + bot) / 2.0 + lift

    aspect = RES[0] / RES[1]
    lens = 58.0
    vfov = 2.0 * math.atan((36.0 / max(aspect, 1e-6) / 2.0) / lens) if aspect < 1 \
        else 2.0 * math.atan(18.0 / lens)
    dist = (height / 2.0) / math.tan(vfov / 2.0)
    # aim dead at the middle of the bounds: offsetting the camera up pushed the
    # subject low and clipped the hem on the taller styles
    cam = P3.camera((-dist * 0.26, -dist * 0.95, mid + height * 0.02),
                    (0, 0, mid), lens=lens)

    sc = bpy.context.scene
    sc.render.film_transparent = True
    P3.render(os.path.join(HERE, "shots", f"style_{name}"), res=RES)
    sc.render.film_transparent = False
    return cam


# style key -> (builder, turn, note). Filled in once the five are decided.
STYLES = {
    "voxel": (M.character, 24),
    "lowpoly": (M.character_hooded, -20),
}


def main():
    args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    want = args or list(STYLES)
    os.makedirs(os.path.join(HERE, "shots"), exist_ok=True)
    for key in want:
        if key not in STYLES:
            print(f"  ! unknown style {key!r}; have {sorted(STYLES)}", flush=True)
            continue
        builder, turn = STYLES[key][0], STYLES[key][1]
        print(f"  {key}", flush=True)
        shot(key, builder, turn=turn)
    print("STYLES RENDER DONE", flush=True)


if __name__ == "__main__":
    main()
