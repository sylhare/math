"""Animation: the deltoid drawn by a circle rolling inside a 3x circle (kakeya.md 2b; Accromath).

"en faisant tourner un cercle de rayon 1 a l'interieur d'un cercle de rayon 3. La deltoide est la
courbe dessinee par un point lors de ce mouvement." A rolling circle of radius r inside a fixed circle
of radius 3r; a marked point on the rolling circle traces the three-cusped hypocycloid (deltoid):

    x(t) = 2r cos t + r cos 2t,   y(t) = 2r sin t - r sin 2t.

With r = 1/4 the traced deltoid has constant tangent chord 4r = 1 (a unit needle) and area 2 pi r^2 =
pi/8, matching 2b. The rolling circle centre travels on the radius-(2r) circle; the marked point is
fixed on the rolling rim.

Run: PYTHONPATH=research/kakeya/figures uv run --with matplotlib --with shapely --with pillow \
     python research/kakeya/figures/2_kakeya_2d/2_1_2_deltoid_rolling_anim.py
"""

import math

import numpy as np
from _shared import COLORS, circle, deltoid, math_check, save_gif

R_ROLL = 0.25  # rolling radius r (= b); fixed circle radius = 3r
R_FIX = 3.0 * R_ROLL
N = 96  # frames over one full revolution
END_HOLD = 10


def rolling_center(t):
    return np.array([(R_FIX - R_ROLL) * math.cos(t), (R_FIX - R_ROLL) * math.sin(t)])


def traced_point(t):
    """Marked point on the rolling rim = the deltoid point at parameter t."""
    return np.array([2 * R_ROLL * math.cos(t) + R_ROLL * math.cos(2 * t),
                     2 * R_ROLL * math.sin(t) - R_ROLL * math.sin(2 * t)])


def main():
    ts = np.linspace(0.0, 2 * math.pi, N, endpoint=True)
    curve = deltoid(R_ROLL, n=400)  # reference deltoid from _shared

    # --- honesty: the traced point lies on the rolling rim; chord 4r = 1; area 2 pi r^2 = pi/8 ----
    rim_err = max(abs(np.linalg.norm(traced_point(t) - rolling_center(t)) - R_ROLL) for t in ts)
    assert rim_err < 1e-9, f"traced point must lie on the rolling rim (err {rim_err:.2e})"
    chord = 4 * R_ROLL
    area = 2 * math.pi * R_ROLL**2

    math_check(
        "deltoid by rolling a radius-r circle inside a radius-3r circle",
        [
            ("rolling / fixed radius", f"r = {R_ROLL}, fixed = 3r = {R_FIX}"),
            ("traced point on rim", f"|traced - centre| = r for all t (max err {rim_err:.1e})"),
            ("tangent chord 4r", f"{chord:.3f}  (unit needle)"),
            ("deltoid area 2 pi r^2", f"{area:.4f}  (pi/8 = {math.pi / 8:.4f})"),
        ],
    )

    # ---- figure -------------------------------------------------------------------------
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    fixed = circle(R_FIX, n=200)
    lim = R_FIX + 0.06
    fig, ax = plt.subplots(figsize=(6.0, 6.0))
    ax.set_aspect("equal")
    ax.axis("off")

    frames = list(range(N)) + [N - 1] * END_HOLD

    def update(fi):
        k = frames[fi]
        t = ts[k]
        c = rolling_center(t)
        p = traced_point(t)
        roll = circle(R_ROLL, n=80, cx=c[0], cy=c[1])

        ax.cla()
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.plot(fixed[:, 0], fixed[:, 1], color=COLORS["guide"], lw=1.5)  # fixed circle
        ax.plot(curve[: max(2, int(400 * (k + 1) / N)), 0],
                curve[: max(2, int(400 * (k + 1) / N)), 1], color=COLORS["accent"], lw=2.0)  # deltoid so far
        ax.fill(roll[:, 0], roll[:, 1], facecolor=COLORS["region"], edgecolor=COLORS["outer"], lw=1.2, alpha=0.7)
        ax.plot([c[0], p[0]], [c[1], p[1]], color=COLORS["outer"], lw=1.0)  # spoke to the marked point
        ax.plot(*p, "o", color=COLORS["accent"], ms=8, zorder=5)  # the tracing point
        ax.plot(*c, "o", color=COLORS["guide"], ms=3, zorder=5)
        ax.set_title("a circle rolling inside a 3x circle draws the deltoid", fontsize=11)
        return []

    anim = FuncAnimation(fig, update, frames=len(frames), interval=70, blit=False)
    print("wrote", save_gif(anim, fps=16, dpi=95))


if __name__ == "__main__":
    main()
