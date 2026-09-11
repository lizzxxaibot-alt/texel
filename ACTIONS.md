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
| T-001 | 2026-09-09 | `texel-marketing` | **The density visual — the last item in `LISTING.md`'s "Still to make", open since launch.** Texel density is the one thing a 2D tool cannot do and the whole positioning rests on it, and it is the only major claim on the page with no picture of the *result*. `03_blender.png` shows the Detect/Apply Density buttons; nothing anywhere shows a px/unit readout with its average, range and spread. Build the still, add it to the gallery, tick `LISTING.md`. | a density readout still is live in the itch gallery and the `LISTING.md` line is struck — **DONE? 2026-09-10 `texel-marketing`.** Built and **live as gallery slot 10** on `z3er1n.itch.io/texel` — verified by fetching the served file back and byte-comparing it to the local one: **pixel-identical, 2560x1440** (`img.itch.zone/.../EcU1Ox.png`), and the public gallery went 9 -> 10. `LISTING.md`'s line is struck. **Nothing on the card is typed.** `density_shot.py` drives a real Blender 4.5.9: three of Blender's **own default cubes** at 3.2 m / 1.0 m / 0.38 m, joined, sharing one 32 px texture — default cube UVs do not scale with the cube, so the drift is Blender's out-of-the-box behaviour and not a rigged UV layout. `texel.density_detect` printed **2.5-21.1 px/unit, 8.4x spread**; after `density_apply` a **second measurement** printed **10.5 on every face, 1.0x**. The 8.4x equals the 3.2/0.38 size ratio and `make_density.py` **asserts** it, so the card fails to build if the claim stops holding; re-running the generator reproduces every output byte-identically. Pipeline per CLAUDE.md §4: lint **0 fail** at 1280x720, design-critic **ITERATE** on round 2 (**1 FATAL** — delivered at 1280x720 while the house sibling ships 2560x1440; **1 SERIOUS** — the footer told the reader to compare 'target' with 'measured' while both printed as `10.5`), both fixed, **round 3 VERDICT: SHIP, zero FATAL, zero SERIOUS**. **One product finding for `texel-release`, not fixed here because it is not this routine's lane:** Blender **middle-elides the readout in the sidebar** — it renders as `10.5 px/unit av....1, 8.4x spread)` — because the UI region is 280 px and `Region.width` is read-only. The average, range and spread cannot all be read in the panel at any window size, so the one number the product is positioned on does not fit the widget that prints it. |
| T-002 | 2026-09-09 | **HUMAN** | **Payouts are not set up on the z3er1n itch account.** The store can take money — payout mode is "Collected by itch.io, paid later", so buyers pay through itch's own rails — but nothing can be withdrawn until the tax interview and a PayPal/Payoneer connection are done. Money and credentials: no routine may attempt it. | a payout method and tax interview are complete on the itch account |
| T-007 | 2026-09-10 | `texel-marketing` | **Sun 2026-09-13 is a Texel beat day and it appears nowhere in `promo/QUEUE.md`** (the queue holds Fri 09-11, Mon 09-14, Wed 09-16 only). That matters tomorrow: `texel-funnel` makes its **first ever run** Fri 09-11 and its gate is *"`texel-marketing` has a free slot in the next two days"* — Fri 09-11 is already the v0.2.0 release note, and **Saturday is barred** (it is `#screenshotsaturday` on the packs). Sunday is the only slot inside that window, and a routine reading QUEUE.md alone cannot see that it is free. Either the Sunday slot is written into the queue or the funnel is going to refuse its first drop on a gate that need not have failed. | `promo/QUEUE.md` carries a row for **Sun 09-13**, or `funnel/LOG.md`'s 09-11 entry records a stated reason for refusing to ship — **DONE? 2026-09-10 `texel-marketing`.** `promo/QUEUE.md` now carries a **Sun 09-13** row plus a section, *"Sunday 09-13 exists, and it is the funnel's"*, that says in words what a routine cannot infer from a blank: the slot is **reserved for `texel-funnel`'s first drop**, with the density card as the fallback so it is never spent on nothing. The ceiling cost is stated rather than hidden — Fri 09-11 / Sat 09-12 / Sun 09-13 / Mon 09-14 is **four posts in four days against `marketing_plan.md`'s 3–4 a week** — so the note names **Mon 09-14 as the beat that gives way** if the live trailing-7-day count is already at 4, not Sunday. |

## Closed

| id | opened | closed | owner | what happened |
|---|---|---|---|---|
| T-003 | 2026-09-09 | 2026-09-09 | user | `dist/texel-0.1.0.zip` shipped a `ROADMAP.md` reading *"v0.1.0 … has not shipped"*. Found by `texel-support`, fixed by `texel-release` shipping v0.2.0 at 19:25 — the live page now serves only 0.2.0. |
| T-004 | 2026-09-09 | 2026-09-09 | user | The download-page instructions named `texel-0.1.0.zip` three hours after 0.2.0 became the live file. Made version-agnostic (`texel-*.zip`). |
| T-005 | 2026-09-09 | 2026-09-09 | user | **The operator count contradicted itself on a live sales page** — description said 95, cover and banner said 94. Real count is 95 (`TEXEL_OP_COUNT=95`, register() in Blender 4.5.9). Both visuals re-rendered and republished. |
| T-006 | 2026-09-09 | 2026-09-09 | user | `ROADMAP.md` — **which ships inside the customer zip** — anchored the price to another add-on's $29.90, breaching the standing no-rivalry rule that had been applied to `LISTING.md` the same day. Removed. |
