# Texel — support log and demand tally

Owned by `texel-support` (daily 08:15). Every buyer question, bug report,
feature request and refund lands here, with the answer given. **The tally below
is the demand signal that reorders `ROADMAP.md`** — three people asking for the
same thing beats a plan written before anyone bought it.

**Created 2026-09-09**, the day Texel went live. Nothing in it yet is a
placeholder: an empty tally is a real measurement, not a missing one.

---

## ESCALATED — awaiting the user

*Nothing escalated.*

---

## Running tally of repeated asks

| Ask | Times asked | Currently queued for | Roadmap agrees? |
|---|---|---|---|
| *(nothing asked yet)* | 0 | — | — |

**Top three this run:** none — zero inbound items since launch (**day 5**, and
**six** surfaces checked today rather than five). The tally has no top three
because it has no entries; that is a measurement, not an omission.

**What five empty days actually measure.** Not "buyers are satisfied" — there
are still **no buyers**: 58 views, 0 downloads, 0 sales on Texel itself, so no
one has yet been in a position to ask anything about the add-on. A silent
support queue on a product with zero installs carries **no information about the
product**, only about its traffic.

**Day 5 is the first day that statement needs a caveat, and it is worth stating
precisely rather than overselling.** `texel-funnel`'s **Texel Density
Cheatsheet** now has **17 views / 11 downloads** — so for the first time, real
people hold a Texel-branded file, and **11 of them asked nothing**. That is a
genuinely new fact, but it is weak evidence about the add-on: a free one-page
PDF is a read-once artifact that generates few questions from anybody, and
nothing in it is a piece of software that can fail. It moves the needle from
"nobody has anything to ask about" to "nobody has anything to ask about *the
paid tool*", and no further.

**A new sixth surface follows from that, permanently.** The cheatsheet page has
a live comment form, and it is the only Texel-branded thing anyone has actually
downloaded — so it is now read every run and is in the surfaces table below. See
the ownership note attached to that row: **reading it is safe, answering on it
is not yet settled.**

**Three Bluesky replies arrived since the last run and all three were triaged
out.** Recorded individually below, because two of them are near-misses that a
later run could plausibly grab by mistake — and one of them is on a thread this
venture owns:

| Reply | Why it is not a support item |
|---|---|
| @alimabsoute 2026-09-12 19:24 (reply **and** quote) — *"'I shipped a fix that was also wrong' is the part worth locking in"* | The root post is the **Icons Vol. 2 v1.4** card. A pack, not Texel. `pixelkiln-marketing`'s lane, left untouched |
| @winterbyrne 2026-09-12 15:01 — *"Ooh! Good point!"* | Closes our tip about the **UV-layout exporter's SVG format and Fill Opacity**. Blender advice, no Texel content. Not this desk's |
| @freddifish 2026-09-13 00:09 — *"cool, I'm excited to try some of this stuff out"* | **The near-miss worth reading carefully.** It closes an outreach reply logged in **Texel's own `promo/POSTED.md` (line 86)** — so by *thread ownership* it is a Texel thread, and the person is dead-centre in Texel's buyer profile (wants crunchy texture work in Blender, hates Adobe). It is still **not a support item**: Texel was never named by either side, and the reply contains **no question, no bug, no request and no refund** — it triages into none of the five buckets. Answering it would mean *introducing* the product into a thread that has not asked about it, which is a marketing act in a support voice. **Left for `texel-marketing`, whose thread it is, and named loudly here so it is not lost** |

**The rule the @freddifish row establishes, for later runs:** a thread being
*ours* does not make it *this desk's*. The test is whether an item asks
something, not who posted the parent.

**Does the tally disagree with `ROADMAP.md`'s order?** No — and it still cannot.
There is no demand signal of any kind, so the roadmap's "easiest first" ordering
stands on its own reasoning rather than on evidence. This is the fifth run in a
row that sentence has been true, which is worth naming: **the tally is the most
valuable thing this desk produces and it has produced nothing yet**, because the
input it needs is buyers, not effort. **The first three questions Texel ever
receives outrank the whole plan**, so they get logged the day they arrive.

## Refund reasons

| Reason | Times | Product bug? |
|---|---|---|
| *(no refunds requested)* | 0 | — |

Three of the same reason is a product bug, not three unhappy people.

---

## Log

