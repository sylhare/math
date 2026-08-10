"""Animation: Fourier partial sums reconstruct an odd square wave as N grows (Part 4, "Fourier").

Mirror of the static `fourier_transform.py`, set in motion. The odd square wave of period 1 has the
sine series (symbolic first, then the picture):

    sq(x) = (4 / pi) * sum_{k odd} sin(2 pi k x) / k,     b_k = 4 / (pi k)  (k odd), 0 (k even).

As N climbs through the odd harmonics 1, 3, 5, ..., 49 the partial sum S_N closes on the target and
the spectrum fills in one bar at a time. Two honest facts carry the animation:

  * L2 reconstruction error  ||sq - S_N||_2  decreases MONOTONICALLY as N grows (each added
    orthogonal harmonic can only shrink the residual).
  * The Gibbs overshoot near the jump does NOT vanish: the peak of S_N stays about 9% above the
    step no matter how large N gets (it narrows but never shrinks below ~8.9%).

INVARIANT asserted at the end: errors strictly decreasing (first vs last printed) and the Gibbs
overshoot persists at ~9% (first vs last printed).

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/fourier_partial_sums_anim.py
"""
import math

import numpy as np
from _shared import COLORS, math_check, save_gif
from matplotlib.animation import FuncAnimation


def square_wave(x: np.ndarray) -> np.ndarray:
    """Odd square wave of period 1, amplitude +-1 (sign of sin 2 pi x)."""
    return np.sign(np.sin(2 * math.pi * x))


def coeffs(k_max: int) -> tuple[np.ndarray, np.ndarray]:
    """Sine coefficients b_k = 4/(pi k) for odd k (0 for even), k = 1..k_max."""
    ks = np.arange(1, k_max + 1)
    bk = np.where(ks % 2 == 1, 4.0 / (math.pi * ks), 0.0)
    return ks, bk


def partial_sum(x: np.ndarray, k_max: int) -> np.ndarray:
    """S_N(x) = sum_{k<=k_max} b_k sin(2 pi k x)."""
    ks, bk = coeffs(k_max)
    return (bk[:, None] * np.sin(2 * math.pi * ks[:, None] * x[None, :])).sum(axis=0)


def main():
    x = np.linspace(0.0, 1.0, 20001)
    f = square_wave(x)

    odd_ns = list(range(1, 50, 2))  # 1, 3, 5, ..., 49
    errors, overshoots, gibbs = [], [], []
    for n in odd_ns:
        s = partial_sum(x, n)
        errors.append(math.sqrt(max(np.trapezoid((f - s) ** 2, x), 0.0)))
        peak = float(s.max()) - 1.0            # peak height above the step (step = 1)
        overshoots.append(peak)
        gibbs.append(peak / 2.0)               # as a fraction of the jump (jump = 2)
    errors = np.array(errors)
    overshoots = np.array(overshoots)
    gibbs = np.array(gibbs)

    monotone = bool(np.all(np.diff(errors) < 1e-9))
    gibbs_persists = bool(gibbs[-1] > 0.085)

    math_check(
        "Fourier partial sums of a square wave (animated)",
        [
            ("series", "sq(x) = (4/pi) sum_{k odd} sin(2 pi k x)/k"),
            ("frames (odd harmonics N)", f"{odd_ns[0]}, {odd_ns[1]}, ..., {odd_ns[-1]}  ({len(odd_ns)} steps)"),
            ("L2 error  N=1  ->  N=49", f"{errors[0]:.4f}  ->  {errors[-1]:.4f}"),
            ("L2 error monotone decreasing?", "YES" if monotone else "NO"),
            ("Gibbs overshoot (frac of jump)  N=1 -> N=49", f"{100*gibbs[0]:.1f}%  ->  {100*gibbs[-1]:.2f}%"),
            ("Gibbs limit ~ 8.95% of the jump", f"{100*gibbs[-1]:.2f}%  (persists, does not -> 0)"),
        ],
    )
    assert monotone, "L2 error must decrease monotonically as N grows"
    assert gibbs_persists, "Gibbs overshoot must persist near ~9%, not vanish"
    assert 0.085 <= gibbs[-1] <= 0.095, "overshoot should sit near the 8.95% Gibbs constant"

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 2, figsize=(12.5, 5.0))

    # (a) reconstruction: target + live partial sum
    ax[0].plot(x, f, color=COLORS["guide"], lw=1.6, label="square wave")
    ax[0].axhline(1.0, color=COLORS["muted"], lw=0.7, ls=":")
    ax[0].axhline(-1.0, color=COLORS["muted"], lw=0.7, ls=":")
    live, = ax[0].plot([], [], color=COLORS["needle"], lw=1.6)
    ax[0].set_xlim(0, 1)
    ax[0].set_ylim(-1.4, 1.4)
    ax[0].set_xlabel("x")
    ax[0].set_ylabel("amplitude")
    ax[0].legend(fontsize=8, loc="upper right")

    ks_all, bk_all = coeffs(odd_ns[-1])
    odd_mask = ks_all % 2 == 1

    seq = [odd_ns[0]] * 3 + odd_ns + [odd_ns[-1]] * 5

    def update(i):
        n = seq[i]
        idx = odd_ns.index(n)
        s = partial_sum(x, n)
        live.set_data(x, s)
        ax[0].set_title(f"N = {n}    L2 err = {errors[idx]:.3f}    Gibbs = {100*gibbs[idx]:.1f}% of jump")

        # (b) spectrum filling in: bars up to N strong, the rest faint
        ax[1].cla()
        shown = odd_mask & (ks_all <= n)
        rest = odd_mask & (ks_all > n)
        ax[1].vlines(ks_all[rest], 0, bk_all[rest], color=COLORS["muted"], lw=1.0, alpha=0.35)
        ax[1].vlines(ks_all[shown], 0, bk_all[shown], color=COLORS["needle"], lw=1.6)
        ax[1].scatter(ks_all[shown], bk_all[shown], s=18, color=COLORS["accent"], zorder=3)
        ax[1].plot(ks_all[odd_mask], 4.0 / (math.pi * ks_all[odd_mask]), color=COLORS["muted"], lw=0.9, ls="--")
        ax[1].set_xlim(0, odd_ns[-1] + 1)
        ax[1].set_ylim(0, bk_all[odd_mask].max() * 1.1)
        ax[1].set_title("spectrum  b_k = 4/(pi k)")
        ax[1].set_xlabel("frequency k")
        ax[1].set_ylabel("coefficient")
        return (live,)

    anim = FuncAnimation(fig, update, frames=len(seq), interval=180, blit=False)
    print("wrote", save_gif(anim, fps=6, dpi=95))


if __name__ == "__main__":
    main()
