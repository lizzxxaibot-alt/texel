"""Real animation, by borrowing Blender's timeline instead of inventing one.

Blender already has a frame counter, a scrub bar, playback with the spacebar, an
FPS setting and a render range. Building a second, worse timeline inside a
sidebar would be the wrong answer. So Texel binds its frames to Blender's: a
frame_change handler shows the right frame, and everything else - play, loop,
scrub, set the fps - is Blender's own UI doing what it already does well.

That buys the three things frames-as-layers was missing:
  * playback you can actually watch
  * per-frame timing, by holding a frame for more than one Blender frame
  * an export that carries the timing with it (GIF, or a sheet plus JSON)
"""
import json
import os
import shutil
import subprocess

import bpy
from bpy.app.handlers import persistent
from bpy.props import BoolProperty, IntProperty, StringProperty
from bpy.types import Operator

from . import tex_doc

FRAME_PREFIX = "Frame "
_BOUND = {"image": None}


def _doc(context=None):
    ctx = context or bpy.context
    sp = getattr(ctx, "space_data", None)
    img = sp.image if sp and sp.type == "IMAGE_EDITOR" else None
    if img is None and _BOUND["image"]:
        img = bpy.data.images.get(_BOUND["image"])
    return tex_doc.get(img, create=False) if img else None


def frames_of(canvas):
    """Kept for callers that just want a count. A frame is now a SET of cels
    across tracks, not a single layer, so this returns frame indices."""
    return list(range(canvas.frame_count()))


def holds_of(canvas, n):
    """Per-frame hold length in Blender frames. Defaults to 1 each."""
    holds = getattr(canvas, "frame_holds", None)
    if not isinstance(holds, list) or len(holds) != n:
        holds = [1] * n
        canvas.frame_holds = holds
    return holds


def frame_at(canvas, blender_frame):
    """Which Texel frame is on screen at a given Blender frame, with looping."""
    n = canvas.frame_count()
    if not n:
        return None
    holds = holds_of(canvas, n)
    total = sum(max(1, h) for h in holds)
    t = (blender_frame - 1) % total
    acc = 0
    for i, h in enumerate(holds):
        acc += max(1, h)
        if t < acc:
            return i
    return n - 1


@persistent
def _on_frame(scene, _depsgraph=None):
    name = _BOUND.get("image")
    if not name:
        return
    img = bpy.data.images.get(name)
    if img is None:
        return
    doc = tex_doc.get(img, create=False)
    if doc is None:
        return
    c = doc.canvas
    fr = frames_of(c)
    if not fr:
        return
    i = frame_at(c, scene.frame_current)
    if i is None:
        return
    before = [(l.visible, l.opacity) for l in c.layers]
    c.show_frame(i, onion=False)               # every track for that frame
    if before != [(l.visible, l.opacity) for l in c.layers]:
        scene.texel.current_frame = i
        doc.flush()


def _install():
    if _on_frame not in bpy.app.handlers.frame_change_post:
        bpy.app.handlers.frame_change_post.append(_on_frame)


def _remove():
    while _on_frame in bpy.app.handlers.frame_change_post:
        bpy.app.handlers.frame_change_post.remove(_on_frame)


class TEXEL_OT_anim_bind(Operator):
    bl_idname = "texel.anim_bind"
    bl_label = "Bind to Timeline"
    bl_description = ("Drive the frames from Blender's timeline. Then play, scrub and "
                      "set the fps with Blender's own controls - spacebar works")
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        d = _doc(context)
        return d is not None and d.canvas.frame_count() > 0

    def execute(self, context):
        d = _doc(context)
        c = d.canvas
        n = c.frame_count()
        holds = holds_of(c, n)
        total = sum(max(1, h) for h in holds)
        _BOUND["image"] = d.image_name
        _install()
        sc = context.scene
        sc.frame_start = 1
        sc.frame_end = total
        sc.frame_current = 1
        _on_frame(sc)
        sc.texel.status = (f"Bound {n} frames to the timeline "
                           f"({total} at {sc.render.fps} fps). Press space to play")
        self.report({"INFO"}, sc.texel.status)
        return {"FINISHED"}


