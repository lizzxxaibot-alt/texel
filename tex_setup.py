"""Setup, grid overlay, pixel-art unwrap, workspace and external-file reload.

The convenience layer. None of it is clever; all of it is the difference between
a tool you can use and a tool you can demo.
"""
import os
import time

import bmesh
import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty, StringProperty
from bpy.types import Operator

from . import tex_doc
from .core import raster as R
from .core import uvmap
from .tex_density import _active_mesh, _texture_size

GRID_LAYER = "Pixel Grid"


def _doc(context):
    sp = context.space_data
    img = sp.image if sp and sp.type == "IMAGE_EDITOR" else None
    return tex_doc.get(img, create=False) if img else None


# --------------------------------------------------------------------- grid
class TEXEL_OT_grid_add(Operator):
    bl_idname = "texel.grid_add"
    bl_label = "Add Pixel Grid Layer"
    bl_description = "Add a grid layer on top so you can see the texel spacing while you work"
    bl_options = {"REGISTER", "UNDO"}

    spacing: IntProperty(name="Every", default=8, min=2, max=64,
                        description="Grid line every N texels")

    @classmethod
    def poll(cls, context):
        return _doc(context) is not None

    def execute(self, context):
        d = _doc(context)
        c = d.canvas
        for i, layer in enumerate(c.layers):
            if layer.name == GRID_LAYER:
                c.layers.pop(i)
                break
        idx = c.add_colour((70, 70, 82, 255))
        grid = c.add_layer(GRID_LAYER)
        c.layers.remove(grid)
        c.layers.append(grid)                    # grid is always the TOP layer
        c.active = len(c.layers) - 1
        for n in range(0, c.w, self.spacing):
            for x, y in R.line(n, 0, n, c.h - 1):
                grid.set(x, y, idx)
        for n in range(0, c.h, self.spacing):
            for x, y in R.line(0, n, c.w - 1, n):
                grid.set(x, y, idx)
        grid.locked = True                       # you should not paint on the grid
        c.active = max(0, len(c.layers) - 2)     # drop back to a paintable layer
        d.flush()
        self.report({"INFO"}, f"Grid every {self.spacing} texels")
        return {"FINISHED"}


class TEXEL_OT_grid_toggle(Operator):
    bl_idname = "texel.grid_toggle"
    bl_label = "Toggle Grid Layer"
    bl_description = "Show or hide the pixel grid layer"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return _doc(context) is not None

    def execute(self, context):
        d = _doc(context)
        for layer in d.canvas.layers:
            if layer.name == GRID_LAYER:
                layer.visible = not layer.visible
                d.flush()
                return {"FINISHED"}
        self.report({"INFO"}, "No grid layer yet - add one first")
        return {"CANCELLED"}


class TEXEL_OT_viewport_grid_toggle(Operator):
    bl_idname = "texel.viewport_grid_toggle"
    bl_label = "Toggle Pixel Grid"
    bl_description = "Show Blender's own UV/pixel grid in the Image Editor"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return context.space_data and context.space_data.type == "IMAGE_EDITOR"

    def execute(self, context):
        ov = context.space_data.overlay
        ov.show_grid_background = not ov.show_grid_background
        state = "on" if ov.show_grid_background else "off"
        self.report({"INFO"}, f"Image editor grid {state}")
        return {"FINISHED"}


