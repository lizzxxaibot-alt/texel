"""Animation: timeline binding, per-frame holds, GIF and JSON export.

  blender --background --factory-startup --python test_anim.py
"""
import json
import os
import shutil
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
from texel import tex_doc
from texel.core import raster as R
from texel.tex_anim import _BOUND, _on_frame, frame_at, holds_of

print(f"[info] Blender {bpy.app.version_string}")
s = bpy.context.scene.texel

for idname in ("anim_bind", "anim_unbind", "anim_play", "frame_hold",
               "export_gif", "export_anim_data"):
    check(f"operator texel.{idname} registered", hasattr(bpy.ops.texel, idname))

bpy.ops.texel.canvas_new(size=8, name="Anim")
img = bpy.data.images["Anim"]
area = bpy.context.screen.areas[0]
area.type = "IMAGE_EDITOR"
area.spaces.active.image = img
region = next(r for r in area.regions if r.type == "WINDOW")
ctx = dict(area=area, region=region, space_data=area.spaces.active,
           screen=bpy.context.screen, window=bpy.context.window)
doc = tex_doc.get(img)
c = doc.canvas

with bpy.context.temp_override(**ctx):
    check("bind refuses with no frames", not bpy.ops.texel.anim_bind.poll())

    # three frames, each a different colour, PLUS a second track so the test
    # proves a frame carries more than one drawing through playback
    cols = [c.add_colour(x) for x in ((255, 0, 0, 255), (0, 255, 0, 255), (0, 0, 255, 255))]
    for i in range(3):
        bpy.ops.texel.frame_add(copy_previous=False)
        for x, y in R.rect(0, 0, 7, 7, filled=True):
            c.layers[c.active].set(x, y, cols[i])
    check("three frames exist", c.frame_count() == 3, c.frame_count())
    bpy.ops.texel.track_add(name="BG")
    check("a second track spans every frame",
          all(c.cel("BG", f) is not None for f in range(3)))

    # ---- holds default to 1 each
    holds = holds_of(c, 3)
    check("holds default to one each", holds == [1, 1, 1], holds)

    # ---- frame_at maps a timeline frame to a drawing, and loops
    got = [frame_at(c, n) for n in range(1, 8)]
    check("frame_at walks then loops", got == [0, 1, 2, 0, 1, 2, 0], got)

    # ---- holds change the mapping and the timeline length
    check("frame_hold sets a hold",
          bpy.ops.texel.frame_hold(index=1, hold=3) == {"FINISHED"})
    check("hold stored", holds_of(c, 3) == [1, 3, 1], holds_of(c, 3))
    got = [frame_at(c, n) for n in range(1, 7)]
    check("a held frame occupies three timeline frames",
          got == [0, 1, 1, 1, 2, 0], got)

    # ---- binding drives the timeline
    check("bind succeeds", bpy.ops.texel.anim_bind() == {"FINISHED"})
    check("bound to this image", _BOUND["image"] == "Anim", _BOUND["image"])
    sc = bpy.context.scene
    check("frame_start is 1", sc.frame_start == 1)
    check("frame_end matches the total hold", sc.frame_end == 5, sc.frame_end)
    check("handler installed", _on_frame in bpy.app.handlers.frame_change_post)
    print(f"[info] {s.status}")

    # ---- scrubbing actually swaps which frame is visible
    def visible_index():
        return sorted({l.frame for l in c.layers
                       if l.visible and l.frame is not None})
    for blender_frame, want in ((1, 0), (2, 1), (3, 1), (4, 1), (5, 2)):
        sc.frame_current = blender_frame
        _on_frame(sc)
        check(f"timeline frame {blender_frame} shows drawing {want + 1}",
              visible_index() == [want], visible_index())
    check("exactly one frame visible at a time", len(visible_index()) == 1)
    check("BOTH tracks of that frame are visible",
          len([l for l in c.layers if l.visible and l.frame == visible_index()[0]]) == 2)

    # the visible frame must be fully opaque even if onion skin left it ghosted
    c.cel("Main", 0).opacity = 0.3
    sc.frame_current = 1
    _on_frame(sc)
    check("bound playback restores full opacity", c.cel("Main", 0).opacity == 1.0)

    # ---- pixels really change in the Blender image, not just the model
    buf = [0.0] * (8 * 8 * 4)
    sc.frame_current = 1
    _on_frame(sc)
    img.pixels.foreach_get(buf)
    first = tuple(round(v * 255) for v in buf[:4])
    sc.frame_current = 5
    _on_frame(sc)
    img.pixels.foreach_get(buf)
    last = tuple(round(v * 255) for v in buf[:4])
    check("the image content changes with the timeline", first != last, (first, last))

    # ---- export sheet + JSON with timing
    tmp = tempfile.mkdtemp(prefix="texel_anim_")
    check("export_anim_data runs",
          bpy.ops.texel.export_anim_data(columns=3, directory=tmp) == {"FINISHED"})
    jpath = os.path.join(tmp, "Anim_anim.json")
    check("json written", os.path.exists(jpath))
    if os.path.exists(jpath):
        data = json.load(open(jpath, encoding="utf-8"))
        check("json lists every frame", len(data["frames"]) == 3, len(data["frames"]))
        check("json carries the holds", [f["hold"] for f in data["frames"]] == [1, 3, 1],
              [f["hold"] for f in data["frames"]])
        check("json carries durations in ms",
              all(f["duration_ms"] > 0 for f in data["frames"]),
              [f["duration_ms"] for f in data["frames"]])
        check("json frame rects tile across the sheet",
              [f["x"] for f in data["frames"]] == [0, 8, 16],
              [f["x"] for f in data["frames"]])
        check("json records fps", data["fps"] == bpy.context.scene.render.fps)
    check("sheet png written", os.path.exists(os.path.join(tmp, "Anim_sheet.png")))

    # ---- GIF, only if ffmpeg is present; the operator must say so if not
    if shutil.which("ffmpeg"):
        check("export_gif runs",
              bpy.ops.texel.export_gif(scale=2, directory=tmp) == {"FINISHED"})
        gif = os.path.join(tmp, "Anim.gif")
        check("gif written", os.path.exists(gif) and os.path.getsize(gif) > 100)
        check("gif temp folder cleaned up",
              not os.path.exists(os.path.join(tmp, "_texel_gif")))
        print(f"[info] {s.status}")
    else:
        print("[info] ffmpeg absent - GIF path not exercised")
    check("layer visibility restored after export",
          len({l.frame for l in c.layers if l.visible and l.frame is not None}) == 1)

    # ---- unbind removes the handler
    check("unbind succeeds", bpy.ops.texel.anim_unbind() == {"FINISHED"})
    check("handler removed", _on_frame not in bpy.app.handlers.frame_change_post)
    check("binding cleared", _BOUND["image"] is None)
    check("unbind twice is harmless", bpy.ops.texel.anim_unbind() == {"FINISHED"})

    shutil.rmtree(tmp, ignore_errors=True)

# unregister must never leave a handler behind
bpy.ops.texel.anim_bind.poll()
texel.unregister()
check("unregister leaves no frame handler",
      _on_frame not in bpy.app.handlers.frame_change_post)

print()
if fails:
    print(f"{len(fails)} FAILED: {fails}")
    sys.exit(1)
print("TEXEL ANIM: ALL PASS")
