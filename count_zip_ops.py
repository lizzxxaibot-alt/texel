"""Count registered operators inside a SHIPPED zip, not the working tree.

    blender --background --factory-startup --python count_zip_ops.py -- <zip>

Companion to `count_ops.py`, which counts the working tree. This one counts the
artifact a buyer actually downloads, which is the number the honesty rules care
about: the tree can be several unshipped commits ahead of the store, and on
2026-09-09 it was. Written by `texel-support` 2026-09-10 to settle whether the
devlog's "94 operators" contradicted the page's "95" -- it did not, they are
different versions (0.1.0 = 94, 0.2.0 = 95, the difference being
`texel.selection_transform`).
"""
import os, sys, zipfile, tempfile, shutil
import bpy

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
zp = argv[0]
tmp = tempfile.mkdtemp(prefix="texelzip_")
with zipfile.ZipFile(zp) as z:
    z.extractall(tmp)
# the add-on package dir is the single top-level dir containing __init__.py
cands = [d for d in os.listdir(tmp)
         if os.path.isfile(os.path.join(tmp, d, "__init__.py"))]
pkgdir = cands[0]
sys.path.insert(0, tmp)
mod = __import__(pkgdir)
mod.register()
ops = sorted(o for o in dir(bpy.ops.texel) if not o.startswith("_"))
print(f"ZIP={os.path.basename(zp)} PKG={pkgdir} TEXEL_OP_COUNT={len(ops)}")
for o in ops:
    print(f"  texel.{o}")
mod.unregister()
shutil.rmtree(tmp, ignore_errors=True)
