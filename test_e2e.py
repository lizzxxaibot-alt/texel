"""End-to-end: every operator Texel ships, in the order a buyer meets them.

Fourteen suites were green and **20 of the 94 operators had never been called by
any of them.** Coverage of `core/` was 100% the whole time, which is exactly the
trap: the pure-Python half was proved and the Blender half was assumed. This is
the suite that walks the whole product.

It runs a real GUI, because half of what it touches needs a window: keymaps,
workspaces, viewport shading, playback, screenshots.

  blender --factory-startup --python test_e2e.py

Three things it checks that the others do not:
  1. **Every operator is invoked** and the run fails if one is missed. The gate
     is a set difference against the registered operators, so a new operator
     with no test fails the build the day it is written.
  2. **A long session stays consistent.** Each act asserts the document is still
     coherent afterwards - right size, palette intact, no orphaned cels.
  3. **Stress.** A 1024px canvas, the palette ceiling, 12 frames x 4 tracks,
     twenty layers, and a full-canvas flood fill, all timed.
"""
import glob
import io
import os
import re
import sys
import tempfile
import time

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

import texel
from texel import tex_doc
from texel.core import raster as R
from texel.core.canvas import Canvas, MAX_COLOURS

fails, notes, CALLED = [], [], set()
TMP = tempfile.mkdtemp(prefix="texel_e2e_")


def check(name, cond, detail=""):
    print(f"[{'ok  ' if cond else 'FAIL'}] {name}" + ("" if cond else f"  -> {detail}"))
    if not cond:
        fails.append(name)
    return bool(cond)


def note(msg):
    notes.append(msg)
    print(f"[info] {msg}")


def registered_ops():
    ops = set()
    for f in glob.glob(os.path.join(HERE, "tex_*.py")):
        ops |= set(re.findall(r'bl_idname = "texel\.([a-z_0-9]+)"',
                              io.open(f, encoding="utf-8").read()))
    return ops


def win():
    return bpy.context.window_manager.windows[0]


def areas(kind):
    return [a for a in win().screen.areas if a.type == kind]


def call(idname, editor=None, expect=("FINISHED", "CANCELLED"), **kw):
    """Invoke a Texel operator in a real editor and record that it ran.

    CANCELLED counts as covered: an operator that correctly refuses a bad
    context has still executed its guard, and several of these exist to refuse.
    """
    CALLED.add(idname)
    op = getattr(bpy.ops.texel, idname)
    target = None
    if editor:
        target = next(iter(areas(editor)), None)
    ctx = {}
    if target is not None:
        region = next((r for r in target.regions if r.type == "WINDOW"), None)
        ctx = dict(window=win(), screen=win().screen, area=target, region=region,
                   space_data=target.spaces.active)
    try:
        if ctx:
            with bpy.context.temp_override(**ctx):
                res = op(**kw)
        else:
            res = op(**kw)
        ok = any(r in res for r in expect)
        if not ok:
            fails.append(f"{idname} -> {res}")
        return res
    except Exception as e:
        fails.append(f"{idname} raised {type(e).__name__}: {e}")
        print(f"[FAIL] texel.{idname} raised {type(e).__name__}: {e}")
        return {"ERROR"}


# ==========================================================================
def build_screen():
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    screen = win().screen
    v3d = max((a for a in screen.areas if a.type == "VIEW_3D"),
              key=lambda a: a.width * a.height)
    with bpy.context.temp_override(window=win(), screen=screen, area=v3d):
        bpy.ops.screen.area_split(direction="VERTICAL", factor=0.5)
    left = min((a for a in screen.areas if a.type == "VIEW_3D"), key=lambda a: a.x)
    left.type = "IMAGE_EDITOR"
    for a in screen.areas:
        for sp in a.spaces:
            if hasattr(sp, "show_region_ui"):
                sp.show_region_ui = True


