# Texel — itch.io listing copy

**Status: DRAFT, not uploaded. Needs the user's decisions marked ⚠ below.**

---

## Title
`Texel — Pixel Art Painting for Blender`

## Short description / tagline (itch limit ~120 chars)
`Pixel art painted straight onto your models in Blender - and animated. Texel density, seamless tiles, cel animation, sheet+JSON export.`

## Who it is for
Solo devs and small teams shipping **metroidvanias, roguelikes, isometric ARPGs,
top-down adventures and side-scrollers** with a pixel look on 3D geometry - the
people who already own Aseprite and keep hitting the wall where 2D art meets a
mesh. Also jam devs who need a tileset and a walk cycle in one evening.

## Classification
- **Kind of project:** Tool
- **Release status:** Released
- **Pricing:** ⚠ **DECISION NEEDED** — see Pricing below
- **Platforms:** Windows / macOS / Linux (it is a Blender add-on; it runs wherever Blender does)
- **Tags:** `blender`, `pixel-art`, `texture`, `gamedev`, `tool`, `addon`, `3d`, `uv`, `sprites`, `animation`

## Description (store body)

### Your pixel art looks right in Aseprite and wrong on the model.

Two things go wrong, every time, and neither is your drawing.

**The pixels change size across the mesh.** A crate at 32 px/unit next to a wall
at 19 px/unit reads as two different games glued together. You cannot see it in
the UV editor and you cannot unsee it in the render.

**The strokes come out as staircases.** Freehand a shallow diagonal in a normal
paint tool and you get L-shaped double-texels down the whole line — the exact
artefact pixel artists spend their lives removing by hand.

**Texel fixes both, inside Blender, with no round trip.** Then it keeps going:
it animates the sprites too.

---

### What you actually get

**94 operators.** The nearest comparable add-on ships 67.

**Paint on the model.** Strokes in the 3D viewport are raycast onto the mesh and
resolved through its UVs, so the texel you hit is the texel you meant. Pencil,
eraser, line, rectangle, ellipse, flood fill, colour picker — square, round or
diamond brush at any size — with **Pixel Perfect on by default**, so a shallow
diagonal is a clean 1px line instead of a staircase. Mirror X and Y while you
paint and do half the work.

**Texel density, measured — not eyeballed.** *Detect Density* reports px/unit
across the mesh with its average, range and spread. *Apply Density* rescales
each face's UVs to your target. *Snap UVs to Pixels* puts every UV on a texel
corner and kills half-pixel seams. **This is the part a 2D paint tool cannot
do**, and it is the part that decides whether pixel art on a model reads at all.

**Density zones** let a hero prop sit at 64 px/unit inside a world at 24,
stored per face-group on the mesh, so it survives your next edit.

**Tiles that actually tile.** *Check Tiling* wraps the texture against itself
and scores the seam against the harshest edge already inside your own artwork.
It is a number, not a vibe. Every tile in the videos on this page was checked
this way before it went on a model.

**An indexed canvas — how pixel art actually works.** Every texel is an index
into a palette. Swap a colour and the whole image recolours instantly and
exactly: no drift, no float comparison, no "close enough". It is lighter too — a
512×512 layer costs 256 KB instead of 1 MB. Palette-wide brightness, contrast,
hue, saturation, posterise, greyscale and invert all run on the palette, so they
are exact and instant on any canvas size.

**Palettes that talk to your other tools.** Load `.gpl`, `.hex` or plain hex
lists. Save back to `.gpl` for Aseprite, Krita or GIMP. Lift a palette out of any
image open in Blender. Or pull one straight from **Lospec** by its slug.

**Generate shading ramps from one colour.** Real ramps shift hue toward blue in
shadow and toward yellow in light, and push saturation through the midtones.
Darkening toward black is what makes a ramp look muddy, and Texel does not do it.

---

### And it animates. Frames and tracks, like cel animation.

A **track** is a named row that runs the length of the animation — Body, BG, FX.
A **cel** is one track's drawing on one frame. So a single frame holds your
character, its background and its effects pass at once, and you edit each without
touching the others. Tracks stack like layers; the arrows in the cel grid send a
background behind where it belongs.

**Onion skin** ghosts the neighbouring frames of the track you are editing — only
that track, because ghosting an opaque backdrop twice over turns the canvas to
soup.

