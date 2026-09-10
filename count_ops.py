"""Count Texel's registered operators.

The number this prints is the one the store page publishes, so it is read off a
real `register()` in a real Blender rather than by grepping for `bl_idname` --
an operator that fails to register is not an operator, and only registration
knows the difference.

    blender --background --python count_ops.py

This script used to also count a second add-on's operators and print the two
side by side, to support a "we ship more than they do" line on the store page.
Both the line and the comparison were removed on 2026-09-09: Texel is not
positioned against another product, so a count is only ever OUR count.
"""
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import texel

texel.register()
ops = sorted(o for o in dir(bpy.ops.texel) if not o.startswith("_"))
print(f"TEXEL_OP_COUNT={len(ops)}")
for o in ops:
    print(f"  texel.{o}")
texel.unregister()
