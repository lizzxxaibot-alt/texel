"""T-028: does Texel Lite 0.2.6 need a fresh texel.paint invocation per stroke?
Extracts the SHIPPED zip to a temp dir (nothing installed into the user's
Blender), registers it, then drives TEXEL_OT_paint's own invoke/modal code with
synthetic events. texel_under_mouse is patched to map event x/y straight to
texels, since background mode has no viewport to raycast into."""
import bpy, sys, tempfile, zipfile, importlib
ZIP = sys.argv[sys.argv.index("--")+1]
EXT = tempfile.mkdtemp(prefix="texel_t028_"); zipfile.ZipFile(ZIP).extractall(EXT)
sys.path.insert(0, EXT)
import texel; texel.register()
print("LOADED", texel.__file__, "blender", bpy.app.version_string, "bl_info", texel.bl_info.get("version") if hasattr(texel, "bl_info") else "-")
from texel import tex_paint as P, tex_pick as PK, tex_keys as K, tex_doc as D

print("KEYMAP bindings for texel.paint:", [(b[0], b[3]) for b in K.BINDINGS if b[2] == "texel.paint"])
print("KEYMAP any mouse binding:", [b for b in K.BINDINGS if "MOUSE" in b[3]])

img = bpy.data.images.new("C", 16, 16, alpha=True)
img.pixels.foreach_set([0.0] * 16 * 16 * 4)
P.tex_pick.texel_under_mouse = lambda ctx, ev, w, h: (ev.x, ev.y)

class Ev:
    def __init__(s, t, v="NOTHING", x=0, y=0): s.type, s.value, s.x, s.y, s.pressure = t, v, x, y, 1.0
class WM:
    handlers = 0
    def modal_handler_add(s, op): WM.handlers += 1
class Sp: type = "IMAGE_EDITOR"; image = img
class Ctx:
    space_data = Sp(); scene = bpy.context.scene; window_manager = WM(); active_object = None
class Op:   # the operator's own methods on a plain object (bpy_struct can't be built by hand)
    invoke = P.TEXEL_OT_paint.invoke; modal = P.TEXEL_OT_paint.modal
    _image = P.TEXEL_OT_paint._image; _commit = P.TEXEL_OT_paint._commit; _shape = P.TEXEL_OT_paint._shape
    def report(s, *a): print("REPORT", a)
ctx = Ctx(); s = ctx.scene.texel; s.tool = "PENCIL"; s.colour = (1, 0, 0, 1)
lit = lambda: sum(1 for i in D.get(img).canvas.flatten() if i)

print("== stroke 1: invoke (D / Texel Paint), drag along row 2, release")
op = Op(); print("invoke ->", op.invoke(ctx, Ev("D", "PRESS", 1, 2)), "| modal handlers added:", WM.handlers)
for x in range(2, 8): op.modal(ctx, Ev("MOUSEMOVE", "NOTHING", x, 2))
r = op.modal(ctx, Ev("LEFTMOUSE", "RELEASE", 7, 2)); print("LMB release ->", r)
print("LIT after stroke 1:", lit())
print("== stroke 2 attempted with the mouse only, no re-invoke")
print("FINISHED removes the modal handler; keymap has no mouse entry; so no Texel code receives the drag.")
print("LIT after stroke-2 attempt:", lit(), "| handlers still", WM.handlers)
print("== stroke 2 with a second invoke")
op2 = Op(); print("invoke ->", op2.invoke(ctx, Ev("D", "PRESS", 1, 5)), "| handlers:", WM.handlers)
for x in range(2, 6): op2.modal(ctx, Ev("MOUSEMOVE", "NOTHING", x, 5))
print("LMB PRESS mid-stroke ->", op2.modal(ctx, Ev("LEFTMOUSE", "PRESS", 5, 5)))
print("LMB RELEASE ->", op2.modal(ctx, Ev("LEFTMOUSE", "RELEASE", 5, 5)))
print("LIT after stroke 2:", lit())