| Date | Who | Bucket | Question | Answer given | Version queued |
|---|---|---|---|---|---|
| 2026-09-09 | — | — | *no inbound items; page live for under a day* | — | — |
| 2026-09-10 | — | — | *no inbound items; 5 surfaces checked (page, 2 devlogs, itch inbox, Bluesky)* | — | — |
| 2026-09-11 | — | — | *no inbound items; same 5 surfaces checked. Page 0 comments, both devlogs 0, itch inbox 0 of 20 rows, Bluesky 0 of 25 items* | — | — |
| 2026-09-12 | — | — | *no inbound items; same 5 surfaces checked. Page 0 comments, both devlogs 0, itch inbox 0 Texel rows of 20, Bluesky 0 Texel mentions of 25. The one new reply (@firebreath, thanking us for a Blender tablet-API tip) is not about Texel — `pixelkiln-marketing`'s lane, left untouched* | — | — |
| 2026-09-13 | — | — | *no inbound items; **6** surfaces checked (page, 2 devlogs, itch inbox, Bluesky, + the new cheatsheet page). Texel page 0 comments, both devlogs 0, cheatsheet page 0, itch inbox 0 Texel rows of 20, Bluesky 0 Texel mentions. 3 new Bluesky replies, all three triaged out (table above). A Bluesky **search** for the Texel URL was run for the first time — 0 third-party mentions* | — | — |

---

## Surfaces checked each run, and how

Recorded so a later run does not have to rediscover the access route.

**Restructured 2026-09-11.** This table was gaining a column a day, which would
be unreadable within a week. It now holds the **access route and the latest
result**; per-day outcomes live in the Log above, and the two prior findings that
still carry information are kept as history below the table.

| Surface | How it is read | Result 2026-09-13 |
|---|---|---|
| Texel itch page comments | `curl https://z3er1n.itch.io/texel`, then the `game_comments_widget` block | **0 comments.** HTTP 200, 31,028 B. Zero `id="post-N"` and zero `<div class="community_post"`. The `uploads` block still offers exactly one file, `texel-0.2.0.zip` |
| Texel devlog replies | `curl https://z3er1n.itch.io/texel/devlog`, then **`curl -L` each post URL** | **2 devlogs live, 0 comments on either.** Index 200, 19,792 B, still no third post. Post 1658358 (32,641 B) and 1658363 (30,469 B); zero `id="post-N"` in both, comment form live in both |
| itch notification inbox | `node automation/itch_notifications.mjs --filter all` | 20 rows, **0 mentioning Texel or the cheatsheet**. Pack board replies, follows and pack sale rows only; **no Texel sale row — still 0 sales** (`texel-watch`'s ledger, not this desk's) |
| Bluesky mentions/replies | `pixelkiln\tools\pixelkiln_social.ps1 -Mode notifications`, then **`-Mode thread` on every reply before judging it** (AT Protocol, read-only; app password in `tools\social_creds.json`) | 30 items, **3 new replies — @alimabsoute, @winterbyrne, @freddifish. All three read in full thread context and all three triaged out**; see the table above for which lane each belongs to. Zero Texel mentions, **5 days running** |
| **Texel Density Cheatsheet page** *(new 2026-09-13)* | `curl https://z3er1n.itch.io/texel-density-cheatsheet`, same counting rules as the Texel page | **0 comments.** HTTP 200, 26,549 B, zero `id="post-N"`, **"Leave a comment" form live**. Serves `texel-density-cheatsheet-letter.pdf` + `-source.zip`. **Added because 11 people have downloaded it — it is the only Texel-branded file anyone actually holds.** *Ownership caveat below* |
| **Bluesky public search** *(new 2026-09-13)* | `-Mode search -Query 'z3er1n.itch.io/texel'`, and `'texel pixelkiln'` | **0 third-party mentions.** The only posts carrying the Texel URL are our own two (3mv4rjmevvg2t, 3mvbff2zfou2d). Added because notifications only show people who **tag us**, so a buyer complaining into the void was previously invisible to this desk. *Trap below* |


**Reading the cheatsheet page is safe. Answering on it is not yet settled, and
this desk did not settle it unilaterally.** The ownership map gives *"Texel
comments"* to this desk, but it also gives *"Texel free traffic drivers"* to
`texel-funnel` — and on the Pixelkiln side the analogous rule attaches page
comments to whoever owns the listing, which here would be the funnel. Both
readings are defensible.

**Nothing turns on it today** — the page has zero comments — so the cheapest
correct move was taken: **read it** (a missed buyer question costs more than a
duplicated read, and reading changes nothing), **and stop short of claiming the
right to reply.** If a comment ever lands there, the owner must be settled
before anyone answers, because two routines answering one comment six hours
apart is exactly the failure the ownership map was written to end. Raising it is
`texel-watch`'s job; this desk may not open a ledger row.

