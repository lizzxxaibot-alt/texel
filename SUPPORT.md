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

**Top three this run:** none — zero inbound items since launch.

**Does the tally disagree with `ROADMAP.md`'s order?** No. It cannot yet: there
is no demand signal at all, so the roadmap's "easiest first" ordering stands
unchallenged on its own reasoning rather than on evidence. **The first three
questions Texel ever receives are worth more than the whole plan**, so they get
logged the day they arrive.

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

---

## Surfaces checked each run, and how

Recorded so a later run does not have to rediscover the access route.

| Surface | How it is read | Result 2026-09-09 |
|---|---|---|
| Texel itch page comments | `curl https://z3er1n.itch.io/texel`, then the `game_comments_widget` block | **0 comments.** Widget renders "Leave a comment / Log in with itch.io" — the form is live, so silence is silence, not a broken channel |
| Texel devlog replies | `curl https://z3er1n.itch.io/texel/devlog` | **404 at 08:15 — no devlogs existed.** The v0.1.0 launch devlog was published later the same day (post 1658358); from the next run this is a live surface with its own comment thread |
| itch notification inbox | `node automation/itch_notifications.mjs --filter all` | 21 rows, **0 mentioning Texel**. All are Pixelkiln pack board topics, owned by `pixelkiln-itch-boards` |
| Bluesky mentions/replies | `pixelkiln\tools\pixelkiln_social.ps1 -Mode notifications` (AT Protocol, read-only; app password in `tools\social_creds.json`) | 33 items: 24 likes, 4 reposts, 4 follows, **1 reply**. The reply (@gamebrief, 09-08) is about the Icons Vol. 2 chestplate and was already answered 09-09; it is a pack question, not Texel |

**`automation/itch_comments.mjs` does NOT read comments** — despite the name it
reads and sets `game[community_type]`, the setting that decides whether a page
*has* a comment form. Comments are read from the public page HTML. Noted because
the task brief names it as a collector and it is not one.

**Bluesky is signed out in Chrome** (`claude-in-chrome` on `bsky.app/notifications`
renders Create account / Sign in). That is not a blocker: the AT Protocol route
above needs no browser session. Signing in would be a credential action and no
routine will take it.

---

## Doc disagreement found this run

`ROADMAP.md` opens with *"v0.1.0 is built and install-verified; it has not
shipped"* and marks v0.1.0 **"Status: BUILT. Blocked on three user decisions."**
Both are stale: `LISTING.md` records the page **LIVE since 2026-09-09** at
https://z3er1n.itch.io/texel (game 4991926, $9.95, AI disclosure Yes + Code +
Graphics), all three decisions settled, and the live page returns 200. Left for
`texel-release` (Wednesday) to tick, since it owns that file — flagged here so
it is not discovered twice.

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

## Also found, not fixed

`dist/texel-0.1.0.zip` — the shipped file buyers download — contains a
`ROADMAP.md` whose first line reads *"v0.1.0 is built and install-verified; it
has not shipped."* A buyer who opens the zip reads that the thing they just
bought has not shipped. It is stale rather than false, and correcting it means
rebuilding and re-uploading the zip, which is `texel-release`'s gate to run, not
this desk's. **Flagged for Wednesday.**

