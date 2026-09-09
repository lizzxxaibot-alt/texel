"""Stitch every marketing video into one labelled reel for review. Not shipped.

There are 34 clips at five different resolutions across three folders. Reviewing
them one at a time means opening 34 files and remembering which is which, so
this normalises them all to 1280x720, burns a caption on each saying what it is
and where it is meant to go, and concatenates the lot with a title card in front
of each group.

  python review_reel.py            # all of them
  python review_reel.py cinematic  # one group

  ->  promo/REVIEW-REEL.mp4

Nothing here is a marketing asset; it is a contact sheet that happens to move.
"""
from __future__ import annotations
import os
import shutil
import subprocess
import sys
import tempfile

import marketing_index as MI

HERE = MI.HERE
OUT = os.path.join(HERE, "promo", "REVIEW-REEL.mp4")
W, H = 1280, 720
FONT = os.path.join(MI.ROOT, "brand", "fonts", "Inter.ttf")
FONT_B = os.path.join(MI.ROOT, "brand", "fonts", "GeistMono-Bold.ttf")


def cap_file(work: str, name: str, text: str) -> str:
    """Captions go in a FILE, not in the filtergraph.

    drawtext's text= has to survive filtergraph parsing, which eats commas,
    colons, apostrophes and backslashes - stripping them turned "Bluesky, itch
    trailers, Gumroad." into "Bluesky itch trailers Gumroad." textfile= has no
    such problem and the caption reads the way it was written.
    """
    with open(os.path.join(work, name), "w", encoding="utf-8") as fh:
        fh.write(text)
    return name


def run(args, cwd):
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        print("    ffmpeg failed:", (r.stderr or "").strip().splitlines()[-1:])
    return r.returncode == 0


def title_card(work, idx, text, sub, seconds=1.6):
    """A group divider, so the reel does not run 34 clips together."""
    out = f"c{idx:03d}.mp4"
    a = cap_file(work, f"t{idx:03d}a.txt", text)
    b = cap_file(work, f"t{idx:03d}b.txt", sub)
    vf = (f"drawtext=fontfile=b.ttf:textfile={a}:fontcolor=0xf2e6c8:"
          f"fontsize=54:x=(w-text_w)/2:y=(h-text_h)/2-26,"
          f"drawtext=fontfile=r.ttf:textfile={b}:fontcolor=0xab9f8a:"
          f"fontsize=25:x=(w-text_w)/2:y=(h-text_h)/2+42")
    ok = run([MI.FFMPEG, "-y", "-v", "error", "-f", "lavfi", "-i",
              f"color=c=0x141317:s={W}x{H}:d={seconds}:r=30", "-vf", vf,
              "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
              "-pix_fmt", "yuv420p", out], work)
    return out if ok else None


def clip(work, idx, src, caption, group):
    """One clip, letterboxed to 1280x720 with a caption bar burned in."""
    out = f"c{idx:03d}.mp4"
    a = cap_file(work, f"t{idx:03d}a.txt", caption)
    b = cap_file(work, f"t{idx:03d}b.txt", group)
    vf = (f"scale={W}:{H}:force_original_aspect_ratio=decrease:flags=lanczos,"
          f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:color=0x141317,"
          f"drawbox=x=0:y={H - 74}:w={W}:h=74:color=0x0d0c10@0.82:t=fill,"
          f"drawtext=fontfile=b.ttf:textfile={a}:fontcolor=0xf2e6c8:"
          f"fontsize=25:x=28:y={H - 56},"
          f"drawtext=fontfile=r.ttf:textfile={b}:fontcolor=0xff9c3f:"
          f"fontsize=19:x=28:y={H - 26},"
          f"fps=30,format=yuv420p")
    ok = run([MI.FFMPEG, "-y", "-v", "error", "-i", src, "-an", "-vf", vf,
              "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", out], work)
    return out if ok else None


def main():
    only = sys.argv[1].lower() if len(sys.argv) > 1 else None
    rows = MI.walk()

    # reuse the index's own grouping so the reel and the page never disagree
    plan, used = [], set()
    for title, blurb, entries in MI.GROUPS:
        vids = []
        for pref, note in entries:
            for k, r in sorted(rows.items()):
                if (k.startswith(pref) and k not in used and r["ext"] == ".mp4"
                        and not any(s in k for s in MI.SCRATCH)
                        and k not in MI.BROKEN):
                    used.add(k)
                    vids.append((r, note))
        if vids and (only is None or only in title.lower()):
            plan.append((title, blurb, vids))

    total = sum(len(v) for _, _, v in plan)
    if not total:
        sys.exit("no videos matched")
    print(f"{total} clips in {len(plan)} groups -> {os.path.basename(OUT)}")

    work = tempfile.mkdtemp(prefix="texel_reel_")
    shutil.copy(FONT, os.path.join(work, "r.ttf"))
    shutil.copy(FONT_B if os.path.exists(FONT_B) else FONT,
                os.path.join(work, "b.ttf"))
    parts, i, n = [], 0, 0
    try:
        for title, blurb, vids in plan:
            i += 1
            p = title_card(work, i, title, f"{len(vids)} clips · {blurb}")
            if p:
                parts.append(p)
            for r, note in vids:
                i += 1; n += 1
                src = os.path.join(HERE, r["href"].replace("/", os.sep))
                cap = f"{n}/{total}  ·  {r['name']}  ·  {r['dur']:.0f}s  ·  {r['w']}×{r['h']}"
                p = clip(work, i, src, cap, note or title)
                print(f"  {n:2d}/{total}  {r['name']}" + ("" if p else "   FAILED"))
                if p:
                    parts.append(p)

        with open(os.path.join(work, "list.txt"), "w", encoding="utf-8") as fh:
            for p in parts:
                fh.write(f"file '{p}'\n")
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        ok = run([MI.FFMPEG, "-y", "-v", "error", "-f", "concat", "-safe", "0",
                  "-i", "list.txt", "-c", "copy", OUT], work)
        if not ok:
            sys.exit("concat failed")
    finally:
        shutil.rmtree(work, ignore_errors=True)

    w, h, _, dur = MI.probe(OUT, ".mp4")
    print(f"\n{OUT}")
    print(f"  {w}x{h}  {dur / 60:.1f} min  {os.path.getsize(OUT) / 1e6:.0f} MB")


if __name__ == "__main__":
    main()
