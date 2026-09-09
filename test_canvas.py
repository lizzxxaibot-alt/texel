"""Headless test for the canvas/layer core.  py -3 test_canvas.py"""
import sys
from core.canvas import Canvas, Layer, TRANSPARENT

fails = []
def check(name, cond, detail=""):
    if cond: print(f"[ok]   {name}")
    else:    print(f"[FAIL] {name}  {detail}"); fails.append(name)

RED   = (255, 0, 0, 255)
BLUE  = (0, 0, 255, 255)

c = Canvas(8, 6)
check("starts with one layer", len(c.layers) == 1)
check("index 0 is transparent", c.palette[0] == (0,0,0,0))
try:
    Canvas(0, 5); check("rejects zero size", False)
except ValueError: check("rejects zero size", True)

# --- palette
r = c.add_colour(RED)
check("add_colour returns index >=1", r == 1, r)
check("add_colour dedupes", c.add_colour(RED) == r)
b = c.add_colour(BLUE)
check("second colour gets its own index", b == 2 and b != r)

# --- painting + bounds
L = c.layers[0]
L.set(2, 3, r); L.set(5, 1, b)
check("get returns what set wrote", L.get(2,3) == r and L.get(5,1) == b)
check("out-of-bounds get is transparent", L.get(-1,0) == TRANSPARENT and L.get(99,0) == TRANSPARENT)
check("out-of-bounds set is rejected", L.set(99, 0, r) is False)
check("bounds is tight", L.bounds() == (2,1,5,3), L.bounds())
L.locked = True
check("locked layer refuses writes", L.set(0,0,r) is False and L.get(0,0) == TRANSPARENT)
L.locked = False
check("empty layer has no bounds", Layer("e", 4, 4).bounds() is None)

# --- palette swap is the indexed payoff
c.replace_colour(r, (1,2,3,255))
check("palette swap changes output without touching pixels",
      c.to_rgba()[(3*8+2)*4:(3*8+2)*4+4] == bytearray((1,2,3,255)))
check("pixel index is unchanged by the swap", L.get(2,3) == r)

# --- layers
c.add_layer("Top")
check("add_layer inserts and activates", len(c.layers) == 2 and c.active == 1)
c.layers[c.active].set(2, 3, b)     # directly over the red pixel
flat = c.flatten()
check("upper opaque pixel wins", flat[3*8+2] == b, flat[3*8+2])
c.layers[c.active].visible = False
check("hidden layer is skipped", c.flatten()[3*8+2] == r)
c.layers[c.active].visible = True

check("merge_down keeps upper where opaque", c.merge_down(1) and c.layers[0].get(2,3) == b)
check("merge_down leaves one layer", len(c.layers) == 1)
check("merge_down on bottom layer is refused", c.merge_down(0) is False)
check("cannot remove the last layer", c.remove_layer(0) is False)

c.add_layer("A"); c.add_layer("B")
names = [l.name for l in c.layers]
c.move_layer(0, 2)
check("move_layer reorders", [l.name for l in c.layers] == names[1:] + names[:1],
      [l.name for l in c.layers])
check("move_layer rejects bad index", c.move_layer(9, 0) is False)
check("remove_layer clamps active", c.remove_layer(len(c.layers)-1) and c.active < len(c.layers))

# --- Blender handoff: bpy.types.Image.pixels is BOTTOM-UP. Getting this
#     backwards flips every texture, which is the classic silent bug.
c2 = Canvas(2, 2)
top = c2.add_colour((255,255,255,255))
c2.layers[0].set(0, 0, top)          # top-left in image space
fl = c2.to_blender_floats()
check("to_blender_floats length = w*h*4", len(fl) == 2*2*4, len(fl))
check("top-left pixel lands in the LAST row for Blender", fl[8:12] == [1.0,1.0,1.0,1.0], fl)
check("blender floats are 0..1", all(0.0 <= v <= 1.0 for v in fl))

# --- scale: a 512x512 layer is 256 KB indexed, not 1 MB float
big = Layer("big", 512, 512)
check("512x512 layer is 262144 bytes indexed", len(big.px) == 512*512, len(big.px))


