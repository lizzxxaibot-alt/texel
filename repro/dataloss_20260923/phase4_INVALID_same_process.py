"""Phase 4: the same loss, driven entirely through SHIPPED OPERATORS in a real
GUI Blender - paint, pack, save, reopen, then the add-on's own documented
're-enter your texture' operator (texel.show_canvas / 'Paint On This Texture')
followed by one dither_fill stroke.
"""
import os, sys
import bpy

WORK = os.environ["TEXEL_WORK"]
sys.path.insert(0, os.path.join(WORK, "addon"))
import texel; texel.register()
from texel import tex_doc

W = H = 32
RED = (255, 0, 0, 255)
LOG = []

def census(img, tag):
    buf = [0.0] * (W * H * 4)
    img.pixels.foreach_get(buf)
    counts = {}
    for i in range(W * H):
        o = i * 4
        k = tuple(round(buf[o + j] * 255) for j in range(4))
        counts[k] = counts.get(k, 0) + 1
    red = counts.get(RED, 0)
    line = f"[{tag}] red={red} distinct={len(counts)} top={sorted(counts.items(), key=lambda kv:-kv[1])[:2]}"
    print(line, flush=True); LOG.append(line)
    return red

def win():  return bpy.context.window_manager.windows[0]
def area(t):
    return max((a for a in win().screen.areas if a.type == t),
               key=lambda a: a.width * a.height, default=None)

def run():
    try:
        for o in list(bpy.data.objects):
            bpy.data.objects.remove(o, do_unlink=True)

        v3d = area("VIEW_3D")
        region = next(r for r in v3d.regions if r.type == "WINDOW")
        with bpy.context.temp_override(window=win(), screen=win().screen, area=v3d,
                                       region=region, space_data=v3d.spaces.active):
            bpy.ops.texel.add_cube(size=1.0, texture=32)

        img = bpy.data.images["Pixel Cube Texture"]
        d = tex_doc.get(img); c = d.canvas
        ri = c.add_colour(RED)
        for y in range(8, 24):
            for x in range(8, 24):
                c.layers[c.active].set(x, y, ri)
        d.flush()
        census(img, "1 painted")

        img.pack()
        blend = os.path.join(WORK, "gui.blend")
        bpy.ops.wm.save_as_mainfile(filepath=blend)
        bpy.ops.wm.open_mainfile(filepath=blend)
        img = bpy.data.images["Pixel Cube Texture"]
        census(img, "2 reopened (packed)")

        # --- re-enter the texture the way the add-on tells you to
        v3d = area("VIEW_3D")
        v3d.type = "IMAGE_EDITOR"
        ie = area("IMAGE_EDITOR")
        bpy.context.view_layer.objects.active = bpy.data.objects["Pixel Cube"]
        reg = next(r for r in ie.regions if r.type == "WINDOW")
        with bpy.context.temp_override(window=win(), screen=win().screen, area=ie,
                                       region=reg, space_data=ie.spaces.active):
            r = bpy.ops.texel.pick_texture()
            LOG.append(f"[op] texel.pick_texture -> {r}")
            print(LOG[-1], flush=True)
            doc = tex_doc.get(ie.spaces.active.image, create=False)
            nz = sum(1 for v in doc.canvas.layers[0].px if v) if doc else None
            LOG.append(f"[op] doc after pick_texture: exists={doc is not None} nonzero_px={nz}")
            print(LOG[-1], flush=True)
            census(img, "3 after pick_texture")
            bpy.ops.texel.select_all()
            r2 = bpy.ops.texel.dither_fill(density="QUARTER", second=0)
            LOG.append(f"[op] texel.dither_fill -> {r2}")
            print(LOG[-1], flush=True)
        red = census(img, "4 after dither_fill")
        LOG.append(f"RESULT final_red={red}")
        print(LOG[-1], flush=True)
    except Exception as e:
        import traceback; traceback.print_exc()
        LOG.append(f"ERROR {e}")
    with open(os.path.join(WORK, "phase4.log"), "w") as f:
        f.write("\n".join(LOG))
    bpy.ops.wm.quit_blender()

bpy.app.timers.register(run, first_interval=1.0)
