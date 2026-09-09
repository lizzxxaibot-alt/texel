"""Head-to-head: run the SAME drawing operations through both engines and diff
the actual texels.

This is the only comparison that means anything. Feature counts are marketing;
what matters is whether the pixels come out right. We call each engine's own
rasteriser directly, so nothing is mediated by UI or modal state.

  py -3 compare.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

REF = os.environ.get("PAS_CORE") or os.path.join(
    os.environ.get("TEMP", ""), "claude",
    "C--Users-opule-Desktop-Make-Money",
    "6080a209-9835-4624-bd62-6e59612150f8", "scratchpad", "pas", "1.1.5-0",
    "pixel_art_studio")

if not os.path.isdir(REF):
    sys.exit(f"reference not found at {REF}\nSet PAS_CORE to the unpacked add-on folder.")

# BOTH packages are called `core`. Ours must be imported BEFORE the reference
# goes anywhere near sys.path, and theirs must then be loaded by explicit file
# path so it cannot shadow ours. Getting this backwards silently compares the
# reference against itself.
from core import raster as OURS_R                     # ours
import importlib.util


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


THEIR_ALGO = _load("pas_algo", os.path.join(REF, "core", "algo.py"))

W = H = 32
rows = []


def render(pts, w=W, h=H):
    """Rasterise a point list to a set, ignoring out-of-bounds."""
    return {(x, y) for x, y in pts if 0 <= x < w and 0 <= y < h}


def compare(name, ours, theirs, note=""):
    a, b = render(ours), render(theirs)
    same = a == b
    only_a = len(a - b)
    only_b = len(b - a)
    jaccard = len(a & b) / len(a | b) * 100 if (a | b) else 100.0
    rows.append((name, len(a), len(b), same, only_a, only_b, jaccard, note))
    return same


def ascii_art(pts, w=W, h=H, mark="#"):
    grid = [["." for _ in range(w)] for _ in range(h)]
    for x, y in render(pts, w, h):
        grid[y][x] = mark
    return ["".join(r) for r in grid]


def side_by_side(title, ours, theirs, w=W, h=H):
    a, b = ascii_art(ours, w, h), ascii_art(theirs, w, h)
    print(f"\n{title}")
    print(f"  {'TEXEL (ours)'.ljust(w)}   {'PIXEL ART STUDIO'.ljust(w)}")
    for la, lb in zip(a, b):
        flag = "  " if la == lb else " <"
        print(f"  {la}   {lb}{flag}")


print("=" * 78)
print("  TEXEL  vs  PIXEL ART STUDIO 1.1.5  -  same input, same rasteriser call")
print("=" * 78)

# ---------------------------------------------------------------- 1. lines
for (x0, y0, x1, y1) in ((2, 2, 29, 12), (0, 0, 31, 31), (5, 28, 27, 3), (4, 4, 4, 25)):
    ours = OURS_R.line(x0, y0, x1, y1)
    theirs = THEIR_ALGO.line_continuous(x0, y0, x1, y1)
    compare(f"line ({x0},{y0})-({x1},{y1})", ours, theirs)

# ------------------------------------------------ 2. pixel-perfect filtering
staircase = [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (3, 2), (3, 3), (4, 3), (4, 4)]
ours_pp = OURS_R.pixel_perfect(staircase)
theirs_pp = THEIR_ALGO.pixel_perfect_filter(list(staircase))
compare("pixel-perfect on a freehand staircase", ours_pp, theirs_pp)

ours_line_pp = OURS_R.pixel_perfect(OURS_R.line(2, 2, 29, 12))
theirs_line_pp = THEIR_ALGO.line_perfect(2, 2, 29, 12)
compare("pixel-perfect line (2,2)-(29,12)", ours_line_pp, theirs_line_pp)

# ------------------------------------------------------------- 3. rectangles
for (x0, y0, x1, y1) in ((3, 3, 20, 14), (0, 0, 31, 31)):
    compare(f"rect outline ({x0},{y0})-({x1},{y1})",
            OURS_R.rect(x0, y0, x1, y1),
            THEIR_ALGO.rect_outline(x0, y0, x1, y1))

# ---------------------------------------------------------------- 4. ellipses
for (x0, y0, x1, y1) in ((4, 4, 27, 20), (8, 8, 23, 23), (2, 10, 29, 18)):
    compare(f"ellipse ({x0},{y0})-({x1},{y1})",
            OURS_R.ellipse_box(x0, y0, x1, y1),
            THEIR_ALGO.ellipse_points(x0, y0, x1, y1))

# ------------------------------------------------------------------- report
print(f"\n{'operation':<42} {'ours':>5} {'theirs':>7} {'match':>6} {'overlap':>8}")
print("-" * 78)
ident = 0
for name, na, nb, same, oa, ob, jac, note in rows:
    if same:
        ident += 1
    print(f"{name:<42} {na:>5} {nb:>7} {'YES' if same else ' no':>6} {jac:>7.1f}%")
print("-" * 78)
print(f"identical output on {ident}/{len(rows)} operations")

side_by_side("LINE (2,2)-(29,12), pixel-perfect",
             ours_line_pp, theirs_line_pp)
side_by_side("ELLIPSE bounding box (4,4)-(27,20)",
             OURS_R.ellipse_box(4, 4, 27, 20),
             THEIR_ALGO.ellipse_points(4, 4, 27, 20))
