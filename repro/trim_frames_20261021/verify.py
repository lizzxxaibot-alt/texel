"""T-024 read-back: Trim to Content on an animation, run through the real
operator in a ZIP (not the tree). 3 frames, onion skin off and on, Trim run
with each frame current. Asserts no frame loses an opaque texel and the
frames keep their offsets to each other.

  TEXEL_ZIP=dist/texel-0.2.5.zip blender --background --factory-startup --python verify.py
"""
import os, sys, zipfile, tempfile
import bpy

ZIP = os.environ["TEXEL_ZIP"]
EXT = tempfile.mkdtemp(prefix="texel_trim_")
zipfile.ZipFile(ZIP).extractall(EXT)
sys.path.insert(0, EXT)
import texel
texel.register()
from texel import tex_doc
from texel.core import raster as R
print(f"[env] blender {bpy.app.version_string}  zip {os.path.basename(ZIP)}  from {texel.__file__}")

fails = []
BOXES = [(2, 2, 12, 12), (5, 5, 15, 15), (40, 40, 60, 60)]

def opaque(layer):
    return sum(1 for v in layer.px if v)

def run(onion, show):
    tag = f"onion={'on ' if onion else 'off'} frame {show + 1} current"
    img = bpy.data.images.new(f"T_{onion}_{show}", 64, 64, alpha=True)
    img.pixels.foreach_set([0.0] * (64 * 64 * 4)); img.update()
    area = bpy.context.screen.areas[0]
    area.type = "IMAGE_EDITOR"
    area.spaces.active.image = img
    region = next(r for r in area.regions if r.type == "WINDOW")
    ctx = dict(area=area, region=region, space_data=area.spaces.active,
               screen=bpy.context.screen, window=bpy.context.window)
    doc = tex_doc.get(img)
    c = doc.canvas
    col = c.add_colour((200, 40, 40, 255))
    with bpy.context.temp_override(**ctx):
        for _ in BOXES:
            bpy.ops.texel.frame_add(copy_previous=False)
        bpy.context.scene.texel.onion_skin = onion
        for f, box in enumerate(BOXES):
            L = c.cel("Main", f)
            for x, y in R.rect(*box, filled=True):
                L.set(x, y, col)
        bpy.ops.texel.frame_show(index=show)
        doc.flush()
        vis = [l.visible for l in c.layers]
        before = [opaque(c.cel("Main", f)) for f in range(c.frame_count())]
        r = bpy.ops.texel.trim(margin=0)
        after = [opaque(c.cel("Main", f)) for f in range(c.frame_count())]
        b1 = [c.cel("Main", f).bounds() for f in range(c.frame_count())]
    o = b1[0] or (0, 0)
    offs = [(b[0] - o[0], b[1] - o[1]) if b else None for b in b1]
    ok = (after == before and offs == [(0, 0), (3, 3), (38, 38)]
          and r == {"FINISHED"})
    print(f"[{'ok' if ok else 'FAIL'}] {tag}: visible {vis} trim {r} canvas {c.w}x{c.h} "
          f"opaque {before} -> {after} offsets {offs}")
    if not ok:
        fails.append(tag)

for onion in (False, True):
    for show in range(3):
        run(onion, show)
print(f"{len(fails)} FAILED: {fails}" if fails else "TRIM FRAMES: ALL PASS")
