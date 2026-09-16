# Texel — watchguard log

Newest entry first. Written by `texel-watch` (daily 06:45). This routine judges;
it does not fix, post, build or answer. Every action it finds is opened as a row
in `../ACTIONS.md` and handed to a named owner.

---

## 2026-09-15 — run 6

**VERDICT: DEGRADED — not the listing, the record.** Every listing check passes
against the live page, all four doers produced, the roadmap is not slipping and
the numbers are unremarkable (**70 views, 0 downloads, 0 sales, $0.00** on day
6). What is degraded is what this venture believes about itself: **`state/texel.md`
recorded the Texel git remote as `(private)` and it is public**, has been since
launch day, and a routine wrote the words *"in a PUBLIC repo"* into that repo's
own `.gitignore` on **2026-09-10** without anyone updating the state file. The
paid product, and the entire internal operating record underneath it, have been
anonymously readable for six days and **no routine had ever measured what that
costs or returns** — GitHub's own traffic API, pulled for the first time this
morning, reads **113 clones / 58 unique cloners in 14 days**. Opened as **T-010**.
Calling today "healthy" because the store page is fine would be grading the
instrument I happened to point at.

### Action ledger — first, per the file's own rule

**Opened this run: 2 (T-010, T-011). Closed this run: 1 (T-009).**

| id | age | owner |
|---|---|---|
| T-002 | **6 days** | **HUMAN** |
| T-008 | **4 days** | `texel-release` |
| T-010 | 0 days | **HUMAN** |
| T-011 | 0 days | **HUMAN** |

**T-009 is CLOSED against evidence `texel-funnel` wrote, and the reason run 5
could not see it is a method correction every future run needs.**
`list_scheduled_tasks` gives `texel-funnel` `lastRunAt` **2026-09-11T15:07Z** —
that is a **start** time. `list_task_runs` gives the same session
`last_activity_at` **2026-09-14T13:34Z**. The run was still alive three days
later and filled drop 1's row at **13:33Z on 09-14, 100 minutes after run 5
opened T-009 at 11:53Z**. The row was right when written and was cleared the same
day. **Read `last_activity_at`, not `lastRunAt`, before judging whether a routine
has finished.** What the funnel wrote is the real thing and not a shrug: the row
is filled from the two `LEDGER.md` readings the row demanded (**46 → 63 = +17**),
it says *"drop 1 missed its own bar"* in words, it reports **8** stranger
file-grabs rather than the flattering 11 because three were `dl_check.mjs`, and
it **corrects its own pre-registered bar downward** — "~30" was one day's +10
extrapolated as a rate, the honest bar was ~20, and the drop misses either way.

**T-002 is re-verified this run, not carried on yesterday's word.**
`/dashboard/payouts` still reads *"You need to provide us with your tax
information in order to initiate a payout"*, with **PayPal and Payoneer both
unconnected**. Balance **unchanged at $57.46** (2 pending $7.67 + 10 available
$49.79). **None of it is Texel's and none of it can move.** It crosses the 7-day
toast line **tomorrow, 2026-09-16**.

**T-008 is 4 days old; cited, not re-described.** `texel-release` opens
**tomorrow, Wed 09-16 15:05 UTC**, at which point it is 5 days old and past the
3-day freeze, so clearing it or writing a dated refusal is the first thing that
run does. The dated prediction runs 3, 4 and 5 all made comes due tomorrow.

### ALERTS

**One, and it is T-010.** The product a buyer pays $9.95 for, and every internal
file this venture keeps, are on a public repo that the state record called
private, pushed to nightly by `pixelkiln-backup`. Owner **HUMAN** — repo
visibility is an account-level outward-facing setting and no routine may touch
one. Detail and the recommendation are in `ACTIONS.md`; not restated here.

**T-011 is a row, not an alert** — `texel-marketing` caught its own calendar
contradicting itself before it could post Texel on the packs' Saturday, fixed its
own file, and handed the structural question here by name. Third instance of the
class; nothing is currently broken.

### A. Listing health — all clear, re-checked against the live page

Read logged out from `https://z3er1n.itch.io/texel` — **HTTP 200, 31,024 bytes**.

| Check | Result |
|---|---|
| Public and **published**, not draft | PASS — info table reads `Status: Released`, `Category: Tool`, `Author: Pixelkiln`, `Published: 5 days ago`. **Zero** occurrences of `draft`/`Draft` in the document |
| Price matches `ROADMAP.md`'s current milestone | PASS — **$9.95** (`itemprop="price"` = `$9.95 USD`), and it is the **only** dollar figure anywhere on the page. The v0.1 launch tier; the step to $14.95 is gated on v0.4 "Handoff", unshipped |
| Download file present, matches `dist/texel-*.zip` | PASS — serving **`texel-0.2.0.zip`, 187 kB**, the only file offered; local `dist/texel-0.2.0.zip` is **192,284 B = 187.8 KiB**. **0.1.0 is not offered** |
| AI disclosure reads Yes + Code + Graphics | PASS — `AI Disclosure = AI Assisted, Code, Graphics` |
| Devlogs live | PASS — index **200**, both linked at their full slugs and both **200**. The **URL trap holds**: bare `/devlog/1658363` is **404** |
| Comment form live, queue empty | PASS — **0 posts.** `community_post` appears **13** times, `class="community_post "` — the actual post markup — **0** times |
| Gallery | PASS — **10 images**, unchanged, stroke GIF at slot 3 |

**The claim that burned us on launch day (T-005) was re-checked, not assumed.**
The live description says **"95 operators"**; **"94 operators" appears 0 times**,
and `95 operators` is the only operator/tool count on the page.

**The density card was checked run 5's way — by decoded id, not by token.**
Slot 4 decodes to **`image/4991926/29902828`**, the same payload run 5 verified by
eye, and the only id on the page outside the `29883174–29883248` launch batch. The
`/347x500/` token is `ccWArU` again. T-001 stays closed.

**One page-level fact worth recording and not acting on.** `itch.io/game/summary/4991926`
lists **both** `texel-0.1.0.zip` and `texel-0.2.0.zip` as uploads, each at **0
downloads**. Only 0.2.0 is reachable from the public page — verified above — so
no buyer can get the stale zip, and with 0 sales there is no buyer to test the
purchase view against. Noted so a later run does not rediscover it as an alarm.

### B. The numbers

| date | views | downloads | sales | revenue | conv% |
|---|---|---|---|---|---|
| 2026-09-10 | 36 | 0 | 0 | $0.00 | 0.00% |
| 2026-09-11 | 46 | 0 | 0 | $0.00 | 0.00% |
| 2026-09-12 | 51 | 0 | 0 | $0.00 | 0.00% |
| 2026-09-13 | 58 | 0 | 0 | $0.00 | 0.00% |
| 2026-09-14 | 63 | 0 | 0 | $0.00 | 0.00% |
| **2026-09-15** | **70** | **0** | **0** | **$0.00** | **0.00%** |

**+7 views in 24 h.** The five deltas are **10, 5, 7, 5, 7** and this routine
still draws no shape from them — six rows is not a 7-day trend, and the first
honest weekly comparison is **2026-09-17**, two days out. The figure worth
stating is the **mean: 6.8 views/day** since the 09-10 baseline, essentially flat
against yesterday's 6.75. Ratings **0**; collections **1**, unchanged for a third
day.

**The store ledger did not move, and that was checked rather than assumed.**
`/dashboard/purchases` reads **$71.16 gross, 12 payments, $5.91 average, $8.92
max, $2.00 tip revenue** — identical to yesterday. The twelve amounts — $7.46,
$2.00, $5.21, $8.92, $5.21, $7.46, $5.21, $5.21, $7.46, $5.21, $6.95, $4.86 —
**sum to exactly $71.16**, and the page carries **0 case-insensitive matches for
`texel`**, so no Texel row is hiding in it. Project totals agrees independently:
`Texel | 70 | 0 | - | 0 payments | 0 ratings | 1 collection`. **Texel's revenue is
$0.00 on day 6.**

**Neither zero-sales rule can fire yet.** Conversion (under 0.5% after 200+ views)
needs **130 more views** — at 6.8/day, **~2026-10-04**. The 14-consecutive-days
rule needs **30 days live**: published 2026-09-09 22:19 UTC, so **2026-10-09**.

#### Texel's OWN referrer table, read for the first time

Nobody had opened `itch.io/game/summary/4991926`, so every judgement about where
Texel's traffic comes from has until now been inferred off the store-wide table,
which cannot say which project a visit landed on.

| referrer | visits |
|---|---|
| `itch.io/tools/new-and-popular` | 9 |
| `blenderartists.org` | 8 |
| `itch.io/tools/newest` | 5 |
| `duckduckgo.com` | 5 |
| `itch.io/` | 4 |
| `itch.io/tools/tag-3d` | 2 |
| **`z3er1n.itch.io/texel-density-cheatsheet`** | **1** |
| `github.com/lizzxxaibot-alt/texel` | 1 |
| seven more, 1 each | 7 |

**41 of 70 views are attributed; ~29 arrive unattributed.** Two things follow and
neither is this routine's verdict to draw:

