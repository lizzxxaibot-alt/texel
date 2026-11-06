"""Texel Paint mode in a REAL window, driven by real (simulated) input events.

  blender --factory-startup --enable-event-simulate --python test_paintmode_gui.py
  (or: blender ... -- <extracted addon parent dir>   to test a built zip)

`test_features.py` drives the paint operator's own invoke/modal with synthetic
event objects, which proves the state machine but not the parts that only exist
in a running window: the region hit test, `temp_override` inside a modal
handler, `ed.undo_push` from a modal, and entering the mode from the SIDEBAR
(where a 3D raycast has no view). This file covers those. It exists because the
first stranger to use Texel (T-028) had to press Texel Paint before every
stroke, and the old operator was never driven by a real mouse in any suite.

Each step runs on a timer so Blender's event loop processes the simulated
events between steps. A watchdog quits with a failure if the sequence stalls.
"""
import os
import sys
import time

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else os.path.dirname(HERE)
sys.path.insert(0, ROOT)

import texel
texel.register()
from texel import tex_doc, tex_paint as TP
if not hasattr(TP, "paint_mode_on"):          # a pre-0.2.7 build, as negative control
    TP.paint_mode_on = lambda area=None: False

print(f"[info] Blender {bpy.app.version_string}, texel from {texel.__file__}", flush=True)
fails = []
T0 = time.time()


def check(name, cond, detail=""):
    print(f"[{'ok  ' if cond else 'FAIL'}] {name}" + ("" if cond else f"  -> {detail}"),
          flush=True)
    if not cond:
        fails.append(name)


def finish():
    print()
    if fails:
        print(f"{len(fails)} FAILED: {fails}", flush=True)
        os._exit(1)
    print("TEXEL PAINT MODE GUI: ALL PASS", flush=True)
    os._exit(0)


win = bpy.context.window
if not hasattr(win, "event_simulate"):
    check("event simulation is available (--enable-event-simulate)", False)
    finish()

scr = win.screen
area = max(scr.areas, key=lambda a: a.width * a.height)   # the big viewport


def region(a, t):
    return next(r for r in a.regions if r.type == t)


def lit(img):
    return sum(1 for v in tex_doc.get(img).canvas.flatten() if v)


def sim(t, v, x, y):
    win.event_simulate(type=t, value=v, x=int(x), y=int(y))


S = {}          # state carried between steps


# ------------------------------------------------------------ IMAGE EDITOR
def img_setup():
    area.type = "IMAGE_EDITOR"
    img = bpy.data.images.new("ModeGUI", 16, 16, alpha=True)
    img.pixels.foreach_set([0.0] * 16 * 16 * 4)
    area.spaces.active.image = img
    sp = area.spaces.active
    sp.show_region_ui = True
    S["img"] = img
    s = bpy.context.scene.texel
    s.tool, s.colour, s.brush_size, s.brush_shape = "PENCIL", (1, 0, 0, 1), 1, "SQUARE"
    s.dither, s.mirror_x, s.mirror_y, s.symmetry, s.use_pressure = "OFF", False, False, 1, False
    with bpy.context.temp_override(window=win, area=area, region=region(area, "WINDOW")):
        bpy.ops.image.view_all(fit_view=True)


def img_enter_from_sidebar():
    ui = region(area, "UI")
    with bpy.context.temp_override(window=win, area=area, region=ui):
        r = bpy.ops.texel.paint("INVOKE_DEFAULT")
    check("Image Editor: Texel Paint from the sidebar enters the mode",
          r == {"RUNNING_MODAL"} and TP.paint_mode_on(area), r)


def uv_to_win(u, v):
    w = region(area, "WINDOW")
    rx, ry = w.view2d.view_to_region(u, v, clip=False)
    return w.x + rx, w.y + ry


def img_stroke(row):
    # texel row `row` from the top, columns 2..9; texel centres
    def at(cx):
        return uv_to_win((cx + 0.5) / 16, 1 - (row + 0.5) / 16)
    def go():
        x, y = at(2)
        sim("MOUSEMOVE", "NOTHING", x, y)
        sim("LEFTMOUSE", "PRESS", x, y)
        for cx in range(3, 10):
            sim("MOUSEMOVE", "NOTHING", *at(cx))
        sim("LEFTMOUSE", "RELEASE", *at(9))
    return go


def img_after_1():
    S["l1"] = lit(S["img"])
    check("Image Editor: stroke 1 paints a row of 8", S["l1"] == 8, S["l1"])
    check("Image Editor: the mode is still on after the release", TP.paint_mode_on(area))


def img_after_2():
    l2 = lit(S["img"])
    check("Image Editor: stroke 2 paints with the mouse alone (T-028)",
          l2 == 16, l2)


def hover_sidebar():
    ui = region(area, "UI")
    x, y = ui.x + ui.width // 2, ui.y + ui.height // 2
    S["before_ui"] = lit(S["img"])
    sim("MOUSEMOVE", "NOTHING", x, y)
    sim("LEFTMOUSE", "PRESS", x, y)
    sim("LEFTMOUSE", "RELEASE", x, y)


def after_sidebar_click():
    check("Image Editor: a click on the sidebar paints nothing under it",
          lit(S["img"]) == S["before_ui"], (lit(S["img"]), S["before_ui"]))
    check("Image Editor: and leaves the mode on", TP.paint_mode_on(area))


