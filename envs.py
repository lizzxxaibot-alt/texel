"""Five game environments, every texture painted by Texel's own core.

Each environment exists to show a DIFFERENT capability, so the advert set is not
five versions of one idea:

  shrine    forest shrine at dusk    -> tileable textures, verified by Check Tiling
  corridor  sci-fi corridor          -> generated shading ramps + emissive palettes
  ruins     desert ruins at noon     -> density zones (huge pillars vs small pots)
  tavern    tavern interior          -> layers, and a palette swap for variants
  cavern    ice cavern               -> mirror symmetry, and translucent crystal

Textures come from core.raster / core.canvas only. Geometry is boxes and
cylinders, deliberately, because the point on screen is the TEXTURE.
"""
import math

import bpy

from core import raster as R
from core import tools as T
from core.canvas import Canvas


# ============================================================== paint helpers
def to_image(name, c):
    img = bpy.data.images.get(name)
    if img:
        bpy.data.images.remove(img)
    img = bpy.data.images.new(name, c.w, c.h, alpha=True)
    img.pixels.foreach_set(c.to_blender_floats())
    img.update()
    img["texel_seam"] = T.tile_seam_score(c.flatten(), c.w, c.h, c.palette)["score"]
    return img


def fill(L, idx, w, h):
    for p in R.rect(0, 0, w - 1, h - 1, filled=True):
        L.set(*p, idx)


def speckle(L, w, h, idx, period, thresh=2, only=None):
    """Deterministic scatter - a hash, not random, so a texture is reproducible."""
    for y in range(h):
        for x in range(w):
            if only is not None and L.get(x, y) != only:
                continue
            if (x * 7 + y * 13) % period < thresh:
                L.set(x, y, idx)


def ramp_of(c, base, steps=5):
    """Palette ramp through Texel's own generator, returned as indices."""
    return [c.add_colour(rgba) for rgba in T.make_ramp(base, steps)]


def bricks(L, w, h, mortar, face, hi, lo, bw=16, bh=8):
    fill(L, mortar, w, h)
    for i, y in enumerate(range(0, h, bh)):
        off = 0 if i % 2 == 0 else bw // 2
        for x in range(-bw + off, w, bw):
            for p in R.rect(x + 1, y + 1, x + bw - 2, y + bh - 2, filled=True):
                L.set(*p, face)
    for y in range(h):
        for x in range(w):
            if L.get(x, y) == face:
                if L.get(x, y - 1) == mortar:
                    L.set(x, y, hi)
                elif L.get(x, y + 1) == mortar:
                    L.set(x, y, lo)


def planks(L, w, h, wood, seam, light, every=8):
    fill(L, wood, w, h)
    for x in range(0, w, every):
        for p in R.line(x, 0, x, h - 1):
            L.set(*p, seam)
        for p in R.line(x + 1, 0, x + 1, h - 1):
            L.set(*p, light)