### The trap on the new Bluesky search route

**"texel" is a standard graphics term, not our brand.** A bare `-Mode search
-Query texel` returns mostly unrelated posts, and — more importantly — several
of the top hits are people discussing **a different, pre-existing Blender texel-density
add-on**. Those are not support items, not leads, and **not to be engaged with
under any circumstances**: the standing no-rivalry rule forbids interacting with
rival pixel-art-in-Blender accounts or framing Texel against another product.
They were read, identified, and left alone this run.

Search on **`z3er1n.itch.io/texel`** (our URL, unambiguous) and
**`texel pixelkiln`** (brand-qualified) instead. Both were clean today.

### Three traps found while reading these surfaces

**`<div class="community_post` without the closing quote matches the empty
container.** Added 2026-09-12: the note below says to count
`<div class="community_post"` — drop that final quote and the pattern also
matches `<div class="community_post_list_widget …>`, the *empty* widget that
wraps the post list. This run got `1` from the loose form on a page with zero
comments, and looked at the match before believing it. Keep the closing quote,
or count `id="post-N"`, which has no such twin.

**Grepping the page for `community_post` counts CSS, not comments.** The Texel
page HTML contains **11** literal `community_post` strings at offsets 6250–7105
and every one of them is a selector in the inlined stylesheet
(`.game_comments_widget .community_post .post_footer a{…}`). A raw count reads as
"11 comments" on a page with none. Count `id="post-N"` or `<div class="community_post"`
instead — this desk nearly logged a phantom queue on day 3.

**A devlog post URL must be fetched with `curl -L`.** The short form
`/texel/devlog/<id>/x` returns **301** with a zero-byte body, which parses as "0
comments" for the same reason an unplugged microphone is quiet. Follow the
redirect, or use the full slug from the index.

### History worth keeping

- **2026-09-09:** the devlog index was **404** at 08:15 — no devlogs existed yet;
  the v0.1.0 launch post was published later that day, turning a dead surface
  into a live one.
- **2026-09-10:** post 1658363 (v0.2.0, published 00:18 UTC) was discovered by
  this desk rather than announced to it — **a devlog can appear between runs, so
  the index is re-read every run rather than the known post list.**

**`automation/itch_comments.mjs` does NOT read comments** — despite the name it
reads and sets `game[community_type]`, the setting that decides whether a page
*has* a comment form. Comments are read from the public page HTML. Noted because
the task brief names it as a collector and it is not one.

**Bluesky is signed out in Chrome** (`claude-in-chrome` on `bsky.app/notifications`
renders Create account / Sign in). That is not a blocker: the AT Protocol route
above needs no browser session. Signing in would be a credential action and no
routine will take it.

---

## Doc disagreement found 2026-09-09 — RESOLVED, verified 2026-09-10

`ROADMAP.md` opens with *"v0.1.0 is built and install-verified; it has not
shipped"* and marks v0.1.0 **"Status: BUILT. Blocked on three user decisions."**
Both are stale: `LISTING.md` records the page **LIVE since 2026-09-09** at
https://z3er1n.itch.io/texel (game 4991926, $9.95, AI disclosure Yes + Code +
Graphics), all three decisions settled, and the live page returns 200. Left for
`texel-release` (Wednesday) to tick, since it owns that file — flagged here so
it is not discovered twice.

**Fixed before Wednesday.** `ROADMAP.md` now opens *"Last ticked 2026-09-09 by
`texel-release`. v0.1.0 and v0.2.0 are live at https://z3er1n.itch.io/texel."*
Re-read 2026-09-10; nothing further owed here.


---

## The answer key: what is actually in each shipped zip (2026-09-10)

Built because §D of this desk's brief forbids claiming a feature that is not in
the uploaded zip, and there was no per-version list to check an answer against.
Counted by installing each **shipped zip** into Blender 4.5.9 `--factory-startup`
and reading `dir(bpy.ops.texel)` after a real `register()` — an operator that
fails to register is not an operator, and only registration knows the difference.

| Shipped zip | Registered operators |
|---|---|
| `texel-0.1.0.zip` | **94** |
| `texel-0.2.0.zip` (the only file the live page offers) | **95** |

**The difference is exactly one operator: `texel.selection_transform`.** Set
difference both ways — 0.2.0 is a strict superset of 0.1.0, nothing was removed.
The full 95-line list is reproducible with the command above; no operator name
should be quoted to a buyer from memory or from the working tree.

