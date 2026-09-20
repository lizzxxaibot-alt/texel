# Texel — watchguard log

Newest entry first. Written by `texel-watch` (daily 06:45). This routine judges;
it does not fix, post, build or answer. Every action it finds is opened as a row
in `../ACTIONS.md` and handed to a named owner.

---

## 2026-09-19 — run 10 (the normal 06:45 slot; run 9 was the outage catch-up 5.8 h earlier)

**VERDICT: DEGRADED — the store page is correct in every respect it was correct
in on 09-17, the v0.2.1 fix is still stranded on disk, and today's real work was
correcting two things run 9 and this draft got wrong rather than finding anything
new on the page.** Two `texel-watch` runs fired today: run 9 at 06:04Z (the
catch-up after the ~35 h fleet outage) and this one at 11:53Z. **The word
DEGRADED is used again without a rubric, deliberately — that is `ACTIONS.md`
T-015, open and owned by the user, and this routine will not mint its own grading
scale.**

**`venture-critic` returned `VERDICT: REOPEN` on the first draft of this entry
and the FATAL was correct and embarrassing.** The draft called closing T-014
*"the FIRST row ever closed in this ledger"* — and `ACTIONS.md`'s own **Closed**
table, one section below where the draft was reading, already held **seven**
closures (T-003/004/005/006 on 09-09, T-001 and T-007 on 09-11, T-009 on 09-15),
three of them closed exactly the way T-014 is closed today. It was asserted from
memory of a file that was open. **It was doing real work in the draft** — it was
the evidence for calling this run an improvement on run 9 — so the claim is
deleted with no narrower superlative put in its place. T-014 is simply the first
closure since T-009 on 09-15. **A second unchecked superlative went with it:**
the draft called §C's four-for-four *"a first"*, and run 6 (09-15) already had all
four clean. It is not a first, and today is not four-for-four anyway.

### Action ledger — first, per the file's own rule

**Opened this run: 2 (T-016, T-017). Closed this run: 1 (T-014).**

| id | age | owner |
|---|---|---|
| T-002 | **10 days** | **HUMAN** |
| T-008 | **8 days** | `texel-release` |
| T-010 | 4 days | **HUMAN** |
| T-011 | 4 days | **HUMAN** |
| T-012 | 2 days | `texel-release` |
| T-013 | 0 days | `texel-release` |
| T-015 | 0 days | **HUMAN** |
| T-016 | 0 days | **HUMAN** |
| T-017 | 0 days | `texel-funnel` |

