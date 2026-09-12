"""Write the itch cover's HTML from the cover template + tables.json.

Same discipline as promo/density/make_density.py: the three numbers shown on
the cover are the ones the sheet prints, pulled from the same tables.json, so
the cover cannot advertise a figure the PDF disagrees with. Nothing is typed.

  python funnel/density_cheatsheet/make_cover.py     (run from texel/)

Writes brand/html/itch_cover_density.html, which render.mjs turns into the
630x500 cover. The template lives beside this file as cover.tpl.html.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
# density_cheatsheet -> funnel -> texel -> gumroad -> app_ventures -> Make_Money
ROOT = HERE
for _ in range(5):
    ROOT = os.path.dirname(ROOT)
OUT = os.path.join(ROOT, "brand", "html", "itch_cover_density.html")

d = json.load(open(os.path.join(HERE, "tables.json"), encoding="utf-8"))

# The cover shows ONE density column, because three rows at one density is the
# thing a stranger can read in a 315px grid thumbnail; the full 8x4 grid is
# what they get for downloading it. 32 px/unit is the middle rung.
SHOW_D = 32
PICKS = ["Small crate", "Character", "Wall section"]

col = d["densities"].index(SHOW_D)
by_name = {r["name"]: r for r in d["grid"]}
cells = []
for name in PICKS:
    r = by_name[name]                               # KeyError if ever renamed
    cells.append(
        '<div class="cell">'
        f'<div class="what">{name}</div>'
        f'<div class="size">{r["m"]} m</div>'
        f'<div class="tex">{r["cells"][col]["tex"]}<span>px</span></div>'
        '</div>')

html = open(os.path.join(HERE, "cover.tpl.html"), encoding="utf-8").read()
for key, val in (
    ("{{CELLS}}", "\n      ".join(cells)),
    ("{{D}}", str(SHOW_D)),
    ("{{ROWS}}", str(len(d["grid"]))),
):
    assert key in html, f"template lost {key}"
    html = html.replace(key, val)

open(OUT, "w", encoding="utf-8").write(html)
print("ok:", os.path.relpath(OUT, ROOT))
print(f"  showing {SHOW_D} px/unit:",
      ", ".join(f'{n} {by_name[n]["m"]}m -> {by_name[n]["cells"][col]["tex"]}px'
                for n in PICKS))