# ================================================================== 1. SHRINE
def tex_shrine(size=64):
    out = {}

    c = Canvas(size, size)
    g = ramp_of(c, (72, 128, 66, 255), 5)
    L = c.layers[0]
    fill(L, g[1], size, size)
    speckle(L, size, size, g[2], 5, 2)
    speckle(L, size, size, g[3], 11, 2)
    for bx, by in ((6, 14), (21, 7), (38, 19), (52, 11), (13, 41), (44, 50), (29, 31)):
        for p in R.line(bx, by, bx, by - 4):
            L.set(*p, g[4])
        L.set(bx - 1, by - 3, g[3])
        L.set(bx + 1, by - 4, g[4])
    out["grass"] = to_image("Shrine Grass", c)

    c = Canvas(size, size)
    s = ramp_of(c, (128, 124, 118, 255), 5)
    L = c.layers[0]
    fill(L, s[2], size, size)
    for gy in range(0, size, 16):                      # irregular flagstones
        for gx in range(0, size, 16):
            off = 8 if (gy // 16) % 2 else 0
            x0 = (gx + off) % size
            for p in R.rect(x0 + 1, gy + 1, x0 + 13, gy + 13, filled=True):
                L.set(*p, s[3])
            for p in R.line(x0 + 2, gy + 2, x0 + 12, gy + 2):
                L.set(*p, s[4])
    speckle(L, size, size, s[1], 17, 2)
    out["path"] = to_image("Shrine Path", c)

    c = Canvas(size, size)
    v = ramp_of(c, (188, 62, 48, 255), 5)              # vermilion torii
    L = c.layers[0]
    planks(L, size, size, v[2], v[1], v[3], every=11)
    speckle(L, size, size, v[1], 29, 2)
    out["vermilion"] = to_image("Shrine Vermilion", c)

    c = Canvas(size, size)
    t = ramp_of(c, (58, 66, 82, 255), 5)               # roof tiles
    L = c.layers[0]
    fill(L, t[1], size, size)
    for y in range(0, size, 8):
        for x in range(0, size, 10):
            off = 5 if (y // 8) % 2 else 0
            for p in R.ellipse_box(x + off, y, x + off + 8, y + 6, filled=True):
                L.set(*p, t[3])
            for p in R.line(x + off + 1, y + 1, x + off + 7, y + 1):
                L.set(*p, t[4])
    out["roof"] = to_image("Shrine Roof", c)

    c = Canvas(32, 32)
    p = c.add_colour((252, 226, 168, 255))
    pd = c.add_colour((214, 172, 96, 255))
    L = c.layers[0]
    fill(L, p, 32, 32)
    for y in (6, 15, 24):
        for q in R.line(0, y, 31, y):
            L.set(*q, pd)
    out["paper"] = to_image("Shrine Paper", c)
    return out


def build_shrine(mats):
    B = _box
    B("Ground", (0, 0, -0.3), (34, 34, 0.6), mats["grass"])
    for i in range(9):                                   # a path leading in
        B(f"Path{i}", (0, -9 + i * 2.4, 0.02), (3.4, 2.3, 0.08), mats["path"])
    # torii gate
    for x in (-3.2, 3.2):
        B(f"ToriiLeg{x}", (x, 1.0, 2.6), (0.55, 0.55, 5.2), mats["vermilion"])
    B("ToriiTop", (0, 1.0, 5.4), (8.6, 0.8, 0.55), mats["vermilion"])
    B("ToriiCap", (0, 1.0, 5.95), (9.6, 1.0, 0.35), mats["roof"])
    B("ToriiTie", (0, 1.0, 4.2), (7.0, 0.5, 0.4), mats["vermilion"])
    # shrine building
    B("ShrineBody", (0, 9.5, 1.6), (6.0, 4.4, 3.2), mats["vermilion"])
    B("ShrineRoof", (0, 9.5, 3.7), (7.6, 6.0, 0.9), mats["roof"])
    B("ShrineStep", (0, 6.9, 0.35), (5.0, 1.2, 0.7), mats["path"])
    # lanterns
    for x, y in ((-4.6, 5.0), (4.6, 5.0), (-4.6, 8.4), (4.6, 8.4)):
        B(f"LPost{x}{y}", (x, y, 1.0), (0.3, 0.3, 2.0), mats["vermilion"])
        B(f"LBox{x}{y}", (x, y, 2.35), (0.95, 0.95, 0.95), mats["paper"], emissive=True)
    # trees framing the shot
    for x, y, h in ((-9, 3, 4.0), (9.5, 6, 4.6), (-8.5, 11, 3.6), (10, 13, 4.2)):
        B(f"Trunk{x}{y}", (x, y, h / 2), (0.9, 0.9, h), mats["vermilion"])
        for k in range(3):
            s = 5.2 - k * 1.3
            B(f"Leaf{x}{y}{k}", (x, y, h + 0.7 + k * 1.1), (s, s, 1.1), mats["grass"])
    return "grass"


def light_shrine():
    # Golden hour, not night. A dark scene through AgX crushes to black and
    # reads as a rendering fault rather than a mood.
    _sun((1.0, 0.80, 0.56), 6.0, (48, 0, 116))
    for x, y in ((-4.6, 5.0), (4.6, 5.0), (-4.6, 8.4), (4.6, 8.4)):
        _point((x, y, 2.4), (1.0, 0.76, 0.40), 700, 0.5)
    _world((0.42, 0.46, 0.66), 1.1)
    _fog(0.0014, (0.72, 0.58, 0.52))


def cam_shrine(t):
    e = _ease(t)
    a = math.radians(-108 + 34 * e)
    r = 26.0 - 8.0 * e                    # stop well short of the torii at y=1
    return (math.cos(a) * r, math.sin(a) * r - 2.0, 7.4 - 2.2 * e), (0, 5.5, 3.4)


# ================================================================ 2. CORRIDOR
def tex_corridor(size=64):
    out = {}
    c = Canvas(size, size)
    m = ramp_of(c, (96, 106, 124, 255), 6)
    L = c.layers[0]
    fill(L, m[2], size, size)
    for gy in range(0, size, 32):                        # big panels
        for gx in range(0, size, 32):
            for p in R.rect(gx + 2, gy + 2, gx + 29, gy + 29):
                L.set(*p, m[0])
            for p in R.rect(gx + 3, gy + 3, gx + 28, gy + 28, filled=True):
                L.set(*p, m[3])
            for p in R.line(gx + 4, gy + 4, gx + 27, gy + 4):
                L.set(*p, m[5])
            for rx, ry in ((7, 7), (25, 7), (7, 25), (25, 25)):   # rivets
                L.set(gx + rx, gy + ry, m[1])
                L.set(gx + rx + 1, gy + ry, m[5])
    out["panel"] = to_image("Corr Panel", c)

    c = Canvas(size, size)
    f = ramp_of(c, (70, 78, 92, 255), 5)
    L = c.layers[0]
    fill(L, f[1], size, size)
    for y in range(0, size, 8):
        for p in R.line(0, y, size - 1, y):
            L.set(*p, f[0])
        for p in R.line(0, y + 1, size - 1, y + 1):
            L.set(*p, f[3])
    speckle(L, size, size, f[2], 13, 2)
    out["floor"] = to_image("Corr Floor", c)

    c = Canvas(size, 16)
    glow = c.add_colour((94, 232, 255, 255))
    core = c.add_colour((226, 252, 255, 255))
    dim = c.add_colour((22, 92, 116, 255))
    L = c.layers[0]
    fill(L, dim, size, 16)
    for p in R.rect(0, 5, size - 1, 10, filled=True):
        L.set(*p, glow)
    for p in R.rect(0, 7, size - 1, 8, filled=True):
        L.set(*p, core)
    out["strip"] = to_image("Corr Strip", c)

    c = Canvas(size, size)
    o = ramp_of(c, (204, 122, 42, 255), 5)
    L = c.layers[0]
    fill(L, o[2], size, size)
    for p in R.rect(4, 4, size - 5, size - 5):
        L.set(*p, o[0])
    for p in R.rect(6, 6, size - 7, size - 7):
        L.set(*p, o[4])
    for p in R.pixel_perfect(R.line(8, 8, size - 9, size - 9)):
        L.set(*p, o[0])
    for p in R.pixel_perfect(R.line(size - 9, 8, 8, size - 9)):
        L.set(*p, o[0])
    out["crate"] = to_image("Corr Crate", c)
    return out


def build_corridor(mats):
    B = _box
    B("Floor", (0, 0, -0.25), (7.0, 40, 0.5), mats["floor"])
    B("Ceiling", (0, 0, 5.2), (7.0, 40, 0.5), mats["panel"])
    for x in (-3.4, 3.4):
        B(f"Wall{x}", (x, 0, 2.5), (0.6, 40, 5.4), mats["panel"])
    for i in range(9):                                    # ribs and light strips
        y = -16 + i * 4.2
        for x in (-2.9, 2.9):
            B(f"Rib{i}{x}", (x, y, 2.5), (0.45, 0.7, 5.2), mats["panel"])
        B(f"Strip{i}L", (-3.02, y, 3.9), (0.12, 3.2, 0.34), mats["strip"], emissive=True)
        B(f"Strip{i}R", (3.02, y, 3.9), (0.12, 3.2, 0.34), mats["strip"], emissive=True)
        B(f"StripC{i}", (0, y, 5.0), (1.6, 0.34, 0.12), mats["strip"], emissive=True)
    for loc, s in (((-2.0, -6.0, 0.6), 1.2), ((-2.2, -4.6, 1.75), 1.0),
                   ((2.1, -2.0, 0.55), 1.1), ((2.3, 3.6, 0.65), 1.3),
                   ((-2.1, 7.0, 0.5), 1.0)):
        o = B("Crate", loc, (s, s, s), mats["crate"])
        o.rotation_euler = (0, 0, math.radians((loc[1] * 23) % 30 - 15))
    for i in range(5):                                    # overhead pipes
        B(f"Pipe{i}", (-1.6 + i * 0.8, 0, 4.85), (0.28, 40, 0.28), mats["panel"])
    # The camera flies TOWARD -y, so the far end needs something to arrive at.
    # Without a bulkhead the shot ends on empty space and the move has no payoff.
    B("EndWall", (0, -20.4, 2.5), (7.0, 0.8, 5.4), mats["panel"])
    B("DoorFrame", (0, -20.0, 1.9), (3.4, 0.4, 3.8), mats["panel"])
    B("DoorGlow", (0, -19.8, 1.8), (2.6, 0.2, 3.2), mats["strip"],
      emissive=True, strength=3.4)
    for dz in (0.4, 3.5):                                 # frame accents
        B(f"DoorTrim{dz}", (0, -19.7, dz), (3.0, 0.16, 0.22), mats["strip"],
          emissive=True, strength=5.0)
    for x, s2 in ((-2.3, 1.0), (2.3, 1.2)):               # crates by the door
        B("Crate", (x, -17.5, 0.5 * s2), (s2, s2, s2), mats["crate"])
    return "floor"


def light_corridor():
    for i in range(9):
        y = -16 + i * 4.2
        _point((-2.9, y, 3.9), (0.36, 0.86, 1.0), 620, 0.35)
        _point((2.9, y, 3.9), (0.36, 0.86, 1.0), 620, 0.35)
    _point((0, -18.5, 2.4), (0.42, 0.86, 1.0), 3000, 1.4)   # doorway glow
    _world((0.03, 0.05, 0.08), 0.35)
    _fog(0.0032, (0.24, 0.44, 0.58))


def cam_corridor(t):
    e = _ease(t)
    return (math.sin(t * math.pi * 1.2) * 0.7, 13.0 - 22.0 * e, 2.3 + 0.5 * e), \
           (0, -16.0, 2.2)


# =================================================================== 3. RUINS
def tex_ruins(size=64):
    out = {}
    c = Canvas(size, size)
    s = ramp_of(c, (206, 176, 122, 255), 6)
    L = c.layers[0]
    bricks(L, size, size, s[1], s[3], s[5], s[2], bw=32, bh=16)
    speckle(L, size, size, s[2], 19, 2, only=s[3])
    out["sandstone"] = to_image("Ruins Sandstone", c)

    c = Canvas(size, size)
    d = ramp_of(c, (222, 194, 140, 255), 5)
    L = c.layers[0]
    fill(L, d[3], size, size)
    for y in range(size):                                 # wind ripples
        for x in range(size):
            if (x + y * 2) % 9 < 2:
                L.set(x, y, d[4])
            elif (x + y * 2) % 9 == 4:
                L.set(x, y, d[2])
    out["sand"] = to_image("Ruins Sand", c)

    c = Canvas(size, size)
    p = ramp_of(c, (176, 92, 62, 255), 5)
    L = c.layers[0]
    fill(L, p[2], size, size)
    for y in range(0, size, 6):
        for q in R.line(0, y, size - 1, y):
            L.set(*q, p[1])
        for q in R.line(0, y + 1, size - 1, y + 1):
            L.set(*q, p[4])
    for q in R.rect(18, 22, 45, 41, filled=True):         # painted band
        L.set(*q, p[0])
    for q in R.rect(21, 25, 42, 38):
        L.set(*q, p[4])
    out["pottery"] = to_image("Ruins Pottery", c)

    c = Canvas(size, size)
    g = ramp_of(c, (198, 164, 108, 255), 5)
    L = c.layers[0]
    fill(L, g[2], size, size)
    for i in range(4):                                    # carved relief glyphs
        ox = 4 + i * 15
        for q in R.rect(ox, 12, ox + 10, 50):
            L.set(*q, g[0])
        for q in R.rect(ox + 2, 16, ox + 8, 30, filled=True):
            L.set(*q, g[4])
        for q in R.ellipse_box(ox + 2, 34, ox + 8, 46, filled=True):
            L.set(*q, g[1])
    out["relief"] = to_image("Ruins Relief", c)
    return out


def build_ruins(mats):
    B = _box
    B("Sand", (0, 0, -0.4), (44, 44, 0.8), mats["sand"])
    for i, (x, y, h) in enumerate(((-6.5, 2, 7.0), (-6.5, 9, 4.2), (6.5, 2, 6.2),
                                   (6.5, 9, 7.4), (-6.5, 16, 2.6), (6.5, 16, 3.4))):
        B(f"Pillar{i}", (x, y, h / 2), (2.0, 2.0, h), mats["sandstone"])
        B(f"Cap{i}", (x, y, h + 0.35), (2.6, 2.6, 0.7), mats["relief"])
    B("Lintel", (0, 2, 7.6), (15.0, 2.2, 1.0), mats["sandstone"])
    B("Wall", (0, 20, 2.6), (20, 1.2, 5.2), mats["relief"])
    for i, (x, y, s) in enumerate(((-2.2, 5.5, 1.0), (2.6, 6.2, 1.3),
                                   (-3.6, 12.0, 0.8), (4.0, 13.5, 1.1))):
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.42 * s,
                                            depth=1.1 * s, location=(x, y, 0.55 * s))
        o = bpy.context.view_layer.objects.active
        o.name = f"Pot{i}"
        bpy.ops.object.shade_flat()
        o.data.materials.append(mats["pottery"])
    for i, (x, y) in enumerate(((-3.0, 3.4), (3.4, 10.0), (-5.0, 14.0), (1.2, 16.0))):
        o = B(f"Rubble{i}", (x, y, 0.45), (1.6, 1.3, 0.9), mats["sandstone"])
        o.rotation_euler = (0, math.radians(9), math.radians((x * 31) % 60))
    return "sand"


def light_ruins():
    _sun((1.0, 0.94, 0.80), 3.4, (62, 0, 24))              # hard noon sun
    _world((0.55, 0.68, 0.92), 0.75)                        # bright desert sky
    _fog(0.0009, (0.86, 0.76, 0.60))


def cam_ruins(t):
    e = _ease(t)
    a = math.radians(-104 + 44 * e)
    r = 22.0 - 7.0 * e
    return (math.cos(a) * r, math.sin(a) * r + 6.0, 6.4 - 2.6 * e), (0, 7.0, 3.0)


# ================================================================== 4. TAVERN
def tex_tavern(size=64):
    out = {}
    c = Canvas(size, size)
    w = ramp_of(c, (146, 98, 54, 255), 6)
    L = c.layers[0]
    planks(L, size, size, w[2], w[0], w[4], every=11)
    speckle(L, size, size, w[1], 23, 2, only=w[2])
    for y in range(0, size, 21):                           # cross joints
        for p in R.line(0, y, size - 1, y):
            L.set(*p, w[0])
    out["floor"] = to_image("Tav Floor", c)

    c = Canvas(size, size)
    pl = ramp_of(c, (214, 198, 168, 255), 5)
    L = c.layers[0]
    fill(L, pl[3], size, size)
    speckle(L, size, size, pl[2], 7, 2)
    for x in (10, 32, 54):                                 # timber framing
        for p in R.rect(x, 0, x + 5, size - 1, filled=True):
            L.set(*p, pl[0])
        for p in R.line(x + 1, 0, x + 1, size - 1):
            L.set(*p, pl[1])
    out["plaster"] = to_image("Tav Plaster", c)

    c = Canvas(size, size)
    r = ramp_of(c, (152, 48, 56, 255), 5)
    L = c.layers[0]
    fill(L, r[2], size, size)
    for p in R.rect(3, 3, size - 4, size - 4):
        L.set(*p, r[4])
    for p in R.rect(6, 6, size - 7, size - 7):
        L.set(*p, r[1])
    for i in range(5):                                     # woven diamonds
        cx = 8 + i * 12
        for p in R.ellipse_box(cx, 24, cx + 9, 39, filled=True):
            L.set(*p, r[4])
    out["rug"] = to_image("Tav Rug", c)

    c = Canvas(size, size)
    b = ramp_of(c, (128, 84, 44, 255), 5)
    L = c.layers[0]
    planks(L, size, size, b[2], b[0], b[3], every=8)
    for y in (8, size - 12):
        for p in R.rect(0, y, size - 1, y + 4, filled=True):
            L.set(*p, b[0])
    out["barrel"] = to_image("Tav Barrel", c)
    return out


def build_tavern(mats):
    B = _box
    B("Floor", (0, 0, -0.25), (24, 24, 0.5), mats["floor"])
    B("Ceiling", (0, 0, 6.0), (24, 24, 0.5), mats["barrel"])
    B("WallBack", (0, 10, 3.0), (24, 0.6, 6.4), mats["plaster"])
    B("WallL", (-10, 0, 3.0), (0.6, 24, 6.4), mats["plaster"])
    B("WallR", (10, 0, 3.0), (0.6, 24, 6.4), mats["plaster"])
    for i in range(5):                                     # ceiling beams
        B(f"Beam{i}", (0, -8 + i * 4.4, 5.5), (20, 0.7, 0.6), mats["barrel"])
    B("Rug", (0, 0.5, 0.03), (9.0, 7.0, 0.06), mats["rug"])
    for tx, ty in ((-4.2, -1.0), (4.0, 1.4), (-3.4, 5.4)):
        B(f"TTop{tx}", (tx, ty, 1.15), (3.4, 2.2, 0.22), mats["barrel"])
        for dx in (-1.4, 1.4):
            for dy in (-0.8, 0.8):
                B(f"TLeg{tx}{dx}{dy}", (tx + dx, ty + dy, 0.55),
                  (0.24, 0.24, 1.1), mats["barrel"])
        for dy in (-1.7, 1.7):                             # benches
            B(f"Bench{tx}{dy}", (tx, ty + dy, 0.6), (3.0, 0.7, 0.2), mats["barrel"])
    B("Bar", (6.8, 6.4, 1.2), (5.6, 1.4, 2.4), mats["barrel"])
    B("BarTop", (6.8, 6.4, 2.5), (6.2, 1.9, 0.25), mats["floor"])
    for i, (x, y) in enumerate(((-8.4, 8.2), (-7.0, 8.4), (8.6, -3.0))):
        bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=0.62, depth=1.5,
                                            location=(x, y, 0.75))
        o = bpy.context.view_layer.objects.active
        o.name = f"Barrel{i}"
        bpy.ops.object.shade_flat()
        o.data.materials.append(mats["barrel"])
    B("Hearth", (-8.6, 1.0, 1.3), (2.2, 3.6, 2.6), mats["plaster"])
    B("Fire", (-7.6, 1.0, 0.8), (0.4, 2.2, 1.2), mats["rug"], emissive=True, strength=9.0)
    for x, y in ((-3.0, 2.0), (3.6, 3.4), (0.0, 7.0)):     # hanging lamps
        B(f"Lamp{x}{y}", (x, y, 4.3), (0.62, 0.62, 0.62), mats["plaster"],
          emissive=True, strength=7.0)
    return "floor"


