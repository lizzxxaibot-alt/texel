"""The torchbearer scene, shared by the promo scripts. NOT part of the add-on.

Kept in one place so the exported GIF and the screen-capture video are provably
the same artwork - if they drifted apart, the advertisement would be showing a
workflow that produces something other than the result it claims.

Every drawing routine takes a cel and writes into it. Which cel belongs to which
track and frame is Texel's business, not this file's.
"""
from texel.core import raster as R
from texel.core import tools as TT

SIZE = 64
FLOOR = 46                      # y of the ground line, texels from the top
CX = 26                         # character centre column

# a teardrop: narrow where it meets the torch, bulging, then a point.
# (dy up from the base, half-width)
FLAME = ((0, 1), (-1, 2), (-2, 2), (-3, 3), (-4, 2), (-5, 2), (-6, 1), (-7, 0))
# stalactites at irregular x, so the ceiling reads as rock and not as a fence
TEETH = ((2, 5), (9, 8), (15, 3), (23, 7), (31, 4), (38, 9), (46, 5), (55, 7))
SCONCES = (7, 40)               # dead iron brackets along the wall

TRACKS = ("Cave", "Glow", "Main", "Torch")      # bottom to top


def palette(c):
    """Build every ramp with Texel's own generator and return the indices."""
    P = {}
    P["rock"] = [c.add_colour(x) for x in TT.make_ramp((78, 70, 96, 255), 5)]
    # the same rock, one and two steps into the torchlight. Painting the glow
    # as a SOLID ellipse would wipe the wall detail out; mapping each rock
    # colour to its warmed counterpart keeps every stone edge and just lights it
    P["lit1"] = [c.add_colour(x) for x in TT.make_ramp((122, 96, 96, 255), 5)]
    P["lit2"] = [c.add_colour(x) for x in TT.make_ramp((176, 134, 104, 255), 5)]
    P["cloak"] = [c.add_colour(x) for x in TT.make_ramp((146, 44, 58, 255), 5)]
    P["skin"] = [c.add_colour(x) for x in TT.make_ramp((216, 160, 120, 255), 4)]
    P["fire"] = [c.add_colour(x) for x in TT.make_ramp((250, 180, 56, 255), 5)]
    P["hair"] = c.add_colour((58, 40, 46, 255))
    P["wood"] = c.add_colour((102, 68, 40, 255))
    P["ink"] = c.add_colour((20, 16, 26, 255))
    P["W1"] = {P["rock"][i]: P["lit1"][i] for i in range(5)}
    P["W2"] = {P["rock"][i]: P["lit2"][i] for i in range(5)}
    return P


def pose(f):
    """Everything that changes per frame, in one place.

    The flicker runs on 4 and the walk on 8 - which is the whole argument for
    giving the flame its own track instead of redrawing the character.
    """
    bob = (0, -1, -1, 0, 0, -1, -1, 0)[f % 8]
    return dict(bob=bob,
                step=(0, 2, 3, 2, 0, -2, -3, -2)[f % 8],
                lick=(0, 2, 1, 3)[f % 4],
                drift=(f * 2) % 22,
                hy=18 + bob,
                tx=CX + 15,
                ty=18 + bob + 1 - (0, 2, 1, 3)[f % 4])


def fill(cel, pts, v):
    for p in pts:
        cel.set(*p, v)


def light(dst, src, box, table, dither=False):
    """Warm whatever the cave already put there, inside an ellipse.

    The dithered pass is what stops the torchlight reading as a hard brown
    ball: a checkerboard edge is how pixel art has always faked a gradient.
    """
    for x, y in R.ellipse_box(*box, filled=True):
        if dither and (x + y) % 2:
            continue
        v = table.get(src.get(x, y))
        if v:
            dst.set(x, y, v)


