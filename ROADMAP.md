# Texel by Pixelkiln — upgrade schedule

**Written 2026-09-09. Last ticked 2026-09-16 by `texel-release`.**
**v0.1.0, v0.2.0 and v0.2.1 are live at https://z3er1n.itch.io/texel.**

This is the promise the store page makes and the queue `texel-release` works
from. It exists because **update cadence is the retention mechanic** — the same
lesson the LimeZu playbook taught the pack business, applied to a tool. A
Blender add-on that ships once is dead in three months.

One correction to that, made 2026-09-16 because it was borrowed without
checking: **Texel has no buyers yet, so there is nobody to retain.** The audience
for these releases is the person who has not bought it, reading a page with a
track record on it. That is still a reason to ship on the dates; it is a
different reason, and the file should say which one it is using.

---

## The ordering rule: easiest first, hardest last

Releases are ordered by **how hard they are to build**, not by how badly anyone
wants them. Three reasons:

1. **A young tool has to prove it ships.** Two releases that land on their dates
   buy more trust than one ambitious release that slips twice. Nobody believes a
   roadmap; they believe a track record.
2. **The hard features get better for waiting.** Normal-map generation and
   tweening both want a settled foundation. Building them in month one means
   building them on assumptions the support queue has not tested yet.
3. **It fails safely.** If this venture stalls at v0.3, buyers still got three
   real releases. Front-loading v1.0's features and stalling would leave them
   holding half a dope sheet.

The one thing that overrides it: **a reproduced crash jumps everything**, and so
does an ask three or more people have made (`SUPPORT.md` keeps that tally).

---

## The two commitments, made publicly on the listing

1. **Every update is free to everyone who has ever bought it.** No paid v2, no
   subscription, no "pro" tier. Buy once.
2. **The price rises at named milestones, announced in advance.** Buying early
   is rewarded; the reward is real because the price genuinely steps up.

| Milestone | Price | Why the step is honest |
|---|---|---|
| v0.1 launch | **$9.95** | The top of Pixelkiln's own ladder. An unproven tool from an unknown seller. |
| v0.4 "Handoff" ships | **$14.95** | Engine export closes the gap that stops it being a production tool. |
| v1.0 "Studio" ships | **$19.95** | Tweening + dope sheet + project files. Feature-complete against the brief. |

The position never changes with the number: *the one that measures texel
density, at a price that does not need a discussion.*

> These two lines used to anchor the price to another add-on's $29.90. The
> standing rule in `promo/POSTED.md` (user, 2026-09-09) is that no listing line
> **or log entry** frames Texel as competing with or descending from another
> product, and it was applied to `LISTING.md` the same day but missed here -
> which matters more, not less, because **this file ships inside the customer
> zip**. Removed 2026-09-09; it reaches buyers at the next release.

---

## Release ladder

Dates are targets, not guesses dressed as promises. Each release is gated on its
own tests passing and the zip installing clean — **a date is never met by
shipping something untested.** If a gate fails, the release slips and the devlog
says so.

### v0.1.0 — "Launch" · target 2026-09-12
**SHIPPED 2026-09-09**, three days early. The three blocking decisions (price
$9.95, AI disclosure Yes + Code + Graphics, name Texel) were settled the same
day and are recorded in `LISTING.md`.

94 operators. Painting on the model and the flat canvas, pixel-perfect strokes,
texel density measure/apply/snap, density zones, indexed canvas, palettes
(.gpl/.hex/Lospec), layers with opacity and groups, selection + clipboard,
palette adjustments, tiling check, mirror, outline, dither fill, showcase
renders, cel animation (tracks × frames), sprite tools, GIF + sheet + JSON
export — and **keyboard shortcuts**, pulled forward from v0.2 because a paint
tool without them reads as a prototype in the first thirty seconds.

### v0.2.0 — "Brush" · **SHIPPED 2026-09-09**, seventeen days early
A **partial** release, which the header of this file says is normal: the slice
that was ready shipped rather than waiting for the rest of the version.
- ✅ **Selection transforms — rotate, scale, flip — nearest-neighbour, no
  resampling.** `core.tools.scale_nearest` and `core.select.transform_region`,
  operator `texel.selection_transform`. The mask is transformed with the art, so
  a magic-wand selection survives a rotation as its own shape; the result is
  centred on the box it replaced rather than pinned to a corner.

