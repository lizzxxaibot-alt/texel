# Texel by Pixelkiln — operations

**Written 2026-09-09.** The standing schedule that runs the product after
launch: who watches it, who answers buyers, who markets it, who ships the next
version, and what drives traffic in for free.

Texel ships **under the Pixelkiln itch account and the Pixelkiln Bluesky
account** — same brand, same audience, adjacent product. A pixel-art buyer who
already trusts Pixelkiln for assets is the exact person who needs a pixel-art
tool. That is the whole reason for not spinning up a new identity.

---

## 1. The five Texel routines

Slotted around the six existing Pixelkiln tasks so nothing collides.

| Task | When | Owns | Must never |
|---|---|---|---|
| `texel-watch` | daily **06:45** | Health of the listing + the numbers ledger + roadmap slippage | fix, post, build, or answer anything |
| `texel-support` | daily **08:15** | Every buyer question, comment, bug report, refund request | promise a date, or answer a bug it has not reproduced |
| `texel-marketing` | daily **15:15** | One Bluesky beat from the calendar; itch page conversion work | reuse a visual inside 21 days |
| `texel-release` | **Wed 10:00** | Advancing `ROADMAP.md` — build, gate, ship, devlog | ship with a red gate |
| `texel-funnel` | **Fri 10:00** | Free traffic drivers that lead back to Texel | ship a freebie with no beat to announce it |

`pixelkiln-watch` (06:00) is amended to watch these five as well, so there is
one watchguard over eleven routines rather than two partial ones.

**The times above are nominal.** The scheduler adds a few minutes of jitter, and
a task can be moved without this table being updated — the same drift that made
STATE.md wrong about the marketing cadence for a week. **Read the live schedule
from `list_scheduled_tasks`, not from here.**

### Why the split is this way
- **Support is separate from marketing** because a tool generates questions a
  pack never does ("does it work on 4.2?", "my UVs are wrong"), and an unanswered
  question on a paid tool is worse than no post at all.
- **Release is weekly, not daily**, because a version bump every day is noise and
  the gate (16 suites + install test) is the expensive part.
- **Watch does no work.** Same rule as `pixelkiln-watch`: a watchguard that
  starts fixing things stops being able to judge.

---

## 2. Files each routine keeps

| File | Owner | What it is |
|---|---|---|
| `LEDGER.md` | `texel-watch` | One row per day: views, downloads, sales, revenue, conversion. Never edited by anything else. |
| `SUPPORT.md` | `texel-support` | Every question asked, the answer given, and the tally of what people keep asking. **This is the demand signal that reorders `ROADMAP.md`.** |
| `promo/QUEUE.md` | `texel-release` writes, `texel-marketing` consumes | Marketing beats waiting to be posted, each with its asset path |
| `promo/POSTED.md` | `texel-marketing` | What went out, when, with which visual — the 21-day reuse guard |
| `ROADMAP.md` | `texel-release` | The upgrade ladder; ticked with real ship dates |
| `funnel/LOG.md` | `texel-funnel` | Each free drop, its page, and the click-through it produced |

---

## 3. The Bluesky content calendar

One post per day, rotating. Same account as Pixelkiln, so Texel posts must not
crowd out pack posts — **Texel takes Mon/Wed/Fri/Sun, packs keep Tue/Thu/Sat.**

| Day | Beat | Asset |
|---|---|---|
| **Mon** | One capability, one clip, 6s | a cut from `promo/shot-*.mp4` |
| **Wed** | Release or WIP note, tied to `texel-release` that morning | devlog screenshot or a diff |
| **Fri** | Sprite/animation beat | `promo/anim/Torchbearer.gif`, sheet, or a cel-grid crop |
| **Sun** | The best-looking render of the week | a still from `store/stills/` |

**Saturday moved to Sunday, 2026-09-09.** This table claimed Sat for Texel while
`pixelkiln/launch/marketing_plan.md` claims Sat for `#screenshotsaturday` on the
packs. Both routines post to the **same Bluesky account** and neither can see the
other from inside, so both believed they owned it — `pixelkiln-watch` run 8 caught
it two days before it landed. The packs' plan predates the split, so Saturday is
theirs and the hashtag goes with it.

