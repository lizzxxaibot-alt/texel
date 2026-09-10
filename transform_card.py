"""Build the v0.2.0 selection-transform marketing card. Not shipped.

Every panel on the card is produced by the SHIPPED code - `transform_region`
from `core.select`, the same function `texel.selection_transform` calls. A promo
image that demonstrates a private copy of the feature demonstrates nothing.

The sprite is not drawn here either: it is `promo/shots/dungeon/sprite/walk_02.png`,
one frame of the walk cycle Texel painted and exported for the launch video. So
the claim "made with Texel" is true of the art AND of the transform.

  python transform_card.py  ->  promo/transform/*.png + card.html
"""
from __future__ import annotations

import copy
import os

from PIL import Image

from core.canvas import Canvas
from core.select import Selection, transform_region

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "promo", "transform")
SRC = os.path.join(HERE, "promo", "shots", "dungeon", "sprite", "walk_02.png")

SIZE = 128          # the demo canvas, room for any of the transforms
WIN_W = WIN_H = 46  # the texel window each panel shows, identical on all four.
#                     Square, and only a little larger than the sprite: the
#                     upright pose is 24x40 and the rotated one is 40x24, so a
#                     square window lets BOTH fill their frame. It is also why
#                     the fourth panel demonstrates a HALF scale rather than a
#                     double - at 2x the window would have to be twice as big
#                     and the other three panels would shrink to a smudge that
#                     cannot be read in an itch feed thumbnail.
ZOOM = 5            # CSS px per texel. A whole number, so at the 2x render
#                     scale a texel is a whole number of device pixels and stays
#                     a hard square - the one thing this image must not get wrong


def load_sprite() -> tuple[Canvas, Selection]:
    """Import the walk frame into an indexed canvas, centred, and select it."""
    im = Image.open(SRC).convert("RGBA")
    px = list(im.getdata())
    w, h = im.size

    canvas = Canvas(SIZE, SIZE)
    layer = canvas.layers[0]
    ox, oy = (SIZE - w) // 2, (SIZE - h) // 2
    sel = Selection(SIZE, SIZE)
    pts = []
    for y in range(h):
        for x in range(w):
            rgba = px[y * w + x]
            if rgba[3] == 0:
                continue
            layer.set(ox + x, oy + y, canvas.add_colour(rgba))
            pts.append((ox + x, oy + y))
    # the selection is the sprite's own texels, not its bounding box - which is
    # the case the transformed mask exists for
    sel.add_points(pts)
    return canvas, sel


