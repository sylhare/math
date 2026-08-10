"""Animation: self-similar fractals building by iteration depth (section 3b of ../kakeya.md).

Mirrors dimension_fractal.py in motion. Two self-similar sets grow one iteration at a time:

  * Sierpinski triangle - depth k has  3^k  filled sub-triangles;  dim = log 3 / log 2 = 1.5850
  * Koch curve          - depth k has  4^k  segments;              dim = log 4 / log 3 = 1.2619

Each step replaces every piece by its scaled copies (N copies each at scale 1/r), so the piece
count multiplies by N while the size divides by r. The similarity dimension

    dim = log N / log r

is the SAME at every depth (it is a property of the rule, not the depth); it is annotated on every
frame while the count 3^k / 4^k climbs. Geometric honesty: the piece count is the actual number of
triangles / segments drawn, not a formula, and it is checked against 3^k / 4^k for each depth.

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/fractal_iterate_anim.py
"""
import math
from itertools import pairwise

import numpy as np
from _shared import COLORS, SQRT3, math_check, save_gif
from matplotlib.animation import FuncAnimation

SIERP_DEPTH = 6
KOCH_DEPTH = 5
HOLD = 7
END_HOLD = 8


# --- geometry: pure-numpy fractal builders (replicated locally, no figure imports) --------
def sierpinski_triangles(depth):
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
    pts = np.array([[0.0, 0.0], [1.0, 0.0]])
    ang = math.radians(60)
    rot = np.array([[math.cos(ang), -math.sin(ang)], [math.sin(ang), math.cos(ang)]])
    for _ in range(depth):
        out = [pts[0]]
        for p, q in pairwise(pts):
            d = q - p
            a = p + d / 3.0
            b = p + 2 * d / 3.0
            apex = a + rot @ (b - a)
            out += [a, apex, b, q]
        pts = np.array(out)
    return pts


def main():
    dim_sierp = math.log(3) / math.log(2)
    dim_koch = math.log(4) / math.log(3)

    sierp = [sierpinski_triangles(k) for k in range(SIERP_DEPTH + 1)]
    koch = [koch_curve(k) for k in range(KOCH_DEPTH + 1)]

    rows = []
    ok = True
    for k in range(max(SIERP_DEPTH, KOCH_DEPTH) + 1):
        parts = []
        if k <= SIERP_DEPTH:
            n_s = len(sierp[k])
            ok = ok and n_s == 3 ** k
            parts.append(f"Sierpinski {n_s:<4d}(=3^{k} {3**k})")
        if k <= KOCH_DEPTH:
            n_k = len(koch[k]) - 1
            ok = ok and n_k == 4 ** k
            parts.append(f"Koch {n_k:<5d}(=4^{k} {4**k})")
        rows.append((f"depth {k}", "   ".join(parts)))
    assert ok, "piece counts must equal 3^k (Sierpinski) and 4^k (Koch) at every depth"

    math_check(
        "self-similar dimension: pieces = N^k, dim = log N / log r (constant)",
        [
            *rows,
            ("Sierpinski dim = log3/log2", f"{dim_sierp:.4f}   (want 1.5850, constant in k)"),
            ("Koch dim = log4/log3", f"{dim_koch:.4f}   (want 1.2619, constant in k)"),
        ],
    )

    # ---- figure ----
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 2, figsize=(12.5, 5.4))
    for a in ax:
        a.set_aspect("equal")
        a.axis("off")

    # stage sequence: depth 0..max, holding each; both fractals advance together (clamped)
    n_stages = max(SIERP_DEPTH, KOCH_DEPTH) + 1
    frame_stage = []
    for k in range(n_stages):
        frame_stage += [k] * HOLD
    frame_stage += [n_stages - 1] * END_HOLD

    def update(fi):
        k = frame_stage[fi]
        ks = min(k, SIERP_DEPTH)
        kk = min(k, KOCH_DEPTH)

        ax[0].cla(); ax[0].axis("off"); ax[0].set_aspect("equal")
        for tri in sierp[ks]:
            ax[0].fill(tri[:, 0], tri[:, 1], color=COLORS["needle"], lw=0)
        ax[0].set_xlim(-0.05, 1.05); ax[0].set_ylim(-0.05, SQRT3 / 2.0 + 0.05)
        ax[0].set_title(f"Sierpinski, depth {ks}\n"
                        f"{3 ** ks} triangles = 3^{ks}   dim = log3/log2 = {dim_sierp:.4f}")

        ax[1].cla(); ax[1].axis("off"); ax[1].set_aspect("equal")
        c = koch[kk]
        ax[1].plot(c[:, 0], c[:, 1], color=COLORS["needle"], lw=1.1)
        ax[1].set_xlim(-0.05, 1.05); ax[1].set_ylim(-0.1, 0.5)
        ax[1].set_title(f"Koch curve, depth {kk}\n"
                        f"{4 ** kk} segments = 4^{kk}   dim = log4/log3 = {dim_koch:.4f}")
        return []

    anim = FuncAnimation(fig, update, frames=len(frame_stage), interval=180, blit=False)
    print("wrote", save_gif(anim, fps=6, dpi=95))


if __name__ == "__main__":
    main()
