"""Screen-record the features that arrived after the first cut of the videos.

Real Blender GUI, real operators, real sidebar - the same harness as
steps_env.py, pointed at the new ground:

  anim      frames, tracks, cels, onion skin, bind to the timeline, scrub, GIF
  sprite    reference layer, brush shapes, layer opacity, trim, colour count
  showcase  pick a light and a camera move, set it up, render the still

  blender --factory-startup --python steps_anim.py -- anim

Writes PNG frames into promo/steps/<name>/; assemble with build_videos.sh.
"""
import math
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["anim"]
NAME = argv[0]

OUT = os.path.join(HERE, "promo", "steps", NAME)
os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT):
    os.remove(os.path.join(OUT, f))

import texel
from texel import tex_doc
from texel.core import raster as R

try:
    texel.register()
except Exception:
    pass
try:
    bpy.context.preferences.view.show_splash = False       # or it covers frame 1
except Exception:
    pass

import demo_art as A

SIZE = A.SIZE
FRAMES = 4                      # a 4-wide cel grid stays legible in the sidebar
G = {}
SCRIPT = []
state = {"n": 0, "step": 0, "sub": 0, "ready": False}


def win():
    return bpy.context.window_manager.windows[0]          # context.window is None
    #                                                       inside a timer


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
    """Re-assert every frame: the regions are not laid out yet at setup time."""
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


def base_setup(image_only):
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    s = bpy.context.scene.texel
    img = bpy.data.images.new("Torchbearer", SIZE, SIZE, alpha=True)
    img.pixels.foreach_set([0.0] * (SIZE * SIZE * 4))
    img.update()
    screen = win().screen
    v3d = max((a for a in screen.areas if a.type == "VIEW_3D"),
              key=lambda a: a.width * a.height)
    if image_only:
        v3d.type = "IMAGE_EDITOR"
        v3d.spaces.active.image = img
    else:
        with bpy.context.temp_override(window=win(), screen=screen, area=v3d):
            bpy.ops.screen.area_split(direction="VERTICAL", factor=0.42)
        left = min((a for a in screen.areas if a.type == "VIEW_3D"),
                   key=lambda a: a.x)
        left.type = "IMAGE_EDITOR"
        left.spaces.active.image = img
    for a in screen.areas:
        for sp in a.spaces:
            if hasattr(sp, "show_region_ui"):
                sp.show_region_ui = True
    force_tab()
    for a in areas("IMAGE_EDITOR"):
        in_area(a, bpy.ops.image.view_all, fit_view=True)
    doc = tex_doc.get(img)
    G.update(img=img, doc=doc, c=doc.canvas, s=s, P=A.palette(doc.canvas))
    return s


def beat(label, fn, frames=3):
    SCRIPT.append((label, fn, frames))


def op_beat(label, idname, editor="IMAGE_EDITOR", frames=8, **kw):
    def run():
        G["s"].status = label
        for a in areas(editor):
            mod, nm = idname.split(".")
            in_area(a, getattr(getattr(bpy.ops, mod), nm), **kw)
            break
    beat(label, run, frames)


