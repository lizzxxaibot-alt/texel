"""Phase 3: same cycle, but the user does the standard Blender mitigation
(Image > Pack) before saving - the exact tip our own account posted on 09-21.

Measured by COLOUR, not by alpha, so 'regenerated black' cannot read as 'survived'.
"""
import os, sys, zipfile
import bpy

WORK = os.environ["TEXEL_WORK"]
EXT  = os.path.join(WORK, "addon")
sys.path.insert(0, EXT)
import texel; texel.register()
from texel import tex_doc

W = H = 32
RED = (255, 0, 0, 255)

def census(img, tag):
    buf = [0.0] * (W * H * 4)
    img.pixels.foreach_get(buf)
    counts = {}
    for i in range(W * H):
        o = i * 4
        k = tuple(round(buf[o + j] * 255) for j in range(4))
        counts[k] = counts.get(k, 0) + 1
    red = counts.get(RED, 0)
    top = sorted(counts.items(), key=lambda kv: -kv[1])[:3]
    print(f"[{tag}] red={red}  distinct={len(counts)}  top={top}")
    return red

for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)

bpy.ops.texel.add_cube(size=1.0, texture=32)
img = bpy.data.images["Pixel Cube Texture"]
d = tex_doc.get(img); c = d.canvas; L = c.layers[c.active]
ri = c.add_colour(RED)
for y in range(8, 24):
    for x in range(8, 24):
        L.set(x, y, ri)
d.flush()
census(img, "painted")

img.pack()                                   # Image > Pack, the standard fix
print(f"[pack] packed={bool(img.packed_file)} source={img.source}")

blend = os.path.join(WORK, "packed.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend)
bpy.ops.wm.open_mainfile(filepath=blend)     # genuine reopen

img = bpy.data.images["Pixel Cube Texture"]
print(f"[reopen] source={img.source} packed={bool(img.packed_file)} has_data={img.has_data}")
a = census(img, "A/reopen-packed")

tex_doc.clear()                              # a fresh session has no _DOCS
print(f"[B] get(create=False) -> {tex_doc.get(img, create=False)!r}")
d = tex_doc.get(img)                         # tex_paint.py:84, first brush stroke
c = d.canvas
c.layers[c.active].set(0, 0, c.add_colour((0, 255, 0, 255)))
d.flush()                                    # tex_paint.py:76
b = census(img, "B/after-one-stroke")

print(f"RESULT packed_reopen_red={a} packed_after_stroke_red={b}")
print("PHASE3_OK")
