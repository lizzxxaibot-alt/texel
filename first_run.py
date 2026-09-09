"""Open Blender the way a buyer does: install the zip, enable it, and stop.

Not shipped. This is the dry run of somebody's first five minutes - the same
steps in the same order as START-HERE.html tells them to take:

    Edit > Preferences > Add-ons > Install from Disk...  -> texel-0.1.0.zip
    it enables itself
    press N, pick the Texel tab

The one difference is that this does it from a script so the run is repeatable
and reports what actually happened. **It deliberately does not quit** - Blender
is left open to be used by hand.

  blender --python first_run.py
"""
import glob
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
ZIPS = sorted(glob.glob(os.path.join(HERE, "dist", "texel-*.zip")))


def say(msg):
    print(f"[first-run] {msg}", flush=True)


def install():
    if not ZIPS:
        say("NO ZIP FOUND in dist/ - run `python build.py` first")
        return False
    zp = ZIPS[-1]
    say(f"installing {os.path.basename(zp)} "
        f"({os.path.getsize(zp) / 1024:.0f} KB)")

    # A buyer on 4.2+ uses "Install from Disk", which is the extensions system.
    # Fall back to the legacy add-on installer so this works either way.
    ok = False
    try:
        bpy.ops.extensions.package_install_files(filepath=zp, repo="user_default",
                                                 enable_on_install=True)
        ok = True
        say("installed through the extensions system (Install from Disk)")
    except Exception as e:
        say(f"extensions path unavailable ({type(e).__name__}), using legacy")
        try:
            bpy.ops.preferences.addon_install(filepath=zp, overwrite=True)
            bpy.ops.preferences.addon_enable(module="texel")
            ok = True
            say("installed through the legacy add-on installer")
        except Exception as e2:
            say(f"INSTALL FAILED: {e2}")
    return ok


def verify():
    n = len([o for o in dir(bpy.ops.texel) if not o.startswith("_")]) \
        if hasattr(bpy.ops, "texel") else 0
    say(f"operators registered: {n}")
    if not n:
        say("the add-on did not register - nothing to look at")
        return False
    for mod in ("bl_ext.user_default.texel", "texel"):
        if mod in sys.modules:
            say(f"module: {mod}")
            break
    return True


def open_workspace():
    """Press the button the buyer is told to press."""
    try:
        bpy.ops.texel.workspace_create()
        say(f"workspace: {bpy.context.scene.texel.status}")
    except Exception as e:
        say(f"workspace_create failed: {e}")


def go():
    ok = install()
    if ok:
        try:
            bpy.ops.wm.save_userpref()
            say("preferences saved - it will still be here next time you open Blender")
        except Exception as e:
            say(f"could not save preferences: {e}")
    if verify():
        open_workspace()
    say("")
    say("READY. Blender is yours now.")
    say("  * The Texel tab is in the sidebar - press N in either editor.")
    say("  * The cube is already textured; try Pencil and draw on it.")
    say("  * Texel > Setup > Add 1m Cube starts a fresh one.")
    say("  * Sprite > Add Frame begins an animation.")
    return None                       # one shot; do NOT quit


bpy.app.timers.register(go, first_interval=1.5)
