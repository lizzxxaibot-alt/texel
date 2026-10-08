"""Install the free Lite zip, AS BUILT, and prove it works and leaks nothing.

Lite is the full source with three modules left out and a flag flipped inside
the zip, so nothing about it exists in the working tree - every check here runs
on the unpacked zip, never on the source. The working tree is read only to
learn which operators the paid modules define, so a new paid operator is
covered without editing this file.

  blender --factory-startup --python test_lite.py 2>&1 | grep -i traceback
  blender --factory-startup --python test_lite.py -- <zip>

The GUI run is the real one: the Sprite and Showcase panels are replaced by a
stub in Lite, and a panel only fails at draw time, where Blender swallows the
exception into an on-screen error box. So, as for test_panels.py, an empty
traceback grep plus "TEXEL LITE: ALL PASS" is the pass, and the screenshots in
shots/lite/ get looked at. --background runs everything except the drawing.
"""
import glob
import io
import os
import re
import shutil
import sys
import tempfile
import zipfile

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
PAID = ("tex_anim.py", "tex_sprite.py", "tex_showcase.py")
fails = []


def check(name, cond, detail=""):
    print(f"[{'ok  ' if cond else 'FAIL'}] {name}" + ("" if cond else f"  {detail}"),
          flush=True)
    if not cond:
        fails.append(name)


def op_ids(paths):
    ids = set()
    for p in paths:
        ids |= set(re.findall(r'bl_idname = "texel\.([a-z_0-9]+)"',
                              io.open(p, encoding="utf-8").read()))
    return ids


argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
zips = sorted(glob.glob(os.path.join(HERE, "dist", "lite", "texel-lite-*.zip")))
zip_path = argv[0] if argv else (zips[-1] if zips else None)
check("a Lite build exists", zip_path and os.path.exists(zip_path),
      "run: py -3 build.py --lite")
if not zip_path or not os.path.exists(zip_path):
    sys.exit(1)
print(f"[info] installing {os.path.basename(zip_path)}  "
      f"({os.path.getsize(zip_path) / 1024:.1f} KB)", flush=True)
print(f"[info] Blender {bpy.app.version_string}", flush=True)

tmp = tempfile.mkdtemp(prefix="texel_lite_")
with zipfile.ZipFile(zip_path) as z:
    names = z.namelist()
    z.extractall(tmp)
pkg = os.path.join(tmp, "texel")

# ---- the zip itself: no paid code, and it says what it is
leaked = [n for n in names if n.split("/")[-1] in PAID]
check("no paid module in the zip", not leaked, leaked)
check("no tests in the zip", not any("/test_" in n for n in names))
edition = io.open(os.path.join(pkg, "tex_edition.py"), encoding="utf-8").read()
check("edition flag is LITE = True", re.search(r"^LITE = True$", edition, re.M), "")
manifest = io.open(os.path.join(pkg, "blender_manifest.toml"), encoding="utf-8").read()
check("manifest names it Texel Lite", 'name = "Texel Lite"' in manifest)
init = io.open(os.path.join(pkg, "__init__.py"), encoding="utf-8").read()
check("bl_info names it Texel Lite", '"name": "Texel Lite"' in init)
readme = io.open(os.path.join(pkg, "README.md"), encoding="utf-8").read()
check("README opens by saying what Lite lacks",
      readme.startswith("> **This is Texel Lite") and "Not in Lite" in readme[:600])
start = io.open(os.path.join(pkg, "START-HERE.html"), encoding="utf-8").read()
check("START-HERE does not thank a Lite user for buying",
      "Thank you for buying" not in start and "This is Texel Lite" in start)

# ---- install and register, from the zip and nowhere else
sys.path.insert(0, tmp)
for m in [m for m in sys.modules if m == "texel" or m.startswith("texel.")]:
    del sys.modules[m]
import texel  # noqa: E402
check("imported from the unpacked zip, not the source tree",
      os.path.dirname(os.path.abspath(texel.__file__)) == os.path.abspath(pkg),
      texel.__file__)
texel.register()
check("Lite registers", hasattr(bpy.context.scene, "texel"))

paid_ops = op_ids(os.path.join(HERE, f) for f in PAID)
free_ops = op_ids(glob.glob(os.path.join(pkg, "tex_*.py")))
live = {o for o in dir(bpy.ops.texel) if not o.startswith("_")}
check(f"no paid operator registered ({len(paid_ops)} checked)",
      not (paid_ops & live), sorted(paid_ops & live))
check(f"every free operator registered ({len(free_ops)})",
      free_ops <= live, sorted(free_ops - live))
print(f"[info] Lite registers {len(live)} operators", flush=True)

# the real user path: a canvas, paint on it, the pixel reaches the image
bpy.ops.texel.canvas_new(size=16, name="LiteCheck")
img = bpy.data.images.get("LiteCheck")
check("canvas_new works in Lite", img is not None)
from texel import tex_doc  # noqa: E402
from texel.core import raster as R  # noqa: E402
doc = tex_doc.get(img)
idx = doc.canvas.add_colour((0, 255, 0, 255))
for x, y in R.pixel_perfect(R.line(0, 0, 15, 15)):
    doc.canvas.layers[0].set(x, y, idx)
