"""Animation: the non-convex answers, a unit needle turning in deltoid -> Perron tree -> Besicovitch star.

The concave counterpart of 2_1_3 (kakeya.md 2b-2e). Dropping convexity lets the footprint keep falling
while the needle still points in every direction:

  deltoid (3 concave cusps)            area pi/8      needle tangent, turning
  Perron tree (sprouted triangle)      area smaller   needle lies along each branch; footprint shrinks
  Besicovitch star (three trees)       area -> 0       the six-pointed star covers every direction

In each panel the needle is a real unit chord of the shape for its direction, never pivoting about a
single point. In the deltoid it stays tangent (constant chord); in the tree and star it sits along the
branch that carries that direction, so as the direction sweeps the needle both translates (its tip runs
along the branch tips) and rotates. The article's optimal small-area star (kakeya12/13) uses a petal
construction not reproduced here; the turnable star drawn is the Besicovitch one.

Run: PYTHONPATH=research/kakeya/figures uv run --with matplotlib --with shapely --with pillow \
     python research/kakeya/figures/2_kakeya_2d/2_1_4_nonconvex_answers_anim.py
"""

import math

import numpy as np
from _shared import COLORS, deltoid, math_check, poly, save_gif
from shapely.affinity import rotate as shp_rotate
from shapely.affinity import translate as shp_translate
from shapely.geometry import LineString, Polygon
from shapely.ops import unary_union

STEPS = 40
END_HOLD = 9

# Deltoid: tangent needle (constant chord 4b = 1)
B = 0.25
DELT = poly(deltoid(B, 400))
if not DELT.is_valid:
    DELT = DELT.buffer(0)


def _delt_pt(t):
    return np.array([2 * B * math.cos(t) + B * math.cos(2 * t), 2 * B * math.sin(t) - B * math.sin(2 * t)])


def _delt_dir(t):
    d = np.array([-2 * B * math.sin(t) - 2 * B * math.sin(2 * t), 2 * B * math.cos(t) - 2 * B * math.cos(2 * t)])
    n = np.linalg.norm(d)
    return None if n < 1e-4 else d / n


def deltoid_needles():
    out = []
    for t in np.linspace(0.03, 2 * math.pi + 0.03, STEPS, endpoint=False):
        d = _delt_dir(t)
        if d is None:
            continue
        p = _delt_pt(t)
        chord = DELT.intersection(LineString([tuple(p - 3 * d), tuple(p + 3 * d)]))
        seg = None
        if chord.geom_type == "LineString" and chord.length > 0.5:
            seg = chord
        elif chord.geom_type == "MultiLineString" and len(chord.geoms):
            longest = max(chord.geoms, key=lambda g: g.length)
            seg = longest if longest.length > 0.5 else None
        if seg is not None:
            xy = np.array(seg.coords)
            out.append((xy[0], xy[-1]))
    return out


# Height-1 equilateral triangle: unit needles from the apex fit
APEX = np.array([0.0, 1.0])
HB = 1.0 / math.sqrt(3.0)  # half base; corners (+-HB, 0), side = apex..corner = 2/sqrt3
NLEV = 6
TRI = Polygon([(-HB, 0.0), (HB, 0.0), tuple(APEX)])
TRI_AREA = TRI.area
AR = math.atan2(-1.0, HB)  # apex -> right corner direction angle
AL = math.atan2(-1.0, -HB)  # apex -> left corner


def sprout_pieces(alpha=0.6):
    xs = np.linspace(-HB, HB, 2**NLEV + 1)
    pieces = [[Polygon([(xs[i], 0.0), (xs[i + 1], 0.0), tuple(APEX)])] for i in range(2**NLEV)]
    w = 2 * HB / 2**NLEV
    for _ in range(NLEV):
        step = 0.5 * alpha * w
        pieces = [
            [shp_translate(p, xoff=+step) for p in pieces[i]] + [shp_translate(p, xoff=-step) for p in pieces[i + 1]]
            for i in range(0, len(pieces), 2)
        ]
        w *= 1.0 + alpha
    return [p for g in pieces for p in g]


def branch_needle(piece):
    """A unit needle lying along a sub-triangle's branch: from its (translated) apex, one unit toward
    its base midpoint. It is a real chord of the piece (in the original orientation, apex up), so a real
    chord of the tree, pointing in that branch's direction. Length exactly 1."""
    xy = np.array(piece.exterior.coords)[:-1]
    apex = xy[np.argmax(xy[:, 1])]
    basemid = xy[xy[:, 1] < 0.5].mean(axis=0)
    d = basemid - apex
    d = d / np.linalg.norm(d)
    return apex, apex + d


def _needle_dir(ab):
    return math.atan2(ab[1][1] - ab[0][1], ab[1][0] - ab[0][0]) % math.pi  # direction in [0, pi)


def rot_needle(ab, deg, ctr):
    th = math.radians(deg)
    cs, sn = math.cos(th), math.sin(th)
    rot = np.array([[cs, -sn], [sn, cs]])
    return tuple(rot @ (np.asarray(p) - ctr) + ctr for p in ab)


