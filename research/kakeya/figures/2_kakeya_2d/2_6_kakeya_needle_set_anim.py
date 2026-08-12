"""Kakeya needle set (Wikipedia image), built up by granularity (kakeya.md 2e).

A solid central triangle with Perron-tree branches at each corner and a needle fringe along the
edges: a Besicovitch set (a unit segment in every direction) drawn as the FILLED SILHOUETTE of its
needle family (union of core + needles, one outline). Granularity rises coarse -> dense. The area
shrinking is the companion animation 2_7.

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/2_kakeya_2d/2_6_kakeya_needle_set_anim.py
"""
import math

import numpy as np
from _shared import COLORS, math_check, save_gif
from shapely.geometry import Polygon
from shapely.ops import unary_union

SIDE = 1.0
R = SIDE / math.sqrt(3.0)
CORNERS_DEG = (90.0, 210.0, 330.0)
HALFW = 0.012                  # needle half-width (wider so the union reads as filled branches)
LEN_CORNER, LEN_EDGE = 0.62, 0.30
KF, JF = 28, 62                # finest needle counts per edge / per corner fan
CORE = "#f4ec7a"
EDGE = "#8a8a3a"

# (edge, corner) needle counts per frame, coarse -> fine, then hold on the full set
LEVELS = [(2, 6), (3, 9), (4, 13), (6, 18), (9, 26), (13, 35), (18, 46), (28, 62)]

VERTS = np.array([R * np.array([math.cos(math.radians(d)), math.sin(math.radians(d))]) for d in CORNERS_DEG])


def _unit(deg):
    return np.array([math.cos(math.radians(deg)), math.sin(math.radians(deg))])


def _sliver(base, direction, length):
    d = direction / np.linalg.norm(direction)
    perp = np.array([-d[1], d[0]]) * HALFW
    tip = base + length * d
    return Polygon([base - perp, base + perp, tip + perp, tip - perp])


def build_fine():
    rng = np.random.default_rng(7)
    cen = VERTS.mean(0)
    edge_needles, corner_needles = [], []
    for a, b in ((VERTS[0], VERTS[1]), (VERTS[1], VERTS[2]), (VERTS[2], VERTS[0])):
        nrm = np.array([(b - a)[1], -(b - a)[0]]); nrm = nrm / np.linalg.norm(nrm)
        if np.dot(nrm, (a + b) / 2 - cen) < 0:
            nrm = -nrm
        for t in np.linspace(0.06, 0.94, KF):
            edge_needles.append(_sliver(a + t * (b - a), nrm, LEN_EDGE * (0.75 + 0.5 * rng.random())))
    for d0 in CORNERS_DEG:
        v = R * _unit(d0)
        for th in np.linspace(d0 - 60, d0 + 60, JF):
            corner_needles.append(_sliver(v, _unit(th), LEN_CORNER * (0.72 + 0.5 * rng.random())))
    return edge_needles, corner_needles


def _subset(items, k):
    if k >= len(items):
        return items
    return [items[i] for i in np.unique(np.linspace(0, len(items) - 1, k).round().astype(int))]


def _fill(ax, geom, fc, ec, lw, z=2):
    """Fill a (Multi)Polygon as a single silhouette (one outline per component, no internal edges)."""
    geoms = geom.geoms if geom.geom_type == "MultiPolygon" else [geom]
    arts = []
    for g in geoms:
        if g.is_empty:
            continue
        a, = ax.fill(*g.exterior.xy, facecolor=fc, edgecolor=ec, linewidth=lw, zorder=z)
        arts.append(a)
    return arts


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    edge_fine, corner_fine = build_fine()
    core_tri = Polygon([tuple(v) for v in VERTS])
    fringe_all = unary_union([core_tri, *edge_fine, *corner_fine])

    frames = LEVELS + [LEVELS[-1]] * 4

    math_check(
        "Kakeya needle set (Wikipedia image, built by granularity)",
        [
            ("shape", "solid triangle + corner Perron-tree branches + edge fringe (filled silhouette)"),
            ("coverage", "the three corner fans tile the full turn: a needle in every direction"),
            ("granularity", f"edge {LEVELS[0][0]}->{KF}, corner {LEVELS[0][1]}->{JF} per side"),
            ("area shrinking", "companion animation 2_7 (Perron cut-and-shift)"),
        ],
    )

    pts = np.array(fringe_all.envelope.exterior.coords)
    (x0, y0), (x1, y1) = pts.min(0), pts.max(0)
    m = 0.08 * max(x1 - x0, y1 - y0)

    fig, ax = plt.subplots(figsize=(6.6, 6.6))
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(x0 - m, x1 + m); ax.set_ylim(y0 - m, y1 + m)
    ax.set_title("Kakeya needle set: a solid triangle with Perron-tree branches", fontsize=10)
    counter = ax.text(0.02, 0.98, "", transform=ax.transAxes, va="top", fontsize=10, color=COLORS["guide"])
    holder = {"arts": []}

    def update(i):
        for a in holder["arts"]:
            a.remove()
        ke, kc = frames[i]
        shape = unary_union([core_tri, *_subset(edge_fine, ke * 3), *_subset(corner_fine, kc * 3)])
        holder["arts"] = _fill(ax, shape, CORE, "none", 0.0, z=2)
        counter.set_text(f"granularity: {ke} edge + {kc} corner needles per side")
        return holder["arts"] + [counter]

    anim = FuncAnimation(fig, update, frames=len(frames), interval=320, blit=False)
    print("wrote", save_gif(anim, fps=3, dpi=105))


if __name__ == "__main__":
    main()
