"""Layer groups, swatch editing, custom brushes, navigation, and the tools that
go past parity: dithered fill, selection outline, palette sort, canvas resize,
and spritesheet export.
"""
import bpy
from bpy.props import (BoolProperty, EnumProperty, FloatProperty, IntProperty,
                       StringProperty)
from bpy.types import Operator

from . import tex_doc
from .core import raster as R
from .core.canvas import Canvas
from .core.select import Selection
from .tex_props import rgba_bytes

_BRUSHES: dict[str, dict] = {}


def _doc(context):
    sp = context.space_data
    img = sp.image if sp and sp.type == "IMAGE_EDITOR" else None
    return tex_doc.get(img, create=False) if img else None


class _DocOp(Operator):
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return _doc(context) is not None


# ------------------------------------------------------------- layer groups
class TEXEL_OT_layer_duplicate(_DocOp):
    bl_idname = "texel.layer_duplicate"
    bl_label = "Duplicate Layer"

    def execute(self, context):
        d = _doc(context)
        if d.canvas.duplicate_layer(d.canvas.active) is None:
            return {"CANCELLED"}
        d.flush()
        return {"FINISHED"}


class TEXEL_OT_layer_group(_DocOp):
    bl_idname = "texel.layer_group"
    bl_label = "Group Layers"
    bl_description = "Tag the visible layers into a named group you can hide together"

    name: StringProperty(name="Group", default="Group")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        d = _doc(context)
        members = [i for i, l in enumerate(d.canvas.layers) if l.visible and l.group is None]
        if not d.canvas.group_layers(members, self.name):
            self.report({"WARNING"}, "No ungrouped visible layers")
            return {"CANCELLED"}
        self.report({"INFO"}, f"{len(members)} layers grouped as '{self.name}'")
        return {"FINISHED"}


class TEXEL_OT_layer_ungroup(_DocOp):
    bl_idname = "texel.layer_ungroup"
    bl_label = "Ungroup"

    name: StringProperty(name="Group", default="")

    def execute(self, context):
        d = _doc(context)
        name = self.name or (d.canvas.layers[d.canvas.active].group or "")
        if not name:
            self.report({"WARNING"}, "Active layer is not in a group")
            return {"CANCELLED"}
        n = d.canvas.ungroup(name)
        self.report({"INFO"}, f"{n} layers ungrouped")
        return {"FINISHED"}


class TEXEL_OT_layer_merge_selected(_DocOp):
    bl_idname = "texel.layer_merge_selected"
    bl_label = "Merge Visible"
    bl_description = "Merge every visible layer into the lowest visible one"

    def execute(self, context):
        d = _doc(context)
        vis = [i for i, l in enumerate(d.canvas.layers) if l.visible]
        if not d.canvas.merge_indices(vis):
            self.report({"WARNING"}, "Need at least two visible layers")
            return {"CANCELLED"}
        d.flush()
        self.report({"INFO"}, f"Merged {len(vis)} layers")
        return {"FINISHED"}


# ----------------------------------------------------------- swatch editing
class TEXEL_OT_swatch_add(_DocOp):
    bl_idname = "texel.swatch_add"
    bl_label = "Add Swatch"
    bl_description = "Add the current paint colour to the palette"

    def execute(self, context):
        d = _doc(context)
        try:
            i = d.canvas.add_colour(rgba_bytes(context.scene.texel.colour))
        except ValueError as e:
            self.report({"WARNING"}, str(e))
            return {"CANCELLED"}
        self.report({"INFO"}, f"Swatch {i}")
        return {"FINISHED"}


class TEXEL_OT_swatch_remove(_DocOp):
    bl_idname = "texel.swatch_remove"
    bl_label = "Remove Swatch"
    bl_description = "Remove a swatch. Texels using it become transparent"

    index: IntProperty(default=0)

    def execute(self, context):
        d = _doc(context)
        c = d.canvas
        if not (0 < self.index < len(c.palette)):
            return {"CANCELLED"}
        for layer in c.layers:
            for n, v in enumerate(layer.px):
                if v == self.index:
                    layer.px[n] = 0
                elif v > self.index:
                    layer.px[n] = v - 1          # keep indices contiguous
        c.palette.pop(self.index)
        d.flush()
        return {"FINISHED"}


class TEXEL_OT_palette_clear(_DocOp):
    bl_idname = "texel.palette_clear"
    bl_label = "Clear Swatches"
    bl_description = "Drop every swatch. The canvas is cleared too, since its indices would dangle"

    def execute(self, context):
        d = _doc(context)
        d.canvas.palette = [(0, 0, 0, 0)]
        for layer in d.canvas.layers:
            layer.clear()
        d.flush()
        self.report({"INFO"}, "Palette and canvas cleared")
        return {"FINISHED"}