def main():
    dN = deltoid_needles()
    tree_pieces = sprout_pieces()
    tree = unary_union(tree_pieces)
    c = tree.centroid
    pv = np.array([c.x, c.y])
    besic_pieces = [shp_rotate(p, a, origin=(c.x, c.y)) for a in (0, 120, 240) for p in tree_pieces]
    besic = unary_union(besic_pieces)
    tree_nd = [branch_needle(p) for p in tree_pieces]
    pN = sorted(tree_nd, key=_needle_dir)
    bN = sorted((rot_needle(ab, r, pv) for r in (0, 120, 240) for ab in tree_nd), key=_needle_dir)

    areas = (math.pi / 8, tree.area, besic.area)
    dlen = [np.linalg.norm(b - a) for a, b in dN]
    assert min(dlen) > 0.9 and max(dlen) < 1.1, f"deltoid chord ~1, got [{min(dlen):.3f},{max(dlen):.3f}]"
    for a, b in pN + bN:
        assert abs(np.linalg.norm(b - a) - 1.0) < 1e-9, "tree/besic branch needles must have length 1"
    for name, shp, nd in (("tree", tree, pN), ("star", besic, bN)):
        buffered = shp.buffer(1e-6)
        assert all(buffered.contains(LineString([tuple(a), tuple(b)])) for a, b in nd), (
            f"every {name} branch needle must lie inside the shape"
        )
    tree_deg = math.degrees(max(map(_needle_dir, pN)) - min(map(_needle_dir, pN)))
    star_bins = {round(math.degrees(_needle_dir(ab))) % 180 for ab in bN}
    assert len(star_bins) > 90, f"star needles must sample most directions ({len(star_bins)}/180)"

    math_check(
        "non-convex answers: deltoid -> Perron tree -> Besicovitch star (needles lie in real branches)",
        [
            ("deltoid", f"area pi/8 = {areas[0]:.3f}, tangent chord 4b = 1"),
            ("Perron tree", f"area {areas[1]:.3f}  (= {areas[1] / TRI_AREA * 100:.0f}% of the triangle)"),
            ("Besicovitch star", f"area {areas[2]:.3f} (finite level; true limit 0)"),
            ("tree fan", f"branch needles span {tree_deg:.0f} degrees; each a real unit chord of the tree"),
            ("star directions", f"{len(star_bins)}/180 one-degree bins hit (a unit segment in every direction)"),
        ],
    )

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    tris = {  # faint underlying triangle(s) that the needle fan lives in
        1: [np.array(TRI.exterior.coords)],
        2: [np.array(shp_rotate(TRI, a, origin=(c.x, c.y)).exterior.coords) for a in (0, 120, 240)],
    }
    shapes = [DELT, tree, besic]
    needles = [dN, pN, bN]
    titles = [
        f"deltoid\narea pi/8 = {areas[0]:.3f}",
        f"Perron tree\narea {areas[1]:.3f} ({areas[1] / TRI_AREA * 100:.0f}% of triangle)",
        f"Besicovitch star (3 trees)\narea {areas[2]:.3f} -> 0 in the limit",
    ]
    lims = [(-0.85, 0.85, -0.8, 0.8), (-0.95, 0.95, -0.2, 1.15), (-1.25, 1.25, -1.25, 1.25)]
    nframes = max(len(n) for n in needles)
    frames = list(range(nframes)) + [nframes - 1] * END_HOLD

    def update(fi):
        k = frames[fi]
        for j, ax in enumerate(axes):
            ax.cla()
            ax.set_aspect("equal")
            ax.axis("off")
            ax.set_xlim(lims[j][0], lims[j][1])
            ax.set_ylim(lims[j][2], lims[j][3])
            if j in tris:  # faint underlying triangle(s)
                for tr in tris[j]:
                    ax.plot(tr[:, 0], tr[:, 1], color=COLORS["muted"], lw=0.8, ls="--", alpha=0.7)
            g = shapes[j]
            for gg in g.geoms if g.geom_type == "MultiPolygon" else [g]:
                ax.fill(*gg.exterior.xy, facecolor=COLORS["region"], edgecolor=COLORS["outer"], lw=0.9, alpha=0.6)
            lst = needles[j]
            upto = min(k + 1, len(lst))
            for a, b in lst[:upto]:
                ax.plot([a[0], b[0]], [a[1], b[1]], color=COLORS["needle"], lw=0.7, alpha=0.28)
            a, b = lst[upto - 1]
            ax.plot([a[0], b[0]], [a[1], b[1]], color=COLORS["accent"], lw=2.6, zorder=4)
            ax.set_title(titles[j], fontsize=10)
        return []

    fig, axes = plt.subplots(1, 3, figsize=(13.2, 5.2))
    anim = FuncAnimation(fig, update, frames=len(frames), interval=95, blit=False)
    print("wrote", save_gif(anim, fps=12, dpi=92))


if __name__ == "__main__":
    main()
