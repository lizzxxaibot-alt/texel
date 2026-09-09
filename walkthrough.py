"""The torchbearer walks down a corridor of Texel-painted tiles.

The logic the earlier renders got wrong: a character sprite is not a tile. You
do not wrap a man with a torch around a crate. He walks THROUGH the tiles.

So this scene uses Texel for what each job actually needs:
  * three seamless tiles - flagstone floor, block wall, pillar stone - on the
    geometry, all set to ONE texel density with texel.density_apply
  * the 8-frame walk cycle as an animated sprite on a card, exported from the
    same file that drew the cave, just with the Cave and Glow tracks hidden.
    That is the cel model earning its keep: one document, two deliverables.

  blender --background --factory-startup --python walkthrough.py -- 192
"""
import math
import os
import subprocess
import sys
import time

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
NFRAMES = int(argv[0]) if argv else 192
RES = (1280, 720)
SAMPLES = 48
FPS = 24

OUT = os.path.join(HERE, "promo", "walk")
FR = os.path.join(OUT, "frames")
SPR = os.path.join(OUT, "sprite")
for d in (OUT, FR, SPR):
    os.makedirs(d, exist_ok=True)
for f in os.listdir(FR):
    os.remove(os.path.join(FR, f))

import texel
from texel import tex_doc
from texel.core import raster as R
from texel.core import tools as TT

texel.register()
import demo_art as A

TILE = 64
STRIDE = 1.15                   # world units the walk cycle covers, per loop
HOLD = 2                        # render frames per drawing -> 12fps on 24fps


# --------------------------------------------------------------- tile painting
def new_canvas(name):
    bpy.ops.texel.canvas_new(size=TILE, name=name)
    img = bpy.data.images[name]
    return img, tex_doc.get(img)


def paint(name, fn):
    img, doc = new_canvas(name)
    c = doc.canvas
    fn(c, c.layers[0])
    doc.flush()
    img.filepath_raw = os.path.join(OUT, f"tile_{name.lower()}.png")
    img.file_format = "PNG"
    img.save()
    seam = TT.tile_seam_score(c.flatten(), TILE, TILE, c.palette)
    print(f"[tile] {name}: {len(c.palette) - 1} colours, seam {seam['score']} "
          f"({'seamless' if seam.get('seamless') else 'has a seam'})", flush=True)
    return img


def flagstone(c, L):
    """Irregular slabs, so the floor does not read as graph paper."""
    g = [c.add_colour(x) for x in TT.make_ramp((122, 118, 132, 255), 5)]
    A.fill(L, R.rect(0, 0, TILE - 1, TILE - 1, filled=True), g[0])
    slabs = ((0, 0, 29, 20), (31, 0, 63, 14), (0, 22, 17, 41), (19, 16, 45, 37),
             (47, 16, 63, 41), (0, 43, 27, 63), (29, 39, 63, 63))
    for n, (x0, y0, x1, y1) in enumerate(slabs):
        A.fill(L, R.rect(x0 + 1, y0 + 1, x1 - 1, y1 - 1, filled=True),
               g[2] if n % 3 else g[3])
        A.fill(L, R.line(x0 + 1, y0 + 1, x1 - 1, y0 + 1), g[4])
        A.fill(L, R.line(x0 + 1, y1 - 1, x1 - 1, y1 - 1), g[1])
    for sx, sy in ((7, 9), (38, 5), (52, 30), (11, 52), (40, 49), (24, 27)):
        A.fill(L, R.ellipse_box(sx, sy, sx + 3, sy + 1, filled=True), g[1])


