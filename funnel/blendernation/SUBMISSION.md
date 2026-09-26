# BlenderNation submission — mapped, drafted, and HUMAN-blocked

Prepared by `texel-funnel`, **2026-09-19**. `funnel/LOG.md` carried this as
*"Next Friday's job"* and `ACTIONS.md` **T-014** required it to either happen or
be written up as `HUMAN`-blocked with the reason. It is the second.

**Everything a person needs to send this is on this page.** The form is mapped
field by field, the copy is drafted and fact-checked against the live zip, and
the one missing piece (the image) is named with its exact spec.

---

## Why this channel at all — it is not a hunch, it is Texel's own referrer table

From `LEDGER.md` 2026-09-19, **44 of 75 views attributed**:

| source | visits | what it cost us |
|---|---|---|
| `itch.io/tools/new-and-popular` | 9 | nothing — itch's own shelf |
| **`blenderartists.org`** | **8** | **nothing — organic** |
| `duckduckgo.com` | 6 | nothing |
| `itch.io/tools/newest` | 5 | nothing — itch's own shelf |
| **`z3er1n.itch.io/texel-density-cheatsheet`** | **2** | **a full free drop, ~2 days of build** |

**The Blender community already refers four times what our own free drop does,
with zero effort spent on it.** BlenderNation is the same audience, reached
deliberately instead of by accident. That is the argument for spending funnel
effort here, and it is measured rather than assumed.

---

## Why a routine may not send it — three independent blocks, any one is enough

1. **reCAPTCHA is present on the page.** `https://www.google.com/recaptcha/api2/aframe`
   is loaded on `/submit-news/` (read out of the live DOM this run). `SKILL.md`
   §G: *"never solve a CAPTCHA. If any is required, stop and hand off to the
   user."* Hard stop, on its own.
2. **The form requires a real name and email** (`Your name:*`, `Your email:*`).
   Entering personal data into a third-party form is a user decision, not a
   routine's.
3. **It publishes public content** under the user's name — BlenderNation's own
   note: *"If you're logged in while submitting news, the article will be
   published under your name."*

**An account is NOT required** — that was the specific thing `LOG.md` said to go
and check, and the answer is no, login is optional. So this is blocked on
permission and a CAPTCHA, not on a signup.

---

## The form, field by field (read off the live page 2026-09-19)

`https://www.blendernation.com/submit-news/`

| Field | What to put | Note |
|---|---|---|
| I want to send a…* | **Full post** | The form says a full post *"will increase your chances of quick publication by 10000% ;-)"* — a lead alone is the weak option |
| Is your post about a commercial product or service?* | **Yes** | Texel is $9.95. Answering No would be a lie and the listing proves it |
| Your name:* | the user's call | |
| Your email:* | the user's call | |
| Post Title* | see below | Their rule: *"Please refrain from using clickbait-y/sensationalist titles, all-caps etc."* |
| Post Category* | **Development → Add-ons** | |
| Post Image* | **NOT YET BUILT — see the spec below** | required field |
| Post Body* | see below | Rendered as *"(your name) writes:"* followed by the quoted text |

### The image spec, stated exactly because it disqualifies every asset we own

- **1456×672** for retina (or 728×336 — same 2.167∶1 ratio). Other sizes are
  auto-cropped.
- **"We're trying to clean up our homepage and prefer 'clean' images without any
  text or logo overlays on them."**

**That rules out the entire promo library.** Every card in `promo/` is a designed
graphic with type on it — the transform card, the bilinear card, the density
card, the cheatsheet cover. All text overlays. All unusable here.

**And the existing render library does not fit either, for a second reason.**
`store/stills/` holds 57 clean 1280×720 Cycles renders with no text — right kind
of asset, wrong shape (16∶9, would be cropped) and, looked at rather than
assumed, **the wrong content**: `env_corridor_02.png` was opened this run and it
reads as smooth low-poly shading with almost no visible pixel texture. For a
product whose entire pitch is pixel texels on a lit 3D surface, a hero image
that does not show a texel is the weakest possible lead.

**What to build instead:** a purpose-made 1456×672 Cycles render on the
`funnel/density_cheatsheet/render_chip.py` pattern — which already produces a
clean, warmly-lit object with unmistakably chunky texels and passed the §4 loop
at round 4 — widened to the 2.167∶1 frame.

