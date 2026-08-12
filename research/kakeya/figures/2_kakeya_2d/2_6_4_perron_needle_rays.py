"""Kakeya needle set drawn as the Perron-tree needle family (method 4: perron_needle_rays).

Builds a real Perron tree (base of an equilateral triangle split into 2^n slivers joined to a
shared apex, then sprouted). Each sliver's needle direction is base-midpoint -> apex; these 2^n
directions span the tree's 60 deg fan and bunch toward the fan edges. Six copies rotated about the
centroid give a needle in every direction. Each needle is extended to a unit ray and anchored on the
boundary of a solid triangular core along its own direction: many directions pile onto the three
corners (wide sprays) while a flat edge keeps only its single normal (thin fringe). Single yellow
fill, no borders; resembles Wikimedia KakeyaNeedleSet3.GIF.

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/2_kakeya_2d/2_6_4_perron_needle_rays.py
"""
import math

import numpy as np
from _shared import math_check, save_preview
from shapely.geometry import Polygon

N = 6                                  # 2^N = 64 slivers per tree
YELLOW = "#f4e37a"
R = 1.0 / math.sqrt(3.0)               # circumradius (centroid at origin)
CORNERS_DEG = (90.0, 210.0, 330.0)     # solid core: apex up, three-fold
OFFSET = 30.0                          # rotate the 6 tree copies so their dense fan edges land on corners
SPREAD = 68.0                          # each corner collects directions within +-SPREAD of its bisector
L_SPRAY = 1.05 * R                     # corner ray length (along the bisector paintbrush)
L_FRINGE = 0.42 * R                    # edge fringe ray length (mid-edge)
HALFW = 0.006 * R                      # needle half-width at its base (tapers to a point)


def perron_directions(n):
    """Angles (deg) of the 2^n Perron slivers: base-midpoint -> shared apex, spanning a 60 deg fan."""
    xs = np.linspace(-0.5, 0.5, 2 ** n + 1)
    mids = 0.5 * (xs[:-1] + xs[1:])
    apex_y = math.sqrt(3.0) / 2.0
    return np.degrees(np.arctan2(apex_y, -mids))       # 60..120 deg, bunched toward the edges


def core_polygon():
    verts = [(R * math.cos(math.radians(d)), R * math.sin(math.radians(d))) for d in CORNERS_DEG]
    return Polygon(verts).buffer(0.02, join_style=1)   # barely rounded corners


def _sliver(anchor, theta, length):
    d = np.array([math.cos(theta), math.sin(theta)])
    perp = np.array([-d[1], d[0]]) * HALFW
    return np.array([anchor - perp, anchor + perp, anchor + length * d])


def corner_sprays(rng):
    """Six rotated Perron copies -> 360 deg of needles; each pivots about its nearest corner.

    The copies are offset so the trees' dense fan edges land on the corner bisectors: each corner
    gets a tight, long paintbrush along its outward bisector that thins and shortens toward the
    edges. A corner collects every direction within SPREAD of its bisector.
    """
    thetas = np.radians(np.concatenate([perron_directions(N) + 60.0 * k + OFFSET for k in range(6)]))
    bis = [math.radians(d) for d in CORNERS_DEG]
    verts = [R * np.array([math.cos(b), math.sin(b)]) for b in bis]
    slivers = []
    for theta in thetas:
        k = int(np.argmin([abs(math.atan2(math.sin(theta - b), math.cos(theta - b))) for b in bis]))
        off = math.atan2(math.sin(theta - bis[k]), math.cos(theta - bis[k]))   # radians, |.| <= 60 deg
        taper = math.cos(0.5 * math.pi * off / math.radians(SPREAD)) ** 2      # 1 at bisector, 0 at edge
        length = L_SPRAY * (0.42 + 0.58 * taper) * (0.82 + 0.30 * rng.random())
        slivers.append(_sliver(verts[k], theta, length))
    return slivers


def edge_fringe(rng):
    """Short outward comb along each edge: perpendicular needles, shortest at mid-edge."""
    fan = np.radians(perron_directions(N) - 90.0)      # -30..30 deg spread about the normal
    verts = [R * np.array([math.cos(math.radians(d)), math.sin(math.radians(d))]) for d in CORNERS_DEG]
    slivers = []
    for a, b in ((verts[0], verts[1]), (verts[1], verts[2]), (verts[2], verts[0])):
        e = b - a
        nrm = np.array([e[1], -e[0]])
        nrm = nrm / np.linalg.norm(nrm)               # outward normal (centroid at origin)
        base_ang = math.atan2(nrm[1], nrm[0])
        for t in np.linspace(0.10, 0.90, 40):
            lean = math.radians(42.0) * (t - 0.5) * 2.0         # grazing: lean toward the nearer corner
            theta = base_ang + lean + 0.30 * fan[rng.integers(len(fan))]
            grow = 0.30 + 0.70 * (2.0 * abs(t - 0.5)) ** 1.5    # longer toward the corners
            length = L_FRINGE * grow * (0.8 + 0.4 * rng.random())
            slivers.append(_sliver(a + t * e, theta, length))
    return slivers


def build_needles():
    rng = np.random.default_rng(11)
    core = core_polygon()
    slivers = corner_sprays(rng) + edge_fringe(rng)
    return core, slivers


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.collections import PolyCollection
    from matplotlib.patches import Polygon as MplPolygon

    core, slivers = build_needles()

    math_check(
        "Perron needle-ray set (method 4)",
        [
            ("Perron tree", f"2^{N} = {2 ** N} slivers, base-midpoint -> apex directions"),
            ("fan", f"one tree spans {np.ptp(perron_directions(N)):.0f} deg, bunched toward the edges"),
            ("full turn", f"6 rotated copies -> {6 * 2 ** N} corner needles covering every direction"),
            ("symmetry", "wide sprays at the 3 corners, thin fringe along the 3 edges (three-fold)"),
        ],
    )

    fig, ax = plt.subplots(figsize=(6.7, 5.9))
    ax.set_aspect("equal")
    ax.axis("off")

    xy = np.array(core.exterior.coords)
    ax.add_patch(MplPolygon(xy, closed=True, facecolor=YELLOW, edgecolor="none", zorder=2))
    ax.add_collection(PolyCollection(slivers, facecolors=YELLOW, edgecolors="none", zorder=1))

    m = 1.55 * R
    ax.set_xlim(-m, m)
    ax.set_ylim(-1.15 * R, 1.75 * R)
    print("wrote", save_preview(fig, dpi=150))


if __name__ == "__main__":
    main()