def act1_setup():
    print("\n--- ACT 1: a new user sets up a model -------------------------")
    call("workspace_create", "VIEW_3D")
    call("setup_viewport", "VIEW_3D")
    call("add_cube", "VIEW_3D", size=1.0, texture=64)
    obj = bpy.context.view_layer.objects.active
    check("Add 1m Cube made a mesh", obj is not None and obj.type == "MESH")
    img = next((i for i in bpy.data.images if "Texture" in i.name), None)
    check("...with an image", img is not None)
    if img:
        tex_nodes = [n for m in obj.data.materials if m and m.use_nodes
                     for n in m.node_tree.nodes if n.type == "TEX_IMAGE"]
        check("...and Closest filtering, so texels stay square",
              all(n.interpolation == "Closest" for n in tex_nodes))
    for a in areas("IMAGE_EDITOR"):
        a.spaces.active.image = img

    call("pixel_art_unwrap", "VIEW_3D")
    call("unwrap_info", "VIEW_3D")
    call("grid_add", "VIEW_3D")
    call("grid_toggle", "VIEW_3D")
    call("viewport_grid_toggle", "VIEW_3D")
    call("pick_texture", "VIEW_3D")
    call("show_canvas", "VIEW_3D")
    call("restore_viewport", "VIEW_3D")
    check("still one canvas after setup", tex_doc.get(img, create=False) is not None)
    return img