class TEXEL_OT_palette_sort(_DocOp):
    bl_idname = "texel.palette_sort"
    bl_label = "Sort Palette"
    bl_description = "Sort swatches by hue or brightness so ramps sit together"

    by: EnumProperty(name="By", default="LUMA",
                     items=[("LUMA", "Brightness", "Dark to light"),
                            ("HUE", "Hue", "Around the colour wheel")])

    def execute(self, context):
        import colorsys
        d = _doc(context)
        c = d.canvas
        body = c.palette[1:]
        if len(body) < 2:
            return {"CANCELLED"}
        def key(rgba):
            r, g, b, _a = rgba
            if self.by == "LUMA":
                return 0.2126 * r + 0.7152 * g + 0.0722 * b
            return colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)[0]
        order = sorted(range(len(body)), key=lambda i: key(body[i]))
        remap = {0: 0}
        for new_i, old_i in enumerate(order):
            remap[old_i + 1] = new_i + 1
        c.palette = [(0, 0, 0, 0)] + [body[i] for i in order]
        for layer in c.layers:
            for n, v in enumerate(layer.px):
                layer.px[n] = remap.get(v, 0)
        d.flush()
        self.report({"INFO"}, f"Sorted {len(body)} swatches by {self.by.lower()}")
        return {"FINISHED"}


# ------------------------------------------------------------ custom brushes
class TEXEL_OT_custom_brush_add(_DocOp):
    bl_idname = "texel.custom_brush_add"
    bl_label = "Save Custom Brush"
    bl_description = "Save the current selection as a reusable stamp"

    name: StringProperty(name="Name", default="Brush")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        d = _doc(context)
        sel = d.canvas.selection
        if sel is None or sel.is_empty():
            self.report({"WARNING"}, "Select the texels you want to save first")
            return {"CANCELLED"}
        box = sel.bounds()
        x0, y0, x1, y1 = box
        layer = d.canvas.layers[d.canvas.active]
        pts = [(x - x0, y - y0) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)
               if (x, y) in sel and layer.get(x, y)]
        _BRUSHES[self.name] = {"w": x1 - x0 + 1, "h": y1 - y0 + 1, "pts": pts}
        self.report({"INFO"}, f"Brush '{self.name}': {len(pts)} texels")
        return {"FINISHED"}


class TEXEL_OT_custom_brush_remove(_DocOp):
    bl_idname = "texel.custom_brush_remove"
    bl_label = "Remove Custom Brush"

    name: StringProperty(name="Name", default="")

    def execute(self, context):
        if _BRUSHES.pop(self.name, None) is None:
            self.report({"WARNING"}, f"No brush called '{self.name}'")
            return {"CANCELLED"}
        return {"FINISHED"}


# ----------------------------------------------------------------- navigation
class TEXEL_OT_show_canvas(Operator):
    bl_idname = "texel.show_canvas"
    bl_label = "Show in Image Editor"
    bl_description = "Open the active object's texture in an Image Editor"
    bl_options = {"REGISTER"}

    def execute(self, context):
        from .tex_density import _active_mesh
        obj = _active_mesh(context)
        img = None
        if obj:
            for slot in obj.material_slots:
                mat = slot.material
                if mat and mat.use_nodes:
                    for n in mat.node_tree.nodes:
                        if n.type == "TEX_IMAGE" and n.image:
                            img = n.image
                            break
        if img is None:
            self.report({"WARNING"}, "No image texture on the active object")
            return {"CANCELLED"}
        for area in context.screen.areas:
            if area.type == "IMAGE_EDITOR":
                area.spaces.active.image = img
                tex_doc.get(img)
                self.report({"INFO"}, f"Showing {img.name}")
                return {"FINISHED"}
        self.report({"INFO"}, "No Image Editor open - use the Texel workspace")
        return {"CANCELLED"}


class TEXEL_OT_show_in_3d(Operator):
    bl_idname = "texel.show_in_3d"
    bl_label = "Show in 3D Viewport"
    bl_description = "Frame the object that uses this canvas"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return _doc(context) is not None

    def execute(self, context):
        d = _doc(context)
        target = None
        for obj in context.scene.objects:
            if obj.type != "MESH":
                continue
            for slot in obj.material_slots:
                mat = slot.material
                if mat and mat.use_nodes:
                    for n in mat.node_tree.nodes:
                        if n.type == "TEX_IMAGE" and n.image == d.image:
                            target = obj
                            break
        if target is None:
            self.report({"WARNING"}, "No object uses this canvas")
            return {"CANCELLED"}
        bpy.ops.object.select_all(action="DESELECT")
        target.select_set(True)
        context.view_layer.objects.active = target
        self.report({"INFO"}, f"Selected {target.name}")
        return {"FINISHED"}


class TEXEL_OT_pick_texture(Operator):
    bl_idname = "texel.pick_texture"
    bl_label = "Paint On This Texture"
    bl_description = "Make the active object's texture the canvas"
    bl_options = {"REGISTER"}

    def execute(self, context):
        return bpy.ops.texel.show_canvas()


class TEXEL_OT_clear_report(Operator):
    bl_idname = "texel.clear_report"
    bl_label = "Dismiss"
    bl_description = "Clear the status line"
    bl_options = {"REGISTER"}

    def execute(self, context):
        context.scene.texel.status = ""
        return {"FINISHED"}


