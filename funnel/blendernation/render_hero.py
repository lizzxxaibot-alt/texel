"""BlenderNation lead image: 1456x672, clean, no text and no logo.

  blender -b --factory-startup --python funnel/blendernation/render_hero.py -- <texel_dir>

WHY A NEW RENDER AND NOT AN EXISTING ASSET. BlenderNation's submission form asks
for 1456x672 (2.167:1) and says plainly: "we prefer 'clean' images without any
text or logo overlays on them."

  * Every card in promo/ is a designed graphic with type on it. All disqualified.
  * store/stills/ holds 57 clean 1280x720 Cycles renders - right kind of asset,
    wrong ratio. And on opening env_corridor_02.png it reads as smooth low-poly
    shading with almost no visible pixel texture, which for a product whose whole
    pitch is texels on a lit 3D surface is the weakest possible lead image.

ROUND 1 OF THIS SCRIPT FAILED, and the reason is recorded so it is not repeated.
It framed 4.6 m across at 32 px/unit with an ORTHO camera. Looked at, it was a
close-up of two boxes: the tiles were stretched so far that the wall read as
large flat rectangles - low-poly blocks, not pixel texture - and the flagstone
floor blew out to near-white. Too few texels, each too big, is just as wrong as
the corridor still's too-many-too-small.

So round 2: a wider frame (7.2 m) at a finer density (48 px/unit), a PERSPECTIVE
camera so the space has depth like a game screenshot rather than a product shot,
a warm practical light against a cool ambient, and AgX rather than Standard so
the highlights roll off instead of clipping.

THE GATE IS ON THE RENDERED PNG, NOT ON THE ARITHMETIC. Screen-pixels-per-texel
is easy to compute and proves nothing about the shipped image - under a
perspective camera it is different at every depth anyway. What actually
distinguishes pixel art from smooth shading is FLATNESS: a texel several screen
pixels wide produces runs of exactly-equal neighbouring pixels, and a smooth
gradient does not. So after rendering we measure the fraction of horizontally
adjacent pixel pairs that are exactly equal, and compare it against
store/stills/env_corridor_02.png as a control - the very image this render
exists to beat. Failing that comparison fails the build.

ROUNDS 4 AND 5 (2026-09-25) FAILED TOO: 0.241 and 0.210 against a pass line of
0.263. That uses up the 5-round cap. This file holds the round 5 scene; round 4
rendered better and is kept as hero_round4.png. The design-critic findings, and
its doubt about whether this gate can be passed at all on a lit render, are in
SUBMISSION.md. Read them before running a round 6.
"""
import math
import os
import struct
import sys
import zlib

import bpy

ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
TEXEL = os.path.abspath(ARGS[0]) if ARGS else os.getcwd()
SHOTS = os.path.join(TEXEL, "promo", "shots", "dungeon")
OUT = os.path.join(TEXEL, "funnel", "blendernation", "hero_1456x672.png")
CONTROL = os.path.join(TEXEL, "store", "stills", "env_corridor_02.png")

RES_X, RES_Y = 1456, 672
PX_PER_UNIT = 32.0     # texel density every surface in the scene is built at
                       # (round 4: coarser than round 3's 48, so a texel is
                       # several screen pixels across the near half of frame)
TILE_PX = 64           # the dungeon source tiles are 64x64


def clear():
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)


def pixel_mat(name, tile_png, tile_px=TILE_PX, emit=0.0):
    """Closest-interpolation material, BOX-projected in object space.

    Round 2 passed one uniform UV scale per object and the floor (9 x 14 m) came
    back with tiles stretched 1.55x in V, because a default cube's UVs run 0..1
    across each face regardless of that face's real size. Box projection from
    OBJECT coordinates makes the repeat a function of metres, so every surface in
    the scene lands at exactly PX_PER_UNIT whatever its dimensions - which is
    also, not incidentally, the thing the product is for.
    """
    img = bpy.data.images.load(tile_png)
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    tex.interpolation = "Closest"          # never Linear; this is the product
    tex.projection = "BOX"
    tex.projection_blend = 0.0             # hard seam, not a blend - pixel art
    tex.extension = "REPEAT"
    tex.location = (-500, 200)
    mapping = nt.nodes.new("ShaderNodeMapping")
    mapping.location = (-700, 200)
    rep = PX_PER_UNIT / tile_px            # tile repeats per metre
    mapping.inputs["Scale"].default_value = (rep, rep, rep)
    coord = nt.nodes.new("ShaderNodeTexCoord")
    coord.location = (-900, 200)
    nt.links.new(coord.outputs["Object"], mapping.inputs["Vector"])
    nt.links.new(mapping.outputs["Vector"], tex.inputs["Vector"])
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.95
    bsdf.inputs["Specular IOR Level"].default_value = 0.12
    if emit:
        nt.links.new(tex.outputs["Color"], bsdf.inputs["Emission Color"])
        bsdf.inputs["Emission Strength"].default_value = emit
    return mat


