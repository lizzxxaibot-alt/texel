"""Headless test for the raster core. Plain python, no Blender needed.
  py -3 test_raster.py    ->  exits non-zero on failure
"""
import sys
from core import raster as R

fails = []
def check(name, cond, detail=""):
    if cond: print(f"[ok]   {name}")
    else:    print(f"[FAIL] {name}  {detail}"); fails.append(name)

# --- line
l = R.line(0, 0, 4, 0)
check("horizontal line", l == [(0,0),(1,0),(2,0),(3,0),(4,0)], l)
d = R.line(0, 0, 3, 3)
check("perfect diagonal", d == [(0,0),(1,1),(2,2),(3,3)], d)
check("endpoints inclusive", R.line(2,2,2,2) == [(2,2)])
rev = R.line(5, 1, 0, 3)
check("reversed line same length", len(rev) == len(R.line(0,3,5,1)))

# --- pixel_perfect: the marquee feature. Freehand drags land as staircases.
def has_L(pts):
    for a, b, c in zip(pts, pts[1:], pts[2:]):
        if (abs(b[0]-a[0])+abs(b[1]-a[1])) == 1 and (abs(c[0]-b[0])+abs(c[1]-b[1])) == 1            and (c[0]-b[0]) != (b[0]-a[0]) and (c[1]-b[1]) != (b[1]-a[1]):
            return True
    return False

# a mouse-traced shallow drag: orthogonal steps only, which is what events give us
raw = [(0,0),(1,0),(1,1),(2,1),(2,2),(3,2),(3,3)]
pp  = R.pixel_perfect(raw)
check("bresenham line() emits NO L-corners (it steps diagonally)", not has_L(R.line(0,0,5,2)))
check("freehand staircase HAS L-corners (so the test is meaningful)", has_L(raw), raw)
check("pixel_perfect removes every L-corner", not has_L(pp), pp)
check("pixel_perfect keeps endpoints", pp[0] == raw[0] and pp[-1] == raw[-1], pp)
check("pixel_perfect is shorter", len(pp) < len(raw), f"{len(raw)}->{len(pp)}")
check("pixel_perfect result is a clean diagonal", pp == [(0,0),(1,1),(2,2),(3,3)], pp)
check("pixel_perfect no-op on pure diagonal", R.pixel_perfect(d) == d)
check("pixel_perfect no-op on straight run", R.pixel_perfect(R.line(0,0,4,0)) == R.line(0,0,4,0))

# --- PerfectStroke: the filter as the live paint loop actually uses it.
# This block exists because the filter passing its own tests was not enough.
# tex_paint stamps and never clears, so it used to commit the filter's
# provisional last point, and a 420-event drag landed the SAME 69 texels with
# the toggle on as with it off. The feature was a no-op on the one tool it
# advertises. What follows drives the shipped object, not a copy of it.
import math