# ---------------------------------------------- layer opacity, really blended
print()
c4 = Canvas(2, 2)
r4 = c4.add_colour((255, 0, 0, 255))
b4 = c4.add_colour((0, 0, 255, 255))
c4.layers[0].px = bytearray([b4] * 4)
t4 = c4.add_layer("Top")
t4.px = bytearray([r4] * 4)
check("opaque top wins", tuple(c4.to_rgba()[:4]) == (255, 0, 0, 255))
t4.opacity = 0.0
check("zero opacity reveals below", tuple(c4.to_rgba()[:4]) == (0, 0, 255, 255))
t4.opacity = 0.5
mid = tuple(c4.to_rgba()[:4])
check("half opacity blends", 100 < mid[0] < 160 and 100 < mid[2] < 160, mid)
check("blend stays opaque", mid[3] == 255, mid)
t4.opacity = 0.25
q = tuple(c4.to_rgba()[:4])
check("quarter opacity leans to the lower layer", q[2] > q[0], q)
t4.opacity = 0.5
t4.visible = False
check("hidden layer is skipped even with opacity",
      tuple(c4.to_rgba()[:4]) == (0, 0, 255, 255))
t4.visible = True
# a transparent texel on the blended path must not paint anything
t4.px[0] = 0
check("transparent texel falls through to the layer below",
      tuple(c4.to_rgba()[:4]) == (0, 0, 255, 255), tuple(c4.to_rgba()[:4]))
# nothing underneath: the blend composites against empty
c5 = Canvas(1, 1)
w5 = c5.add_colour((255, 255, 255, 255))
c5.layers[0].px = bytearray([w5])
c5.layers[0].opacity = 0.5
half5 = tuple(c5.to_rgba())
check("blending over nothing keeps the colour, halves the alpha",
      half5[0] == 255 and 120 < half5[3] < 136, half5)
c5.layers[0].opacity = 1.0

# ------------------------------------------------------ content bounds + crop
c6 = Canvas(16, 16)
g6 = c6.add_colour((0, 200, 0, 255))
for x in range(5, 10):
    for y in range(6, 12):
        c6.layers[0].set(x, y, g6)
check("content_bounds is tight", c6.content_bounds() == (5, 6, 9, 11), c6.content_bounds())
c6.add_layer("Empty")
check("content_bounds ignores an empty layer", c6.content_bounds() == (5, 6, 9, 11))
c6.layers[1].set(1, 2, g6)
check("content_bounds unions across layers", c6.content_bounds() == (1, 2, 9, 11),
      c6.content_bounds())
c6.layers[1].visible = False
check("content_bounds skips hidden layers", c6.content_bounds() == (5, 6, 9, 11))
c6.layers[1].visible = True
from core.select import Selection as _Sel
c6.selection = _Sel(16, 16, all_selected=True)
check("crop resizes every layer", c6.crop(1, 2, 9, 11) and (c6.w, c6.h) == (9, 10),
      (c6.w, c6.h))
check("crop resized the layers too", all(l.w == 9 and l.h == 10 for l in c6.layers))
check("crop dropped the now-invalid selection", c6.selection is None)
check("crop kept the art", c6.layers[0].get(4, 4) == g6)
check("crop refuses a no-op", c6.crop(0, 0, 8, 9) is False)
check("crop refuses an inverted box", c6.crop(5, 5, 5, 5) is not None)
check("crop clamps out-of-range coords", Canvas(8, 8).crop(-9, -9, 99, 99) is False)
check("content_bounds of an empty canvas is None", Canvas(4, 4).content_bounds() is None)

# the two guards inside the blended composite path
c7 = Canvas(1, 1)
solid = c7.add_colour((10, 20, 30, 255))
ghost = c7.add_colour((99, 99, 99, 0))      # a fully transparent PALETTE entry
c7.layers[0].px = bytearray([solid])
mid7 = c7.add_layer("Ghost")
mid7.px = bytearray([ghost])
top7 = c7.add_layer("Faded")
top7.px = bytearray([0])
top7.opacity = 0.5                          # forces the blended path
check("a zero-alpha palette entry paints nothing",
      tuple(c7.to_rgba()) == (10, 20, 30, 255), tuple(c7.to_rgba()))
hidden7 = c7.add_layer("Hidden")
hidden7.px = bytearray([solid])
hidden7.visible = False
check("hidden layer skipped on the blended path",
      tuple(c7.to_rgba()) == (10, 20, 30, 255))