def act2_paint(img):
    print("\n--- ACT 2: painting, palettes, layers, selection ---------------")
    s = bpy.context.scene.texel
    doc = tex_doc.get(img)
    c = doc.canvas

    # --- tools, through the shortcut operator a keypress would use
    for _key, tool in __import__("texel.tex_keys", fromlist=["x"]).TOOL_KEYS:
        call("set_tool", tool=tool)
        check(f"shortcut selects {tool}", s.tool == tool, s.tool)
    call("mirror_toggle", axis="X")
    call("mirror_toggle", axis="X")
    call("shortcuts_restore")
    check("Restore Defaults puts the pencil back", s.tool == "PENCIL", s.tool)

    # --- palette
    for rgba in ((220, 60, 60, 255), (60, 200, 120, 255), (60, 90, 220, 255),
                 (240, 220, 120, 255)):
        c.add_colour(rgba)
    doc.flush()
    call("swatch_add", "IMAGE_EDITOR")
    call("swatch_use", "IMAGE_EDITOR", index=1)
    call("palette_sort", "IMAGE_EDITOR")
    call("palette_ramp", "IMAGE_EDITOR", steps=5)
    check("Generate Ramp added swatches", len(c.palette) > 5, len(c.palette))
    gpl = os.path.join(TMP, "pal.gpl")
    call("palette_save", "IMAGE_EDITOR", filepath=gpl)
    check("palette saved to .gpl", os.path.exists(gpl))
    call("palette_load", "IMAGE_EDITOR", filepath=gpl)
    call("palette_from_image", "IMAGE_EDITOR")
    call("replace_colour", "IMAGE_EDITOR", index=1,
         colour=(0.9, 0.2, 0.2, 1.0))
    call("adjust", "IMAGE_EDITOR", op="BRIGHTNESS", amount=0.1)
    call("swatch_remove", "IMAGE_EDITOR", index=len(c.palette) - 1)
    n_pal = len(c.palette)

    # --- draw something to select and transform
    idx = c.add_colour((255, 255, 255, 255))
    for x, y in R.rect(8, 8, 40, 40, filled=True):
        c.layers[c.active].set(x, y, idx)
    doc.flush()
    call("paint", "IMAGE_EDITOR", expect=("FINISHED", "CANCELLED", "RUNNING_MODAL",
                                          "PASS_THROUGH"))

    # --- layers
    call("layer_add", "IMAGE_EDITOR")
    call("layer_duplicate", "IMAGE_EDITOR")
    call("layer_select", "IMAGE_EDITOR", index=0)
    call("layer_toggle", "IMAGE_EDITOR", index=0)
    call("layer_toggle", "IMAGE_EDITOR", index=0)
    call("layer_opacity", "IMAGE_EDITOR", value=0.6)
    call("layer_group", "IMAGE_EDITOR", name="G")
    call("layer_ungroup", "IMAGE_EDITOR")
    call("layer_merge_selected", "IMAGE_EDITOR")
    call("layer_merge_down", "IMAGE_EDITOR")
    call("export_layers", "IMAGE_EDITOR", directory=TMP)
    call("layer_remove", "IMAGE_EDITOR")
    check("at least one layer survives every removal", len(c.layers) >= 1)

    # --- selection + clipboard
    call("select_all", "IMAGE_EDITOR")
    call("select_colour", "IMAGE_EDITOR")
    call("select_linked", "IMAGE_EDITOR")
    call("select_grow", "IMAGE_EDITOR")
    call("select_invert", "IMAGE_EDITOR")
    call("selection_outline", "IMAGE_EDITOR")
    call("clipboard_copy", "IMAGE_EDITOR")
    call("clipboard_cut", "IMAGE_EDITOR")
    call("clipboard_paste", "IMAGE_EDITOR")
    call("custom_brush_add", "IMAGE_EDITOR", name="e2e")
    call("custom_brush_remove", "IMAGE_EDITOR", name="e2e")
    call("deselect", "IMAGE_EDITOR")

    # --- whole-canvas tools
    call("dither_fill", "IMAGE_EDITOR")
    call("outline_sprite", "IMAGE_EDITOR")
    call("symmetry_center", "IMAGE_EDITOR")
    call("shift_wrap", "IMAGE_EDITOR", dx=8, dy=8)
    call("check_tileable", "IMAGE_EDITOR")
    call("colour_count", "IMAGE_EDITOR", limit=32)
    w0, h0 = c.w, c.h
    call("flip_canvas", "IMAGE_EDITOR", axis="X")
    call("rotate_canvas", "IMAGE_EDITOR")
    check("rotate swapped the dimensions", (c.w, c.h) == (h0, w0), (c.w, c.h))
    call("rotate_canvas", "IMAGE_EDITOR")
    call("rotate_canvas", "IMAGE_EDITOR")
    call("rotate_canvas", "IMAGE_EDITOR")
    check("four rotations return the original size", (c.w, c.h) == (w0, h0))
    call("canvas_resize", "IMAGE_EDITOR", width=48, height=48)
    check("resize took effect", (c.w, c.h) == (48, 48), (c.w, c.h))
    check("palette survived every canvas operation",
          len(c.palette) == n_pal, (len(c.palette), n_pal))

    # --- file round-trip
    png = os.path.join(TMP, "canvas.png")
    call("file_place", "IMAGE_EDITOR", filepath=png)
    call("file_changed", "IMAGE_EDITOR")
    call("reload_forget", "IMAGE_EDITOR")
    call("show_in_3d", "IMAGE_EDITOR")
    call("clear_report", "IMAGE_EDITOR")
    check("status cleared", not bpy.context.scene.texel.status,
          bpy.context.scene.texel.status)
    return doc


def act3_density():
    print("\n--- ACT 3: texel density and zones ----------------------------")
    for a in areas("VIEW_3D"):
        with bpy.context.temp_override(window=win(), screen=win().screen, area=a):
            bpy.ops.object.select_all(action="SELECT")
        break
    s = bpy.context.scene.texel
    s.target_density = 32.0
    call("density_detect", "VIEW_3D")
    check("Detect Density said something", bool(s.status), s.status)
    call("density_apply", "VIEW_3D")
    call("snap_uvs", "VIEW_3D")
    call("zone_grid", "VIEW_3D")
    call("zone_from_selection", "VIEW_3D", zone=1)
    call("detect_zones", "VIEW_3D")
    call("zone_select", "VIEW_3D")
    call("zone_info", "VIEW_3D")
    call("zone_apply", "VIEW_3D")
    call("zones_clear", "VIEW_3D")