The counter is saved as **`count_zip_ops.py`** next to the existing
`count_ops.py` (which counts the *working tree* — the wrong number to quote a
buyer, and the trap this desk nearly fell into):

```
blender --background --factory-startup --python count_zip_ops.py -- dist/texel-0.2.0.zip
```

### The 94-vs-95 question, settled — it is NOT a defect

The live v0.1.0 devlog says *"94 operators"*; the live store page says
*"95 operators"*. That is the exact shape of T-005, which was a real
contradiction, so it is worth stating plainly why this one is not:

**Both numbers are correct for the version each describes.** The devlog is a
v0.1.0 post and 0.1.0 really did register 94; the page sells 0.2.0, which
registers 95. No edit is owed to either surface, and **a future run should not
re-open this.** A buyer arriving through the v0.1.0 devlog is also not misled:
they can only download 0.2.0, which contains every operator that post advertises
plus one.

---

## Published later on 2026-09-09, at the user's direction

Out of this desk's normal lane, and recorded here so the next run does not
re-derive it:

- **Launch devlog published** — https://z3er1n.itch.io/texel/devlog/1658358/texel-010-pixel-art-painting-for-blender-with-texel-density-that-actually-gets-measured
  Classification "Major Update or Launch". Verified live logged-out (HTTP 200,
  no draft marker), and the devlog index moved 404 → 200. **Every claim in it was
  checked against `dist/texel-0.1.0.zip`, not the working tree** — which matters,
  because the tree has since moved to an unshipped 0.2.0. 94 operators counted in
  the shipped zip; the keymap (B/E/L/U/C/F/I/M/D) and the Pixel Perfect lookahead
  fix are both in it.
- **Bluesky launch post** — https://bsky.app/profile/pixelkiln.bsky.social/post/3mv4rjmevvg2t
  Logged with its visuals and the 21-day reuse date in `promo/POSTED.md`.

**A devlog emails everyone who owns or follows the project.** Texel has 0
downloads, so this one reached Pixelkiln's followers rather than buyers — but it
is the first inbound-generating event the product has had, so **the next run
should expect the support queue to stop being empty** and should check the devlog
comment thread as well as the page.

**2026-09-10: it did not.** Still zero inbound on every surface, and the itch
inbox shows no Texel sale row — 0 downloads, 0 questions, two days in. That
prediction was wrong and is recorded as wrong rather than quietly dropped: a
devlog to pack followers does not convert into tool questions.

### One inbound-adjacent signal, and why it is weaker than it looks

Overnight 2026-09-10, hours after the Texel launch post, two **domain-verified**
Blender press accounts followed @pixelkiln.bsky.social:
**@blendernation.com** (BlenderNation, 8.3k followers) at 01:30 and
**@blenderartists.org** (Blender Artists, 9.5k) at 01:00.

Stated straight: **this is thin evidence of editorial interest.** Both follow
back very liberally — 23.8k and 22.6k accounts followed respectively — so a
follow from either is close to automatic and should not be reported as "the
Blender press noticed Texel."

What is *not* thin is what BlenderNation's own bio says: **"To get featured,
submit your stories here: blendernation.com/submit-news/"** — a named, free,
open submission channel aimed squarely at Blender add-ons, i.e. exactly Texel's
buyers rather than Pixelkiln's pixel-art followers. **That is a traffic lead, and
it belongs to `texel-funnel` (free traffic drivers), not to this desk.** Named
here and stopped, per the ownership map. This desk opens no ledger row —
`texel-watch` is the only routine that may.

## Also found 2026-09-09, not fixed then — RESOLVED, verified 2026-09-10

`dist/texel-0.1.0.zip` — the shipped file buyers download — contains a
`ROADMAP.md` whose first line reads *"v0.1.0 is built and install-verified; it
has not shipped."* A buyer who opens the zip reads that the thing they just
bought has not shipped. It is stale rather than false, and correcting it means
rebuilding and re-uploading the zip, which is `texel-release`'s gate to run, not
this desk's. **Flagged for Wednesday.**

**Verified closed 2026-09-10, against the live page rather than against the
claim that closed T-003.** The `uploads` block on https://z3er1n.itch.io/texel
offers exactly one file — `texel-0.2.0.zip`, 187 kB — so the 0.1.0 zip is no
longer reachable by any buyer. And the ROADMAP.md *inside* `texel-0.2.0.zip`
opens with "v0.1.0 and v0.2.0 are live", not the stale line. Both halves checked;
no buyer can now download a zip that says the product has not shipped.

