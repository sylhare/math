"""Kakeya needle set drawn as a line-drawing sunburst (no fill).

Same geometry as the filled needle-set figure (solid triangular core, Perron-tree corner sprays,
edge fringe) but every needle is a thin yellow LINE. Body is filled by dense vertex->opposite-edge
fans; the three corner fans and the edge fringes give the outward rays. Three-fold symmetric.

Run: PYTHONPATH=research/kakeya/figures uv run --with matplotlib --with shapely --with pillow \
     python research/kakeya/figures/2_kakeya_2d/2_6_2_fan_fringe_rays.py
"""
import math

import numpy as np
from _shared import math_check, save_preview

SIDE = 1.0
R = SIDE / math.sqrt(3.0)
CORNERS_DEG = (90.0, 210.0, 330.0)
YELLOW = "#f4e37a"

LEN_CORNER = 0.62
LEN_EDGE_MID, LEN_EDGE_END = 0.22, 0.46   # fringe length: short mid-edge, long near corners
FAN_HALF = 74                             # corner-fan half angle (deg); wide enough to close wedges
JF, KF = 74, 40                           # corner-fan rays per corner / fringe rays per edge
BODY_N = 260                              # vertex->opposite-edge lines per corner (fill the core)
BULGE = 0.045                             # outward bow of the core edges (rounded body)

VERTS = np.array([R * np.array([math.cos(math.radians(d)), math.sin(math.radians(d))]) for d in CORNERS_DEG])
CEN = VERTS.mean(0)


def _unit(deg):
    return np.array([math.cos(math.radians(deg)), math.sin(math.radians(deg))])


def body_segments():
    """Fan every vertex to its opposite edge (bowed outward): overlaid fans fill a rounded core."""
    segs = []
    for i, v in enumerate(VERTS):
        a, b = VERTS[(i + 1) % 3], VERTS[(i + 2) % 3]
        nrm = np.array([(b - a)[1], -(b - a)[0]])
        nrm = nrm / np.linalg.norm(nrm)
        if np.dot(nrm, (a + b) / 2 - CEN) < 0:
            nrm = -nrm
        for t in np.linspace(0.0, 1.0, BODY_N):
            p = a + t * (b - a) + BULGE * math.sin(math.pi * t) * nrm
            segs.append([v, p])
    return segs


def corner_segments(rng):
    """Perron-tree corner sprays: a fan of outward rays over d0 +/- 60 at each vertex."""
    segs = []
    for d0 in CORNERS_DEG:
        v = R * _unit(d0)
        for th in np.linspace(d0 - FAN_HALF, d0 + FAN_HALF, JF):
            length = LEN_CORNER * (0.72 + 0.5 * rng.random())
            segs.append([v, v + length * _unit(th)])
    return segs


def fringe_segments(rng):
    """Outward-normal needle fringe along each edge."""
    segs = []
    for a, b in ((VERTS[0], VERTS[1]), (VERTS[1], VERTS[2]), (VERTS[2], VERTS[0])):
        nrm = np.array([(b - a)[1], -(b - a)[0]])
        nrm = nrm / np.linalg.norm(nrm)
        if np.dot(nrm, (a + b) / 2 - CEN) < 0:
            nrm = -nrm
        for t in np.linspace(0.06, 0.94, KF):
            base = a + t * (b - a)
            grade = LEN_EDGE_MID + (LEN_EDGE_END - LEN_EDGE_MID) * abs(t - 0.5) * 2.0
            length = grade * (0.8 + 0.4 * rng.random())
            segs.append([base, base + length * nrm])
    return segs


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection

    rng = np.random.default_rng(7)
    body = body_segments()
    corners = corner_segments(rng)
    fringe = fringe_segments(rng)

    math_check(
        "Kakeya needle set as a line-drawing sunburst (no fill)",
        [
            ("body", f"3 vertex->opposite-edge fans, {BODY_N} lines each (solid core, lines only)"),
            ("corner sprays", f"{JF} rays over d0 +/- {FAN_HALF} at each of 3 corners"),
            ("edge fringe", f"{KF} outward-normal rays per edge"),
            ("coverage", "corner fans span the full turn: a needle in every direction"),
            ("symmetry", "three-fold about the centroid"),
        ],
    )

    all_pts = np.array([p for seg in body + corners + fringe for p in seg])
    (x0, y0), (x1, y1) = all_pts.min(0), all_pts.max(0)
    m = 0.06 * max(x1 - x0, y1 - y0)

    fig, ax = plt.subplots(figsize=(6.6, 6.6))
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(x0 - m, x1 + m)
    ax.set_ylim(y0 - m, y1 + m)

    # Body: dense overlapping lines saturate to a solid yellow core.
    lc_body = LineCollection(body, colors=YELLOW, linewidths=1.1, alpha=0.5, capstyle="round")
    lc_body.set_rasterized(True)
    ax.add_collection(lc_body)
    # Rays: thin needles reading individually against white.
    lc_rays = LineCollection(corners + fringe, colors=YELLOW, linewidths=0.9, alpha=0.85, capstyle="round")
    lc_rays.set_rasterized(True)
    ax.add_collection(lc_rays)

    print("wrote", save_preview(fig, dpi=170))


if __name__ == "__main__":
    main()