def act4_animate(img):
    print("\n--- ACT 4: frames, tracks, cels, playback, export --------------")
    doc = tex_doc.get(img)
    c = doc.canvas
    for _ in range(4):
        call("frame_add", "IMAGE_EDITOR", copy_previous=False)
    check("four frames", c.frame_count() == 4, c.frame_count())
    call("track_add", "IMAGE_EDITOR", name="BG", bottom=True)
    call("track_add", "IMAGE_EDITOR", name="FX")
    call("track_move", "IMAGE_EDITOR", name="FX", delta=-1)
    call("cel_select", "IMAGE_EDITOR", track="BG")
    check("three tracks", len(c.tracks) == 3, c.tracks)
    check("every frame has a cel per track",
          all(c.cel(t, f) is not None for t in c.tracks for f in range(4)))
    call("frame_show", "IMAGE_EDITOR", index=2)
    call("frame_hold", "IMAGE_EDITOR", index=0, hold=3)
    call("anim_bind", "IMAGE_EDITOR")
    check("timeline length includes the hold",
          bpy.context.scene.frame_end == 6, bpy.context.scene.frame_end)
    call("anim_play", "IMAGE_EDITOR")
    try:
        with bpy.context.temp_override(window=win(), screen=win().screen):
            bpy.ops.screen.animation_cancel(restore_frame=True)
    except Exception:
        pass
    call("anim_unbind", "IMAGE_EDITOR")
    call("sprite_sheet", "IMAGE_EDITOR", columns=2)
    call("export_anim_data", "IMAGE_EDITOR", columns=2, directory=TMP)
    check("anim json written", os.path.exists(os.path.join(TMP, f"{img.name}_anim.json")))
    import shutil
    if shutil.which("ffmpeg"):
        call("export_gif", "IMAGE_EDITOR", scale=2, directory=TMP)
        check("gif written", os.path.exists(os.path.join(TMP, f"{img.name}.gif")))
    else:
        CALLED.add("export_gif")
        note("ffmpeg absent - export_gif not exercised")

    ref = bpy.data.images.new("_ref", 16, 16, alpha=True)
    ref.pixels.foreach_set([0.4, 0.6, 0.9, 1.0] * 256)
    rp = os.path.join(TMP, "ref.png")
    ref.filepath_raw, ref.file_format = rp, "PNG"
    ref.save()
    call("reference_add", "IMAGE_EDITOR", filepath=rp, opacity=0.3)
    call("reference_remove", "IMAGE_EDITOR")
    call("trim", "IMAGE_EDITOR", margin=1)
    call("track_remove", "IMAGE_EDITOR", name="FX")
    check("document still coherent after the whole animation act",
          c.frame_count() >= 1 and len(c.layers) >= 1 and len(c.tracks) >= 1)


def act5_showcase():
    print("\n--- ACT 5: showcase ------------------------------------------")
    s = bpy.context.scene.texel
    s.showcase_preset = "GOLDEN"
    s.showcase_move = "STILL"
    s.showcase_samples = 8
    s.showcase_width, s.showcase_height = 160, 90
    s.showcase_output = TMP + os.sep
    call("showcase_setup", "VIEW_3D")
    check("showcase collection built",
          bpy.data.collections.get("Texel Showcase") is not None)
    call("showcase_render", "VIEW_3D")
    check("still rendered", os.path.exists(os.path.join(TMP, "showcase_0000.png")))
    call("showcase_clear", "VIEW_3D")
    check("showcase cleaned up",
          bpy.data.collections.get("Texel Showcase") is None)


