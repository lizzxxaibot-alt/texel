"""The workspace a buyer opens into, and the promise that it costs them nothing.

`workspace.blend` is composed offline by `make_workspace.py` and appended at
runtime. That is the comparable add-on's approach and, having tried the other
one, clearly the right call: building a layout live means area_split, a
workspace switch and a scene edit all inside one operator, and Blender processes
none of them until the operator returns - so every read afterwards is stale.
That path shipped a bug which renamed the user's own Layout workspace.

Two things here matter more than the layout:

  * **It must not touch anything of theirs.** Not their workspaces, not a scene
    they have worked in. One click from unforgivable.
  * **It must always exit.** Runs on guikit, which force-quits on a watchdog, so
    a hang costs a known number of seconds instead of a stuck Blender.

  blender --factory-startup --python test_workspace.py
"""
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

import guikit
import texel


def setup(ctx):
    try:
        texel.register()
    except Exception:
        pass
    ctx.check("workspace.blend ships with the add-on",
              os.path.exists(os.path.join(HERE, "workspace.blend")))
    ctx.data["before_ws"] = [w.name for w in bpy.data.workspaces]
    ctx.check("no Texel workspace to begin with",
              "Texel" not in ctx.data["before_ws"])
    bpy.ops.texel.workspace_create()
    return 0.6


def layout(ctx):
    ctx.check("the workspace exists", "Texel" in bpy.data.workspaces)
    ws = bpy.data.workspaces.get("Texel")
    if ws is None:
        return None
    screen = ws.screens[0]
    ctx.data["screen"] = screen

    img = [a for a in screen.areas if a.type == "IMAGE_EDITOR"]
    v3d = [a for a in screen.areas if a.type == "VIEW_3D"]
    tl = [a for a in screen.areas if a.type == "DOPESHEET_EDITOR"]
    ctx.check("a canvas", bool(img), len(img))
    ctx.check("a model view", bool(v3d), len(v3d))
    ctx.check("a timeline", bool(tl), len(tl))
    if tl:
        ctx.check("...in Timeline mode, not the dope sheet",
                  tl[0].spaces.active.mode == "TIMELINE", tl[0].spaces.active.mode)
    if img and v3d:
        ctx.check("canvas is left of the model",
                  min(a.x for a in img) < min(a.x for a in v3d),
                  (min(a.x for a in img), min(a.x for a in v3d)))
    ctx.check("both sidebars are open",
              all(sp.show_region_ui for a in screen.areas for sp in a.spaces
                  if hasattr(sp, "show_region_ui")))
    for a in v3d:
        ctx.check("the viewport shows the texture",
                  a.spaces.active.shading.type == "MATERIAL",
                  a.spaces.active.shading.type)
        break
    return 0.2


def nothing_of_theirs_was_harmed(ctx):
    names = [w.name for w in bpy.data.workspaces]
    for was in ctx.data["before_ws"]:
        ctx.check(f"their '{was}' workspace survived", was in names)
    ctx.check("no stray Layout.001 was left behind", "Layout.001" not in names,
              names)
    return 0.1


def first_impression(ctx):
    """The very first frame should say 'pixel art tool', not 'Blender'."""
    objs = sorted(o.name for o in bpy.context.scene.objects)
    ctx.check("the factory camera and light are gone",
              "Camera" not in objs and "Light" not in objs, objs)
    cube = next((o for o in bpy.context.scene.objects if "Pixel" in o.name), None)
    ctx.check("a pixel-ready cube is there instead", cube is not None, objs)
    if cube:
        ctx.check("...wearing a material", bool(cube.data.materials))
        tex = [n for m in cube.data.materials if m and m.use_nodes
               for n in m.node_tree.nodes if n.type == "TEX_IMAGE"]
        ctx.check("...with an image texture", bool(tex))
        ctx.check("...filtered Closest, so texels stay square",
                  all(n.interpolation == "Closest" for n in tex))
    # the welcome canvas must not be blank: an empty canvas is transparent, so
    # the cube renders as a black box and the opening frame teaches nothing
    img = next((i for i in bpy.data.images if i.name.endswith("Texture")), None)
    ctx.check("a welcome canvas exists", img is not None)
    if img:
        import texel.tex_doc as td
        doc = td.get(img, create=False)
        ctx.check("...that Texel is tracking", doc is not None)
        if doc:
            painted = sum(1 for v in doc.canvas.layers[0].px if v)
            ctx.check("...and it is actually painted, not blank",
                      painted > (doc.canvas.w * doc.canvas.h) // 2, painted)
            ctx.check("...with a real palette",
                      len(doc.canvas.palette) >= 5, len(doc.canvas.palette))

    vs = bpy.context.scene.view_settings
    ctx.check("colours are shown exactly as painted, not through AgX",
              vs.view_transform == "Standard", vs.view_transform)
    return 0.1


def idempotent(ctx):
    n = len(bpy.data.workspaces)
    bpy.ops.texel.workspace_create()
    ctx.check("calling it again switches, never duplicates",
              len(bpy.data.workspaces) == n, len(bpy.data.workspaces))
    ctx.check("and we are on it",
              guikit.win().workspace.name == "Texel",
              guikit.win().workspace.name)
    return 0.2


def never_touches_real_work(ctx):
    """A scene somebody has worked in must be left completely alone."""
    bpy.ops.mesh.primitive_uv_sphere_add()
    bpy.context.view_layer.objects.active.name = "UserWork"
    n = len(bpy.context.scene.objects)
    # Getting the operator to take its create path again just needs the name
    # freed. bpy.data.workspaces has no .remove(), and workspace.delete() would
    # not fire from here either - renaming needs neither.
    bpy.data.workspaces["Texel"].name = "Texel (old)"
    ctx.check("the name is free again", "Texel" not in bpy.data.workspaces)
    bpy.ops.texel.workspace_create()
    ctx.check("a fresh Texel workspace was created", "Texel" in bpy.data.workspaces)
    after = [o.name for o in bpy.context.scene.objects]
    ctx.check("a scene with the user's own work is untouched",
              len(after) == n and "UserWork" in after, after)
    return 0.4


def framed(ctx):
    """The deferred framing must actually have run - an unframed viewport is a
    buyer opening onto empty grey, which is the whole thing we are fixing."""
    ws = bpy.data.workspaces.get("Texel")
    if ws is None:
        return None
    for a in ws.screens[0].areas:
        if a.type == "VIEW_3D":
            r3d = a.spaces.active.region_3d
            ctx.check("the viewport is framed on the cube, not off in space",
                      1.0 < r3d.view_distance < 8.0, r3d.view_distance)
            ctx.check("...in perspective", r3d.view_perspective == "PERSP",
                      r3d.view_perspective)
            break
    return 0.2


def shoot(ctx):
    ws = bpy.data.workspaces.get("Texel")
    if ws is None:
        return None
    p = os.path.join(HERE, "shots", "workspace.png")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with bpy.context.temp_override(window=guikit.win(), screen=ws.screens[0]):
        bpy.ops.screen.screenshot(filepath=p)
    ctx.note(f"screenshot -> {p}")
    return 0.2


# shoot() runs right after first_impression, NOT at the end: the later
# steps deliberately dirty the scene to prove the operator leaves real work
# alone, and a screenshot of that is not what a buyer opens into.
guikit.run([setup, layout, nothing_of_theirs_was_harmed, first_impression,
            framed, shoot, idempotent, never_touches_real_work],
           budget=150, name="TEXEL WORKSPACE")
