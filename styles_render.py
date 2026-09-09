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
import styles3d as S                                          # noqa: E402
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


# far enough back for the raised torch AND the flame above it: the first
# fixed camera framed the body and guillotined every torch
CAM = (-1.35, -5.25, 2.05)
LOOK = (0.0, 0.0, 1.52)
LENS = 58.0


def shot(name, builder, turn=22, lift=0.0, pad=1.45, native=None, torch=True,
         face_camera=False):
    """Build one style and shoot it from a FIXED camera, on transparency.

    Framing from each object's own bounds made the styles different sizes on
    the sheet - the one without a torch got blown up to fill the frame - and a
    size difference reads as a style difference. Every character is built to
    about the same height, so one camera serves all five and the comparison is
    about the art.
    """
    P3.reset()
    light()
    ch = builder()
    if face_camera:
        # a billboard is a plane. Off-axis it renders as a LINE, which is what
        # the first sheet showed. Turn it to face the camera, which is what a
        # billboard does every frame in an actual game.
        turn = math.degrees(math.atan2(CAM[0], -CAM[1]))
    ch.rotation_euler = (0, 0, math.radians(turn))
    if torch:
        torch_in_hand(ch)

    P3.camera(CAM, LOOK, lens=LENS)

    # A style whose look IS its output resolution gets rendered at that
    # resolution. Upscaling happens afterwards, nearest, so the pixels stay
    # square - which is the whole PS1 signature.
    #
    # Transparency has to be passed THROUGH: proof3d.render set
    # film_transparent = False itself, so setting it here was overwritten and
    # every "transparent" render came out with an opaque world behind it.
    P3.render(os.path.join(HERE, "shots", f"style_{name}"), res=native or RES,
              transparent=True)


# The five styles this audience actually ships, ranked by itch.io tag counts
# pulled 2026-09-09. `native` is the resolution the style is rendered AT before
# being upscaled - a PS1 output 320x240 and nothing about that is optional if
# the look is going to be honest.
STYLES = {
    "psx":       dict(build=S.psx, turn=24, native=(256, 337), torch=True,
                      degrade=True),
    "voxel":     dict(build=S.voxel, turn=26, native=None, torch=False),
    # billboard has its torch drawn into the sprite, and must face the lens
    "billboard": dict(build=S.billboard, turn=0, native=None, torch=False,
                      face_camera=True),
    "lowpoly":   dict(build=S.lowpoly, turn=22, native=None, torch=True),
    "n64":       dict(build=S.n64, turn=-22, native=(456, 600), torch=True),
}


def main():
    args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    want = args or list(STYLES)
    os.makedirs(os.path.join(HERE, "shots"), exist_ok=True)
    for key in want:
        if key not in STYLES:
            print(f"  ! unknown style {key!r}; have {sorted(STYLES)}", flush=True)
            continue
        st = STYLES[key]
        print(f"  {key}", flush=True)
        shot(key, st["build"], turn=st["turn"], native=st.get("native"),
             torch=st.get("torch", True),
             face_camera=st.get("face_camera", False))
    print("STYLES RENDER DONE", flush=True)


if __name__ == "__main__":
    main()
