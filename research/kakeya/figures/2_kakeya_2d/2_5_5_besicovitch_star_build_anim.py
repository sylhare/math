"""Animation: building the six-pointed Besicovitch star from rotated Perron trees (kakeya.md 2e).

One Perron tree carries a unit segment in every direction of a 60-degree fan. Rotating copies of it
about a common centre spreads that fan around the circle: three copies (0, 60, 120 degrees) already
cover all 180 degrees of directions, and six copies (every 60 degrees) close up into the symmetric
six-pointed star. Each rotated tree still has area heading to zero, so their union is a Besicovitch set:
a set of arbitrarily small area holding a unit segment in every direction.

Shown in parts, then applied in full:
  1. one tree   a single Perron tree; the needle sweeps its 60-degree fan.
  2. rotate     copies drop in every 60 degrees; each adds a star point and a fresh band of directions.
  3. full       the finished six-pointed star; the needle sweeps every direction, 0..180.

Run: PYTHONPATH=research/kakeya/figures uv run --with matplotlib --with shapely --with pillow \
     python research/kakeya/figures/2_kakeya_2d/2_5_5_besicovitch_star_build_anim.py
"""

import math

import numpy as np
from _shared import COLORS, math_check, save_gif
from shapely.affinity import rotate as shp_rotate
from shapely.affinity import translate as shp_translate
from shapely.geometry import Polygon
from shapely.ops import unary_union

APEX = np.array([0.0, 1.0])
HB = 1.0 / math.sqrt(3.0)
NLEV = 5
ALPHA = 0.6
ROTS = [0, 60, 120, 180, 240, 300]  # six copies -> symmetric six-pointed star


def sprout_pieces(alpha=ALPHA):
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
    xy = np.array(piece.exterior.coords)[:-1]
    apex = xy[np.argmax(xy[:, 1])]
    basemid = xy[xy[:, 1] < 0.5].mean(axis=0)
    d = basemid - apex
    return apex, d / np.linalg.norm(d)


def _dir(ab):
    return math.atan2(ab[1][1] - ab[0][1], ab[1][0] - ab[0][0]) % math.pi


def rot_needle(ab, deg, ctr):
    th = math.radians(deg)
    cs, sn = math.cos(th), math.sin(th)
    rot = np.array([[cs, -sn], [sn, cs]])
    return tuple(rot @ (np.asarray(p) - ctr) + ctr for p in ab)


def covered_bins(rot_list, base_dirs):
    """Directions (1-degree bins in [0,180)) covered by the rotated fans. The fan is a CONTINUOUS range
    [min, max] of the base branch directions, so fill the whole range per rotation, not just samples."""
    lo, hi = math.degrees(min(base_dirs)), math.degrees(max(base_dirs))
    bins = set()
    for r in rot_list:
        for d in range(math.floor(lo + r), math.ceil(hi + r) + 1):
            bins.add(d % 180)
    return bins


