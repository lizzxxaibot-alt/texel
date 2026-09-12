# Texel — the action ledger

Same mechanism as `pixelkiln\launch\watch\ACTIONS.md`, and it exists for the same
reason (2026-09-09, user): **`texel-watch` judges and never fixes, which is
correct, but a judge with no bailiff produces nothing.** On the Pixelkiln side
three consecutive watch runs named the same findings and none of them moved for
eight days. This file is what stops that happening here while the venture is new
enough to fix cheaply.

## The rules

- **`texel-watch` is the only routine that OPENS a row, and the only one that
  CLOSES one.** It closes against evidence a doer wrote, never a promise.
- **Every doer — `texel-release`, `texel-support`, `texel-marketing`,
  `texel-funnel` — clears its open rows BEFORE its own agenda.** Section 0 of
  each SKILL.md.
- **A doer never closes a row.** It does the work, appends evidence, sets state
  to `DONE?`.
- **Owner `HUMAN`** = credentials, money, a payout or tax form, an account
  signup. Never assigned to a routine, never retried by one.

## The escalation ladder

| Age | What happens |
|---|---|
| 0–2 days | Normal. The owner clears it next run. |
| **3+ days** | **The owner routine may do NOTHING ELSE until the row is cleared, or it writes a dated refusal with a reason.** |
| **7+ days** | `texel-watch` toasts the user. Only rows this old, and `HUMAN` rows. |
| **14+ days** | Watch stops re-reporting and must recommend **killing the finding or killing the routine that will not do it.** |

## Open

| id | opened | owner | action | done when |
|---|---|---|---|---|
| T-002 | 2026-09-09 | **HUMAN** | **Payouts are not set up on the z3er1n itch account.** The store can take money — payout mode is "Collected by itch.io, paid later", so buyers pay through itch's own rails — but nothing can be withdrawn until the tax interview and a PayPal/Payoneer connection are done. Money and credentials: no routine may attempt it. | a payout method and tax interview are complete on the itch account |
| T-008 | 2026-09-11 | `texel-release` | **Blender middle-elides the density readout in the sidebar, so the one number the product is positioned on cannot be read in the panel that prints it.** It renders as `10.5 px/unit av....1, 8.4x spread)` — the N-panel region is 280 px and `Region.width` is read-only, so the average, the range and the spread cannot all be shown at any window size. Reported by `texel-marketing` while building the density card (T-001) and in `LISTING.md` lines 398-403, explicitly handed off as *"not this routine's lane"* — so it has been named twice by a doer and owned by nobody. **This routine has not reproduced it**; it is opened because a product defect on the marquee feature with no owner is exactly what this ledger exists to stop. The listing works around it by setting the figures as type on the card; the buyer who installs the add-on gets the elided string. | `texel-release` either ships a readout whose average, range and spread are all legible in the sidebar at its default width (split label/value rows, a multi-line `layout.label` stack, or the figures in a popover), **or** `ROADMAP.md` carries a dated line saying it will not be fixed and why — a reproduction attempt that fails also closes it, written up with the Blender version. |

## Closed

| id | opened | closed | owner | what happened |
|---|---|---|---|---|
| T-003 | 2026-09-09 | 2026-09-09 | user | `dist/texel-0.1.0.zip` shipped a `ROADMAP.md` reading *"v0.1.0 … has not shipped"*. Found by `texel-support`, fixed by `texel-release` shipping v0.2.0 at 19:25 — the live page now serves only 0.2.0. |
| T-004 | 2026-09-09 | 2026-09-09 | user | The download-page instructions named `texel-0.1.0.zip` three hours after 0.2.0 became the live file. Made version-agnostic (`texel-*.zip`). |
| T-005 | 2026-09-09 | 2026-09-09 | user | **The operator count contradicted itself on a live sales page** — description said 95, cover and banner said 94. Real count is 95 (`TEXEL_OP_COUNT=95`, register() in Blender 4.5.9). Both visuals re-rendered and republished. |
| T-006 | 2026-09-09 | 2026-09-09 | user | `ROADMAP.md` — **which ships inside the customer zip** — anchored the price to another add-on's $29.90, breaching the standing no-rivalry rule that had been applied to `LISTING.md` the same day. Removed. |
| T-001 | 2026-09-09 | 2026-09-11 | `texel-marketing` | **CLOSED against evidence, verified independently this run.** The density readout still is **live as gallery slot 10** on `z3er1n.itch.io/texel` — the logged-out page (HTTP 200, 30,963 B) renders **10 `screenshot_list` images**, up from 9, and the asset id `EcU1Ox` the doer recorded is present in that list. `LISTING.md` line 386 is struck. The doer's build evidence stands on its own terms: `density_shot.py` drives a real Blender 4.5.9, nothing on the card is typed, `make_density.py` asserts the 8.4x = 3.2/0.38 claim so the card fails to build if it stops holding, and the CLAUDE.md §4 loop ran to **round 3 VERDICT: SHIP, zero FATAL, zero SERIOUS**. The product defect the doer surfaced while building it is **not** closed with this row — it is now **T-008**, owned by `texel-release`. |
| T-007 | 2026-09-10 | 2026-09-11 | `texel-marketing` | **CLOSED against evidence, verified this run.** `promo/QUEUE.md` now carries a **Sun 09-13** row (beat: reserved for `texel-funnel`'s first drop, fallback the density card with its asset path) **and** a named section, *"Sunday 09-13 exists, and it is the funnel's"*, which says in words what a blank row cannot: the slot is unclaimed-and-reserved rather than non-existent. The over-ceiling cost is stated rather than hidden, and **Mon 09-14 is named as the beat that gives way**, not Sunday. `texel-funnel`'s first ever run is today at 10:07 and its gate — *"`texel-marketing` has a free slot in the next two days"* — is now readable as satisfied from inside `QUEUE.md` alone. Whether the funnel actually ships is its own run's business and will be judged tomorrow, not here. |
