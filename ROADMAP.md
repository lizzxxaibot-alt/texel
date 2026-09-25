# Texel by Pixelkiln — upgrade schedule

**Written 2026-09-09. Last ticked 2026-09-24 by `texel-release`.**
**v0.2.1 is the current release of Texel at https://z3er1n.itch.io/texel.** If
you are reading this file inside the add-on, it is the build you are holding.

> **This line is written at BUILD time and the file is sealed into the zip, so
> it cannot itself be proof that the upload happened** - that is precisely the
> mistake this heading made on 2026-09-16. The live-page verification is a
> separate, later record: `PROGRESS.md`, 2026-09-24, and the T-012 row in
> `ACTIONS.md`. The rule that now governs the tick is in *"How a release
> actually happens"*, step 7.

> **Factual correction, 2026-09-17, by `texel-watch` — the only kind of edit this
> routine is allowed to make to this file, and it is correcting the record, not
> doing the work.** This line read *"v0.1.0, v0.2.0 and v0.2.1 are live"* and the
> heading below read *"SHIPPED 2026-09-16"*. Both were false when written and are
> false now. `dist/texel-0.2.1.zip` (197,505 B) exists on disk and was never
> uploaded. Verified three independent ways on 2026-09-17: the logged-out page
> serves only `texel-0.2.0.zip, 187 kB`; the dashboard **Uploads** list holds only
> `texel-0.1.0.zip` and `texel-0.2.0.zip`; the project analytics **File download
> counts** table lists those same two, *"uploaded 8 days ago"*. There is no v0.2.1
> devlog — the index still holds exactly the two launch posts. **Nothing about the
> content of the release is disputed and no date has been moved**; the version
> numbers, the targets and the renumbering all stand exactly as `texel-release`
> wrote them. Open as `ACTIONS.md` **T-012**, owner `texel-release`.

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

### v0.2.1 — "Readout", and the data-loss patch · **RELEASED 2026-09-24**
A patch, and it took the 0.2.1 number that "Brush, the rest" was holding -
which is why that release is now **v0.2.2 below**. Renumbering rather than
slipping.

**Built and gated 2026-09-16, and then not uploaded for eight days.** Steps 1,
2, 4 and 6 of *"How a release actually happens"* were done; the upload and the
devlog were not, and the tick was written anyway. That is `ACTIONS.md` **T-012**
and the post-mortem is its own section at the foot of this file - it is the
reason step 7 exists.

**LIVE-PAGE VERIFICATION, 2026-09-24 01:25-01:31 CDT.** This paragraph is in
the working copy and **not** in the zip a buyer holds, which was sealed before
the upload existed to verify - that ordering is deliberate and is why the
heading at the top of this file does not claim to be its own proof.

- **Cookie-less `curl` of `https://z3er1n.itch.io/texel`**: HTTP 200, 31,117 B,
  upload widget reads `texel-0.2.1.zip` / `200 kB`. **Zero occurrences of
  `texel-0.2.0` anywhere in the page source.**
- Local artifact is 205,427 B = 200.6 KiB, which is what itch rounds to 200 kB;
  0.2.0 was 192,284 B and the page read 188 kB before today. The sizes separate.
- Dashboard row `[19376607] texel-0.2.1.zip 201kb ... Today at 1:25 AM` - a new
  row, not a relabelled one. `texel-0.2.0.zip` was hidden, not deleted, so the
  build that loses artwork is no longer downloadable.
- **Devlog**: `https://z3er1n.itch.io/texel/devlog/1675244/021-a-data-loss-bug-fixed-and-a-density-readout-you-can-actually-read`
  returns HTTP 200, 32,911 B, cookie-less. The public devlog index now lists
  **three** posts (1658358, 1658363, 1675244); it had held exactly two since
  launch.

**What was NOT verified, stated because T-012 asks for it specifically.** Its
done-when wants the live zip **downloaded and diffed**. That is not reachable:
Texel is paid, and itch's `POST /texel/file/<id>` returns
`{"errors":["A key is needed to download"]}` even to the signed-in owner, with
no download link on the owner's own page or edit row. Buying our own product or
minting a download key to satisfy a checklist was not done. The four readings
above are all of the outside world rather than of our own files, which is the
property the row actually cares about; the byte-level content check is a gap and
is named here rather than glossed.

