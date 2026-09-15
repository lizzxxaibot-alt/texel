"""Regenerate the nearest-neighbour half of the resample card using TEXEL'S OWN CODE.

Why this file exists (2026-09-14, `texel-marketing`):

`make_resample.py` generated BOTH halves with Pillow - `Image.NEAREST` on the
left, `Image.BILINEAR` on the right - and the card headed the left panel
"WHAT TEXEL DOES" while its footer disclosed only that the RIGHT side was
Pillow's. Every NUMBER on that panel was true of Texel's real output (103
texels, 11 colours, 0 off-palette, 0 soft-edge, all re-verified), but the
PIXELS were not Texel's: cropped to their bounding boxes the two images differ
in 71 of 216 texels, because nearest-neighbour sampling phase is an
implementation choice and Pillow makes a different one.

A panel labelled "WHAT TEXEL DOES" has to be what Texel does. This writes
`nn_half_texel.png` through `core.select.transform_region` - the shipped
function `texel.selection_transform` calls, the same one `transform_card.py`
used for the 0.2.0 card - so the label is true of the picture and not only of
the caption.

  python promo/transform/make_texel_half.py
"""
from __future__ import annotations

import json
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, ROOT)

from core.canvas import Canvas          # noqa: E402
from core.select import Selection, transform_region  # noqa: E402

SRC = os.path.join(HERE, "original.png")
OUT = os.path.join(HERE, "nn_half_texel.png")


def main() -> None:
    im = Image.open(SRC).convert("RGBA")
    w, h = im.size
    px = list(im.get_flattened_data())

    canvas = Canvas(w, h)
    layer = canvas.layers[0]
    sel = Selection(w, h)
    pts = []
    for y in range(h):
        for x in range(w):
            rgba = px[y * w + x]
            if rgba[3] == 0:
                continue
            layer.set(x, y, canvas.add_colour(rgba))
            pts.append((x, y))
    sel.add_points(pts)          # the sprite's own texels, not its bounding box

    n, bw, bh = transform_region(layer, sel, "SCALE", 0.5)

    full = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    full.putdata([tuple(canvas.palette[i]) for i in layer.px])

    # Crop the same 23x23 window the Pillow half occupies, centred on the
    # canvas, so the two panels stay directly comparable on the card.
    half = w // 2
    off = (w - half) // 2
    out = full.crop((off, off, off + half, off + half))
    out.save(OUT)

    src_pal = set(p for p in px if p[3] > 0)
    got = [p for p in out.get_flattened_data() if p[3] > 0]
    cols = set(got)
    facts = {
        "produced_by": "core.select.transform_region(mode='SCALE', factor=0.5)",
        "returned": {"texels": n, "box": [bw, bh]},
        "window": list(out.size),
        "texels": len(got),
        "colours": len(cols),
        "colours_not_in_palette": len(cols - src_pal),
        "partial_alpha_texels": len([p for p in out.get_flattened_data()
                                     if 0 < p[3] < 255]),
    }
    # --- the two display panels, cropped to ONE derived window -------------
    # design-critic round 1 (2026-09-14, SERIOUS): the sprite occupied ~19% of
    # the panel width, so at 380px feed width the nearest-vs-bilinear difference
    # - the thing the card exists to show - was a ~35px blob. The window below
    # is the UNION of both bounding boxes plus a 1px margin, so the pair stays
    # co-registered (the critic measured the registration and it is the one
    # thing that must not regress) while the dead horizontal margin goes.
    bl = Image.open(os.path.join(HERE, "bl_half.png")).convert("RGBA")
    assert bl.size == out.size, (bl.size, out.size)
    bx, by = out.getbbox(), bl.getbbox()
    x0 = max(0, min(bx[0], by[0]) - 1)
    y0 = max(0, min(bx[1], by[1]) - 1)
    x1 = min(out.width, max(bx[2], by[2]) + 1)
    y1 = min(out.height, max(bx[3], by[3]) + 1)
    win = (x0, y0, x1, y1)
    for im, name in ((out, "panel_nn.png"), (bl, "panel_bl.png")):
        before = len([q for q in im.get_flattened_data() if q[3] > 0])
        cropped = im.crop(win)
        after = len([q for q in cropped.get_flattened_data() if q[3] > 0])
        # A crop that silently eats texels would make the printed counts lie.
        assert before == after, (name, before, after)
        cropped.save(os.path.join(HERE, name))
    facts["panel_window"] = list(win)
    facts["panel_size"] = [x1 - x0, y1 - y0]

    # --- the left swatch strip, also from Texel's output --------------------
    # `make_resample.py` derived pal_nn.png from its Pillow NEAREST half. Same
    # 11 colours, but ordered by frequency, and the frequencies differ - so the
    # strip under a panel headed "WHAT TEXEL DOES" was still a Pillow artifact.
    # Same defect class as the sprite itself; fixed the same way.
    counts = {}
    for q in got:
        counts[q] = counts.get(q, 0) + 1
    ordered = [c for c, _ in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))]
    strip = Image.new("RGBA", (len(ordered), 1))
    strip.putdata(ordered)
    strip.save(os.path.join(HERE, "pal_nn_texel.png"))
    # The card prints "11 colours total" beside this strip; if they ever
    # disagree the strip is lying about the number next to it.
    assert len(ordered) == facts["colours"] == 11, (len(ordered), facts)
    facts["palette_strip"] = f"pal_nn_texel.png ({len(ordered)}x1)"

    print(json.dumps(facts, indent=2))
    # The card prints these four; if Texel ever stops satisfying them the
    # picture must not be built, rather than built and quietly wrong.
    assert facts["texels"] == 103, facts
    assert facts["colours"] == 11, facts
    assert facts["colours_not_in_palette"] == 0, facts
    assert facts["partial_alpha_texels"] == 0, facts
    print(f"  -> {OUT}")


if __name__ == "__main__":
    main()