**Playback is Blender's own timeline.** *Bind to Timeline* and the spacebar plays
it, the scrub bar scrubs it, the fps field is the fps field you already know. No
second, worse timeline in a sidebar.

**Per-frame timing.** Hold a drawing for several frames to give a contact pose
weight. 2 frames at 12 fps is a sixth of a second.

**Export the way your engine wants it:**
- **Sprite sheet** at your column count
- **Sheet + JSON** — every frame's rect, hold and duration in milliseconds, so
  Godot, Unity, LÖVE or your own loader plays it without guessing
- **Animated GIF** at the scene fps, holds honoured, nearest-neighbour upscaled
  so texels stay square (needs ffmpeg)

**Hiding a track is an export.** Draw the character and its scenery in one
document, hide the scenery tracks, save — the same file hands you the finished
frame *and* the sprite on transparent, with no second copy to keep in sync. Every
character in the videos on this page was exported exactly that way.

---

### For 2D sprite work specifically
A locked, faint **reference layer** to trace over. **Trim to Content** to crop a
canvas to its artwork. A **colour count** that tells you how far over your palette
budget you are. Per-layer opacity. Selection, copy, paste and outline that
remaps through the destination palette instead of guessing.

---

### Present it without leaving Blender
**Showcase** builds a lit studio around your asset — six lighting presets
(golden hour, torch, cool, noon, ice, studio), four camera moves, bounded fog,
nearest-neighbour filtering forced on every texture so nothing is ever blurred —
and renders a still or a clip. The point is that **you** can make the images on
this page for your own asset, on your own store page, without building a set.

---

### Not in v0.1 — and which update brings it

Nothing here is a maybe. Each is a named release with a target date, and **every
one of them is free to you** if you buy today.

Releases are ordered **easiest first**. A young tool has to prove it ships, and
two releases that land beat one ambitious one that slips twice.

| Not yet | Arrives in | Target |
|---|---|---|
| Dither patterns, dithered gradients, custom stamps, radial symmetry | **v0.2 — the next release** | 26 Sep 2026 |
| Selection transforms (rotate / scale / flip, nearest-neighbour) | **v0.2 — the next release** | 26 Sep 2026 |
| Drawing-tablet pressure mapped to brush size | **v0.2 — the next release** | 26 Sep 2026 |
| Tileset slicing, a tile palette to stamp from, edge-wrap painting | **v0.3** | 17 Oct 2026 |
| Autotile / 47-tile blob generator | **v0.3** | 17 Oct 2026 |
| One-click Godot, Unity and Aseprite export | **v0.4** | 14 Nov 2026 |
| Animation tags (walk / idle / attack) carried into exports | **v0.4** | 14 Nov 2026 |
| Normal, emission and AO maps generated from the indexed art | **v0.5** | 12 Dec 2026 |
| Tweening between key cels, and a dope sheet | **v1.0** | 30 Jan 2027 |

Two things on that list are **deliberate and not going to change**:

- **255 colours plus transparent.** That is what an indexed canvas *is*, and it
  is why a palette swap is exact and instant. Opening a texture with more refuses
  rather than silently quantising your art.
- **GIF export needs ffmpeg** on PATH. Bundling a video encoder into a Blender
  add-on is not a thing a good add-on does. Sheet and JSON export need nothing.

Dates are targets, not promises. **A release that misses one says so in its
devlog** rather than quietly moving the date, and what buyers actually ask for
reorders this list — three people asking for the same thing beats a plan written
before anyone bought it.

### The update promise
**Every update is free to everyone who has ever bought it.** No paid v2, no
subscription, no pro tier.

**The price rises at named milestones, announced in advance** — $14.95 when v0.4
ships engine export, $19.95 when v1.0 ships tweening and the dope sheet. Buying
early is cheaper because the tool is younger, and that is the whole deal.

The full ladder, with dates and what is in each version, is in `ROADMAP.md`
inside the download. Dates are targets, and a release that misses one says so in
its devlog rather than quietly moving the date.

---

## FAQ

Grouped the way a buyer actually decides: what stops them buying, then what
stops them working.

### Before you buy

**Is this a standalone app?**
No. It is a Blender add-on and it runs inside Blender, on your existing scene.

