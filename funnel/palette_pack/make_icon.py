"""Render a pixel-art shaded sphere from one of the pack's own ramps.

  python funnel/palette_pack/make_icon.py

WHY THIS EXISTS. The design-critic's round-1 review of the cover returned one
FATAL and three SERIOUS, and two of the SERIOUS shared a single cause: the cover
was ~308x100px of empty charcoal in the lower left, and its swatch field "reads
as a generic palette export, not a pixel-art asset - like a Coolors swatch strip.
Nothing in the GRAPHIC confirms 'for pixel art in Blender'; only the text claims
it." In the game-assets/newest feed, next to real sprite crops, that is fatal to
the thing the cover is for.

A shaded sphere is the honest answer, not a decorative one. It is the canonical
demonstration of what a colour ramp is FOR: the eight steps are not eight
arbitrary colours, they are the shading of one material, and putting a light on a
ball is how you show that. So the icon is not an illustration added to fill
space - it is the product, used.

It is built as a real indexed canvas through Texel's own core (the same
`Canvas` the add-on paints on and the same `make_ramp` that generated the .gpl
files), out of the SHIPPED zip, then written out as pixels. No PIL drawing
primitives - those are banned for customer-facing art - just an indexed buffer
serialised to a PNG at integer nearest-neighbour scale.
"""
from __future__ import annotations

import pathlib
import types
import zipfile

from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
TEXEL = HERE.parents[1]
ADDON = TEXEL / "dist" / "texel-0.2.0.zip"

SIZE = 32          # canvas is 32x32 texels
SCALE = 5          # -> 160px, integer scale so every texel stays square
# RAMP MUST BE ONE OF THE EIGHT THE COVER ACTUALLY SHOWS. The first version used
# Copper, chosen because it "sits against the cover's ember band" - an aesthetic
# reason, not a correspondence one. The design-critic decoded the embedded data
# URI, extracted its eight hexes and diffed them against every swatch rendered in
# the cover's grid: ZERO matches. So the sphere and the chart were two unrelated
# things sharing a canvas, literally, by data - and the whole justification for
# drawing the sphere was that it demonstrates the pictured ramps. A demonstration
# of a ramp nobody can point at demonstrates nothing.
#
# Redbrick is row 8 of make_cover.py's HERO list, so a viewer can now put a
# finger on the swatch strip that shades the ball.
RAMP = "Redbrick"
BASE = (158, 84, 73, 255)     # must match build.py's Redbrick base


def shipped(mod: str):
    z = zipfile.ZipFile(ADDON)
    name = next(n for n in z.namelist() if n.endswith(f"core/{mod}.py"))
    m = types.ModuleType(f"shipped_{mod}")
    exec(compile(z.read(name).decode("utf8"), name, "exec"), m.__dict__)
    return m


canvas_mod = shipped("canvas")
tools = shipped("tools")

# The base must be the one build.py actually ships for this ramp, and the ramp
# must be one the cover pictures. Both are read from the real sources rather
# than trusted, because both drifted once already.
import json as _json
_facts = _json.loads((HERE / "facts.json").read_text(encoding="utf8"))
_entry = next((p for p in _facts["palettes"] if p["name"] == RAMP), None)
assert _entry, f"{RAMP} is not in the pack"
assert tuple(_entry["base"]) == BASE[:3], (
    f"BASE {BASE[:3]} does not match build.py's {tuple(_entry['base'])} for {RAMP}")
_cover_src = (HERE / "make_cover.py").read_text(encoding="utf8")
_hero = _cover_src.split("HERO = [", 1)[1].split("]", 1)[0]
assert f'"{RAMP}"' in _hero, (
    f"{RAMP} is not among the ramps the cover shows ({_hero.strip()}) - the "
    "sphere would demonstrate a ramp that is not on the cover")

ramp = tools.make_ramp(BASE, steps=8)
assert len(ramp) == 8
assert ["#%02x%02x%02x" % c[:3] for c in ramp] == _entry["colours"],     f"{RAMP} sphere colours differ from the shipped {RAMP.lower()}.gpl"

c = canvas_mod.Canvas(SIZE, SIZE)
for col in ramp:
    c.add_colour(col)                       # indices 1..8; 0 stays transparent
layer = c.layers[0]

# A lit sphere. Lambert against a light up and to the left, quantised into the
# ramp's eight steps - which is exactly the operation a ramp exists to serve.
cx = cy = (SIZE - 1) / 2.0
r = SIZE / 2.0 - 1.5
lx, ly, lz = -0.52, -0.62, 0.59             # light direction, normalised below
ln = (lx * lx + ly * ly + lz * lz) ** 0.5
lx, ly, lz = lx / ln, ly / ln, lz / ln

for y in range(SIZE):
    for x in range(SIZE):
        dx, dy = (x - cx) / r, (y - cy) / r
        d2 = dx * dx + dy * dy
        if d2 > 1.0:
            continue                        # outside the sphere: transparent
        nz = (1.0 - d2) ** 0.5              # surface normal z
        lam = dx * lx + dy * ly + nz * lz
        # a little ambient so the dark side still carries the ramp's darkest
        # steps rather than falling out of the silhouette entirely
        t = max(0.0, min(0.999, 0.18 + 0.86 * max(0.0, lam)))
        layer.px[y * SIZE + x] = 1 + int(t * 8)

used = sorted({v for v in layer.px if v})
assert len(used) >= 6, f"only {len(used)} of 8 ramp steps appear - reshade"
opaque = sum(1 for v in layer.px if v)
assert opaque > 0, "sphere is empty"
# The silhouette must be a circle, not a square: a square means the mask failed.
assert opaque < SIZE * SIZE * 0.85, "silhouette fills the canvas - mask broken"

img = Image.new("RGBA", (SIZE, SIZE))
px = img.load()
for y in range(SIZE):
    for x in range(SIZE):
        i = layer.px[y * SIZE + x]
        px[x, y] = c.palette[i] if i else (0, 0, 0, 0)

out = HERE / "icon_sphere.png"
img.resize((SIZE * SCALE, SIZE * SCALE), Image.NEAREST).save(out)
print(f"make_icon: wrote {out.name}  {SIZE * SCALE}x{SIZE * SCALE}")
print(f"  ramp {RAMP}, {len(used)} of 8 steps used, {opaque} opaque texels "
      f"of {SIZE * SIZE}")
print(f"  built from {ADDON.name} via core.canvas + core.tools")
