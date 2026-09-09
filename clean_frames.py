"""Delete the intermediate render frames. Keep everything marketing needs.

Every MP4 and GIF has already been encoded from these, and `store/stills/` holds
57 harvested frames - about fourteen weeks of non-repeating posts. What is left
is ~3 GB of numbered PNGs that only exist to be fed to ffmpeg once.

  python clean_frames.py            # dry run: says what it would do
  python clean_frames.py --delete   # does it

Deletes ONLY: directories named `frames`, and `f_####.png` / `<name>_####.png`
sequences. Never touches an .mp4, a .gif, a tile_*.png, a sprite/ folder, or
anything in store/.
"""
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DO_IT = "--delete" in sys.argv

SEQ = re.compile(r"^[a-z_]*_?\d{4}\.png$", re.I)
KEEP_EXT = {".mp4", ".gif", ".json", ".txt", ".md", ".html"}
# NOT "sprite": promo/steps/sprite is a frame dump, while the walk sprites in
# promo/shots/*/sprite are named walk_00.png - two digits, so the four-digit
# sequence pattern below already spares them.
KEEP_DIRS = {"store", "dist", "core", "reference"}


def is_sequence_frame(name):
    return bool(SEQ.match(name)) and not name.startswith("tile_")


def walk_targets():
    """Whole `frames/` dirs, plus loose numbered sequences elsewhere."""
    dirs, files = [], []
    for root, subdirs, names in os.walk(HERE):
        rel = os.path.relpath(root, HERE).replace("\\", "/")
        if rel.split("/")[0] in KEEP_DIRS:
            subdirs[:] = []
            continue
        if os.path.basename(root) == "frames":
            dirs.append(root)
            subdirs[:] = []
            continue
        if os.path.basename(root) in KEEP_DIRS:
            subdirs[:] = []
            continue
        seq = [n for n in names if is_sequence_frame(n)]
        # a folder is only a frame dump if most of it is numbered PNGs
        if len(seq) >= 20:
            files.extend(os.path.join(root, n) for n in seq)
    return dirs, files


def size_of(path):
    if os.path.isfile(path):
        return os.path.getsize(path)
    return sum(os.path.getsize(os.path.join(r, f))
               for r, _, fs in os.walk(path) for f in fs)


def main():
    dirs, files = walk_targets()
    total = sum(size_of(d) for d in dirs) + sum(size_of(f) for f in files)

    for d in dirs:
        print(f"  dir   {os.path.relpath(d, HERE):<44} {size_of(d) / 1048576:8.1f} MB")
    by_dir = {}
    for f in files:
        by_dir.setdefault(os.path.dirname(f), []).append(f)
    for d, fs in sorted(by_dir.items()):
        n = sum(os.path.getsize(x) for x in fs)
        print(f"  seq   {os.path.relpath(d, HERE):<44} {n / 1048576:8.1f} MB "
              f"({len(fs)} frames)")

    print(f"\n  TOTAL {total / 1073741824:.2f} GB in {len(dirs)} dirs "
          f"+ {len(files)} loose frames")

    if not DO_IT:
        print("\n  dry run. add --delete to actually remove them.")
        return

    for d in dirs:
        shutil.rmtree(d, ignore_errors=True)
    for f in files:
        try:
            os.remove(f)
        except OSError:
            pass
    print(f"\nCLEAN_DONE freed={total} bytes ({total / 1073741824:.2f} GB)")


if __name__ == "__main__":
    main()
