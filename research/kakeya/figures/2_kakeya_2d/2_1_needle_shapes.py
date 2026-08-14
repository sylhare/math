"""Three classic Kakeya shapes and their areas (kakeya.md 2a-2c).

  disc      r = 1/2                         A = pi r^2      = pi/4   ~ 0.7854
  deltoid   x=2b cos t + b cos 2t, y=2b sin t - b sin 2t, b=1/4,
            tangent chord = 4b = 1          A = 2 pi b^2    = pi/8   ~ 0.3927  (= half the disc)
  triangle  equilateral of height 1         A = 1/sqrt3            ~ 0.5774  (Pal's convex minimum)

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/needle_shapes.py
"""
import math

import numpy as np
from _shared import COLORS, SQRT3, circle, deltoid, math_check, new_axes, poly, save_preview, unit_needle
from shapely.geometry import LineString


def deltoid_needle(b, t, n=1200):
    """Endpoints of the unit needle = tangent chord of the deltoid at parameter t (length 4b)."""
    for _ in range(5):  # cusps (t = 0, 2pi/3, 4pi/3) have zero velocity; nudge off them
        d = np.array([-2 * b * math.sin(t) - 2 * b * math.sin(2 * t), 2 * b * math.cos(t) - 2 * b * math.cos(2 * t)])
        if np.linalg.norm(d) > 1e-4:
            break
        t += 1e-2
    p = np.array([2 * b * math.cos(t) + b * math.cos(2 * t), 2 * b * math.sin(t) - b * math.sin(2 * t)])
    d = d / np.linalg.norm(d)
    line = LineString([tuple(p - 2 * d), tuple(p + 2 * d)])
    inter = poly(deltoid(b, n)).boundary.intersection(line)
    pts = [np.array(g.coords[0]) for g in getattr(inter, "geoms", [inter]) if g.geom_type == "Point"]
    if len(pts) < 2:
        return p, p
    proj = [float(np.dot(q - p, d)) for q in pts]
    return pts[int(np.argmin(proj))], pts[int(np.argmax(proj))]


def main():
    disc = poly(circle(0.5, 400))
    delt = poly(deltoid(0.25, 1200))
    h = 1.0
    tri = poly(np.array([[-1 / SQRT3, 0.0], [1 / SQRT3, 0.0], [0.0, h]]))  # equilateral, height 1

    chords = [np.linalg.norm(np.subtract(*deltoid_needle(0.25, t))) for t in np.linspace(0.2, math.pi, 7)]
    math_check(
        "classic Kakeya shapes",
        [
            ("disc area  pi/4", f"{disc.area:.4f}  (exact {math.pi/4:.4f})"),
            ("deltoid area  pi/8", f"{delt.area:.4f}  (exact {math.pi/8:.4f})"),
            ("deltoid = half disc?", f"{delt.area/disc.area:.3f}  (want 0.5)"),
            ("deltoid tangent chord", f"mean {np.mean(chords):.3f} (want 1.000, = 4b)"),
            ("triangle area  1/sqrt3", f"{tri.area:.4f}  (exact {1/SQRT3:.4f})"),
        ],
    )

    fig, ax = new_axes(3, figsize=(15, 5.2))
    # disc: unit needles through the centre (length 1 spans the diameter)
    ax[0].fill(*disc.exterior.xy, color=COLORS["region"], alpha=0.6)
    for a in np.linspace(0, math.pi, 12, endpoint=False):
        n = unit_needle(0, 0, a, 1.0)
        ax[0].plot(n[:, 0], n[:, 1], color=COLORS["needle"], lw=0.8, alpha=0.8)
    ax[0].set_title(f"disc  A = pi/4 = {disc.area:.3f}")
    # deltoid: unit tangent-chord needles
    ax[1].fill(*delt.exterior.xy, color=COLORS["region"], alpha=0.6)
    for t in np.linspace(0, 2 * math.pi, 24, endpoint=False):
        p, q = deltoid_needle(0.25, t)
        ax[1].plot([p[0], q[0]], [p[1], q[1]], color=COLORS["needle"], lw=0.7, alpha=0.8)
    ax[1].set_title(f"deltoid  A = pi/8 = {delt.area:.3f}  (half)")
    # triangle: unit needles that actually lie inside (altitude + the two edge directions)
    ax[2].fill(*tri.exterior.xy, color=COLORS["region"], alpha=0.6)
    bl, br, ap = np.array([-1 / SQRT3, 0.0]), np.array([1 / SQRT3, 0.0]), np.array([0.0, h])
    needles = [
        (np.array([0.0, 0.0]), np.array([0.0, 1.0])),                      # altitude, length 1
        (bl, bl + (ap - bl) / np.linalg.norm(ap - bl)),                    # unit along left edge
        (br, br + (ap - br) / np.linalg.norm(ap - br)),                    # unit along right edge
    ]
    for p, q in needles:
        ax[2].plot([p[0], q[0]], [p[1], q[1]], color=COLORS["needle"], lw=1.0, alpha=0.9)
    ax[2].set_title(f"equilateral (height 1)  A = 1/sqrt3 = {tri.area:.3f}")
    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
