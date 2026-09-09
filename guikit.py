"""Run a script inside a GUI Blender and ALWAYS get the process back.

Not shipped. This exists because GUI runs kept hanging: a script driven by
`bpy.app.timers` that raises never reaches `quit_blender()`, so Blender sits
there with a window open and no output, and the only symptom is "you press go
and nothing happens". Every one of those was my script failing silently, not
Blender.

Three guarantees:

  1. **It always exits.** A watchdog timer force-quits after `budget` seconds
     whatever the script is doing, so a hang costs you a known number of
     seconds instead of a stuck process and a killed shell.
  2. **It always reports.** The step function is wrapped, so a traceback is
     printed and counted as a failure rather than vanishing into Blender's
     console.
  3. **Output is flushed per line**, so a crash halfway through still leaves
     you the log up to that point.

Usage:

    import guikit

    def step1(ctx): ...          # return the seconds to wait, or None to finish
    def step2(ctx): ...

    guikit.run([step1, step2], budget=180, name="TEXEL WORKSPACE")
"""
import sys
import time
import traceback

import bpy


class Ctx:
    """Passed to every step. Carries the failure list and scratch state."""

    def __init__(self):
        self.fails = []
        self.notes = []
        self.data = {}
        self.t0 = time.perf_counter()

    def check(self, name, cond, detail=""):
        ok = bool(cond)
        print(f"[{'ok  ' if ok else 'FAIL'}] {name}"
              + ("" if ok else f"  -> {detail}"), flush=True)
        if not ok:
            self.fails.append(name)
        return ok

    def note(self, msg):
        self.notes.append(msg)
        print(f"[info] {msg}", flush=True)


def win():
    """The window. `bpy.context.window` is None inside a timer callback."""
    return bpy.context.window_manager.windows[0]


def areas(kind, screen=None):
    sc = screen or win().screen
    return [a for a in sc.areas if a.type == kind]


def in_area(area, fn, screen=None):
    """Call fn() with a real area/region override. Returns None on a bad area."""
    if area is None:
        return None
    region = next((r for r in area.regions if r.type == "WINDOW"), None)
    with bpy.context.temp_override(window=win(), screen=screen or win().screen,
                                   area=area, region=region,
                                   space_data=area.spaces.active):
        return fn()


def _quit():
    try:
        bpy.ops.wm.quit_blender()
    except Exception:
        # last resort: if even quitting fails, take the process down rather
        # than leave a window nobody asked for
        sys.stdout.flush()
        import os
        os._exit(1)


def run(steps, budget=180, name="TEXEL GUI", settle=1.2):
    """Run `steps` in order inside a GUI Blender, then quit no matter what."""
    ctx = Ctx()
    state = {"i": 0, "done": False}

    def finish(why=""):
        if state["done"]:
            return
        state["done"] = True
        el = time.perf_counter() - ctx.t0
        print(flush=True)
        for n in ctx.notes:
            print(f"  note: {n}", flush=True)
        if why:
            print(f"  {why}", flush=True)
            ctx.fails.append(why)
        if ctx.fails:
            print(f"\n{len(ctx.fails)} FAILED:", flush=True)
            for f in ctx.fails:
                print(f"   - {f}", flush=True)
            print(f"{name}: FAILED  ({el:.1f}s)", flush=True)
        else:
            print(f"\n{name}: ALL PASS  ({el:.1f}s)", flush=True)
        _quit()

    def watchdog():
        finish(f"WATCHDOG: still running after {budget}s - killed")
        return None

    def tick():
        if state["done"]:
            return None
        i = state["i"]
        if i >= len(steps):
            finish()
            return None
        state["i"] = i + 1
        try:
            wait = steps[i](ctx)
        except Exception as e:
            print(f"[FAIL] step {i + 1} ({steps[i].__name__}) raised "
                  f"{type(e).__name__}: {e}", flush=True)
            traceback.print_exc()
            sys.stdout.flush()
            ctx.fails.append(f"{steps[i].__name__} raised {type(e).__name__}: {e}")
            wait = 0.05                 # keep going; later steps may still tell us
        return wait if wait is not None else 0.05

    print(f"[info] Blender {bpy.app.version_string} | budget {budget}s", flush=True)
    bpy.app.timers.register(watchdog, first_interval=budget)
    bpy.app.timers.register(tick, first_interval=settle)
    return ctx
