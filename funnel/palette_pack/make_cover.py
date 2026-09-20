"""Generate the itch cover for the Material Palettes drop, from facts.json.

  python funnel/palette_pack/make_cover.py

The swatches on the cover ARE the palettes in the download - every hex is read
out of facts.json, which build.py writes from the .gpl files it just gated. So
the cover physically cannot advertise a colour the pack does not contain, and
the "24" cannot drift from the file count. Same discipline as drop 1's cover,
which took its three texture sizes out of tables.json.

Writes brand/html/itch_cover_palettes.html. Edit THIS template, never the
generated file.
"""
from __future__ import annotations

import base64
import json
import os

import pathlib
HERE = pathlib.Path(os.path.abspath(__file__)).parent
TEXEL = HERE.parents[1]
ROOT = TEXEL.parents[2]
OUT = os.path.join(ROOT, "brand", "html", "itch_cover_palettes.html")

facts = json.load(open(HERE / "facts.json", encoding="utf8"))
pals = facts["palettes"]
n = len(pals)
steps = facts["steps"]

# Eight ramps for the hero, chosen to span the pack's hue range rather than to
# be the prettiest eight - the cover should represent what is in the zip.
HERO = ["Ember", "Gold", "Moss", "Verdigris", "Frostfire", "Deepwater",
        "Arcane", "Redbrick"]
by_name = {p["name"]: p for p in pals}
missing = [h for h in HERO if h not in by_name]
assert not missing, f"cover names a palette the pack does not have: {missing}"

rows = []
for name in HERO:
    cells = "".join(f'<i style="background:{c}"></i>' for c in by_name[name]["colours"])
    # No per-ramp label. Round 1 carried one and the lint caught it colliding
    # with the subhead ("FROSTFIRE" ghosting behind "Effect."); it also flagged
    # them among 17 elements dropping under 8px at the 300px thumbnail, which is
    # where most listing impressions happen. An unreadable label that breaks the
    # headline is a straight loss, so the colour field gets the space instead.
    rows.append(f'<div class="ramp"><div class="cells">{cells}</div></div>')
ramp_html = "\n      ".join(rows)

# Embedded as a data URI rather than referenced by path: the HTML is written into
# brand/html/ but the icon lives beside this generator, and a render that depends
# on a relative hop between the two is a silent-failure waiting to happen - a
# missing <img> just renders as nothing and the gap looks deliberate.
ICON = HERE / "icon_sphere.png"
assert ICON.exists(), "run make_icon.py first - the cover needs the sphere"
icon_b64 = base64.b64encode(ICON.read_bytes()).decode("ascii")
icon_ramp = (HERE / "make_icon.py").read_text(encoding="utf8")     .split('RAMP = "', 1)[1].split('"', 1)[0]
assert icon_ramp in [p["name"] for p in pals], icon_ramp

groups = []
seen = []
for p in pals:
    if p["group"] not in seen:
        seen.append(p["group"])
half = (len(seen) + 1) // 2
groups_a = " · ".join(seen[:half])
groups_b = " · ".join(seen[half:])
groups = " · ".join(seen)

