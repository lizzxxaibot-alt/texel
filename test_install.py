"""Install the built zip into a throwaway Blender profile and register it.

This is the only test that proves what the CUSTOMER does works. The source tests
import from the working tree, which hides packaging mistakes entirely.

  blender --background --factory-startup --python test_install.py
"""
import os
import sys
import zipfile

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
fails = []


def check(name, cond, detail=""):
    print(f"[{'ok  ' if cond else 'FAIL'}] {name}" + ("" if cond else f"  {detail}"))
    if not cond:
        fails.append(name)


zips = sorted(f for f in os.listdir(os.path.join(HERE, "dist")) if f.endswith(".zip"))
check("a build exists in dist/", bool(zips), "run: py -3 build.py")
if not zips:
    sys.exit(1)
zip_path = os.path.join(HERE, "dist", zips[-1])
print(f"[info] installing {zips[-1]}  ({os.path.getsize(zip_path) / 1024:.1f} KB)")
print(f"[info] Blender {bpy.app.version_string}")

# unpack somewhere Blender will import from, exactly as an install does
import tempfile
tmp = tempfile.mkdtemp(prefix="texel_install_")
with zipfile.ZipFile(zip_path) as z:
    z.extractall(tmp)
sys.path.insert(0, tmp)

check("zip unpacks to a single texel/ root",
      os.path.isdir(os.path.join(tmp, "texel")), os.listdir(tmp))
check("manifest shipped", os.path.exists(os.path.join(tmp, "texel", "blender_manifest.toml")))
check("licence shipped", os.path.exists(os.path.join(tmp, "texel", "LICENSE.txt")))
check("no tests shipped",
      not any(f.startswith("test_") for f in os.listdir(os.path.join(tmp, "texel"))))

import texel
texel.register()
check("installed copy registers", True)
check("scene property present", hasattr(bpy.context.scene, "texel"))

# smoke the real user path: make a canvas, paint, confirm it reached the image
bpy.ops.texel.canvas_new(size=16, name="InstallCheck")
img = bpy.data.images.get("InstallCheck")
check("canvas_new works from the installed copy", img is not None)

from texel import tex_doc
from texel.core import raster as R
doc = tex_doc.get(img)
idx = doc.canvas.add_colour((0, 255, 0, 255))
for x, y in R.pixel_perfect(R.line(0, 0, 15, 15)):
    doc.canvas.layers[0].set(x, y, idx)
doc.flush()
buf = [0.0] * (16 * 16 * 4)
img.pixels.foreach_get(buf)
o = ((16 - 1 - 0) * 16 + 0) * 4
check("painted pixel is live after install",
      tuple(round(v * 255) for v in buf[o:o + 4]) == (0, 255, 0, 255),
      tuple(round(v * 255) for v in buf[o:o + 4]))

# palette round trip through the shipped core
from texel.core import palette as P
gpl = P.to_gpl("Ship", [(1, 2, 3, 255)])
check("shipped palette core round trips", P.parse(gpl, "x.gpl")[1] == [(1, 2, 3, 255)])

texel.unregister()
check("installed copy unregisters", True)

import shutil
shutil.rmtree(tmp, ignore_errors=True)

print()
if fails:
    print(f"{len(fails)} FAILED: {fails}")
    sys.exit(1)
print("TEXEL INSTALL: ALL PASS")
