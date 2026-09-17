"""Status text that fits the sidebar it is drawn in.

Written first, against T-008: Blender middle-elided the density readout to
"10.5 px/unit av....1, 8.4x spread)" in a 280 px N-panel, which loses the range
AND the spread - the entire measurement the product is positioned on. Region
width is read-only, so the string has to shrink instead of the panel growing.

Reproduced on Blender 4.5.9 before this file existed: 34 characters survived in
that row, so the LIMIT below is set with headroom rather than at the edge - a
threshold set at the lowest passing case decides nothing.

  py -3 test_report.py
"""
import sys

from core import report as Rp

fails = []


def check(n, c, d=""):
    print(f"[{'ok  ' if c else 'FAIL'}] {n}" + ("" if c else f"  {d}"))
    if not c:
        fails.append(n)


# ------------------------------------------------------- the reproduction
# The exact numbers from the three-cube mesh: 3.2 m / 1.0 m / 0.38 m joined,
# one 32 px texture. This is the string that shipped, and what replaces it.
old = "10.5 px/unit avg  (2.5-21.1, 8.4x spread)"
check("the shipped one-liner is over budget", len(old) > Rp.LIMIT, len(old))

got = Rp.density_status(2.5, 21.1, 10.52)
lines = Rp.status_lines(got)
check("density reports three lines", len(lines) == 3, lines)
check("every line fits", all(len(x) <= Rp.LIMIT for x in lines),
      [(x, len(x)) for x in lines])
check("the average survives", "10.5" in lines[0], lines)
check("the range survives", "2.5" in lines[1] and "21.1" in lines[1], lines)
check("the spread survives", "8.4" in lines[2], lines)
check("the unit is stated once", sum("px/unit" in x for x in lines) == 1, lines)

# the spread is hi/lo, and for this mesh that equals the 3.2/0.38 size ratio -
# the same assertion promo/density/make_density.py makes about the card
check("spread equals the size ratio", "8.4x" in lines[2], lines[2])

# ------------------------------------------------------- degenerate input
check("a zero floor does not divide by zero",
      Rp.density_status(0.0, 5.0, 2.5).count("\n") == 2,
      Rp.density_status(0.0, 5.0, 2.5))
check("zero floor says so rather than printing a ratio",
      Rp.density_status(0.0, 5.0, 2.5).split("\n")[2] == "spread n/a",
      Rp.density_status(0.0, 5.0, 2.5))
uniform = Rp.status_lines(Rp.density_status(8.0, 8.0, 8.0))
check("a uniform mesh reads 1.0x", "1.0x" in uniform[2], uniform)

# a four-digit density still fits - a 2 cm prop on a 512 px texture is real
big = Rp.status_lines(Rp.density_status(1024.0, 4096.0, 2048.0))
check("four-digit densities still fit", all(len(x) <= Rp.LIMIT for x in big),
      [(x, len(x)) for x in big])

# ------------------------------------------------------------ the wrapper
check("a short line is left alone", Rp.status_lines("12 faces") == ["12 faces"])
check("blank text gives no lines", Rp.status_lines("") == [])
check("whitespace gives no lines", Rp.status_lines("   \n  ") == [])

zones = Rp.status_lines("2.5-21.1 px/unit -> 3 zones: 4 / 12 / 8 faces")
check("a long zone summary is split", len(zones) > 1, zones)
check("every wrapped line fits", all(len(x) <= Rp.LIMIT for x in zones),
      [(x, len(x)) for x in zones])
check("wrapping loses no words",
      " ".join(zones).split() ==
      "2.5-21.1 px/unit -> 3 zones: 4 / 12 / 8 faces".split(), zones)

# a word longer than the budget cannot be wrapped politely, so it is cut rather
# than allowed to elide - a path a pasted filename reaches immediately
long_word = "C:/a/very/long/path/that/nobody/should/have/pasted/here.png"
cut = Rp.status_lines(long_word)
check("an unbreakable word is hard-cut", all(len(x) <= Rp.LIMIT for x in cut),
      [(x, len(x)) for x in cut])
check("a hard cut keeps every character", "".join(cut) == long_word, cut)

mixed = Rp.status_lines("saved " + long_word)
check("a long word after a short one still fits",
      all(len(x) <= Rp.LIMIT for x in mixed), [(x, len(x)) for x in mixed])

check("an explicit break is honoured",
      Rp.status_lines("one\ntwo") == ["one", "two"])
check("a custom limit is honoured",
      all(len(x) <= 10 for x in Rp.status_lines("alpha beta gamma delta", 10)),
      Rp.status_lines("alpha beta gamma delta", 10))
check("a limit of one degrades to one char per line",
      Rp.status_lines("ab", 1) == ["a", "b"], Rp.status_lines("ab", 1))

print()
if fails:
    print(f"{len(fails)} FAILED: {fails}"); sys.exit(1)
print("REPORT CORE: ALL PASS")
