"""Expanding wavefront and the space-time light cone (kakeya.md 5c-iii).

Point source of u(x, t) = e^{it sqrt(-Delta)} f spreads along the light cone |x| = t.
  (a) 2D: circular wavefront radius = t (unit speed), past slices faint.
  (b) 3D space-time: cone {(x, t) : |x| = t}, 45-degree half-angle (dr/dt = 1).

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/wavefront_cone_anim.py
"""
import math

import numpy as np
from _shared import COLORS, circle, math_check, save_gif
from matplotlib.animation import FuncAnimation

FRAMES = 90
T_MAX = 1.6
HOLD = 8  # frames held at the start and end


def s_p(n: int, p: float) -> float:
    """Sharp fixed-time Sobolev loss exponent s_p = (n-1) |1/2 - 1/p| (p = inf -> 1/p = 0)."""
    inv_p = 0.0 if math.isinf(p) else 1.0 / p
    return (n - 1) * abs(0.5 - inv_p)


def time_schedule() -> np.ndarray:
    up = np.linspace(0.0, T_MAX, FRAMES - 2 * HOLD)
    return np.concatenate([np.zeros(HOLD), up, np.full(HOLD, T_MAX)])


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (registers 3d projection)

    times = time_schedule()

    # Validation across every frame: measured wavefront radius == t (unit speed)
    max_radius_err = 0.0
    for t in times:
        c = circle(r=max(t, 1e-9), n=200)
        r_meas = float(np.mean(np.hypot(c[:, 0], c[:, 1])))
        max_radius_err = max(max_radius_err, abs(r_meas - max(t, 1e-9)))
    half_angle = math.degrees(math.atan2(1.0, 1.0))  # dr/dt = 1

    math_check(
        "wavefront + light cone (n=2):  |x| = t",
        [
            ("frames", f"{FRAMES}"),
            ("t range", f"{times.min():.3f} -> {times.max():.3f}"),
            ("wavefront radius == t (all frames)", f"max err {max_radius_err:.2e}  (< 1e-9 ok)"),
            ("cone half-angle (|x|=t)", f"{half_angle:.1f} deg  (want 45.0)"),
            ("s_p = (n-1)|1/2-1/p|, p=4", f"{s_p(2, 4):.4f}  (= 1/4)"),
            ("s_p, p=infinity", f"{s_p(2, math.inf):.4f}  (= 1/2)"),
        ],
    )
    assert max_radius_err < 1e-9 and abs(half_angle - 45.0) < 1e-9

    fig = plt.figure(figsize=(11, 5.4))

    # (a) 2D space: expanding wavefront, past slices faint
    ax = fig.add_subplot(1, 2, 1)
    ax.set_aspect("equal"); ax.axis("off")
    lim = T_MAX * 1.15
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
    ax.plot([0], [0], marker="*", ms=13, color=COLORS["accent"], zorder=5)
    ax.set_title("wavefront: radius = t")
    (live2d,) = ax.plot([], [], color=COLORS["outer"], lw=2.6, zorder=4)
    readout = ax.text(-lim * 0.95, lim * 0.86, "", fontsize=11, color=COLORS["outer"])

    # (b) 3D space-time cone building up
    ax3 = fig.add_subplot(1, 2, 2, projection="3d")
    ax3.set_xlabel("x_1"); ax3.set_ylabel("x_2"); ax3.set_zlabel("t")
    ax3.set_title("space-time light cone  |x| = t  (45 deg)")
    ax3.set_xlim(-T_MAX, T_MAX); ax3.set_ylim(-T_MAX, T_MAX); ax3.set_zlim(0, T_MAX)
    ax3.set_box_aspect((1, 1, 1))
    ax3.view_init(elev=18, azim=-60)
    ax3.scatter([0], [0], [0], color=COLORS["accent"], marker="*", s=90)

    trails2d, rings3d = [], []

    def update(i):
        t = times[i]
        c = circle(r=max(t, 1e-9), n=160)
        ring = np.vstack([c, c[:1]])
        # 2D live wavefront + a faint trail of the family
        live2d.set_data(ring[:, 0], ring[:, 1])
        if t > 1e-6:
            (tr,) = ax.plot(ring[:, 0], ring[:, 1], color=COLORS["needle"], lw=0.7, alpha=0.16)
            trails2d.append(tr)
        readout.set_text(f"t = {t:.2f}    |x| = {t:.2f}")
        # 3D: stack a ring at height t so the cone builds up
        if t > 1e-6:
            (r3,) = ax3.plot(ring[:, 0], ring[:, 1], zs=t, color=COLORS["outer"], lw=1.4, alpha=0.6)
            rings3d.append(r3)
        return live2d, readout

    anim = FuncAnimation(fig, update, frames=FRAMES, interval=60, blit=False)
    print("wrote", save_gif(anim, fps=18, dpi=95))


if __name__ == "__main__":
    main()
