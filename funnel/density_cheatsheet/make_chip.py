"""Trim and scale the cover chip from render_chip.py's output.

  python funnel/density_cheatsheet/make_chip.py      (run from texel/)

History, because this file used to do something much worse. The chip began as a
CROP of promo/density/after.png, and this script keyed the Blender world grey
out of it, eroded the anti-aliased fringe and feathered the edges. That cleared
the design-critic's round-2 finding - a foreign rgb(63,63,63) sitting next to
brand colour - but not its round 3: after.png is the THREE-cube measurement
scene, and an opaque slice of the 3.2 m wall survived behind the 1.0 m crate,
fusing the sheet's 128 px reference and its 16 px reference into one silhouette.
No amount of keying fixes that; the wall is subject, not backdrop.

So the object is rendered alone now, on a transparent film, by render_chip.py.
There is nothing to key, nothing to erode and nothing to feather. This script
only trims to the silhouette and scales. The gates below are what stop a later
run quietly reintroducing a scene crop.
"""
import os

import numpy as np
from PIL import Image
from scipy.ndimage import label

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "chip_render.png")
OUT = os.path.join(HERE, "chip_crate.png")

SIDE = 312          # CSS 156px at render.mjs's 2x, so it draws 1:1 on device
MARGIN = 10         # breathing room around the silhouette, in output px

im = Image.open(SRC)
assert im.mode == "RGBA", f"{SRC} is {im.mode}; film_transparent must be on"
alpha = np.array(im)[..., 3]
assert alpha.max() == 255, "nothing opaque in the render"

# Trim to the silhouette, pad back to square, then scale - so the cube is
# centred and fills its box instead of floating in the render's own margin.
ys, xs = np.where(alpha > 8)
cut = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
side = max(cut.size)
sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
sq.paste(cut, ((side - cut.size[0]) // 2, (side - cut.size[1]) // 2))
inner = SIDE - 2 * MARGIN
chip = Image.new("RGBA", (SIDE, SIDE), (0, 0, 0, 0))
chip.paste(sq.resize((inner, inner), Image.LANCZOS), (MARGIN, MARGIN))

# --- gates -----------------------------------------------------------------
out = np.array(chip).astype(int)
oa = out[..., 3]

# 1. Empty corners. A crop out of a scene render would not have them.
corner = max(oa[0, 0], oa[0, -1], oa[-1, 0], oa[-1, -1])
assert corner == 0, f"corner alpha {corner} - is this a crop rather than a render?"

# 2. No flat neutral backdrop grey visible. Kept from the keying version purely
#    as a regression gate: if SRC is ever pointed back at a scene crop, this is
#    what catches it.
rgb = out[..., :3][oa > 24]
grey = ((np.abs(rgb - 63).max(axis=1) <= 7) &
        (rgb.max(axis=1) - rgb.min(axis=1) <= 4)).sum()
assert grey == 0, f"{grey} backdrop-grey pixels visible"

# 3. ONE connected silhouette, not two fused objects. This is the round-3
#    finding written down as a check that could fail.
_, n = label(oa > 24)
assert n == 1, f"{n} separate opaque shapes - the chip must show ONE object"

cover = (oa > 24).mean()
assert 0.35 < cover < 0.80, f"coverage {cover:.2f} - framing is wrong"

chip.save(OUT)
print(f"ok: chip_crate.png {SIDE}x{SIDE} RGBA")
print(f"  silhouettes: {n}   coverage: {cover * 100:.0f}%   corner alpha: {corner}")
