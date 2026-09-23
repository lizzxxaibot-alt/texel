"""Phase 5: a GENUINELY fresh Blender process opens the packed .blend written by
phase 3. No simulation of a new session - this IS one.

Question: after reopening, does the add-on's own re-entry path give you back your
art, or a blank canvas that will overwrite it on the next flush?
"""
import os, sys
import bpy

WORK = os.environ["TEXEL_WORK"]
sys.path.insert(0, os.path.join(WORK, "addon"))
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
    print(f"[{tag}] red={counts.get(RED,0)} distinct={len(counts)} "
          f"top={sorted(counts.items(), key=lambda kv:-kv[1])[:2]}", flush=True)
    return counts.get(RED, 0)

bpy.ops.wm.open_mainfile(filepath=os.path.join(WORK, "packed.blend"))
img = bpy.data.images["Pixel Cube Texture"]
print(f"[env] blender {bpy.app.version_string}  _DOCS at process start = {len(tex_doc._DOCS)}")
print(f"[reopen] source={img.source} packed={bool(img.packed_file)}")
a = census(img, "A reopened")

# the state every re-entry operator finds: pick_texture/show_canvas/paint all
# call tex_doc.get(img) with create=True
before = tex_doc.get(img, create=False)
print(f"[B] tex_doc.get(create=False) -> {before!r}   (None = no doc in this session)")
d = tex_doc.get(img)                       # what show_canvas/pick_texture/paint do
nz = sum(1 for v in d.canvas.layers[0].px if v)
print(f"[B] canvas handed to the tools: {d.canvas.w}x{d.canvas.h} "
      f"palette={len(d.canvas.palette)} nonzero_px={nz}")

d.flush()                                  # any edit ends here (tex_doc.flush)
b = census(img, "C after one flush")
print(f"RESULT reopen_red={a} doc_nonzero={nz} after_flush_red={b}")
print("PHASE5_OK")
