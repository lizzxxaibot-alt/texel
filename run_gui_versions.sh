#!/bin/bash
# The GUI suites, per Blender version, ONE AT A TIME.
# They open real windows; two Blenders drawing at once makes the results
# meaningless, which is why these are not in test_versions.sh.
cd "$(dirname "$0")"
TOOLS=/c/Users/opule/tools
for BL in "$TOOLS"/blender-*/blender.exe; do
  [ -x "$BL" ] || continue
  VER=$("$BL" --version 2>/dev/null | head -1 | sed 's/Blender //;s/ .*//')
  echo "=== Blender $VER ==="
  for t in test_panels test_keys test_workspace test_e2e; do
    printf "  %-16s " "$t"
    out=$("$BL" --factory-startup --python "$t.py" 2>&1)
    if echo "$out" | grep -qE "ALL PASS"; then echo "pass"
    else
      echo "FAIL"
      echo "$out" | grep -E "^\[FAIL|^   - |WATCHDOG" | head -4 | sed 's/^/       /'
    fi
  done
done
echo "GUI_VERSIONS_DONE"
