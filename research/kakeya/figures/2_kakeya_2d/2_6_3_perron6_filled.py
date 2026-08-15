"""Kakeya needle set as a filled Perron-tree silhouette (reproduces Wikimedia KakeyaNeedleSet3.GIF).

A wide-apex Perron tree (the base of an isosceles triangle split into 2^n slivers joined to a shared
apex, then sprouted by overlapping consecutive pairs bottom-up) is planted apex-first at each corner of
a solid equilateral core and rotated 0/120/240 deg about the centroid. Each tree carries a ~150 deg fan
of needle directions, so the three cover the whole turn; a short outward fringe along the edges
completes the halo. Everything is unioned and filled as one silhouette: single colour, no border.

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/2_kakeya_2d/2_6_3_perron6_filled.py
"""
import math

import numpy as np
from _shared import math_check, new_axes, save_preview
from shapely.affinity import rotate as shp_rotate
from shapely.affinity import scale as shp_scale
from shapely.affinity import translate as shp_translate
from shapely.geometry import Polygon
from shapely.ops import unary_union

YELLOW = "#f4e37a"                 # single fill colour (edgecolor "none" everywhere)
N = 7                              # 2^N slivers per Perron tree
ALPHA = 0.5                        # sprout overlap fraction (bottom-up)
B, HT = 1.5, 0.42                  # tree base half-width / height -> apex fan 2*atan(B/HT) ~ 149 deg
R = 0.6                            # circumradius of the equilateral core
CORNERS_DEG = (90.0, 210.0, 330.0)
VERTS = [np.array([R * math.cos(math.radians(d)), R * math.sin(math.radians(d))]) for d in CORNERS_DEG]
EDGES = ((VERTS[0], VERTS[1]), (VERTS[1], VERTS[2]), (VERTS[2], VERTS[0]))


def perron_slivers(n, alpha, b, ht):
    """Sprouted Perron tree on an isosceles base triangle, returned as separate slivers.

    The tree is reframed so its apex sits at the origin and the fan opens toward +y, ready to plant
    apex-first at a core corner. Slivers are kept unmerged so their tips can be jittered individually.
    """
    xs = np.linspace(-b, b, 2 ** n + 1)
    apex = (0.0, ht)
    pieces = [[Polygon([(xs[i], 0.0), (xs[i + 1], 0.0), apex])] for i in range(2 ** n)]
    w = (2.0 * b) / 2 ** n
    for _ in range(n):                                   # bottom-up: overlap consecutive pairs
        step = 0.5 * alpha * w
        pieces = [[shp_translate(p, xoff=+step) for p in pieces[i]]
                  + [shp_translate(p, xoff=-step) for p in pieces[i + 1]]
                  for i in range(0, len(pieces), 2)]
        w *= (1.0 + alpha)
    slivers = [p for group in pieces for p in group]
    return [shp_scale(shp_translate(p, yoff=-ht), xfact=1.0, yfact=-1.0, origin=(0, 0)) for p in slivers]


def _needle(base, angle_deg, length, half_w=0.006):
    d = np.array([math.cos(math.radians(angle_deg)), math.sin(math.radians(angle_deg))])
    perp = np.array([-d[1], d[0]]) * half_w
    tip = base + length * d
    return Polygon([base - perp, base + perp, tip + perp, tip - perp])


def build(seed=5, fringe_n=22, fringe_len=0.5):
    """Union of the solid core, three planted Perron trees, and the outward edge fringe."""
    rng = np.random.default_rng(seed)
    slivers = perron_slivers(N, ALPHA, B, HT)
    parts = [Polygon([tuple(v) for v in VERTS])]
    for deg, v in zip(CORNERS_DEG, VERTS, strict=True):
        for p in slivers:
            jitter = 0.85 + 0.30 * rng.random()                 # per-tip length variation
            q = shp_scale(p, xfact=1.0, yfact=jitter, origin=(0, 0))
            q = shp_rotate(q, deg - 90.0, origin=(0, 0))        # aim the fan outward from this corner
            parts.append(shp_translate(q, xoff=v[0], yoff=v[1]))
    centre = np.mean(VERTS, axis=0)
    for a, b in EDGES:
        nrm = np.array([(b - a)[1], -(b - a)[0]])
        nrm = nrm / np.linalg.norm(nrm)
        if np.dot(nrm, (a + b) / 2 - centre) < 0:
            nrm = -nrm
        ang = math.degrees(math.atan2(nrm[1], nrm[0]))
        for t in np.linspace(0.14, 0.86, fringe_n):
            base = a + t * (b - a)
            bulge = 1.0 - abs(t - 0.5)                          # longer mid-edge -> gently convex halo
            length = fringe_len * (0.55 + 0.8 * rng.random()) * (0.7 + 0.6 * bulge)
            parts.append(_needle(base, ang + 12.0 * (rng.random() - 0.5), length))
    return unary_union(parts)


def _fill(ax, geom, colour):
    for g in (geom.geoms if geom.geom_type == "MultiPolygon" else [geom]):
        if not g.is_empty:
            ax.fill(*g.exterior.xy, facecolor=colour, edgecolor="none", zorder=2)


def main():
    silhouette = build()
    core = Polygon([tuple(v) for v in VERTS])
    tree = unary_union(perron_slivers(N, ALPHA, B, HT))
    base_tri = Polygon([(-B, 0.0), (B, 0.0), (0.0, HT)])
    apex_fan = 2.0 * math.degrees(math.atan(B / HT))

    math_check(
        "Kakeya needle set (filled Perron-tree silhouette)",
        [
            ("Perron tree", f"2^{N} = {2 ** N} slivers, sprout alpha={ALPHA}; area {tree.area / base_tri.area * 100:.0f}% of its triangle"),
            ("apex fan per tree", f"{apex_fan:.0f} deg"),
            ("direction coverage", f"3 trees x {apex_fan:.0f} deg (rot 120) = {3 * apex_fan:.0f} deg -> a needle in every direction"),
            ("symmetry", "three-fold (C3): core corners + trees + fringe at 90/210/330 deg"),
            ("silhouette area", f"{silhouette.area:.3f}  (solid core {core.area:.3f})"),
        ],
    )

    fig, ax = new_axes(1, figsize=(6.6, 6.4))
    _fill(ax, silhouette, YELLOW)
    (x0, y0, x1, y1) = silhouette.bounds
    m = 0.05 * max(x1 - x0, y1 - y0)
    ax.set_xlim(x0 - m, x1 + m)
    ax.set_ylim(y0 - m, y1 + m)
    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
