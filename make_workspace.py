"""Build `workspace.blend` — the layout a buyer opens into. BUILD STEP, not shipped code.

The comparable add-on ships four prebuilt `workspace_*.blend` files and appends
one at runtime. Having fought the alternative, the reason is obvious: composing
a screen layout live means `area_split`, a workspace switch and a scene edit all
inside one operator, and Blender does not process any of them until the operator
returns. Every read after a change is stale. That path produced a bug that
renamed the user's own Layout workspace and stranded them on "Layout.001".

Appending a WorkSpace datablock is one atomic call with nothing to get wrong. So
this script composes the layout ONCE, here, in a real GUI where the operators
behave, and saves it. Runtime just appends it.

  blender --factory-startup --python make_workspace.py

Writes `workspace.blend` next to this file. Re-run it whenever the layout
changes; the result is deterministic, so the diff is meaningful.
"""
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

import guikit
import texel

OUT = os.path.join(HERE, "workspace.blend")
WS_NAME = "Texel"


def register(ctx):
    try:
        texel.register()
    except Exception:
        pass
    ctx.check("add-on registered", hasattr(bpy.ops.texel, "canvas_new"))
    return 0.3


def build_workspace(ctx):
    """Duplicate the current workspace and lay it out for pixel work."""
    before = {w.as_pointer() for w in bpy.data.workspaces}
    bpy.ops.workspace.duplicate()
    made = [w for w in bpy.data.workspaces if w.as_pointer() not in before]
    ctx.check("a workspace was duplicated", len(made) == 1, len(made))
    if not made:
        return None
    ws = made[0]
    ws.name = WS_NAME
    guikit.win().workspace = ws
    ctx.data["ws"] = ws
    return 0.4                     # let Blender switch before touching the screen


def split_vertical(ctx):
    """Cut the viewport in two. Nothing may be READ about the result yet:
    `area_split` returns before Blender repositions anything, so a.x is stale
    until the next redraw - which is why this is its own step."""
    ws = ctx.data["ws"]
    screen = ws.screens[0]
    ctx.data["screen"] = screen
    v3ds = [a for a in screen.areas if a.type == "VIEW_3D"]
    ctx.check("the duplicate has a 3D viewport", bool(v3ds))
    if not v3ds:
        return None
    big = max(v3ds, key=lambda a: a.width * a.height)
    guikit.in_area(big, lambda: bpy.ops.screen.area_split(
        direction="VERTICAL", factor=0.46), screen=screen)
    return 0.4


def convert_left(ctx):
    """NOW the geometry is real. Canvas goes on the left, by measurement."""
    screen = ctx.data["screen"]
    pair = [a for a in screen.areas if a.type == "VIEW_3D"]
    ctx.check("two viewports after the split", len(pair) >= 2, len(pair))
    left = min(pair, key=lambda a: a.x)
    left.type = "IMAGE_EDITOR"
    ctx.data["left_x"] = left.x
    ctx.note(f"canvas at x={left.x}, model at x={max(a.x for a in pair)}")
    guikit.in_area(left, lambda: bpy.ops.screen.area_split(
        direction="HORIZONTAL", factor=0.80), screen=screen)
    return 0.4


def dress(ctx):
    screen = ctx.data["screen"]
    col = [a for a in screen.areas
           if a.type == "IMAGE_EDITOR" and abs(a.x - ctx.data["left_x"]) < 4]
    if len(col) > 1:
        bottom = min(col, key=lambda a: a.y)
        bottom.type = "DOPESHEET_EDITOR"
        bottom.spaces.active.mode = "TIMELINE"

    for area in screen.areas:
        sp = area.spaces.active
        if hasattr(sp, "show_region_ui"):
            sp.show_region_ui = True
        if hasattr(sp, "shading") and hasattr(sp.shading, "use_scene_lights"):
            sp.shading.type = "MATERIAL"        # or the texture is invisible
            sp.shading.use_scene_lights = False  # even light while painting
            if hasattr(sp, "overlay"):
                sp.overlay.show_floor = True
                sp.overlay.show_axis_x = False
                sp.overlay.show_axis_y = False
                sp.overlay.show_cursor = False   # clutter you never use here

    img = [a for a in screen.areas if a.type == "IMAGE_EDITOR"]
    v3d = [a for a in screen.areas if a.type == "VIEW_3D"]
    tl = [a for a in screen.areas if a.type == "DOPESHEET_EDITOR"]
    ctx.check("canvas, model and timeline all present",
              img and v3d and tl, (len(img), len(v3d), len(tl)))
    ctx.check("canvas sits left of the model",
              min(a.x for a in img) < min(a.x for a in v3d),
              (min(a.x for a in img), min(a.x for a in v3d)))
    return 0.2


def welcome_scene(ctx):
    """Replace the factory cube/camera/light with something paintable.

    The buyer's very first frame should say "pixel art tool", not "Blender".
    """
    for obj in list(bpy.context.scene.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    screen = ctx.data["screen"]
    v3d = next((a for a in screen.areas if a.type == "VIEW_3D"), None)
    guikit.in_area(v3d, lambda: bpy.ops.texel.add_cube(size=1.0, texture=64),
                   screen=screen)
    obj = bpy.context.view_layer.objects.active
    ctx.check("a pixel cube exists", obj is not None and obj.type == "MESH")

    guikit.in_area(v3d, lambda: (bpy.ops.object.select_all(action="SELECT"),
                                 bpy.ops.view3d.view_selected(),
                                 bpy.ops.object.select_all(action="DESELECT")),
                   screen=screen)

    img = next((i for i in bpy.data.images if i.name.endswith("Texture")), None)
    ctx.check("a canvas image exists", img is not None)
    for a in screen.areas:
        sp = a.spaces.active
        if hasattr(sp, "image") and a.type == "IMAGE_EDITOR":
            sp.image = img
            guikit.in_area(a, lambda: bpy.ops.image.view_all(fit_view=True),
                           screen=screen)

    # exact colours: AgX is a film response and desaturates a hand-picked
    # palette on screen, so the colour you chose is not the colour you see
    vs = bpy.context.scene.view_settings
    vs.view_transform = "Standard"
    vs.look = "None"
    ctx.check("colours shown exactly as painted",
              vs.view_transform == "Standard", vs.view_transform)
    return 0.2


def save(ctx):
    bpy.ops.wm.save_as_mainfile(filepath=OUT, compress=True)
    ok = os.path.exists(OUT)
    ctx.check("workspace.blend written", ok)
    if ok:
        ctx.note(f"{OUT}  {os.path.getsize(OUT) / 1024:.0f} KB")
    return None


guikit.run([register, build_workspace, split_vertical, convert_left,
            dress, welcome_scene, save],
           budget=120, name="TEXEL WORKSPACE BUILD")