The rest of "Brush" moves to **v0.2.2**, keeping the original 26 Sep target.
(It was v0.2.1 until 2026-09-16, when a patch took that number.)

### v0.2.1 — "Readout" · **SHIPPED 2026-09-16**
A patch, and it took the 0.2.1 number that "Brush, the rest" was holding -
which is why that release is now **v0.2.2 below, with its 26 Sep target
unchanged.** Renumbering rather than slipping: no dated promise moved.

- ✅ **The density readout fits the sidebar.** It printed as one 41-character
  line, and Blender middle-elides anything wider than its row, so a 280 px
  N-panel showed `10.5 px/unit av....1, 8.4x spread)` - the average survived and
  the range and the spread were replaced by dots. `Region.width` is read-only,
  so no window size fixed it; the string had to shrink instead. Now three lines,
  one measurement each. Reproduced on 4.5.9 before the fix and re-shot after, at
  UI scale 1.0 and 1.5.
- ✅ `build.py` now fails when a source module exists but is missing from its
  file lists. The first 0.2.1 zip built without `core/report.py` in it.
- ✅ **Radial symmetry.** One drag repeats up to sixteen times around the canvas
  centre, and it composes with the mirrors - radial 4 with Mirror X is eight-fold.
  `core.raster.symmetry_points`, which also took over the mirror maths that had
  been sitting in `tex_paint` where no headless test could reach it. No new
  operator: it is a property on the existing stroke.

**The density readout is the feature the product is positioned on, and it had
been unreadable in the panel that prints it since launch.** It was named twice by
other routines before it was owned, which is the part worth not repeating.

> Radial was not in the original plan for this release, and the honest reason it
> is here is that `venture-critic` returned FATAL on the first version of the
> scope call. That version said "none of the remaining Brush items is a small
> slice" without checking any of them. Two things were wrong: **Mirror Y has
> shipped since v0.1.0** and this file was simply stale in listing it as
> outstanding, and radial symmetry reduces to one pure function over the points
> a stroke already produces. The gate was being paid for the bugfix either way,
> so the marginal cost was the feature, not a second gate.

### v0.2.2 — "Brush", the rest · target 2026-09-26
Four items, not five - **Mirror Y was never outstanding** (shipped in v0.1.0;
this list was stale) and **radial symmetry shipped in v0.2.1**. Each remaining
item is priced against the code that already exists, because "too big" was
asserted once here without anyone checking:

- **Dither patterns as a brush mode**; Bayer and hand-authored masks.
  *Medium.* The density masks exist inside `TEXEL_OT_dither_fill`
  (`tex_extra.py`) but are inline in that operator and keyed on absolute x/y.
  Lifting them into `core` and consulting them per stamp touches the modal paint
  path and the tool enum.
- **Gradient tool that dithers between two palette indices** instead of blending.
  *Large.* Needs a two-point drag interaction that does not exist yet, plus a
  ramp-to-dither mapping on top of the item above.
- **Custom stamp from a selection.** *Medium.* Stamp storage on the doc, a new
  operator, UI, and paint-path integration.
- **Tablet pressure mapped to brush size.** *Small-to-medium, and unverifiable
  here* - `event.pressure` always reads 1.0 from a mouse, so the gate can prove
  the plumbing and cannot prove the feel. That is worth saying out loud before
  it is claimed on the page.

**Is 26 Sep still reachable?** One release run remains before it (Wed 23 Sep).
One run does not carry a Medium, a Large and two Mediums. So the honest reading
is that v0.2.2 ships **partial on 26 Sep** - the dither brush mode, most likely -
with the rest moving to v0.2.3. That is the normal pattern on this roadmap and
it is written down now rather than discovered on the day.