def light_tavern():
    _point((-7.4, 1.0, 1.3), (1.0, 0.46, 0.16), 4200, 1.0)
    for x, y in ((-3.0, 2.0), (3.6, 3.4), (0.0, 7.0)):
        _point((x, y, 4.2), (1.0, 0.74, 0.42), 1700, 0.55)
    _sun((0.62, 0.72, 1.0), 2.2, (54, 0, -110))            # cool light from a window
    _world((0.06, 0.06, 0.09), 0.4)
    _fog(0.0024, (0.5, 0.36, 0.26))


def cam_tavern(t):
    e = _ease(t)
    a = math.radians(-96 + 40 * e)
    r = 15.5 - 4.6 * e
    return (math.cos(a) * r, math.sin(a) * r + 1.0, 5.0 - 1.9 * e), (0, 2.2, 1.6)


# ================================================================== 5. CAVERN
def tex_cavern(size=64):
    out = {}
    c = Canvas(size, size)
    i = ramp_of(c, (146, 190, 224, 255), 6)
    L = c.layers[0]
    fill(L, i[2], size, size)
    for k in range(7):                                     # fracture lines
        x0, y0 = (k * 11) % size, (k * 23) % size
        for p in R.pixel_perfect(R.line(x0, y0, (x0 + 26) % size, (y0 + 40) % size)):
            if 0 <= p[0] < size and 0 <= p[1] < size:
                L.set(*p, i[4])
    speckle(L, size, size, i[3], 9, 2)
    speckle(L, size, size, i[5], 31, 1)
    out["ice"] = to_image("Cav Ice", c)

    c = Canvas(size, size)
    s = ramp_of(c, (226, 234, 246, 255), 5)
    L = c.layers[0]
    fill(L, s[4], size, size)
    speckle(L, size, size, s[3], 6, 2)
    speckle(L, size, size, s[2], 23, 2)
    out["snow"] = to_image("Cav Snow", c)

    # crystal: drawn on the LEFT half only and mirrored, which is the feature
    c = Canvas(size, size)
    cr = ramp_of(c, (108, 224, 232, 255), 6)
    L = c.layers[0]
    fill(L, cr[1], size, size)
    half = []
    for p in R.ellipse_box(2, 6, 31, 57, filled=True):
        half.append(p)
    for p in half:
        L.set(*p, cr[3])
        L.set(size - 1 - p[0], p[1], cr[3])
    facets = R.pixel_perfect(R.line(30, 8, 8, 34)) + R.pixel_perfect(R.line(8, 36, 30, 56))
    for p in facets:
        L.set(*p, cr[5])
        L.set(size - 1 - p[0], p[1], cr[5])
    out["crystal"] = to_image("Cav Crystal", c)

    c = Canvas(size, size)
    r = ramp_of(c, (72, 78, 96, 255), 5)
    L = c.layers[0]
    bricks(L, size, size, r[0], r[2], r[3], r[1], bw=21, bh=13)
    speckle(L, size, size, r[1], 11, 2)
    out["rock"] = to_image("Cav Rock", c)
    return out


