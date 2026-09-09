"""Every panel must actually DRAW.

The headless suites register operators and call them; none of them draws a
panel, and a panel only fails at draw time - a bad property name or an operator
id that does not exist raises inside draw() and Blender renders the panel as an
error box while every other test stays green. That is exactly how 56 operators
sat unreachable and a phantom `texel.save_canvas` reference survived review.

So this one runs a real GUI, opens the sidebar in both editors, forces the Texel
tab, and screenshots it in each of the states that change what gets drawn.

**Blender will not hand a draw() exception to Python** - it catches it, prints a
traceback to stderr and renders an error box in the panel. So the real gate is
the console, not this script's own verdict:

  blender --factory-startup --python test_panels.py 2>&1 | grep -i traceback

An empty grep plus "TEXEL PANELS: ALL PASS" is the pass. The screenshots in
shots/panels/ are the second check - look at them.
"""
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

import texel
from texel import tex_doc
from texel.core import raster as R

try:
    texel.register()
except Exception:
    pass
try:
    bpy.context.preferences.view.show_splash = False
except Exception:
    pass

OUT = os.path.join(HERE, "shots", "panels")
os.makedirs(OUT, exist_ok=True)

state = {"n": 0, "step": 0, "ready": False, "fails": []}


def win():
    return bpy.context.window_manager.windows[0]


def areas(kind):
    return [a for a in win().screen.areas if a.type == kind]


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


def coverage_check():
    """Every operator a buyer can use must have a button.

    56 of 92 were registered and drawn nowhere - reachable only through F3
    search, if you already knew the name. This is the check that would have
    caught it, so it is a gate now rather than something someone remembers to
    run. INTERNAL operators are exempt: they are the plumbing behind a keyboard
    shortcut and are not supposed to appear in a panel.
    """
    import glob
    import re
    ops, internal = set(), set()
    for f in glob.glob(os.path.join(HERE, "tex_*.py")):
        src = io.open(f, encoding="utf-8").read()
        for block in src.split("class ")[1:]:
            m = re.search(r'bl_idname = "(texel\.[a-z_0-9]+)"', block)
            if not m:
                continue
            ops.add(m.group(1))
            if "INTERNAL" in (re.search(r"bl_options = \{([^}]*)\}", block)
                              or type("", (), {"group": lambda *a: ""})()).group(1):
                internal.add(m.group(1))
    ui = io.open(os.path.join(HERE, "tex_ui.py"), encoding="utf-8").read()
    shown = set(re.findall(r'operator\(\s*"(texel\.[a-z_0-9]+)"', ui))

    hidden = sorted(ops - shown - internal)
    phantom = sorted(shown - ops)
    print(f"[info] {len(ops)} operators, {len(internal)} internal, "
          f"{len(ops & shown)} with a button")
    if hidden:
        state["fails"].append(f"{len(hidden)} operators have no button: {hidden[:6]}")
    if phantom:
        state["fails"].append(f"panel references a non-existent operator: {phantom}")
    print(f"[{'ok  ' if not hidden else 'FAIL'}] every usable operator has a button")
    print(f"[{'ok  ' if not phantom else 'FAIL'}] no panel references a missing operator")


def icon_check():
    """Every icon name must exist. Blender does not raise on a bad one - the
    button just draws blank - so a typo ships silently and forever.

    This does not check whether an icon MEANS the right thing; that needs eyes.
    Doing it by reading identifiers is how PANEL_CLOSE, which draws an X, sat on
    the eraser, and how five icons that were fine got called wrong.
    """
    import re
    valid = {i.identifier for i in
             bpy.types.UILayout.bl_rna.functions["prop"]
             .parameters["icon"].enum_items}
    used = set(re.findall(r'icon="([A-Z_0-9]+)"',
                          io.open(os.path.join(HERE, "tex_ui.py"),
                                  encoding="utf-8").read()))
    from texel.tex_props import TOOLS
    used |= {t[3] for t in TOOLS}
    bad = sorted(used - valid - {"NONE"})
    print(f"[info] {len(used)} distinct icons used", flush=True)
    print(f"[{'ok  ' if not bad else 'FAIL'}] every icon name exists in Blender"
          + ("" if not bad else f"  -> {bad}"), flush=True)
    if bad:
        state["fails"].append(f"invalid icon names: {bad}")


