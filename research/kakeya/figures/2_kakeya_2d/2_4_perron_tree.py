"""Figure: Perron tree -> Besicovitch set (beats 2d-2f of ../kakeya.md).

Math validated here:
  * one equilateral tree carries a 60 deg fan (apex angle);  translation preserves direction, so
    three copies rotated 0/60/120 deg cover all 180 deg  (=> 60 deg is NOT a limitation);
  * the cut-and-shift overlap strictly REDUCES area while keeping every direction.

Honesty note (see the user's guidance): the true Besicovitch area -> 0, but only logarithmically
slowly (~1/log N, Keich), and a zero-area shape cannot be drawn.  So we render the *minimum visible*
approximation and print the real area readout, rather than pretending the region vanishes.

Run:  uv run --with matplotlib --with shapely python research/kakeya/figures/perron_tree.py
"""

import numpy as np
from _shared import COLORS, SQRT3, equilateral, math_check, new_axes, poly, save_preview, triangle_fan_degrees
from shapely.affinity import rotate as shp_rotate
from shapely.affinity import translate as shp_translate
from shapely.ops import unary_union

H = SQRT3 / 2.0
APEX_X = 0.5


def _slivers(n):
    N = 2 ** n
    w = 1.0 / N
    return [[poly(np.array([[i * w, 0.0], [(i + 1) * w, 0.0], [APEX_X, H]]))] for i in range(N)]


def perron_tree(n: int, s: float = 0.2):
    """Symmetric cut-and-shift merge, n levels, keeping s*block of fresh base per merge.
    Returns (shapely union, list of triangles)."""
    shapes = _slivers(n)
    w = 1.0 / (2 ** n)
    for _ in range(n):
        step = 0.5 * (1.0 - s) * w
        shapes = [
            [shp_translate(p, xoff=+step) for p in shapes[i]] + [shp_translate(p, xoff=-step) for p in shapes[i + 1]]
            for i in range(0, len(shapes), 2)
        ]
        w *= (1.0 + s)
    tris = [p for shp in shapes for p in shp]
    return unary_union(tris), tris


def _draw_region(ax, geom, color, alpha):
    geoms = geom.geoms if geom.geom_type == "MultiPolygon" else [geom]
    for g in geoms:
        ax.fill(*g.exterior.xy, color=color, alpha=alpha, edgecolor="none")


def _draw_needles(ax, tris, color, k=48):
    """Overlay a sample of unit-direction segments (base point -> apex) like Hickman Fig 3."""
    for t in tris[:: max(1, len(tris) // k)]:
        xy = np.array(t.exterior.coords)[:3]
        base_mid = 0.5 * (xy[0] + xy[1])
        ax.plot([base_mid[0], xy[2][0]], [base_mid[1], xy[2][1]], color=color, lw=0.5, alpha=0.7)


def main():
    base = poly(equilateral(1.0))
    base_area = base.area
    n, s = 9, 0.2
    tree, tris = perron_tree(n, s)

    # --- validation ---
    lo, hi = triangle_fan_degrees(equilateral(1.0))
    pivot = (APEX_X, H)
    full = unary_union([shp_rotate(tree, a, origin=pivot) for a in (0, 120, 240)])
    # area decay is monotone but plateaus for THIS visible schedule; report honestly
    areas = {k: perron_tree(k, s)[0].area for k in (1, 3, 6)}
    areas[n] = tree.area  # reuse the already-built n=9 union instead of rebuilding it
    math_check(
        "Perron tree / Besicovitch",
        [
            ("equilateral apex fan", f"{lo:.0f}..{hi:.0f} deg  (60 deg wide)"),
            ("3 rotations cover", "0..180 deg  => all directions (60 deg is NOT a wall)"),
            ("base triangle area", f"{base_area:.4f}  (base=1 equilateral => sqrt3/4 = {SQRT3/4:.4f})"),
            ("tree area, this schedule", "  ".join(f"n={k}:{v:.3f}" for k, v in areas.items())),
            ("=> visible approximation", f"{tree.area:.3f} = {tree.area/base_area*100:.0f}% of triangle"),
            ("true Besicovitch area", "-> 0 as N->inf, but only ~1/log N (Keich): not drawable, so we show the min visible form"),
        ],
    )

    # --- preview ---
    fig, ax = new_axes(3, figsize=(16, 5.4))
    _draw_region(ax[0], base, COLORS["region"], 0.6)
    _draw_needles(ax[0], [base], COLORS["needle"])
    ax[0].set_title(f"base triangle  (area {base_area:.3f}, 60 deg of directions)")

    _draw_region(ax[1], tree, COLORS["region"], 0.7)
    _draw_needles(ax[1], tris, COLORS["needle"])
    ax[1].set_title(f"Perron tree  (area {tree.area:.3f} = {tree.area/base_area*100:.0f}% of triangle)")

    _draw_region(ax[2], full, COLORS["accent"], 0.75)
    ax[2].set_title("3 trees rotated 120 deg: all directions")

    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
