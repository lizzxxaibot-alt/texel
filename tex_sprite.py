"""Tools aimed at 2D sprite work rather than 3D texturing.

Texel started as a texture tool for models, but the same canvas is exactly what
a sprite artist wants - so these close the gap: frames as layers, a sprite sheet
out the other end, trim-to-content, a reference layer to trace over, and a
colour-count report because pixel artists work to palette limits.
"""
import os

import bpy
from bpy.props import BoolProperty, EnumProperty, IntProperty, StringProperty
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper

from . import tex_doc
from .core.canvas import Canvas
from .core.palette import from_image_pixels

REFERENCE = "Reference"


def _doc(context):
    sp = context.space_data
    img = sp.image if sp and sp.type == "IMAGE_EDITOR" else None
    return tex_doc.get(img, create=False) if img else None


class _DocOp(Operator):
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return _doc(context) is not None


class TEXEL_OT_frame_add(_DocOp):
    bl_idname = "texel.frame_add"
    bl_label = "Add Frame"
    bl_description = ("Add a frame. Every track gets a new cel, so a frame can hold "
                      "a character and a background at once")

    copy_previous: BoolProperty(
        name="Copy Current", default=True,
        description="Start from the current frame instead of empty cels")

    def execute(self, context):
        d = _doc(context)
        c = d.canvas
        cur = context.scene.texel.current_frame if c.frame_count() else None
        f = c.add_frame(copy_current=cur if self.copy_previous else None)
        c.show_frame(f, onion=False)
        context.scene.texel.current_frame = f
        cel = c.cel(c.tracks[0], f)
        if cel is not None:
            c.active = c.layers.index(cel)
        d.flush()
        self.report({"INFO"}, f"Frame {f + 1} - {len(c.tracks)} track(s)")
        return {"FINISHED"}


class TEXEL_OT_frame_show(_DocOp):
    bl_idname = "texel.frame_show"
    bl_label = "Show Frame"
    bl_description = "Make this the current frame, optionally with onion skinning"

    index: IntProperty(default=0)

    def execute(self, context):
        d = _doc(context)
        c = d.canvas
        s = context.scene.texel
        n = c.frame_count()
        if not n:
            self.report({"WARNING"}, "No frames yet - use Add Frame")
            return {"CANCELLED"}
        i = max(0, min(self.index, n - 1))
        c.show_frame(i, onion=s.onion_skin, track=c.layers[c.active].track)
        s.current_frame = i
        track = c.layers[c.active].track if c.layers[c.active].track else (
            c.tracks[0] if c.tracks else None)
        cel = c.cel(track, i) if track else None
        if cel is not None:
            c.active = c.layers.index(cel)
        d.flush()
        s.status = f"Frame {i + 1} of {n}"
        return {"FINISHED"}


class TEXEL_OT_track_add(_DocOp):
    bl_idname = "texel.track_add"
    bl_label = "Add Track"
    bl_description = ("Add a named row that runs across every frame - a background, "
                      "a character, an effects pass. This is what a cel is")

    name: StringProperty(name="Name", default="Track")
    bottom: BoolProperty(
        name="Behind", default=False,
        description="Put the new track under the existing ones - what you want "
                    "for a background")

    def invoke(self, context, event):
        d = _doc(context)
        self.name = f"Track {len(d.canvas.tracks) + 1}"
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        d = _doc(context)
        c = d.canvas
        if not c.tracks and not c.frame_count():
            c.add_frame(copy_current=None)          # seed frame 0
        made = c.add_track(self.name.strip() or "Track", bottom=self.bottom)
        if made == 0:
            self.report({"WARNING"}, "A track with that name already exists")
            return {"CANCELLED"}
        c.show_frame(context.scene.texel.current_frame, onion=False)
        d.flush()
        context.scene.texel.status = f"Track '{self.name}' - {made} cel(s)"
        self.report({"INFO"}, context.scene.texel.status)
        return {"FINISHED"}


class TEXEL_OT_track_remove(_DocOp):
    bl_idname = "texel.track_remove"
    bl_label = "Remove Track"
    bl_description = "Delete a track and all of its cels"

    name: StringProperty(name="Name", default="")

    def execute(self, context):
        d = _doc(context)
        c = d.canvas
        name = self.name or (c.layers[c.active].track or "")
        if len(c.tracks) <= 1:
            self.report({"WARNING"}, "Keep at least one track")
            return {"CANCELLED"}
        n = c.remove_track(name)
        if not n:
            self.report({"WARNING"}, f"No track called '{name}'")
            return {"CANCELLED"}
        c.show_frame(context.scene.texel.current_frame, onion=False)
        d.flush()
        self.report({"INFO"}, f"Removed '{name}' ({n} cels)")
        return {"FINISHED"}


