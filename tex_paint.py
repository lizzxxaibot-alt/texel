"""The modal paint operator. Every tool routes through one stroke pipeline."""
from __future__ import annotations
import bpy
from bpy.types import Operator

from . import tex_doc, tex_pick
from .core import raster as R
from .core.select import Clip
from .tex_props import rgba_bytes


_MASK_CACHE = {}


def _stamp(layer, x, y, idx, size, w, h, shape="SQUARE", dither="OFF", level=8):
    """Stamp the brush centred on (x, y). Masks are cached - a 32px round brush
    is 800 offsets and recomputing it per texel of a stroke is wasteful.

    Dither is tested per stamped texel at its canvas position, not per stroke
    point, so a wide brush dithers inside itself and the texels it skips keep
    whatever was under them."""
    key = (size, shape)
    mask = _MASK_CACHE.get(key)
    if mask is None:
        mask = R.brush_mask(size, shape)
        _MASK_CACHE[key] = mask
    for dx, dy in mask:
        if dither == "OFF" or R.dither_hit(dither, x + dx, y + dy, level):
            layer.set(x + dx, y + dy, idx)




def stroke_points(s, pts, w, h):
    """Every texel a stroke touches, after mirror and radial symmetry.

    Module level on purpose. A registered Operator cannot be instantiated from
    Python - `TEXEL_OT_paint()` raises `bpy_struct.__new__(struct): expected a
    single argument` - so a test cannot reach `_commit` directly, and an
    uncaught raise there makes Blender quit with status 0 and no summary line.
    Reading the scene properties here instead is what a headless suite can call
    with a real property group.
    """
    return R.symmetry_points(pts, w, h, s.mirror_x, s.mirror_y, s.symmetry)


_STAMP_CACHE = {}


def saved_stamp(s):
    """The scene's selected stamp as (dx, dy, rgba) offsets, or None.

    Decoded once per distinct saved string, not once per mouse event. A
    damaged string reads as no stamp, so the brush falls back to a square
    rather than painting garbage or raising inside the modal handler."""
    item = s.stamps.get(s.stamp) if s.stamp else None
    if item is None:
        return None
    offs = _STAMP_CACHE.get(item.data)
    if offs is None:
        try:
            clip = Clip.decode(item.data)
        except ValueError:
            return None
        offs = [(dx, dy, clip.palette[v]) for dx, dy, v in clip.offsets()]
        _STAMP_CACHE[item.data] = offs
    return offs


def commit_stroke(doc, s, pts, idx, pressure=1.0):
    """Stamp `pts` onto the active layer with the scene's brush and flush.

    The body of `_commit`, at module level for the same reason as
    `stroke_points`: it is the only way a test reaches the real write path.
    `pressure` only narrows the brush when the Pressure toggle is on."""
    layer = doc.canvas.layers[doc.canvas.active]
    w, h = doc.canvas.w, doc.canvas.h
    # fill hands over every texel of a region; stamping a pattern on each of
    # them would smear it, so fill keeps the plain brush
    offs = saved_stamp(s) if s.brush_shape == "STAMP" and s.tool != "FILL" else None
    if offs is not None:
        # a stamp paints its own colours; the eraser (idx 0) rubs out its
        # footprint. Colours join this canvas's palette once per stroke.
        remap = {rgba: (doc.canvas.add_colour(rgba) if idx else 0)
                 for _, _, rgba in offs}
        for x, y in stroke_points(s, pts, w, h):
            for dx, dy, rgba in offs:
                if s.dither == "OFF" or R.dither_hit(s.dither, x + dx, y + dy, s.dither_level):
                    layer.set(x + dx, y + dy, remap[rgba])
        doc.flush()
        return
    size = R.pressure_size(s.brush_size, pressure) if s.use_pressure else s.brush_size
    for x, y in stroke_points(s, pts, w, h):
        _stamp(layer, x, y, idx, size, w, h, s.brush_shape,
               s.dither, s.dither_level)
    doc.flush()


# The running paint mode, if any: {"token": object, "area": area pointer}.
# One per Blender session. A second Texel Paint (button or D) in the same
# editor leaves the mode; in another editor it moves the mode there.
_SESSION: dict = {}

HINT = "Texel Paint: left-drag paints  |  Esc, D or the Texel Paint button to stop"


def paint_mode_on(area=None) -> bool:
    """True while Texel Paint mode runs (in `area`, when one is given)."""
    if not _SESSION:
        return False
    return area is None or _SESSION.get("area") == area.as_pointer()


