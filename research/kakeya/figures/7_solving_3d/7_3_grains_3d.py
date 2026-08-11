"""Guth's grains + Besicovitch compression (kakeya.md beats 7c-7d).

Left (3D): a fat tube (wireframe box) whose thin tubes cluster into GRAINS, parallel slabs of
size delta x c x c (delta << c << 1), one tube thick, tiling the tube along its length. Within a
fat tube the grains are disjoint (share only zero-volume faces), so every point lies in at most one
grain.

Right (2D): Besicovitch compression: 1 x delta rectangles in delta-separated directions whose areas
sum to >= 1 yet whose union has measure < eta. Laid out by the Perron cut-and-shift so they overlap;
the union is measured with shapely. The true union -> 0 but only ~1/log N (Keich), so a visible
drawing plateaus above 0.
Run: uv run --with matplotlib --with shapely python research/kakeya/figures/grains_3d.py
"""
import math

import numpy as np
from _shared import COLORS, math_check, save_preview, union_area
from shapely.affinity import translate as shp_translate
from shapely.geometry import Polygon

SQRT3 = math.sqrt(3.0)
H = SQRT3 / 2.0            # height of the unit-base equilateral triangle
APEX_X = 0.5


# =====================================================================================
# GEOMETRY (pure numpy / shapely, portable)
# =====================================================================================
def grain_boxes(delta: float, c: float, x_starts) -> list[tuple]:
    """Axis-aligned grains delta x c x c inside a fat tube [0,1] x [0,c] x [0,c].
    Each grain is delta-thin along the tube axis X and spans the c x c cross-section."""
    return [(x0, x0 + delta, 0.0, c, 0.0, c) for x0 in x_starts]


def box_pairwise_overlap(a: tuple, b: tuple) -> float:
    """Overlap VOLUME of two axis-aligned boxes (x0,x1,y0,y1,z0,z1)."""
    ox = max(0.0, min(a[1], b[1]) - max(a[0], b[0]))
    oy = max(0.0, min(a[3], b[3]) - max(a[2], b[2]))
    oz = max(0.0, min(a[5], b[5]) - max(a[4], b[4]))
    return ox * oy * oz


def _rect(center, angle, length, width) -> Polygon:
    """A length x width rectangle centred at `center`, long axis at `angle` (rad)."""
    u = np.array([math.cos(angle), math.sin(angle)])
    v = np.array([-math.sin(angle), math.cos(angle)])
    c = np.asarray(center)
    corners = [c + s1 * (length / 2) * u + s2 * (width / 2) * v
               for s1, s2 in ((1, 1), (1, -1), (-1, -1), (-1, 1))]
    return Polygon([tuple(p) for p in corners])


def perron_triangles(n: int, s: float = 0.2):
    """Symmetric Perron cut-and-shift merge (same schedule as perron_tree.py): 2**n thin
    sub-triangles of a unit-base equilateral, translated to overlap while keeping directions."""
    N = 2 ** n
    w = 1.0 / N
    shapes = [[Polygon([(i * w, 0.0), ((i + 1) * w, 0.0), (APEX_X, H)])] for i in range(N)]
    while len(shapes) > 1:
        step = 0.5 * (1.0 - s) * w
        shapes = [[shp_translate(p, xoff=+step) for p in shapes[i]]
                  + [shp_translate(p, xoff=-step) for p in shapes[i + 1]]
                  for i in range(0, len(shapes), 2)]
        w *= (1.0 + s)
    return [p for shp in shapes for p in shp]


def compression_rectangles(n: int, s: float = 0.2):
    """1 x delta rectangles in delta-separated directions, laid out by the Perron shift so they
    overlap.  width delta = angular separation = (pi/3)/N over the 60 deg fan (so areas sum to the
    fan width pi/3 >= 1).  Returns (rectangles, delta, N)."""
    tris = perron_triangles(n, s)
    N = len(tris)
    delta = (math.pi / 3.0) / N              # both the direction separation and the tube width
    rects = []
    for t in tris:
        xy = np.array(t.exterior.coords)[:3]
        base_mid = 0.5 * (xy[0] + xy[1])
        apex = xy[2]
        d = apex - base_mid
        ang = math.atan2(d[1], d[0])
        center = 0.5 * (base_mid + apex)     # unit segment centred on the needle midpoint
        rects.append(_rect(center, ang, 1.0, delta))
    return rects, delta, N


# =====================================================================================
# PREVIEW
# =====================================================================================
def _draw_box_wire(ax, box, color, lw=1.2, alpha=1.0):
    x0, x1, y0, y1, z0, z1 = box
    xs, ys, zs = (x0, x1), (y0, y1), (z0, z1)
    corners = np.array([[x, y, z] for x in xs for y in ys for z in zs])
    edges = [(0, 1), (0, 2), (0, 4), (1, 3), (1, 5), (2, 3),
             (2, 6), (3, 7), (4, 5), (4, 6), (5, 7), (6, 7)]
    for a, b in edges:
        ax.plot(*zip(corners[a], corners[b], strict=True), color=color, lw=lw, alpha=alpha)


