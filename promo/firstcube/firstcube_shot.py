"""Wed beat 2026-11-18: the first five minutes. Add 1m Cube, then paint on it.

  blender --factory-startup --enable-event-simulate -p 0 0 1500 900 --python firstcube_shot.py -- <dir holding the extracted texel/>

Same mechanism as promo/dither/dither_shot.py: drives the SHIPPED add-on in a
real window with simulated mouse input, this time in the 3D Viewport, where
strokes are raycast onto the mesh and resolved through its UVs.

texel.add_cube -> texel.setup_viewport -> texel.paint once -> one Fill click,
then on each of the three faces the view shows: one Rect drag (the frame) and
one Line drag (the brace). Between strokes only sidebar properties change.
Every stroke is counted off the canvas and must land inside its own face's
texel rect. Writes shot_full.png + facts.json; exits 1 on any miss.
"""
import json, os, sys, time
import bpy
from bpy_extras import view3d_utils
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = sys.argv[sys.argv.index("--") + 1]
sys.path.insert(0, ROOT)
import texel
texel.register()
from texel import tex_doc, tex_paint as TP
from texel.core import uvmap

try:
    bpy.context.preferences.view.show_splash = False
except Exception:
    pass

N = 64
PLANK = (0.76, 0.52, 0.27, 1)
FRAME = (0.33, 0.19, 0.10, 1)
win = bpy.context.window
area = max(win.screen.areas, key=lambda a: a.width * a.height)
S = {"fails": [], "strokes": []}
T0 = time.time()


def region(t):
    return next(r for r in area.regions if r.type == t)


def rv3d():
    return area.spaces.active.region_3d


def flat():
    return bytes(tex_doc.get(S["img"]).canvas.flatten())


def sim(t, v, x, y):
    win.event_simulate(type=t, value=v, x=int(x), y=int(y))


def force_tab():
    for r in area.regions:
        if r.type == "UI":
            try:
                if r.active_panel_category != "Texel":
                    r.active_panel_category = "Texel"
            except Exception:
                pass
    area.tag_redraw()


def ctx():
    return bpy.context.temp_override(window=win, area=area, region=region("WINDOW"))


# ---------------------------------------------------------------- face maths
def face_info(obj, poly):
    """UV box of a quad, its texel rect, and a (u, v) -> world function."""
    uvs = obj.data.uv_layers.active.data
    pts = [(uvs[li].uv.copy(), obj.data.vertices[obj.data.loops[li].vertex_index].co.copy())
           for li in poly.loop_indices]
    u0, u1 = min(p[0].x for p in pts), max(p[0].x for p in pts)
    v0, v1 = min(p[0].y for p in pts), max(p[0].y for p in pts)

    def corner(u, v):
        return next(co for uv, co in pts if abs(uv.x - u) < 1e-4 and abs(uv.y - v) < 1e-4)

    a, b, d = corner(u0, v0), corner(u1, v0), corner(u0, v1)

    def world(u, v):
        s, t = (u - u0) / (u1 - u0), (v - v0) / (v1 - v0)
        return obj.matrix_world @ (a + s * (b - a) + t * (d - a))

    tx0, ty0 = uvmap.uv_to_texel(u0 + 1e-6, v1 - 1e-6, N, N)
    tx1, ty1 = uvmap.uv_to_texel(u1 - 1e-6, v0 + 1e-6, N, N)
    return {"uv": (u0, v0, u1, v1), "world": world, "rect": (tx0, ty0, tx1, ty1)}


def screen(face, i, j):
    """Window coords of the centre of face-local texel (i, j), j counted down."""
    u0, v0, u1, v1 = face["uv"]
    n = face["rect"][2] - face["rect"][0] + 1
    u = u0 + (i + 0.5) / n * (u1 - u0)
    v = v1 - (j + 0.5) / n * (v1 - v0)
    r = region("WINDOW")
    p = view3d_utils.location_3d_to_region_2d(r, rv3d(), face["world"](u, v))
    return r.x + p.x, r.y + p.y


# -------------------------------------------------------------------- steps
def setup():
    if area.type != "VIEW_3D":
        S["fails"].append(f"largest area is {area.type}")
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    area.spaces.active.show_region_ui = True
    force_tab()


def add_cube():
    with ctx():
        r = bpy.ops.texel.add_cube()
    obj = bpy.context.view_layer.objects.active
    S["obj"] = obj
    node = next(n for n in obj.material_slots[0].material.node_tree.nodes if n.type == "TEX_IMAGE")
    S["img"] = node.image
    S["add_cube"] = {"result": list(r), "object": obj.name, "dimensions": [round(d, 4) for d in obj.dimensions],
                     "image": node.image.name, "image_size": list(node.image.size),
                     "interpolation": node.interpolation, "material": obj.material_slots[0].material.name,
                     "uv_layers": len(obj.data.uv_layers), "faces": len(obj.data.polygons),
                     "canvas_texels_before": sum(1 for v in flat() if v)}
    a = S["add_cube"]
    if (r != {"FINISHED"} or a["image_size"] != [N, N] or a["interpolation"] != "Closest"
            or a["uv_layers"] != 1 or a["canvas_texels_before"] != 0):
        S["fails"].append(f"add_cube: {a}")


def viewport():
    with ctx():
        r = bpy.ops.texel.setup_viewport()
        bpy.ops.view3d.view_selected()
    S["setup_viewport"] = {"result": list(r), "shading": area.spaces.active.shading.type}
    if area.spaces.active.shading.type != "MATERIAL":
        S["fails"].append("viewport not in material preview")


