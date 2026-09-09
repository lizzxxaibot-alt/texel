"""Density zones: different texel densities on different parts of one mesh.

Why this exists: a character's face wants more pixels per unit than the soles of
its boots. One global density either wastes texture on the boots or starves the
face. A zone is a named group of faces with its own target density.

Zones live in a mesh face attribute ("texel_zone", INT), so they survive save,
reload and the .blend being sent to someone else. No sidecar file, no add-on
state to lose.
"""
import bmesh
import bpy
from bpy.props import EnumProperty, FloatProperty, IntProperty, StringProperty
from bpy.types import Operator

from .core import uvmap
from .tex_density import _active_mesh, _face_areas, _texture_size

ATTR = "texel_zone"
MAX_ZONES = 8


def _zone_layer(bm, create=True):
    lay = bm.faces.layers.int.get(ATTR)
    if lay is None and create:
        lay = bm.faces.layers.int.new(ATTR)
    return lay


class _ZoneOp(Operator):
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return _active_mesh(context) is not None

    def _open(self, context, need_uv=True):
        obj = _active_mesh(context)
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        lay = _zone_layer(bm)
        uvl = bm.loops.layers.uv.active
        if need_uv and uvl is None:
            bm.free()
            self.report({"WARNING"}, "Mesh has no UV map")
            return None
        return obj, bm, lay, uvl

    def _close(self, obj, bm):
        bm.to_mesh(obj.data)
        bm.free()
        obj.data.update()


class TEXEL_OT_zone_from_selection(_ZoneOp):
    bl_idname = "texel.zone_from_selection"
    bl_label = "Zone from Selection"
    bl_description = "Put the selected faces into a density zone"

    zone: IntProperty(name="Zone", default=1, min=1, max=MAX_ZONES)

    def execute(self, context):
        obj = _active_mesh(context)
        was_edit = obj.mode == "EDIT"
        if was_edit:
            bpy.ops.object.mode_set(mode="OBJECT")
        opened = self._open(context, need_uv=False)
        if opened is None:
            return {"CANCELLED"}
        _o, bm, lay, _uvl = opened
        n = 0
        for f in bm.faces:
            if f.select:
                f[lay] = self.zone
                n += 1
        self._close(obj, bm)
        if was_edit:
            bpy.ops.object.mode_set(mode="EDIT")
        if n == 0:
            self.report({"WARNING"}, "No faces selected - select some in Edit Mode first")
            return {"CANCELLED"}
        self.report({"INFO"}, f"{n} faces assigned to zone {self.zone}")
        return {"FINISHED"}


class TEXEL_OT_zone_select(_ZoneOp):
    bl_idname = "texel.zone_select"
    bl_label = "Select Zone Faces"
    bl_description = "Select every face in this zone"

    zone: IntProperty(name="Zone", default=1, min=0, max=MAX_ZONES)

    def execute(self, context):
        obj = _active_mesh(context)
        was_edit = obj.mode == "EDIT"
        if was_edit:
            bpy.ops.object.mode_set(mode="OBJECT")
        opened = self._open(context, need_uv=False)
        if opened is None:
            return {"CANCELLED"}
        _o, bm, lay, _uvl = opened
        n = 0
        for f in bm.faces:
            f.select = (f[lay] == self.zone)
            n += 1 if f.select else 0
        self._close(obj, bm)
        if was_edit:
            bpy.ops.object.mode_set(mode="EDIT")
        self.report({"INFO"}, f"{n} faces in zone {self.zone}")
        return {"FINISHED"}