def blockwall(c, L):
    s = [c.add_colour(x) for x in TT.make_ramp((186, 158, 118, 255), 5)]
    BW, BH = 16, 8
    A.fill(L, R.rect(0, 0, TILE - 1, TILE - 1, filled=True), s[0])
    for row, wy in enumerate(range(0, TILE, BH)):
        off = (row % 2) * (BW // 2)
        for n, bx in enumerate(range(-BW, TILE + BW, BW)):
            x0 = bx + off
            A.fill(L, R.rect(x0 + 1, wy + 1, x0 + BW - 1, wy + BH - 1,
                             filled=True), s[3] if (row * 5 + n * 3) % 4 else s[2])
            A.fill(L, R.line(x0 + 1, wy + 1, x0 + BW - 1, wy + 1), s[4])
            A.fill(L, R.line(x0 + 1, wy + BH - 1, x0 + BW - 1, wy + BH - 1), s[1])
    for bx, by in ((6, 4), (29, 12), (46, 21), (14, 29), (53, 37), (23, 45),
                   (39, 53), (10, 60)):
        A.fill(L, R.ellipse_box(bx, by, bx + 2, by + 1, filled=True), s[1])


def pillarstone(c, L):
    d = [c.add_colour(x) for x in TT.make_ramp((96, 84, 104, 255), 5)]
    A.fill(L, R.rect(0, 0, TILE - 1, TILE - 1, filled=True), d[1])
    for wy in range(0, TILE, 11):
        A.fill(L, R.line(0, wy, TILE - 1, wy), d[0])
        A.fill(L, R.line(0, wy + 1, TILE - 1, wy + 1), d[3])
        A.fill(L, R.rect(0, wy + 2, TILE - 1, wy + 9, filled=True), d[2])
        A.fill(L, R.line(0, wy + 9, TILE - 1, wy + 9), d[1])
    for k in range(0, TILE, 8):                    # a carved vertical channel
        A.fill(L, R.rect(28, k, 35, k + 5, filled=True), d[1])
        A.fill(L, R.line(28, k, 28, k + 5), d[0])
        A.fill(L, R.line(35, k, 35, k + 5), d[3])


# ------------------------------------------------------------- the walk sprite
def build_walk():
    """Draw the full four-track scene, then export the character ALONE.

    Hiding two tracks is the whole trick - the same document that made the
    cave GIF hands over a transparent sprite sheet for the 3D scene.
    """
    bpy.ops.texel.canvas_new(size=A.SIZE, name="Walk")
    img = bpy.data.images["Walk"]
    # the frame/track operators poll for an image editor, so give them one
    area = bpy.context.screen.areas[0]
    area.type = "IMAGE_EDITOR"
    area.spaces.active.image = img
    region = next(r for r in area.regions if r.type == "WINDOW")
    ctx = dict(area=area, region=region, space_data=area.spaces.active,
               screen=bpy.context.screen, window=bpy.context.window)
    doc = tex_doc.get(img)
    c = doc.canvas
    P = A.palette(c)
    with bpy.context.temp_override(**ctx):
      for _ in range(8):
          bpy.ops.texel.frame_add(copy_previous=False)
      bpy.ops.texel.track_add(name="Cave", bottom=True)
      bpy.ops.texel.track_add(name="Torch")
      bpy.ops.texel.track_add(name="Glow")
      for _ in range(2):
          bpy.ops.texel.track_move(name="Glow", delta=-1)
    for f in range(8):
        cels = {t: c.cel(t, f) for t in A.TRACKS}
        for t in A.TRACKS:
            A.DRAW[t](cels, P, f)

    paths = []
    for f in range(8):
        c.show_frame(f, onion=False)
        for t in ("Cave", "Glow"):                 # scenery off, character only
            c.cel(t, f).visible = False
        doc.flush()
        p = os.path.join(SPR, f"walk_{f:02d}.png")
        img.filepath_raw, img.file_format = p, "PNG"
        img.save()
        paths.append(p)
    print(f"[sprite] 8 frames, Cave and Glow hidden -> {SPR}", flush=True)
    return paths


# -------------------------------------------------------------------- geometry
def tiled_material(name, image):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = image
    tex.interpolation = "Closest"                  # never blur a texel
    tex.extension = "REPEAT"
    bsdf = nt.nodes["Principled BSDF"]
    bsdf.inputs["Roughness"].default_value = 0.86
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    return mat


def box(name, loc, size, mat):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.view_layer.objects.active
    o.name = name
    o.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bpy.ops.object.shade_flat()
    o.data.materials.append(mat)
    return o


def apply_density(objs, density):
    """One density across every surface. Without this the floor's big faces get
    a stretched tile and the pillars get a fine one - the exact defect Texel
    exists to catch."""
    bpy.context.scene.texel.target_density = density
    for o in objs:
        bpy.ops.object.select_all(action="DESELECT")
        o.select_set(True)
        bpy.context.view_layer.objects.active = o
        bpy.ops.texel.density_apply()
    print(f"[uv] {len(objs)} objects at {density} px/unit: "
          f"{bpy.context.scene.texel.status}", flush=True)


def build_scene(floor_img, wall_img, pillar_img, sprite_paths):
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)

    m_floor = tiled_material("Floor", floor_img)
    m_wall = tiled_material("Wall", wall_img)
    m_pill = tiled_material("Pillar", pillar_img)

    solid = []
    solid.append(box("Ground", (4, 0, -0.25), (26, 9, 0.5), m_floor))
    solid.append(box("BackWall", (4, 3.4, 1.9), (26, 0.6, 4.4), m_wall))
    # a stepped plinth running along the base of the wall, for silhouette
    solid.append(box("Plinth", (4, 2.7, 0.22), (26, 0.9, 0.45), m_pill))
    for i, x in enumerate((-5.5, -0.5, 4.5, 9.5, 14.5)):
        solid.append(box(f"Pillar{i}", (x, 2.5, 1.7), (0.85, 0.85, 3.4), m_pill))
        solid.append(box(f"Cap{i}", (x, 2.5, 3.55), (1.15, 1.15, 0.3), m_wall))
    # foreground blocks, close to camera, to give the frame depth
    for i, (x, y, z, s) in enumerate(((-2.2, -2.6, 0.45, 0.9),
                                      (6.4, -2.9, 0.35, 0.7),
                                      (11.8, -2.4, 0.55, 1.1))):
        solid.append(box(f"Block{i}", (x, y, z), (s, s, z * 2), m_wall))
    apply_density(solid, 28.0)

    # ---- the character, on a card that always faces the camera's axis
    imgs = []
    for p in sprite_paths:
        im = bpy.data.images.load(p, check_existing=False)
        im.alpha_mode = "STRAIGHT"
        imgs.append(im)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 1.7))
    card = bpy.context.view_layer.objects.active
    card.name = "Walker"
    card.scale = (3.4, 3.4, 1)
    card.rotation_euler = (math.radians(90), 0, 0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    mat = bpy.data.materials.new("Walker")
    mat.use_nodes = True
    nt = mat.node_tree
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = imgs[0]
    tex.interpolation = "Closest"
    tex.extension = "CLIP"
    bsdf = nt.nodes["Principled BSDF"]
    bsdf.inputs["Roughness"].default_value = 1.0
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(tex.outputs["Alpha"], bsdf.inputs["Alpha"])
    # a touch of self-emission so he is not a silhouette when the torch swings
    emis = nt.nodes.new("ShaderNodeEmission")
    emis.inputs["Strength"].default_value = 0.55
    nt.links.new(tex.outputs["Color"], emis.inputs["Color"])
    mix = nt.nodes.new("ShaderNodeAddShader")
    out = nt.nodes["Material Output"]
    nt.links.new(bsdf.outputs["BSDF"], mix.inputs[0])
    nt.links.new(emis.outputs["Emission"], mix.inputs[1])
    nt.links.new(mix.outputs["Shader"], out.inputs["Surface"])
    card.data.materials.append(mat)

    # ---- the torch itself, as a real light
    torch = bpy.data.lights.new("Torch", type="POINT")
    torch.color = (1.0, 0.62, 0.26)
    torch.shadow_soft_size = 0.35
    torch_o = bpy.data.objects.new("Torch", torch)
    bpy.context.collection.objects.link(torch_o)

    # ---- a cold fill from the far end of the corridor, so it is not one note
    key = bpy.data.lights.new("Far", type="AREA")
    key.color = (0.42, 0.58, 0.95)
    key.energy = 260
    key.size = 6
    key_o = bpy.data.objects.new("Far", key)
    key_o.location = (20, 1.0, 3.0)
    key_o.rotation_euler = (math.radians(74), 0, math.radians(-96))
    bpy.context.collection.objects.link(key_o)

    # ---- bounded fog. A world volume attenuates the lights across infinity.
    bpy.ops.mesh.primitive_cube_add(size=1, location=(4, 0.5, 2.2))
    haze = bpy.context.view_layer.objects.active
    haze.name = "Haze"
    haze.scale = (28, 10, 6)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    hm = bpy.data.materials.new("Haze")
    hm.use_nodes = True
    hnt = hm.node_tree
    for n in list(hnt.nodes):
        if n.type != "OUTPUT_MATERIAL":
            hnt.nodes.remove(n)
    sc_n = hnt.nodes.new("ShaderNodeVolumeScatter")
    sc_n.inputs["Density"].default_value = 0.012
    sc_n.inputs["Anisotropy"].default_value = 0.35
    hnt.links.new(sc_n.outputs["Volume"],
                  hnt.nodes["Material Output"].inputs["Volume"])
    haze.data.materials.append(hm)
    haze.visible_shadow = False

    cam_d = bpy.data.cameras.new("Cam")
    cam_d.lens = 46
    cam_d.dof.use_dof = True
    cam_d.dof.aperture_fstop = 2.6
    cam = bpy.data.objects.new("Cam", cam_d)
    bpy.context.collection.objects.link(cam)
    bpy.context.scene.camera = cam
    tgt = bpy.data.objects.new("Focus", None)
    bpy.context.collection.objects.link(tgt)
    con = cam.constraints.new("TRACK_TO")
    con.target = tgt
    con.track_axis, con.up_axis = "TRACK_NEGATIVE_Z", "UP_Y"
    cam_d.dof.focus_object = tgt

    world = bpy.data.worlds.new("W")
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (0.03, 0.035,
                                                                   0.06, 1)
    world.node_tree.nodes["Background"].inputs[1].default_value = 0.35
    bpy.context.scene.world = world

    return dict(card=card, tex=tex, imgs=imgs, torch=torch_o, cam=cam, tgt=tgt)


def main():
    t0 = time.perf_counter()
    floor = paint("Flagstone", flagstone)
    wall = paint("Blockwall", blockwall)
    pillar = paint("Pillarstone", pillarstone)
    sprite_paths = build_walk()
    S = build_scene(floor, wall, pillar, sprite_paths)

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
    sc.render.resolution_x, sc.render.resolution_y = RES
    sc.render.image_settings.file_format = "PNG"
    sc.view_settings.look = "AgX - Base Contrast"

    speed = STRIDE / (8 * HOLD)         # units per render frame, no foot slide
    x0 = -4.5
    for i in range(NFRAMES):
        t = i / max(1, NFRAMES - 1)
        f = (i // HOLD) % 8
        p = A.pose(f)

        S["tex"].image = S["imgs"][f]
        x = x0 + speed * i
        S["card"].location = (x, 0.0, 1.70 + (0.02 if p["bob"] else 0.0))

        # the torch, in world units, from where the flame sits on the sprite
        tx = x + (p["tx"] - A.SIZE / 2) * (3.4 / A.SIZE)
        tz = 1.70 + (A.SIZE / 2 - p["ty"]) * (3.4 / A.SIZE)
        S["torch"].location = (tx, -0.12, tz)
        S["torch"].data.energy = 190 + 55 * p["lick"]

        # camera: trails him, then closes in and drops slightly
        S["cam"].location = (x - 3.6 + 1.9 * t, -5.4 + 1.5 * t, 2.9 - 0.8 * t)
        S["tgt"].location = (x + 0.5, 0.4, 1.55)

        sc.render.filepath = os.path.join(FR, f"f_{i:04d}")
        bpy.ops.render.render(write_still=True)
        if i and i % 24 == 0:
            el = time.perf_counter() - t0
            print(f"  walk {i}/{NFRAMES}  {el:.0f}s  "
                  f"eta {el / i * (NFRAMES - i):.0f}s", flush=True)

    dst = os.path.join(HERE, "promo", "texel-walkthrough.mp4")
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate",
                        str(FPS), "-i", os.path.join(FR, "f_%04d.png"),
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17",
                        dst], capture_output=True, text=True)
    ok = r.returncode == 0 and os.path.exists(dst)
    print(f"TEXEL_WALK_DONE frames={NFRAMES} mp4={'ok' if ok else 'FAIL'} "
          f"bytes={os.path.getsize(dst) if ok else 0} "
          f"secs={NFRAMES / FPS:.1f} total={time.perf_counter() - t0:.0f}s",
          flush=True)


if __name__ == "__main__":
    main()
