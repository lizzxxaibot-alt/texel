# Texel — what has been posted, and with which visual

Owned by `texel-marketing`. **This is the 21-day reuse guard**: no visual in the
table below may appear in another Texel post until the "reusable from" date.
Texel's Bluesky days are **Mon / Wed / Fri / Sun** (packs keep Tue / Thu / Sat),
against `marketing_plan.md`'s ceiling of 3-4 posts a week across the whole
account, packs included.

*Corrected 2026-09-10: this line read "Mon / Wed / Fri / Sat (packs keep
Tue/Thu/Sun)", which is the pre-2026-09-09 calendar. **Saturday is the packs'** —
`pixelkiln/launch/marketing_plan.md` claims it for `#screenshotsaturday`, that
plan predates the Texel split, and `pixelkiln-watch` run 8 gave Saturday back and
moved Texel to Sunday. Both routines post to the same account and neither can see
the other from inside, which is exactly how the collision happened the first
time; a stale calendar sitting inside the reuse guard is how it happens again.*

Created 2026-09-09 by `texel-support`, out of its normal lane, because the user
asked for the launch devlog and the launch post directly. The beats below were
**not** taken from `promo/QUEUE.md` (which did not exist yet at the time) — so if
`texel-release` later queues a launch beat, it is already spent. *(QUEUE.md
exists as of 2026-09-09 and is the source from here on.)*

## BlenderArtists — a NEW surface, with its own budget (2026-09-10)

Posted to **Resources → Released Add-ons and Extensions** (category 50 — the
category was renamed from "Released Scripts and Themes", the old name still
resolves). Account: `texel`.

**Its rules, read before posting and verified on the site itself:**

- **One self-promotion post per week**, averaged over a rolling 30 days.
- **Replies to your own promo thread count toward that limit.** Answering three
  technical questions in the thread spends the week. The policy explicitly
  softens for people with genuine community involvement, so answering real
  questions is right — bumping is not.
- Over the limit gets deleted.
- The category **requires a tag from the "Free or Commercial" group**. The tags
  are literally **`free`** and **`commercial`** — there is no `paid` tag, despite
  the category blurb reading "free or paid" in some places. Texel is tagged
  `commercial`.

**This budget is separate from the Bluesky ceiling** in `marketing_plan.md` —
different surface, different audience, different counter. Next BlenderArtists
self-promo slot is **2026-09-17** at the earliest.

**Not posted, and deliberately: r/blender.** Reddit is blocked from the
environment these routines run in, so its self-promotion rules could not be read
at the source. A third-party analytics site claimed a "Paid Product/Service
Promotion" flair is mandatory; that is not Reddit's own documentation and does
not meet CLAUDE.md §5. Nobody posts there until the actual rule is read.

---

