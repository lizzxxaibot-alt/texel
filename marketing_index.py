"""Inventory every Texel marketing asset and write a browsable index. Not shipped.

There are ~290 image and video files across five folders, most of them working
intermediates nobody should ever upload. This walks the lot, measures each one
(dimensions, duration, frame count, bytes), separates the publishable from the
scratch, and writes MARKETING.html - open it and every asset is on one page,
videos playable, grouped by where it is meant to go.

  python marketing_index.py

Re-run it after making new art; it is the index, not a hand-maintained list.
"""
from __future__ import annotations
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SITE = os.path.join(ROOT, "mintworks_site", "texel", "img")
MAGICK = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick"
FFBIN = (r"C:\Users\opule\AppData\Local\Microsoft\WinGet\Packages"
         r"\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
         r"\ffmpeg-9.0-full_build\bin")
FFPROBE = os.path.join(FFBIN, "ffprobe.exe")
FFMPEG = os.path.join(FFBIN, "ffmpeg.exe")
POSTERS = os.path.join(HERE, "_posters")
OUT = os.path.join(HERE, "MARKETING.html")

# folders that only ever hold intermediates: per-frame dumps, sprite strips, the
# input art the renders were built from. Real work, not things to upload.
SCRATCH = ("gallery/_frames", "/sprite", "promo/steps/", "promo/anim",
           "promo/walk", "promo/shots/", "promo/_reel", "shots/panels",
           "promo/shield", "promo/sword", "promo/tutorial", "promo/cinematic",
           "gif/palette.png", "gif/stroke.json")

# (heading, blurb, [(glob-ish path prefix, note)]) - order is the order shown
GROUPS = [
    ("Store listing", "itch.io and Gumroad. These are the images a buyer sees "
     "before they read a word.", [
        ("store/cover_630x500.png", "itch cover - the required 630x500"),
        ("store/cover_thumb_315.png", "itch thumbnail, 315x250"),
        ("store/pixel-perfect.gif", "the marquee-feature demo"),
        ("store/shots_1280x720.png", "five-scene contact sheet"),
        ("store/animates_1280x720.png", "the animation pitch, one image"),
        ("store/shot_dungeon.png", "gallery 1 - animation"),
        ("store/shot_temple.png", "gallery 2 - seamless tiling"),
        ("store/shot_hangar.png", "gallery 3 - palette swap"),
        ("store/shot_market.png", "gallery 4 - texel density"),
        ("store/shot_shrine.png", "gallery 5 - mirror symmetry"),
        ("store/hero_frame.png", "hero still"),
        ("store/celgrid.png", "the cel grid, explained"),
        ("store/sheet_big.png", "exported sprite sheet"),
        ("store/strip8_big.png", "8-frame walk strip"),
        ("store/strip8.png", "the same strip at 1x"),
    ]),
    ("Product page", "mintworks.cc/texel - already live on the page.", [
        ("site/", ""),
    ]),
    ("Cinematic video", "Scenes built from Texel's own output. Bluesky, itch "
     "trailers, Gumroad.", [
        ("promo/texel-reel-2026.mp4", "the 30s reel - the one trailer"),
        ("promo/shot-dungeon.mp4", ""), ("promo/shot-temple.mp4", ""),
        ("promo/shot-hangar.mp4", ""), ("promo/shot-market.mp4", ""),
        ("promo/shot-shrine.mp4", ""),
        ("promo/env-cavern.mp4", ""), ("promo/env-corridor.mp4", ""),
        ("promo/env-ruins.mp4", ""), ("promo/env-shrine.mp4", ""),
        ("promo/env-tavern.mp4", ""),
        ("promo/texel-environment.mp4", ""),
        ("promo/env-contact.png", "all five environments, one sheet"),
    ]),
    ("How it is made", "Screen-recorded build-ups. Good for replies and "
     "\"how did you do that\" threads.", [
        ("promo/texel-tutorial.mp4", "14s, the longest teaching clip"),
        ("promo/steps-anim.mp4", ""), ("promo/steps-sprite.mp4", ""),
        ("promo/steps-showcase.mp4", ""),
        ("promo/steps-cavern.mp4", ""), ("promo/steps-corridor.mp4", ""),
        ("promo/steps-ruins.mp4", ""), ("promo/steps-shrine.mp4", ""),
        ("promo/steps-tavern.mp4", ""),
        ("promo/texel-sword.mp4", ""), ("promo/texel-shield.mp4", ""),
    ]),
    ("Painting reveals", "Ten objects appearing stroke by stroke - the canvas on "
     "the left, the object it lands on on the right. Nothing rotates: these are "
     "reveals, not turntables. Drop-in posts, one a day.", [
        ("gallery/contact-sheet.png", "all ten at once"),
        ("gallery/texel-reel.mp4", "all ten, 29s"),
        ("gallery/", ""),
    ]),
    ("Still library", "57 frames harvested from the renders. Ad creative, "
     "thumbnails, blog headers - anywhere a still beats a video.", [
        ("store/stills/", ""),
    ]),
    ("Loose ends", "In the repo, not part of a set.", [
        ("shots/hero.png", ""), ("shots/workspace.png", "the add-on in Blender"),
        ("shots/texture_64.png", ""), ("gif/texel-pixel-perfect.gif", "master copy"),
    ]),
]

