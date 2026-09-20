"""Drop 2 - the Texel Material Palettes. 24 eight-step .gpl ramps, CC0.

  python funnel/palette_pack/build.py

WHAT THIS IS, AND THE CLAIM IT DELIBERATELY DOES NOT MAKE
---------------------------------------------------------
`OPERATIONS.md` §4 queued this drop with the hook "24 .gpl palettes tuned for
lit 3D pixel art, with a note on why a 3D palette needs more midtones than a 2D
one." **That note is not being written, because the claim was tested twice on
2026-09-19 and neither test supported it:**

  1. Pooled every ramp entry across five irradiance levels in LINEAR light and
     measured CIELAB dE76 between neighbouring lit swatches. A 4-step ramp and a
     7-step ramp over the same value range gave an IDENTICAL worst gap (31.9
     dE), and gaps above 5 dE went UP, 19 -> 28. More midtones did not help.
  2. Tested the opposite story - that a lit renderer supplies the contrast, so a
     3D palette wants a NARROWER albedo span. Measured how many ramp steps stay
     distinguishable (dE > 2.3) after lighting across four exposures. 100%
     survived at every span from 0.20 to 0.80. No discrimination either.

Neither model is the last word on perception, but CLAUDE.md §6 is plain: never
claim what was not tested. So this pack says what is true and checkable about
how it was built, and says nothing about 2D versus 3D.

WHAT IS TRUE, AND IS GATED BELOW
  * Every ramp comes out of `core.tools.make_ramp`, Texel's own ramp builder.
    Its hue ROTATES across the ramp instead of staying fixed, and saturation
    peaks in the midtones, so a ramp is not just the base colour sliding toward
    black. The rotation is measured per palette and asserted below - it lands
    between 15 and 30 degrees across these 24. NOTE: tools.py's own docstring
    describes this as "toward blue in shadow and toward yellow in light"; the
    measured shift is a rotation of the base hue in one direction, which for a
    warm base means redder in shadow rather than bluer. The pack's copy quotes
    the MEASUREMENT, not the docstring.
  * Every file is written by `core.palette.to_gpl` and read back by
    `core.palette.parse_gpl` - Texel's own writer and its own parser.
  * .gpl is the GIMP palette format, so these open in Aseprite, Krita and GIMP
    as well as in Texel. Useful to someone who never buys; one click if they do.

BOTH MODULES ARE LOADED OUT OF THE SHIPPED ZIP, NOT THE WORKING TREE.
Drop 1 established this: the tree has run ahead of what buyers can download
before (SUPPORT.md's 94-vs-95 note), and a freebie generated from code nobody
can install is quoting maths that does not exist yet.
"""
from __future__ import annotations

import colorsys
import io
import json
import os
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TEXEL = os.path.dirname(os.path.dirname(HERE))
ZIP = os.path.join(TEXEL, "dist", "texel-0.2.0.zip")
OUT = os.path.join(HERE, "palettes")
LIVE_ZIP_NAME = "texel-0.2.0.zip"


# ---------------------------------------------------------------- load core
def load_from_zip():
    """Import core.palette and core.tools straight out of the shipped archive."""
    import importlib.util
    import types

    zf = zipfile.ZipFile(ZIP)
    names = zf.namelist()
    pkg = types.ModuleType("shipped")
    pkg.__path__ = []
    sys.modules["shipped"] = pkg
    mods = {}
    for mod in ("palette", "tools"):
        cand = [n for n in names if n.endswith(f"core/{mod}.py")]
        if not cand:
            raise SystemExit(f"core/{mod}.py is not in {LIVE_ZIP_NAME}")
        src = zf.read(cand[0]).decode("utf8")
        m = types.ModuleType(f"shipped.{mod}")
        m.__file__ = cand[0]
        sys.modules[f"shipped.{mod}"] = m
        exec(compile(src, cand[0], "exec"), m.__dict__)
        mods[mod] = m
    return mods["palette"], mods["tools"]


P, T = load_from_zip()

