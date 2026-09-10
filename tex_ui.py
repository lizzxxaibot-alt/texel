"""Panels. Same layout in both editors, drawn from one function."""
import bpy
from bpy.types import Panel
from . import tex_doc


def _draw_tools(layout, s):
    col = layout.column(align=True)
    grid = col.grid_flow(row_major=True, columns=4, even_columns=True, align=True)
    grid.prop(s, "tool", expand=True)
    col.separator()
    col.prop(s, "colour", text="")
    row = col.row(align=True)
    row.prop(s, "brush_size")
    row.prop(s, "pixel_perfect", text="", icon="MOD_SMOOTH")
    if s.brush_size > 1:
        col.prop(s, "brush_shape", text="")
    if s.tool in {"RECT", "ELLIPSE"}:
        col.prop(s, "filled")
    if s.tool == "FILL":
        r = col.row(align=True)
        r.prop(s, "tolerance")
        r.prop(s, "contiguous", text="", icon="MESH_DATA")
    r = col.row(align=True)
    r.prop(s, "mirror_x", toggle=True)
    r.prop(s, "mirror_y", toggle=True)
    col.operator("texel.shortcuts_restore", text="Restore Defaults", icon="LOOP_BACK")


class _Base:
    bl_category = "Texel"
    bl_region_type = "UI"


class TEXEL_PT_tools_2d(_Base, Panel):
    bl_space_type = "IMAGE_EDITOR"
    bl_label = "Texel"

    def draw(self, context):
        s = context.scene.texel
        self.layout.operator("texel.canvas_new", icon="IMAGE_DATA")
        img = context.space_data.image
        if img is None:
            self.layout.label(text="No image open", icon="INFO")
            return
        _draw_tools(self.layout, s)
        self.layout.operator("texel.paint", icon="BRUSH_DATA")


class TEXEL_PT_sprite(_Base, Panel):
    bl_space_type = "IMAGE_EDITOR"
    bl_label = "Sprite"
    bl_parent_id = "TEXEL_PT_tools_2d"

    def draw(self, context):
        s = context.scene.texel
        img = context.space_data.image
        doc = tex_doc.get(img, create=False) if img else None
        col = self.layout.column(align=True)
        row = col.row(align=True)
        row.operator("texel.trim", icon="FULLSCREEN_EXIT")
        row.operator("texel.colour_count", text="", icon="COLOR")
        col.separator()
        col.label(text="Frames")
        row = col.row(align=True)
        row.operator("texel.frame_add", icon="ADD")
        row.operator("texel.track_add", text="", icon="OUTLINER_OB_GROUP_INSTANCE")
        row.operator("texel.track_remove", text="", icon="X")
        row.prop(s, "onion_skin", text="", icon="ONIONSKIN_ON")
        if doc is not None and doc.canvas.frame_count():
            c = doc.canvas
            n = c.frame_count()
            cur = min(s.current_frame, n - 1)
            # the cel grid: a row per track, a column per frame. The active cel
            # is the one you paint on.
            active = c.layers[c.active]
            movable = len(c.tracks) > 1

            def grid_row():
                """One row of the grid: name | cells | reorder arrows.

                Both splits are identical on every row, including the number
                row, or the frame numbers drift out from under their column.
                """
                sp = col.split(factor=0.24, align=True)
                name = sp.row(align=True)
                rest = sp.split(factor=0.999 if not movable else 0.78, align=True)
                return name, rest.row(align=True), rest.row(align=True)

            for track in reversed(c.tracks):          # top track drawn first
                name, cells, tail = grid_row()
                name.label(text=track[:8])
                for f in range(n):
                    cel = c.cel(track, f)
                    sub = cells.row(align=True)
                    sub.alert = (cel is active)
                    op = sub.operator("texel.cel_select",
                                      text="*" if (cel and any(cel.px)) else ".",
                                      depress=(f == cur))
                    op.track = track
                if movable:                      # reorder: background to the back
                    for icon, d in (("TRIA_UP", 1), ("TRIA_DOWN", -1)):
                        op = tail.operator("texel.track_move", text="", icon=icon)
                        op.name, op.delta = track, d
            name, cells, tail = grid_row()
            name.label(text="")
            for f in range(n):
                cells.operator("texel.frame_show", text=str(f + 1),
                               depress=(f == cur)).index = f
            if movable:
                tail.label(text="")
            col.separator()
            row = col.row(align=True)
            row.operator("texel.anim_play", icon="PLAY")
            row.operator("texel.anim_bind", text="", icon="TIME")
            row.operator("texel.anim_unbind", text="", icon="X")
            row = col.row(align=True)
            row.prop(context.scene.render, "fps", text="FPS")
            row.operator("texel.frame_hold", text="", icon="PREVIEW_RANGE").index = cur
            col.separator()
            row = col.row(align=True)
            row.operator("texel.sprite_sheet", text="Sheet", icon="IMAGE_DATA")
            row.operator("texel.export_gif", text="GIF", icon="RENDER_ANIMATION")
            col.operator("texel.export_anim_data", icon="FILE_TEXT")
        col.separator()
        col.label(text="Reference")
        row = col.row(align=True)
        row.operator("texel.reference_add", icon="IMAGE_REFERENCE")
        row.operator("texel.reference_remove", text="", icon="X")


