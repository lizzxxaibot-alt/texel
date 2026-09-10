# BlenderArtists release thread — Texel v0.2 (DRAFT, not posted)

**Status:** awaiting user approval to post. Nothing has been published.

## Where it goes and the rules it must obey

Verified 2026-09-09 against BlenderArtists' own self-promotion policy
(`blenderartists.org/t/new-policy-on-self-promotion/1416473`):

- **Category: Resources → Released Scripts and Themes.** A paid product link
  belongs there and nowhere else.
- **One self-promotion post per week**, averaged over a rolling 30 days.
- **Replies to your own promo thread count toward that limit.** So answering
  three questions in the thread spends the week's budget. Answer genuine
  technical questions — that is community engagement, and the policy explicitly
  softens for people with real involvement — but do not bump.
- Posts over the limit get deleted.

**r/blender is NOT cleared.** Reddit is blocked from this environment, so its
rules could not be read. Do not post there until someone verifies the
self-promotion rule and whether a "Paid Product/Service Promotion" flair is
mandatory. A third-party analysis site claimed the flair is required; that is
not the platform's own documentation and does not meet CLAUDE.md §5.

---

## Title

`Texel — pixel art painted straight onto your models, and animated [$9.95]`

## Body

Pixel art that looks right in Aseprite goes wrong the moment it lands on a mesh,
and it is usually not the drawing.

**The pixel size drifts across the model.** A crate at 32 px/unit sitting next
to a wall at 19 px/unit reads as two different games glued together. You cannot
see it in the UV editor, and you cannot unsee it in the render.

**Shallow diagonals come out as staircases.** Freehand one in a normal paint
tool and you get L-shaped double-texels down the whole line — the exact artefact
pixel artists spend their lives cleaning up by hand.

Texel fixes both inside Blender, with no round trip to a 2D editor. Then it
keeps going and animates the sprites too — frames and tracks, like cel
animation, with sheet + JSON export.

**What's in it**

- 95 operators, each with a sidebar button; nine are on keys
- Texel-density tools so the pixel size stays consistent across the model
- Seamless tiling, and a paint mode that does not produce staircase artefacts
- Cel-style frame/track animation, exported as sprite sheets plus JSON
- Palette I/O that talks to the rest of your pipeline: load `.gpl`, `.hex` or
  plain hex lists, save back to `.gpl` for Aseprite, Krita or GIMP, and lift a
  palette out of any image

**Honest compatibility**

Built and tested on **Windows**, against **Blender 4.2.23, 4.5.9 and 5.2.1**,
plus the Microsoft Store 5.2.1 build. The test suite — 16 suites, including one
that invokes all 95 operators in a real GUI and fails if any goes uncalled —
runs green on all three. There are no Windows-specific calls in it except
looking for ffmpeg, so it should run on macOS and Linux, but **I have not tested
it there and will not claim I have.** If you are on either and it breaks, tell
me and I will fix it.

**Licence** — GPL-3.0, and the source ships inside the zip. Any Blender add-on
using `bpy` has to be GPL; that is Blender's licence, not a choice I made, and
it means you can read and modify everything you get.

**Updates** — free forever to anyone who has ever bought it. No pro tier, no
subscription. The price does rise at named milestones, announced ahead of time:
$14.95 at v0.4, $19.95 at v1.0. Buying now is the cheapest it will ever be, and
you still get every later version.

**$9.95 — <ITCH_URL>**

Written with AI assistance, including the code and some of the artwork.

Happy to answer technical questions in the thread.

---

## Pre-post checklist

- [ ] **itch payouts configured on the `z3er1n` account** — without this a sale
      cannot pay out, and driving traffic to a page that cannot take money is
      worse than not posting
- [ ] Substitute the real listing URL for `<ITCH_URL>`
- [ ] Confirm the current version number in the post matches what is live
- [ ] Posting in **Resources → Released Scripts and Themes**, not General
- [ ] No other Mintworks self-promo post on BlenderArtists in the last 7 days
- [ ] User has approved the text

## Notes on the copy

The AI disclosure is one sentence, per the standing rule — a paragraph
justifying the pipeline reads defensively and invites the argument rather than
settling it.

The macOS/Linux paragraph deliberately refuses to claim tested support (§6).
Claiming it and being wrong on a $9.95 tool costs a refund and a public reply
saying so, which is worth far more than the sale.
