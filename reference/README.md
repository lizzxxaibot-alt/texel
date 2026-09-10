# Why this directory still exists

`api-surface.txt` is kept **deliberately, as a record** (user's decision,
2026-09-09). It is not tooling, it is not a benchmark, and it is not to be used
for either. Read this before touching it or deciding it looks like clutter.

## What the file is

An **API surface** for Pixel Art Studio v1.1.1–1.1.5 by Alfred Reinold Baudisch
(GPL-3.0-or-later, a copy the user owns): operator names, panel names and
one-line descriptions, extracted by an AST walk. **What it does, never how.**
No implementation, no source, no algorithms.

Content is unaltered from extraction — 16,979 bytes,
md5 `0bb6b67d1fe367232ae10f262acf1c06`. It was briefly deleted and restored the
same day; the restore was verified byte-for-byte against the removed file, and
against git's LF-normalised copy in history (identical modulo line endings, 279
CRLF→LF, nothing else).

## Why it is kept rather than deleted

`PROGRESS.md` records that Texel was written as a re-implementation specified
against this surface, and states that **no implementation was copied.**

**This file is the evidence for that statement.** Deleting it would leave the
record making a claim with nothing behind it — an admission stripped of the one
artifact that shows the process was clean. That is a worse position than keeping
both, so both are kept.

## Rules

1. **It never ships.** Verified against `texel-0.1.0.zip` and `texel-0.2.0.zip`
   on 2026-09-09: 0 matching files, 0 mentions, across all 32 files in each.
   Re-check this if the packager ever changes what it sweeps in.
2. **It never feeds a comparison.** No store-page line, no marketing beat, no
   post, no operator-count contrast. The "the nearest comparable add-on ships 67"
   line it once supported was removed from `LISTING.md` on 2026-09-09 and had
   never been published.
3. **It is never re-run or refreshed.** The harness that did that — `compare.py`,
   `compare_run.py`, `count_ops.py`'s second column and both run logs — was
   removed on 2026-09-09 and is not to be rebuilt. This is a frozen historical
   record, not a live measurement. Do not extract a newer version.
4. **Texel is not positioned against anything and is not derived from anything.**
   Standing rule, `promo/POSTED.md`. Keeping a provenance record is not the same
   as having a rival, and nothing here licenses treating it as one.

Git history for the removal and the restore: `3f56614` and the commit that
follows it.