class TEXEL_PT_tools_3d(_Base, Panel):
    bl_space_type = "VIEW_3D"
    bl_label = "Texel"

    def draw(self, context):
        s = context.scene.texel
        _draw_tools(self.layout, s)
        self.layout.operator("texel.paint", icon="BRUSH_DATA")


class TEXEL_PT_layers(_Base, Panel):
    bl_space_type = "IMAGE_EDITOR"
    bl_label = "Layers"
    bl_parent_id = "TEXEL_PT_tools_2d"

    def draw(self, context):
        img = context.space_data.image
        doc = tex_doc.get(img, create=False) if img else None
        if doc is None:
            self.layout.label(text="No canvas yet", icon="INFO")
            return
        col = self.layout.column(align=True)
        row = col.row(align=True)
        row.operator("texel.layer_add", text="", icon="ADD")
        row.operator("texel.layer_remove", text="", icon="REMOVE")
        row.operator("texel.layer_merge_down", text="", icon="TRIA_DOWN_BAR")
        col.separator()
        # top of the stack first, which is how a layer panel reads. Once there
        # are frames, only the CURRENT frame's cels are listed - four tracks
        # across eight frames is thirty-two rows, and thirty-one of them are
        # about a moment you are not looking at.
        c = doc.canvas
        cur = min(context.scene.texel.current_frame, max(0, c.frame_count() - 1))
        shown = [i for i, l in enumerate(c.layers)
                 if l.frame is None or l.frame == cur]
        for i in reversed(shown):
            layer = doc.canvas.layers[i]
            r = col.row(align=True)
            r.alert = (i == doc.canvas.active)
            op = r.operator("texel.layer_select", text=layer.name,
                            emboss=(i == doc.canvas.active))
            op.index = i
            r.operator("texel.layer_toggle", text="",
                       icon="HIDE_OFF" if layer.visible else "HIDE_ON").index = i
        # core.Layer is a plain Python object, so layout.prop cannot bind to it -
        # the value is shown on a button that opens a dialog instead
        active = doc.canvas.layers[doc.canvas.active]
        col.separator()
        row = col.row(align=True)
        row.label(text="Opacity")
        row.operator("texel.layer_opacity", text=f"{active.opacity:.0%}")
        col.separator()
        row = col.row(align=True)
        row.operator("texel.layer_duplicate", text="Duplicate", icon="DUPLICATE")
        row.operator("texel.layer_merge_selected", text="", icon="SELECT_EXTEND")
        row = col.row(align=True)
        row.operator("texel.layer_group", text="Group", icon="OUTLINER_OB_GROUP_INSTANCE")
        row.operator("texel.layer_ungroup", text="", icon="X")
        col.operator("texel.export_layers", icon="EXPORT")


class TEXEL_PT_palette(_Base, Panel):
    bl_space_type = "IMAGE_EDITOR"
    bl_label = "Palette"
    bl_parent_id = "TEXEL_PT_tools_2d"

    def draw(self, context):
        img = context.space_data.image
        doc = tex_doc.get(img, create=False) if img else None
        col = self.layout.column(align=True)
        row = col.row(align=True)
        row.operator("texel.palette_load", text="", icon="FILE_FOLDER")
        row.operator("texel.palette_save", text="", icon="FILE_TICK")
        row.operator("texel.palette_from_image", text="", icon="IMAGE_DATA")
        row.operator("texel.palette_lospec", text="Lospec", icon="URL")
        if doc is None:
            return
        swatches = doc.canvas.palette[1:]
        if not swatches:
            col.label(text="No swatches yet", icon="INFO")
            return
        col.separator()
        grid = col.grid_flow(row_major=True, columns=8, even_columns=True, align=True)
        for i, _c in enumerate(swatches, start=1):
            grid.operator("texel.swatch_use", text=str(i), emboss=True).index = i
        col.separator()
        row = col.row(align=True)
        row.operator("texel.swatch_add", text="", icon="ADD")
        row.operator("texel.swatch_remove", text="", icon="REMOVE")
        row.operator("texel.palette_sort", text="Sort", icon="SORTSIZE")
        row.operator("texel.palette_clear", text="", icon="TRASH")
        row = col.row(align=True)
        row.operator("texel.palette_ramp", text="Generate Ramp", icon="COLORSET_02_VEC")
        row.operator("texel.replace_colour", text="", icon="EYEDROPPER")
        col.operator("texel.adjust", icon="MODIFIER")