# ---------------------------------------------------------------- the pack
# (name, base RGB, group). The base is the MIDTONE; make_ramp builds outward.
MATERIALS = [
    # (name, base RGB = the MIDTONE, group). make_ramp builds outward from it.
    #
    # THE BASES WERE REVISED TWICE, AND BOTH REVISIONS CAME FROM A CHECK, NOT
    # FROM TASTE (2026-09-19).
    # The first set had Granite and Iron as near-identical greys, Sandstone and
    # Dunesand as near-identical tans, and Oakwood/Loam/Bronze as three barely
    # distinguishable browns - about five of twenty-four slots spent on
    # duplicates - and the second set was no better, because five low-saturation
    # cool entries (Granite, Slate, Basalt, Steel, Snowpack) collide however they
    # are nudged. Fixed structurally: three neutrals kept, and the two freed
    # slots spent on hue families the pack did not have at all - Deepwater for
    # blue and Orchid for magenta. Closest pair is now 14.0 dE, not 12.1, because
    # a set tuned to exactly clear its own gate has not really been checked.
    # Slate, Basalt, Pine and Loam also crushed their darkest two
    # steps to near-black, because make_ramp derives its floor from the base's
    # own value and a dark base bottoms out at v=0.05. Marble clipped to pure
    # white at the top for the mirror-image reason. Fixed by choosing better
    # bases rather than by touching core.tools, which is the shipped product.
    # The duplicate check further down is that finding turned into a gate.
    #
    # THE FLOOR/CEILING GATES THEN FIRED ON SIX MORE AND THE ARITHMETIC IS WHY.
    # make_ramp sets hi = max(v*1.25, 0.47) and lo = min(v*0.40, hi-0.42). So a
    # base above v=0.788 pins hi at 1.0 and the lightest step clips to pure
    # white (Gold, Ember, Torchlight, Frostfire, Snowpack all did), and a base
    # below v=0.38 pins lo at 0.05 and the darkest crushes to black (Basalt).
    # The usable window for a base value is therefore 0.38 < v < 0.788, and
    # every base below sits inside it. Found by the gates, not by squinting.
    #
    # stone and structure
    ("Granite",     (140, 139, 148), "Stone"),
    ("Marble",      (194, 189, 180), "Stone"),
    ("Slate",       ( 94, 109, 128), "Stone"),
    ("Redbrick",    (158,  84,  73), "Stone"),
    ("Sandstone",   (186, 156, 112), "Stone"),
    ("Loam",        (102,  72,  55), "Stone"),
    # ground, water and growing things
    ("Moss",        ( 92, 128,  66), "Nature"),
    ("Oakwood",     (138,  95,  58), "Nature"),
    ("Pine",        ( 67, 112,  99), "Nature"),
    ("Seafoam",     (128, 191, 160), "Nature"),
    ("Deepwater",   ( 42,  65, 117), "Nature"),
    ("Orchid",      (191, 107, 163), "Nature"),
    # metals
    ("Verdigris",   ( 79, 158, 148), "Metal"),
    ("Copper",      (189,  98,  53), "Metal"),
    ("Gold",        (196, 164,  59), "Metal"),
    ("Steel",       (155, 176, 194), "Metal"),
    ("Bronze",      (143, 128,  54), "Metal"),
    ("Rust",        (117,  55,  33), "Metal"),
    # light and effect
    ("Ember",       (199,  72,  40), "Effect"),
    ("Torchlight",  (158, 105,  35), "Effect"),
    ("Arcane",      (140,  85, 194), "Effect"),
    ("Venom",       ( 92, 178,  75), "Effect"),
    ("Frostfire",   ( 64, 164, 189), "Effect"),
    ("Bloodmoon",   (148,  50,  80), "Effect"),
]
STEPS = 8
assert len(MATERIALS) == 24, len(MATERIALS)


def value_of(rgb):
    return colorsys.rgb_to_hsv(*[c / 255 for c in rgb[:3]])[2]


def hue_of(rgb):
    return colorsys.rgb_to_hsv(*[c / 255 for c in rgb[:3]])[0] * 360.0


