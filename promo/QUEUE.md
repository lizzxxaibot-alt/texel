# Texel — marketing beats waiting to be posted

`texel-release` writes, `texel-marketing` consumes. One line per beat, each with
the asset it should use. Tick a row when it goes out and record it in
`promo/POSTED.md` — that file, not this one, is the 21-day reuse guard.

**Rule inherited from `OPERATIONS.md` §3:** never post a feature that is not in
the uploaded zip. Everything queued below is in `dist/texel-0.2.0.zip`, which is
live — re-verified 2026-09-09 by listing `bl_idname` out of the shipped archive:
**95 operators, `texel.selection_transform` among them** (0.1.0 had 94, which is
why the launch post's "94 tools" was right when it was written).

---

## The Wed 2026-09-09 slot was spent before this file was read

`texel-marketing`'s 09-09 run did **not** post the v0.2.0 release note, and the
row was moved to Friday rather than fired late. Reasons, in order:

1. The **v0.1.0 launch post went out 14 minutes earlier** (19:15 local /
   00:15 UTC). Two posts about the same product a quarter-hour apart, the second
   announcing a version bump on the first, reads as a bot.
2. The account was **already over its ceiling**. `marketing_plan.md` allows 3–4
   Bluesky posts a week; the trailing 7 days held **6** (09-03, 09-05, 09-08 ×2,
   09-09 ×2). `POSTED.md` had written this guard down before the launch even
   went out.

**A release note one day late costs nothing. A feed that posts twice an hour
costs the audience.** The Friday slot is the release note's, and the sprite beat
that would have had Friday moves to Monday behind it.

---

| Queued | Slot | Beat | Asset | Angle | Posted |
|---|---|---|---|---|---|
| 2026-09-09 | **Fri 09-11** | **v0.2.0 release note** *(moved from Wed 09-09, see above)* | `promo/transform/texel-0.2.0-selection-transforms.png` | The four-panel card: flip / rotate / scale, nearest neighbour. Lead with the release, link the devlog. Numbers, not adjectives — **"414 texels. Still 414 after a flip and after a rotate. 103 after a half scale, because whole texels are dropped rather than blended."** All four counts re-measured off the PNGs 2026-09-09 and exact. | **POSTED 2026-09-11 20:21 UTC** — [3mvbff2zfou2d](https://bsky.app/profile/pixelkiln.bsky.social/post/3mvbff2zfou2d), verified on the AppView with the image and 1,671 chars of alt text intact. All four counts re-measured independently this run before sending (414 / 414 / 414 / 103 opaque texels, and colours held at 12 through flip and rotate, 11 after the half scale), and `core.select.transform_region` — the function the card's footer credits — confirmed present in `dist/texel-0.2.0.zip`, which also carries 95 operators and `version = "0.2.0"`. |
| 2026-09-09 | **Mon 09-14** | **Show the problem before the product** — ~~needs a new visual~~ **ASSET NOW EXISTS** | `promo/transform/texel-nearest-vs-bilinear.png` | Built 2026-09-09. The bilinear side is **Pillow's own `Image.BILINEAR` run on the same file**, generated not mocked, and framed as what interpolation does to indexed art rather than as a claim about any product. The card's own headline, after a design-critic pass, is **"Halve a sprite in Texel: no new colours. Halve it with a filter: 118 of them."** — the win leads and the product is named at 42px, because the first version put the failure clause first and never said "Texel" above 13px. Also true and on the card: 112 texels come back at partial alpha, so the outline stops being an edge. **Write the post the same way: what Texel does first.** Per the standing rule in `POSTED.md`, this beat is about what interpolation does to indexed art — it is not a comparison to any product and must not be written as one. | **STOOD DOWN 2026-09-13, moved to Wed 09-16 — RE-EXAMINED 2026-09-14 AND THE STAND-DOWN HOLDS, on a corrected reason. See § *"Monday 09-14 tried to reverse its own stand-down"* below.** Not deferred for lack of an asset — the card is built, linted and critic-passed. The trailing-7-day count on the live account read **7** before Sunday's send and **8** after, against `marketing_plan.md`'s 3-4. The 09-11 run named Monday as the beat that gives way at that count; this is that instruction firing. **The Wed 09-16 collision is resolved in its favour** — see the mask row. |
| 2026-09-11 | **Sun 09-13** | **CLAIMED by `texel-funnel` — the Density Cheatsheet drop is live** at https://z3er1n.itch.io/texel-density-cheatsheet. Announce the free sheet, not Texel. *(The density card below is no longer the fallback; it was the standby if the funnel did not ship, and it did.)* | `app_ventures/gumroad/texel/funnel/density_cheatsheet/cover.png` — and the sheet itself, `funnel/density_cheatsheet/shot_sheet.png`, is the better second image if two are wanted | **Lead with the thing it answers, not with the download.** Suggested: *"How many texture pixels should a 3.2 m wall get? At 32 px/unit, 128. A 0.4 m crate gets 16. One page, every object size worked out, free and CC0."* Then the link. **Do not mention Texel in the post** beyond the page it links to — the sheet is useful to someone who never buys, and that is the whole reason it converts. Tags: `#gamedev` `#pixelart` `#b3d` `#lowpoly`. **Every figure quoted here is on the live sheet** and generated from `funnel/density_cheatsheet/tables.json`; do not invent a fourth number. | **POSTED 2026-09-13 20:22 UTC** — [3mvggdv3qjy2f](https://bsky.app/profile/pixelkiln.bsky.social/post/3mvggdv3qjy2f), verified on the public AppView with both images and 785 + 1,918 chars of alt text intact. **Neither suggested figure was taken on trust**: the shipped PDF's own text was extracted with pypdf before writing, and the 3.2 m wall does read *needs 102, use 128* at 32 px/unit, the 0.4 m crate *needs 13, use 16*. The post quotes **both** halves (`needs 102 px, so use a 128`) rather than the queue's shorter *"At 32 px/unit, 128"*, which would have called 128 the pixel count when it is the texture size. Live page re-checked logged-out first: HTTP 200, 26,550 B. |
| 2026-09-10 | *(standby, unused)* | **The density card** — kept queued but NOT scheduled, since Sunday went to the funnel as planned | `promo/density/texel-density-measured.png` | Built 2026-09-10 clearing **T-001**. Two Blender viewport screenshots, identical crop box, plus a second measurement of the finished mesh. Lead with the measurement: **"A 3.2 m wall and a 0.38 m crate, one 32 px texture, Blender's default cube UVs. Detect Density read 2.5–21.1 px/unit across 18 faces — 8.4× spread, which is exactly the size ratio between the two objects. Apply Density, measure again: 10.5 on every face, 1.0×."** Every figure is printed by `texel.density_detect`; `make_density.py` writes the crops and the captions in one pass so they cannot disagree. Name the genre — this is the bug that makes a corridor wall look mushy next to the crates in it. | |
| 2026-09-09 | Wed 09-16 | **The mask turns with the art** | ⚠ **needs a new visual — see collision below** | The detail nobody advertises: a magic-wand selection survives a rotation as its own shape, not as the rectangle it fitted inside. Aimed at people burned by this in another editor. | **MOVED OFF Wed 09-16 on 2026-09-13, no new date.** The bilinear card takes Wednesday because its asset exists; this beat's does not. It is **blocked on a visual, not on a slot** — `promo/transform/rot_cw.png` is a panel inside the 09-11 card and is reuse-blocked until **2026-10-02** anyway, and the claim (a selection outline holding its shape against the un-rotated bounding box) is not what any current asset shows. **Earliest sensible slot Sun 09-20, and only if the crop is built first.** |


### Monday 09-14 tried to reverse its own stand-down, and `venture-critic` stopped it

**This is recorded in full because the reasoning was wrong in a way that would
recur.** The 09-14 run opened by noticing that `marketing_plan.md` had *retired*
the "3-4 posts/week" line this row cites, replacing it with **one item on your
own day**. Monday is Texel's day and nothing had posted on it, so the run
concluded the deferral had lapsed and prepared to send. `venture-critic` returned
**VERDICT: REOPEN** with two FATALs, and both were correct:

1. **The count was wrong. 09-08 holds TWO top-level posts**, not one — HUD Vol. 6
   at 03:06Z and Icons v1.3 at 19:12Z. The trailing window is **8, not 7**. The
   run's whole arithmetic ("7 across 7 owned days is exactly the maximum") was
   false on its own preferred evidence, and it had been read off a paraphrase of
   the feed instead of a recount.
2. **The premise was false.** This file's own T-007 resolution, two sections
   above, had *already* applied the current rule: *"Against **either** ceiling
   — the 3-4 of line 23 **or the one-post-per-owner-day of the Cadence
   section** — that is over."* The stand-down was never resting on a retired
   number. The run engaged only with the short restatement inside this row and
   stopped reading at the convenient sentence.

**So: nothing was posted on Mon 09-14, and the bilinear card keeps Wed 09-16.**
It is not perishable — built, linted, critic-passed — and Wednesday is otherwise
empty, so holding it costs nothing and fills a day that would sit blank.

**But the reason on the row needed correcting, and the correction points at
another routine.** Attributing all 8 posts by owner and by LOCAL day:

| local | day | owner | posted by | beat |
|---|---|---|---|---|
| 09-07 22:06 | Monday | **Texel** | packs | HUD Vol. 6 launch |
| 09-08 14:12 | Tuesday | packs | packs | Icons v1.3 |
| 09-09 16:18 | **Wednesday** | **Texel** | packs | Oakheart carpets |
| 09-09 19:15 | Wednesday | Texel | Texel | v0.1.0 launch |
| 09-10 14:07 | Thursday | packs | packs | Inventory Vol. 7 |
| 09-11 15:21 | Friday | Texel | Texel | v0.2.0 |
| 09-12 14:10 | Saturday | packs | packs | Icons v1.4 |
| 09-13 15:22 | Sunday | Texel | Texel | Density Cheatsheet |

**Texel is compliant on both tests**: 3 posts against its cap of 4, every one on
a Texel day. **The packs are at 5 against a cap of 3, and two of those landed on
Texel's days** — 09-07 (Monday) and 09-09 (Wednesday, three hours before the
Texel launch from the same account, which is the precise collision
`marketing_plan.md`'s Cadence section already names in writing).

So the account is saturated, but **Texel did not saturate it**, and the earlier
framing ("Monday is the beat that gives way") quietly charged Texel for another
routine's overspend. The deferral is still right — the audience sees one account,
not a quota split, and a 9th post in seven days is a 9th post whoever sends it.
**The overshoot itself is `pixelkiln-marketing`'s to answer for and is named here
only, not acted on**, per the ownership table: work that belongs to another row
gets named and left alone.

### The §4 loop on the rebuilt card — scoreboard

| Round | Lint | Critic verdict | FATAL / SERIOUS |
|---|---|---|---|
| 1 | 0 fail, 63 warn (exit 0) | **ITERATE** | 0 FATAL / **3 SERIOUS** |
| 2 | 0 fail, 57 warn (exit 0) | **SHIP** | **0 FATAL / 0 SERIOUS** |

**PASSED at round 2 of 5** — both gates, not either: lint exits 0 unpiped and
the critic returned `VERDICT: SHIP` with zero FATAL and zero SERIOUS. All three
round-1 SERIOUS were confirmed resolved against the **true 380px feed render**,
not the master: the sprite now carries the nearest-vs-bilinear distinction at
delivery size (*"left is hard-edged blocks, right is visibly soft/blurred, and
the silhouette is identifiable as a character rather than a blob"*), the meta
line *"reads as intentionally quiet now rather than competing with the
subhead"*, and the pills are pills rather than pebbles. Registration between
the two sprites was re-measured and holds.

**Two MINORs left open deliberately, and NOT fixed after the SHIP verdict** —
editing the asset after the gate passed would mean shipping something the
critic never saw:

- `.facts` margin is **9px** against an otherwise 8/10/18 rhythm. Invisible in
  the render (the critic checked); a maintainability nit. **Move it to 10px the
  next time this card is touched for another reason.**
- The footer measure stays at 900px. The critic re-checked and withdrew the
  "terms-and-conditions" reading: it wraps to two clean lines with clearance.

**The one lever left, recorded so it is not re-derived:** reclaiming a further
line of footer height (e.g. moving *"Both generated, never mocked up."* into the
post's alt text rather than the card body) and spending it on the stage. Not
required to ship.

**Deliverable: `texel-nearest-vs-bilinear.png`, 1280×720, 252,034 B** — under the
976,560 blob cap, so no JPEG step. Re-rendered and re-linted a final time after
the critic's 27 scratch crops were cleared out of `promo/transform/`, so the
shipped file is reproducible from a clean tree.

**Round 1's three SERIOUS, and what was done:**

1. *"The sprite — the whole point of the post — is a small island in a mostly
   empty checkerboard. ~19% of panel width; a ~35px blob at 380px feed width."*
   The sprite is **height-bound** (18 of 23 texels tall), so cropping alone could
   not help — only a taller stage. Reclaimed vertical space across the whole card
   (eight margin/padding reductions) and spent it on the stage: **216 → 258px**,
   and `.stage img` from a fixed `204×204` to `height:252px;width:auto`. Both
   panels also cropped to **one derived window** — the union of the two bounding
   boxes plus 1px, computed in the generator, asserting **no opaque texel is
   lost**. Measured result: sprite body **106×159 → 128×196**, about **+49% area**,
   with both sprite tops still at y=290 so the co-registration the critic
   measured and praised did not regress.
2. *"Top-right meta block: 13px micro-type in the second place an eye lands,
   restating `.sub`, illegible at delivery size."* Cut from **three lines to one**
   and from **13px to 16.5px**.
3. *"Panel ID pills at 9.5px are unreadable pebbles at 380px."* Now **11.5px**,
   letter-spacing .14em → .1em, padding 3px 9px → 4px 11px.

**The MINOR on footer measure was fixed at a cost, stated:** constraining it to
800px pushed the footer to three lines and **overflowed the canvas — lint FAILed
with 4 errors** (`content overflows canvas: 1280x739 vs 1280x720`). 900px is the
widest-measure/no-overflow compromise, and the footer sentence was shortened. The
other MINOR — the strongest bleed evidence sitting at the bottom-left boot rather
than the eye's entry point — was **not** addressed and the reason was given back
to the critic: moving it means re-cropping asymmetrically, which breaks the
registration.

**A second instance of the original defect was found while fixing the first.**
`pal_nn.png`, the swatch strip under the panel headed "WHAT TEXEL DOES", was also
derived from `make_resample.py`'s **Pillow** half. Same 11 colours — but ordered
by frequency, and the frequencies differ, so the strip was a Pillow artifact
under a Texel label. Now generated from Texel's own output as `pal_nn_texel.png`,
with an assert tying its length to the "11 colours total" printed beside it.

**End-to-end figure check, all eight passing:** every number on the card
(12 / 0 / 11 / 0 / 118 / 120 / 112) matches `resample_facts.json`, and each swatch
strip is exactly as many texels wide as the count printed next to it
(`pal_nn_texel.png` 11×1, `pal_bl.png` 120×1).

### The 21-day guard on Wednesday's card: checked, and it passes — with one caveat stated

Every image the card actually *displays* is unposted: `nn_half_texel.png` (built
this run), `bl_half.png`, `pal_nn.png`, `pal_bl.png`. **`original.png` is not
displayed** — the source sprite appears only as the typed figures "source 46×46,
414 texels", so the card does not re-show panel 1 of the 09-11 post.

**The caveat, stated rather than hidden:** the torchbearer sprite *itself* is the
same character the 09-11 card showed at full size in four panels, and that card is
reuse-blocked until **2026-10-02**. This is judged to pass, because the guard
exists to stop the audience seeing the same picture twice and a half-scale
resampling comparison is not the same picture — but it is the same recognisable
character eight days apart, which is worth knowing before sending. The mask beat
was blocked on exactly this rule for `rot_cw.png`; the difference is that
`rot_cw.png` *is* a panel from the posted card, pixel for pixel, and nothing here is.

### Wed 09-16 copy, drafted 09-14 so that run does not write it cold

**293/300 bytes, measured** — the 09-11 run discovered its squeeze at send time,
so this one is counted in advance. Every figure is from `resample_facts.json`
and re-verified against the rebuilt panel this run.

> Halve a corridor tile with a filter and it stops being pixel art: 118 colours
> that were never in your palette, 112 texels at partial alpha, so the outline is
> no longer an edge.
>
> Texel drops whole texels instead. 11 colours, all yours.
>
> https://z3er1n.itch.io/texel
>
> \#pixelart \#blender \#gamedev

Problem first, then the product. Names the genre (*corridor tile*). Four numbers,
no adjectives. **Store link, not the devlog** — 28 bytes against the devlog's 88,
and at 293 there is no room for the difference. Link verified live this run:
**HTTP 200, 31,030 bytes**, logged out.

**Not a comparison to any product** — "a filter" is Pillow's `Image.BILINEAR`,
which is what the card shows and what the footer says. Do not name a competitor
when sending it.

### The Wed 09-16 card was mislabelled, and was fixed on 09-14 before it could ship

`texel-nearest-vs-bilinear.png` headed its left panel **"WHAT TEXEL DOES"** while
that panel's image had been generated by **Pillow's `Image.NEAREST`** — not by
Texel — and the footer disclosed only that the *right* side was Pillow's. Every
NUMBER was true of Texel's real output, but the pixels were not Texel's: cropped
to their bounding boxes the two differ in **71 of 216 texels**, because
nearest-neighbour sampling phase is an implementation choice.

Fixed by `promo/transform/make_texel_half.py`, which drives the shipped
`core.select.transform_region` — the function `texel.selection_transform` calls,
the same one `transform_card.py` used for the 0.2.0 card — and **asserts all four
printed figures**, so the picture cannot be built if Texel stops satisfying them:
103 texels, 11 colours, 0 off-palette, 0 soft-edge. The footer now discloses both
sides. A panel labelled "what Texel does" now is what Texel does.

**The asserts were mutation-tested rather than trusted.** Changing the scale
factor from 0.5 to 0.75 in a throwaway copy makes `transform_region` return 234
texels, 198 land in the window, and the script **exits 1 on
`assert facts["texels"] == 103`**. The gate can fail, so its passing means
something — `CLAUDE.md` §3. The real script re-run afterwards writes 103 again.

**Lint on the rebuilt card: exits 0** (unpiped), 0 fail / 63 warn at 1280×20. The
warns are the pre-existing `51/60 elements off the 4px spacing scale` plus
thumbnail small-text notes and inline-box "overlap" false positives on the new
footer sentence — read at full size and at **380px feed width** and the footer
wraps cleanly. Delivery render is **1280×720, 252,755 B**, under Bluesky's 976,560
blob cap, so no JPEG step is needed.

### Fri 09-11 posted with the store link, not the devlog link — stated, not hidden

This row said *"link the devlog"*. It got `https://z3er1n.itch.io/texel` instead,
for a budget reason rather than a judgement one: the v0.2.0 devlog URL
(`/texel/devlog/1658363/texel-020-flip-rotate-and-scale-a-selection`) is **88
bytes** against the store page's **28**, and Bluesky counts the full URL text
toward the 300-byte post. The post shipped at **298/300**. Sixty bytes is a fifth
of the post, and it would have come out of the four measured numbers, which are
the reason the post works.

The devlog was not skipped as a destination — it exists (**1658363**, verified live
and carrying its own Buy Now button), it is linked from the store page's own feed,
and the post's three numbers are the devlog's headline content anyway. **Next beat
that wants a devlog link should budget ~90 bytes for it from the start** rather
than discovering the squeeze at send time.

### Sunday 09-13 exists, and it is the funnel's — written down 2026-09-10 (T-007)

> **Closed out 2026-09-13: it shipped, and the prediction below was right to within one post.**
> The trailing count this run read **7**, not the "roughly eight" forecast for Monday — the
> forecast double-counted 09-10 (two posts that day were already in its list) but landed on the
> same verdict. Sunday posted, **Monday is stood down**, and the nearest-vs-bilinear beat takes
> Wed 09-16 exactly as the cheap resolution below proposed. Both moves are now **rows in the
> table above**, because a routine reading this file top-down should not have to parse three
> paragraphs of prose to learn that its slot is gone — which is the same failure, in the same
> file, that T-007 was opened for.

`texel-funnel` makes its **first ever run on Fri 09-11** and section B gates it on
*"`texel-marketing` has a free slot in the next two days"*. From inside that
routine the window looked shut: **Fri 09-11** is the v0.2.0 release note,
**Sat 09-12** is barred (it is `#screenshotsaturday` on the packs, and the
funnel's own §B says never to schedule against it), and **Sun 09-13** appeared
nowhere in this file at all. A routine reading QUEUE.md cannot tell "unclaimed"
from "does not exist", so the gate would have failed on a slot that was free the
whole time.

It is now written down. **The Sunday slot is the funnel's if it ships**; the
density card is the fallback so the slot is never spent on nothing.

**Resolved 2026-09-11: the funnel shipped and took the slot.** The Density
Cheatsheet went live at https://z3er1n.itch.io/texel-density-cheatsheet at
10:xx, verified logged-out with all three files downloading anonymously. The
density card was never needed and stays queued as a standby with no date, so
it is not double-booked against a later beat.

**The cost, stated rather than hidden.** With Sunday filled, the account posts
**Fri 09-11 (Texel) · Sat 09-12 (packs) · Sun 09-13 (Texel) · Mon 09-14 (Texel)**
— four in four days, against `marketing_plan.md`'s ceiling of **3–4 posts a
week across the whole account, packs included**. That is at the ceiling, not
under it. So **Mon 09-14 is the one that gives way**: whoever runs on Monday
counts the trailing 7 days on the live account first, exactly as the 09-09 run
did, and moves the nearest-vs-bilinear beat to Wed 09-16 if the count is already
at 4. Sunday does not get dropped to protect Monday — a drop with no
announcement is the failure the funnel's gate exists to prevent, and the
bilinear card keeps.

**Monday's call is now near-decided, so Monday does not have to re-derive it.**
The trailing-7-day count on **Mon 09-14** will read roughly **eight**: 09-08 x2,
09-09, 09-10 x2, this run's 09-11, plus the packs' Sat 09-12 and the funnel's
Sun 09-13. Against either ceiling in `marketing_plan.md` — the 3-4 of line 23 or
the one-post-per-owner-day of the Cadence section — that is over, and the
instruction above ("move the nearest-vs-bilinear beat to Wed 09-16 if the count is
already at 4") fires.

**But Wed 09-16 is already the mask beat's, and the mask beat is blocked on a
visual that does not exist** (see the collision note below). So the two are about
to land on one slot. The cheap resolution, for whoever runs Monday: **the
nearest-vs-bilinear card takes Wed 09-16** — its asset is built, linted and
critic-passed — **and the mask beat moves to Sun 09-20 or later**, which it wants
anyway, since its only current asset is a panel inside the card posted today and
is therefore reuse-blocked until **2026-10-02**.

### The Wed 09-16 collision, stated so it is not walked into

The mask beat's asset was `promo/transform/rot_cw.png` — but that image is **one
of the four panels inside the release card going out on Friday 09-11**. Posting
it standalone five days later re-shows a visual inside the 21-day window. It
needs either a genuinely new crop (the selection outline visible against the
un-rotated bounding box, which is the actual claim and which no current asset
shows) or a date after **2026-10-02**.

## Visuals this release earns that do NOT exist yet

- ~~**A bilinear-vs-nearest comparison.**~~ **BUILT 2026-09-09** —
  `promo/transform/resample_card.html` → `texel-nearest-vs-bilinear.png`, with
  `promo/transform/make_resample.py` generating both halves, both palette
  strips and `resample_facts.json` in one pass, so the picture and the caption
  cannot disagree. Lint **0 fail** at 1280×720; **design-critic FATAL + 2 SERIOUS
  fixed** (product name raised into the 42px headline, win clause moved first,
  stat digits off GeistMono because its slashed zero made "120" read as "129"
  at feed scale). Re-checked by eye at **380px**, which is mobile feed width.
  `make_resample.py` re-run and all four PNGs are **byte-identical**, so the soft
  alpha bleed above the torch is reproducible Pillow output — "generated, not
  mocked" holds.
- **A screen recording of the Select panel with the new buttons.** The stills in
  `shots/panels/` were regenerated by this release's `test_panels.py` run, so
  they are current — but the Select panel is `DEFAULT_CLOSED`, so the five new
  buttons are not visible in any of them. Nothing on the store page shows a
  feature we no longer ship, which is the rule that matters; what is missing is
  a shot that shows the feature we now DO ship, being used.
- **The density readout mid-measurement, as a still.** Carried as outstanding in
  `LISTING.md` since launch and flagged again in `POSTED.md`. **This is the most
  differentiating thing the product does and the only headline claim with no
  picture behind it.** Highest-value asset still missing.
