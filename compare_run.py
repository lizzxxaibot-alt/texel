"""Open a Blender with BOTH add-ons, for a side-by-side look. Not shipped.

Installs Pixel Art Studio (the copy already purchased and sitting in Downloads)
alongside Texel, and lands on THEIR workspace, so the first impression being
judged is the one they designed rather than a generic Blender.

Deliberately does NOT save preferences: this is a comparison session, and the
other Blender window already has the real Texel install saved.

  blender --python compare_run.py
"""
import glob
import os

import bpy

DOWNLOADS = os.path.join(os.path.expanduser("~"), "Downloads")


def say(msg):
    print(f"[compare] {msg}", flush=True)


def newest_pas():
    zips = sorted(glob.glob(os.path.join(DOWNLOADS, "pixel_art_studio_blender_v*.zip")))
    return zips[-1] if zips else None


def go():
    zp = newest_pas()
    if zp is None:
        say("no Pixel Art Studio zip found in Downloads")
        return None
    say(f"installing {os.path.basename(zp)} "
        f"({os.path.getsize(zp) / 1024:.0f} KB)")
    try:
        bpy.ops.extensions.package_install_files(filepath=zp, repo="user_default",
                                                 enable_on_install=True)
        say("installed through the extensions system, same as Texel was")
    except Exception as e:
        say(f"extensions path failed ({type(e).__name__}); trying legacy")
        try:
            bpy.ops.preferences.addon_install(filepath=zp, overwrite=True)
            bpy.ops.preferences.addon_enable(module="pixel_art_studio")
            say("installed through the legacy add-on installer")
        except Exception as e2:
            say(f"INSTALL FAILED: {e2}")
            return None

    theirs = len([o for o in dir(bpy.ops.pixel_art_studio) if not o.startswith("_")]) \
        if hasattr(bpy.ops, "pixel_art_studio") else 0
    ours = len([o for o in dir(bpy.ops.texel) if not o.startswith("_")]) \
        if hasattr(bpy.ops, "texel") else 0
    say(f"operators — Pixel Art Studio: {theirs}   Texel: {ours}")

    # land on THEIR first impression
    try:
        bpy.ops.pixel_art_studio.workspace_create()
        say("opened the Pixel Art Studio workspace")
    except Exception as e:
        say(f"their workspace_create did not run: {e}")

    say(f"workspaces now: {[w.name for w in bpy.data.workspaces]}")

    # which of our shortcut letters they also claim, globally
    kc = bpy.context.window_manager.keyconfigs.addon
    mine = {"B", "E", "L", "U", "C", "F", "I", "M", "D"}
    clash = {}
    if kc:
        for km in kc.keymaps:
            for kmi in km.keymap_items:
                if (kmi.type in mine and not (kmi.ctrl or kmi.alt or kmi.shift)
                        and kmi.idname.startswith("pixel_art_studio")):
                    clash.setdefault(kmi.type, set()).add(km.name)
    say(f"keys both add-ons bind: {sorted(clash) or 'none'}")

    say("")
    say("READY. Both add-ons are live in this window.")
    say("  * Sidebar (N) has TWO tabs now: 'Pixel Art Studio' and 'Texel'.")
    say("  * The workspace bar at the top has both workspaces.")
    say("  * Your other Blender window still has Texel on its own.")
    return None


bpy.app.timers.register(go, first_interval=1.5)
