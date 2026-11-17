"""Mon beat 2026-11-16: the dither brush (shipped in 0.2.2, never had a visual).

  blender --factory-startup --enable-event-simulate --python dither_shot.py -- <dir holding the extracted texel/>

Same mechanism as promo/paintmode/paintmode_shot.py: drives the SHIPPED add-on
in a real window with simulated mouse input. A 64x64 dusk sky: one click with a
64-texel solid brush lays the navy, then seven left-drags with an 8-texel Pencil
at Bayer 2, 4, 6, 8, 10, 12 and 14 sixteenths lay the orange. Between strokes only sidebar
properties change (colour, size, dither, density). Every band is counted off
the canvas: a 64x8 band at level L must hold exactly 512*L/16 orange texels.
Writes shot_full.png + facts.json; exits 1 on any miss.
"""
import json, os, sys, time
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

N = 64
NAVY = (0.09, 0.11, 0.27, 1)
ORANGE = (0.98, 0.56, 0.24, 1)
BANDS = [(12 + 8 * i, 2 + 2 * i) for i in range(7)]   # (centre screen row, Bayer level): 2..14 sixteenths
win = bpy.context.window
area = max(win.screen.areas, key=lambda a: a.width * a.height)
S = {"fails": [], "strokes": []}
T0 = time.time()


def region(t):
    return next(r for r in area.regions if r.type == t)


def flat():
    return bytes(tex_doc.get(S["img"]).canvas.flatten())


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
    img = bpy.data.images.new("dusk_sky", N, N, alpha=True)
    img.pixels.foreach_set([0.0] * N * N * 4)
    sp = area.spaces.active
    sp.image = img
    sp.show_region_ui = True
    force_tab()
    S["img"] = img
    s = bpy.context.scene.texel
    s.tool, s.brush_size, s.brush_shape = "PENCIL", 64, "SQUARE"
    s.dither, s.mirror_x, s.mirror_y, s.symmetry, s.use_pressure = "OFF", False, False, 1, False
    s.colour = NAVY
    with bpy.context.temp_override(window=win, area=area, region=region("WINDOW")):
        bpy.ops.image.view_all(fit_view=True)


def enter():
    with bpy.context.temp_override(window=win, area=area, region=region("UI")):
        r = bpy.ops.texel.paint("INVOKE_DEFAULT")
    S["enter"] = list(r)
    if not (r == {"RUNNING_MODAL"} and TP.paint_mode_on(area)):
        S["fails"].append(f"enter: {r}")


def navy():
    x, y = at(N // 2, N // 2)
    sim("MOUSEMOVE", "NOTHING", x, y)
    sim("LEFTMOUSE", "PRESS", x, y)
    sim("LEFTMOUSE", "RELEASE", x, y)


def navy_check():
    f = flat()
    vals = sorted(set(f))
    S["navy_texels"] = sum(1 for v in f if v)
    S["navy_index"] = vals[-1]
    if S["navy_texels"] != N * N or len(vals) != 1:
        S["fails"].append(f"navy fill: {S['navy_texels']} texels, indices {vals}")


def band(i):
    row, level = BANDS[i]

    def go():
        S["before"] = flat()
        s = bpy.context.scene.texel
        s.colour, s.brush_size, s.dither, s.dither_level = ORANGE, 8, "BAYER", level
        sim("MOUSEMOVE", "NOTHING", *at(0, row))
        sim("LEFTMOUSE", "PRESS", *at(0, row))
        for c in range(1, N):
            sim("MOUSEMOVE", "NOTHING", *at(c, row))
        sim("LEFTMOUSE", "RELEASE", *at(N - 1, row))
    return go


def band_check(i):
    row, level = BANDS[i]

    def go():
        b, a = S["before"], flat()
        changed = [n for n in range(N * N) if a[n] != b[n]]
        rows = sorted({n // N for n in changed})
        want = N * 8 * level // 16
        S["strokes"].append({"screen_row": row, "level_16ths": level, "texels_changed": len(changed),
                             "expected": want, "canvas_rows": [rows[0], rows[-1]] if rows else [],
                             "mode_on_after": TP.paint_mode_on(area)})
        # a sparse level leaves some rows of its band untouched, so test containment, not span
        if len(changed) != want or not rows or rows[0] < row - 4 or rows[-1] > row + 3 or not TP.paint_mode_on(area):
            S["fails"].append(f"band {row}/L{level}: {len(changed)} (want {want}), rows {rows[:1]}..{rows[-1:]}")
    return go


def shot():
    for a in win.screen.areas:
        a.tag_redraw()
    p = os.path.join(HERE, "shot_full.png")
    with bpy.context.temp_override(window=win, screen=win.screen):
        bpy.ops.screen.screenshot(filepath=p)
    f = flat()
    S["tab"] = region("UI").active_panel_category
    S["area"] = {"x": area.x, "y": area.y, "w": area.width, "h": area.height}
    S["window"] = {"w": win.width, "h": win.height}
    S["mode_on_at_shot"] = TP.paint_mode_on(area)
    S["index_counts"] = {str(v): f.count(v) for v in sorted(set(f))}
    S["row_orange"] = [sum(1 for v in f[r * N:(r + 1) * N] if v != S.get("navy_index")) for r in range(N)]
    S["blender"] = bpy.app.version_string
    S["texel_from"] = texel.__file__
    s = bpy.context.scene.texel
    S["panel_at_shot"] = {"tool": s.tool, "size": s.brush_size, "dither": s.dither, "density": s.dither_level}


def done():
    S.pop("img", None)
    S.pop("before", None)
    with open(os.path.join(HERE, "facts.json"), "w") as f:
        json.dump(S, f, indent=2)
    print("FACTS", json.dumps(S), flush=True)
    os._exit(1 if S["fails"] else 0)


STEPS = [setup, enter, navy, navy_check]
for i in range(len(BANDS)):
    STEPS += [band(i), band_check(i)]
STEPS += [shot, shot, done]


def step():
    if time.time() - T0 > 180:
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
    return 0.7


bpy.app.timers.register(step, first_interval=2.0)
