"""Shrinking a Kakeya set's area by Perron cut-and-shift (kakeya.md 2f).

Start from the needle set (solid triangle + faded needle fringe showing every direction), then
subdivide the core into 2^n sub-triangles and TRANSLATE them to overlap (sprouting). Translation
preserves each needle's direction, so every direction stays covered while the (shapely-measured)
area drops. Sprout n = 0 -> 9; area falls 100% -> ~22%.

True area -> 0 only as n -> inf and only ~1/log N slowly (Keich): below ~20% needs ~1e5-1e6 pieces,
not drawable. A continuous-rotation needle set never reaches 0 (Cunningham 1971).

Companion to 2_6 (the needle-set build).

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/2_kakeya_2d/2_7_kakeya_area_shrink_anim.py
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
HALFW = 0.012
LEN_CORNER, LEN_EDGE = 0.62, 0.30
KF, JF = 28, 62
CORE = "#f4ec7a"
EDGE = "#8a8a3a"

DEPTHS = list(range(0, 10))    # cut-and-shift depth n = 0 (solid triangle) -> 9 (512 pieces)

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
    """The needle fringe (faded backdrop): unit needles in every direction."""
    rng = np.random.default_rng(7)
    cen = VERTS.mean(0)
    needles = []
    for a, b in ((VERTS[0], VERTS[1]), (VERTS[1], VERTS[2]), (VERTS[2], VERTS[0])):
        nrm = np.array([(b - a)[1], -(b - a)[0]]); nrm = nrm / np.linalg.norm(nrm)
        if np.dot(nrm, (a + b) / 2 - cen) < 0:
            nrm = -nrm
        for t in np.linspace(0.06, 0.94, KF):
            needles.append(_sliver(a + t * (b - a), nrm, LEN_EDGE * (0.75 + 0.5 * rng.random())))
    for d0 in CORNERS_DEG:
        v = R * _unit(d0)
        for th in np.linspace(d0 - 60, d0 + 60, JF):
            needles.append(_sliver(v, _unit(th), LEN_CORNER * (0.72 + 0.5 * rng.random())))
    return needles


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

    core_tri = Polygon([tuple(v) for v in VERTS])
    tri_area = core_tri.area
    fringe_all = unary_union([core_tri, *build_fine()])

    sprout_at = {n: sprout(n) for n in DEPTHS}
    area_at = {n: unary_union(sprout_at[n]).area for n in DEPTHS}

    frames = DEPTHS + [DEPTHS[-1]] * 5

    math_check(
        "Shrinking a Kakeya set by Perron cut-and-shift",
        [
            ("mechanism", "subdivide the core into 2^n sub-triangles, translate to overlap (direction preserved)"),
            ("area vs depth", "  ".join(f"n{n}:{area_at[n] / tri_area * 100:.0f}%" for n in (0, 2, 4, 6, 9))),
            ("drawable floor", f"~{area_at[9] / tri_area * 100:.0f}% at n=9 (512 pieces); the fall decelerates"),
            ("true area -> 0", "only as n->inf, ~1/log N slowly (Keich): <10% needs ~1e5-1e6 pieces, not drawable"),
            ("needle set", "continuous-rotation set stays > 0 (Cunningham 1971)"),
        ],
    )

    pts = np.vstack([np.array(fringe_all.envelope.exterior.coords),
                     *[np.array(p.exterior.coords) for p in sprout_at[9]]])
    (x0, y0), (x1, y1) = pts.min(0), pts.max(0)
    m = 0.08 * max(x1 - x0, y1 - y0)

    fig, ax = plt.subplots(figsize=(6.6, 6.6))
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(x0 - m, x1 + m); ax.set_ylim(y0 - m, y1 + m)
    ax.set_title("Shrinking the area: sprout the pieces to overlap (every direction kept)", fontsize=10)
    counter = ax.text(0.02, 0.98, "", transform=ax.transAxes, va="top", fontsize=10, color=COLORS["guide"])
    holder = {"arts": []}

    def update(i):
        for a in holder["arts"]:
            a.remove()
        n = frames[i]
        fade = 0.5 * (1.0 - n / DEPTHS[-1]) + 0.06        # fringe fades as the core sprouts
        arts = _fill(ax, fringe_all, CORE, "none", 0.0, alpha=fade, z=1)
        arts += _fill(ax, unary_union(sprout_at[n]), CORE, "none", 0.0, z=3)
        holder["arts"] = arts
        counter.set_text(f"cut-and-shift depth n = {n} ({2 ** n} pieces)      "
                         f"area = {area_at[n] / tri_area * 100:.0f}% of the triangle  (-> 0 slowly; never 0)")
        return holder["arts"] + [counter]

    anim = FuncAnimation(fig, update, frames=len(frames), interval=320, blit=False)
    print("wrote", save_gif(anim, fps=4, dpi=105))


if __name__ == "__main__":
    main()
