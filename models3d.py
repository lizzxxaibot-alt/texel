"""Real 3D models for the marketing art. Not shipped.

Why this exists: the promo renders used a flat plane wherever a model was
needed. `record.py` put every prop on an angled card and `gameshots.card()` put
the character on one, with a comment claiming that was "how a 2D sprite appears
in a 3D scene". It was a dodge. A transparent texture on a cube looks hollow, so
instead of modelling a sword I flattened it and wrote a justification.

That contradicts the product. Texel's whole pitch is pixel art painted ON THE
MODEL, and a cardboard cutout is the one thing that proves it is not.

So: everything here is real geometry, built the way pixel-art 3D actually is -
blocky parts, flat shading, one texture atlas, nearest-neighbour filtering. Box
UVs are assigned by hand rather than by `cube_project`, because the atlas layout
has to be known in order to paint into it.

Every texel of every texture comes from Texel's own raster core.

  import models3d
  obj = models3d.character("Torchbearer")
  obj = models3d.prop("sword")
"""
from __future__ import annotations
import math

import bpy

from core import canvas as C
from core import raster as R
from core import tools as TT

TEXEL = 1.0 / 16.0          # one texel of model = 1/16 blender unit
ARM_SWING = math.radians(-135)   # torch arm, swung up at the shoulder
ATLAS = 64                  # atlas is 64x64 texels; parts are packed into it


# --------------------------------------------------------------------------
# atlas
# --------------------------------------------------------------------------
class Atlas:
    """A canvas plus a shelf packer, so each box knows where its faces live.

    A box of w x d x h texels needs its six faces laid out as
        row 1 (h tall):  LEFT(d)  FRONT(w)  RIGHT(d)  BACK(w)
        row 2 (d tall):  TOP(w)   BOTTOM(w)
    which is 2d+2w wide and h+d tall. Allocating that block up front is what
    lets the painter and the UV assignment agree without either guessing.
    """

    def __init__(self, size: int = ATLAS):
        self.size = size
        self.c = C.Canvas(size, size)
        self.L = self.c.layers[0]
        self.x = self.y = self.shelf = 0
        self.P: dict = {}

    # -- packing ---------------------------------------------------------
    def alloc(self, w: int, h: int) -> tuple[int, int]:
        if self.x + w > self.size:
            self.x, self.y = 0, self.y + self.shelf
            self.shelf = 0
        if self.y + h > self.size:
            raise ValueError(f"atlas full: cannot fit {w}x{h}")
        at = (self.x, self.y)
        self.x += w
        self.shelf = max(self.shelf, h)
        return at

    def box_rects(self, w: int, d: int, h: int) -> dict[str, tuple[int, int, int, int]]:
        """Allocate one box and return {face: (x, y, w, h)} in canvas texels."""
        ox, oy = self.alloc(2 * d + 2 * w, h + d)
        return {
            "LEFT":   (ox, oy, d, h),
            "FRONT":  (ox + d, oy, w, h),
            "RIGHT":  (ox + d + w, oy, d, h),
            "BACK":   (ox + 2 * d + w, oy, w, h),
            "TOP":    (ox, oy + h, w, d),
            "BOTTOM": (ox + w, oy + h, w, d),
        }

    # -- painting --------------------------------------------------------
    def col(self, rgba) -> int:
        return self.c.add_colour(rgba)

    def ramp(self, base, n) -> list[int]:
        return [self.c.add_colour(x) for x in TT.make_ramp(base, n)]

    def fill(self, rect, idx) -> None:
        x, y, w, h = rect
        for px, py in R.rect(x, y, x + w - 1, y + h - 1, filled=True):
            self.L.set(px, py, idx)

    def shade(self, rect, ramp, flip=False) -> None:
        """Light at the top of the face, dark at the bottom.

        make_ramp returns DARKEST FIRST, so indexing it in row order lights
        every model from underneath - which is what the first render looked
        like. Walk the ramp backwards unless asked not to.
        """
        x, y, w, h = rect
        n = len(ramp)
        for row in range(h):
            t = row / max(h - 1, 1)
            i = min(int(t * n), n - 1)
            idx = ramp[i] if flip else ramp[n - 1 - i]
            for px in range(x, x + w):
                self.L.set(px, y + row, idx)

    def px(self, rect, pts, idx) -> None:
        """Paint texels given in FACE-LOCAL coordinates."""
        x, y, w, h = rect
        for dx, dy in pts:
            if 0 <= dx < w and 0 <= dy < h:
                self.L.set(x + dx, y + dy, idx)

    def edge(self, rect, idx, top=True, bottom=True, left=True, right=True) -> None:
        x, y, w, h = rect
        if top:
            self.px(rect, [(i, 0) for i in range(w)], idx)
        if bottom:
            self.px(rect, [(i, h - 1) for i in range(w)], idx)
        if left:
            self.px(rect, [(0, i) for i in range(h)], idx)
        if right:
            self.px(rect, [(w - 1, i) for i in range(h)], idx)

    def image(self, name: str):
        """Never reuse or delete a name another material may still hold.

        This used to remove any existing image of the same name first. Put two
        torches in one scene and the second one deleted the first one's texture,
        leaving that material pointing at nothing - which Cycles renders as
        magenta. Take the next free name instead.
        """
        base, n = name, 1
        while name in bpy.data.images:
            name = f"{base}.{n:03d}"
            n += 1
        img = bpy.data.images.new(name, self.c.w, self.c.h, alpha=True)
        img.pixels.foreach_set(self.c.to_blender_floats())
        img.update()
        return img


