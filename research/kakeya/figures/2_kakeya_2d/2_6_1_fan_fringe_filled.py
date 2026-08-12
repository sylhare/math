"""Kakeya needle set (Wikipedia KakeyaNeedleSet3.GIF look-alike), fan+fringe silhouette.

Solid equilateral core (apex up); at each of the 3 corners a ~120-degree fan of feathered-length
needles; plus outward-normal needles along each edge. Union of core + all needles, filled as a
single yellow silhouette (one outline, no internal edges).

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/2_kakeya_2d/2_6_1_fan_fringe_filled.py
"""
import math

import numpy as np
from _shared import math_check, save_preview
from shapely.geometry import Polygon
from shapely.ops import unary_union

SIDE = 1.0
R = SIDE / math.sqrt(3.0)          # circumradius; corners sit at distance R from centroid
CORNERS_DEG = (90.0, 210.0, 330.0)  # apex up, three-fold symmetric
HALFW = 0.007                       # needle half-width (thin, so tips separate into ragged spikes)
LEN_CORNER, LEN_EDGE = 0.90, 0.24   # nominal needle lengths (relative units)
J_CORNER, K_EDGE = 110, 52          # needles per corner fan / per edge
FAN_HALF = 60.0                     # corner fan half-angle in degrees (120 deg -> full turn x3)
BASE_SPREAD = 0.06                  # how far corner-fan bases slide down the two edges
CORE_ROUND = 0.09                   # buffer radius that rounds/fattens the core silhouette
YELLOW = "#f4e37a"

VERTS = np.array([R * np.array([math.cos(math.radians(d)), math.sin(math.radians(d))]) for d in CORNERS_DEG])


def _unit(deg):
    return np.array([math.cos(math.radians(deg)), math.sin(math.radians(deg))])


def _sliver(base, direction, length):
    """A thin quad (needle) of given length and half-width HALFW from `base` along `direction`."""
    d = direction / np.linalg.norm(direction)
    perp = np.array([-d[1], d[0]]) * HALFW
    tip = base + length * d
    return Polygon([base - perp, base + perp, tip + perp, tip - perp])


def build():
    """Core triangle plus the corner fans and edge fringe (feathered lengths)."""
    rng = np.random.default_rng(11)
    cen = VERTS.mean(0)
    core = Polygon([tuple(v) for v in VERTS]).buffer(CORE_ROUND, join_style=1)
    needles = []

    # Corner fans: ~110-degree spray outward from each vertex. The bases slide down the two
    # adjacent edges (proportional to the angular offset) so the lobe has a wide base and merges
    # seamlessly with the core instead of pinching to a point at the vertex.
    for i, d0 in enumerate(CORNERS_DEG):
        v = VERTS[i]
        left = VERTS[(i - 1) % 3]   # neighbour reached by the +offset half of the fan
        right = VERTS[(i + 1) % 3]  # neighbour reached by the -offset half
        for th in np.linspace(d0 - FAN_HALF, d0 + FAN_HALF, J_CORNER):
            off = (th - d0) / FAN_HALF                      # -1 .. +1 across the fan
            nb = left if off >= 0 else right
            base = v + BASE_SPREAD * abs(off) * (nb - v)    # base slides onto the edge
            taper = max(0.0, math.cos(math.radians((th - d0) * 1.35))) ** 1.4  # centre longest, sides short
            ragged = 0.45 + 0.75 * rng.random() ** 1.6       # a few needles reach far -> spiky halo
            length = LEN_CORNER * (0.18 + 0.82 * taper) * ragged
            needles.append(_sliver(base, _unit(th), length))

    # Edge fringe: outward-normal needles along each side, longest near the two corners so the
    # fuzz reaches up into the corner lobes (feathered, parabolic in position).
    for a, b in ((VERTS[0], VERTS[1]), (VERTS[1], VERTS[2]), (VERTS[2], VERTS[0])):
        nrm = np.array([(b - a)[1], -(b - a)[0]])
        nrm = nrm / np.linalg.norm(nrm)
        if np.dot(nrm, (a + b) / 2 - cen) < 0:
            nrm = -nrm
        for t in np.linspace(0.06, 0.94, K_EDGE):
            length = LEN_EDGE * (0.55 + 0.85 * rng.random())  # short ragged fuzz along the edge
            needles.append(_sliver(a + t * (b - a), nrm, length))

    return core, needles


def _fill(ax, geom, fc):
    """Fill a (Multi)Polygon as a single silhouette: one outline per component, no internal edges."""
    geoms = geom.geoms if geom.geom_type == "MultiPolygon" else [geom]
    for g in geoms:
        if not g.is_empty:
            ax.fill(*g.exterior.xy, facecolor=fc, edgecolor="none", zorder=2)


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    core, needles = build()
    silhouette = unary_union([core, *needles])

    math_check(
        "Kakeya needle set (fan + fringe, filled silhouette)",
        [
            ("shape", "solid triangle + 3 corner fans + edge fringe, one yellow outline"),
            ("coverage", "the three ~120-degree fans tile the full turn: a needle in every direction"),
            ("symmetry", "three-fold (identical corner + edge treatment)"),
            ("silhouette area", f"{silhouette.area:.3f} (core {core.area:.3f})"),
        ],
    )

    pts = np.array(silhouette.envelope.exterior.coords)
    (x0, y0), (x1, y1) = pts.min(0), pts.max(0)
    m = 0.06 * max(x1 - x0, y1 - y0)

    fig, ax = plt.subplots(figsize=(6.6, 6.6))
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(x0 - m, x1 + m)
    ax.set_ylim(y0 - m, y1 + m)
    _fill(ax, silhouette, YELLOW)

    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
