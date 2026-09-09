"""Five cinematic shots that look like the games Texel's buyers actually ship.

Each shot answers "why buy this" with a different capability, and every texture
in every shot is painted by Texel's own operators inside this file:

  dungeon   side-scroller corridor, the torchbearer walking
            -> ANIMATION. One document, four tracks; hide two and the same file
               that drew the scene hands over a transparent sprite sheet.
  temple    isometric ARPG chamber, one floor tile repeated across a big room
            -> SEAMLESS TILING, measured. The seam score is printed, not hoped.
  hangar    sci-fi bay, three identical wall textures in three palettes
            -> PALETTE SWAP. One texture, three moods, no repainting.
  market    top-down adventure exterior, huge ground and tiny props
            -> TEXEL DENSITY. Every surface at the same pixels-per-unit.
  shrine    symmetric facade, drawn as one half
            -> MIRROR SYMMETRY and sprite outlines.

  blender --background --factory-startup --python gameshots.py -- dungeon 144
"""
import math
import os
import subprocess
import sys
import time

import bmesh
import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["dungeon"]
NAME = argv[0]
NFRAMES = int(argv[1]) if len(argv) > 1 else 144
RES = (1280, 720)
SAMPLES = 48
FPS = 24

import texel
from texel import tex_doc
from texel.core import raster as R
from texel.core import tools as TT

texel.register()
import demo_art as A

TILE = 64
STRIDE = 1.15                   # world units one walk cycle covers
HOLD = 2                        # render frames per drawing -> 12fps of walk

OUT = os.path.join(HERE, "promo", "shots", NAME)
FR = os.path.join(OUT, "frames")
os.makedirs(FR, exist_ok=True)
for f in os.listdir(FR):
    os.remove(os.path.join(FR, f))

_seams = []


# ============================================================ Texel does the art
def canvas(name, size=TILE):
    bpy.ops.texel.canvas_new(size=size, name=name)
    img = bpy.data.images[name]
    return img, tex_doc.get(img)


def paint(name, fn, size=TILE, check=True):
    """Paint a tile with Texel, save it, and measure whether it actually tiles."""
    img, doc = canvas(name, size)
    c = doc.canvas
    fn(c, c.layers[0])
    doc.flush()
    img.filepath_raw = os.path.join(OUT, f"tile_{name.lower()}.png")
    img.file_format = "PNG"
    img.save()
    if check:
        s = TT.tile_seam_score(c.flatten(), size, size, c.palette)
        _seams.append((name, s["score"], bool(s.get("seamless"))))
        print(f"[tile] {name}: {len(c.palette) - 1} colours, seam {s['score']}"
              f" ({'seamless' if s.get('seamless') else 'HAS A SEAM'})", flush=True)
    return img, doc


def ramp(c, base, n=5):
    return [c.add_colour(x) for x in TT.make_ramp(base, n)]


def flagstone(c, L, base=(122, 118, 132, 255)):
    """Irregular slabs, so a floor does not read as graph paper."""
    g = ramp(c, base)
    A.fill(L, R.rect(0, 0, TILE - 1, TILE - 1, filled=True), g[0])
    for n, (x0, y0, x1, y1) in enumerate((
            (0, 0, 29, 20), (31, 0, 63, 14), (0, 22, 17, 41), (19, 16, 45, 37),
            (47, 16, 63, 41), (0, 43, 27, 63), (29, 39, 63, 63))):
        A.fill(L, R.rect(x0 + 1, y0 + 1, x1 - 1, y1 - 1, filled=True),
               g[2] if n % 3 else g[3])
        A.fill(L, R.line(x0 + 1, y0 + 1, x1 - 1, y0 + 1), g[4])
        A.fill(L, R.line(x0 + 1, y1 - 1, x1 - 1, y1 - 1), g[1])
    for sx, sy in ((7, 9), (38, 5), (52, 30), (11, 52), (40, 49), (24, 27)):
        A.fill(L, R.ellipse_box(sx, sy, sx + 3, sy + 1, filled=True), g[1])