class TEXEL_OT_anim_unbind(Operator):
    bl_idname = "texel.anim_unbind"
    bl_label = "Unbind"
    bl_description = "Stop driving frames from the timeline"
    bl_options = {"REGISTER"}

    def execute(self, context):
        _remove()
        _BOUND["image"] = None
        d = _doc(context)
        if d and d.canvas.frame_count():        # leave frame 1 visible
            d.canvas.show_frame(0, onion=False)
            d.flush()
        context.scene.texel.status = "Timeline unbound"
        return {"FINISHED"}


class TEXEL_OT_anim_play(Operator):
    bl_idname = "texel.anim_play"
    bl_label = "Play"
    bl_description = "Bind if needed, then start Blender's playback"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        d = _doc(context)
        return d is not None and d.canvas.frame_count() > 0

    def execute(self, context):
        if _BOUND["image"] is None:
            bpy.ops.texel.anim_bind()
        try:
            bpy.ops.screen.animation_play()
        except RuntimeError as e:
            self.report({"WARNING"}, f"Playback needs a window: {e}")
            return {"CANCELLED"}
        return {"FINISHED"}


class TEXEL_OT_frame_hold(Operator):
    bl_idname = "texel.frame_hold"
    bl_label = "Frame Timing"
    bl_description = ("How many timeline frames this drawing stays on screen. "
                      "2 at 12 fps is a sixth of a second")
    bl_options = {"REGISTER", "UNDO"}

    index: IntProperty(default=0, min=0)
    hold: IntProperty(name="Hold", default=1, min=1, max=64)

    @classmethod
    def poll(cls, context):
        d = _doc(context)
        return d is not None and d.canvas.frame_count() > 0

    def invoke(self, context, event):
        d = _doc(context)
        holds = holds_of(d.canvas, d.canvas.frame_count())
        if 0 <= self.index < len(holds):
            self.hold = holds[self.index]
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        d = _doc(context)
        holds = holds_of(d.canvas, d.canvas.frame_count())
        if not (0 <= self.index < len(holds)):
            return {"CANCELLED"}
        holds[self.index] = self.hold
        d.canvas.frame_holds = holds
        if _BOUND["image"]:
            bpy.ops.texel.anim_bind()          # re-derive the timeline length
        context.scene.texel.status = f"Frame {self.index + 1} holds {self.hold}"
        return {"FINISHED"}


class TEXEL_OT_export_gif(Operator):
    bl_idname = "texel.export_gif"
    bl_label = "Export GIF"
    bl_description = ("Write an animated GIF at the scene fps, honouring per-frame "
                      "holds. Needs ffmpeg on PATH")
    bl_options = {"REGISTER"}

    scale: IntProperty(name="Scale", default=4, min=1, max=16,
                       description="Nearest-neighbour upscale, so texels stay square")
    directory: StringProperty(subtype="DIR_PATH", default="//")

    @classmethod
    def poll(cls, context):
        d = _doc(context)
        return d is not None and d.canvas.frame_count() > 0

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        ff = shutil.which("ffmpeg")
        if ff is None:
            self.report({"ERROR"}, "ffmpeg is not on PATH - use Export Sprite Sheet instead")
            return {"CANCELLED"}
        d = _doc(context)
        c = d.canvas
        n_frames = c.frame_count()
        holds = holds_of(c, n_frames)
        out = bpy.path.abspath(self.directory or "//")
        os.makedirs(out, exist_ok=True)
        tmp = os.path.join(out, "_texel_gif")
        os.makedirs(tmp, exist_ok=True)

        # write one PNG per TIMELINE frame, so holds become real duration
        saved = [(l.visible, l.opacity) for l in c.layers]
        n = 0
        try:
            for i in range(n_frames):
                c.show_frame(i, onion=False)   # all tracks for this frame
                png = bpy.data.images.new(f"_texel_f{i}", c.w, c.h, alpha=True)
                png.pixels.foreach_set(c.to_blender_floats())
                for _ in range(max(1, holds[i])):
                    png.filepath_raw = os.path.join(tmp, f"g_{n:04d}.png")
                    png.file_format = "PNG"
                    png.save()
                    n += 1
                bpy.data.images.remove(png)
        finally:
            for l, (v, o) in zip(c.layers, saved):
                l.visible, l.opacity = v, o
            d.flush()

        fps = context.scene.render.fps
        gif = os.path.join(out, f"{d.image_name}.gif")
        vf = (f"scale=iw*{self.scale}:ih*{self.scale}:flags=neighbor,"
              f"split[a][b];[a]palettegen=reserve_transparent=1[p];"
              f"[b][p]paletteuse=dither=none")
        r = subprocess.run([ff, "-y", "-loglevel", "error", "-framerate", str(fps),
                            "-i", os.path.join(tmp, "g_%04d.png"), "-vf", vf,
                            "-loop", "0", gif], capture_output=True, text=True)
        shutil.rmtree(tmp, ignore_errors=True)
        if r.returncode != 0:
            self.report({"ERROR"}, f"ffmpeg failed: {r.stderr.strip()[:120]}")
            return {"CANCELLED"}
        context.scene.texel.status = (
            f"{n_frames} frames -> {n} at {fps}fps -> {os.path.basename(gif)}")
        self.report({"INFO"}, context.scene.texel.status)
        return {"FINISHED"}


