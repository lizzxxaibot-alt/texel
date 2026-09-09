"""Build the frame data for the pixel-perfect GIF. Not shipped.

Everything drawn in the GIF comes out of the SHIPPED code - core.raster.line,
pixel_perfect and PerfectStroke - replayed exactly the way tex_paint's modal
loop replays it. Nothing here re-implements the feature, because a promo asset
that demonstrates a private copy of the algorithm demonstrates nothing.

  python gif_stroke.py   ->  gif/stroke.json
"""
from __future__ import annotations
import json
import math
import os

from core import raster as R

W, H = 58, 13                      # canvas, in texels
ZOOM = 8                           # screen px per texel while "drawing"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gif", "stroke.json")


def hand_arch(n: int = 460) -> list[tuple[int, int]]:
    """A hand-drawn arch, sampled once per mouse event and floored to texels.

    An arch rather than a straight diagonal on purpose: its slope runs from
    almost flat at the ends through steep in the middle, so the filter is shown
    working at every angle instead of the one angle that flatters it. The sine
    term is hand tremor - without it the path is machine-smooth and the
    staircase it produces would not be the one a real drag produces.

    Tuned to leave one empty row above the peak and one below the endpoints, so
    the arc sits centred in its box instead of low in it.
    """
    pts = []
    for i in range(n):
        t = i / (n - 1)
        x = 2.0 + t * (W - 5)
        y = 11.0 - 9.4 * math.sin(math.pi * t) + 0.5 * math.sin(t * 13.0)
        sx, sy = x * ZOOM + 3, y * ZOOM + 3
        pts.append((int(sx // ZOOM), int(sy // ZOOM)))
    return pts


def replay(events, perfect):
    """tex_paint's modal loop: what is on the canvas after each mouse event.

    Also records the PROVISIONAL texel at each moment - the one the filter is
    holding back because the next event could still prove it a corner. The GIF
    draws it dimmed, so the two rows are the same length at every instant. They
    are the same drag; only one of them is allowed to commit yet.
    """
    st = R.PerfectStroke(events[0], perfect)
    painted = [events[0]]
    per_event, prov = [list(painted)], [None]
    for e in events[1:]:
        new = st.add(e)
        if new:
            painted.extend(new)
        per_event.append(list(painted))
        if perfect:
            held = R.pixel_perfect(st.trail)[-1]
            prov.append(held if held not in painted else None)
        else:
            prov.append(None)
    painted.extend(st.end())
    per_event.append(list(painted))
    prov.append(None)                       # mouse-up: nothing is held any more
    return st, painted, per_event, prov


def has_L(pts):
    """Corner texels: three in a row that turn, each orthogonal to the last."""
    out = []
    for a, b, c in zip(pts, pts[1:], pts[2:]):
        if ((abs(b[0]-a[0]) + abs(b[1]-a[1])) == 1
                and (abs(c[0]-b[0]) + abs(c[1]-b[1])) == 1
                and (c[0]-b[0]) != (b[0]-a[0]) and (c[1]-b[1]) != (b[1]-a[1])):
            out.append(b)
    return out


def main():
    ev = hand_arch()
    st_off, off, off_steps, _ = replay(ev, False)
    st_on,  on,  on_steps, on_prov = replay(ev, True)
    walked = st_off.trail

    # dedupe OFF: consecutive joined segments share their first point, and
    # _commit stamps, so the canvas only ever shows distinct texels
    def uniq(seq):
        seen, out = set(), []
        for p in seq:
            if p not in seen:
                seen.add(p); out.append(p)
        return out
    off_steps = [uniq(s) for s in off_steps]
    off = uniq(off)

    corners = has_L(off)
    assert on == R.pixel_perfect(walked), "ON diverged from the one-shot filter"
    assert not has_L(on), "ON still has corners - the fix is not working"
    assert corners, "the path produced no corners; the demo would show nothing"
    assert max(y for _, y in walked) < H and min(y for _, y in walked) >= 0, \
        "the arc does not fit the canvas"

    # One keyframe per newly-touched texel - but BOTH panels are sampled at the
    # same mouse event. Keyframing them independently desynced them: ON paints
    # fewer texels, so its keyframes ran ahead and the finished stroke appeared
    # in front of the cursor, which is the opposite of what the feature does.
    moments = [0]
    for i in range(1, len(off_steps)):
        if len(off_steps[i]) != len(off_steps[i - 1]):
            moments.append(i)
    if moments[-1] != len(off_steps) - 1:
        moments.append(len(off_steps) - 1)      # mouse-up: ON releases its held texel

    ko = [off_steps[i] for i in moments]
    kn = [on_steps[i] for i in moments]
    kp = [on_prov[i] for i in moments]
    cur = [ev[min(i, len(ev) - 1)] for i in moments]
    # how many mouse events have arrived by each frame, so the readout counts up
    # with its neighbours instead of sitting frozen at the total
    seen = [min(i, len(ev) - 1) + 1 for i in moments]
    frames = len(moments)

    # corners frame by frame: a texel only becomes a corner once the texel
    # after it exists, so the final set is wrong for every frame but the last
    corner_steps = [has_L(s) for s in ko]

    for f, (o, n, c) in enumerate(zip(ko, kn, cur)):
        assert o[-1] == c, f"frame {f}: OFF does not end under the cursor"
        assert len(n) <= len(o), f"frame {f}: ON is ahead of OFF"
    # with the provisional texel drawn, the two rows must reach the same length
    def reach(pts, extra):
        xs = [x for x, _ in pts] + ([extra[0]] if extra else [])
        return max(xs)
    lagging = [f for f, (o, n, p) in enumerate(zip(ko, kn, kp))
               if reach(n, p) != reach(o, None)]

    data = {
        "w": W, "h": H, "frames": frames, "lift": frames - 1,
        "cursor": [list(p) for p in cur],
        "seen": seen,
        "off": [[list(p) for p in s] for s in ko],
        "on":  [[list(p) for p in s] for s in kn],
        "prov": [list(p) if p else None for p in kp],
        "corner_steps": [[list(p) for p in c] for c in corner_steps],
        "total_off": len(off), "total_on": len(on), "total_corners": len(corners),
        "events": len(ev), "walked": len(walked),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh)

    print(f"canvas          {W} x {H} texels")
    print(f"rows used       {min(y for _, y in walked)}..{max(y for _, y in walked)}")
    print(f"mouse events    {len(ev)}")
    print(f"texels walked   {len(walked)}")
    print(f"OFF paints      {len(off)}   with {len(corners)} doubled corners")
    print(f"ON  paints      {len(on)}   with {len(has_L(on))} doubled corners")
    print(f"frames          {frames}   (both panels sampled at the same event)")
    print(f"rows end short   {len(lagging)} frames"
          + (f"  <- {lagging[:6]}" if lagging else "  (both rows always reach the same column)"))
    print(f"wrote           {OUT}")


if __name__ == "__main__":
    main()
