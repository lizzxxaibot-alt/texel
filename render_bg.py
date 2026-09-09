"""Render an environment as a WIDE page background. Tooling, not shipped.

  blender --background --factory-startup --python render_bg.py -- ruins

The store page's background is `background-attachment: fixed`, so the browser
shows exactly one viewport-sized crop of it, anchored top-centre, at the image's
natural size. That makes tiling the wrong tool: any repeat of a 16:9 render puts
a hard sky-meets-floor seam across the margins (measured - see cand_C). The fix
is not a cleverer tile, it is an image wide and tall enough that a repeat never
has to happen: 3440x1440 covers every common monitor.

So this re-renders the same camera position as the still, on a much wider lens,
instead of upscaling or mirroring the 1280x720 frame. The scene is the same
scene; only the framing is new.
"""
import math
import os
import sys
import time

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

import envs                                                    # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["ruins"]
NAME = argv[0]
OUT = os.path.join(HERE, "store", "theme", "_bg_src")
os.makedirs(OUT, exist_ok=True)

# `harvest_stills.take()` picks the first still at int(216 * 0.08) = frame 17 of
# 216, so this is the exact camera the chosen still was shot on.
T = 17 / 215

# Widening the still's own camera FAILED (measured): the set is 44 units of sand
# with six pillars on it, so at 74deg the frame is mostly empty ground and the
# sand plane's far edge cuts a hard line against the sky - a diorama on a table.
# The fix is to move IN instead of pulling back: stand inside the colonnade so
# pillars flank the frame, the lintel caps it and the wall closes the back, then
# raise the haze so the little sky that is left reads as desert air.
#
# (label, w, h, lens, cam_loc, look_at, fog_density)
# h3 is the keeper. It is rendered 2880 tall rather than 1440 so make_bg can
# crop rows 720..2879: that is h3's exact framing with 720 rows MORE floor under
# it. The extra height is not decoration - at 1440 the fixed background tiled
# vertically on any viewport past 1440px (4K desktops), and row 1439 is warm
# ground meeting row 0's cool sky: a hard, ugly seam, on the page of a tool that
# advertises seam checking. 2160 clears every viewport in use.
VARIANTS = [
    ("h3tall", 2400, 2880, 28, (0.0, -15.0, 9.0), (0.0, 8.0, 0.8), 0.0050),
]
SAMPLES = 48


def make_material(name, img):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    tex.interpolation = "Closest"
    tex.extension = "REPEAT"
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.93
    bsdf.inputs["Specular IOR Level"].default_value = 0.08
    return mat


def apply_density(env):
    import texel as _t
    try:
        _t.register()
    except Exception:
        pass
    d_arch, d_prop = env["dens"]
    for o in [x for x in bpy.data.objects
              if x.type == "MESH" and x.name != "FogVolume"]:
        is_arch = any(o.name.split(".")[0].startswith(a) for a in env["arch"])
        bpy.context.scene.texel.target_density = d_arch if is_arch else d_prop
        bpy.ops.object.select_all(action="DESELECT")
        o.select_set(True)
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.uv.cube_project(cube_size=1.0)
        bpy.ops.object.mode_set(mode="OBJECT")
        if bpy.ops.texel.density_apply.poll():
            bpy.ops.texel.density_apply()
    bpy.ops.object.select_all(action="DESELECT")


def set_fog(density):
    """Retune the env's haze box. envs._fog builds it at build time; the frame
    behind a text column wants far more of it than a cinematic does, because
    haze is what hides the edge of a 44-unit sand plane."""
    o = bpy.data.objects.get("FogVolume")
    if not o or not o.data.materials:
        print("[warn] no FogVolume to retune", flush=True)
        return
    for n in o.data.materials[0].node_tree.nodes:
        if n.type == "VOLUME_SCATTER":
            n.inputs["Density"].default_value = density


def widen_ground(ground, times=3.0):
    """Grow the floor slab and the haze box that sits over it.

    A cinematic frames away from the edges; a 3440-wide still does not, and at
    this camera the sand plane's far corners showed sky BELOW the horizon. The
    slab is scaled BEFORE density_apply so Texel re-derives the UVs and the
    ground keeps its 9 px/unit - scaling afterwards would have stretched every
    texel to a third of its size.
    """
    for name, s in ((ground, times), ("FogVolume", max(1.0, times * 0.8))):
        o = bpy.data.objects.get(name)
        if o is None:
            print(f"[warn] no {name} to widen", flush=True)
            continue
        o.scale = (s, s, 1.0)


def main():
    t0 = time.perf_counter()
    env = envs.ENVIRONMENTS[NAME]
    bpy.ops.wm.read_factory_settings(use_empty=True)

    mats = {k: make_material(k, v) for k, v in env["tex"]().items()}
    ground = env["build"](mats)          # build returns the ground slab's key
    env["light"]()
    widen_ground({"sand": "Sand", "ground": "Ground", "floor": "Floor",
                  "snow": "Snow"}.get(ground, "Sand"))
    apply_density(env)

    cam_d = bpy.data.cameras.new("Cam")
    # AUTO fits the sensor to the LARGER dimension, so a 2400x2880 render would
    # silently re-frame against the vertical axis and stop being a taller crop
    # of the same shot. Pin it.
    cam_d.sensor_fit = "HORIZONTAL"
    # No depth of field. The still had f/3.2 to sell a cinematic move; a blurred
    # background behind a text column just reads as an out-of-focus photo.
    cam = bpy.data.objects.new("Cam", cam_d)
    bpy.context.collection.objects.link(cam)
    bpy.context.scene.camera = cam
    tgt = bpy.data.objects.new("Target", None)
    bpy.context.collection.objects.link(tgt)
    con = cam.constraints.new("TRACK_TO")
    con.target = tgt
    con.track_axis, con.up_axis = "TRACK_NEGATIVE_Z", "UP_Y"

    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    try:
        sc.cycles.device = "GPU"
        p = bpy.context.preferences.addons["cycles"].preferences
        p.compute_device_type = "OPTIX"
        p.get_devices()
        for d in p.devices:
            d.use = True
    except Exception as e:
        print(f"[warn] CPU fallback: {e}", flush=True)
    sc.cycles.samples = SAMPLES
    sc.cycles.use_denoising = True
    sc.cycles.volume_step_rate = 4.0
    sc.cycles.volume_max_steps = 64
    sc.render.image_settings.file_format = "PNG"
    sc.view_settings.look = "AgX - Base Contrast"
    sc.view_settings.exposure = env.get("exposure", 0.0)

    for label, w, h, lens, loc, look, fog in VARIANTS:
        cam_d.lens = lens
        cam.location = loc
        tgt.location = look
        set_fog(fog)
        sc.render.resolution_x, sc.render.resolution_y = w, h
        sc.render.filepath = os.path.join(OUT, f"{NAME}_{label}")
        bpy.ops.render.render(write_still=True)
        hfov = math.degrees(2 * math.atan(cam_d.sensor_width / (2 * lens)))
        print(f"[bg] {NAME}_{label}  {w}x{h}  {lens}mm  hFOV={hfov:.0f}deg  "
              f"fog={fog}  {time.perf_counter() - t0:.0f}s", flush=True)

    print(f"BG_DONE name={NAME} variants={len(VARIANTS)} out={OUT}", flush=True)


if __name__ == "__main__":
    main()
