"""Animation: the pair-correlation histogram of the zeta zeros building toward Montgomery's law.

    w_k = gamma_k * log(gamma_k / 2pi) / 2pi     unfold ordinates to mean spacing 1
    differences w_j - w_i  (j > i, <= 3)          pairwise distances of the unfolded zeros
    density(u) = counts / (n * bin_width)         normalised so the mean level is ~1
    R2(u) = 1 - (sin(pi u) / (pi u))^2            Montgomery's pair-correlation law

Frame by frame the histogram is built from an increasing number of zeros n = 100, 200, ..., 1200.
It shows a dip near u = 0 (level repulsion) and settles near 1, matching R2. On the final frame we
assert repulsion: mean density for bin centres < 0.5 is below that for centres > 1.5.

Run: PYTHONPATH=research/riemann/figures uv run --with matplotlib --with mpmath --with pillow \
     python research/riemann/figures/5_two_methods/5_2_pair_correlation_anim.py
"""

import math

import numpy as np
from _shared import COLORS, math_check, save_gif

U_MAX = 3.0
N_BINS = 60
COUNTS = list(range(100, 1300, 100))
CACHE = "research/riemann/framework/zeros_cache.npy"


def montgomery_r2(u: np.ndarray) -> np.ndarray:
    """R2(u) = 1 - (sin(pi u)/(pi u))^2, the pair-correlation law (=1 at u=0 by limit)."""
    out = np.ones_like(u)
    nz = u != 0.0
    s = np.sin(math.pi * u[nz]) / (math.pi * u[nz])
    out[nz] = 1.0 - s * s
    return out


def pair_density(w: np.ndarray, n: int, edges: np.ndarray) -> np.ndarray:
    """Histogram density of unfolded pair differences w_j - w_i (j>i, <=U_MAX) from the first n zeros.

    The prefix is linearly rescaled to exactly unit mean spacing (residual unfolding at finite
    height), so the histogram level settles near 1.
    """
    ww = w[:n]
    ww = (ww - ww[0]) * (n - 1) / (ww[-1] - ww[0])
    diffs = ww[:, None] - ww[None, :]
    d = np.abs(diffs[np.triu_indices(n, k=1)])
    d = d[(d > 0) & (d <= U_MAX)]
    counts, _ = np.histogram(d, bins=edges)
    width = edges[1] - edges[0]
    return counts / (n * width)


def main():
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    gammas = np.load(CACHE)
    w = gammas * np.log(gammas / (2 * math.pi)) / (2 * math.pi)

    edges = np.linspace(0.0, U_MAX, N_BINS + 1)
    centres = 0.5 * (edges[:-1] + edges[1:])
    width = edges[1] - edges[0]

    curve_u = np.linspace(1e-6, U_MAX, 400)
    curve = montgomery_r2(curve_u)

    final_density = pair_density(w, COUNTS[-1], edges)
    near = final_density[centres < 0.5].mean()
    far = final_density[centres > 1.5].mean()
    assert near < far, f"repulsion failed: near={near:.3f} not < far={far:.3f}"

    math_check(
        "Pair correlation of the zeros -> 1 - (sin pi u / pi u)^2",
        [
            ("zeros used (unfolded)", f"{COUNTS[-1]} ordinates from cache"),
            ("bins on [0, 3], width", f"{N_BINS} bins, {width:.3f}"),
            ("near-0 density (centres < 0.5)", f"{near:.3f} (suppressed by repulsion)"),
            ("far density (centres > 1.5)", f"{far:.3f} (settles near 1)"),
            ("repulsion near < far", f"{near:.3f} < {far:.3f}  OK"),
            ("R2(0+) limit, R2 -> 1 as u grows", f"{montgomery_r2(np.array([1e-6]))[0]:.3f}, {curve[-1]:.3f}"),
        ],
    )

    fig, ax = plt.subplots(figsize=(7.2, 5.0))
    ax.grid(True, color="#e6e6e6", lw=0.8)
    ax.set_axisbelow(True)
    bars = ax.bar(
        centres, np.zeros_like(centres), width=width * 0.92, color=COLORS["zero"], alpha=0.75, label="pair histogram"
    )
    ax.plot(curve_u, curve, color=COLORS["line"], lw=2.0, label=r"$1-\left(\frac{\sin \pi u}{\pi u}\right)^2$")
    ax.axhline(1.0, color=COLORS["muted"], lw=0.8, ls="--")
    ax.set_xlim(0, U_MAX)
    ax.set_ylim(0, 1.6)
    ax.set_xlabel("normalised gap u")
    ax.set_ylabel("density")
    ax.set_title("Pair correlation of the zeros")
    ax.legend(loc="lower right", framealpha=0.9)
    readout = ax.text(0.03, 0.94, "", transform=ax.transAxes, va="top", fontsize=10, color=COLORS["guide"])

    def update(frame):
        n = COUNTS[frame]
        dens = pair_density(w, n, edges)
        for b, h in zip(bars, dens, strict=True):
            b.set_height(h)
        readout.set_text(f"n = {n} zeros")
        return [*bars, readout]

    anim = FuncAnimation(fig, update, frames=len(COUNTS), interval=500, blit=False)
    print("wrote", save_gif(anim, fps=3, dpi=100))


if __name__ == "__main__":
    main()
