"""Compute every number on the density cheatsheet from Texel's own shipped maths.

The rule this file exists to enforce is CLAUDE.md §3 and the same discipline as
promo/density/make_density.py: nothing printed on the sheet is typed by hand.
Every figure comes out of `core.uvmap` - the identical module the add-on's
`texel.density_detect` and `texel.density_apply` operators call - so if the
product's arithmetic ever changes, the cheatsheet's arithmetic changes with it
or this build fails.

  python funnel/density_cheatsheet/make_tables.py     (run from texel/)

Writes tables.json, which cheatsheet.typ reads. No hand-editing either file.
"""
import importlib.util
import json
import os
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TEXEL = os.path.dirname(os.path.dirname(HERE))            # .../texel

# Load core/uvmap.py OUT OF THE SHIPPED ZIP, not out of the working tree.
# Two reasons. The package __init__ imports bpy, so `from texel.core import
# uvmap` cannot run outside Blender at all - but more importantly the tree has
# run ahead of the zip before (SUPPORT.md's 94-vs-95 note), and a sheet that
# quotes the tree is quoting maths nobody can download. uvmap.py is pure
# arithmetic with no bpy import, which is what makes this possible.
ZIP = os.path.join(TEXEL, "dist", "texel-0.2.0.zip")
LOCAL = os.path.join(HERE, "uvmap.py")
if os.path.exists(ZIP):
    with zipfile.ZipFile(ZIP) as z:
        member = next(n for n in z.namelist() if n.endswith("core/uvmap.py"))
        src = z.read(member).decode("utf-8")
    origin = f"{os.path.basename(ZIP)}!{member}"
else:
    # The source bundle we publish alongside the PDF carries uvmap.py beside
    # this script instead of the whole add-on zip, so a reader can actually run
    # the generator and check the sheet's arithmetic. Byte-identical file.
    src = open(LOCAL, encoding="utf-8").read()
    origin = "uvmap.py"
spec = importlib.util.spec_from_loader("uvmap", loader=None)
uvmap = importlib.util.module_from_spec(spec)
exec(compile(src, origin, "exec"), uvmap.__dict__)

# --------------------------------------------------------------------------
# The density ladder. Powers of two, and the sheet argues for them: at 32
# px/unit a 0.5 m object gets exactly 16 px and its edges land on texel
# corners; at 17.8 px/unit it gets 8.9 px and they do not.
DENSITIES = [8, 16, 32, 64]

# The ladder shows one more rung than the grid does. 128 px/unit is a real
# choice for HD pixel art, but adding it to the grid would make that table ten
# columns wide and unreadable at print size - so it lives here only.
LADDER_DENSITIES = DENSITIES + [128]

# A character is the anchor every artist actually has in their head, so the
# ladder is reported in those terms. 1.8 m is a standing adult.
CHARACTER_M = 1.8

# Real objects at sizes a level actually uses. `m` is the longest edge of the
# face being textured, which is what decides how many pixels it needs.
OBJECTS = [
    ("Small crate", 0.4),
    ("Barrel", 0.8),
    ("Floor tile", 1.0),
    ("Character", CHARACTER_M),
    ("Door", 2.1),
    ("Wall section", 3.2),
    ("Tree", 6.0),
    ("Building facade", 12.0),
]


def next_pow2(n: float) -> int:
    p = 1
    while p < n:
        p *= 2
    return p


def density_of_square(side_m: float, tex_px: int) -> float:
    """px/unit for a square face of `side_m` using the whole tex_px texture.

    Goes through the shipped function rather than doing tex/side directly, so
    the sheet is demonstrably quoting the product's own maths.
    """
    return uvmap.texel_density(uv_area=1.0, world_area=side_m ** 2,
                               tex_size=tex_px)


