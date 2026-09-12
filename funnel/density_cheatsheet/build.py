"""Build the density cheatsheet, and fail if it is not what it claims to be.

  python funnel/density_cheatsheet/build.py      (run from texel/)

Four gates, each of which could fail and has:

  1. make_tables.py runs core/uvmap.py out of the SHIPPED zip and asserts the
     simplified formula printed on the sheet is exactly the full one, and that
     the drift predicted from object sizes matches what Blender measured.
  2. Each PDF - A4 and US Letter - must be ONE page. The first build silently
     became two when the closing block overflowed, and "ONE-PAGE REFERENCE" is
     printed on the sheet itself, so a two-page build makes it lie about itself.
  3. No font family fell back. Typst only WARNS about an unknown family.
  4. No fallback font is embedded. A missing GLYPH does not even warn - Typst
     silently substitutes LibertinusSerif, which is how the first build shipped
     a non-brand face for one arrow. Only the embedded-font table catches it.
"""
import os
import re
import subprocess
import sys

import pypdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))                     # .../texel
FONTS = os.path.normpath(os.path.join(ROOT, "..", "..", "..", "brand", "fonts"))
PDF = os.path.join(HERE, "texel-density-cheatsheet.pdf")
PDF_LETTER = os.path.join(HERE, "texel-density-cheatsheet-letter.pdf")

ALLOWED = ("Newsreader16pt", "IBMPlexMono", "Sora", "YoungSerif")
SUBSET = re.compile(r"^/[A-Z]{6}\+")


def compile_sheet(out, paper):
    cmd = ["typst", "compile", "--font-path", FONTS]
    if paper:
        cmd += ["--input", "paper=" + paper]
    cmd += [os.path.join(HERE, "cheatsheet.typ"), out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    name = os.path.basename(out)
    if r.returncode:
        sys.exit("typst failed for " + name + ":\n" + r.stderr)
    if "unknown font family" in r.stderr:
        sys.exit("FAIL: font family fell back in " + name + "\n" + r.stderr)

    doc = pypdf.PdfReader(out)
    used = set()
    for page in doc.pages:
        for f in (page.get("/Resources", {}).get("/Font") or {}).values():
            used.add(SUBSET.sub("", str(f.get_object().get("/BaseFont", ""))))

    stray = sorted(f for f in used if not f.startswith(ALLOWED))
    if stray:
        sys.exit("FAIL: non-brand font embedded in " + name + ": " + str(stray)
                 + "\n  A glyph is missing from brand/fonts/ and Typst"
                   " substituted it silently.")

    if len(doc.pages) != 1:
        sys.exit("FAIL: " + name + " is " + str(len(doc.pages)) + " pages; the"
                 " sheet prints ONE-PAGE REFERENCE on itself")

    box = doc.pages[0].mediabox
    print("ok: %-38s 1 page, %.0fx%.0f pt, %.0f kB"
          % (name, float(box.width), float(box.height),
             os.path.getsize(out) / 1024))
    return used


subprocess.run([sys.executable, os.path.join(HERE, "make_tables.py")], check=True)

fonts = set()
for out, paper in ((PDF, None), (PDF_LETTER, "us-letter")):
    fonts |= compile_sheet(out, paper)
print("  fonts  " + ", ".join(sorted(fonts)))
