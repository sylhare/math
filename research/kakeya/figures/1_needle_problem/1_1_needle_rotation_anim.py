"""Animation: a unit needle turning through every direction.

  * disc   - needle pivots about its midpoint, sweeps the disc of radius 1/2 (area pi/4);
  * deltoid- needle stays a tangent chord of the three-cusped hypocycloid (chord 4b=1), sweeps pi/8.

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/needle_rotation_anim.py
"""
import math

import numpy as np
from _shared import COLORS, circle, deltoid, math_check, new_axes, poly, save_gif
from matplotlib.animation import FuncAnimation
from shapely.geometry import LineString

B = 0.25
FRAMES = 72


def disc_needle(theta):
    d = np.array([math.cos(theta), math.sin(theta)])
    return -0.5 * d, 0.5 * d  # length 1, midpoint at origin


def deltoid_needle(t):
    for _ in range(5):  # nudge off cusps (zero velocity there)
        d = np.array([-2 * B * math.sin(t) - 2 * B * math.sin(2 * t), 2 * B * math.cos(t) - 2 * B * math.cos(2 * t)])
        if np.linalg.norm(d) > 1e-4:
            break
        t += 1e-2
    p = np.array([2 * B * math.cos(t) + B * math.cos(2 * t), 2 * B * math.sin(t) - B * math.sin(2 * t)])
    d = d / np.linalg.norm(d)
    line = LineString([tuple(p - 2 * d), tuple(p + 2 * d)])
    inter = poly(deltoid(B, 900)).boundary.intersection(line)
    pts = [np.array(g.coords[0]) for g in getattr(inter, "geoms", [inter]) if g.geom_type == "Point"]
    if len(pts) < 2:
        return p, p
    proj = [float(np.dot(q - p, d)) for q in pts]
    return pts[int(np.argmin(proj))], pts[int(np.argmax(proj))]


def main():
    thetas = np.linspace(0, 2 * math.pi, FRAMES, endpoint=False)
    disc_pos = [disc_needle(t) for t in thetas]
    delt_pos = [deltoid_needle(t) for t in thetas]

    lengths = [np.linalg.norm(b - a) for a, b in disc_pos] + [np.linalg.norm(b - a) for a, b in delt_pos]
    math_check(
        "rotating needle",
        [
            ("needle length (all frames)", f"min {min(lengths):.4f}  max {max(lengths):.4f}  (want 1.0000)"),
            ("disc swept area", f"pi/4 = {math.pi/4:.4f}"),
            ("deltoid swept area", f"pi/8 = {math.pi/8:.4f}  (half)"),
            ("directions covered", "full turn: every orientation in [0,180)"),
        ],
    )

    fig, ax = new_axes(2, figsize=(11, 5.6))
    ax[0].plot(*circle(0.5, 200).T, color=COLORS["muted"], lw=1)
    ax[0].set_xlim(-0.62, 0.62); ax[0].set_ylim(-0.62, 0.62)
    ax[0].set_title("disc: pivot about the midpoint")
    dl = poly(deltoid(B, 400))
    ax[1].plot(*np.array(dl.exterior.coords).T, color=COLORS["muted"], lw=1)
    ax[1].set_xlim(-0.8, 0.55); ax[1].set_ylim(-0.7, 0.7)
    ax[1].set_title("deltoid: needle stays a tangent chord")

    trails0, trails1 = [], []
    live0, = ax[0].plot([], [], color=COLORS["needle"], lw=2.2)
    live1, = ax[1].plot([], [], color=COLORS["needle"], lw=2.2)

    def update(i):
        a0, b0 = disc_pos[i]
        a1, b1 = delt_pos[i]
        t0, = ax[0].plot([a0[0], b0[0]], [a0[1], b0[1]], color=COLORS["needle"], lw=0.6, alpha=0.18)
        t1, = ax[1].plot([a1[0], b1[0]], [a1[1], b1[1]], color=COLORS["needle"], lw=0.6, alpha=0.18)
        trails0.append(t0); trails1.append(t1)
        live0.set_data([a0[0], b0[0]], [a0[1], b0[1]])
        live1.set_data([a1[0], b1[0]], [a1[1], b1[1]])
        return live0, live1, t0, t1

    anim = FuncAnimation(fig, update, frames=FRAMES, interval=60, blit=False)
    print("wrote", save_gif(anim, fps=18, dpi=95))


if __name__ == "__main__":
    main()
