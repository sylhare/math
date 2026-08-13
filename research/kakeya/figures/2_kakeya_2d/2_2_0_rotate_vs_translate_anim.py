"""Animation: only rotation costs area; sliding a needle along its length is free (kakeya.md 2d).

The insight every area-shrinking trick rests on (Accromath, UQAM): "les glissements lineaires de
l'aiguille utilisent des regions d'aires nulles. Ce ne sont que les rotations de l'aiguille qui
necessitent des regions d'aires non nulles."

One needle, one panel, two moves in sequence:
  1. ROTATE about an endpoint through theta: it sweeps a circular sector of area theta/2 (grows).
  2. SLIDE the needle along its own axis: it stays on the line it already swept, so NO new area.

Run: PYTHONPATH=research/kakeya/figures uv run --with matplotlib --with shapely --with pillow \
     python research/kakeya/figures/2_kakeya_2d/2_2_0_rotate_vs_translate_anim.py
"""

import math

import numpy as np
from _shared import COLORS, math_check, poly, save_gif

THETA_MAX = math.pi / 3.0  # rotate through 60 deg
SLIDE_MAX = 0.9  # slide distance along the needle axis
N_ROT, N_SLIDE = 22, 18
HOLD, MID_HOLD, END_HOLD = 5, 5, 9


def sector(theta, r=1.0, n=64):
    """Sector polygon: pivot at origin, radius r, angles 0..theta (area r^2 theta / 2)."""
    if theta <= 1e-9:
        return None
    a = np.linspace(0.0, theta, n)
    return poly(np.array([(0.0, 0.0), *[(r * math.cos(t), r * math.sin(t)) for t in a]]))


def main():
    # sector area == theta/2 (rotation cost); along-axis slide adds 0
    for th in (math.pi / 6, math.pi / 4, THETA_MAX):
        meas = sector(th).area
        assert abs(meas - th / 2) < 1e-3, "sector area must be theta/2"

    math_check(
        "rotate costs area (sector = theta/2); slide along axis is free (area 0)",
        [
            ("rotate 30 deg", f"area theta/2 = {math.pi / 6 / 2:.4f}"),
            ("rotate 60 deg", f"area theta/2 = {THETA_MAX / 2:.4f}  (pi/6)"),
            ("slide along the axis", "swept area unchanged (needle stays on its own line)"),
            ("principle", "position is nearly free; only direction (rotation) costs area"),
        ],
    )

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    u_final = np.array([math.cos(THETA_MAX), math.sin(THETA_MAX)])  # needle direction after rotating
    fig, ax = plt.subplots(figsize=(5.6, 6.0))
    ax.set_aspect("equal")
    ax.axis("off")

    # phases: 0 hold, 1 rotate (theta 0->max), 2 hold, 3 slide (s 0->max), 4 hold
    frames = ([("rot", 0.0)] * HOLD
              + [("rot", (i + 1) / N_ROT) for i in range(N_ROT)]
              + [("rot", 1.0)] * MID_HOLD
              + [("slide", (i + 1) / N_SLIDE) for i in range(N_SLIDE)]
              + [("slide", 1.0)] * END_HOLD)

    def draw_sector(theta):
        sec = sector(theta)
        if sec is not None:
            sx, sy = sec.exterior.xy
            ax.fill(sx, sy, facecolor=COLORS["accent"], edgecolor="none", alpha=0.35, zorder=1)

    def update(fi):
        kind, f = frames[fi]
        ax.cla()
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-0.25, 1.25)
        ax.set_ylim(-0.2, 2.0)

        if kind == "rot":
            theta = THETA_MAX * f
            draw_sector(theta)
            for t in np.linspace(0.0, theta, 7):  # faint fan of positions
                ax.plot([0, math.cos(t)], [0, math.sin(t)], color=COLORS["needle"], lw=0.7, alpha=0.3, zorder=2)
            tip = np.array([math.cos(theta), math.sin(theta)])
            ax.plot([0, tip[0]], [0, tip[1]], color=COLORS["needle"], lw=3.2, zorder=4)
            ax.plot(0, 0, "o", color=COLORS["guide"], ms=6, zorder=5)
            ax.set_title(f"ROTATE: swept area = theta/2 = {theta / 2:.3f}\n(turned {math.degrees(theta):.0f} deg)",
                         fontsize=12)
        else:  # slide the (already rotated) needle along its own axis
            draw_sector(THETA_MAX)
            s = SLIDE_MAX * f
            a = s * u_final
            b = (1.0 + s) * u_final
            ax.annotate("", xy=tuple(b), xytext=tuple(b - 0.4 * u_final),
                        arrowprops=dict(arrowstyle="->", color=COLORS["needle"], lw=1.6))
            ax.plot([a[0], b[0]], [a[1], b[1]], color=COLORS["needle"], lw=3.2, zorder=4)
            ax.plot(0, 0, "o", color=COLORS["guide"], ms=6, zorder=5)
            ax.set_title(f"SLIDE along the needle: swept area stays {THETA_MAX / 2:.3f}\n"
                         f"(moving along its own line adds nothing)", fontsize=12)
        return []

    anim = FuncAnimation(fig, update, frames=len(frames), interval=110, blit=False)
    print("wrote", save_gif(anim, fps=9, dpi=100))


if __name__ == "__main__":
    main()