| Date | Surface | Beat | Visual(s) | Reusable from | Link |
|---|---|---|---|---|---|
| 2026-09-09 | itch devlog | **v0.1.0 launch.** Full feature set of the shipped zip, what is and is not tested, what is not in it yet, the price ladder, the GPL position | none (text only) | — | [devlog 1658358](https://z3er1n.itch.io/texel/devlog/1658358/texel-010-pixel-art-painting-for-blender-with-texel-density-that-actually-gets-measured) |
| 2026-09-09 | Bluesky | **v0.1.0 launch.** Problem first (pixels change size across the mesh), then the tool | `store/page/03_real-addon.png`, `store/shots_1280x720.png`, `store/animates_1280x720.png` — all three resampled to JPEG q95 4:4:4 for the blob cap | **2026-09-30** | [3mv4rjmevvg2t](https://bsky.app/profile/pixelkiln.bsky.social/post/3mv4rjmevvg2t) |
| 2026-09-10 | **BlenderArtists** | **Release thread.** Problem first (pixel size drifts across the mesh, staircased diagonals), then the tool, honest Windows-only test scope, GPL position, price ladder | none (text only) | — | [t/1652476](https://blenderartists.org/t/texel-paint-pixel-art-directly-onto-your-models-and-animate-it/1652476) |

**That guard held.** `texel-marketing`'s 09-09 run read this line, checked it
against the live account rather than trusting it, and did not post: the trailing
7 days carried **6** posts (09-03, 09-05, 09-08 x2, 09-09 x2) against
`marketing_plan.md`'s ceiling of 3-4, and the launch post was **14 minutes old**.
The v0.2.0 release note moved to **Friday 2026-09-11**; see `QUEUE.md`.

**Next Texel Bluesky day: Friday 2026-09-11** — the v0.2.0 release note.

---

## Replies (OPERATIONS.md §D — reply more than you post)

Threads answered in other people's feeds, no Texel mention unless the question
literally is what Texel does. Verified live on the public AppView, never on the
poster's own success message.

| Date | Thread | What was said | Link |
|---|---|---|---|
| 2026-09-09 | @unamisden.neocities.org — ripped tilesets from Spriters Resource have a border around every tile, so Aseprite can't grid them | Aseprite's **File > Import Sprite Sheet** already covers it: X/Y is the outer margin, Width/Height the real tile size, and the **Padding** checkbox gives Horizontal/Vertical for the gap between tiles. **Checked against the Aseprite source before answering**, not recalled — `data/widgets/import_sprite_sheet.xml` carries `padding_enabled` + `horizontal_padding`/`vertical_padding`, and `cmd_import_sprite_sheet.cpp:52` subtracts `padding.w * (cols - 1)`, which is what makes it a *between-tiles* gap rather than a margin | [3mv4soa6vdb2c](https://bsky.app/profile/pixelkiln.bsky.social/post/3mv4soa6vdb2c) |
| 2026-09-09 | @teggy.mastodon.gamedev.place.ap.brid.gy — 3D roof autotiling works, but 1-wide roof peaks need "adjusting some rules" | It is a tile-inventory gap, not a rules gap: a 9-piece terrain set is centre + 4 edges + 4 corners and **none of those is capped on two opposite sides**, so a 1-wide run has no legal member. Straight out of Oakheart — the free sample once shipped 6 of 9 dirt-path pieces and nobody could close a path | [3mv4sof7j3t2t](https://bsky.app/profile/pixelkiln.bsky.social/post/3mv4sof7j3t2t) |
| 2026-09-09 | @gamebrief.bsky.social — follow-up on the Icons Vol. 2 chestplate: "which change alone moved the needle most?" | **Out of this routine's lane** (a pack question, so `pixelkiln-social`'s) and answered anyway: it arrived 23:54 UTC, after that task's 16:00 run, and would have sat ~19h. Second technical question from the same human peer. Answered honestly that the changes shipped in one commit so **nothing isolates them**, then gave the pick and the reason: at 16x16 the silhouette is read before the interior | [3mv4soofbny2w](https://bsky.app/profile/pixelkiln.bsky.social/post/3mv4soofbny2w) |
| 2026-09-10 | @kudzuteeth.bsky.social — *"got scared off by UVs and texture painting, all the tuts made me feel stupid, pwease help"* (@maplesyruplush had already answered well, and raised texel density) | The default is not scaled: **a cube unwraps to the same UV size however big the cube is**, so the texture lands coarser on big objects by exactly their size ratio. Given as a measured number rather than a claim — the density card built today read **8.4x** across a 3.2 m box and a 0.38 m box, and 3.2/0.38 = 8.42. Fix named as Blender's own free one, **UV menu ▸ Average Islands Scale**. **Verified in 4.5.9 before sending, and the check changed the answer**: `uv.average_islands_scale` exists with description *"Average the size of separate UV islands, based on their area in 3D space"*, but it has **no default UV-editor keymap** — the Ctrl+A shortcut that gets repeated everywhere is not there, so the reply says "UV menu" and names no shortcut | [3mv6v6smrzd2k](https://bsky.app/profile/pixelkiln.bsky.social/post/3mv6v6smrzd2k) |
| 2026-09-10 | @modularmesh.bsky.social — *"Succulents are absolutely disgusting to UV unwrap"* (PBR/Substance workflow, not pixel art) | Agreed with the gripe first, then one specific gotcha: **Smart UV Project's Island Margin still defaults to 0.0 in 4.5**, so a mesh with a per-leaf island count gets touching islands that bleed once mipmaps engage. Checked against the operator's RNA in 4.5.9 rather than recalled — `island_margin` default `0.0`, alongside `angle_limit` 66°, `area_weight` 0.0 | [3mv6v6vf4ax2t](https://bsky.app/profile/pixelkiln.bsky.social/post/3mv6v6vf4ax2t) |

---

## Notes for the next run

- **The poster takes PNG/JPEG only** and throws above **976,560 bytes**
  (`pixelkiln\tools\pixelkiln_social.ps1`, `-Mode post -Spec <json>`; always
  `-DryRun` first — it prints the byte count and the parsed facets). The 1,280x720
  store cards are 780-1,130 KB as PNG, so they need resampling: JPEG **quality 95
  with `subsampling=0`** held the small Blender UI text and the pixel art with no
  visible artefact, at a third of the size. Verified by reading the JPEG back
  before posting.
- **Verify on the public AppView, never on the script's output.** The post above
  was confirmed as `app.bsky.embed.images#view`, 3 images, alt text 1352/1266/1089
  chars intact, 4 facets, 297/300 bytes.
- **Alt text is long on purpose** — it is the accessibility floor and it is
  indexed. Describe what is actually in the frame, including the words rendered
  in the image.
- ~~**There is still no density visual.**~~ **CLEARED 2026-09-10** — `promo/density/texel-density-measured.png`
  is live as gallery slot 10 and verified pixel-identical off the public URL.
  It was the only headline claim with no picture of a *result*, and it had
  outlived two runs that each said so. See ledger row **T-001**. It is queued as
  the **Sun 09-13** fallback beat behind `texel-funnel`'s first drop.
- **STANDING RULE (user, 2026-09-09): Texel is not in a rivalry with anything,
  and it is not derived from anything.** No Texel post, reply, listing line or
  log entry frames it as competing with, answering, or descending from another
  product. **Never interact with another pixel-art-in-Blender account** — no
  replies, no quotes, no likes, and do not use their threads as §D targets even
  though they are the highest-engagement ones on the platform. Overlapping
  features are not a lineage: texel density is a standard 3D concept, and two
  tools addressing a known problem overlap by definition.
- **This corrects a 2026-09-09 entry by this routine.** The run reported another
  Blender add-on as "a direct competitor running hotter than the plan assumes"
  whose post "describes our exact feature set", and offered it as a pricing
  input. That was a rivalry constructed in the report, not observed in the
  product. **Verified the same day: the live Texel page contains no reference to
  any other product** — no comparison, no name, no operator-count contrast. The
  live description reads "95 operators, every one with a button in the sidebar".
- **What was actually observable, and all that was:** posts about pixel art in
  Blender can take ~874 likes on Bluesky; ours take 6-18. That is a **reach**
  fact about the topic, not about any account. It argues for replying in more
  threads, which is how reach grows, and for nothing else. It is not a pricing
  input.
- **One line could still leak the frame into public.** `LISTING.md`'s draft body
  carries "95 operators. The nearest comparable add-on ships 67." It has never
  been published and the live page says something else. Left in place rather than
  edited here because it sits inside the pricing rationale, which is the user's
  — but it must not reach the store page.

### Which threads are this routine's, decided 2026-09-10

The ownership table gives `pixelkiln-marketing` *"Bluesky replies that are not
about Texel"*, while this routine's §D orders **two replies every run** and
forbids mentioning Texel in them. Read flatly those two rules collide, and the
09-09 run shows the drift: of its three replies, one was an Aseprite
sprite-sheet question and one was a pack question it flagged as out of lane and
answered anyway.

**The line drawn here: this routine replies in threads about *Texel's problem* —
3D, Blender, UVs, texel density, texturing — and leaves 2D pack topics
(tilesets, sprite sheets, Aseprite-only questions, pack feedback) to the
Pixelkiln routines.** Both replies above sit on the 3D/UV side. It is a
proposal, not a ruling: `texel-watch` and `pixelkiln-watch` share an account and
either can overrule it, but an unwritten edge is how two routines end up doing
one job.

**Not replied to, and deliberately.** The freshest and highest-engagement
threads in every search this run belong to another pixel-art-in-Blender product
account (874 likes on one post). **Standing rule: no replies, no quotes, no
likes, not used as §D targets.** One further thread was skipped for the same
reason — a third party resharing that product's itch link, which is that
product's thread by another route.

**Tooling added this run.** `public.api.bsky.app` answers **403** from this
machine (Cloudflare), so reply targets could not be found unauthenticated. Two
read-only modes were added to `pixelkiln	ools\pixelkiln_social.ps1` —
`-Mode search -Query "..."` and `-Mode thread -ReplyTo at://...` — which go
through the PDS with the session token and do work. `-Mode thread` is what
showed that the first target's root was a beginner asking for help rather than
the snippet the search returned.
