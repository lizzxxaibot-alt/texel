r"""Run the gate inside the MICROSOFT STORE Blender, which cannot be scripted.

The Store build lives under C:\Program Files\WindowsApps, whose ACL denies
execution to anything but an interactive shell launch - `blender.exe --python`
answers "Access is denied", so test_versions.sh skips it and the store page's
compatibility claim has a hole in it exactly where a lot of Windows users get
Blender from.

The way in is Blender's own startup folder: every .py in
  %APPDATA%\Blender Foundation\Blender\<ver>\scripts\startup\
is imported at launch. So drop a runner there, start Blender through the shell
app alias (which IS allowed), let it run one suite and quit, read the report,
repeat. The runner is deleted afterwards, pass or fail.

Note this runs against the user's REAL preferences, not --factory-startup. That
is deliberate: it is the environment a buyer actually has.

  python store_check.py                 # every suite
  python store_check.py test_install    # just one

Nothing here is shipped and nothing is left behind.
"""
from __future__ import annotations
import os
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(os.environ["TEMP"], "texel_store_check")
VER = "5.2"                       # the Store package is Blender 5.2.1

# The Store build is an MSIX package, so its %APPDATA% is REDIRECTED into the
# package's private store. A runner dropped in the ordinary
# %APPDATA%\Blender Foundation\... is invisible to it - verified: the portable
# 5.2.1 imported it, the Store 5.2.1 did not. Worth knowing beyond this script:
# a buyer who installs Texel in the Store build gets it under here, not in the
# folder every "where are my add-ons" answer online points at.
USER = os.path.join(os.environ["LOCALAPPDATA"], "Packages",
                    "BlenderFoundation.Blender_ppwjx1n5r4v9t", "LocalCache",
                    "Roaming", "Blender Foundation", "Blender", VER)
STARTUP = os.path.join(USER, "scripts", "startup")
RUNNER = os.path.join(STARTUP, "zz_texel_store_check.py")
ALIAS = r"shell:AppsFolder\BlenderFoundation.Blender_ppwjx1n5r4v9t!Blender"

HEADLESS = ["test_blender", "test_addon", "test_features", "test_showcase",
            "test_sprite", "test_anim", "test_install"]
GUI = ["test_panels", "test_keys", "test_workspace", "test_e2e"]

# NOTE: this is a template rendered into a real file, so every backslash and
# every brace here is consumed twice. Keep it escape-free - chr(10) rather than
# a newline escape - because getting that wrong writes a file that will not
# parse, and Blender swallows the SyntaxError silently at startup.
RUNNER_SRC = '''"""TEMPORARY - written by texel/store_check.py. Safe to delete."""
import os, sys, traceback
import bpy

BASE = r"{base}"
WORK = r"{work}"
GUI = {gui!r}


def _go():
    try:
        job = open(os.path.join(WORK, "job.txt"), encoding="utf-8").read().strip()
    except Exception:
        return None
    rep = open(os.path.join(WORK, "report.txt"), "w", buffering=1,
               encoding="utf-8", errors="replace")
    # stdout goes straight to disk: a guikit suite quits the process itself, so
    # anything still buffered in memory when it does would be lost
    sys.stdout = sys.stderr = rep
    print("BLENDER " + bpy.app.version_string)
    print("EXE     " + bpy.app.binary_path)
    print("JOB     " + job)
    print("-" * 60)
    path = os.path.join(BASE, job + ".py")
    try:
        os.chdir(BASE)
        if BASE not in sys.path:
            sys.path.insert(0, BASE)
        g = {{"__file__": path, "__name__": "__main__"}}
        exec(compile(open(path, encoding="utf-8").read(), path, "exec"), g)
    except SystemExit as e:
        print("__EXIT__ " + str(e.code))
    except Exception:
        traceback.print_exc()
        print("__EXIT__ crash")
    if job not in GUI:
        # a guikit suite quits itself once its own timers finish
        print("__JOB_DONE__")
        bpy.ops.wm.quit_blender()
    return None


def _watchdog():
    try:
        open(os.path.join(WORK, "report.txt"), "a", encoding="utf-8").write(
            chr(10) + "__WATCHDOG__ forced quit" + chr(10))
    except Exception:
        pass
    bpy.ops.wm.quit_blender()
    return None


bpy.app.timers.register(_go, first_interval=2.0)
bpy.app.timers.register(_watchdog, first_interval=240.0)
'''


