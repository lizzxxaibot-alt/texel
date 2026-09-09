"""One character in each of the five styles this audience actually ships.

Not shipped with the add-on. Built from measured research, not taste - itch.io
tag counts pulled 2026-09-09:

  1 PS1/PSX retro      6,407 games / 2,398 assets   Lethal Company, Signalis
  2 Voxel              3,068 games /   967 assets   Bonfire Peaks, Cube World
  3 Billboard / 2.5D     594 (fps+pixel-art)        Nightmare Reaper, HD-2D
  4 Clean pixel low-poly  not isolable from #1      Anodyne 2
  5 N64 retro            182 games                  Corn Kidz 64

Two of these are honest NON-fits for Texel and are built anyway, because a
comparison that only shows the flattering cases is a sales pitch, not a test:

  - VOXEL has no UV texture at all. Colour is per-cube, assigned in MagicaVoxel
    or Blockbench and baked to vertex colours or a palette strip on export. A
    texture painter has nothing to do on the primary authoring step. (The
    palette-strip UV used here is exactly what MagicaVoxel's OBJ export writes.)
  - BILLBOARD has no mesh. The character is a flat plane wearing an Aseprite
    sprite sheet. Texel can paint that sheet in the Image Editor, but there is
    no model to paint ON.

The other three - PSX, clean low-poly and N64 - are the same mechanic Texel
exists for: a UV-mapped low-poly mesh wearing a small hand-painted texture.

Every texel of every texture here comes from Texel's own raster core.
"""
from __future__ import annotations
import math

import bpy

from core import canvas as C
from core import raster as R
from core import tools as TT
import models3d as M


# --------------------------------------------------------------------------
# 1 + 4 + 5: low-poly meshes wearing a painted atlas
# --------------------------------------------------------------------------
def _skin_pal(a: M.Atlas) -> dict:
    P = a.P
    P["cloth"] = a.ramp((150, 62, 54, 255), 5)
    P["cloth_d"] = a.ramp((92, 34, 40, 255), 4)
    P["skin"] = a.ramp((214, 158, 118, 255), 4)
    P["hair"] = a.ramp((62, 42, 40, 255), 3)
    P["leather"] = a.ramp((96, 62, 36, 255), 4)
    P["steel"] = a.ramp((176, 182, 196, 255), 5)
    P["gold"] = a.ramp((222, 176, 62, 255), 4)
    P["wood"] = a.ramp((118, 78, 44, 255), 4)
    P["fire"] = a.ramp((255, 148, 38, 255), 5)
    P["glass"] = a.ramp((92, 170, 176, 255), 4)
    P["stone"] = a.ramp((122, 118, 132, 255), 4)
    P["ink"] = a.col((24, 20, 28, 255))
    return P


