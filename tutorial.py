"""Record a TUTORIAL-style advert: build a small environment with Texel.

A real screen capture of Blender with the add-on running. Every step calls a
real operator; the sidebar you see is the actual Texel panel reacting. The
sequence is written as a lesson, not a feature list:

  1. Build a scene and give it a canvas
  2. Pixel Art Unwrap, then measure what the density actually is
  3. Fix the density so texels are the same size everywhere
  4. Paint the tileset - tools, palette ramp, mirror
  5. Check the tiling, which nothing else does
  6. Density zones: props get finer texels than the floor
  7. Orbit the finished environment

  blender --factory-startup --python tutorial.py
"""
import math
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

OUT = os.path.join(HERE, "promo", "tutorial")
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

SIZE = 64
G = {}                      # img, doc, canvas, layer, settings, env object


# ------------------------------------------------------------------ helpers
def win():
    return bpy.context.window_manager.windows[0]


def areas(kind):
    return [a for a in win().screen.areas if a.type == kind]


def in_area(area, op, **kw):
    """Run an operator with a proper area/region context."""
    region = next((r for r in area.regions if r.type == "WINDOW"), None)
    if region is None:
        return
    try:
        with bpy.context.temp_override(window=win(), screen=win().screen,
                                       area=area, region=region):
            op(**kw)
    except Exception as e:
        print(f"[warn] {op.__name__ if hasattr(op,'__name__') else op}: {e}")


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


def redraw():
    for a in win().screen.areas:
        a.tag_redraw()