# --------------------------------------------------------------------------
# geometry
# --------------------------------------------------------------------------
# Each face is four corners, listed counter-clockwise seen from OUTSIDE and
# starting at the corner that gets UV (0,0) of its rect. Getting this wrong
# shows up as a texture rotated a quarter turn on some faces, which is exactly
# the bug the cube unwrap has.
_CORNERS = {
    "FRONT":  (0, 1, 2, 3),
    "BACK":   (5, 4, 7, 6),
    "LEFT":   (4, 0, 3, 7),
    "RIGHT":  (1, 5, 6, 2),
    "TOP":    (3, 2, 6, 7),
    "BOTTOM": (1, 0, 4, 5),
}


def _rotx(pt, pivot, ang):
    """Swing a point around a pivot in the YZ plane - how a shoulder works."""
    y, z = pt[1] - pivot[1], pt[2] - pivot[2]
    c, sn = math.cos(ang), math.sin(ang)
    return (pt[0], pivot[1] + y * c - z * sn, pivot[2] + y * sn + z * c)


def _box_geom(size, offset, rects, atlas_size, vbase, rot=0.0, pivot=None,
              top=None):
    """Vertices, faces and per-loop UVs for one box, in texel units.

    `top` is the (width, depth) of the TOP face. Make it smaller than the
    bottom and the box becomes a frustum - a tapered sleeve, a flared robe, a
    pointed hood. Cubes alone can only ever produce the Minecraft silhouette,
    so this is the one parameter that separates "voxel" from "low-poly".
    """
    w, d, h = size
    tw, td = top if top else (w, d)
    ox, oy, oz = offset
    hx, hy, hz = w / 2.0, d / 2.0, h / 2.0
    tx, ty = tw / 2.0, td / 2.0
    verts = [
        (ox - hx, oy - hy, oz - hz),  # 0 front bottom left
        (ox + hx, oy - hy, oz - hz),  # 1 front bottom right
        (ox + tx, oy - ty, oz + hz),  # 2 front top right
        (ox - tx, oy - ty, oz + hz),  # 3 front top left
        (ox - hx, oy + hy, oz - hz),  # 4 back bottom left
        (ox + hx, oy + hy, oz - hz),  # 5 back bottom right
        (ox + tx, oy + ty, oz + hz),  # 6 back top right
        (ox - tx, oy + ty, oz + hz),  # 7 back top left
    ]
    if rot:
        pv = pivot or (ox, oy, oz)
        verts = [_rotx(v, pv, rot) for v in verts]
    faces, uvs = [], []
    S = float(atlas_size)
    for face, idx in _CORNERS.items():
        rx, ry, rw, rh = rects[face]
        u0, u1 = rx / S, (rx + rw) / S
        # the canvas is top-down and Blender images are bottom-up, so a rect
        # whose top row is ry sits at v = 1 - ry/S
        v1, v0 = 1.0 - ry / S, 1.0 - (ry + rh) / S
        faces.append(tuple(vbase + i for i in idx))
        uvs.extend([(u0, v0), (u1, v0), (u1, v1), (u0, v1)])
    return verts, faces, uvs


