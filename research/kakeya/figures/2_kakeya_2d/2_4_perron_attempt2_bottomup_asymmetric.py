"""Perron tree, bottom-up asymmetric merge (right shape slid left).

Split the base [0,1] into N = 2^n equal blocks; sliver E_i has that block as base and shared apex
A = (1/2, h). The slivers tile the triangle T. Each carries unit segments in its own narrow fan
(base-point -> A).

Merge (bottom up): pair consecutive shapes; translate the right shape left so its base overlaps the
left shape's on a fraction (1-s) of a block, keeping s*block of new base. Translation preserves each
segment's direction, so the merge covers the union of both fans while area drops; repeat n times.
Three copies rotated 0/60/120 deg cover all 180 deg.
"""
import math

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from shapely.affinity import rotate, translate
from shapely.geometry import LineString, Polygon
from shapely.ops import unary_union

H = math.sqrt(3) / 2.0  # equilateral, base 1 -> apex angle 60 deg
APEX = 0.5


def slivers(n):
    N = 2 ** n
    w = 1.0 / N
    return [[Polygon([(i * w, 0.0), ((i + 1) * w, 0.0), (APEX, H)])] for i in range(N)]


def merge_pass(shapes, block_w, s):
    """Pair up shapes; slide right shape left by (1-s)*block_w so bases overlap."""
    out = []
    shift = (1.0 - s) * block_w
    for i in range(0, len(shapes), 2):
        left, right = shapes[i], shapes[i + 1]
        right = [translate(p, xoff=-shift) for p in right]
        out.append(left + right)
    return out


def perron(n, s):
    shapes = slivers(n)
    block_w = 1.0 / (2 ** n)
    for _ in range(n):
        shapes = merge_pass(shapes, block_w, s)
        block_w *= (1.0 + s)  # merged base width grows by factor (1+s)
    flat = [p for shp in shapes for p in shp]
    return unary_union(flat), flat


def frac_directions_covered(geom, lo_deg, hi_deg, n_ang=180, chord=0.3, tries=250):
    import random

    random.seed(0)
    minx, miny, maxx, maxy = geom.bounds
    hits = 0
    total = 0
    for k in range(n_ang):
        th = math.radians(lo_deg + (hi_deg - lo_deg) * k / n_ang)
        dx, dy = math.cos(th), math.sin(th)
        total += 1
        for _ in range(tries):
            px = random.uniform(minx, maxx)
            py = random.uniform(miny, maxy)
            if geom.contains(LineString([(px, py), (px + chord * dx, py + chord * dy)])):
                hits += 1
                break
    return hits / total


base_area = Polygon([(0, 0), (1, 0), (APEX, H)]).area
print("Perron tree (equilateral, 60 deg fan).  base triangle area = %.4f" % base_area)
print(f"{'n':>3} {'#tri':>6} {'s=0.5':>10} {'s=0.3':>10} {'s=0.1':>10}")
for n in range(1, 9):
    row = [f"{n:>3}", f"{2**n:>6}"]
    for s in (0.5, 0.3, 0.1):
        g, _ = perron(n, s)
        row.append(f"{g.area:>10.4f}")
    print(" ".join(row))

# pick a good tree and check coverage
n, s = 7, 0.30
tree, tris = perron(n, s)
cov60 = frac_directions_covered(tree, 60, 120)  # apex fan of an upward equilateral spans 60..120 deg
print(f"\nn={n}, s={s}: area={tree.area:.4f}  ({tree.area/base_area*100:.1f}% of triangle)")
print(f"  fraction of the 60 deg fan covered (chord test): {cov60:.2f}")

pivot = (APEX, 0.0)
full = unary_union([rotate(tree, a, origin=pivot) for a in (0, 60, 120)])
cov180 = frac_directions_covered(full, 0, 180)
print(f"full set (3 rotations): area={full.area:.4f}  all-direction coverage: {cov180:.2f}")

# Render
fig, axes = plt.subplots(1, 3, figsize=(16, 5.2))
for ax, (title, geoms, col) in zip(
    axes,
    [
        ("base triangle (area %.3f)" % base_area, [Polygon([(0, 0), (1, 0), (APEX, H)])], "#999"),
        ("Perron tree n=%d, 60 deg fan (area %.3f)" % (n, tree.area),
         tree.geoms if tree.geom_type == "MultiPolygon" else [tree], "#1f77b4"),
        ("all directions: 3 rotated trees (area %.3f)" % full.area,
         full.geoms if full.geom_type == "MultiPolygon" else [full], "#d62728"),
    ],
    strict=False,
):
    for g in geoms:
        ax.fill(*g.exterior.xy, alpha=0.75, color=col, edgecolor="none")
    ax.set_title(title); ax.set_aspect("equal"); ax.axis("off")
fig.tight_layout()
fig.savefig("perron2_render.png", dpi=130)
print("wrote perron2_render.png")
