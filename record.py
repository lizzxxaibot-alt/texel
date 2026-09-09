"""Generate the ten assets and RECORD each one being painted.

Not a slideshow: for every stage we diff the canvas before and after, then reveal
the new texels in chunks, rendering a frame each time. So the video shows the
artwork appearing stroke by stroke, driven by the same core the paint operator
uses.

The scene shows both halves of the pitch at once - the flat canvas you paint on,
and the model it lands on, nearest-neighbour so texels stay square.

  blender --background --factory-startup --python record.py
"""
import math
import os
import subprocess
import sys
import time

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import assets as A
from core.canvas import Canvas

OUT = os.path.join(HERE, "gallery")
FRAMES = os.path.join(OUT, "_frames")
os.makedirs(OUT, exist_ok=True)
os.makedirs(FRAMES, exist_ok=True)

CHUNKS_PER_STAGE = 6          # frames each stage is revealed over
HOLD = 8                      # frames held on the finished asset
RES = (720, 480)
SAMPLES = 24
FPS = 12


def build_scene(img, tileable):
    """Canvas on the left, textured model on the right, one camera on both.

    The caller must reset the file BEFORE creating `img` - read_factory_settings
    wipes bpy.data, which invalidates any image made ahead of it.
    """
    mat = bpy.data.materials.new("TexelMat")
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    tex.interpolation = "Closest"
    tex.extension = "REPEAT"
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(tex.outputs["Alpha"], bsdf.inputs["Alpha"])
    bsdf.inputs["Roughness"].default_value = 0.9
    bsdf.inputs["Specular IOR Level"].default_value = 0.06
    mat.blend_method = "CLIP" if hasattr(mat, "blend_method") else mat.blend_method

    # left: the flat canvas, square to camera
    bpy.ops.mesh.primitive_plane_add(size=3.2, location=(-2.3, 0, 1.6),
                                     rotation=(math.radians(90), 0, 0))
    canvas = bpy.context.active_object
    canvas.name = "Canvas"
    canvas.data.materials.append(mat)

    # right: what the texture is FOR.
    # A tile belongs on a block - that is the point of it. A sprite has
    # transparency, and wrapping that round a cube renders it hollow and
    # see-through, which looks broken. Sprites get an angled card instead,
    # which is how a 2D sprite actually appears in a 3D scene.
    if tileable:
        bpy.ops.mesh.primitive_cube_add(size=2.2, location=(2.1, 0.4, 1.1))
        model = bpy.context.active_object
        model.rotation_euler = (0, 0, math.radians(28))
        bpy.ops.object.shade_flat()
    else:
        bpy.ops.mesh.primitive_plane_add(size=3.0, location=(2.2, 0.6, 1.55),
                                         rotation=(math.radians(90), 0,
                                                   math.radians(-26)))
        model = bpy.context.active_object
    model.data.materials.append(mat)

    # floor
    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0))
    fm = bpy.data.materials.new("Floor")
    fm.use_nodes = True
    fm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (
        0.035, 0.032, 0.04, 1)
    fm.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.95
    bpy.context.active_object.data.materials.append(fm)

    cam_d = bpy.data.cameras.new("Cam")
    cam_d.lens = 46
    cam = bpy.data.objects.new("Cam", cam_d)
    bpy.context.collection.objects.link(cam)
    cam.location = (0.2, -8.6, 3.4)
    cam.rotation_euler = (math.radians(80), 0, 0)
    bpy.context.scene.camera = cam

    key = bpy.data.lights.new("Key", "AREA")
    key.energy, key.size = 1400, 9
    ko = bpy.data.objects.new("Key", key)
    bpy.context.collection.objects.link(ko)
    ko.location = (-3, -6, 8)
    ko.rotation_euler = (math.radians(28), 0, math.radians(-20))

    rim = bpy.data.lights.new("Rim", "AREA")
    rim.energy, rim.size = 500, 6
    rim.color = (1.0, 0.62, 0.3)
    ro = bpy.data.objects.new("Rim", rim)
    bpy.context.collection.objects.link(ro)
    ro.location = (6, 4, 4)
    ro.rotation_euler = (math.radians(70), 0, math.radians(120))

    w = bpy.data.worlds.new("W")
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs["Color"].default_value = (0.015, 0.015, 0.02, 1)
    bpy.context.scene.world = w

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
        print(f"[warn] no GPU, using CPU: {e}")
    sc.cycles.samples = SAMPLES
    sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = RES
    sc.render.image_settings.file_format = "PNG"
    sc.render.film_transparent = False
    return canvas, model


