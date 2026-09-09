#!/bin/bash
# Cut the five shots into one reel, and pull a still out of each for the
# listing contact sheet.
#
# Hard cuts, not dissolves: a tool reel is a list of claims, and a dissolve
# blurs the boundary between two of them.
set -e
cd /c/Users/opule/Desktop/Make_Money/app_ventures/gumroad/texel
OUT=promo
STORE=store
mkdir -p "$STORE" "$OUT/_reel"

# a representative frame from each shot, for the contact sheet
pick () { cp "$OUT/shots/$1/frames/$(printf 'f_%04d.png' "$2")" "$STORE/shot_$1.png"; }
pick dungeon 120
pick temple  110
pick hangar  120
pick market  130
pick shrine  110

# 6 seconds from the middle of each, re-encoded to identical parameters so the
# concat demuxer does not have to guess
i=0
: > "$OUT/_reel/list.txt"
for s in dungeon temple hangar market shrine; do
  ffmpeg -y -loglevel error -ss 1.0 -t 6.0 -i "$OUT/shot-$s.mp4" \
    -vf "scale=1280:720:flags=lanczos,fps=24" \
    -c:v libx264 -pix_fmt yuv420p -crf 18 -an "$OUT/_reel/p$i.mp4"
  echo "file 'p$i.mp4'" >> "$OUT/_reel/list.txt"
  i=$((i+1))
done

ffmpeg -y -loglevel error -f concat -safe 0 -i "$OUT/_reel/list.txt" \
  -c copy "$OUT/texel-reel-2026.mp4"

DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT/texel-reel-2026.mp4")
SZ=$(stat -c %s "$OUT/texel-reel-2026.mp4")
echo "REEL_DONE dur=${DUR}s bytes=$SZ stills=$(ls $STORE/shot_*.png | wc -l)"
