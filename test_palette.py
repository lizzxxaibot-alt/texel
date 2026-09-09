"""Palette parsing tests. py -3 test_palette.py"""
import sys
from core import palette as P
fails = []
def check(n, c, d=""):
    print(f"[{'ok  ' if c else 'FAIL'}] {n}" + ("" if c else f"  {d}"))
    if not c: fails.append(n)

gpl = "GIMP Palette\nName: Sunset\nColumns: 4\n# a comment\n255   0   0\tred\n  0 128 255\tblue\n"
name, cols = P.parse(gpl, "x.gpl")
check("gpl name parsed", name == "Sunset", name)
check("gpl colours parsed", cols == [(255,0,0,255), (0,128,255,255)], cols)
check("gpl skips comments and headers", len(cols) == 2)

check("hex 6-digit", P.parse_hex("#ff0000\n00ff00") == [(255,0,0,255),(0,255,0,255)])
check("hex 3-digit shorthand", P.parse_hex("#f00") == [(255,0,0,255)])
check("hex 8-digit carries alpha", P.parse_hex("80ff0000") == [(255,0,0,128)])
check("hex ignores junk", P.parse_hex("not-a-colour\n#00f") == [(0,0,255,255)])
check("hex handles commas", len(P.parse_hex("ff0000, 00ff00, 0000ff")) == 3)

lj = '{"name":"PICO-8","colors":["000000","1D2B53","FF004D"]}'
n2, c2 = P.parse_lospec_json(lj)
check("lospec json name", n2 == "PICO-8", n2)
check("lospec json colours", c2[2] == (255,0,77,255), c2)
check("parse() sniffs json without an extension", P.parse(lj)[0] == "PICO-8")
check("parse() sniffs gpl by header", P.parse(gpl)[0] == "Sunset")

check("dedupe preserves order",
      P.dedupe([(1,1,1,255),(2,2,2,255),(1,1,1,255)]) == [(1,1,1,255),(2,2,2,255)])

rt = P.parse(P.to_gpl("RT", [(10,20,30,255),(40,50,60,255)]), "RT.gpl")
check("gpl round trips", rt[1] == [(10,20,30,255),(40,50,60,255)], rt)
check("gpl round trips the name", rt[0] == "RT", rt[0])

# frequency ordering: blue appears 3x, red once -> blue must rank first
px = []
for c in [(0,0,1,1)]*3 + [(1,0,0,1)] + [(0,0,0,0)]*4:
    px += list(c)
got = P.from_image_pixels(px, 4, 2)
check("image palette drops transparent", (0,0,0,0) not in got, got)
check("image palette ranks by frequency", got[0] == (0,0,255,255), got)

print()
if fails: print(f"{len(fails)} FAILED: {fails}"); sys.exit(1)
print("PALETTE CORE: ALL PASS")
