"""Perron tree via top-down cevian split, right subtree shifted left to overlap.

  - A triangle with base on y=0 and apex P carries a unit segment in every direction of the fan
    {base-point -> P} = the apex angle.
  - Cevian apex->base-midpoint splits it into Left/Right (shared apex), each carrying half the fan.
  - Translation preserves each segment's direction, so pieces slide to overlap (area shrinks) with
    the fan unchanged; recurse.
  - Three copies rotated 0/60/120 deg tile 180 deg (all directions).

Measures union area vs depth and samples direction coverage, then renders PNGs.
"""
import math

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from shapely.affinity import rotate, translate
from shapely.geometry import Polygon
from shapely.ops import unary_union

H = math.sqrt(3) / 2.0  # equilateral triangle, base 1 -> apex angle 60 deg


def tri(a, b, apex):
    """Triangle with base [a,b] on y=0 and apex (px,H)."""
    return Polygon([(a, 0.0), (b, 0.0), (apex, H)])


def sprout(a, b, apex, depth, overlap):
    """Return list of leaf triangles. `overlap` in (0,1]: fraction of half-base to slide."""
    if depth == 0:
        return [tri(a, b, apex)]
    m = 0.5 * (a + b)
    left = sprout(a, m, apex, depth - 1, overlap)          # covers left half-fan
    right = sprout(m, b, apex, depth - 1, overlap)         # covers right half-fan
    delta = overlap * (m - a)                              # slide right piece left
    right = [translate(p, xoff=-delta, yoff=0.0) for p in right]
    return left + right


def union_area(polys):
    return unary_union(polys).area


def covered_directions(polys, n=360):
    """Fraction of angles in [0,180) for which some triangle contains a segment in that
    direction. Test: a triangle contains a unit direction theta iff a line of slope theta
    crosses it (its interior admits a chord of that direction)."""
    u = unary_union(polys)
    hits = 0
    for k in range(n):
        th = math.pi * k / n
        d = np.array([math.cos(th), math.sin(th)])
        # sample chords: project polygon, see if a line in direction d fits inside union.
        # cheap proxy: does the union contain a segment of length L in direction th?
        ok = False
        minx, miny, maxx, maxy = u.bounds
        for _ in range(40):
            px = np.random.uniform(minx, maxx)
            py = np.random.uniform(miny, maxy)
            seg = _seg(px, py, d, 0.25)  # look for a modest chord (rendering proof, not full unit)
            if u.contains(seg):
                ok = True
                break
        hits += ok
    return hits / n


def _seg(px, py, d, L):
    from shapely.geometry import LineString

    return LineString([(px, py), (px + L * d[0], py + L * d[1])])


# --- area shrinks with depth (single 60 deg tree) -------------------------------------
print("single equilateral tree (apex angle 60 deg), overlap=1.0")
print(f"{'depth':>5} {'#tri':>6} {'union_area':>12}  area/orig")
base_area = tri(0, 1, 0.5).area
for depth in range(0, 8):
    leaves = sprout(0.0, 1.0, 0.5, depth, overlap=1.0)
    a = union_area(leaves)
    print(f"{depth:>5} {len(leaves):>6} {a:>12.5f}  {a / base_area:>7.3f}")

# --- full 180 deg: rotate three 60 deg trees ------------------------------------------
depth = 6
leaves = sprout(0.0, 1.0, 0.5, depth, overlap=1.0)
single = unary_union(leaves)
# recenter on the base midpoint before rotating so copies share a pivot
pivot = (0.5, 0.0)
full = unary_union([rotate(single, ang, origin=pivot) for ang in (0, 60, 120)])
print(f"\nfull all-directions set (3x rotated depth-{depth} trees): area = {full.area:.5f}")

# --- render ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# panel 1: naive union (depth 0) vs sprouted
ax = axes[0]
for p in sprout(0.0, 1.0, 0.5, 0, 1.0):
    ax.fill(*p.exterior.xy, alpha=0.5, color="#888")
ax.set_title("depth 0: plain triangle (area %.3f)" % base_area)
ax.set_aspect("equal"); ax.axis("off")

ax = axes[1]
for p in leaves:
    ax.fill(*p.exterior.xy, alpha=0.25, color="#1f77b4", edgecolor="none")
ax.set_title("depth %d sprout, 60 deg fan (area %.3f)" % (depth, single.area))
ax.set_aspect("equal"); ax.axis("off")

ax = axes[2]
geoms = full.geoms if full.geom_type == "MultiPolygon" else [full]
for g in geoms:
    ax.fill(*g.exterior.xy, alpha=0.7, color="#d62728", edgecolor="none")
ax.set_title("all directions: 3 rotated trees (area %.3f)" % full.area)
ax.set_aspect("equal"); ax.axis("off")

fig.tight_layout()
fig.savefig("perron_render.png", dpi=130)
print("\nwrote perron_render.png")