### v0.3.0 — "Tileset" · target 2026-10-17
**Medium: new data structures, but still all our own code.**
- Slice an image into a tile grid; a tile palette panel you stamp from
- Stamp brush with a tile picked from the sheet
- Per-tile seam check across a whole tileset, not one image at a time
- Edge-wrap paint mode (a stroke off the right edge continues on the left)
- **Autotile / blob generator**: paint one tile, get the 47-tile transition set.
  The hardest single thing in this release, which is why the release sits third
  and not first.

### v0.4.0 — "Handoff" · target 2026-11-14 · **price steps to $14.95**
**Harder, because it means being correct about other people's formats.** A wrong
pivot or a malformed `.meta` is worse than no exporter at all.
- Godot: atlas + `.tres` sprite-frames with animation names
- Unity: sheet + `.meta` sprite rects, pivot and pixels-per-unit set correctly
- Aseprite: import/export frames and tags, so it round-trips with the tool
  everyone already owns
- Animation **tags** (walk / idle / attack) carried into every export
- Batch export: every canvas in the file, one click

### v0.5.0 — "Lit" · target 2026-12-12
**The first genuinely hard release, and the thing no 2D tool can do.** Deriving
a believable normal from flat indexed art is an image-processing problem, not a
UI problem.
- Generate **normal, emission and AO maps** from the indexed art
- Per-palette-index material slots — mark index 12 emissive, get glowing lamps
- Pixel-art shading preview: quantise the lit result to the palette so you see
  the game's look, not Blender's

### v1.0.0 — "Studio" · target 2027-01-30 · **price steps to $19.95**
**The most complex release, deliberately last.** A dope sheet is a whole new
editor surface, and a project file is a format we then have to keep reading
forever.
- Tweening between key cels (position/opacity only — never interpolated pixels)
- Dope sheet view for retiming without the sidebar grid
- `.texel` project file so a document survives outside a .blend
- The upgrade promise closes: v1.0 is the feature set the launch page described

---

## Taken off this list, and why

- **Per-stroke undo.** It sat here until `texel.paint` was read properly: it is
  a *modal* operator with `bl_options = {"REGISTER", "UNDO"}`, so one drag is one
  undo push. **Undo is already per stroke.** The documentation said otherwise and
  was under-selling the product; it is corrected everywhere.
- **Customisable keymaps.** Moved into v0.1. Registering a keymap is a small job,
  it is the most visible thing the reference product had that we did not, and
  "everything is a sidebar button" is the first complaint a power user makes.
- **A free "lite" build.** The add-on is GPL, so a crippled version would be
  stripped and reposted inside a week. The free tier is *content* instead —
  `texel-funnel` ships palettes, tiles and cheatsheets.

---

## After v1.0 — the maintenance contract
Support does not end at v1.0. The standing commitment on the page becomes:
**compatibility with each Blender LTS within 30 days of its release**, and bug
fixes indefinitely. New feature work becomes demand-led, from the support queue
(`texel-support` keeps the tally in `SUPPORT.md`).

---

## How a release actually happens

`texel-release` runs **Wednesdays at 10:00** and owns this file. Its loop:

1. Read the next unshipped version here. Pick the **smallest shippable slice**
   of it, not the whole version.
2. Build it. Write tests **first** where the behaviour is checkable in pure
   Python (`core/`), which is most of it.
3. Gate: all 17 suites green, `core/` coverage still 100%, `build.py` clean,
   and **`bash test_versions.sh` green on every installed Blender** - the
   store page claims 4.2+, so one version passing is not evidence for it.
   Then **`python store_check.py`**, which runs the same suites inside the
   Microsoft Store build: it is a different install path, it is how a lot of
   Windows users get Blender, and its ACL means no other script can reach it.
   **Any red gate = no ship.**
4. Bump `blender_manifest.toml` and `bl_info` together (`build.py` fails if they
   disagree). Rebuild the zip.
5. Upload to itch, write the devlog, hand the marketing beat to
   `texel-marketing` by appending to `promo/QUEUE.md`.
6. Tick the item here with the date it actually shipped.

**A version ships when its slice is done, not when its date arrives.** Partial
versions are fine and normal — v0.3.0 may ship tile slicing and stamping without
autotile, and the leftover moves to v0.3.1.