def _draw_box_solid(ax, box, color, alpha=0.55):
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    x0, x1, y0, y1, z0, z1 = box
    v = {
        "xlo": [(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)],
        "xhi": [(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)],
        "ylo": [(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)],
        "yhi": [(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)],
        "zlo": [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)],
        "zhi": [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)],
    }
    pc = Poly3DCollection(list(v.values()), facecolor=color, edgecolor=color, alpha=alpha, linewidths=0.6)
    ax.add_collection3d(pc)


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (registers 3d projection)

    # ---- geometry ----
    delta3d, c = 0.05, 0.30
    fat_tube = (0.0, 1.0, 0.0, c, 0.0, c)
    x_starts = [0.08, 0.26, 0.44, 0.62, 0.80]
    grains = grain_boxes(delta3d, c, x_starts)

    max_overlap = max((box_pairwise_overlap(grains[i], grains[j])
                       for i in range(len(grains)) for j in range(i + 1, len(grains))), default=0.0)
    # point multiplicity: grains are delta-thin, disjoint intervals along X -> every point in <= 1
    starts = sorted(x_starts)
    max_mult = 1 if all(starts[i] + delta3d <= starts[i + 1] + 1e-12 for i in range(len(starts) - 1)) else 2

    rects, delta2d, N = compression_rectangles(n=6)
    sum_areas = N * 1.0 * delta2d
    union = union_area(rects)
    eta = 0.6

    math_check(
        "grains + Besicovitch compression",
        [
            ("grain size", f"delta x c x c = {delta3d} x {c} x {c}   (delta << c << 1: {delta3d} << {c} << 1)"),
            ("grains per fat tube (drawn)", f"{len(grains)}  (tile the length; ~1/delta in the limit)"),
            ("grains DISJOINT in one tube", f"max pairwise overlap volume = {max_overlap:.6f}  (want 0)"),
            ("point lies in few grains", f"max grains through any point = {max_mult}  (want 1)"),
            ("compression: N rects 1 x delta", f"N = {N},  delta = {delta2d:.5f}  (delta-separated dirs, 60 deg fan)"),
            ("compression: sum of areas", f"{sum_areas:.4f}  (= N*delta = fan width pi/3 = {math.pi/3:.4f}) >= 1"),
            ("compression: union measure", f"{union:.4f}  < eta = {eta}  (visible plateau; true -> 0 like 1/log N)"),
            ("=> compression ratio", f"union / sum = {union / sum_areas:.3f}  (footprint far below content)"),
        ],
    )

    # ---- preview ----
    fig = plt.figure(figsize=(13.5, 5.8))

    ax = fig.add_subplot(1, 2, 1, projection="3d")
    _draw_box_wire(ax, fat_tube, COLORS["guide"], lw=1.3)
    for g in grains:
        _draw_box_solid(ax, g, COLORS["accent"], alpha=0.6)
    # a few thin tubes running lengthwise along the grain
    for (y, z) in [(0.09, 0.18), (0.20, 0.09), (0.15, 0.24), (0.24, 0.20)]:
        ax.plot([0, 1], [y, y], [z, z], color=COLORS["outer"], lw=0.9, alpha=0.85)
    # delta thickness label on one grain, c cross-section label
    ax.text(x_starts[2] + delta3d / 2, -0.06, 0.0, "delta", color=COLORS["accent"], fontsize=11, ha="center")
    ax.text(1.02, c / 2, 0.0, "c", color=COLORS["guide"], fontsize=11)
    ax.text(1.02, 0.0, c / 2, "c", color=COLORS["guide"], fontsize=11)
    ax.text(0.5, c / 2, c * 1.35, "fat tube: grains tile it, disjoint",
            color=COLORS["guide"], fontsize=9, ha="center")
    ax.set_box_aspect((1.0, c, c))
    ax.view_init(elev=18, azim=-58)
    ax.set_axis_off()
    ax.set_title("grains = delta x c x c slabs, one tube thick", fontsize=11)

    ax2 = fig.add_subplot(1, 2, 2)
    from shapely.ops import unary_union
    for r in rects:
        ax2.fill(*r.exterior.xy, color=COLORS["accent"], alpha=0.12, edgecolor="none")
    merged = unary_union(rects)
    for g in (merged.geoms if merged.geom_type == "MultiPolygon" else [merged]):
        ax2.plot(*g.exterior.xy, color=COLORS["outer"], lw=1.0, alpha=0.9)
    ax2.set_aspect("equal")
    ax2.axis("off")
    ax2.set_title(f"compression: sum areas {sum_areas:.2f} >= 1,  union {union:.2f} < {eta}", fontsize=11)

    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
