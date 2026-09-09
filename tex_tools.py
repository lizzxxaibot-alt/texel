"""Operators past parity, plus the last two parity items."""
import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty
from bpy.types import Operator

from . import tex_doc
from .core import tools as T
from .tex_props import rgba_bytes


def _doc(context):
    sp = context.space_data
    img = sp.image if sp and sp.type == "IMAGE_EDITOR" else None
    return tex_doc.get(img, create=False) if img else None


class _DocOp(Operator):
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return _doc(context) is not None


class TEXEL_OT_outline_sprite(_DocOp):
    bl_idname = "texel.outline_sprite"
    bl_label = "Outline Sprite"
    bl_description = "Ring every opaque shape on this layer with the current colour"

    diagonal: BoolProperty(name="Include Diagonals", default=False)

    def execute(self, context):
        d = _doc(context)
        layer = d.canvas.layers[d.canvas.active]
        pts = T.outline_points(layer, self.diagonal)
        if not pts:
            self.report({"WARNING"}, "Layer is empty or already full")
            return {"CANCELLED"}
        idx = d.canvas.add_colour(rgba_bytes(context.scene.texel.colour))
        for x, y in pts:
            layer.set(x, y, idx)
        d.flush()
        self.report({"INFO"}, f"Outlined with {len(pts)} texels")
        return {"FINISHED"}


