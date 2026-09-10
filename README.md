# Texel — pixel art, painted on the model

A Blender add-on for painting pixel art directly onto 3D models, with the pixel
grid respected end to end.

**Two things go wrong when pixel art meets a mesh, and neither is your drawing.**
The pixel size drifts across the model — a crate at 32 px/unit beside a wall at
19 px/unit reads as two different games glued together. And shallow diagonals
come out as staircases, the L-shaped double-texels pixel artists spend their
lives cleaning up. Texel fixes both inside Blender, with no round trip to a 2D
editor, then animates the sprites too.

## Get it

**[z3er1n.itch.io/texel](https://z3er1n.itch.io/texel) — $9.95.** Every future
update is free to anyone who has ever bought it; the price rises at named
milestones ($14.95 at v0.4, $19.95 at v1.0), announced in advance.

Licensed **GPL-3.0**, and the source ships inside the zip — every Blender add-on
that uses `bpy` has to be GPL. Buying it pays for the work and the updates, not
for access to the code.

Built and tested on **Windows** against Blender 4.2.23, 4.5.9 and 5.2.1 plus the
Microsoft Store build. 95 operators, 100% coverage of `core/`, 16 test suites —
one of which invokes every operator in a live GUI and fails if any goes uncalled.
Nothing in it is Windows-specific beyond looking for ffmpeg, so it should run on
macOS and Linux, but that is untested and not claimed.

Built with AI assistance, including the code and some of the artwork.

## Install

1. Blender → Edit → Preferences → Add-ons → the ▾ menu → **Install from Disk…**
2. Pick `texel-x.y.z.zip`
3. Tick **Texel** in the list

Blender **4.2 or newer**. Nothing else to install — no numpy, no external
dependencies, no internet needed except for the optional Lospec palette fetch.

## Where it lives

Press **N** for the sidebar, then the **Texel** tab. It appears in both the
**Image Editor** and the **3D Viewport**.

## Painting

**New Canvas** makes a square image and opens it. Then pick a tool and hit
**Paint**:

| Tool | What it does |
|---|---|
| Pencil | Freehand, one texel per sample |
| Eraser | Freehand erase back to transparent |
| Line / Rect / Ellipse | Drag to place. Right-click or Esc cancels |
| Fill | Flood fill, with tolerance and a contiguous toggle |
| Pick | Sample a colour off the canvas |

**Pixel Perfect** (on by default) removes the L-shaped corner texels a freehand
drag leaves behind, so a shallow diagonal comes out as a clean 1px line instead
of a staircase with fat joints. **Mirror X / Y** paints symmetrically.

In the 3D viewport, strokes are raycast onto the mesh and resolved through its
UVs, so you paint where you point.

## Layers

Add, remove, reorder, toggle visibility, merge down. The canvas is **indexed** —
every pixel is an index into a palette — which is why a palette swap recolours
the whole image instantly and exactly, with no colour drift and no float
comparison. A 512×512 layer costs 256 KB, not 1 MB.

## Palettes

Load `.gpl` (GIMP/Aseprite/Krita), `.hex`, or plain hex lists. Save back out as
`.gpl` so your palette opens in Aseprite. **Palette from Image** lifts the
colours out of any image already open in Blender, ranked by frequency. **Lospec**
fetches a palette by its slug — `pico-8`, `endesga-32`, whatever is in the URL.

## Texel density — the part that matters on a model

Pixel art on 3D breaks when the pixel size drifts between faces: crisp here,
mushy there. So:

- **Detect Density** measures pixels-per-world-unit across the mesh and reports
  the average, the range, and the spread. A spread above ~1.5× is visible.
- **Apply Density** scales each face's UVs to hit your target, about the face's
  own centre.
- **Snap UVs to Pixels** moves every UV onto the nearest texel corner, which
  kills half-pixel seams.

## Known limits, stated plainly

- The canvas is **indexed to 255 colours plus transparent**. Opening an existing
  texture with more than that will fail rather than silently quantise it — a
  silent quantise is how a texture comes back subtly wrong.
- Animation borrows **Blender's timeline** rather than adding a second one, so
  playback, scrubbing and fps use controls you already know. What you do not get
  is a dope sheet or tweening — every frame is drawn by hand.
- Undo goes through Blender's own stack per operator, not per stroke.

## For 2D sprite work

Texel is not only a 3D texture tool:

- **Tracks × frames — the cel model.** A *track* is a named row that runs the
  length of the animation (Body, BG, FX). A *cel* is one track's drawing on one
  frame. So a single frame can hold a character and a background at once, and
  you edit each independently.
- **Track order.** Tracks stack like layers, bottom first. Add a track with
  *Behind* ticked to drop it under the character, or use the arrows in the cel
  grid to move one. A background added on top would otherwise paint over
  everything under it.
- **Onion skin** ghosts the neighbouring frames of the track you are editing at
  28%. Only that track: ghosting an opaque backdrop twice over turns the canvas
  to soup, and you want to see where the character was, not where the wall was.
- **Hiding a track is an export.** Draw the character and its scenery in one
  document, then hide the scenery tracks and save — the same file gives you the
  full frame and a sprite on transparent, with no second copy to keep in sync.
- A layer with no frame is **static** — it appears on every frame, which is what
  a fixed backdrop or a traced reference wants.
- **Export Sprite Sheet** lays every frame out on one image at your chosen
  column count, ready for an engine.
- **Bind to Timeline** drives the frames from Blender's own timeline, so play,
  scrub and fps all work with the controls you already know. Press space.
- **Frame timing**: hold a drawing for several timeline frames — 2 frames at
  12 fps is a sixth of a second.
- **Export GIF** writes an animated GIF at the scene fps, honouring holds,
  upscaled nearest-neighbour so texels stay square. Needs ffmpeg.
- **Export Sheet + JSON** writes the sheet plus a manifest of frame rects and
  durations in milliseconds, so an engine can play it without guessing.
- **Trim to Content** crops away empty space, with an optional margin.
- **Add Reference** loads an image as a faint locked layer underneath to trace
  over. It is reduced to the palette on the way in.
- **Count Colours** reports how many colours the art actually uses against a
  target, because pixel artists work to limits.
- **Brush shapes**: square, round and diamond. Square is right at 1px; round is
  what you want above about 3 texels; diamond suits isometric work.
- **Layer opacity** blends properly.

## Licence

GPL-3.0-or-later, as every add-on built on the Blender Python API must be. See
`LICENSE.txt`. **Artwork you make with Texel is yours** — the licence covers the
add-on only and places no restriction on your textures, commercial use included.

Built by Mintworks · https://mintworks.cc
