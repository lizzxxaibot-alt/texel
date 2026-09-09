"""Grade a render from render_bg.py into the itch page background. Tooling.

  python make_bg.py ruins_h3tall bg_ruins

itch serves the background at NATURAL SIZE on `div.game_page_wrapper`, anchored
`50% 0`, `attachment: fixed`, with an opaque 960px content column centred over
it. Three consequences drive everything here:

  * only the two margins are ever seen, and the column edges sit at exactly
    width/2 +- 480 on EVERY viewport width, because column and background are
    both centred. So a falloff baked at those columns tracks the real edge on
    every screen - which a screen-space CSS gradient could not do.
  * the vertical anchor is always the top, so the image is composed for its top
    ~950 rows and everything below that is bonus for taller windows.
  * `repeat` is on, so the top row and the bottom row are neighbours. They are
    both faded to the theme's own bg_color here, which makes that join
    invisible instead of the hard sky-meets-ground cut a 1440-tall version
    showed on 4K viewports.

Output is JPEG - itch re-signs a URL per size variant, and a 2400x2160 PNG of
this is 8 MB, a slow first paint for no visible gain on a backdrop.
"""
from __future__ import annotations

import os
import sys

from PIL import Image, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(HERE, "store", "theme", "_bg_src")
OUT_DIR = os.path.join(HERE, "store", "theme")

# The source is rendered 2880 tall; this window is the composed frame plus 720
# rows of extra floor beneath it. See render_bg.VARIANTS.
CROP = (0, 720, 2400, 2880)

BRIGHTNESS = 0.48
SATURATION = 0.68
TINT = (20, 16, 23)          # #141017, the theme's bg_color
TINT_MIX = 0.22

TOP_SHADE, TOP_SPAN = 1.00, 460      # px, fades down from the top edge
BOT_SHADE, BOT_SPAN = 1.00, 300      # px, fades up from the bottom edge

COLUMN_HALF = 480            # itch's content column is 960px wide, centred
EDGE_SHADE, EDGE_SPAN = 0.42, 320    # a soft shadow cast outward by the column

QUALITY = 88


def _ramp(size, stops):
    """An L mask from (position, alpha) stops, linearly interpolated."""
    m = Image.new("L", (size, 1), 0)
    px = m.load()
    stops = sorted(stops)
    for i in range(size):
        for (x0, a0), (x1, a1) in zip(stops, stops[1:]):
            if x0 <= i <= x1:
                t = 0 if x1 == x0 else (i - x0) / (x1 - x0)
                px[i, 0] = int(255 * (a0 + (a1 - a0) * t))
                break
    return m


def veil(im, mask_1d, vertical):
    """Composite the tint over `im` through a 1-D mask stretched to fill."""
    w, h = im.size
    mask = (mask_1d.rotate(-90, expand=True) if vertical else mask_1d).resize((w, h))
    return Image.composite(Image.new("RGB", im.size, TINT), im, mask)


def grade(im: Image.Image) -> Image.Image:
    im = ImageEnhance.Brightness(im.convert("RGB")).enhance(BRIGHTNESS)
    im = ImageEnhance.Color(im).enhance(SATURATION)
    im = Image.blend(im, Image.new("RGB", im.size, TINT), TINT_MIX)
    w, h = im.size

    # top and bottom, so the vertical repeat joins tint to tint
    im = veil(im, _ramp(h, [(0, TOP_SHADE), (TOP_SPAN, 0.0),
                            (h - 1 - BOT_SPAN, 0.0), (h - 1, BOT_SHADE)]), vertical=True)

    # a shadow under each column edge, strongest at the edge, fading outward
    mid = w // 2
    im = veil(im, _ramp(w, [
        (0, 0.0),
        (mid - COLUMN_HALF - EDGE_SPAN, 0.0), (mid - COLUMN_HALF, EDGE_SHADE),
        (mid + COLUMN_HALF, EDGE_SHADE), (mid + COLUMN_HALF + EDGE_SPAN, 0.0),
        (w - 1, 0.0)]), vertical=False)
    return im


def main() -> None:
    src = sys.argv[1] if len(sys.argv) > 1 else "ruins_h3tall"
    dst = sys.argv[2] if len(sys.argv) > 2 else "bg_ruins"
    path = os.path.join(SRC_DIR, src + ".png")
    if not os.path.exists(path):
        sys.exit(f"no such render: {path}")

    im = Image.open(path)
    if CROP[3] > im.size[1] or CROP[2] > im.size[0]:
        sys.exit(f"{src} is {im.size}, too small for crop {CROP}")
    im = grade(im.crop(CROP))

    out = os.path.join(OUT_DIR, dst + ".jpg")
    im.save(out, "JPEG", quality=QUALITY, optimize=True, progressive=True)

    # the repeat seam is the top row against the bottom row: report it, do not
    # claim it
    g = im.convert("L")
    w, h = im.size
    top = sum(g.getpixel((x, 0)) for x in range(0, w, 8)) / (w // 8)
    bot = sum(g.getpixel((x, h - 1)) for x in range(0, w, 8)) / (w // 8)
    mean = sum(g.getpixel((x, y)) for x in range(0, w, 16) for y in range(0, h, 16))
    mean /= (w // 16) * (h // 16)
    print(f"[bg] {os.path.basename(out)}  {w}x{h}  "
          f"{os.path.getsize(out) / 1024:.0f} KB  mean_luma={mean:.0f}/255  "
          f"repeat_seam: top={top:.1f} bottom={bot:.1f} delta={abs(top - bot):.1f}")


if __name__ == "__main__":
    main()