hidden7.visible = True
hidden7.opacity = 0.0
check("zero-opacity layer skipped on the blended path",
      tuple(c7.to_rgba()) == (10, 20, 30, 255))


# ------------------------------------------------- cel model: tracks x frames
print()
c8 = Canvas(4, 4)
bg = c8.add_colour((10, 20, 30, 255))
ch = c8.add_colour((200, 30, 40, 255))
check("a fresh canvas has no frames", c8.frame_count() == 0)

f0 = c8.add_frame()
check("first frame is index 0", f0 == 0, f0)
check("adding a frame seeds a Main track", c8.tracks == ["Main"], c8.tracks)
check("frame_count is 1", c8.frame_count() == 1)

check("add_track makes a cel per frame", c8.add_track("BG") == 1)
check("two tracks now", c8.tracks == ["Main", "BG"], c8.tracks)
check("adding the same track twice is refused", c8.add_track("BG") == 0)

# THE POINT: one frame, two tracks, different content
c8.cel("Main", 0).px = bytearray([ch] * 16)
c8.cel("BG", 0).px = bytearray([bg] * 16)
cels = c8.cels_at(0)
check("frame 0 holds both tracks", len(cels) == 2, len(cels))
flat = c8.flatten_frame(0)
check("both tracks composite into one frame", all(v for v in flat))

f1 = c8.add_frame(copy_current=0)
check("second frame is index 1", f1 == 1)
check("copying a frame copies every track",
      c8.cel("Main", 1) is not None and c8.cel("BG", 1) is not None)
check("the copy has the pixels", any(c8.cel("Main", 1).px))
check("the copy is independent",
      c8.cel("Main", 1).px is not c8.cel("Main", 0).px)
f2 = c8.add_frame(copy_current=None)
check("an empty frame has empty cels", not any(c8.cel("Main", 2).px))
check("frame_count follows", c8.frame_count() == 3, c8.frame_count())

# --- static layers appear on every frame
stat = c8.add_layer("Backdrop")
stat.frame = None
stat.track = None
for f in range(3):
    check(f"a static layer shows on frame {f}", stat in c8.cels_at(f))

# --- show_frame
c8.show_frame(1, onion=False)
vis = {(l.track, l.frame) for l in c8.layers if l.visible and l.frame is not None}
check("show_frame reveals exactly one frame's cels",
      vis == {("Main", 1), ("BG", 1)}, vis)
c8.show_frame(1, onion=True)
ghost = [l for l in c8.layers if l.visible and l.frame is not None and 0 < l.opacity < 1]
check("onion skin ghosts the neighbours", len(ghost) == 4, len(ghost))
check("with no track named, every track is ghosted",
      {l.track for l in ghost} == {"Main", "BG"}, {l.track for l in ghost})
# naming a track is the useful case: ghosting an opaque backdrop twice over
# just turns the canvas to soup
c8.show_frame(1, onion=True, track="Main")
ghost = [l for l in c8.layers if l.visible and l.frame is not None and 0 < l.opacity < 1]
check("onion skin can be limited to one track",
      {l.track for l in ghost} == {"Main"}, {l.track for l in ghost})
check("and it still ghosts both neighbours of that track",
      sorted(l.frame for l in ghost) == [0, 2], sorted(l.frame for l in ghost))
check("the other track shows only the current frame",
      {l.frame for l in c8.layers if l.visible and l.track == "BG"} == {1})
c8.show_frame(1, onion=False)
check("turning onion off hides them again",
      not any(l.visible and l.frame not in (None, 1) for l in c8.layers))

# --- removing a track takes its cels with it
n_before = len(c8.layers)
check("remove_track drops every cel", c8.remove_track("BG") == 3, n_before)
check("track list updated", c8.tracks == ["Main"], c8.tracks)
check("removing an unknown track is a no-op", c8.remove_track("Nope") == 0)
check("cel() returns None for a removed track", c8.cel("BG", 0) is None)

# a fully transparent cel must contribute nothing to the composite
c9 = Canvas(2, 2)
v9 = c9.add_colour((90, 90, 90, 255))
c9.add_frame()
c9.add_track("Ghost")
c9.cel("Main", 0).px = bytearray([v9] * 4)
c9.cel("Ghost", 0).px = bytearray([v9] * 4)
c9.cel("Ghost", 0).opacity = 0.0
flat9 = c9.flatten_frame(0)
check("a zero-opacity cel is skipped in flatten_frame", all(v == v9 for v in flat9),
      list(flat9))
