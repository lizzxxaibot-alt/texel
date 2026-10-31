"""@wenvikstudios 10-30: can Torch and Glow be exported as separate layers?
Runs the SHIPPED zip. Two frames, tracks Main + Glow, each painted a distinct
colour. Measures, per export path, whether hiding the Glow cels (the eye
toggle) or zeroing their opacity keeps Glow out of the output.

  TEXEL_ZIP=dist/texel-0.2.6.zip blender --background --factory-startup --python verify.py
"""
import os, sys, zipfile, tempfile
import bpy

ZIP = os.environ["TEXEL_ZIP"]
EXT = tempfile.mkdtemp(prefix="texel_trk_")
zipfile.ZipFile(ZIP).extractall(EXT)
sys.path.insert(0, EXT)
import texel
texel.register()
from texel import tex_doc
print(f"[env] blender {bpy.app.version_string}  zip {os.path.basename(ZIP)}  from {texel.__file__}")

W = 32
img = bpy.data.images.new("Hero", W, W, alpha=True)
img.pixels.foreach_set([0.0] * (W * W * 4)); img.update()
area = bpy.context.screen.areas[0]
area.type = "IMAGE_EDITOR"
area.spaces.active.image = img
region = next(r for r in area.regions if r.type == "WINDOW")
ctx = dict(area=area, region=region, space_data=area.spaces.active,
           screen=bpy.context.screen, window=bpy.context.window)
doc = tex_doc.get(img)
c = doc.canvas
RED = (200, 40, 40, 255); GOLD = (250, 200, 40, 255)
ri = c.add_colour(RED); gi = c.add_colour(GOLD)

def count(image, rgb):
    px = list(image.pixels)
    t = [v / 255 for v in rgb[:3]]
    return sum(1 for i in range(0, len(px), 4)
               if px[i + 3] > 0.5 and all(abs(px[i + k] - t[k]) < 0.02 for k in range(3)))

with bpy.context.temp_override(**ctx):
    bpy.ops.texel.frame_add(copy_previous=False)
    bpy.ops.texel.frame_add(copy_previous=False)
    first = c.tracks[0]
    bpy.ops.texel.track_add(name="Glow")
    print(f"[setup] tracks {c.tracks} frames {c.frame_count()} layers {[(l.name, l.track, l.frame) for l in c.layers]}")
    for f in range(2):
        for x in range(4, 12):
            for y in range(4, 12):
                c.cel(first, f).set(x, y, ri)
        for x in range(16, 20):
            for y in range(16, 20):
                c.cel("Glow", f).set(x, y, gi)
    bpy.ops.texel.frame_show(index=0); doc.flush()
    print(f"[0 baseline] displayed image: red {count(img, RED)} gold {count(img, GOLD)}")

    # 1. eye toggle on the Glow cel of the current frame
    gl = c.layers.index(c.cel("Glow", 0))
    bpy.ops.texel.layer_toggle(index=gl); doc.flush()
    print(f"[1 eye-hide Glow f0] cel visible={c.cel('Glow',0).visible}; displayed image: red {count(img, RED)} gold {count(img, GOLD)}")
    bpy.ops.texel.sprite_sheet(columns=0)
    sh = bpy.data.images["Hero Sheet"]
    print(f"[1 eye-hide Glow f0] Export Sprite Sheet {sh.size[0]}x{sh.size[1]}: red {count(sh, RED)} gold {count(sh, GOLD)}  (both frames' Glow = 32)")
    for f in range(2):
        c.cel("Glow", f).visible = False
    bpy.ops.texel.sprite_sheet(columns=0)
    sh = bpy.data.images["Hero Sheet"]
    print(f"[1b Glow hidden on both frames] Export Sprite Sheet: red {count(sh, RED)} gold {count(sh, GOLD)}")

    # 2. opacity 0 on every Glow cel
    for f in range(2):
        c.cel("Glow", f).opacity = 0.0
    bpy.ops.texel.sprite_sheet(columns=0)
    sh = bpy.data.images["Hero Sheet"]
    print(f"[2 Glow opacity 0] Export Sprite Sheet: red {count(sh, RED)} gold {count(sh, GOLD)}")
    # and the inverse: base off, Glow on -> lighting-only sheet
    for f in range(2):
        c.cel("Glow", f).opacity = 1.0; c.cel("Glow", f).visible = True
        c.cel(first, f).opacity = 0.0
    bpy.ops.texel.sprite_sheet(columns=0)
    sh = bpy.data.images["Hero Sheet"]
    print(f"[2b base opacity 0] Export Sprite Sheet: red {count(sh, RED)} gold {count(sh, GOLD)}")
    for f in range(2):
        c.cel(first, f).opacity = 1.0

    # 3. Layers to Images
    before = set(bpy.data.images.keys())
    bpy.ops.texel.export_layers()
    new = sorted(set(bpy.data.images.keys()) - before)
    print(f"[3 Layers to Images] {len(new)} images: " + "; ".join(
        f"{n}: red {count(bpy.data.images[n], RED)} gold {count(bpy.data.images[n], GOLD)}" for n in new))
print("DONE")
