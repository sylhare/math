"""Figure: Hausdorff dimension via self-similar fractals (section 3b of ../kakeya.md).

Hausdorff measure and dimension. For s >= 0,

    H^s_delta(E) = inf { sum_i (diam U_i)^s : E in union U_i, diam U_i <= delta },
    H^s(E)       = lim_{delta -> 0+} H^s_delta(E),

and the Hausdorff dimension is the single threshold s where H^s jumps from infinity to 0:

    dim_H E = inf { s >= 0 : H^s(E) = 0 } = sup { s >= 0 : H^s(E) = infinity }.

Always  dim_H E <= dim_box E  (Hausdorff is the finer, smaller-or-equal notion).

Self-similar dimension. If a set is N copies of itself each scaled by 1/r, then dim = log N / log r:

    Cantor middle-thirds:  N=2, r=3   dim = log 2 / log 3 ~ 0.6309
    Sierpinski triangle:   N=3, r=2   dim = log 3 / log 2 ~ 1.5850
    Koch curve:            N=4, r=3   dim = log 4 / log 3 ~ 1.2619

No reference image. STANDARD REPRESENTATION: three stacked panels rendering the three classic
fractals to a few iterations (Cantor as a stack of shrinking segment-levels, Sierpinski as removed
triangles, Koch as the polyline). The Sierpinski panel is additionally box-counted at several delta
and the log-log slope is fit; it reproduces log 3 / log 2 ~ 1.585, showing dim_H = dim_box for a
self-similar set (the safe place where the two notions agree, before Kakeya makes them bite).

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/dimension_fractal.py
"""
import math
from itertools import pairwise

import numpy as np
from _shared import COLORS, SQRT3, math_check, new_axes, save_preview


# --- geometry: pure-numpy fractal builders ---------------------------------------------
def cantor_levels(depth):
    """List over levels; each level is a list of (x_left, x_right) surviving intervals."""
    levels = [[(0.0, 1.0)]]
    for _ in range(depth):
        nxt = []
        for a, b in levels[-1]:
            t = (b - a) / 3.0
            nxt.append((a, a + t))
            nxt.append((b - t, b))
        levels.append(nxt)
    return levels


def sierpinski_triangles(depth):
    """Filled sub-triangles (each a 3x2 vertex array) after `depth` subdivisions of the unit tri."""
    base = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, SQRT3 / 2.0]])
    tris = [base]
    for _ in range(depth):
        nxt = []
        for tri in tris:
            a, b, c = tri
            mab, mbc, mca = (a + b) / 2, (b + c) / 2, (c + a) / 2
            nxt += [np.array([a, mab, mca]), np.array([mab, b, mbc]), np.array([mca, mbc, c])]
        tris = nxt
    return tris


def koch_curve(depth):
    """Polyline (M x 2) of the Koch curve on [0,1] after `depth` subdivisions."""
    pts = np.array([[0.0, 0.0], [1.0, 0.0]])
    for _ in range(depth):
        out = [pts[0]]
        for p, q in pairwise(pts):
            d = q - p
            a = p + d / 3.0
            b = p + 2 * d / 3.0
            # apex of the outward bump (rotate (b-a) by +60 deg)
            ang = math.radians(60)
            rot = np.array([[math.cos(ang), -math.sin(ang)], [math.sin(ang), math.cos(ang)]])
            apex = a + rot @ (b - a)
            out += [a, apex, b, q]
        pts = np.array(out)
    return pts


def sierpinski_points(n_chains=150_000, steps=45, burn=8, seed=0):
    """Chaos-game sample of the Sierpinski attractor (pure numpy). Many independent chains are run
    in parallel and advanced with vectorized IFS steps, so we get millions of points fast and dense
    enough to box-count down to fine scales."""
    rng = np.random.default_rng(seed)
    verts = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, SQRT3 / 2.0]])
    p = rng.random((n_chains, 2)) * 0.3  # start inside the triangle
    out = []
    for s in range(steps):
        idx = rng.integers(0, 3, size=n_chains)
        p = (p + verts[idx]) / 2.0
        if s >= burn:  # drop burn-in, then keep every generation
            out.append(p.copy())
    return np.concatenate(out)


def boxcount_slope(points, ks):
    """Empirical box-count over deltas = 2^-k; return (deltas, counts, fitted slope)."""
    counts = []
    for k in ks:
        delta = 2.0 ** (-k)
        cells = np.floor(points / delta).astype(np.int64)
        counts.append(len({tuple(c) for c in cells}))
    counts = np.array(counts, dtype=float)
    logN = np.log(counts)
    log_inv_delta = np.array(ks, dtype=float) * math.log(2.0)
    slope = float(np.polyfit(log_inv_delta, logN, 1)[0])
    return [2.0 ** (-k) for k in ks], counts, slope


def main():
    dim_cantor = math.log(2) / math.log(3)
    dim_sierp = math.log(3) / math.log(2)
    dim_koch = math.log(4) / math.log(3)

    # empirical Sierpinski box-count over a clean range of fine scales (delta = 2^-5 .. 2^-10)
    pts = sierpinski_points()
    ks = list(range(5, 11))
    _, counts, slope = boxcount_slope(pts, ks)
    ratios = counts[1:] / counts[:-1]  # successive N(2^-(k+1)) / N(2^-k) -> 3

    math_check(
        "Hausdorff / self-similar dimension  (dim = log N / log r)",
        [
            ("Cantor  log2/log3", f"{dim_cantor:.4f}   (want 0.6309)"),
            ("Sierpinski  log3/log2", f"{dim_sierp:.4f}   (want 1.5850)"),
            ("Koch  log4/log3", f"{dim_koch:.4f}   (want 1.2619)"),
            ("Sierpinski box-count N(2^-k)", ", ".join(f"{int(c)}" for c in counts)),
            ("N ratios (want ~3 = 3^k scaling)", ", ".join(f"{r:.2f}" for r in ratios)),
            ("Sierpinski measured slope", f"{slope:.4f}   (want ~1.585 = log3/log2)"),
            ("dim_H <= dim_box", "equality here (self-similar); Kakeya is where it bites"),
        ],
    )

    fig, ax = new_axes(3, figsize=(15, 5.2))

    # Cantor: stack surviving intervals, one row per level (top = level 0)
    levels = cantor_levels(5)
    for lvl, intervals in enumerate(levels):
        y = -lvl
        for a, b in intervals:
            ax[0].plot([a, b], [y, y], color=COLORS["needle"], lw=3.0, solid_capstyle="butt")
    ax[0].set_xlim(-0.05, 1.05)
    ax[0].set_ylim(-len(levels) + 0.5, 0.5)
    ax[0].set_title(f"Cantor set   dim = log2/log3 = {dim_cantor:.4f}")

    # Sierpinski: fill the surviving sub-triangles
    for tri in sierpinski_triangles(6):
        ax[1].fill(tri[:, 0], tri[:, 1], color=COLORS["needle"], lw=0)
    ax[1].set_xlim(-0.05, 1.05)
    ax[1].set_ylim(-0.05, SQRT3 / 2.0 + 0.05)
    ax[1].set_title(f"Sierpinski   dim = log3/log2 = {dim_sierp:.4f}\n(box-count slope {slope:.3f})")

    # Koch: the polyline
    koch = koch_curve(4)
    ax[2].plot(koch[:, 0], koch[:, 1], color=COLORS["needle"], lw=1.0)
    ax[2].set_xlim(-0.05, 1.05)
    ax[2].set_ylim(-0.15, 0.5)
    ax[2].set_title(f"Koch curve   dim = log4/log3 = {dim_koch:.4f}")

    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