# ------------------------------------------------------------------- setup
class TEXEL_OT_add_cube(Operator):
    bl_idname = "texel.add_cube"
    bl_label = "Add 1m Cube"
    bl_description = "Add a flat-shaded 1m cube already set up for pixel painting"
    bl_options = {"REGISTER", "UNDO"}

    size: FloatProperty(name="Size", default=1.0, min=0.01, max=100.0)
    texture: IntProperty(name="Texture", default=64, min=8, max=2048)

    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add(size=self.size)
        obj = context.active_object
        obj.name = "Pixel Cube"
        bpy.ops.object.shade_flat()
        img = bpy.data.images.new(f"{obj.name} Texture", self.texture, self.texture,
                                  alpha=True)
        img.pixels.foreach_set([0.0] * (self.texture * self.texture * 4))
        img.update()
        mat = bpy.data.materials.new(f"{obj.name} Material")
        mat.use_nodes = True
        nt = mat.node_tree
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = img
        tex.interpolation = "Closest"            # pixels must stay pixels
        tex.location = (-400, 200)
        nt.links.new(tex.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"])
        obj.data.materials.append(mat)
        tex_doc.get(img)
        self.report({"INFO"}, f"Cube with a {self.texture}px canvas, nearest-neighbour")
        return {"FINISHED"}


class TEXEL_OT_setup_viewport(Operator):
    bl_idname = "texel.setup_viewport"
    bl_label = "Setup Viewport"
    bl_description = "Switch to material preview with filtering off, so pixels look like pixels"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return context.space_data and context.space_data.type == "VIEW_3D"

    def execute(self, context):
        sp = context.space_data
        sp.shading.type = "MATERIAL"
        sp.shading.use_scene_lights = False
        sp.shading.use_scene_world = False
        n = 0
        for mat in bpy.data.materials:
            if not mat.use_nodes:
                continue
            for node in mat.node_tree.nodes:
                if node.type == "TEX_IMAGE" and node.interpolation != "Closest":
                    node.interpolation = "Closest"
                    n += 1
        self.report({"INFO"}, f"Material preview on; {n} textures set to nearest-neighbour")
        return {"FINISHED"}


class TEXEL_OT_restore_viewport(Operator):
    bl_idname = "texel.restore_viewport"
    bl_label = "Restore Viewport"
    bl_description = "Put the viewport back to solid shading with scene lighting"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return context.space_data and context.space_data.type == "VIEW_3D"

    def execute(self, context):
        sp = context.space_data
        sp.shading.type = "SOLID"
        sp.shading.use_scene_lights = True
        sp.shading.use_scene_world = True
        return {"FINISHED"}


class TEXEL_OT_workspace_create(Operator):
    bl_idname = "texel.workspace_create"
    bl_label = "Texel Workspace"
    bl_description = "Create a workspace with the canvas and the model side by side"
    bl_options = {"REGISTER"}

    def execute(self, context):
        name = "Texel"
        if name in bpy.data.workspaces:
            context.window.workspace = bpy.data.workspaces[name]
            self.report({"INFO"}, "Switched to the Texel workspace")
            return {"FINISHED"}
        bpy.ops.workspace.duplicate()
        ws = context.window.workspace
        ws.name = name
        screen = ws.screens[0]
        areas = [a for a in screen.areas if a.type == "VIEW_3D"]
        if areas:
            v3d = max(areas, key=lambda a: a.width * a.height)
            with context.temp_override(window=context.window, screen=screen, area=v3d):
                bpy.ops.screen.area_split(direction="VERTICAL", factor=0.42)
            left = min((a for a in screen.areas if a.type == "VIEW_3D"), key=lambda a: a.x)
            left.type = "IMAGE_EDITOR"
        for area in screen.areas:
            for space in area.spaces:
                if hasattr(space, "show_region_ui"):
                    space.show_region_ui = True
        self.report({"INFO"}, "Texel workspace created")
        return {"FINISHED"}


# ------------------------------------------------------------------ unwrap
class TEXEL_OT_pixel_art_unwrap(Operator):
    bl_idname = "texel.pixel_art_unwrap"
    bl_label = "Pixel Art Unwrap"
    bl_description = ("Unwrap, then force every UV onto the texel grid at a uniform "
                      "density - the unwrap a pixel artist actually wants")
    bl_options = {"REGISTER", "UNDO"}

    method: EnumProperty(
        name="Method",
        items=[("SMART", "Smart Project", "Angle-based, good for hard-surface"),
               ("CUBE", "Cube Project", "Best for boxy, low-poly shapes"),
               ("UNWRAP", "Unwrap", "Uses your existing seams")],
        default="SMART")
    angle: FloatProperty(name="Angle Limit", default=66.0, min=1.0, max=89.0)
    margin: FloatProperty(name="Island Margin", default=0.02, min=0.0, max=0.5)

    @classmethod
    def poll(cls, context):
        return _active_mesh(context) is not None

    def execute(self, context):
        obj = _active_mesh(context)
        size = _texture_size(obj)
        if not size:
            self.report({"WARNING"}, "No image texture on this object")
            return {"CANCELLED"}
        prev = obj.mode
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="SELECT")
        if self.method == "SMART":
            bpy.ops.uv.smart_project(angle_limit=self.angle * 3.14159 / 180.0,
                                     island_margin=self.margin)
        elif self.method == "CUBE":
            bpy.ops.uv.cube_project(cube_size=1.0)
        else:
            bpy.ops.uv.unwrap(margin=self.margin)
        bpy.ops.object.mode_set(mode="OBJECT")

        # uniform density, then snap - order matters, snapping first then scaling
        # would drift every UV straight back off the grid
        bpy.ops.texel.density_apply()
        bpy.ops.texel.snap_uvs()
        if prev != "OBJECT":
            bpy.ops.object.mode_set(mode=prev)
        context.scene.texel.status = (
            f"Unwrapped ({self.method.title()}), uniform density, snapped to {size}px")
        self.report({"INFO"}, context.scene.texel.status)
        return {"FINISHED"}


