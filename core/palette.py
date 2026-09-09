"""Palette parsing. No bpy, no network - callers supply the bytes.

Formats a pixel artist actually has on disk:
  .gpl  GIMP palette, which Aseprite/Krita/GIMP all read and write
  .hex  one RRGGBB per line, what Lospec's "hex" download gives you
  .txt  Paint.NET / JASC style, tolerated as a hex variant
Lospec's JSON is parsed too, since its API returns a colors[] of bare hex.
"""
from __future__ import annotations

import json

RGBA = tuple[int, int, int, int]


def _hex_to_rgba(h: str) -> RGBA | None:
    h = h.strip().lstrip("#").strip()
    if len(h) == 8:                      # AARRGGBB (Paint.NET) or RRGGBBAA
        try:
            a, r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4, 6))
        except ValueError:
            return None
        return (r, g, b, a)
    if len(h) == 6:
        try:
            r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
        except ValueError:
            return None
        return (r, g, b, 255)
    if len(h) == 3:                      # #abc shorthand
        try:
            r, g, b = (int(c * 2, 16) for c in h)
        except ValueError:
            return None
        return (r, g, b, 255)
    return None


def parse_gpl(text: str) -> tuple[str, list[RGBA]]:
    """GIMP palette. Header line 'GIMP Palette', optional 'Name: ...', then rows."""
    name = "Palette"
    cols: list[RGBA] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.lower().startswith("name:"):
            name = line.split(":", 1)[1].strip() or name
            continue
        if line.lower().startswith(("gimp palette", "columns:")):
            continue
        parts = line.split()
        if len(parts) >= 3:
            try:
                r, g, b = (int(p) for p in parts[:3])
            except ValueError:
                continue
            if all(0 <= v <= 255 for v in (r, g, b)):
                cols.append((r, g, b, 255))
    return name, cols


def parse_hex(text: str) -> list[RGBA]:
    out: list[RGBA] = []
    for line in text.splitlines():
        for token in line.replace(",", " ").split():
            c = _hex_to_rgba(token)
            if c:
                out.append(c)
    return out


def parse_lospec_json(text: str) -> tuple[str, list[RGBA]]:
    """Lospec palette JSON: {name, author, colors: ["ff0000", ...]}."""
    data = json.loads(text)
    name = data.get("name") or "Lospec Palette"
    cols = [c for c in (_hex_to_rgba(h) for h in data.get("colors", [])) if c]
    return name, cols


def parse(text: str, filename: str = "") -> tuple[str, list[RGBA]]:
    """Sniff the format. Extension is a hint, content decides."""
    stripped = text.lstrip()
    if stripped.startswith("{"):
        return parse_lospec_json(text)
    if stripped.lower().startswith("gimp palette") or filename.lower().endswith(".gpl"):
        return parse_gpl(text)
    cols = parse_hex(text)
    base = filename.rsplit("/", 1)[-1].rsplit("\\", 1)[-1]
    return (base.rsplit(".", 1)[0] or "Palette", cols)


def to_gpl(name: str, colours: list[RGBA]) -> str:
    """Write GIMP format, so the palette opens in Aseprite, Krita and GIMP."""
    lines = ["GIMP Palette", f"Name: {name}", "Columns: 0",
             "# Written by Texel (Mintworks)"]
    for r, g, b, _a in colours:
        lines.append(f"{r:3d} {g:3d} {b:3d}\t#{r:02x}{g:02x}{b:02x}")
    return "\n".join(lines) + "\n"


def dedupe(colours: list[RGBA]) -> list[RGBA]:
    """Order-preserving dedupe. Palettes in the wild repeat colours constantly."""
    seen: set[RGBA] = set()
    out: list[RGBA] = []
    for c in colours:
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out


def from_image_pixels(pixels: list[float], w: int, h: int, limit: int = 256) -> list[RGBA]:
    """Extract the distinct colours from a bpy-style bottom-up RGBA float buffer.

    Ordered by frequency, so the dominant colours survive when a palette image
    has stray anti-aliased edge pixels.
    """
    counts: dict[RGBA, int] = {}
    for i in range(0, min(len(pixels), w * h * 4), 4):
        a = round(pixels[i + 3] * 255)
        if a == 0:
            continue
        c = (round(pixels[i] * 255), round(pixels[i + 1] * 255),
             round(pixels[i + 2] * 255), a)
        counts[c] = counts.get(c, 0) + 1
    ranked = sorted(counts.items(), key=lambda kv: -kv[1])
    return [c for c, _n in ranked[:limit]]