def blocks(c, L, base=(186, 158, 118, 255), bw=16, bh=8):
    s = ramp(c, base)
    A.fill(L, R.rect(0, 0, TILE - 1, TILE - 1, filled=True), s[0])
    for row, wy in enumerate(range(0, TILE, bh)):
        off = (row % 2) * (bw // 2)
        for n, bx in enumerate(range(-bw, TILE + bw, bw)):
            x0 = bx + off
            # 2px joints, not 1: a single-texel mortar line disappears at
            # grazing angles and the wall reads as siding instead of masonry
            A.fill(L, R.rect(x0 + 2, wy + 2, x0 + bw - 1, wy + bh - 1,
                             filled=True), s[3] if (row * 5 + n * 3) % 4 else s[2])
            A.fill(L, R.line(x0 + 2, wy + 2, x0 + bw - 1, wy + 2), s[4])
            A.fill(L, R.line(x0 + 2, wy + bh - 1, x0 + bw - 1, wy + bh - 1), s[1])
    for bx, by in ((6, 4), (29, 12), (46, 21), (14, 29), (53, 37), (23, 45),
                   (39, 53), (10, 60)):
        A.fill(L, R.ellipse_box(bx, by, bx + 2, by + 1, filled=True), s[1])


def fluted(c, L, base=(96, 84, 104, 255)):
    d = ramp(c, base)
    A.fill(L, R.rect(0, 0, TILE - 1, TILE - 1, filled=True), d[1])
    for wy in range(0, TILE, 11):
        A.fill(L, R.line(0, wy, TILE - 1, wy), d[0])
        A.fill(L, R.line(0, wy + 1, TILE - 1, wy + 1), d[3])
        A.fill(L, R.rect(0, wy + 2, TILE - 1, wy + 9, filled=True), d[2])
        A.fill(L, R.line(0, wy + 9, TILE - 1, wy + 9), d[1])
    for k in range(0, TILE, 8):
        A.fill(L, R.rect(28, k, 35, k + 5, filled=True), d[1])
        A.fill(L, R.line(28, k, 28, k + 5), d[0])
        A.fill(L, R.line(35, k, 35, k + 5), d[3])


def panel(c, L):
    """Sci-fi plating: greebles, a vent, a warning stripe. Deliberately built
    from ONE hue ramp so a palette swap can restate the whole thing."""
    m = ramp(c, (104, 116, 138, 255))
    A.fill(L, R.rect(0, 0, TILE - 1, TILE - 1, filled=True), m[1])
    for gx in (0, 32):
        for gy in (0, 32):
            A.fill(L, R.rect(gx + 2, gy + 2, gx + 29, gy + 29, filled=True), m[2])
            A.fill(L, R.rect(gx + 2, gy + 2, gx + 29, gy + 29), m[0])
            A.fill(L, R.line(gx + 3, gy + 3, gx + 28, gy + 3), m[3])
            for rx, ry in ((6, 6), (25, 6), (6, 25), (25, 25)):
                L.set(gx + rx, gy + ry, m[4])
            A.fill(L, R.rect(gx + 9, gy + 12, gx + 22, gy + 19, filled=True), m[0])
            for vy in range(gy + 13, gy + 19, 2):     # vent slots
                A.fill(L, R.line(gx + 10, vy, gx + 21, vy), m[3])
    for sy in range(30, 34):                          # hazard stripe
        for sx in range(TILE):
            if (sx + sy) % 8 < 4:
                L.set(sx, sy, m[4])


def swap_palette(img, doc, degrees, sat):
    """Restate a whole texture through its palette. texel.adjust runs exactly
    this on a click; the pixels never move, only what each index means.

    The re-save matters: paint() has already written the PNG, and Cycles reads
    the file, so a swap that only touched the datablock rendered as the
    original and the whole point of the shot went missing.
    """
    from texel.core import adjust
    pal = adjust.apply_to_palette(doc.canvas.palette, "HUE", degrees)
    pal = adjust.apply_to_palette(pal, "SATURATION", sat)
    doc.canvas.palette[:] = pal
    doc.flush()
    img.save()


def mirrored(c, L, base=(178, 150, 104, 255)):
    """Drawn as ONE half. Every set() is echoed across the centre line, which
    is exactly what Mirror X does while you paint."""
    s = ramp(c, base)
    half = TILE // 2

    def m(pts, v):
        for x, y in pts:
            if x < half:
                L.set(x, y, v)
                L.set(TILE - 1 - x, y, v)

    A.fill(L, R.rect(0, 0, TILE - 1, TILE - 1, filled=True), s[1])
    m(R.rect(4, 6, 27, 57, filled=True), s[2])
    m(R.rect(4, 6, 27, 9, filled=True), s[3])
    m(R.ellipse_box(8, 14, 23, 44, filled=True), s[0])
    m(R.ellipse_box(10, 16, 21, 42, filled=True), s[3])
    m(R.line(16, 18, 16, 40), s[4])
    for k in range(20, 56, 8):
        m(R.rect(2, k, 5, k + 4, filled=True), s[4])
    m(R.rect(0, 58, 31, 63, filled=True), s[0])
    m(R.line(0, 58, 31, 58), s[4])


def cloth(c, L, base=(150, 52, 62, 255)):
    """A hanging banner, on transparent - the kind of prop that needs an
    outline to read against a busy wall."""
    s = ramp(c, base)
    A.fill(L, R.rect(18, 2, 45, 52, filled=True), s[2])
    A.fill(L, R.rect(18, 2, 45, 8, filled=True), s[3])
    A.fill(L, R.rect(24, 14, 39, 34, filled=True), s[4])
    A.fill(L, R.ellipse_box(26, 16, 37, 32, filled=True), s[1])
    for k, x in enumerate(range(18, 46, 9)):          # ragged hem
        A.fill(L, R.ellipse_box(x, 48, x + 8, 58, filled=True), s[2])
    A.fill(L, TT.outline_points(L), c.add_colour((22, 18, 26, 255)))


def build_walk():
    """The 8-frame cycle, exported with the scenery tracks hidden."""
    bpy.ops.texel.canvas_new(size=A.SIZE, name="Walk")
    img = bpy.data.images["Walk"]
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

    spr = os.path.join(OUT, "sprite")
    os.makedirs(spr, exist_ok=True)
    out = []
    for f in range(8):
        c.show_frame(f, onion=False)
        for t in ("Cave", "Glow"):
            c.cel(t, f).visible = False
        doc.flush()
        p = os.path.join(spr, f"walk_{f:02d}.png")
        img.filepath_raw, img.file_format = p, "PNG"
        img.save()
        im = bpy.data.images.load(p, check_existing=False)
        im.alpha_mode = "STRAIGHT"
        out.append(im)
    print(f"[sprite] 8 frames x 4 tracks; Cave and Glow hidden for export",
          flush=True)
    return out


# ==================================================================== 3D helpers
def mat_of(name, image, rough=0.86, emit=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = image
    tex.interpolation = "Closest"                  # never blur a texel
    tex.extension = "REPEAT"
    b = nt.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = rough
    nt.links.new(tex.outputs["Color"], b.inputs["Base Color"])
    if emit:
        b.inputs["Emission Color"].default_value = (1, 1, 1, 1)
        nt.links.new(tex.outputs["Color"], b.inputs["Emission Color"])
        b.inputs["Emission Strength"].default_value = emit
    return mat


def box(name, loc, size, mat, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.view_layer.objects.active
    o.name = name
    o.scale = size
    o.rotation_euler = rot
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bpy.ops.object.shade_flat()
    o.data.materials.append(mat)
    return o


def card(name, loc, size, image, rot=(math.radians(90), 0, 0), unlit=True):
    """A sprite on a plane.

    Unlit by default, and that is deliberate: a lamp sitting next to the card
    blows a torch flame past 1.0 long before the view transform sees it, and
    the sprite stops looking like the pixel art you painted. Emission plus a
    transparent BSDF renders the cel exactly as drawn, which is what a 2D
    sprite in a 3D scene is supposed to do.
    """
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc)
    o = bpy.context.view_layer.objects.active
    o.name = name
    o.scale = (size[0], size[1], 1)
    o.rotation_euler = rot
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    out = nt.nodes["Material Output"]
    for n in list(nt.nodes):
        if n.type != "OUTPUT_MATERIAL":
            nt.nodes.remove(n)
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = image
    tex.interpolation = "Closest"
    tex.extension = "CLIP"
    if unlit:
        emis = nt.nodes.new("ShaderNodeEmission")
        emis.inputs["Strength"].default_value = 1.0
        clear = nt.nodes.new("ShaderNodeBsdfTransparent")
        mix = nt.nodes.new("ShaderNodeMixShader")
        nt.links.new(tex.outputs["Color"], emis.inputs["Color"])
        nt.links.new(tex.outputs["Alpha"], mix.inputs["Fac"])
        nt.links.new(clear.outputs["BSDF"], mix.inputs[1])
        nt.links.new(emis.outputs["Emission"], mix.inputs[2])
        nt.links.new(mix.outputs["Shader"], out.inputs["Surface"])
    else:
        b = nt.nodes.new("ShaderNodeBsdfPrincipled")
        b.inputs["Roughness"].default_value = 1.0
        nt.links.new(tex.outputs["Color"], b.inputs["Base Color"])
        nt.links.new(tex.outputs["Alpha"], b.inputs["Alpha"])
        nt.links.new(b.outputs["BSDF"], out.inputs["Surface"])
    o.data.materials.append(mat)
    o.visible_shadow = False           # a flat card casts a flat wrong shadow
    return o, tex


def orient_walls(obj):
    """Blender's default cube unwrap lays the side faces on their side, so a
    16x8 brick renders as an 8x16 plank and a stone wall reads as fencing.
    Rotate the UVs a quarter turn on every face that is not floor or ceiling."""
    me = obj.data
    bm = bmesh.new()
    bm.from_mesh(me)
    uvl = bm.loops.layers.uv.active
    if uvl is None:
        bm.free()
        return
    for f in bm.faces:
        if abs(f.normal.z) > 0.5:
            continue                       # floors and ceilings are already flat
        n = len(f.loops)
        cx = sum(l[uvl].uv[0] for l in f.loops) / n
        cy = sum(l[uvl].uv[1] for l in f.loops) / n
        for l in f.loops:
            u, v = l[uvl].uv
            l[uvl].uv = (cx + (v - cy), cy - (u - cx))
    bm.to_mesh(me)
    bm.free()
    me.update()


def density(objs, px):
    """One texel density across every surface. Skip it and a big floor face
    gets a stretched tile while a crate gets a fine one - the exact defect."""
    bpy.context.scene.texel.target_density = px
    for o in objs:
        orient_walls(o)
        bpy.ops.object.select_all(action="DESELECT")
        o.select_set(True)
        bpy.context.view_layer.objects.active = o
        bpy.ops.texel.density_apply()
    print(f"[uv] {len(objs)} objects at {px} px/unit", flush=True)


def light(name, kind, loc, colour, energy, rot=(0, 0, 0), size=4.0):
    d = bpy.data.lights.new(name, type=kind)
    d.color = colour
    d.energy = energy
    if kind == "AREA":
        d.size = size
    elif kind == "POINT":
        d.shadow_soft_size = 0.35
    elif kind == "SUN":
        d.angle = math.radians(2.5)
    o = bpy.data.objects.new(name, d)
    o.location = loc
    o.rotation_euler = rot
    o.visible_camera = False            # or the lamp renders as a white slab
    bpy.context.collection.objects.link(o)
    return o


def haze(loc, size, dens=0.012, aniso=0.35):
    """Bounded fog. A world volume attenuates every light across infinity and
    the scene renders near-black - measured once, never repeated."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.view_layer.objects.active
    o.name = "Haze"
    o.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    m = bpy.data.materials.new("Haze")
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        if n.type != "OUTPUT_MATERIAL":
            nt.nodes.remove(n)
    v = nt.nodes.new("ShaderNodeVolumeScatter")
    v.inputs["Density"].default_value = dens
    v.inputs["Anisotropy"].default_value = aniso
    nt.links.new(v.outputs["Volume"], nt.nodes["Material Output"].inputs["Volume"])
    o.data.materials.append(m)
    o.visible_shadow = False
    return o


def rig(lens=46, fstop=2.6):
    cd = bpy.data.cameras.new("Cam")
    cd.lens = lens
    cd.dof.use_dof = True
    cd.dof.aperture_fstop = fstop
    cam = bpy.data.objects.new("Cam", cd)
    bpy.context.collection.objects.link(cam)
    bpy.context.scene.camera = cam
    tgt = bpy.data.objects.new("Focus", None)
    bpy.context.collection.objects.link(tgt)
    con = cam.constraints.new("TRACK_TO")
    con.target = tgt
    con.track_axis, con.up_axis = "TRACK_NEGATIVE_Z", "UP_Y"
    cd.dof.focus_object = tgt
    return cam, tgt


def world(colour, strength):
    w = bpy.data.worlds.new("W")
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = colour
    w.node_tree.nodes["Background"].inputs[1].default_value = strength
    bpy.context.scene.world = w


def clear():
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)


# ======================================================================== shots
def shot_dungeon():
    """Side-scroller. The character is a SPRITE walking through the tiles -
    he is not wrapped around a crate."""
    floor, _ = paint("Flagstone", flagstone)
    wall, _ = paint("Blockwall", blocks)
    pill, _ = paint("Fluted", fluted)
    walk = build_walk()
    clear()

    m_f, m_w, m_p = (mat_of("F", floor), mat_of("W", wall), mat_of("P", pill))
    solid = [box("Ground", (4, 0, -0.25), (26, 9, 0.5), m_f),
             box("Back", (4, 3.4, 1.9), (26, 0.6, 4.4), m_w),
             box("Plinth", (4, 2.7, 0.22), (26, 0.9, 0.45), m_p)]
    for i, x in enumerate((-6.0, 2.0, 10.0)):
        solid.append(box(f"Pillar{i}", (x, 2.4, 1.7), (1.1, 1.1, 3.4), m_p))
        solid.append(box(f"Cap{i}", (x, 2.4, 3.6), (1.5, 1.5, 0.4), m_w))
        solid.append(box(f"Sconce{i}", (x, 1.85, 2.5), (0.34, 0.34, 0.44), m_p))
    # an archway the camera passes through, so the wall is not one long slab
    solid.append(box("ArchL", (4.0, 3.4, 1.6), (1.6, 0.7, 3.2), m_p))
    solid.append(box("ArchR", (7.6, 3.4, 1.6), (1.6, 0.7, 3.2), m_p))
    solid.append(box("ArchTop", (5.8, 3.4, 3.5), (5.2, 0.9, 0.6), m_w))
    solid.append(box("Room", (5.8, 6.2, 1.9), (5.0, 5.0, 3.8), m_w))
    solid.append(box("RoomFloor", (5.8, 6.2, 0.05), (5.0, 5.0, 0.4), m_f))
    for i, (x, y, r, h) in enumerate(((-9.4, 1.9, 0.42, 1.0),
                                      (-8.7, 2.3, 0.38, 0.86),
                                      (14.6, 2.0, 0.45, 1.1))):
        solid.append(box(f"Barrel{i}", (x, y, h / 2), (r * 2, r * 2, h), m_p))
    for i, (x, y, sz) in enumerate(((-8.4, -3.2, 0.9), (3.2, -3.4, 0.7),
                                    (13.6, -3.0, 1.1))):
        solid.append(box(f"Fore{i}", (x, y, sz / 2), (sz, sz, sz), m_w))
    density(solid, 30.0)

    banner, _ = paint("Banner", cloth, check=False)
    for i, x in enumerate((-6.0, 10.0)):              # outlined banner props
        card(f"Banner{i}", (x, 1.82, 2.0), (1.5, 2.6), banner)
    walker, tex = card("Walker", (0, 0, 1.7), (3.4, 3.4), walk[0])
    torch = light("Torch", "POINT", (0, 0, 2), (1.0, 0.62, 0.26), 105)
    for i, x in enumerate((-6.0, 2.0, 10.0)):         # the sconces are lit
        light(f"Wall{i}", "POINT", (x, 1.2, 2.55), (1.0, 0.66, 0.34), 26)
    light("Room", "POINT", (5.8, 5.4, 2.4), (1.0, 0.7, 0.4), 260)  # through the arch
    light("Far", "AREA", (20, 1.0, 3.2), (0.42, 0.58, 0.95), 420,
          (math.radians(74), 0, math.radians(-96)), size=6)
    haze((4, 0.5, 2.2), (28, 10, 6))
    world((0.03, 0.035, 0.06, 1), 0.35)
    cam, tgt = rig(46, 2.6)

    def move(i, t):
        f = (i // HOLD) % 8
        p = A.pose(f)
        tex.image = walk[f]
        x = -4.5 + (STRIDE / (8 * HOLD)) * i
        walker.location = (x, 0.0, 1.70)
        torch.location = (x + (p["tx"] - A.SIZE / 2) * (3.4 / A.SIZE), -0.12,
                          1.70 + (A.SIZE / 2 - p["ty"]) * (3.4 / A.SIZE))
        torch.data.energy = 150 + 45 * p["lick"]
        cam.location = (x - 4.2 + 0.9 * t, -7.6 + 1.1 * t, 3.2 - 0.5 * t)
        tgt.location = (x + 0.9, 0.4, 1.6)
    return move


def shot_temple():
    """Isometric ARPG chamber. One tile, a whole floor, no seam anywhere -
    and the seam score above says so rather than the eye."""
    floor, _ = paint("Marble", lambda c, L: flagstone(c, L, (196, 188, 172, 255)))
    wall, _ = paint("Sandstone", lambda c, L: blocks(c, L, (198, 166, 116, 255)))
    trim, _ = paint("Jade", lambda c, L: fluted(c, L, (72, 116, 104, 255)))
    walk = build_walk()
    clear()

    m_f, m_w, m_t = mat_of("F", floor), mat_of("W", wall), mat_of("T", trim)
    solid = [box("Floor", (0, 0, -0.3), (22, 22, 0.6), m_f)]
    for sx, sy, w, d in ((0, 10.6, 22, 1.2), (0, -10.6, 22, 1.2),
                         (10.6, 0, 1.2, 22), (-10.6, 0, 1.2, 22)):
        solid.append(box("Wall", (sx, sy, 1.6), (w, d, 3.2), m_w))
    for i, r in enumerate((3.2, 2.4, 1.6)):           # a stepped dais
        solid.append(box(f"Step{i}", (0, 0, 0.22 + i * 0.44),
                         (r * 2, r * 2, 0.44), m_t))
    solid.append(box("Altar", (0, 0, 1.72), (1.3, 1.3, 0.9), m_w))
    solid.append(box("Obelisk", (0, 0, 3.0), (0.5, 0.5, 1.7), m_t))
    for i, (x, y) in enumerate(((-6, -6), (6, -6), (-6, 6), (6, 6))):
        solid.append(box(f"Col{i}", (x, y, 1.5), (1.0, 1.0, 3.0), m_t))
        solid.append(box(f"Top{i}", (x, y, 3.15), (1.4, 1.4, 0.3), m_w))
    for i, (x, y, s) in enumerate(((-3.4, -8.2, 0.8), (4.2, -8.6, 0.6),
                                   (8.4, 3.0, 0.9), (-8.6, 1.4, 0.7))):
        solid.append(box(f"Crate{i}", (x, y, s / 2), (s, s, s), m_w))
    density(solid, 52.0)

    walker, tex = card("Walker", (0, 0, 1.9), (3.4, 3.4), walk[0])
    torch = light("Torch", "POINT", (0, 0, 2.4), (1.0, 0.64, 0.3), 140)
    for i, (x, y) in enumerate(((-6, -6), (6, -6), (-6, 6), (6, 6))):
        light(f"Brazier{i}", "POINT", (x, y, 3.4), (1.0, 0.7, 0.38), 120)
    light("Shaft", "AREA", (0, 0, 9), (1.0, 0.9, 0.72), 1500, (0, 0, 0), size=4)
    haze((0, 0, 3), (24, 24, 8), dens=0.009)
    world((0.05, 0.06, 0.09, 1), 0.5)
    cam, tgt = rig(58, 3.2)

    def move(i, t):
        f = (i // HOLD) % 8
        p = A.pose(f)
        tex.image = walk[f]
        # he crosses the chamber toward the dais while the camera arcs
        wx = -7.5 + 7.5 * t
        walker.location = (wx, -1.2, 1.9)
        walker.rotation_euler = (math.radians(90), 0, 0)
        torch.location = (wx + (p["tx"] - A.SIZE / 2) * (3.4 / A.SIZE), -1.35,
                          1.9 + (A.SIZE / 2 - p["ty"]) * (3.4 / A.SIZE))
        torch.data.energy = 190 + 55 * p["lick"]
        a = math.radians(236 + 22 * t)
        r = 15.0 - 1.8 * t
        cam.location = (math.cos(a) * r, math.sin(a) * r, 8.2 - 1.2 * t)
        tgt.location = (wx * 0.3, -0.6, 1.5)
    return move


def shot_hangar():
    """Sci-fi bay. Three bays wearing the SAME painted texture, restated
    through its palette - repaint nothing, ship three moods."""
    base_img, base_doc = paint("Plating", panel)
    cool_img, cool_doc = paint("PlatingCool", panel, check=False)
    warm_img, warm_doc = paint("PlatingWarm", panel, check=False)
    swap_palette(cool_img, cool_doc, -128.0, 0.55)
    swap_palette(warm_img, warm_doc, 158.0, 0.7)
    floor, _ = paint("Deck", lambda c, L: blocks(c, L, (96, 104, 122, 255), 32, 16))
    clear()

    mats = [mat_of("A", base_img), mat_of("B", cool_img), mat_of("C", warm_img)]
    m_d = mat_of("D", floor, rough=0.55)
    solid = [box("Deck", (0, 0, -0.3), (9, 32, 0.6), m_d),
             box("Roof", (0, 0, 6.4), (9, 32, 0.6), m_d)]
    for i in range(4):                                # four bays, not six
        y = -10.5 + i * 7.0
        m = mats[i % 3]
        for sx in (-4.1, 4.1):
            solid.append(box(f"Bay{i}", (sx, y, 3.0), (0.9, 6.0, 6.0), m))
            solid.append(box(f"Rib{i}", (sx * 0.9, y + 3.5, 3.0),
                             (1.4, 0.6, 6.4), m_d))
        solid.append(box(f"Crate{i}", (2.6 - 5.2 * (i % 2), y - 1.6, 0.6),
                         (1.2, 1.2, 1.2), mats[(i + 1) % 3]))
        solid.append(box(f"Pipe{i}", (0, y + 3.5, 6.0), (7.2, 0.4, 0.4), m_d))
    density(solid, 48.0)

    # Lights aimed ACROSS the corridor, not down it. The palette swap is the
    # whole point of this shot and it cannot be read in silhouette.
    for i in range(4):
        y = -10.5 + i * 7.0
        col = ((0.55, 0.78, 1.0), (0.42, 1.0, 0.82), (1.0, 0.58, 0.34))[i % 3]
        for k, (sx, yaw) in enumerate(((-3.2, -90), (3.2, 90))):
            light(f"Wash{i}{k}", "AREA", (sx, y, 3.4), (1.0, 0.97, 0.92), 190,
                  (math.radians(90), 0, math.radians(yaw)), size=4.5)
        light(f"Strip{i}", "AREA", (0, y + 3.5, 5.9), col, 130,
              (math.radians(180), 0, 0), size=4)
    solid.append(box("Bulkhead", (0, 15.5, 3.0), (9, 0.8, 6.0), mats[1]))
    solid.append(box("DoorL", (-2.4, 15.0, 2.2), (2.6, 0.4, 4.4), m_d))
    solid.append(box("DoorR", (2.4, 15.0, 2.2), (2.6, 0.4, 4.4), m_d))
    light("Door", "AREA", (0, 14.4, 2.2), (0.75, 0.9, 1.0), 220,
          (math.radians(90), 0, math.radians(180)), size=2.2)
    haze((0, 2, 3.0), (10, 36, 7), dens=0.006)
    world((0.015, 0.02, 0.035, 1), 0.12)
    cam, tgt = rig(30, 2.2)

    def move(i, t):
        cam.location = (2.6 - 4.6 * t, -14.0 + 14.5 * t, 1.9 + 0.9 * t)
        tgt.location = (-1.8 + 3.2 * t, -6 + 15 * t, 2.9)
    return move


def shot_market():
    """Top-down adventure exterior. A huge ground and hand-sized props, every
    one of them at 24 px/unit, so nothing looks like it came from another game."""
    walk = build_walk()
    ground, _ = paint("Dirt", lambda c, L: flagstone(c, L, (150, 124, 92, 255)))
    wood, _ = paint("Timber", lambda c, L: blocks(c, L, (146, 104, 62, 255), 8, 16))
    cloth_img, _ = paint("Awning", lambda c, L: blocks(c, L, (172, 78, 72, 255),
                                                        32, 8))
    stone, _ = paint("Kerb", lambda c, L: fluted(c, L, (128, 124, 128, 255)))
    clear()

    m_g, m_w, m_c, m_s = (mat_of("G", ground), mat_of("W", wood),
                          mat_of("C", cloth_img), mat_of("S", stone))
    solid = [box("Ground", (0, 0, -0.3), (40, 40, 0.6), m_g)]
    for sx in (-4.4, 4.4):                            # a paved road
        solid.append(box("Kerb", (sx, 0, 0.06), (0.8, 40, 0.24), m_s))
    goods, _ = paint("Goods", lambda c, L: blocks(c, L, (92, 132, 84, 255), 16, 16))
    m_go = mat_of("Go", goods)
    for i in range(5):                                # market stalls
        y = -12 + i * 6.0
        sx = 7.0 if i % 2 else -7.0
        face = -1 if i % 2 else 1
        solid.append(box(f"Counter{i}", (sx, y, 0.55), (2.6, 3.4, 1.1), m_w))
        solid.append(box(f"Top{i}", (sx + face * 0.4, y, 1.14),
                         (3.4, 3.6, 0.22), m_w))
        for k, py in ((0, -1.6), (1, 1.6)):           # awning posts
            solid.append(box(f"Post{i}{k}", (sx + face * 1.9, y + py, 1.28),
                             (0.3, 0.3, 2.56), m_w))
        solid.append(box(f"Awn{i}", (sx + face * 0.9, y, 2.72),
                         (3.4, 3.6, 0.2), m_c,
                         rot=(0, math.radians(-12 * face), 0)))
        for k, (by, sz) in enumerate(((-1.1, 0.42), (0.2, 0.36), (1.2, 0.46))):
            solid.append(box(f"Ware{i}{k}", (sx + face * 0.6, y + by,
                                             1.26 + sz / 2), (sz, sz, sz), m_go))
        for k, (bx, by, sz) in enumerate(((-2.4, -2.4, 0.7), (2.6, 2.2, 0.55))):
            solid.append(box(f"Barrel{i}{k}", (sx + bx, y + by, sz / 2),
                             (sz, sz, sz), m_w))
    density(solid, 44.0)

    walker, wtex = card("Walker", (0.6, -8, 1.7), (3.4, 3.4), walk[0])
    light("Sun", "SUN", (0, 0, 20), (1.0, 0.78, 0.52), 5.0,
          (math.radians(64), 0, math.radians(34)))
    light("Sky", "AREA", (0, 0, 22), (0.5, 0.64, 1.0), 700, size=30)
    haze((0, 0, 4), (44, 44, 10), dens=0.008)
    world((0.30, 0.40, 0.56, 1), 1.0)
    cam, tgt = rig(44, 3.2)

    def move(i, t):
        f = (i // HOLD) % 8
        wtex.image = walk[f]
        wy = -9.0 + 13.0 * t                      # he walks up the street
        walker.location = (0.6, wy, 1.7)
        a = math.radians(-98 + 20 * t)
        r = 12.0 - 1.6 * t
        cam.location = (math.cos(a) * r, math.sin(a) * r + wy * 0.55,
                        6.4 - 1.0 * t)
        tgt.location = (0.5, wy + 1.0, 1.4)
    return move


def shot_shrine():
    """A symmetric facade. The wall texture was drawn as ONE half and echoed
    across the centre line - which is Mirror X, and it halves the work."""
    face, _ = paint("Shrineface", mirrored, check=False)
    step, _ = paint("Steps", lambda c, L: blocks(c, L, (150, 142, 128, 255), 32, 10))
    banner_img, _ = paint("Banner", cloth, check=False)
    clear()

    m_f, m_s = mat_of("F", face), mat_of("S", step)
    solid = [box("Plaza", (0, 0, -0.3), (26, 26, 0.6), m_s)]
    for i in range(4):                                # a flight of steps
        solid.append(box(f"Step{i}", (0, 4.6 + i * 0.9, 0.18 + i * 0.36),
                         (12 - i * 0.8, 0.9, 0.36), m_s))
    # a doorway, so the facade has a silhouette instead of reading as wallpaper
    for sx in (-3.6, 3.6):
        solid.append(box("Jamb", (sx, 9.4, 2.6), (4.8, 1.2, 5.2), m_f))
    solid.append(box("Header", (0, 9.4, 5.9), (12, 1.2, 2.6), m_f))
    for sx in (-3.9, 3.9):                            # mirrored wing towers
        solid.append(box("Wing", (sx, 8.4, 2.4), (2.4, 2.4, 4.8), m_f))
        solid.append(box("Cap", (sx, 8.4, 5.0), (3.0, 3.0, 0.4), m_s))
    solid.append(box("Lintel", (0, 9.4, 7.1), (13.4, 1.8, 0.6), m_s))
    density(solid, 26.0)

    for sx in (-3.55, 3.55):                          # outlined banner props
        card("Banner", (sx, 8.72, 3.6), (2.6, 4.4), banner_img)
        light("Brazier", "POINT", (sx * 1.8, 5.4, 1.6), (1.0, 0.66, 0.34), 260)
    light("Inner", "POINT", (0, 11.4, 3.2), (1.0, 0.66, 0.34), 320)
    light("Idol", "POINT", (0, 11.0, 1.4), (1.0, 0.78, 0.5), 160)
    light("Moon", "SUN", (0, 0, 20), (0.58, 0.72, 1.0), 2.4,
          (math.radians(44), 0, math.radians(-24)))
    haze((0, 5, 3.5), (28, 28, 9), dens=0.016)
    world((0.05, 0.07, 0.12, 1), 0.55)
    cam, tgt = rig(40, 2.8)

    def move(i, t):
        cam.location = (0.0, -13.0 + 6.4 * t, 4.2 - 0.9 * t)
        tgt.location = (0, 9.2, 3.2 + 0.5 * t)
    return move


SHOTS = {"dungeon": shot_dungeon, "temple": shot_temple, "hangar": shot_hangar,
         "market": shot_market, "shrine": shot_shrine}


def main():
    t0 = time.perf_counter()
    move = SHOTS[NAME]()

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
    # AgX Base, not Medium-High Contrast: the contrasty look crushes shadow
    # detail in fogged interiors and reads as a black frame.
    sc.view_settings.look = "AgX - Base Contrast"

    for i in range(NFRAMES):
        move(i, i / max(1, NFRAMES - 1))
        sc.render.filepath = os.path.join(FR, f"f_{i:04d}")
        bpy.ops.render.render(write_still=True)
        if i and i % 24 == 0:
            el = time.perf_counter() - t0
            print(f"  {NAME} {i}/{NFRAMES}  {el:.0f}s  "
                  f"eta {el / i * (NFRAMES - i):.0f}s", flush=True)

    dst = os.path.join(HERE, "promo", f"shot-{NAME}.mp4")
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate",
                        str(FPS), "-i", os.path.join(FR, "f_%04d.png"),
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17",
                        dst], capture_output=True, text=True)
    ok = r.returncode == 0 and os.path.exists(dst)
    seams = " ".join(f"{n}={s}" for n, s, _ in _seams)
    print(f"TEXEL_SHOT_DONE name={NAME} frames={NFRAMES} "
          f"mp4={'ok' if ok else 'FAIL'} "
          f"bytes={os.path.getsize(dst) if ok else 0} "
          f"secs={NFRAMES / FPS:.1f} seams[{seams}] "
          f"total={time.perf_counter() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
