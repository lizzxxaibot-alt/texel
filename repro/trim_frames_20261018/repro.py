"""Trim to Content on an animation: does it keep frames aligned, and does it
keep art on frames that are not the one on screen?  Runs the SHIPPED zip.

  TEXEL_ZIP=dist/texel-0.2.4.zip blender --background --factory-startup --python repro.py
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

def opaque(layer):
    return sum(1 for v in layer.px if v)

def run(tag, f0_box, f1_box, show, onion=True, f2_box=None):
    img = bpy.data.images.new(f"T_{tag}", 64, 64, alpha=True)
    img.pixels.foreach_set([0.0] * (64 * 64 * 4)); img.update()   # start transparent
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
        bpy.ops.texel.frame_add(copy_previous=False)   # seeds frame 0
        bpy.ops.texel.frame_add(copy_previous=False)   # frame 1
        if f2_box: bpy.ops.texel.frame_add(copy_previous=False)
        bpy.context.scene.texel.onion_skin = onion
        for f, box in [(0, f0_box), (1, f1_box)] + ([(2, f2_box)] if f2_box else []):
            L = c.cel("Main", f)
            for x, y in R.rect(*box, filled=True):
                L.set(x, y, col)
        bpy.ops.texel.frame_show(index=show)
        doc.flush()
        before = [opaque(c.cel("Main", f)) for f in range(c.frame_count())]
        b0 = [c.cel("Main", f).bounds() for f in range(c.frame_count())]
        vis = [(l.name, l.visible) for l in c.layers]
        r = bpy.ops.texel.trim(margin=0)
        after = [opaque(c.cel("Main", f)) for f in range(c.frame_count())]
        b1 = [c.cel("Main", f).bounds() for f in range(c.frame_count())]
    print(f"[{tag}] showing frame {show+1}; visible at trim {vis}; trim -> {r}; canvas {c.w}x{c.h}")
    print(f"[{tag}] opaque before {before}  after {after}  LOST {[a-b for a,b in zip(before,after)]}")
    print(f"[{tag}] bounds before {b0}  after {b1}")
    d0 = (b0[1][0]-b0[0][0], b0[1][1]-b0[0][1]); d1 = (b1[1][0]-b1[0][0], b1[1][1]-b1[0][1]) if b1[1] else None
    print(f"[{tag}] frame2-minus-frame1 offset before {d0} after {d1}  ALIGNED={d0==d1}")

# A: frame 2 is tighter than frame 1 (the asker's case), frame 1 on screen
run("A_f2_tighter_show1", (10, 10, 40, 50), (20, 20, 30, 40), show=0)
# B: same art, frame 2 on screen - frame 1 extends past frame 2's box
run("B_f2_tighter_show2", (10, 10, 40, 50), (20, 20, 30, 40), show=1)
# C: the two frames do not overlap at all
run("C_disjoint_show1", (2, 2, 12, 12), (40, 40, 60, 60), show=0)
# D: onion skin OFF, frames disjoint, frame 1 on screen
run("D_onion_off_show1", (2, 2, 12, 12), (40, 40, 60, 60), show=0, onion=False)
# E: onion ON (default), three frames, frame 3 not adjacent to the frame on screen
run("E_3frames_show1", (2, 2, 12, 12), (5, 5, 15, 15), show=0, f2_box=(40, 40, 60, 60))
print("REPRO_DONE")
