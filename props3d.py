"""The ten gallery props as REAL geometry wearing a staged texture atlas.

Not shipped. This replaces the half of `assets.py` that painted a single-view
sprite and let `record.py` hang it on an angled plane.

Why it is a rewrite rather than a swap: the old painters produce ONE view of an
object - a sword seen from the side, with transparency around it. That can only
ever go on a card. A model needs an atlas: every face of every part, laid out in
one image. So the painting itself had to change, not just what it lands on.

Each prop declares
    parts   - the boxes and lathes it is made of, each with a key
    stages  - (label, [part keys], painter) applied in order

The recorder allocates the atlas first, builds the model against it, then runs
the stages one at a time and diffs the canvas, so the video shows the atlas
filling in AND the model gaining it at the same moment. Nothing is faked: the
image on the left is the image on the model.

Two of the ten never needed this. grass-tile and brick-tile are tiles, and a
tile belongs on a cube - they were already right and are left alone.
"""
from __future__ import annotations
import math

from core import raster as R
import assets as A
import models3d as M


# --------------------------------------------------------------------------
# palette
# --------------------------------------------------------------------------
def palette(a: M.Atlas) -> dict:
    P = a.P
    P["wood"] = a.ramp((124, 82, 46, 255), 5)
    P["dark_wood"] = a.ramp((78, 50, 30, 255), 4)
    P["steel"] = a.ramp((176, 182, 196, 255), 5)
    P["gold"] = a.ramp((224, 176, 60, 255), 5)
    P["iron"] = a.ramp((92, 96, 108, 255), 4)
    P["glass"] = a.ramp((88, 172, 178, 255), 5)
    P["potion"] = a.ramp((206, 62, 92, 255), 4)
    P["cork"] = a.ramp((150, 112, 66, 255), 3)
    P["leather"] = a.ramp((96, 62, 36, 255), 4)
    P["stone"] = a.ramp((124, 120, 132, 255), 4)
    P["fire"] = a.ramp((255, 150, 40, 255), 5)
    P["ink"] = a.col((26, 22, 30, 255))
    return P


# --------------------------------------------------------------------------
# painters - each fills every face of one part
# --------------------------------------------------------------------------
def _all(a, rects, fn):
    for f in M._CORNERS:
        fn(rects[f])


def p_plank(a, rects, size):
    """Sawn timber: shaded, with a grain line and a darker end grain."""
    P = a.P
    _all(a, rects, lambda r: a.shade(r, P["wood"]))
    for f in ("FRONT", "BACK", "LEFT", "RIGHT"):
        r = rects[f]
        for y in range(1, r[3], 3):
            a.px(r, [(x, y) for x in range(r[2])], P["wood"][1])
    for f in ("TOP", "BOTTOM"):
        a.fill(rects[f], P["dark_wood"][2])


def p_crate_face(a, rects, size):
    """Crate boards plus the diagonal brace - the thing that says 'crate'."""
    P = a.P
    _all(a, rects, lambda r: a.shade(r, P["wood"]))
    for f in ("FRONT", "BACK", "LEFT", "RIGHT", "TOP"):
        r = rects[f]
        w, h = r[2], r[3]
        a.edge(r, P["dark_wood"][1])
        for p in R.line(1, 1, w - 2, h - 2):
            a.px(r, [p], P["dark_wood"][2])
        for p in R.line(w - 2, 1, 1, h - 2):
            a.px(r, [p], P["dark_wood"][2])
    a.fill(rects["BOTTOM"], P["dark_wood"][0])


def p_iron(a, rects, size):
    P = a.P
    _all(a, rects, lambda r: a.shade(r, P["iron"]))
    for f in ("FRONT", "BACK"):
        a.edge(rects[f], P["iron"][0], left=False, right=False)


def p_gold(a, rects, size):
    _all(a, rects, lambda r: a.shade(r, a.P["gold"]))