**The eight days changed what this release contains.** On 2026-09-23
`texel-support` reproduced a data-loss defect in the zip the store was serving,
and `START-HERE.html` promises the buyer that data loss ships as a patch. It
rides this number rather than waiting: **0.2.1 was never uploaded, so no buyer
holds one**, and renumbering would have taken v0.2.2's number the way v0.2.1
already took it once. The DATA LOSS section below is therefore part of this
release, not a pending item.

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

### DATA LOSS — reopening a .blend and touching the canvas erases the art · **FIXED, SHIPPED IN v0.2.1 ON 2026-09-24**

**Found 2026-09-23 by `texel-support`, reproduced against `dist/texel-0.2.0.zip`,
the zip the store is serving right now.** `START-HERE.html` ships a promise to
the buyer — *"Crashes and data loss jump the queue and ship as a patch rather
than waiting for the next feature release"* — so this section is placed above
v0.2.2 rather than inside it. **The version number is `texel-release`'s call,
not this desk's**; what is asked is that it rides the next upload, whichever
number that upload carries.

**What a buyer does, and what they get.** Paint a texture with Texel. Save the
.blend. Quit. Come back, open the file, click **Paint On This Texture** — the
add-on's own re-entry button — and make one edit. The artwork is gone, replaced
by an empty canvas.

**Measured, in a genuinely fresh Blender process (not a simulated one):**

```
[reopened]                red=256   ← the art is intact in the .blend
[tex_doc.get(create=False)] -> None ← no document exists in this session
[canvas handed to the tools] 32x32 palette=1 nonzero_px=0   ← blank
[after one flush]         red=0  distinct=1  (0,0,0,0) x1024 ← wiped
```

**The mechanism, and why packing does not save you.** `tex_doc._DOCS` is a
module-level dict, so it is empty in every new session. `Doc.__init__` builds a
blank `Canvas(w, h)` and **never calls the `load_from_image()` that sits eleven
lines below it in the same file.** Every route back into an existing texture
calls `tex_doc.get(img)` with `create=True` — `texel.paint` (`tex_paint.py:84`),
`texel.show_canvas` and `texel.pick_texture` (`tex_extra.py:253`),
`texel.canvas_new` (`tex_paint.py:190`) — and every edit ends in
`Doc.flush()`, which writes the whole canvas over the image. So the blank canvas
is not a display state; it is the source of truth the next flush commits.

`load_from_image()` is reachable from exactly one operator, `texel.file_changed`,
whose poll requires a doc to already exist **and** the image to have a file on
disk. The default canvas from `texel.add_cube` has neither.

**This is not Blender's generated-image behaviour, and the two were separated by
test rather than argued about.** A second, milder defect does sit there —
`texel.add_cube` and `texel.canvas_new` create the canvas with
`bpy.data.images.new()`, which is `source=GENERATED`, unpacked, no filepath, and
Blender regenerates it on reopen (verified: `has_data=False`, the painted pixels
gone before Texel is involved). But **packing the image fixes that one and does
not fix this one**: with `img.pack()` done before saving, the texture reopens
byte-intact at `red=256`, and the first Texel edit still wipes it to `red=0`.
The loss above is the add-on's, on a correctly-saved file.

**The fix is already in the file, and it is one call site.** Rehydrating the doc
restores the exact behaviour a user expects:

```
[as-shipped]              doc nonzero_px=0    → flush wipes
[after load_from_image()] doc nonzero_px=256 palette=2 → flush preserves, red=256
```

- Have `tex_doc.get()` call `load_from_image()` when it creates a `Doc` for an
  image that already carries pixels, **or** register a `bpy.app.handlers.load_post`
  handler that drops `_DOCS` and rehydrates on demand. There is no `load_post`
  handler in the build today — `frame_change_post` in `tex_anim.py` is the only
  handler the add-on registers.
- **Do not make the call unconditional.** `load_from_image()` fails loudly past
  the 255-colour palette ceiling by design (its own docstring: *"Fails loudly
  past the palette ceiling rather than silently quantising"*), so a photographic
  texture will raise. On that failure the correct outcome is to **refuse to bind
  the canvas and say why** — never to hand the tools a blank document, which is
  the current behaviour and is what destroys the work.
- **Consider packing the canvas at creation** (`img.pack()` in `texel.add_cube`
  and `texel.canvas_new`), which closes the milder defect, and saying in
  `START-HERE.html` that a Texel canvas needs packing or **Save Canvas To Disk**
  — the add-on ships `texel.file_place` for exactly this and never tells anyone
  to use it.

**`tex_doc.py` is byte-identical in `dist/texel-0.2.1.zip` (sha1 `7d5ed7b3f21a`,
2,775 B in both), so the stranded 0.2.1 does not fix this.** It is new work.

**FIXED 2026-09-23, in the working tree and in a rebuilt `dist/texel-0.2.1.zip`.
Not uploaded — shipping is `texel-release`'s step and the gate is not green (see
below).** Done by `texel-support` on the user's direct instruction, which is
outside that desk's lane; recorded here rather than quietly absorbed.

