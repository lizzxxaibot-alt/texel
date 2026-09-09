"""Canvas and layer stack: an indexed-colour pixel document.

Design decision that differs from the reference: we store an INDEXED canvas
(one byte per pixel into a palette) rather than RGBA floats per layer. Pixel art
is palette work - indexed makes palette swaps O(palette), colour-replace exact,
and a 1024x1024 layer 4 KB instead of 4 MB. RGBA is derived only at flush time.

Index 0 is always transparent.

STACK ORDER, stated once because getting it wrong corrupts every merge and
reorder: **layers[0] is the BOTTOM layer, layers[-1] is the TOP.** Compositing
walks the list forward so later layers overwrite earlier ones. `add_layer(above)`
inserts at active+1 and `merge_down(i)` folds i into i-1, both consistent with
that. A UI layer panel displays this list reversed - that is presentation only.
"""
from __future__ import annotations

TRANSPARENT = 0
MAX_COLOURS = 255          # 1..255 usable; 0 reserved for transparent


class Layer:
    """One layer, and - when animating - one CEL.

    A cel is a track's content at a single frame, which is the model Aseprite
    uses and the reason a frame can hold a character and a background at once.
      track  which named row it belongs to ("Body", "BG"). None for a plain layer.
      frame  which frame index it appears on. None means "every frame", which is
             what a static backdrop or a traced reference wants.
    """
    __slots__ = ("name", "w", "h", "px", "visible", "opacity", "locked", "group",
                 "track", "frame")

    def __init__(self, name: str, w: int, h: int, group: str | None = None,
                 track: str | None = None, frame: int | None = None):
        self.name = name
        self.w, self.h = w, h
        self.px = bytearray(w * h)      # all transparent
        self.visible = True
        self.opacity = 1.0
        self.locked = False
        self.group = group
        self.track = track
        self.frame = frame

    def get(self, x: int, y: int) -> int:
        if 0 <= x < self.w and 0 <= y < self.h:
            return self.px[y * self.w + x]
        return TRANSPARENT

    def set(self, x: int, y: int, idx: int) -> bool:
        if self.locked or not (0 <= x < self.w and 0 <= y < self.h):
            return False
        self.px[y * self.w + x] = idx
        return True

    def clear(self) -> None:
        self.px = bytearray(self.w * self.h)

    def copy(self, name: str | None = None) -> "Layer":
        l = Layer(name or f"{self.name} copy", self.w, self.h, self.group,
                  self.track, self.frame)
        l.px = bytearray(self.px)
        l.visible, l.opacity, l.locked = self.visible, self.opacity, self.locked
        return l

    def bounds(self) -> tuple[int, int, int, int] | None:
        """Tight bbox of non-transparent pixels, or None if empty."""
        minx = miny = 1 << 30
        maxx = maxy = -1
        for y in range(self.h):
            row = self.px[y * self.w:(y + 1) * self.w]
            if not any(row):
                continue
            miny = min(miny, y); maxy = max(maxy, y)
            for x, v in enumerate(row):
                if v:
                    if x < minx: minx = x
                    if x > maxx: maxx = x
        return None if maxx < 0 else (minx, miny, maxx, maxy)


