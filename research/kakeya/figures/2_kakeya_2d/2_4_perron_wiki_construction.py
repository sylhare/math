"""Besicovitch set by the documented Perron construction (kakeya.md 2d-2e; Wikipedia Kakeya set, Falconer pp.96-99).

Panels:
 (1) equilateral triangle, base split into 2^n segments each joined to the shared apex;
 (2) sprout: overlap consecutive pairs so their bases overlap (bottom-up), giving one Perron tree;
 (3) three trees rotated 120 deg about the centroid, unioned: a Besicovitch set covering all directions.

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/2_kakeya_2d/2_4_perron_wiki_construction.py
"""
import numpy as np
from _shared import SQRT3, math_check, new_axes, save_preview
from shapely.affinity import rotate as shp_rotate
from shapely.affinity import translate as shp_translate
from shapely.geometry import Polygon
from shapely.ops import unary_union

H = SQRT3 / 2.0
APEX = (0.0, H)
N = 6
ALPHA = 0.5
CORE, EDGE = "#f4ec7a", "#8a8a3a"


def subdivided(n):
    """2^n triangles: base [-0.5,0.5] split into equal segments, each joined to the shared apex."""
    xs = np.linspace(-0.5, 0.5, 2 ** n + 1)
    return [Polygon([(xs[i], 0.0), (xs[i + 1], 0.0), APEX]) for i in range(2 ** n)]


def sprout(n, alpha):
    """Overlap consecutive pairs bottom-up so their bases overlap; union = one Perron tree."""
    pieces = [[p] for p in subdivided(n)]
    w = 1.0 / 2 ** n
    for _ in range(n):
        step = 0.5 * alpha * w
        pieces = [[shp_translate(p, xoff=+step) for p in pieces[i]] + [shp_translate(p, xoff=-step) for p in pieces[i + 1]]
                  for i in range(0, len(pieces), 2)]
        w *= (1.0 + alpha)
    return unary_union([p for g in pieces for p in g])


def _fill(ax, geom, fc, ec, lw):
    for g in (geom.geoms if geom.geom_type == "MultiPolygon" else [geom]):
        ax.fill(*g.exterior.xy, facecolor=fc, edgecolor=ec, linewidth=lw)


def main():
    tri_area = Polygon([(-0.5, 0.0), (0.5, 0.0), APEX]).area
    tree = sprout(N, ALPHA)
    c = tree.centroid
    besic = unary_union([shp_rotate(tree, a, origin=(c.x, c.y)) for a in (0, 120, 240)])

    math_check(
        "Perron construction (documented)",
        [
            ("subdivision", f"2^{N} = {2 ** N} triangles, base split, shared apex"),
            ("sprout", f"overlap bases bottom-up, alpha={ALPHA}; one tree area {tree.area / tri_area * 100:.0f}% of triangle"),
            ("Besicovitch", f"3 trees rotated 120 deg about centroid; union area {besic.area:.3f}"),
            ("directions", "each tree carries a 60 deg fan; 3 x 60 rotated -> all 180 deg"),
        ],
    )

    fig, ax = new_axes(3, figsize=(16, 5.4))
    _fill(ax[0], unary_union(subdivided(N)), CORE, EDGE, 0.4)
    for p in subdivided(N)[:: max(1, 2 ** N // 16)]:
        xy = np.array(p.exterior.coords)
        ax[0].plot([xy[:2, 0].mean(), APEX[0]], [xy[:2, 1].mean(), APEX[1]], color=EDGE, lw=0.4)
    ax[0].set_title(f"subdivide base into 2^{N}, shared apex", fontsize=10)
    _fill(ax[1], tree, CORE, EDGE, 0.4)
    ax[1].set_title("sprout: overlap bases -> one Perron tree", fontsize=10)
    _fill(ax[2], besic, CORE, EDGE, 0.3)
    ax[2].set_title("three trees rotated 120 deg -> Besicovitch set", fontsize=10)
    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