BROKEN = {"promo/texel-walkthrough.mp4": "2 frames, 0.08s - truncated, do not use"}


def probe(path: str, ext: str):
    if ext == ".mp4":
        try:
            st = json.loads(subprocess.run(
                [FFPROBE, "-v", "error", "-select_streams", "v:0", "-show_entries",
                 "stream=width,height,duration", "-of", "json", path],
                capture_output=True, text=True, timeout=60).stdout)["streams"][0]
            return int(st["width"]), int(st["height"]), 0, float(st.get("duration", 0))
        except Exception:
            return 0, 0, 0, 0.0
    try:
        o = subprocess.run([MAGICK, "identify", "-format", "%w %h %n", path],
                           capture_output=True, text=True, timeout=60).stdout.split()
        return int(o[0]), int(o[1]), int(o[2]) if len(o) > 2 else 1, 0.0
    except Exception:
        return 0, 0, 1, 0.0


def walk():
    rows = {}
    for base in (HERE, SITE):
        for dirpath, dirnames, files in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in
                           ("__pycache__", "dist", "frames", ".git", "core",
                            "reference", "node_modules")]
            for f in sorted(files):
                ext = os.path.splitext(f)[1].lower()
                if ext not in (".png", ".jpg", ".jpeg", ".gif", ".mp4"):
                    continue
                full = os.path.join(dirpath, f)
                rel = os.path.relpath(full, ROOT).replace("\\", "/")
                # group prefixes are written relative to THIS folder, with the
                # website's images folded in under site/ - matching on the
                # repo-root path silently matched nothing
                key = ("site/" + f if base == SITE
                       else os.path.relpath(full, HERE).replace("\\", "/"))
                w, h, n, dur = probe(full, ext)
                rows[key] = dict(rel=rel, key=key, name=f, ext=ext, w=w, h=h,
                                 frames=n, dur=dur, bytes=os.path.getsize(full),
                                 href=os.path.relpath(full, HERE).replace("\\", "/"))
    return rows


def poster(r):
    """A frame from the middle of a clip, so the index shows what a video IS.

    Without it every video card is a black rectangle and the page cannot be used
    to pick an asset, which is the whole job of the page.
    """
    out = os.path.join(POSTERS, os.path.splitext(r["name"])[0] + ".jpg")
    if not os.path.exists(out):
        src = os.path.join(HERE, r["href"].replace("/", os.sep))
        subprocess.run([FFMPEG, "-y", "-v", "error", "-ss", f"{r['dur'] * 0.45:.2f}",
                        "-i", src, "-frames:v", "1", "-vf", "scale=520:-2",
                        "-q:v", "4", out], capture_output=True, timeout=90)
    if not os.path.exists(out):
        return ""
    return os.path.relpath(out, HERE).replace(os.sep, "/")


def card(r, note):
    mb = r["bytes"] / 1e6
    size = f"{mb:.1f} MB" if mb >= 0.1 else f"{r['bytes'] / 1024:.0f} KB"
    meta = f"{r['w']}&times;{r['h']}"
    if r["ext"] == ".mp4":
        meta += f" &middot; {r['dur']:.0f}s"
        pos = poster(r)
        media = (f'<video src="{r["href"]}" controls preload="none" muted loop '
                 f'playsinline' + (f' poster="{pos}"' if pos else "") + '></video>')
    else:
        if r["ext"] == ".gif" and r["frames"] > 1:
            meta += f" &middot; {r['frames']} frames"
        media = f'<img src="{r["href"]}" loading="lazy" alt="{r["name"]}">'
    bad = BROKEN.get(r["key"])
    return f'''<figure class="card{' bad' if bad else ''}">
  <div class="m">{media}</div>
  <figcaption>
    <div class="n">{r["name"]}</div>
    <div class="d">{meta} &middot; {size}</div>
    {f'<div class="note">{bad or note}</div>' if (note or bad) else ''}
  </figcaption>
</figure>'''