def build(name: str, parts: list[dict], atlas: Atlas, image_name: str | None = None):
    """One object from many boxes, one material, one atlas.

    `parts` are dicts of {size, offset, rects} in texel units.
    """
    verts, faces, uvs = [], [], []
    for p in parts:
        v, f, u = _box_geom(p["size"], p["offset"], p["rects"], atlas.size,
                            len(verts), p.get("rot", 0.0), p.get("pivot"),
                            p.get("top"))
        verts.extend(v); faces.extend(f); uvs.extend(u)

    me = bpy.data.meshes.new(name)
    me.from_pydata([(x * TEXEL, y * TEXEL, z * TEXEL) for x, y, z in verts], [], faces)
    me.update()
    uvl = me.uv_layers.new(name="UVMap")
    for i, uv in enumerate(uvs):
        uvl.data[i].uv = uv
    for poly in me.polygons:
        poly.use_smooth = False          # pixel art is flat-shaded, always

    obj = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(obj)

    img = atlas.image(image_name or f"{name}Atlas")
    mat = bpy.data.materials.new(f"{name}Mat")
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    tex.interpolation = "Closest"        # texels stay square
    tex.location = (-420, 240)
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.92
    bsdf.inputs["Specular IOR Level"].default_value = 0.06
    me.materials.append(mat)
    obj["texel_atlas"] = img.name
    return obj


def part(atlas: Atlas, size, offset, paint=None, rot=0.0, pivot=None,
         top=None) -> dict:
    """Allocate atlas space for a box and let a painter fill it.

    `rot` swings the box around `pivot` in the YZ plane, which is what turns a
    hanging arm into a raised one without needing an armature. `top` gives the
    (width, depth) of the top face - set it smaller than the bottom and the part
    tapers, which is the whole difference between a voxel look and a low-poly
    one.
    """
    w, d, h = size
    rects = atlas.box_rects(w, d, h)
    if paint:
        paint(atlas, rects, size)
    return {"size": size, "offset": offset, "rects": rects,
            "rot": rot, "pivot": pivot, "top": top}


# --------------------------------------------------------------------------
# the character
# --------------------------------------------------------------------------
def _pal(a: Atlas) -> dict:
    """The same ramps the sprite art uses, so the 3D and 2D read as one world."""
    P = a.P
    P["cloak"] = a.ramp((146, 44, 58, 255), 5)
    P["cloak_d"] = a.ramp((96, 28, 40, 255), 4)
    P["skin"] = a.ramp((216, 160, 120, 255), 4)
    P["hair"] = a.ramp((58, 40, 46, 255), 3)
    P["leather"] = a.ramp((92, 60, 34, 255), 4)
    P["steel"] = a.ramp((186, 190, 204, 255), 5)
    P["gold"] = a.ramp((226, 178, 58, 255), 4)
    P["wood"] = a.ramp((118, 78, 44, 255), 4)
    P["fire"] = a.ramp((255, 148, 38, 255), 5)
    P["glass"] = a.ramp((92, 170, 176, 255), 4)
    P["stone"] = a.ramp((122, 118, 132, 255), 4)
    P["ink"] = a.col((22, 18, 28, 255))
    return P


def _paint_head(a, rects, size):
    P = a.P
    for f in ("FRONT", "BACK", "LEFT", "RIGHT", "TOP", "BOTTOM"):
        a.shade(rects[f], P["hair"])
    fr = rects["FRONT"]
    w, h = fr[2], fr[3]
    # skin below the fringe. Two rows of hair, not three - a deep fringe on an
    # 8-texel head leaves no face.
    for y in range(2, h):
        a.px(fr, [(x, y) for x in range(w)], P["skin"][2])
    a.px(fr, [(x, h - 1) for x in range(w)], P["skin"][1])       # jaw in shadow
    a.px(fr, [(x, 2) for x in range(w)], P["hair"][0])           # fringe edge
    # eyes: iris plus a catchlight beside it. Two-texel black bars read as a
    # visor, which is what the first pass looked like.
    for ix, lx in ((2, 1), (w - 3, w - 2)):
        a.px(fr, [(ix, 4)], P["ink"])
        a.px(fr, [(lx, 4)], P["skin"][3])
    a.px(fr, [(3, 6), (w - 4, 6)], P["skin"][1])                 # mouth
    a.px(fr, [(0, y) for y in range(2, h)], P["hair"][1])        # sideburns
    a.px(fr, [(w - 1, y) for y in range(2, h)], P["hair"][1])