def hand_drag(n=420, zoom=8):
    """A human diagonal, sampled per mouse event and floored to texels."""
    out = []
    for i in range(n):
        t = i / (n - 1)
        sx, sy = 6 + t * 46 * zoom, 8 + (t * 22 + 2.2 * math.sin(t * 7.0)) * zoom
        out.append((int(sx // zoom), int(sy // zoom)))
    return out

def replay(events, perfect):
    """What tex_paint's modal loop commits, in order, for one drag."""
    st = R.PerfectStroke(events[0], perfect)
    painted = [events[0]]
    for e in events[1:]:
        painted.extend(st.add(e))
    painted.extend(st.end())
    return st, painted

ev = hand_drag()
st_on,  on  = replay(ev, True)
st_off, off = replay(ev, False)
walked = st_on.trail

check("the simulated drag is a staircase (so the test can fail)", has_L(walked),
      f"{len(walked)} texels")
check("PerfectStroke ON leaves no L-corner", not has_L(on), has_L(on))
check("PerfectStroke ON matches the one-shot filter", on == R.pixel_perfect(walked),
      f"{len(on)} vs {len(R.pixel_perfect(walked))}")
# OFF hands back each joined segment whole, so consecutive segments share a
# point. _commit stamps, which is idempotent, so the duplicates cost nothing -
# compare what lands on the canvas.
check("PerfectStroke ON paints FEWER texels than OFF (it is not a no-op)",
      len(set(on)) < len(set(off)), f"on={len(set(on))} off={len(set(off))}")
check("PerfectStroke OFF covers the untouched walk", set(off) == set(walked),
      f"{len(set(off))} vs {len(walked)}")
check("PerfectStroke keeps both endpoints", on[0] == walked[0] and on[-1] == walked[-1])
check("PerfectStroke never hands the same texel out twice", len(on) == len(set(on)))
check("PerfectStroke ignores an event that stays in one texel",
      R.PerfectStroke((3, 3)).add((3, 3)) == [])
check("PerfectStroke joins a gap when events skip texels",
      R.PerfectStroke((0, 0)).add((6, 0)) + R.PerfectStroke((0, 0), True).end() != [])
one = R.PerfectStroke((2, 2))
check("a stroke that never moves still commits nothing extra", one.end() == [])

# --- rect
check("rect outline 3x3 = 8 px", len(R.rect(0,0,2,2)) == 8, R.rect(0,0,2,2))
check("rect filled 3x3 = 9 px", len(R.rect(0,0,2,2,filled=True)) == 9)
check("rect handles reversed coords", R.rect(2,2,0,0) == R.rect(0,0,2,2))

# --- ellipse
e = R.ellipse(10, 10, 5, 3)
check("ellipse is 4-way symmetric",
      all((20-x, y) in set(e) and (x, 20-y) in set(e) for x, y in e))
check("ellipse spans full width", min(x for x,_ in e) == 5 and max(x for x,_ in e) == 15)
check("ellipse spans full height", min(y for _,y in e) == 7 and max(y for _,y in e) == 13)
check("ellipse r=0 is a dot", R.ellipse(3,3,0,0) == [(3,3)])
ef = set(R.ellipse(10,10,5,3, filled=True))
check("filled ellipse contains its outline", set(e) <= ef)
check("filled ellipse contains centre", (10,10) in ef)

# --- flood fill on a 8x8 grid split by a wall at x=4
W = H = 8
grid = [[(255,255,255,255)]*W for _ in range(H)]
for y in range(H): grid[y][4] = (0,0,0,255)
get = lambda x, y: grid[y][x]
left = R.flood_fill(get, W, H, 0, 0, (255,0,0,255))
check("flood stays left of the wall", all(x < 4 for x,_ in left), max(x for x,_ in left))
check("flood filled the whole left region", len(left) == 4*H, len(left))
check("flood never crosses the wall", not any(x == 4 for x,_ in left))
glob = R.flood_fill(get, W, H, 0, 0, (255,0,0,255), contiguous=False)
check("non-contiguous crosses the wall", any(x > 4 for x,_ in glob))
check("flood on same colour is a no-op", R.flood_fill(get, W, H, 0, 0, (255,255,255,255)) == [])
check("flood outside bounds is empty", R.flood_fill(get, W, H, 99, 0, (0,0,0,255)) == [])

# --- stack safety: a big fill must not recurse
big = [[(1,1,1,255)]*256 for _ in range(256)]
r = R.flood_fill(lambda x,y: big[y][x], 256, 256, 0, 0, (9,9,9,255))
check("256x256 fill completes without stack overflow", len(r) == 256*256, len(r))


# ---------------------------------------------------------------- uv mapping
from core import uvmap as U
print()
check("uv (0,1) is top-left texel", U.uv_to_texel(0.0, 1.0, 16, 16) == (0, 0))
check("uv (0,0) is bottom-left texel", U.uv_to_texel(0.0, 0.0, 16, 16) == (0, 15))
check("uv (1,1) clamps inside", U.uv_to_texel(1.0, 1.0, 16, 16) == (15, 0))
check("uv out of range clamps", U.uv_to_texel(-5.0, 9.0, 16, 16) == (0, 0))
# floor vs round: 0.99 of the way across texel 0 must still be texel 0
check("uses floor not round (0.03 stays in texel 0)", U.uv_to_texel(0.03, 0.97, 16, 16) == (0, 0),
      U.uv_to_texel(0.03, 0.97, 16, 16))
check("texel 1 starts exactly at 1/16", U.uv_to_texel(1/16, 1.0, 16, 16) == (1, 0))
rt = U.uv_to_texel(*U.texel_to_uv(7, 3, 32, 32), 32, 32)
check("texel -> uv -> texel round trips", rt == (7, 3), rt)

b = U.barycentric((0.5, 0.5), (0, 0), (1, 0), (0, 1))
check("barycentric weights sum to 1", abs(sum(b) - 1.0) < 1e-9, b)
check("barycentric at vertex a is (1,0,0)",
      all(abs(x - y) < 1e-9 for x, y in zip(U.barycentric((0,0),(0,0),(1,0),(0,1)), (1,0,0))))
check("degenerate triangle does not divide by zero",
      U.barycentric((1,1),(0,0),(0,0),(0,0)) == (1.0, 0.0, 0.0))
check("interp_uv at a returns uv_a", U.interp_uv((1,0,0), (0.25,0.75), (0,0), (1,1)) == (0.25,0.75))

# a 1x1 world quad fully covering a 64px texture resolves at 64 px/unit
check("texel_density basic case", abs(U.texel_density(1.0, 1.0, 64) - 64.0) < 1e-6,
      U.texel_density(1.0, 1.0, 64))
check("texel_density guards zero area", U.texel_density(1.0, 0.0, 64) == 0.0)
s = U.uv_scale_for_density(32.0, 1.0, 64)
check("uv_scale_for_density inverts texel_density",
      abs(U.texel_density(s*s, 1.0, 64) - 32.0) < 1e-6, s)
check("snap_uv_to_grid lands on a corner", U.snap_uv_to_grid(0.26, 0.51, 16, 16) == (0.25, 0.5),
      U.snap_uv_to_grid(0.26, 0.51, 16, 16))

# --- ellipse_box: must fill the bounding box EXACTLY at both parities.
# Regression: centre+radius form lost a texel on even spans (24 wide -> 23).
for _box in ((4, 4, 27, 20), (8, 8, 23, 23), (0, 0, 4, 4), (0, 0, 5, 5), (3, 1, 30, 12)):
    _x0, _y0, _x1, _y1 = _box
    _e = R.ellipse_box(*_box)
    _xs = [x for x, _ in _e]; _ys = [y for _, y in _e]
    check(f"ellipse_box {_box} fills width", min(_xs) == _x0 and max(_xs) == _x1,
          (min(_xs), max(_xs)))
    check(f"ellipse_box {_box} fills height", min(_ys) == _y0 and max(_ys) == _y1,
          (min(_ys), max(_ys)))
check("ellipse_box filled contains its outline",
      set(R.ellipse_box(4, 4, 27, 20)) <= set(R.ellipse_box(4, 4, 27, 20, filled=True)))
check("ellipse_box handles reversed corners",
      R.ellipse_box(27, 20, 4, 4) == R.ellipse_box(4, 4, 27, 20))
check("ellipse_box degenerate 1px box", R.ellipse_box(5, 5, 5, 5) == [(5, 5)])

# --- ellipse accuracy against the TRUE continuous ellipse, in texel-centre space.
# A texel (x,y) covers [x,x+1), so its centre is (x+.5, y+.5) and a box x0..x1
# inclusive has centre (x0+x1+1)/2 and semi-axis (x1-x0+1)/2. Measuring at
# integer y instead skews the result by half a texel and inverts the verdict -
# that mistake was made once and must not come back.
import math as _m
def _rms(pts, box):
    _x0, _y0, _x1, _y1 = box
    _cx, _cy = (_x0+_x1+1)/2.0, (_y0+_y1+1)/2.0
    _a, _b = (_x1-_x0+1)/2.0, (_y1-_y0+1)/2.0
    _rows = {}
    for _x, _y in pts:
        _rows.setdefault(_y, []).append(_x)
    _e = []
    for _y, _xs in _rows.items():
        _t = (_y+0.5-_cy)/_b
        if abs(_t) > 1.0:
            continue
        _e.append((min(_xs)+0.5 - (_cx - _a*_m.sqrt(max(0.0, 1-_t*_t))))**2)
    return _m.sqrt(sum(_e)/len(_e)) if _e else 0.0

for _box in ((4, 4, 27, 20), (8, 8, 23, 23), (0, 0, 31, 31), (3, 3, 40, 12), (5, 5, 20, 40)):
    _err = _rms(R.ellipse_box(*_box), _box)
    check(f"ellipse_box {_box} within 1 texel of the true curve", _err < 1.0, f"{_err:.3f}")


# --- brush masks
for _sh in ("SQUARE", "ROUND", "DIAMOND"):
    check(f"{_sh} size 1 is a single texel", R.brush_mask(1, _sh) == [(0, 0)])
    _m = R.brush_mask(7, _sh)
    check(f"{_sh} 7 is centred", (0, 0) in _m)
    check(f"{_sh} 7 stays in its box", all(-3 <= x <= 3 and -3 <= y <= 3 for x, y in _m))
check("square 5 fills 25", len(R.brush_mask(5, "SQUARE")) == 25)
check("round 5 is 21", len(R.brush_mask(5, "ROUND")) == 21, len(R.brush_mask(5, "ROUND")))
check("diamond 5 is 13", len(R.brush_mask(5, "DIAMOND")) == 13)
check("round < square", len(R.brush_mask(9, "ROUND")) < len(R.brush_mask(9, "SQUARE")))
check("diamond < round", len(R.brush_mask(9, "DIAMOND")) < len(R.brush_mask(9, "ROUND")))
check("size 0 clamps to one texel", R.brush_mask(0) == [(0, 0)])
check("even sizes work too", len(R.brush_mask(4, "ROUND")) > 0)
check("unknown shape falls back to square",
      len(R.brush_mask(5, "NONSENSE")) == 25)

print()
if fails:
    print(f"{len(fails)} FAILED: {fails}"); sys.exit(1)
print("RASTER CORE: ALL PASS")
