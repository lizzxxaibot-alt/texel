"""Texel - pixel-perfect pixel art painting for Blender.

Paint pixel art directly onto models in the 3D viewport or in the Image Editor,
with an indexed canvas, layers, palettes, and texel-density tools that keep the
pixel size consistent across a mesh.

Copyright (c) 2026 Mintworks. Licensed GPL-3.0-or-later, as every add-on built
on the Blender Python API must be.
"""

bl_info = {
    "name": "Texel",
    "author": "Mintworks",
    "version": (0, 2, 0),
    "blender": (4, 2, 0),
    "location": "Image Editor / 3D Viewport > Sidebar (N) > Texel",
    "description": "Pixel-perfect pixel art painting, layers and texel density",
    "doc_url": "https://mintworks.cc",
    "category": "Paint",
}

import importlib
import sys

from . import (tex_props, tex_doc, tex_pick, tex_paint, tex_layers,
               tex_density, tex_palette, tex_select, tex_zones, tex_setup,
               tex_extra, tex_tools, tex_showcase, tex_sprite, tex_anim, tex_keys,
               tex_ui)

_MODULES = (tex_props, tex_paint, tex_layers, tex_density, tex_palette,
            tex_select, tex_zones, tex_setup, tex_extra, tex_tools, tex_showcase,
            tex_sprite, tex_anim, tex_keys, tex_ui)


def _reload():
    """Re-import every submodule. Blender caches them between add-on reloads,
    so without this an edit to a submodule silently does nothing."""
    from .core import raster, canvas, uvmap, palette, select, adjust, tools
    for m in (raster, canvas, uvmap, palette, select, adjust, tools, tex_props, tex_doc,
              tex_pick, tex_paint, tex_layers, tex_density, tex_palette,
              tex_select, tex_zones, tex_setup, tex_extra, tex_tools, tex_showcase,
              tex_sprite, tex_anim, tex_keys, tex_ui):
        importlib.reload(m)


if "bpy" in locals():
    _reload()

import bpy


def register():
    for m in _MODULES:
        m.register()


def unregister():
    for m in reversed(_MODULES):
        m.unregister()
    tex_doc.clear()