HTML = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="_fonts.css">
<style>
  /* Texel Material Palettes - itch.io cover, 630x500 (shown ~315x250 in grid).

     GENERATED from funnel/palette_pack/make_cover.py. Every swatch hex comes
     out of facts.json, so the cover cannot show a colour the download lacks.
     Edit the generator, not this file.

     SIBLING OF brand/html/itch_cover_texel.html and the density cheatsheet
     cover: same ember/gold band, same charcoal ground, same closing spec bar.
     Those variables are inherited verbatim from those two covers rather than
     invented here - the band is what reads "tool family, not another pack" at
     315px.

     WHAT DIFFERS: the hero. The cheatsheet led with three numbers because a
     reference sheet's promise is the answer it saves you working out. A palette
     pack's promise is the colour itself, so the colour IS the hero - eight real
     ramps straight out of the zip. At thumbnail size a field of saturated colour
     is the one thing that survives.

     (An earlier version of this comment claimed the grid was "bled off the right
     edge" as a deliberate device. It was not a device, it was a hard crop, the
     critic called it FATAL, and the grid now keeps the same 32px margin as
     everything else. The comment is corrected rather than deleted because a
     confident false comment is how the next reader repeats the mistake.)
  */
  :root {{
    --char:#141317; --char2:#1d1c22; --cream:#f2e6c8;
    --ember:#ff9c3f; --ember-d:#c96a24; --gold:#e7b23a; --quiet:#a89d89;
    --hero:#fff8ec;
  }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ width:630px; height:500px; overflow:hidden; }}
  .stage {{ position:relative; width:630px; height:500px; overflow:hidden;
    background:
      radial-gradient(560px 340px at 14% 14%, rgba(255,156,63,.16), transparent 62%),
      radial-gradient(460px 320px at 96% 92%, rgba(231,178,58,.10), transparent 60%),
      linear-gradient(168deg, var(--char2), var(--char) 72%); }}
  .grain {{ position:absolute; inset:0; opacity:.4; pointer-events:none;
    mix-blend-mode:overlay;
    background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2'/%3E%3C/filter%3E%3Crect width='200' height='200' filter='url(%23n)' opacity='0.5'/%3E%3C/svg%3E"); }}

  .bar {{ position:absolute; left:0; right:0; top:0; height:52px; z-index:7;
    background:linear-gradient(90deg, var(--ember), var(--gold));
    display:flex; align-items:center; justify-content:space-between;
    padding:0 32px;
    font:16px/1 'PlexMonoBold', ui-monospace, monospace; letter-spacing:.15em;
    color:var(--char); text-transform:uppercase; }}

  .head {{ position:absolute; left:32px; top:76px; z-index:6; width:258px; }}
   /* 14px, not 16: narrowing .head to 258px to clear the ramp grid made the
     24-character kicker wrap and strand "BLENDER" on a line of its own. Shrinking
     the type keeps the whole phrase on one line, which is what it is for. */
  .kicker {{ font:14px/1 'PlexMonoBold', ui-monospace, monospace; color:var(--ember);
    letter-spacing:.14em; text-transform:uppercase; white-space:nowrap; }}
  .name {{ margin-top:12px; font:54px/.94 'YoungSerif', Georgia, serif;
    color:var(--hero); letter-spacing:.004em;
    text-shadow: 0 4px 0 rgba(0,0,0,.5), 0 14px 30px rgba(0,0,0,.6); }}
  .name em {{ font-style:normal; color:var(--ember); }}
  .sub {{ margin-top:16px; font:16px/1.4 'PlexMono', ui-monospace, monospace;
    color:var(--cream); letter-spacing:.02em; }}

  /* the hero: eight real ramps from the download */
  /* right:32px, NOT right:0. Round 1 ran the ramps off the canvas edge and the
     critic returned FATAL: with no vignette and no partial cell, a hard vertical
     cut at x=630 is indistinguishable from an export bug, and it was also the
     only element in the layout ignoring the 32px margin that .bar, .head and
     .spec all keep. The "fragment of something larger" idea was in the comment
     and not in the pixels. */
  .grid {{ position:absolute; right:32px; top:100px; z-index:5;
    display:flex; flex-direction:column; gap:8px; }}
  .ramp {{ display:flex; align-items:center; gap:12px; }}
  .cells {{ display:flex; box-shadow:0 6px 18px rgba(0,0,0,.45); }}
  .cells i {{ display:block; width:36px; height:36px; }}

  /* The lower-left void was ~308x100px of bare charcoal, and the critic tied it
     to a second defect: the flat swatch field "reads as a generic palette
     export, not a pixel-art asset". One object fixes both. This sphere is a real
     32x32 indexed canvas shaded with the pack's own {icon_ramp} ramp through
     Texel's core (make_icon.py) - the product demonstrated, not an ornament, and
     rendered at an integer scale so the texels stay square.

     The ramp name above is INTERPOLATED, not typed. It said "Copper" for a whole
     round after RAMP became Redbrick, because the hexes were gated and the prose
     describing them was not - the same stale-comment failure this file had
     already corrected once, reproduced three lines away. */
  .icon {{ position:absolute; left:32px; bottom:76px; z-index:6; width:136px;
    height:136px; image-rendering:pixelated;
    filter:drop-shadow(0 10px 18px rgba(0,0,0,.55)); }}
  .spec {{ position:absolute; left:0; right:0; bottom:0; height:44px; z-index:7;
    background:rgba(0,0,0,.42); border-top:1px solid rgba(255,156,63,.28);
    display:flex; align-items:center; justify-content:space-between;
    padding:0 32px;
    font:13px/1 'PlexMono', ui-monospace, monospace; color:var(--quiet);
    letter-spacing:.12em; text-transform:uppercase; }}
  .spec b {{ color:var(--cream); font-weight:400; }}
</style>
</head>
<body>
  <div class="stage">
    <div class="bar"><span>Free</span><span>CC0 &middot; .gpl</span></div>

    <div class="head">
      <div class="kicker">For pixel art in Blender</div>
      <div class="name">Material<br><em>Palettes</em></div>
      <div class="sub">{n} ramps, {steps} steps each.<br>{groups_a} &middot;<br>{groups_b}.</div>
    </div>

    <img class="icon" alt="" src="data:image/png;base64,{icon_b64}">

    <div class="grid">
      {ramp_html}
    </div>

    <div class="spec">
      <span>Pixelkiln</span>
      <span><b>{n * steps}</b> colours</span>
      <span>Texel &middot; Aseprite &middot; Krita &middot; GIMP</span>
    </div>
    <div class="grain"></div>
  </div>
</body>
</html>
"""

with open(OUT, "w", encoding="utf8", newline="\n") as fh:
    fh.write(HTML)
print(f"make_cover: wrote {OUT}")
print(f"  {n} palettes, {steps} steps, {n * steps} colours, hero = {', '.join(HERO)}")