**ATTEMPTED THIS RUN, THREE ROUNDS, NOT PASSED — and it is not presented as
done.** `render_hero.py` exists and runs; the scoreboard:

| round | what changed | result |
|---|---|---|
| 1 | 4.6 m frame, 32 px/unit, ORTHO camera | **Rejected on looking.** A close-up of two boxes; tiles stretched so far the wall read as flat low-poly rectangles, and the floor blew out to near-white. |
| 2 | 7.2 m frame, 48 px/unit, PERSPECTIVE camera, AgX | **Gate failed**, flatness 0.249 against a control of 0.202. A real space with depth, but one tan wash, crates cut by the frame edge, and a visible wallpaper-like tile repeat. |
| 3 | object-space BOX projection, narrower corridor, asymmetric camera, cool light pushed | **Gate failed**, flatness 0.185 — *below* the control. |
| 4 *(2026-09-25)* | 32 px/unit (was 48), 3.6 m corridor, camera 1.15 m from the crates, 30 mm, pixel filter 0.75, darker world | **Gate failed**, flatness **0.241** (needs > 0.263). Texels visibly larger. Kept as `hero_round4.png`. |
| 5 *(2026-09-25)* | pulled back to 28 mm, torch up, near fill down, AgX Medium High Contrast, pixel filter 0.50 | **Gate failed**, flatness **0.210**. The ceiling hotspot blows toward white and the wall edges crush toward black. This is `hero_1456x672.png`. |

**The gate watches the rendered pixels, not the arithmetic**, because a check
aimed at anything except the shipped output reports a number and proves nothing.
It measures the fraction of horizontally adjacent pixel pairs that are exactly
equal — a texel several pixels wide produces runs of identical pixels, a smooth
gradient does not — and compares that against `store/stills/env_corridor_02.png`,
the smooth-shaded render this image exists to beat. Both are denoised Cycles
output, so it is like for like.

**Round 3 scoring BELOW the control is the instrument working, not failing.** Box
projection fixed a real bug — the 9×14 m floor had a single uniform UV scale, so
its tiles were stretched 1.55× in V — but at 48 px/unit across a 7.2 m
perspective frame the texels fall to sub-pixel across most of the image. The
measurement is telling the truth: **at that framing the texels are not the
subject**, which is precisely the defect that disqualified the existing stills.

The fix is a tighter frame at a coarser density, between round 1's mistake and
round 3's. That is a fourth round on an asset for a submission **no routine can
send anyway**, so it was stopped rather than run down the clock. Round 4 is where
this picks up.

---

## Drafted copy — fact-checked against the LIVE zip, not the working tree

**Every claim below was verified by reading `dist/texel-0.2.0.zip`, which is what
`z3er1n.itch.io/texel` actually serves** (confirmed logged-out this run: the page
names `texel-0.2.0.zip, 187 kB`). 95 operators; `texel.density_detect`,
`texel.density_apply`, `texel.palette_load`, `texel.sprite_sheet`,
`texel.anim_bind`, `texel.export_anim_data` and 11 layer operators all present;
`blender_version_min = "4.2.0"`; GPL.

**Nothing below describes v0.2.1**, which is built but not uploaded
(`ACTIONS.md` **T-012**) — so the radial symmetry work and the density-readout
fix are deliberately absent from this copy. Posting a feature that is not in the
uploaded zip is banned by `OPERATIONS.md` §3 and it is the exact trap
`texel-marketing` avoided on 09-16.

### Post Title

> Texel: indexed pixel-art painting and texel density tools inside Blender

### Post Body

