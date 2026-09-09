"""Showcase: turn finished pixel art into a presentable still or video.

The problem this solves is one every pixel artist hits and no paint tool answers:
you have made a good texture, and now you need an image for your store page.
Lighting a scene, placing a camera and getting nearest-neighbour filtering right
is a separate skill from drawing, and getting it wrong makes good art look bad.

So: pick a mood, press a button. Every preset here was tuned on real renders,
and three of the traps are baked in rather than left to the user:

  * texture filtering is forced to Closest, or texels blur into mush
  * fog is a BOUNDED box, never a world volume - a world volume attenuates light
    across infinite space and drops a lit scene to near black
  * the view transform is AgX Base, because the contrastier looks crush shadow
    detail in a fogged interior and the render reads as a fault, not a mood
"""
import math
import os
import shutil
import subprocess

import bpy
from bpy.props import EnumProperty, IntProperty, StringProperty
from bpy.types import Operator

COLLECTION = "Texel Showcase"

# (key, label, description, sun_colour, sun_energy, sun_rot, world_col, world_str,
#  fog_density, fog_colour, rim_colour, rim_energy)
PRESETS = {
    "GOLDEN": dict(label="Golden Hour", sun=((1.0, 0.80, 0.56), 6.0, (48, 0, 116)),
                   world=((0.42, 0.46, 0.66), 1.1), fog=(0.0014, (0.72, 0.58, 0.52)),
                   rim=((1.0, 0.72, 0.42), 260)),
    "TORCH": dict(label="Torchlit", sun=((1.0, 0.66, 0.34), 1.2, (54, 0, 40)),
                  world=((0.06, 0.06, 0.09), 0.4), fog=(0.0024, (0.5, 0.36, 0.26)),
                  rim=((1.0, 0.52, 0.20), 620)),
    "COOL": dict(label="Cool Sci-Fi", sun=((0.66, 0.80, 1.0), 1.8, (58, 0, -30)),
                 world=((0.03, 0.05, 0.08), 0.35), fog=(0.0032, (0.24, 0.44, 0.58)),
                 rim=((0.36, 0.86, 1.0), 520)),
    "NOON": dict(label="Hard Noon", sun=((1.0, 0.94, 0.80), 3.4, (62, 0, 24)),
                 world=((0.55, 0.68, 0.92), 0.75), fog=(0.0009, (0.86, 0.76, 0.60)),
                 rim=((1.0, 0.94, 0.84), 120)),
    "ICE": dict(label="Ice Cavern", sun=((0.66, 0.82, 1.0), 4.2, (68, 0, 40)),
                world=((0.06, 0.12, 0.20), 0.7), fog=(0.0042, (0.44, 0.72, 0.88)),
                rim=((0.36, 0.92, 1.0), 420)),
    "STUDIO": dict(label="Clean Studio", sun=((1.0, 0.98, 0.96), 3.0, (52, 0, 30)),
                   world=((0.55, 0.57, 0.62), 1.6), fog=(0.0, (1, 1, 1)),
                   rim=((0.9, 0.94, 1.0), 300)),
}

PRESET_ITEMS = [(k, v["label"], v["label"]) for k, v in PRESETS.items()]

MOVES = [
    ("ORBIT", "Orbit", "Circle the subject - best for a single prop"),
    ("PUSH", "Push In", "Move toward the subject - best for a scene or corridor"),
    ("ARC", "Arc", "Swing round and close in at the same time"),
    ("STILL", "Still", "One frame, no movement"),
]


def _collection():
    col = bpy.data.collections.get(COLLECTION)
    if col is None:
        col = bpy.data.collections.new(COLLECTION)
        bpy.context.scene.collection.children.link(col)
    return col


def _add(obj):
    for c in obj.users_collection:
        c.objects.unlink(obj)
    _collection().objects.link(obj)
    return obj


def subject_bounds(context):
    """World-space bounds of everything that is NOT part of the showcase rig."""
    show = {o.name for o in _collection().objects}
    pts = []
    for o in context.scene.objects:
        if o.type != "MESH" or o.name in show:
            continue
        for corner in o.bound_box:
            pts.append(o.matrix_world @ __import__("mathutils").Vector(corner))
    if not pts:
        return None
    lo = [min(p[i] for p in pts) for i in range(3)]
    hi = [max(p[i] for p in pts) for i in range(3)]
    centre = [(lo[i] + hi[i]) / 2 for i in range(3)]
    radius = max(max(hi[i] - lo[i] for i in range(3)) / 2, 0.5)
    return centre, radius, lo, hi