class Canvas:
    def __init__(self, w: int, h: int):
        if w <= 0 or h <= 0:
            raise ValueError("canvas must be at least 1x1")
        self.w, self.h = w, h
        self.palette: list[tuple[int, int, int, int]] = [(0, 0, 0, 0)]  # idx 0
        self.layers: list[Layer] = [Layer("Layer 1", w, h)]
        self.active = 0
        self.selection = None          # core.select.Selection, or None
        self.frame_holds: list[int] = []   # per-frame hold, in timeline frames
        self.tracks: list[str] = []        # named rows, bottom-up
        self.groups: dict[str, bool] = {}   # group name -> expanded/visible

    # ---- palette
    def add_colour(self, rgba: tuple[int, int, int, int]) -> int:
        """Return the index for this colour, adding it if new. Dedupes."""
        if rgba in self.palette:
            return self.palette.index(rgba)
        if len(self.palette) > MAX_COLOURS:
            raise ValueError(f"palette full ({MAX_COLOURS} colours)")
        self.palette.append(rgba)
        return len(self.palette) - 1

    def replace_colour(self, idx: int, rgba: tuple[int, int, int, int]) -> None:
        """Palette swap: every pixel using this index changes at once. O(1)."""
        if not (1 <= idx < len(self.palette)):
            raise IndexError(idx)
        self.palette[idx] = rgba

    # ---- layers
    def add_layer(self, name: str | None = None, above: bool = True) -> Layer:
        l = Layer(name or f"Layer {len(self.layers) + 1}", self.w, self.h)
        self.layers.insert(self.active + (1 if above else 0), l)
        if above:
            self.active += 1
        return l

    def remove_layer(self, i: int) -> bool:
        if len(self.layers) <= 1 or not (0 <= i < len(self.layers)):
            return False           # never leave a canvas with no layers
        self.layers.pop(i)
        self.active = min(self.active, len(self.layers) - 1)
        return True

    def move_layer(self, i: int, to: int) -> bool:
        if not (0 <= i < len(self.layers)) or not (0 <= to < len(self.layers)):
            return False
        self.layers.insert(to, self.layers.pop(i))
        return True

    def duplicate_layer(self, i: int) -> "Layer | None":
        if not (0 <= i < len(self.layers)):
            return None
        dup = self.layers[i].copy()
        self.layers.insert(i + 1, dup)
        self.active = i + 1
        return dup

    def group_layers(self, indices: list[int], name: str) -> bool:
        """Tag layers into a named group. Groups are a UI/visibility construct;
        the stack order is untouched, so compositing is unaffected."""
        idx = [i for i in indices if 0 <= i < len(self.layers)]
        if not idx:
            return False
        for i in idx:
            self.layers[i].group = name
        self.groups[name] = True
        return True

    def ungroup(self, name: str) -> int:
        n = 0
        for layer in self.layers:
            if layer.group == name:
                layer.group = None
                n += 1
        self.groups.pop(name, None)
        return n

    def group_members(self, name: str) -> list[int]:
        return [i for i, l in enumerate(self.layers) if l.group == name]

    def set_group_visible(self, name: str, visible: bool) -> int:
        n = 0
        for layer in self.layers:
            if layer.group == name:
                layer.visible = visible
                n += 1
        self.groups[name] = visible
        return n

    def merge_indices(self, indices: list[int]) -> bool:
        """Merge several layers into the lowest of them, preserving stack order."""
        idx = sorted(i for i in set(indices) if 0 <= i < len(self.layers))
        if len(idx) < 2:
            return False
        target = self.layers[idx[0]]
        if target.locked:
            return False
        for i in idx[1:]:                       # lower index = lower in stack
            for n, v in enumerate(self.layers[i].px):
                if v:
                    target.px[n] = v
        for i in reversed(idx[1:]):
            self.layers.pop(i)
        self.active = min(idx[0], len(self.layers) - 1)
        return True

    def merge_down(self, i: int) -> bool:
        """Merge layer i into i-1. Upper wins where it is opaque."""
        if not (1 <= i < len(self.layers)):
            return False
        upper, lower = self.layers[i], self.layers[i - 1]
        if lower.locked:
            return False
        for n, v in enumerate(upper.px):
            if v:
                lower.px[n] = v
        self.layers.pop(i)
        self.active = min(self.active, len(self.layers) - 1)
        return True

    # ---- composite
    def flatten(self) -> bytearray:
        """Composite bottom-up into one index buffer; higher opaque pixels win."""
        out = bytearray(self.w * self.h)
        for l in self.layers:                  # layers[0] is the BOTTOM
            if not l.visible or l.opacity <= 0:
                continue
            for n, v in enumerate(l.px):
                if v:
                    out[n] = v
        return out

    # ------------------------------------------------------------ animation
    def frame_count(self) -> int:
        """How many frames exist. Zero means this is a still image."""
        idx = [l.frame for l in self.layers if l.frame is not None]
        return (max(idx) + 1) if idx else 0

    def cels_at(self, frame: int) -> list["Layer"]:
        """Every layer drawn at this frame, bottom first.

        Layers with frame=None are static and appear on every frame, so a
        backdrop or a reference does not need copying into each cel.
        """
        return [l for l in self.layers if l.frame is None or l.frame == frame]

    def cel(self, track: str, frame: int) -> "Layer | None":
        for l in self.layers:
            if l.track == track and l.frame == frame:
                return l
        return None

    def _sort_cels(self) -> None:
        """Put the cels back in (frame, track) order, leaving static layers put.

        New cels are appended, so without this a background track added after a
        character would sit ON TOP of it and paint the character out. Sorting by
        the track's index in self.tracks makes the stack mean what the cel grid
        shows. Static layers keep their exact slots - a reference pinned to the
        bottom stays at the bottom whatever the tracks do.
        """
        slots = [i for i, l in enumerate(self.layers) if l.frame is not None]
        if len(slots) < 2:
            return
        order = self.tracks
        cels = sorted((self.layers[i] for i in slots),
                      key=lambda l: (l.frame, order.index(l.track)
                                     if l.track in order else len(order)))
        keep = self.layers[self.active] if self.layers else None
        for i, l in zip(slots, cels):
            self.layers[i] = l
        if keep is not None:
            self.active = self.layers.index(keep)

    def move_track(self, name: str, delta: int) -> bool:
        """Reorder a track. tracks[0] is the BOTTOM, so -1 sends it behind."""
        if name not in self.tracks:
            return False
        i = self.tracks.index(name)
        j = max(0, min(len(self.tracks) - 1, i + delta))
        if j == i:
            return False
        self.tracks.insert(j, self.tracks.pop(i))
        self._sort_cels()
        return True

    def add_track(self, name: str, bottom: bool = False) -> int:
        """Add a named row. Every existing frame gets an empty cel for it."""
        if name in self.tracks:
            return 0
        self.tracks.insert(0, name) if bottom else self.tracks.append(name)
        n = max(1, self.frame_count())
        made = 0
        for f in range(n):
            if self.cel(name, f) is None:
                self.layers.append(Layer(f"{name} F{f + 1}", self.w, self.h,
                                         track=name, frame=f))
                made += 1
        self._sort_cels()
        return made

    def remove_track(self, name: str) -> int:
        if name not in self.tracks:
            return 0
        self.tracks.remove(name)
        keep = [l for l in self.layers if l.track != name]
        n = len(self.layers) - len(keep)
        if keep:                              # never leave a canvas with no layers
            self.layers = keep
            self.active = min(self.active, len(self.layers) - 1)
        return n

    def add_frame(self, copy_current: int | None = None) -> int:
        """Append a frame: one new cel per track. Returns the new frame index."""
        if not self.tracks:
            # Seeding converts the existing plain layer INTO frame 0, so the
            # first add_frame() must return 0 rather than creating a second one.
            self.tracks.append("Main")
            for l in self.layers:
                if l.frame is None and l.track is None:
                    l.track, l.frame = "Main", 0
                    l.name = "Main F1"
                    return 0
        f = self.frame_count()
        for t in self.tracks:
            src = self.cel(t, copy_current) if copy_current is not None else None
            cel = src.copy(f"{t} F{f + 1}") if src else                 Layer(f"{t} F{f + 1}", self.w, self.h, track=t, frame=f)
            cel.track, cel.frame, cel.visible, cel.opacity = t, f, True, 1.0
            self.layers.append(cel)
        self._sort_cels()
        return f

    def show_frame(self, frame: int, onion: bool = False,
                   track: str | None = None) -> None:
        """Set visibility so exactly this frame is drawn, optional onion skin.

        `track` limits the ghosting to one row. That matters: ghosting every
        track stacks two more translucent copies of an opaque backdrop over the
        drawing and the canvas turns to soup. You want to see where the
        character was, not where the wall was.
        """
        for l in self.layers:
            if l.frame is None:
                continue                       # static layers keep their own state
            if l.frame == frame:
                l.visible, l.opacity = True, 1.0
            elif (onion and abs(l.frame - frame) == 1
                  and (track is None or l.track == track)):
                l.visible, l.opacity = True, 0.28
            else:
                l.visible = False

    def flatten_frame(self, frame: int) -> bytearray:
        """Composite one frame's cels, ignoring current visibility flags."""
        out = bytearray(self.w * self.h)
        for l in self.cels_at(frame):
            if l.opacity <= 0:
                continue
            for n, v in enumerate(l.px):
                if v:
                    out[n] = v
        return out

    def to_rgba(self, flat: bytearray | None = None) -> bytearray:
        """Indexed -> RGBA bytes, row 0 at the TOP (image convention).

        When every visible layer is fully opaque this is a straight lookup off
        the flattened buffer. When a layer carries opacity < 1 we cannot stay
        indexed - a half-transparent red over blue is a colour that exists in
        neither palette - so the stack is composited in RGBA instead. Paying
        that cost only when opacity is actually used keeps the common path fast.
        """
        pal = self.palette
        blended = [l for l in self.layers
                   if l.visible and 0.0 < l.opacity < 1.0]
        if not blended:
            flat = self.flatten() if flat is None else flat
            out = bytearray(len(flat) * 4)
            for n, idx in enumerate(flat):
                r, g, b, a = pal[idx] if idx < len(pal) else (0, 0, 0, 0)
                o = n * 4
                out[o] = r; out[o + 1] = g; out[o + 2] = b; out[o + 3] = a
            return out

        n_px = self.w * self.h
        out = bytearray(n_px * 4)
        for layer in self.layers:                  # layers[0] is the BOTTOM
            if not layer.visible or layer.opacity <= 0:
                continue
            k = max(0.0, min(1.0, layer.opacity))
            for n, idx in enumerate(layer.px):
                if not idx:
                    continue
                sr, sg, sb, sa = pal[idx] if idx < len(pal) else (0, 0, 0, 0)
                if sa == 0:
                    continue
                a = (sa / 255.0) * k               # source alpha after opacity
                o = n * 4
                da = out[o + 3] / 255.0
                # na cannot be zero here: `a` is positive because opacity > 0
                # and source alpha > 0 were both checked above.
                na = a + da * (1.0 - a)
                out[o] = round((sr * a + out[o] * da * (1.0 - a)) / na)
                out[o + 1] = round((sg * a + out[o + 1] * da * (1.0 - a)) / na)
                out[o + 2] = round((sb * a + out[o + 2] * da * (1.0 - a)) / na)
                out[o + 3] = round(na * 255)
        return out

    def content_bounds(self) -> tuple[int, int, int, int] | None:
        """Tight box around every opaque texel on every visible layer."""
        box = None
        for layer in self.layers:
            if not layer.visible:
                continue
            b = layer.bounds()
            if b is None:
                continue
            box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]),
                                         max(box[2], b[2]), max(box[3], b[3]))
        return box

    def crop(self, x0: int, y0: int, x1: int, y1: int) -> bool:
        """Crop every layer to the given box, in place."""
        x0, x1 = max(0, min(x0, x1)), min(self.w - 1, max(x0, x1))
        y0, y1 = max(0, min(y0, y1)), min(self.h - 1, max(y0, y1))
        nw, nh = x1 - x0 + 1, y1 - y0 + 1
        if nw <= 0 or nh <= 0 or (nw == self.w and nh == self.h):
            return False
        for layer in self.layers:
            px = bytearray(nw * nh)
            for y in range(nh):
                src = (y0 + y) * self.w + x0
                px[y * nw:(y + 1) * nw] = layer.px[src:src + nw]
            layer.px = px
            layer.w, layer.h = nw, nh
        self.w, self.h = nw, nh
        if self.selection is not None:
            self.selection = None            # a stale mask is worse than none
        return True

    def to_blender_floats(self) -> list[float]:
        """Flat RGBA 0..1 list for bpy Image.pixels, which is BOTTOM-UP."""
        rgba = self.to_rgba()
        w4 = self.w * 4
        rows = [rgba[y * w4:(y + 1) * w4] for y in range(self.h)]
        rows.reverse()                          # flip to Blender's origin
        return [b / 255.0 for row in rows for b in row]
