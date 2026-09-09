# TEXEL (working name) — where the build is up to

A **re-implementation** of the pixel-art-texture-painting category for Blender,
for the Pixelkiln line. Same method as `App_generation/obscura` (a
re-implementation of Pixel Pumper): the user owns the reference, we extracted a
behavioural spec from it, and we write our own code against that spec.

**Reference:** Pixel Art Studio v1.1.1–1.1.5 by Alfred Reinold Baudisch
(GPL-3.0-or-later). Owned by the user. **No implementation is copied** — see
`reference/api-surface.txt`, which is the API surface only (what it does),
extracted by AST walk. Our add-on will be GPL-3.0 because every Blender add-on
using `bpy` must be, exactly like AssetDrop.

## Run the tests

```
py -3 test_raster.py
py -3 test_canvas.py
"C:\Users\opule\tools\blender-4.5.9-windows-x64\blender.exe" --background --factory-startup --python test_blender.py
```

## Status: BUILT AND VERIFIED. Not uploaded.

**1,597 lines of our own code. Six test suites, all green.**

| Suite | Where | Covers |
|---|---|---|
| `test_raster.py` | plain python | line, pixel-perfect, rect, ellipse, flood fill, UV/texel maths |
| `test_canvas.py` | plain python | indexed canvas, layer stack, merge/move, Blender float export |
| `test_palette.py` | plain python | .gpl / .hex / Lospec JSON parsing, round trip, frequency ranking |
| `test_blender.py` | Blender 4.5.9 | the core drives a live bpy Image, orientation, palette swap, 512x512 in 80 ms |
| `test_addon.py` | Blender 4.5.9 | registers, all 15 operators, canvas ops, density maths against a real cube |
| `test_install.py` | Blender 4.5.9 | **the built zip installs and paints** - the only test that proves what a buyer does |

Run them all:
```
py -3 test_raster.py && py -3 test_canvas.py && py -3 test_palette.py
blender --background --factory-startup --python test_addon.py
blender --background --factory-startup --python test_install.py
```

### Density maths verified against ground truth
A 2 m cube on a 64 px texture measures **8.0 px/unit**; asking for 16.0 and
re-measuring returns **16.0**; snapping puts all 24 UVs on the texel grid.

## Shipping artefacts
- `dist/texel-0.1.0.zip` - 23.3 KB, 17 files, install-verified
- `store/cover_630x500.png` - house pipeline (HTML/CSS -> render.mjs, brand fonts), checked at 315 px browse size
- `shots/hero.png` - Cycles render, textured **through Texel's own core** - if the add-on could not paint, that image could not exist
- `README.md` (ships in the zip) · `LISTING.md` (store copy)

## The architectural bet
**Indexed canvas** - one byte per pixel into a palette, not RGBA per layer.
Palette swap is O(palette) and exact; a 512x512 layer is 256 KB not 1 MB.

## Why we beat the reference on structure
Their `ps_session.py` is **5,067 lines - 29% of the add-on - and changed in
every one of five releases**. They added a 606-line hot-reload harness to fight
Blender. Our largest module is 203 lines and `core/` has no `bpy` in it at all,
which is why three of six suites run without launching Blender.

## Bugs the tests caught (all would have shipped silently)
1. `pixel_perfect` is for freehand strokes, not `line()` output - our Bresenham
   steps diagonally and emits no L-corners.
2. **Layer stack order was inconsistent** - `flatten()` said index 0 was top,
   `add_layer`/`merge_down` said bottom. Would have corrupted every merge.
3. The raster test's summary ran before an appended block, so those failures
   could not fail the build.
4. Store cover clipped "CRISP IN THE VIEWPORT" at the frame edge.

## Advertising: five shots, one capability each
The first cut of the promo material had a logic hole worth writing down: a
character sprite was mapped onto a cube as if it were a tile. Nobody wraps a man
with a torch around a crate. The set was rebuilt so each shot looks like a genre
our buyers actually ship, and argues one capability:

| shot | genre | what it proves |
|---|---|---|
| `dungeon` | side-scroller corridor | ANIMATION - the walk cycle as a sprite moving through the tiles |
| `temple` | isometric ARPG chamber | SEAMLESS TILING - one tile across a whole room, seam score printed |
| `hangar` | sci-fi bay | PALETTE SWAP - one texture, three palettes, no repainting |
| `market` | top-down exterior | TEXEL DENSITY - huge ground and hand-sized props at one px/unit |
| `shrine` | symmetric facade | MIRROR SYMMETRY - drawn as one half |

Every texture in every shot is painted by Texel's operators inside
`gameshots.py`, and each tile's seam score is measured and printed at build
time rather than assumed.