def over_canvas(area, region, mx, my) -> bool:
    """Is window point (mx, my) on the drawing region, and not on a panel?

    With region overlap the sidebar and toolbar sit ON TOP of the main region,
    so being inside the main region's box is not enough: a click on a sidebar
    button would otherwise paint the texel underneath it."""
    if not (region.x <= mx < region.x + region.width
            and region.y <= my < region.y + region.height):
        return False
    for r in area.regions:
        if r.type == "WINDOW" or r.width <= 1 or r.height <= 1:
            continue
        if r.x <= mx < r.x + r.width and r.y <= my < r.y + r.height:
            return False
    return True


class TEXEL_OT_paint(Operator):
    bl_idname = "texel.paint"
    bl_label = "Texel Paint"
    bl_description = ("Enter Texel Paint mode: left-drag paints on the canvas until "
                      "you press Esc, D, or this button again")
    # No UNDO here on purpose: the mode pushes one undo step per drag itself.
    # With UNDO the whole session would also collapse into one step on exit.
    bl_options = {"REGISTER"}

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

    def _commit(self, context, pts, pressure=1.0):
        s = context.scene.texel
        idx = 0 if s.tool == "ERASER" else self.colour_index
        commit_stroke(self.doc, s, pts, idx, pressure)

    def _texel(self, context, event):
        """Texel under the cursor on this mode's canvas region, or None.

        A mode entered from the sidebar button runs with the SIDEBAR as its
        context region, where a 3D raycast has no view to cast from, so the
        lookup is pinned to the editor's main region explicitly."""
        area, region = self._area, self._region
        if not over_canvas(area, region, event.mouse_x, event.mouse_y):
            return None
        with context.temp_override(area=area, region=region):
            return tex_pick.texel_under_mouse(context, event, self.doc.canvas.w,
                                              self.doc.canvas.h)

    def _bind(self, context):
        """The Doc for the canvas this editor shows now, or None with a report.

        Looked up at every press, not once: the user may switch images while
        the mode is on."""
        img = self._image(context)
        if img is None:
            self.report({"WARNING"}, "No canvas: open an image, or give the object an image texture")
            return None
        doc = tex_doc.get(img)
        if doc is None:
            self.report({"ERROR"}, "This texture has more than 255 colours, so it cannot be opened as an indexed canvas. Reduce it to 255 or fewer first")
            return None
        if doc.canvas.w != img.size[0] or doc.canvas.h != img.size[1]:
            doc = tex_doc.Doc(img)
            tex_doc._DOCS[img.name] = doc
        return doc

    def _push(self):
        """One undo step per finished drag, as when one drag was one run."""
        try:
            bpy.ops.ed.undo_push(message="Texel Paint")
        except RuntimeError:
            pass                     # no undo stack (background): nothing to push

    def _exit(self, context, owned=True):
        if self.drag:
            self._end_drag(context, cancel=False)
        if owned:
            _SESSION.clear()
        try:
            self._area.header_text_set(None)
        except ReferenceError:
            pass                     # the editor was closed under us
        for area in getattr(context.screen, "areas", ()):
            area.tag_redraw()        # the panel button stops reading "Stop"

    # -- modal -------------------------------------------------------------
    def invoke(self, context, event):
        area = context.area
        if paint_mode_on(area):
            _SESSION.clear()         # the running mode sees this and leaves
            for a in context.screen.areas:
                a.tag_redraw()
            return {"CANCELLED"}
        if area is None or area.type not in {"IMAGE_EDITOR", "VIEW_3D"}:
            self.report({"WARNING"}, "Texel Paint runs in the Image Editor or the 3D Viewport")
            return {"CANCELLED"}
        region = next((r for r in area.regions if r.type == "WINDOW"), None)
        if region is None:
            return {"CANCELLED"}
        self.doc = self._bind(context)
        if self.doc is None:
            return {"CANCELLED"}
        self._area, self._region, self.drag = area, region, False
        self.token = object()
        _SESSION.clear()             # a mode running in another editor moves here
        _SESSION.update(token=self.token, area=area.as_pointer())
        area.header_text_set(HINT)
        for a in context.screen.areas:
            a.tag_redraw()
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}

    def cancel(self, context):
        """Blender is removing the handler (a file load, a closed window)."""
        if _SESSION.get("token") is self.token:
            _SESSION.clear()

    def _begin(self, context, event, start):
        """A left press on the canvas: one stroke, or a single-shot pick/fill."""
        s = context.scene.texel
        w = self.doc.canvas.w
        if s.tool == "PICK":
            i = self.doc.canvas.flatten()[start[1] * w + start[0]]
            if i:
                r, g, b, a = self.doc.canvas.palette[i]
                s.colour = (r / 255, g / 255, b / 255, a / 255)
            return
        try:
            self.colour_index = self.doc.canvas.add_colour(rgba_bytes(s.colour))
            if s.brush_shape == "STAMP" and s.tool not in {"ERASER", "FILL"}:
                # join the stamp's colours now, where a full palette can be
                # reported, rather than mid-stroke
                for _, _, rgba in saved_stamp(s) or ():
                    self.doc.canvas.add_colour(rgba)
        except ValueError:
            self.report({"ERROR"}, "The palette is full, so this colour cannot be added to it")
            return
        if s.tool == "FILL":
            h = self.doc.canvas.h
            flat = self.doc.canvas.flatten()
            pal = self.doc.canvas.palette
            get = lambda x, y: pal[flat[y * w + x]]
            self._commit(context, R.flood_fill(get, w, h, start[0], start[1],
                                               rgba_bytes(s.colour), s.tolerance,
                                               s.contiguous))
            self._push()
            return
        self.start, self.drag = start, True
        self.stroke = R.PerfectStroke(start, s.pixel_perfect)
        if s.tool in {"PENCIL", "ERASER"}:
            self._commit(context, [start], event.pressure)
        else:
            # shapes preview against a snapshot we restore each mouse-move
            self.snapshot = bytearray(self.doc.canvas.layers[self.doc.canvas.active].px)

    def _end_drag(self, context, cancel):
        s = context.scene.texel
        if s.tool in {"PENCIL", "ERASER"}:
            self._commit(context, self.stroke.end())   # never end a texel short
        elif cancel:
            self.doc.canvas.layers[self.doc.canvas.active].px = self.snapshot
        self.doc.flush()
        self.drag = False
        if not cancel:
            self._push()

    def modal(self, context, event):
        if _SESSION.get("token") is not self.token:
            self._exit(context, owned=False)    # turned off, or moved elsewhere
            return {"FINISHED"}
        try:
            self._area.type
        except ReferenceError:
            self._exit(context)
            return {"FINISHED"}
        s = context.scene.texel

        if event.type == "ESC" and event.value == "PRESS":
            if self.drag and s.tool not in {"PENCIL", "ERASER"}:
                self._end_drag(context, cancel=True)   # Esc mid-shape drops it
            self._exit(context)
            return {"FINISHED"}

        if not self.drag:
            if event.type == "LEFTMOUSE" and event.value == "PRESS":
                doc = self._bind(context)
                if doc is None:
                    return {"PASS_THROUGH"}
                self.doc = doc
                start = self._texel(context, event)
                if start is None:
                    return {"PASS_THROUGH"}            # a click off the canvas
                self._begin(context, event, start)
                return {"RUNNING_MODAL"}
            return {"PASS_THROUGH"}       # navigate, use the sidebar, shortcuts

        if event.type == "RIGHTMOUSE" and event.value == "PRESS":
            # right-click mid-drag drops a shape; a pencil stroke just ends
            self._end_drag(context, cancel=s.tool not in {"PENCIL", "ERASER"})
            return {"RUNNING_MODAL"}

        if event.type == "MOUSEMOVE":
            cur = self._texel(context, event)
            if cur is None:
                return {"RUNNING_MODAL"}
            if s.tool in {"PENCIL", "ERASER"}:
                # PerfectStroke joins the gap since the last event and hands
                # back only the texels that can no longer change. Anything it
                # withholds is still provisional: committing it here would
                # stamp a corner we cannot rub out afterwards.
                # a withheld texel lands at the pressure of the event that
                # releases it, one event late - too small a lag to see
                new = self.stroke.add(cur)
                if new:
                    self._commit(context, new, event.pressure)
            else:
                layer = self.doc.canvas.layers[self.doc.canvas.active]
                layer.px = bytearray(self.snapshot)
                self._commit(context, self._shape(s, self.start, cur))
            return {"RUNNING_MODAL"}

        if event.type == "LEFTMOUSE" and event.value == "RELEASE":
            self._end_drag(context, cancel=False)      # the tail is final now
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
        if tex_doc.get(img) is None:
            self.report({"ERROR"}, "Could not create a canvas for this image")
            return {"CANCELLED"}
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
