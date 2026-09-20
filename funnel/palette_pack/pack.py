"""Assemble texel-material-palettes.zip and verify it from the inside.

  python funnel/palette_pack/build.py      # 1. generate + gate the .gpl files
  python funnel/palette_pack/make_readme.py # 2. README.txt (build.py wipes it)
  python funnel/palette_pack/make_icon.py  # 3. the shaded sphere (cover needs it)
  python funnel/palette_pack/make_cover.py # 4. cover HTML
  python funnel/palette_pack/make_sheet.py # 5. reference sheet HTML
  python funnel/palette_pack/make_spec.py  # 6. itch_spec.json
  python funnel/palette_pack/pack.py       # 7. this - zip it and check it

Steps 4 and 5 are then rendered through automation/render.mjs at their delivery
sizes (630x500 and 1600x1000) and linted with automation/design_lint.mjs.

The verification deliberately reads the files back OUT OF THE ARCHIVE rather
than off disk, with Texel's own parser loaded out of the shipped add-on zip.
Checking the source directory would prove the generator works; checking the
archive proves the thing a stranger downloads works, which is the only version
that matters. Drop 1's lesson, in the stronger form: it verified its PDFs
against the live bytes only AFTER a broken link had already shipped.
"""
from __future__ import annotations

import os
import pathlib
import types
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
TEXEL = HERE.parents[1]
ADDON_ZIP = TEXEL / "dist" / "texel-0.2.0.zip"
OUT = HERE / "texel-material-palettes.zip"

EXPECT_GPL = 25          # 24 material ramps + _all-midtones.gpl
EXPECT_COLOURS = 216     # 24 * 8 + 24


def texel_palette_module():
    """core/palette.py, loaded from the add-on archive buyers can download."""
    z = zipfile.ZipFile(ADDON_ZIP)
    name = next(n for n in z.namelist() if n.endswith("core/palette.py"))
    m = types.ModuleType("shipped_palette")
    exec(compile(z.read(name).decode("utf8"), name, "exec"), m.__dict__)
    return m


def main():
    src = HERE / "palettes"
    gpls = sorted(src.glob("*.gpl"))
    readme = src / "README.txt"
    sheet = HERE / "sheet.png"
    for p in (readme, sheet):
        if not p.exists():
            raise SystemExit(f"missing {p} - run the earlier steps first")

    if OUT.exists():
        OUT.unlink()
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for g in gpls:
            z.write(g, g.name)
        z.write(readme, readme.name)
        z.write(sheet, "reference-sheet.png")

    # ---------------------------------------------------- verify the ARCHIVE
    P = texel_palette_module()
    z = zipfile.ZipFile(OUT)
    if z.testzip() is not None:
        raise SystemExit(f"corrupt member: {z.testzip()}")

    names = z.namelist()
    found_gpl = [n for n in names if n.endswith(".gpl")]
    assert len(found_gpl) == EXPECT_GPL, f"{len(found_gpl)} .gpl, wanted {EXPECT_GPL}"
    assert "README.txt" in names, "README.txt missing from the archive"
    assert "reference-sheet.png" in names, "reference sheet missing"

    total = 0
    for n in sorted(found_gpl):
        pname, cols = P.parse_gpl(z.read(n).decode("utf8"))
        assert cols, f"{n} parsed to zero colours"
        assert pname.startswith("Texel "), f"{n} palette name is {pname!r}"
        total += len(cols)
    assert total == EXPECT_COLOURS, f"{total} colours, wanted {EXPECT_COLOURS}"

    # The one link the drop exists to create has to be IN the download, not
    # only on the page - a .gpl sitting in someone's palettes folder six months
    # from now is the only lasting piece of this.
    rd = z.read("README.txt").decode("utf8")
    assert "https://z3er1n.itch.io/texel" in rd, \
        "README in the archive does not carry the Texel link"

    png = z.read("reference-sheet.png")
    assert png[:8] == b"\x89PNG\r\n\x1a\n", "reference sheet is not a PNG"

    print(f"pack: {OUT.name}  {os.path.getsize(OUT):,} bytes")
    print(f"  {len(found_gpl)} .gpl + README.txt + reference-sheet.png")
    print(f"  {total} colours re-parsed FROM INSIDE THE ARCHIVE using "
          f"core/palette.py out of {ADDON_ZIP.name}")
    print("  README carries the Texel link")
    print("pack: OK")


if __name__ == "__main__":
    main()
