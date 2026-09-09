"""Mouse -> texel, for both editors. The only module that knows about regions."""
from __future__ import annotations
import bpy
from .core import uvmap

try:
    from bpy_extras import view3d_utils
except ImportError:            # not available in some background contexts
    view3d_utils = None


def image_editor_uv(context, event) -> tuple[float, float] | None:
    region = context.region
    if region is None or context.space_data is None:
        return None
    v2d = region.view2d
    x = event.mouse_x - region.x
    y = event.mouse_y - region.y
    return v2d.region_to_view(x, y)


def viewport_hit(context, event):
    """Raycast the scene. Returns (object, face_index, location) or None."""
    if view3d_utils is None:
        return None
    region, rv3d = context.region, context.region_data
    if region is None or rv3d is None:
        return None
    coord = (event.mouse_x - region.x, event.mouse_y - region.y)
    direction = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
    origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)
    dg = context.evaluated_depsgraph_get()
    hit, loc, _n, face_index, obj, _m = context.scene.ray_cast(dg, origin, direction)
    if not hit or obj is None or obj.type != "MESH":
        return None
    return (obj, face_index, loc)


def uv_at_hit(obj, face_index: int, world_loc) -> tuple[float, float] | None:
    """Barycentric UV at a raycast hit. Triangulates the polygon fan."""
    me = obj.data
    if not me.uv_layers.active or face_index < 0 or face_index >= len(me.polygons):
        return None
    poly = me.polygons[face_index]
    uvs = me.uv_layers.active.data
    inv = obj.matrix_world.inverted()
    p = inv @ world_loc
    loops = list(poly.loop_indices)
    verts = [me.vertices[me.loops[li].vertex_index].co for li in loops]
    # fan-triangulate; take the triangle whose barycentric weights are all >= 0
    for i in range(1, len(loops) - 1):
        tri = (0, i, i + 1)
        a, b, c = (verts[t] for t in tri)
        bary = uvmap.barycentric(p, a, b, c)
        if all(wgt >= -1e-4 for wgt in bary):
            uva, uvb, uvc = (uvs[loops[t]].uv for t in tri)
            return uvmap.interp_uv(bary, uva, uvb, uvc)
    return None


def texel_under_mouse(context, event, w: int, h: int):
    """(x, y) texel under the cursor, or None. Works in both editors."""
    space = context.space_data
    if space is None:
        return None
    if space.type == "IMAGE_EDITOR":
        uv = image_editor_uv(context, event)
        if uv is None:
            return None
        u, v = uv
        if not (0.0 <= u < 1.0 and 0.0 <= v < 1.0):
            return None
        return uvmap.uv_to_texel(u, v, w, h)
    if space.type == "VIEW_3D":
        hit = viewport_hit(context, event)
        if hit is None:
            return None
        obj, fi, loc = hit
        uv = uv_at_hit(obj, fi, loc)
        if uv is None:
            return None
        u, v = uv
        return uvmap.uv_to_texel(u % 1.0, v % 1.0, w, h)
    return None