class TEXEL_OT_unwrap_info(Operator):
    bl_idname = "texel.unwrap_info"
    bl_label = "Unwrap Help"
    bl_description = "What each unwrap method is for"
    bl_options = {"REGISTER"}

    def execute(self, context):
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width=380)

    def draw(self, context):
        col = self.layout.column(align=True)
        col.label(text="Pixel Art Unwrap", icon="UV")
        col.separator()
        for title, body in (
            ("Cube Project", "Boxy, low-poly shapes. Fastest, cleanest islands."),
            ("Smart Project", "Angle-based. Good default for hard-surface meshes."),
            ("Unwrap", "Uses seams you marked yourself. Most control."),
        ):
            col.label(text=title + ":")
            col.label(text="    " + body)
        col.separator()
        col.label(text="All three then set a uniform density and snap every UV")
        col.label(text="to the texel grid, which is what kills half-pixel seams.")


# ------------------------------------------------------- external file reload
_WATCH: dict[str, float] = {}


class TEXEL_OT_file_changed(Operator):
    bl_idname = "texel.file_changed"
    bl_label = "Reload If Changed"
    bl_description = ("Reload the texture if it changed on disk - lets you round-trip "
                      "to Aseprite and come back")
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return _doc(context) is not None

    def execute(self, context):
        d = _doc(context)
        img = d.image
        path = bpy.path.abspath(img.filepath) if img.filepath else ""
        if not path or not os.path.exists(path):
            self.report({"WARNING"}, "This canvas has no file on disk yet")
            return {"CANCELLED"}
        mtime = os.path.getmtime(path)
        if _WATCH.get(img.name) == mtime:
            self.report({"INFO"}, "Unchanged")
            return {"FINISHED"}
        img.reload()
        try:
            d.load_from_image()
        except ValueError as e:
            self.report({"ERROR"}, f"Cannot load: {e}")
            return {"CANCELLED"}
        _WATCH[img.name] = mtime
        self.report({"INFO"}, f"Reloaded {os.path.basename(path)}")
        return {"FINISHED"}


class TEXEL_OT_file_place(Operator):
    bl_idname = "texel.file_place"
    bl_label = "Save Canvas To Disk"
    bl_description = "Write the canvas to a PNG so another editor can open it"
    bl_options = {"REGISTER"}

    filepath: StringProperty(subtype="FILE_PATH")

    @classmethod
    def poll(cls, context):
        return _doc(context) is not None

    def invoke(self, context, event):
        d = _doc(context)
        self.filepath = bpy.path.abspath(f"//{d.image.name}.png")
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        d = _doc(context)
        img = d.image
        img.filepath_raw = self.filepath
        img.file_format = "PNG"
        try:
            img.save()
        except RuntimeError as e:
            self.report({"ERROR"}, f"Could not save: {e}")
            return {"CANCELLED"}
        if os.path.exists(self.filepath):
            _WATCH[img.name] = os.path.getmtime(self.filepath)
        self.report({"INFO"}, f"Saved {os.path.basename(self.filepath)}")
        return {"FINISHED"}


class TEXEL_OT_reload_forget(Operator):
    bl_idname = "texel.reload_forget"
    bl_label = "Stop Watching"
    bl_description = "Forget the on-disk file for this canvas"
    bl_options = {"REGISTER"}

    def execute(self, context):
        d = _doc(context)
        if d:
            _WATCH.pop(d.image_name, None)
        self.report({"INFO"}, "Stopped watching")
        return {"FINISHED"}


CLASSES = (TEXEL_OT_grid_add, TEXEL_OT_grid_toggle, TEXEL_OT_viewport_grid_toggle,
           TEXEL_OT_add_cube, TEXEL_OT_setup_viewport, TEXEL_OT_restore_viewport,
           TEXEL_OT_workspace_create, TEXEL_OT_pixel_art_unwrap, TEXEL_OT_unwrap_info,
           TEXEL_OT_file_changed, TEXEL_OT_file_place, TEXEL_OT_reload_forget)


def register():
    for c in CLASSES:
        bpy.utils.register_class(c)


def unregister():
    _WATCH.clear()
    for c in reversed(CLASSES):
        bpy.utils.unregister_class(c)