def build_cavern(mats):
    B = _box
    B("Snow", (0, 0, -0.3), (36, 36, 0.6), mats["snow"])
    B("Ceiling", (0, 0, 8.4), (36, 36, 0.8), mats["rock"])
    for x in (-8.5, 8.5):
        B(f"Wall{x}", (x, 0, 4.0), (1.2, 36, 8.4), mats["ice"])
    B("WallBack", (0, 15, 4.0), (36, 1.2, 8.4), mats["ice"])
    for i, (x, y, h, s) in enumerate(((-5.5, 3.0, 7.6, 1.5), (5.8, 5.0, 8.0, 1.7),
                                      (-4.0, 10.5, 6.4, 1.2), (4.4, 12.0, 7.0, 1.3))):
        B(f"Col{i}", (x, y, h / 2), (s, s, h), mats["ice"])       # ice columns
    for i, (x, y, h, s) in enumerate(((-2.4, 2.0, 3.4, 0.8), (2.8, 1.2, 4.4, 1.0),
                                      (0.4, 6.5, 5.2, 1.1), (-3.6, 7.4, 2.6, 0.7),
                                      (3.8, 8.6, 3.0, 0.8), (-1.0, 11.0, 3.8, 0.9))):
        o = B(f"Crystal{i}", (x, y, h / 2), (s, s, h), mats["crystal"],
              emissive=True, strength=2.6)
        o.rotation_euler = (math.radians((x * 7) % 12 - 6), math.radians((y * 5) % 12 - 6),
                            math.radians((x * 31) % 90))
    for i, (x, y, h, s) in enumerate(((-6.8, 1.0, 2.2, 0.6), (6.4, 3.4, 2.6, 0.7),
                                      (-5.2, 13.0, 1.8, 0.5))):
        o = B(f"Stalag{i}", (x, y, h / 2), (s, s, h), mats["ice"])
    for i, (x, y, s) in enumerate(((-3.0, 4.4, 1.6), (3.4, 3.0, 1.9), (0.0, 9.0, 1.4))):
        B(f"Drift{i}", (x, y, 0.28), (s, s * 0.8, 0.55), mats["snow"])
    return "snow"


