"""Minkowski vs Hausdorff dimension (kakeya.md 3a-3b).

Both measure a set by covers. Minkowski uses ONE box size delta: N(delta) boxes,
d_box = log N(delta) / log(1/delta). Hausdorff allows covers of ANY sizes <= delta and takes
H^s(E) = lim_{delta->0} inf { sum (diam U_i)^s : E subset union U_i, diam U_i <= delta }; the
Hausdorff dimension is the threshold where H^s jumps from +inf to 0:
dim_H = inf{ s : H^s(E) = 0 }. Always dim_H <= dim_box.

Panels: (1) uniform delta-grid cover of a Koch curve (Minkowski); (2) a variable-size cover of the
same curve (Hausdorff); (3) the H^s vs s jump at s = dim_H.

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/3_dimension/3_3_hausdorff_minkowski.py
"""
import math

import numpy as np
from _shared import COLORS, math_check, save_preview

DIM = math.log(4) / math.log(3)   # Koch curve Hausdorff = Minkowski dimension ~ 1.2619


def koch(p0, p1, depth):
    if depth == 0:
        return [np.asarray(p0, float)]
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    d = (p1 - p0) / 3.0
    a, b = p0 + d, p0 + 2 * d
    c, s = math.cos(math.radians(-60)), math.sin(math.radians(-60))
    peak = a + np.array([[c, -s], [s, c]]) @ (b - a)
    return koch(p0, a, depth - 1) + koch(a, peak, depth - 1) + koch(peak, b, depth - 1) + koch(b, p1, depth - 1)


def polyline(depth):
    pts = [*koch((0, 0), (1, 0), depth), np.array([1.0, 0.0])]
    return np.array(pts)


def boxes_hit(curve, delta):
    """Cells of a delta-grid the curve passes through (dense-sample the polyline)."""
    seg = np.diff(curve, axis=0)
    n = max(2, int(np.ceil(np.sum(np.hypot(seg[:, 0], seg[:, 1])) / (delta / 4))))
    samp = curve[np.linspace(0, len(curve) - 1, n).astype(int)]
    cells = {(int(np.floor(x / delta)), int(np.floor(y / delta))) for x, y in samp}
    return cells


def main():
    fig, ax = new_axes3()
    curve = polyline(4)

    # panel 1: uniform delta-grid (Minkowski)
    delta = 1.0 / 27.0
    cells = boxes_hit(curve, delta)
    for (i, j) in cells:
        ax[0].add_patch(_rect(i * delta, j * delta, delta, delta, COLORS["region"], 0.55))
    ax[0].plot(curve[:, 0], curve[:, 1], color=COLORS["needle"], lw=1.2)
    ax[0].set_title(f"Minkowski: one size delta, N(delta) = {len(cells)} boxes\n"
                    f"d_box = log N / log(1/delta)", fontsize=10)

    # panel 2: variable-size cover (Hausdorff) -- coarse boxes on the straight left, fine on the right
    ax[1].plot(curve[:, 0], curve[:, 1], color=COLORS["needle"], lw=1.2)
    for k in range(3):        # three big boxes over the left half
        ax[1].add_patch(_rect(k / 6.0, -0.02, 1 / 6.0, 1 / 6.0, COLORS["region"], 0.5))
    fine = 1.0 / 27.0         # many small boxes over the wiggly right half
    for (i, j) in boxes_hit(curve[len(curve) // 2:], fine):
        ax[1].add_patch(_rect(i * fine, j * fine, fine, fine, COLORS["accent"], 0.45))
    ax[1].set_title("Hausdorff: any sizes <= delta,\nminimise sum (diam U_i)^s", fontsize=10)

    for a in ax[:2]:
        a.set_xlim(-0.05, 1.05); a.set_ylim(-0.45, 0.35)

    # panel 3: H^s jumps from +inf to 0 at s = dim_H
    s = np.linspace(0.6, 2.0, 400)
    hs = np.where(s < DIM, 1.0 / np.clip(DIM - s, 1e-2, None), 0.0)
    ax[2].plot(s, np.clip(hs, 0, 12), color=COLORS["accent"], lw=2)
    ax[2].axvline(DIM, color=COLORS["guide"], ls="--", lw=1)
    ax[2].text(DIM + 0.03, 6, f"dim_H = {DIM:.4f}", color=COLORS["guide"], fontsize=9)
    ax[2].text(0.62, 11, "H^s = +inf", color=COLORS["accent"], fontsize=9, va="top")
    ax[2].text(1.55, 0.6, "H^s = 0", color=COLORS["accent"], fontsize=9)
    ax[2].set_xlim(0.6, 2.0); ax[2].set_ylim(-0.5, 12)
    ax[2].set_xlabel("s"); ax[2].set_title("H^s jumps at s = dim_H   (dim_H <= dim_box)", fontsize=10)
    ax[2].set_yticks([])
    ax[2].axis("on"); ax[2].spines[["top", "right"]].set_visible(False)

    math_check(
        "Minkowski vs Hausdorff",
        [
            ("Koch curve dim", f"log4/log3 = {DIM:.4f}  (self-similar: dim_H = dim_box)"),
            ("Minkowski", "one box size delta; d_box = log N(delta)/log(1/delta)"),
            ("uniform cover count", f"N(delta={delta:.3f}) = {len(cells)} boxes"),
            ("Hausdorff", "covers of any size <= delta; H^s = inf sum (diam)^s"),
            ("dimension", "dim_H = inf{s: H^s=0}; always dim_H <= dim_box"),
        ],
    )
    print("wrote", save_preview(fig))


def new_axes3():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 3, figsize=(15, 5.0))
    for a in (axes[0], axes[1]):
        a.set_aspect("equal"); a.axis("off")
    return fig, axes


def _rect(x, y, w, h, color, alpha):
    import matplotlib.patches as mpatches
    return mpatches.Rectangle((x, y), w, h, facecolor=color, edgecolor=color, alpha=alpha, linewidth=0.3)


if __name__ == "__main__":
    main()
