"""Texel density: measure it, hit a target, snap UVs to the pixel grid.

This is what makes pixel art on 3D models actually work, and what a general
paint add-on does not have. Density is pixels-per-world-unit; when it varies
across a mesh, the same texture reads crisp on one face and mushy on the next.
"""
import bmesh
import bpy
from bpy.types import Operator

from .core import uvmap


def _active_mesh(context):
    obj = context.active_object
    return obj if obj and obj.type == "MESH" else None


def _texture_size(obj) -> int:
    """Longest edge of the first image texture on the object, or 0."""
    for slot in obj.material_slots:
        mat = slot.material
        if mat and mat.use_nodes:
            for n in mat.node_tree.nodes:
                if n.type == "TEX_IMAGE" and n.image:
                    return max(n.image.size)
    return 0


def _face_areas(obj, bm, uv_layer):
    """Yield (face, uv_area, world_area) for every face.

    World area is taken from the evaluated matrix so a scaled object reports the
    density a viewer actually sees, not the density in local space.
    """
    scale = obj.matrix_world.to_scale()
    k = (abs(scale.x) + abs(scale.y) + abs(scale.z)) / 3.0
    out = []
    for f in bm.faces:
        uvs = [loop[uv_layer].uv for loop in f.loops]
        area = 0.0
        for i in range(1, len(uvs) - 1):
            x1, y1 = uvs[i][0] - uvs[0][0], uvs[i][1] - uvs[0][1]
            x2, y2 = uvs[i + 1][0] - uvs[0][0], uvs[i + 1][1] - uvs[0][1]
            area += abs(x1 * y2 - x2 * y1) * 0.5
        out.append((f, area, f.calc_area() * k * k))
    return out


class _MeshOp(Operator):
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return _active_mesh(context) is not None

    def _open(self, context):
        """Return (obj, bm, uv_layer, size) or None, reporting why on failure."""
        obj = _active_mesh(context)
        size = _texture_size(obj)
        if not size:
            self.report({"WARNING"}, "No image texture on this object")
            return None
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        uvl = bm.loops.layers.uv.active
        if uvl is None:
            bm.free()
            self.report({"WARNING"}, "Mesh has no UV map")
            return None
        return obj, bm, uvl, size


class TEXEL_OT_density_detect(_MeshOp):
    bl_idname = "texel.density_detect"
    bl_label = "Detect Density"
    bl_description = "Measure pixels-per-unit across the mesh"

    def execute(self, context):
        opened = self._open(context)
        if opened is None:
            return {"CANCELLED"}
        obj, bm, uvl, size = opened
        vals = [uvmap.texel_density(ua, wa, size)
                for _f, ua, wa in _face_areas(obj, bm, uvl) if wa > 0 and ua > 0]
        bm.free()
        if not vals:
            self.report({"WARNING"}, "No faces with both UV and world area")
            return {"CANCELLED"}
        lo, hi, avg = min(vals), max(vals), sum(vals) / len(vals)
        spread = hi / lo if lo > 0 else 0.0
        context.scene.texel.status = (
            f"{avg:.1f} px/unit avg  ({lo:.1f}-{hi:.1f}, {spread:.1f}x spread)")
        context.scene.texel.target_density = round(avg, 3)
        self.report({"INFO"}, context.scene.texel.status)
        return {"FINISHED"}


class TEXEL_OT_density_apply(_MeshOp):
    bl_idname = "texel.density_apply"
    bl_label = "Apply Density"
    bl_description = "Scale each face's UVs to hit the target density"

    def execute(self, context):
        opened = self._open(context)
        if opened is None:
            return {"CANCELLED"}
        obj, bm, uvl, size = opened
        target = context.scene.texel.target_density
        n = 0
        for f, ua, wa in _face_areas(obj, bm, uvl):
            if wa <= 0 or ua <= 0:
                continue
            want = uvmap.uv_scale_for_density(target, wa, size)
            have = ua ** 0.5
            if have <= 0:
                continue
            k = want / have
            cx = sum(loop[uvl].uv[0] for loop in f.loops) / len(f.loops)
            cy = sum(loop[uvl].uv[1] for loop in f.loops) / len(f.loops)
            for loop in f.loops:
                u, v = loop[uvl].uv
                loop[uvl].uv = (cx + (u - cx) * k, cy + (v - cy) * k)
            n += 1
        bm.to_mesh(obj.data)
        bm.free()
        obj.data.update()
        context.scene.texel.status = f"{n} faces set to {target:.1f} px/unit"
        self.report({"INFO"}, context.scene.texel.status)
        return {"FINISHED"}


class TEXEL_OT_snap_uvs(_MeshOp):
    bl_idname = "texel.snap_uvs"
    bl_label = "Snap UVs to Pixels"
    bl_description = "Move every UV onto the nearest texel corner"

    def execute(self, context):
        opened = self._open(context)
        if opened is None:
            return {"CANCELLED"}
        obj, bm, uvl, size = opened
        n = 0
        for f in bm.faces:
            for loop in f.loops:
                u, v = loop[uvl].uv
                loop[uvl].uv = uvmap.snap_uv_to_grid(u, v, size, size)
                n += 1
        bm.to_mesh(obj.data)
        bm.free()
        obj.data.update()
        context.scene.texel.status = f"{n} UVs snapped to the {size}px grid"
        self.report({"INFO"}, context.scene.texel.status)
        return {"FINISHED"}


CLASSES = (TEXEL_OT_density_detect, TEXEL_OT_density_apply, TEXEL_OT_snap_uvs)


def register():
    for c in CLASSES:
        bpy.utils.register_class(c)


def unregister():
    for c in reversed(CLASSES):
        bpy.utils.unregister_class(c)