def draw_cave(bg, P, f):
    rock, p = P["rock"], pose(f)
    drift = p["drift"]
    fill(bg, R.rect(0, 0, SIZE - 1, SIZE - 1, filled=True), rock[1])
    fill(bg, R.rect(0, 0, SIZE - 1, 8, filled=True), rock[0])
    # a running-bond stone wall. Without courses to catch it, torchlight on a
    # flat wall just produces a flat brown circle.
    for row, wy in enumerate(range(9, FLOOR, 5)):
        fill(bg, R.line(0, wy, SIZE - 1, wy), rock[0])
        off = (row % 2) * 5 + drift
        for x in range(-11 + off, SIZE + 11, 11):
            fill(bg, R.rect(x, wy + 1, x, wy + 4, filled=True), rock[0])
            fill(bg, R.line(x + 1, wy + 1, x + 10, wy + 1), rock[2])
    for sx, d in TEETH:                       # stalactites, tapering
        for k in range(d):
            half = max(0, (d - k) // 3)
            fill(bg, R.rect(sx - half, 6 + k, sx + half, 6 + k),
                 rock[0] if k > d - 3 else rock[1])
    for sx in SCONCES:
        x0 = sx + drift - 11
        for rep in (0, 22, 44):
            fill(bg, R.rect(x0 + rep, 20, x0 + rep + 3, 21, filled=True), rock[0])
            fill(bg, R.rect(x0 + rep + 1, 22, x0 + rep + 2, 26, filled=True),
                 rock[0])
    fill(bg, R.rect(0, FLOOR, SIZE - 1, SIZE - 1, filled=True), rock[1])
    fill(bg, R.line(0, FLOOR, SIZE - 1, FLOOR), rock[2])
    for k, fy in enumerate((FLOOR + 5, FLOOR + 11)):      # flagstones
        fill(bg, R.line(0, fy, SIZE - 1, fy), rock[0])
        for x in range(-9 + (k % 2) * 7 + drift, SIZE + 9, 14):
            fill(bg, R.rect(x, fy - 4, x, fy - 1, filled=True), rock[0])
        fill(bg, R.line(0, fy + 1, SIZE - 1, fy + 1), rock[2])


def draw_glow(gl, bg, P, f):
    """The light the torch throws. Sits UNDER the character and warms the
    cave's own colours, so the stonework still reads through it."""
    p = pose(f)
    tx, lick = p["tx"], p["lick"]
    gy = (p["ty"] + FLOOR + 10) // 2          # the pool reaches the floor
    r1, r2 = 22 + lick, 13 + lick
    light(gl, bg, (tx - r1 - 3, gy - r1 - 2, tx + r1 + 3, gy + r1 + 2),
          P["W1"], dither=True)
    light(gl, bg, (tx - r1 + 3, gy - r1 + 3, tx + r1 - 3, gy + r1 - 3), P["W1"])
    light(gl, bg, (tx - r2 - 2, gy - r2 - 2, tx + r2 + 2, gy + r2 + 2),
          P["W2"], dither=True)
    light(gl, bg, (tx - r2 + 2, gy - r2 + 2, tx + r2 - 2, gy + r2 - 2), P["W2"])
    # he blocks the light: a contact shadow, thrown away from the torch
    fill(gl, R.ellipse_box(CX - 12, FLOOR + 1, CX + 3, FLOOR + 4, filled=True),
         P["rock"][0])


def draw_char(ch, P, f, outline=True):
    p = pose(f)
    hy, step = p["hy"], p["step"]
    cloak, skin, wood, hair, ink = (P["cloak"], P["skin"], P["wood"],
                                    P["hair"], P["ink"])
    back, front = CX - 5 + step, CX + step // 2
    for lx, leg in ((back, cloak[0]), (front, cloak[2])):
        fill(ch, R.rect(lx, hy + 20, lx + 3, hy + 25, filled=True), leg)
        fill(ch, R.rect(lx, hy + 26, lx + 4, hy + 27, filled=True), wood)
    fill(ch, R.rect(CX - 5, hy + 9, CX + 4, hy + 21, filled=True), cloak[1])
    fill(ch, R.rect(CX + 1, hy + 9, CX + 4, hy + 21, filled=True), cloak[2])
    fill(ch, R.line(CX - 5, hy + 10, CX - 5, hy + 20), cloak[0])
    fill(ch, R.rect(CX - 5, hy + 16, CX + 4, hy + 17, filled=True), wood)
    ch.set(CX + 4, hy + 16, P["fire"][3])                  # buckle catches light
    fill(ch, R.rect(CX + 3, hy + 10, CX + 8, hy + 12, filled=True), cloak[2])
    fill(ch, R.line(CX + 8, hy + 10, CX + 12, hy + 6), skin[2])
    fill(ch, R.line(CX + 8, hy + 11, CX + 12, hy + 7), skin[1])
    fill(ch, R.ellipse_box(CX - 4, hy, CX + 3, hy + 8, filled=True), skin[2])
    fill(ch, R.rect(CX + 1, hy + 3, CX + 3, hy + 7, filled=True), skin[1])
    fill(ch, R.ellipse_box(CX - 4, hy - 1, CX + 3, hy + 3, filled=True), hair)
    fill(ch, R.rect(CX - 5, hy + 1, CX - 3, hy + 6, filled=True), hair)
    ch.set(CX + 1, hy + 5, ink)                            # eye
    ch.set(CX + 3, hy + 6, skin[0])                        # jaw shadow
    fill(ch, R.line(CX + 11, hy + 5, CX + 15, hy + 1), wood)
    fill(ch, R.line(CX + 11, hy + 6, CX + 15, hy + 2), wood)
    if outline:
        fill(ch, TT.outline_points(ch), ink)


def draw_torch(fx, P, f):
    p = pose(f)
    tx, ty, fire = p["tx"], p["ty"], P["fire"]
    for dy, half in FLAME:
        fill(fx, R.rect(tx - half, ty + dy, tx + half, ty + dy), fire[2])
    for dy, half in FLAME[:5]:
        h = max(0, half - 1)
        fill(fx, R.rect(tx - h, ty + dy - 1, tx + h, ty + dy - 1), fire[3])
    fill(fx, R.rect(tx - 1, ty - 3, tx, ty - 1, filled=True), fire[4])
    for i, s in enumerate(((0, -10), (2, -12), (-2, -13))):    # embers
        if (f + i) % 3 == 0:
            fx.set(tx + s[0], ty + s[1], fire[3])


DRAW = {"Cave": lambda cels, P, f: draw_cave(cels["Cave"], P, f),
        "Glow": lambda cels, P, f: draw_glow(cels["Glow"], cels["Cave"], P, f),
        "Main": lambda cels, P, f: draw_char(cels["Main"], P, f),
        "Torch": lambda cels, P, f: draw_torch(cels["Torch"], P, f)}
