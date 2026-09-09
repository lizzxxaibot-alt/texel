"""Render one environment's cinematic.

  blender --background --factory-startup --python render_env.py -- shrine [frames]

Texel does the texturing AND the texel density: every mesh is cube-unwrapped and
then scaled by texel.density_apply to a per-class target, so architecture and
props each carry a sensible pixel size. That is not decoration - at one global
density a small prop shows only a dozen texels and its detail vanishes.
"""
import math
import os
import subprocess
import sys
import time

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

import envs

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["shrine"]
NAME = argv[0]
NFRAMES = int(argv[1]) if len(argv) > 1 else 216
RES = (1280, 720)
SAMPLES = 40
FPS = 24

ENV = envs.ENVIRONMENTS[NAME]
OUT = os.path.join(HERE, "promo", "envs", NAME)
FR = os.path.join(OUT, "frames")
os.makedirs(FR, exist_ok=True)
for f in os.listdir(FR):
    os.remove(os.path.join(FR, f))


def make_material(name, img):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    tex.interpolation = "Closest"        # texels stay square, always
    tex.extension = "REPEAT"
    tex.location = (-460, 220)
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.93
    bsdf.inputs["Specular IOR Level"].default_value = 0.08
    return mat


def apply_density():
    """Cube-unwrap everything, then let Texel set the pixel size per class."""
    import texel as _t
    try:
        _t.register()
    except Exception:
        pass
    arch_names = ENV["arch"]
    d_arch, d_prop = ENV["dens"]
    n_a = n_p = 0
    for o in [x for x in bpy.data.objects
              if x.type == "MESH" and x.name != "FogVolume"]:
        base = o.name.split(".")[0]
        is_arch = any(base.startswith(a) for a in arch_names)
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
            if is_arch:
                n_a += 1
            else:
                n_p += 1
    bpy.ops.object.select_all(action="DESELECT")
    print(f"[texel] {NAME}: {n_a} architecture @ {d_arch} px/unit, "
          f"{n_p} props @ {d_prop} px/unit", flush=True)


def main():
    t0 = time.perf_counter()
    bpy.ops.wm.read_factory_settings(use_empty=True)

    images = ENV["tex"]()
    seams = {k: round(v.get("texel_seam", -1), 1) for k, v in images.items()}
    mats = {k: make_material(k, v) for k, v in images.items()}
    ENV["build"](mats)
    ENV["light"]()
    apply_density()

    cam_d = bpy.data.cameras.new("Cam")
    cam_d.lens = 38
    cam_d.dof.use_dof = True
    cam_d.dof.aperture_fstop = 3.2
    cam = bpy.data.objects.new("Cam", cam_d)
    bpy.context.collection.objects.link(cam)
    bpy.context.scene.camera = cam
    tgt = bpy.data.objects.new("Target", None)
    bpy.context.collection.objects.link(tgt)
    con = cam.constraints.new("TRACK_TO")
    con.target = tgt
    con.track_axis, con.up_axis = "TRACK_NEGATIVE_Z", "UP_Y"
    cam_d.dof.focus_object = tgt

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
        print(f"[warn] CPU fallback: {e}")
    sc.cycles.samples = SAMPLES
    sc.cycles.use_denoising = True
    sc.cycles.volume_step_rate = 4.0      # cheap volumetrics; fog is soft anyway
    sc.cycles.volume_max_steps = 64
    sc.render.resolution_x, sc.render.resolution_y = RES
    sc.render.image_settings.file_format = "PNG"
    # AgX Base, not Medium-High Contrast: the contrasty look crushes shadow
    # detail in fogged interiors and makes a moody scene read as a black frame.
    sc.view_settings.look = "AgX - Base Contrast"
    sc.view_settings.exposure = ENV.get("exposure", 0.0)

    for i in range(NFRAMES):
        loc, look = ENV["cam"](i / max(1, NFRAMES - 1))
        cam.location = loc
        tgt.location = look
        sc.render.filepath = os.path.join(FR, f"f_{i:04d}")
        bpy.ops.render.render(write_still=True)
        if i and i % 40 == 0:
            el = time.perf_counter() - t0
            print(f"  {NAME} {i}/{NFRAMES}  {el:.0f}s  "
                  f"eta {el / i * (NFRAMES - i):.0f}s", flush=True)

    dst = os.path.join(HERE, "promo", f"env-{NAME}.mp4")
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS),
                        "-i", os.path.join(FR, "f_%04d.png"), "-c:v", "libx264",
                        "-pix_fmt", "yuv420p", "-crf", "17", dst],
                       capture_output=True, text=True)
    print(f"TEXEL_ENV_DONE name={NAME} frames={NFRAMES} "
          f"secs={time.perf_counter()-t0:.0f} seams={seams} "
          f"mp4={'ok' if r.returncode == 0 else r.stderr[:120]}", flush=True)


if __name__ == "__main__":
    main()