class TEXEL_PT_density(_Base, Panel):
    bl_space_type = "VIEW_3D"
    bl_label = "Texel Density"
    bl_parent_id = "TEXEL_PT_tools_3d"

    def draw(self, context):
        s = context.scene.texel
        col = self.layout.column(align=True)
        col.prop(s, "target_density")
        col.operator("texel.density_detect", icon="VIEWZOOM")
        col.operator("texel.density_apply", icon="CHECKMARK")
        col.operator("texel.snap_uvs", icon="SNAP_ON")
        if s.status:
            col.separator()
            row = col.row(align=True)
            row.label(text=s.status, icon="INFO")
            row.operator("texel.clear_report", text="", icon="X")


class TEXEL_PT_showcase(_Base, Panel):
    bl_space_type = "VIEW_3D"
    bl_label = "Showcase"
    bl_parent_id = "TEXEL_PT_tools_3d"

    def draw(self, context):
        s = context.scene.texel
        col = self.layout.column(align=True)
        col.prop(s, "showcase_preset", text="")
        col.prop(s, "showcase_move", text="")
        col.separator()
        col.operator("texel.showcase_setup", icon="LIGHT_SUN")
        row = col.row(align=True)
        row.operator("texel.showcase_render", icon="RENDER_ANIMATION")
        row.operator("texel.showcase_clear", text="", icon="TRASH")
        col.separator()
        box = col.box().column(align=True)
        if s.showcase_move != "STILL":
            box.prop(s, "showcase_frames")
        box.prop(s, "showcase_samples")
        r = box.row(align=True)
        r.prop(s, "showcase_width", text="W")
        r.prop(s, "showcase_height", text="H")
        box.prop(s, "showcase_output", text="")


class TEXEL_PT_select(_Base, Panel):
    """Selection and clipboard.

    These were registered but unreachable: 56 of the 92 operators had no button
    anywhere, so a buyer could only find them through F3 search. A feature you
    paid for and cannot see is worse than one that does not exist.
    """
    bl_space_type = "IMAGE_EDITOR"
    bl_label = "Select"
    bl_parent_id = "TEXEL_PT_tools_2d"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        col = self.layout.column(align=True)
        row = col.row(align=True)
        row.operator("texel.select_all", text="All")
        row.operator("texel.deselect", text="None")
        row.operator("texel.select_invert", text="Invert")
        row = col.row(align=True)
        row.operator("texel.select_colour", text="By Colour", icon="EYEDROPPER")
        row.operator("texel.select_linked", text="Linked", icon="MESH_DATA")
        row = col.row(align=True)
        row.operator("texel.select_grow", text="Grow", icon="FULLSCREEN_ENTER")
        row.operator("texel.selection_outline", text="Outline", icon="MESH_CIRCLE")
        col.separator()
        # Two per row, and every one of them labelled. An icon-only rotate
        # button next to a labelled Flip reads as an arrow you have to hover to
        # identify, which is the sidebar equivalent of not shipping the feature.
        for a, b in ((("FLIP_H", "Flip X", "MOD_MIRROR"),
                      ("FLIP_V", "Flip Y", "MOD_MIRROR")),
                     (("ROT_CW", "Rotate CW", "LOOP_FORWARDS"),
                      ("ROT_CCW", "Rotate CCW", "LOOP_BACK"))):
            row = col.row(align=True)
            for mode, label, icon in (a, b):
                row.operator("texel.selection_transform", text=label,
                             icon=icon).mode = mode
        col.operator("texel.selection_transform", text="Scale Selection",
                     icon="FULLSCREEN_ENTER").mode = "SCALE"
        col.separator()
        row = col.row(align=True)
        row.operator("texel.clipboard_cut", text="Cut", icon="X")
        row.operator("texel.clipboard_copy", text="Copy", icon="COPYDOWN")
        row.operator("texel.clipboard_paste", text="Paste", icon="PASTEDOWN")