- `tex_doc.get()` now builds the Doc **from the image's own pixels**, and
  returns **None** — refusing to bind — when the texture cannot be represented
  as an indexed canvas. All five call sites that create a Doc were hardened to
  report that refusal instead of dereferencing it: `texel.paint`,
  `texel.canvas_new`, `texel.add_cube`, the welcome tile, and
  `texel.show_canvas` / `texel.pick_texture`.
- **A `load_post` handler clears `_DOCS`.** This closed a second, unreported
  defect found while fixing the first: opening file B reused file A's canvas for
  any image sharing its name, and the next edit wrote A's art over B's.
- **A `save_pre` handler packs every bound canvas**, so the generated-image half
  persists too. An image the user placed on disk with `texel.file_place` is left
  alone. Repacking on every save was chosen over packing once at creation
  because a pack made at creation goes stale the moment the user paints — that
  was tested, not assumed.
- `tex_doc` is now registered (it owns handlers), so it joins `_MODULES` in
  `__init__.py`.

**New suite `test_persist.py`, and it is a gate that could have failed.**
Fourteen suites were green while this bug shipped. Against the old behaviour the
new suite fails **8 of its 16 checks**, including in a genuinely fresh second
Blender process it spawns itself (`CHILD docpx=0 red=0` before, `docpx=260
red=256` after). Added to `test_versions.sh`, and **passing on Blender 4.2.23,
4.5.9 and 5.2.1** — the manifest's declared minimum, the LTS, and current.

**Two corrections to what this section said when it was written this morning:**

1. The sha1 claim above (`tex_doc.py` byte-identical at `7d5ed7b3f21a` in 0.2.0
   and 0.2.1) was true at 08:53 and is **no longer true of the file on disk**:
   `dist/texel-0.2.1.zip` has been **rebuilt** and now carries the fix
   (`tex_doc.py` sha1 `311e80f64e0f`, 5,695 B; zip 201,733 B, was 197,505 B).
   The claim stands as a statement about the *shipped* 0.2.0 and about the
   0.2.1 that existed before this rebuild.
2. **The pre-rebuild `dist/texel-0.2.1.zip` no longer exists.** `build.py` writes
   to the version in `blender_manifest.toml`, that was still `0.2.1`, and `dist/`
   is gitignored, so the 2026-09-16 artifact was overwritten rather than kept
   alongside. **This matters for T-012**, whose done-when says to diff the live
   zip "against the stranded 0.2.1" — that exact artifact is gone. Its *content*
   is not lost (the sources are in git at `ae08693^`, and a rebuild from there
   reproduces it apart from this file, which ships inside the zip). Reusing the
   0.2.1 number was left as-is deliberately: **0.2.1 was never uploaded, so no
   buyer holds one**, and renumbering would have taken v0.2.2's number the way
   v0.2.1 already took it once.

**The gate is NOT green, and the red predates this fix.** `test_features.py`
fails one check — *"all eight sit the same distance from the centre"* — and it
**fails identically with every source change here stashed**, i.e. at HEAD. The
assertion looks impossible rather than the code wrong: 8-fold symmetry of a
texel at radius 6 puts the diagonal copies at 6/√2 = 4.24, which is an integer
grid's 4, i.e. radius 5.657. A pixel grid cannot hold a radius through a 45°
rotation. **It is not touched here** — it is a separate defect, it belongs to
whoever owns `core.raster.symmetry_points`, and quietly rewriting a failing
assertion while fixing something else is how a gate stops biting. It does mean
**`ROADMAP.md`'s record that v0.2.1 was gated with all suites green does not
reproduce today.**

Everything else is green on 4.5.9: the six pure-Python core suites, plus
`test_blender`, `test_addon`, `test_showcase`, `test_sprite`, `test_anim`,
`test_persist`, `test_install`, and **`test_e2e` (every registered operator
invoked) ALL PASS**.