class TEXEL_OT_shift_wrap(_DocOp):
    bl_idname = "texel.shift_wrap"
    bl_label = "Shift (Wrap)"
    bl_description = "Offset the layer with wraparound. Shift by half to expose a tiling seam"

    dx: IntProperty(name="X", default=0)
    dy: IntProperty(name="Y", default=0)
    half: BoolProperty(name="Half Canvas", default=True,
                       description="Ignore X/Y and shift by exactly half, the seam test")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        d = _doc(context)
        c = d.canvas
        dx, dy = (c.w // 2, c.h // 2) if self.half else (self.dx, self.dy)
        layer = c.layers[c.active]
        layer.px = T.shift_wrap(layer.px, c.w, c.h, dx, dy)
        d.flush()
        self.report({"INFO"}, f"Shifted by ({dx}, {dy}) with wrap")
        return {"FINISHED"}


class TEXEL_OT_check_tileable(_DocOp):
    bl_idname = "texel.check_tileable"
    bl_label = "Check Tiling"
    bl_description = ("Measure whether this texture tiles seamlessly. Nothing in a "
                      "general paint tool tells you this, and every game texture needs it")

    def execute(self, context):
        d = _doc(context)
        c = d.canvas
        r = T.tile_seam_score(c.flatten(), c.w, c.h, c.palette)
        if r["seamless"]:
            msg = "Seamless: both edge pairs match exactly"
        else:
            msg = (f"{r['score']}% - wrap edge changes by {r['h_wrap']:.0f}/"
                   f"{r['v_wrap']:.0f} vs the texture's own worst "
                   f"{r['h_worst']:.0f}/{r['v_worst']:.0f} (h/v)")
        context.scene.texel.status = msg
        self.report({"INFO"} if r["seamless"] else {"WARNING"}, msg)
        return {"FINISHED"}


class TEXEL_OT_flip_canvas(_DocOp):
    bl_idname = "texel.flip_canvas"
    bl_label = "Flip"
    bl_description = "Mirror the active layer"

    axis: EnumProperty(name="Axis", default="H",
                       items=[("H", "Horizontal", ""), ("V", "Vertical", "")])

    def execute(self, context):
        d = _doc(context)
        c = d.canvas
        layer = c.layers[c.active]
        layer.px = T.flip(layer.px, c.w, c.h, self.axis == "H")
        d.flush()
        return {"FINISHED"}


class TEXEL_OT_rotate_canvas(_DocOp):
    bl_idname = "texel.rotate_canvas"
    bl_label = "Rotate 90"
    bl_description = "Rotate the active layer a quarter turn"

    clockwise: BoolProperty(name="Clockwise", default=True)

    def execute(self, context):
        d = _doc(context)
        c = d.canvas
        if c.w != c.h:
            self.report({"WARNING"}, "Rotate needs a square canvas")
            return {"CANCELLED"}
        layer = c.layers[c.active]
        layer.px, _w, _h = T.rotate90(layer.px, c.w, c.h, self.clockwise)
        d.flush()
        return {"FINISHED"}


class TEXEL_OT_palette_ramp(_DocOp):
    bl_idname = "texel.palette_ramp"
    bl_label = "Generate Ramp"
    bl_description = ("Build a shading ramp from the current colour, shifting hue toward "
                      "blue in shadow and yellow in light instead of fading to grey")

    steps: IntProperty(name="Steps", default=5, min=2, max=16)
    hue_shift: FloatProperty(name="Hue Shift", default=-12.0, min=-90.0, max=90.0)
    sat_boost: FloatProperty(name="Midtone Saturation", default=0.18, min=0.0, max=1.0)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        d = _doc(context)
        ramp = T.make_ramp(rgba_bytes(context.scene.texel.colour), self.steps,
                           self.hue_shift, self.sat_boost)
        added = 0
        for rgba in ramp:
            try:
                d.canvas.add_colour(rgba)
                added += 1
            except ValueError:
                self.report({"WARNING"}, "Palette is full")
                break
        d.flush()
        self.report({"INFO"}, f"Added a {added}-step ramp")
        return {"FINISHED"}


class TEXEL_OT_replace_colour(_DocOp):
    bl_idname = "texel.replace_colour"
    bl_label = "Replace Colour"
    bl_description = "Swap one swatch for the current colour everywhere it appears"

    index: IntProperty(name="Swatch", default=1, min=1)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        d = _doc(context)
        c = d.canvas
        if not (0 < self.index < len(c.palette)):
            self.report({"WARNING"}, "No such swatch")
            return {"CANCELLED"}
        c.replace_colour(self.index, rgba_bytes(context.scene.texel.colour))
        d.flush()
        self.report({"INFO"}, f"Swatch {self.index} replaced across the canvas")
        return {"FINISHED"}


class TEXEL_OT_symmetry_center(Operator):
    bl_idname = "texel.symmetry_center"
    bl_label = "Center Mirror"
    bl_description = "Put the mirror axes back on the canvas centre"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        s = context.scene.texel
        s.mirror_x = False
        s.mirror_y = False
        self.report({"INFO"}, "Mirror axes reset to centre")
        return {"FINISHED"}


class TEXEL_OT_shortcuts_restore(Operator):
    bl_idname = "texel.shortcuts_restore"
    bl_label = "Restore Defaults"
    bl_description = "Reset Texel's tool settings to their defaults"
    bl_options = {"REGISTER"}

    def execute(self, context):
        s = context.scene.texel
        s.tool = "PENCIL"
        s.brush_size = 1
        s.pixel_perfect = True
        s.filled = False
        s.tolerance = 0
        s.contiguous = True
        s.mirror_x = False
        s.mirror_y = False
        self.report({"INFO"}, "Defaults restored")
        return {"FINISHED"}


class TEXEL_OT_export_layers(_DocOp):
    bl_idname = "texel.export_layers"
    bl_label = "Layers to Images"
    bl_description = "Split each layer into its own Blender image, for spritesheet work"

    def execute(self, context):
        d = _doc(context)
        c = d.canvas
        made = 0
        for layer in c.layers:
            tmp = type(c)(c.w, c.h)
            tmp.palette = list(c.palette)
            tmp.layers = [layer]
            img = bpy.data.images.new(f"{d.image_name} - {layer.name}", c.w, c.h, alpha=True)
            img.pixels.foreach_set(tmp.to_blender_floats())
            img.update()
            made += 1
        self.report({"INFO"}, f"{made} layer images created")
        return {"FINISHED"}


CLASSES = (TEXEL_OT_outline_sprite, TEXEL_OT_shift_wrap, TEXEL_OT_check_tileable,
           TEXEL_OT_flip_canvas, TEXEL_OT_rotate_canvas, TEXEL_OT_palette_ramp,
           TEXEL_OT_replace_colour, TEXEL_OT_symmetry_center,
           TEXEL_OT_shortcuts_restore, TEXEL_OT_export_layers)


def register():
    for c in CLASSES:
        bpy.utils.register_class(c)


def unregister():
    for c in reversed(CLASSES):
        bpy.utils.unregister_class(c)
