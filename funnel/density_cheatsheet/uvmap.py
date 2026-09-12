"""UV <-> texel mapping. Pure maths, no bpy, so it is testable outside Blender."""
from __future__ import annotations


def uv_to_texel(u: float, v: float, w: int, h: int) -> tuple[int, int]:
    """UV (0..1, v up) -> image pixel (x, y) with y=0 at the TOP row.

    floor(), not round(): a texel owns the half-open square [n, n+1). Rounding
    puts the boundary in the middle of a texel and makes strokes land one pixel
    off on exactly half the canvas - a classic and very hard-to-see bug.
    """
    x = int(u * w)
    y = int((1.0 - v) * h)
    return (min(max(x, 0), w - 1), min(max(y, 0), h - 1))


def texel_to_uv(x: int, y: int, w: int, h: int, centre: bool = True) -> tuple[float, float]:
    off = 0.5 if centre else 0.0
    return ((x + off) / w, 1.0 - (y + off) / h)


def barycentric(p, a, b, c):
    """Barycentric weights of p in triangle abc. 2D or 3D tuples/Vectors."""
    v0 = [b[i] - a[i] for i in range(len(a))]
    v1 = [c[i] - a[i] for i in range(len(a))]
    v2 = [p[i] - a[i] for i in range(len(a))]
    d00 = sum(x * x for x in v0)
    d01 = sum(x * y for x, y in zip(v0, v1))
    d11 = sum(x * x for x in v1)
    d20 = sum(x * y for x, y in zip(v2, v0))
    d21 = sum(x * y for x, y in zip(v2, v1))
    den = d00 * d11 - d01 * d01
    if abs(den) < 1e-12:                       # degenerate triangle
        return (1.0, 0.0, 0.0)
    v = (d11 * d20 - d01 * d21) / den
    w = (d00 * d21 - d01 * d20) / den
    return (1.0 - v - w, v, w)


def interp_uv(bary, uv_a, uv_b, uv_c) -> tuple[float, float]:
    x, y, z = bary
    return (uv_a[0] * x + uv_b[0] * y + uv_c[0] * z,
            uv_a[1] * x + uv_b[1] * y + uv_c[1] * z)


def texel_density(uv_area: float, world_area: float, tex_size: int) -> float:
    """Pixels per world unit for a face. The number the whole category is about.

    A face covering `uv_area` of UV space on a `tex_size` texture, occupying
    `world_area` square units, resolves at sqrt(uv_area * tex_size^2 / world_area).
    """
    if world_area <= 0 or uv_area <= 0:
        return 0.0
    return (uv_area * tex_size * tex_size / world_area) ** 0.5


def uv_scale_for_density(target_px_per_unit: float, world_area: float,
                         tex_size: int) -> float:
    """How much to scale a face's UVs to hit a target density."""
    if world_area <= 0 or tex_size <= 0 or target_px_per_unit <= 0:
        return 1.0
    return (target_px_per_unit ** 2 * world_area / (tex_size * tex_size)) ** 0.5


def snap_uv_to_grid(u: float, v: float, w: int, h: int) -> tuple[float, float]:
    """Snap a UV onto the nearest texel CORNER - what UV snapping should do."""
    return (round(u * w) / w, round(v * h) / h)
