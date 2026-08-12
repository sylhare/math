"""Constructing a Kakeya (Besicovitch) set (kakeya.md 2d-2e).

Steps: equilateral triangle -> divide the base into 2^n triangles (shared apex) -> slide consecutive
pairs so their bases overlap (bottom-up sprouting; area shrinks, directions kept) -> union three trees
rotated 120 deg about the centroid.

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/2_kakeya_2d/2_8_kakeya_construction_anim.py
"""
import numpy as np
from _shared import COLORS, SQRT3, math_check, save_gif
from shapely.affinity import rotate as shp_rotate
from shapely.affinity import translate as shp_translate
from shapely.geometry import Polygon
from shapely.ops import unary_union

H = SQRT3 / 2.0
APEX = (0.0, H)
N = 6                         # 2^N sub-triangles
ALPHA = 0.6                  # overlap fraction of the finished tree
CORE = "#f4ec7a"


def subdivided():
    xs = np.linspace(-0.5, 0.5, 2 ** N + 1)
    return [Polygon([(xs[i], 0.0), (xs[i + 1], 0.0), APEX]) for i in range(2 ** N)]


def sprout(alpha):
    pieces = [[p] for p in subdivided()]
    w = 1.0 / 2 ** N
    for _ in range(N):
        step = 0.5 * alpha * w
        pieces = [[shp_translate(p, xoff=+step) for p in pieces[i]] + [shp_translate(p, xoff=-step) for p in pieces[i + 1]]
                  for i in range(0, len(pieces), 2)]
        w *= (1.0 + alpha)
    return unary_union([p for g in pieces for p in g])


def _fill(ax, geom, fc, ec, lw, alpha=1.0, z=2):
    arts = []
    for g in (geom.geoms if geom.geom_type == "MultiPolygon" else [geom]):
        if not g.is_empty:
            a, = ax.fill(*g.exterior.xy, facecolor=fc, edgecolor=ec, linewidth=lw, alpha=alpha, zorder=z)
            arts.append(a)
    return arts


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    tri = Polygon([(-0.5, 0.0), (0.5, 0.0), APEX])
    tri_area = tri.area
    tree = sprout(ALPHA)
    c = tree.centroid
    besic = unary_union([shp_rotate(tree, a, origin=(c.x, c.y)) for a in (0, 120, 240)])

    math_check(
        "Kakeya set construction",
        [
            ("subdivide", f"2^{N} = {2 ** N} triangles, base split, shared apex"),
            ("sprout", f"overlap bases, alpha={ALPHA}; one tree area {tree.area / tri_area * 100:.0f}% of triangle"),
            ("rotate", f"3 copies 120 deg about centroid; Besicovitch area {besic.area:.3f}"),
            ("directions", "each tree = 60 deg fan; 3 rotations -> all 180 deg"),
        ],
    )

    SUB, SPR, ROT, HOLD = 6, 16, 12, 5
    frames = [("tri", None)] * HOLD
    frames += [("subdiv", None)] * SUB
    frames += [("sprout", a) for a in np.linspace(0.0, ALPHA, SPR)]
    frames += [("sprout", ALPHA)] * 3
    frames += [("rot", (120.0 * j / ROT, 0.0, 2)) for j in range(1, ROT + 1)]
    frames += [("rot", (120.0, 0.0, 2))] * 3
    frames += [("rot", (120.0, 240.0 * j / ROT, 3)) for j in range(1, ROT + 1)]
    frames += [("rot", (120.0, 240.0, 3))] * (HOLD + 3)

    pts = np.array(besic.envelope.exterior.coords)
    (x0, y0), (x1, y1) = pts.min(0), pts.max(0)
    m = 0.10 * max(x1 - x0, y1 - y0)

    fig, ax = plt.subplots(figsize=(6.6, 6.6))
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(x0 - m, x1 + m); ax.set_ylim(y0 - m, y1 + m)
    title = ax.set_title("", fontsize=10)
    counter = ax.text(0.02, 0.98, "", transform=ax.transAxes, va="top", fontsize=10, color=COLORS["guide"])
    holder = {"arts": []}

    def update(i):
        for a in holder["arts"]:
            a.remove()
        kind, val = frames[i]
        if kind == "tri":
            holder["arts"] = _fill(ax, tri, CORE, "none", 0.0)
            title.set_text("Start: equilateral triangle (a segment in every 60 deg direction)")
            counter.set_text("")
        elif kind == "subdiv":
            arts = _fill(ax, tri, CORE, "none", 0.0)
            for p in subdivided()[:: max(1, 2 ** N // 24)]:
                xy = np.array(p.exterior.coords)
                ln, = ax.plot([xy[:2, 0].mean(), APEX[0]], [xy[:2, 1].mean(), APEX[1]], color=COLORS["muted"], lw=0.4)
                arts.append(ln)
            holder["arts"] = arts
            title.set_text(f"Divide the base into 2^{N} triangles (shared apex)")
            counter.set_text("")
        elif kind == "sprout":
            shape = sprout(val)
            holder["arts"] = _fill(ax, shape, CORE, "none", 0.0)
            title.set_text("Slide the pieces to overlap: area shrinks, directions kept")
            counter.set_text(f"area = {shape.area / tri_area * 100:.0f}% of the triangle")
        else:
            a1, a2, nvis = val
            arts = _fill(ax, tree, CORE, "none", 0.0, alpha=0.55, z=2)
            if nvis >= 2:
                arts += _fill(ax, shp_rotate(tree, a1, origin=(c.x, c.y)), CORE, "none", 0.0, alpha=0.55, z=3)
            if nvis >= 3:
                arts += _fill(ax, shp_rotate(tree, a2, origin=(c.x, c.y)), CORE, "none", 0.0, alpha=0.55, z=4)
            holder["arts"] = arts
            title.set_text("Union three trees rotated 120 deg: a Besicovitch set (all directions)")
            counter.set_text(f"copies: {nvis}/3")
        return holder["arts"] + [title, counter]

    anim = FuncAnimation(fig, update, frames=len(frames), interval=140, blit=False)
    print("wrote", save_gif(anim, fps=10, dpi=105))


if __name__ == "__main__":
    main()