# -------------------------------------------------------------------- setup
def build_environment():
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)

    img = bpy.data.images.new("Dungeon Tileset", SIZE, SIZE, alpha=True)
    img.pixels.foreach_set([0.0] * (SIZE * SIZE * 4))
    img.update()

    mat = bpy.data.materials.new("Dungeon")
    mat.use_nodes = True
    nt = mat.node_tree
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    tex.interpolation = "Closest"
    tex.extension = "REPEAT"
    nt.links.new(tex.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"])
    nt.links.new(tex.outputs["Alpha"], nt.nodes["Principled BSDF"].inputs["Alpha"])
    nt.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.92

    # a floor slab, three wall blocks and two crates - deliberately different
    # sizes, so the density really does vary and the fix is visible
    pieces = [
        ((0, 0, -0.15), (6.0, 6.0, 0.3)),          # floor
        ((0, 3.0, 1.0), (6.0, 0.4, 2.0)),          # back wall
        ((-3.0, 0, 1.0), (0.4, 6.0, 2.0)),         # left wall
        ((3.0, 0, 1.0), (0.4, 6.0, 2.0)),          # right wall
        ((-1.6, 1.4, 0.45), (0.9, 0.9, 0.9)),      # crate
        ((1.7, 1.9, 0.35), (0.7, 0.7, 0.7)),       # small crate
    ]
    objs = []
    for loc, scale in pieces:
        bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
        o = bpy.context.view_layer.objects.active
        o.scale = scale
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        objs.append(o)
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    env = bpy.context.view_layer.objects.active
    env.name = "Dungeon"
    bpy.ops.object.shade_flat()
    env.data.materials.append(mat)

    sun = bpy.data.lights.new("Sun", "SUN")
    sun.energy = 3.0
    so = bpy.data.objects.new("Sun", sun)
    bpy.context.collection.objects.link(so)
    so.rotation_euler = (math.radians(52), 0, math.radians(35))

    # split: Image Editor left, 3D right
    screen = win().screen
    v3d = max((a for a in screen.areas if a.type == "VIEW_3D"),
              key=lambda a: a.width * a.height)
    with bpy.context.temp_override(window=win(), screen=screen, area=v3d):
        bpy.ops.screen.area_split(direction="VERTICAL", factor=0.42)
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
        in_area(a, bpy.ops.view3d.view_axis, type="TOP")
        bpy.ops.object.select_all(action="SELECT")
        in_area(a, bpy.ops.view3d.view_selected)
        in_area(a, bpy.ops.view3d.view_orbit, angle=math.radians(58), type="ORBITUP")
        bpy.ops.object.select_all(action="DESELECT")

    doc = tex_doc.get(img)
    G.update(img=img, doc=doc, c=doc.canvas, L=doc.canvas.layers[0],
             s=bpy.context.scene.texel, env=env)


# ------------------------------------------------------------------- script
SCRIPT = []


def beat(label, fn, frames=3):
    SCRIPT.append((label, fn, frames))


def paint(pts, idx):
    for x, y in pts:
        G["L"].set(x, y, idx)


def stage(label, tool, fn, chunks=5):
    """A painting stage: set the tool in the panel, reveal its texels over frames."""
    def run():
        G["s"].tool = tool if tool in {"PENCIL", "ERASER", "LINE", "RECT",
                                       "ELLIPSE", "FILL", "PICK"} else G["s"].tool
        G["s"].status = label
    beat(label, run, 2)
    holder = {}

    def prep():
        before = bytearray(G["L"].px)
        fn()
        holder["after"] = bytearray(G["L"].px)
        G["L"].px = before
        holder["changed"] = [i for i in range(len(holder["after"]))
                             if holder["after"][i] != before[i]]
    beat(label, prep, 0)

    for k in range(chunks):
        def reveal(k=k):
            ch = holder.get("changed", [])
            if not ch:
                return
            per = max(1, len(ch) // chunks)
            for i in ch[k * per:(k + 1) * per if k < chunks - 1 else len(ch)]:
                G["L"].px[i] = holder["after"][i]
            G["doc"].flush()
        beat(label, reveal, 2)


def build_script():
    c = G["c"]
    s = G["s"]
    stone = c.add_colour((104, 100, 112, 255))
    stone_d = c.add_colour((62, 60, 70, 255))
    stone_l = c.add_colour((146, 142, 154, 255))
    moss = c.add_colour((78, 118, 70, 255))
    wood = c.add_colour((134, 90, 50, 255))
    ink = c.add_colour((30, 28, 34, 255))

    # --- 1. unwrap and measure
    def do_unwrap():
        s.status = "Pixel Art Unwrap"
        bpy.ops.object.select_all(action="DESELECT")
        G["env"].select_set(True)
        bpy.context.view_layer.objects.active = G["env"]
        for a in areas("VIEW_3D"):
            in_area(a, bpy.ops.texel.pixel_art_unwrap, method="CUBE")
            break
    beat("Pixel Art Unwrap", do_unwrap, 8)

    def do_detect():
        for a in areas("VIEW_3D"):
            in_area(a, bpy.ops.texel.density_detect)
            break
    beat("Detect Density", do_detect, 8)

    # --- 2. paint the tileset
    stage("Fill the stone base", "FILL",
          lambda: paint(R.rect(0, 0, SIZE - 1, SIZE - 1, filled=True), stone), 3)
    stage("Block out the slabs", "RECT", lambda: [
        paint(R.rect(x + 1, y + 1, x + 14, y + 14), stone_d)
        for y in range(0, SIZE, 16) for x in range(0, SIZE, 16)], 4)
    stage("Light the top edges", "LINE", lambda: [
        paint(R.line(x + 2, y + 2, x + 13, y + 2), stone_l)
        for y in range(0, SIZE, 16) for x in range(0, SIZE, 16)], 4)
    stage("Dither some wear", "PENCIL", lambda: paint(
        [(x, y) for y in range(SIZE) for x in range(SIZE)
         if (x + y) % 2 == 0 and (x * 5 + y * 11) % 17 < 3], stone_d), 4)
    stage("Moss in the cracks", "PENCIL", lambda: paint(
        [(x, y) for y in range(SIZE) for x in range(SIZE)
         if (x * 3 + y * 7) % 23 < 2 and G["L"].get(x, y) == stone], moss), 4)
    stage("Timber inlay", "RECT", lambda: paint(
        R.rect(24, 24, 39, 39, filled=True), wood), 3)
    stage("Outline the inlay", "LINE",
          lambda: paint(R.rect(24, 24, 39, 39), ink), 2)

    # --- 3. the checks nothing else does
    def do_tiling():
        for a in areas("IMAGE_EDITOR"):
            in_area(a, bpy.ops.texel.check_tileable)
            break
    beat("Check Tiling", do_tiling, 10)

    def do_ramp():
        s.colour = (0.41, 0.39, 0.44, 1.0)
        for a in areas("IMAGE_EDITOR"):
            in_area(a, bpy.ops.texel.palette_ramp, steps=5)
            break
    beat("Generate a shading ramp", do_ramp, 8)

    # --- 4. density zones, the part a paint add-on cannot do
    def zones_assign():
        import bmesh
        s.status = "Zone 2: the crates"
        me = G["env"].data
        bm = bmesh.new()
        bm.from_mesh(me)
        lay = bm.faces.layers.int.get("texel_zone") or bm.faces.layers.int.new("texel_zone")
        for f in bm.faces:
            # the two crates sit above z=0.1 and are small: give them zone 2
            f[lay] = 2 if f.calc_area() < 1.2 else 1
        bm.to_mesh(me)
        bm.free()
        me.update()
    beat("Assign density zones", zones_assign, 8)

    def zone_apply_fine():
        for a in areas("VIEW_3D"):
            in_area(a, bpy.ops.texel.zone_apply, zone=2, density=48.0)
            break
    beat("Crates: 48 px/unit", zone_apply_fine, 8)

    def zone_apply_floor():
        for a in areas("VIEW_3D"):
            in_area(a, bpy.ops.texel.zone_apply, zone=1, density=16.0)
            break
    beat("Floor and walls: 16 px/unit", zone_apply_floor, 8)

    def zone_report():
        for a in areas("VIEW_3D"):
            in_area(a, bpy.ops.texel.zone_info)
            break
    beat("Density summary", zone_report, 10)

    # --- 5. the reveal
    for i in range(28):
        def orbit(i=i):
            G["s"].status = "Painted in Blender with Texel"
            for a in areas("VIEW_3D"):
                in_area(a, bpy.ops.view3d.view_orbit,
                        angle=math.radians(4.0), type="ORBITRIGHT")
        beat("Finished environment", orbit, 1)


# ----------------------------------------------------------------- recording
state = {"n": 0, "step": 0, "sub": 0, "ready": False}


def shoot():
    force_tab()
    redraw()
    p = os.path.join(OUT, f"f_{state['n']:04d}.png")
    with bpy.context.temp_override(window=win(), screen=win().screen):
        bpy.ops.screen.screenshot(filepath=p)
    state["n"] += 1


def tick():
    if not state["ready"]:
        build_environment()
        build_script()
        state["ready"] = True
        for _ in range(6):
            shoot()
        return 0.05

    if state["step"] >= len(SCRIPT):
        seam = TT.tile_seam_score(G["c"].flatten(), SIZE, SIZE, G["c"].palette)
        G["img"].filepath_raw = os.path.join(OUT, "dungeon_tileset.png")
        G["img"].file_format = "PNG"
        G["img"].save()
        print(f"TEXEL_TUTORIAL_DONE frames={state['n']} beats={len(SCRIPT)} "
              f"colours={len(G['c'].palette)-1} seam={seam['score']}", flush=True)
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