def press_esc():
    w = region(area, "WINDOW")
    sim("MOUSEMOVE", "NOTHING", w.x + 20, w.y + 20)
    sim("ESC", "PRESS", w.x + 20, w.y + 20)
    sim("ESC", "RELEASE", w.x + 20, w.y + 20)


def after_esc_img():
    check("Image Editor: Esc leaves the mode", not TP.paint_mode_on())
    n = lit(S["img"])
    x, y = uv_to_win(12.5 / 16, 1 - 12.5 / 16)
    S["after_esc"] = n
    sim("MOUSEMOVE", "NOTHING", x, y)
    sim("LEFTMOUSE", "PRESS", x, y)
    sim("LEFTMOUSE", "RELEASE", x, y)


def after_click_out_of_mode():
    check("Image Editor: out of the mode, a click does not paint",
          lit(S["img"]) == S["after_esc"], lit(S["img"]))


def d_toggles_on():
    w = region(area, "WINDOW")
    x, y = uv_to_win(0.5, 0.5)
    sim("MOUSEMOVE", "NOTHING", x, y)
    sim("D", "PRESS", x, y)
    sim("D", "RELEASE", x, y)


def after_d_on():
    check("Image Editor: D turns the mode on", TP.paint_mode_on(area))
    check("Image Editor: D paints nothing by itself", lit(S["img"]) == S["after_esc"],
          lit(S["img"]))
    d_toggles_on()          # the same key again


def after_d_off():
    check("Image Editor: D again turns it off", not TP.paint_mode_on())


# --------------------------------------------------------------- 3D VIEWPORT
def v3d_setup():
    area.type = "VIEW_3D"
    sp = area.spaces.active
    sp.show_region_ui = True
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o)
    with bpy.context.temp_override(window=win, area=area, region=region(area, "WINDOW")):
        bpy.ops.texel.add_cube()
        obj = bpy.context.active_object
        sp.region_3d.view_perspective = "ORTHO"
        sp.region_3d.view_rotation = (1, 0, 0, 0)       # top view
        bpy.ops.view3d.view_selected()
    S["cube"] = bpy.context.active_object
    img = None
    for slot in S["cube"].material_slots:
        for n in slot.material.node_tree.nodes:
            if n.type == "TEX_IMAGE" and n.image:
                img = n.image
    S["cimg"] = img
    S["c0"] = lit(img) if img else -1


def v3d_enter_from_sidebar():
    ui = region(area, "UI")
    with bpy.context.temp_override(window=win, area=area, region=ui):
        r = bpy.ops.texel.paint("INVOKE_DEFAULT")
    check("3D View: Texel Paint from the sidebar enters the mode",
          r == {"RUNNING_MODAL"} and TP.paint_mode_on(area), r)


def v3d_stroke(dy):
    def go():
        from bpy_extras import view3d_utils as V
        w = region(area, "WINDOW")
        rv3d = area.spaces.active.region_3d
        top = S["cube"].matrix_world.translation.copy()
        top.z += 0.5
        p = []
        for i in range(6):
            q = top.copy()
            q.x += -0.3 + i * 0.12
            q.y += dy
            c = V.location_3d_to_region_2d(w, rv3d, q)
            p.append((w.x + c.x, w.y + c.y))
        sim("MOUSEMOVE", "NOTHING", *p[0])
        sim("LEFTMOUSE", "PRESS", *p[0])
        for pt in p[1:]:
            sim("MOUSEMOVE", "NOTHING", *pt)
        sim("LEFTMOUSE", "RELEASE", *p[-1])
    return go


def v3d_after_1():
    S["c1"] = lit(S["cimg"])
    check("3D View: stroke 1 paints the cube", S["c1"] > S["c0"], (S["c0"], S["c1"]))
    check("3D View: the mode is still on after the release", TP.paint_mode_on(area))


def v3d_after_2():
    c2 = lit(S["cimg"])
    check("3D View: stroke 2 paints with the mouse alone (T-028)", c2 > S["c1"],
          (S["c1"], c2))


def after_esc_v3d():
    check("3D View: Esc leaves the mode and clears the header",
          not TP.paint_mode_on())


STEPS = [img_setup, img_enter_from_sidebar, img_stroke(3), img_after_1,
         img_stroke(6), img_after_2, hover_sidebar, after_sidebar_click,
         press_esc, after_esc_img, after_click_out_of_mode, d_toggles_on,
         after_d_on, after_d_off,
         v3d_setup, v3d_enter_from_sidebar, v3d_stroke(-0.2), v3d_after_1,
         v3d_stroke(0.2), v3d_after_2, press_esc, after_esc_v3d]


def step():
    if time.time() - T0 > 120:
        check("WATCHDOG: the sequence finished in time", False)
        finish()
    if not STEPS:
        finish()
    fn = STEPS.pop(0)
    try:
        fn()
    except Exception as e:  # a raise inside a timer is swallowed; make it a FAIL
        import traceback
        traceback.print_exc()
        check(f"{fn.__name__} ran without raising", False, repr(e))
        finish()
    return 0.4


bpy.app.timers.register(step, first_interval=1.5)