**Which Blender versions?**
**4.2 and newer**, and that is measured rather than declared. The full suite -
16 of them, including the one that invokes all 94 operators - is run against
**4.2.23** (the oldest LTS we support), **4.5.9 LTS**, **5.2.1**, and the
**Microsoft Store 5.2.1** build as well, because that one installs add-ons to a
different place than every other Blender and deserved its own run. All four
pass. If it breaks on a version we claim, that is a bug and it gets fixed.

**Does it need anything else installed?**
No. Pure Python against Blender's own API — no numpy, nothing to compile, no
internet. Two optional extras: fetching a palette from Lospec needs a connection,
and **GIF export needs ffmpeg on PATH**. Sheet and JSON export do not.

**Windows, Mac or Linux?**
Wherever Blender runs. It is platform-independent Python with no OS-specific
calls except looking for ffmpeg. **Built and tested on Windows** — if something
is wrong on macOS or Linux, tell me and it gets fixed, but I am not going to
claim a test I did not run.

**Does this replace Aseprite?**
No, and it is not trying to. Aseprite is a better 2D drawing program and always
will be. Texel does the part Aseprite cannot: paint directly on the model, and
measure and fix texel density across a mesh. They round-trip — Texel reads and
writes `.gpl` palettes and exports sprite sheets.

**Can I sell what I make with it?**
Yes. The licence covers the add-on, not your artwork. Commercial use, client
work, paid asset packs — all yours, no royalty, no attribution required.

**It says GPL-3.0. What does that actually mean for me?**
Every Blender add-on that uses `bpy` must be GPL — that is Blender's licence, not
a choice. In practice: you can use it, modify it, and pass it on. The source is
in the zip because it has to be. **It places no restriction on the art you make.**

**Do I get updates free?**
Yes, forever. No paid v2, no subscription, no pro tier. The price rises at
milestones announced in advance, and you never pay the difference.

**Can I get a refund?**
Yes. Ask and it is granted — no interrogation, no retention pitch.

### Using it

**Can I paint in the 3D viewport?**
Yes, and in the Image Editor. Viewport strokes are raycast onto the mesh and
resolved through its UVs, so the texel you hit is the texel you meant.

**Does it work with my custom shader / material?**
Yes. Texel writes into an image texture. If your material uses one, it paints it.

**Do I still have to unwrap my UVs?**
**Yes.** Texel *measures* and *rescales* UVs — it does not make a good unwrap out
of a bad one. Unwrap the way you normally would, then let *Apply Density* put
every face at the same pixels-per-unit.

**Is there undo?**
Yes — Blender's own undo stack, and it works the way you expect: **one Ctrl+Z
undoes one stroke.** Painting is a modal operator, so a whole drag is a single
undo step, and a fill or a palette change is likewise one step.

**Are there keyboard shortcuts?**
**Yes.** B pencil, E eraser, L line, U rectangle, C ellipse, F fill, I picker,
M mirror, D paint — in the Image Editor, plus D to paint in the 3D viewport.
Every one is **rebindable in Preferences → Keymap** (search "texel"), because
they are registered as a real Blender keymap rather than grabbed events. The
keys were picked by measuring Blender 4.5's own bindings, so nothing of yours is
stomped, and a test re-runs that measurement on every release.

**Does it work with a drawing tablet?**
Today a tablet works as a mouse — **pressure is not mapped to anything.**
Pressure-to-size ships in **v0.2, the next release, targeted 26 September**.

**How big can a canvas be?**
Up to 4096×4096. The canvas is indexed — one byte per texel — so a 512×512 layer
costs 256 KB instead of 1 MB, and layers stay cheap.

**My texture has more than 255 colours.**
It will **refuse to open it** rather than silently quantise your art. 255 plus
transparent is the ceiling. A silent quantise is how a texture comes back subtly
wrong three hours later.

**Does it generate normal or PBR maps?**
Not yet. Normal, emission and AO maps generated straight from the indexed art
ship in **v0.5, targeted 12 December**. Right now it paints base colour.

**Does the animation do tweening?**
Not yet. Frames are drawn by hand, which is how pixel-art animation works, and
you get cels, tracks, per-frame timing and export today. Tweening between key
cels and a dope sheet ship in **v1.0, targeted 30 January 2027**.

