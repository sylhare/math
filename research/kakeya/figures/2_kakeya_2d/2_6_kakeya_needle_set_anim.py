"""Kakeya needle set (Wikipedia image), then its area shrinking (kakeya.md).

Phase A -- the picture. A solid central triangle with Perron-tree branches at each corner and a
needle fringe along the edges; the whole thing is rendered as the FILLED SILHOUETTE of the set (the
union of all needles and the core, one outline), not as separate needle bars. Granularity rises
coarse -> dense.

Phase B -- shrink the area. Perron cut-and-shift: subdivide the core into 2^n sub-triangles and
TRANSLATE them to overlap. Translation preserves each needle's direction, so every direction stays
covered while the (shapely-measured) area drops. Sprout n = 0 -> 9; area falls 100% -> ~22%.

True area -> 0 only as n -> inf and only ~1/log N slowly (Keich): below ~20% needs ~1e5-1e6 pieces,
not drawable. A continuous-rotation needle set never reaches 0 (Cunningham 1971).

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/2_kakeya_2d/2_6_kakeya_needle_set_anim.py
"""
import math

import numpy as np
from _shared import COLORS, math_check, save_gif
from shapely.affinity import translate as shp_translate
from shapely.geometry import Polygon
from shapely.ops import unary_union

SIDE = 1.0
R = SIDE / math.sqrt(3.0)
CORNERS_DEG = (90.0, 210.0, 330.0)
HALFW = 0.012                  # needle half-width (wider so the union reads as filled branches)
LEN_CORNER, LEN_EDGE = 0.62, 0.30
KF, JF = 28, 62                # finest needle counts per edge / per corner fan
CORE = "#f4ec7a"
EDGE = "#8a8a3a"

# Phase A: (edge, corner) needle counts rising.  Phase B: sprout depth n rising (area shrinks).
LEVELS = [(2, 6), (3, 9), (4, 13), (6, 18), (9, 26), (13, 35), (18, 46), (28, 62)]
DEPTHS = list(range(0, 10))    # n = 0 (solid triangle) -> 9 (512 pieces)

VERTS = np.array([R * np.array([math.cos(math.radians(d)), math.sin(math.radians(d))]) for d in CORNERS_DEG])
_EDIR = (VERTS[2] - VERTS[1]) / np.linalg.norm(VERTS[2] - VERTS[1])


def _unit(deg):
    return np.array([math.cos(math.radians(deg)), math.sin(math.radians(deg))])


def _sliver(base, direction, length):
    d = direction / np.linalg.norm(direction)
    perp = np.array([-d[1], d[0]]) * HALFW
    tip = base + length * d
    return Polygon([base - perp, base + perp, tip + perp, tip - perp])


def build_fine():
    rng = np.random.default_rng(7)
    cen = VERTS.mean(0)
    edge_needles, corner_needles = [], []
    for a, b in ((VERTS[0], VERTS[1]), (VERTS[1], VERTS[2]), (VERTS[2], VERTS[0])):
        nrm = np.array([(b - a)[1], -(b - a)[0]]); nrm = nrm / np.linalg.norm(nrm)
        if np.dot(nrm, (a + b) / 2 - cen) < 0:
            nrm = -nrm
        for t in np.linspace(0.06, 0.94, KF):
            edge_needles.append(_sliver(a + t * (b - a), nrm, LEN_EDGE * (0.75 + 0.5 * rng.random())))
    for d0 in CORNERS_DEG:
        v = R * _unit(d0)
        for th in np.linspace(d0 - 60, d0 + 60, JF):
            corner_needles.append(_sliver(v, _unit(th), LEN_CORNER * (0.72 + 0.5 * rng.random())))
    return edge_needles, corner_needles


def _subset(items, k):
    if k >= len(items):
        return items
    return [items[i] for i in np.unique(np.linspace(0, len(items) - 1, k).round().astype(int))]


def sprout(n):
    """Perron cut-and-shift of the core triangle to depth n (decreasing overlap alpha 1.0 -> 0.5);
    n=0 is the solid triangle. Returns the sub-triangle polygons (their union is the shrunk core)."""
    v0, v1, v2 = VERTS
    if n == 0:
        return [Polygon([tuple(v0), tuple(v1), tuple(v2)])]
    alphas = np.linspace(1.0, 0.5, n)
    N = 2 ** n
    pieces = [[Polygon([tuple(v1 + (v2 - v1) * (i / N)), tuple(v1 + (v2 - v1) * ((i + 1) / N)), tuple(v0)])]
              for i in range(N)]
    w = np.linalg.norm(v2 - v1) / N
    for k in range(n):
        step = 0.5 * alphas[k] * w * _EDIR
        pieces = [[shp_translate(p, *(+step)) for p in pieces[i]] + [shp_translate(p, *(-step)) for p in pieces[i + 1]]
                  for i in range(0, len(pieces), 2)]
        w *= (1.0 + alphas[k])
    return [p for grp in pieces for p in grp]


