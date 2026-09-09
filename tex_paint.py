"""The modal paint operator. Every tool routes through one stroke pipeline."""
from __future__ import annotations
import bpy
from bpy.types import Operator

from . import tex_doc, tex_pick
from .core import raster as R
from .tex_props import rgba_bytes


_MASK_CACHE = {}


def _stamp(layer, x, y, idx, size, w, h, shape="SQUARE"):
    """Stamp the brush centred on (x, y). Masks are cached - a 32px round brush
    is 800 offsets and recomputing it per texel of a stroke is wasteful."""
    key = (size, shape)
    mask = _MASK_CACHE.get(key)
    if mask is None:
        mask = R.brush_mask(size, shape)
        _MASK_CACHE[key] = mask
    for dx, dy in mask:
        layer.set(x + dx, y + dy, idx)


def _mirrored(pts, w, h, mx, my):
    out = list(pts)
    if mx:
        out += [(w - 1 - x, y) for x, y in pts]
    if my:
        out += [(x, h - 1 - y) for x, y in pts]
    if mx and my:
        out += [(w - 1 - x, h - 1 - y) for x, y in pts]
    return out


class TEXEL_OT_paint(Operator):
    bl_idname = "texel.paint"
    bl_label = "Texel Paint"
    bl_description = "Paint pixel art onto the active canvas"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        sp = context.space_data
        if sp is None:
            return False
        if sp.type == "IMAGE_EDITOR":
            return sp.image is not None
        return sp.type == "VIEW_3D"

    # -- helpers -----------------------------------------------------------
    def _image(self, context):
        sp = context.space_data
        if sp.type == "IMAGE_EDITOR":
            return sp.image
        obj = context.active_object
        if obj is None or obj.type != "MESH":
            return None
        for slot in obj.material_slots:
            mat = slot.material
            if not mat or not mat.use_nodes:
                continue
            for node in mat.node_tree.nodes:
                if node.type == "TEX_IMAGE" and node.image is not None:
                    return node.image
        return None

    def _commit(self, context, pts):
        s = context.scene.texel
        layer = self.doc.canvas.layers[self.doc.canvas.active]
        w, h = self.doc.canvas.w, self.doc.canvas.h
        idx = 0 if s.tool == "ERASER" else self.colour_index
        for x, y in _mirrored(pts, w, h, s.mirror_x, s.mirror_y):
            _stamp(layer, x, y, idx, s.brush_size, w, h, s.brush_shape)
        self.doc.flush()

    # -- modal -------------------------------------------------------------
    def invoke(self, context, event):
        img = self._image(context)
        if img is None:
            self.report({"WARNING"}, "No canvas: open an image, or give the object an image texture")
            return {"CANCELLED"}
        self.doc = tex_doc.get(img)
        if self.doc.canvas.w != img.size[0] or self.doc.canvas.h != img.size[1]:
            self.doc = tex_doc.Doc(img)
            tex_doc._DOCS[img.name] = self.doc

        s = context.scene.texel
        w, h = self.doc.canvas.w, self.doc.canvas.h
        start = tex_pick.texel_under_mouse(context, event, w, h)
        if start is None:
            self.report({"INFO"}, "Cursor is not over the canvas")
            return {"CANCELLED"}

        # picker and fill are single-shot; no modal needed
        if s.tool == "PICK":
            flat = self.doc.canvas.flatten()
            i = flat[start[1] * w + start[0]]
            if i:
                r, g, b, a = self.doc.canvas.palette[i]
                s.colour = (r / 255, g / 255, b / 255, a / 255)
            return {"FINISHED"}

        self.colour_index = self.doc.canvas.add_colour(rgba_bytes(s.colour))

        if s.tool == "FILL":
            flat = self.doc.canvas.flatten()
            pal = self.doc.canvas.palette
            get = lambda x, y: pal[flat[y * w + x]]
            pts = R.flood_fill(get, w, h, start[0], start[1],
                               rgba_bytes(s.colour), s.tolerance, s.contiguous)
            self._commit(context, pts)
            return {"FINISHED"}

        self.start = start
        self.trail = [start]
        self.preview_undo = None
        if s.tool in {"PENCIL", "ERASER"}:
            self._commit(context, [start])
        else:
            # shapes preview against a snapshot we restore each mouse-move
            self.snapshot = bytearray(self.doc.canvas.layers[self.doc.canvas.active].px)
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        s = context.scene.texel
        w, h = self.doc.canvas.w, self.doc.canvas.h

        if event.type in {"RIGHTMOUSE", "ESC"}:
            if s.tool not in {"PENCIL", "ERASER"}:
                self.doc.canvas.layers[self.doc.canvas.active].px = self.snapshot
                self.doc.flush()
            return {"CANCELLED"}

        if event.type == "MOUSEMOVE":
            cur = tex_pick.texel_under_mouse(context, event, w, h)
            if cur is None:
                return {"RUNNING_MODAL"}
            if s.tool in {"PENCIL", "ERASER"}:
                if cur != self.trail[-1]:
                    # join the gap since the last event, then clean the joint.
                    # We filter the whole tail, not just the new segment: a
                    # corner can straddle two events, and filtering per-segment
                    # would leave exactly those joints behind.
                    seg = R.line(*self.trail[-1], *cur)
                    tail = self.trail[-2:] + seg[1:]
                    self.trail.extend(seg[1:])
                    self._commit(context, R.pixel_perfect(tail) if s.pixel_perfect else seg)
            else:
                layer = self.doc.canvas.layers[self.doc.canvas.active]
                layer.px = bytearray(self.snapshot)
                self._commit(context, self._shape(s, self.start, cur))
            return {"RUNNING_MODAL"}

        if event.type == "LEFTMOUSE" and event.value == "RELEASE":
            self.doc.flush()
            return {"FINISHED"}
        return {"RUNNING_MODAL"}

    def _shape(self, s, a, b):
        if s.tool == "LINE":
            pts = R.line(*a, *b)
            return R.pixel_perfect(pts) if s.pixel_perfect else pts
        if s.tool == "RECT":
            return R.rect(*a, *b, filled=s.filled)
        if s.tool == "ELLIPSE":
            # box form, not centre+radius: a drag defines a bounding box, and the
            # centre+radius form loses a texel on even spans
            return R.ellipse_box(a[0], a[1], b[0], b[1], filled=s.filled)
        return []


class TEXEL_OT_canvas_new(Operator):
    bl_idname = "texel.canvas_new"
    bl_label = "New Canvas"
    bl_description = "Create a pixel-art canvas image and open it here"
    bl_options = {"REGISTER", "UNDO"}

    size: bpy.props.IntProperty(name="Size", default=64, min=1, max=4096)
    name: bpy.props.StringProperty(name="Name", default="Texel Canvas")

    def execute(self, context):
        img = bpy.data.images.new(self.name, self.size, self.size, alpha=True)
        img.pixels.foreach_set([0.0] * (self.size * self.size * 4))
        img.update()
        tex_doc.get(img)
        if context.space_data and context.space_data.type == "IMAGE_EDITOR":
            context.space_data.image = img
        self.report({"INFO"}, f"Canvas {self.size}x{self.size} created")
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


CLASSES = (TEXEL_OT_paint, TEXEL_OT_canvas_new)


def register():
    for c in CLASSES:
        bpy.utils.register_class(c)


def unregister():
    for c in reversed(CLASSES):
        bpy.utils.unregister_class(c)
