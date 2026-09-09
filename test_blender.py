"""Spike: prove the core drives a REAL Blender image, correct way up.
  blender --background --factory-startup --python test_blender.py
"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from core.canvas import Canvas
from core import raster as R

fails = []
def check(name, cond, detail=""):
    if cond: print(f"[ok]   {name}")
    else:    print(f"[FAIL] {name}  {detail}"); fails.append(name)

print(f"[info] Blender {bpy.app.version_string}")

W = H = 64
c = Canvas(W, H)
red   = c.add_colour((255, 0, 0, 255))
blue  = c.add_colour((0, 0, 255, 255))

# paint: a marker at image top-left, a diagonal, a filled ellipse
c.layers[0].set(0, 0, red)
for x, y in R.pixel_perfect(R.line(4, 4, 40, 20)):
    c.layers[0].set(x, y, red)
c.add_layer("shapes")
for x, y in R.ellipse(44, 44, 12, 8, filled=True):
    c.layers[c.active].set(x, y, blue)

# ---- push into a real Blender image
img = bpy.data.images.new("texel_spike", W, H, alpha=True)
t0 = time.perf_counter()
img.pixels.foreach_set(c.to_blender_floats())
img.update()
dt = (time.perf_counter() - t0) * 1000
check("image created at requested size", tuple(img.size) == (W, H), tuple(img.size))
print(f"[info] foreach_set of {W}x{H} took {dt:.1f} ms")

# ---- read it back out of Blender and verify
buf = [0.0] * (W * H * 4)
img.pixels.foreach_get(buf)

def bl_px(x, y):
    """Sample by IMAGE coords (row 0 = top), converting to Blender's bottom-up."""
    o = ((H - 1 - y) * W + x) * 4
    return tuple(round(v * 255) for v in buf[o:o + 4])

check("top-left marker survived the round trip", bl_px(0, 0) == (255, 0, 0, 255), bl_px(0, 0))
check("orientation is NOT flipped (bottom-left is empty)", bl_px(0, H - 1) == (0, 0, 0, 0), bl_px(0, H - 1))
check("diagonal landed", bl_px(4, 4) == (255, 0, 0, 255), bl_px(4, 4))
check("upper layer ellipse composited", bl_px(44, 44) == (0, 0, 255, 255), bl_px(44, 44))
check("untouched pixel is transparent", bl_px(60, 2) == (0, 0, 0, 0), bl_px(60, 2))

# ---- palette swap must repaint the whole image with one operation
c.replace_colour(red, (0, 255, 0, 255))
img.pixels.foreach_set(c.to_blender_floats())
img.pixels.foreach_get(buf)
check("palette swap recoloured every red pixel", bl_px(4, 4) == (0, 255, 0, 255), bl_px(4, 4))
check("palette swap left blue alone", bl_px(44, 44) == (0, 0, 255, 255), bl_px(44, 44))

# ---- realistic canvas size, for the performance claim
big = Canvas(512, 512)
w = big.add_colour((255, 255, 255, 255))
for x, y in R.rect(10, 10, 500, 500, filled=True):
    big.layers[0].set(x, y, w)
img2 = bpy.data.images.new("texel_spike_512", 512, 512, alpha=True)
t0 = time.perf_counter()
img2.pixels.foreach_set(big.to_blender_floats())
img2.update()
dt = (time.perf_counter() - t0) * 1000
print(f"[info] 512x512 full flush took {dt:.0f} ms")
check("512x512 flush completes under 2s", dt < 2000, f"{dt:.0f} ms")

print()
if fails: print(f"{len(fails)} FAILED: {fails}"); sys.exit(1)
print("BLENDER SPIKE: ALL PASS")