**The asset library, after the 2026-09-09 cleanup:** 24 MP4s in `promo/`, **57
stills in `store/stills/`** (shot_*, env_*, ui_* — roughly fourteen weeks of
non-repeating posts), the animated GIF, sheet and JSON in `promo/anim/`, the
painted tiles in `promo/shots/*/tile_*.png`, and the walk sprite frames in
`promo/shots/*/sprite/`. **3.39 GB of raw render frames were deleted** — they had
already been encoded and harvested. Need a new angle? Re-render with
`gameshots.py`; do not re-post a still early.

**Hashtags that actually reach this audience:** `#gamedev` `#indiedev`
`#pixelart` `#b3d` `#blender` `#lowpoly` `#gamedevtools`. **Not `#screenshotsaturday`** - that tag belongs to the packs' Saturday post on the same account.
Three to five, never a wall.

**The tactics that work for a gamedev tool, in priority order:**
1. **Show the problem before the product.** A clip of pixel size drifting across
   a model, then the same model after Apply Density. Nobody buys "texel density
   measurement"; everybody recognises the drift.
2. **Numbers, not adjectives.** "8-frame walk cycle, 4 cel tracks, 64×64" beats
   "powerful animation tools."
3. **The workflow, not the feature.** Post the 20 seconds where a thing gets
   made, not a list of what the sidebar contains.
4. **Name the genre.** "metroidvania corridor", "isometric ARPG floor",
   "top-down RPG street" — the buyer is searching for their own game.
5. **Reply more than you post.** Answering a real question in someone else's
   thread outperforms a promo post, and it is how the account stops reading as
   a billboard. This is the whole reach strategy — see §3a.

**Never:** promise earnings, imply an endorsement, post the same visual twice
inside 21 days, or post a feature that is not in the shipped zip.

---

## 3a. Reach comes from replies, not from more posts

**The measurement that settles this (2026-09-09):** posts about pixel art in
Blender can take **~874 likes** on Bluesky. Ours take **6-18**. That gap is the
size of the topic's audience, not the quality of our posts — the people
interested in this are on the platform in numbers we are not reaching.

**The gap cannot be closed by posting more.** `marketing_plan.md` caps the whole
account at 3-4 posts a week and Texel only gets four days of it; on 2026-09-09
the account was already at **6 posts in 7 days** and a queued beat had to move.
Posting is a rationed channel with a hard ceiling.

**Replies have no ceiling.** They put us in front of people who are already
talking about the exact problem, on their post, in their audience's feed, at the
moment they care. Two useful replies reach more of the right people than a fifth
post reaches of the wrong ones.

**So the target is a floor, not a nice-to-have: two genuine replies every run,
and more is better. A run that posts nothing and replies twice is a successful
run.**

### The voice — a peer in the community, never a salesperson

Every one of these is a rule, because the failure mode is drifting into pitch:

1. **Answer as someone who hit the same problem**, not as someone with a product.
   The test before sending: *would this reply be worth reading if we sold
   nothing?* If no, do not send it.
2. **Supportive and friendly by default.** People are showing work in progress.
   Meet them where they are, be glad about what is working, and never open by
   correcting.
3. **Never pushy.** No pitch, no link, no "we built a tool for that" — **do not
   mention Texel at all** unless the question is literally what Texel does. If
   someone asks what we make, answer plainly once and stop.
4. **Specific beats supportive-generic.** "Nice work!" costs nothing and returns
   nothing. Bring a number, a setting name, a file path, a thing that was
   measured. The reply that lands is the one that saves them an afternoon.
5. **Verify before answering** (§3 of `CLAUDE.md` applies to replies too). The
   2026-09-09 Aseprite answer was checked against Aseprite's own source before it
   was sent, not recalled from memory — that is the standard.
6. **Never correct someone publicly on something that does not cost them
   anything.** If they are wrong in a way that will cost them work, give the
   useful part without the correction framing.
7. **Never argue, never DM, never quote-post to disagree.** If a thread turns
   into an argument, leave it.
8. **Silence is free.** A thread we cannot genuinely add to gets nothing. There
   is no quota of replies worth a bad one.
9. **Never reply in another pixel-art-in-Blender product's threads** — standing
   rule, `promo/POSTED.md`. They are the highest-engagement threads available and
   they are all off limits, because anything we say in them reads as sniping
   whether or not Texel is named.

### What this is not an argument for

The reach gap says **reply more**. It does **not** say post more, price
differently, position against anyone, or monitor another account. Texel is not
in a rivalry with anything and is not derived from anything; other people's
numbers are only ever evidence about how big a topic is.

### Logging

Every reply goes in `promo/POSTED.md` under **Replies**, with the thread, what
was actually said, and the live URL — verified on the public AppView, never on
the poster's own success message. The log is what makes "two per run" auditable
instead of aspirational.

