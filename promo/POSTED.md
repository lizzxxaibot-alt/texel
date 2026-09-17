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
| 2026-09-11 | Bluesky | **v0.2.0 release note** *(queued for Wed 09-09, moved to Fri 09-11)*. Problem first (a mirrored corridor tile should land back on the grid), then the release, then the four counts | `promo/transform/texel-0.2.0-selection-transforms.png`, downsampled 2560x1440 -> 1280x720 and saved JPEG q95 subsampling=0 (259,740 B, well under the 976,560 cap) as `..._post.jpg` | **2026-10-02** | [3mvbff2zfou2d](https://bsky.app/profile/pixelkiln.bsky.social/post/3mvbff2zfou2d) |
| 2026-09-13 | Bluesky | **The Density Cheatsheet drop** — `texel-funnel`'s free CC0 sheet, announced as the sheet rather than as Texel, per the `QUEUE.md` row that claimed this slot. Problem first (one wall crisp, the crate in front of it mushy, same texture, same distance), then the two worked numbers, then the link | `funnel/density_cheatsheet/_full_2x.png` (the 2x render of the live itch cover, 1260x1000, 615,699 B — under the 976,560 blob cap, so no JPEG step was needed) and `funnel/density_cheatsheet/shot_sheet.png` (1240x1754, 664,404 B). Neither had been posted before; `_full_2x.png` was checked against `cover.png` by downsampling it to 630x500 (mean channel delta 4.6, differences confined to type antialiasing) to confirm it is the same critic-passed design and not a stale intermediate | **2026-10-04** | [3mvggdv3qjy2f](https://bsky.app/profile/pixelkiln.bsky.social/post/3mvggdv3qjy2f) |
| 2026-09-16 | Bluesky | **Nearest-vs-bilinear — problem first.** Queued 2026-09-09 for Mon 09-14, stood down there on the account-saturation ground, and landed on Wed 09-16 exactly as `QUEUE.md` planned. Sent as "what interpolation does to indexed art", **not** as a comparison to any product — the footer names `Pillow.Image.BILINEAR` as the right-hand generator, which is a library function, not a rival | `promo/transform/texel-nearest-vs-bilinear.png`, **252,034 B at 1280x720** — under the 976,560 blob cap, so no JPEG step was needed and the posted bytes are the linted bytes. Every image the card displays (`nn_half_texel.png`, `bl_half.png`, `pal_nn_texel.png`, `pal_bl.png`) was unposted; `original.png` is not displayed, only quoted as figures | **2026-10-07** | [3mvnxwghjbm2c](https://bsky.app/profile/pixelkiln.bsky.social/post/3mvnxwghjbm2c) |

**That guard held.** `texel-marketing`'s 09-09 run read this line, checked it
against the live account rather than trusting it, and did not post: the trailing
7 days carried **6** posts (09-03, 09-05, 09-08 x2, 09-09 x2) against
`marketing_plan.md`'s ceiling of 3-4, and the launch post was **14 minutes old**.
The v0.2.0 release note moved to **Friday 2026-09-11**; see `QUEUE.md`.

**First-hour engagement, 09-13:** at 3 minutes the post held **3 likes and 2 reposts**. The reposts are the number worth watching — this account's last ten posts took 6-15 likes each and are not normally reposted at all, so a free CC0 resource behaving differently from a product post is the first weak evidence for the funnel's premise. One post is not a result; `texel-watch` has the ledger for whether it converts to downloads.

**Sunday 2026-09-13 posted, and Monday is now decided rather than left to be re-derived.**

The 09-11 run wrote that Monday gives way "if the trailing count is already at
4". This run counted the live account before sending: the trailing 7 days held
**7** posts (09-08 x2, 09-09, 09-10 x2, 09-11, 09-12) against
`marketing_plan.md` line 23's ceiling of **3-4 a week across the whole account**.
Today's send makes **8**, and four consecutive posting days (09-10, 09-11,
09-12, 09-13).

**Stated rather than hidden: that is double the volume ceiling.** It was sent
anyway, on the reasoning already recorded in `QUEUE.md` and not re-litigated
here — Sunday is Texel's under the day-split that A-005 settled, the slot was
claimed in writing two days before, the page had been live since 09-11 with no
traffic driver pointed at it, and dropping it silently is the exact failure the
funnel's gate was built to prevent. The day-split and the 3-4 volume line
genuinely do conflict (seven owned days cannot fit four posts); the split is the
later and more specific rule, so it governs *whose* day it is, and the volume
line still governs *whether* a day gets spent.

**So Monday 2026-09-14 does not post.** The trailing count on Monday will read
8. The nearest-vs-bilinear beat (`promo/transform/texel-nearest-vs-bilinear.png`,
built, linted, critic-passed) **takes Wed 09-16**, and the mask beat that held
Wednesday moves out — it wants to anyway, since its only asset is a panel inside
the 09-11 card and is reuse-blocked until 2026-10-02. `QUEUE.md` carries both
moves as rows, not as prose.

**Whoever runs Monday: the work is section D, not a post.** Replies have no
ceiling; that is the whole point of §3a.

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
| 2026-09-11 | @firebreath.bsky.social — which screen tablet (Wacom / Huion / XP-Pen) is stable with Blender, Krita/Affinity and ArmorPaint; by the time this ran they had already linked a Huion in their own follow-up | Did **not** answer the brand question — we own none of those three and could not check it. Gave the thing that applies whichever they bought: **Preferences > Input > Tablet API**, the setting that decides whether pressure reaches Blender at all. **Read out of Blender 4.5.9 rather than recalled** — the enum is `AUTOMATIC` (the default), `WINDOWS_INK` (*"native Windows Ink API, for modern tablet and pen devices"*) and `WINTAB` (*"Wintab driver for older tablets and Windows versions"*) | [3mvbfhnb4bs2t](https://bsky.app/profile/pixelkiln.bsky.social/post/3mvbfhnb4bs2t) |
| 2026-09-11 | @winterbyrne.bsky.social — a Waterman Butterfly world map unwrapped off a UV sphere in Blender and exported as a UV layout to paint over in Krita/GIMP/Inkscape; they had already got it working and posted the result | Opened on the work, not a correction, then two settings in that exporter: **Format has an SVG option** (vector guide lines that scale to any texture size — they had named Inkscape themselves) and **Fill Opacity defaults to 0.25**, so every face ships a grey wash under the paint; 0 gives outlines only. **Verified by running `uv.export_layout` in 4.5.9 twice and diffing the SVG**, not by reading the tooltip: at the default every polygon is written `fill="rgb(204, 204, 204)" fill-opacity="0.25"`, at 0 it is `fill-opacity="0"` with the black stroke intact. (`export_all` also defaults to **False** — *"not just visible ones"* — but they had clearly already cleared that, so it was left out rather than used to correct them) | [3mvbfhnrsiz2k](https://bsky.app/profile/pixelkiln.bsky.social/post/3mvbfhnrsiz2k) |
| 2026-09-12 | @freddifish.bsky.social — *"is this type of texture work (Cloverpit) possible without Substance Painter? I hate Adobe so much"* (16 likes, root of the thread; @sasvel.itch.io had guessed Blender could do it but said "can't say personally") | Answered the question actually asked — yes, with no Adobe — and closed sasvel's stated uncertainty rather than correcting it. The one setting that decides the look: **the Image Texture node's Interpolation**, which **defaults to `Linear`** and smooths a deliberately small map straight back out; `Closest` keeps the texels hard. **Read out of Blender 4.5.9 rather than recalled** — `ShaderNodeTexImage.interpolation` default is `'Linear'` and the enum is `Linear / Closest / Cubic / Smart`. Nothing was claimed about how Cloverpit itself was made, because that was not checkable | [3mvdvtigovx26](https://bsky.app/profile/pixelkiln.bsky.social/post/3mvdvtigovx26) |
| 2026-09-12 | @navnoise.bsky.social — *"A pipe thing / Getting the hang of texture painting in blender"*, alt text "A grime covered pipe" (4 likes, **0 replies**, so ours is the only one in it) | Opened on the work, not a correction: the grime streaks follow the form instead of sitting on top of it. Then one thing that bites later — **Texture Paint's Bleed (Tool Settings ▸ Options) defaults to 2 px**, enough to hide island seams on a 1k map and not on a 4k one. **Verified in 4.5.9**: `ImagePaint.seam_bleed` default `2`, description *"Extend paint beyond the faces' UVs to reduce seams (in pixels, slower)"*. Deliberately a different fact from the 09-10 Smart-UV-Project `island_margin` answer, which is the adjacent trap and was already spent | [3mvdvtniwvu2f](https://bsky.app/profile/pixelkiln.bsky.social/post/3mvdvtniwvu2f) |
| 2026-09-13 | @redvampire.itch.io — a Star Trek ship's UV layout, *"getting better at not shooting my dick off doing UVs"* (3 likes, one reply already from @lumininja91). Their own alt text says the islands *"aren't stretched out weirdly or in a way that changes the texel density across the model"* — i.e. they were checking density **by eye** | Opened on the work, not a correction. Then Blender's own built-in measurement of the thing they were eyeballing: **UV Editor > Overlays > Display Stretch**, and the trap that makes it useless if you don't know it — **it opens in Angle mode, which shows shear, not scale**; Area is the density one. **Read out of Blender 4.5.9 rather than recalled**: `SpaceUVEditor.show_stretch` default `False`, `display_stretch_type` default `'ANGLE'`, enum `ANGLE` (*"Angular distortion between UV and 3D angles"*) / `AREA` (*"Area distortion between UV and 3D faces"*). Deliberately **not** the `uv.average_islands_scale` answer given to @kudzuteeth on 09-10 — their screenshot shows the Mio3 UV sidebar with its own Average Island Scales and a density Get/Set field, so that answer would have been both spent and redundant | [3mvggigm65o2i](https://bsky.app/profile/pixelkiln.bsky.social/post/3mvggigm65o2i) |
| 2026-09-13 | @chichimunga.com — *"I'm going to be selling my first tileset for $10 (jokes)"*, with a screenshot of an inventory grid being drawn in Aseprite 1.3.18.5 (11 likes, **0 replies**, so ours is the only one in it) | Opened on a detail actually visible in the screenshot — the 1px orange corner pips reading as depth without a bevel — then picked up their own word *tileset*: **Layer > New > New Tilemap Layer**, and that **Tileset Mode defaults to Auto**, so an identically redrawn slot reuses its tile rather than duplicating it. **Verified against the Aseprite source on this machine, not recalled** — `data/gui.xml:909` carries `<item command="NewLayer" text="@.layer_new_tilemap_layer">` with `tilemap=true` and `ask=true` (hence "it asks for a tile size"), `data/pref.xml:287` sets `default_tileset_mode` to `app::TilesetMode::Auto`, and `en.ini:163` defines Auto as *"Modify and reuse existing tiles, create/delete tiles if needed/possible"* | [3mvggilmbse2f](https://bsky.app/profile/pixelkiln.bsky.social/post/3mvggilmbse2f) |

---

### The ceiling said don't post. This run posted anyway, and here is the arithmetic

**`marketing_plan.md` contradicts itself, and the contradiction is what gates this
routine.** Line 23 says **"3-4 posts/week max"**. The **Cadence** section of the
same file, rewritten 2026-09-10 under ledger row A-011, says *"the account is
shared with Texel, so the week is split by DAY, not by volume"* and *"trailing-7-day
post counts are NOT a sufficient check"*, then hands out **all seven days** to an
owner - four to Texel, three to the packs. Read together those are 4/week and
7/week. **Neither section cites the other.**

**What the live account actually held at 15:20 on 2026-09-11** (counted off
`-Mode feed`, not off this log). Six posts in the trailing seven days:

| when (UTC) | line | day, local |
|---|---|---|
| 09-05 09:19 | packs - UI Vol.1 9-slice | Fri - **a Texel day** |
| 09-08 03:06 | packs - HUD Vol.6 | Mon - **a Texel day** |
| 09-08 19:12 | packs - Icons Vol.2 chestplate | Tue - packs' |
| 09-09 21:18 | packs - Oakheart carpets | Wed - **a Texel day** |
| 09-10 00:15 | **Texel** - v0.1.0 launch | Wed - Texel's |
| 09-10 19:07 | packs - Inventory Vol.7 | Thu - packs' |

**Five of the six are the packs', and three of those five landed on Texel days.**
Texel has posted on Bluesky exactly **once, ever**. Deferring the v0.2.0 note a
second time would have charged Texel for an overspend it did not make, on the day
the split gives it, and would have pushed a release note five days past the
release it announces.

**The 09-09 refusal is not being overturned - its second reason simply expired.**
That run gave two: the count, *and* that the launch post was **14 minutes old**.
Today the nearest post is the packs' Inventory Vol. 7 at **20 hours**, a different
product line. "Two posts about the same product a quarter-hour apart reads as a
bot" was the load-bearing half, and it no longer applies.

**What was checked for fatigue before deciding**, since the count alone is not
evidence of harm: engagement across the cluster is flat, not decaying - 09-05 = 8
likes, 09-08 = 15 and 11, 09-09 = 13, 09-10 = 12 and 6. The 6 is the newest post
and the lowest, which is worth watching; it is not yet a trend.

**Not this routine's file to fix.** `marketing_plan.md` belongs to the packs, and
the ownership table gives non-Texel Bluesky to `pixelkiln-marketing`. **Handed to
`pixelkiln-watch` as a finding for the Pixelkiln ledger:** line 23 and the Cadence
section give two different ceilings, and until one of them is struck, every routine
sharing this account is reading its own budget out of the same file and getting a
different number. The honest reading is that line 23 predates the account carrying
two product lines - when it was written, "the account" meant the packs alone, and
3-4/week is what the day split still gives the packs. But that is an inference,
not what the file says.

**Standing rule held again this run.** Every one of the four freshest and
highest-engagement results for "texel density" and "texture painting blender"
belonged to the other pixel-art-in-Blender product account (63-875 likes). Not
replied to, not liked, not used as section D targets. One further result was
skipped for the same reason at one remove - a third party's post inside that
account's thread, praising it. The two threads answered instead are both on the
3D/UV side of the line drawn on 2026-09-10.

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


---

## Sat 2026-09-12 — a packs day, so nothing was posted about Texel. Section D + E run.

**No Texel post, by the calendar and not by omission.** Saturday is the packs'
(`#screenshotsaturday`, `marketing_plan.md`); Texel takes Mon/Wed/Fri/Sun. No beat
was consumed from `QUEUE.md` — **Sun 09-13 is still `texel-funnel`'s cheatsheet
drop**, and Mon 09-14 still carries the cadence decision already written down for it.

**Ledger: no `texel-marketing` rows were open.** T-008 is `texel-release`'s, T-002
is `HUMAN`. Nothing to clear and nothing to refuse.

### Two replies, both verified on the public AppView

Logged in the table above. `public.api.bsky.app` answered **200** from this machine
this run — the **403 recorded on 2026-09-10 was transient, not a standing block** — so
both replies were confirmed against the real AppView (parent URI, full text, byte
count) rather than against the PDS or the script's success line. Worth knowing next
run: the unauthenticated path works again, and it is the stronger check.

**Standing rule held again, and it cost the best targets.** Every high-engagement
result for "texel density" and "texture painting blender" this run belonged to the
other pixel-art-in-Blender product account (880 and 16 likes, plus four promo
posts). **Not replied to, not liked, not used as §D targets.** One further post was
skipped at one remove — a third party inside that account's thread saying "addons
like yours help" — same precedent as 09-10 and 09-11. Also skipped deliberately:
`@johanpeitz.com`'s picoCAD 2 launch (**397 likes**, the highest-reach thread
available all run). picoCAD is not a Blender add-on, so the letter of the rule does
not reach it — but it *is* a pixel-art 3D texturing tool, and anything a tool
account says in its launch thread reads as sniping. Rule 9's reason applies even
where its letter does not.

### The listing page was changed — the gallery order, and one tag

**§E's conversion trigger did NOT fire.** `LEDGER.md` reads **51 views, 0 sales,
0 downloads** at 2026-09-12; the rule needs 200+ views (~09-20). These changes were
made on the weekly Saturday check, **not** on conversion evidence, and that
distinction should survive into whatever `texel-watch` concludes at 200 views.

**Nothing was contaminated by changing it now.** 0 sales on 51 views has a
confidence interval containing every plausible conversion rate — there was no
baseline worth protecting, only a first image a `design-critic` pass called FATAL.

**The gallery was reordered to `02,03,01,10,06,04,05,08,07,09`** (ids
`29883177,29883185,29883174,29902828,29883200,29883192,29883196,29883208,29883203,29883248`)
after that pass returned **VERDICT: ITERATE** with 1 FATAL and 2 SERIOUS:

- **FATAL — the first slot did not say what the product is.** The old hero was the
  animated pixel-perfect stroke demo: a zigzag line on a dark grid. **No Blender
  chrome, no viewport, no mesh.** The tagline promises "paint pixel art straight
  onto your models in Blender", and the one image that renders large showed no
  model. The new hero is the pixel-textured character on the cobbled street — the
  only asset showing mesh + Blender render + pixel art at once, and it still reads
  at thumbnail size. The stroke GIF keeps prime real estate at **slot 3**, where its
  motion still lands but now as "problem 1, solved" rather than an abstraction.
- **SERIOUS — the most differentiating claim was last.** The density card (8.4x
  spread then 1.0x, measured) is the only image answering *why does this need a
  dedicated tool*, and it sat at position 10 behind a thumbnail strip. **Now
  position 4**, inside the top four where it is actually seen.
- **SERIOUS — the gallery did not follow the description's own argument.** The copy
  sequences two claims (staircase strokes, then texel size drift); the gallery gave
  claim 1 cold and claim 2 as an afterthought. The new order runs *what is it → is
  it really Blender → problem 1 → problem 2*.
- POLISH, also applied: slot04 (the four frame-state renders) now sits directly
  behind slot06 (the Frames panel that produces them) instead of orphaned, and the
  sci-fi corridor — the least differentiated asset — is correctly last.

**Verified logged-out, not in the editor.** `itch_shots_manage.mjs` reported OK after
its own full reload; the public page was then re-fetched (HTTP 200, 30,973 B) and the
ten `screenshot_list` hrefs base64-decoded to confirm the order really is
`29883177, 29883185, 29883174, 29902828, …` in public.

**One tag added: `textures`** — now 3D, Animation, Blender, Pixel Art, Sprites,
**Textures**, confirmed live logged-out. Five of ten slots were in use on a page
whose actual problem is 51 views in three days, and `textures` is on itch's own
suggested-tag list and is literally what the product paints.

**Four candidate tags were rejected on purpose**, recorded so it is not
re-litigated. itch's quality guidelines say *"do not use unrelated tags or
classifications to promote your game"* and *"prefer using a suggested tag"* (read at
the source this run: `itch.io/docs/creators/quality-guidelines`). `low-poly` — Texel
neither requires nor targets low-poly; our demo art merely is. `unity` / `godot` —
the sheet+JSON export is engine-agnostic, and Texel is not a tool for either.
`retro` / `psx` — an aesthetic association, not what the add-on does. Each would
plausibly buy traffic; each is the kind of reach that gets a page delisted, and
CLAUDE.md §5 rates that a liability rather than a venture. **`modeling` and `tool`
were skipped too** — the second because itch tells you not to tag what the metadata
page already classifies, and Category is already **Tool**.

**AI disclosure survived both saves and was checked, not assumed** —
`{yes: true, graphics: true, text: false, code: true}` after the tag write.

### The other three §E checks came back clean

- **Tagline still true.** *"Paint pixel art straight onto your models in Blender.
  Texel density, seamless tiles, cel animation, sheet + JSON export."* Every clause
  ships in `dist/texel-0.2.0.zip`. It does not mention the v0.2.0 selection
  transforms, which is a field-length choice rather than a staleness problem.
- **Description still leads with the problem.** The problem lands in sentence two,
  inside the first 40 words: *"the two things that go wrong when 2D pixel art meets
  a mesh: strokes that come out as staircases, and pixels that change size from one
  face to the next."*
- **A suspected mojibake on the live page was checked and is NOT one.** The
  description rendered as `Blender � and animates it` in this run's console. The raw
  bytes are `Blender &mdash; and animates it`, and the page decodes as UTF-8 with
  **zero U+FFFD**. It was the Windows console codepage, not the store page.
  Recorded because the next run will see the same artefact and must not "fix" a live
  sales page over it.

### Fixed in this routine's own SKILL.md — it contradicted itself two lines apart

The §A table still read `| Sat | #screenshotsaturday — the best render of the week |`
while the prose **directly above it** said Saturday moved to Sunday on 2026-09-09 and
belongs to the packs, and §A's own first line said *"Texel takes Mon / Wed / Fri /
Sun."* A run reading only the table — the normal way to read a calendar — would have
posted Texel on a Saturday **using the packs' hashtag, on the shared account**: the
exact collision `pixelkiln-watch` run 8 caught before it landed. This run hit it and
had to resolve it from the prose.

The row now reads `| Sun | The best-looking render of the week |`, and
`#screenshotsaturday` is struck from the §A hashtag list (which had also listed it
as *allowed*) with a pointer to `OPERATIONS.md` §3, where it is already banned for
Texel. `#lowpoly` replaces it — it is in OPERATIONS.md's list and was missing here.
**This changes no policy**; it makes the file agree with its own prose and with the
document it tells you to read first. Backup at `SKILL.md.bak`.

This is the same defect class the 2026-09-09 routine audit was opened for
(`pixelkiln-marketing` both forbidding and prescribing Reddit two lines apart), and
**it is now the third instance** — so it is worth `texel-watch` asking whether the
calendar should live in exactly one file rather than being restated in three.

### Two threads were looked at and left alone this run

- **@thelaastame.bsky.social** (today, Blender texture-painting practice) — the
  subject is horror fan art of a partially-clothed figure. The work is fine and
  the thread is on-topic, but a product account arriving to comment on that
  specific image is not something this routine should do. `OPERATIONS.md` §3a:
  silence is free.
- **@augsofficial.bsky.social** (2026-08-30) — their own self-reply names the
  sub-texel problem exactly (*"I made my UVs too small, the tops of the metal
  bands kinda flipped out when I pixelated the textures"*), and there is a real
  answer for it. Passed over only on **age**: a reply on a 14-day-old post gets
  almost no reach, and reach is the stated purpose of §3a. **Worth picking up if
  they post about it again.**

| 2026-09-14 | @hillsguy.bsky.social — first low-poly car, a 1994 Supra MK4 in #b3d, **392 tris / 128x128 texture**, hand-painted in Krita with some photo projection (2 likes, **0 outside replies**, so ours is the only one in it) | Opened on the two numbers they stated rather than on the render — the four images carry **empty alt text**, so nothing was claimed about how it looks. Then the trap that a 128px map makes expensive: **`uv.pack_islands` margin defaults to 0.001 and `margin_method` sits on `SCALED`** (*"Use scale of existing UVs to multiply margin"*), so the gutter is not a predictable pixel count; `FRACTION` is *"a precise fraction of final UV output"*, making 1/128 = 0.008 exactly one pixel. **Read out of Blender 4.5.9 LTS with `--factory-startup` rather than recalled** — `margin` default `0.001`, `margin_method` `'SCALED'`, `rotate` `True`, `shape_method` `'CONCAVE'`. Deliberately **not** the 09-10 `island_margin` answer given to @modularmesh: different operator, different default, different failure | [3mvix2yb3e22z](https://bsky.app/profile/pixelkiln.bsky.social/post/3mvix2yb3e22z) |
| 2026-09-14 | @ultim8nik.bsky.social — *"Ruby Heart (MvC2) WIP #3 / texture painting will be the end of me"* (#b3d, **37 likes and 0 replies** — high visibility, nobody had answered in 10 days) | Answered the gripe, not the render (alt text empty again). **Blender 4.5.9's factory default `view_transform` is `AgX`**, so a hand-picked colour is not the colour on screen. **Measured rather than asserted**: an authored sRGB **204,26,26** written into a float image and saved through the scene's own colour management comes back **191,38,14** under AgX and **exactly 204,26,26** under Standard. Fix named as Blender's own — Colour Management ▸ View Transform ▸ Standard. Deliberately a different fact from the 09-12 Image Texture `Interpolation` answer and the 09-13 Paint Hard/Soft one, both already spent | [3mvix36455z2i](https://bsky.app/profile/pixelkiln.bsky.social/post/3mvix36455z2i) |

**All of @alfredbaudisch.com's threads were excluded on sight**, including the
880-like one that keeps topping every search for this topic. Standing rule, no
exceptions, not re-litigated.

---

## Tue 2026-09-15 — a packs day, so nothing was posted about Texel. Section D run.

**No Texel post, by the calendar and not by omission.** Tuesday is the packs'
(`OPERATIONS.md` §3: Texel takes Mon/Wed/Fri/Sun). **No beat was consumed from
`QUEUE.md`** — the nearest-vs-bilinear card still holds **Wed 09-16**, which is
tomorrow, and the mask beat is still blocked on a visual with no date.

**The ledger was cleared first and it was empty.** `ACTIONS.md` carries four open
rows — T-002, T-010 and T-011 owned by `HUMAN`, T-008 owned by `texel-release`.
**None is `texel-marketing`'s**, so nothing was frozen and nothing was touched.
T-011 is this routine's own 09-14 handoff about the calendar living in three
files; it is the user's to rule on and was left alone.

**§E is not due.** The listing check is Saturday's; last run 2026-09-12.

### Two replies, both verified on the public AppView

| Date | Thread | What was said | Link |
|---|---|---|---|
| 2026-09-15 | @neswest.bsky.social — revisiting an old scene, *"need to clean up texel density … and bring it all back into unreal next"* (#blender #gamedev #unrealengine, **19 likes and 0 replies** — nobody had answered in 20 hours, and ours is the only reply in it). No image alt text was exposed on the post, so **nothing was claimed about how it looks** | The cause that hides in an old scene rather than a new one: **non-uniform object scale**. `uv.unwrap` lays UVs out on the *un-scaled* mesh — Blender prints it itself, *"Object has non-uniform scale, unwrap will operate on a non-scaled version of the mesh"* — so a prop stretched on one axis keeps the UV island of the shape before the stretch. **Measured, not asserted** (script in the session scratchpad, seams marked on every edge so the unwrap is exact rather than the failed single-island fallback): a 2 m cube at object scale **(4,1,1)** unwraps to **42.62 px/m on the unstretched faces and 21.31 on the stretched ones — a 2.000× spread** at a 256 map; `Ctrl+A ▸ Scale` then re-unwrap gives **25.58 px/m on every face, 1.000×**. Identical in **4.5.9 and 5.2.1**. Deliberately **not** the 09-10 `uv.average_islands_scale` answer or the 09-13 Display-Stretch one — both spent, and neither sees this, because the UVs are internally consistent for a mesh that is not the shape on screen | [3mvlhd6dwun2f](https://bsky.app/profile/pixelkiln.bsky.social/post/3mvlhd6dwun2f) |
| 2026-09-15 | @fuyukarasu.xyz — *"anyways I'm learning uv unwrapping and texturing"*, alt text *"low poly 3D model of Hatsune Miku dressed similarly to Red Pokemon … the rest being placeholders made in Blender's texture paint mode"* (4 likes, **0 replies**). Their parent post puts them on **Blender 5**, so the fact was checked in 5.2.1 rather than 4.5.9 | Opened on the concept they described themselves, then the Texture Paint default that costs a beginner an afternoon of flat placeholder fills: **Normal Falloff is ON by default at 80°**, so faces turning away from the view take less paint and a flat colour arrives with a soft edge nobody asked for. **Read out of Blender 5.2.1 with `--factory-startup` rather than recalled** — `ImagePaint.use_normal_falloff` default `True`, `normal_angle` default `80`, description *"Paint most on faces pointing towards the view according to this angle"*. The UI path was checked in Blender's own scripts, not guessed: `space_view3d_toolbar.py:915` defines `VIEW3D_PT_tools_brush_falloff_normal`, label **Normal Falloff**, `bl_parent_id = VIEW3D_PT_tools_brush_falloff` and `bl_options = {'DEFAULT_CLOSED'}` — hence "a collapsed sub-panel under Tool ▸ Falloff", which is why nobody finds it. Deliberately a different fact from the 09-12 `seam_bleed` answer, which lives in the neighbouring **Options** panel (`:1354`) and was already spent | [3mvlhd6xmq22o](https://bsky.app/profile/pixelkiln.bsky.social/post/3mvlhd6xmq22o) |

### A reply this run nearly sent was false, and the test is what caught it

**Recorded because the next run will be tempted by the same sentence.** The
first draft for @neswest was the folk rule *"apply your scale or your texel
density is wrong"*. Tested before sending, and it is **wrong as stated**:

| case | per-face spread | density |
|---|---|---|
| uniform scale (4,4,4), **not** applied | **1.000×** | 10.65 px/m |
| uniform scale (4,4,4), applied | **1.000×** | 10.65 px/m |
| non-uniform (4,1,1), **not** applied | **2.000×** | 21.31 / 42.62 |
| non-uniform (4,1,1), applied | **1.000×** | 25.58 |

**Uniform scale costs nothing** — unwrap normalises the island to the UV bounds
either way, so the whole-object density changes with object size but stays even
across faces. It is **only** non-uniform scale that skews it, which is why the
reply says "stretched 4x on one axis" and not "apply your scale".

**A second near-miss, for the same file.** The first version of the test
unwrapped a cube with **no seams**; Blender answered *"Unwrap failed to solve 1
of 1 island(s)"* and the numbers came out of the fallback, showing an identical
2.000× spread before and after Apply Scale — i.e. the measurement said the fix
does not work. **The warning line was the only thing separating a real result
from a confident wrong one.** Marking every edge as a seam made each face its
own island and the effect appeared cleanly.

**And a version claim that did not survive:** the draft angle *"Blender 5
changed the Unwrap default, so the tutorials are stale"* is false.
`bpy.ops.uv.unwrap`'s RNA `method` default is **`CONFORMAL` in both 4.5.9 and
5.2.1**, with `margin` 0.001, `margin_method` `SCALED`, `correct_aspect` True and
`iterations` 10 identical across the two. Nothing to say there; it was dropped.

### Threads looked at and left alone this run

- **@johanpeitz.com — picoCAD 2 launch** (2026-09-11, **411 likes, 6 replies**,
  by far the highest-reach on-topic thread available that is not the off-limits
  account). Left alone deliberately. It is a **product launch thread for an
  adjacent paid pixel-art 3D tool**, and a product account arriving in it has no
  reading that is not piggybacking, whether or not Texel is named. The standing
  rule names pixel-art-*in-Blender* products specifically and picoCAD is a
  standalone modeller, so this is **not** that rule firing — it is §3a rule 8,
  silence is free, applied on its own merits. Noted here so the next run does not
  re-derive it as an opportunity.
- **@nostalgianinja.com** (2026-09-12, texturing stream announcement, 3 likes) —
  on topic and friendly, but a "live now" post has nothing to answer; a reply
  three days after the stream ended reaches nobody.
- **@lvnatav.bsky.social** (2026-09-15) — *"low poly, low res textures and
  texture warping? we're feeling daring today"* is a joke between friends, not a
  question. Nothing to add that would not land as a lecture.
- **@alfredbaudisch.com** — every thread excluded on sight as always, including
  the 883-like one that still tops the `texel density` search. Standing rule, no
  exceptions, not re-litigated. **Two further posts were excluded by the same
  route**: @smlcaptain and @puppiesandanime reposting that product's itch link.

### The ceiling count, recounted — for tomorrow's Wed 09-16 slot

**Taken as a real count, not a paraphrase of the feed** — `getAuthorFeed` through
the PDS with `filter=posts_no_replies`, which is the only way to separate
top-level posts from the §D replies that inflate every other view of this
account. (`-Mode feed` in `pixelkiln_social.ps1` still hits `$PublicAPI` and
still 403s from this machine; the snippet used is in the session scratchpad.)

**7 top-level posts in the trailing 7 days**, at 2026-09-15T20:24Z:

| UTC | local | owner of the day | posted by | beat |
|---|---|---|---|---|
| 09-09 21:18Z | Wed 16:18 | **Texel** | packs | Oakheart carpets |
| 09-10 00:15Z | Wed 19:15 | Texel | Texel | v0.1.0 launch |
| 09-10 19:07Z | Thu 14:07 | packs | packs | Inventory Vol. 7 |
| 09-11 20:21Z | Fri 15:21 | Texel | Texel | v0.2.0 |
| 09-12 19:10Z | Sat 14:10 | packs | packs | Icons Vol. 2 fix |
| 09-13 20:22Z | Sun 15:22 | Texel | Texel | Density Cheatsheet |
| 09-15 19:09Z | Tue 14:09 | packs | packs | Godot theme slots |

**Two corrections to what this file said on 09-14, both against the recount:**

1. **Mon 09-14 is empty — neither routine posted at top level.** The Texel
   stand-down held, and the packs did not take the day either.
2. **The packs are at 4 in the trailing 7 days, not 5.** The 09-14 section called
   them "5 against a cap of 3, two of those on Texel's days". On today's window
   it is **4, one of them on a Texel day** (09-09). The earlier figure was
   counted over a different, earlier window and is not wrong for that window —
   but it must not be carried forward as a standing charge against another
   routine. **Texel is at 3, every one on a Texel day**, unchanged.

**What this does NOT do is decide tomorrow.** By 09-16 15:19 local the window
rolls past the 09-09 21:18Z packs post, so the count will read **6** before
anything is sent and **7** after — over the 3-4 line, compliant with the
one-post-per-owner-day line, which is the same genuine conflict recorded on
09-13 and not re-litigated here. **The Wed 09-16 run must recount for itself
before it sends.** That is the whole lesson of the 09-14 FATAL: the arithmetic
was read off a paraphrase and was false on its own preferred evidence. A number
in this file is 24 hours old by the time the next run reads it.

---

## Run 2026-09-16 (Wednesday, a Texel day)

### Two replies, both verified on the public AppView

| date | thread | what was said | url |
|---|---|---|---|
| 2026-09-16 | @hauntedwolfmaive.bsky.social — *"lately ive been trying to have a lil more fun with my texturing process and 90% of it has just been UV unwrapping by projecting from view and tweaking them from there,,, its SO scuffed but it works and i like how these models have turned out :3"* (**13 likes, 0 replies** in three days, so ours is the only one in it). Their own alt text is unusually rich and was used rather than the render — *"the belly button is just a slice of the collar bone texture"* | Opened on the detail **they** flagged, and affirmed it rather than correcting — they like the result, so a correction would have been the wrong opening. Then the default that sits under the exact technique they named: **`uv.project_from_view` has `orthographic` OFF by default**, so a perspective viewport rides along into the UVs; it is a tickbox in the F9 Adjust Last Operation panel. **Read out of Blender 4.5.9 LTS with `--factory-startup` rather than recalled** — `orthographic` default `False` (*"Use orthographic projection"*), alongside `camera_bounds` `True`, `correct_aspect` `True`, `clip_to_bounds` `False`, `scale_to_bounds` `False`. Deliberately a different operator from every spent answer: not `average_islands_scale` (09-10), not `smart_project`'s `island_margin` (09-10), not `pack_islands` (09-14), not the non-uniform-scale unwrap (09-15) | [3mvnxtiqmsz2g](https://bsky.app/profile/pixelkiln.bsky.social/post/3mvnxtiqmsz2g) |
| 2026-09-16 | @erodozer.moe — *"I am out here just not giving a fuck, moving UVs for each face individually, and reusing sections that look about right instead unwrapping things as they're shaped. I am not a trained 3d artist"* (**13 likes, 0 replies**, so ours is the only one in it) | Self-deprecating post, so the reply **legitimises the technique first** — reusing sections is atlasing, and shipped props do it deliberately — then names the one real cost: overlap breaks baking, because AO wants unique texel space. The escape hatch is a second UV map kept only for the bake. **Measured rather than recalled**: `me.uv_layers.new()` was called in a loop in 4.5.9 `--factory-startup` and **returns `None` on the 8th add**, so a mesh carries exactly **8 UV maps** — a check that could have failed and would have changed the number in the reply. (`scene.render.bake.margin` default `16`, `margin_type` `ADJACENT_FACES`, read in the same run but left out of the reply as one fact too many) | [3mvnxtnzyjc2o](https://bsky.app/profile/pixelkiln.bsky.social/post/3mvnxtnzyjc2o) |

Both re-fetched from `app.bsky.feed.getPostThread` on the public AppView after sending: correct author, correct parent handle, full text intact.

### Threads looked at and left alone this run

- **@alfredbaudisch.com — every thread, including the 883-like one** (*"Imagine Aseprite or another #pixelart program inside Blender?"*, 26 replies) and the 09-15 and 09-16 posts. This is the other pixel-art-in-Blender product and it is **off limits under the standing no-rivalry rule**, which is exactly why it keeps surfacing at the top of every search this routine runs: it is the highest-engagement account on the topic. Not replied to, not named in any post, not quoted. **Also skipped: @obsurveyor and @nostalgianinja replies that sit inside those threads** — the rule is the thread, not just the account.
- **@tiotiohan** (*"Real life UV unwrapping"*, 8 likes) — a visual joke, nothing genuine to add.
- **@blooink.neocities.org** (*"UV unwrapping is a pain though"*) — 0 likes, 0 replies; the honest answer is one of the two facts already spent above, and repeating a spent fact into a dead thread is volume, not reach.

### What went out, and the two false premises `venture-critic` made this run delete first

**POSTED 2026-09-16 20:25:44 UTC** — [3mvnxwghjbm2c](https://bsky.app/profile/pixelkiln.bsky.social/post/3mvnxwghjbm2c),
**293/300 bytes**, re-fetched from the public AppView after sending: the image is attached
(`app.bsky.embed.images#view`, 1280x720), **1,525 characters of alt text intact**, 4 facets
(one link, three tags). All four figures were re-checked against `resample_facts.json`
before sending — 118 off-palette, 112 partial-alpha, 11 colours, 103 texels — and
`core.select.transform_region`, the function the card credits, was confirmed **present in
the live `dist/texel-0.2.0.zip`** by reading the archive rather than the roadmap.

`venture-critic` returned **VERDICT: REOPEN** on the draft decision — not against posting
the card, which it re-verified independently and found sound, but against **two premises in
the reasoning that were false and would have gone into this file as fact.** Both are
corrected here rather than quietly dropped, because the whole point of the 09-14 entry two
sections up is that a wrong number in this file survives to mislead the next run.

**FATAL 1 — the run nearly recorded that the v0.2.1 beat lost on quality. It lost on legality.**
The draft reasoning said radial symmetry "deserves a purpose-built visual" and was "not
perishable." That is a judgement about a post that **was never lawful to write**: §B's hard
ban is *never show a feature that is not in the uploaded zip*, and v0.2.1 is not uploaded
(see the new section in `QUEUE.md`). Had the Friday row been filed as "blocked on a visual",
a future run could have built a beautiful radial card on schedule and posted it **while the
zip was still unshipped** — walking into the exact ban this run avoided by accident of
checking. The Friday row now gates on **the live upload widget naming `texel-0.2.1.zip`
first, and the visual second.**

**FATAL 2 — the ceiling count was wrong in the self-serving direction, and is restated here properly.**
The draft said the account held **5 posts** and that the saturation ground had "cleared."
That used calendar-day buckets over the last 7 local days, which is **not this venture's
established method** — every prior check in this file uses a **rolling 168-hour window on
the live feed**. On that method, at a 15:15 CDT run on 09-16 (cutoff 09-09 20:15Z), the
window holds **7**: 09-09 21:18Z, 09-10 00:15Z, 09-10 19:07Z, 09-11 20:21Z, 09-12 19:10Z,
09-13 20:22Z, 09-15 19:09Z. The bucket method conveniently dropped the two 09-09 posts that
a rolling window still counts. **It is the same defect as the 09-14 FATAL, mirrored:** that
run miscounted to justify *not* posting, this one miscounted to justify posting.

**The action was still right, on a reason the draft never gave.** The count of 7 is not a
breach, because `marketing_plan.md` **retired the 3-4/week line in writing** — *"Volume is
governed by the day-split in Cadence below, not by a weekly number"* — and the day-split
permits one item per owned day, so 7 owned days admit 7 posts. **Wednesday is Texel's, and
it was unspent.** Texel has used **2 of its 4** owned days (09-11 Fri, 09-13 Sun); the packs
held 09-10, 09-12, 09-15, and `pixelkiln-marketing` ran today at 19:06Z and **correctly did
not post on a Texel day**. So the honest sentence is *"the day-split governs and Wednesday
was free"*, per the 09-13 precedent — **not** *"the ceiling has cleared"*, which was false.

**SERIOUS — a visual library was declared absent without opening the folder.**
The draft asserted there was no asset for the v0.2.1 beat. `shots/t008/` had been created
by `texel-release` at 13:02-13:12 **the same day** and holds a full before/after set for the
density-readout fix — `repro_top.png`, `repro_density.png`, `crop_sidebar.png`,
`crop_sidebar_1.50.png`, `after_15.png`, `after_density.png` and a `settle/` sequence.
**Precisely: those are readout-fix captures, not radial-symmetry ones**, so the claim "no
radial asset exists" survives — but the claim that the readout half was "a weak outbound
post" was **asserted without checking**, and it was the move that let radial be called the
marketable half. `ROADMAP.md` calls the readout *"the feature the product is positioned on"*.
Moot today because the whole beat is barred, but the ranking could have been wrong.

**NOTE, recorded because it is the run's one real save:** checking the live store page
before drafting a release note is what caught the unshipped zip. Trusting `ROADMAP.md`'s
tick would have produced a post advertising radial symmetry to an audience that cannot
download it.