def light_cavern():
    for x, y, z in ((-2.4, 2.0, 2.4), (2.8, 1.2, 3.0), (0.4, 6.5, 3.6),
                    (-3.6, 7.4, 1.8), (3.8, 8.6, 2.0), (-1.0, 11.0, 2.6)):
        _point((x, y, z), (0.36, 0.92, 1.0), 900, 0.6)
    _sun((0.66, 0.82, 1.0), 4.2, (68, 0, 40))
    _world((0.06, 0.12, 0.20), 0.7)
    _fog(0.0042, (0.44, 0.72, 0.88))


def cam_cavern(t):
    e = _ease(t)
    a = math.radians(-100 + 34 * e)
    r = 18.0 - 5.4 * e
    return (math.cos(a) * r, math.sin(a) * r + 3.0, 5.6 - 2.0 * e), (0, 6.0, 2.6)


# ================================================================== utilities
def _ease(t):
    return t * t * (3 - 2 * t)


def _box(name, loc, scale, mat, emissive=False, strength=4.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.view_layer.objects.active
    o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bpy.ops.object.shade_flat()
    o.data.materials.append(mat if not emissive else _emissive_variant(mat, strength))
    return o


_EMIT_CACHE = {}


def _emissive_variant(mat, strength):
    key = (mat.name, round(strength, 2))
    if key in _EMIT_CACHE:
        return _EMIT_CACHE[key]
    m = mat.copy()
    m.name = f"{mat.name} Emit"
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    tex = next((n for n in nt.nodes if n.type == "TEX_IMAGE"), None)
    if tex:
        nt.links.new(tex.outputs["Color"], bsdf.inputs["Emission Color"])
    bsdf.inputs["Emission Strength"].default_value = strength
    _EMIT_CACHE[key] = m
    return m


def _sun(color, energy, rot_deg):
    li = bpy.data.lights.new("Sun", "SUN")
    li.color, li.energy, li.angle = color, energy, math.radians(2.5)
    o = bpy.data.objects.new("Sun", li)
    bpy.context.collection.objects.link(o)
    o.rotation_euler = tuple(math.radians(v) for v in rot_deg)
    return o


def _point(loc, color, energy, size):
    li = bpy.data.lights.new("P", "POINT")
    li.color, li.energy, li.shadow_soft_size = color, energy, size
    o = bpy.data.objects.new("P", li)
    bpy.context.collection.objects.link(o)
    o.location = loc
    return o


def _world(color, strength):
    w = bpy.data.worlds.new("W")
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs["Color"].default_value = (*color, 1)
    w.node_tree.nodes["Background"].inputs["Strength"].default_value = strength
    bpy.context.scene.world = w


def _fog(density, color, size=(70, 70, 26), centre=(0, 4, 9)):
    """Atmospheric haze as a BOUNDED box, never a world volume.

    A world volume in Cycles fills infinite space, so a sun is attenuated across
    the whole universe before it reaches anything. Measured: the same scene went
    from mean brightness 171/255 to near black just by adding world fog. A box
    around the set gives the same god-rays and costs nothing in exposure.
    """
    bpy.ops.mesh.primitive_cube_add(size=1, location=centre)
    o = bpy.context.view_layer.objects.active
    o.name = "FogVolume"
    o.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.visible_shadow = False
    o.visible_camera = True
    mat = bpy.data.materials.new("Fog")
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        if n.type != "OUTPUT_MATERIAL":
            nt.nodes.remove(n)
    vol = nt.nodes.new("ShaderNodeVolumeScatter")
    vol.inputs["Density"].default_value = density
    vol.inputs["Color"].default_value = (*color, 1)
    vol.inputs["Anisotropy"].default_value = 0.4
    nt.links.new(vol.outputs["Volume"], nt.nodes["Material Output"].inputs["Volume"])
    o.data.materials.append(mat)
    return o


ENVIRONMENTS = {
    "shrine": dict(title="Forest Shrine", showcase="Seamless tiling, verified",
                   tex=tex_shrine, build=build_shrine, light=light_shrine,
                   cam=cam_shrine, arch={"Ground", "Path"}, dens=(10.0, 26.0)),
    "corridor": dict(title="Sci-Fi Corridor", showcase="Generated shading ramps",
                     tex=tex_corridor, build=build_corridor, light=light_corridor,
                     cam=cam_corridor, arch={"Floor", "Ceiling", "Wall"},
                     dens=(11.0, 30.0)),
    "ruins": dict(title="Desert Ruins", showcase="Density zones",
                  tex=tex_ruins, build=build_ruins, light=light_ruins,
                  cam=cam_ruins, arch={"Sand", "Pillar", "Lintel", "Wall"},
                  dens=(9.0, 34.0)),
    "tavern": dict(title="Tavern Interior", showcase="Layers and palette swaps",
                   tex=tex_tavern, build=build_tavern, light=light_tavern,
                   cam=cam_tavern, arch={"Floor", "Ceiling", "Wall"},
                   dens=(12.0, 30.0)),
    "cavern": dict(title="Ice Cavern", showcase="Mirror symmetry",
                   tex=tex_cavern, build=build_cavern, light=light_cavern,
                   cam=cam_cavern, arch={"Snow", "Ceiling", "Wall", "Col"},
                   dens=(10.0, 28.0)),
}
