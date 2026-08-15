"""Radial Kakeya needle set: a small triangular core with a unit needle in every direction.

For each of ~300 directions over the full turn, a ray leaves the core centre, exits the triangle
boundary, and a fixed needle continues outward from that exit point. The filled union silhouette
(core + all needles) is a Besicovitch set drawn in one colour, three-fold symmetric.

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/2_kakeya_2d/2_6_6_radial_needle_set.py
"""
import math

import numpy as np
from _shared import math_check, save_preview
from shapely.geometry import LineString, Polygon
from shapely.ops import unary_union

R = 1.0 / math.sqrt(3.0)          # core circumradius (equilateral, side 1)
CORNERS_DEG = (90.0, 210.0, 330.0)
VERTS = np.array([R * np.array([math.cos(math.radians(d)), math.sin(math.radians(d))]) for d in CORNERS_DEG])

N_DIR = 480                       # directions over the full turn (divisible by 3 -> three-fold symmetric)
HALFW = 0.005                     # needle half-width
L_MIN, L_MAX = 0.16, 0.74         # needle length: short off the edges, long off the corners
INRAD = R / 2.0                   # inradius (exit radius at an edge midpoint)
FILL = "#f4e37a"


def _unit(deg):
    return np.array([math.cos(math.radians(deg)), math.sin(math.radians(deg))])


def _exit_radius(direction):
    """Distance from the centroid to the triangle boundary along `direction`."""
    ray = LineString([(0.0, 0.0), tuple(direction * 10.0 * R)])
    hit = ray.intersection(Polygon([tuple(v) for v in VERTS]).boundary)
    if hit.is_empty:
        return R
    pt = hit.geoms[-1] if hit.geom_type == "MultiPoint" else hit
    return math.hypot(pt.x, pt.y)


def _sliver(base, direction, length):
    perp = np.array([-direction[1], direction[0]]) * HALFW
    tip = base + length * direction
    return Polygon([base - perp, base + perp, tip + perp, tip - perp])


def build():
    """Core triangle plus one outward needle per direction; jitter tiles per 120 deg to stay symmetric."""
    rng = np.random.default_rng(4)
    per_sector = N_DIR // 3
    jitter = 0.70 + 0.55 * rng.random(per_sector)         # length jitter for one sector
    jitter = np.tile(jitter, 3)                           # repeat -> three-fold symmetric fray
    needles = []
    for k, deg in enumerate(np.linspace(0.0, 360.0, N_DIR, endpoint=False)):
        d = _unit(deg)
        r = _exit_radius(d)
        # corner-proximity in [0,1]: 0 at an edge midpoint, 1 at a corner
        prox = np.clip((r - INRAD) / (R - INRAD), 0.0, 1.0)
        length = (L_MIN + (L_MAX - L_MIN) * prox) * jitter[k]
        needles.append(_sliver(r * d, d, length))
    return needles


def _fill(ax, geom, fc, z=2):
    geoms = geom.geoms if geom.geom_type == "MultiPolygon" else [geom]
    for g in geoms:
        if not g.is_empty:
            ax.fill(*g.exterior.xy, facecolor=fc, edgecolor="none", zorder=z)


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    needles = build()
    core = Polygon([tuple(v) for v in VERTS])
    shape = unary_union([core, *needles])

    math_check(
        "Radial Kakeya needle set (method 6: exit-point needles)",
        [
            ("core", "equilateral triangle, side 1, apex up"),
            ("directions", f"{N_DIR} needles over the full turn (a unit segment in every direction)"),
            ("coverage", "each needle anchored where its centre-ray exits the boundary"),
            ("symmetry", "length jitter tiled per 120 deg -> three-fold symmetric"),
        ],
    )

    pts = np.array(shape.envelope.exterior.coords)
    (x0, y0), (x1, y1) = pts.min(0), pts.max(0)
    m = 0.05 * max(x1 - x0, y1 - y0)

    fig, ax = plt.subplots(figsize=(6.6, 6.0))
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(x0 - m, x1 + m)
    ax.set_ylim(y0 - m, y1 + m)
    _fill(ax, shape, FILL)
    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
