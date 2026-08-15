"""Half-wave propagator e^{it sqrt(-Delta)} and the light cone (kakeya.md 5c-iii).

u(x, t) = e^{it sqrt(-Delta)} f solves the wave equation; a point source spreads along the light cone
|x| = t (45-degree half-angle, dr/dt = 1). Fixed-time Sobolev loss s_p = (n-1)|1/2 - 1/p|; the local
smoothing conjecture recovers it by averaging in t:

    ( int_1^2 || e^{it sqrt(-Delta)} f ||_{L^p}^p dt )^{1/p}  <~  || f ||_{L^p_{s_p - sigma}}.

(a) 2D: expanding wavefronts radius = t. (b) 3D space-time cone |x| = t.

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/local_smoothing_wave.py
"""
import math

import numpy as np
from _shared import COLORS, circle, math_check, save_preview


def s_p(n: int, p: float) -> float:
    """Sharp fixed-time Sobolev loss exponent s_p = (n-1) |1/2 - 1/p| (p = inf -> 1/p = 0)."""
    inv_p = 0.0 if math.isinf(p) else 1.0 / p
    return (n - 1) * abs(0.5 - inv_p)


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (registers 3d projection)

    times = [0.5, 1.0, 1.5]  # t1 < t2 < t3

    # Validation: each wavefront is the circle of radius exactly t
    radius_ok = True
    for t in times:
        c = circle(r=t, n=200)  # helper draws radius-r circle centred at origin
        r_meas = float(np.mean(np.hypot(c[:, 0], c[:, 1])))
        radius_ok = radius_ok and abs(r_meas - t) < 1e-9
    # cone half-angle: |x| = t means radius grows as slope dr/dt = 1 -> angle to t-axis is atan(1)
    half_angle = math.degrees(math.atan2(1.0, 1.0))

    fig = plt.figure(figsize=(12, 5.6))

    # (a) 2D space: expanding wavefronts
    ax = fig.add_subplot(1, 2, 1)
    ax.set_aspect("equal")
    ax.axis("off")
    shades = [COLORS["region"], COLORS["needle"], COLORS["outer"]]
    for t, col in zip(times, shades, strict=False):
        c = circle(r=t, n=200)
        ring = np.vstack([c, c[:1]])
        ax.plot(ring[:, 0], ring[:, 1], color=col, lw=2.2, label=f"t = {t:g},  |x| = {t:g}")
    ax.plot([0], [0], marker="*", ms=13, color=COLORS["accent"], zorder=5)
    ax.annotate("point source", (0, 0), textcoords="offset points", xytext=(6, 6),
                fontsize=9, color=COLORS["accent"])
    lim = max(times) * 1.15
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_title("wavefronts: radius = t")
    ax.legend(loc="lower center", fontsize=8, frameon=False, ncol=1)

    # (b) 3D space-time cone |x| = t
    ax3 = fig.add_subplot(1, 2, 2, projection="3d")
    T = 1.6
    tt = np.linspace(0.0, T, 40)
    th = np.linspace(0.0, 2 * math.pi, 80)
    TT, TH = np.meshgrid(tt, th)
    X = TT * np.cos(TH)   # radius = t
    Y = TT * np.sin(TH)
    ax3.plot_surface(X, Y, TT, color=COLORS["outer"], alpha=0.35,
                     linewidth=0, antialiased=True, shade=True)
    # stack the three fixed-time slices as rings up the cone (the t we average over)
    for t, col in zip(times, shades, strict=False):
        c = circle(r=t, n=120)
        ring = np.vstack([c, c[:1]])
        ax3.plot(ring[:, 0], ring[:, 1], zs=t, color=col, lw=2.0)
    ax3.scatter([0], [0], [0], color=COLORS["accent"], marker="*", s=90)
    ax3.set_xlabel("x_1")
    ax3.set_ylabel("x_2")
    ax3.set_zlabel("t")
    ax3.set_title("space-time light cone  |x| = t  (45 deg)")
    ax3.set_box_aspect((1, 1, 1))
    ax3.view_init(elev=18, azim=-60)

    fig.suptitle(
        r"half-wave propagator  $e^{it\sqrt{-\Delta}}$:  averaging in $t$ buys regularity"
        f"   (n=2:  s_4 = {s_p(2, 4):.2f},  s_inf = {s_p(2, math.inf):.2f})",
        fontsize=11,
    )

    print("wrote", save_preview(fig))

    math_check(
        "local smoothing / light cone (n=2)",
        [
            ("wavefront radius = t", f"{'OK' if radius_ok else 'FAIL'} for t in {times}"),
            ("cone half-angle (|x|=t)", f"{half_angle:.1f} deg  (want 45.0)"),
            ("s_p = (n-1)|1/2-1/p|, p=4", f"{s_p(2, 4):.4f}  (= 1/4)"),
            ("s_p, p=infinity", f"{s_p(2, math.inf):.4f}  (= 1/2)"),
        ],
    )


if __name__ == "__main__":
    main()