---

## 4. The free funnel

Every free drop is its own itch page (free, no email wall — itch buries gated
downloads), and every one of them ends at Texel. The rule: **a freebie must be
useful to someone who never buys, and obviously better if they do.**

| Drop | What it is | The hook back |
|---|---|---|
| **Palette Pack** | 24 `.gpl` palettes tuned for lit 3D pixel art, with a note on why a 3D palette needs more midtones than a 2D one | "Load these straight into Texel with one click" |
| **Density Cheatsheet** | A one-page PDF (Typst): what px/unit to use for 16/32/64px games, with the arithmetic shown | The number it tells you to use is the number Texel's Apply Density takes |
| **Starter Tiles** | 8 seamless 64px tiles + the `.blend` they are applied in, CC0 | The .blend opens with Texel's canvas already bound; editing them needs the add-on |
| **Sheet Reader** | MIT snippets that read Texel's `_anim.json` in Godot and Unity | Useless without something producing that JSON |
| **Showcase Presets** | Extra lighting/camera preset JSON for the Showcase panel | Only loads inside Texel |

**Cadence (changed 2026-09-09, user): weekly Fridays through the launch push,
then the first Friday of the month.** Front-loaded rather than even, because the
`newest` and `newest/free` feeds are the biggest external source this store has
(46 + 12 visits, ahead of every other off-site referrer) and a feed slot is
worth most while the paid page is new and has no ratings. Five drops are
queued, so the push is about five weeks.

Moved off Saturday because Saturday is `#screenshotsaturday` — the one beat with
a built-in audience, and a drop should not compete with it.

**Every drop is gated on distribution, not on the calendar.** No marketing beat
available that week means no drop. The evidence is HUD Vol. 6's free sample: **5
views, 0 downloads**. An unpromoted free page is not a funnel, and it is not
free either — itch's storefront grid is newest-first with **no pinning**, so
every drop pushes Texel and every paid pack one slot further down the shop.

**Measurement:** `funnel/LOG.md` records the free page's views and the Texel
page's referral bump in the 72h after. A drop that moves nothing twice is
retired, not repeated.

---

## 5. Answering buyers — the rules `texel-support` runs on

1. **Reproduce before answering.** A bug report gets a run in Blender 4.5.9
   against the shipped zip. If it reproduces, say so and give the version it will
   be fixed in. If it does not, ask for the .blend, do not argue.
2. **Never promise a date.** Say which version it is queued for; `ROADMAP.md`
   dates are targets and the store page says so.
3. **A refund request is granted.** No interrogation, no retention attempt. Log
   the reason in `SUPPORT.md`; three of the same reason is a product bug.
4. **Escalate to the user, never decide alone:** anything touching money beyond a
   refund, a licence dispute, a takedown claim, an accusation of copying, or a
   request to add a paid tier.
5. **Tally every question.** The support tally reorders `ROADMAP.md`. If eleven
   people ask for Aseprite round-trip, it moves up regardless of the plan.
6. **Answer in one paragraph.** A wall of text on a $9.95 tool reads as
   defensiveness.

---

## 6. Escalation — what stops a routine and wakes the user

- The itch page is down, unpublished, or the price is wrong
- A payout or tax form is requested (**no routine ever fills one**)
- A login or password is needed (**no routine ever types one**)
- A DMCA, licence, or plagiarism claim
- A crash report that reproduces on the shipped zip → `texel-release` is
  interrupted and a patch release jumps the queue
- Two consecutive weeks with zero sales after 30 days live → the picks-and-
  shovels test has failed for this product and that is a decision, not a fix

---

## 7. The honesty rules, restated because marketing is where they slip

- **AI disclosure on itch is Yes + Code + Graphics.** Different from the packs'
  Graphics-only, because this product's substance is code. Never softened.
- **GPL-3.0-or-later.** Source ships in the zip. Buyers may redistribute; that is
  the licence and the page says so plainly rather than hoping nobody notices.
- **Never claim a feature that is not in the uploaded zip**, including in a
  screenshot. Every listing image is regenerated when the feature set changes.
- **Never claim compatibility that was not tested.** The page says Blender 4.2+;
  4.5.9 is what the suites actually run against, and the page says that too.
- **"Made with Texel" is only said of things Texel actually made.** The promo
  renders are lit and composed by unshipped scripts; the claim is *"every texture
  in this video was painted with Texel"*, which is true and checkable.