def _tunic(a, rects, size):
    P = a.P
    for f in M._CORNERS:
        a.shade(rects[f], P["cloth"])
    for f in ("FRONT", "BACK", "LEFT", "RIGHT"):
        r = rects[f]
        w, h = r[2], r[3]
        a.px(r, [(x, h - 3) for x in range(w)], P["leather"][1])
        a.px(r, [(x, h - 2) for x in range(w)], P["leather"][0])
    fr = rects["FRONT"]
    w, h = fr[2], fr[3]
    a.px(fr, [(w // 2, y) for y in range(1, h - 3)], P["cloth_d"][2])
    a.px(fr, [(x, 0) for x in range(w)], P["cloth_d"][0])


def _limb(a, rects, size):
    P = a.P
    for f in M._CORNERS:
        a.shade(rects[f], P["cloth"])
    for f in ("FRONT", "BACK", "LEFT", "RIGHT"):
        r = rects[f]
        h = r[3]
        for y in range(max(h - 3, 1), h):
            a.px(r, [(x, y) for x in range(r[2])], P["skin"][2])


def _boot(a, rects, size):
    for f in M._CORNERS:
        a.shade(rects[f], a.P["leather"])


def _headwrap(a, rects, size):
    """A lathed head: one strip, so the face is painted into it directly."""
    P = a.P
    x, y, w, h = rects["SIDE"]
    for cx in range(w):
        for cy in range(h):
            t = cy / max(h - 1, 1)
            a.L.set(x + cx, y + cy, P["skin"][2] if t > 0.30 else P["hair"][1])
    # the face occupies the front quarter of the wrap
    fx = x + int(w * 0.5)
    eye_y = y + int(h * 0.46)
    for dx in (-3, 2):
        a.L.set(fx + dx, eye_y, P["ink"])
        a.L.set(fx + dx + (1 if dx < 0 else -1), eye_y, P["skin"][3])
    for dx in range(-1, 1):
        a.L.set(fx + dx, y + int(h * 0.68), P["skin"][1])
    for cx in range(w):
        a.L.set(x + cx, y + int(h * 0.28), P["hair"][0])


def _lowpoly_body(atlas, sides, head_sides, smooth):
    """The shared low-poly skeleton behind PSX, clean and N64.

    Same construction, and that is the point: the three styles differ in how
    they are TEXTURED and RENDERED, not in how they are modelled.
    """
    head = [(0, 0), (4.4, 0.6), (5.0, 2.4), (4.9, 5.6), (3.6, 7.4), (0, 8.0)]
    return [
        # torso, tapered to the shoulders
        M.part(atlas, (8, 5, 11), (0, 0, 15.5), _tunic, top=(9, 5)),
        # hips and legs
        M.part(atlas, (7, 5, 4), (0, 0, 8), _tunic, top=(8, 5)),
        M.part(atlas, (3, 4, 8), (-2.0, 0, 4), _limb, top=(4, 4)),
        M.part(atlas, (3, 4, 8), (2.0, 0, 4), _limb, top=(4, 4)),
        M.part(atlas, (4, 6, 2), (-2.0, -0.6, 1), _boot),
        M.part(atlas, (4, 6, 2), (2.0, -0.6, 1), _boot),
        # arms; the right one swings up at the shoulder to carry the torch
        M.part(atlas, (3, 3, 10), (-5.4, 0, 16), _limb, top=(4, 4)),
        M.part(atlas, (3, 3, 10), (5.4, 0, 16), _limb, top=(4, 4),
               rot=M.ARM_SWING, pivot=(5.4, 0, 21)),
        # lathed head - boxes cannot make a skull read as a skull
        M.lathe(atlas, head, head_sides, (0, 0, 21), _headwrap, smooth=smooth),
    ]


def _hand_point():
    hy = -(11 - 21) * math.sin(M.ARM_SWING)
    hz = 21 + (11 - 21) * math.cos(M.ARM_SWING)
    return (5.4 * M.TEXEL, hy * M.TEXEL, hz * M.TEXEL)


def psx(name: str = "PSX"):
    """PS1-era: hard facets, a tiny atlas, nearest filtering, flat shading.

    The corruption that defines the look - affine texture warp, vertex jitter,
    dithering - happens at RENDER time, not in the mesh; styles_render does the
    part of it that is honest offline (a 320x240 render upscaled nearest, which
    is what a PS1 actually output).
    """
    a = M.Atlas(64)
    _skin_pal(a)
    obj = M.build(name, _lowpoly_body(a, 6, 7, smooth=False), a,
                  image_name=f"{name}Atlas")
    obj["texel_hand"] = _hand_point()
    return obj


def lowpoly(name: str = "Clean"):
    """The same mesh, painted at 128 and rendered crisp: no PS1 damage.

    Anodyne 2 is the shipped example - low-poly, pixel-textured, stable.
    """
    a = M.Atlas(128)
    _skin_pal(a)
    obj = M.build(name, _lowpoly_body(a, 8, 9, smooth=False), a,
                  image_name=f"{name}Atlas")
    obj["texel_hand"] = _hand_point()
    return obj


def n64(name: str = "N64"):
    """N64 hardware had perspective-correct mapping and subpixel precision, so
    there is no warp and no jitter. The signature is Gouraud shading and a
    BILINEAR-filtered low-res texture - soft, not blocky. Also traditionally
    segmented rigid parts rather than a skinned mesh, which this already is.
    """
    a = M.Atlas(64)
    _skin_pal(a)
    obj = M.build(name, _lowpoly_body(a, 10, 12, smooth=True), a,
                  image_name=f"{name}Atlas")
    obj["texel_hand"] = _hand_point()
    # the one N64 trait that is a material setting rather than geometry
    for m in obj.data.materials:
        for n in m.node_tree.nodes:
            if n.type == "TEX_IMAGE":
                n.interpolation = "Linear"
    for p in obj.data.polygons:
        p.use_smooth = True
    return obj


# --------------------------------------------------------------------------
# 2: voxel - cubes, per-voxel colour, NO uv texture
# --------------------------------------------------------------------------
_NB = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
_FACE_VERTS = {
    (0, 0, -1): ((0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)),
    (0, 0, 1):  ((0, 1, 1), (1, 1, 1), (1, 0, 1), (0, 0, 1)),
    (0, -1, 0): ((0, 0, 1), (1, 0, 1), (1, 0, 0), (0, 0, 0)),
    (0, 1, 0):  ((0, 1, 0), (1, 1, 0), (1, 1, 1), (0, 1, 1)),
    (-1, 0, 0): ((0, 1, 1), (0, 0, 1), (0, 0, 0), (0, 1, 0)),
    (1, 0, 0):  ((1, 0, 1), (1, 1, 1), (1, 1, 0), (1, 0, 0)),
}


def _fill(vol, a, b, col):
    (x0, y0, z0), (x1, y1, z1) = a, b
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            for z in range(z0, z1 + 1):
                vol[(x, y, z)] = col


def voxel(name: str = "Voxel"):
    """A MagicaVoxel-style character: a grid of cubes, colour per cube.

    Deliberately built the way the voxel community actually works, which is why
    it is the honest non-fit: there is no UV texture to paint. Colour is baked
    to a palette strip and every face of a cube points at ONE texel of it -
    exactly what MagicaVoxel's OBJ export writes. Texel has nothing to do here.
    """
    a = M.Atlas(64)
    P = _skin_pal(a)
    pal = [P["cloth"][3], P["cloth"][1], P["skin"][2], P["hair"][1],
           P["leather"][1], P["gold"][2], P["ink"], P["cloth_d"][1]]
    CLOTH, CLOTH_D, SKIN, HAIR, LEATHER, GOLD, INK, TRIM = range(8)
    # a palette strip: one texel per colour, along the top row of the atlas
    for i, idx in enumerate(pal):
        a.L.set(i, 0, idx)

    vol: dict = {}
    _fill(vol, (-3, -2, 0), (2, 1, 2), LEATHER)        # boots
    _fill(vol, (-3, -2, 3), (2, 1, 9), CLOTH)          # legs
    _fill(vol, (-1, -2, 3), (0, 1, 9), CLOTH_D)        #   a gap between them
    _fill(vol, (-4, -3, 10), (3, 2, 19), CLOTH)        # torso
    _fill(vol, (-4, -3, 10), (3, 2, 11), TRIM)         # hem
    _fill(vol, (-4, -3, 14), (3, 2, 15), LEATHER)      # belt
    _fill(vol, (-1, -4, 14), (0, -4, 15), GOLD)        #   buckle
    _fill(vol, (-6, -2, 12), (-5, 1, 19), CLOTH)       # left arm
    _fill(vol, (5, -2, 12), (6, 1, 19), CLOTH)         # right arm, raised
    _fill(vol, (5, -2, 20), (6, 1, 25), CLOTH)
    _fill(vol, (5, -2, 26), (6, 1, 27), SKIN)          #   hand
    _fill(vol, (-4, -4, 20), (3, 3, 27), HAIR)         # head
    _fill(vol, (-3, -5, 21), (2, -5, 25), SKIN)        #   face plate
    _fill(vol, (-4, -4, 20), (3, 3, 21), SKIN)         #   jaw
    _fill(vol, (-3, -5, 26), (2, -5, 26), HAIR)        #   fringe over the brow
    vol[(-1, -6, 23)] = SKIN                           #   a nose voxel, which
    vol[(0, -6, 23)] = SKIN                            #   is what stops a head
                                                       #   reading as a slab
    for c in ((-4, -4, 27), (3, -4, 27), (-4, 3, 27), (3, 3, 27),
              (-4, -4, 20), (3, -4, 20), (-4, 3, 20), (3, 3, 20)):
        vol.pop(c, None)                               # bevel the head corners
    vol[(-2, -5, 24)] = INK                            # eyes
    vol[(1, -5, 24)] = INK
    # the torch is built from voxels too. Putting the smooth low-poly prop in
    # this hand would be a different style stapled onto this one.
    _fill(vol, (5, -1, 28), (6, 0, 37), LEATHER)       # haft
    _fill(vol, (5, -1, 33), (6, 0, 34), GOLD)          # binding
    _fill(vol, (4, -2, 38), (7, 1, 40), GOLD)          # flame, wide base
    _fill(vol, (5, -1, 41), (6, 0, 42), GOLD)
    vol[(5, -1, 43)] = GOLD

    verts, faces, uvs = [], [], []
    S = float(a.size)
    for (x, y, z), col in sorted(vol.items()):
        for d in _NB:
            if (x + d[0], y + d[1], z + d[2]) in vol:
                continue                               # interior face, skip it
            base = len(verts)
            for vx, vy, vz in _FACE_VERTS[d]:
                verts.append((x + vx, y + vy, z + vz))
            faces.append((base, base + 1, base + 2, base + 3))
            u = (col + 0.5) / S
            v = 1.0 - 0.5 / S
            uvs.extend([(u, v)] * 4)

    parts = [{"kind": "raw", "verts": verts, "faces": faces, "uvs": uvs}]
    obj = _build_raw(name, parts, a, f"{name}Palette")
    obj["texel_hand"] = (5.5 * M.TEXEL, -4.0 * M.TEXEL, 27.0 * M.TEXEL)
    obj["texel_nofit"] = "no UV texture - colour is per-cube"
    return obj


def _build_raw(name, parts, atlas, image_name):
    """Build straight from vertex/face/uv lists, for geometry that is not boxes."""
    verts, faces, uvs = [], [], []
    for p in parts:
        off = len(verts)
        verts.extend(p["verts"])
        faces.extend(tuple(i + off for i in f) for f in p["faces"])
        uvs.extend(p["uvs"])
    me = bpy.data.meshes.new(name)
    me.from_pydata([(x * M.TEXEL, y * M.TEXEL, z * M.TEXEL) for x, y, z in verts],
                   [], faces)
    me.update()
    uvl = me.uv_layers.new(name="UVMap")
    for i, uv in enumerate(uvs):
        uvl.data[i].uv = uv
    for poly in me.polygons:
        poly.use_smooth = False
    obj = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(obj)
    img = atlas.image(image_name)
    mat = bpy.data.materials.new(f"{name}Mat")
    mat.use_nodes = True
    nt = mat.node_tree
    b = nt.nodes["Principled BSDF"]
    t = nt.nodes.new("ShaderNodeTexImage")
    t.image = img
    t.interpolation = "Closest"
    nt.links.new(t.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.92
    b.inputs["Specular IOR Level"].default_value = 0.05
    me.materials.append(mat)
    obj["texel_atlas"] = img.name
    return obj


# --------------------------------------------------------------------------
# 3: billboard - a flat plane wearing a 2D sprite. No mesh to paint.
# --------------------------------------------------------------------------
SPRITE_W, SPRITE_H = 28, 44


def _sprite() -> "C.Canvas":
    """A side-on pixel sprite, drawn with the raster core, alpha where empty."""
    c = C.Canvas(SPRITE_W, SPRITE_H)
    L = c.layers[0]
    cloth = [c.add_colour(x) for x in TT.make_ramp((150, 62, 54, 255), 5)]
    skin = [c.add_colour(x) for x in TT.make_ramp((214, 158, 118, 255), 4)]
    hair = [c.add_colour(x) for x in TT.make_ramp((62, 42, 40, 255), 3)]
    leather = [c.add_colour(x) for x in TT.make_ramp((96, 62, 36, 255), 4)]
    wood = [c.add_colour(x) for x in TT.make_ramp((118, 78, 44, 255), 4)]
    fire = [c.add_colour(x) for x in TT.make_ramp((255, 148, 38, 255), 5)]
    ink = c.add_colour((24, 20, 28, 255))

    def box(x0, y0, x1, y1, idx):
        for p in R.rect(x0, y0, x1, y1, filled=True):
            L.set(*p, idx)

    cx = SPRITE_W // 2
    box(cx - 5, 34, cx + 4, 41, leather[1])            # boots
    box(cx - 5, 20, cx + 4, 35, cloth[3])              # robe
    box(cx - 5, 20, cx + 4, 22, cloth[4])
    box(cx - 5, 27, cx + 4, 28, leather[1])            # belt
    for x in range(cx - 5, cx + 5, 3):                 # folds
        for y in range(29, 40):
            L.set(x, y, cloth[1])
    box(cx - 4, 12, cx + 3, 21, cloth[3])              # torso
    box(cx - 3, 6, cx + 2, 13, skin[2])                # head
    box(cx - 4, 4, cx + 3, 8, hair[1])                 # hair
    L.set(cx - 2, 10, ink); L.set(cx + 1, 10, ink)     # eyes
    box(cx - 7, 13, cx - 5, 24, cloth[2])              # near arm
    box(cx - 7, 22, cx - 5, 24, skin[2])
    box(cx + 4, 6, cx + 6, 16, cloth[2])               # raised arm
    box(cx + 4, 4, cx + 6, 6, skin[2])
    for p in R.line(cx + 5, 0, cx + 5, 6):             # torch haft
        L.set(*p, wood[2])
        L.set(p[0] + 1, p[1], wood[1])
    box(cx + 4, 0, cx + 7, 1, fire[3])                 # flame
    box(cx + 5, 0, cx + 6, 0, fire[4])

    # a one-texel dark outline, the way a sprite artist would finish it
    solid = {(x, y) for y in range(SPRITE_H) for x in range(SPRITE_W)
             if L.get(x, y)}
    for x, y in list(solid):
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if (0 <= n[0] < SPRITE_W and 0 <= n[1] < SPRITE_H
                    and n not in solid):
                L.set(*n, ink)
    return c


def billboard(name: str = "Billboard"):
    """The 2.5D case: a camera-facing plane wearing an Aseprite-style sheet.

    Unlit on purpose - emission mixed with transparency by alpha - because a
    lamp falling across a hand-shaded sprite destroys the shading the artist
    painted. This is the style where a flat card is CORRECT, as opposed to a
    dodge for a prop that should have been modelled.
    """
    c = _sprite()
    img = bpy.data.images.get(f"{name}Sprite")
    if img:
        bpy.data.images.remove(img)
    img = bpy.data.images.new(f"{name}Sprite", c.w, c.h, alpha=True)
    img.pixels.foreach_set(c.to_blender_floats())
    img.update()

    # one sprite texel = one model texel, so the sprite stands the same height
    # as the modelled characters and the comparison is like for like
    h = SPRITE_H * M.TEXEL
    w = h * SPRITE_W / SPRITE_H
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(0, 0, h / 2))
    o = bpy.context.active_object
    o.name = name
    # a default plane lies in XY with z=0. Scaling Z does NOTHING to it - the
    # first version scaled (w, 1, h) and rendered a squashed strip.
    o.scale = (w, h, 1.0)
    o.rotation_euler = (math.radians(90), 0, 0)
    # bake BOTH: the caller sets rotation_euler to turn the character, which
    # would otherwise wipe the stand-up and lay the plane flat - it rendered as
    # a horizontal line
    bpy.ops.object.transform_apply(scale=True, rotation=True, location=False)

    mat = bpy.data.materials.new(f"{name}Mat")
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        if n.type != "OUTPUT_MATERIAL":
            nt.nodes.remove(n)
    out = nt.nodes["Material Output"]
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    tex.interpolation = "Closest"
    tex.location = (-620, 0)
    emis = nt.nodes.new("ShaderNodeEmission")
    emis.inputs["Strength"].default_value = 1.0
    trans = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(tex.outputs["Color"], emis.inputs["Color"])
    nt.links.new(tex.outputs["Alpha"], mix.inputs[0])
    nt.links.new(trans.outputs["BSDF"], mix.inputs[1])
    nt.links.new(emis.outputs["Emission"], mix.inputs[2])
    nt.links.new(mix.outputs["Shader"], out.inputs["Surface"])
    o.data.materials.append(mat)
    o["texel_nofit"] = "no mesh - the character is a 2D sheet"
    return o
