"""Screen-record Texel building ONE environment's signature texture.

Real Blender GUI, real operators, real sidebar. Each environment demonstrates a
different capability, so the five videos are not the same video five times:

  shrine    paint a grass tile, then Check Tiling reports it seamless
  corridor  Generate Ramp builds the metal shading, then paint with it
  ruins     paint sandstone, then set two density zones on the model
  tavern    build on separate LAYERS, toggle one, then swap a palette colour
  cavern    Mirror X on: draw the left half only, watch the right appear

  blender --factory-startup --python steps_env.py -- shrine
"""
import math
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["shrine"]
NAME = argv[0]
SIZE = 64

OUT = os.path.join(HERE, "promo", "steps", NAME)
os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT):
    os.remove(os.path.join(OUT, f))

import texel
from texel import tex_doc
from texel.core import raster as R
from texel.core import tools as TT

try:
    texel.register()
except Exception:
    pass
try:
    bpy.context.preferences.view.show_splash = False
except Exception:
    pass

G = {}
SCRIPT = []
state = {"n": 0, "step": 0, "sub": 0, "ready": False}


def win():
    return bpy.context.window_manager.windows[0]


def areas(kind):
    return [a for a in win().screen.areas if a.type == kind]


def in_area(area, op, **kw):
    region = next((r for r in area.regions if r.type == "WINDOW"), None)
    if region is None:
        return
    try:
        with bpy.context.temp_override(window=win(), screen=win().screen,
                                       area=area, region=region):
            op(**kw)
    except Exception as e:
        print(f"[warn] {getattr(op, '__name__', op)}: {e}", flush=True)


def force_tab():
    for a in win().screen.areas:
        if a.type not in {"IMAGE_EDITOR", "VIEW_3D"}:
            continue
        for r in a.regions:
            if r.type == "UI" and r.active_panel_category != "Texel":
                try:
                    r.active_panel_category = "Texel"
                    r.tag_redraw()
                except Exception:
                    pass


