"""Scene-level state. One PropertyGroup, deliberately flat."""
import bpy
from bpy.props import (BoolProperty, EnumProperty, FloatProperty,
                       FloatVectorProperty, IntProperty, StringProperty)

TOOLS = [
    ("PENCIL",  "Pencil",  "Freehand, one texel per sample", "GREASEPENCIL", 0),
    # PANEL_CLOSE draws an X - a close button, not an eraser. Checked by
    # rendering the candidates and looking, not by reading identifiers: the
    # other six are fine, because IPO_LINEAR draws a line, MESH_PLANE a square,
    # MESH_CIRCLE a circle and SNAP_FACE a filled square, whatever their names
    # suggest.
    ("ERASER",  "Eraser",  "Freehand erase to transparent",
     "EVENT_TABLET_ERASER", 1),
    ("LINE",    "Line",    "Straight line, drag to place",   "IPO_LINEAR",   2),
    ("RECT",    "Rect",    "Rectangle, drag to place",       "MESH_PLANE",   3),
    ("ELLIPSE", "Ellipse", "Ellipse, drag to place",         "MESH_CIRCLE",  4),
    ("FILL",    "Fill",    "Flood fill a region",            "SNAP_FACE",    5),
    ("PICK",    "Pick",    "Sample a colour from the canvas","EYEDROPPER",   6),
]


class TexelSettings(bpy.types.PropertyGroup):
    tool: EnumProperty(name="Tool", items=TOOLS, default="PENCIL")
    colour: FloatVectorProperty(
        name="Colour", subtype="COLOR_GAMMA", size=4, min=0.0, max=1.0,
        default=(0.0, 0.0, 0.0, 1.0))
    brush_size: IntProperty(name="Size", default=1, min=1, max=64,
                            description="Brush width, in texels")
    brush_shape: EnumProperty(
        name="Shape", default="SQUARE",
        items=[("SQUARE", "Square", "Hard corners - the default, and correct at 1px"),
               ("ROUND", "Round", "Circular - what you want above ~3 texels"),
               ("DIAMOND", "Diamond", "45-degree, for isometric work")])
    pixel_perfect: BoolProperty(
        name="Pixel Perfect", default=True,
        description="Drop L-shaped corner texels from freehand strokes")
    filled: BoolProperty(name="Filled", default=False,
                         description="Fill shapes instead of outlining them")
    tolerance: IntProperty(name="Tolerance", default=0, min=0, max=255,
                           description="Flood fill colour tolerance, 0-255")
    contiguous: BoolProperty(name="Contiguous", default=True,
                             description="Fill only the connected region")
    mirror_x: BoolProperty(name="Mirror X", default=False)
    mirror_y: BoolProperty(name="Mirror Y", default=False)
    target_density: FloatProperty(
        name="Texel Density", default=32.0, min=0.001, soft_max=512.0,
        description="Pixels per world unit to aim for")
    status: StringProperty(name="Status", default="")

    # ---- Showcase: turn finished art into a presentable still or video
    showcase_preset: EnumProperty(
        name="Mood", default="GOLDEN",
        items=[("GOLDEN", "Golden Hour", "Warm low sun, soft haze"),
               ("TORCH", "Torchlit", "Dark interior, firelight"),
               ("COOL", "Cool Sci-Fi", "Cyan key, dense atmosphere"),
               ("NOON", "Hard Noon", "Bright sky, crisp shadows"),
               ("ICE", "Ice Cavern", "Cold blue, heavy haze"),
               ("STUDIO", "Clean Studio", "Neutral, no fog - for store images")])
    showcase_move: EnumProperty(
        name="Move", default="ARC",
        items=[("ORBIT", "Orbit", "Circle the subject - best for one prop"),
               ("PUSH", "Push In", "Move toward it - best for a scene"),
               ("ARC", "Arc", "Swing round and close in"),
               ("STILL", "Still", "One frame")])
    showcase_frames: IntProperty(name="Frames", default=96, min=2, max=600,
                                 description="24 frames is one second")
    showcase_samples: IntProperty(name="Samples", default=48, min=4, max=1024)
    showcase_width: IntProperty(name="Width", default=1280, min=64, max=7680)
    showcase_height: IntProperty(name="Height", default=720, min=64, max=4320)
    current_frame: IntProperty(name="Frame", default=0, min=0)
    onion_skin: BoolProperty(
        name="Onion Skin", default=True,
        description="Ghost the neighbouring frame at 28% while you draw")
    layer_opacity: FloatProperty(
        name="Layer Opacity", default=1.0, min=0.0, max=1.0,
        description="Opacity of the active layer")
    showcase_output: StringProperty(
        name="Output", default="//texel_showcase/", subtype="DIR_PATH")


def rgba_bytes(col) -> tuple[int, int, int, int]:
    return tuple(max(0, min(255, round(c * 255))) for c in col)


def register():
    bpy.utils.register_class(TexelSettings)
    bpy.types.Scene.texel = bpy.props.PointerProperty(type=TexelSettings)


def unregister():
    del bpy.types.Scene.texel
    bpy.utils.unregister_class(TexelSettings)