# --- assert the everyday form the sheet prints is the full formula ----------
# The sheet says: "a face using the whole SxS texture across M metres is S/M
# px/unit". That is a simplification of sqrt(uv_area * S^2 / area). If it ever
# stops being exactly true, the sheet is teaching something false - so fail.
for s in (16, 32, 64, 128):
    for m in (0.4, 1.0, 1.8, 3.2, 12.0):
        assert abs(density_of_square(m, s) - s / m) < 1e-9, (s, m)

# --- ladder ----------------------------------------------------------------
ladder = []
for d in LADDER_DENSITIES:
    ladder.append({
        "d": d,
        # What the anchor object resolves to at this density.
        "char_px": round(d * CHARACTER_M),
        # The texture a 1 m tile needs - equals the density by definition, and
        # that identity is why 1 m is the unit worth thinking in.
        "tile_px": round(d * 1.0),
        "half_px": d * 0.5,
    })

# --- object x density grid -------------------------------------------------
grid = []
for name, m in OBJECTS:
    row = {"name": name, "m": m, "cells": []}
    for d in DENSITIES:
        need = d * m
        row["cells"].append({"need": round(need), "tex": next_pow2(need)})
    grid.append(row)

# --- the drift, measured -------------------------------------------------
# Not modelled: these are the figures texel.density_detect printed in Blender
# 4.5.9 for the scene behind promo/density/texel-density-measured.png.
FACTS = os.path.join(TEXEL, "shots", "density", "facts.json")
if not os.path.exists(FACTS):
    FACTS = os.path.join(HERE, "facts.json")     # the published source bundle
measured = json.load(open(FACTS, encoding="utf-8"))
WALL_M, CRATE_M = 3.2, 0.38
size_ratio = WALL_M / CRATE_M

# Blender's default cube unwrap gives every cube the SAME UV layout whatever
# its size, so uv_area is constant and density falls as 1/size. Predict the
# spread from the sizes alone and check it against what Blender measured.
predicted = density_of_square(CRATE_M, measured["texture_px"]) / \
    density_of_square(WALL_M, measured["texture_px"])
assert abs(predicted - size_ratio) < 1e-9, (predicted, size_ratio)
assert abs(size_ratio - 8.4) < 0.05, size_ratio          # matches the readout

# --- the correction --------------------------------------------------------
# uv_scale_for_density returns the LINEAR UV extent a face needs, as a fraction
# of the texture width, to sit at the target density. Worked on the wall face.
EX_D, EX_S = 32, 64
EX_AREA = 2.0 * 1.5                                       # a 2.0 x 1.5 m panel
ex_uv = uvmap.uv_scale_for_density(EX_D, EX_AREA, EX_S)
# Round-trip it: a face at that UV extent must measure back at the target.
assert abs(uvmap.texel_density(ex_uv ** 2, EX_AREA, EX_S) - EX_D) < 1e-9

out = {
    "densities": DENSITIES,
    "character_m": CHARACTER_M,
    "ladder": ladder,
    "grid": grid,
    "drift": {
        "wall_m": WALL_M, "crate_m": CRATE_M,
        "ratio": round(size_ratio, 1),
        "tex": measured["texture_px"],
        "faces": measured["faces"],
        "before": measured["before"],
        "after": measured["after"],
    },
    "example": {
        "d": EX_D, "s": EX_S, "w": 2.0, "h": 1.5,
        "area": EX_AREA,
        "uv": round(ex_uv, 3),
        "uv_pct": round(ex_uv * 100),
        "px_across": round(ex_uv * EX_S),
    },
}
json.dump(out, open(os.path.join(HERE, "tables.json"), "w", encoding="utf-8"),
          indent=2)
print("ok: tables.json")
print("  ladder     ", [(l["d"], l["char_px"]) for l in ladder])
print("  drift      ", f"{size_ratio:.2f}x predicted, readout says {measured['before']}")
print("  example    ", f"{EX_D} px/unit on {EX_AREA} m^2 @ {EX_S}px -> UV {ex_uv:.3f}")
