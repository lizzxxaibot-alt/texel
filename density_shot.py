"""T-001: the density readout, as a still, with real measured numbers.

The claim on the store page is that Texel MEASURES texel density. Nothing on the
page shows the result of a measurement - `03_blender.png` shows the buttons.
This builds the missing evidence and refuses to fake any of it:

  * the scene is three Blender DEFAULT cubes at 3.2m / 1.0m / 0.38m, joined,
    sharing one 32px texture. Default cube UVs are identical regardless of the
    cube's world size, so the drift is Blender's own out-of-the-box behaviour,
    not a rigged UV layout.
  * every number in the readout comes from the shipped `texel.density_detect`
    operator running on that mesh. Nothing is typed in.
  * the same operator is re-run AFTER `texel.density_apply` and the second
    readout is captured too, so the after-figure is measured, not asserted.

Run with a GUI Blender (screen.screenshot needs a window):
  blender --factory-startup --python density_shot.py
Writes shots/density/*.png and shots/density/facts.json
"""
import json
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

import texel  # noqa: E402

try:
    texel.register()
except Exception:
    pass
try:
    bpy.context.preferences.view.show_splash = False
except Exception:
    pass

OUT = os.path.join(HERE, "shots", "density")
os.makedirs(OUT, exist_ok=True)
TILE = os.path.join(HERE, "store", "tile_blockwall_32.png")

state = {"step": 0, "facts": {}, "fails": []}


def win():
    return bpy.context.window_manager.windows[0]


def v3d():
    return max((a for a in win().screen.areas if a.type == "VIEW_3D"),
               key=lambda a: a.width * a.height)


def force_tab():
    for a in win().screen.areas:
        if a.type != "VIEW_3D":
            continue
        for r in a.regions:
            if r.type == "UI":
                try:
                    r.active_panel_category = "Texel"
                    r.tag_redraw()
                except Exception:
                    pass