c9.cel("Main", 0).opacity = 0.0
check("every cel at zero opacity leaves the frame empty",
      not any(c9.flatten_frame(0)))

# ------------------------------------- stack order: a background must go UNDER
# Cels are appended, so a track added after the character used to paint over it.
# This is the check that would have caught it.
c10 = Canvas(2, 2)
fg = c10.add_colour((255, 0, 0, 255))
bk = c10.add_colour((0, 0, 255, 255))
c10.add_frame()
c10.add_track("BG")
c10.cel("Main", 0).px = bytearray([fg] * 4)
c10.cel("BG", 0).px = bytearray([bk] * 4)
check("a track appended on top wins", set(c10.flatten_frame(0)) == {bk})
check("move_track sends it behind", c10.move_track("BG", -1))
check("track order updated", c10.tracks == ["BG", "Main"], c10.tracks)
check("now the character wins", set(c10.flatten_frame(0)) == {fg},
      set(c10.flatten_frame(0)))
check("the layer stack agrees with the track order",
      c10.layers.index(c10.cel("BG", 0)) < c10.layers.index(c10.cel("Main", 0)))
check("moving past the end is refused", c10.move_track("BG", -1) is False)
check("moving an unknown track is refused", c10.move_track("Nope", 1) is False)
check("move_track clamps rather than wrapping", c10.move_track("BG", 99) and
      c10.tracks == ["Main", "BG"], c10.tracks)

# added at the bottom in the first place - no move needed
c11 = Canvas(2, 2)
a11 = c11.add_colour((10, 200, 10, 255))
b11 = c11.add_colour((200, 10, 10, 255))
c11.add_frame()
check("add_track(bottom=True) goes under", c11.add_track("Sky", bottom=True) == 1)
check("bottom track is first", c11.tracks == ["Sky", "Main"], c11.tracks)
c11.cel("Main", 0).px = bytearray([a11] * 4)
c11.cel("Sky", 0).px = bytearray([b11] * 4)
check("the seeded track still draws on top", set(c11.flatten_frame(0)) == {a11})

# new frames keep the order, and the active layer survives the reshuffle
c11.active = c11.layers.index(c11.cel("Main", 0))
keep = c11.layers[c11.active]
c11.add_frame(copy_current=0)
check("add_frame preserves the active layer", c11.layers[c11.active] is keep)
check("frame 1 is ordered too",
      c11.layers.index(c11.cel("Sky", 1)) < c11.layers.index(c11.cel("Main", 1)))
check("cels stay grouped by frame",
      [l.frame for l in c11.layers] == [0, 0, 1, 1], [l.frame for l in c11.layers])

# a static layer keeps its slot at the bottom, whatever the tracks do
c12 = Canvas(2, 2)
c12.add_frame()
c12.add_track("Over")
c12.layers.insert(0, Layer("Reference", 2, 2))
c12.move_track("Over", -1)
check("a static layer stays at the bottom", c12.layers[0].name == "Reference")
check("sorting ignored the static layer", c12.layers[0].frame is None)

# a cel whose track is no longer listed must sort, not raise. Nothing in the
# add/remove paths can produce that today; the guard is what keeps a future one
# from crashing a UI redraw.
c13 = Canvas(2, 2)
c13.add_frame()
c13.add_track("Extra")
c13.tracks.remove("Extra")                      # inconsistent on purpose
c13._sort_cels()
check("an orphaned cel sorts to the top instead of raising",
      c13.layers[-1].track == "Extra", c13.layers[-1].track)

# adding a track to a canvas that has no frames yet makes exactly one cel,
# and sorting a single cel must be a no-op rather than a reshuffle
c14 = Canvas(2, 2)
check("add_track on a still canvas makes one cel", c14.add_track("Solo") == 1)
check("the cel belongs to that track", c14.layers[-1].track == "Solo")
check("the original layer is untouched", c14.layers[0].frame is None)

print()
if fails: print(f"{len(fails)} FAILED: {fails}"); sys.exit(1)
print("CANVAS CORE: ALL PASS")