def write_png(canvas: Canvas, name: str, centre: tuple[int, int]) -> str:
    """Crop an identical window around the sprite's centre on every panel.

    Identical, because the panels are read side by side: if each were cropped to
    its own content the 2x scale would look the same size as the original and
    the one thing that panel exists to show would be invisible.
    """
    layer = canvas.layers[0]
    full = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    full.putdata([tuple(canvas.palette[i]) for i in layer.px])
    cx, cy = centre
    box = (cx - WIN_W // 2, cy - WIN_H // 2, cx - WIN_W // 2 + WIN_W,
           cy - WIN_H // 2 + WIN_H)
    path = os.path.join(OUT, f"{name}.png")
    full.crop(box).save(path)
    return path


PANELS = [
    ("original", None, 1.0, "Original", "a wand selection, not a box", False),
    ("flip_h", "FLIP_H", 1.0, "Flip X", "mirrored, same texels", False),
    ("rot_cw", "ROT_CW", 1.0, "Rotate CW", "the mask turns with it", True),
    ("scale", "SCALE", 0.5, "Scale ½×", "whole texels dropped, never blended", False),
]


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    base, base_sel = load_sprite()
    bx0, by0, bx1, by1 = base.layers[0].bounds()
    centre = ((bx0 + bx1 + 1) // 2, (by0 + by1 + 1) // 2)
    rows = []
    for name, mode, factor, label, sub, hero in PANELS:
        c, s = copy.deepcopy(base), copy.deepcopy(base_sel)
        if mode is None:
            n, w, h = s.count(), SIZE, SIZE
        else:
            n, w, h = transform_region(c.layers[0], s, mode, factor)
        write_png(c, name, centre)
        rows.append((name, label, sub, n, hero))
        print(f"  {name:9} {label:11} texels={n:5}  selection={s.count():5}  box={w}x{h}")

    html = TEMPLATE.replace("__PANELS__", "\n".join(
        PANEL.replace("__SRC__", f"{n}.png").replace("__LABEL__", lab)
             .replace("__SUB__", sub).replace("__N__", f"{cnt:,}")
             .replace("__HERO__", " hero" if hero else "")
        for n, lab, sub, cnt, hero in rows))
    path = os.path.join(OUT, "card.html")
    open(path, "w", encoding="utf-8").write(html)
    print(f"  -> {path}")


PANEL = """      <figure class="panel__HERO__">
        <div class="stage"><img src="__SRC__" alt="__LABEL__"></div>
        <figcaption><b>__LABEL__</b><i>__SUB__</i><u><b>__N__</b> texels</u></figcaption>
      </figure>"""

TEMPLATE = """<!doctype html><meta charset="utf-8">
<title>Texel 0.2.0 - selection transforms</title>
<style>
  @font-face{font-family:'YoungSerif';src:url('../../../../../brand/fonts/YoungSerif-Regular.ttf') format('truetype')}
  @font-face{font-family:'Inter';src:url('../../../../../brand/fonts/Inter.ttf') format('truetype')}
  /* Palette note: these are NOT from brand/tokens.json. They are the Texel
     product palette already fixed by gif/frame.html, which is what every other
     Texel promo frame renders in; matching that matters more here than matching
     the Mintworks token ramp, and drifting from it would be the actual defect.
     One accent only - the previous pass used --gold and --ember within 30 deg
     of each other, which at thumbnail size is one orange used four times and
     therefore no accent at all. */
  :root{
    --bg:#141317; --panel:#1e1d25; --line:rgba(242,230,200,.14);
    --text:#f2e6c8; --dim:#ab9f8a; --ember:#ff9c3f;
  }
  *{margin:0;padding:0;box-sizing:border-box}
  html,body{width:1280px;height:720px;overflow:hidden}
  body{background:var(--bg);color:var(--text);font-family:'Inter',sans-serif;
       -webkit-font-smoothing:antialiased}
  .card{width:1280px;height:720px;padding:44px 48px;display:flex;
        flex-direction:column;
        background:
          radial-gradient(1000px 480px at 80% -16%,rgba(255,156,63,.24),transparent 64%),
          var(--bg)}
  .head{display:flex;align-items:flex-end;justify-content:space-between}
  .kicker{font-size:13px;letter-spacing:.19em;text-transform:uppercase;
          color:var(--ember);font-weight:600}
  h1{font-family:'YoungSerif',Georgia,serif;font-size:42px;line-height:1.1;
     margin-top:12px;font-weight:400;letter-spacing:-.01em}
  h1 em{font-style:normal;color:var(--ember)}
  .meta{text-align:right;font-size:13px;color:var(--dim);line-height:1.8}
  .meta b{color:var(--text);font-weight:600;font-variant-numeric:tabular-nums}
  .row{margin-top:38px;display:flex;gap:20px}
  .panel{flex:1;background:var(--panel);border:1px solid var(--line);
         border-radius:10px;padding:16px 16px 14px;display:flex;
         flex-direction:column;align-items:center;position:relative}
  /* One deliberate break in the grid. Rotate is the panel carrying the claim
     that is hardest to build and easiest to get wrong - the MASK turning with
     the art - and it is also the one a stranger is most likely to read as a
     broken image. Marking it says the pose is on purpose. */
  .panel.hero{border-color:rgba(255,156,63,.55);
              box-shadow:0 0 0 1px rgba(255,156,63,.18) inset}
  .panel.hero::after{content:'THE HARD ONE';position:absolute;top:-8px;
         left:50%;transform:translateX(-50%);background:var(--ember);
         color:#171216;font-size:9.5px;font-weight:700;letter-spacing:.14em;
         padding:3px 9px;border-radius:99px}
  .stage{width:100%;height:290px;display:flex;align-items:center;
         justify-content:center;
         background-image:
           linear-gradient(45deg,rgba(242,230,200,.045) 25%,transparent 25%,transparent 75%,rgba(242,230,200,.045) 75%),
           linear-gradient(45deg,rgba(242,230,200,.045) 25%,transparent 25%,transparent 75%,rgba(242,230,200,.045) 75%);
         background-size:16px 16px;background-position:0 0,8px 8px;
         border-radius:6px}
  .stage img{width:__PW__px;height:__PH__px;image-rendering:pixelated}
  figcaption{margin-top:13px;text-align:center;line-height:1.45}
  figcaption b{display:block;font-size:17px;font-weight:600;color:var(--text)}
  figcaption i{display:block;font-style:normal;font-size:12.5px;color:var(--dim);
               margin-top:3px}
  figcaption u{display:block;text-decoration:none;font-size:12px;color:var(--dim);
               margin-top:6px;font-variant-numeric:tabular-nums;
               letter-spacing:.02em}
  figcaption u b{color:var(--text);font-weight:600}
  .foot{margin-top:auto;display:flex;align-items:center;
        justify-content:space-between;font-size:14.5px;color:var(--text)}
  .foot b{color:var(--text);font-weight:600}
  .foot .url{color:var(--dim);font-size:13px}
</style>
<div class="card">
  <div class="head">
    <div>
      <div class="kicker">Texel 0.2.0 &middot; shipped 9 Sep 2026</div>
      <h1>Flip, rotate and scale a selection.<br><em>Nearest neighbour</em>, nothing resampled.</h1>
    </div>
    <div class="meta">
      <div><b>95</b> operators</div>
      <div>Blender <b>4.2+</b></div>
      <div><b>$9.95</b> &middot; every update free</div>
    </div>
  </div>
  <div class="row">
__PANELS__
  </div>
  <div class="foot">
    <div>Every panel produced by <b>core.select.transform_region</b> &mdash; the shipped function, not a mock-up.</div>
    <div class="url">z3er1n.itch.io/texel</div>
  </div>
</div>
""".replace("__PW__", f"{WIN_W * ZOOM:g}").replace("__PH__", f"{WIN_H * ZOOM:g}")


if __name__ == "__main__":
    main()
