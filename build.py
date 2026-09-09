"""Build the installable Texel add-on zip.

  py -3 build.py

Produces dist/texel-<version>.zip with the package rooted at texel/ so Blender's
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
              "tex_ui.py")
CORE_PY = ("__init__.py", "raster.py", "canvas.py", "uvmap.py", "palette.py",
           "select.py", "adjust.py", "tools.py")


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


def main() -> None:
    version = read_version()
    check_bl_info(version)

    missing = [f for f in INCLUDE_PY if not os.path.exists(os.path.join(HERE, f))]
    missing += [f"core/{f}" for f in CORE_PY
                if not os.path.exists(os.path.join(HERE, "core", f))]
    if missing:
        sys.exit(f"missing source files: {missing}")

    os.makedirs(DIST, exist_ok=True)
    out = os.path.join(DIST, f"texel-{version}.zip")
    if os.path.exists(out):
        os.remove(out)

    n = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in INCLUDE_PY:
            z.write(os.path.join(HERE, f), f"texel/{f}")
            n += 1
        for f in CORE_PY:
            z.write(os.path.join(HERE, "core", f), f"texel/core/{f}")
            n += 1
        for f in INCLUDE_FILES:
            p = os.path.join(HERE, f)
            if os.path.exists(p):
                z.write(p, f"texel/{f}")
                n += 1

    # never ship tests, the reference spec, or __pycache__
    with zipfile.ZipFile(out) as z:
        names = z.namelist()
    bad = [x for x in names
           if "__pycache__" in x or "/test_" in x or "reference" in x or x.endswith(".pyc")]
    if bad:
        sys.exit(f"build leaked files that must not ship: {bad}")

    size = os.path.getsize(out)
    print(f"built {out}")
    print(f"  {n} files, {size / 1024:.1f} KB, version {version}")
    print(f"  root: {sorted({x.split('/')[0] for x in names})}")


if __name__ == "__main__":
    main()