## Bugs the promo work caught in the PRODUCT
Making the advertisement is the only reason these were found - all four were
real defects a buyer would have hit on day one.
1. **A track added after a character painted over it.** `add_track` appended
   cels, so a background landed on top of the thing it was meant to sit behind.
   Fixed with `_sort_cels()`, a `bottom=` option and a new `texel.track_move`
   operator with arrows in the cel grid.
2. **Onion skin ghosted every track.** Two translucent copies of an opaque
   backdrop over the drawing turned the canvas to soup. Now it ghosts only the
   track being edited - you want to see where the character was, not where the
   wall was.
3. **The Layers panel listed every cel.** Four tracks across eight frames is
   thirty-two rows, thirty-one of them about a moment you are not looking at.
   It now lists the current frame's cels plus static layers.
4. **The cel grid's frame numbers did not line up with its columns**, because
   the track rows carried two extra arrow buttons. Both rows now use identical
   splits.

## Mistakes made while shooting, recorded so they are not repeated
- **Area lights left visible to camera** render as flat white rectangles. The
  hangar shot was a blank wall until `visible_camera = False`.
- **A corridor with no end bulkhead** sends the camera at empty space. Second
  time this exact mistake has been made on this product.
- **A 64px tile at 26 px/unit spans 2.5 world units**, so every pattern read
  enormous next to a crate. Pixel-art games put a tile at roughly a metre;
  40-50 px/unit is the usable band here.
- **Blender's default cube unwrap lays side faces on their side**, so a 16x8
  brick renders as an 8x16 plank and a stone wall reads as fencing.
- **A palette swap that only touches the datablock renders as the original**,
  because the PNG was already written and Cycles reads the file. Re-save.
- **A lamp next to a sprite card blows the flame past 1.0** before the view
  transform sees it. Sprites are unlit billboards - emission plus a transparent
  BSDF - which is also how they work in the games this is sold into.

## The worst defect found so far, and it was found by writing the manual

Writing the buyer's getting-started guide meant naming the buttons. There was no
button. **56 of the 92 operators were registered but drawn in no panel** — a
buyer could only reach 39% of what they had paid for, and only through F3 search
if they knew the operator existed at all.

Registered but invisible: the entire Setup group (Add 1m Cube, Pixel Art Unwrap,
Texel Workspace, viewport setup, the pixel grid), the entire selection and
clipboard group, the entire Density Zones group, canvas flip/rotate/resize,
Check Tiling, Generate Ramp, palette sort/clear, layer duplicate/group, custom
brushes, dither fill, outline, file round-trip. All of it built, tested and
shipped; none of it findable.

**Fixed by adding five panels** — Select, Canvas and File in the Image Editor;
Setup and Density Zones in the 3D viewport — and folding the rest into the
panels that already existed. **92 of 92 operators now have a button.** A phantom
reference to a non-existent `texel.save_canvas` was found and removed in the
same pass.

### Why every existing suite missed it
All eleven of them registered operators and called them. **Not one drew a
panel.** Blender does not hand a `draw()` exception to Python — it catches it,
prints a traceback to stderr and renders an error box on screen — so a panel
referencing a property that does not exist leaves every test green.

`test_panels.py` is the twelfth suite. It runs a real GUI, opens both sidebars,
forces the Texel tab, and steps through nine UI states that change what gets
drawn (frames present, onion skin on, brush > 1, rect vs fill tool, a status
line to dismiss). The gate is the console:

    blender --factory-startup --python test_panels.py 2>&1 | grep -i traceback

An empty grep plus `TEXEL PANELS: ALL PASS`, and the screenshots in
`shots/panels/` looked at by eye.

## After-sale material, added 2026-09-09
- **`START-HERE.html`** ships inside the zip. Self-contained, no internet, system
  fonts — because the moment a buyer needs it is the moment the download finished
  and nothing has worked yet. Install, first five minutes, the seven things that
  actually trip people up, what is in the download, updates, how to get help.
- **`mintworks_site/texel/index.html`** is the canonical support hub: the same
  guide plus the full FAQ, the roadmap and the changelog, kept current so a buyer
  on v0.1 reading it in March gets March's answers. **Built, not deployed** — it
  goes live with the launch, not before.
- The listing FAQ answers the questions the reference product's own buyers ask
  (standalone? dependencies? Blender version? shortcuts? tablet? custom shaders?
  undo? do I still unwrap?) plus the ones this product raises (GPL, refunds, the
  255-colour ceiling, no tweening, no engine importers yet).

## Keyboard shortcuts, and a measurement that nearly went the wrong way

Shortcuts were planned for v0.2 and are now in v0.1: a paint tool that makes you
reach for a sidebar button reads as a prototype in the first thirty seconds, and
registering a keymap is a small job. They go into **Blender's own keymap editor**,
so every one is rebindable by the user without code from us.

