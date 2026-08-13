"""Animation: only rotation costs area, sliding a needle along its own length is free (kakeya.md 2d).

The insight every area-shrinking trick rests on (Accromath, UQAM):
"les glissements lineaires de l'aiguille utilisent des regions d'aires nulles. Ce ne sont que les
rotations de l'aiguille qui necessitent des regions d'aires non nulles."

  LEFT  ROTATE: a unit needle pivoting about an endpoint through angle theta sweeps a circular sector
                of area theta/2 (grows with the angle turned).
  RIGHT SLIDE : sliding the needle ALONG its own axis sweeps only the line it lies on, area 0; sliding
                it ACROSS (perpendicular) by the same distance s would cost a 1 x s rectangle, area s.

So position is nearly free (translate along the needle) but direction is expensive (rotation). The
Pal detour (2_2) exploits exactly this: go far out cheaply, then the rotation you still need is tiny.

Run: PYTHONPATH=research/kakeya/figures uv run --with matplotlib --with shapely --with pillow \
     python research/kakeya/figures/2_kakeya_2d/2_2_0_rotate_vs_translate_anim.py
"""

import math

import numpy as np
from _shared import COLORS, math_check, poly, save_gif

THETA_MAX = math.pi / 3.0  # rotate through 60 deg
S_MAX = 1.2  # slide distance
N = 30  # animation steps
HOLD = 5
END_HOLD = 8
NY = 0.5  # needle y on the right panel


def sector(theta, r=1.0, n=60):
    """Circular sector polygon: pivot at origin, radius r, angles 0..theta (area r^2 theta / 2)."""
    if theta <= 1e-9:
        return None
    a = np.linspace(0.0, theta, n)
    pts = [(0.0, 0.0), *[(r * math.cos(t), r * math.sin(t)) for t in a]]
    return poly(np.array(pts))


def main():
    thetas = np.linspace(0.0, THETA_MAX, N)
    slides = np.linspace(0.0, S_MAX, N)

    # --- MATH: sector area = theta/2 (rotation cost) vs along-axis area 0, across-axis area s -------
    sample = [N // 4, N // 2, 3 * N // 4, N - 1]
    rows = []
    max_err = 0.0
    for k in sample:
        th = thetas[k]
        measured = sector(th).area
        formula = th / 2.0
        max_err = max(max_err, abs(measured - formula))
        rows.append((f"theta = {math.degrees(th):4.0f} deg", f"sector {measured:.4f}  vs theta/2 {formula:.4f}"))
    assert max_err < 1e-3, f"sector area must equal theta/2 (max err {max_err:.2e})"

    math_check(
        "rotate costs area (sector = theta/2), slide along axis is free (area 0)",
        [
            *rows,
            ("rotate, full 60 deg", f"area = theta/2 = {THETA_MAX / 2:.4f}  (pi/6)"),
            ("slide ALONG axis, any s", "swept area = 0   (the needle stays on its own line)"),
            ("slide ACROSS by s", f"swept area = 1 * s  (e.g. s = {S_MAX} -> {S_MAX:.2f})"),
            ("principle", "position is nearly free; only direction (rotation) costs area"),
        ],
    )

    # ---- figure -------------------------------------------------------------------------
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(11.5, 5.0))
    fig.suptitle("only rotation costs area; sliding along the needle is free", fontsize=13)
    for a in (axL, axR):
        a.set_aspect("equal")
        a.axis("off")

    frames = [0] * HOLD + list(range(N)) + [N - 1] * END_HOLD

    def update(fi):
        k = frames[fi]
        th, s = thetas[k], slides[k]

        # LEFT: rotate about an endpoint -> sector of area theta/2
        axL.cla()
        axL.set_aspect("equal")
        axL.axis("off")
        axL.set_xlim(-0.2, 1.15)
        axL.set_ylim(-0.15, 1.15)
        sec = sector(th)
        if sec is not None:
            sx, sy = sec.exterior.xy
            axL.fill(sx, sy, facecolor=COLORS["region"], edgecolor="none", alpha=0.6, zorder=1)
        for t in np.linspace(0.0, th, 9):  # the fan of needle positions
            axL.plot([0, math.cos(t)], [0, math.sin(t)], color=COLORS["needle"], lw=0.8, alpha=0.35, zorder=2)
        axL.plot([0, math.cos(th)], [0, math.sin(th)], color=COLORS["needle"], lw=3.0, zorder=3)  # current
        axL.plot(0, 0, "o", color=COLORS["guide"], ms=6, zorder=4)
        axL.set_title(f"ROTATE: swept area = theta/2 = {th / 2:.3f}\n(turned {math.degrees(th):.0f} deg)", fontsize=11)

        # RIGHT: slide along the axis (area 0); ghost of the perpendicular move (area s)
        axR.cla()
        axR.set_aspect("equal")
        axR.axis("off")
        axR.set_xlim(-0.25, 1.75)
        axR.set_ylim(NY - 0.35, NY + S_MAX + 0.35)
        # ghost: perpendicular move would sweep a 1 x s rectangle
        if s > 1e-6:
            axR.fill([0, 1, 1, 0], [NY, NY, NY + s, NY + s], facecolor=COLORS["muted"], edgecolor="none", alpha=0.25)
            axR.text(0.5, NY + s + 0.12, f"across: area = 1 x s = {s:.2f}", ha="center", va="bottom",
                     fontsize=9, color=COLORS["guide"])
        # along-axis slide: the needle at [s, s+1] on its own line (swept set is the line, area 0)
        axR.plot([0, S_MAX + 1], [NY, NY], color=COLORS["muted"], lw=0.8, alpha=0.5, zorder=1)  # its line
        axR.plot([s, s + 1.0], [NY, NY], color=COLORS["needle"], lw=3.0, zorder=3)  # current needle
        axR.annotate("", xy=(s + 1.0, NY), xytext=(s + 0.55, NY),
                     arrowprops=dict(arrowstyle="->", color=COLORS["needle"], lw=1.5))
        axR.set_title("SLIDE along the axis: swept area = 0\n(across would cost area = s)", fontsize=11)
        return []

    anim = FuncAnimation(fig, update, frames=len(frames), interval=140, blit=False)
    print("wrote", save_gif(anim, fps=8, dpi=95))


if __name__ == "__main__":
    main()
