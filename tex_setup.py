"""Setup, grid overlay, pixel-art unwrap, workspace and external-file reload.

The convenience layer. None of it is clever; all of it is the difference between
a tool you can use and a tool you can demo.
"""
import os
import time

import math

import bmesh
import bpy
import mathutils
from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty, StringProperty
from bpy.types import Operator

from . import tex_doc
from .core import raster as R
from .core import tools
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
    bl_description = ("Build a workspace set up for pixel art: canvas beside the "
                      "model, a timeline for frames, both sidebars on Texel, and "
                      "colours shown exactly as painted")
    bl_options = {"REGISTER"}

    exact_colours: BoolProperty(
        name="Exact Colours", default=True,
        description=("Set the view transform to Standard. Blender's default AgX "
                     "is a film response - it desaturates a hand-picked palette "
                     "on screen, so the colour you chose is not the colour you "
                     "see. Turn this off to keep AgX for rendering"))
    timeline: BoolProperty(
        name="Timeline", default=True,
        description="Add a timeline under the canvas, for animation playback")
    tidy_scene: BoolProperty(
        name="Replace the Default Cube", default=True,
        description=("If the file is still Blender's untouched startup scene, "
                     "swap its cube, camera and light for a pixel-ready cube "
                     "with a canvas. Never touches a scene you have worked in"))

    # We CANNOT select the Texel tab for the user. `Region.active_panel_category`
    # is read-only in the Python API - assigning to it raises
    # "attribute ... from Region is read-only" - so there is no supported way to
    # put a sidebar on a particular tab. An earlier version of this file
    # retried the assignment twenty times inside a try/except; it never once
    # worked, it just swallowed the error and looked deliberate. Code that
    # pretends to do something it cannot is worse than no code, so it is gone
    # and the operator says where to click instead.

    @staticmethod
    def _is_factory_scene(context):
        """True only for Blender's untouched startup scene.

        Deleting somebody's objects would be unforgivable, so the bar is
        deliberately high: exactly the three factory objects, under their
        factory names, with the cube still an unmodified, unmaterialed
        eight-vertex box at the origin. Anything else and we leave the scene
        entirely alone.
        """
        objs = list(context.scene.objects)
        if len(objs) != 3:
            return False
        if sorted(o.name for o in objs) != ["Camera", "Cube", "Light"]:
            return False
        cube = context.scene.objects.get("Cube")
        if cube is None or cube.type != "MESH":
            return False
        if len(cube.data.vertices) != 8:
            return False
        if not all(abs(v) < 1e-4 for v in cube.location):
            return False
        # Blender's factory cube DOES carry a material, called "Material" - so
        # "has any material" is not evidence of user work, and treating it as
        # such meant this returned False every single time and the welcome
        # scene never once ran. Accept exactly the factory one, untextured.
        mats = [m for m in cube.data.materials if m]
        if len(mats) > 1 or (mats and mats[0].name != "Material"):
            return False
        if mats and mats[0].use_nodes:
            if any(n.type == "TEX_IMAGE" for n in mats[0].node_tree.nodes):
                return False
        return True

    def _exact_colours(self, context):
        """Show the palette as painted.

        AgX is a film response: it rolls off highlights and desaturates, so a
        hand-picked palette is not the palette you see on screen. Pixel artists
        pick exact colours and expect exact colours back.
        """
        if not self.exact_colours:
            return
        vs = context.scene.view_settings
        vs.view_transform = "Standard"
        vs.look = "None"

    @staticmethod
    def _paint_welcome_tile(img):
        """Put a real tile on the welcome cube.

        An empty canvas is transparent, so the cube renders as a black box and
        the first thing a buyer sees teaches them nothing. This paints a
        cobbled stone tile with the add-on's own operators, so the opening
        frame shows crisp texels on a model - which is the entire product in
        one look.

        Cobbles, not brick courses, deliberately: Blender's unwrap lays a
        cube's side faces on their side, so anything with a strong horizontal
        grain renders rotated a quarter turn on four of the six faces. Roughly
        square stones read correctly whichever way the face lands.
        """
        doc = tex_doc.get(img)
        c = doc.canvas
        L = c.layers[c.active]
        w, h = c.w, c.h
        stone = [c.add_colour(x) for x in tools.make_ramp((124, 112, 98, 255), 5)]

        def put(points, v):
            for x, y in points:
                L.set(x, y, v)

        put(R.rect(0, 0, w - 1, h - 1, filled=True), stone[0])
        step = max(8, w // 8)
        for gy in range(0, h, step):
            for gx in range(0, w, step):
                # a little jitter so it reads as stone, not as tiling
                k = (gx * 7 + gy * 13) // step
                inset = 1 + (k % 2)
                body = stone[3] if k % 3 else stone[2]
                x0, y0 = gx + inset, gy + inset
                x1, y1 = gx + step - 2, gy + step - 2
                put(R.rect(x0, y0, x1, y1, filled=True), body)
                put(R.line(x0, y0, x1, y0), stone[4])       # lit top edge
                put(R.line(x0, y0, x0, y1), stone[4])       # lit left edge
                put(R.line(x0, y1, x1, y1), stone[1])       # shadowed bottom
                put(R.line(x1, y0, x1, y1), stone[1])
                if k % 4 == 0:
                    L.set(x0 + 2, y0 + 2, stone[1])         # a chip
        doc.flush()

    @staticmethod
    def _frame_later(screen_name):
        """Frame both editors once Blender has actually drawn them."""
        def go():
            screen = bpy.data.screens.get(screen_name)
            if screen is None:
                return None
            win = bpy.context.window_manager.windows[0]
            for area in screen.areas:
                sp = area.spaces.active
                if area.type == "VIEW_3D":
                    # Written directly. view_selected() needs a context that is
                    # not reliably there right after a workspace switch, and a
                    # silent failure here is a buyer opening onto empty grey.
                    r3d = getattr(sp, "region_3d", None)
                    if r3d is not None:
                        r3d.view_location = (0.0, 0.0, 0.0)
                        r3d.view_distance = 3.2
                        r3d.view_rotation = mathutils.Euler(
                            (math.radians(62), 0.0, math.radians(40)),
                            "XYZ").to_quaternion()
                        r3d.view_perspective = "PERSP"
                elif area.type == "IMAGE_EDITOR" and getattr(sp, "image", None):
                    region = next((r for r in area.regions
                                   if r.type == "WINDOW"), None)
                    try:
                        with bpy.context.temp_override(window=win, screen=screen,
                                                       area=area, region=region,
                                                       space_data=sp):
                            bpy.ops.image.view_all(fit_view=True)
                    except Exception:
                        pass
                area.tag_redraw()
            return None
        bpy.app.timers.register(go, first_interval=0.30)

    def _welcome_scene(self, context, screen):
        """Swap the factory scene for something that says 'pixel art tool'."""
        for obj in list(context.scene.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        v3d = next((a for a in screen.areas if a.type == "VIEW_3D"), None)
        if v3d is None:
            return None
        region = next((r for r in v3d.regions if r.type == "WINDOW"), None)
        with context.temp_override(window=context.window, screen=screen,
                                   area=v3d, region=region):
            bpy.ops.texel.add_cube(size=1.0, texture=64)
            # Dogfood: the default cube unwrap lays side faces on their side, so
            # a brick course renders as vertical bars - the exact defect this
            # add-on exists to fix, on its own welcome screen. Our unwrap puts
            # every face on the texel grid at one density.
            try:
                bpy.ops.texel.pixel_art_unwrap()
            except Exception:
                pass
            bpy.ops.object.select_all(action="SELECT")
            bpy.ops.view3d.view_selected()
            bpy.ops.object.select_all(action="DESELECT")
        img = next((i for i in bpy.data.images if i.name.endswith("Texture")), None)
        if img is not None:
            self._paint_welcome_tile(img)
            for a in screen.areas:
                sp = a.spaces.active
                if a.type == "IMAGE_EDITOR" and hasattr(sp, "image"):
                    sp.image = img
                    r = next((x for x in a.regions if x.type == "WINDOW"), None)
                    with context.temp_override(window=context.window,
                                               screen=screen, area=a, region=r):
                        bpy.ops.image.view_all(fit_view=True)
        return img

    def execute(self, context):
        name = "Texel"
        if name in bpy.data.workspaces:
            context.window.workspace = bpy.data.workspaces[name]
            self.report({"INFO"}, "Switched to the Texel workspace")
            return {"FINISHED"}

        # ---- the fast path: append a workspace that was composed offline.
        #
        # Building a layout live means area_split, a workspace switch and a
        # scene edit all inside one operator, and Blender processes none of
        # them until the operator returns - so every read afterwards is stale.
        # That is not a bug to work around, it is how Blender works, and it is
        # why the comparable add-on ships prebuilt workspace .blend files too.
        # `make_workspace.py` composes ours once, in a GUI, where the operators
        # behave. Appending the result is a single atomic call.
        blend = os.path.join(os.path.dirname(__file__), "workspace.blend")
        if os.path.exists(blend):
            have = {w.as_pointer() for w in bpy.data.workspaces}
            try:
                bpy.ops.wm.append(filepath=os.path.join(blend, "WorkSpace", name),
                                  directory=os.path.join(blend, "WorkSpace") + os.sep,
                                  filename=name, link=False)
            except Exception as e:
                self.report({"WARNING"}, f"Could not append the workspace: {e}")
            fresh = [w for w in bpy.data.workspaces if w.as_pointer() not in have]
            if fresh:
                ws = fresh[0]
                ws.name = name                  # strip any .001 Blender added
                context.window.workspace = ws
                if self.tidy_scene and self._is_factory_scene(context):
                    self._welcome_scene(context, ws.screens[0])
                # scene settings live in the SCENE, not the workspace, so an
                # appended layout brings none of them - they have to be applied
                # on both paths or the fast one quietly skips them
                self._exact_colours(context)
                self._frame_later(ws.screens[0].name)
                context.scene.texel.status = (
                    "Texel workspace ready. Pick the Texel tab in either sidebar")
                self.report({"INFO"}, context.scene.texel.status)
                return {"FINISHED"}

        # ---- fallback: no workspace.blend (a partial install, or someone
        # running from source). Build it live. Slower and fussier, but a
        # missing file must never leave the button doing nothing.
        #
        # `workspace.duplicate()` switches the window to the COPY, but
        # `context.window.workspace` still reports the old one from inside this
        # operator. Trusting it renamed the user's own Layout workspace to
        # "Texel" and left them stranded on a stray "Layout.001" - one click,
        # and their default workspace was gone. Identify the new one by
        # difference instead of by context.
        before = {w.as_pointer() for w in bpy.data.workspaces}
        bpy.ops.workspace.duplicate()
        made = [w for w in bpy.data.workspaces if w.as_pointer() not in before]
        if not made:
            self.report({"WARNING"}, "Blender did not create a workspace")
            return {"CANCELLED"}
        ws = made[0]
        ws.name = name
        context.window.workspace = ws
        screen = ws.screens[0]

        v3ds = [a for a in screen.areas if a.type == "VIEW_3D"]
        if v3ds:
            big = max(v3ds, key=lambda a: a.width * a.height)
            before = {a.as_pointer() for a in screen.areas}
            with context.temp_override(window=context.window, screen=screen,
                                       area=big):
                bpy.ops.screen.area_split(direction="VERTICAL", factor=0.46)
            # Which half area_split hands back as "new" is not something to
            # assume - it put the canvas on the RIGHT the first time this was
            # written. Take the leftmost of the pair by measurement instead.
            pair = [a for a in screen.areas if a.type == "VIEW_3D"
                    and (a.as_pointer() not in before or a is big)]
            left = min(pair, key=lambda a: a.x) if pair else big
            left.type = "IMAGE_EDITOR"

            # a timeline under the canvas, so playback is where the frames are
            if self.timeline:
                with context.temp_override(window=context.window, screen=screen,
                                           area=left):
                    bpy.ops.screen.area_split(direction="HORIZONTAL", factor=0.82)
                col = [a for a in screen.areas if a.type == "IMAGE_EDITOR"
                       and abs(a.x - left.x) < 4]
                if len(col) > 1:
                    bottom = min(col, key=lambda a: a.y)
                    bottom.type = "DOPESHEET_EDITOR"
                    bottom.spaces.active.mode = "TIMELINE"

        for area in screen.areas:
            for space in area.spaces:
                if hasattr(space, "show_region_ui"):
                    space.show_region_ui = True
            # `area.type` reports the new value before `spaces.active` has
            # actually swapped, so check the SPACE, not the area.
            sp = area.spaces.active
            if hasattr(sp, "shading") and hasattr(sp.shading, "use_scene_lights"):
                sp.shading.type = "MATERIAL"       # or the texture is invisible
                sp.shading.use_scene_lights = False  # even light while painting

        self._exact_colours(context)

        fresh = None
        if self.tidy_scene and self._is_factory_scene(context):
            fresh = self._welcome_scene(context, screen)

        self._frame_later(screen.name)
        bits = ["canvas", "model"]
        if self.timeline:
            bits.append("timeline")
        if fresh is not None:
            bits.append("a 64px cube ready to paint")
        context.scene.texel.status = (
            f"Workspace ready ({' | '.join(bits)}). "
            "Pick the Texel tab in either sidebar")
        self.report({"INFO"}, context.scene.texel.status)
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
