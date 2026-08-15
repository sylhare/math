"""Besicovitch set from three Perron trees (kakeya.md 2e-2f).

One equilateral Perron tree carries only its 60 deg apex fan (here 60..120 deg). Translation
preserves direction, so rotating three finished trees by 0 / 120 / 240 deg about the apex spreads
those fans over the full 180 deg (a direction and its reverse are the same): an all-directions set.

    tree fan            = 60..120 deg
    + rotate 120 deg    = 180..240 deg == 0..60 deg (mod 180)
    + rotate 240 deg    = 300..360 deg == 120..180 deg (mod 180)
    union               = 0..180 deg   -> a unit segment in every direction.

True |K| = 0 (Besicovitch) is a limit (n -> inf), area shrinking only ~1/log N (Keich), so this
renders the minimum-visible finite-level approximation.

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/besicovitch_assembly.py
"""
import numpy as np
from _shared import COLORS, SQRT3, equilateral, math_check, new_axes, poly, save_preview, triangle_fan_degrees
from shapely.affinity import rotate as shp_rotate
from shapely.affinity import translate as shp_translate
from shapely.ops import unary_union

H = SQRT3 / 2.0          # height of the base-1 equilateral triangle
APEX = (0.5, H)          # shared apex / rotation pivot


# Perron cut-and-shift, replicated locally (not imported)
def _slivers(n: int):
    """2^n thin subtriangles of the base-1 equilateral triangle, all sharing the apex."""
    N = 2 ** n
    w = 1.0 / N
    return [[poly(np.array([[i * w, 0.0], [(i + 1) * w, 0.0], APEX]))] for i in range(N)]


def perron_tree(n: int, s: float = 0.2):
    """Symmetric cut-and-shift merge over n levels (keep fraction s of fresh base each merge).

    Each level pairs neighbouring blocks and translates them toward each other so they overlap,
    which shrinks the footprint while preserving every segment's direction. Returns (union, tris).
    """
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


def _covered_directions(tris, rotations, pivot):
    """Boolean coverage of 1-degree direction bins in [0,180) from all triangles' apex fans."""
    covered = np.zeros(180, dtype=bool)
    for ang in rotations:
        for t in tris:
            rt = shp_rotate(t, ang, origin=pivot)
            xy = np.array(rt.exterior.coords)[:3]
            lo, hi = triangle_fan_degrees(xy)
            for d in range(int(np.floor(lo)), int(np.ceil(hi)) + 1):
                covered[d % 180] = True
    return covered


def _draw_region(ax, geom, color, alpha):
    geoms = geom.geoms if geom.geom_type == "MultiPolygon" else [geom]
    for g in geoms:
        ax.fill(*g.exterior.xy, color=color, alpha=alpha, edgecolor="none")


def _draw_rays(ax, tris, rotations, pivot, color, k=40):
    """Overlay unit-direction rays (base-midpoint -> apex) for a sample of subtriangles, per rotation."""
    for ang in rotations:
        sample = tris[:: max(1, len(tris) // k)]
        for t in sample:
            rt = shp_rotate(t, ang, origin=pivot)
            xy = np.array(rt.exterior.coords)[:3]
            base_mid = 0.5 * (xy[0] + xy[1])
            ax.plot([base_mid[0], xy[2][0]], [base_mid[1], xy[2][1]], color=color, lw=0.5, alpha=0.7)


def main():
    n, s = 9, 0.2
    tree, tris = perron_tree(n, s)
    base_area = poly(equilateral(1.0)).area
    rotations = (0.0, 120.0, 240.0)

    # assemble: three rotated copies of the finished tree about the apex
    besic = unary_union([shp_rotate(tree, a, origin=APEX) for a in rotations])
    covered = _covered_directions(tris, rotations, APEX)
    lo, hi = triangle_fan_degrees(equilateral(1.0))

    # tree area by level (this schedule plateaus)
    decay = {k: perron_tree(k, s)[0].area for k in (1, 3, 6, 9)}

    math_check(
        "Besicovitch assembly (three Perron trees, 0/120/240 deg)",
        [
            ("one tree apex fan", f"{lo:.0f}..{hi:.0f} deg  (60 deg wide)"),
            ("rotations applied", "0, 120, 240 deg about the apex"),
            ("direction bins covered", f"{int(covered.sum())}/180 deg"),
            ("spans 0..180 deg?", f"{bool(covered.all())}  (a unit segment in every direction)"),
            ("base triangle area", f"{base_area:.4f}  (sqrt3/4)"),
            ("tree area by level n", "  ".join(f"n={k}:{v:.3f}" for k, v in decay.items())),
            ("assembled area (visible)", f"{besic.area:.4f}  (finite-level approximation)"),
            ("true |K|", "= 0 (Besicovitch), reached as n -> inf; ~1/log N (Keich), not drawable"),
        ],
    )

    # Preview
    fig, ax = new_axes(2, figsize=(11, 5.6))
    _draw_region(ax[0], tree, COLORS["region"], 0.75)
    _draw_rays(ax[0], tris, (0.0,), APEX, COLORS["needle"])
    ax[0].set_title(f"one Perron tree  (fan {lo:.0f}..{hi:.0f} deg, area {tree.area:.3f})")

    _draw_region(ax[1], besic, COLORS["region"], 0.8)
    _draw_rays(ax[1], tris, rotations, APEX, COLORS["needle"])
    ax[1].set_title(f"three trees 0/120/240 deg: all {int(covered.sum())} deg  (area {besic.area:.3f} -> 0 in the limit)")
    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
