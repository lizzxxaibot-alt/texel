"""Wed beat 2026-11-25: Detect Density, Apply, Detect again, in the 3D Viewport.

  blender --factory-startup -p 0 0 1500 900 --python density_cap.py -- <dir holding the extracted texel/>

Drives the SHIPPED add-on in a real window (the firstcube_shot.py pattern).
Scene: three Blender default cubes (4 m, 1 m, 0.5 m), joined, one 64x64 tile.
Default cube UVs give every face the same 16 texels whatever its size, so the
drift is Blender's out-of-the-box behaviour, not a rigged layout.

texel.density_detect -> screenshot -> target typed to 16 -> texel.density_apply
-> texel.density_detect -> screenshot. Every face's density is ALSO measured
here from the mesh's own UVs and areas, without the add-on's maths, and must
agree with what the add-on's readout says. Exits 1 on any miss.
"""
import json, os, sys, time
import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = sys.argv[sys.argv.index("--") + 1]
sys.path.insert(0, ROOT)
import texel
texel.register()

try:
    bpy.context.preferences.view.show_splash = False
except Exception:
    pass

TILE = os.path.normpath(os.path.join(HERE, "..", "shots", "market", "tile_timber.png"))
SIZES = ((4.0, (0.0, 0.0, 2.0)), (1.0, (3.0, -1.2, 0.5)), (0.5, (3.0, -2.6, 0.25)))
TARGET = 16.0
win = bpy.context.window
area = max(win.screen.areas, key=lambda a: a.width * a.height)
S = {"fails": [], "sizes_m": [s for s, _ in SIZES], "target": TARGET}
T0 = time.time()


def region(t):
    return next(r for r in area.regions if r.type == t)


def ctx():
    return bpy.context.temp_override(window=win, area=area, region=region("WINDOW"))


def force_tab():
    for r in area.regions:
        if r.type == "UI":
            try:
                if r.active_panel_category != "Texel":
                    r.active_panel_category = "Texel"
            except Exception:
                pass
    area.tag_redraw()


def own_density():
    """Per-face px/unit from the mesh itself: sqrt(uv area) * image px / sqrt(world area)."""
    obj, img = S["obj"], S["img"]
    px = max(img.size)
    uv = obj.data.uv_layers.active.data
    out = []
    for p in obj.data.polygons:
        pts = [uv[li].uv for li in p.loop_indices]
        a = 0.0
        for i in range(1, len(pts) - 1):
            x1, y1 = pts[i][0] - pts[0][0], pts[i][1] - pts[0][1]
            x2, y2 = pts[i + 1][0] - pts[0][0], pts[i + 1][1] - pts[0][1]
            a += abs(x1 * y2 - x2 * y1) * 0.5
        out.append((a ** 0.5) * px / (p.area ** 0.5))
    return out


def summary(v):
    return {"faces": len(v), "lo": round(min(v), 3), "hi": round(max(v), 3),
            "avg": round(sum(v) / len(v), 3), "spread": round(max(v) / min(v), 3),
            "distinct": sorted({round(x, 2) for x in v})}


