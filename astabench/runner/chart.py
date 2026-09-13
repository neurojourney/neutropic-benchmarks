#!/usr/bin/env python3
"""Render ../chart.png from chart.json — same layout as the Aside benchmark charts.

1500 px wide · one row per system (brand mark from logos/, name, config) ·
horizontal bar · value right-aligned. Neutropic rows are blue; a projected (not yet measured) Neutropic
row is light blue, its value prefixed with "≥" and its config says "target".
Bars are scaled between the lowest and highest value like the reference charts.

    python chart.py
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.image as mpimg  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.offsetbox import AnnotationBbox, OffsetImage  # noqa: E402
from matplotlib.patches import Circle, FancyBboxPatch  # noqa: E402

HERE = Path(__file__).resolve().parent
SPEC = json.loads((HERE / "chart.json").read_text(encoding="utf-8"))
LOGOS = HERE / "logos"

W, ROW_H, HEAD_H, FOOT_H = 1500, 100, 115, 51
BLUE, BLUE_LIGHT, GRAY = "#1B66FF", "#A9C4FF", "#E5E5E5"
INK, MUTED, RULE = "#111111", "#8A8A8A", "#E9E9E9"
FONT = "Helvetica Neue"
X_MARK, X_NAME, X_BAR0, X_BAR1, X_VALUE = 82, 124, 430, 1290, 1447


def text(ax, x, y, s, size, color=INK, weight="normal", ha="left"):
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight, ha=ha, va="center", fontfamily=FONT)


def mark(ax, x, y, row):
    """Brand mark: logos/<logo>.png (96 px, drawn at 44 px); falls back to an initial in a ring."""
    logo = LOGOS / f"{row.get('logo', '')}.png"
    if logo.exists():
        ax.add_artist(AnnotationBbox(OffsetImage(mpimg.imread(logo), zoom=44 / 96), (x, y), frameon=False))
        return
    ax.add_patch(Circle((x, y), 22, facecolor="white", edgecolor=INK, linewidth=2.2))
    text(ax, x, y + 1, row["system"][0], 19, weight="bold", ha="center")


def main() -> Path:
    rows = SPEC["rows"]
    height = HEAD_H + ROW_H * len(rows) + FOOT_H
    fig = plt.figure(figsize=(W / 100, height / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(height, 0)
    ax.axis("off")

    text(ax, 60, 68, SPEC["title"], 26, weight="bold")
    if SPEC.get("note"):
        text(ax, X_VALUE, 72, SPEC["note"], 18, color=MUTED, ha="right")
    ax.plot([60, X_VALUE], [HEAD_H - 1, HEAD_H - 1], color=RULE, lw=1)

    values = [r["value"] for r in rows]
    lo, hi = min(values), max(values)
    span = X_BAR1 - X_BAR0
    fmt = SPEC.get("format", "{:.1f}%")
    for i, r in enumerate(rows):
        top = HEAD_H + i * ROW_H
        mid = top + ROW_H / 2
        mark(ax, X_MARK, mid, r)
        text(ax, X_NAME, mid - 15, r["system"], 20, weight="bold")
        text(ax, X_NAME, mid + 15, r.get("config", ""), 16, color=MUTED)
        frac = 1.0 if hi == lo else (r["value"] - lo) / (hi - lo)
        width = span * (0.10 + 0.90 * frac)
        color = GRAY
        if r.get("highlight"):
            color = BLUE_LIGHT if r.get("projected") else BLUE
        ax.add_patch(FancyBboxPatch((X_BAR0, mid - 22), width, 44, boxstyle="round,pad=0,rounding_size=4",
                                    facecolor=color, edgecolor="none"))
        label = fmt.format(r["value"])
        text(ax, X_VALUE, mid, f"≥ {label}" if r.get("projected") else label, 22, ha="right")
        ax.plot([60, X_VALUE], [top + ROW_H, top + ROW_H], color=RULE, lw=1)

    out = HERE.parent / "chart.png"
    fig.savefig(out, dpi=100, facecolor="white")
    plt.close(fig)
    return out


if __name__ == "__main__":
    print(main())
