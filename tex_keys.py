"""Keyboard shortcuts.

Every paint tool lets you press B for brush and E for eraser, and one that makes
you reach for a sidebar button instead reads as a prototype in the first thirty
seconds. This was planned for v0.2; it is baseline, so it ships in v0.1.

The bindings live in Blender's own keymap editor (Preferences > Keymap, search
"texel"), which is the whole reason to register a keymap instead of grabbing raw
events: **the user can rebind every one of them without touching our code.**

Which keys are safe was MEASURED against Blender 4.5's own keymap, not guessed:

  Image Editor   B E L U C F I M D all free (only J is taken, by
                 image.cycle_render_slot) - so the 2D surface gets the full set.
  3D View        B is view3d.select_box, C is view3d.select_circle, W is
                 wm.tool_set_by_id; Object Mode also takes I, M, K and X.
                 So the viewport gets ONE binding, D, and keeps every Blender
                 default intact. Painting there is what you are doing anyway.

Nothing is bound to a mouse button. LEFTMOUSE in either editor is select, and an
add-on that takes it over is a bug report we would deserve.

`test_keys.py` re-runs that measurement against whatever Blender is installed,
so a future version that claims one of these letters fails the gate instead of
silently stomping the user.
"""
import bpy

# key -> tool enum value. Order is the order they appear in the sidebar.
TOOL_KEYS = (
    ("B", "PENCIL"),        # brush
    ("E", "ERASER"),
    ("L", "LINE"),
    ("U", "RECT"),          # not R - R is Rotate nearly everywhere
    ("C", "ELLIPSE"),       # circle
    ("F", "FILL"),
    ("I", "PICK"),          # eyedropper, as in every other paint tool
)

_keymaps = []


class TEXEL_OT_set_tool(bpy.types.Operator):
    """One operator behind every tool shortcut, so the keymap editor lists seven
    readable entries instead of seven copies of a generic setter."""
    bl_idname = "texel.set_tool"
    bl_label = "Set Texel Tool"
    bl_description = "Switch the active Texel tool"
    bl_options = {"REGISTER", "INTERNAL"}

    tool: bpy.props.StringProperty(default="PENCIL")

    def execute(self, context):
        s = context.scene.texel
        try:
            s.tool = self.tool
        except TypeError:
            self.report({"WARNING"}, f"No such tool: {self.tool}")
            return {"CANCELLED"}
        s.status = f"Tool: {self.tool.title()}"
        for area in context.screen.areas:
            area.tag_redraw()
        return {"FINISHED"}


class TEXEL_OT_mirror_toggle(bpy.types.Operator):
    bl_idname = "texel.mirror_toggle"
    bl_label = "Toggle Mirror"
    bl_description = "Toggle mirrored painting on an axis"
    # INTERNAL: the sidebar already has mirror_x / mirror_y as toggle props, so
    # this operator exists only to give the keyboard shortcut something to call.
    # A second button for the same state would be clutter, and the panel-
    # coverage gate is right to insist that every non-internal operator has one.
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    axis: bpy.props.EnumProperty(items=(("X", "X", ""), ("Y", "Y", "")),
                                 default="X")

    def execute(self, context):
        s = context.scene.texel
        attr = "mirror_x" if self.axis == "X" else "mirror_y"
        setattr(s, attr, not getattr(s, attr))
        s.status = f"Mirror {self.axis}: {'on' if getattr(s, attr) else 'off'}"
        for area in context.screen.areas:
            area.tag_redraw()
        return {"FINISHED"}


CLASSES = (TEXEL_OT_set_tool, TEXEL_OT_mirror_toggle)

# What register() will install. Kept as data so test_keys.py can check it
# against Blender's defaults without duplicating the list.
BINDINGS = (
    ("Image", "IMAGE_EDITOR", "texel.set_tool", "B", {"tool": "PENCIL"}),
    ("Image", "IMAGE_EDITOR", "texel.set_tool", "E", {"tool": "ERASER"}),
    ("Image", "IMAGE_EDITOR", "texel.set_tool", "L", {"tool": "LINE"}),
    ("Image", "IMAGE_EDITOR", "texel.set_tool", "U", {"tool": "RECT"}),
    ("Image", "IMAGE_EDITOR", "texel.set_tool", "C", {"tool": "ELLIPSE"}),
    ("Image", "IMAGE_EDITOR", "texel.set_tool", "F", {"tool": "FILL"}),
    ("Image", "IMAGE_EDITOR", "texel.set_tool", "I", {"tool": "PICK"}),
    ("Image", "IMAGE_EDITOR", "texel.mirror_toggle", "M", {"axis": "X"}),
    ("Image", "IMAGE_EDITOR", "texel.paint", "D", {}),
    ("3D View", "VIEW_3D", "texel.paint", "D", {}),
)


def register():
    for c in CLASSES:
        bpy.utils.register_class(c)

    kc = bpy.context.window_manager.keyconfigs.addon
    if kc is None:
        return                          # background mode has no addon keyconfig

    for km_name, space, idname, key, props in BINDINGS:
        km = kc.keymaps.new(name=km_name, space_type=space)
        kmi = km.keymap_items.new(idname, key, "PRESS")
        for k, v in props.items():
            setattr(kmi.properties, k, v)
        _keymaps.append((km, kmi))


def unregister():
    for km, kmi in reversed(_keymaps):
        try:
            km.keymap_items.remove(kmi)
        except Exception:
            pass                        # already gone with the keyconfig
    _keymaps.clear()
    for c in reversed(CLASSES):
        bpy.utils.unregister_class(c)