def build():
    if area.type != "VIEW_3D":
        S["fails"].append(f"largest area is {area.type}")
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    img = bpy.data.images.load(TILE)
    mat = bpy.data.materials.new("Timber")
    mat.use_nodes = True
    nt = mat.node_tree
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image, tex.interpolation = img, "Closest"
    nt.links.new(tex.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"])
    with ctx():
        for size, loc in SIZES:
            bpy.ops.mesh.primitive_cube_add(size=size, location=loc)
            bpy.context.active_object.data.materials.append(mat)
        bpy.ops.object.select_all(action="SELECT")
        bpy.ops.object.join()
    obj = bpy.context.view_layer.objects.active
    obj.name = "Stall + Crates"
    S["obj"], S["img"] = obj, img
    S["scene"] = {"faces": len(obj.data.polygons), "image": os.path.basename(TILE),
                  "image_size": list(img.size), "interpolation": tex.interpolation,
                  "extension": tex.extension}
    area.spaces.active.show_region_ui = True
    force_tab()


def viewport():
    sp = area.spaces.active
    with ctx():
        r = bpy.ops.texel.setup_viewport()
        bpy.ops.view3d.view_selected()
        bpy.ops.object.select_all(action="DESELECT")
    sp.overlay.show_cursor = False
    sp.overlay.show_object_origins = False
    S["setup_viewport"] = {"result": list(r), "shading": sp.shading.type}
    if sp.shading.type != "MATERIAL":
        S["fails"].append("viewport not in material preview")


def back_off():
    area.spaces.active.region_3d.view_distance *= 1.25
    area.tag_redraw()


def wait():
    area.tag_redraw()


def detect(key):
    def go():
        with ctx():
            r = bpy.ops.texel.density_detect()
        S[key] = {"result": list(r), "readout": bpy.context.scene.texel.status.split("\n"),
                  "target_after_detect": bpy.context.scene.texel.target_density,
                  "own": summary(own_density())}
        if r != {"FINISHED"}:
            S["fails"].append(f"{key}: {r}")
    go.__name__ = "detect_" + key
    return go


def apply():
    bpy.context.scene.texel.target_density = TARGET
    with ctx():
        r = bpy.ops.texel.density_apply()
    S["apply"] = {"result": list(r), "status": bpy.context.scene.texel.status}
    if r != {"FINISHED"}:
        S["fails"].append(f"apply: {r}")


def shot(name):
    def go():
        force_tab()
        for a in win.screen.areas:
            a.tag_redraw()
        with bpy.context.temp_override(window=win, screen=win.screen):
            bpy.ops.screen.screenshot(filepath=os.path.join(HERE, name))
    go.__name__ = "shot_" + name
    return go


def done():
    b, a = S.get("before", {}), S.get("after", {})
    if b and a:
        bo, ao = b["own"], a["own"]
        # before: three sizes, three densities, 16 texels across every face
        if bo["distinct"] != [4.0, 16.0, 32.0] or bo["faces"] != 18:
            S["fails"].append(f"before own: {bo}")
        if ao["distinct"] != [TARGET] or ao["faces"] != 18:
            S["fails"].append(f"after own: {ao}")
        # the add-on's readout must say what the mesh says
        want_b = [f"{bo['avg']:.1f} px/unit average", f"range {bo['lo']:.1f} - {bo['hi']:.1f}",
                  f"{bo['spread']:.1f}x spread"]
        want_a = [f"{ao['avg']:.1f} px/unit average", f"range {ao['lo']:.1f} - {ao['hi']:.1f}",
                  f"{ao['spread']:.1f}x spread"]
        if b["readout"] != want_b:
            S["fails"].append(f"before readout {b['readout']} != {want_b}")
        if a["readout"] != want_a:
            S["fails"].append(f"after readout {a['readout']} != {want_a}")
        if S["apply"]["status"] != f"18 faces set to {TARGET:.1f} px/unit":
            S["fails"].append(f"apply status: {S['apply']['status']}")
    else:
        S["fails"].append("missing before/after")
    S["tab"] = region("UI").active_panel_category
    S["area"] = {"x": area.x, "y": area.y, "w": area.width, "h": area.height}
    S["window"] = {"w": win.width, "h": win.height}
    S["blender"] = bpy.app.version_string
    S["texel_from"] = texel.__file__
    S["texel_version"] = list(texel.bl_info.get("version", ())) if hasattr(texel, "bl_info") else None
    for k in ("img", "obj"):
        S.pop(k, None)
    with open(os.path.join(HERE, "facts.json"), "w") as f:
        json.dump(S, f, indent=2)
    print("FACTS", json.dumps(S), flush=True)
    os._exit(1 if S["fails"] else 0)


STEPS = [build, viewport, wait, back_off, wait, wait, wait, detect("before"), wait, wait,
         shot("before_full.png"), shot("before_full.png"), apply, detect("after"), wait, wait, wait,
         shot("after_full.png"), shot("after_full.png"), done]


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