# ------------------------------------------------------ past parity: new tools
class TEXEL_OT_dither_fill(_DocOp):
    bl_idname = "texel.dither_fill"
    bl_label = "Dither Fill"
    bl_description = ("Fill the selection with a checker of two colours - the classic "
                      "pixel-art gradient, and something the reference has no operator for")

    density: EnumProperty(
        name="Pattern", default="CHECKER",
        items=[("CHECKER", "50%", "Alternating texels"),
               ("QUARTER", "25%", "Every fourth texel"),
               ("THREE", "75%", "Three of four texels")])
    second: IntProperty(name="Second Swatch", default=0, min=0)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        d = _doc(context)
        c = d.canvas
        sel = c.selection
        if sel is None or sel.is_empty():
            self.report({"WARNING"}, "Select an area to fill")
            return {"CANCELLED"}
        primary = c.add_colour(rgba_bytes(context.scene.texel.colour))
        other = self.second if 0 <= self.second < len(c.palette) else 0
        layer = c.layers[c.active]
        n = 0
        for y in range(c.h):
            for x in range(c.w):
                if (x, y) not in sel:
                    continue
                if self.density == "CHECKER":
                    hit = (x + y) % 2 == 0
                elif self.density == "QUARTER":
                    hit = (x % 2 == 0) and (y % 2 == 0)
                else:
                    hit = not ((x % 2 == 1) and (y % 2 == 1))
                layer.set(x, y, primary if hit else other)
                n += 1
        d.flush()
        self.report({"INFO"}, f"Dithered {n} texels")
        return {"FINISHED"}


class TEXEL_OT_selection_outline(_DocOp):
    bl_idname = "texel.selection_outline"
    bl_label = "Outline Selection"
    bl_description = "Draw a 1px border around the selection in the current colour"

    def execute(self, context):
        d = _doc(context)
        sel = d.canvas.selection
        if sel is None or sel.is_empty():
            self.report({"WARNING"}, "Nothing selected")
            return {"CANCELLED"}
        idx = d.canvas.add_colour(rgba_bytes(context.scene.texel.colour))
        layer = d.canvas.layers[d.canvas.active]
        pts = sel.outline()
        for x, y in pts:
            layer.set(x, y, idx)
        d.flush()
        self.report({"INFO"}, f"Outlined {len(pts)} texels")
        return {"FINISHED"}


class TEXEL_OT_canvas_resize(_DocOp):
    bl_idname = "texel.canvas_resize"
    bl_label = "Resize Canvas"
    bl_description = "Change the canvas size, scaling texels by whole numbers so they stay square"

    size: IntProperty(name="New Size", default=128, min=8, max=4096)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        d = _doc(context)
        old = d.canvas
        new = Canvas(self.size, self.size)
        new.palette = list(old.palette)
        # Carry the cel model across. Rebuilding layers WITHOUT track and frame
        # silently destroyed every frame and track in the document - three
        # frames of animation became a still image with no warning and no undo
        # that made sense. Found by the end-to-end suite; it is the worst class
        # of bug this product could ship, because the loss is invisible until
        # you look for the work you already did.
        new.tracks = list(getattr(old, "tracks", []))
        holds = getattr(old, "frame_holds", None)
        if isinstance(holds, list):
            new.frame_holds = list(holds)
        sx = self.size / old.w
        sy = self.size / old.h
        new.layers = []
        for src in old.layers:
            dst = type(src)(src.name, self.size, self.size, src.group,
                            src.track, src.frame)
            dst.visible, dst.opacity, dst.locked = src.visible, src.opacity, src.locked
            for y in range(self.size):
                for x in range(self.size):
                    dst.px[y * self.size + x] = src.get(int(x / sx), int(y / sy))
            new.layers.append(dst)
        new.active = min(old.active, len(new.layers) - 1)
        img = d.image
        img.scale(self.size, self.size)
        d.canvas = new
        d.flush()
        self.report({"INFO"}, f"Canvas is now {self.size}x{self.size}")
        return {"FINISHED"}


CLASSES = (TEXEL_OT_layer_duplicate, TEXEL_OT_layer_group, TEXEL_OT_layer_ungroup,
           TEXEL_OT_layer_merge_selected, TEXEL_OT_swatch_add, TEXEL_OT_swatch_remove,
           TEXEL_OT_palette_clear, TEXEL_OT_palette_sort, TEXEL_OT_custom_brush_add,
           TEXEL_OT_custom_brush_remove, TEXEL_OT_show_canvas, TEXEL_OT_show_in_3d,
           TEXEL_OT_pick_texture, TEXEL_OT_clear_report, TEXEL_OT_dither_fill,
           TEXEL_OT_selection_outline, TEXEL_OT_canvas_resize)


def register():
    for c in CLASSES:
        bpy.utils.register_class(c)


def unregister():
    _BRUSHES.clear()
    for c in reversed(CLASSES):
        bpy.utils.unregister_class(c)
