"""Kakeya needle set as a density glow (method 7).

Samples points along the whole needle family (solid triangular core + three 120-degree corner
fans + edge fringe), bins them into a 2D histogram, and imshows the accumulation with a warm
dark->#f4e37a colormap so overlapping needles glow. Three-fold symmetric; a needle in every
direction.

Run: uv run --with matplotlib --with shapely --with pillow python research/kakeya/figures/2_kakeya_2d/2_6_7_density_glow.py
"""
import math

import numpy as np
from _shared import math_check, save_preview

SIDE = 1.0
R = SIDE / math.sqrt(3.0)
CORNERS_DEG = (90.0, 210.0, 330.0)
LEN_CORNER, LEN_EDGE = 0.74, 0.52
HALFW = 0.009                       # needle half-width (perp jitter in the density)
JF, KF = 210, 95                    # needles per corner fan / per edge
CORE = "#f4e37a"
GRID = 1200
STEP = 0.0010                       # spacing of samples along a needle
CORE_LEVEL = 0.82                   # brightness of the solid core plateau (0..1)
BLUR_SIGMA = 1.1                    # gaussian glow radius, in grid cells

VERTS = np.array([R * np.array([math.cos(math.radians(d)), math.sin(math.radians(d))]) for d in CORNERS_DEG])


def _unit(deg):
    return np.array([math.cos(math.radians(deg)), math.sin(math.radians(deg))])


def _segments():
    """(base, tip) endpoints for every needle: three corner fans + an outward edge fringe."""
    rng = np.random.default_rng(7)
    cen = VERTS.mean(0)
    segs = []
    for d0 in CORNERS_DEG:                       # corner fans: full turn once tripled
        v = R * _unit(d0)
        for th in np.linspace(d0 - 60, d0 + 60, JF):
            segs.append((v, v + LEN_CORNER * (0.60 + 0.62 * rng.random()) * _unit(th)))
    for a, b in ((VERTS[0], VERTS[1]), (VERTS[1], VERTS[2]), (VERTS[2], VERTS[0])):
        nrm = np.array([(b - a)[1], -(b - a)[0]])
        nrm = nrm / np.linalg.norm(nrm)
        if np.dot(nrm, (a + b) / 2 - cen) < 0:
            nrm = -nrm
        for t in np.linspace(0.03, 0.97, KF):
            base = a + t * (b - a)
            segs.append((base, base + LEN_EDGE * (0.35 + 0.9 * rng.random()) * nrm))
    return segs


def _needle_points(segs, rng):
    """Sample points along each needle with a little perpendicular spread (its width)."""
    xs, ys = [], []
    for base, tip in segs:
        d = tip - base
        length = np.linalg.norm(d)
        n = max(int(length / STEP), 2)
        t = np.linspace(0.0, 1.0, n)
        pts = base + np.outer(t, d)
        perp = np.array([-d[1], d[0]]) / length
        pts = pts + np.outer(rng.uniform(-HALFW, HALFW, n), perp)
        xs.append(pts[:, 0]); ys.append(pts[:, 1])
    return np.concatenate(xs), np.concatenate(ys)


def _core_mask(x0, x1, y0, y1):
    """Boolean grid (row=y, col=x) marking cells inside the core triangle."""
    xc = x0 + (np.arange(GRID) + 0.5) * (x1 - x0) / GRID
    yc = y0 + (np.arange(GRID) + 0.5) * (y1 - y0) / GRID
    gx, gy = np.meshgrid(xc, yc)
    inside = np.ones_like(gx, dtype=bool)
    for p, q in ((VERTS[0], VERTS[1]), (VERTS[1], VERTS[2]), (VERTS[2], VERTS[0])):
        side = (q[0] - p[0]) * (gy - p[1]) - (q[1] - p[1]) * (gx - p[0])
        inside &= side <= 1e-9 if _clockwise() else side >= -1e-9
    return inside


def _clockwise():
    (ax, ay), (bx, by), (cx, cy) = VERTS
    return (bx - ax) * (cy - ay) - (by - ay) * (cx - ax) < 0


def _blur(a, sigma):
    """Separable gaussian blur with numpy only (glow)."""
    r = max(int(3 * sigma), 1)
    k = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma) ** 2)
    k /= k.sum()
    a = np.apply_along_axis(lambda m: np.convolve(m, k, mode="same"), 1, a)
    a = np.apply_along_axis(lambda m: np.convolve(m, k, mode="same"), 0, a)
    return a


def _glow_cmap():
    from matplotlib.colors import LinearSegmentedColormap

    return LinearSegmentedColormap.from_list(
        "kakeya_glow",
        [(0.00, "#0b0b12"), (0.14, "#2f2708"), (0.34, "#8a7220"),
         (0.62, CORE), (0.86, "#faf0a6"), (1.00, "#fffde8")],
    )


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(11)
    segs = _segments()
    px, py = _needle_points(segs, rng)

    m = 0.06
    x0, x1 = px.min() - m, px.max() + m
    y0, y1 = py.min() - m, py.max() + m
    span = max(x1 - x0, y1 - y0)
    xc, yc = (x0 + x1) / 2, (y0 + y1) / 2
    x0, x1 = xc - span / 2, xc + span / 2
    y0, y1 = yc - span / 2, yc + span / 2

    hist, _, _ = np.histogram2d(px, py, bins=GRID, range=[[x0, x1], [y0, y1]])
    dens = np.sqrt(hist.T)                             # (row=y, col=x); sqrt lifts faint tips
    dens = np.clip(dens / np.percentile(dens[dens > 0], 99.3), 0.0, 1.0)
    dens = np.maximum(dens, CORE_LEVEL * _core_mask(x0, x1, y0, y1))   # solid glowing core
    dens = _blur(dens, BLUR_SIGMA)
    dens = np.clip(dens / dens.max(), 0.0, 1.0)

    cmap = _glow_cmap()
    fig, ax = plt.subplots(figsize=(6.6, 6.6))
    fig.patch.set_facecolor(cmap(0.0))
    ax.set_position([0, 0, 1, 1]); ax.set_aspect("equal"); ax.axis("off")
    ax.imshow(dens, origin="lower", extent=(x0, x1, y0, y1), cmap=cmap,
              interpolation="bilinear", vmin=0.0, vmax=1.0)

    math_check(
        "Kakeya needle set as a density glow (method 7)",
        [
            ("family", f"{len(segs)} needles: 3 corner fans ({JF} each) + edge fringe ({KF}/edge)"),
            ("coverage", "the three 120-degree corner fans tile the full turn: a needle in every direction"),
            ("render", f"{GRID}x{GRID} histogram, sqrt-compressed, warm dark->{CORE} glow colormap"),
            ("symmetry", "three-fold (corners at 90/210/330 deg)"),
        ],
    )
    print("wrote", save_preview(fig, dpi=170))


if __name__ == "__main__":
    main()
