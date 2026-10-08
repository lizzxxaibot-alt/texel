"""Build the installable Texel add-on zip.

  py -3 build.py           # full build -> dist/texel-<version>.zip
  py -3 build.py --lite    # free demo  -> dist/lite/texel-lite-demo-<version>.zip

Produces a zip with the package rooted at texel/ so Blender's
"Install from Disk" and the extension installer both accept it. Version comes
from blender_manifest.toml, and the script fails if bl_info disagrees with it -
a version skew between those two is a real support headache.
"""
import os
import re
import shutil
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, "dist")

INCLUDE_FILES = ("blender_manifest.toml", "LICENSE.txt", "README.md",
                 "START-HERE.html", "ROADMAP.md",
                 "workspace.blend")
INCLUDE_PY = ("__init__.py", "tex_props.py", "tex_doc.py", "tex_pick.py",
              "tex_paint.py", "tex_layers.py", "tex_density.py",
              "tex_palette.py", "tex_select.py", "tex_zones.py",
              "tex_setup.py", "tex_extra.py", "tex_tools.py", "tex_showcase.py", "tex_sprite.py", "tex_anim.py", "tex_keys.py",
              "tex_ui.py", "tex_edition.py")
# Left out of the free Lite build. Lite paints pixel textures onto your models;
# full Texel animates them and exports the sprite sheets a game engine reads.
PAID_PY = ("tex_showcase.py", "tex_sprite.py", "tex_anim.py")
# Lite goes in its own folder: test_install.py installs the last zip in dist/,
# and "texel-lite-..." sorts after "texel-0...", so a Lite zip sitting beside
# the full one would quietly become the thing the full gate tests.
LITE_DIST = os.path.join(DIST, "lite")
LITE_README = """> **This is Texel Lite, the free demo.** It paints pixel textures onto your
> models: canvas, layers, palettes, selection, zones, tools and texel density.
> **Not in Lite:** frames, tracks and onion skin, sprite sheet / GIF / animation
> data export, trim, colour count, reference images, and Showcase renders. Those
> are in full Texel: https://mintworks.cc/texel
> Uninstall Lite before you install full Texel.

"""
CORE_PY = ("__init__.py", "raster.py", "canvas.py", "uvmap.py", "palette.py",
           "select.py", "adjust.py", "tools.py", "report.py")


def check_nothing_left_behind() -> None:
    """Every source module on disk must be in a list above.

    These lists are hand-written, and a hand-written list of files is a bug
    waiting for the next module. core/report.py was added in v0.2.1, tex_ui.py
    imported it, and the first zip built without it - an add-on that installs
    and then fails to import. `test_install.py` would have caught it, but only
    after the zip existed; this catches it at the point the list went stale.
    """
    stale = []
    for f in sorted(os.listdir(os.path.join(HERE, "core"))):
        if f.endswith(".py") and f not in CORE_PY:
            stale.append(f"core/{f}")
    for f in sorted(os.listdir(HERE)):
        if f.startswith("tex_") and f.endswith(".py") and f not in INCLUDE_PY:
            stale.append(f)
    if stale:
        sys.exit(f"source files exist but are not in build.py's lists: {stale}")


def read_version() -> str:
    txt = open(os.path.join(HERE, "blender_manifest.toml"), encoding="utf-8").read()
    m = re.search(r'^version\s*=\s*"([^"]+)"', txt, re.M)
    if not m:
        sys.exit("no version in blender_manifest.toml")
    return m.group(1)


def check_bl_info(version: str) -> None:
    txt = open(os.path.join(HERE, "__init__.py"), encoding="utf-8").read()
    m = re.search(r'"version":\s*\(([^)]+)\)', txt)
    if not m:
        sys.exit("no version tuple in bl_info")
    tup = ".".join(p.strip() for p in m.group(1).split(","))
    if tup != version:
        sys.exit(f"version skew: manifest {version} vs bl_info {tup}")


