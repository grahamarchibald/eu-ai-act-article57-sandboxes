#!/usr/bin/env python3
"""Timeline of national sandbox instruments against the Article 57 deadline.

Run from the repository root:  python3 scripts/make_figure.py
Writes figures/instrument-timeline.png and .pdf
"""
import csv, os, sys
from datetime import date

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(ROOT, "data", "article57-implementation.csv")
OUTDIR = os.path.join(ROOT, "figures")

ORIGINAL_DEADLINE = date(2026, 8, 2)   # Art. 57(1) as enacted
DEFERRED_DEADLINE = date(2027, 8, 2)   # as amended by Reg. (EU) 2026/1744
OMNIBUS_IN_FORCE = date(2026, 7, 27)

INK = "#1b1b1b"
MUTED = "#8a8a8a"
IN_FORCE = "#2a6f7f"
PUBLISHED = "#c2814a"
PARTICIPANTS = "#8c4a63"


def iso(s):
    return date.fromisoformat(s) if s else None


def main():
    rows = list(csv.DictReader(open(CSV_PATH, encoding="utf-8")))
    pts = []
    for r in rows:
        f, p, a = (iso(r["date_in_force"]), iso(r["date_published"]),
                   iso(r["date_adopted"]))
        anchor = f or p or a or iso(r["date_first_participants"])
        if anchor:
            pts.append((r["member_state"], anchor, f, p or a,
                        iso(r["date_first_participants"]), r["status_verified"]))
    if not pts:
        print("no dated instruments — nothing to plot")
        return 1
    pts.sort(key=lambda t: t[1])

    fig, ax = plt.subplots(figsize=(9.5, 0.44 * len(pts) + 2.4))
    ys = range(len(pts))

    ax.axvline(ORIGINAL_DEADLINE, color=MUTED, ls=":", lw=1.2, zorder=1)
    ax.axvline(DEFERRED_DEADLINE, color=INK, ls="--", lw=1.2, zorder=1)
    ax.axvspan(OMNIBUS_IN_FORCE, DEFERRED_DEADLINE, color="#000000", alpha=0.035, zorder=0)

    for y, (ms, anchor, f, p, fp, status) in zip(ys, pts):
        if p and f and p != f:
            ax.plot([p, f], [y, y], color=MUTED, lw=1.0, zorder=2)
        if p:
            ax.plot(p, y, "o", ms=4.5, mfc="white", mec=PUBLISHED, mew=1.4, zorder=3)
        if f:
            ax.plot(f, y, "o", ms=6, color=IN_FORCE, zorder=4)
        if fp:
            ax.plot(fp, y, "D", ms=6, color=PARTICIPANTS, zorder=5)
        if fp and not (f or p):
            # participants but no national instrument: the conflation case
            ax.annotate(" participants admitted, no Art. 57 instrument", (fp, y),
                        fontsize=7.5, color=PARTICIPANTS, va="center",
                        xytext=(8, 0), textcoords="offset points")

    ax.set_yticks(list(ys))
    ax.set_yticklabels([f"{ms}" for ms, *_ in pts], fontsize=9)
    ax.invert_yaxis()
    ax.set_xlim(date(2023, 8, 1), date(2027, 12, 31))
    ax.tick_params(axis="x", labelsize=9)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="x", color="#eeeeee", lw=0.8, zorder=0)
    ax.set_axisbelow(True)

    ax.text(ORIGINAL_DEADLINE, -0.9, " Art. 57 deadline\n as enacted", fontsize=7.5,
            color=MUTED, va="bottom")
    ax.text(DEFERRED_DEADLINE, -0.9, " deferred by\n Reg. (EU) 2026/1744", fontsize=7.5,
            color=INK, va="bottom")

    handles = [
        Line2D([], [], marker="o", ls="", mfc="white", mec=PUBLISHED, mew=1.4, ms=5, label="published"),
        Line2D([], [], marker="o", ls="", color=IN_FORCE, ms=6, label="in force"),
        Line2D([], [], marker="D", ls="", color=PARTICIPANTS, ms=6, label="first participants admitted"),
    ]
    ax.legend(handles=handles, loc="lower left", frameon=False, fontsize=8,
              bbox_to_anchor=(0.0, 0.02))
    ax.set_title("National sandbox instruments against the Article 57 deadline",
                 fontsize=11, loc="left", pad=26)

    os.makedirs(OUTDIR, exist_ok=True)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(OUTDIR, f"instrument-timeline.{ext}"), dpi=200,
                    bbox_inches="tight")
    print(f"wrote figures/instrument-timeline.png and .pdf — {len(pts)} dated instruments")
    return 0


if __name__ == "__main__":
    sys.exit(main())
