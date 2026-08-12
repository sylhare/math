"""Besicovitch set by exact cut-and-slide of thin needles (Wikipedia KakeyaNeedleSet look-alike).

Each direction over the full turn carries one unit needle, drawn as a thin 1 x delta trapezoid
(length 1, angular width delta). The turn splits into three 120-degree fans, one per corner of an
apex-up equilateral triangle; every needle in a fan is slid so its base sits on the shared corner
apex (the maximal Perron slide), so bases overlap and the union footprint collapses onto the core.
Three fans of 120 degrees tile 360 degrees: a needle in every direction. Union filled in one yellow.

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/2_kakeya_2d/2_6_8_besicovitch_compression.py
"""
import math

import numpy as np
from _shared import math_check, save_preview
from shapely.geometry import Polygon
from shapely.ops import unary_union

SIDE = 1.0
R = SIDE / math.sqrt(3.0)              # circumradius: corners at distance R from the centroid
CORNERS_DEG = (90.0, 210.0, 330.0)    # apex up, three-fold symmetric
VERTS = np.array([R * np.array([math.cos(math.radians(d)), math.sin(math.radians(d))]) for d in CORNERS_DEG])

FAN_HALF = 75.0                       # half-opening of each corner fan (150 deg; fans overlap into a sunburst)
M = 58                                # needles per fan (delta-separated directions)
LEN = 1.0                             # needle length (unit)
DUTY = 0.36                           # drawn angular width / delta spacing (gaps -> visible rays)
K_EDGE = 22                           # short outward-normal needles per edge (fringe)
LEN_EDGE = 0.34
YELLOW = "#f4e37a"


def _unit(deg):
    return np.array([math.cos(math.radians(deg)), math.sin(math.radians(deg))])


def _trapezoid(apex, deg, r0, length, half_ang):
    """Thin 1 x delta trapezoid: from radius r0 to r0+length along `deg`, subtending 2*half_ang at apex."""
    d = _unit(deg)
    p = np.array([-d[1], d[0]])
    b, t = apex + r0 * d, apex + (r0 + length) * d
    wb, wt = max(r0, 1e-3) * math.sin(half_ang), (r0 + length) * math.sin(half_ang)
    return Polygon([b - p * wb, b + p * wb, t + p * wt, t - p * wt])


def build():
    """Three corner fans (bases slid onto the shared apex) plus a short edge fringe."""
    delta = math.radians(2.0 * FAN_HALF / M)          # angular spacing between needles in a fan
    half_ang = 0.5 * DUTY * delta                     # drawn half-width -> gaps between rays
    needles = []
    for i, radial in enumerate(CORNERS_DEG):          # outward radial direction at each corner
        apex = VERTS[i]
        for th in np.linspace(radial - FAN_HALF, radial + FAN_HALF, M):
            needles.append(_trapezoid(apex, th, 0.0, LEN, half_ang))
    for a, b in ((VERTS[0], VERTS[1]), (VERTS[1], VERTS[2]), (VERTS[2], VERTS[0])):
        nrm = np.array([(b - a)[1], -(b - a)[0]])
        nrm = nrm / np.linalg.norm(nrm)
        if np.dot(nrm, (a + b) / 2.0) < 0:            # point outward (away from centroid at origin)
            nrm = -nrm
        deg = math.degrees(math.atan2(nrm[1], nrm[0]))
        for s in np.linspace(0.12, 0.88, K_EDGE):
            grow = 0.5 + 1.4 * (2.0 * s - 1.0) ** 2   # longer toward the corners
            needles.append(_trapezoid(a + s * (b - a), deg, 0.0, LEN_EDGE * grow, half_ang))
    return needles


def _fill(ax, geom, fc):
    for g in (geom.geoms if geom.geom_type == "MultiPolygon" else [geom]):
        if not g.is_empty:
            ax.fill(*g.exterior.xy, facecolor=fc, edgecolor="none", zorder=2)


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    needles = build()
    core = Polygon([tuple(v) for v in VERTS])
    silhouette = unary_union([core, *needles])

    dirs = np.sort(np.concatenate([                    # directions carried by the three corner fans
        (np.linspace(r - FAN_HALF, r + FAN_HALF, M) % 360.0) for r in CORNERS_DEG]))
    max_gap = float(np.max(np.diff(np.append(dirs, dirs[0] + 360.0))))

    math_check(
        "Besicovitch set by cut-and-slide compression (method 8)",
        [
            ("corners", "3, apex-up equilateral, side 1"),
            ("needles", f"{len(needles)} thin 1 x delta trapezoids (unit length)"),
            ("coverage", f"3 overlapping fans x {2 * FAN_HALF:.0f} deg cover 360 deg; max direction gap {max_gap:.1f} deg"),
            ("slide", "each base translated onto the shared corner apex; translation preserves directions"),
            ("silhouette area", f"{silhouette.area:.3f} (core {core.area:.3f})"),
        ],
    )

    pts = np.array(silhouette.envelope.exterior.coords)
    (x0, y0), (x1, y1) = pts.min(0), pts.max(0)
    m = 0.05 * max(x1 - x0, y1 - y0)

    fig, ax = plt.subplots(figsize=(6.6, 6.4))
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(x0 - m, x1 + m)
    ax.set_ylim(y0 - m, y1 + m)
    _fill(ax, silhouette, YELLOW)
    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
