"""Phase 2: reopen the .blend in a FRESH Blender with the same shipped zip.

Two questions, measured separately:
  A. does the painted texture survive the save/reopen at all?
  B. what does the FIRST Texel brush stroke after reopening do to it?
"""
import os, sys, zipfile
import bpy

WORK = os.environ["TEXEL_WORK"]
EXT  = os.path.join(WORK, "addon")
sys.path.insert(0, EXT)

import texel
texel.register()
from texel import tex_doc

blend = os.path.join(WORK, "painted.blend")
bpy.ops.wm.open_mainfile(filepath=blend)

img = bpy.data.images["Pixel Cube Texture"]
W = H = 32

def opaque(tag):
    buf = [0.0] * (W * H * 4)
    img.pixels.foreach_get(buf)
    n = sum(1 for i in range(W * H) if buf[i * 4 + 3] > 0.5)
    print(f"[{tag}] opaque texels: {n}")
    return n

print(f"[env] blender {bpy.app.version_string}")
print(f"[reopen] image '{img.name}' source={img.source} packed={bool(img.packed_file)} "
      f"filepath={img.filepath!r} has_data={img.has_data}")

a = opaque("A/reopen")

# --- B: exactly what texel.paint does on its first stroke (tex_paint.py:84,76)
existing = tex_doc.get(img, create=False)
print(f"[B] tex_doc.get(create=False) after reopen -> {existing!r}")
d = tex_doc.get(img)                       # tex_paint.py:84
print(f"[B] fresh Doc canvas palette size={len(d.canvas.palette)} "
      f"nonzero px={sum(1 for v in d.canvas.layers[0].px if v)}")
c = d.canvas
c.layers[c.active].set(0, 0, c.add_colour((0, 255, 0, 255)))   # one stroke
d.flush()                                                       # tex_paint.py:76
b = opaque("B/after-one-stroke")

print(f"RESULT A_reopen={a} B_after_stroke={b}")
print("PHASE2_OK")
