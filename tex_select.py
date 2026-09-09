"""Selection, clipboard and colour-adjustment operators."""
import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty, StringProperty
from bpy.types import Operator

from . import tex_doc
from .core import adjust as A
from .core.select import Clip, Selection

_CLIP: Clip | None = None


def _doc(context):
    sp = context.space_data
    img = sp.image if sp and sp.type == "IMAGE_EDITOR" else None
    return tex_doc.get(img, create=False) if img else None


def _sel(doc, make=True):
    if doc.canvas.selection is None and make:
        doc.canvas.selection = Selection(doc.canvas.w, doc.canvas.h)
    return doc.canvas.selection


class _DocOp(Operator):
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return _doc(context) is not None


# ------------------------------------------------------------------ selection
class TEXEL_OT_select_all(_DocOp):
    bl_idname = "texel.select_all"
    bl_label = "Select All"
    bl_description = "Select every texel on the canvas"

    def execute(self, context):
        d = _doc(context)
        _sel(d).select_all()
        self.report({"INFO"}, f"{d.canvas.selection.count()} texels selected")
        return {"FINISHED"}


class TEXEL_OT_deselect(_DocOp):
    bl_idname = "texel.deselect"
    bl_label = "Deselect"
    bl_description = "Clear the selection so tools affect the whole canvas again"

    def execute(self, context):
        d = _doc(context)
        if d.canvas.selection:
            d.canvas.selection.clear()
        return {"FINISHED"}


class TEXEL_OT_select_invert(_DocOp):
    bl_idname = "texel.select_invert"
    bl_label = "Invert Selection"
    bl_description = "Swap selected and unselected texels"

    def execute(self, context):
        d = _doc(context)
        _sel(d).invert()
        self.report({"INFO"}, f"{d.canvas.selection.count()} texels selected")
        return {"FINISHED"}


class TEXEL_OT_select_linked(_DocOp):
    bl_idname = "texel.select_linked"
    bl_label = "Select Linked"
    bl_description = "Magic wand: select the connected run of one colour"

    x: IntProperty(default=-1)
    y: IntProperty(default=-1)
    tolerance: IntProperty(name="Tolerance", default=0, min=0, max=255)

    def execute(self, context):
        d = _doc(context)
        if self.x < 0 or self.y < 0:
            self.report({"WARNING"}, "Run this from the canvas so it knows where to start")
            return {"CANCELLED"}
        layer = d.canvas.layers[d.canvas.active]
        _sel(d).select_linked(layer, self.x, self.y, self.tolerance)
        self.report({"INFO"}, f"{d.canvas.selection.count()} texels selected")
        return {"FINISHED"}


class TEXEL_OT_select_colour(_DocOp):
    bl_idname = "texel.select_colour"
    bl_label = "Select by Colour"
    bl_description = "Select every texel using the current paint colour, connected or not"

    def execute(self, context):
        from .tex_props import rgba_bytes
        d = _doc(context)
        want = rgba_bytes(context.scene.texel.colour)
        if want not in d.canvas.palette:
            self.report({"WARNING"}, "That colour is not in the palette yet")
            return {"CANCELLED"}
        idx = d.canvas.palette.index(want)
        _sel(d).select_same_colour(d.canvas.layers[d.canvas.active], idx)
        self.report({"INFO"}, f"{d.canvas.selection.count()} texels selected")
        return {"FINISHED"}


class TEXEL_OT_select_grow(_DocOp):
    bl_idname = "texel.select_grow"
    bl_label = "Grow / Shrink"
    bl_description = "Expand or contract the selection by whole texels"

    amount: IntProperty(name="Texels", default=1, min=-32, max=32)

    def execute(self, context):
        d = _doc(context)
        s = _sel(d)
        if s.is_empty():
            self.report({"WARNING"}, "Nothing selected")
            return {"CANCELLED"}
        s.grow(self.amount) if self.amount > 0 else s.shrink(-self.amount)
        self.report({"INFO"}, f"{s.count()} texels selected")
        return {"FINISHED"}


# ------------------------------------------------------------------ clipboard
class TEXEL_OT_clipboard_copy(_DocOp):
    bl_idname = "texel.clipboard_copy"
    bl_label = "Copy"
    bl_description = "Copy the selection, or the whole layer if nothing is selected"

    def execute(self, context):
        global _CLIP
        d = _doc(context)
        _CLIP = Clip.from_layer(d.canvas.layers[d.canvas.active],
                                d.canvas.selection, d.canvas.palette)
        if _CLIP is None:
            self.report({"WARNING"}, "Nothing to copy")
            return {"CANCELLED"}
        self.report({"INFO"}, f"Copied {_CLIP.w}x{_CLIP.h}")
        return {"FINISHED"}


