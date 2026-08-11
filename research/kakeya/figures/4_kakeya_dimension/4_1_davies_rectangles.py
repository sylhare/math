"""Figure: the Davies overlap engine for the 2D theorem (Davies 1971: Kakeya sets in R^2 have dimension 2).

Two 1 x delta rectangles crossing at angle theta overlap in a parallelogram of area

    | R_1 cap R_2 |  ~  delta^2 / sin theta        (small delta).

Small overlaps force the union to spread out: the "area 0 but dimension 2" mechanism.

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/davies_rectangles.py
"""
import math

import numpy as np
from _shared import COLORS, math_check, new_axes, poly, save_preview, union_area


# --- geometry: pure-numpy rectangles ---------------------------------------------------
def rectangle(length, width, angle_rad, cx=0.0, cy=0.0):
    """Corners (4x2) of a length x width rectangle centred at (cx,cy), long axis at angle_rad."""
    hl, hw = length / 2.0, width / 2.0
    corners = np.array([[-hl, -hw], [hl, -hw], [hl, hw], [-hl, hw]])
    c, s = math.cos(angle_rad), math.sin(angle_rad)
    rot = np.array([[c, -s], [s, c]])
    return corners @ rot.T + np.array([cx, cy])


def overlap_area(delta, theta_rad):
    """Measured intersection area of two 1 x delta rectangles crossing at angle theta (shapely)."""
    r1 = poly(rectangle(1.0, delta, 0.0))
    r2 = poly(rectangle(1.0, delta, theta_rad))
    return r1.intersection(r2).area


def main():
    delta = 0.01
    thetas_deg = [30, 45, 60, 90]

    rows = []
    max_rel_err = 0.0
    for td in thetas_deg:
        th = math.radians(td)
        measured = overlap_area(delta, th)
        formula = delta**2 / math.sin(th)
        rel = abs(measured - formula) / formula
        max_rel_err = max(max_rel_err, rel)
        rows.append((f"theta={td:>2} deg  overlap",
                     f"measured {measured:.3e}  formula {formula:.3e}  err {rel*100:.2f}%"))

    # fan of rectangles through a common center
    delta_fan = 0.05  # drawn rectangle thickness
    fan_counts = [1, 6, 12, 24]
    union_rows = []
    fan_polys_full = None
    for m in fan_counts:
        rects = [poly(rectangle(1.0, delta_fan, a)) for a in np.linspace(0, math.pi, m, endpoint=False)]
        ua = union_area(rects)
        union_rows.append((f"fan union, {m:>2} directions",
                           f"{ua:.4f}   (sum of areas {m*delta_fan:.3f})"))
        if m == max(fan_counts):
            fan_polys_full = rects

    math_check(
        "Davies overlap  |R1 cap R2| ~ delta^2 / sin theta   (delta = 0.01)",
        [
            *rows,
            ("max relative error", f"{max_rel_err*100:.2f}%   (want few %)"),
            *union_rows,
            ("mechanism", "small overlaps -> large spread union -> dim 2 at area 0"),
        ],
    )

    fig, ax = new_axes(2, figsize=(11, 5.6))

    # left: two rectangles at theta = 30 deg + shaded intersection
    dvis, thv = 0.18, math.radians(30)
    ra = poly(rectangle(1.0, dvis, 0.0))
    rb = poly(rectangle(1.0, dvis, thv))
    inter = ra.intersection(rb)
    for r, col in ((ra, COLORS["needle"]), (rb, COLORS["outer"])):
        xs, ys = r.exterior.xy
        ax[0].fill(xs, ys, color=col, alpha=0.35)
        ax[0].plot(xs, ys, color=col, lw=1.2)
    if not inter.is_empty:
        xs, ys = inter.exterior.xy
        ax[0].fill(xs, ys, color=COLORS["accent"], alpha=0.9, zorder=3)
    ax[0].set_xlim(-0.6, 0.6)
    ax[0].set_ylim(-0.6, 0.6)
    _m = overlap_area(delta, thv)
    _f = delta**2 / math.sin(thv)
    ax[0].set_title(f"two 1 x delta rects, theta=30\noverlap ~ delta^2/sin theta  (err {abs(_m-_f)/_f*100:.1f}% @ delta=0.01)")

    # right: fan through a common center, union shaded
    for r in fan_polys_full:
        xs, ys = r.exterior.xy
        ax[1].fill(xs, ys, color=COLORS["needle"], alpha=0.25, lw=0)
    from shapely.ops import unary_union
    u = unary_union(fan_polys_full)
    geoms = getattr(u, "geoms", [u])
    for g in geoms:
        xs, ys = g.exterior.xy
        ax[1].plot(xs, ys, color=COLORS["accent"], lw=1.0)
    ax[1].set_xlim(-0.6, 0.6)
    ax[1].set_ylim(-0.6, 0.6)
    ax[1].set_title(f"fan of {max(fan_counts)} directions\nunion area {union_area(fan_polys_full):.3f} (grows with spread)")

    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
