"""Animation: the Kakeya needle set, an approximation of the Wikipedia image (kakeya.md 2e-2f).

The Wikipedia "Kakeya needle set" picture is a single still: a small Perron-tree core with unit
needles radiating in EVERY direction (a sunburst).  It is a Besicovitch set drawn as its needle
family: a compact set that still contains a unit segment in every direction.  A true Besicovitch set
has area 0, which cannot be drawn, so we render the minimum-visible approximation and print the real
area (see the honesty note in kakeya.md 2f).

What the animation shows:
  * a genuine small-area Perron tree, built here by symmetric cut-and-shift, as the yellow core;
  * a unit needle turning through every direction 0 -> 360 deg; for each direction it is anchored at
    the core's support point in that direction and extended outward by exactly length 1, so it lies
    in the set and pokes out as a spike;
  * every past needle stays faint, so the family accumulates into the Wikipedia sunburst.

Geometric honesty (asserted in MATH CHECK): the needle length is exactly 1 in every frame; the swept
directions cover the full turn (every orientation); the core area is reported with the -> 0 note.

Run: uv run --with matplotlib --with shapely \
     python research/kakeya/figures/2_kakeya_2d/2_6_kakeya_needle_set_anim.py
"""
import math

import numpy as np
from _shared import COLORS, SQRT3, math_check, poly, save_gif, union_area
from matplotlib.animation import FuncAnimation
from shapely.affinity import translate as shp_translate
from shapely.geometry import LineString
from shapely.ops import unary_union

H = SQRT3 / 2.0            # apex height of the unit equilateral core
APEX = (0.5, H)
N_LEVELS = 7               # tree depth: enough canopy detail to read as the Wikipedia core
FRAMES = 96                # full turn: 360 / 96 = 3.75 deg per frame
NEEDLE_LEN = 1.0


def _perron_tree(n: int, s: float = 0.2):
    """Compact Perron tree by symmetric cut-and-shift (same schedule as 2_4_perron_tree.py)."""
    N = 2 ** n
    w = 1.0 / N
    shapes = [[poly(np.array([[i * w, 0.0], [(i + 1) * w, 0.0], [APEX[0], H]]))] for i in range(N)]
    for _ in range(n):
        step = 0.5 * (1.0 - s) * w
        shapes = [
            [shp_translate(p, xoff=+step) for p in shapes[i]] + [shp_translate(p, xoff=-step) for p in shapes[i + 1]]
            for i in range(0, len(shapes), 2)
        ]
        w *= (1.0 + s)
    return unary_union([p for shp in shapes for p in shp])


def _exterior_points(geom) -> np.ndarray:
    geoms = geom.geoms if geom.geom_type == "MultiPolygon" else [geom]
    return np.vstack([np.asarray(g.exterior.coords) for g in geoms])


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    tree = _perron_tree(N_LEVELS)
    core_pts = _exterior_points(tree)
    cen = np.array([tree.centroid.x, tree.centroid.y])
    boundary = tree.boundary
    reach = 3.0  # ray length from the centroid, longer than the core

    # For each direction theta, cast a ray from the core centroid; anchor the unit needle where the
    # ray exits the boundary (the silhouette point in that direction) and extend outward by length 1.
    # Ray-from-centroid distributes anchors smoothly around the whole silhouette (a plain support
    # point would collapse every direction onto the 3 triangle corners), giving the all-around sunburst.
    thetas = np.linspace(0.0, 2 * math.pi, FRAMES, endpoint=False)

    def needle(theta):
        d = np.array([math.cos(theta), math.sin(theta)])
        hit = LineString([tuple(cen), tuple(cen + reach * d)]).intersection(boundary)
        pts = [np.array(g.coords[0]) for g in getattr(hit, "geoms", [hit]) if g.geom_type == "Point"]
        anchor = max(pts, key=lambda q: float(q @ d)) if pts else core_pts[int(np.argmax(core_pts @ d))]
        return anchor, anchor + NEEDLE_LEN * d

    segs = [needle(t) for t in thetas]

    # --- INVARIANT checks ----------------------------------------------------
    lengths = [float(np.linalg.norm(b - a)) for a, b in segs]
    needle_polys = [poly(np.array([a, b, b + 1e-4, a + 1e-4])) for a, b in segs]  # thin quads for area
    set_area = union_area([tree, *needle_polys])
    tri_area = SQRT3 / 4.0
    assert abs(max(lengths) - 1.0) < 1e-9 and abs(min(lengths) - 1.0) < 1e-9, f"needle length != 1: {lengths[:3]}"
    assert tree.area < 0.5 * tri_area, "Perron core must be well under the base triangle area"

    math_check(
        "Kakeya needle set (Wikipedia approximation)",
        [
            ("needle length (all frames)", f"min {min(lengths):.4f}  max {max(lengths):.4f}  (want 1.0000)"),
            ("directions covered", f"{FRAMES} orientations over 0..360 deg  (every direction)"),
            ("Perron core area", f"{tree.area:.3f}  ({tree.area / tri_area * 100:.0f}% of the unit triangle {tri_area:.3f})"),
            ("needle-set area (drawn)", f"{set_area:.3f}  (min visible approximation)"),
            ("true Besicovitch area", "-> 0 as N->inf, but only ~1/log N (Keich): not drawable"),
        ],
    )

    # --- fixed view limits from the whole final set (so accumulation never rescales / clips) ------
    allpts = np.vstack([core_pts, *[np.array([a, b]) for a, b in segs]])
    (x0, y0), (x1, y1) = allpts.min(0), allpts.max(0)
    padx, pady = 0.12 * (x1 - x0), 0.12 * (y1 - y0)

    fig, ax = plt.subplots(figsize=(6.6, 6.6))
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(x0 - padx, x1 + padx)
    ax.set_ylim(y0 - pady, y1 + pady)
    ax.set_title("Kakeya needle set: a unit segment in every direction, packed small", fontsize=10)

    # the yellow Perron core, drawn once underneath the accumulating needles
    for g in (tree.geoms if tree.geom_type == "MultiPolygon" else [tree]):
        ax.fill(*g.exterior.xy, color="#f7f19a", alpha=0.9, edgecolor="none", zorder=1)

    live, = ax.plot([], [], color=COLORS["accent"], lw=2.4, zorder=4)
    counter = ax.text(0.02, 0.98, "", transform=ax.transAxes, va="top", fontsize=10, color=COLORS["guide"])
    trails = []

    def update(i):
        a, b = segs[i]
        t, = ax.plot([a[0], b[0]], [a[1], b[1]], color=COLORS["needle"], lw=0.7, alpha=0.35, zorder=2)
        trails.append(t)
        live.set_data([a[0], b[0]], [a[1], b[1]])
        counter.set_text(f"direction {math.degrees(thetas[i]):3.0f} deg   length = 1.000")
        return live, counter, t

    anim = FuncAnimation(fig, update, frames=FRAMES, interval=60, blit=False)
    print("wrote", save_gif(anim, fps=18, dpi=95))


if __name__ == "__main__":
    main()