def record(slug, name, fn, tileable):
    """Paint one asset, capturing frames as it appears."""
    c = Canvas(A.SIZE, A.SIZE)
    stages = fn(c)                       # binds the step closures to THIS canvas

    bpy.ops.wm.read_factory_settings(use_empty=True)   # before the image, not after
    img = bpy.data.images.new(f"Texel {name}", A.SIZE, A.SIZE, alpha=True)
    img.pixels.foreach_set([0.0] * (A.SIZE * A.SIZE * 4))
    img.update()
    build_scene(img, tileable)
    sc = bpy.context.scene

    layer = c.layers[0]
    frame = 0
    t0 = time.perf_counter()

    def shoot():
        nonlocal frame
        img.pixels.foreach_set(c.to_blender_floats())
        img.update()
        sc.render.filepath = os.path.join(FRAMES, f"{slug}_{frame:04d}")
        bpy.ops.render.render(write_still=True)
        frame += 1

    shoot()                              # empty canvas, so the reveal is visible
    for label, step in stages:
        before = bytearray(layer.px)
        step()
        after = bytearray(layer.px)
        changed = [i for i in range(len(after)) if after[i] != before[i]]
        if not changed:
            continue
        layer.px = bytearray(before)     # rewind, then reveal in chunks
        per = max(1, len(changed) // CHUNKS_PER_STAGE)
        for k in range(0, len(changed), per):
            for i in changed[k:k + per]:
                layer.px[i] = after[i]
            shoot()
        layer.px = after                 # make sure nothing is left behind
    for _ in range(HOLD):
        shoot()

    # deliverables
    img.filepath_raw = os.path.join(OUT, f"{slug}.png")
    img.file_format = "PNG"
    img.save()

    from core import tools as T
    seam = T.tile_seam_score(c.flatten(), c.w, c.h, c.palette)
    dt = time.perf_counter() - t0
    print(f"[ok] {slug:<12} {frame:>3} frames  {len(c.palette)-1} colours  "
          f"{dt:>5.1f}s" + (f"  tiling {seam['score']}%" if tileable else ""))
    return frame, seam


def encode(slug):
    src = os.path.join(FRAMES, f"{slug}_%04d.png")
    dst = os.path.join(OUT, f"{slug}.mp4")
    r = subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", src,
         "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2", "-c:v", "libx264",
         "-pix_fmt", "yuv420p", "-crf", "18", dst],
        capture_output=True, text=True)
    if r.returncode != 0:
        print(f"[FAIL] ffmpeg {slug}: {r.stderr.strip()[:200]}")
        return None
    return dst


if __name__ == "__main__":
    print(f"Recording {len(A.ASSETS)} assets at {RES[0]}x{RES[1]}, {SAMPLES} samples\n")
    total = time.perf_counter()
    made = []
    for slug, name, fn, tileable in A.ASSETS:
        n, seam = record(slug, name, fn, tileable)
        mp4 = encode(slug)
        if mp4:
            made.append((slug, n, os.path.getsize(mp4) // 1024))
    print(f"\n{'asset':<14} {'frames':>7} {'mp4 KB':>8}")
    for slug, n, kb in made:
        print(f"{slug:<14} {n:>7} {kb:>8}")
    print(f"\n{len(made)}/{len(A.ASSETS)} recorded in {time.perf_counter()-total:.0f}s")
    print(f"PNGs and MP4s in: {OUT}")