def _fill(ax, geom, fc, ec, lw, alpha=1.0, z=2):
    """Fill a (Multi)Polygon as a single silhouette (one outline per component, no internal edges)."""
    geoms = geom.geoms if geom.geom_type == "MultiPolygon" else [geom]
    arts = []
    for g in geoms:
        if g.is_empty:
            continue
        a, = ax.fill(*g.exterior.xy, facecolor=fc, edgecolor=ec, linewidth=lw, alpha=alpha, zorder=z)
        arts.append(a)
    return arts


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    edge_fine, corner_fine = build_fine()
    core_tri = Polygon([tuple(v) for v in VERTS])
    tri_area = core_tri.area
    fringe_all = unary_union([core_tri, *edge_fine, *corner_fine])

    sprout_at = {n: sprout(n) for n in DEPTHS}
    area_at = {n: unary_union(sprout_at[n]).area for n in DEPTHS}

    frames = [("A", lv) for lv in LEVELS] + [("A", LEVELS[-1])] * 3 + [("B", n) for n in DEPTHS] + [("B", DEPTHS[-1])] * 4

    math_check(
        "Kakeya needle set: build (Wikipedia image) then shrink the area by sprouting",
        [
            ("phase A shape", "solid triangle + corner Perron-tree branches + edge fringe (filled silhouette)"),
            ("phase A coverage", "the three corner fans tile the full turn: a needle in every direction"),
            ("phase B mechanism", "Perron cut-and-shift, depth 0->9 (translate pieces to overlap; direction preserved)"),
            ("area vs depth", "  ".join(f"n{n}:{area_at[n] / tri_area * 100:.0f}%" for n in (0, 2, 4, 6, 9))),
            ("drawable floor", f"~{area_at[9] / tri_area * 100:.0f}% at n=9 (512 pieces); the fall decelerates"),
            ("true area -> 0", "only as n->inf, ~1/log N slowly (Keich): <10% needs ~1e5-1e6 pieces, not drawable"),
            ("needle set", "continuous-rotation set stays > 0 (Cunningham 1971)"),
        ],
    )

    allpts = np.vstack([np.array(fringe_all.envelope.exterior.coords),
                        *[np.array(p.exterior.coords) for p in sprout_at[9]]])
    (x0, y0), (x1, y1) = allpts.min(0), allpts.max(0)
    m = 0.08 * max(x1 - x0, y1 - y0)

    fig, ax = plt.subplots(figsize=(6.6, 6.6))
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(x0 - m, x1 + m); ax.set_ylim(y0 - m, y1 + m)
    title = ax.set_title("", fontsize=10)
    counter = ax.text(0.02, 0.98, "", transform=ax.transAxes, va="top", fontsize=10, color=COLORS["guide"])
    holder = {"arts": []}

    def update(i):
        for a in holder["arts"]:
            a.remove()
        phase, val = frames[i]
        if phase == "A":
            ke, kc = val
            shape = unary_union([core_tri, *_subset(edge_fine, ke * 3), *_subset(corner_fine, kc * 3)])
            holder["arts"] = _fill(ax, shape, CORE, EDGE, 0.7, z=2)
            title.set_text("Kakeya needle set: a solid triangle with Perron-tree branches")
            counter.set_text(f"building granularity: {ke} edge + {kc} corner needles per side")
        else:
            n = val
            fade = 0.5 * (1.0 - n / DEPTHS[-1]) + 0.06        # fringe fades as the core sprouts
            arts = _fill(ax, fringe_all, CORE, "none", 0.0, alpha=fade, z=1)
            arts += _fill(ax, unary_union(sprout_at[n]), CORE, EDGE, 0.5, z=3)
            holder["arts"] = arts
            title.set_text("Shrinking the area: sprout the pieces to overlap (every direction kept)")
            counter.set_text(f"cut-and-shift depth n = {n} ({2 ** n} pieces)      "
                             f"area = {area_at[n] / tri_area * 100:.0f}% of the triangle  (-> 0 slowly; never 0)")
        return holder["arts"] + [title, counter]

    anim = FuncAnimation(fig, update, frames=len(frames), interval=300, blit=False)
    print("wrote", save_gif(anim, fps=4, dpi=105))


if __name__ == "__main__":
    main()
