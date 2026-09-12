# Texel — watchguard log

Newest entry first. Written by `texel-watch` (daily 06:45). This routine judges;
it does not fix, post, build or answer. Every action it finds is opened as a row
in `../ACTIONS.md` and handed to a named owner.

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
