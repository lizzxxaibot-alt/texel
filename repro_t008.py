"""T-008 reproduction: does the density readout fit the sidebar?

Runs a real GUI Blender, builds the same three-cube mesh the density card used
(3.2 m / 1.0 m / 0.38 m, joined, one 32 px texture), runs texel.density_detect,
and screenshots the N-panel region ONLY - cropped to the region rectangle, so
what is measured is the widget that draws the string, not the window around it.

  blender --factory-startup --python _repro_t008.py
"""
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

import texel

try:
    texel.register()
except Exception:
    pass

SCALE = float(os.environ.get("TEXEL_UI_SCALE", "1.0"))
bpy.context.preferences.view.ui_scale = SCALE


OUT = os.path.join(HERE, "shots", "t008", os.environ.get("TEXEL_TAG", "4.5.9"))
os.makedirs(OUT, exist_ok=True)
state = {"step": 0}


def win():
    return bpy.context.window_manager.windows[0]


def v3d():
    return max((a for a in win().screen.areas if a.type == "VIEW_3D"),
               key=lambda a: a.width * a.height)


def build():
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    a = v3d()
    region = next(r for r in a.regions if r.type == "WINDOW")
    with bpy.context.temp_override(window=win(), screen=win().screen, area=a,
                                   region=region, space_data=a.spaces.active):
        for size in (3.2, 1.0, 0.38):
            bpy.ops.texel.add_cube(size=size, texture=32)
        for i, ob in enumerate(bpy.data.objects):
            ob.location.x = i * 4.0
        bpy.ops.object.select_all(action="SELECT")
        bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
        bpy.ops.object.join()
        bpy.ops.texel.density_detect()
    for sp in a.spaces:
        if hasattr(sp, "show_region_ui"):
            sp.show_region_ui = True
    for ar in win().screen.areas:
        for r in ar.regions:
            if r.type == "UI":
                try:
                    r.active_panel_category = "Texel"
                    r.tag_redraw()
                except Exception:
                    pass


def shoot(name):
    a = v3d()
    ui = next(r for r in a.regions if r.type == "UI")
    p = os.path.join(OUT, name)
    print(f"[info] UI region {ui.width}x{ui.height} at ({ui.x},{ui.y})", flush=True)
    with bpy.context.temp_override(window=win(), screen=win().screen):
        bpy.ops.screen.screenshot(filepath=p)
    # crop to the sidebar region: screen.screenshot writes the whole window and
    # the window origin is bottom-left, same as Region.x/y
    img = bpy.data.images.load(p)
    w, h = img.size
    px = list(img.pixels)
    cw, ch = ui.width, ui.height
    out = bpy.data.images.new("crop", cw, ch, alpha=True)
    buf = []
    for y in range(ch):
        row = (ui.y + y) * w + ui.x
        buf.extend(px[row * 4:(row + cw) * 4])
    out.pixels = buf
    out.filepath_raw = os.path.join(OUT, "crop_" + name)
    out.file_format = "PNG"
    out.save()
    print(f"[info] wrote {out.filepath_raw}", flush=True)


def force_tab():
    for ar in win().screen.areas:
        for r in ar.regions:
            if r.type == "UI":
                try:
                    r.active_panel_category = "Texel"
                except Exception as e:
                    print(f"[warn] tab: {e}", flush=True)
                r.tag_redraw()
        ar.tag_redraw()


def tick():
    """Shoot the sidebar on several consecutive redraws of the SAME state.

    One shot proves the readout fits; it does not prove the panel settled.
    Blender positions a sub-panel from its parent's measured height, so a
    parent that grew by two rows can under-report for a frame and let the next
    header draw over the text. Shooting frames 0..3 unchanged is what tells a
    one-frame artifact apart from a layout that ships broken."""
    if state["step"] == 0:
        build()
        print(f"[status] {bpy.context.scene.texel.status!r}", flush=True)
        state["step"] = 1
        return 0.5
    if state["step"] > 4:
        print("T008 REPRO DONE", flush=True)
        bpy.ops.wm.quit_blender()
        return None
    force_tab()
    shoot(f"f{state['step'] - 1}_{SCALE:.2f}.png")
    state["step"] += 1
    return 0.4


bpy.app.timers.register(tick, first_interval=1.5)
