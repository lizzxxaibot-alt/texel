"""Binds a core.Canvas to a real bpy Image, and owns the flush.

Kept deliberately small. The reference's equivalent (ps_session.py) is 5,067
lines and changed in every release; that is the failure mode we are avoiding.
"""
from __future__ import annotations
import bpy
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
    if image is None:
        return None
    d = _DOCS.get(image.name)
    if d is None and create:
        d = Doc(image)
        _DOCS[image.name] = d
    return d


def forget(name: str) -> None:
    _DOCS.pop(name, None)


def clear() -> None:
    _DOCS.clear()
