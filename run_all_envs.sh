#!/bin/bash
cd /c/Users/opule/Desktop/Make_Money/app_ventures/gumroad/texel
BL="/c/Users/opule/tools/blender-4.5.9-windows-x64/blender.exe"
for e in shrine corridor ruins tavern cavern; do
  "$BL" --background --factory-startup --python render_env.py -- $e 216 2>&1 \
    | grep -E "TEXEL_ENV_DONE|\[texel\]|eta "
done
echo "ALL_ENVS_COMPLETE"
