import sys, os, tempfile, zipfile, shutil, glob
import bpy
args = sys.argv[sys.argv.index("--")+1:]
ZIP, HERE, OUT = args
EXT = tempfile.mkdtemp(prefix="texel_hide_")
zipfile.ZipFile(ZIP).extractall(EXT)
sys.path.insert(0, EXT); sys.path.insert(1, HERE)
import texel
texel.register()
from texel import tex_doc
import demo_art as A
print("version", texel.bl_info["version"], "file", texel.__file__)
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
bpy.ops.texel.canvas_new(size=A.SIZE, name="Torchbearer")
img = bpy.data.images["Torchbearer"]
area = bpy.context.screen.areas[0]; area.type = "IMAGE_EDITOR"; area.spaces.active.image = img
region = next(r for r in area.regions if r.type == "WINDOW")
ctx = dict(area=area, region=region, space_data=area.spaces.active, screen=bpy.context.screen, window=bpy.context.window)
c = tex_doc.get(img).canvas
P = A.palette(c)
FR = 8
def sheet(tag):
    d = tempfile.mkdtemp(prefix="sheet_")
    r = bpy.ops.texel.export_anim_data(columns=4, directory=d)
    print(tag, r, bpy.context.scene.texel.status)
    pngs = glob.glob(os.path.join(d, "*.png"))
    print(tag, pngs)
    dst = os.path.join(OUT, f"sheet_{tag}.png"); shutil.copy(pngs[0], dst); return dst
with bpy.context.temp_override(**ctx):
    for _ in range(FR): bpy.ops.texel.frame_add(copy_previous=False)
    bpy.ops.texel.track_add(name="Cave", bottom=True)
    bpy.ops.texel.track_add(name="Torch")
    bpy.ops.texel.track_add(name="Glow")
    for _ in range(2): bpy.ops.texel.track_move(name="Glow", delta=-1)
    assert c.tracks == list(A.TRACKS), c.tracks
    for f in range(FR):
        cels = {t: c.cel(t, f) for t in A.TRACKS}
        for t in A.TRACKS:
            c.active = c.layers.index(cels[t]); A.DRAW[t](cels, P, f)
    for i, h in enumerate((2,1,1,1,2,1,1,1)): bpy.ops.texel.frame_hold(index=i, hold=h)
    print("tracks", c.tracks, "has set_track_visible", hasattr(c, "set_track_visible"))
    sheet("all")
    for name in ("Torch", "Glow"):
        bpy.ops.texel.layer_toggle(index=c.layers.index(c.cel(name, 0)))
    bpy.ops.texel.frame_show(index=3)   # step a frame: 0.2.6 switched hidden cels back on here
    sheet("hidden")
print("DONE")
