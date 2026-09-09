"""Our shortcuts must not stomp Blender's.

This has to run in a **GUI** session. In background mode Blender populates about
12 keymap items instead of 3,000, so every key looks free and the check passes
by knowing nothing — which is exactly the false negative that nearly shipped a
binding on top of view3d.select_box.

  blender --factory-startup --python test_keys.py

Fails if any Texel binding collides with an unmodified default in the same
keymap, so a future Blender that claims one of our letters breaks the build
instead of silently taking it away from the user.
"""
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

import texel
from texel import tex_keys

fails = []


def check(name, cond, detail=""):
    print(f"[{'ok  ' if cond else 'FAIL'}] {name}" + ("" if cond else f"  {detail}"))
    if not cond:
        fails.append(name)


# Object Mode and Edit Mode sit UNDER the 3D View keymap at runtime, so a
# binding in "3D View" has to clear them too.
ALSO = {"3D View": ("Object Mode", "Mesh"), "Image": ("Image Generic",)}


def run():
    try:
        texel.register()
    except Exception:
        pass

    kc = bpy.context.window_manager.keyconfigs.default
    total = sum(len(km.keymap_items) for km in kc.keymaps)
    print(f"[info] Blender {bpy.app.version_string}, {total} default keymap items")
    check("the default keymap is actually populated (GUI, not background)",
          total > 1000, total)

    addon = bpy.context.window_manager.keyconfigs.addon
    check("addon keyconfig exists", addon is not None)

    ours = []
    for km_name, space, idname, key, _props in tex_keys.BINDINGS:
        km = addon.keymaps.get(km_name) if addon else None
        got = [k for k in km.keymap_items if k.idname == idname and k.type == key] \
            if km else []
        check(f"{idname} bound to {key} in {km_name}", bool(got))
        ours.append((km_name, idname, key))

    # ---- the real test: does any of ours already mean something else?
    for km_name, idname, key in ours:
        for target in (km_name,) + ALSO.get(km_name, ()):
            km = kc.keymaps.get(target)
            if km is None:
                continue
            clash = [k.idname for k in km.keymap_items
                     if k.type == key and k.value == "PRESS"
                     and not (k.ctrl or k.alt or k.shift or k.oskey)
                     and k.idname != idname]
            check(f"{key} is free in '{target}' (for {idname})",
                  not clash, f"taken by {sorted(set(clash))[:3]}")

    # ---- and the shortcuts must actually do something
    bpy.ops.texel.set_tool(tool="ERASER")
    check("set_tool switches the tool",
          bpy.context.scene.texel.tool == "ERASER", bpy.context.scene.texel.tool)
    bpy.ops.texel.set_tool(tool="FILL")
    check("set_tool switches again", bpy.context.scene.texel.tool == "FILL")
    check("set_tool refuses a bogus tool",
          bpy.ops.texel.set_tool(tool="NOPE") == {"CANCELLED"})

    before = bpy.context.scene.texel.mirror_x
    bpy.ops.texel.mirror_toggle(axis="X")
    check("mirror_toggle flips X", bpy.context.scene.texel.mirror_x != before)
    bpy.ops.texel.mirror_toggle(axis="X")
    check("and flips it back", bpy.context.scene.texel.mirror_x == before)
    bpy.ops.texel.mirror_toggle(axis="Y")
    check("mirror_toggle flips Y", bpy.context.scene.texel.mirror_y is True)

    # ---- unregister must leave no keymap items behind
    n_before = len(tex_keys._keymaps)
    texel.unregister()
    check("unregister removed every binding", not tex_keys._keymaps,
          f"{len(tex_keys._keymaps)} left of {n_before}")

    print()
    if fails:
        print(f"{len(fails)} FAILED: {fails}")
        print("TEXEL KEYS: FAILED")
    else:
        print("TEXEL KEYS: ALL PASS")
    bpy.ops.wm.quit_blender()
    return None


bpy.app.timers.register(run, first_interval=1.5)
