"""Palette operators: load, save, import from an image, fetch from Lospec."""
import json
import os
import urllib.error
import urllib.request

import bpy
from bpy.props import IntProperty, StringProperty
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper, ImportHelper

from . import tex_doc
from .core import palette as P

LOSPEC_URL = "https://lospec.com/palette-list/{slug}.json"


def _doc(context):
    sp = context.space_data
    img = sp.image if sp and sp.type == "IMAGE_EDITOR" else None
    return tex_doc.get(img, create=False) if img else None


def _apply(context, colours):
    """Replace the working palette, keeping index 0 transparent."""
    d = _doc(context)
    if d is None:
        return 0
    colours = P.dedupe(colours)[:255]
    d.canvas.palette = [(0, 0, 0, 0)] + list(colours)
    d.flush()
    return len(colours)


class TEXEL_OT_palette_load(Operator, ImportHelper):
    bl_idname = "texel.palette_load"
    bl_label = "Load Palette"
    bl_description = "Load a .gpl, .hex or .txt palette"
    filename_ext = ".gpl"
    filter_glob: StringProperty(default="*.gpl;*.hex;*.txt;*.json", options={"HIDDEN"})

    @classmethod
    def poll(cls, context):
        return _doc(context) is not None

    def execute(self, context):
        try:
            with open(self.filepath, "r", encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError as e:
            self.report({"ERROR"}, f"Could not read: {e}")
            return {"CANCELLED"}
        name, cols = P.parse(text, self.filepath)
        if not cols:
            self.report({"WARNING"}, "No colours found in that file")
            return {"CANCELLED"}
        n = _apply(context, cols)
        self.report({"INFO"}, f"{name}: {n} colours")
        return {"FINISHED"}


class TEXEL_OT_palette_save(Operator, ExportHelper):
    bl_idname = "texel.palette_save"
    bl_label = "Save Palette"
    bl_description = "Write the current palette as a GIMP .gpl, readable by Aseprite and Krita"
    filename_ext = ".gpl"
    filter_glob: StringProperty(default="*.gpl", options={"HIDDEN"})

    @classmethod
    def poll(cls, context):
        return _doc(context) is not None

    def execute(self, context):
        d = _doc(context)
        cols = [c for c in d.canvas.palette[1:]]
        if not cols:
            self.report({"WARNING"}, "Palette is empty")
            return {"CANCELLED"}
        name = os.path.splitext(os.path.basename(self.filepath))[0]
        try:
            with open(self.filepath, "w", encoding="utf-8") as fh:
                fh.write(P.to_gpl(name, cols))
        except OSError as e:
            self.report({"ERROR"}, f"Could not write: {e}")
            return {"CANCELLED"}
        self.report({"INFO"}, f"Saved {len(cols)} colours")
        return {"FINISHED"}


class TEXEL_OT_palette_from_image(Operator):
    bl_idname = "texel.palette_from_image"
    bl_label = "Palette from Image"
    bl_description = "Take the palette from an image already open in Blender"

    image_name: StringProperty(name="Image")

    @classmethod
    def poll(cls, context):
        return _doc(context) is not None

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        self.layout.prop_search(self, "image_name", bpy.data, "images", text="")

    def execute(self, context):
        img = bpy.data.images.get(self.image_name)
        if img is None:
            self.report({"WARNING"}, "Pick an image")
            return {"CANCELLED"}
        w, h = img.size
        buf = [0.0] * (w * h * 4)
        img.pixels.foreach_get(buf)
        cols = P.from_image_pixels(buf, w, h)
        if not cols:
            self.report({"WARNING"}, "That image has no opaque pixels")
            return {"CANCELLED"}
        n = _apply(context, cols)
        self.report({"INFO"}, f"{n} colours taken from {img.name}")
        return {"FINISHED"}


class TEXEL_OT_palette_lospec(Operator):
    bl_idname = "texel.palette_lospec"
    bl_label = "Fetch from Lospec"
    bl_description = "Download a palette from lospec.com by its slug"

    slug: StringProperty(
        name="Palette", default="pico-8",
        description="The slug from the Lospec URL, e.g. 'pico-8' or 'endesga-32'")

    @classmethod
    def poll(cls, context):
        return _doc(context) is not None

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        slug = self.slug.strip().strip("/").rsplit("/", 1)[-1]
        if not slug:
            self.report({"WARNING"}, "Enter a palette slug")
            return {"CANCELLED"}
        url = LOSPEC_URL.format(slug=slug)
        try:
            with urllib.request.urlopen(url, timeout=10) as r:
                text = r.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            self.report({"ERROR"}, f"Lospec has no palette '{slug}' ({e.code})")
            return {"CANCELLED"}
        except Exception as e:                       # offline, DNS, TLS, timeout
            self.report({"ERROR"}, f"Could not reach Lospec: {e}")
            return {"CANCELLED"}
        try:
            name, cols = P.parse_lospec_json(text)
        except (json.JSONDecodeError, TypeError):
            self.report({"ERROR"}, "Lospec returned something unexpected")
            return {"CANCELLED"}
        if not cols:
            self.report({"WARNING"}, "That palette is empty")
            return {"CANCELLED"}
        n = _apply(context, cols)
        self.report({"INFO"}, f"{name}: {n} colours")
        return {"FINISHED"}


class TEXEL_OT_swatch_use(Operator):
    bl_idname = "texel.swatch_use"
    bl_label = "Use Swatch"
    bl_description = "Set the paint colour from this swatch"
    index: IntProperty()

    def execute(self, context):
        d = _doc(context)
        if d and 0 < self.index < len(d.canvas.palette):
            r, g, b, a = d.canvas.palette[self.index]
            context.scene.texel.colour = (r / 255, g / 255, b / 255, a / 255)
        return {"FINISHED"}


CLASSES = (TEXEL_OT_palette_load, TEXEL_OT_palette_save, TEXEL_OT_palette_from_image,
           TEXEL_OT_palette_lospec, TEXEL_OT_swatch_use)


def register():
    for c in CLASSES:
        bpy.utils.register_class(c)


def unregister():
    for c in reversed(CLASSES):
        bpy.utils.unregister_class(c)