def box(name, size, loc, rot_z=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = size
    ob.rotation_euler = (0, 0, math.radians(rot_z))
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return ob




clear()

# ---------------------------------------------------------------- the space
# A corridor running away from camera: floor, two side walls, a back wall. The
# depth is what stops this reading as a product shot on a backdrop.
floor = box("Floor", (3.6, 10.0, 0.2), (0, 3.0, -0.1))
wall_l = box("WallL", (0.25, 10.0, 3.0), (-1.8, 3.0, 1.5))
wall_r = box("WallR", (0.25, 10.0, 3.0), (1.8, 3.0, 1.5))
wall_b = box("WallB", (3.6, 0.25, 3.0), (0, 6.2, 1.5))
ceiling = box("Ceil", (3.6, 10.0, 0.2), (0, 3.0, 3.1))

crate_a = box("CrateA", (0.80, 0.80, 0.80), (-1.05, 1.55, 0.40), rot_z=14)
crate_b = box("CrateB", (0.56, 0.56, 0.56), (-0.40, 2.05, 0.28), rot_z=-27)
crate_c = box("CrateC", (0.62, 0.62, 0.62), (1.10, 3.90, 0.31), rot_z=33)
crate_d = box("CrateD", (0.52, 0.52, 0.52), (-1.10, 1.62, 1.06), rot_z=-8)
column = box("Column", (0.36, 0.36, 3.0), (1.40, 5.20, 1.5))

flag = pixel_mat("Flagstone", os.path.join(SHOTS, "tile_flagstone.png"))
brick = pixel_mat("Blockwall", os.path.join(SHOTS, "tile_blockwall.png"))
brick_b = pixel_mat("BlockwallB", os.path.join(SHOTS, "tile_blockwall.png"))
fluted = pixel_mat("Fluted", os.path.join(SHOTS, "tile_fluted.png"))

floor.data.materials.append(flag)
ceiling.data.materials.append(brick)
wall_l.data.materials.append(brick)
wall_r.data.materials.append(brick)
wall_b.data.materials.append(brick_b)
column.data.materials.append(fluted)
for ob in (crate_a, crate_b, crate_c, crate_d):
    ob.data.materials.append(
        pixel_mat(ob.name + "Mat",
                  os.path.join(TEXEL, "store", "tile_blockwall_32.png"), 32))

# A banner on the left wall, lifted straight from the dungeon tile set, to give
# the eye one saturated accent against all the stone.
banner = box("Banner", (0.06, 0.75, 1.4), (-1.64, 3.9, 1.85))
banner.data.materials.append(
    pixel_mat("Banner", os.path.join(SHOTS, "tile_banner.png")))

# ---------------------------------------------------------------- lighting
# A warm practical up ahead (the thing a torch would be) and a cool low ambient,
# so the corridor has a direction to walk toward.
torch = bpy.data.lights.new("Torch", "POINT")
torch.energy, torch.shadow_soft_size = 330.0, 0.15
torch.color = (1.0, 0.66, 0.36)
to = bpy.data.objects.new("Torch", torch)
to.location = (0.2, 4.4, 2.2)
bpy.context.collection.objects.link(to)

near = bpy.data.lights.new("Near", "AREA")
near.energy, near.size = 16.0, 1.6
near.color = (1.0, 0.82, 0.62)
no = bpy.data.objects.new("Near", near)
no.location = (-1.2, -0.6, 2.7)
no.rotation_euler = (math.radians(48), 0, math.radians(-24))
bpy.context.collection.objects.link(no)

cool = bpy.data.lights.new("Cool", "AREA")
cool.energy, cool.size = 140.0, 4.0
cool.color = (0.40, 0.55, 1.0)
co = bpy.data.objects.new("Cool", cool)
co.location = (1.6, -2.4, 1.6)
co.rotation_euler = (math.radians(80), 0, math.radians(30))
bpy.context.collection.objects.link(co)

world = bpy.data.worlds.new("W")
world.use_nodes = True
bg = next(n for n in world.node_tree.nodes if n.type == "BACKGROUND")
bg.inputs["Color"].default_value = (0.012, 0.015, 0.024, 1.0)
bg.inputs["Strength"].default_value = 1.0
bpy.context.scene.world = world

# ---------------------------------------------------------------- camera
# PERSPECTIVE, not ortho. Round 1's ortho camera is part of why the frame read
# as a flat product shot; a game screenshot has convergence in it.
cam_d = bpy.data.cameras.new("Cam")
cam_d.type = "PERSP"
cam_d.lens = 28.0
cam = bpy.data.objects.new("Cam", cam_d)
cam.location = (0.70, -1.70, 1.05)
bpy.context.collection.objects.link(cam)
bpy.context.scene.camera = cam

target = bpy.data.objects.new("Target", None)
target.location = (-0.40, 3.4, 1.10)
bpy.context.collection.objects.link(target)
con = cam.constraints.new("TRACK_TO")
con.target = target
con.track_axis = "TRACK_NEGATIVE_Z"
con.up_axis = "UP_Y"

# ---------------------------------------------------------------- render
sc = bpy.context.scene
sc.render.engine = "CYCLES"
sc.cycles.samples = 220
sc.cycles.use_denoising = True
# Round 4: a narrower pixel filter keeps texel edges crisp instead of
# spreading each one across a 1.5 px Gaussian.
sc.cycles.filter_width = 0.50
sc.render.resolution_x, sc.render.resolution_y = RES_X, RES_Y
sc.render.resolution_percentage = 100
sc.render.film_transparent = False
sc.render.image_settings.file_format = "PNG"
sc.render.image_settings.color_mode = "RGB"
sc.render.filepath = OUT
# AgX with base contrast: Standard clipped the warm practical to white in round
# 1 and took the floor's tile detail with it.
sc.view_settings.view_transform = "AgX"
sc.view_settings.look = "AgX - Medium High Contrast"

try:
    sc.cycles.device = "GPU"
    prefs = bpy.context.preferences.addons["cycles"].preferences
    prefs.get_devices()
    for dev in prefs.devices:
        dev.use = dev.type != "CPU"
except Exception as exc:
    print("hero: GPU unavailable (%s), CPU" % exc)

bpy.ops.render.render(write_still=True)
print("hero: wrote", OUT)


# ------------------------------------------------- the gate, on the real pixels
def flatness(path):
    """Fraction of horizontally adjacent pixel pairs that are EXACTLY equal.

    Decoded with zlib + the PNG spec rather than Pillow, because this runs
    inside Blender's Python and Pillow is not guaranteed there.
    """
    raw = open(path, "rb").read()
    assert raw[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG: " + path
    pos, idat, w = 8, b"", None
    while pos < len(raw):
        ln = struct.unpack(">I", raw[pos:pos + 4])[0]
        typ = raw[pos + 4:pos + 8]
        data = raw[pos + 8:pos + 8 + ln]
        if typ == b"IHDR":
            w, h, depth, ctype = (*struct.unpack(">II", data[:8]), data[8], data[9])
            assert depth == 8 and ctype in (2, 6), f"unexpected PNG {depth}/{ctype}"
            nch = 3 if ctype == 2 else 4
        elif typ == b"IDAT":
            idat += data
        elif typ == b"IEND":
            break
        pos += 12 + ln
    buf = zlib.decompress(idat)
    stride = w * nch
    prev = bytearray(stride)
    same = total = 0
    off = 0
    for _y in range(h):
        ft = buf[off]; off += 1
        line = bytearray(buf[off:off + stride]); off += stride
        # undo the PNG row filter
        for i in range(stride):
            a = line[i - nch] if i >= nch else 0
            b = prev[i]
            c = prev[i - nch] if i >= nch else 0
            if ft == 1:   line[i] = (line[i] + a) & 255
            elif ft == 2: line[i] = (line[i] + b) & 255
            elif ft == 3: line[i] = (line[i] + (a + b) // 2) & 255
            elif ft == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[i] = (line[i] + pr) & 255
        for x in range(1, w):
            o0, o1 = (x - 1) * nch, x * nch
            total += 1
            if line[o0:o0 + 3] == line[o1:o1 + 3]:
                same += 1
        prev = line
    return same / total


hero_flat = flatness(OUT)
ctrl_flat = flatness(CONTROL) if os.path.exists(CONTROL) else None
print("hero: flatness %.3f  (control env_corridor_02 %s)"
      % (hero_flat, "%.3f" % ctrl_flat if ctrl_flat is not None else "missing"))
assert ctrl_flat is not None, "control still missing; the gate cannot decide"
assert hero_flat > ctrl_flat * 1.30, (
    "hero flatness %.3f is not meaningfully above the smooth-shaded control "
    "%.3f - the texels are not reading, which is the one thing this image has "
    "to do." % (hero_flat, ctrl_flat))
print("hero: GATE PASS")
