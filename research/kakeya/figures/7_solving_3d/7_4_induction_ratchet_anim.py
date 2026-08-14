"""Dimension ratchet 2.5 -> 3 (kakeya.md beat 7e).

Motion version of `induction_on_scales.py`. Induction on scales with fixed gain alpha = 0.1; two
staircases climb in parallel:
  * graininess (red): mu <~ mu_coarse * mu_fine, grains disjoint in a fat tube, so each step gains
    alpha and the estimate ratchets 2.5 -> 3.0 in 5 steps;
  * lossy "Chinese whispers" (blue): mu <~ mu_fat * mu_fine over-counts the fat tube, so it stalls
    below 3.

Schematic: alpha, start 2.5 and cap 3 are exact; the lossy leak is illustrative.
Run: uv run --with matplotlib --with shapely python research/kakeya/figures/induction_ratchet_anim.py
"""
import math

import numpy as np
from _shared import COLORS, math_check, save_gif
from matplotlib.animation import FuncAnimation

D_START = 2.5    # Wolff's 1995 lower bound in R^3 = (n+2)/2
D_TARGET = 3.0   # full dimension (Wang-Zahl)
ALPHA = 0.1      # fixed per-step gain of the graininess induction


def ratchet(d_start, d_target, alpha):
    """Graininess induction: gain exactly alpha per step, capped at d_target."""
    ds = [d_start]
    while ds[-1] < d_target - 1e-12:
        ds.append(min(d_target, ds[-1] + alpha))
    return np.array(ds)


def lossy(d_start, alpha, leak, n_steps):
    """Chinese-whispers induction: nominal gain alpha but a compounding leak, so the net gain per
    step shrinks and the estimate converges to a ceiling < 3."""
    ds = [d_start]
    for _ in range(n_steps):
        gain = alpha - leak * (ds[-1] - d_start)
        ds.append(ds[-1] + max(0.0, gain))
    return np.array(ds)


def staircase_vertices(g):
    """Vertices of a `where=post` staircase: tread then riser for each step."""
    v = [(0.0, float(g[0]))]
    for i in range(len(g) - 1):
        v.append((float(i + 1), float(g[i])))      # tread end
        v.append((float(i + 1), float(g[i + 1])))  # riser end
    return v


def revealed(v, p):
    """Polyline of `v` revealed up to segment-progress p in [0, len(v)-1]; also the whole-segment
    count k so callers can mark the settled corner vertices."""
    k = min(math.floor(p), len(v) - 1)
    pts = list(v[: k + 1])
    if k < len(v) - 1:
        frac = p - k
        (x0, y0), (x1, y1) = v[k], v[k + 1]
        pts.append((x0 + frac * (x1 - x0), y0 + frac * (y1 - y0)))
    return pts, k


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    good = ratchet(D_START, D_TARGET, ALPHA)
    n_steps = len(good) - 1
    bad = lossy(D_START, ALPHA, leak=0.28, n_steps=n_steps)
    incs = np.diff(good)

    # Invariant assertions
    assert n_steps == 5, n_steps
    assert all(abs(inc - ALPHA) < 1e-9 for inc in incs), incs
    assert abs(good[-1] - 3.0) < 1e-12, good[-1]
    assert bad[-1] < 3.0 - 1e-3, bad[-1]

    math_check(
        "induction ratchet 2.5 -> 3 (animated)",
        [
            ("start K(d)", f"d = {D_START}   (Wolff 1995 bound (n+2)/2 in R^3)"),
            ("fixed per-step gain", f"alpha = {ALPHA}   K(d) => K(d + alpha)"),
            ("steps to close the gap", f"{n_steps}  = (3 - 2.5) / alpha"),
            ("red step increments", "  ".join(f"{inc:.2f}" for inc in incs) + "   (each = 0.10)"),
            ("graininess reaches (5th step)", f"{good[-1]:.3f}   (exactly 3.000)"),
            ("lossy 'Chinese whispers' ends", f"{bad[-1]:.3f}   (< 3: leak never closes the gap)"),
            ("graininess inequality", "mu <~ mu_coarse * mu_fine   (grains disjoint => gain)"),
            ("lossy inequality", "mu <~ mu_fat * mu_fine       (fat tube over-counted => loss)"),
        ],
    )

    good_v = staircase_vertices(good)
    bad_v = staircase_vertices(bad)
    seg_total = len(good_v) - 1  # = 2 * n_steps

    H0, ADV, H1 = 8, 60, 16
    progress = np.concatenate([np.zeros(H0), np.linspace(0, seg_total, ADV), np.full(H1, seg_total)])

    fig, ax = plt.subplots(figsize=(9.5, 6.2))

    def update(fi):
        p = float(progress[fi])
        ax.clear()
        ax.axhline(D_TARGET, color=COLORS["accent"], ls="--", lw=1.2, alpha=0.7)
        ax.text(0.05, D_TARGET + 0.008, "dimension 3 (Wang-Zahl: full)", color=COLORS["accent"], fontsize=10)
        ax.axhline(D_START, color=COLORS["guide"], ls=":", lw=0.9, alpha=0.6)
        ax.text(0.05, D_START - 0.05, "start 2.5  (Wolff 1995)", color=COLORS["guide"], fontsize=9)

        gp, gk = revealed(good_v, p)
        bp, bk = revealed(bad_v, p)
        gx, gy = zip(*gp, strict=False)
        bx, by = zip(*bp, strict=False)
        ax.plot(bx, by, color=COLORS["outer"], lw=2.0, label="lossy: mu ~ mu_fat * mu_fine")
        ax.plot(gx, gy, color=COLORS["accent"], lw=2.4, label="graininess: mu ~ mu_coarse * mu_fine")

        for j in range(0, gk + 1, 2):  # settled level corners of the red staircase
            ax.plot(*good_v[j], "o", color=COLORS["accent"], ms=6, zorder=4)
        for j in range(0, bk + 1, 2):
            ax.plot(*bad_v[j], "s", color=COLORS["outer"], ms=4, zorder=4)

        ax.plot(gx[-1], gy[-1], "o", color=COLORS["accent"], ms=9, mec="white", zorder=5)
        ax.text(gx[-1] + 0.08, gy[-1], f"{gy[-1]:.2f}", color=COLORS["accent"], fontsize=10, va="center")
        if p >= seg_total - 1e-9:
            ax.text(n_steps, bad[-1] - 0.05, f"stalls at {bad[-1]:.2f}", color=COLORS["outer"], fontsize=9, ha="right")

        ax.set_xlabel("induction step (scale)")
        ax.set_ylabel("dimension estimate")
        ax.set_ylim(2.35, 3.12)
        ax.set_xlim(-0.3, n_steps + 0.6)
        ax.set_xticks(np.arange(n_steps + 1))
        ax.legend(loc="lower right", fontsize=9, framealpha=0.9)
        ax.set_title("Induction on scales: the dimension ratchet 2.5 -> 3", fontsize=12)
        ax.grid(True, alpha=0.15)
        return []

    anim = FuncAnimation(fig, update, frames=len(progress), interval=60, blit=False)
    print("wrote", save_gif(anim, fps=15, dpi=95))


if __name__ == "__main__":
    main()
