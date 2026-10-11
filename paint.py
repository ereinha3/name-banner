#!/usr/bin/env python3
"""Paint a 52x7 pixel banner onto a GitHub contribution graph year.

Column c, row r (Sun..Sat) -> YEAR-01-01 + 7c + r days. YEAR must start on a Sunday.
Usage: python3 paint.py [--dry-run]
"""
import datetime, os, subprocess, sys
from font import F

TEXT, YEAR, W, PER_PIXEL = "Ethan Reinhart", 2017, 52, 4

def grid():
    cols = []
    for k, ch in enumerate(TEXT):
        g = F[ch]
        cols += [[g[r][c] for r in range(7)] for c in range(len(g[0]))]
        if k < len(TEXT) - 1 and ch != ' ' and TEXT[k + 1] != ' ':
            cols.append(['.'] * 7)
    pad = (W - len(cols)) // 2
    return [(r, pad + c) for c, col in enumerate(cols) for r in range(7) if col[r] == "#"]

start = datetime.date(YEAR, 1, 1)
assert start.weekday() == 6, f"{YEAR} does not start on a Sunday"
days = sorted(start + datetime.timedelta(days=7 * c + r) for r, c in grid())
print(f"{len(days)} pixels x {PER_PIXEL} commits = {len(days) * PER_PIXEL} commits, {days[0]} .. {days[-1]}")
if "--dry-run" in sys.argv:
    sys.exit()
for d in days:
    for i in range(PER_PIXEL):
        stamp = f"{d}T12:{i:02d}:00+0000"
        with open("pixels.log", "a") as f:
            f.write(f"{stamp}\n")
        subprocess.run(["git", "add", "pixels.log"], check=True)
        env = {**os.environ, "GIT_AUTHOR_DATE": stamp, "GIT_COMMITTER_DATE": stamp}
        subprocess.run(["git", "commit", "-q", "-m", f"pixel {d}"], env=env, check=True)