class TEXEL_OT_track_move(_DocOp):
    bl_idname = "texel.track_move"
    bl_label = "Move Track"
    bl_description = ("Reorder a track in the stack. A background belongs at the "
                      "bottom, an effects pass at the top")

    name: StringProperty()
    delta: IntProperty(default=-1)

    @classmethod
    def poll(cls, context):
        d = _doc(context)
        return d is not None and len(d.canvas.tracks) > 1

    def execute(self, context):
        d = _doc(context)
        c = d.canvas
        name = self.name or (c.layers[c.active].track or "")
        if not c.move_track(name, self.delta):
            return {"CANCELLED"}
        c.show_frame(context.scene.texel.current_frame,
                     onion=context.scene.texel.onion_skin,
                     track=c.layers[c.active].track)
        d.flush()
        context.scene.texel.status = f"'{name}' -> {c.tracks.index(name) + 1} of {len(c.tracks)}"
        return {"FINISHED"}


class TEXEL_OT_cel_select(_DocOp):
    bl_idname = "texel.cel_select"
    bl_label = "Select Cel"
    bl_description = "Edit this track's drawing on the current frame"

    track: StringProperty()

    def execute(self, context):
        d = _doc(context)
        c = d.canvas
        cel = c.cel(self.track, context.scene.texel.current_frame)
        if cel is None:
            return {"CANCELLED"}
        c.active = c.layers.index(cel)
        return {"FINISHED"}