def back_off():
    rv3d().view_distance *= 1.9          # keep the cube clear of the sidebar
    area.tag_redraw()


def wait():
    area.tag_redraw()


def pick_faces():
    obj = S["obj"]
    cam = rv3d().view_matrix.inverted().translation
    vis = []
    for poly in obj.data.polygons:
        c = obj.matrix_world @ poly.center
        n = (obj.matrix_world.to_3x3() @ poly.normal).normalized()
        d = n.dot((cam - c).normalized())
        if d > 0.05:
            vis.append((d, poly.index))
    vis.sort(reverse=True)
    S["faces"] = [face_info(obj, obj.data.polygons[i]) for _, i in vis]
    S["face_report"] = [{"poly": i, "facing": round(d, 3), "texel_rect": list(f["rect"])}
                        for (d, i), f in zip(vis, S["faces"])]
    if len(S["faces"]) != 3:
        S["fails"].append(f"{len(S['faces'])} faces toward the view, want 3")
    ui = region("UI")
    for f in S["faces"]:
        for i, j in ((0, 0), (15, 0), (0, 15), (15, 15)):
            x, y = screen(f, i, j)
            if not TP.over_canvas(area, region("WINDOW"), int(x), int(y)):
                S["fails"].append(f"face corner under a panel at {int(x)},{int(y)} (sidebar x={ui.x})")


def enter():
    with bpy.context.temp_override(window=win, area=area, region=region("UI")):
        r = bpy.ops.texel.paint("INVOKE_DEFAULT")
    S["enter"] = list(r)
    if not (r == {"RUNNING_MODAL"} and TP.paint_mode_on(area)):
        S["fails"].append(f"enter: {r}")


def fill():
    S["before"] = flat()
    s = bpy.context.scene.texel
    s.tool, s.colour, s.contiguous, s.tolerance = "FILL", PLANK, True, 0
    s.dither, s.mirror_x, s.mirror_y, s.symmetry, s.use_pressure = "OFF", False, False, 1, False
    x, y = screen(S["faces"][0], 8, 8)
    sim("MOUSEMOVE", "NOTHING", x, y)
    sim("LEFTMOUSE", "PRESS", x, y)
    sim("LEFTMOUSE", "RELEASE", x, y)


def fill_check():
    f = flat()
    S["fill_texels"] = sum(1 for v in f if v)
    if S["fill_texels"] != N * N or len(set(f)) != 1:
        S["fails"].append(f"fill: {S['fill_texels']} texels, indices {sorted(set(f))}")


def drag(fi, tool, a, b):
    def go():
        S["before"] = flat()
        s = bpy.context.scene.texel
        s.tool, s.colour, s.filled, s.pixel_perfect = tool, FRAME, False, True
        s.brush_size, s.brush_shape = 1, "SQUARE"
        f = S["faces"][fi]
        steps = 15
        sim("MOUSEMOVE", "NOTHING", *screen(f, *a))
        sim("LEFTMOUSE", "PRESS", *screen(f, *a))
        for k in range(1, steps + 1):
            i = a[0] + (b[0] - a[0]) * k / steps
            j = a[1] + (b[1] - a[1]) * k / steps
            sim("MOUSEMOVE", "NOTHING", *screen(f, i, j))
        sim("LEFTMOUSE", "RELEASE", *screen(f, *b))
    return go


def drag_check(fi, tool, want):
    def go():
        b, a = S["before"], flat()
        changed = [n for n in range(N * N) if a[n] != b[n]]
        x0, y0, x1, y1 = S["faces"][fi]["rect"]
        inside = all(x0 <= n % N <= x1 and y0 <= n // N <= y1 for n in changed)
        S["strokes"].append({"face": fi, "tool": tool, "texels_changed": len(changed), "expected": want,
                             "inside_face_rect": inside, "mode_on_after": TP.paint_mode_on(area)})
        if len(changed) != want or not inside or not TP.paint_mode_on(area):
            S["fails"].append(f"face {fi} {tool}: {len(changed)} (want {want}), inside={inside}")
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
    S["palette_used"] = len(set(f))
    S["blender"] = bpy.app.version_string
    S["texel_from"] = texel.__file__
    s = bpy.context.scene.texel
    S["panel_at_shot"] = {"tool": s.tool, "size": s.brush_size}


def done():
    for k in ("img", "before", "obj", "faces"):
        S.pop(k, None)
    with open(os.path.join(HERE, "facts.json"), "w") as f:
        json.dump(S, f, indent=2)
    print("FACTS", json.dumps(S), flush=True)
    os._exit(1 if S["fails"] else 0)


STEPS = [setup, add_cube, viewport, wait, back_off, wait, wait, pick_faces, enter, fill, fill_check]
for fi in range(3):
    STEPS += [drag(fi, "RECT", (0, 0), (15, 15)), drag_check(fi, "RECT", 60),
              drag(fi, "LINE", (1, 14), (14, 1)), drag_check(fi, "LINE", 14)]
STEPS += [wait, wait, wait, shot, shot, done]


def step():
    if time.time() - T0 > 240:
        S["fails"].append("watchdog")
        done()
    fn = STEPS.pop(0)
    try:
        force_tab()
        fn()
    except Exception as e:
        import traceback
        traceback.print_exc()
        S["fails"].append(f"{getattr(fn, '__name__', fn)}: {e!r}")
        done()
    return 0.8


bpy.app.timers.register(step, first_interval=2.0)
