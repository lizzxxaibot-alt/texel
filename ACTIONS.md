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
| T-001 | 2026-09-09 | `texel-marketing` | **The density visual — the last item in `LISTING.md`'s "Still to make", open since launch.** Texel density is the one thing a 2D tool cannot do and the whole positioning rests on it, and it is the only major claim on the page with no picture of the *result*. `03_blender.png` shows the Detect/Apply Density buttons; nothing anywhere shows a px/unit readout with its average, range and spread. Build the still, add it to the gallery, tick `LISTING.md`. | a density readout still is live in the itch gallery and the `LISTING.md` line is struck |
| T-002 | 2026-09-09 | **HUMAN** | **Payouts are not set up on the z3er1n itch account.** The store can take money — payout mode is "Collected by itch.io, paid later", so buyers pay through itch's own rails — but nothing can be withdrawn until the tax interview and a PayPal/Payoneer connection are done. Money and credentials: no routine may attempt it. | a payout method and tax interview are complete on the itch account |

## Closed

| id | opened | closed | owner | what happened |
|---|---|---|---|---|
| T-003 | 2026-09-09 | 2026-09-09 | user | `dist/texel-0.1.0.zip` shipped a `ROADMAP.md` reading *"v0.1.0 … has not shipped"*. Found by `texel-support`, fixed by `texel-release` shipping v0.2.0 at 19:25 — the live page now serves only 0.2.0. |
| T-004 | 2026-09-09 | 2026-09-09 | user | The download-page instructions named `texel-0.1.0.zip` three hours after 0.2.0 became the live file. Made version-agnostic (`texel-*.zip`). |
| T-005 | 2026-09-09 | 2026-09-09 | user | **The operator count contradicted itself on a live sales page** — description said 95, cover and banner said 94. Real count is 95 (`TEXEL_OP_COUNT=95`, register() in Blender 4.5.9). Both visuals re-rendered and republished. |
| T-006 | 2026-09-09 | 2026-09-09 | user | `ROADMAP.md` — **which ships inside the customer zip** — anchored the price to another add-on's $29.90, breaching the standing no-rivalry rule that had been applied to `LISTING.md` the same day. Removed. |
