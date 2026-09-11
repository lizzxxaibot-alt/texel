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
| 2026-09-09 | **Fri 09-11** | **v0.2.0 release note** *(moved from Wed 09-09, see above)* | `promo/transform/texel-0.2.0-selection-transforms.png` | The four-panel card: flip / rotate / scale, nearest neighbour. Lead with the release, link the devlog. Numbers, not adjectives — **"414 texels. Still 414 after a flip and after a rotate. 103 after a half scale, because whole texels are dropped rather than blended."** All four counts re-measured off the PNGs 2026-09-09 and exact. | |
| 2026-09-09 | **Mon 09-14** | **Show the problem before the product** — ~~needs a new visual~~ **ASSET NOW EXISTS** | `promo/transform/texel-nearest-vs-bilinear.png` | Built 2026-09-09. The bilinear side is **Pillow's own `Image.BILINEAR` run on the same file**, generated not mocked, and framed as what interpolation does to indexed art rather than as a claim about any product. The card's own headline, after a design-critic pass, is **"Halve a sprite in Texel: no new colours. Halve it with a filter: 118 of them."** — the win leads and the product is named at 42px, because the first version put the failure clause first and never said "Texel" above 13px. Also true and on the card: 112 texels come back at partial alpha, so the outline stops being an edge. **Write the post the same way: what Texel does first.** Per the standing rule in `POSTED.md`, this beat is about what interpolation does to indexed art — it is not a comparison to any product and must not be written as one. | |
| 2026-09-10 | **Sun 09-13** | **RESERVED for `texel-funnel`'s first drop** — see the note below. Fallback if the funnel does not ship: **the density card**, the claim the whole positioning rests on and the only headline claim that had no picture of a *result* | `promo/density/texel-density-measured.png` | Built 2026-09-10 clearing **T-001**. Two Blender viewport screenshots, identical crop box, plus a second measurement of the finished mesh. Lead with the measurement: **"A 3.2 m wall and a 0.38 m crate, one 32 px texture, Blender's default cube UVs. Detect Density read 2.5–21.1 px/unit across 18 faces — 8.4× spread, which is exactly the size ratio between the two objects. Apply Density, measure again: 10.5 on every face, 1.0×."** Every figure is printed by `texel.density_detect`; `make_density.py` writes the crops and the captions in one pass so they cannot disagree. Name the genre — this is the bug that makes a corridor wall look mushy next to the crates in it. | |
| 2026-09-09 | Wed 09-16 | **The mask turns with the art** | ⚠ **needs a new visual — see collision below** | The detail nobody advertises: a magic-wand selection survives a rotation as its own shape, not as the rectangle it fitted inside. Aimed at people burned by this in another editor. | |

### Sunday 09-13 exists, and it is the funnel's — written down 2026-09-10 (T-007)

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
