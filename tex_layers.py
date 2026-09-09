"""Layer operators. Thin wrappers over core.canvas, which holds the real logic."""
import bpy
from bpy.types import Operator
from bpy.props import FloatProperty, IntProperty
from . import tex_doc


def _doc(context):
    sp = context.space_data
    img = sp.image if sp and sp.type == "IMAGE_EDITOR" else None
    return tex_doc.get(img, create=False) if img else None


class _LayerOp(Operator):
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return _doc(context) is not None


class TEXEL_OT_layer_add(_LayerOp):
    bl_idname = "texel.layer_add"
    bl_label = "Add Layer"

    def execute(self, context):
        _doc(context).canvas.add_layer()
        return {"FINISHED"}


class TEXEL_OT_layer_remove(_LayerOp):
    bl_idname = "texel.layer_remove"
    bl_label = "Remove Layer"

    def execute(self, context):
        d = _doc(context)
        if not d.canvas.remove_layer(d.canvas.active):
            self.report({"WARNING"}, "A canvas needs at least one layer")
            return {"CANCELLED"}
        d.flush()
        return {"FINISHED"}


class TEXEL_OT_layer_merge_down(_LayerOp):
    bl_idname = "texel.layer_merge_down"
    bl_label = "Merge Down"

    def execute(self, context):
        d = _doc(context)
        if not d.canvas.merge_down(d.canvas.active):
            self.report({"WARNING"}, "Nothing below to merge into")
            return {"CANCELLED"}
        d.flush()
        return {"FINISHED"}


class TEXEL_OT_layer_select(_LayerOp):
    bl_idname = "texel.layer_select"
    bl_label = "Select Layer"
    index: IntProperty()

    def execute(self, context):
        d = _doc(context)
        if 0 <= self.index < len(d.canvas.layers):
            d.canvas.active = self.index
        return {"FINISHED"}


class TEXEL_OT_layer_toggle(_LayerOp):
    bl_idname = "texel.layer_toggle"
    bl_label = "Toggle Visibility"
    index: IntProperty()

    def execute(self, context):
        d = _doc(context)
        if 0 <= self.index < len(d.canvas.layers):
            layer = d.canvas.layers[self.index]
            layer.visible = not layer.visible
            d.flush()
        return {"FINISHED"}


class TEXEL_OT_layer_opacity(_LayerOp):
    bl_idname = "texel.layer_opacity"
    bl_label = "Layer Opacity"
    bl_description = "Set the opacity of the active layer"
    value: FloatProperty(name="Opacity", default=1.0, min=0.0, max=1.0, subtype="FACTOR")

    def invoke(self, context, event):
        d = _doc(context)
        self.value = d.canvas.layers[d.canvas.active].opacity
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        d = _doc(context)
        d.canvas.layers[d.canvas.active].opacity = self.value
        d.flush()
        return {"FINISHED"}


CLASSES = (TEXEL_OT_layer_add, TEXEL_OT_layer_remove, TEXEL_OT_layer_merge_down,
           TEXEL_OT_layer_select, TEXEL_OT_layer_toggle,
           TEXEL_OT_layer_opacity)


def register():
    for c in CLASSES:
        bpy.utils.register_class(c)


def unregister():
    for c in reversed(CLASSES):
        bpy.utils.unregister_class(c)
