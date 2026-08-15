"""Perron tree, bottom-up symmetric merge: push both halves toward the pair centre so the tree
stays centred and the 3 rotated copies tile symmetrically about the apex. Area -> 0 slowly
(~1/log N). Prints area vs level n and renders a symmetric PNG."""
import math

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from shapely.affinity import rotate, translate
from shapely.geometry import Polygon
from shapely.ops import unary_union

H = math.sqrt(3) / 2.0
APEX = 0.5


def slivers(n):
    N = 2 ** n
    w = 1.0 / N
    return [[Polygon([(i * w, 0.0), ((i + 1) * w, 0.0), (APEX, H)])] for i in range(N)]


def perron(n, s):
    shapes = slivers(n)
    w = 1.0 / (2 ** n)
    for _ in range(n):
        step = 0.5 * (1.0 - s) * w  # symmetric push toward the pair centre
        out = []
        for i in range(0, len(shapes), 2):
            left = [translate(p, xoff=+step) for p in shapes[i]]
            right = [translate(p, xoff=-step) for p in shapes[i + 1]]
            out.append(left + right)
        shapes = out
        w *= (1.0 + s)
    flat = [p for shp in shapes for p in shp]
    return unary_union(flat)


base_area = Polygon([(0, 0), (1, 0), (APEX, H)]).area
print("area vs subdivision level n (does it keep dropping toward 0?)  base=%.4f" % base_area, flush=True)
print(f"{'n':>3} {'N=2^n':>7} {'s=0.5':>9} {'s=0.2':>9}  {'s=0.2 %base':>11}", flush=True)
for n in [1, 2, 4, 6, 8, 10, 11]:
    a5 = perron(n, 0.5).area
    a2 = perron(n, 0.2).area
    print(f"{n:>3} {2**n:>7} {a5:>9.4f} {a2:>9.4f}  {a2/base_area*100:>10.1f}%", flush=True)

# clean symmetric render
n, s = 9, 0.2
tree = perron(n, s)
# pivot at the apex (top of canopy) so 3 copies meet there
pivot = (APEX, H)
copies = [rotate(tree, ang, origin=pivot) for ang in (0, 120, 240)]
full = unary_union(copies)

fig, axes = plt.subplots(1, 2, figsize=(12, 6))
g = tree.geoms if tree.geom_type == "MultiPolygon" else [tree]
for p in g:
    axes[0].fill(*p.exterior.xy, alpha=0.85, color="#1f77b4", edgecolor="none")
axes[0].set_title("Perron tree  n=%d  (area %.3f = %.0f%% of triangle)" % (n, tree.area, tree.area / base_area * 100))
g = full.geoms if full.geom_type == "MultiPolygon" else [full]
for p in g:
    axes[1].fill(*p.exterior.xy, alpha=0.85, color="#d62728", edgecolor="none")
axes[1].set_title("Besicovitch set: 3 trees rotated 120 deg  (all directions)")
for ax in axes:
    ax.set_aspect("equal"); ax.axis("off")
fig.tight_layout()
fig.savefig("perron3_render.png", dpi=140)
print("\nwrote perron3_render.png; full-set area = %.4f" % full.area)