def kill_blender():
    subprocess.run(["taskkill", "/IM", "blender.exe", "/F"],
                   capture_output=True, text=True)


def running():
    out = subprocess.run(["tasklist", "/FI", "IMAGENAME eq blender.exe"],
                         capture_output=True, text=True).stdout
    return "blender.exe" in out


def one(job, budget=300):
    report = os.path.join(WORK, "report.txt")
    for f in ("job.txt", "report.txt"):
        p = os.path.join(WORK, f)
        if os.path.exists(p):
            os.remove(p)
    with open(os.path.join(WORK, "job.txt"), "w", encoding="utf-8") as fh:
        fh.write(job)

    kill_blender()
    time.sleep(1)
    subprocess.run(["explorer.exe", ALIAS], capture_output=True)

    t0 = time.time()
    text = ""
    while time.time() - t0 < budget:
        time.sleep(2)
        if os.path.exists(report):
            try:
                text = open(report, encoding="utf-8", errors="replace").read()
            except Exception:
                continue
            if ("__JOB_DONE__" in text or "__WATCHDOG__" in text
                    or "ALL PASS" in text or "FAILED" in text):
                break
        elif time.time() - t0 > 45 and not running():
            text = "(Blender exited without writing a report - runner never ran)"
            break
    kill_blender()
    return ("ALL PASS" in text), text, time.time() - t0


def main():
    jobs = sys.argv[1:] or (HEADLESS + GUI)
    os.makedirs(WORK, exist_ok=True)
    made_startup = not os.path.isdir(STARTUP)
    os.makedirs(STARTUP, exist_ok=True)

    src = RUNNER_SRC.format(base=HERE, work=WORK, gui=GUI)
    compile(src, RUNNER, "exec")      # never write a runner Blender cannot parse
    with open(RUNNER, "w", encoding="utf-8") as fh:
        fh.write(src)
    print(f"runner  -> {RUNNER}")
    print("target  -> Microsoft Store Blender 5.2.1 (launched via the app alias)")
    print()

    results = []
    try:
        for job in jobs:
            print(f"  {job:<16} ", end="", flush=True)
            ok, text, el = one(job)
            print(f"{'pass' if ok else 'FAIL'}  ({el:.0f}s)")
            if not ok:
                for line in text.splitlines():
                    if line.startswith(("[FAIL", "__", "Traceback")) or "Error" in line:
                        print(f"      {line[:110]}")
            with open(os.path.join(WORK, f"{job}.log"), "w", encoding="utf-8",
                      errors="replace") as fh:
                fh.write(text)
            results.append((job, ok))
    finally:
        if os.path.exists(RUNNER):
            os.remove(RUNNER)
        # Blender compiles the runner on import, so removing the .py leaves a
        # __pycache__ behind and the "is it empty" check below never fires
        shutil.rmtree(os.path.join(STARTUP, "__pycache__"), ignore_errors=True)
        if made_startup and os.path.isdir(STARTUP) and not os.listdir(STARTUP):
            shutil.rmtree(STARTUP, ignore_errors=True)
            scripts = os.path.dirname(STARTUP)
            if os.path.isdir(scripts) and not os.listdir(scripts):
                shutil.rmtree(scripts, ignore_errors=True)
        kill_blender()
        print(f"\nrunner removed: {not os.path.exists(RUNNER)}")

    bad = [j for j, ok in results if not ok]
    print(f"logs in {WORK}")
    print(f"STORE_DONE pass={len(results) - len(bad)} fail={len(bad)}"
          + (f" -> {bad}" if bad else ""))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