**How do I get an animation into Godot / Unity / my engine?**
Export **Sheet + JSON** — a manifest with every frame's rect, hold and duration
in milliseconds, which any engine reads in a few lines. **One-click Godot, Unity
and Aseprite export ships in v0.4, targeted 14 November**, and it is free to you.

### After you buy

**Where do I start?**
Open `START-HERE.html` in the zip — install steps and a first five minutes. The
same guide, kept up to date, is at **mintworks.cc/texel**.

**I found a bug.**
Comment on the itch page. Every report is reproduced against the shipped zip
before it is answered, and you get told which version fixes it. If it crashes or
loses work, it jumps the queue.

**I want a feature.**
Ask. Requests are tallied, and the tally reorders the roadmap — three people
asking for the same thing beats a plan written before anyone bought it.

### What you need
Blender **4.2 or newer**. No other dependencies — no numpy, nothing to compile,
no internet required except the optional Lospec fetch.

### Licence
**GPL-3.0-or-later**, as every add-on built on the Blender Python API must be.
**The artwork you make with it is yours** — the licence covers the add-on only
and places no restriction on your textures, commercial use included.

---

## ⚠ Decisions needed before upload

### 1. Price
The nearest comparable Blender add-on asks **$29.90**. AssetDrop currently asks
$4.95, which is a sixth of what this market bears.
**Recommendation: $14.95**, or $9.95 as a launch price. High enough to signal a
real tool, below the incumbent, and roughly 3× AssetDrop, which the store data
says we have been underpricing.

### 2. AI disclosure — READ THIS, IT DIFFERS FROM THE PACKS
itch asks which parts of a project are AI-generated: Graphics, Sound, Text, Code.

Our standing answer for the **pixel art packs** is **Yes + Graphics only**
(settled 2026-08-25). **That answer would be false here.** Texel's source code
was written with AI assistance, so the honest answer for this project is
**Yes + Code**, and **Graphics** as well because the cover art was generated.

Claiming Graphics-only on a product whose substance is code would be a false
declaration on a form we are on record telling other routines never to soften.
**Recommendation: tick Yes, Code and Graphics.**

### 3. Name
`Texel` is precise — texel density is the whole problem the tool solves — and
does not collide with the reference product. Confirm before the URL is claimed,
because the itch slug is painful to change afterwards.

---

## Prose AI disclosure for the page (one sentence, per house rule)
> Texel was built with AI assistance; every feature described here was tested in
> Blender 4.5 and the test suite ships in the repository.

## Devlog opener (for launch)
`Texel 0.1.0 — pixel art painting for Blender, with texel density that actually gets measured`

## Assets ready

**Video — five cinematic shots, each arguing one capability.** Every texture in
every shot is painted by Texel's own operators, and each tile's seam score is
measured, not assumed.
- `promo/shot-dungeon.mp4` — side-scroller corridor, the character walking. ANIMATION.
- `promo/shot-temple.mp4` — isometric ARPG chamber. SEAMLESS TILING.
- `promo/shot-hangar.mp4` — sci-fi bay, one texture in three palettes. PALETTE SWAP.
- `promo/shot-market.mp4` — top-down exterior, huge ground and hand-sized props. TEXEL DENSITY.
- `promo/shot-shrine.mp4` — symmetric facade drawn as one half. MIRROR SYMMETRY.

**Video — the interface, actually being used.** Real Blender, real operators.
- `promo/steps-anim.mp4` — frames, tracks, cel grid, onion skin, bind, scrub, GIF
- `promo/steps-sprite.mp4` — reference layer, brush shapes, opacity, trim, colour count
- `promo/steps-showcase.mp4` — pick a light and a move, build it, render the still

**Stills and files**
- `promo/anim/Torchbearer.gif` — 8 frames across 4 tracks, exported BY Texel
- `promo/anim/Torchbearer_sheet.png` + `_anim.json` — the sheet and its timing manifest
- `store/cover_630x500.png` — itch cover, house pipeline, verified at 315px browse size
- `shots/hero.png` — Cycles render, textured through Texel's own core
- `dist/texel-0.1.0.zip` — install-verified in Blender 4.5.9

## Still to make before upload
- The density readout mid-measurement, as a still
