"""Animation: the Davies overlap engine, building a fan of 1 x delta rectangles across [0, pi).

Each new rectangle (angle theta) overlaps the base (angle 0) in

    | R_theta cap R_0 |  =  delta^2 / sin theta.

Small overlaps force the union to spread out: the "area 0 but dimension 2" mechanism.

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/davies_fan_anim.py
"""
import math

import numpy as np
from _shared import COLORS, math_check, poly, save_gif, union_area
from matplotlib.animation import FuncAnimation

DELTA = 0.05           # rectangle width
N_DIR = 36             # directions across [0, pi)
END_HOLD = 8


# Geometry: pure-numpy rectangle
def rectangle(length, width, angle_rad, cx=0.0, cy=0.0):
    hl, hw = length / 2.0, width / 2.0
    corners = np.array([[-hl, -hw], [hl, -hw], [hl, hw], [-hl, hw]])
    c, s = math.cos(angle_rad), math.sin(angle_rad)
    rot = np.array([[c, -s], [s, c]])
    return corners @ rot.T + np.array([cx, cy])


def main():
    angles = np.linspace(0.0, math.pi, N_DIR, endpoint=False)
    base = poly(rectangle(1.0, DELTA, 0.0))

    # measured overlap vs formula, and running union area
    measured, formula, unions = [], [], []
    polys = []
    for a in angles:
        polys.append(poly(rectangle(1.0, DELTA, a)))
        unions.append(union_area(polys))
        if a == 0.0:
            measured.append(math.nan); formula.append(math.nan)
        else:
            measured.append(base.intersection(polys[-1]).area)
            formula.append(DELTA ** 2 / math.sin(a))

    # measured overlap matches delta^2/sin theta
    rel_errs = [abs(measured[k] - formula[k]) / formula[k]
                for k in range(1, N_DIR)]
    max_rel = max(rel_errs)
    assert max_rel < 0.02, f"overlap must match delta^2/sin theta (max rel err {max_rel:.3%})"

    # union area is non-decreasing
    diffs = np.diff(unions)
    assert (diffs >= -1e-12).all(), "union area must be non-decreasing"

    sample = [1, N_DIR // 4, N_DIR // 2, 3 * N_DIR // 4]
    rows = [(f"theta={math.degrees(angles[k]):5.1f} deg",
             f"measured {measured[k]:.3e}  formula {formula[k]:.3e}  "
             f"err {abs(measured[k]-formula[k])/formula[k]*100:.2f}%") for k in sample]

    math_check(
        f"Davies fan: |R_theta cap R_0| = delta^2/sin theta   (delta = {DELTA})",
        [
            *rows,
            ("max relative overlap error", f"{max_rel*100:.2f}%   (want < 2%)"),
            ("union area, first -> last", f"{unions[0]:.4f} -> {unions[-1]:.4f}"),
            ("union monotone non-decreasing", f"min step {float(diffs.min()):.2e}  (>= 0)"),
            ("mechanism", "small overlaps -> spread-out union -> dim 2 at area 0"),
        ],
    )

    # Figure
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 2, figsize=(12.0, 5.6))
    ax[0].set_aspect("equal"); ax[0].axis("off")

    frames = list(range(N_DIR)) + [N_DIR - 1] * END_HOLD

    # dense reference curve delta^2 / sin theta for the right panel
    th_dense = np.linspace(math.radians(2), math.pi - math.radians(2), 400)
    ov_dense = DELTA ** 2 / np.sin(th_dense)

    def update(fi):
        k = frames[fi]

        # left: accumulate the fan, base + current highlighted, intersection shaded
        ax[0].cla(); ax[0].axis("off"); ax[0].set_aspect("equal")
        for j in range(k + 1):
            xs, ys = polys[j].exterior.xy
            ax[0].fill(xs, ys, color=COLORS["needle"], alpha=0.22, lw=0)
        xs, ys = base.exterior.xy
        ax[0].plot(xs, ys, color=COLORS["outer"], lw=1.6)
        xs, ys = polys[k].exterior.xy
        ax[0].fill(xs, ys, color=COLORS["needle"], alpha=0.5, lw=0)
        ax[0].plot(xs, ys, color=COLORS["needle"], lw=1.6)
        if k >= 1:
            inter = base.intersection(polys[k])
            if not inter.is_empty and inter.geom_type == "Polygon":
                ix, iy = inter.exterior.xy
                ax[0].fill(ix, iy, color=COLORS["accent"], alpha=0.95, zorder=4)
        ax[0].set_xlim(-0.62, 0.62); ax[0].set_ylim(-0.62, 0.62)
        ax[0].set_title(f"fan of {k + 1} directions through a center\n"
                        f"union area {unions[k]:.4f}  (grows with spread)")

        # right: overlap vs theta, formula curve + measured points
        ax[1].cla()
        ax[1].plot(np.degrees(th_dense), ov_dense, color=COLORS["muted"], lw=1.2,
                   label="delta^2 / sin theta")
        km = [j for j in range(1, k + 1)]
        if km:
            ax[1].plot([math.degrees(angles[j]) for j in km], [measured[j] for j in km],
                       "o", color=COLORS["accent"], ms=5, label="measured overlap")
        if k >= 1:
            ax[1].plot(math.degrees(angles[k]), measured[k], "o", color=COLORS["accent"],
                       ms=11, mfc="none", mew=2)
        ax[1].set_xlim(0, 180); ax[1].set_ylim(0, DELTA ** 2 / math.sin(math.radians(8)))
        ax[1].set_xlabel("theta (deg)"); ax[1].set_ylabel("pairwise overlap area")
        ax[1].grid(True, color=COLORS["muted"], alpha=0.25, lw=0.5)
        cur = f"{math.degrees(angles[k]):.1f} deg" if k >= 1 else "base"
        ax[1].set_title(f"overlap = delta^2 / sin theta   (theta = {cur})")
        ax[1].legend(loc="upper center", fontsize=9)
        return []

    anim = FuncAnimation(fig, update, frames=len(frames), interval=140, blit=False)
    print("wrote", save_gif(anim, fps=8, dpi=95))


if __name__ == "__main__":
    main()
