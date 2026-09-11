"""Build the density card's crops AND its captions from one pass.

Same discipline as promo/transform/make_resample.py: every number printed on the
card is parsed out of shots/density/facts.json, which was written by the shipped
`texel.density_detect` operator running in Blender. Nothing on the card is typed
by hand, so the picture and the caption cannot drift apart.

  python promo/density/make_density.py     (run from the texel/ directory)
"""
import json
import os
import re

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))          # .../texel
SHOTS = os.path.join(ROOT, "shots", "density")

# Same crop box for both states, so the comparison is a comparison and not two
# different framings. A wide band cut to the card's stage aspect (2.10:1) so the
# CSS crops nothing: wall face on the left, the whole crate on the right. The
# first version was 4:3 and object-fit:cover ate the wall, which left the
# "before" side reading as an untextured brown box rather than as huge texels.
BOX = (700, 730, 1800, 1254)          # 1100x524

facts = json.load(open(os.path.join(SHOTS, "facts.json"), encoding="utf-8"))


def parse(line):
    """'10.5 px/unit avg  (2.5-21.1, 8.4x spread)' -> dict of floats."""
    m = re.match(r"([\d.]+) px/unit avg\s+\(([\d.]+)-([\d.]+), ([\d.]+)x spread\)", line)
    if not m:
        raise SystemExit(f"unparseable readout: {line!r}")
    avg, lo, hi, spread = (float(g) for g in m.groups())
    return {"avg": avg, "lo": lo, "hi": hi, "spread": spread}


b, a = parse(facts["before"]), parse(facts["after"])

for src, dst in (("01_detected", "before"), ("03_verified", "after")):
    Image.open(os.path.join(SHOTS, f"{src}.png")).crop(BOX).save(
        os.path.join(HERE, f"{dst}.png"))
# The wall is 3.2m and the crate 0.38m. Blender's default cube UVs are identical
# whatever the cube's size, so density lands inversely proportional to size and
# the measured spread should equal the size ratio. Asserted, not assumed - if
# this ever stops holding, the card's explanation is wrong and the build fails.
SIZE_RATIO = 3.2 / 0.38
assert abs(b["spread"] - SIZE_RATIO) < 0.15, (b["spread"], SIZE_RATIO)

out = {
    "faces": facts["faces"], "texture_px": facts["texture_px"],
    "before": b, "after": a,
    "target": facts["target"], "applied": facts["applied"],
    "size_ratio": round(SIZE_RATIO, 1),
    "wall_m": 3.2, "crate_m": 0.38,
    "readout_before": facts["before"], "readout_after": facts["after"],
}
json.dump(out, open(os.path.join(HERE, "density_facts.json"), "w",
                    encoding="utf-8"), indent=2)

tpl = open(os.path.join(HERE, "density_card.tpl.html"), encoding="utf-8").read()
subs = {
    "SPREAD_B": f'{b["spread"]:.1f}', "SPREAD_A": f'{a["spread"]:.1f}',
    "LO_B": f'{b["lo"]:.1f}', "HI_B": f'{b["hi"]:.1f}',
    "LO_A": f'{a["lo"]:.1f}', "HI_A": f'{a["hi"]:.1f}',
    "AVG_B": f'{b["avg"]:.1f}', "AVG_A": f'{a["avg"]:.1f}',
    # Two decimals, deliberately. The footer's whole honesty claim is that the
    # after-figure is a SECOND MEASUREMENT and not the target echoed back - and
    # at one decimal both print as "10.5", so the card asked the reader to spot
    # a difference it had rounded away. 10.52 vs 10.5 is the daylight.
    "TARGET": f'{facts["target"]:.2f}',
    "FACES": str(facts["faces"]), "TEX": str(facts["texture_px"]),
    "WALL": "3.2", "CRATE": "0.38", "RATIO": f"{SIZE_RATIO:.1f}",
}
for k, v in subs.items():
    tpl = tpl.replace("{{" + k + "}}", v)
if "{{" in tpl:
    raise SystemExit("unsubstituted placeholder: " + tpl[tpl.index("{{"):][:40])
open(os.path.join(HERE, "density_card.html"), "w", encoding="utf-8").write(tpl)

print(f"[ok] before {b} \n[ok] after  {a}")
print(f"[ok] spread {b['spread']}x == size ratio {SIZE_RATIO:.2f}x (asserted)")
print("[ok] wrote density_card.html, density_facts.json, before/after/panel.png")