class TEXEL_OT_detect_zones(_ZoneOp):
    bl_idname = "texel.detect_zones"
    bl_label = "Detect Density Zones"
    bl_description = ("Group faces by the density they already have. Reveals where a "
                      "mesh is inconsistent before you decide what to fix")

    buckets: IntProperty(name="Zones", default=3, min=2, max=MAX_ZONES)

    def execute(self, context):
        opened = self._open(context)
        if opened is None:
            return {"CANCELLED"}
        obj, bm, lay, uvl = opened
        size = _texture_size(obj)
        if not size:
            bm.free()
            self.report({"WARNING"}, "No image texture on this object")
            return {"CANCELLED"}
        rows = [(f, uvmap.texel_density(ua, wa, size))
                for f, ua, wa in _face_areas(obj, bm, uvl) if wa > 0 and ua > 0]
        if not rows:
            bm.free()
            self.report({"WARNING"}, "No usable faces")
            return {"CANCELLED"}
        vals = sorted(d for _f, d in rows)
        lo, hi = vals[0], vals[-1]
        if hi - lo < 1e-6:
            for f, _d in rows:
                f[lay] = 1
            self._close(obj, bm)
            context.scene.texel.status = f"Uniform at {lo:.1f} px/unit - one zone"
            self.report({"INFO"}, context.scene.texel.status)
            return {"FINISHED"}
        # equal-count buckets, so a few outliers cannot swallow a whole band
        per = max(1, len(vals) // self.buckets)
        edges = [vals[min(len(vals) - 1, (i + 1) * per)] for i in range(self.buckets - 1)]
        counts = [0] * (self.buckets + 1)
        for f, d in rows:
            z = 1
            for e in edges:
                if d > e:
                    z += 1
            z = min(z, self.buckets)
            f[lay] = z
            counts[z] += 1
        self._close(obj, bm)
        summary = ", ".join(f"z{i}:{counts[i]}" for i in range(1, self.buckets + 1) if counts[i])
        context.scene.texel.status = f"{lo:.1f}-{hi:.1f} px/unit -> {summary}"
        self.report({"INFO"}, context.scene.texel.status)
        return {"FINISHED"}


class TEXEL_OT_zone_apply(_ZoneOp):
    bl_idname = "texel.zone_apply"
    bl_label = "Apply Zone Density"
    bl_description = "Scale the UVs of one zone to its own target density"

    zone: IntProperty(name="Zone", default=1, min=1, max=MAX_ZONES)
    density: FloatProperty(name="Density", default=32.0, min=0.001, soft_max=512.0)

    def invoke(self, context, event):
        self.density = context.scene.texel.target_density
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        opened = self._open(context)
        if opened is None:
            return {"CANCELLED"}
        obj, bm, lay, uvl = opened
        size = _texture_size(obj)
        if not size:
            bm.free()
            self.report({"WARNING"}, "No image texture on this object")
            return {"CANCELLED"}
        n = 0
        for f, ua, wa in _face_areas(obj, bm, uvl):
            if f[lay] != self.zone or wa <= 0 or ua <= 0:
                continue
            want = uvmap.uv_scale_for_density(self.density, wa, size)
            have = ua ** 0.5
            if have <= 0:
                continue
            k = want / have
            cx = sum(l[uvl].uv[0] for l in f.loops) / len(f.loops)
            cy = sum(l[uvl].uv[1] for l in f.loops) / len(f.loops)
            for l in f.loops:
                u, v = l[uvl].uv
                l[uvl].uv = (cx + (u - cx) * k, cy + (v - cy) * k)
            n += 1
        self._close(obj, bm)
        if n == 0:
            self.report({"WARNING"}, f"Zone {self.zone} has no faces")
            return {"CANCELLED"}
        context.scene.texel.status = f"Zone {self.zone}: {n} faces at {self.density:.1f} px/unit"
        self.report({"INFO"}, context.scene.texel.status)
        return {"FINISHED"}


class TEXEL_OT_zone_info(_ZoneOp):
    bl_idname = "texel.zone_info"
    bl_label = "Density Summary"
    bl_description = "Report face count and measured density per zone"

    def execute(self, context):
        opened = self._open(context)
        if opened is None:
            return {"CANCELLED"}
        obj, bm, lay, uvl = opened
        size = _texture_size(obj) or 1
        per: dict[int, list[float]] = {}
        for f, ua, wa in _face_areas(obj, bm, uvl):
            if wa <= 0 or ua <= 0:
                continue
            per.setdefault(f[lay], []).append(uvmap.texel_density(ua, wa, size))
        bm.free()
        if not per:
            self.report({"WARNING"}, "No usable faces")
            return {"CANCELLED"}
        parts = []
        for z in sorted(per):
            v = per[z]
            name = "unzoned" if z == 0 else f"zone {z}"
            parts.append(f"{name}: {len(v)}f @ {sum(v) / len(v):.1f}")
        context.scene.texel.status = " | ".join(parts)
        self.report({"INFO"}, context.scene.texel.status)
        print("[Texel] " + context.scene.texel.status)
        return {"FINISHED"}


class TEXEL_OT_zone_grid(_ZoneOp):
    bl_idname = "texel.zone_grid"
    bl_label = "Grid from Zone"
    bl_description = "Lay this zone's faces out on the texel grid without overlapping"

    zone: IntProperty(name="Zone", default=1, min=1, max=MAX_ZONES)

    def execute(self, context):
        opened = self._open(context)
        if opened is None:
            return {"CANCELLED"}
        obj, bm, lay, uvl = opened
        size = _texture_size(obj) or 64
        faces = [f for f in bm.faces if f[lay] == self.zone]
        if not faces:
            bm.free()
            self.report({"WARNING"}, f"Zone {self.zone} has no faces")
            return {"CANCELLED"}
        cols = max(1, int(len(faces) ** 0.5 + 0.999))
        cell = 1.0 / cols
        snap = 1.0 / size
        for i, f in enumerate(faces):
            gx, gy = i % cols, i // cols
            us = [l[uvl].uv[0] for l in f.loops]
            vs = [l[uvl].uv[1] for l in f.loops]
            umin, umax = min(us), max(us)
            vmin, vmax = min(vs), max(vs)
            du, dv = (umax - umin) or 1e-6, (vmax - vmin) or 1e-6
            k = min(cell / du, cell / dv) * 0.92        # margin so cells cannot touch
            for l in f.loops:
                u, v = l[uvl].uv
                nu = gx * cell + (u - umin) * k
                nv = gy * cell + (v - vmin) * k
                l[uvl].uv = (round(nu / snap) * snap, round(nv / snap) * snap)
        self._close(obj, bm)
        context.scene.texel.status = f"Zone {self.zone}: {len(faces)} faces gridded {cols}x"
        self.report({"INFO"}, context.scene.texel.status)
        return {"FINISHED"}


class TEXEL_OT_zones_clear(_ZoneOp):
    bl_idname = "texel.zones_clear"
    bl_label = "Clear Zones"
    bl_description = "Remove every zone assignment from this mesh"

    def execute(self, context):
        obj = _active_mesh(context)
        opened = self._open(context, need_uv=False)
        if opened is None:
            return {"CANCELLED"}
        _o, bm, lay, _uvl = opened
        for f in bm.faces:
            f[lay] = 0
        self._close(obj, bm)
        context.scene.texel.status = "Zones cleared"
        self.report({"INFO"}, context.scene.texel.status)
        return {"FINISHED"}


CLASSES = (TEXEL_OT_zone_from_selection, TEXEL_OT_zone_select, TEXEL_OT_detect_zones,
           TEXEL_OT_zone_apply, TEXEL_OT_zone_info, TEXEL_OT_zone_grid,
           TEXEL_OT_zones_clear)


def register():
    for c in CLASSES:
        bpy.utils.register_class(c)


def unregister():
    for c in reversed(CLASSES):
        bpy.utils.unregister_class(c)
