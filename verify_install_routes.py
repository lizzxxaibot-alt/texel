"""Prove BOTH install routes work before telling a buyer to use one. Tooling.

  BLENDER_USER_RESOURCES=<temp> blender --background --factory-startup \
      --python verify_install_routes.py -- dist/texel-0.1.0.zip

The zip carries a `blender_manifest.toml` AND a legacy `bl_info`, so it should
install either as a 4.2+ extension (Preferences > Get Extensions > Install from
Disk) or through the older Add-ons tab. "Should" is not good enough for a line
on a paid download page, so this runs both operators and reports which of them
actually leaves a registered, enabled add-on with Texel's operators present.

Point BLENDER_USER_RESOURCES at a throwaway directory: without it this installs
into the real Blender config.
"""
from __future__ import annotations

import os
import sys

import bpy

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ZIP = os.path.abspath(argv[0] if argv else "dist/texel-0.1.0.zip")
MODULE = "bl_ext.user_default.texel"          # where an extension lands
LEGACY = "texel"                              # where a legacy add-on lands


def registered():
    """Is Texel actually usable? Not 'did the operator return FINISHED'."""
    names = [m for m in (MODULE, LEGACY) if m in bpy.context.preferences.addons]
    ops = hasattr(bpy.ops, "texel") and bool(
        [o for o in dir(bpy.ops.texel) if not o.startswith("_")])
    return names, ops


def try_route(label, fn):
    try:
        fn()
    except Exception as e:
        print(f"[{label}] FAILED to run: {type(e).__name__}: {e}", flush=True)
        return False
    names, ops = registered()
    ok = bool(names) and ops
    print(f"[{label}] {'PASS' if ok else 'FAIL'}  enabled={names}  "
          f"texel_ops={ops}", flush=True)
    return ok


def route_extension():
    bpy.ops.extensions.package_install_files(
        filepath=ZIP, repo="user_default", enable_on_install=True)


def route_legacy():
    bpy.ops.preferences.addon_install(filepath=ZIP, overwrite=True)
    bpy.ops.preferences.addon_enable(module=LEGACY)


def main():
    print(f"blender {bpy.app.version_string}  resources="
          f"{os.environ.get('BLENDER_USER_RESOURCES', '(default!)')}", flush=True)
    if not os.path.exists(ZIP):
        sys.exit(f"no zip at {ZIP}")

    a = try_route("Get Extensions > Install from Disk", route_extension)
    # disable whatever the first route left, so the second is a real test
    for m in list(bpy.context.preferences.addons.keys()):
        if m in (MODULE, LEGACY):
            try:
                bpy.ops.preferences.addon_disable(module=m)
            except Exception:
                pass
    b = try_route("Add-ons > Install from Disk", route_legacy)
    print(f"ROUTES_DONE extension={'ok' if a else 'FAIL'} "
          f"legacy={'ok' if b else 'FAIL'}", flush=True)


if __name__ == "__main__":
    main()
