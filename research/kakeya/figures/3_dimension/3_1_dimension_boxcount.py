"""Figure: Minkowski (box-counting) dimension.

Cover a set with side-delta boxes and count the N(delta) it meets:

    dim_box K = lim_{delta -> 0+} log N(delta) / log(1/delta),   i.e. N(delta) ~ delta^-d.

    segment (length 1):  N = delta^-1 = 10   d = 1
    unit square:         N = delta^-2 = 100  d = 2

Fattening form: |N_delta K| >= c_eps * delta^eps for every eps > 0.

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/dimension_boxcount.py
"""
import math

import numpy as np
from _shared import COLORS, math_check, new_axes, save_preview


# Geometry: pure-numpy box-counting
def _seg_hits_box(p0, p1, xmin, xmax, ymin, ymax):
    """Liang-Barsky: does segment p0->p1 meet the closed axis-aligned box?"""
    x0, y0 = p0
    dx, dy = p1[0] - x0, p1[1] - y0
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, x0 - xmin), (dx, xmax - x0), (-dy, y0 - ymin), (dy, ymax - y0)):
        if abs(p) < 1e-15:
            if q < 0:  # parallel, outside this slab
                return False
            continue
        r = q / p
        if p < 0:
            t0 = max(t0, r)
        else:
            t1 = min(t1, r)
        if t0 > t1:
            return False
    return True


def boxcount_segment(p0, p1, delta):
    """Side-delta boxes the segment meets; returns (count, indices)."""
    n = round(1.0 / delta)
    hits = []
    for i in range(n):
        for j in range(n):
            if _seg_hits_box(p0, p1, i * delta, (i + 1) * delta, j * delta, (j + 1) * delta):
                hits.append((i, j))
    return len(hits), hits


def boxcount_square(delta):
    """The filled unit square meets every box of the grid over [0,1]^2."""
    n = round(1.0 / delta)
    return n * n, [(i, j) for i in range(n) for j in range(n)]


def _dim(n_boxes, delta):
    return math.log(n_boxes) / math.log(1.0 / delta)


def _draw_grid_and_boxes(ax, delta, hits, geometry_draw, title):
    n = round(1.0 / delta)
    for (i, j) in hits:  # shade the covering boxes
        ax.fill([i * delta, (i + 1) * delta, (i + 1) * delta, i * delta],
                [j * delta, j * delta, (j + 1) * delta, (j + 1) * delta],
                color=COLORS["region"], alpha=0.7, zorder=1)
    for k in range(n + 1):  # grid lines
        ax.plot([0, 1], [k * delta, k * delta], color=COLORS["muted"], lw=0.5, zorder=2)
        ax.plot([k * delta, k * delta], [0, 1], color=COLORS["muted"], lw=0.5, zorder=2)
    geometry_draw(ax)
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)
    ax.set_title(title)


def main():
    delta = 0.1
    # horizontal unit segment, strictly inside one grid row
    seg_p0, seg_p1 = np.array([0.0, 0.55]), np.array([1.0, 0.55])

    n_seg, hits_seg = boxcount_segment(seg_p0, seg_p1, delta)
    n_sq, hits_sq = boxcount_square(delta)
    d_seg, d_sq = _dim(n_seg, delta), _dim(n_sq, delta)

    # scaling check at delta = 1/5
    n_seg2, _ = boxcount_segment(seg_p0, seg_p1, 0.2)
    n_sq2, _ = boxcount_square(0.2)

    math_check(
        "Minkowski box-counting dimension  (delta = 1/10)",
        [
            ("segment N(1/10) = delta^-1", f"{n_seg}   (want 10)"),
            ("segment d = logN/log(1/delta)", f"{d_seg:.4f}   (want 1)"),
            ("square  N(1/10) = delta^-2", f"{n_sq}   (want 100)"),
            ("square  d = logN/log(1/delta)", f"{d_sq:.4f}   (want 2)"),
            ("scaling delta=1/5 segment N", f"{n_seg2}   (want 5 = delta^-1)"),
            ("scaling delta=1/5 square  N", f"{n_sq2}   (want 25 = delta^-2)"),
            ("fattening form", "|N_delta K| >= c_eps * delta^eps  for all eps>0"),
        ],
    )

    fig, ax = new_axes(2, figsize=(11, 5.6))
    for a in ax:
        a.axis("on")
        a.set_xticks([])
        a.set_yticks([])

    def _seg(a):
        a.plot([seg_p0[0], seg_p1[0]], [seg_p0[1], seg_p1[1]],
               color=COLORS["needle"], lw=3.0, zorder=3)

    def _square(a):
        a.fill([0, 1, 1, 0], [0, 0, 1, 1], facecolor="none",
               edgecolor=COLORS["needle"], lw=2.5, hatch="//", zorder=3)

    _draw_grid_and_boxes(ax[0], delta, hits_seg, _seg,
                         f"unit segment   N = {n_seg},  d = {d_seg:.0f}")
    _draw_grid_and_boxes(ax[1], delta, hits_sq, _square,
                         f"unit square   N = {n_sq},  d = {d_sq:.0f}")
    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
