"""Binds a core.Canvas to a real bpy Image, and owns the flush.

Kept deliberately small. The reference's equivalent (ps_session.py) is 5,067
lines and changed in every release; that is the failure mode we are avoiding.

**This module owns canvas persistence**, and it did not until 2026-09-23. `_DOCS`
is module state, so it is empty in every new Blender session - and a Doc built
blank is not merely empty, it is authoritative, because the next `flush()`
writes it over the image. Reopening a .blend and touching the canvas therefore
replaced the artwork with a blank one, even when the image was packed and had
reopened byte-intact. See `ROADMAP.md`, the DATA LOSS section.
"""
from __future__ import annotations
import os

import bpy
from bpy.app.handlers import persistent

from .core.canvas import Canvas

_DOCS: dict[str, "Doc"] = {}


class Doc:
    """One open canvas, keyed by image name."""

    def __init__(self, image: bpy.types.Image):
        self.image_name = image.name
        w, h = image.size
        self.canvas = Canvas(w, h)
        self.dirty = False

    @property
    def image(self):
        return bpy.data.images.get(self.image_name)

    def load_from_image(self) -> None:
        """Read an existing image into the indexed canvas, building a palette.

        Fails loudly past the palette ceiling rather than silently quantising -
        a silent quantise is how a user's texture comes back subtly wrong.
        """
        img = self.image
        if img is None:
            return
        w, h = img.size
        buf = [0.0] * (w * h * 4)
        img.pixels.foreach_get(buf)
        c = Canvas(w, h)
        layer = c.layers[0]
        seen: dict[tuple, int] = {}
        for y in range(h):
            src_row = h - 1 - y                      # bpy is bottom-up
            for x in range(w):
                o = (src_row * w + x) * 4
                rgba = (round(buf[o] * 255), round(buf[o+1] * 255),
                        round(buf[o+2] * 255), round(buf[o+3] * 255))
                if rgba[3] == 0:
                    continue
                idx = seen.get(rgba)
                if idx is None:
                    idx = c.add_colour(rgba)          # raises past 255 colours
                    seen[rgba] = idx
                layer.px[y * w + x] = idx
        self.canvas = c
        self.dirty = False

    def flush(self) -> bool:
        """Push the canvas into Blender. 512x512 measures ~80 ms."""
        img = self.image
        if img is None:
            return False
        img.pixels.foreach_set(self.canvas.to_blender_floats())
        img.update()
        for area in getattr(bpy.context, "screen", None).areas if getattr(bpy.context, "screen", None) else []:
            if area.type in {"IMAGE_EDITOR", "VIEW_3D"}:
                area.tag_redraw()
        self.dirty = False
        return True


def get(image: bpy.types.Image, create: bool = True) -> Doc | None:
    """The Doc for an image, built from the image's own pixels when created.

    Reading the image back is the whole point, not an optimisation: every route
    into an existing texture lands here - `texel.paint`, `texel.show_canvas`,
    `texel.pick_texture` - and whatever canvas this hands back is what the next
    flush commits.

    Returns **None** when the image cannot be represented as an indexed canvas
    (more than 255 colours, or a zero-size image). Refusing to bind is the
    correct outcome; handing back a blank canvas is what destroyed work.
    """
    if image is None:
        return None
    d = _DOCS.get(image.name)
    if d is None and create:
        try:
            d = Doc(image)
            d.load_from_image()
        except ValueError:
            return None
        _DOCS[image.name] = d
    return d


def forget(name: str) -> None:
    _DOCS.pop(name, None)


def clear() -> None:
    _DOCS.clear()


# --------------------------------------------------------------- persistence
@persistent
def _on_load(_dummy) -> None:
    """A different .blend means every Doc in memory belongs to the old one.

    Without this, opening file B reuses file A's canvas for any image that
    happens to share its name, and the first edit writes A's art over B's.
    """
    _DOCS.clear()


@persistent
def _on_save_pre(_dummy) -> None:
    """Pack every bound canvas so the .blend actually carries the pixels.

    A canvas from `texel.add_cube` or `texel.canvas_new` is a GENERATED image.
    Blender does not store a generated image's pixels in the .blend; it
    regenerates it on reopen, so the painting was gone before Texel was
    involved. One PNG encode per canvas per save buys that back.

    An image the user deliberately placed on disk (`texel.file_place`) is left
    alone - it is their file, and `texel.file_changed` reads it back.
    """
    for name in list(_DOCS):
        img = bpy.data.images.get(name)
        if img is None:
            continue
        path = bpy.path.abspath(img.filepath) if img.filepath else ""
        if path and os.path.exists(path):
            continue
        try:
            img.pack()
        except RuntimeError:
            pass                      # nothing to pack; never block a save


def register() -> None:
    if _on_load not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(_on_load)
    if _on_save_pre not in bpy.app.handlers.save_pre:
        bpy.app.handlers.save_pre.append(_on_save_pre)


def unregister() -> None:
    while _on_load in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(_on_load)
    while _on_save_pre in bpy.app.handlers.save_pre:
        bpy.app.handlers.save_pre.remove(_on_save_pre)
    _DOCS.clear()