class TEXEL_PT_canvas(_Base, Panel):
    """Whole-canvas operations, and the tools that check your work."""
    bl_space_type = "IMAGE_EDITOR"
    bl_label = "Canvas"
    bl_parent_id = "TEXEL_PT_tools_2d"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        col = self.layout.column(align=True)
        row = col.row(align=True)
        row.operator("texel.flip_canvas", text="Flip", icon="MOD_MIRROR")
        row.operator("texel.rotate_canvas", text="Rotate", icon="FILE_REFRESH")
        row = col.row(align=True)
        row.operator("texel.canvas_resize", text="Resize", icon="FULLSCREEN_ENTER")
        row.operator("texel.symmetry_center", text="", icon="MOD_MIRROR")
        col.separator()
        col.operator("texel.check_tileable", icon="TEXTURE")
        col.operator("texel.shift_wrap", icon="ARROW_LEFTRIGHT")
        col.separator()
        col.operator("texel.outline_sprite", icon="MESH_CIRCLE")
        col.operator("texel.dither_fill", icon="TEXTURE_DATA")
        col.separator()
        row = col.row(align=True)
        row.operator("texel.custom_brush_add", text="Brush From Selection", icon="ADD")
        row.operator("texel.custom_brush_remove", text="", icon="REMOVE")
        col.separator()
        row = col.row(align=True)
        row.operator("texel.grid_add", text="Grid Layer", icon="GRID")
        row.operator("texel.grid_toggle", text="", icon="HIDE_OFF")
        col.operator("texel.viewport_grid_toggle", icon="MESH_GRID")
        col.separator()
        col.operator("texel.show_in_3d", icon="VIEW3D")


class TEXEL_PT_file(_Base, Panel):
    """Round-tripping the canvas with a file on disk, for Aseprite users."""
    bl_space_type = "IMAGE_EDITOR"
    bl_label = "File"
    bl_parent_id = "TEXEL_PT_tools_2d"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        col = self.layout.column(align=True)
        col.operator("texel.file_place", icon="FILE_TICK")
        row = col.row(align=True)
        row.operator("texel.file_changed", text="Reload If Changed", icon="FILE_REFRESH")
        row.operator("texel.reload_forget", text="", icon="X")


class TEXEL_PT_setup(_Base, Panel):
    """Getting a model ready to paint. This is the first thing a new buyer
    needs and it had no button at all."""
    bl_space_type = "VIEW_3D"
    bl_label = "Setup"
    bl_parent_id = "TEXEL_PT_tools_3d"

    def draw(self, context):
        col = self.layout.column(align=True)
        col.operator("texel.add_cube", icon="MESH_CUBE")
        col.operator("texel.pixel_art_unwrap", icon="UV")
        col.operator("texel.unwrap_info", text="", icon="QUESTION")
        col.separator()
        col.operator("texel.workspace_create", icon="WORKSPACE")
        row = col.row(align=True)
        row.operator("texel.setup_viewport", text="Viewport", icon="SHADING_TEXTURE")
        row.operator("texel.restore_viewport", text="", icon="LOOP_BACK")
        col.separator()
        row = col.row(align=True)
        row.operator("texel.pick_texture", text="Pick Texture", icon="EYEDROPPER")
        row.operator("texel.show_canvas", text="", icon="IMAGE_DATA")
        # The pixel-grid buttons are NOT here: all three poll for an Image
        # Editor, so in this panel they would render permanently greyed out.
        # They live in the Canvas panel on the 2D side. Found by the end-to-end
        # suite, which is the only thing that actually presses every button.


class TEXEL_PT_zones(_Base, Panel):
    """Per-face-group density. A hero prop at 64 px/unit inside a world at 24."""
    bl_space_type = "VIEW_3D"
    bl_label = "Density Zones"
    bl_parent_id = "TEXEL_PT_density"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        col = self.layout.column(align=True)
        col.operator("texel.zone_from_selection", icon="RESTRICT_SELECT_OFF")
        col.operator("texel.zone_grid", icon="MESH_GRID")
        col.operator("texel.detect_zones", icon="VIEWZOOM")
        col.separator()
        col.operator("texel.zone_apply", icon="CHECKMARK")
        row = col.row(align=True)
        row.operator("texel.zone_select", text="Select", icon="RESTRICT_SELECT_OFF")
        row.operator("texel.zone_info", text="", icon="INFO")
        col.operator("texel.zones_clear", icon="TRASH")


CLASSES = (TEXEL_PT_tools_2d, TEXEL_PT_layers, TEXEL_PT_palette,
           TEXEL_PT_sprite, TEXEL_PT_select, TEXEL_PT_canvas, TEXEL_PT_file,
           TEXEL_PT_tools_3d, TEXEL_PT_setup, TEXEL_PT_density, TEXEL_PT_zones,
           TEXEL_PT_showcase)


def register():
    for c in CLASSES:
        bpy.utils.register_class(c)


def unregister():
    for c in reversed(CLASSES):
        bpy.utils.unregister_class(c)
