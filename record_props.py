"""Record the eight sprite props being painted onto REAL models. Not shipped.

  blender --background --factory-startup --python record_props.py -- [name ...]

Replaces the half of record.py that hung a single-view sprite on an angled
plane. Here the left half of the frame is the texture ATLAS - every face of
every part, in one image - and the right half is the model wearing that exact
image. They are the same bpy image, so they cannot drift.

The reveal mechanic is record.py's: diff the canvas before and after each stage
and uncover the changed texels in chunks, rendering a frame each time. The
difference is what is being revealed. A sprite could only ever appear on a card;
an atlas appears on the object.

grass-tile and brick-tile are not here. They are tiles, they were already on a
cube, and they were already right.
"""
from __future__ import annotations
import math
import os
import subprocess
import sys
import time

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from core import canvas as C                                  # noqa: E402
from core import raster as R                                  # noqa: E402
import models3d as M                                          # noqa: E402
import props3d as P                                           # noqa: E402

OUT = os.path.join(HERE, "gallery")
FRAMES = os.path.join(OUT, "_frames")
os.makedirs(OUT, exist_ok=True)
os.makedirs(FRAMES, exist_ok=True)

CHUNKS_PER_STAGE = 6
HOLD = 8
RES = (720, 480)
SAMPLES = 28
FPS = 12
FFMPEG = (r"C:\Users\opule\AppData\Local\Microsoft\WinGet\Packages"
          r"\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
          r"\ffmpeg-9.0-full_build\bin\ffmpeg.exe")


def aim(obj, target):
    lx, ly, lz = obj.location
    dx, dy, dz = target[0] - lx, target[1] - ly, target[2] - lz
    obj.rotation_euler = (math.atan2(math.hypot(dx, dy), -dz), 0,
                          math.atan2(dy, dx) - math.pi / 2)