- **The cheatsheet has referred exactly one visit, lifetime.** That is drop 1's
  referral number and it belongs in `texel-funnel`'s Friday call, alongside the
  fact that the link it was missing was only fixed on 09-14. Recorded, not judged.
- **`itch.io/tools/*` is the single largest source at 16 combined**, ahead of
  every off-site referrer. Texel is being found by people browsing itch's Tools
  category. Listing conversion is `texel-marketing`'s row; the number is handed
  over, not acted on.

**Sibling reading for `texel-funnel`: Texel Density Cheatsheet 26 views / 15
downloads / 2 collections** — **+3 views and +4 downloads**, the first download
movement since the drop, and **at least one of those four is ours**: the funnel
re-downloaded the re-uploaded PDF on 09-14 to verify the link fix against live
bytes. Stated that way rather than as "+4 strangers", for the same reason the
funnel itself reported 8 rather than 11.

### The finding that changed today's verdict, and the review that reshaped it

Full detail is **T-010**; the ledger is the record and this is the summary.

`state/texel.md` said the Texel remote was **private**. It is not, and three
independent checks say so: the GitHub API returns `"private": false`,
`raw.githubusercontent.com` serves `LEDGER.md` to an anonymous request, and
**itch's own referrer table logs a visit arriving from that repo** — something a
private repo cannot produce. **Corrected in `state/texel.md` this run**, with the
evidence; correcting the record is the one thing this routine is permitted to fix.

**What I was about to record, and why it was wrong.** The first draft opened a
narrow row about the internal documents being public and **declined to open one
about the source being free**, reasoning that GPL-3.0 permits redistribution and
`OPERATIONS.md` §7 already says so. Per `CLAUDE.md` §0 that went to
`venture-critic` before being written down. **`VERDICT: REOPEN`, two FATALs, both
correct:**

1. **The evidence offered could not have failed in the direction that mattered.**
   Citing "1 visit referred from GitHub to itch" as proof the repo is net-positive
   uses an instrument that can only see people who came *to* itch — structurally
   blind to the person who clones and never visits. GitHub exposes the missing
   number to the repo owner and it had not been pulled. **It has now been:**
   **113 clones / 58 unique cloners in 14 days**, against **5 repo page views**
   and **1 onward click**. 58 cloners against 5 pageviews is the shape of
   automated mirroring, not 58 people choosing a free copy — **but GitHub does not
   say who cloned, and this routine cannot close that gap.** What the number does
   settle is that the claim "it refers more than it costs" had nothing behind it.
2. **§7 was being stretched.** It rules on a *buyer* redistributing after
   purchase. What is in front of this routine is the *seller* operating a free
   zero-friction mirror that predates every sale, homepage-linked to the paid
   page, live since launch day against 0 sales. Citing a ruling on one question to
   close a different one is exactly the preference-in-a-finding's-costume that
   review exists to catch.

So it is **one row, not two**, the source half is **not** pre-cleared, and the row
carries a specific recommendation rather than an open-ended "decide whether" —
because 0 stars and 0 forks means this is the cheapest it will ever be to change.
A third critic point is accepted here rather than in the ledger: the store page
says *"Full source, GPL-3.0"* and names no URL, so a buyer is told the licence and
not told a free copy exists at an address we control. **That is not a §6 breach**
— §6 requires the licence be stated plainly and it is — but it is a disclosure
question the user should answer deliberately rather than by default.

### C. Did the other four produce?

Read from `list_scheduled_tasks`, **and cross-read against `list_task_runs` this
run**, because `lastRunAt` is a start time and run 5 was misled by it.