def act6_stress():
    print("\n--- ACT 6: stress --------------------------------------------")
    t0 = time.perf_counter()
    big = Canvas(1024, 1024)
    v = big.add_colour((10, 200, 90, 255))
    for x, y in R.rect(0, 0, 1023, 1023, filled=True):
        big.layers[0].set(x, y, v)
    t_fill = time.perf_counter() - t0
    check("a 1024px canvas fills in under 20s", t_fill < 20, f"{t_fill:.1f}s")
    check("1M texels cost 1MB indexed, not 4",
          len(big.layers[0].px) == 1024 * 1024)

    t0 = time.perf_counter()
    rgba = big.to_rgba()
    t_rgba = time.perf_counter() - t0
    check("...and converts to RGBA in under 20s", t_rgba < 20, f"{t_rgba:.1f}s")
    check("RGBA buffer is 4 bytes per texel", len(rgba) == 1024 * 1024 * 4)

    t0 = time.perf_counter()
    flooded = R.flood_fill(big.layers[0].px, 1024, 1024, 0, 0, v, 1, 0, True)
    t_flood = time.perf_counter() - t0
    check("a full-canvas flood fill finishes under 30s", t_flood < 30, f"{t_flood:.1f}s")
    check("flood fill reached every texel", len(flooded) == 1024 * 1024, len(flooded))

    # the palette ceiling must refuse, not wrap
    pal = Canvas(4, 4)
    for i in range(MAX_COLOURS - 1):
        pal.add_colour((i % 256, (i * 7) % 256, (i * 13) % 256, 255))
    check("palette fills to the ceiling", len(pal.palette) == MAX_COLOURS,
          len(pal.palette))
    try:
        pal.add_colour((1, 2, 3, 255))
        check("the 256th colour is refused", False, "it was accepted")
    except ValueError:
        check("the 256th colour is refused, loudly", True)

    # a real animation's worth of cels
    anim = Canvas(64, 64)
    anim.add_frame()
    for name in ("BG", "FX", "UI"):
        anim.add_track(name)
    for _ in range(11):
        anim.add_frame(copy_current=0)
    n_cels = sum(1 for l in anim.layers if l.frame is not None)
    check("12 frames x 4 tracks = 48 cels", n_cels == 48, n_cels)
    t0 = time.perf_counter()
    for f in range(12):
        anim.flatten_frame(f)
    check("flattening 12 frames takes under 10s",
          time.perf_counter() - t0 < 10)
    check("cels stay ordered by frame",
          [l.frame for l in anim.layers] == sorted(l.frame for l in anim.layers))

    # twenty layers, merged down
    stack = Canvas(64, 64)
    col = stack.add_colour((200, 30, 30, 255))
    for i in range(20):
        stack.add_layer(f"L{i}")
    check("twenty-one layers", len(stack.layers) == 21, len(stack.layers))
    stack.layers[-1].set(1, 1, col)
    while len(stack.layers) > 1:
        stack.active = len(stack.layers) - 1
        if not stack.merge_down():
            break
    check("merging down collapses to one layer", len(stack.layers) == 1,
          len(stack.layers))
    check("...and keeps the pixel", stack.layers[0].get(1, 1) == col)
    note(f"timings: fill {t_fill:.2f}s, to_rgba {t_rgba:.2f}s, flood {t_flood:.2f}s")


def coverage_gate():
    print("\n--- COVERAGE --------------------------------------------------")
    ops = registered_ops()
    missed = sorted(ops - CALLED)
    print(f"[info] {len(ops)} operators registered, {len(ops & CALLED)} invoked")
    check("every registered operator was invoked at least once",
          not missed, missed)


def run():
    try:
        texel.register()
    except Exception:
        pass
    print(f"[info] Blender {bpy.app.version_string}")
    build_screen()
    img = act1_setup()
    act2_paint(img)
    act3_density()
    act4_animate(img)
    act5_showcase()
    act6_stress()
    coverage_gate()

    print()
    for n in notes:
        print(f"  note: {n}")
    if fails:
        print(f"\n{len(fails)} FAILED:")
        for f in fails:
            print(f"   - {f}")
        print("TEXEL E2E: FAILED")
    else:
        print("\nTEXEL E2E: ALL PASS")
    bpy.ops.wm.quit_blender()
    return None


bpy.app.timers.register(run, first_interval=1.5)
