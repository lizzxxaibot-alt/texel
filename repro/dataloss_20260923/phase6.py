"""Phase 6: is the fix already in the file? Fresh process, packed .blend, but
call the load_from_image() that tex_doc.py already ships and get() never uses.
"""
import os, sys
import bpy
WORK = os.environ["TEXEL_WORK"]
sys.path.insert(0, os.path.join(WORK, "addon"))
import texel; texel.register()
from texel import tex_doc

W=H=32; RED=(255,0,0,255)
def census(img, tag):
    buf=[0.0]*(W*H*4); img.pixels.foreach_get(buf)
    c={}
    for i in range(W*H):
        o=i*4; k=tuple(round(buf[o+j]*255) for j in range(4)); c[k]=c.get(k,0)+1
    print(f"[{tag}] red={c.get(RED,0)} distinct={len(c)}", flush=True); return c.get(RED,0)

bpy.ops.wm.open_mainfile(filepath=os.path.join(WORK,"packed.blend"))
img=bpy.data.images["Pixel Cube Texture"]
census(img,"reopened")
d=tex_doc.get(img)
print(f"[as-shipped] doc nonzero_px={sum(1 for v in d.canvas.layers[0].px if v)}")
d.load_from_image()                       # the method that exists and is unused
print(f"[after load_from_image] doc nonzero_px={sum(1 for v in d.canvas.layers[0].px if v)} "
      f"palette={len(d.canvas.palette)}")
d.flush()
r=census(img,"after flush WITH rehydrate")
print(f"RESULT rehydrated_red={r}")
print("PHASE6_OK")