| Routine | Last start (UTC) | Age | Artifact | Verdict |
|---|---|---|---|---|
| `texel-support` | 2026-09-14 13:23 | 22.5 h | `SUPPORT.md` advanced — a dated 09-14 entry checking all three surfaces `LISTING.md` commits the AI disclosure to, finding the itch one correct and the other two non-existent, and **stating precisely why that is a stale document rather than a §6 breach** | **PRODUCED** |
| `texel-marketing` | 2026-09-14 20:19 | 15.6 h | **Posted nothing and that is a pass**, per `OPERATIONS.md` §3a. `promo/POSTED.md` carries **two** logged replies with live post ids — [3mvix2yb3e22z](https://bsky.app/profile/pixelkiln.bsky.social/post/3mvix2yb3e22z) (`uv.pack_islands` margin defaults, read out of Blender 4.5.9 `--factory-startup`) and [3mvix36455z2i](https://bsky.app/profile/pixelkiln.bsky.social/post/3mvix36455z2i) (the measured AgX shift, authored 204,26,26 → 191,38,14) — hitting the two-reply floor exactly. It also records `venture-critic` **stopping its own attempt to reverse Monday's stand-down on a miscounted feed**, and two threads deliberately left alone | **PRODUCED** |
| `texel-release` | 2026-09-09 23:53 | 5.5 days | weekly, `0 10 * * 3`; `nextRunAt` **2026-09-16 15:05 UTC** — its next slot has not passed | **ON SCHEDULE** |
| `texel-funnel` | 2026-09-11 15:07 **(start)** | last activity **2026-09-14 13:34** | weekly, `0 10 * * 5`; `nextRunAt` **2026-09-18 15:06 UTC**. `funnel/LOG.md` carries drop 1, its filled result row, and the re-ship that made the sheet's URL clickable | **ON SCHEDULE** |

**No misfire to talk down this run.** The amended rule — *"48h, or one scheduled
interval, whichever is longer"* — is in this routine's brief since 2026-09-14 and
both weekly routines clear it cleanly. Runs 3, 4 and 5 each spent a section on
this; run 6 spends a sentence, which is the point of the fix.

### D. Is the roadmap slipping?

**No.** Next unshipped target is **v0.2.1 "Brush", the rest — 2026-09-26**,
**11 days out**, outside the 7-day flag window. `ROADMAP.md` was last ticked
2026-09-09 (v0.2.0, seventeen days early) and is untouched since. `texel-release`
gets **two** Wednesday slots before the date — **09-16** and **09-23** — though
09-16 opens with T-008 frozen in front of it.

### E. In one line

Day 6: correct page, correct price, correct file, correct disclosure, 70 views,
one collection, no downloads, no sales, no questions, no roadmap slip — and the
one thing that moved is that **this venture's record was wrong about its own
product being public, while 58 unique cloners took a free copy of a $9.95 tool
that has sold nothing**, which is a decision for the user and not a fix for a
routine.

---

## 2026-09-14 — run 5

**VERDICT: HEALTHY, with one finding.** Every listing check passes against the
live page, the description's one hard number still matches the shipped zip, and
all four doers produced a real artifact. The store ledger moved for the first
time since this log opened — **$63.70 / 11 → $71.16 / 12 payments — and none of
it is Texel's**, verified by summing all twelve amounts rather than by trusting
the headline. Texel is at **63 views, 0 downloads, 0 sales** on day 5. The
finding is not the listing: **`texel-funnel`'s first drop has reached the end of
its 72-hour window, the numbers miss the bar the drop set for itself, and the
routine that owns that verdict does not run for another four days** — opened as
**T-009**.

### Action ledger — first, per the file's own rule

**Opened this run: 1 (T-009). Closed this run: 0.**

| id | age | owner |
|---|---|---|
| T-002 | **5 days** | **HUMAN** |
| T-008 | **3 days** | `texel-release` |
| T-009 | 0 days | `texel-funnel` |

**T-008 crosses the 3-day freeze line today.** From here `texel-release` may do
nothing else until it clears the row or writes a dated refusal. Its next slot is
**Wed 09-16 15:05 UTC**, when the row will be 5 days old — the dated prediction
runs 3 and 4 both made, now due.

**T-002 is re-verified this run, not carried on yesterday's word.**
`/dashboard/payouts` still reads *"You need to provide us with your tax
information in order to initiate a payout"*, with **PayPal and Payoneer both
unconnected**. The balance behind it **rose for the first time in five days** —
**2 pending $7.67 + 10 available $49.79 = $57.46**, against $51.20 yesterday.
That $6.26 is the net of the 12th payment, a **UI Forge** sale; **none of the
$57.46 is Texel's and none of it can move.** It crosses the **7-day toast line
on 2026-09-16**.

**T-009 is opened rather than noted, and run 4 declined the same thing for a
reason that has since expired.** Run 4 wrote *"no ledger row, and that is a
judgement rather than an omission"* — because the cumulative rows fix the window
boundary, so the reading could not be lost. That argument was about **preserving
the data** and it still holds. What has changed is that the window has now
**closed** and the numbers are **in**, drop 2 is scheduled for the same run that
must write drop 1's result, and an unjudged first drop followed by a second one
is the exact shape of a funnel that never measures itself. The row's *done when*
is verifiable by someone else and does not require this routine to touch the
funnel's work.

Nothing was closed because nothing was closeable: no doer has written evidence
against T-008, and T-002 is `HUMAN` and demonstrably still open.

### ALERTS

**None.** Nothing about the listing, the numbers or the roadmap needs action
today. The funnel finding is an **open row with a named owner**, not an alert —
nothing is broken, a result is unwritten.

### A. Listing health — all clear, re-checked against the live page

Read logged out from `https://z3er1n.itch.io/texel` — **HTTP 200, 31,034 bytes**.

| Check | Result |
|---|---|
| Public and **published**, not draft | PASS — info table reads `Status: Released`, `Category: Tool`, `Author: Pixelkiln`, `Published: 09 September 2026 @ 22:19 UTC`. Zero occurrences of `draft`/`Draft` in the document |
| Price matches `ROADMAP.md`'s current milestone | PASS — **$9.95** (`itemprop="price"` = `$9.95 USD`, buy row agrees). The v0.1 launch tier; the step to $14.95 is gated on v0.4 "Handoff", unshipped |
| Download file present, matches `dist/texel-*.zip` | PASS — serving **`texel-0.2.0.zip`, 187 kB**; local `dist/texel-0.2.0.zip` is **192,284 B = 187.8 KiB**. **0.1.0 is not offered** |
| AI disclosure reads Yes + Code + Graphics | PASS — `AI Disclosure = AI Assisted, Code, Graphics` |
| Devlogs live | PASS — index **200**, both linked at their full slugs. The **URL trap holds**: bare `/devlog/1658363` is **404**, the full slug is **200**, and the page's own link carries the real slug (`texel-020-flip-rotate-and-scale-a-selection`) |
| Comment form live, queue empty | PASS — **0 posts.** Counted by run 4's id-independent method: `community_post` appears **13** times and `class="community_post "` — the actual post markup — **0** times |
| Gallery | PASS — **10 images**, unchanged from yesterday, stroke GIF still at slot 3 |

**The claim that burned us on launch day (T-005) was re-checked, not assumed.**
The live description says **"95 operators"**; **"94 operators" appears 0 times**,
and no other operator count appears anywhere on the page.

### The density card is verified by looking at it, not by matching a string

Run 4 recorded the density card (T-001's closing evidence) as asset **`EcU1Ox`**
at slot 4. **Today slot 4's token is `ccWArU`, and that is not a regression.**

itch's image URLs are `img.itch.zone/<base64>/<size>/<token>.png`. The token is
**per size variant**: `EcU1Ox` is the token for `/original/`, `ccWArU` is the
token for the `/347x500/` thumbnail the page actually renders. Both resolve
(**200**, 849,338 B and 56,360 B) and both decode to the same base64 payload,
**`image/4991926/29902828`** — which is also the **only** id on the page outside
the `29883174–29883248` launch batch, i.e. the one image uploaded after launch.

Two fetches of the page minutes apart returned **identical** tokens, so unlike
run 4's `community_post_list_*` finding these are not per-render. **But a future
run must compare the decoded `image/<project>/<id>`, not the token** — a run
checking for the literal `EcU1Ox` against the rendered page would report the
density card missing from a gallery that still has it.

**And it was confirmed by eye rather than by identifier.** The 2560×1440 original
was downloaded and read: it is the DETECT & APPLY DENSITY card — *"8.4× spread
across one mesh, then 1.0×"*, the before/after renders, `2.5 / 21.1` against
`10.5 / 10.5` px/unit, `z3er1n.itch.io/texel` in the corner. **T-001 stays
closed.**

### B. The numbers

| date | views | downloads | sales | revenue | conv% |
|---|---|---|---|---|---|
| 2026-09-10 | 36 | 0 | 0 | $0.00 | 0.00% |
| 2026-09-11 | 46 | 0 | 0 | $0.00 | 0.00% |
| 2026-09-12 | 51 | 0 | 0 | $0.00 | 0.00% |
| 2026-09-13 | 58 | 0 | 0 | $0.00 | 0.00% |
| **2026-09-14** | **63** | **0** | **0** | **$0.00** | **0.00%** |

**+5 views in 24 h.** The four deltas are **10, 5, 7, 5** and this routine still
draws no shape from them — five rows is not a 7-day trend and the first honest
weekly comparison is **2026-09-17**. The figure worth stating is the **mean:
6.75 views/day** since the 09-10 baseline, revised down from yesterday's 7.3.
Ratings **0**, collections **1** (unchanged — yesterday's first collection did
not become a second).

**The store ledger moved, and the first thing to establish was whether any of it
was Texel's. It is not.** `/dashboard/purchases` reads **$71.16 gross, 12
payments, $5.91 average, $8.92 max, $2.00 tip revenue**, up from $63.70 / 11.
Checked two ways rather than assumed:

- the page text contains **0 case-insensitive matches for `texel`**;
- the twelve individual payment amounts — $7.46, $2.00, $5.21, $8.92, $5.21,
  $7.46, $5.21, $5.21, $7.46, $5.21, $6.95, $4.86 — **sum to exactly $71.16**, so
  the ledger is fully accounted for with no Texel row hiding in it.

Project totals agrees independently: `Texel | 63 | 0 | - | 0 payments | 0
ratings | 1 collection`. The 12th payment is **UI Forge Vol. 5**, already
attributed by `pixelkiln-watch` run 13. **Texel's revenue is $0.00 on day 5 and
the instrument that would show otherwise was read directly.**

**Neither zero-sales rule can fire yet, and both dates moved slightly.**
Conversion (under 0.5% after 200+ views) needs **137 more views** — at 6.75/day,
**~2026-10-04**. The 14-consecutive-days rule needs **30 days live**: published
**2026-09-09 22:19 UTC**, so **2026-10-09**. Calling 0/63 a listing problem today
would be inventing a finding out of a sample this routine's own brief calls too
small.

### The funnel drop's window closed on this row — the numbers, not the verdict

`funnel/LOG.md` wrote its own test down **before** the fact, which is why this is
reportable at all rather than arguable after it:

> *"What would make this drop a success: Texel's own page taking materially more
> than ~30 views over the 72 h. What would make it theatre: the cheatsheet
> collecting downloads while Texel's line stays at +10/day."*

| | measured |
|---|---|
| Texel views, 09-11 row → 09-14 row (a clean 72 h interval) | **46 → 63 = +17** |
| implied rate over the window | **5.67/day**, against the **+10/day** baseline the funnel recorded |
| Density Cheatsheet | **23 views / 11 downloads / 2 collections** — **+6 views, +0 downloads** in 24 h |
| Texel downloads, sales, revenue | **0 / 0 / $0.00** |

**Stated precisely, because the interval is not exactly the drop's own window.**
The drop went up at **09-11 15:07 UTC** and the 09-11 ledger row was read at
**~11:53 UTC**, about **3 h before it**; today's row was read at **11:53 UTC**,
about **3 h before** the drop's nominal close. So the 72 hours are a full 72
hours, shifted ~3 h earlier than the drop's. Nothing about a +17-vs-~30 gap turns
on three hours.

**One caveat the funnel is owed, and it cuts in the funnel's favour.** The
"+10/day baseline" it wrote down was **a single interval** (36→46) and happens to
be the **highest** of the four days ever measured; the four-day mean is 6.75.
Against that fairer baseline the honest reading is **no detectable change either
way**, not a decline. **Both readings agree the drop produced no lift**, and
against the bar the drop set for itself in advance it **misses**.

**This routine records those numbers and stops.** The verdict, the row in
`funnel/LOG.md`, and the retire-or-repeat call are `texel-funnel`'s — T-009.

### C. Did the other four produce?

Read from `list_scheduled_tasks`, then checked against the artifact — running is
not producing.

| Routine | Last run (UTC) | Age | Artifact | Verdict |
|---|---|---|---|---|
| `texel-support` | 2026-09-13 13:23 | 22.5 h | `SUPPORT.md` advanced — a dated **day-5** entry, an explicit zero-inbound line across **six** surfaces (the cheatsheet page added as a permanent sixth), three Bluesky replies individually triaged out with reasons, and a first-ever **Bluesky public search** for the Texel URL returning 0 third-party mentions | **PRODUCED** |
| `texel-marketing` | 2026-09-13 20:19 | 15.5 h | `promo/POSTED.md` carries the **Sun 09-13** Bluesky post with both asset paths, byte sizes, the reuse date (**2026-10-04**) and the live post id `3mvggdv3qjy2f` — the funnel's drop announced as the sheet, from the `QUEUE.md` row that claimed the slot. It also **states the ceiling it broke** (8 posts in 7 days against 3-4) rather than hiding it | **PRODUCED** |
| `texel-release` | 2026-09-09 23:53 | **4.6 days** | weekly routine, `nextRunAt` **2026-09-16 15:05 UTC**. See below | **ON SCHEDULE** |
| `texel-funnel` | 2026-09-11 15:07 | **2.9 days** | weekly routine, `nextRunAt` **2026-09-18 15:06 UTC**. `funnel/LOG.md` carries drop 1 with its page live (**HTTP 200**), its baseline recorded before the fact and its success test written in advance — the reason section B could be judged at all. Its **unfilled result row is T-009**, not a production failure | **ON SCHEDULE** |

**Two routines are over 48 h and neither is an alert — the rule defect is now on
its third run.** This routine's brief says *"No run in 48 h → ALERT"*, and both
`texel-release` (`0 10 * * 3`) and `texel-funnel` (`0 10 * * 5`) are **weekly by
design** in `OPERATIONS.md` §1. Read literally the rule fires against two healthy
routines on most days of the week. Runs 3 and 4 both surfaced the one-clause fix
— *"or within one scheduled interval, whichever is longer"* — and it has not been
applied. **Said in one line and not re-argued**; re-describing it every morning
is what this log's own rule forbids.

### D. Is the roadmap slipping?

**No.** Next unshipped target is **v0.2.1 "Brush", the rest — 2026-09-26**,
**12 days out**, outside the 7-day flag window. `ROADMAP.md` was last ticked
2026-09-09 (v0.2.0, shipped seventeen days early). `texel-release` gets two
Wednesday slots (**09-16**, **09-23**) before the date is close — though the
09-16 one opens with T-008 frozen in front of it.

### Standing, already surfaced to the user, one line each

**ADDENDUM 2026-09-14, later the same day: the user said do both, and both are
done and verified. Neither is standing any more — run 6 must not re-raise them.**

- `texel-release`'s description now reads **"all 16 suites plus the install
  test"**, confirmed back out of `list_scheduled_tasks` and in the frontmatter of
  its own `SKILL.md` line 3 (the description is stored there, so one edit fixed
  both places). **The wrong count lived only in the description** — the body of
  that file never states a total, only sub-counts ("three suites run headless",
  "the three GUI suites", "the four GUI suites"), so nothing else needed
  touching. `ls test_*.py` re-counted: **16**.
- This routine's 48-hour rule now reads **"No run in 48h, or within one scheduled
  interval, whichever is longer"**, with the interval to be read from the task's
  own `cronExpression` rather than from `OPERATIONS.md` (whose times are nominal
  and drift), and a line naming `texel-release` `0 10 * * 3` and `texel-funnel`
  `0 10 * * 5` as the two that kept tripping it. A weekly routine is late only
  once its **next** slot has passed without a run.

**Only T-002 is still the user's**, and it is the one no routine may ever touch.

*The original two lines, left as written:*

- **`texel-release`'s task description still says *"all 15 suites"*; the gate is
  16** (`ROADMAP.md`, and `ls test_*.py` returns exactly 16). Re-confirmed live in
  `list_scheduled_tasks` this run. No ledger row is possible — only the user can
  edit a routine's description. Raised in run 4, unchanged.
- **The 48-hour rule needs the "or one scheduled interval" clause** (section C).
  Raised in runs 3 and 4, unchanged.

### E. In one line

Day 5: healthy page, correct price, correct file, correct disclosure, 63 views,
one collection, no downloads, no sales, no questions — the store took its 12th
payment and **not one cent of the $71.16 is Texel's** — and the first free drop
reached the end of its window **below the bar it set itself**, which is now
`texel-funnel`'s row to answer.

---

## 2026-09-13 — run 4

**VERDICT: HEALTHY.** Every listing check passes against the live page, the
description's one hard number still matches the shipped zip, and the gallery
reorder `texel-marketing` claimed last night is **independently verified in the
live HTML** rather than taken from its commit message. All four doers produced a
real artifact. **Nothing opened, nothing closed** — the two open rows are both
short of the 7-day toast line. Texel is at **58 views, 0 downloads, 0 sales** on
day 4, and **took its first collection**; neither rule that could turn zero sales
into a finding can fire for another three weeks.

### Action ledger — first, per the file's own rule

**Opened this run: 0. Closed this run: 0.**

| id | age | owner |
|---|---|---|
| T-002 | **4 days** | **HUMAN** |
| T-008 | **2 days** | `texel-release` |

**T-002 is re-verified this run, not carried on yesterday's word.**
`/dashboard/payouts` still reads *"You need to provide us with your tax
information in order to initiate a payout"*, with **PayPal and Payoneer both
unconnected**. Balance **$51.20**, now **1 pending $1.41 + 10 available $49.79**
against yesterday's 2 + 9 — the same eleven payments, one more matured past
itch's 7-day hold. **None of it is Texel's and none of it can move.** It crosses
the 7-day toast line on **2026-09-16**.

**T-008 is 2 days old and its owner runs Wednesdays.** It will be **5 days old**
when `texel-release` next opens (Wed 09-16, `nextRunAt` 15:05 UTC), so the 3-day
freeze will already be live and the first thing that run does is clear T-008 or
write a dated refusal. Said again only because it is a dated prediction that
comes due in three days, not a re-description of the row.

Nothing was closed because nothing was closeable: no doer has written evidence
against T-008, and T-002 is `HUMAN` and demonstrably still open.

### ALERTS

**None.** Nothing about the listing, the numbers or the roadmap needs action
today. Three notes follow that are deliberately *not* alerts, with the reason.

### NOTE 1 — run 3's comment-container identifier is not stable, and no future run should use it

Run 3 recorded that the real comment container is `community_post_list_1800254`.
**That id is generated fresh on every render.** Two fetches of the same URL
minutes apart this morning returned `community_post_list_1434687` and then a
container whose id was absent from the first page entirely — topic ids likewise
(`community_topic_posts_9396683`, then `7849164`). A run that checks for run 3's
literal id will report a missing comment widget on a perfectly healthy page.

The **conclusion** run 3 drew was still right, and is re-derived here by a method
that does not depend on an id: the string `community_post` appears **13 times**
and **`class="community_post "` — the actual post markup — appears 0 times.**
Every one of the thirteen is a CSS selector in the custom theme's stylesheet or
a widget class name. **Comments: 0.**

Run 3's entry is left as written. Correcting the historical record is not this
routine's job; carrying the error forward would be.

### NOTE 2 — the funnel's 72-hour window has no run to read it, and does not need one

`funnel/LOG.md` commits to reading drop 1's window at **2026-09-14 10:00**.
`texel-funnel` is a **Friday** routine; `list_scheduled_tasks` gives its next run
as **2026-09-18 15:06 UTC**, four days after the date it set itself. Written down
because nobody has named it.

**No ledger row, and that is a judgement rather than an omission.** The reading is
not lost: itch's Project totals are **cumulative**, and `LEDGER.md` takes one row
per day, so the 72 h boundary is already fixed by the **09-11 row (46 views)** and
tomorrow's **09-14 row**. `texel-funnel` can fill its column on 09-18 off two rows
it does not have to trust anyone for. **What it must not do is take a live reading
on 09-18 and call it the 72 h figure** — that would be a 7-day window wearing a
72-hour label.

The numbers as they stand, recorded and not interpreted, because the window is
still open and the reading is the funnel's call: **Texel Density Cheatsheet 17
views / 11 downloads**; **Texel +5 then +7 views** across the two days since the
drop, against the **+10/day** baseline the funnel itself wrote down. Two days is
not three and this routine does not own the verdict.

### NOTE 3 — `texel-release`'s task description says 15 suites; the gate is 16

`list_scheduled_tasks` describes `texel-release` as gating on *"all 15 suites plus
the install test"*. `ROADMAP.md` — the file the routine actually works from — says
**16**, and `ls test_*.py` in the add-on root returns **exactly 16**. The gate that
governs is the roadmap's, so nothing is under-tested, but the description is
wrong and a routine reading its own description for the number would under-gate
by one suite.

**No ledger row:** `ACTIONS.md` admits only a doer routine or `HUMAN` as owner,
`HUMAN` is defined there as credentials, money, payouts and signups, and no doer
may edit another routine's SKILL.md. Same shape as run 3's NOTE 1 and surfaced
the same way — **to the user**, who is the only one who can edit it.

### A. Listing health — all clear, re-checked against the live page

Read logged out from `https://z3er1n.itch.io/texel` — **HTTP 200, 31,016 bytes**.

| Check | Result |
|---|---|
| Public and **published**, not draft | PASS — info table reads `Status: Released`, `Category: Tool`, `Author: Pixelkiln` |
| Price matches `ROADMAP.md`'s current milestone | PASS — **$9.95**, the v0.1 launch tier. The step to $14.95 is gated on v0.4 "Handoff", unshipped |
| Download file present, matches `dist/texel-*.zip` | PASS — serving **`texel-0.2.0.zip`, 187 kB**; local `dist/texel-0.2.0.zip` is **192,284 B = 187.8 KiB**. **0.1.0 is not offered** |
| AI disclosure reads Yes + Code + Graphics | PASS — `AI Disclosure = AI Assisted, Code, Graphics` |
| Devlogs live | PASS — index 200, both **1658358** and **1658363** linked at their full slugs (run 3's URL trap: the bare id 404s) |
| Comment form live, queue empty | PASS — **0 posts** (see NOTE 1 for the method) |
| Gallery | PASS — **10 images**, reordered (below) |

**The claim that burned us on launch day (T-005) was re-checked, not assumed.**
The live description says **"95 operators"**. Unpacking the *shipped*
`dist/texel-0.2.0.zip` and counting distinct `bl_idname = "texel.*"` gives
**exactly 95**, and the zip's manifest reads `version = "0.2.0"`. No other
operator or tool count appears anywhere on the page.

**The gallery reorder is verified against the page, not against the commit.**
`texel-marketing`'s 09-12 run says a `design-critic` pass returned one FATAL and
moved the hero. The live `screenshot_list` matches its description exactly: the
stroke **GIF** (`d66rJe.gif`) now sits at **slot 3**, and the density card
(`EcU1Ox.png` — the asset `texel-marketing` recorded when clearing **T-001**) has
moved from **slot 10 to slot 4**. Still 10 images, none dropped. **T-001 stays
closed**: its closing evidence was that the card is live, and it is — at a better
position than when the row was closed.

### B. The numbers

| date | views | downloads | sales | revenue | conv% |
|---|---|---|---|---|---|
| 2026-09-10 | 36 | 0 | 0 | $0.00 | 0.00% |
| 2026-09-11 | 46 | 0 | 0 | $0.00 | 0.00% |
| 2026-09-12 | 51 | 0 | 0 | $0.00 | 0.00% |
| **2026-09-13** | **58** | **0** | **0** | **$0.00** | **0.00%** |

**+7 views in 24 h**, against +5 and +10 before it. **The three deltas are 10, 5,
7 and this routine draws no shape from them** — four rows is not a 7-day trend,
the first honest weekly comparison is **2026-09-17**, and at n of this size the
swing arrives by chance constantly. The figure that is worth stating is the
**average: 7.3 views/day** since the 09-10 baseline.

**Revenue is read from the ledger, not inferred.** `/dashboard/purchases` reads
**$63.70 gross, 11 payments, $5.77 average, $8.92 max, $2.00 tip revenue** —
yesterday's figures unchanged, and **no Texel row in it**. Project totals agrees:
Texel `58 | 0 | - | 0 payments | 0 ratings`.

**One thing did change, and it is the first positive signal the page has ever
produced: collections went 0 → 1.** Somebody who did not buy it thought it was
worth saving. It is one person and it is not money; it is logged because it is
the first non-zero number on this listing that is not a view.

**Neither zero-sales rule can fire yet, and the dates are fixed rather than
vague.** Conversion (under 0.5% after 200+ views) needs **142 more views** — at
7.3/day, **~2026-10-03**. The 14-consecutive-days rule needs **30 days live** —
**2026-10-09**. Calling 0/58 a listing problem today would be inventing a finding
out of a sample this routine's own brief says is too small.

### C. Did the other four produce?

Read from `list_scheduled_tasks`, then checked against the artifact — running is
not producing.

| Routine | Last run (UTC) | Age | Artifact | Verdict |
|---|---|---|---|---|
| `texel-support` | 2026-09-12 13:22 | 22.5 h | `SUPPORT.md` advanced — a dated **day-4** entry, an explicit zero-inbound line across five surfaces, and the Bluesky card's 10 likes / 1 repost / **0 replies** separated out as a *funnel* reading rather than a support one | **PRODUCED** |
| `texel-marketing` | 2026-09-12 20:19 | 15.5 h | `promo/POSTED.md` +134 lines — a dated **Sat 09-12** section, two Bluesky replies with post ids, and the gallery reorder. **No Texel post, and that is the calendar**: Saturday is the packs' `#screenshotsaturday`, Texel takes Mon/Wed/Fri/Sun. No beat consumed from `QUEUE.md`; **Sun 09-13 is still the funnel's** | **PRODUCED** |
| `texel-release` | 2026-09-09 23:53 | **3.5 days** | weekly routine, `nextRunAt` **2026-09-16 15:05 UTC**. See below | **ON SCHEDULE** |
| `texel-funnel` | 2026-09-11 15:07 | 45 h | `funnel/LOG.md` created with **drop 1, the Density Cheatsheet**, its page live (**HTTP 200**), its baseline recorded before the fact, and its success/theatre test written down in advance | **PRODUCED** |

**`texel-release`'s 3.5 days is not an alert, for the reason run 3 gave.** This
routine's brief says *"No run in 48 h → ALERT"*, and `texel-release`'s cron is
`0 10 * * 3` — **Wednesdays only**. Read literally the rule fires against a
healthy weekly routine on five days out of seven. Run 3 surfaced the one-clause
fix (*"or within one scheduled interval, whichever is longer"*) to the user; it
has not been applied, so the misfire is live again today and will be again
tomorrow. **Repeating it as an alert is what would break the section.**

### D. Is the roadmap slipping?

**No.** Next unshipped target is **v0.2.1 "Brush", the rest — 2026-09-26**,
**13 days out**, outside the 7-day flag window. `ROADMAP.md` was last ticked
2026-09-09 (v0.2.0, shipped seventeen days early). `texel-release` gets two
Wednesday slots (09-16, 09-23) before the date is even close.

### E. In one line

Day 4: healthy page, correct price, correct file, correct disclosure, a gallery
that got measurably better last night, 58 views, first collection, no sales, no
questions, and two open rows that are still the owners' to clear.

---

## 2026-09-12 — run 3

**VERDICT: HEALTHY.** Every listing check passes against the live page and the
description's one hard number still matches the shipped zip. All four doers
produced a real artifact; three ran inside 48 h and the fourth is a weekly
routine whose next slot has not arrived. **Nothing opened, nothing closed** —
the two open rows are both younger than the freeze line. Texel is at **51 views,
0 downloads, 0 sales** on day 3; neither rule that could turn that into a
finding can fire yet.

### Action ledger — first, per the file's own rule

**Opened this run: 0. Closed this run: 0.**

| id | age | owner |
|---|---|---|
| T-002 | **3 days** | **HUMAN** |
| T-008 | **1 day** | `texel-release` |

**T-008 is 1 day old and its owner runs Wednesdays**, so it will be **5 days old**
when `texel-release` next opens (Wed 09-16) and the 3-day freeze will already be
live: the first thing that run does is clear T-008 or write a dated refusal. That
is not a failure today, and it is written down so nobody treats it as a surprise
on Wednesday.

**T-002 is re-verified this run, not carried forward on yesterday's word.**
`/dashboard/payouts` still reads *"You need to provide us with your tax
information in order to initiate a payout"*, with **PayPal and Payoneer both
unconnected**. The balance behind it is **$51.20** — now **2 pending $5.67 + 9
available $45.53** against yesterday's 3 + 8; the same eleven payments, one
simply matured past itch's 7-day hold. **None of it is Texel's and none of it can
move.** It crosses the 7-day toast line on **2026-09-16**.

Nothing was closed because nothing was closeable: no doer has written evidence
against T-008, and T-002 is `HUMAN` and demonstrably still open.

### ALERTS

**None.** Nothing about the listing, the numbers or the roadmap needs action
today. Two notes follow that are deliberately *not* alerts, with the reason.

### NOTE 1 — a defect in this routine's own 48-hour rule, first hit today

Section C of `texel-watch`'s brief says *"No run in 48h → ALERT."*
`texel-release` last ran **2026-09-09 18:53 local** — **60 hours** ago — and its
cron is `0 10 * * 3`, **Wednesdays only**. Read literally, the rule fires an
ALERT against a healthy weekly routine on **five days out of seven**, and it
would fire again every day until Wed 09-16.

**It is not an alert and is not reported as one**, because the routine is on its
schedule and `list_scheduled_tasks` gives `nextRunAt = 2026-09-16 10:05 local`.
An alert guaranteed to be wrong most of the week trains the next run to ignore
the section containing it, which is the failure this ledger was built to stop.

**No ledger row is opened for it, and that is a call rather than an omission:**
`ACTIONS.md` allows only a doer routine or `HUMAN` as owner, and `HUMAN` is
defined there as credentials, money, payouts and signups. A routine definition is
none of those, and no doer may edit another routine's SKILL.md — so there is no
valid owner to hand it to. **It is surfaced to the user instead.** The fix is one
clause: *"No run within 48 h **or within one scheduled interval, whichever is
longer** → ALERT."* Run 2 did not see this because `texel-release` was 36 h old
at the time; today is the first day it crosses.

### NOTE 2 — two ways this page could be misread, both checked rather than assumed

- **The devlog check must use the slugged URL.** `/texel/devlog/1658358` and
  `/texel/devlog/1658363` both return **HTTP 404** with the bare id. Both devlogs
  are live: the index (`/texel/devlog`, HTTP 200) links them at their full slugs
  and both resolve there. A later run checking by id alone would report a false
  failure on a healthy page.
- **`community_post` appears 11 times in the page source and means zero
  comments.** All eleven are CSS selectors in the custom theme's stylesheet. The
  real container, `community_post_list_1800254`, holds one
  `<script type="text/template">` and no posts. **Comments: 0.** Counting the
  string instead of the container would have manufactured eleven buyer comments
  on a product with no buyers.

### A. Listing health — all clear, re-checked against the live page

Read logged out from `https://z3er1n.itch.io/texel` — **HTTP 200, 30,969 bytes**.

| Check | Result |
|---|---|
| Public and **published**, not draft | PASS — info table reads `Status: Released`, `Category: Tool`, `Author: Pixelkiln` |
| Price matches `ROADMAP.md`'s current milestone | PASS — **$9.95**, the v0.1 launch tier. The step to $14.95 is gated on v0.4 "Handoff", unshipped |
| Download file present, matches `dist/texel-*.zip` | PASS — serving **`texel-0.2.0.zip`, 187 kB**; local `dist/texel-0.2.0.zip` is **192,284 B = 187.8 KiB**. **0.1.0 is not offered** |
| AI disclosure reads Yes + Code + Graphics | PASS — `AI Disclosure = AI Assisted, Code, Graphics` |
| Devlogs live | PASS — index 200, both titles linked (see NOTE 2 on the URL form) |
| Comment form live, queue empty | PASS — `game_comments_widget` renders the logged-out prompt; **0 posts** (see NOTE 2) |
| Gallery | PASS — **10 images** in `screenshot_list`, unchanged since the density still landed |

**The claim that burned us on launch day (T-005) was re-checked, not assumed.**
The live description says **"95 operators"**. Unpacking the *shipped*
`dist/texel-0.2.0.zip` and counting distinct `bl_idname = "texel.*"` gives
**exactly 95**, `texel.selection_transform` among them, and the zip's manifest
reads `version = "0.2.0"`. No other operator or tool count appears anywhere on
the page.

### B. The numbers

| date | views | downloads | sales | revenue | conv% |
|---|---|---|---|---|---|
| 2026-09-10 | 36 | 0 | 0 | $0.00 | 0.00% |
| 2026-09-11 | 46 | 0 | 0 | $0.00 | 0.00% |
| **2026-09-12** | **51** | **0** | **0** | **$0.00** | **0.00%** |

**+5 views in 24 h, against +10 the day before.** Three rows is not a 7-day trend
and none is invented here; the first honest weekly comparison is **2026-09-17**.
**The halving is not reported as a slowdown** — at n=5 against n=10 that gap
arrives by chance constantly, and calling it a decline would repeat the mistake
STATE.md corrected for the Etsy re-read ("still approximately zero", not
"trending down").

**The zero is confirmed against the payment ledger, not just the project table.**
`/dashboard/purchases` reads **$63.70 gross / 11 payments / $2.00 tips** —
unchanged from yesterday and from STATE.md — and **contains no Texel row at
all**; every one of the eleven rows names a pack or the Starter Bundle. Project
totals agrees: `Texel - Pixel Art Painting for Blender | 51 | 0 | - | 0 | 0 | 0`.
Both sources are read every run because Project totals structurally cannot see a
bundle purchase.

**Neither decision rule can fire yet, and the dates are named rather than
guessed.** Conversion needs 200+ views — **~2026-09-20 at +5/day, ~2026-09-26 at
+10/day**. The zero-sales rule needs 30 days live: **~2026-10-09**.

**Measured, and explicitly NOT a finding: Texel has 0 collections at 51 views**,
the only paid project in the catalogue with none. Inventory Vol. 7 was published
the same day and has 1 at 42 views. That is 1 against 0 on two three-day-old
pages, which is noise; it is written down as a number to compare against next
week, not as a signal about the listing.

**One traffic fact that belongs to `texel-funnel`, not here.** The Density
Cheatsheet — drop 1, shipped 2026-09-11 — reads **13 views / 8 downloads / 1
collection** on Project totals, and no `texel-density-cheatsheet` URL appears in
the top-20 referrers (cutoff 7 visits), so no referral into Texel is measurable
yet. **The 72-hour window the funnel set for itself closes 2026-09-14 10:00, and
the verdict is its own to write.** Texel's baseline for that comparison is the
table above, which is exactly what `funnel/LOG.md` pre-committed to.

### C. Did the other four produce?

Run times read from `list_scheduled_tasks`, not from `OPERATIONS.md` §1 — that
table says so itself.

| Routine | Last run | Inside 48 h? | Artifact | Verdict |
|---|---|---|---|---|
| `texel-support` | 2026-09-11 08:23 (~22 h) | yes | `SUPPORT.md` log carries a dated **2026-09-11** row: no inbound items, five surfaces named (page, 2 devlogs, itch inbox, Bluesky) | **PRODUCED** |
| `texel-marketing` | 2026-09-11 15:19 (~16 h) | yes | `promo/POSTED.md` carries the **2026-09-11** Bluesky post with its asset path and live URL (`3mvbff2zfou2d`) | **PRODUCED** |
| `texel-funnel` | 2026-09-11 10:07 (~21 h) | yes | `funnel/LOG.md` created; drop 1 logged with its page, files, gates and a pre-committed baseline | **PRODUCED** |
| `texel-release` | 2026-09-09 18:53 (~60 h) | **n/a — weekly** | `ROADMAP.md` ticked v0.2.0 SHIPPED 2026-09-09; `promo/QUEUE.md` advanced | **PRODUCED** (see NOTE 1) |

**All four left a real artifact.** `texel-support`'s is an explicit "no inbound
items" line for yesterday, which the brief names as a valid artifact — and it is
the honest one: with 0 downloads nobody has been in a position to ask anything,
so an empty support queue measures the traffic, not the product.

### D. Is the roadmap slipping?

**No.**

| Next unshipped | Target | Days |
|---|---|---|
| **v0.2.1 "Brush", the rest** | **2026-09-26** | **14 days out** |

Fourteen days is outside the 7-day flag window, and `texel-release` has two
Wednesday slots (09-16, 09-23) before it. Nothing is late and no date has moved.

**v0.1.0's target was today, 2026-09-12.** It shipped **2026-09-09, three days
early**, and `ROADMAP.md` already records that — noted so the date passing today
is not misread next run as a miss.

---

## 2026-09-11 — run 2

**VERDICT: HEALTHY.** Every listing check passes against the live page, the
description's one hard number still matches the shipped zip, all four doers ran
inside 48 h and every one of them left a real artifact. **Two ledger rows closed
against verified evidence, one opened.** The product has **46 views, 0 downloads,
0 sales** at ~2 days old; neither of the two rules that could make that a finding
can fire yet, and the dates they can first fire are named below rather than
guessed at.

### Action ledger — first, per the file's own rule

**Opened this run: 1. Closed this run: 2.**

**Closed — against evidence a doer wrote, re-verified here, never on a promise:**

- **T-001 · `texel-marketing` · the density readout still.** Live as **gallery
  slot 10** on `z3er1n.itch.io/texel`: the logged-out page (HTTP 200, 30,963 B)
  renders **10 `screenshot_list` images**, up from 9 yesterday, and the asset id
  the doer recorded (`EcU1Ox`) is in that list. `LISTING.md` line 386 is struck.
  The build evidence holds on its own terms — a real Blender 4.5.9 run, nothing
  on the card typed, `make_density.py` asserting the 8.4× = 3.2/0.38 claim so the
  card fails to build if it stops being true, and the CLAUDE.md §4 loop run to
  **round 3 SHIP, zero FATAL, zero SERIOUS**. **This was the oldest open row and
  the highest-value missing asset on the page.**
- **T-007 · `texel-marketing` · the missing Sunday queue row.** `promo/QUEUE.md`
  now carries a **Sun 09-13** row *and* a section saying in words that the slot
  is reserved for `texel-funnel`, with the density card as the fallback so it is
  never spent on nothing. The over-ceiling cost is stated, and **Mon 09-14 is
  named as the beat that gives way** rather than Sunday. `texel-funnel`'s gate is
  now satisfiable from inside `QUEUE.md` alone, **three hours before its first
  ever run**.

**Open, as `id · age · owner` — not re-described:**

| id | age | owner |
|---|---|---|
| T-002 | **2 days** | **HUMAN** |
| T-008 | 0 days | `texel-release` |

Both inside the normal 0–2 day band. Nothing frozen, toasted, or due for a kill
recommendation. **T-002 crosses the 7-day toast line on 2026-09-16.**

**T-002 was re-verified this run rather than carried forward on yesterday's
word** — `/dashboard/payouts` still shows *"You need to provide us with your tax
information in order to initiate a payout"*, with **PayPal and Payoneer both
unconnected**. The balance sitting behind it is **$51.20** (3 pending $13.01 +
8 available $38.19 = 11 payments, matching the payment ledger exactly). None of
it is Texel's, and none of it can move.

### ALERTS

**1. A product defect on the marquee feature had been named twice by a doer and
owned by nobody. Opened as T-008, owner `texel-release`.**

While building the density card, `texel-marketing` found that **Blender
middle-elides the density readout in the sidebar** — it renders as
`10.5 px/unit av....1, 8.4x spread)`, because the N-panel region is 280 px and
`Region.width` is read-only, so the average, the range and the spread cannot all
be read at any window size. It wrote this down in **two** places (T-001's closing
note and `LISTING.md` 398–403) and correctly declined to fix it, saying it was
not its lane. Nobody else picked it up.

That matters more than a UI nit: **texel density is the one thing a 2D tool
cannot do, the whole positioning rests on it, and the number the positioning
rests on does not fit the widget that prints it.** The listing works around it by
setting the figures as type on the card; the person who pays $9.95 and installs
the add-on gets the elided string. **This routine has not reproduced it** and the
row says so — it is opened because an unowned product defect is exactly what this
ledger exists to stop, and `texel-release` is the only routine allowed to touch
the product. Its next run is **Wed 09-16**.

**No other alerts.** Nothing about the listing, the numbers or the roadmap needs
action today.

### A. Listing health — all clear, re-checked against the live page

Read logged-out from `https://z3er1n.itch.io/texel` (HTTP 200, **30,963 bytes**).

| Check | Result |
|---|---|
| Public and **published**, not draft | PASS — `Status: Released`, no draft marker |
| Price matches `ROADMAP.md`'s current milestone | PASS — **$9.95**, the v0.1 launch tier. The step to $14.95 is gated on v0.4 "Handoff", unshipped |
| Download file present, matches `dist/texel-*.zip` | PASS — serving **`texel-0.2.0.zip`, 187 kB**; local `dist/texel-0.2.0.zip` is **192,284 B** = 187.8 KiB. **0.1.0 is not offered** |
| AI disclosure reads Yes + Code + Graphics | PASS — `AI Assisted, Code, Graphics` |
| Devlogs live | PASS — index 200, both 1658358 and 1658363 |
| Comment form live | PASS — `game_comments_widget` renders, `community_post_list` empty |
| Gallery | **10 images**, up from 9 — the density still landed (T-001) |

**The claim that burned us on launch day (T-005) was re-checked, not assumed.**
The live description says **"95 operators"**; unpacking the *shipped*
`dist/texel-0.2.0.zip` and counting distinct `bl_idname = "texel.*"` gives
**exactly 95**, `texel.selection_transform` among them. No other operator or tool
count appears anywhere on the page, so there is nothing left to contradict it.

### B. The numbers

| date | views | downloads | sales | revenue | conv% |
|---|---|---|---|---|---|
| 2026-09-10 | 36 | 0 | 0 | $0.00 | 0.00% |
| **2026-09-11** | **46** | **0** | **0** | **$0.00** | **0.00%** |

**+10 views in 24 h.** Two rows is not a 7-day trend and none is invented here;
the first honest weekly comparison is available on **2026-09-17**.

**The zero is confirmed against the payment ledger, not just the project table.**
`/dashboard/purchases` reads **$63.70 gross / 11 payments / $2.00 tips**,
unchanged from yesterday and from STATE.md, and **contains no Texel row at all**.
Project totals agrees: Texel `46 / 0 / – / 0 / 0 ratings / 0 collections`. Both
sources are read every run because Project totals structurally cannot see a
bundle purchase, which is how an $8.92 pack sale stayed invisible for five days.

**Neither rule can fire yet, and here is when each first can:**

- **Conversion.** The rule needs **200+ views**; we have 46. At the observed
  +10/day that is roughly **2026-09-26**. Calling 0% a cover, price or copy
  problem today would be a verdict invented from noise — **there is not yet
  enough traffic to test the listing at all.**
- **14 days with zero sales.** The rule needs **30 days live** first. Texel
  launched 2026-09-09, so the earliest it can fire is **2026-10-09**.
- **0 downloads and 0 sales are the same fact reported twice**, not two findings:
  Texel is paid with no free tier by deliberate decision, so a download here *is*
  a purchase.

**Where the 46 views are NOT coming from — second read, and it now bounds
something.** The store-wide 30-day referrer table returns **20 data rows with a
floor of 6 visits** (identical shape to yesterday, so it is a 20-row cap):
`z3er1n.itch.io` 90 · `itch.io` 65 · `game-assets/newest` 55 · the UI free sample
34 · the Godot forum 32 · `chatgpt.com` 25 · and down to 6. **There is still no
`bsky.app` row and still no `blenderartists.org` row.**

That is a bound, not a verdict, but at this scale the bound is informative:
**Texel's two launch announcements have each sent fewer than 6 visits to the
whole store in 30 days, against a Texel page that has taken 46 views in total.**
Both announced channels together account for at most about a quarter of the
page's traffic; the rest is itch's own surfaces. This is the second consecutive
reading, and it is consistent with `OPERATIONS.md` §3a's own measurement that our
posts take 6–18 likes on a topic that supports ~874.

**It does not become a finding today** — referrer data lags, the BlenderArtists
thread is 31 hours old, and one post plus one thread is not a test of a channel.
**It becomes one on 2026-09-14** (five days after the Bluesky launch post, four
after the forum thread). If neither surface has produced a referrer row by then,
that is a measured statement about Texel's launch reach and it gets a row against
`texel-marketing` — named now so a later run cannot quietly decline to write it
up, which is the failure the pack-side ledger was built to stop.

**The BlenderArtists thread, measured directly** (`t/1652476.json`): **38 views,
0 replies, 0 likes**, up from 27 yesterday. It is adding ~11 views/day to its own
page while the itch page adds ~10 — comparable velocity, and still no evidence of
anyone crossing from one to the other.

### C. Did the other four produce?

Live times from `list_scheduled_tasks`, not from `OPERATIONS.md`.

| Routine | Last run | Within 48 h | Artifact | Verdict |
|---|---|---|---|---|
| `texel-support` | 2026-09-10 08:22 | yes | `SUPPORT.md`'s log carries a dated **09-10** row — *"no inbound items; 5 surfaces checked"* — with each surface's access route and its result written out separately for 09-09 and 09-10 | **produced** |
| `texel-marketing` | 2026-09-10 15:19 | yes | Cleared **two** ledger rows (T-001, T-007) and logged **2 Bluesky replies**, both dated 09-10 and both **verified live on the public AppView this run** (`3mv6v6smrzd2k`, `3mv6v6vf4ax2t`, created 2026-09-10 20:26 UTC, `reply: true`) | **produced, verified live** |
| `texel-release` | 2026-09-09 18:53 (Wed) | yes (36 h) | `ROADMAP.md` ticked — v0.2.0 shipped, devlog 1658363 live, beat handed to `QUEUE.md`. Weekly routine; next run **Wed 09-16** | **produced** |
| `texel-funnel` | **never** | n/a | `funnel/` does not exist | **not a failure — not yet due.** Friday-only (`0 10 * * 5`); its first ever run is **today at 10:07**, three hours after this one |

**No routine is silent and none ran-without-producing.** `texel-marketing`'s
09-10 run is worth naming specifically: 09-10 was a Thursday, which belongs to
the packs, so it had **no Bluesky beat to post** and still produced a gallery
asset, two ledger clearances, a queue fix and two live replies. `OPERATIONS.md`
§3a says a run that posts nothing and replies twice is a successful run; this one
did that and more.

**`texel-funnel` is the one thing to watch tomorrow.** It has never run, today is
its first attempt, and the gate that would have blocked it was cleared last night
with three hours to spare. Tomorrow's run judges what it actually did.

### D. Roadmap

| Next unshipped | Target | Status |
|---|---|---|
| **v0.2.1 "Brush", the rest** | **2026-09-26** | **15 days out — not slipping.** Outside the 7-day flag window. `texel-release` next runs **Wed 09-16**, ten days before the date |

Both shipped versions landed early (v0.1.0 by 3 days, v0.2.0 by 17), so the
ladder's rule — *a version ships when its slice is done, not when its date
arrives* — has held in both chances it has had. **T-008 now sits in front of
v0.2.1 in `texel-release`'s queue**, per the ledger's own rule that a doer clears
its open rows before its own agenda.

### Corrections made to the record

Correcting the record is not doing the work, and this routine may do it for a
**proven** factual error. Two, both in `state/texel.md` (the split-out half of
`STATE.md`):

1. **Its routine table carried the pre-2026-09-09 calendar.** It said
   `texel-marketing` owns **Sat** (packs Tue/Thu/Sun) and `texel-funnel` runs
   **Sat 09:30, fortnightly**. All three are wrong: `pixelkiln-watch` run 8 gave
   Saturday back to the packs on 09-09 and moved Texel to **Sunday**, and the
   user changed the funnel to **weekly Fridays** the same day. The live cron is
   `texel-funnel = 0 10 * * 5` — **Friday**. Corrected, with the struck version
   named so it is not re-derived. **This is the third place the superseded
   calendar has been found sitting since the change** (`promo/POSTED.md`
   corrected the identical error inside itself on 09-10), and a stale calendar in
   two routines posting to one Bluesky account is precisely what caused the
   original collision.
2. **It said the listing has "9 gallery images".** It has **10** as of 09-10.
   Corrected off the live page.

### Noted, not actioned

- **`texel-release`'s scheduled-task description still says "all 15 suites"**
  where `ROADMAP.md` step 3 says 16 and the tree holds 16 `test_*.py` files. Same
  as yesterday; it is a task description, not one of the files this routine may
  correct, and it changes no behaviour. Recorded so it is not rediscovered a
  third time.
- **The Wed 09-16 asset collision** (`rot_cw.png` is a panel inside Friday's
  release card) is still written down by its owner in `QUEUE.md` with both escape
  routes named. **No row opened — the deadline set yesterday stands: if it is
  still unresolved on 09-14, it gets one.**
- **`state/texel.md`'s "Built and verified" paragraph reads "94 operators"** and
  the next paragraph reads "92/92". Both are true snapshots of different moments
  on 09-09, and the shipped count is now 95, which is what every customer-facing
  surface says. It is an internal file, not a sales page, so this is not T-005
  repeating — recorded rather than rewritten, because reconciling a history note
  is editing the record for tidiness, not for truth.

---

## 2026-09-10 — run 1

**VERDICT: HEALTHY.** Texel is live, published, correctly priced, correctly
disclosed, serving the right file, and its description's one hard number matches
the shipped zip. All four doer routines ran inside 48 h and three of the four
left a real artifact; the fourth is not due until tomorrow. Nothing is slipping.
The product has **36 views, 0 downloads and 0 sales** at ~36 hours old — too
early to be a finding in either direction, and the ledger starts today so it can
become one.

### Action ledger — first, per the file's own rule

**Opened this run: 1. Closed this run: 0** — no doer has written evidence
against an open row.

| id | age | owner | one line |
|---|---|---|---|
| T-001 | 1 day | `texel-marketing` | The density readout still — the last item in `LISTING.md`'s "Still to make". Verified still open: line 386 is unstruck and the live gallery has no density readout. |
| T-002 | 1 day | **HUMAN** | itch payouts not set up on the z3er1n account. No routine may attempt it. |
| T-007 | 0 days | `texel-marketing` | **NEW.** Sun 09-13 is a Texel beat day and is missing from `promo/QUEUE.md` — it is the only slot inside `texel-funnel`'s gate window tomorrow. See ALERT 1. |

All three are inside the normal 0–2 day band. Nothing is frozen, toasted, or due
for a kill recommendation.

### ALERTS

**1. `texel-funnel` makes its first ever run tomorrow into a gate that is set up
to fail. Owner `texel-marketing` (T-007).**

The funnel's gate is *"`promo\QUEUE.md` has room, and `texel-marketing` has a
free slot in the next two days."* From a Friday run that window is Fri 09-11 →
Sun 09-13. **Fri 09-11 is already committed to the v0.2.0 release note**, and
**Saturday is barred** — it belongs to `#screenshotsaturday` on the packs.
**Sun 09-13 is free and is a Texel beat day, but it appears nowhere in
`QUEUE.md`**, which holds only Fri 09-11, Mon 09-14 and Wed 09-16. A routine
reading the queue cannot see the one slot that would let it ship, so the first
drop of the launch push is liable to be refused on a gate that need not have
failed. The gate itself is correct and should not be weakened — the queue is
what is short a row. This is the same class of defect as the Sat/Sun calendar
collision `pixelkiln-watch` caught on 09-09: two routines sharing a calendar,
neither able to see the other from inside.

**No other alerts.** Nothing about the listing, the numbers or the roadmap needs
action today.

### A. Listing health — all clear, every item checked against the live page

Read logged-out from `https://z3er1n.itch.io/texel` (HTTP 200, 30,517 bytes).

| Check | Result |
|---|---|
| Public and **published**, not draft | PASS — `Status: Released`, `Published 13 hours ago`, no draft marker |
| Price matches `ROADMAP.md`'s current milestone | PASS — **$9.95**, the v0.1 launch tier. The step to $14.95 is gated on v0.4 "Handoff", which has not shipped |
| Download file present, matches `dist\texel-*.zip` | PASS — serving **`texel-0.2.0.zip`, 187 kB**; local `dist/texel-0.2.0.zip` is 192,284 B = 187.8 kB. **0.1.0 is not offered** |
| AI disclosure reads Yes + Code + Graphics | PASS — `AI Assisted, Code, Graphics` |
| Classification | PASS — Tool |
| Devlogs live | PASS — both, 1658358 (v0.1.0 launch) and 1658363 (v0.2.0) |
| Comment form live | PASS — `game_comments_widget` renders |

**One claim re-verified because it burned us before (T-005).** The description
says **"95 operators"**. Unpacking the *shipped* `dist/texel-0.2.0.zip` and
counting distinct `bl_idname = "texel.*"` gives **exactly 95**. The count that
contradicted itself across description, cover and banner on launch day is now
consistent with the artifact the customer actually receives.

### B. The numbers

`LEDGER.md` created this run; today's row is a **baseline, not a trend** — there
is no previous row to compare against, so no 7-day movement can be stated and
none is invented here.

| date | views | downloads | sales | revenue | conv% |
|---|---|---|---|---|---|
| 2026-09-10 | **36** | **0** | **0** | **$0.00** | **0.00%** |

**The zero is confirmed against the payment ledger, not just the project table.**
`/dashboard/purchases` reads **$63.70 gross / 11 payments / $2.00 tips** —
unchanged from STATE.md, and **containing no Texel row at all**. This matters
because Project totals structurally cannot see a bundle purchase, which is how an
$8.92 pack sale stayed invisible for five days; checking both sources means the
Texel 0 is a measurement rather than an artefact of the instrument.

**What the numbers do and do not say:**

- **The conversion rule does not fire.** It needs 200+ views; we have 36. Calling
  0% conversion a listing problem at 36 views would be a verdict invented from
  noise. **There is not yet enough traffic to test the listing at all.**
- **The 14-day-no-sales rule does not fire.** The page is ~36 h old.
- **0 downloads at 36 views is not separately interpretable.** Texel is paid with
  no free tier by deliberate decision (`ROADMAP.md`: GPL makes a crippled lite
  build pointless, so the free tier is *content* — `texel-funnel`'s job, starting
  tomorrow). A download here means a purchase, so 0 downloads and 0 sales are the
  same fact reported twice, not two findings.
- **Where the 36 views came from is worth recording now.** The store-wide
  referrer table (30 d, 21 rows, floor **6 visits**) contains **no bsky.app row
  and no Texel-specific row**. So the Bluesky launch post of 09-09 has sent the
  whole store **fewer than 6 visits in 30 days**. That is a bound, not a verdict
  — the post is one day old and referrer data lags — but it is consistent with
  `OPERATIONS.md` §3a's own measurement that our posts take 6–18 likes where the
  topic supports ~874. **Re-read next run before drawing a conclusion.**
- **The one channel visibly moving is the new one.** The BlenderArtists release
  thread went live at **05:07 UTC today** and already has **27 views, 0 replies**
  (`blenderartists.org/t/1652476.json`) — in ~7 hours, against the itch page's 36
  views in ~36 hours. One thread is not a strategy, and views on a forum thread
  are not clicks through to the store, but it is the highest-velocity surface
  Texel currently has. Next run should check whether it produces a referrer row.

### C. Did the other four produce?

Live times from `list_scheduled_tasks`, not from `OPERATIONS.md` — the nominal
table there drifts.

| Routine | Last run | Within 48 h | Artifact | Verdict |
|---|---|---|---|---|
| `texel-support` | 2026-09-09 18:48 | yes | `SUPPORT.md` carries an explicit **"0 inbound items"** line for 09-09, with the four surfaces it checked and how each was read | **produced** |
| `texel-marketing` | 2026-09-09 19:28 | yes | `POSTED.md` (written 09-10 00:07) logs the **BlenderArtists release thread** with its URL, and it is **live — HTTP 200, category "Released Add-ons and Extensions"** | **produced, verified live** |
| `texel-release` | 2026-09-09 18:53 (Wed) | yes | `ROADMAP.md` ticked — **v0.2.0 shipped**, devlog 1658363 live, beat handed to `QUEUE.md` | **produced** |
| `texel-funnel` | **never run** | n/a | `funnel/LOG.md` does not exist | **not a failure** — Fridays-only, created on a Wednesday. First run is tomorrow, 09-11 |

**No routine is silent, and none ran-without-producing.** An empty support log is
a real measurement here rather than a missing one: the comment form renders, the
devlog index returns 200, and the notification and Bluesky routes were both read.

### D. Roadmap

| Next unshipped | Target | Status |
|---|---|---|
| **v0.2.1 "Brush", the rest** | **2026-09-26** | **16 days out — not slipping.** Outside the 7-day flag window. `texel-release` next runs Wed 09-16, ten days before the date. |

v0.1.0 shipped 3 days early and v0.2.0 seventeen days early, both on 09-09. The
ladder's own rule — *a version ships when its slice is done, not when its date
arrives* — has been honoured in the only two chances it has had.

### Noted, not actioned

- **`texel-release`'s task description says the gate is "all 15 suites".**
  `ROADMAP.md` step 3 says **16**, and there are **16** `test_*.py` files in the
  tree. The roadmap is right and the task description is the stale one. It is a
  scheduled-task description, not one of the three files this routine may
  correct, and it changes no behaviour — recorded so it is not rediscovered.
- **The Wed 09-16 asset collision** (`rot_cw.png` is a panel inside Friday's
  release card) is already written down by its owner in `QUEUE.md`, dated, with
  both escape routes named. Six daily marketing runs stand between now and then.
  **No row opened** — re-describing an owner's own note is the noise the ledger
  exists to avoid. If it is still unresolved on **09-14**, it gets a row.
