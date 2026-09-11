# Texel — watchguard log

Newest entry first. Written by `texel-watch` (daily 06:45). This routine judges;
it does not fix, post, build or answer. Every action it finds is opened as a row
in `../ACTIONS.md` and handed to a named owner.

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