class TEXEL_OT_showcase_setup(Operator):
    bl_idname = "texel.showcase_setup"
    bl_label = "Build Showcase"
    bl_description = ("Light and frame your art automatically: camera, lighting preset, "
                      "bounded haze, and nearest-neighbour filtering forced on")
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def execute(self, context):
        s = context.scene.texel
        b = subject_bounds(context)
        if b is None:
            self.report({"WARNING"}, "Nothing to show - add a mesh first")
            return {"CANCELLED"}
        centre, radius, lo, hi = b
        p = PRESETS[s.showcase_preset]

        bpy.ops.texel.showcase_clear()
        col = _collection()

        # --- filtering. Every image texture, every time. This is the single
        # thing most likely to be wrong in a user's file, and it ruins pixel art.
        fixed = 0
        for mat in bpy.data.materials:
            if not mat.use_nodes:
                continue
            for n in mat.node_tree.nodes:
                if n.type == "TEX_IMAGE" and n.interpolation != "Closest":
                    n.interpolation = "Closest"
                    fixed += 1

        # --- key light
        sun_col, sun_e, sun_rot = p["sun"]
        li = bpy.data.lights.new("Texel Key", "SUN")
        li.color, li.energy, li.angle = sun_col, sun_e, math.radians(2.5)
        key = _add(bpy.data.objects.new("Texel Key", li))
        key.rotation_euler = tuple(math.radians(v) for v in sun_rot)

        # --- rim light, opposite the key, for separation from the background
        rim_col, rim_e = p["rim"]
        rl = bpy.data.lights.new("Texel Rim", "AREA")
        rl.color, rl.energy, rl.size = rim_col, rim_e * max(1.0, radius / 3.0), radius
        rim = _add(bpy.data.objects.new("Texel Rim", rl))
        rim.location = (centre[0] - radius * 2.0, centre[1] + radius * 2.0,
                        centre[2] + radius * 1.6)
        rim.rotation_euler = (math.radians(62), 0, math.radians(-125))

        # --- ground, unless the subject already has one
        if hi[2] - lo[2] > 0.05:
            bpy.ops.mesh.primitive_plane_add(size=radius * 14,
                                             location=(centre[0], centre[1], lo[2] - 0.01))
            floor = _add(bpy.context.view_layer.objects.active)
            floor.name = "Texel Ground"
            gm = bpy.data.materials.new("Texel Ground")
            gm.use_nodes = True
            gm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (
                0.05, 0.05, 0.06, 1)
            gm.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.95
            floor.data.materials.append(gm)

        # --- world + BOUNDED haze
        world = bpy.data.worlds.new("Texel World")
        world.use_nodes = True
        wc, ws = p["world"]
        world.node_tree.nodes["Background"].inputs["Color"].default_value = (*wc, 1)
        world.node_tree.nodes["Background"].inputs["Strength"].default_value = ws
        context.scene.world = world
        density, fcol = p["fog"]
        if density > 0:
            bpy.ops.mesh.primitive_cube_add(size=1, location=centre)
            fog = _add(bpy.context.view_layer.objects.active)
            fog.name = "Texel Haze"
            fog.scale = (radius * 8, radius * 8, radius * 6)
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            fog.visible_shadow = False
            fm = bpy.data.materials.new("Texel Haze")
            fm.use_nodes = True
            nt = fm.node_tree
            for n in list(nt.nodes):
                if n.type != "OUTPUT_MATERIAL":
                    nt.nodes.remove(n)
            vs = nt.nodes.new("ShaderNodeVolumeScatter")
            vs.inputs["Density"].default_value = density
            vs.inputs["Color"].default_value = (*fcol, 1)
            vs.inputs["Anisotropy"].default_value = 0.4
            nt.links.new(vs.outputs["Volume"], nt.nodes["Material Output"].inputs["Volume"])
            fog.data.materials.append(fm)

        # --- camera on a tracked target
        tgt = _add(bpy.data.objects.new("Texel Focus", None))
        tgt.location = centre
        cam_d = bpy.data.cameras.new("Texel Camera")
        cam_d.lens = 42
        cam_d.dof.use_dof = True
        cam_d.dof.aperture_fstop = 3.2
        cam_d.dof.focus_object = tgt
        cam = _add(bpy.data.objects.new("Texel Camera", cam_d))
        con = cam.constraints.new("TRACK_TO")
        con.target = tgt
        con.track_axis, con.up_axis = "TRACK_NEGATIVE_Z", "UP_Y"
        context.scene.camera = cam
        _place(cam, centre, radius, s.showcase_move, 0.0)

        sc = context.scene
        sc.render.engine = "CYCLES"
        try:
            sc.cycles.device = "GPU"
            prefs = context.preferences.addons["cycles"].preferences
            prefs.compute_device_type = "OPTIX"
            prefs.get_devices()
            for d in prefs.devices:
                d.use = True
        except Exception:
            pass                              # CPU is a fine fallback, just slower
        sc.cycles.samples = s.showcase_samples
        sc.cycles.use_denoising = True
        sc.cycles.volume_step_rate = 4.0
        sc.render.resolution_x = s.showcase_width
        sc.render.resolution_y = s.showcase_height
        try:
            sc.view_settings.look = "AgX - Base Contrast"
        except Exception:
            pass

        s.status = (f"{p['label']} rig built - {fixed} textures set to nearest-neighbour")
        self.report({"INFO"}, s.status)
        return {"FINISHED"}