**Which keys are safe was measured, not guessed — and the first measurement lied.**
Probing `keyconfigs.default` in `--background` reported every letter free. It was
not: background Blender populates ~12 keymap items instead of **3,017**, so the
check passed by knowing nothing. Re-run in a GUI it showed `B` is
`view3d.select_box`, `C` is `view3d.select_circle`, `W` is `wm.tool_set_by_id`,
and Object Mode also owns `I`, `M`, `K`, `X`.

So the Image Editor gets the full set (B E L U C F I M D, all verified free) and
**the 3D viewport gets exactly one binding, D**, keeping every Blender default
intact. Nothing is bound to a mouse button — LEFTMOUSE is select in both editors
and an add-on that takes it is a bug report we would deserve.

`test_keys.py` re-runs that measurement on whatever Blender is installed, so a
future version that claims one of our letters fails the build instead of quietly
stomping the user.

## Two corrections to our own documentation

1. **Undo was under-sold.** Every buyer-facing document said undo is "per
   operator, not per stroke". `texel.paint` is a *modal* operator with
   `bl_options = {"REGISTER", "UNDO"}` — one drag is one undo push, so **undo is
   already per stroke**. "Per-stroke undo" came off the roadmap; it was never
   missing. Under-claiming is as wrong as over-claiming and costs sales.
2. **The panel-coverage check is now a gate**, inside `test_panels.py`: every
   non-INTERNAL operator must have a button, and no panel may reference an
   operator that does not exist. It immediately caught `texel.mirror_toggle`,
   which is shortcut plumbing and is now correctly marked INTERNAL.

## Roadmap reordered: easiest first, hardest last
v0.2 Brush · v0.3 Tileset · v0.4 Handoff · v0.5 Lit · v1.0 Studio. Ordered by
build difficulty rather than demand, because a young tool has to prove it ships —
two releases that land beat one ambitious release that slips twice — and because
stalling at v0.3 still leaves buyers with three real releases instead of half a
dope sheet.

## The end-to-end suite, and the data loss it found

Fifteen suites now. The fifteenth, `test_e2e.py`, exists because of a number:
**fourteen suites were green with 100% coverage of `core/`, and 20 of the 94
operators had never been called by any of them.** The pure-Python half was
proved and the Blender half was assumed.

It walks the product in a real GUI — setup, paint, palettes, layers, selection,
density, zones, animation, export, showcase — then stresses it, and **fails if
any registered operator goes uninvoked**. A new operator with no test now breaks
the build the day it is written.

### What it found

1. **`canvas_resize` destroyed the animation.** It rebuilt every layer as
   `Layer(name, w, h, group)` and never passed `track` or `frame` — the two
   arguments the cel model lives in. Measured before the fix:
   `frames=3 tracks=['BG','Main'] cels=6` → `frames=0 tracks=[] cels=0`.
   Silent, no error, no sensible undo. A buyer resizes a sprite, does not look
   at the frame grid for ten minutes, and has lost the afternoon. It now carries
   `tracks`, `frame_holds` and per-layer `track`/`frame`, with a regression test.
   **`canvas_resize` was one of the 20 operators nothing had ever called** — it
   was written, shipped in the zip, and never once executed.
2. **Three pixel-grid buttons could never be pressed.** Added to the 3D Setup
   panel; all three poll for an Image Editor. Moved to the Canvas panel.
3. **`palette_lospec` fetched 32 colours and said nothing.** The sidebar status
   line is the only feedback left after the toast fades.

### Eight of the twelve first-run failures were the test's own fault
Worth recording, because taking them at face value would have meant "fixing"
correct code: `flip_canvas` is `H`/`V` not `X`/`Y`; `canvas_resize` takes one
square `size`; `replace_colour` takes an index and reads the colour from the
scene; `export_layers` makes Blender images rather than files; `merge_down`
takes an index; `flood_fill` takes a `get_px` callable; and **the palette
ceiling is 255 *usable* colours plus transparent — 256 entries, one byte,
exactly right.** That last one I nearly filed as a product bug. Same failure
mode as the ellipse metric that first reported "theirs wins 5-0".

Timings on a 1024×1024 canvas: fill 0.18s, `to_rgba` 0.16s, full-canvas flood
fill 0.60s over a million texels.

## Blocked on the user
1. **Price** - reference asks $29.90, AssetDrop asks $4.95. Recommend $14.95.
2. **AI disclosure** - the packs answer "Yes + Graphics" would be FALSE here;
   this product's substance is code. Recommend **Yes + Code + Graphics**.
3. **Name** - confirm `Texel` before the itch slug is claimed.

## Remaining before upload
- a 3-second GIF of a pixel-perfect stroke (the marquee feature, demos instantly)
- a still of the density readout mid-measurement
