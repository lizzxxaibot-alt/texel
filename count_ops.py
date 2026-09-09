"""Count registered operators and compare against the reference surface."""
import os, re, sys
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import texel
texel.register()
ops = sorted(o for o in dir(bpy.ops.texel) if not o.startswith("_"))
print(f"TEXEL_OP_COUNT={len(ops)}")
for o in ops:
    print(f"  texel.{o}")
spec = open(os.path.join(HERE, "reference", "api-surface.txt"), encoding="utf-8").read()
theirs = re.findall(r"^  (pixel_art_studio\.\S+)", spec, re.M)
print(f"THEIR_OP_COUNT={len(theirs)}")
texel.unregister()