doc.flush()
buf = [0.0] * (16 * 16 * 4)
img.pixels.foreach_get(buf)
o = ((16 - 1 - 0) * 16 + 0) * 4
check("painted pixel is live in Lite",
      tuple(round(v * 255) for v in buf[o:o + 4]) == (0, 255, 0, 255),
      tuple(round(v * 255) for v in buf[o:o + 4]))


def finish():
    texel.unregister()
    check("Lite unregisters", not hasattr(bpy.types, "TEXEL_PT_tools_2d"))
    shutil.rmtree(tmp, ignore_errors=True)
    print(flush=True)
    if fails:
        print(f"{len(fails)} FAILED: {fails}", flush=True)
        print("TEXEL LITE: FAILED", flush=True)
    else:
        print("TEXEL LITE: ALL PASS", flush=True)


if bpy.app.background:
    print("[info] background run: panel drawing skipped, run without "
          "--background for it", flush=True)
    finish()
    sys.exit(1 if fails else 0)

# ---- GUI: every panel draws, including the two stubs, in both editors
OUT = os.path.join(HERE, "shots", "lite")
os.makedirs(OUT, exist_ok=True)
state = {"step": 0}
try:
    bpy.context.preferences.view.show_splash = False
except Exception:
    pass

# Count the stub draws. The first version of this test passed with the Texel
# tab never selected - nothing drew, so nothing could fail. A screenshot shows
# that only if someone looks; a counter makes it a gate.
from texel import tex_ui  # noqa: E402
drawn = []
_stub = tex_ui._draw_full_only


def _counting_stub(layout, what):
    drawn.append(what)
    return _stub(layout, what)


tex_ui._draw_full_only = _counting_stub


def force_tab():
    for a in win().screen.areas:
        if a.type not in {"IMAGE_EDITOR", "VIEW_3D"}:
            continue
        for r in a.regions:
            if r.type == "UI" and r.active_panel_category != "Texel":
                try:
                    r.active_panel_category = "Texel"
                except Exception:
                    pass
        a.tag_redraw()


def win():
    return bpy.context.window_manager.windows[0]


def setup():
    screen = win().screen
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    v3d = max((a for a in screen.areas if a.type == "VIEW_3D"),
              key=lambda a: a.width * a.height)
    with bpy.context.temp_override(window=win(), screen=screen, area=v3d):
        bpy.ops.screen.area_split(direction="VERTICAL", factor=0.45)
    left = min((a for a in screen.areas if a.type == "VIEW_3D"), key=lambda a: a.x)
    left.type = "IMAGE_EDITOR"
    for a in screen.areas:
        if a.type == "VIEW_3D":
            region = next(r for r in a.regions if r.type == "WINDOW")
            with bpy.context.temp_override(window=win(), screen=screen, area=a,
                                           region=region):
                bpy.ops.texel.add_cube(size=1.0, texture=32)
            break
    cube = next((i for i in bpy.data.images if "Texture" in i.name), img)
    for a in screen.areas:
        if a.type == "IMAGE_EDITOR":
            a.spaces.active.image = cube
            region = next(r for r in a.regions if r.type == "WINDOW")
            with bpy.context.temp_override(window=win(), screen=screen, area=a,
                                           region=region, space_data=a.spaces.active):
                bpy.ops.texel.layer_add()
            check("layer_add works in Lite",
                  len(tex_doc.get(cube).canvas.layers) == 2,
                  len(tex_doc.get(cube).canvas.layers))
        for sp in a.spaces:
            if hasattr(sp, "show_region_ui"):
                sp.show_region_ui = True
        for r in a.regions:
            if r.type == "UI" and a.type in {"IMAGE_EDITOR", "VIEW_3D"}:
                try:
                    r.active_panel_category = "Texel"
                except Exception:
                    pass
        a.tag_redraw()


def tick():
    force_tab()
    if state["step"] == 0:
        setup()
    elif state["step"] < 3:
        pass                         # let the sidebars redraw on the Texel tab
    elif state["step"] in (3, 4):
        # two shots: the first can land mid-relayout, the second is settled
        p = os.path.join(OUT, f"lite_{state['step']}.png")
        with bpy.context.temp_override(window=win(), screen=win().screen):
            bpy.ops.screen.screenshot(filepath=p)
        check(f"screenshot {state['step']} written", os.path.exists(p), p)
    else:
        for what in ("Sprite tools", "Showcase renders"):
            check(f"the '{what}' stub actually drew", what in drawn, sorted(set(drawn)))
        finish()
        bpy.ops.wm.quit_blender()
        return None
    state["step"] += 1
    return 0.5


bpy.app.timers.register(tick, first_interval=1.0)