class TEXEL_OT_export_anim_data(Operator):
    bl_idname = "texel.export_anim_data"
    bl_label = "Export Sheet + JSON"
    bl_description = ("Sprite sheet plus a JSON manifest with frame rects and "
                      "durations, so an engine can play it without guessing")
    bl_options = {"REGISTER"}

    columns: IntProperty(name="Columns", default=0, min=0, max=64)
    directory: StringProperty(subtype="DIR_PATH", default="//")

    @classmethod
    def poll(cls, context):
        d = _doc(context)
        return d is not None and d.canvas.frame_count() > 0

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        d = _doc(context)
        c = d.canvas
        n_frames = c.frame_count()
        holds = holds_of(c, n_frames)
        cols = self.columns or n_frames
        rows = (n_frames + cols - 1) // cols
        fps = context.scene.render.fps

        bpy.ops.texel.sprite_sheet(columns=cols, frames_only=True)
        sheet = bpy.data.images.get(f"{d.image_name} Sheet")
        out = bpy.path.abspath(self.directory or "//")
        os.makedirs(out, exist_ok=True)
        if sheet:
            sheet.filepath_raw = os.path.join(out, f"{d.image_name}_sheet.png")
            sheet.file_format = "PNG"
            sheet.save()

        data = {
            "image": f"{d.image_name}_sheet.png",
            "frame_width": c.w, "frame_height": c.h,
            "columns": cols, "rows": rows, "fps": fps,
            "frames": [
                {"index": i, "x": (i % cols) * c.w, "y": (i // cols) * c.h,
                 "w": c.w, "h": c.h, "hold": max(1, holds[i]),
                 "duration_ms": round(max(1, holds[i]) / fps * 1000)}
                for i in range(n_frames)],
        }
        path = os.path.join(out, f"{d.image_name}_anim.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
        context.scene.texel.status = (
            f"{n_frames} frames x {len(c.tracks)} track(s) -> "
            f"{os.path.basename(path)} + sheet")
        self.report({"INFO"}, context.scene.texel.status)
        return {"FINISHED"}


CLASSES = (TEXEL_OT_anim_bind, TEXEL_OT_anim_unbind, TEXEL_OT_anim_play,
           TEXEL_OT_frame_hold, TEXEL_OT_export_gif, TEXEL_OT_export_anim_data)


def register():
    for c in CLASSES:
        bpy.utils.register_class(c)


def unregister():
    _remove()                                   # never leave a handler behind
    _BOUND["image"] = None
    for c in reversed(CLASSES):
        bpy.utils.unregister_class(c)
