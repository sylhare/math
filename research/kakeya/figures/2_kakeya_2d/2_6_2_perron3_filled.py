"""Kakeya needle set: filled union of three Perron trees, with the tree's needle fringe.

Equilateral triangle, base [0,1] split into 2^N slivers sharing the apex; merged bottom-up by
sliding consecutive pairs so their bases overlap (fraction ALPHA). Three copies rotated 0/120/240
deg about the union centroid give a concave triangular core whose three tips span all 180 deg of
line-directions. From each tip a Perron-density fan of needles radiates (one tree's 60 deg fan
reflected to +/-180 deg), plus an edge fringe of outward-normal needles; together they carry a
needle in every direction. Single yellow fill, no borders.

Run: PYTHONPATH=research/kakeya/figures uv run --with matplotlib --with shapely --with pillow \
     python research/kakeya/figures/2_kakeya_2d/2_6_2_perron3_filled.py
"""
import math

import numpy as np
from _shared import math_check, save_preview
from shapely.affinity import rotate, translate
from shapely.geometry import Polygon
from shapely.ops import unary_union

N = 6                      # 2^N slivers in the base
ALPHA = 0.5                # base-overlap fraction per merge
H = math.sqrt(3) / 2.0     # apex height
APEX = (0.5, H)
YELLOW = "#f4e37a"
FAN_HALF = 58.0            # corner-fan half angle (deg)
HALFW = 0.0022             # needle half-width
BASE_SPREAD = 0.62         # how far fan bases slide down the two edges
K_EDGE = 34                # needles per edge fringe


def perron(n, alpha):
    """2^n apex-sharing slivers merged bottom-up; each pair slid so bases overlap by `alpha`."""
    w = 1.0 / 2 ** n
    shapes = [[Polygon([(i * w, 0.0), ((i + 1) * w, 0.0), APEX])] for i in range(2 ** n)]
    for _ in range(n):
        step = 0.5 * (1.0 - alpha) * w
        shapes = [[translate(p, xoff=+step) for p in a] + [translate(p, xoff=-step) for p in b]
                  for a, b in zip(shapes[::2], shapes[1::2], strict=True)]
        w *= (1.0 + alpha)
    return unary_union([p for grp in shapes for p in grp])


def fan_offsets(n):
    """2^n offsets in [-FAN_HALF, FAN_HALF] from the tree's base-midpoint -> apex fan (bunched at edges)."""
    xs = np.linspace(0.0, 1.0, 2 ** n + 1)
    dirs = np.degrees(np.arctan2(H, 0.5 - 0.5 * (xs[:-1] + xs[1:])))   # 60..120 deg, bunched
    return (dirs - 90.0) / 30.0 * FAN_HALF


def sliver(base, deg, length):
    d = np.array([math.cos(math.radians(deg)), math.sin(math.radians(deg))])
    perp = np.array([-d[1], d[0]]) * HALFW
    tip = base + length * d
    return Polygon([base - perp, base + perp, tip + perp, tip - perp])


def build():
    rng = np.random.default_rng(7)
    tree = perron(N, ALPHA)
    cen = np.array(tree.centroid.coords[0])
    core = unary_union([rotate(tree, a, origin=tuple(cen)) for a in (0, 120, 240)]).buffer(0.015)

    tips = [cen + (H - cen[1]) * np.array([math.cos(math.radians(d)), math.sin(math.radians(d))])
            for d in (90.0, 210.0, 330.0)]        # the three rotated apexes
    off = fan_offsets(N)
    needles = []
    for i, d0 in enumerate((90.0, 210.0, 330.0)):  # outward Perron fan at each tip
        tip = tips[i]
        for o in off:
            neigh = tips[(i - 1) % 3] if o >= 0 else tips[(i + 1) % 3]
            base = tip + BASE_SPREAD * abs(o) / FAN_HALF * (neigh - tip)  # base slides along the edge
            length = 0.62 * (0.55 + 0.45 * math.cos(math.radians(o))) * (0.82 + 0.3 * rng.random())
            needles.append(sliver(base, d0 + o, length))
    for a, b in ((tips[0], tips[1]), (tips[1], tips[2]), (tips[2], tips[0])):
        e = b - a
        nrm = np.array([e[1], -e[0]]) / np.linalg.norm(e)
        if np.dot(nrm, (a + b) / 2 - cen) < 0:
            nrm = -nrm
        base_deg = math.degrees(math.atan2(nrm[1], nrm[0]))
        for t in np.linspace(0.08, 0.92, K_EDGE):  # edge fringe, longest toward the tips
            length = 0.30 * (1.0 + 1.3 * (2 * t - 1) ** 2) * (0.75 + 0.4 * rng.random())
            needles.append(sliver(a + t * e, base_deg + 26.0 * (2 * t - 1), length))
    return unary_union([core, *needles]), core


def _fill(ax, geom):
    geoms = geom.geoms if geom.geom_type == "MultiPolygon" else [geom]
    for g in geoms:
        if not g.is_empty:
            ax.fill(*g.exterior.xy, facecolor=YELLOW, edgecolor="none", zorder=1)


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    full, core = build()

    math_check(
        "Kakeya needle set: filled union of 3 Perron trees",
        [
            ("tree", f"2^{N} = {2 ** N} apex-sharing slivers, bottom-up overlap alpha={ALPHA}"),
            ("core", f"3 copies rotated 0/120/240 deg about the centroid, area {core.area:.3f}"),
            ("fans", f"{2 * FAN_HALF:.0f} deg Perron fan at each of 3 tips (bunched at edges) + edge fringe"),
            ("coverage", "3 fans + fringe span the full turn: a needle in every direction"),
        ],
    )

    pts = np.array(full.envelope.exterior.coords)
    (x0, y0), (x1, y1) = pts.min(0), pts.max(0)
    m = 0.05 * max(x1 - x0, y1 - y0)

    fig, ax = plt.subplots(figsize=(6.6, 6.6))
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(x0 - m, x1 + m)
    ax.set_ylim(y0 - m, y1 + m)
    _fill(ax, full)

    print("wrote", save_preview(fig, dpi=160))


if __name__ == "__main__":
    main()
