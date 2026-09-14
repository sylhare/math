r"""Kakeya maximal function, animated (kakeya.md 5a).

A probe delta-tube through x0 = 0 sweeps every direction omega; for each direction the tube average
(1/|T|) int_T f is recorded (f = indicator of a disc). The maximal function at x0 is the running
supremum over directions:  M f(x0) = sup_omega  avg(omega).

Left: the probe tube rotating over the blob, with its live average read out. Right: the per-direction
average curve building up as the sweep proceeds, the running max marked.

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/5_conjecture_tower/5_1_kakeya_maximal_anim.py
"""

import numpy as np
from _shared import COLORS, math_check, save_gif
from matplotlib.animation import FuncAnimation

DELTA = 0.06
BLOB_C = (0.22, 0.14)
BLOB_R = 0.12
GRID_N = 160
EXTENT = 0.62
N_DIRS = 72
HOLD_TAIL = 10  # frames held at end


def tube_mask(X, Y, angle, p0=(0.0, 0.0), length=1.0, half_width=DELTA / 2):
    """Boolean grid mask of the delta-tube through p0 in direction `angle` (length 1, radius delta/2)."""
    ca, sa = np.cos(angle), np.sin(angle)
    dx, dy = X - p0[0], Y - p0[1]
    along = dx * ca + dy * sa
    perp = -dx * sa + dy * ca
    return (np.abs(perp) <= half_width) & (np.abs(along) <= length / 2)


def main():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon

    xs = np.linspace(-EXTENT, EXTENT, GRID_N)
    X, Y = np.meshgrid(xs, xs)
    f = (((X - BLOB_C[0]) ** 2 + (Y - BLOB_C[1]) ** 2) <= BLOB_R**2).astype(float)

    angles = np.linspace(0.0, np.pi, N_DIRS, endpoint=False)
    avgs = []
    for a in angles:
        m = tube_mask(X, Y, a)
        avgs.append(float(f[m].mean()))
    avgs = np.array(avgs)
    running_max = np.maximum.accumulate(avgs)
    final_max = float(running_max[-1])

    assert final_max >= avgs.max() - 1e-12
    assert all(running_max[i] >= avgs[i] - 1e-12 for i in range(N_DIRS))

    math_check(
        "Kakeya maximal function, sweep (animated)",
        [
            ("definition", "M f(x0) = sup_omega  (1/|T|) int_T f,  T tube through x0 along omega"),
            ("bound", "|| f*_delta ||_{L^n(S^{n-1})} <= C_eps delta^{-eps} || f ||_{L^n(R^n)}"),
            ("delta (tube radius)", f"{DELTA}"),
            ("directions swept", f"{N_DIRS}  (delta-separated on the half-circle)"),
            ("tube averages", f"min {avgs.min():.3f}  max {avgs.max():.3f}"),
            ("maximal average M f(x0)", f"{final_max:.3f}   (= sup over directions)"),
            ("running max dominates each avg", "YES"),
        ],
    )

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(12.5, 5.4))

    th = np.linspace(0, 2 * np.pi, 200)
    axL.plot(BLOB_C[0] + BLOB_R * np.cos(th), BLOB_C[1] + BLOB_R * np.sin(th), color=COLORS["accent"], lw=1.4)
    axL.text(BLOB_C[0], BLOB_C[1], "f=1", color=COLORS["accent"], ha="center", va="center", fontsize=9)
    axL.plot([0], [0], "o", color=COLORS["guide"], ms=7, zorder=5)
    axL.text(0.02, -0.06, "x0", color=COLORS["guide"], fontsize=10)
    tube_patch = Polygon(
        np.zeros((4, 2)), closed=True, facecolor=COLORS["needle"], edgecolor=COLORS["needle"], alpha=0.45, lw=0.8
    )
    axL.add_patch(tube_patch)
    axL.set_xlim(-EXTENT, EXTENT)
    axL.set_ylim(-EXTENT, EXTENT)
    axL.set_aspect("equal")

    deg = np.degrees(angles)
    (curve,) = axR.plot([], [], color=COLORS["needle"], lw=2.0)
    (maxline,) = axR.plot([], [], color=COLORS["accent"], lw=1.2, ls="--")
    (dot,) = axR.plot([], [], "o", color=COLORS["accent"], ms=6)
    axR.set_xlim(0, 180)
    axR.set_ylim(-0.02, max(0.15, float(avgs.max()) * 1.25))
    axR.set_xlabel("direction omega (deg)")
    axR.set_ylabel("tube average  (1/|T|) int_T f")

    n_frames = N_DIRS + HOLD_TAIL

    def update(i):
        k = min(i, N_DIRS - 1)
        a = float(angles[k])
        ca, sa = np.cos(a), np.sin(a)
        axis = np.array([ca, sa])
        perp = np.array([-sa, ca])
        c = 0.5 * axis
        corners = np.array(
            [c - (DELTA / 2) * perp, c + (DELTA / 2) * perp, -c + (DELTA / 2) * perp, -c - (DELTA / 2) * perp]
        )
        tube_patch.set_xy(corners)
        axL.set_title(f"probe tube at {np.degrees(a):5.1f} deg:  avg = {avgs[k]:.3f}", fontsize=11)
        curve.set_data(deg[: k + 1], avgs[: k + 1])
        maxline.set_data([0, np.degrees(a)], [running_max[k], running_max[k]])
        dot.set_data([np.degrees(a)], [running_max[k]])
        axR.set_title(f"running max  M f(x0) = {running_max[k]:.3f}", fontsize=11)
        return tube_patch, curve, maxline, dot

    anim = FuncAnimation(fig, update, frames=n_frames, interval=140, blit=False)
    print("wrote", save_gif(anim, fps=8, dpi=95))


if __name__ == "__main__":
    main()