def main():
    os.makedirs(POSTERS, exist_ok=True)
    rows = walk()
    used, sections = set(), []
    for title, blurb, entries in GROUPS:
        cards, n_bytes = [], 0
        for pref, note in entries:
            match = [r for k, r in sorted(rows.items())
                     if k.startswith(pref) and k not in used
                     and not any(s in k for s in SCRATCH)]
            for r in match:
                used.add(r["key"]); n_bytes += r["bytes"]
                cards.append(card(r, note if len(match) == 1 else ""))
        if cards:
            sections.append((title, blurb, len(cards), n_bytes, cards))

    pub = len(used)
    scratch = [k for k in rows if k not in used]
    total_mb = sum(rows[k]["bytes"] for k in used) / 1e6
    vids = sum(1 for k in used if rows[k]["ext"] == ".mp4")
    secs = sum(rows[k]["dur"] for k in used)

    nav = " ".join(f'<a href="#{i}">{t}</a>' for i, (t, *_) in enumerate(sections))
    body = "\n".join(
        f'''<section id="{i}">
  <h2>{t} <span class="c">{n} files &middot; {b / 1e6:.0f} MB</span></h2>
  <p class="sub">{blurb}</p>
  <div class="grid">{"".join(cs)}</div>
</section>''' for i, (t, blurb, n, b, cs) in enumerate(sections))

    html = f'''<!doctype html><meta charset="utf-8">
<title>Texel &mdash; marketing assets</title>
<style>
  @font-face{{font-family:'YoungSerif';src:url('{os.path.relpath(os.path.join(ROOT, "brand", "fonts", "YoungSerif-Regular.ttf"), HERE).replace(chr(92), "/")}') format('truetype')}}
  @font-face{{font-family:'Inter';src:url('{os.path.relpath(os.path.join(ROOT, "brand", "fonts", "Inter.ttf"), HERE).replace(chr(92), "/")}') format('truetype')}}
  :root{{--bg:#141317;--bg2:#1b1a21;--panel:#1e1d25;--line:rgba(242,230,200,.14);
    --text:#f2e6c8;--dim:#ab9f8a;--ember:#ff9c3f;--gold:#e7b23a;--bad:#e0563f}}
  *{{margin:0;padding:0;box-sizing:border-box}}
  body{{background:var(--bg);color:var(--text);font-family:'Inter',system-ui,sans-serif;
    line-height:1.55;padding:0 0 80px}}
  header{{padding:56px 40px 28px;border-bottom:1px solid var(--line);
    background:radial-gradient(900px 400px at 80% -20%,rgba(255,156,63,.10),transparent 60%)}}
  h1{{font-family:'YoungSerif',Georgia,serif;font-size:2.5rem;font-weight:400}}
  h1 em{{font-style:normal;color:var(--ember)}}
  .lede{{color:var(--dim);margin-top:10px;max-width:70ch}}
  .tot{{margin-top:20px;display:flex;gap:10px;flex-wrap:wrap}}
  .tot span{{background:var(--panel);border:1px solid var(--line);border-radius:999px;
    padding:6px 14px;font-size:.85rem}}
  .tot b{{color:var(--gold)}}
  nav{{position:sticky;top:0;z-index:9;background:rgba(20,19,23,.94);
    backdrop-filter:blur(8px);border-bottom:1px solid var(--line);
    padding:12px 40px;display:flex;gap:20px;flex-wrap:wrap;font-size:.86rem}}
  nav a{{color:var(--dim);text-decoration:none}}
  nav a:hover{{color:var(--ember)}}
  section{{padding:44px 40px 8px}}
  h2{{font-family:'YoungSerif',Georgia,serif;font-size:1.5rem;font-weight:400}}
  h2 .c{{font-family:'Inter',sans-serif;font-size:.78rem;color:var(--dim);
    margin-left:12px;letter-spacing:.04em}}
  .sub{{color:var(--dim);margin-top:6px;max-width:70ch;font-size:.92rem}}
  .grid{{margin-top:22px;display:grid;gap:18px;
    grid-template-columns:repeat(auto-fill,minmax(260px,1fr))}}
  .card{{background:var(--bg2);border:1px solid var(--line);border-radius:10px;
    overflow:hidden;display:flex;flex-direction:column}}
  .card.bad{{border-color:var(--bad)}}
  .m{{background:#0f0e12;display:flex;align-items:center;justify-content:center;
    min-height:150px;max-height:230px;overflow:hidden}}
  .m img,.m video{{max-width:100%;max-height:230px;display:block;
    image-rendering:auto}}
  figcaption{{padding:11px 13px 13px;border-top:1px solid var(--line)}}
  .n{{font-size:.85rem;word-break:break-all}}
  .d{{font-size:.74rem;color:var(--dim);margin-top:3px;letter-spacing:.03em}}
  .note{{font-size:.76rem;color:var(--gold);margin-top:6px}}
  .card.bad .note{{color:var(--bad)}}
</style>
<header>
  <h1>Texel &mdash; <em>every marketing asset</em></h1>
  <p class="lede">Everything shippable, grouped by where it goes. Videos play in
     place. Regenerate with <code>python marketing_index.py</code> after new art;
     nothing here is maintained by hand.</p>
  <div class="tot">
    <span><b>{pub}</b> publishable files</span>
    <span><b>{total_mb:.0f} MB</b></span>
    <span><b>{vids}</b> videos &middot; {secs / 60:.1f} min</span>
    <span><b>{len(scratch)}</b> working files not listed</span>
  </div>
</header>
<nav>{nav}</nav>
{body}
'''
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(html)

    print(f"{pub} publishable assets, {total_mb:.0f} MB "
          f"({vids} videos, {secs / 60:.1f} min)")
    for t, _, n, b, _ in sections:
        print(f"  {n:3d}  {b / 1e6:7.1f} MB  {t}")
    print(f"  {len(scratch):3d}          working files excluded")
    if BROKEN:
        for k, why in BROKEN.items():
            print(f"  ! {k}: {why}")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