class TEXEL_OT_clipboard_cut(_DocOp):
    bl_idname = "texel.clipboard_cut"
    bl_label = "Cut"
    bl_description = "Copy the selection then clear it"

    def execute(self, context):
        global _CLIP
        d = _doc(context)
        layer = d.canvas.layers[d.canvas.active]
        _CLIP = Clip.from_layer(layer, d.canvas.selection, d.canvas.palette)
        if _CLIP is None:
            self.report({"WARNING"}, "Nothing to cut")
            return {"CANCELLED"}
        sel = d.canvas.selection
        if sel and not sel.is_empty():
            for y in range(d.canvas.h):
                for x in range(d.canvas.w):
                    if (x, y) in sel:
                        layer.set(x, y, 0)
        else:
            layer.clear()
        d.flush()
        self.report({"INFO"}, f"Cut {_CLIP.w}x{_CLIP.h}")
        return {"FINISHED"}


class TEXEL_OT_clipboard_paste(_DocOp):
    bl_idname = "texel.clipboard_paste"
    bl_label = "Paste"
    bl_description = "Paste the clipboard into the active layer"

    x: IntProperty(name="X", default=0)
    y: IntProperty(name="Y", default=0)

    def execute(self, context):
        d = _doc(context)
        if _CLIP is None:
            self.report({"WARNING"}, "Clipboard is empty")
            return {"CANCELLED"}
        n = _CLIP.paste_into(d.canvas, d.canvas.layers[d.canvas.active], self.x, self.y)
        d.flush()
        self.report({"INFO"}, f"Pasted {n} texels")
        return {"FINISHED"}


# ---------------------------------------------------------------- adjustments
ADJUSTMENTS = [
    ("BRIGHTNESS", "Brightness", "Lighten or darken"),
    ("CONTRAST", "Contrast", "Push or pull from mid grey"),
    ("HUE", "Hue Shift", "Rotate hue in degrees"),
    ("SATURATION", "Saturation", "More or less colourful"),
    ("POSTERIZE", "Posterize", "Quantise to N levels per channel"),
    ("GREYSCALE", "Greyscale", "Rec.709 luma"),
    ("INVERT", "Invert", "Flip every channel"),
]


class TEXEL_OT_adjust(_DocOp):
    bl_idname = "texel.adjust"
    bl_label = "Adjust Colours"
    bl_description = ("Adjust the palette. On an indexed canvas this changes every "
                      "texel of those colours at once, at any canvas size")

    op: EnumProperty(name="Adjustment", items=ADJUSTMENTS, default="BRIGHTNESS")
    amount: FloatProperty(name="Amount", default=0.2, min=-1.0, max=1.0)
    degrees: FloatProperty(name="Degrees", default=30.0, min=-360.0, max=360.0)
    levels: IntProperty(name="Levels", default=4, min=2, max=32)
    selection_only: BoolProperty(
        name="Selection Only", default=False,
        description="Restrict to the palette indices the selection uses")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        col = self.layout.column()
        col.prop(self, "op")
        if self.op == "HUE":
            col.prop(self, "degrees")
        elif self.op == "POSTERIZE":
            col.prop(self, "levels")
        elif self.op not in {"GREYSCALE", "INVERT"}:
            col.prop(self, "amount")
        col.prop(self, "selection_only")

    def execute(self, context):
        d = _doc(context)
        amount = {"HUE": self.degrees, "POSTERIZE": self.levels}.get(self.op, self.amount)
        only = None
        if self.selection_only:
            sel = d.canvas.selection
            if sel is None or sel.is_empty():
                self.report({"WARNING"}, "Nothing selected")
                return {"CANCELLED"}
            only = A.indices_in(d.canvas.layers[d.canvas.active], sel)
        d.canvas.palette = A.apply_to_palette(d.canvas.palette, self.op, amount, only)
        d.flush()
        self.report({"INFO"}, f"{self.op.title()} applied to {len(d.canvas.palette) - 1} colours")
        return {"FINISHED"}


CLASSES = (TEXEL_OT_select_all, TEXEL_OT_deselect, TEXEL_OT_select_invert,
           TEXEL_OT_select_linked, TEXEL_OT_select_colour, TEXEL_OT_select_grow,
           TEXEL_OT_clipboard_copy, TEXEL_OT_clipboard_cut, TEXEL_OT_clipboard_paste,
           TEXEL_OT_adjust)


def register():
    for c in CLASSES:
        bpy.utils.register_class(c)


def unregister():
    global _CLIP
    _CLIP = None
    for c in reversed(CLASSES):
        bpy.utils.unregister_class(c)
