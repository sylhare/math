"""Kakeya needle set as the bare needle family: 3 rotated Perron trees, unit rays, no fill.

An equilateral Perron tree carries a 60 deg apex fan whose base-midpoint -> apex directions bunch
toward the fan edges. Three trees rotated 0/120/240 deg span the full 180 deg of line-orientations,
so the family holds a unit needle in every direction. Each needle (as an undirected segment, both
its directions) is parked at the corner (90/210/330 deg) nearest its heading and drawn outward at
unit length: every corner collects a 120 deg spray, the three sprays tile the whole turn. No fill.

Run: PYTHONPATH=research/kakeya/figures uv run --with matplotlib --with shapely --with pillow \
     python research/kakeya/figures/2_kakeya_2d/2_6_4_needle_rays.py
"""
import math

import numpy as np
from _shared import math_check, save_preview

N = 6                                   # 2^N unit needles per tree
R = 1.0 / math.sqrt(3.0)                # corner distance from centroid (equilateral, side 1)
B = 0.17                                # Perron base half-width
H = math.sqrt(3.0) * B                  # apex height -> 60 deg apex fan
CORNERS_DEG = (90.0, 210.0, 330.0)      # apex up, three-fold
OFF = np.arctan2(H, np.linspace(-B, B, 2 ** N)) - math.pi / 2.0   # +/-30 deg, bunched at edges
YELLOW = "#f4e37a"


def _unit(a):
    return np.column_stack([np.cos(a), np.sin(a)])


def build():
    """Unit rays for the 3-tree needle family, each parked at its nearest corner (heading outward)."""
    centers = np.radians(CORNERS_DEG)
    dirs = np.concatenate([c + OFF for c in centers] + [c + OFF + math.pi for c in centers])
    diff = np.angle(np.exp(1j * (dirs[:, None] - centers[None, :])))
    k = np.argmin(np.abs(diff), axis=1)
    anchors = R * _unit(centers)[k]
    return np.stack([anchors, anchors + _unit(dirs)], axis=1), dirs


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection

    segs, dirs = build()
    verts = R * _unit(np.radians(CORNERS_DEG))

    covered = np.zeros(180, dtype=int)
    covered[np.round(np.degrees(dirs)).astype(int) % 180] = 1
    math_check(
        "Kakeya needle set: 3 Perron trees as unit rays (method 4, no fill)",
        [
            ("one tree", f"2^{N} = {2 ** N} unit needles, base-midpoint -> apex directions"),
            ("fan span", f"{np.ptp(np.degrees(OFF)):.0f} deg, bunched toward the fan edges"),
            ("three trees", "rotated 0/120/240 deg -> 180/180 deg of line-orientations"),
            ("parking", "each needle drawn outward from its nearest corner -> 120 deg sprays"),
            ("coverage", f"{int(covered.sum())}/180 deg -> a unit needle in every direction"),
        ],
    )

    fig, ax = plt.subplots(figsize=(6.6, 6.2))
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-1.65, 1.65)
    ax.set_ylim(-1.55, 1.75)

    ax.add_collection(LineCollection([verts[[0, 1]], verts[[1, 2]], verts[[2, 0]]],
                                     colors=YELLOW, linewidths=0.8, alpha=0.35))
    lc = LineCollection(segs, colors=YELLOW, linewidths=0.8, alpha=0.6, capstyle="round")
    lc.set_rasterized(True)
    ax.add_collection(lc)

    print("wrote", save_preview(fig, dpi=150))


if __name__ == "__main__":
    main()