import io  # noqa: E402  (used by coverage_check)


def setup():
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    screen = win().screen
    v3d = max((a for a in screen.areas if a.type == "VIEW_3D"),
              key=lambda a: a.width * a.height)
    with bpy.context.temp_override(window=win(), screen=screen, area=v3d):
        bpy.ops.screen.area_split(direction="VERTICAL", factor=0.45)
    left = min((a for a in screen.areas if a.type == "VIEW_3D"), key=lambda a: a.x)
    left.type = "IMAGE_EDITOR"

    # a cube with a canvas, through the shipped setup operator
    for a in areas("VIEW_3D"):
        region = next(r for r in a.regions if r.type == "WINDOW")
        with bpy.context.temp_override(window=win(), screen=screen, area=a,
                                       region=region):
            bpy.ops.texel.add_cube(size=1.0, texture=32)
        break
    img = next((i for i in bpy.data.images if "Texture" in i.name), None)
    for a in areas("IMAGE_EDITOR"):
        a.spaces.active.image = img
    for a in screen.areas:
        for sp in a.spaces:
            if hasattr(sp, "show_region_ui"):
                sp.show_region_ui = True
    force_tab()

    # give the panels something to draw: palette, layers, frames, a selection
    doc = tex_doc.get(img)
    c = doc.canvas
    for rgba in ((200, 60, 60, 255), (60, 200, 120, 255), (60, 90, 200, 255)):
        c.add_colour(rgba)
    for x, y in R.rect(4, 4, 20, 20, filled=True):
        c.layers[0].set(x, y, 1)
    doc.flush()
    return img


# Each step puts the UI in a different state, because panels draw different
# things depending on it. A panel that only breaks when a canvas has frames is
# still a broken panel.
STEPS = [
    ("plain canvas", lambda img: None),
    ("with layers", lambda img: bpy.ops.texel.layer_add()),
    ("with frames + tracks", lambda img: (bpy.ops.texel.frame_add(copy_previous=False),
                                          bpy.ops.texel.track_add(name="BG", bottom=True))),
    ("onion skin on", lambda img: setattr(bpy.context.scene.texel, "onion_skin", True)),
    ("big brush", lambda img: setattr(bpy.context.scene.texel, "brush_size", 6)),
    ("rect tool", lambda img: setattr(bpy.context.scene.texel, "tool", "RECT")),
    ("fill tool", lambda img: setattr(bpy.context.scene.texel, "tool", "FILL")),
    ("still move", lambda img: setattr(bpy.context.scene.texel,
                                       "showcase_move", "STILL")),
    ("status set", lambda img: setattr(bpy.context.scene.texel, "status",
                                       "a status line to dismiss")),
]


def tick():
    if not state["ready"]:
        coverage_check()
        icon_check()
        state["img"] = setup()
        state["ready"] = True
        return 0.2

    if state["step"] >= len(STEPS):
        n = state["n"]
        if state["fails"]:
            print(f"{len(state['fails'])} FAILED: {state['fails']}", flush=True)
            print("TEXEL PANELS: FAILED", flush=True)
        else:
            print(f"[ok  ] every panel drew in {len(STEPS)} UI states, "
                  f"{n} screenshots", flush=True)
            print("TEXEL PANELS: ALL PASS", flush=True)
        bpy.ops.wm.quit_blender()
        return None

    label, fn = STEPS[state["step"]]
    ed = next((a for a in areas("IMAGE_EDITOR")), None)
    region = next(r for r in ed.regions if r.type == "WINDOW")
    try:
        with bpy.context.temp_override(window=win(), screen=win().screen, area=ed,
                                       region=region, space_data=ed.spaces.active):
            fn(state["img"])
    except Exception as e:
        state["fails"].append(f"{label}: {e}")

    force_tab()
    for a in win().screen.areas:
        a.tag_redraw()
    p = os.path.join(OUT, f"panel_{state['n']:02d}_{label.replace(' ', '_')}.png")
    with bpy.context.temp_override(window=win(), screen=win().screen):
        bpy.ops.screen.screenshot(filepath=p)
    state["n"] += 1
    state["step"] += 1
    return 0.25


bpy.app.timers.register(tick, first_interval=1.0)