def main():
    pieces = sprout_pieces()
    tree = unary_union(pieces)
    c = tree.centroid
    ctr = np.array([c.x, c.y])
    trees = [shp_rotate(tree, r, origin=(c.x, c.y)) for r in ROTS]
    star = unary_union(trees)

    base_nd = [branch_needle(p) for p in pieces]
    base_dirs = [math.atan2(u[1], u[0]) for _, u in base_nd]
    tree_nd = [(t, t + u) for t, u in base_nd]  # (A, B) needles of the base tree
    all_nd = sorted((rot_needle(ab, r, ctr) for r in ROTS for ab in tree_nd), key=_dir)

    cov_after = [len(covered_bins(ROTS[: k + 1], base_dirs)) for k in range(len(ROTS))]
    assert cov_after[2] >= 170, f"three copies must already cover ~all directions (got {cov_after[2]}/180)"

    math_check(
        "build the six-pointed Besicovitch star",
        [
            ("one tree", f"{len(pieces)} branches, 60-degree fan, area {tree.area:.3f}"),
            ("three copies", f"cover {cov_after[2]}/180 directions (0, 60, 120 degrees)"),
            ("six copies", f"cover {cov_after[5]}/180, symmetric six-pointed star, area {star.area:.3f}"),
            ("still Besicovitch", "each tree area -> 0 in the limit; the union holds a segment in every direction"),
        ],
    )

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    def fill(geom, alpha, z=2, ec=None):
        for g in geom.geoms if geom.geom_type == "MultiPolygon" else [geom]:
            if not g.is_empty:
                ax.fill(
                    *g.exterior.xy,
                    facecolor=COLORS["region"],
                    edgecolor=ec or COLORS["outer"],
                    lw=0.7,
                    alpha=alpha,
                    zorder=z,
                )

    ONE, DROP, SWEEP, FULL, END = len(tree_nd), 6, 10, len(all_nd), 12
    frames = [("one", i) for i in range(ONE)]
    for k in range(1, len(ROTS)):  # dropping in copies 2..6, each followed by a short local sweep
        frames += [("drop", (k, f / (DROP - 1))) for f in range(DROP)]
        frames += [("band", (k, f / (SWEEP - 1))) for f in range(SWEEP)]
    frames += [("full", i) for i in range(FULL)]
    frames += [("full", FULL - 1)] * END

    pts = np.array(star.envelope.exterior.coords)
    (x0, y0), (x1, y1) = pts.min(0), pts.max(0)
    mg = 0.08 * max(x1 - x0, y1 - y0)

    fig, ax = plt.subplots(figsize=(6.8, 7.0))

    def setup():
        ax.cla()
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(x0 - mg, x1 + mg)
        ax.set_ylim(y0 - mg, y1 + mg)

    def gauge(nbins, extra=""):
        ax.text(
            0.02,
            0.98,
            f"directions covered: {nbins}/180{extra}",
            transform=ax.transAxes,
            va="top",
            fontsize=10,
            color=COLORS["guide"],
        )

    def update(fi):
        kind, val = frames[fi]
        setup()
        if kind == "one":
            fill(trees[0], 0.55)
            for a, b in tree_nd[: val + 1]:
                ax.plot([a[0], b[0]], [a[1], b[1]], color=COLORS["needle"], lw=0.7, alpha=0.28)
            a, b = tree_nd[val]
            ax.plot([a[0], b[0]], [a[1], b[1]], color=COLORS["accent"], lw=2.6, zorder=4)
            gauge(round(60 * (val + 1) / ONE))
            ax.set_title("1. one Perron tree: a 60-degree fan of directions", fontsize=12)
        elif kind == "drop":
            k, f = val
            for j in range(k):
                fill(trees[j], 0.5)
            fill(trees[k], 0.15 + 0.4 * f, z=3)  # the arriving copy fades in
            gauge(cov_after[k - 1])
            ax.set_title(f"2. rotate a copy {ROTS[k]} degrees: a new star point", fontsize=12)
        elif kind == "band":
            k, f = val
            for j in range(k + 1):
                fill(trees[j], 0.5)
            band = sorted((rot_needle(ab, ROTS[k], ctr) for ab in tree_nd), key=_dir)
            upto = max(1, int(f * len(band)))
            for a, b in band[:upto]:
                ax.plot([a[0], b[0]], [a[1], b[1]], color=COLORS["needle"], lw=0.7, alpha=0.3)
            a, b = band[upto - 1]
            ax.plot([a[0], b[0]], [a[1], b[1]], color=COLORS["accent"], lw=2.6, zorder=4)
            gauge(cov_after[k])
            ax.set_title(f"2. the new copy adds a fresh band of directions ({k + 1} of 6 copies)", fontsize=11)
        else:
            for t in trees:
                fill(t, 0.5)
            for a, b in all_nd[: val + 1]:
                ax.plot([a[0], b[0]], [a[1], b[1]], color=COLORS["needle"], lw=0.5, alpha=0.16)
            a, b = all_nd[val]
            ax.plot([a[0], b[0]], [a[1], b[1]], color=COLORS["accent"], lw=2.6, zorder=5)
            gauge(cov_after[5], f"   dir = {round(math.degrees(_dir(all_nd[val])))} deg")
            ax.set_title("3. six-pointed Besicovitch star: a needle in every direction", fontsize=12)
        return []

    anim = FuncAnimation(fig, update, frames=len(frames), interval=95, blit=False)
    print("wrote", save_gif(anim, fps=11, dpi=95))


if __name__ == "__main__":
    main()
