"""Record a REAL screen capture of Texel being used in Blender, for the store page.

This is not an animation of artwork appearing. Blender runs with its actual GUI,
the Texel sidebar is open, every step calls a real operator, and each frame is
`bpy.ops.screen.screenshot()` of the whole window. What you see is the add-on.

  blender --python promo.py -- sword
  blender --python promo.py -- shield

Run with a normal (non-background) Blender: it needs a window to photograph.
"""
import math
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["sword"]
SUBJECT = argv[0]
SIZE = 32

OUT = os.path.join(HERE, "promo", SUBJECT)
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

# The startup splash covers the whole UI and would sit in every frame. Turning
# it off at import time works; dismissing it later does not, and calling
# read_homefile from a timer crashes Blender.
try:
    bpy.context.preferences.view.show_splash = False
except Exception:
    pass


# ------------------------------------------------------------------ workspace
def setup():
    # NEVER call read_factory_settings from a timer: it frees the screen the
    # timer is running on and Blender dies with an access violation. Blender is
    # already launched with --factory-startup, so just clear the default objects.
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    s = bpy.context.scene.texel

    img = bpy.data.images.new(f"{SUBJECT.title()}", SIZE, SIZE, alpha=True)
    img.pixels.foreach_set([0.0] * (SIZE * SIZE * 4))
    img.update()

    mat = bpy.data.materials.new("M")
    mat.use_nodes = True
    nt = mat.node_tree
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    tex.interpolation = "Closest"
    nt.links.new(tex.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"])
    nt.links.new(tex.outputs["Alpha"], nt.nodes["Principled BSDF"].inputs["Alpha"])

    bpy.ops.mesh.primitive_plane_add(size=2, rotation=(math.radians(90), 0, 0))
    obj = bpy.context.view_layer.objects.active   # active_object is not bound
    obj.name = SUBJECT.title()                    # this early in startup
    obj.data.materials.append(mat)

    # split the main area: Image Editor on the left, 3D viewport on the right.
    # A timer callback has no window in its context, so take it from the window
    # manager rather than bpy.context.window (which is None here).
    win = bpy.context.window_manager.windows[0]
    screen = win.screen
    v3d = max((a for a in screen.areas if a.type == "VIEW_3D"),
              key=lambda a: a.width * a.height)
    with bpy.context.temp_override(window=win, screen=screen, area=v3d):
        bpy.ops.screen.area_split(direction="VERTICAL", factor=0.55)
    left = min((a for a in screen.areas if a.type == "VIEW_3D"), key=lambda a: a.x)
    left.type = "IMAGE_EDITOR"
    left.spaces.active.image = img

    # open every N-sidebar and put it on the Texel tab
    for area in screen.areas:
        for space in area.spaces:
            if hasattr(space, "show_region_ui"):
                space.show_region_ui = True
    for area in screen.areas:
        if area.type == "VIEW_3D":
            area.spaces.active.shading.type = "MATERIAL"
            area.spaces.active.overlay.show_overlays = False

    # Put every sidebar on the Texel tab. `Region.active_panel_category` is the
    # only way to do this - there is no space-level property for it.
    for area in screen.areas:
        for region in area.regions:
            if region.type == "UI":
                try:
                    region.active_panel_category = "Texel"
                except Exception:
                    pass

    # Frame both editors, or the sprite sits 20px wide in a corner.
    for area in screen.areas:
        win_region = next((r for r in area.regions if r.type == "WINDOW"), None)
        if win_region is None:
            continue
        try:
            with bpy.context.temp_override(window=win, screen=screen, area=area,
                                           region=win_region):
                if area.type == "IMAGE_EDITOR":
                    bpy.ops.image.view_all(fit_view=True)
                elif area.type == "VIEW_3D":
                    bpy.ops.object.select_all(action="SELECT")
                    bpy.ops.view3d.view_axis(type="FRONT")   # face-on, not skewed
                    bpy.ops.view3d.view_selected()
                    bpy.ops.object.select_all(action="DESELECT")
        except Exception as e:
            print(f"[warn] could not frame {area.type}: {e}")

    doc = tex_doc.get(img)
    return img, doc, s


IMG = DOC = S = C = L = None


def px(pts, idx):
    for x, y in pts:
        L.set(x, y, idx)


# --------------------------------------------------------------------- steps
def sword_steps():
    """Each step sets a REAL tool in the panel, then does what that tool does."""
    steel = C.add_colour((176, 184, 198, 255))
    edge = C.add_colour((232, 238, 246, 255))
    dark = C.add_colour((96, 102, 116, 255))
    gold = C.add_colour((214, 170, 58, 255))
    grip = C.add_colour((104, 68, 40, 255))
    ink = C.add_colour((26, 24, 30, 255))

    yield "RECT", "Blade", lambda: px(R.rect(14, 3, 17, 20, filled=True), steel)
    yield "PENCIL", "Tip", lambda: px([(15, 2), (16, 2), (15, 1), (16, 1)], steel)
    yield "LINE", "Edge highlight", lambda: px(R.line(15, 2, 15, 19), edge)
    yield "LINE", "Shadow side", lambda: px(R.line(17, 3, 17, 20), dark)
    yield "RECT", "Crossguard", lambda: px(R.rect(8, 21, 23, 23, filled=True), gold)
    yield "RECT", "Grip", lambda: px(R.rect(14, 24, 17, 29, filled=True), grip)
    yield "ELLIPSE", "Pommel", lambda: px(R.ellipse_box(13, 28, 18, 31, filled=True), gold)
    yield "PENCIL", "Grip wrap", lambda: px(
        [(x, y) for y in (25, 27) for x in range(14, 18)], ink)
    yield "OUTLINE", "Outline sprite", lambda: px(TT.outline_points(L), ink)


def shield_steps():
    """The shield shows MIRROR X: only the left half is ever drawn."""
    wood = C.add_colour((132, 88, 48, 255))
    wood_d = C.add_colour((88, 56, 30, 255))
    iron = C.add_colour((150, 156, 168, 255))
    gold = C.add_colour((214, 170, 58, 255))
    red = C.add_colour((176, 54, 58, 255))
    ink = C.add_colour((26, 24, 30, 255))

    def mirrored(pts, idx):
        """Draw on the left, mirror to the right - what Mirror X does live."""
        for x, y in pts:
            L.set(x, y, idx)
            L.set(SIZE - 1 - x, y, idx)

    yield "ELLIPSE", "Shield body", lambda: mirrored(
        [(x, y) for x, y in R.ellipse_box(4, 2, 27, 24, filled=True) if x <= 15], wood)
    yield "PENCIL", "Taper to a point", lambda: mirrored(
        [(x, y) for y in range(20, 31) for x in range(4 + (y - 20), 16)
         if abs(x - 15.5) < 12 - (y - 20)], wood)
    yield "LINE", "Plank seams", lambda: mirrored(
        [p for n in (9, 13) for p in R.line(n, 3, n, 29)], wood_d)
    yield "RECT", "Iron band", lambda: mirrored(
        [(x, y) for x, y in R.rect(3, 9, 15, 11, filled=True) if L.get(x, y)], iron)
    yield "ELLIPSE", "Boss", lambda: mirrored(
        [(x, y) for x, y in R.ellipse_box(11, 12, 20, 21, filled=True) if x <= 15], gold)
    yield "FILL", "Heraldry", lambda: mirrored(
        [(x, y) for x, y in R.ellipse_box(13, 14, 18, 19, filled=True) if x <= 15], red)
    yield "OUTLINE", "Outline sprite", lambda: px(TT.outline_points(L), ink)


STEPS = []

# ------------------------------------------------------------------ recording
CHUNKS = 5          # frames each step is revealed over
HOLD_START = 6
HOLD_END = 16
state = {"n": 0, "i": 0, "queue": []}


def force_texel_tab(screen):
    """Re-assert the sidebar tab every frame.

    Setting `active_panel_category` once during setup does NOT stick: the UI
    regions have not been laid out yet, so the assignment is discarded. Writing
    it each frame is cheap and is the only thing that reliably holds it.
    """
    for area in screen.areas:
        if area.type not in {"IMAGE_EDITOR", "VIEW_3D"}:
            continue
        for region in area.regions:
            if region.type == "UI" and region.active_panel_category != "Texel":
                try:
                    region.active_panel_category = "Texel"
                    region.tag_redraw()
                except Exception:
                    pass


def shoot():
    p = os.path.join(OUT, f"f_{state['n']:04d}.png")
    win = bpy.context.window_manager.windows[0]
    force_texel_tab(win.screen)
    with bpy.context.temp_override(window=win, screen=win.screen):
        bpy.ops.screen.screenshot(filepath=p)
    state["n"] += 1


def push_step(tool, label, fn):
    """Set the panel to the tool this step uses, then reveal its texels."""
    before = bytearray(L.px)
    fn()
    after = bytearray(L.px)
    L.px = bytearray(before)
    changed = [i for i in range(len(after)) if after[i] != before[i]]
    if not changed:
        return
    if tool in {"PENCIL", "LINE", "RECT", "ELLIPSE", "FILL"}:
        S.tool = tool
    S.mirror_x = (SUBJECT == "shield" and tool != "OUTLINE")
    S.status = f"{label}"
    per = max(1, len(changed) // CHUNKS)
    for k in range(0, len(changed), per):
        state["queue"].append((changed[k:k + per], after))


def prepare():
    """Everything that needs a live context. Called from the first timer tick,
    because at --python time bpy.context is only partly populated."""
    global IMG, DOC, S, C, L, STEPS
    IMG, DOC, S = setup()
    C = DOC.canvas
    L = C.layers[0]
    STEPS = list(shield_steps() if SUBJECT == "shield" else sword_steps())
    for tool, label, fn in STEPS:
        push_step(tool, label, fn)


def tick():
    if state["i"] == 0 and not state["queue"]:
        prepare()
    if state["i"] < HOLD_START:
        state["i"] += 1
        shoot()
        return 0.08
    j = state["i"] - HOLD_START
    if j < len(state["queue"]):
        idxs, after = state["queue"][j]
        for i in idxs:
            L.px[i] = after[i]
        DOC.flush()
        IMG.update()
        for area in bpy.context.window_manager.windows[0].screen.areas:
            area.tag_redraw()
        state["i"] += 1
        shoot()
        return 0.08
    if j < len(state["queue"]) + HOLD_END:
        state["i"] += 1
        shoot()
        return 0.08
    seam = TT.tile_seam_score(C.flatten(), C.w, C.h, C.palette)
    print(f"TEXEL_PROMO_DONE frames={state['n']} colours={len(C.palette)-1} "
          f"steps={len(STEPS)} seam={seam['score']}", flush=True)
    IMG.filepath_raw = os.path.join(OUT, f"{SUBJECT}.png")
    IMG.file_format = "PNG"
    IMG.save()
    bpy.ops.wm.quit_blender()
    return None


bpy.app.timers.register(tick, first_interval=1.2)