> Texel is a Blender add-on for making pixel art where the pixels end up living —
> on the model, at a size you choose, rather than whatever size the UV unwrap
> happened to give you.
>
> It paints an *indexed* canvas onto the image texture bound to your object: one
> palette index per pixel, index 0 transparent. Because the document is indexed
> rather than RGBA, a palette swap and a colour replace are exact operations
> instead of filtered approximations. Layers, groups, cels and an animation
> timeline live in the same document, and a sprite sheet exports with a JSON
> sidecar an engine can read. Palettes load and save as .gpl, so they move
> between Texel, Aseprite, Krita and GIMP.
>
> The part I actually built it for is texel density. Blender's default cube UVs
> give every object roughly the same UV area regardless of how big it is, so a
> 3.2 m wall and a 0.38 m crate sharing one 32 px texture land about 8.4×
> apart in pixels-per-unit — which is why the wall behind a crate so often looks
> mushy next to the crate itself. Texel measures density per face and rescales
> the UV islands to a figure you type in.
>
> Blender 4.2 and up. GPL-3.0-or-later, as a Blender add-on has to be. It's
> $9.95 on itch.
>
> Some of the work on Texel, code and art both, was done with AI assistance.

**Notes on the draft, so a later run does not "improve" it into a breach:**

- The **8.4×** figure is measured, not rhetorical — `texel.density_detect` read
  2.5–21.1 px/unit across 18 faces on the two-object scene, and the density card
  on the live listing is built from the same numbers by `make_density.py`, which
  asserts the ratio so the card fails to build if it stops holding.
- The AI-assistance line is **one sentence**. BlenderNation does not ask, but
  disclosing where it is material is the house rule; the standing rule is that a
  prose disclosure is one sentence and never a paragraph defending the pipeline.
- **No comparison to any other add-on appears anywhere in this copy**, and none
  may be added. Texel is not framed as competing with or derived from anything —
  standing rule, `promo/POSTED.md`.
- "$9.95" and "Blender 4.2 and up" are both read off the live listing and the
  live manifest respectively. If either changes, this draft is stale.

---

### 2026-09-25 — THE 5-ROUND CAP IS REACHED, NOT PASSED. Do not send this image as it stands.

`texel-funnel` spent the two unspent rounds, as `ACTIONS.md` T-017 asked. **Both
failed the flatness gate, so the image fails §4 and is not presented as done.**
The render is on disk for the user to look at, and the call is the user's.

**`design-critic` on both renders (2026-09-25): ITERATE for both.** It judged
round 4 the stronger one, because its flatter light keeps the texel edges readable
across more of the frame. Findings still open:

- **SERIOUS (both): there is no subject.** A brick corridor corner with three
  crates reads as a generic Minecraft-style test scene. Nothing shows what the
  add-on is for: hand-painted texel detail on an asset.
- **SERIOUS (both): the black banner with a red sliver looks like a missing texture.**
  To Blender users it reads as a render error. Take it out, or light it so its
  texels show.
- **SERIOUS (both): the composition is close to dead-centre on the wall corner.**
- **FATAL for round 5: the ceiling hotspot washes out the texel banding** at both
  ends of the frame. That is the one thing the image has to sell, and it also
  explains why round 5 scored below round 4.
- **MINOR (round 4): the ceiling is cropped,** so the space reads as a shallow box.

**The critic also judged the instrument, and the finding is recorded, not acted on.**
Exact-equality adjacency on a denoised Cycles render is *"close to unreachable
inside any texel's interior once GI, soft shadows and denoising add sub-pixel
gradients"*. The smooth control scores 0.202. Rounds that visibly carry
several-pixel texels score only 0.21–0.24, so the metric has almost no headroom.
The critic's proposed replacement is a **block-uniformity ratio**: quantise each
texel cell, then compare the gradient *between* cells (it should be a hard step)
against the variance *within* a cell (it should be small). **This run did not swap
the gate.** Changing the instrument on the day it failed, to make it pass, is the
exact move §4's cap exists to stop. The swap goes to the next attempt as a proposal,
with its own control, and is judged before any render is scored against it.

**What the next attempt needs, in order:** (1) a real subject, meaning one
hand-painted hero prop in the foreground with the corridor as context; (2) the
banner gone; (3) off-axis framing; (4) the gate question settled first. **None of
this matters unless T-016 comes back yes.** Nobody can send the submission without
the user, so no further rounds get spent until the user answers.

## What would make this sendable

1. The **1456×672 clean texel render** exists and has been looked at.
2. **T-012 is cleared** — ideally the page serves the current build before a new
   audience arrives on it. This is a *preference*, not a block: 0.2.0 is a
   working, honestly-described product and holding a free channel hostage to
   another routine's unshipped zip would be letting its failure freeze this one.
3. **The user sends it**, because of the three blocks above.
