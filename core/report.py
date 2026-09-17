"""Turning a measurement into text that fits the panel it is drawn in.

Blender's `layout.label()` middle-elides anything wider than its row, and
`Region.width` is read-only, so a panel cannot grow to fit a string. The N-panel
is 280 px; the density readout was 41 characters and came out as
"10.5 px/unit av....1, 8.4x spread)" - average intact, range and spread gone.

So the string shrinks. No bpy in here, which is why the wrapping is testable
without opening Blender at all.
"""
from __future__ import annotations

# 34 characters survived in the reproduction on Blender 4.5.9 at UI scale 1.
# This sits well under that on purpose: the row loses width again to the icon
# and the dismiss button, and a user at a larger UI scale has fewer characters
# than we measured. A budget set at the last passing case is not a budget.
LIMIT = 24


def density_status(lo: float, hi: float, avg: float) -> str:
    """The density readout, one measurement per line.

    Three facts, and all three are the claim: the average is what you set a
    target from, the range is how bad it is, and the spread is the number that
    says whether the mesh is consistent at all. Losing any one of them to an
    ellipsis loses the readout.
    """
    spread = f"{hi / lo:.1f}x spread" if lo > 0 else "spread n/a"
    return f"{avg:.1f} px/unit average\nrange {lo:.1f} - {hi:.1f}\n{spread}"


def status_lines(text: str, limit: int = LIMIT) -> list[str]:
    """Split a status into lines no wider than `limit` characters.

    Honours explicit newlines first, then word-wraps what is left. A single word
    longer than the budget is cut rather than left to elide - a pasted file path
    reaches that path on its first use, and half a path is more useful than a
    path with its middle replaced by dots.
    """
    limit = max(1, limit)
    out: list[str] = []
    for chunk in text.split("\n"):
        line = ""
        for word in chunk.split():
            while len(word) > limit:               # unbreakable: cut it
                if line:
                    out.append(line)
                    line = ""
                out.append(word[:limit])
                word = word[limit:]
            if not line:
                line = word
            elif len(line) + 1 + len(word) <= limit:
                line += " " + word
            else:
                out.append(line)
                line = word
        if line:
            out.append(line)
    return out