def setup():
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    s = bpy.context.scene.texel
    img = bpy.data.images.new(NAME.title(), SIZE, SIZE, alpha=True)
    img.pixels.foreach_set([0.0] * (SIZE * SIZE * 4))
    img.update()

    mat = bpy.data.materials.new("M")
    mat.use_nodes = True
    nt = mat.node_tree
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    tex.interpolation = "Closest"
    tex.extension = "REPEAT"
    nt.links.new(tex.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"])

    # a small block of geometry so the 3D half shows the texture in use
    for i, (loc, sc) in enumerate((((0, 0, 0), (3.0, 3.0, 0.4)),
                                   ((-0.9, 0.6, 0.7), (0.9, 0.9, 0.9)),
                                   ((1.0, -0.3, 0.6), (0.7, 0.7, 0.7)))):
        bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
        o = bpy.context.view_layer.objects.active
        o.scale = sc
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        bpy.ops.object.shade_flat()
        o.data.materials.append(mat)

    screen = win().screen
    v3d = max((a for a in screen.areas if a.type == "VIEW_3D"),
              key=lambda a: a.width * a.height)
    with bpy.context.temp_override(window=win(), screen=screen, area=v3d):
        bpy.ops.screen.area_split(direction="VERTICAL", factor=0.5)
    left = min((a for a in screen.areas if a.type == "VIEW_3D"), key=lambda a: a.x)
    left.type = "IMAGE_EDITOR"
    left.spaces.active.image = img
    for a in screen.areas:
        for sp in a.spaces:
            if hasattr(sp, "show_region_ui"):
                sp.show_region_ui = True
    for a in areas("VIEW_3D"):
        a.spaces.active.shading.type = "MATERIAL"
        a.spaces.active.overlay.show_overlays = False
    force_tab()
    for a in areas("IMAGE_EDITOR"):
        in_area(a, bpy.ops.image.view_all, fit_view=True)
    for a in areas("VIEW_3D"):
        bpy.ops.object.select_all(action="SELECT")
        in_area(a, bpy.ops.view3d.view_selected)
        in_area(a, bpy.ops.view3d.view_orbit, angle=math.radians(22), type="ORBITUP")
        bpy.ops.object.select_all(action="DESELECT")

    doc = tex_doc.get(img)
    G.update(img=img, doc=doc, c=doc.canvas, s=s)


def beat(label, fn, frames=3):
    SCRIPT.append((label, fn, frames))


def L():
    return G["c"].layers[G["c"].active]


def stage(label, tool, fn, chunks=5):
    def setup_tool():
        if tool in {"PENCIL", "ERASER", "LINE", "RECT", "ELLIPSE", "FILL", "PICK"}:
            G["s"].tool = tool
        G["s"].status = label
    beat(label, setup_tool, 2)
    hold = {}

    def prep():
        layer = L()
        before = bytearray(layer.px)
        fn()
        hold["after"] = bytearray(layer.px)
        hold["layer"] = layer
        layer.px = before
        hold["ch"] = [i for i in range(len(hold["after"])) if hold["after"][i] != before[i]]
    beat(label, prep, 0)

    for k in range(chunks):
        def rev(k=k):
            ch, layer = hold.get("ch", []), hold.get("layer")
            if not ch:
                return
            per = max(1, len(ch) // chunks)
            hi = (k + 1) * per if k < chunks - 1 else len(ch)
            for i in ch[k * per:hi]:
                layer.px[i] = hold["after"][i]
            G["doc"].flush()
        beat(label, rev, 2)


def op_beat(label, idname, editor="IMAGE_EDITOR", frames=9, **kw):
    def run():
        G["s"].status = label
        for a in areas(editor):
            mod, nm = idname.split(".")
            in_area(a, getattr(getattr(bpy.ops, mod), nm), **kw)
            break
    beat(label, run, frames)


def px(pts, idx):
    for x, y in pts:
        L().set(x, y, idx)


# ------------------------------------------------------------------ scripts
def script_shrine():
    c = G["c"]
    g = [c.add_colour(x) for x in TT.make_ramp((72, 128, 66, 255), 5)]
    stage("Fill the grass base", "FILL",
          lambda: px(R.rect(0, 0, SIZE - 1, SIZE - 1, filled=True), g[1]), 3)
    stage("Dither two greens", "PENCIL", lambda: px(
        [(x, y) for y in range(SIZE) for x in range(SIZE)
         if (x * 7 + y * 13) % 5 < 2], g[2]), 4)
    stage("Scatter highlights", "PENCIL", lambda: px(
        [(x, y) for y in range(SIZE) for x in range(SIZE)
         if (x * 7 + y * 13) % 11 < 2], g[3]), 4)
    stage("Grass blades", "LINE", lambda: [
        px(R.line(bx, by, bx, by - 4), g[4])
        for bx, by in ((6, 14), (21, 7), (38, 19), (52, 11), (13, 41), (44, 50))], 3)
    op_beat("Check Tiling", "texel.check_tileable", frames=14)


def script_corridor():
    c = G["c"]
    def set_base():
        G["s"].colour = (0.38, 0.42, 0.49, 1.0)
        G["s"].status = "Pick one metal colour"
    beat("Pick one metal colour", set_base, 6)
    op_beat("Generate Ramp", "texel.palette_ramp", frames=12, steps=6)
    m = [0] + [c.add_colour(x) for x in TT.make_ramp((96, 106, 124, 255), 6)]
    stage("Fill from the ramp", "FILL",
          lambda: px(R.rect(0, 0, SIZE - 1, SIZE - 1, filled=True), m[3]), 3)
    stage("Panel insets", "RECT", lambda: [
        px(R.rect(gx + 3, gy + 3, gx + 28, gy + 28, filled=True), m[4])
        for gy in range(0, SIZE, 32) for gx in range(0, SIZE, 32)], 4)
    stage("Panel borders", "RECT", lambda: [
        px(R.rect(gx + 2, gy + 2, gx + 29, gy + 29), m[1])
        for gy in range(0, SIZE, 32) for gx in range(0, SIZE, 32)], 3)
    stage("Rivets", "PENCIL", lambda: [
        px([(gx + rx, gy + ry)], m[6])
        for gy in range(0, SIZE, 32) for gx in range(0, SIZE, 32)
        for rx, ry in ((7, 7), (25, 7), (7, 25), (25, 25))], 3)


def script_ruins():
    c = G["c"]
    s = [c.add_colour(x) for x in TT.make_ramp((206, 176, 122, 255), 6)]
    stage("Sandstone base", "FILL",
          lambda: px(R.rect(0, 0, SIZE - 1, SIZE - 1, filled=True), s[1]), 3)
    stage("Lay the blocks", "RECT", lambda: [
        px(R.rect(x + 1, y + 1, x + 30, y + 14, filled=True), s[3])
        for i, y in enumerate(range(0, SIZE, 16))
        for x in range(-32 + (0 if i % 2 == 0 else 16), SIZE, 32)], 4)
    stage("Sun on the top edges", "LINE", lambda: [
        px(R.line(x + 2, y + 2, x + 29, y + 2), s[5])
        for i, y in enumerate(range(0, SIZE, 16))
        for x in range(-32 + (0 if i % 2 == 0 else 16), SIZE, 32)], 3)
    op_beat("Detect Density", "texel.density_detect", editor="VIEW_3D", frames=10)
    def zone_split():
        import bmesh
        G["s"].status = "Zone 2: the small props"
        for o in [x for x in bpy.data.objects if x.type == "MESH"]:
            bm = bmesh.new()
            bm.from_mesh(o.data)
            lay = bm.faces.layers.int.get("texel_zone") or bm.faces.layers.int.new("texel_zone")
            for f in bm.faces:
                f[lay] = 2 if f.calc_area() < 1.5 else 1
            bm.to_mesh(o.data)
            bm.free()
            o.data.update()
    beat("Assign density zones", zone_split, 8)
    op_beat("Props at 40 px/unit", "texel.zone_apply", editor="VIEW_3D",
            frames=10, zone=2, density=40.0)
    op_beat("Density summary", "texel.zone_info", editor="VIEW_3D", frames=12)


def script_tavern():
    c = G["c"]
    w = [c.add_colour(x) for x in TT.make_ramp((146, 98, 54, 255), 6)]
    stage("Plank floor on layer 1", "FILL",
          lambda: px(R.rect(0, 0, SIZE - 1, SIZE - 1, filled=True), w[2]), 3)
    stage("Plank seams", "LINE", lambda: [
        px(R.line(x, 0, x, SIZE - 1), w[0]) or px(R.line(x + 1, 0, x + 1, SIZE - 1), w[4])
        for x in range(0, SIZE, 11)], 4)
    op_beat("Add Layer", "texel.layer_add", frames=7)
    r = [c.add_colour(x) for x in TT.make_ramp((152, 48, 56, 255), 5)]
    stage("Rug on layer 2", "RECT",
          lambda: px(R.rect(10, 12, 53, 51, filled=True), r[2]), 3)
    stage("Woven border", "RECT", lambda: (px(R.rect(13, 15, 50, 48), r[4]),
                                           px(R.rect(16, 18, 47, 45), r[1])), 3)
    op_beat("Hide the rug layer", "texel.layer_toggle", frames=8, index=1)
    op_beat("Show it again", "texel.layer_toggle", frames=8, index=1)
    def swap():
        G["s"].status = "Palette swap: one index, whole canvas"
        G["c"].replace_colour(r[2], (46, 92, 150, 255))
        G["doc"].flush()
    beat("Palette swap to blue", swap, 12)


def script_cavern():
    c = G["c"]
    def mirror_on():
        G["s"].mirror_x = True
        G["s"].status = "Mirror X ON - draw one half"
    beat("Turn on Mirror X", mirror_on, 8)
    cr = [c.add_colour(x) for x in TT.make_ramp((108, 224, 232, 255), 6)]

    def half(pts, idx):
        for x, y in pts:
            if x <= SIZE // 2 - 1:
                L().set(x, y, idx)
                L().set(SIZE - 1 - x, y, idx)

    stage("Crystal body (left half only)", "ELLIPSE",
          lambda: half(R.ellipse_box(2, 6, 61, 57, filled=True), cr[3]), 4)
    stage("Facet lines", "LINE", lambda: (
        half(R.pixel_perfect(R.line(30, 8, 8, 34)), cr[5]),
        half(R.pixel_perfect(R.line(8, 36, 30, 56)), cr[5])), 3)
    stage("Bright core", "ELLIPSE",
          lambda: half(R.ellipse_box(18, 20, 45, 44, filled=True), cr[4]), 3)
    stage("Deep edge", "PENCIL",
          lambda: half(R.ellipse_box(2, 6, 61, 57), cr[1]), 3)
    op_beat("Outline the sprite", "texel.outline_sprite", frames=10)


SCRIPTS = {"shrine": script_shrine, "corridor": script_corridor,
           "ruins": script_ruins, "tavern": script_tavern, "cavern": script_cavern}


def shoot():
    force_tab()
    for a in win().screen.areas:
        a.tag_redraw()
    p = os.path.join(OUT, f"f_{state['n']:04d}.png")
    with bpy.context.temp_override(window=win(), screen=win().screen):
        bpy.ops.screen.screenshot(filepath=p)
    state["n"] += 1


def tick():
    if not state["ready"]:
        setup()
        SCRIPTS[NAME]()
        state["ready"] = True
        for _ in range(6):
            shoot()
        return 0.05
    if state["step"] >= len(SCRIPT):
        seam = TT.tile_seam_score(G["c"].flatten(), SIZE, SIZE, G["c"].palette)
        G["img"].filepath_raw = os.path.join(OUT, f"{NAME}_texture.png")
        G["img"].file_format = "PNG"
        G["img"].save()
        print(f"TEXEL_STEPS_DONE name={NAME} frames={state['n']} "
              f"beats={len(SCRIPT)} colours={len(G['c'].palette)-1} "
              f"seam={seam['score']}", flush=True)
        bpy.ops.wm.quit_blender()
        return None
    label, fn, frames = SCRIPT[state["step"]]
    if state["sub"] == 0:
        try:
            fn()
        except Exception as e:
            print(f"[warn] beat '{label}': {e}", flush=True)
    if state["sub"] < max(1, frames):
        shoot()
        state["sub"] += 1
    else:
        state["step"] += 1
        state["sub"] = 0
    return 0.05


bpy.app.timers.register(tick, first_interval=1.0)