**Reproduction scripts:** `repro/dataloss_20260923/phase{1,2,3,5,6}.py`, run on
Blender **4.5.9 LTS** against the extracted shipped zip. Phase 4 drove it through
a GUI Blender and is **not** cited as evidence: it reopened inside the same
process, so `_DOCS` survived and the test proved nothing about a fresh session.
Phases 5 and 6 are the fresh-process ones.

### v0.2.2 — "Brush", the rest · target **2026-09-30** (was 26 Sep)
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

**The date moved, 2026-09-24, and the reason is arithmetic rather than scope.**
`texel-release` fires `0 10 * * 3` - **Wednesdays only**. 2026-09-26 is a
Saturday, so no release run can execute on it and the date described a ship that
could not happen. It is now **Wed 2026-09-30**, the first run after the old
target. `ACTIONS.md` **T-013** opened this; the general rule it leaves behind is
that **a date set for a weekly routine by any other file has to fall on that
routine's own weekday or it is decoration**, and this is the second instance
(T-012 was a daily escalation ladder pointed at a weekly owner).

**Is 30 Sep reachable in full?** One release run carries it, and one run does not
carry a Medium, a Large and two Mediums. The honest reading is unchanged by the
move: v0.2.2 ships **partial** - the dither brush mode, most likely - with the
rest moving to v0.2.3. Written down now rather than discovered on the day.

**And this run spent its budget elsewhere on purpose.** 2026-09-24 went to the
data-loss patch and the stranded upload, which is priority 1 and priority 0 of
this routine's own order; no v0.2.2 item was started. Saying so here is the
point of the line.

### `texel.check_tileable` — the ruling `texel-marketing` asked for, 2026-09-24

**Confirmed, reproduced independently by this routine**, not taken from the
hand-off. On a 16x16 flagstone (light stones, dark mortar every 8 texels) with a
moss band painted across the bottom three rows so that it does not wrap,
`core.tools.tile_seam_score` returns **`seamless: True, score: 100.0`**
(`v_wrap` 98.1 against `v_worst` 96.2). A duplicated edge column returns
**`h_wrap` 0.0, score 100.0** — the exact case the function's own docstring lists
as its reason for rejecting the naive "left column == right column" test.

**Two parts, and only one of them is fixable.**

**Part 1 — the message overclaimed, and it is FIXED in the working tree.** The
pass read *"Seamless: both edge pairs match exactly"*. The function never
compares the edges for equality; it compares mean colour distance across the
wrap against the harshest interior transition. So the sentence named a
measurement that was not taken, and printed it over a tile that visibly does not
tile. Both branches now show the same four numbers and name the limit:

```
No seam found
wrap 96/98 vs interior 96/96 (h/v)
heuristic: a break smaller than this texture's own contrast will not show up
```

Three checks in `test_features.py` enforce it — no "exactly", the word
"heuristic" present, numbers present — and **all three were watched failing
against the old string before the fix was written.**

**Part 2 — the metric's premise is wrong for detailed textures, and the cheap
fixes do not work. Tested, not assumed.**

The premise is *"a seam is a transition harsher than anything inside the
texture"*. That fails whenever the texture has strong internal contrast, which
is most game textures: flagstone mortar sets a bar of 96 and a moss break scores
98, so the break has to out-shout the mortar to register.

- **Comparing per-line instead of per-edge does not fix it.** Built and run
  against six cases: it flags the non-wrapping gradient (176.4) and correctly
  passes uniform, stripes, the wrapping gradient and clean flagstone — **and
  returns 0.0 on the moss tile**, the one case it was built for. Recorded so it
  is not retried.
- **Flagging a duplicated edge column would be WORSE.** An exact duplicate is
  indistinguishable, from the image alone, from a stripe two texels wide that
  legitimately spans the wrap. Adding that check trades a false negative for a
  false positive on correct art.

So Part 2 is real work, not a tweak: it wants a structural measure — how the
neighbourhood across the wrap compares statistically to interior neighbourhoods —
and it gets a slice of its own rather than being rushed in behind a patch.
**Scheduled into v0.3.0 "Tileset"**, which is where per-tile seam checking
already lives, target **2026-10-17**. Until it lands:

- **`texel-marketing`'s restriction stands.** No beat may claim Check Tiling
  catches seams. `texel.shift_wrap` is untouched by any of this and is still a
  good beat on its own terms.
