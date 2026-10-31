"""Follow-up: the opacity-0 route through the operators a user clicks
(Show Frame -> select cel -> Layer Opacity), 3 frames, then Export Sprite Sheet,
and again after the user steps back through the frames."""
import os, sys, zipfile, tempfile
import bpy
ZIP = os.environ["TEXEL_ZIP"]
EXT = tempfile.mkdtemp(prefix="texel_trk2_"); zipfile.ZipFile(ZIP).extractall(EXT)
sys.path.insert(0, EXT)
import texel; texel.register()
from texel import tex_doc
W, N = 32, 3
img = bpy.data.images.new("Hero", W, W, alpha=True); img.pixels.foreach_set([0.0]*(W*W*4)); img.update()
area = bpy.context.screen.areas[0]; area.type = "IMAGE_EDITOR"; area.spaces.active.image = img
region = next(r for r in area.regions if r.type == "WINDOW")
ctx = dict(area=area, region=region, space_data=area.spaces.active, screen=bpy.context.screen, window=bpy.context.window)
doc = tex_doc.get(img); c = doc.canvas
GOLD = (250, 200, 40, 255); gi = c.add_colour(GOLD)
def gold(im):
    px = list(im.pixels); t = [v/255 for v in GOLD[:3]]
    return sum(1 for i in range(0, len(px), 4) if px[i+3] > .5 and all(abs(px[i+k]-t[k]) < .02 for k in range(3)))
with bpy.context.temp_override(**ctx):
    for _ in range(N): bpy.ops.texel.frame_add(copy_previous=False)
    bpy.ops.texel.track_add(name="Glow")
    for f in range(N):
        for x in range(16, 20):
            for y in range(16, 20): c.cel("Glow", f).set(x, y, gi)
    for f in range(N):
        bpy.ops.texel.frame_show(index=f)
        bpy.ops.texel.layer_select(index=c.layers.index(c.cel("Glow", f)))
        bpy.ops.texel.layer_opacity(value=0.0)
    print("[a] opacity after setting each frame:", [c.cel("Glow", f).opacity for f in range(N)])
    bpy.ops.texel.sprite_sheet(columns=0)
    print(f"[a] sheet straight after: gold {gold(bpy.data.images['Hero Sheet'])} (0 = Glow out)")
    for f in range(N): bpy.ops.texel.frame_show(index=f)
    print("[b] opacity after stepping through frames:", [c.cel("Glow", f).opacity for f in range(N)])
    bpy.ops.texel.sprite_sheet(columns=0)
    print(f"[b] sheet after stepping: gold {gold(bpy.data.images['Hero Sheet'])} of {16*N}")
