"""Does a canvas survive a save, a quit and a reopen?

  blender --background --factory-startup --python test_persist.py

**This suite exists because it did not, and a buyer lost their work.** Found
2026-09-23 against the live `texel-0.2.0.zip`: `tex_doc._DOCS` is module state,
so it is empty in every new Blender session; `Doc` was built blank; and
`Doc.flush()` writes the whole canvas over the image. Reopening a .blend and
touching the canvas replaced the artwork with a blank one - even when the image
had been packed and had reopened byte-intact.

The trap that made it survive fourteen suites: **a reopen inside the same Python
process does not test a new session.** `_DOCS` lives at module scope, so it
survives `wm.open_mainfile` and the doc comes back populated for the wrong
reason. Every test below that claims to be about a new session calls
`tex_doc.clear()` first, and `test_fresh_process` re-runs the decisive one in an
actual second Blender.
"""
import os
import subprocess
import sys
import tempfile

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
fails = []
RED = (255, 0, 0, 255)


def check(name, cond, detail=""):
    print(f"[{'ok  ' if cond else 'FAIL'}] {name}" + ("" if cond else f"  {detail}"))
    if not cond:
        fails.append(name)


import texel
texel.register()
from texel import tex_doc

print(f"[info] Blender {bpy.app.version_string}")


def census(img):
    w, h = img.size
    buf = [0.0] * (w * h * 4)
    img.pixels.foreach_get(buf)
    out = {}
    for i in range(w * h):
        o = i * 4
        k = tuple(round(buf[o + j] * 255) for j in range(4))
        out[k] = out.get(k, 0) + 1
    return out


def paint_square(img, lo=8, hi=24):
    d = tex_doc.get(img)
    c = d.canvas
    idx = c.add_colour(RED)
    for y in range(lo, hi):
        for x in range(lo, hi):
            c.layers[c.active].set(x, y, idx)
    d.flush()
    return d


# --------------------------------------------------- the handlers are installed
check("load_post handler registered", tex_doc._on_load in bpy.app.handlers.load_post)
check("save_pre handler registered", tex_doc._on_save_pre in bpy.app.handlers.save_pre)

# ------------------------------------------------------- 1. paint, save, reopen
tmp = tempfile.mkdtemp(prefix="texel_persist_")
blend = os.path.join(tmp, "a.blend")

bpy.ops.texel.add_cube(size=1.0, texture=32)
img = bpy.data.images["Pixel Cube Texture"]
paint_square(img)
check("painted 256 texels", census(img).get(RED) == 256, census(img).get(RED))

bpy.ops.wm.save_as_mainfile(filepath=blend)
check("save_pre packed the generated canvas", bool(img.packed_file))

bpy.ops.wm.open_mainfile(filepath=blend)
img = bpy.data.images["Pixel Cube Texture"]
check("the art is still in the file after a reopen",
      census(img).get(RED) == 256, census(img).get(RED))
check("load_post dropped the stale docs", tex_doc._DOCS == {}, list(tex_doc._DOCS))

# ------------------------- 2. the bug: what the first edit of a new session does
tex_doc.clear()                      # a new process has no _DOCS; this is that
d = tex_doc.get(img)                 # what texel.paint/show_canvas/pick_texture do
check("get() rehydrates instead of handing back a blank canvas",
      d is not None and sum(1 for v in d.canvas.layers[0].px if v) == 256,
      None if d is None else sum(1 for v in d.canvas.layers[0].px if v))
check("the palette came back too", d is not None and RED in d.canvas.palette,
      None if d is None else d.canvas.palette)
d.flush()
check("a flush after reopening PRESERVES the art",
      census(img).get(RED) == 256, census(img).get(RED))

# ------------------------------------- 3. a second edit/save cycle is not stale
tex_doc.clear()
d = tex_doc.get(img)
blue = d.canvas.add_colour((0, 0, 255, 255))
for x in range(0, 4):
    d.canvas.layers[d.canvas.active].set(x, 0, blue)
d.flush()
bpy.ops.wm.save_as_mainfile(filepath=blend)
bpy.ops.wm.open_mainfile(filepath=blend)
img = bpy.data.images["Pixel Cube Texture"]
c = census(img)
check("the second save repacked rather than keeping a stale pack",
      c.get(RED) == 256 and c.get((0, 0, 255, 255)) == 4,
      {k: v for k, v in c.items() if v < 1000})

# --------------------------------- 4. refuse to bind rather than wipe, past 255
tex_doc.clear()
big = bpy.data.images.new("Too Many", 32, 32, alpha=True)
px = []
for i in range(32 * 32):
    px += [((i * 7) % 256) / 255.0, ((i * 13) % 256) / 255.0,
           ((i * 29) % 256) / 255.0, 1.0]
big.pixels.foreach_set(px)
big.update()
before = census(big)
check("the fixture really does exceed the palette ceiling", len(before) > 255,
      len(before))
check("get() refuses a texture it cannot represent", tex_doc.get(big) is None)
check("and refusing left the texture untouched", census(big) == before)

# ------------------------------------------ 5. an empty canvas still works
tex_doc.clear()
bpy.ops.texel.canvas_new(size=16, name="Blank")
blank = bpy.data.images["Blank"]
check("a brand-new blank canvas binds", tex_doc.get(blank) is not None)

# ------------------------------------- 6. the same thing in a REAL new process
if os.environ.get("TEXEL_CHILD") != "1":
    child = os.path.join(tmp, "child.py")
    open(child, "w", encoding="utf-8").write(
        "import os, sys, bpy\n"
        f"sys.path.insert(0, {os.path.dirname(HERE)!r})\n"
        "import texel; texel.register()\n"
        "from texel import tex_doc\n"
        f"bpy.ops.wm.open_mainfile(filepath={blend!r})\n"
        "img = bpy.data.images['Pixel Cube Texture']\n"
        "d = tex_doc.get(img)\n"
        "n = 0 if d is None else sum(1 for v in d.canvas.layers[0].px if v)\n"
        "d.flush()\n"
        "w,h = img.size\n"
        "buf=[0.0]*(w*h*4); img.pixels.foreach_get(buf)\n"
        "red=sum(1 for i in range(w*h) if tuple(round(buf[i*4+j]*255) for j in range(4))==(255,0,0,255))\n"
        "print(f'CHILD docpx={n} red={red}')\n")
    env = dict(os.environ, TEXEL_CHILD="1")
    out = subprocess.run([bpy.app.binary_path, "--background", "--factory-startup",
                          "--python", child], capture_output=True, text=True, env=env)
    line = next((l for l in out.stdout.splitlines() if l.startswith("CHILD ")), "")
    print(f"[info] {line or out.stdout[-400:]}")
    check("a genuinely fresh Blender process rehydrates and does not wipe",
          line == "CHILD docpx=260 red=256", line)

texel.unregister()
print()
if fails:
    print(f"{len(fails)} FAILED: {fails}")
    sys.exit(1)
print("TEXEL PERSIST: ALL PASS")