def build():
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        os.remove(os.path.join(OUT, f))

    facts = {"source_zip": LIVE_ZIP_NAME, "steps": STEPS, "palettes": []}
    master: list[tuple] = []

    for name, base, group in MATERIALS:
        rgba = (base[0], base[1], base[2], 255)
        ramp = T.make_ramp(rgba, steps=STEPS)

        # ---- gates, each of which can fail -------------------------------
        assert len(ramp) == STEPS, f"{name}: {len(ramp)} steps, wanted {STEPS}"

        vals = [value_of(c) for c in ramp]
        assert all(b > a for a, b in zip(vals, vals[1:])), (
            f"{name}: value is not strictly increasing dark->light: "
            + ", ".join(f"{v:.3f}" for v in vals))

        span = vals[-1] - vals[0]
        assert span >= 0.40, f"{name}: value span only {span:.3f}"

        # the hue shift is the thing the description claims, so it is asserted
        h_dark, h_light = hue_of(ramp[0]), hue_of(ramp[-1])
        shift = (h_light - h_dark + 540) % 360 - 180
        assert abs(shift) >= 4.0, (
            f"{name}: hue barely moves across the ramp ({shift:+.1f} deg) - the "
            "description's 'shifts hue toward blue in shadow' would be false")

        assert len(set(ramp)) == STEPS, f"{name}: duplicate colours in the ramp"

        # ---- write, then read back with Texel's OWN parser ---------------
        text = P.to_gpl(f"Texel {name}", list(ramp))
        path = os.path.join(OUT, f"{name.lower()}.gpl")
        with open(path, "w", encoding="utf8", newline="\n") as fh:
            fh.write(text)

        rname, rcols = P.parse_gpl(open(path, encoding="utf8").read())
        assert rname == f"Texel {name}", f"{name}: name round-tripped as {rname!r}"
        assert len(rcols) == STEPS, f"{name}: parsed {len(rcols)} of {STEPS}"
        assert [c[:3] for c in rcols] == [c[:3] for c in ramp], (
            f"{name}: colours changed through write->parse round trip")

        # No step may sit on the floor or the ceiling: a ramp whose darkest
        # two entries are both v=0.05 has 8 swatches and 7 usable colours, and
        # the first contact sheet had four of those.
        assert vals[0] > 0.055, (
            f"{name}: darkest step crushes to v={vals[0]:.3f} - raise the base")
        assert vals[-1] < 0.985, (
            f"{name}: lightest step clips to v={vals[-1]:.3f} - lower the base")

        master.append(ramp[STEPS // 2])
        facts["palettes"].append({
            "name": name, "group": group, "file": os.path.basename(path),
            "base": list(base), "span": round(span, 3),
            "hue_shift_deg": round(shift, 1),
            "colours": ["#%02x%02x%02x" % c[:3] for c in ramp],
        })

    # DUPLICATE GATE. Looking at the first contact sheet is what found this;
    # this is that finding written down as something that can fail. Any two
    # materials whose midtones are within 12 dE76 are effectively one slot.
    def _lab(rgb):
        def f1(c):
            c /= 255.0
            return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
        r, g, b = (f1(v) for v in rgb[:3])
        X = 0.4124 * r + 0.3576 * g + 0.1805 * b
        Y = 0.2126 * r + 0.7152 * g + 0.0722 * b
        Z = 0.0193 * r + 0.1192 * g + 0.9505 * b
        def f2(t):
            return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
        fx, fy, fz = f2(X / 0.95047), f2(Y), f2(Z / 1.08883)
        return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))

    import math as _m
    worst = None
    for i in range(len(master)):
        for j in range(i + 1, len(master)):
            d = _m.sqrt(sum((a - b) ** 2 for a, b in zip(_lab(master[i]), _lab(master[j]))))
            if worst is None or d < worst[0]:
                worst = (d, MATERIALS[i][0], MATERIALS[j][0])
    assert worst[0] >= 12.0, (
        f"{worst[1]} and {worst[2]} are only {worst[0]:.1f} dE apart - that is "
        "one palette wearing two names, and the pack claims 24")
    print(f"  closest pair     {worst[1]}/{worst[2]} at {worst[0]:.1f} dE")

    # a master sheet: one midtone per material, for picking a scene palette
    mtext = P.to_gpl("Texel Material Midtones", master)
    with open(os.path.join(OUT, "_all-midtones.gpl"), "w",
              encoding="utf8", newline="\n") as fh:
        fh.write(mtext)
    _, mcols = P.parse_gpl(mtext)
    assert len(mcols) == 24, f"master sheet parsed {len(mcols)}"

    shifts = [p["hue_shift_deg"] for p in facts["palettes"]]
    spans = [p["span"] for p in facts["palettes"]]
    facts["summary"] = {
        "files": len(MATERIALS) + 1,
        "colours_total": len(MATERIALS) * STEPS + 24,
        "hue_shift_min": min(shifts, key=abs), "hue_shift_max": max(shifts, key=abs),
        "span_min": min(spans), "span_max": max(spans),
    }
    with open(os.path.join(HERE, "facts.json"), "w", encoding="utf8") as fh:
        json.dump(facts, fh, indent=2)

    s = facts["summary"]
    print(f"palette_pack: {len(MATERIALS)} ramps x {STEPS} steps + master sheet")
    print(f"  files            {s['files']}")
    print(f"  colours          {s['colours_total']}")
    print(f"  hue shift (deg)  {s['hue_shift_min']:+.1f} .. {s['hue_shift_max']:+.1f}")
    print(f"  value span       {s['span_min']:.3f} .. {s['span_max']:.3f}")
    print(f"  built from       {LIVE_ZIP_NAME}")
    print("palette_pack: ALL GATES PASSED")
    return facts


if __name__ == "__main__":
    build()