def p_blade(a, rects, size):
    """Form runs ACROSS a blade, not down it: bright fuller, dark bevels."""
    P = a.P
    _all(a, rects, lambda r: a.fill(r, P["steel"][3]))
    for f in ("FRONT", "BACK"):
        r = rects[f]
        w, h = r[2], r[3]
        a.px(r, [(0, y) for y in range(h)], P["steel"][1])
        a.px(r, [(w - 1, y) for y in range(h)], P["steel"][1])
        if w >= 3:
            a.px(r, [(w // 2, y) for y in range(h)], P["steel"][4])
    for f in ("LEFT", "RIGHT"):
        a.fill(rects[f], P["steel"][2])


def p_wrap(a, rects, size):
    P = a.P
    _all(a, rects, lambda r: a.shade(r, P["leather"]))
    for f in ("FRONT", "BACK", "LEFT", "RIGHT"):
        r = rects[f]
        for y in range(0, r[3], 2):
            a.px(r, [(x, y) for x in range(r[2])], P["leather"][0])


def p_glass(a, rects, size):
    """Empty glass: bright, with one highlight column."""
    P = a.P
    _all(a, rects, lambda r: a.shade(r, P["glass"]))
    for f in ("FRONT", "BACK", "LEFT", "RIGHT"):
        r = rects[f]
        a.px(r, [(1, y) for y in range(1, max(r[3] - 1, 2))], P["glass"][4])


def p_liquid(a, rects, size):
    """Fill the lower half with what is IN the bottle, and mark the surface."""
    P = a.P
    for f in ("FRONT", "BACK", "LEFT", "RIGHT"):
        r = rects[f]
        w, h = r[2], r[3]
        top = max(1, h // 3)
        for y in range(top, h):
            a.px(r, [(x, y) for x in range(w)], P["potion"][1])
        a.px(r, [(x, top) for x in range(w)], P["potion"][3])
        a.px(r, [(1, y) for y in range(top + 1, h - 1)], P["potion"][2])


def p_cork(a, rects, size):
    _all(a, rects, lambda r: a.shade(r, a.P["cork"]))


def p_coin(a, rects, size):
    """A struck face: rim, then a mark in the middle."""
    P = a.P
    _all(a, rects, lambda r: a.shade(r, P["gold"]))
    for f in ("FRONT", "BACK"):
        r = rects[f]
        w, h = r[2], r[3]
        a.edge(r, P["gold"][1])
        for p in R.ellipse_box(1, 1, w - 2, h - 2):
            a.px(r, [p], P["gold"][4])
        for p in R.line(w // 2, 2, w // 2, h - 3):
            a.px(r, [p], P["gold"][0])
        for p in R.line(2, h // 2, w - 3, h // 2):
            a.px(r, [p], P["gold"][0])


def p_milled(a, rects, size):
    """The reeded edge of a coin - the detail that only exists in 3D."""
    P = a.P
    for f in ("LEFT", "RIGHT", "TOP", "BOTTOM"):
        r = rects[f]
        a.fill(r, P["gold"][2])
        for x in range(0, r[2], 2):
            a.px(r, [(x, y) for y in range(r[3])], P["gold"][0])


def p_haft(a, rects, size):
    """A shaft has vertical grain. Plank banding makes it a barber pole."""
    P = a.P
    _all(a, rects, lambda r: a.shade(r, P["wood"]))
    for f in ("FRONT", "BACK", "LEFT", "RIGHT"):
        r = rects[f]
        for x in range(0, r[2], 2):
            a.px(r, [(x, y) for y in range(r[3])], P["wood"][1])


def p_flame(a, rects, size):
    _all(a, rects, lambda r: a.fill(r, a.P["fire"][3]))
    for f in ("FRONT", "BACK", "LEFT", "RIGHT"):
        r = rects[f]
        a.px(r, [(x, r[3] - 1) for x in range(r[2])], a.P["fire"][4])


def p_stone(a, rects, size):
    _all(a, rects, lambda r: a.shade(r, a.P["stone"]))


def p_door_panel(a, rects, size):
    """Vertical boards with iron studs down each edge."""
    P = a.P
    _all(a, rects, lambda r: a.shade(r, P["dark_wood"]))
    for f in ("FRONT", "BACK"):
        r = rects[f]
        w, h = r[2], r[3]
        for x in range(0, w, 3):
            a.px(r, [(x, y) for y in range(h)], P["wood"][1])
        for y in range(2, h - 1, 4):
            a.px(r, [(1, y), (w - 2, y)], P["iron"][3])


def p_lathe_stave(a, rects, size):
    """Barrel staves plus two iron hoops, painted into the lathe strip.

    A lathe gets ONE strip that wraps the whole surface, so the hoops are rows
    and the staves are columns - which is exactly what they are on a barrel.
    """
    P = a.P
    x, y, w, h = rects["SIDE"]
    for cx in range(w):
        for cy in range(h):
            t = cy / max(h - 1, 1)
            n = len(P["wood"])
            a.L.set(x + cx, y + cy, P["wood"][min(int((1 - abs(t - 0.5) * 2) * n), n - 1)])
    for cx in range(0, w, 3):                      # stave seams
        for cy in range(h):
            a.L.set(x + cx, y + cy, P["dark_wood"][1])
    for band in (int(h * 0.18), int(h * 0.19), int(h * 0.78), int(h * 0.79)):
        for cx in range(w):
            a.L.set(x + cx, y + band, P["iron"][3])


def p_lathe_lid(a, rects, size):
    P = a.P
    x, y, w, h = rects["SIDE"]
    for cx in range(w):
        for cy in range(h):
            a.L.set(x + cx, y + cy, P["dark_wood"][2])


# --------------------------------------------------------------------------
# the props: geometry, then the order it gets painted in
# --------------------------------------------------------------------------
# ("key", kind, args) - kind "box" is (size, offset, top) and "lathe" is
# (profile, sides, offset)
SPEC = {
    "sword": dict(atlas=64, height=31, parts=[
        ("blade_lo", "box", ((3, 1, 10), (0, 0, 15), None)),
        ("blade_hi", "box", ((2, 1, 7), (0, 0, 23.5), None)),
        ("tip", "box", ((1, 1, 2), (0, 0, 28), None)),
        ("guard", "box", ((8, 3, 2), (0, 0, 9), None)),
        ("grip", "box", ((2, 2, 6), (0, 0, 5), None)),
        ("pommel", "box", ((3, 3, 2), (0, 0, 1), None)),
    ], stages=[
        ("Blade", ["blade_lo", "blade_hi", "tip"], p_blade),
        ("Crossguard", ["guard"], p_gold),
        ("Bound grip", ["grip"], p_wrap),
        ("Pommel", ["pommel"], p_gold),
    ]),

    "crate": dict(atlas=64, height=10, parts=[
        ("body", "box", ((9, 9, 9), (0, 0, 4.5), None)),
        ("rail_t", "box", ((10, 10, 1), (0, 0, 8.6), None)),
        ("rail_b", "box", ((10, 10, 1), (0, 0, 0.4), None)),
    ], stages=[
        ("Boards", ["body"], p_plank),
        ("Brace", ["body"], p_crate_face),
        ("Rails", ["rail_t", "rail_b"], p_plank),
    ]),

    "chest": dict(atlas=96, height=11, parts=[
        ("base", "box", ((11, 8, 5), (0, 0, 2.5), None)),
        ("lid", "box", ((11, 8, 3), (0, 0, 6.5), None)),
        ("band", "box", ((2, 9, 8), (0, 0, 4), None)),
        ("lock", "box", ((3, 1, 3), (0, -4.3, 5.0), None)),
    ], stages=[
        ("Body", ["base"], p_plank),
        ("Lid", ["lid"], p_plank),
        ("Iron band", ["band"], p_iron),
        ("Lock", ["lock"], p_gold),
    ]),

    "potion": dict(atlas=96, height=16, parts=[
        ("base", "box", ((7, 7, 3), (0, 0, 1.5), None)),
        ("body", "box", ((8, 8, 5), (0, 0, 5.5), None)),
        ("shoulder", "box", ((6, 6, 2), (0, 0, 9), None)),
        ("neck", "box", ((3, 3, 3), (0, 0, 11.5), None)),
        ("cork", "box", ((4, 4, 2), (0, 0, 14), None)),
    ], stages=[
        ("Glass", ["base", "body", "shoulder", "neck"], p_glass),
        ("Contents", ["base", "body"], p_liquid),
        ("Cork", ["cork"], p_cork),
    ]),

    "coin": dict(atlas=64, height=10, turn=64, parts=[
        ("disc", "box", ((9, 3, 9), (0, 0, 4.5), None)),
        ("rim", "box", ((7, 4, 7), (0, 0, 4.5), None)),
    ], stages=[
        ("Blank", ["disc", "rim"], p_gold),
        ("Milled edge", ["disc"], p_milled),
        ("Struck face", ["rim"], p_coin),
    ]),

    "torch": dict(atlas=64, height=20, parts=[
        ("haft", "box", ((2, 2, 13), (0, 0, 6.5), None)),
        ("head", "box", ((3, 3, 4), (0, 0, 14.5), None)),
        ("flame_lo", "box", ((3, 3, 3), (0, 0, 18), None)),
        ("flame_hi", "box", ((2, 2, 3), (0, 0, 20.5), None)),
    ], stages=[
        ("Haft", ["haft"], p_haft),
        ("Binding", ["head"], p_wrap),
        ("Flame", ["flame_lo", "flame_hi"], p_flame),
    ]),

    # --- the two that had no model at all before ---
    "door": dict(atlas=96, height=28, parts=[
        ("panel", "box", ((10, 2, 22), (0, 0, 11), None)),
        ("jamb_l", "box", ((2, 4, 26), (-6, 0, 13), None)),
        ("jamb_r", "box", ((2, 4, 26), (6, 0, 13), None)),
        ("lintel", "box", ((14, 4, 2), (0, 0, 25), (10, 4))),
        ("arch", "box", ((10, 3, 2), (0, 0, 22.5), None)),
        ("handle", "box", ((1, 2, 2), (3, -1.6, 11), None)),
    ], stages=[
        ("Boards", ["panel"], p_door_panel),
        ("Frame", ["jamb_l", "jamb_r"], p_stone),
        ("Arch", ["lintel", "arch"], p_stone),
        ("Handle", ["handle"], p_iron),
    ]),

    "barrel": dict(atlas=96, height=17, parts=[
        ("body", "lathe", ([(0, 0), (5.5, 0), (6.5, 3), (6.5, 13), (5.5, 16),
                            (0, 16)], 12, (0, 0, 0))),
        ("lid", "lathe", ([(0, 0), (5.0, 0), (5.0, 1), (0, 1)], 12, (0, 0, 16))),
    ], stages=[
        ("Staves", ["body"], p_lathe_stave),
        ("Head", ["lid"], p_lathe_lid),
    ]),
}


# The two tiles run through the SAME recorder as the other eight so all ten
# share one camera, one light rig and one layout. They were already correct -
# canvas plus cube - but framed by a different script, and a contact sheet where
# two of ten cells sit differently is a defect even when each cell is right.
TILES = {
    "grass-tile": A.grass_tile,
    "brick-tile": A.brick_tile,
}

SIZES = (16, 24, 32, 48, 64, 96, 128, 192)


def allocate(kind: str):
    """Atlas + parts, UNPAINTED, plus a map of key -> rects for the painters.

    A tile short-circuits this: its canvas IS the texture, so there is one cube
    part and every face takes the whole image.

    The atlas size is found rather than declared: try each size in turn and take
    the first the packer fits into. A hand-picked 64 left the sword using 60x11
    of it, so the video showed a postage stamp of art in a sea of empty canvas -
    and a buyer would reasonably read that as the texture being mostly wasted.
    """
    if kind in TILES:
        a = M.Atlas(A.SIZE)
        palette(a)
        spec = {"height": 12, "turn": 26, "tile": True}
        parts = [M.tile_part(a, (12, 12, 12), (0, 0, 6))]
        return a, parts, {"tile": parts[0]["rects"]}, spec

    spec = SPEC[kind]
    for size in SIZES:
        a = M.Atlas(size)
        palette(a)
        parts, rects = [], {}
        try:
            for key, form, args in spec["parts"]:
                if form == "lathe":
                    profile, sides, offset = args
                    p = M.lathe(a, profile, sides, offset)
                else:
                    box, offset, top = args
                    p = M.part(a, box, offset, top=top)
                parts.append(p)
                rects[key] = p["rects"]
        except ValueError:
            continue                       # atlas full at this size, go bigger
        return a, parts, rects, spec
    raise ValueError(f"{kind}: does not fit any atlas up to {SIZES[-1]}")


def stages_for(a: M.Atlas, rects: dict, spec: dict, kind: str | None = None):
    """(label, thunk) pairs. Each thunk paints one stage into the atlas."""
    if kind in TILES:
        # assets.py's tile painters already return staged closures bound to a
        # canvas; they need no adapting, only the same canvas
        return TILES[kind](a.c)
    out = []
    for label, keys, painter in spec["stages"]:
        def step(keys=keys, painter=painter):
            for k in keys:
                painter(a, rects[k], None)
        out.append((label, step))
    return out
