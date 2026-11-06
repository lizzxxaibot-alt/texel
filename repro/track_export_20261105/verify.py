"""The 0.2.7 regression case @wenvikstudios proposed (ROADMAP v0.2.7), run on a
BUILT zip through the real operators, not on the source tree.

  blender --background --factory-startup --python verify.py -- <zip>

Two frames. Export Sheet with Base alone; add Torch and Glow, hide them with the
eye, step a frame (which in 0.2.6 switched them back on), export again. The two
sheets must match pixel for pixel. On a build with no track hide (0.2.6) the
eye is pressed on EVERY cel of each effect track, which is the most a 0.2.6
user could do. Must PASS on 0.2.7 and FAIL on 0.2.6 (the negative control).
"""
import sys, tempfile, zipfile
import bpy

ZIP = sys.argv[sys.argv.index("--") + 1]
EXT = tempfile.mkdtemp(prefix="texel_trk_")
zipfile.ZipFile(ZIP).extractall(EXT)
sys.path.insert(0, EXT)
import texel
texel.register()
from texel import tex_doc
print("ZIP", ZIP, "| blender", bpy.app.version_string, "| version", texel.bl_info["version"])

area = max(bpy.context.screen.areas, key=lambda a: a.width * a.height)
area.type = "IMAGE_EDITOR"
ctx = {"area": area, "region": next(r for r in area.regions if r.type == "WINDOW"),
       "space_data": area.spaces.active, "screen": bpy.context.screen,
       "window": bpy.context.window}
fails = []
def check(name, cond, detail=""):
    print(f"[{'ok  ' if cond else 'FAIL'}] {name}" + ("" if cond else f"  -> {detail}"))
    if not cond:
        fails.append(name)

with bpy.context.temp_override(**ctx):
    bpy.ops.texel.canvas_new(size=8, name="Reg")
    img = bpy.data.images["Reg"]
    area.spaces.active.image = img
    doc = tex_doc.get(img)
    c = doc.canvas
    bpy.ops.texel.frame_add()
    bpy.ops.texel.frame_add()
    base = c.add_colour((90, 60, 30, 255))
    for f in range(2):
        c.cel(c.tracks[0], f).set(1 + f, 2, base)

    def sheet():
        bpy.ops.texel.sprite_sheet(columns=0)
        return list(bpy.data.images["Reg Sheet"].pixels)

    alone = sheet()
    fire = c.add_colour((255, 140, 0, 255))
    for name in ("Torch", "Glow"):
        bpy.ops.texel.track_add(name=name)
        for f in range(2):
            c.cel(name, f).set(1 + f, 2, fire)
            c.cel(name, f).set(7, 7 - f, fire)
    check("shown effect tracks change the sheet", sheet() != alone)
    track_hide = hasattr(c, "set_track_visible")
    print("track-level hide in this build:", track_hide)
    for name in ("Torch", "Glow"):
        cels = [c.cel(name, 0)] if track_hide else [c.cel(name, f) for f in range(2)]
        for cel in cels:
            bpy.ops.texel.layer_toggle(index=c.layers.index(cel))
    bpy.ops.texel.frame_show(index=1)
    after = sheet()
    diff = sum(1 for a, b in zip(alone, after) if a != b)
    check("Base alone == Base with Torch and Glow hidden, pixel for pixel",
          after == alone, f"{diff} channel values differ")

    # the GIF goes through show_frame(), not flatten_frame(), so it is its own
    # path and gets its own check: no fire-orange texel in any GIF frame while
    # the tracks are hidden, and some when one is shown (the positive control)
    import glob, os, shutil, subprocess
    def gif_has_fire():
        out = tempfile.mkdtemp(prefix="texel_gif_")
        if bpy.ops.texel.export_gif(scale=1, directory=out) != {"FINISHED"}:
            return None
        gifs = glob.glob(os.path.join(out, "*.gif"))
        if not gifs:
            return None
        # Blender's Python has no PIL: decode the GIF back to PNG frames with
        # ffmpeg and read those through bpy
        subprocess.run([shutil.which("ffmpeg"), "-v", "error", "-i", gifs[0],
                        os.path.join(out, "dec_%03d.png")], check=True)
        hit, frames = False, 0
        for png in sorted(glob.glob(os.path.join(out, "dec_*.png"))):
            im = bpy.data.images.load(png)
            px = list(im.pixels)
            frames += 1
            for i in range(0, len(px), 4):
                if (abs(px[i] - 1.0) < 0.02 and abs(px[i + 1] - 140 / 255) < 0.03
                        and px[i + 2] < 0.02 and px[i + 3] > 0.5):
                    hit = True
                    break
            bpy.data.images.remove(im)
        print(f"  [gif] {os.path.basename(gifs[0])}: {frames} decoded frame(s), fire={hit}")
        shutil.rmtree(out, ignore_errors=True)
        return hit if frames else None
    if shutil.which("ffmpeg"):
        g_hidden = gif_has_fire()
        check("GIF: no hidden-track texel in any frame", g_hidden is False, g_hidden)
        if track_hide:
            bpy.ops.texel.layer_toggle(index=c.layers.index(c.cel("Glow", 0)))
        else:
            for f in range(2):
                bpy.ops.texel.layer_toggle(index=c.layers.index(c.cel("Glow", f)))
        g_shown = gif_has_fire()
        check("GIF: a shown track does reach the GIF (positive control)", g_shown is True, g_shown)
    else:
        print("[skip] GIF checks: ffmpeg not on PATH")

print()
if fails:
    print(f"{len(fails)} FAILED: {fails}")
else:
    print("TRACK EXPORT REGRESSION: ALL PASS")