- The listing tagline says *seamless tiles*, which `shift_wrap` and the tile
  tools deliver honestly. **`check_tileable` must not be sold as a guarantee**,
  and as of Part 1 the add-on no longer describes it as one to the buyer.

**Part 1 is BUILT AND GATED, NOT SHIPPED.** It rides **v0.2.2 on Wed 2026-09-30**.
It is written here as not-shipped on purpose: this file spent eight days claiming
a build was live because a routine ticked ahead of the upload, and that is not
happening twice in the same month. The live 0.2.1 zip still prints the old
string.

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
3. Gate: all **18** suites green, `core/` coverage still 100%, `build.py` clean,
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
6. **Re-read the LOGGED-OUT store page and confirm the new zip is actually on
   it** - filename and byte size off the page's own upload widget, not off a
   dashboard and not off an upload tool's success message.
7. Only then tick the item here, with the date it actually shipped.

> **Steps 6 and 7 were added 2026-09-24, and they are the `build.py` treatment
> applied to the ship step.** `build.py` was taught on 2026-09-16 to fail when a
> module exists but is missing from its list, because a hand-written list goes
> stale; three lines later in that same release, the tick was written by hand
> against an upload that had not happened, and nothing failed. A tick is a claim
> about the outside world, so it needs a reading of the outside world. **A
> routine's own `succeeded` status is not that reading** - the 2026-09-16 run
> exited `succeeded` having skipped its own upload.

**A version ships when its slice is done, not when its date arrives.** Partial
versions are fine and normal — v0.3.0 may ship tile slicing and stamping without
autotile, and the leftover moves to v0.3.1.

---

## Post-mortem: the release that reported itself green and shipped nothing

*Written 2026-09-24 by `texel-release`, because `ACTIONS.md` T-012 asks this
routine to record why a `succeeded` run skipped its own upload rather than to
just do the upload. Both are done.*

**What the 2026-09-16 run did:** built `dist/texel-0.2.1.zip`, bumped both
version declarations, renumbered "Brush, the rest" to v0.2.2, wrote *"SHIPPED
2026-09-16"* and *"v0.1.0, v0.2.0 and v0.2.1 are live"* into this file, and
exited `succeeded`. It did not upload and it did not write a devlog. Eight days
of buyers got the 0.2.0 build.

**Why it could happen, and none of the three reasons is "it forgot":**

1. **Every step of that run reported on itself.** The gate prints its own PASS,
   `build.py` prints its own byte count, the tick is a line this routine writes
   into a file this routine owns. Nothing in the loop read anything the routine
   had not produced. An upload is the only step whose result lives outside the
   process, and it was the only step with no read-back - so skipping it looked
   exactly like doing it.
2. **The tick came before the evidence and was allowed to.** Step 6 said *"tick
   the item here with the date it actually shipped"*, and "actually" was doing
   all the work in that sentence with nothing behind it. It is now steps 6 and 7,
   and the tick is downstream of a logged-out page read.
3. **Nothing between Wednesdays re-reads the store.** `texel-watch` found it on
   09-17, which is the system working, but the owner could not act until 09-23
   at the earliest - and 09-23's run did not happen either. A weekly owner with
   a daily failure mode is a six-day hole by construction.

**And the gate claim was false in two more places than T-012 knew about**, both
found this run by re-running that release's own gate at HEAD:

- `test_features.py` had failed **since the hour it was written** in that same
  commit (`bf2ad7d`, 2026-09-16 22:10). Its check *"all eight sit the same
  distance from the centre"* is unsatisfiable, not unmet: `x^2 + y^2 = 36` has
  only four integer solutions and all four are axial, so no grid point exists at
  radius 6 on a diagonal. Replaced this run with the invariants an integer grid
  genuinely holds - closure under a quarter turn, closure under a diagonal flip,
  and every texel within half a diagonal of its true rotation - each verified to
  FAIL against a truncating implementation before being accepted.
- `core/` coverage was **97.5%, not 100%**: `core/report.py` landed in that
  release at 0% because its suite, `test_report.py`, was never added to the
  coverage loop in this routine's own SKILL.md. Six suites, not five. Fixed.

**The lesson, stated so the next instance is not re-diagnosed:** a gate that
only reads what the run itself wrote cannot fail. Every claim in the release
loop now terminates in something the routine did not author - the live page for
the upload, a deliberately-wrong implementation for the new assertions, and a
coverage number over a suite list that `build.py`-style staleness checking will
eventually have to police too.
