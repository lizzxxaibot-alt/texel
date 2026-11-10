"""Mon beat (v0.2.7 Beat 1): "Texel Paint stays on now" - a real capture.

  blender --factory-startup --enable-event-simulate --python paintmode_shot.py -- <dir holding the extracted texel/>

Drives the SHIPPED add-on in a real window with simulated mouse input, same
mechanism as test_paintmode_gui.py: press Texel Paint ONCE from the sidebar,
then draw a 16x16 sword in four separate left-drags without touching the button
again. Between strokes only the colour property changes (what the sidebar
swatch sets). Every stroke is checked: mode still on, texel count as expected.
Then the window is screenshotted with the mode still on, so the button reads
"Stop Texel Paint" and the header shows the hint. Writes shot.png + facts.json.
"""
import json
import os
import sys
import time

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = sys.argv[sys.argv.index("--") + 1]
sys.path.insert(0, ROOT)
import texel
texel.register()
from texel import tex_doc, tex_paint as TP

try:
    bpy.context.preferences.view.show_splash = False
except Exception:
    pass

N = 16
win = bpy.context.window
area = max(win.screen.areas, key=lambda a: a.width * a.height)
S = {"fails": [], "strokes": []}
T0 = time.time()


def region(t):
    return next(r for r in area.regions if r.type == t)


def lit():
    return sum(1 for i, v in enumerate(tex_doc.get(S["img"]).canvas.flatten()) if v)


def sim(t, v, x, y):
    win.event_simulate(type=t, value=v, x=int(x), y=int(y))


def at(col, row):
    w = region("WINDOW")
    rx, ry = w.view2d.view_to_region((col + 0.5) / N, 1 - (row + 0.5) / N, clip=False)
    return w.x + rx, w.y + ry


def force_tab():
    for r in area.regions:
        if r.type == "UI":
            try:
                if r.active_panel_category != "Texel":
                    r.active_panel_category = "Texel"
            except Exception:
                pass
    area.tag_redraw()


def setup():
    area.type = "IMAGE_EDITOR"
    img = bpy.data.images.new("sword", N, N, alpha=True)
    img.pixels.foreach_set([0.0] * N * N * 4)
    sp = area.spaces.active
    sp.image = img
    sp.show_region_ui = True
    force_tab()
    S["img"] = img
    s = bpy.context.scene.texel
    s.tool, s.brush_size, s.brush_shape = "PENCIL", 1, "SQUARE"
    s.dither, s.mirror_x, s.mirror_y, s.symmetry, s.use_pressure = "OFF", False, False, 1, False
    with bpy.context.temp_override(window=win, area=area, region=region("WINDOW")):
        bpy.ops.image.view_all(fit_view=True)


def enter():
    with bpy.context.temp_override(window=win, area=area, region=region("UI")):
        r = bpy.ops.texel.paint("INVOKE_DEFAULT")
    S["enter"] = list(r)
    if not (r == {"RUNNING_MODAL"} and TP.paint_mode_on(area)):
        S["fails"].append(f"enter: {r}")


# (name, colour, cells) - cells are (col, row) from the top-left, in drag order
STROKES = [
    ("blade", (0.80, 0.84, 0.90, 1), [(13, 2), (12, 3), (11, 4), (10, 5), (9, 6), (8, 7), (7, 8), (6, 9)]),
    ("guard", (0.93, 0.72, 0.20, 1), [(3, 8), (4, 9), (5, 10), (6, 11), (7, 12)]),
    ("grip", (0.45, 0.26, 0.14, 1), [(4, 11), (3, 12)]),
    ("pommel", (0.93, 0.72, 0.20, 1), [(2, 13)]),
]


def stroke(i):
    name, col, cells = STROKES[i]

    def go():
        S["before"] = lit()
        bpy.context.scene.texel.colour = col
        x, y = at(*cells[0])
        sim("MOUSEMOVE", "NOTHING", x, y)
        sim("LEFTMOUSE", "PRESS", x, y)
        for c in cells[1:]:
            sim("MOUSEMOVE", "NOTHING", *at(*c))
        sim("LEFTMOUSE", "RELEASE", *at(*cells[-1]))
    return go


def after(i):
    name, col, cells = STROKES[i]

    def go():
        now = lit()
        on = TP.paint_mode_on(area)
        S["strokes"].append({"name": name, "texels_added": now - S["before"],
                             "expected": len(cells), "mode_on_after": on})
        if now - S["before"] != len(cells) or not on:
            S["fails"].append(f"{name}: +{now - S['before']} (want {len(cells)}), on={on}")
    return go


def shot():
    for a in win.screen.areas:
        a.tag_redraw()
    p = os.path.join(HERE, "shot_full.png")
    with bpy.context.temp_override(window=win, screen=win.screen):
        bpy.ops.screen.screenshot(filepath=p)
    S["tab"] = region("UI").active_panel_category
    S["area"] = {"x": area.x, "y": area.y, "w": area.width, "h": area.height}
    S["window"] = {"w": win.width, "h": win.height}
    S["mode_on_at_shot"] = TP.paint_mode_on(area)
    S["total_texels"] = lit()
    S["blender"] = bpy.app.version_string
    S["texel_from"] = texel.__file__
    S["hint"] = TP.HINT


def done():
    S.pop("img", None)
    S.pop("before", None)
    with open(os.path.join(HERE, "facts.json"), "w") as f:
        json.dump(S, f, indent=2)
    print("FACTS", json.dumps(S), flush=True)
    os._exit(1 if S["fails"] else 0)


STEPS = [setup, enter]
for i in range(len(STROKES)):
    STEPS += [stroke(i), after(i)]
STEPS += [shot, shot, done]   # second shot: let the header/button redraw settle


def step():
    if time.time() - T0 > 90:
        S["fails"].append("watchdog")
        done()
    fn = STEPS.pop(0)
    try:
        if area.type == "IMAGE_EDITOR":
            force_tab()
        fn()
    except Exception as e:
        import traceback
        traceback.print_exc()
        S["fails"].append(f"{getattr(fn, '__name__', fn)}: {e!r}")
        done()
    return 0.5


bpy.app.timers.register(step, first_interval=2.0)