def _place(cam, centre, radius, move, t):
    """Camera position for a normalised time t in 0..1."""
    e = t * t * (3 - 2 * t)                    # smoothstep, no jerky start/stop
    cx, cy, cz = centre
    if move == "ORBIT":
        a = math.radians(-120 + 300 * t)
        r = radius * 3.4
        cam.location = (cx + math.cos(a) * r, cy + math.sin(a) * r, cz + radius * 1.5)
    elif move == "PUSH":
        cam.location = (cx, cy - radius * (5.0 - 2.2 * e), cz + radius * (1.5 - 0.4 * e))
    elif move == "ARC":
        a = math.radians(-118 + 62 * e)
        r = radius * (4.4 - 1.3 * e)
        cam.location = (cx + math.cos(a) * r, cy + math.sin(a) * r, cz + radius * (1.9 - 0.6 * e))
    else:                                       # STILL
        a = math.radians(-58)
        r = radius * 3.6
        cam.location = (cx + math.cos(a) * r, cy + math.sin(a) * r, cz + radius * 1.5)


class TEXEL_OT_showcase_clear(Operator):
    bl_idname = "texel.showcase_clear"
    bl_label = "Clear Showcase"
    bl_description = "Remove the showcase camera, lights and haze. Your art is untouched"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        col = bpy.data.collections.get(COLLECTION)
        if col is None:
            return {"FINISHED"}
        for o in list(col.objects):
            bpy.data.objects.remove(o, do_unlink=True)
        bpy.data.collections.remove(col)
        return {"FINISHED"}


class TEXEL_OT_showcase_render(Operator):
    bl_idname = "texel.showcase_render"
    bl_label = "Render Showcase"
    bl_description = ("Render a still, or an image sequence for the chosen move. "
                      "Encodes to MP4 when ffmpeg is on PATH, otherwise leaves PNGs")
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return bpy.data.collections.get(COLLECTION) is not None

    def execute(self, context):
        s = context.scene.texel
        cam = bpy.data.objects.get("Texel Camera")
        tgt = bpy.data.objects.get("Texel Focus")
        if cam is None or tgt is None:
            self.report({"WARNING"}, "Build the showcase first")
            return {"CANCELLED"}
        b = subject_bounds(context)
        if b is None:
            self.report({"WARNING"}, "Nothing to show")
            return {"CANCELLED"}
        centre, radius, _lo, _hi = b

        out = bpy.path.abspath(s.showcase_output or "//texel_showcase/")
        os.makedirs(out, exist_ok=True)
        sc = context.scene
        n = 1 if s.showcase_move == "STILL" else max(2, s.showcase_frames)

        for i in range(n):
            _place(cam, centre, radius, s.showcase_move, i / max(1, n - 1))
            sc.render.filepath = os.path.join(out, f"showcase_{i:04d}")
            bpy.ops.render.render(write_still=True)

        if n == 1:
            s.status = f"Still rendered to {out}"
            self.report({"INFO"}, s.status)
            return {"FINISHED"}

        ff = shutil.which("ffmpeg")
        if ff is None:
            s.status = f"{n} frames in {out} - install ffmpeg to get an MP4"
            self.report({"INFO"}, s.status)
            return {"FINISHED"}
        mp4 = os.path.join(out, "showcase.mp4")
        r = subprocess.run([ff, "-y", "-loglevel", "error", "-framerate", "24",
                            "-i", os.path.join(out, "showcase_%04d.png"),
                            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", mp4],
                           capture_output=True, text=True)
        if r.returncode != 0:
            s.status = f"{n} frames rendered; ffmpeg failed: {r.stderr.strip()[:80]}"
            self.report({"WARNING"}, s.status)
            return {"FINISHED"}
        s.status = f"{n} frames -> {os.path.basename(mp4)}"
        self.report({"INFO"}, s.status)
        return {"FINISHED"}


CLASSES = (TEXEL_OT_showcase_setup, TEXEL_OT_showcase_clear, TEXEL_OT_showcase_render)


def register():
    for c in CLASSES:
        bpy.utils.register_class(c)


def unregister():
    for c in reversed(CLASSES):
        bpy.utils.unregister_class(c)