def _swap(text: str, old: str, new: str, where: str) -> str:
    """Replace exactly one occurrence, or stop the build.

    A rewrite that silently matches nothing ships a Lite zip that calls itself
    full Texel - or worse, one whose LITE flag is still False and whose
    __init__ then imports three files that are not in the zip.
    """
    if text.count(old) != 1:
        sys.exit(f"lite rewrite: expected one {old!r} in {where}, "
                 f"found {text.count(old)}")
    return text.replace(old, new)


def _lite_text(f: str):
    """The Lite version of a file, or None to copy it unchanged."""
    p = os.path.join(HERE, f)
    if f == "tex_edition.py":
        return _swap(open(p, encoding="utf-8").read(),
                     "LITE = False", "LITE = True", f)
    if f == "__init__.py":
        return _swap(open(p, encoding="utf-8").read(),
                     '"name": "Texel",', '"name": "Texel Lite",', f)
    if f == "blender_manifest.toml":
        t = _swap(open(p, encoding="utf-8").read(),
                  'name = "Texel"', 'name = "Texel Lite"', f)
        return re.sub(r'^tagline = ".*"$',
                      'tagline = "Free demo: pixel art painting, layers and texel density"',
                      t, count=1, flags=re.M)
    if f == "README.md":
        return LITE_README + open(p, encoding="utf-8").read()
    if f == "START-HERE.html":
        return _swap(open(p, encoding="utf-8").read(),
                     "<p><strong>Thank you for buying this.</strong>",
                     "<p><strong>This is Texel Lite, the free demo.</strong> It "
                     "paints pixel textures onto your models. Frames and "
                     "animation, sprite sheet and GIF export, trim, colour count, "
                     "reference images and Showcase renders are in full Texel, "
                     "at <a href=\"https://mintworks.cc/texel\">mintworks.cc/texel</a>."
                     "</p>\n\n<p><strong>If you buy full Texel:</strong>", f)
    return None


def main() -> None:
    lite = "--lite" in sys.argv[1:]
    version = read_version()
    check_bl_info(version)
    check_nothing_left_behind()

    missing = [f for f in INCLUDE_PY if not os.path.exists(os.path.join(HERE, f))]
    missing += [f"core/{f}" for f in CORE_PY
                if not os.path.exists(os.path.join(HERE, "core", f))]
    if missing:
        sys.exit(f"missing source files: {missing}")

    if lite:
        os.makedirs(LITE_DIST, exist_ok=True)
        # "demo" in the name is load-bearing: itch_upload.mjs --demo refuses a
        # file without it, so the paid zip cannot be ticked free by a typo
        out = os.path.join(LITE_DIST, f"texel-lite-demo-{version}.zip")
        py = tuple(f for f in INCLUDE_PY if f not in PAID_PY)
    else:
        os.makedirs(DIST, exist_ok=True)
        out = os.path.join(DIST, f"texel-{version}.zip")
        py = INCLUDE_PY
    if os.path.exists(out):
        os.remove(out)

    n = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        def put(src, f, arc):
            text = _lite_text(f) if lite else None
            if text is None:
                z.write(src, arc)
            else:
                z.writestr(arc, text.encode("utf-8"))
        for f in py:
            put(os.path.join(HERE, f), f, f"texel/{f}")
            n += 1
        for f in CORE_PY:
            z.write(os.path.join(HERE, "core", f), f"texel/core/{f}")
            n += 1
        for f in INCLUDE_FILES:
            p = os.path.join(HERE, f)
            if os.path.exists(p):
                put(p, f, f"texel/{f}")
                n += 1

    # never ship tests, the reference spec, or __pycache__
    with zipfile.ZipFile(out) as z:
        names = z.namelist()
    bad = [x for x in names
           if "__pycache__" in x or "/test_" in x or "reference" in x or x.endswith(".pyc")]
    if lite:
        bad += [x for x in names if x.split("/")[-1] in PAID_PY]
    if bad:
        sys.exit(f"build leaked files that must not ship: {bad}")

    size = os.path.getsize(out)
    print(f"built {out}")
    print(f"  {n} files, {size / 1024:.1f} KB, version {version}"
          + ("  [LITE]" if lite else ""))
    print(f"  root: {sorted({x.split('/')[0] for x in names})}")


if __name__ == "__main__":
    main()
