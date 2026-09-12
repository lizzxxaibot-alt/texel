TEXEL DENSITY CHEATSHEET - source
=================================

The sheet says every figure on it is computed rather than typed. This is the
code that computes them, so you can check that claim instead of taking it.

WHAT IS HERE

  cheatsheet.typ   the sheet itself (Typst)
  make_tables.py   computes every number and writes tables.json
  tables.json      the computed figures the .typ reads
  facts.json       what texel.density_detect printed in Blender for the
                   measured scene, which the drift section is checked against
  uvmap.py         Texel's texel-density maths, byte-identical to the copy
                   inside the add-on - this is what make_tables.py runs
  build.py         builds both PDFs and fails if either is wrong
  README.txt       this file

RUNNING IT

  pip install pypdf
  # install Typst: https://github.com/typst/typst

  python make_tables.py            # recompute the figures
  typst compile cheatsheet.typ     # A4
  typst compile --input paper=us-letter cheatsheet.typ letter.pdf

The fonts are Young Serif, Newsreader, IBM Plex Mono and Sora - all free, all
on Google Fonts. Point Typst at them with --font-path if it cannot find them.

WHAT THE CHECKS ACTUALLY CHECK

make_tables.py does not just calculate; it asserts. If any of these stops being
true the build fails rather than printing something false:

  * The everyday formula on the sheet - "a face using the whole SxS texture
    across M metres is S/M px/unit" - is asserted to be exactly equal to the
    full formula sqrt(uv_area * S^2 / area) across a spread of sizes and
    texture resolutions. The simplification on the sheet is not an
    approximation.

  * The drift section claims the spread across a scene equals the size ratio of
    its objects. That is predicted from the object sizes alone and checked
    against what Blender actually measured on the scene (3.2 m wall, 0.38 m
    crate, 8.4x). Prediction and measurement agree to nine decimal places.

  * The worked correction is round-tripped: the UV extent it tells you to use
    is fed back through the density formula and must come out at the target.

build.py adds four more: each PDF must be exactly one page (the sheet prints
"ONE-PAGE REFERENCE" on itself, so two pages would make it lie), no font family
may have silently fallen back, and no non-brand font may be embedded - a
missing glyph does not even warn in Typst, it just substitutes a different
typeface.

LICENCE

  The PDF, cheatsheet.typ, make_tables.py, build.py and tables.json are
  released CC0 - public domain. Use them, change them, ship them, no
  attribution needed.

  uvmap.py is part of Texel and stays GPL-3.0-or-later, the same licence as
  Blender itself. Full text: https://www.gnu.org/licenses/gpl-3.0.html
  You may use, study, modify and redistribute it under those terms; a modified
  version must stay GPL and ship its source.

  These are different licences on purpose. The sheet is meant to be free for
  anyone to do anything with. The add-on's code carries the licence a Blender
  add-on has to carry.

AI DISCLOSURE

  This sheet was built with AI assistance, as is the rest of Pixelkiln's work.
  The arithmetic is not a language model's opinion - it is uvmap.py, run.

Texel, the add-on this came from: https://z3er1n.itch.io/texel
Pixelkiln: https://z3er1n.itch.io