def _paint_torso(a, rects, size):
    P = a.P
    for f in ("FRONT", "BACK", "LEFT", "RIGHT", "TOP", "BOTTOM"):
        a.shade(rects[f], P["cloak"])
    fr = rects["FRONT"]
    w, h = fr[2], fr[3]
    # collar, belt, and a centre seam so the robe is not a flat slab
    a.px(fr, [(x, 0) for x in range(w)], P["cloak_d"][0])
    a.px(fr, [(x, 1) for x in range(w)], P["cloak_d"][1])
    for y in range(2, h - 4):
        a.px(fr, [(w // 2, y)], P["cloak_d"][2])
    belt = h - 4
    a.px(fr, [(x, belt) for x in range(w)], P["leather"][1])
    a.px(fr, [(x, belt + 1) for x in range(w)], P["leather"][2])
    a.px(fr, [(w // 2 - 1, belt), (w // 2, belt), (w // 2 - 1, belt + 1),
              (w // 2, belt + 1)], P["gold"][1])
    for f in ("LEFT", "RIGHT", "BACK"):
        r = f_ = rects[f]
        a.px(r, [(x, belt) for x in range(r[2])], P["leather"][1])
        a.px(r, [(x, belt + 1) for x in range(r[2])], P["leather"][2])


def _paint_skirt(a, rects, size):
    P = a.P
    for f in ("FRONT", "BACK", "LEFT", "RIGHT", "TOP", "BOTTOM"):
        a.shade(rects[f], P["cloak"])
    # vertical folds, which is what stops a robe reading as a box
    for f in ("FRONT", "BACK", "LEFT", "RIGHT"):
        r = rects[f]
        w, h = r[2], r[3]
        # folds start below the waist and stop short of the hem, so they read
        # as cloth rather than as bars across a cage
        for x in range(2, w - 1, 4):
            a.px(r, [(x, y) for y in range(h // 3, h - 1)], P["cloak_d"][2])
        a.px(r, [(x, h - 1) for x in range(w)], P["cloak_d"][0])


def _paint_arm(a, rects, size):
    P = a.P
    for f in ("FRONT", "BACK", "LEFT", "RIGHT", "TOP", "BOTTOM"):
        a.shade(rects[f], P["cloak"])
    for f in ("FRONT", "BACK", "LEFT", "RIGHT"):
        r = rects[f]
        h = r[3]
        # cuff, then a hand below it
        a.px(r, [(x, h - 4) for x in range(r[2])], P["cloak_d"][0])
        for y in range(h - 3, h):
            a.px(r, [(x, y) for x in range(r[2])], P["skin"][1 if y < h - 1 else 2])


def _paint_boot(a, rects, size):
    P = a.P
    for f in ("FRONT", "BACK", "LEFT", "RIGHT", "TOP", "BOTTOM"):
        a.shade(rects[f], P["leather"])


def character(name: str = "Torchbearer"):
    """A blocky humanoid: head, robe, sleeves, boots. Real geometry.

    Proportions are the ones pixel-art 3D games actually use - a large head on a
    short body - because that is what reads at small texture sizes.
    """
    a = Atlas(ATLAS)
    _pal(a)
    parts = [
        part(a, (8, 8, 8), (0, 0, 24), _paint_head),      # head
        part(a, (8, 6, 10), (0, 0, 15), _paint_torso),    # torso
        part(a, (10, 8, 9), (0, 0, 5.5), _paint_skirt),   # robe skirt
        part(a, (3, 4, 11), (-5.5, 0, 15.5), _paint_arm),  # left arm, hanging
        # right arm swung up from the shoulder so the torch is held ALOFT.
        # A figure with both arms down holding a torch at hip height reads as
        # someone carrying a stick.
        part(a, (3, 4, 11), (5.5, 0, 15.5), _paint_arm,
             rot=ARM_SWING, pivot=(5.5, 0, 21)),
        part(a, (4, 5, 2), (-2.5, -0.5, 1), _paint_boot),
        part(a, (4, 5, 2), (2.5, -0.5, 1), _paint_boot),
    ]
    obj = build(name, parts, a, image_name=f"{name}Atlas")
    # the grip point, in the character's own space: bottom of the right sleeve.
    # Published so props can be parented into the hand rather than guessed at.
    obj["texel_hand"] = (5.5 * TEXEL, -7.778 * TEXEL, 28.778 * TEXEL)
    obj["texel_height"] = 29 * TEXEL
    return obj


def _paint_robe(a, rects, size):
    P = a.P
    for f in _CORNERS:
        a.shade(rects[f], P["cloak"])
    for f in ("FRONT", "BACK", "LEFT", "RIGHT"):
        r = rects[f]
        w, h = r[2], r[3]
        for x in range(2, w - 1, 5):
            a.px(r, [(x, y) for y in range(h // 4, h - 1)], P["cloak_d"][2])
        a.px(r, [(x, h - 1) for x in range(w)], P["cloak_d"][0])
        a.px(r, [(x, h - 2) for x in range(w)], P["cloak_d"][1])


def _paint_hood(a, rects, size):
    P = a.P
    for f in _CORNERS:
        a.shade(rects[f], P["cloak_d"])
    for f in ("FRONT", "LEFT", "RIGHT", "BACK"):
        r = rects[f]
        a.px(r, [(x, r[3] - 1) for x in range(r[2])], P["ink"])   # brow shadow


def _paint_face(a, rects, size):
    """A recessed face: dark, with two lit eyes. No Minecraft mouth."""
    P = a.P
    for f in _CORNERS:
        a.fill(rects[f], P["ink"])
    fr = rects["FRONT"]
    w, h = fr[2], fr[3]
    a.px(fr, [(x, y) for x in range(w) for y in range(h // 2, h)], P["skin"][0])
    for ex in (1, w - 2):
        a.px(fr, [(ex, h // 2)], P["fire"][4])


def _paint_sleeve(a, rects, size):
    P = a.P
    for f in _CORNERS:
        a.shade(rects[f], P["cloak"])
    for f in ("FRONT", "BACK", "LEFT", "RIGHT"):
        r = rects[f]
        a.px(r, [(x, 2) for x in range(r[2])], P["cloak_d"][1])


def character_hooded(name: str = "Wanderer"):
    """A hooded low-poly figure - tapered, not cubic.

    Answers the obvious objection to the blocky character: pixel-art 3D does
    NOT have to be voxel. Every part here is a frustum, so the silhouette is a
    flared robe under a pointed hood rather than six stacked cubes, and it does
    not read as a Minecraft skin. Same texture pipeline, same flat shading, same
    nearest-neighbour filtering - only the geometry changed.
    """
    a = Atlas(128)
    _pal(a)
    parts = [
        # robe, flared to the floor
        part(a, (15, 12, 14), (0, 0, 7), _paint_robe, top=(9, 7)),
        part(a, (9, 7, 7), (0, 0, 17.5), _paint_robe, top=(8, 6)),
        # a shoulder cape, which is what breaks the "box man" read at a glance
        part(a, (13, 11, 3), (0, 0, 20.5), _paint_hood, top=(9, 8)),
        # hood: tapers almost to a point
        part(a, (10, 9, 8), (0, 0.6, 25), _paint_hood, top=(3, 3)),
        part(a, (5, 1, 4), (0, -4.2, 24), _paint_face),
        # sleeves taper to the wrist: bottom is the cuff, top the shoulder
        part(a, (3, 3, 10), (-5.4, 0, 16), _paint_sleeve, top=(5, 5)),
        part(a, (3, 3, 10), (5.4, 0, 16), _paint_sleeve, top=(5, 5),
             rot=ARM_SWING, pivot=(5.4, 0, 21)),
    ]
    obj = build(name, parts, a, image_name=f"{name}Atlas")
    hy = -(11 - 21) * math.sin(ARM_SWING)
    hz = 21 + (11 - 21) * math.cos(ARM_SWING)
    obj["texel_hand"] = (5.4 * TEXEL, hy * TEXEL, hz * TEXEL)
    obj["texel_height"] = 29 * TEXEL
    return obj


# --------------------------------------------------------------------------
# props - each one real geometry, not a card
# --------------------------------------------------------------------------
def _steel(a, rects, size):
    """Blade steel: bright fuller down the middle, dark bevels at the edges.

    Shading a blade top-to-bottom like a wall makes it read as a white slab,
    which is what the first pass did. A blade's form runs ACROSS it.
    """
    P = a.P
    for f in _CORNERS:
        a.fill(rects[f], P["steel"][3])
    for f in ("FRONT", "BACK"):
        r = rects[f]
        w, h = r[2], r[3]
        a.px(r, [(0, y) for y in range(h)], P["steel"][1])
        a.px(r, [(w - 1, y) for y in range(h)], P["steel"][1])
        if w >= 3:
            a.px(r, [(w // 2, y) for y in range(h)], P["steel"][4])
    for f in ("LEFT", "RIGHT"):
        a.fill(rects[f], P["steel"][2])
    a.fill(rects["TOP"], P["steel"][4])
    a.fill(rects["BOTTOM"], P["steel"][1])


def _plate(a, rects, size):
    """Solid steel, no fuller. The blade painter's bright centre line makes an
    axe head read as three separate plates stacked together."""
    P = a.P
    for f in _CORNERS:
        a.shade(rects[f], P["steel"])
    for f in ("LEFT", "RIGHT"):
        a.fill(rects[f], P["steel"][4])          # the cutting edge catches light


def _bottle(a, rects, size):
    """Glass with something in it: bright shoulder, dark liquid, one highlight."""
    P = a.P
    for f in _CORNERS:
        a.shade(rects[f], P["glass"])
    for f in ("FRONT", "BACK", "LEFT", "RIGHT"):
        r = rects[f]
        w, h = r[2], r[3]
        for y in range(max(h // 2, 1), h):          # the liquid sits low
            a.px(r, [(x, y) for x in range(w)], P["glass"][1])
        a.px(r, [(x, max(h // 2, 1)) for x in range(w)], P["glass"][3])
        a.px(r, [(1, y) for y in range(1, max(h - 1, 2))], P["glass"][3])


def _wrap(a, rects, size):
    """Bound leather - horizontal bands, so a grip is not a smooth stick."""
    P = a.P
    for f in _CORNERS:
        a.shade(rects[f], P["leather"])
    for f in ("FRONT", "BACK", "LEFT", "RIGHT"):
        r = rects[f]
        for y in range(0, r[3], 2):
            a.px(r, [(x, y) for x in range(r[2])], P["leather"][0])


def _wood(a, rects, size):
    P = a.P
    for f in _CORNERS:
        a.shade(rects[f], P["wood"])
    for f in ("FRONT", "BACK", "LEFT", "RIGHT"):
        r = rects[f]
        for y in range(0, r[3], 3):
            a.px(r, [(x, y) for x in range(r[2])], P["wood"][3])


def _haft(a, rects, size):
    """A shaft: vertical grain. The plank banding used for crates makes a
    handle look like a barber pole."""
    P = a.P
    for f in _CORNERS:
        a.shade(rects[f], P["wood"])
    for f in ("FRONT", "BACK", "LEFT", "RIGHT"):
        r = rects[f]
        for x in range(0, r[2], 2):
            a.px(r, [(x, y) for y in range(r[3])], P["wood"][1])


def _gold(a, rects, size):
    P = a.P
    for f in _CORNERS:
        a.shade(rects[f], P["gold"])


def _glass(a, rects, size):
    P = a.P
    for f in _CORNERS:
        a.shade(rects[f], P["glass"])
    for f in ("FRONT", "BACK", "LEFT", "RIGHT"):
        r = rects[f]
        a.px(r, [(1, y) for y in range(1, max(r[3] - 1, 2))], P["glass"][0])


def _leather(a, rects, size):
    P = a.P
    for f in _CORNERS:
        a.shade(rects[f], P["leather"])


def _stone(a, rects, size):
    P = a.P
    for f in _CORNERS:
        a.shade(rects[f], P["stone"])


# name -> [(size, offset, painter)] in texels
PROPS = {
    # A sword TAPERS. Three blade segments and a tip, not one rectangle.
    "sword":  [((3, 3, 2), (0, 0, 1), _gold),           # pommel
               ((2, 2, 6), (0, 0, 5), _wrap),           # grip
               ((8, 3, 2), (0, 0, 9), _gold),           # crossguard
               ((3, 1, 10), (0, 0, 15), _steel),        # blade, wide
               ((2, 1, 7), (0, 0, 23.5), _steel),       # blade, narrowed
               ((1, 1, 2), (0, 0, 28), _steel)],        # tip
    # the head is a wedge that straddles the haft, not a slab beside it
    "axe":    [((2, 2, 20), (0, 0, 10), _haft),
               ((3, 4, 9), (2.0, 0, 16), _plate),
               ((2, 4, 12), (4.5, 0, 16), _plate),
               ((3, 3, 2), (0, 0, 20.5), _wrap)],
    "torch":  [((2, 2, 13), (0, 0, 6.5), _haft),
               ((3, 3, 4), (0, 0, 14.5), _wrap)],
    "potion": [((7, 7, 3), (0, 0, 1.5), _bottle),       # base
               ((8, 8, 5), (0, 0, 5.5), _bottle),       # body
               ((6, 6, 2), (0, 0, 9), _bottle),         # shoulder
               ((3, 3, 3), (0, 0, 11.5), _bottle),      # neck
               ((4, 4, 2), (0, 0, 14), _wrap)],         # cork
    "chest":  [((11, 8, 5), (0, 0, 2.5), _wood),
               ((11, 8, 3), (0, 0, 6.5), _wood),
               ((2, 9, 8), (0, 0, 4), _gold),
               ((3, 1, 3), (0, -4.3, 5.0), _gold)],     # lock plate
    "crate":  [((9, 9, 9), (0, 0, 4.5), _wood),
               ((10, 10, 1), (0, 0, 8.6), _wood),
               ((10, 10, 1), (0, 0, 0.4), _wood)],
    "coin":   [((9, 2, 9), (0, 0, 4.5), _gold),
               ((7, 3, 7), (0, 0, 4.5), _gold),
               ((3, 4, 3), (0, 0, 4.5), _gold)],
    "brick":  [((9, 9, 9), (0, 0, 4.5), _stone)],
}


def prop(kind: str, name: str | None = None):
    """One prop, built from boxes. No planes anywhere."""
    if kind not in PROPS:
        raise KeyError(f"unknown prop {kind!r}; have {sorted(PROPS)}")
    a = Atlas(ATLAS)
    _pal(a)
    parts = [part(a, s, o, p) for s, o, p in PROPS[kind]]
    return build(name or kind.title(), parts, a, image_name=f"{kind}Atlas")


def flame(name="Flame", loc=(0, 0, 0), scale=1.0):
    """A tapered emissive flame, still real geometry - three stacked boxes."""
    a = Atlas(ATLAS)
    _pal(a)
    # flat fills, brightest at the base: shading a 3-texel box with a 5-step
    # ramp put near-white at the top of every flame and it rendered as a candle
    # Explicit fire colours. A 5-step ramp's brightest entry is near-white, and
    # emission on near-white clips to white - the flame rendered as a candle.
    core = a.col((255, 168, 42, 255))
    mid = a.col((238, 108, 26, 255))
    tip = a.col((186, 54, 22, 255))
    parts = [part(a, (3, 3, 3), (0, 0, 1.5), lambda x, r, s: [
                  x.fill(r[f], core) for f in _CORNERS]),
             part(a, (2, 2, 3), (0, 0, 4), lambda x, r, s: [
                  x.fill(r[f], mid) for f in _CORNERS]),
             part(a, (1, 1, 3), (0, 0, 6.5), lambda x, r, s: [
                  x.fill(r[f], tip) for f in _CORNERS])]
    o = build(name, parts, a, image_name="FlameAtlas")
    nt = o.data.materials[0].node_tree
    b = nt.nodes["Principled BSDF"]
    tex = [n for n in nt.nodes if n.type == "TEX_IMAGE"][0]
    nt.links.new(tex.outputs["Color"], b.inputs["Emission Color"])
    b.inputs["Emission Strength"].default_value = 1.6
    o.location = loc
    o.scale = (scale, scale, scale)
    return o