def build():
    """Three default cubes at different scales, one texture, joined."""
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)

    img = bpy.data.images.load(TILE)
    img.name = "Blockwall"
    mat = bpy.data.materials.new("Pixel")
    mat.use_nodes = True
    nt = mat.node_tree
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    tex.interpolation = "Closest"
    tex.location = (-400, 200)
    nt.links.new(tex.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"])

    # sizes chosen to read as wall / crate / cap - a real prop range, not a stunt
    for size, loc in ((3.2, (0.0, 0.0, 1.6)),
                      (1.0, (2.6, 0.0, 0.5)),
                      (0.38, (2.6, 0.0, 1.19))):
        bpy.ops.mesh.primitive_cube_add(size=size, location=loc)
        o = bpy.context.active_object
        bpy.ops.object.shade_flat()
        o.data.materials.append(mat)

    bpy.ops.object.select_all(action="SELECT")
    bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
    bpy.ops.object.join()
    obj = bpy.context.active_object
    obj.name = "Wall + Crate"
    state["facts"]["faces"] = len(obj.data.polygons)
    state["facts"]["texture_px"] = max(img.size)
    return obj


def fullscreen():
    """One editor filling the window. The outliner and properties editors eat a
    third of the frame and say nothing about density."""
    a = v3d()
    region = next(r for r in a.regions if r.type == "WINDOW")
    with bpy.context.temp_override(window=win(), screen=win().screen, area=a,
                                   region=region, space_data=a.spaces.active):
        bpy.ops.screen.screen_full_area(use_hide_panels=False)


def to_info():
    """Flip the maximised editor to INFO.

    The sidebar is too narrow for the readout - Blender middle-elides it to
    "10.5 px/unit av....1, 8.4x spread)", which loses the range AND the spread,
    i.e. the entire claim. Every one of these operators also calls
    self.report(), and the Info editor prints that at full width without
    eliding, accumulating all three measurements in order. So the log is the
    readout, it is Blender's own widget, and nothing is retyped."""
    a = max(win().screen.areas, key=lambda x: x.width * x.height)
    a.type = "INFO"


def view():
    a = v3d()
    for sp in a.spaces:
        if hasattr(sp, "shading"):
            sp.shading.type = "MATERIAL"
        if hasattr(sp, "show_region_ui"):
            sp.show_region_ui = True
        if hasattr(sp, "overlay"):
            sp.overlay.show_floor = False
            sp.overlay.show_axis_x = False
            sp.overlay.show_axis_y = False
            sp.overlay.show_cursor = False
            sp.overlay.show_object_origins = False
            sp.overlay.show_text = False
    region = next(r for r in a.regions if r.type == "WINDOW")
    with bpy.context.temp_override(window=win(), screen=win().screen, area=a,
                                   region=region, space_data=a.spaces.active):
        bpy.ops.object.select_all(action="SELECT")
        bpy.ops.view3d.view_selected()
        bpy.ops.object.select_all(action="DESELECT")
    force_tab()


def open_density_panel():
    """Panels remember their open/closed state per screen; Texel Density is a
    child panel and starts closed on a factory startup."""
    for a in win().screen.areas:
        if a.type != "VIEW_3D":
            continue
        for r in a.regions:
            if r.type != "UI":
                continue
            for pt in getattr(r, "panels", []) or []:
                pass
    # panel open state lives on the Panel type's instances; use the RNA path
    for name in ("TEXEL_PT_tools_3d", "TEXEL_PT_density"):
        pt = getattr(bpy.types, name, None)
        if pt is not None and hasattr(pt, "bl_options"):
            pt.bl_options = {o for o in pt.bl_options if o != "DEFAULT_CLOSED"}


def run_op(name):
    a = v3d()
    region = next(r for r in a.regions if r.type == "WINDOW")
    with bpy.context.temp_override(window=win(), screen=win().screen, area=a,
                                   region=region, space_data=a.spaces.active):
        getattr(bpy.ops.texel, name)("INVOKE_DEFAULT")
    return bpy.context.scene.texel.status


def shot(name):
    force_tab()
    for a in win().screen.areas:
        a.tag_redraw()
    p = os.path.join(OUT, f"{name}.png")
    with bpy.context.temp_override(window=win(), screen=win().screen):
        bpy.ops.screen.screenshot(filepath=p)
    return p


STEPS = []


def tick():
    n = state["step"]
    state["step"] += 1
    try:
        if n == 0:
            build()
            fullscreen()
            return 0.4
        if n == 1:
            view()
            return 0.4
        if n == 2:
            force_tab()
            open_density_panel()
            return 1.0
        if n == 3:
            force_tab()
            shot("00_scene")
            return 0.3
        if n == 4:
            state["facts"]["before"] = run_op("density_detect")
            state["facts"]["target"] = round(bpy.context.scene.texel.target_density, 3)
            return 1.0
        if n == 5:
            force_tab()
            shot("01_detected")
            return 0.3
        if n == 6:
            state["facts"]["applied"] = run_op("density_apply")
            return 1.0
        if n == 7:
            force_tab()
            shot("02_applied")
            return 0.3
        if n == 8:
            state["facts"]["after"] = run_op("density_detect")
            return 1.2
        if n == 9:
            force_tab()
            shot("03_verified")
            return 0.3
        if n == 10:
            to_info()
            return 1.2
        if n == 11:
            shot("04_log")
            return 0.3
    except Exception as e:  # noqa: BLE001
        state["fails"].append(f"step {n}: {type(e).__name__}: {e}")

    with open(os.path.join(OUT, "facts.json"), "w", encoding="utf-8") as f:
        json.dump(state["facts"], f, indent=2)
    for k, v in state["facts"].items():
        print(f"[fact] {k}: {v}", flush=True)
    if state["fails"]:
        print(f"FAILED: {state['fails']}", flush=True)
        print("TEXEL DENSITY SHOT: FAILED", flush=True)
    else:
        print("TEXEL DENSITY SHOT: ALL PASS", flush=True)
    bpy.ops.wm.quit_blender()
    return None


bpy.app.timers.register(tick, first_interval=1.5)
