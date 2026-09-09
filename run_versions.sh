#!/bin/bash
# Wait for the Blender downloads, unpack them, then gate every version.
#
# Chained rather than done by hand because the downloads are ~350 MB each and
# the point is the matrix at the end, not babysitting the middle.
set -u
TOOLS=/c/Users/opule/tools
cd "$(dirname "$0")"

want=("blender-4.2.23-windows-x64" "blender-5.2.1-windows-x64")

# ---- 1. wait for each zip to arrive AND stop growing
for n in "${want[@]}"; do
  z="$TOOLS/$n.zip"
  echo "[wait] $n.zip"
  last=-1
  while true; do
    [ -f "$z" ] || { sleep 10; continue; }
    now=$(stat -c %s "$z" 2>/dev/null || echo 0)
    # a size that has not moved in 20s, and is plausibly a full build, is done
    if [ "$now" = "$last" ] && [ "$now" -gt 150000000 ]; then break; fi
    last=$now
    sleep 20
  done
  echo "[wait] $n.zip settled at $((now/1048576)) MB"
done

# ---- 2. unpack whatever is not already unpacked
for n in "${want[@]}"; do
  if [ -x "$TOOLS/$n/blender.exe" ]; then
    echo "[unzip] $n already unpacked"
    continue
  fi
  echo "[unzip] $n ..."
  (cd "$TOOLS" && unzip -q -o "$n.zip") || { echo "[unzip] FAILED $n"; exit 1; }
  [ -x "$TOOLS/$n/blender.exe" ] && echo "[unzip] ok" || echo "[unzip] no exe in $n"
done

# ---- 3. what are we about to test
echo
echo "installed Blenders:"
for BL in "$TOOLS"/blender-*/blender.exe; do
  [ -x "$BL" ] && echo "   $("$BL" --version 2>/dev/null | head -1)"
done

# ---- 4. the gate
echo
bash test_versions.sh