class TEXEL_OT_sprite_sheet(_DocOp):
    bl_idname = "texel.sprite_sheet"
    bl_label = "Export Sprite Sheet"
    bl_description = "Lay every frame out on one image, ready for a game engine"

    columns: IntProperty(name="Columns", default=0, min=0, max=64,
                         description="0 packs them into a single row")
    frames_only: BoolProperty(
        name="Frames Only", default=True,
        description="Unused now that a frame is a set of cels; kept for API compatibility")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        d = _doc(context)
        c = d.canvas
        n = c.frame_count()
        if not n:
            self.report({"WARNING"}, "No frames yet - add one first")
            return {"CANCELLED"}
        cols = self.columns or n
        rows = (n + cols - 1) // cols
        sw, sh = c.w * cols, c.h * rows

        sheet = Canvas(sw, sh)
        sheet.palette = list(c.palette)
        dst = sheet.layers[0]
        for i in range(n):
            flat = c.flatten_frame(i)          # every track for that frame
            ox, oy = (i % cols) * c.w, (i // cols) * c.h
            for y in range(c.h):
                start = (oy + y) * sw + ox
                dst.px[start:start + c.w] = flat[y * c.w:(y + 1) * c.w]

        name = f"{d.image_name} Sheet"
        old = bpy.data.images.get(name)
        if old:
            bpy.data.images.remove(old)
        img = bpy.data.images.new(name, sw, sh, alpha=True)
        img.pixels.foreach_set(sheet.to_blender_floats())
        img.update()
        context.scene.texel.status = (
            f"{n} frames x {len(c.tracks)} track(s) -> {cols}x{rows} sheet, {sw}x{sh}px")
        self.report({"INFO"}, context.scene.texel.status)
        return {"FINISHED"}


class TEXEL_OT_trim(_DocOp):
    bl_idname = "texel.trim"
    bl_label = "Trim to Content"
    bl_description = ("Crop away empty space around the art. Sprite sheets and "
                      "engine importers both want a tight sprite")

    margin: IntProperty(name="Margin", default=0, min=0, max=64)

    def execute(self, context):
        d = _doc(context)
        c = d.canvas
        box = c.content_bounds()
        if box is None:
            self.report({"WARNING"}, "Canvas is empty")
            return {"CANCELLED"}
        x0, y0, x1, y1 = box
        m = self.margin
        before = (c.w, c.h)
        if not c.crop(x0 - m, y0 - m, x1 + m, y1 + m):
            self.report({"INFO"}, "Already tight - nothing to trim")
            return {"CANCELLED"}
        img = d.image
        img.scale(c.w, c.h)
        d.flush()
        context.scene.texel.status = f"Trimmed {before[0]}x{before[1]} -> {c.w}x{c.h}"
        self.report({"INFO"}, context.scene.texel.status)
        return {"FINISHED"}


class TEXEL_OT_reference_add(_DocOp, ImportHelper):
    bl_idname = "texel.reference_add"
    bl_label = "Add Reference"
    bl_description = ("Load an image as a faint locked layer underneath, to trace "
                      "over. Uses layer opacity, so it stays visible but out of the way")
    filename_ext = ".png"
    filter_glob: StringProperty(default="*.png;*.jpg;*.jpeg;*.tga;*.bmp",
                                options={"HIDDEN"})

    opacity: bpy.props.FloatProperty(name="Opacity", default=0.35, min=0.05, max=1.0)

    def execute(self, context):
        d = _doc(context)
        c = d.canvas
        try:
            ref = bpy.data.images.load(self.filepath, check_existing=True)
        except RuntimeError as e:
            self.report({"ERROR"}, f"Could not load: {e}")
            return {"CANCELLED"}
        rw, rh = ref.size
        if rw == 0 or rh == 0:
            self.report({"ERROR"}, "That image has no pixels")
            return {"CANCELLED"}
        buf = [0.0] * (rw * rh * 4)
        ref.pixels.foreach_get(buf)

        # reduce to the palette ceiling before sampling, or a photo blows the
        # 255-colour cap and the load fails halfway through
        cols = from_image_pixels(buf, rw, rh, limit=180)
        if not cols:
            self.report({"WARNING"}, "That image is fully transparent")
            return {"CANCELLED"}
        idx = {}
        for rgba in cols:
            try:
                idx[rgba] = c.add_colour(rgba)
            except ValueError:
                break
        if not idx:
            self.report({"WARNING"}, "Palette is full - clear some swatches first")
            return {"CANCELLED"}

        keys = list(idx.keys())

        def nearest(rgba):
            if rgba in idx:
                return idx[rgba]
            r, g, b, _a = rgba
            best, bd = 0, 1 << 30
            for k in keys:                       # small palette, linear is fine
                dd = (k[0] - r) ** 2 + (k[1] - g) ** 2 + (k[2] - b) ** 2
                if dd < bd:
                    bd, best = dd, idx[k]
            return best

        layer = c.add_layer(REFERENCE, above=False)
        c.layers.remove(layer)
        c.layers.insert(0, layer)                # references belong at the bottom
        for y in range(c.h):
            sy = int((c.h - 1 - y) * rh / c.h)   # bpy buffers are bottom-up
            for x in range(c.w):
                sx = int(x * rw / c.w)
                o = (sy * rw + sx) * 4
                a = round(buf[o + 3] * 255)
                if a == 0:
                    continue
                rgba = (round(buf[o] * 255), round(buf[o + 1] * 255),
                        round(buf[o + 2] * 255), a)
                layer.set(x, y, nearest(rgba))
        layer.opacity = self.opacity
        layer.locked = True                      # you trace over it, not on it
        layer.frame = None                       # static: visible on every frame
        c.active = min(len(c.layers) - 1, c.active + 1)
        d.flush()
        context.scene.texel.status = (
            f"Reference loaded at {int(self.opacity * 100)}% ({len(idx)} colours)")
        self.report({"INFO"}, context.scene.texel.status)
        return {"FINISHED"}


class TEXEL_OT_reference_remove(_DocOp):
    bl_idname = "texel.reference_remove"
    bl_label = "Remove Reference"

    def execute(self, context):
        d = _doc(context)
        c = d.canvas
        for i, l in enumerate(c.layers):
            if l.name == REFERENCE:
                c.remove_layer(i)
                d.flush()
                return {"FINISHED"}
        self.report({"INFO"}, "No reference layer")
        return {"CANCELLED"}


class TEXEL_OT_colour_count(_DocOp):
    bl_idname = "texel.colour_count"
    bl_label = "Count Colours"
    bl_description = ("How many distinct colours the art actually uses. Pixel artists "
                      "work to a limit, and the palette can hold more than you have used")

    limit: IntProperty(name="Target", default=16, min=2, max=255)

    def execute(self, context):
        d = _doc(context)
        c = d.canvas
        used = {v for v in c.flatten() if v}
        n = len(used)
        spare = len(c.palette) - 1 - n
        msg = f"{n} colours in use, {spare} unused swatch{'' if spare == 1 else 'es'}"
        if n > self.limit:
            msg += f" - {n - self.limit} over your {self.limit} target"
        context.scene.texel.status = msg
        self.report({"WARNING"} if n > self.limit else {"INFO"}, msg)
        return {"FINISHED"}


CLASSES = (TEXEL_OT_frame_add, TEXEL_OT_frame_show, TEXEL_OT_track_add,
           TEXEL_OT_track_remove, TEXEL_OT_track_move, TEXEL_OT_cel_select, TEXEL_OT_sprite_sheet,
           TEXEL_OT_trim, TEXEL_OT_reference_add, TEXEL_OT_reference_remove,
           TEXEL_OT_colour_count)


def register():
    for c in CLASSES:
        bpy.utils.register_class(c)


def unregister():
    for c in reversed(CLASSES):
        bpy.utils.unregister_class(c)
