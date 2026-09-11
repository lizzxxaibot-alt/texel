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
