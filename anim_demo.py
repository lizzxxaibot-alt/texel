"""Animate a sprite with the SHIPPED operators, then export it.

Every drawing goes through texel.frame_add / track_add / track_move /
frame_hold / export_gif - the same buttons a customer presses. What it proves is
the cel model: one frame carries FOUR drawings at once, and the flame and the
light it casts sit on their own tracks so they flicker on a different beat from
the walk, without the character being redrawn.

The artwork itself lives in demo_art.py, shared with the screen-capture video so
the two can never drift apart.

  blender --background --factory-startup --python anim_demo.py
"""
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

OUT = os.path.join(HERE, "promo", "anim")
os.makedirs(OUT, exist_ok=True)

import texel
from texel import tex_doc

texel.register()
import demo_art as A

FRAMES = 8


def main():
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)

    bpy.ops.texel.canvas_new(size=A.SIZE, name="Torchbearer")
    img = bpy.data.images["Torchbearer"]
    area = bpy.context.screen.areas[0]
    area.type = "IMAGE_EDITOR"
    area.spaces.active.image = img
    region = next(r for r in area.regions if r.type == "WINDOW")
    ctx = dict(area=area, region=region, space_data=area.spaces.active,
               screen=bpy.context.screen, window=bpy.context.window)
    doc = tex_doc.get(img)
    c = doc.canvas
    P = A.palette(c)

    with bpy.context.temp_override(**ctx):
        for _ in range(FRAMES):
            bpy.ops.texel.frame_add(copy_previous=False)
        bpy.ops.texel.track_add(name="Cave", bottom=True)   # behind everything
        bpy.ops.texel.track_add(name="Torch")               # in front
        bpy.ops.texel.track_add(name="Glow")
        for _ in range(2):                                  # slide it behind him
            bpy.ops.texel.track_move(name="Glow", delta=-1)
        assert c.tracks == list(A.TRACKS), c.tracks
        print(f"[demo] {c.frame_count()} frames x {c.tracks}", flush=True)

        for f in range(FRAMES):
            cels = {t: c.cel(t, f) for t in A.TRACKS}
            for t in A.TRACKS:
                c.active = c.layers.index(cels[t])
                A.DRAW[t](cels, P, f)

        # ---- timing: hold the two contact poses a beat longer
        for i, hold in enumerate((2, 1, 1, 1, 2, 1, 1, 1)):
            bpy.ops.texel.frame_hold(index=i, hold=hold)

        bpy.ops.texel.anim_bind()
        print(f"[demo] {bpy.context.scene.texel.status}", flush=True)

        bpy.context.scene.render.fps = 12
        bpy.ops.texel.export_gif(scale=6, directory=OUT)
        print(f"[demo] gif: {bpy.context.scene.texel.status}", flush=True)
        bpy.ops.texel.export_anim_data(columns=4, directory=OUT)
        print(f"[demo] sheet+json: {bpy.context.scene.texel.status}", flush=True)
        bpy.ops.texel.colour_count(limit=32)
        print(f"[demo] {bpy.context.scene.texel.status}", flush=True)

        for name, onion in (("torchbearer_frame.png", False),
                            ("torchbearer_onion.png", True)):
            c.show_frame(2, onion=onion)
            doc.flush()
            img.filepath_raw = os.path.join(OUT, name)
            img.file_format = "PNG"
            img.save()

    gif = os.path.join(OUT, "Torchbearer.gif")
    ok = os.path.exists(gif)
    print(f"TEXEL_ANIM_DEMO_DONE gif={'ok' if ok else 'MISSING'} "
          f"bytes={os.path.getsize(gif) if ok else 0} frames={FRAMES} "
          f"tracks={len(c.tracks)} cels={sum(1 for l in c.layers if l.frame is not None)} "
          f"colours={len(c.palette) - 1}", flush=True)


if __name__ == "__main__":
    main()
