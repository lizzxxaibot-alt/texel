"""Pull a marketing still library out of the render frames, before they go.

`texel-marketing` may not reuse a visual inside 21 days. With four Texel slots a
week that is twelve distinct images a month, and the MP4s alone do not supply
them. So harvest stills across each shot's whole camera move - the frames are
1.3 GB and about to be deleted, and a still is 300 KB.

  python harvest_stills.py
"""
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "store", "stills")
os.makedirs(OUT, exist_ok=True)

MAGICK = shutil.which("magick") or "magick"


def frames(d):
    if not os.path.isdir(d):
        return []
    return sorted(f for f in os.listdir(d) if f.startswith("f_") and f.endswith(".png"))


def take(src_dir, prefix, n):
    """Spread n picks across the move, skipping the first and last 8% - the
    ends of a camera move are the least composed part of it."""
    fs = frames(src_dir)
    if not fs:
        return 0
    lo, hi = int(len(fs) * 0.08), int(len(fs) * 0.92)
    span = max(1, hi - lo)
    made = 0
    for i in range(n):
        idx = lo + (span * i) // max(1, n - 1) if n > 1 else lo + span // 2
        idx = min(idx, len(fs) - 1)
        dst = os.path.join(OUT, f"{prefix}_{i + 1:02d}.png")
        subprocess.run([MAGICK, os.path.join(src_dir, fs[idx]),
                        "-quality", "94", dst], check=True)
        made += 1
    return made


def main():
    total = 0
    # the five new cinematic shots - the primary ad stock
    for name in ("dungeon", "temple", "hangar", "market", "shrine"):
        d = os.path.join(HERE, "promo", "shots", name, "frames")
        n = take(d, f"shot_{name}", 6)
        print(f"[stills] shot/{name}: {n}", flush=True)
        total += n
    # the older environment renders, still perfectly good images
    for name in ("shrine", "corridor", "ruins", "tavern", "cavern"):
        d = os.path.join(HERE, "promo", "envs", name, "frames")
        n = take(d, f"env_{name}", 3)
        print(f"[stills] env/{name}: {n}", flush=True)
        total += n
    # the interface, mid-use
    for name, picks in (("anim", 5), ("sprite", 4), ("showcase", 3)):
        d = os.path.join(HERE, "promo", "steps", name)
        n = take(d, f"ui_{name}", picks)
        print(f"[stills] ui/{name}: {n}", flush=True)
        total += n

    size = sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT))
    print(f"HARVEST_DONE stills={total} dir={OUT} bytes={size} "
          f"weeks_of_content={total / 4:.0f}", flush=True)


if __name__ == "__main__":
    main()
