#!/bin/bash
cd /c/Users/opule/Desktop/Make_Money/app_ventures/gumroad/texel
BL="/c/Users/opule/tools/blender-4.5.9-windows-x64/blender.exe"
run () { "$BL" --background --factory-startup --python gameshots.py -- "$1" "$2" 2>&1 \
  | grep -E "TEXEL_SHOT_DONE|eta |Error"; }
run dungeon 216
run temple  192
run hangar  192
run market  216
run shrine  168
echo ALL_SHOTS_COMPLETE