def backing_image(n=16):
    """A transparency checker, painted with Texel's own raster.

    The atlas has alpha wherever no part was allocated, so without something
    behind it the empty regions render as holes onto the world and the canvas
    reads as ragged rather than as an unfinished texture. A checker says
    "nothing here yet", which is what every pixel editor uses it for.
    """
    c = C.Canvas(n, n)
    L = c.layers[0]
    a = c.add_colour((38, 36, 44, 255))
    b = c.add_colour((30, 28, 36, 255))
    for p in R.rect(0, 0, n - 1, n - 1, filled=True):
        L.set(*p, a if ((p[0] // 2) + (p[1] // 2)) % 2 else b)
    img = bpy.data.images.new("CanvasBacking", n, n, alpha=True)
    img.pixels.foreach_set(c.to_blender_floats())
    img.update()
    return img


def build_scene(img, model, height_texels, turn=28):
    """Atlas on the left, the model it dresses on the right, one camera on both.

    The model is scaled so every prop reads at about the same size regardless of
    how many texels tall it is - otherwise the coin is a speck and the door
    fills the frame.
    """
    # ---- the atlas, square to camera
    # the camera sees x in [-2.9, 2.9] at this distance; a 2.6 plane centred at
    # -2.15 ran off the left edge, so half the atlas was never on screen
    bpy.ops.mesh.primitive_plane_add(size=2.35, location=(-1.45, 0, 1.42),
                                     rotation=(math.radians(90), 0, 0))
    canvas = bpy.context.active_object
    canvas.name = "Atlas"
    mat = bpy.data.materials.new("AtlasMat")
    mat.use_nodes = True
    nt = mat.node_tree
    b = nt.nodes["Principled BSDF"]
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    tex.interpolation = "Closest"
    nt.links.new(tex.outputs["Color"], b.inputs["Base Color"])
    nt.links.new(tex.outputs["Alpha"], b.inputs["Alpha"])
    b.inputs["Roughness"].default_value = 0.9
    b.inputs["Specular IOR Level"].default_value = 0.05
    canvas.data.materials.append(mat)

    # ---- the checker behind it, a hair further from camera
    bpy.ops.mesh.primitive_plane_add(size=2.35, location=(-1.45, 0.02, 1.42),
                                     rotation=(math.radians(90), 0, 0))
    back = bpy.context.active_object
    back.name = "Backing"
    bm = bpy.data.materials.new("BackingMat")
    bm.use_nodes = True
    bnt = bm.node_tree
    bb = bnt.nodes["Principled BSDF"]
    bt = bnt.nodes.new("ShaderNodeTexImage")
    bt.image = backing_image()
    bt.interpolation = "Closest"
    bt.extension = "REPEAT"
    bnt.links.new(bt.outputs["Color"], bb.inputs["Base Color"])
    bb.inputs["Roughness"].default_value = 0.95
    bb.inputs["Specular IOR Level"].default_value = 0.02
    back.data.materials.append(bm)

    # ---- the model
    want = 2.0
    s = want / max(height_texels * M.TEXEL, 1e-6)
    model.scale = (s, s, s)
    model.location = (1.5, 0.2, 0.0)
    model.rotation_euler = (0, 0, math.radians(turn))

    # ---- floor
    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0))
    fm = bpy.data.materials.new("Floor")
    fm.use_nodes = True
    fb = fm.node_tree.nodes["Principled BSDF"]
    fb.inputs["Base Color"].default_value = (0.035, 0.032, 0.04, 1)
    fb.inputs["Roughness"].default_value = 0.95
    bpy.context.active_object.data.materials.append(fm)

    for name, loc, energy, size, col in (
            ("Key", (-3.0, -4.0, 5.4), 300, 4.0, (1.0, 0.95, 0.88)),
            ("Fill", (4.0, -3.2, 2.6), 120, 5.0, (0.68, 0.78, 1.0)),
            ("Rim", (1.2, 4.4, 4.0), 260, 2.4, (1.0, 0.74, 0.44))):
        d = bpy.data.lights.new(name, "AREA")
        d.energy, d.size, d.color = energy, size, col
        o = bpy.data.objects.new(name, d)
        o.location = loc
        o.visible_camera = False
        bpy.context.collection.objects.link(o)
        aim(o, (0, 0, 1.1))

    cd = bpy.data.cameras.new("Cam")
    cd.lens = 46
    cam = bpy.data.objects.new("Cam", cd)
    bpy.context.collection.objects.link(cam)
    cam.location = (0.0, -7.4, 2.6)
    aim(cam, (0.0, 0.0, 1.35))
    bpy.context.scene.camera = cam

    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    try:
        sc.cycles.device = "GPU"
        prefs = bpy.context.preferences.addons["cycles"].preferences
        prefs.compute_device_type = "OPTIX"
        prefs.get_devices()
        for dv in prefs.devices:
            dv.use = True
    except Exception as e:
        print(f"[warn] CPU fallback: {e}", flush=True)
    sc.cycles.samples = SAMPLES
    sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = RES
    sc.render.image_settings.file_format = "PNG"
    sc.view_settings.look = "AgX - Base Contrast"
    sc.world = bpy.data.worlds.new("W")
    sc.world.use_nodes = True
    sc.world.node_tree.nodes["Background"].inputs["Color"].default_value = (
        0.02, 0.019, 0.024, 1)


def record(kind):
    t0 = time.perf_counter()
    bpy.ops.wm.read_factory_settings(use_empty=True)   # BEFORE the image exists

    atlas, parts, rects, spec = P.allocate(kind)
    stages = P.stages_for(atlas, rects, spec, kind)

    img = bpy.data.images.new(f"Texel {kind}", atlas.size, atlas.size, alpha=True)
    img.pixels.foreach_set([0.0] * (atlas.size * atlas.size * 4))
    img.update()

    model = M.build(kind.title(), parts, atlas, image=img)
    build_scene(img, model, spec["height"], spec.get("turn", 28))
    sc = bpy.context.scene

    layer = atlas.L
    frame = 0

    def shoot():
        nonlocal frame
        img.pixels.foreach_set(atlas.c.to_blender_floats())
        img.update()
        sc.render.filepath = os.path.join(FRAMES, f"{kind}_{frame:04d}")
        bpy.ops.render.render(write_still=True)
        frame += 1

    shoot()                                   # blank, so the reveal is visible
    for label, step in stages:
        before = bytearray(layer.px)
        step()
        after = bytearray(layer.px)
        changed = [i for i in range(len(after)) if after[i] != before[i]]
        if not changed:
            print(f"  [warn] stage {label!r} changed nothing", flush=True)
            continue
        layer.px = bytearray(before)
        per = max(1, len(changed) // CHUNKS_PER_STAGE)
        for k in range(0, len(changed), per):
            for i in changed[k:k + per]:
                layer.px[i] = after[i]
            shoot()
        layer.px = after
    for _ in range(HOLD):
        shoot()

    img.filepath_raw = os.path.join(OUT, f"{kind}.png")
    img.file_format = "PNG"
    img.save()

    dst = os.path.join(OUT, f"{kind}.mp4")
    r = subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-framerate", str(FPS),
                        "-i", os.path.join(FRAMES, f"{kind}_%04d.png"),
                        "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
                        dst], capture_output=True, text=True)
    ok = r.returncode == 0 and os.path.exists(dst)
    print(f"[ok] {kind:<8} {frame:>3} frames  {len(atlas.c.palette) - 1} colours  "
          f"{len(model.data.polygons):>4} faces  mp4={'ok' if ok else 'FAIL'}  "
          f"{time.perf_counter() - t0:>5.1f}s", flush=True)
    return ok


def main():
    args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    want = args or (list(P.TILES) + list(P.SPEC))
    bad = [k for k in want if k not in P.SPEC and k not in P.TILES]
    if bad:
        sys.exit(f"unknown prop(s) {bad}; have {sorted(list(P.TILES) + list(P.SPEC))}")
    fails = [k for k in want if not record(k)]
    print(f"PROPS_DONE ok={len(want) - len(fails)} fail={len(fails)}"
          + (f" -> {fails}" if fails else ""), flush=True)


if __name__ == "__main__":
    main()
