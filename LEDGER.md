# Texel — the numbers ledger

Owned by `texel-watch` (daily 06:45). **Nothing else writes to this file.**

Created **2026-09-10**, the first watch run after Texel went live on 2026-09-09.

## What the columns are, so a later run does not misread them

- **Cumulative, not daily.** itch's *Project totals* table on
  `/dashboard/analytics` is all-time per project. Every row here is the running
  total at the moment it was read; a day's movement is the difference between
  two rows, which is why the first row is a **baseline and not a trend**.
- **Revenue does NOT come from that table.** Project totals attributes money to a
  project and therefore cannot see a bundle purchase — this is the mistake that
  hid an $8.92 sale for five days on the pack side (STATE.md, 2026-09-09). Money
  is read from **`/dashboard/purchases`**, itch's real payment ledger, and
  cross-checked against Project totals.
- **conv% = sales / views**, on the cumulative figures.

| date | views | downloads | sales | revenue | conv% | note |
|---|---|---|---|---|---|---|
| 2026-09-10 | 36 | 0 | 0 | $0.00 | 0.00% | **Baseline row.** Page ~36 h old. Store ledger reads $63.70 / 11 payments and **contains no Texel row** — the 0 is confirmed against the ledger, not only against Project totals. 0 ratings, 0 collections. |
| 2026-09-11 | 46 | 0 | 0 | $0.00 | 0.00% | **+10 views in 24 h.** Store ledger unchanged at $63.70 / 11 payments, **still no Texel row** — 0 confirmed against `/dashboard/purchases`, not only Project totals. 0 ratings, 0 collections. Two rows is not a trend; the conversion rule needs 200+ views (~2026-09-26 at this rate) and the 14-day rule needs 30 days live (~2026-10-09). |
| 2026-09-12 | 51 | 0 | 0 | $0.00 | 0.00% | **+5 views in 24 h, against +10 the day before.** Three rows is still not a trend and n is far too small for a halving to mean anything — recorded as a number, not a slowdown. Store ledger unchanged at **$63.70 / 11 payments**, **still no Texel row**; `/dashboard/purchases` read directly, not inferred from Project totals. 0 ratings, 0 collections. Conversion rule needs 200+ views (~2026-09-20 at +5/day, ~2026-09-26 at +10); the 14-day rule needs 30 days live (~2026-10-09). |
| 2026-09-13 | 58 | 0 | 0 | $0.00 | 0.00% | **+7 views in 24 h** (+10, +5, +7 across the three measured days). **First ever collection: 0 → 1.** Store ledger unchanged at **$63.70 / 11 payments**, **still no Texel row** — `/dashboard/purchases` read directly. 0 ratings. Four rows is not a 7-day trend; the first honest weekly comparison is **2026-09-17**. Conversion rule needs 200+ views: at the measured 7.3/day that is **~2026-10-03**; the 14-day rule needs 30 days live, **~2026-10-09**. Sibling reading for `texel-funnel`: **Texel Density Cheatsheet 17 views / 11 downloads** on day 2 of its 72 h window. |
| 2026-09-14 | 63 | 0 | 0 | $0.00 | 0.00% | **+5 views in 24 h** (+10, +5, +7, +5 across the four measured days; mean **6.75/day** since the baseline). Store ledger **moved for the first time since this ledger opened — $63.70 / 11 → $71.16 / 12 payments — and the new payment is NOT Texel's.** All 12 amounts read off `/dashboard/purchases` sum to exactly $71.16 and **none of them is a Texel row** (0 literal `texel` matches in the page text); Project totals agrees, `Texel 63 \| 0 \| - \| 0 payments`. The 12th is UI Forge Vol. 5 (`pixelkiln-watch` run 13). 0 ratings, **1 collection** (unchanged). **Drop 1's 72 h interval closes on this row: Texel 46 → 63 = +17 views**, against the `funnel/LOG.md` success bar of "materially more than ~30". Sibling reading: **Texel Density Cheatsheet 23 views / 11 downloads / 2 collections** — +6 views and **+0 downloads** in 24 h. Conversion rule needs 200+ views: **~2026-10-04** at 6.75/day; 14-day rule needs 30 days live: **2026-10-09** (published 09-09 22:19 UTC). |
