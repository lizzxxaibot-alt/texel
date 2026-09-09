#!/bin/bash
# Run the gate against every installed Blender, not just the one on this desk.
#
# The manifest declares blender_version_min = "4.2.0" and the store page repeats
# it. Until this existed, that claim was tested against exactly one build -
# 4.5.9 - which makes it a claim, not a fact. CLAUDE.md §6: never claim
# compatibility that was not tested.
#
#   bash test_versions.sh
#
# Add a Blender by dropping its portable folder in ~/tools; it is picked up by
# the glob. Store-installed Blender is skipped deliberately: its WindowsApps
# ACL refuses to run the exe from a script, so it cannot be gated here.
cd "$(dirname "$0")"
TOOLS=/c/Users/opule/tools
PASS=0; FAIL=0
declare -a REPORT

# headless suites only: the GUI ones need a window, and a second Blender opening
# windows while the first is mid-run makes the results meaningless
SUITES="test_blender test_addon test_features test_showcase test_sprite test_anim"

for BL in "$TOOLS"/blender-*/blender.exe; do
  [ -x "$BL" ] || continue
  VER=$("$BL" --version 2>/dev/null | head -1 | sed 's/Blender //;s/ .*//')
  echo
  echo "=============================================================="
  echo " Blender $VER   ($BL)"
  echo "=============================================================="
  bad=0
  for t in $SUITES; do
    printf "  %-16s " "$t"
    out=$("$BL" --background --factory-startup --python "$t.py" 2>&1)
    if echo "$out" | grep -qE "ALL PASS"; then
      echo "pass"
    else
      echo "FAIL"
      echo "$out" | grep -E "^\[FAIL|FAILED|Error|Traceback" | head -3 | sed 's/^/      /'
      bad=1
    fi
  done

  # the install test is the one that proves the ZIP works on this version
  printf "  %-16s " "install"
  out=$("$BL" --background --factory-startup --python test_install.py 2>&1)
  if echo "$out" | grep -qE "ALL PASS"; then echo "pass"; else echo "FAIL"; bad=1
    echo "$out" | grep -E "^\[FAIL|Error" | head -3 | sed 's/^/      /'
  fi

  if [ $bad -eq 0 ]; then
    REPORT+=("  $VER  PASS"); PASS=$((PASS+1))
  else
    REPORT+=("  $VER  FAIL"); FAIL=$((FAIL+1))
  fi
done

echo
echo "=============================================================="
printf '%s\n' "${REPORT[@]}"
echo "VERSIONS_DONE pass=$PASS fail=$FAIL"
[ $FAIL -eq 0 ] || exit 1
