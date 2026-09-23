"""Phase 1: paint with the SHIPPED zip, save the .blend, report what is on the canvas."""
import os, sys, zipfile, tempfile
import bpy

ZIP  = os.environ["TEXEL_ZIP"]
WORK = os.environ["TEXEL_WORK"]
EXT  = os.path.join(WORK, "addon")

if not os.path.isdir(EXT):
    os.makedirs(EXT, exist_ok=True)
    zipfile.ZipFile(ZIP).extractall(EXT)
sys.path.insert(0, EXT)

import texel
texel.register()
from texel import tex_doc

print(f"[env] blender {bpy.app.version_string}")
print(f"[env] zip     {os.path.basename(ZIP)}")

# clean scene
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)

# the add-on's own entry-point operator
bpy.ops.texel.add_cube(size=1.0, texture=32)
img = bpy.data.images["Pixel Cube Texture"]
print(f"[step] add_cube -> image '{img.name}' {img.size[0]}x{img.size[1]} "
      f"source={img.source} packed={bool(img.packed_file)} filepath={img.filepath!r}")

# paint, through Texel's own document + flush (the path every tool takes)
d = tex_doc.get(img)
c = d.canvas
L = c.layers[c.active]
red = c.add_colour((255, 0, 0, 255))
for y in range(8, 24):
    for x in range(8, 24):
        L.set(x, y, red)
d.flush()

buf = [0.0] * (32 * 32 * 4)
img.pixels.foreach_get(buf)
opaque = sum(1 for i in range(32 * 32) if buf[i * 4 + 3] > 0.5)
print(f"[paint] opaque texels after flush: {opaque}")

blend = os.path.join(WORK, "painted.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend)
print(f"[save] wrote {blend} ({os.path.getsize(blend)} B)")
print(f"[save] packed at save time: {bool(img.packed_file)}")
print("PHASE1_OK")