def reveal(label, cel_of, draw, chunks=4, frames=2):
    """Play a drawing on in chunks, so it looks painted rather than pasted."""
    hold = {}

    def prep():
        G["s"].status = label
        cel = cel_of()
        before = bytearray(cel.px)
        draw(cel)
        hold["after"] = bytearray(cel.px)
        hold["cel"] = cel
        cel.px = before
        hold["ch"] = [i for i in range(len(before)) if hold["after"][i] != before[i]]
    beat(label, prep, 0)

    for k in range(chunks):
        def rev(k=k):
            ch, cel = hold.get("ch", []), hold.get("cel")
            if not ch:
                return
            per = max(1, len(ch) // chunks)
            hi = (k + 1) * per if k < chunks - 1 else len(ch)
            for i in ch[k * per:hi]:
                cel.px[i] = hold["after"][i]
            G["doc"].flush()
        beat(label, rev, frames)


# ------------------------------------------------------------------ scripts
def script_anim():
    c, P = G["c"], G["P"]
    G["s"].tool = "PENCIL"

    # ---- frame 1, on the seeded Main track
    op_beat("Add a frame", "texel.frame_add", frames=6, copy_previous=False)
    reveal("Draw the character", lambda: c.cel("Main", 0),
           lambda cel: A.draw_char(cel, P, 0), chunks=5)

    # ---- a background track, sent behind
    op_beat("Add a track for the cave", "texel.track_add", frames=8,
            name="Cave", bottom=True)
    reveal("Paint the cave on its own cel", lambda: c.cel("Cave", 0),
           lambda cel: A.draw_cave(cel, P, 0), chunks=5)

    # ---- a light track, added on top then moved behind him
    op_beat("Add a track for the torchlight", "texel.track_add", frames=6,
            name="Glow")
    op_beat("Move it behind the character", "texel.track_move", frames=8,
            name="Glow", delta=-1)
    reveal("The light warms the stone it falls on", lambda: c.cel("Glow", 0),
           lambda cel: A.draw_glow(cel, c.cel("Cave", 0), P, 0), chunks=4)

    # ---- the flame, on top
    op_beat("And the flame on top", "texel.track_add", frames=6, name="Torch")
    reveal("One frame, four drawings", lambda: c.cel("Torch", 0),
           lambda cel: A.draw_torch(cel, P, 0), chunks=2)

    # ---- three more frames, each a full four-cel set
    for f in range(1, FRAMES):
        op_beat(f"Frame {f + 1}", "texel.frame_add", frames=4,
                copy_previous=False)

        def paint(f=f):
            G["s"].status = f"Frame {f + 1}: every track gets a cel"
            for t in A.TRACKS:
                cels = {k: c.cel(k, f) for k in A.TRACKS}
                A.DRAW[t](cels, P, f)
            c.show_frame(f, onion=False)
            G["doc"].flush()
        beat(f"Frame {f + 1}", paint, 6)

    # ---- onion skin, scoped to the character
    def onion_on():
        G["s"].onion_skin = True
        cel = c.cel("Main", 2)
        c.active = c.layers.index(cel)
        c.show_frame(2, onion=True, track="Main")
        G["doc"].flush()
        G["s"].status = "Onion skin: where he was, not where the wall was"
    beat("Onion skin", onion_on, 12)

    def onion_off():
        G["s"].onion_skin = False
        c.show_frame(0, onion=False)
        G["doc"].flush()
    beat("Onion skin off", onion_off, 3)

    # ---- timing, then bind to Blender's own timeline
    for i, h in ((0, 2), (2, 2)):
        op_beat(f"Hold frame {i + 1} for {h}", "texel.frame_hold", frames=5,
                index=i, hold=h)
    op_beat("Bind to the timeline", "texel.anim_bind", frames=12)

    # ---- scrub it. This is the shot: Blender's playhead drives the sprite.
    total = FRAMES + 2                      # the two holds set just above
    for loop in range(3):
        for n in range(1, total + 1):
            def scrub(n=n):
                sc = bpy.context.scene
                sc.frame_current = n
                for h in bpy.app.handlers.frame_change_post:
                    if getattr(h, "__name__", "") == "_on_frame":
                        h(sc)
                sc.texel.status = f"Playing - timeline frame {n} of {total}"
            beat("Play", scrub, 2)

    op_beat("Export GIF", "texel.export_gif", frames=16, scale=6, directory=OUT)


def script_sprite():
    c, P = G["c"], G["P"]
    G["s"].tool = "PENCIL"

    # ---- a reference image to trace over, faint and locked
    ref = bpy.data.images.new("_ref", SIZE, SIZE, alpha=True)
    scratch = tex_doc.get(bpy.data.images.new("_scratch", SIZE, SIZE, alpha=True))
    A.draw_char(scratch.canvas.layers[0], A.palette(scratch.canvas), 0)
    ref.pixels.foreach_set(scratch.canvas.to_blender_floats())
    path = os.path.join(OUT, "_reference.png")
    ref.filepath_raw, ref.file_format = path, "PNG"
    ref.save()
    op_beat("Drop in a reference to trace", "texel.reference_add", frames=12,
            filepath=path, opacity=0.35)

    # ---- brush shapes
    for shape, xs in (("SQUARE", 8), ("ROUND", 26), ("DIAMOND", 44)):
        def swatch(shape=shape, xs=xs):
            G["s"].brush_shape = shape
            G["s"].brush_size = 7
            G["s"].status = f"Brush: {shape.title()}, 7 across"
            layer = c.layers[c.active]
            for dx, dy in R.brush_mask(7, shape):
                layer.set(xs + dx, 12 + dy, P["fire"][3])
            G["doc"].flush()
        beat(f"Brush shape: {shape.title()}", swatch, 8)

    def wipe():
        layer = c.layers[c.active]
        layer.px = bytearray(SIZE * SIZE)
        G["doc"].flush()
        G["s"].status = "Trace it"
    beat("Clear", wipe, 2)

    reveal("Trace over the reference", lambda: c.layers[c.active],
           lambda cel: A.draw_char(cel, P, 0), chunks=6)

    op_beat("Drop the reference", "texel.reference_remove", frames=6)
    op_beat("Count the colours", "texel.colour_count", frames=14, limit=32)

    def fade():
        G["s"].status = "Layer opacity, for a ghost or a shadow pass"
    beat("Layer opacity", fade, 2)
    for v in (0.8, 0.6, 0.4, 0.25, 0.4, 0.6, 0.8, 1.0):
        op_beat(f"Opacity {v:.2f}", "texel.layer_opacity", frames=2, value=v)

    op_beat("Trim to the artwork", "texel.trim", frames=16, margin=1)


def script_showcase():
    c, P = G["c"], G["P"]
    cel = c.layers[c.active]
    # a SEAMLESS sandstone tile, not a scene: this is what goes on geometry.
    # The cave ramp is too low-contrast to survive being lit - on geometry it
    # washes out to flat lavender, which is exactly the mistake Texel exists to
    # let you see before you commit to it.
    sand = [c.add_colour(x) for x in
            __import__("texel").core.tools.make_ramp((198, 166, 116, 255), 5)]
    BW, BH = 16, 8
    A.fill(cel, R.rect(0, 0, SIZE - 1, SIZE - 1, filled=True), sand[0])
    for row, wy in enumerate(range(0, SIZE, BH)):
        off = (row % 2) * (BW // 2)
        for n, bx in enumerate(range(-BW, SIZE + BW, BW)):
            x0 = bx + off
            body = sand[3] if (row * 5 + n * 3) % 4 else sand[2]
            A.fill(cel, R.rect(x0 + 1, wy + 1, x0 + BW - 1, wy + BH - 1,
                               filled=True), body)
            A.fill(cel, R.line(x0 + 1, wy + 1, x0 + BW - 1, wy + 1), sand[4])
            A.fill(cel, R.line(x0 + 1, wy + BH - 1, x0 + BW - 1, wy + BH - 1),
                   sand[1])
    for bx, by in ((6, 4), (29, 12), (46, 21), (14, 29), (53, 37), (23, 45),
                   (39, 53), (10, 60)):                    # chips and pits
        A.fill(cel, R.ellipse_box(bx, by, bx + 2, by + 1, filled=True), sand[1])
        cel.set(bx + 1, by - 1, sand[4])
    G["doc"].flush()

    # a block of geometry wearing the texture
    mat = bpy.data.materials.new("M")
    mat.use_nodes = True
    nt = mat.node_tree
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = G["img"]
    tex.interpolation = "Closest"
    nt.links.new(tex.outputs["Color"],
                 nt.nodes["Principled BSDF"].inputs["Base Color"])
    for loc, sc in (((0, 0, 0), (3.0, 3.0, 0.4)), ((-0.9, 0.6, 0.7), (0.9,) * 3),
                    ((1.0, -0.3, 0.6), (0.7,) * 3)):
        bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
        o = bpy.context.view_layer.objects.active
        o.scale = sc
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        bpy.ops.object.shade_flat()
        o.data.materials.append(mat)
    for a in areas("VIEW_3D"):
        sh = a.spaces.active.shading
        sh.type = "MATERIAL"
        # EEVEE preview lit by the ACTUAL showcase lights, so switching preset
        # is visible instantly instead of waiting on a Cycles render
        sh.use_scene_lights = True
        sh.use_scene_world = True
        a.spaces.active.overlay.show_overlays = False
        bpy.ops.object.select_all(action="SELECT")
        in_area(a, bpy.ops.view3d.view_selected)
        in_area(a, bpy.ops.view3d.view_orbit, angle=math.radians(20),
                type="ORBITUP")
        bpy.ops.object.select_all(action="DESELECT")

    for preset, move in (("ICE", "PUSH"), ("COOL", "ARC"), ("GOLDEN", "ORBIT")):
        def pick(preset=preset, move=move):
            G["s"].showcase_preset = preset
            G["s"].showcase_move = move
            G["s"].status = f"{preset.title()} light, {move.title()} move"
        beat(f"{preset.title()} / {move.title()}", pick, 7)
        op_beat(f"Set up {preset.title()}", "texel.showcase_setup",
                editor="VIEW_3D", frames=10)
    def still():
        G["s"].showcase_move = "STILL"
        G["s"].showcase_samples = 48
        G["s"].showcase_width, G["s"].showcase_height = 960, 540
        G["s"].showcase_output = OUT + os.sep
        G["s"].status = "Render the still"
    beat("Render the still", still, 6)
    op_beat("Rendering", "texel.showcase_render", editor="VIEW_3D", frames=4)

    def load_result():
        p = os.path.join(OUT, "showcase_0000.png")
        if not os.path.exists(p):
            return
        r = bpy.data.images.load(p, check_existing=True)
        for a in areas("IMAGE_EDITOR"):
            a.spaces.active.image = r
            in_area(a, bpy.ops.image.view_all, fit_view=True)
        G["s"].status = "Your asset, presented"
    beat("Your asset, presented", load_result, 22)


SCRIPTS = {"anim": (script_anim, True),
           "sprite": (script_sprite, True),
           "showcase": (script_showcase, False)}


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
        fn, image_only = SCRIPTS[NAME]
        base_setup(image_only)
        fn()
        state["ready"] = True
        for _ in range(6):
            shoot()
        return 0.05
    if state["step"] >= len(SCRIPT):
        G["img"].filepath_raw = os.path.join(OUT, f"{NAME}_result.png")
        G["img"].file_format = "PNG"
        G["img"].save()
        print(f"TEXEL_STEPS_DONE name={NAME} frames={state['n']} "
              f"beats={len(SCRIPT)} tracks={len(G['c'].tracks)} "
              f"cels={sum(1 for l in G['c'].layers if l.frame is not None)}",
              flush=True)
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
