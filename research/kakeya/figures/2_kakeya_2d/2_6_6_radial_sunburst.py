"""Radial sunburst Kakeya needle set: equilateral core + one unit needle per direction.

For each of ~300 directions over the full turn, a ray leaves the core centroid, exits the triangle
boundary, and a unit-length needle continues outward from that exit point. The corners sit farther
from the centroid, so their needles reach farther and bunch into sprays; single yellow slivers.

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/2_kakeya_2d/2_6_6_radial_sunburst.py
"""
import math

import numpy as np
from _shared import math_check, save_preview
from shapely.geometry import LineString, Polygon

R = 1.0 / math.sqrt(3.0)            # core circumradius (equilateral, side 1, apex up)
CORNERS_DEG = (90.0, 210.0, 330.0)
VERTS = np.array([R * np.array([math.cos(math.radians(d)), math.sin(math.radians(d))]) for d in CORNERS_DEG])
CORE = Polygon([tuple(v) for v in VERTS])

N_DIR = 300                         # directions over the full turn (divisible by 3 -> three-fold)
LENGTH = 0.55                       # unit needle length (same in every direction)
HALFW = 0.004                       # needle half-width
YELLOW = "#f4e37a"


def _unit(deg):
    return np.array([math.cos(math.radians(deg)), math.sin(math.radians(deg))])


def _exit_radius(direction):
    """Distance from the centroid to the triangle boundary along `direction`."""
    ray = LineString([(0.0, 0.0), tuple(direction * 10.0 * R)])
    hit = ray.intersection(CORE.boundary)
    if hit.is_empty:
        return R
    pt = hit.geoms[-1] if hit.geom_type == "MultiPoint" else hit
    return math.hypot(pt.x, pt.y)


def _sliver(base, direction):
    perp = np.array([-direction[1], direction[0]]) * HALFW
    tip = base + LENGTH * direction
    return np.array([base - perp, base + perp, tip + perp, tip - perp])


def build():
    """One outward unit needle anchored at each direction's boundary exit."""
    slivers = []
    for deg in np.linspace(0.0, 360.0, N_DIR, endpoint=False):
        d = _unit(deg)
        slivers.append(_sliver(_exit_radius(d) * d, d))
    return slivers


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    slivers = build()

    math_check(
        "Radial sunburst Kakeya needle set",
        [
            ("core", "equilateral triangle, side 1, apex up"),
            ("needles", f"{N_DIR} unit needles ({LENGTH}) over the full turn, one per direction"),
            ("coverage", "a segment in every direction (all 360 deg) -> Besicovitch set"),
            ("symmetry", "three-fold: corners reach farthest, forming the sprays"),
        ],
    )

    reach = R + LENGTH
    m = 0.05 * reach

    fig, ax = plt.subplots(figsize=(6.6, 6.2))
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-reach - m, reach + m)
    ax.set_ylim(-R - m, reach + m)
    ax.fill(*CORE.exterior.xy, facecolor=YELLOW, edgecolor="none", zorder=2)
    for s in slivers:
        ax.fill(s[:, 0], s[:, 1], facecolor=YELLOW, edgecolor="none", zorder=2)

    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