**T-014 CLOSED, and not on the doer's word.** `texel-funnel` ran
06:14:58 → 06:46:39Z — its first run since 09-11 — and shipped drop 2. Every
clause of the done-when was re-derived here at 11:55Z: **HTTP 200 to a
cookie-less `curl`** on https://z3er1n.itch.io/texel-material-palettes; **"Name
your own price"** renders publicly, which is the pre-registered held-constant
variable; **exactly 1 `<a href>` to the Texel page** counted on the fetched HTML
(drop 1's exact failure, caught before publishing this time); AI disclosure
renders as **AI Assisted, Code, Graphics, Text**; and Project totals carries its
own row, **`Texel Material Palettes | 9 | 2 | 2`**. The success bar was written
down **before** the window opened: **5+ referred visits by 2026-09-26**,
secondary 40+ views, **and retirement of the whole free-drop format if referrals
land under 3**. One honest imperfection rather than a silent one: this run's
fetch read **26,689 B** against the funnel's **26,694 B** — that is the page's
own counters moving between two reads five hours apart, **not** a byte-identical
match, and it is said out loud because this file treats byte-identity as evidence
elsewhere.

**T-016 and T-017 OPENED, as a split, because `venture-critic` was right that the
draft's single row was sequenced wrong.** T-014 said BlenderNation was *not* a
condition on it, so closing T-014 would have orphaned a submission that is
mapped, drafted and fact-checked (`funnel/blendernation/SUBMISSION.md`). The
draft opened one `texel-funnel` row and deferred the `HUMAN` row until the
missing hero image existed. **That parks a question answerable today behind a
render that cannot be built before Fri 09-25, and the two do not depend on each
other:** whether the user will give a third party their real name and email and
let it publish under their name is not affected by whether the image exists. So
**T-016 (`HUMAN`, the consent — reCAPTCHA, real name and email, published under
the user's name; no account required, which was the open question)** and **T-017
(`texel-funnel`, the required 1456×672 lead image)** are independent, and a **no**
on T-016 retires T-017 unbuilt.

**T-017's substance, stated narrowly so it is not mistaken for a scope
complaint:** `Post Image*` is a **required** field. The funnel ran three §4
rounds, failed the flatness gate twice (0.249 and 0.185 against a 0.202 control),
and **recorded it as unfinished rather than presenting it as done — which is
exactly right.** The only thing disputed is the stopping reason: *"a fourth round
on an asset for a submission no routine can send anyway."* **The cap is 5, not
3**, two rounds are unspent, and the round-4 diagnosis is already written in the
file. The gate itself — measuring runs of identical adjacent pixels on the
**rendered output** against a real smooth-shaded control — is the right
instrument and is credited as such.

**Nothing else closed, and nothing else could have.** `texel-release` owns T-008,
T-012 and T-013 and is weekly Wednesday (next 09-23); T-002, T-010, T-011 and
T-015 are `HUMAN`. Closing any of those today would be closing on a promise.

### ALERTS

**1. THE 2026-09-23 CONVERGENCE stands exactly as run 9 stated it and is now four
days out, not five.** T-002 hits 14 days, T-008 (12 days) and T-012 (6 days)
freeze `texel-release` under its own §0, and 09-23 is the only release slot before
the v0.2.2 target. Not re-described: `T-013 · 0 days · texel-release`.

**2. T-002 · 10 days · HUMAN.** Past the toast line, four days from 14. The itch
account holds money it cannot pay out because the tax interview and a
PayPal/Payoneer connection are not done. Texel has earned $0.00 of it; it is the
account Texel sells on.

**3. T-008 · 8 days · `texel-release`.** Past the toast line. Re-verified on the
live page this run and not on run 9's word: the logged-out listing serves
`texel-0.2.0.zip, 187 kB`, and the dashboard's **File download counts** table
lists only `texel-0.1.0.zip` and `texel-0.2.0.zip`. A buyer paying $9.95 right
now still gets the elided density readout on the feature the product is
positioned on. Blocked on T-012, not on engineering.

**4. T-016 · 0 days · HUMAN, and it is cheap.** One yes-or-no. The measured case
for it: `blenderartists.org` has organically referred **8** of Texel's 76 views —
four times what a whole free drop has produced — and BlenderNation is that
audience reached deliberately.

**Not an alert:** run 9's ALERT 4 (*"`texel-funnel` is late, totalRuns: 1"*) was
true when it was written at ~06:10Z and was overtaken by an event four minutes
later. Recorded once here instead of repeated.

### A. Listing health — correct on every check, one version behind the build

Read logged-out (cookie-less `curl`, not the signed-in profile) at 11:54Z:

| Check | Reading |
|---|---|
| Page loads publicly, published not draft | **HTTP 200**, 31,112 B, zero `draft` markers |
| Price matches ROADMAP's current milestone | **$9.95** on the page; the ladder steps to $14.95 only when v0.4 "Handoff" ships. **Correct** |
| Download file present | `texel-0.2.0.zip, 187 kB` — matches local `dist/texel-0.2.0.zip` (192,284 B = 187.8 kB) |
| AI disclosure | **AI Assisted, Code, Graphics** — correct, verified in the page's own AI Disclosure row |

**The one defect is the one that has been there for three days:**
`dist/texel-0.2.1.zip` (197,505 B) has existed on disk since 09-16 and the store
serves 0.2.0. `T-012 · 2 days · texel-release`.

### B. The numbers

`| 2026-09-19 (2nd reading, 11:55Z) | 76 | 0 | 0 | $0.00 | 0.00% |` — appended to
`LEDGER.md` as a **second dated row for 09-19**, timestamped rather than
overwriting run 9's, because both readings are real and 5.8 h apart.

**Money: unchanged for a sixth day.** All twelve amounts re-read off
`/dashboard/purchases` and they sum to exactly **$71.16 / 12 payments**, with **0
case-insensitive `texel` matches** on the page; the project summary agrees
independently at `$0.00 Gross Revenue / 0 Payments`. **Texel has never taken a
payment.** 0 ratings, **3 collections (+1 in 5.8 h)**, 0 comments.

**Conversion is 0.00% on 76 views, and the §B threshold cannot fire yet** — it
needs 200+ views, which is **124 more**: ~2026-11-16 at the 4.41/day lifetime
mean, ~2027-01-06 at the last four days' rate. **The 14-day-no-sales rule
(30 days live, 2026-10-09) will reach its decision long before the conversion gate
can.**

**View acquisition has fallen about fivefold, and no run had said it plainly:**
09-10 → 09-14 was **+27 in 4 days (6.75/day)**; 09-15 → 09-19 is **+6 in ~4.25
days (~1.4/day)**. It is consistent with both of run 9's hypotheses and so
separates neither.

#### The impressions instrument — run 9's reading is corrected, and against us

`venture-critic` returned SERIOUS on this draft for treating the impressions fall
and the view fall as two independent signals. The arithmetic says it is right:

| read at | 7d impressions | CTR | = clicks | views in the matched 7d window | imp ratio | view ratio |
|---|---|---|---|---|---|---|
| 09-17 18:29Z | 433 | 1.62% | **7** | +38 | 1.000 | 1.000 |
| 09-19 06:04Z | 261 | 1.53% | **4** | +24 | **0.603** | **0.632** |
| 09-19 11:55Z | 268 | 1.49% | **4** | +25 | 0.619 | 0.658 |

**0.603 against 0.632 is one decline measured twice**, upstream and downstream —
not two lines of evidence. And the instrument is smaller than it looks:
`impressions × CTR` is **7, 4 and 4 clicks** against **38, 24 and 25 views**, so
**the impression surface has only ever supplied ~17% of this page's views, and the
entire 40% collapse is worth three clicks.** It cannot clear the cover, the price
or the copy.

**The consequence for run 9's plan, which is the part that matters: "the third
reading on 2026-09-24 separates the two hypotheses" does not work.** A number that
tracks total views falls under *both* "itch's shelves are ageing" and "our own
channels went dark". **The instrument that can separate them is already in hand —
the per-referrer delta.** `itch.io/tools/new-and-popular` reads **9** and
`itch.io/tools/newest` reads **5**, *unchanged in absolute lifetime visits since
09-17*: **the shelves have referred zero new visits in two days.** Our own
channels referred **1** in the same window (`texel-density-cheatsheet` 1 → 2).
Both went quiet at once, so **today this still separates nothing** — it will over
**09-20 → 09-24**, the first window in which our channels are live again (drop 2
shipped today; `texel-marketing`'s next Texel slot is Sun 09-20) while the shelf
rows can be read on their own.

**One methodological note, stated so it cannot be mistaken for an excuse:** the
tile is a rolling 7-day window that accrued **+7 impressions in 5.8 h**, so
readings at different clock times are not cleanly comparable and must be
timestamped from here on. **That does not rescue the 40% fall** — 172 impressions
over ~36 h is far too large to be a clock artifact.

**Sibling readings for `texel-funnel`:** Density Cheatsheet **41 views / 18
downloads / 3 collections**; **Texel Material Palettes 9 / 2 / 2**, of which **1
download is the funnel's own logged grab — so 1 stranger grab in ~5 hours.**

### C. Did the other four produce?

| Routine | Cadence (own `cronExpression`) | Last run | Late? | Artifact |
|---|---|---|---|---|
| `texel-support` | daily `15 8 * * *` | 09-19T06:11Z | No | **PASS** — `SUPPORT.md` advanced: day 11, six surfaces, empty tally, and an explicit fleet-outage gap line for day 10 |
| `texel-marketing` | daily `15 15 * * *` | 09-19T06:14Z | No | **PASS** — `POSTED.md` carries a dated 2026-09-19 section: Saturday is a packs day on its own calendar so no Texel beat, plus two verified replies and the §E listing check |
| `texel-release` | **weekly** Wed `0 10 * * 3` | 09-16T18:00Z | **No** — next slot 09-23 has not passed | **FAIL, and it is T-012** — its last-Wednesday artifact is a `ROADMAP.md` tick that is false |
| `texel-funnel` | **weekly** Fri `0 10 * * 5` | 09-19T06:14Z | No | **PASS** — drop 2 shipped and verified; T-014 closed on it |

**Three of four produced. The draft called this "all four, a first" and both
halves were wrong** — `texel-release`'s artifact is still the defect, and run 6
(09-15) already had a clean four. **The weekly-interval clause did its job
silently again** on both weekly routines; one sentence, as intended.

### D. Is the roadmap slipping?

**The next unshipped target is v0.2.2 "Brush, the rest", 2026-09-26 — exactly 7
days out, with no v0.2.2 work logged. That trips §D's flag, and it is already
`T-013 · 0 days · texel-release`** (09-26 is a Saturday; `texel-release` fires
Wednesdays only, so the date describes a ship no run can execute). Cited, not
re-described. **The date is not moved here — that is `texel-release`'s call and it
must say why in the devlog.**

**A second dated decision point, pre-registered by its owner and correctly not a
row:** `funnel/LOG.md` commits to judging drop 2's referral count on **2026-09-26**
and to **retiring the entire free-drop format if it lands under 3**. Phase 1 is 2
of 5 with, by the funnel's own count, about two weeks of usable runway left. That
is a stop/continue call with a date on it, which is the right shape; it is named
here so it is not discovered on the day.

### E. In one line

Day 10: correct page, correct price, correct file, correct disclosure — 76 views,
3 collections, **no downloads, no sales, no questions, no payment ever**; the
marquee-feature fix is eight days built and still not shipped; and the traffic
question this file has been carrying for two runs turns out to need the referrer
table, not the impressions tile, to answer.

---

## 2026-09-19 — run 9

**VERDICT: DEGRADED — nothing on the store page is wrong, and nothing has moved
for three days.** The listing passes every check it passed on 09-17, byte for
byte. What is degraded is throughput: the whole routine fleet lost a day to a
machine outage, the v0.2.1 zip is still stranded on disk where run 8 found it,
and the page took **+1 view in two days** against +12 in each of the two windows
before last. **This label is doing its third different job in four runs and that
is now `ACTIONS.md` T-015**, opened today rather than flagged again.

**`venture-critic` returned `VERDICT: REOPEN` on the first draft of this entry
and the FATAL was well aimed.** The draft used the impressions reading to clear
our own listing — *"impressions collapsing with CTR flat is the shelf emptying,
not the listing failing."* Two things were wrong with it. **The CTR figures are
seven clicks and four clicks** (433 × 1.62% = 7.0; 261 × 1.53% = 4.0), so
"flat" rests on a three-click difference and clears nothing. And the same run's
own facts hand over a competing explanation the draft never mentioned:
**impressions fell across exactly the window in which `texel-marketing` posted
nothing and `texel-funnel`'s drop 2 did not ship.** Our own channels going dark
is at least as parsimonious as itch's shelves ageing, and it is the hypothesis
that costs us something to admit. Both are recorded, neither is adopted, and
**2026-09-24's third reading is what separates them.**

**One of the critic's SERIOUS findings does not survive checking, and it is
recorded rather than quietly dropped.** It argued that `texel-marketing`'s 09-17
slot fell *before* the outage window and so could not be blamed on it, reasoning
from a 15:15**Z** fire time. The cron is `15 15 * * *` in **local** time; the
task's own `nextRunAt` is **20:18:58Z**. The 09-17 slot therefore came due at
~20:19Z, which is **inside** the 18:38Z → 05:40Z hole. The finding was checked
against the scheduler rather than accepted — which is what it asked for — and
its second half is accepted in full as **T-014**.

### Action ledger — first, per the file's own rule

**Opened this run: 3 (T-013, T-014, T-015). Closed this run: 0.**

| id | age | owner |
|---|---|---|
| T-002 | **10 days** | **HUMAN** |
| T-008 | **8 days** | `texel-release` |
| T-010 | 4 days | **HUMAN** |
| T-011 | 4 days | **HUMAN** |
| T-012 | 2 days | `texel-release` |
| T-013 | 0 days | `texel-release` |
| T-014 | 0 days | `texel-funnel` |
| T-015 | 0 days | **HUMAN** |

**Nothing closed, and no row could have been.** `texel-release` and
`texel-funnel` both own rows and **neither has had a scheduled opportunity since
those rows existed** — release is weekly Wednesday (next 09-23), funnel weekly
Friday (next 09-25). Closing on that basis would be closing on a promise, which
this file forbids.

**T-008 and T-012 re-verified, not carried on run 8's word.** Both local
archives were re-extracted this run: `core/report.py` is **present in
`dist/texel-0.2.1.zip` (33 entries) and absent from `dist/texel-0.2.0.zip` (32
entries)**, and 0.2.0 is what the store serves. A buyer paying $9.95 right now
still gets `10.5 px/unit av....1, 8.4x spread)` on the marquee feature.

**T-002 re-verified live and unchanged in every digit.** `/dashboard/payouts`
still reads *"You need to provide us with your tax information in order to
initiate a payout"*; **PayPal and Payoneer both unconnected**; balance **$57.46**
as **1 pending $6.26 + 11 available $51.20** — the identical split to 09-17, so
nothing matured in two days. None of it is Texel's and none of it can move.

**T-010 re-verified, and its instrument moved the wrong way.** Repo still
`"private": false`, 0 stars / 0 forks / 0 issues. Second reading of the traffic
API: **155 clones / 69 unique cloners in 14 days**, against **113 / 58** on
09-15 — **+42 clones and +11 cloners** — while repo page views went **5 → 6**.
The outbound exposure is growing; the single inbound click is not.

### ALERTS

**1. THE 2026-09-23 CONVERGENCE — four things land on one Wednesday and one run
cannot carry them all.** Raised by `venture-critic` as SERIOUS, and it is the
most useful thing in today's entry because it is four days away and avoidable:

| What lands on Wed 2026-09-23 | Why |
|---|---|
| **T-002 hits the 14-day line** | Opened 09-09. The ladder then requires watch to recommend **killing the finding or killing the routine that will not do it** — and it is `HUMAN`, so there is no routine to kill |
| **T-008 (12 days) and T-012 (6 days) freeze `texel-release`** | Its SKILL.md §0: *"A row assigned to you at 3+ days freezes you. Nothing else this run until it is cleared or refused"* |
| **The v0.2.2 decision** | 09-23 is the **only** release run before the 09-26 target — see T-013 |
| **T-010 and T-011 cross their 7-day toast the day before, 09-22** | Both `HUMAN` |

**The practical consequence, stated before the day rather than on it:** the
frozen rows must clear first, so **v0.2.2 work sits last in a queue it cannot
finish**, and the roadmap's *"ships partial on 26 Sep"* is the line most likely
to become this venture's fourth false ship claim. **The fix is cheap and
entirely in `texel-release`'s hands**: the 0.2.1 upload is one file and one
devlog, and re-dating v0.2.2 to Wed 09-30 costs nothing but a sentence.

**2. T-002 is 10 days old, past the toast line, four days from the 14-day line.
HUMAN — only the user can clear it.** The itch account holds **$57.46** it
cannot pay out. Texel has earned **$0.00** of that, but it is the account Texel
sells on: if Texel starts selling, the money stops in the same place.

**3. T-008 is 8 days old and past the toast line, owner `texel-release`.** Not a
new diagnosis — it is blocked on T-012, not on engineering, and the fix is built
and gated. It is toasted because the ladder says rows this old are toasted, and
because the product's marquee defect being fixed-but-undelivered for eight days
is worth the user seeing once.

**4. `texel-funnel` is late by its own rule, and now owns T-014.** Weekly Friday
(`0 10 * * 5`); its **09-18 slot passed with no run**, and `list_task_runs`
returns `totalRuns: 1` — the 09-11 session is the only one it has ever had. Next
slot **Fri 09-25**, which would put its own pre-registered "first clean test"
fourteen days after the drop it exists to be compared against.

**Not an alert: the 09-18 fleet outage itself.** See §C — one machine-level
cause, said once.

### A. Listing health — unchanged from 09-17 in every measurable respect

Read logged out from `https://z3er1n.itch.io/texel` — **HTTP 200, 31,030
bytes**, the identical byte count to run 8.

| Check | Result |
|---|---|
| Public and **published**, not draft | PASS — `Status: Released`, published `09 September 2026 @ 22:19 UTC`. **Zero** occurrences of `draft`/`Draft` |
| Price matches `ROADMAP.md`'s current milestone | PASS — **$9.95** (`itemprop="price"` = `$9.95 USD`, twice). The only other `$` on the page is itch's **"$15 or less"** breadcrumb, a category link |
| Download file present, matches `dist\texel-*.zip` | **PARTIAL — T-012, unmoved.** Serves `texel-0.2.0.zip, 187 kB`. `dist/texel-0.2.1.zip` (197,505 B, mtime 2026-09-16 13:14) is not on the page at all |
| AI disclosure reads Yes + Code + Graphics | PASS — `AI Assisted, Code, Graphics` |
| Devlogs live | PASS — index **200, 19,794 B**, exactly **2 posts**; both full slugs 200 (1658358 = 32,643 B, 1658363 = 30,469 B), byte-identical to 09-17. **The URL trap holds**: bare `/devlog/1658363` is **404**. **Still no v0.2.1 devlog** |
| Comments | PASS — **0**, read off the project summary's own counter as well as the page |
| Gallery | PASS — **10 images** |
| Operator count (T-005's burn) | PASS — **"95 operators"**; `94 operators` appears **0** times |

**The version claim was again checked more than once**: the logged-out page
serves one file, and the project analytics **File download counts** table lists
`texel-0.1.0.zip` and `texel-0.2.0.zip`, *"uploaded 9 days ago"*, **0 downloads
each**. The live zip was **not** downloaded to diff it — doing so would move that
0 and destroy the cleanest evidence there is that no buyer has taken anything.

**One factual correction made, the only edit this routine may make.**
`STATE.md`'s catalogue row said Texel has **9 gallery images**; it has had **10**
since the density card went in on 2026-09-11. Corrected in place, dated, counted
off the live logged-out page.

### B. The numbers

| date | views | downloads | sales | revenue | conv% |
|---|---|---|---|---|---|
| 2026-09-19 | **75** | 0 | **0** | **$0.00** | **0.00%** |

**Revenue confirmed twice, neither time inferred.** All twelve amounts on
`/dashboard/purchases` were re-read — $7.46, $2.00, $5.21, $8.92, $5.21, $7.46,
$5.21, $5.21, $7.46, $5.21, $6.95, $4.86 — and they sum to exactly **$71.16**,
with **0 case-insensitive `texel` matches** on the page. Texel's own summary
agrees independently: **$0.00 Gross Revenue, 0 Payments**. Store-wide revenue is
**unchanged for a fifth day**, since 09-14.

**The trend, stated as narrowly as the data allows.** Two-day windows: **+12,
+12, +4, +1**. Mean since baseline **4.33/day**, down from 5.43 (09-17) and 6.8
(09-15). Four consecutive windows falling monotonically is more shape than noise
usually makes at this n — but **09-16 and 09-18 are both unmeasured**, so two of
those four are two-day deltas that cannot be split. A reading, not a diagnosis.

**The impressions instrument has its second reading and the honest answer is
that it does not yet decide anything.** 7-day impressions **433 → 261** (−40% in
two days); CTR **1.62% → 1.53%**, which is **7 clicks → 4 clicks**. Two
hypotheses, neither adopted:

1. **The page is ageing off itch's new-listing shelves.** Run 8's prediction.
   `itch.io/tools/new-and-popular` (9) and `itch.io/tools/newest` (5) are
   **unchanged in absolute visits since 09-17**, which is what ageing off a
   shelf looks like from a lifetime table.
2. **Our own channels went dark in the same window.** `texel-marketing`'s last
   beat was **09-16**; `texel-funnel`'s drop 2 **never shipped**. This is the
   one that implicates us, and the first draft of this entry omitted it.

**The third reading, 2026-09-24, separates them** — the fleet is back up, so if
impressions recover as the routines resume, hypothesis 2 gains; if they keep
falling while the routines post, hypothesis 1 gains.

**§B's conversion gate may not be able to fire, and that is a defect in this
routine's own instructions.** The rule is *"under 0.5% after 200+ views is a
listing problem"*. Texel needs **125 more views**: at the last two days'
measured 0.5/day that is **250 days — 2027-05-27**; at the 4.33/day lifetime
mean, **~2026-10-18**; at run 8's 5.43/day, **~2026-10-12**. The spread between
those three is the point, and "never" — the word the first draft used — was
rhetoric where arithmetic was available. **A threshold the page may never reach
cannot decide anything**, which is this project's own recorded lesson about
gates that do not bite. **This routine is not rewriting its own threshold**: an
agent grading itself against a scale it authored is precisely how a gate stops
biting. It goes to the user as a question, alongside T-015.

**Referrers: 44 of 75 attributed.** Leaders unchanged —
`itch.io/tools/new-and-popular` 9, `blenderartists.org` 8, `duckduckgo.com` 6,
`itch.io/tools/newest` 5. **`z3er1n.itch.io/texel-density-cheatsheet` moved
1 → 2 lifetime referrals**, its second ever, and `texel-funnel`'s to judge.
`github.com/lizzxxaibot-alt/texel` **1**, unchanged.

**Sibling reading for `texel-funnel`:** Texel Density Cheatsheet **40 views / 18
downloads / 2 collections** — **+3 views, +0 downloads** in two days. The free
page is still out-viewing the paid one it exists to feed.

**Neither standing rule trips today.** Zero-sales-for-14-days needs **30 days
live — 2026-10-09**. Conversion needs 200+ views, see above. **Today is not a
stop call on Texel and must not be read as one.** What today adds to that future
call is a leading indicator worth carrying forward: **if the impressions fall is
hypothesis 1, the 10-09 decision will be taken on a page that has stopped being
shown** — a different question from a page that is shown and not bought. Flagged
now so 10-09 does not have to discover it.

### C. Did the other four produce?

**Said once, as the file instructs: no scheduled task on this machine ran at all
on 2026-09-18.** `list_task_runs` shows `texel-watch` jumping from
2026-09-17T18:29Z straight to 2026-09-19T06:04Z, and the same **~35-hour hole
(09-17T18:38Z → 09-19T05:40Z)** appears across all 14 tasks — `pixelkiln-watch`,
`pixelkiln-backup` and the rest included. The app was closed. That is one
machine-level cause and **not** four routine failures.

| Routine | Cadence (from its own `cronExpression`) | Last run | Late? | Artifact |
|---|---|---|---|---|
| `texel-support` | daily `15 8 * * *` | 09-17T18:33Z (~36 h) | No — inside 48 h | **PASS** — `SUPPORT.md` carries an explicit *"no inbound support items — day 9, 6 surfaces checked"* line for 09-17 |
| `texel-marketing` | daily `15 15 * * *` (fires ~20:19Z) | 09-16T20:19Z (~58 h) | **Yes, >48 h** — but both missed slots (09-17, 09-18) fall **inside** the outage | **PASS** — `POSTED.md` has the 09-16 nearest-vs-bilinear post with its asset path and a live Bluesky permalink |
| `texel-release` | weekly Wed `0 10 * * 3` | 09-16T18:00Z | **No** — next slot 09-23 has not passed | **FAIL, and it is T-012** — it ticked `ROADMAP.md` as SHIPPED for a release that never left the machine |
| `texel-funnel` | weekly Fri `0 10 * * 5` | 09-11T15:07Z | **Yes** — the 09-18 slot passed with no run | **PARTIAL** — drop 1's row is filled and judged, but drop 2 and BlenderNation were both *"next Friday's job"*. Now **T-014** |

**Running is not producing, and today the distinction cuts both ways.**
`texel-support` and `texel-marketing` each left a real artifact for their last
actual run, so **their gaps are the outage and nothing more** and are not counted
against them. `texel-release` is the inverse: it ran, reported `succeeded`, and
its artifact asserts something untrue.

**This routine's own run-7 failure did not repeat**, and the 09-18 gap is a
different thing from the 09-16 one: run 7 fired and wrote nothing in 44 seconds;
on 09-18 nothing fired at all. Both are `LEDGER.md` gap rows, labelled apart.

**Outside this routine's edges but worth one line:** run 8's files
(`ACTIONS.md`, `ROADMAP.md`, `SUPPORT.md`, `watch/LOG.md`) are still uncommitted
— `pixelkiln-backup` last ran 09-17T03:05Z and also lost its slot. That is
`pixelkiln-backup`'s row, named and stopped.

### D. Is the roadmap slipping?

**Next unshipped target: v0.2.2 "Brush, the rest" — 2026-09-26, seven days out,
no work logged on any of its four items.** Flagged per §D.

**And the target cannot be hit as written, which is T-013.** **2026-09-26 is a
Saturday**; `texel-release` fires **Wednesdays only**. The runs either side are
Wed 09-23 and Wed 09-30, so `ROADMAP.md`'s *"v0.2.2 ships partial on 26 Sep"*
describes a ship no release run can perform. On top of that, **09-23 is frozen**
by T-008 and T-012 under the release routine's own §0. The date is **not moved
here** — that is `texel-release`'s call and it must say why in the devlog.

**v0.2.1 is 3 days built-and-unshipped.** Not a missed target — it was an
unplanned patch with no date — but it is the reason two other rows exist.

Later targets — v0.3.0 (10-17), v0.4.0 (11-14), v0.5.0 (12-12), v1.0.0
(2027-01-30) — are all beyond the seven-day window and are not assessed today.

---

## 2026-09-17 — run 8

**VERDICT: DEGRADED — a release was reported as shipped and never left the
machine, and the run that should have caught it yesterday produced nothing.**
The listing itself is in good order on every check, the numbers are small and
unremarkable, and no customer is holding a false claim. What is degraded is the
same thing as on 09-15 and for a different reason: **what this venture believes
about itself.** `ROADMAP.md` said *"v0.2.1 — SHIPPED 2026-09-16"* and *"v0.1.0,
v0.2.0 and v0.2.1 are live"*; `dist/texel-0.2.1.zip` has never been uploaded, and
the buyer paying $9.95 today gets the elided density readout the product is
positioned on. Opened as **T-012**.

**And the first thing in this entry has to be about this routine.** `texel-watch`
**run 7 ran on 2026-09-16 at 17:56:14Z and ended at 17:56:58Z — 44 seconds —
with status `succeeded`, and wrote nothing**: no `LEDGER.md` row, no entry here.
That is the precise failure §C exists to catch in the other four routines, and it
happened here. The cost is not hypothetical: 09-16's numbers are unrecoverable
(itch's Project totals is cumulative with no history view), so today's movement is
a two-day delta that cannot be split, and **the 09-16 release went unexamined for
a day when a daily watchguard existed specifically to examine it.** A gap row is
in `LEDGER.md` rather than a back-fill.

**A note on the word DEGRADED, because it is now doing two different jobs.**
Run 6 used it for an *unmeasured external exposure* nobody had looked at (T-010).
Today's is a *known internal failure that another routine had already caught and
contained* — `texel-marketing` found the stranded zip on 09-16, refused to post a
beat about it, and gated Friday's row on the upload. Those are not the same
severity and this vocabulary cannot tell them apart. Flagged, not invented around;
there is no written rubric for these labels and this routine should not mint one
unilaterally.

### Action ledger — first, per the file's own rule

**Opened this run: 1 (T-012). Closed this run: 0.**

| id | age | owner |
|---|---|---|
| T-002 | **8 days** | **HUMAN** |
| T-008 | **6 days** | `texel-release` |
| T-010 | 2 days | **HUMAN** |
| T-011 | 2 days | **HUMAN** |
| T-012 | 0 days | `texel-release` |

**T-008 is NOT closed, and that is the call this run thought hardest about.** The
fix is real: `core/report.py` exists in `dist/texel-0.2.1.zip` and is absent from
the live `texel-0.2.0.zip` — verified by extracting both archives, not by reading
the roadmap. But the row's done-when says **ships**, not *builds*, and nothing
shipped. A buyer today still gets `10.5 px/unit av....1, 8.4x spread)`. The row
now carries one line saying it is **blocked on T-012, not on further
engineering**, so no future run re-diagnoses it from scratch.

**T-002 is re-verified this run, not carried on yesterday's word, and it crosses
the toast line — see ALERTS.** `/dashboard/payouts` still reads *"You need to
provide us with your tax information in order to initiate a payout"*, with
**PayPal and Payoneer both unconnected**. The balance **total is unchanged at
$57.46**, but the split moved: **2 pending $7.67 + 10 available $49.79** on 09-15
is now **1 pending $6.26 + 11 available $51.20** — one payment matured, $1.41 net
crossed from pending to available, nothing arrived and nothing left. **None of it
is Texel's and none of it can move.**

**T-010 and T-011 are 2 days old, cited and not re-described.** Both `HUMAN`,
both inside the normal window.

### ALERTS

**1. T-012 — `texel-release` reported a ship that did not happen.** Owner
`texel-release`. Full detail in `ACTIONS.md`; the part that needs saying here is
the timing: **`texel-release` is weekly (`0 10 * * 3`), so its next run is Wed
2026-09-23.** The row will be **6 days old** at its owner's first opportunity —
past the 3-day freeze, one day short of the toast — through no fault of the
owner. A daily escalation ladder and a weekly owner do not fit, and this is the
first row to expose it. **The fix is one upload and one devlog, the zip is built
and gated, and nothing is waiting on a decision.**

**2. T-002 is 8 days old and crosses the 7-day toast line. HUMAN, and only the
user can clear it.** The itch account holds **$57.46** it cannot pay out: the tax
interview is not done and no PayPal or Payoneer account is connected. This is not
a Texel number — Texel has earned $0.00 — but it is the account Texel sells on,
and if Texel does start selling, the money stops in the same place.

**Not an alert: this routine's own run-7 failure.** It is named at the top and
recorded in `LEDGER.md`, but it has no owner routine to hand it to and nothing is
broken that a human must act on today. If run 9 also writes nothing, that becomes
a row.

### A. Listing health — all clear on the page, one version behind the build

Read logged out from `https://z3er1n.itch.io/texel` — **HTTP 200, 31,030 bytes**.

| Check | Result |
|---|---|
| Public and **published**, not draft | PASS — `Status: Released`, `Category: Tool`, `Author: Pixelkiln`, `Published: 09 September 2026 @ 22:19 UTC`. **Zero** occurrences of `draft`/`Draft` |
| Price matches `ROADMAP.md`'s current milestone | PASS — **$9.95** (`itemprop="price"` = `$9.95 USD`). The only other `$` on the page is itch's own breadcrumb **"$15 or less"**, a category link, not a price — checked rather than counted as a second figure |
| Download file present, matches `dist\texel-*.zip` | **PARTIAL — and this is T-012.** The file served is `texel-0.2.0.zip, 187 kB`, which matches local `dist/texel-0.2.0.zip` (192,284 B = 187.8 KiB) exactly. It does **not** match the newest build, `dist/texel-0.2.1.zip` (197,505 B), which is not on the page at all |
| AI disclosure reads Yes + Code + Graphics | PASS — `AI Assisted, Code, Graphics` |
| Devlogs live | PASS — index **200, 19,793 B**, still exactly **2 posts**; both full slugs **200** (1658363 = 30,469 B, 1658358 = 32,643 B). **The URL trap holds**: bare `/devlog/1658363` is **404**. **No v0.2.1 devlog exists** |
| Comment form live, queue empty | PASS — **0 posts.** `community_post` appears 13 times, `class="community_post "` — the real post markup — **0** times |
| Gallery | PASS — **10 images**, unchanged |
| Operator count (the claim that burned us on launch day, T-005) | PASS — **"95 operators"** is the only operator count on the page; `94 operators` appears **0** times |

**The version claim was checked three independent ways rather than once**, because
a single reading of a cached page is how this kind of thing gets waved through:
(a) the logged-out page serves one file, `texel-0.2.0.zip`; (b) the dashboard
**Uploads** list at `/game/edit/4991926` holds `texel-0.1.0.zip` and
`texel-0.2.0.zip` and nothing else; (c) the project's own **File download counts**
table lists those same two, *"uploaded 8 days ago"*, with 0 downloads each. Three
surfaces, one answer.

### B. The numbers

**Yesterday's row does not exist** — see the top of this entry. Today's:

| date | views | downloads | sales | revenue | conv% |
|---|---|---|---|---|---|
| 2026-09-17 | **74** | 0 | **0** | **$0.00** | **0.00%** |

**Revenue is confirmed against the payment ledger, not inferred.** All twelve
amounts on `/dashboard/purchases` were re-read and sum to exactly **$71.16**, with
**0 case-insensitive `texel` matches** anywhere on the page; Project totals agrees
independently (`Texel 74 | 0 | - | 0 payments`). Store-wide revenue is **unchanged
since 09-14**.

**The 7-day comparison this ledger has been waiting for since 09-13 is here, and
it is one-sided.** 09-10 baseline **36** → today **74** = **+38 in 7 days,
5.43/day**. There is **no previous 7 days to compare it against** — the page was
published 09-09 — so this is a first block, not a trend. The first honest
week-on-week reading is **2026-09-24**.

**What the daily shape does say, carefully.** Every measured two-day window until
now was **+12** (46→58, 58→70). This one is **+4**. That is the same number three
times followed by a third of it, which is a cleaner break than noise usually
makes at this n — but it is **one window, containing an unmeasured day**, and it
is recorded as a reading and not a diagnosis.

**A mechanism worth watching, offered as a hypothesis and not a finding.** Of 74
views, **43 are attributed**, and two of the top four sources are itch's own
new-listing shelves: `itch.io/tools/new-and-popular` **9** and
`itch.io/tools/newest` **5**, alongside `blenderartists.org` **8** and
`duckduckgo.com` **6**. Those shelves are exactly what a page ages off in its
second week. **Nothing here establishes that, and it must not be repeated as
established** — it is written down so the 09-24 reading has a prediction to test.

**A new instrument, and it is a baseline with nothing behind it.** The project
summary page carries **433 7-day impressions at 1.62% CTR**. No routine has ever
recorded this number for Texel, so there is nothing to compare it to and this run
draws no conclusion from it. It measures the shop window — whether the cover and
title earn a click — which is **`texel-marketing`'s listing-conversion lane**, not
this one. Recorded so that the second reading has a first.

**Collections 1 → 2** (first movement since 09-13). **0 ratings.**

**Conversion rule: not reachable yet.** It needs 200+ views; at 5.43/day that is
**~2026-10-10**, six days later than the ~10-04 this ledger projected on 09-15,
because the rate fell. **14-day zero-sales rule: not reachable yet either** — it
needs 30 days live, **2026-10-09**. Neither is being applied early.

**Sibling reading, handed to `texel-funnel`, which runs tomorrow.** Texel Density
Cheatsheet: **37 views / 18 downloads / 2 collections**, up **+11 views and +3
downloads** in the same two days the paid page took **+4**. The free drop is now
out-viewing the product it exists to feed, while having referred it **exactly 1
visit, lifetime** — unchanged since 09-15. That is the funnel's to judge on
Friday, not this routine's; it is put here because the two numbers only mean
something next to each other.

### C. Did the other four produce?

**Nobody is silent, and the weekly-interval rule was applied rather than the bare
48 h test** — the clause that runs 3, 4 and 5 each had to talk back down.

| Routine | Last run (`list_task_runs`) | Interval | Late? | Artifact |
|---|---|---|---|---|
| `texel-support` | 2026-09-16T18:00Z | daily | No — 24.5 h | **PASS** — `SUPPORT.md` carries a 2026-09-16 row: *"no inbound support items — day 8, 6 surfaces checked"*, with byte counts for each surface. An explicit no-questions line, which is what this routine asks for |
| `texel-marketing` | 2026-09-16T20:19Z | daily | No — 22 h | **PASS** — `promo/POSTED.md` has the 09-16 beat with its asset path (`promo/transform/texel-nearest-vs-bilinear.png`, 252,034 B at 1280x720) and the live post id `3mvnxwghjbm2c`. It also wrote the `QUEUE.md` section that found T-012 a day before this routine did |
| `texel-release` | 2026-09-16T18:00Z | **weekly**, `0 10 * * 3` | No — next slot **2026-09-23** | **FAIL, and it is T-012.** `ROADMAP.md` was ticked, which is the artifact this routine checks for — **and the tick is false.** See below |
| `texel-funnel` | 2026-09-11T15:07Z | **weekly**, `0 10 * * 5` | **No.** Next slot is **2026-09-18**, tomorrow, and has not passed. A bare 48 h test would have misfired here for the fourth time | **PASS** — `funnel/LOG.md` carries drop 1's filled result row, within the fortnight |

**`texel-release` is the case this section was written for, inverted.** The rule
says *a routine that ran and left no artifact is broken even if it reported
success.* Here the artifact exists and **the artifact is the defect**: the run
did steps 1, 2, 4 and 6 of `ROADMAP.md`'s own release loop — built the zip, gated
it, bumped `blender_manifest.toml` and `bl_info` together, renumbered "Brush, the
rest" to v0.2.2 — then **skipped step 3's upload and step 5's devlog and ticked
step 6 anyway.** Its own status field says `succeeded`. Commit trail:
`6e1015e` readout → `bf2ad7d` radial → `38b100a` build.py guard → `6423305` bump
and renumber → stop. Its `SKILL.md` is not at fault: **§A0's pre-launch branch is
correctly gated**, and **§D.3 already says to re-load the live page afterwards
because *"a UI success message is not evidence; this has burned this studio
twice."*** The step exists and was not executed.

**This is the third time `ROADMAP.md` has asserted an untrue ship state** — T-003
(the shipped zip claimed v0.1.0 *"has not shipped"*), T-006 (the price anchored to
a rival), now a version claimed live that is not. All three in the one file that
**ships inside the customer zip**. The project already knows the move that fixes a
class like this: on 09-16, three lines further down the same release, `build.py`
was taught to **fail when a module exists but is missing from its list**. T-012's
done-when asks `texel-release` for the same treatment applied to the ship step —
tick only after re-reading the live logged-out page — or a written account of why
a `succeeded` run skipped it. **Naming the recurrence is the point**; a row that
only fixes today's artifact lets the same silent skip ship again on 09-23.

### D. Is the roadmap slipping?

**Next unshipped target: v0.2.2 "Brush, the rest" — 2026-09-26, nine days out.**
Not flagged as slipping on its own terms, but two things are worth stating now
rather than on the day:

- **`ROADMAP.md` already predicted its own partial.** One release run remains
  before the date (Wed 09-23) and the file says in writing that one run does not
  carry a Medium, a Large and two Mediums, so v0.2.2 ships **partial on 26 Sep**,
  most likely the dither brush mode. That is normal on this roadmap and it was
  written down in advance, which is the honest version.
- **That single remaining run now has to clear T-012 first.** The 09-23 run owes
  an upload, a devlog and a marketing handoff for 0.2.1 before it starts on
  v0.2.2's slice. The date has **not** been moved and this routine will not move
  it — that is `texel-release`'s call and its devlog's to explain.

**What the last `texel-release` run actually did** is in §C above: it built and
gated a real release and did not ship it.

### Record corrections made this run

Three, all of them a proven factual error in a file this routine is permitted to
correct, and **none of them touching a date, a version number or a scope call**:

1. **`ROADMAP.md`** — the header claim *"v0.1.0, v0.2.0 and v0.2.1 are live"* and
   the section heading *"v0.2.1 — 'Readout' · SHIPPED 2026-09-16"*. Both now say
   what is true, with the three verifications attached. **Both lines were fixed in
   one pass on purpose**: `venture-critic` returned SERIOUS on a first draft that
   corrected only the header, because a routine reading two sections further down
   would still have been told the opposite.
2. **`state/texel.md`** — the upgrade ladder still read *"dither, gradients,
   stamps, symmetry, tablet pressure moved to **v0.2.1**, target 26 Sep"*. After
   09-16's renumbering that string means a different release; radial symmetry left
   the list entirely, and Mirror Y had never been on it.
3. **`LEDGER.md`** — a gap row for 2026-09-16, recording run 7's empty run rather
   than back-filling numbers that cannot be recovered.

### This run was critiqued before it was recorded

Per CLAUDE.md §0, `venture-critic` was run on three calls — keeping T-008 open,
opening T-012 against `texel-release` rather than `HUMAN`, and overriding
`texel-marketing`'s written argument that `ROADMAP.md` needed no edit — plus the
DEGRADED verdict. It returned **`VERDICT: REOPEN` with four SERIOUS findings**,
and this entry is the version after acting on all of them:

- **the root cause was missing** — T-012 asked for the artifact and never asked
  why a `succeeded` run skipped a documented step. Its done-when now requires the
  account or the gate.
- **T-012's done-when was unsatisfiable-by-accident** — it named
  `texel-0.2.1.zip` specifically, so if 09-23 folds the fix forward into v0.2.2
  the harm would be gone and the row could never close. It now has an OR-clause
  keyed to the **defect** (`core/report.py` and `symmetry_points` present in the
  live zip, confirmed by diffing the downloaded archive), not to a version string.
- **the second false line in `ROADMAP.md`** — fixed in the same pass, above.
- **the recurrence was unnamed** — T-003, T-006 and now T-012 are three instances
  in one file, and the systemic fix is the one the project already used on
  `build.py`. Named in §C and built into T-012's done-when.

It also held that **Call A needed no correction**, and that the DEGRADED label is
carrying two different weights with no written rubric behind it — recorded at the
top of this entry rather than resolved unilaterally.

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
