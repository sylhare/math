"""Figure: a signal as a sum of sines, and its spectrum (Part 4 of ../kakeya.md, "Fourier").

The Fourier transform (convention used throughout the tower in ../kakeya.md):

    f_hat(xi) = int f(x) e^{-2 pi i x xi} dx.

For a 1-periodic signal this collapses to Fourier coefficients on the integer frequencies. We
reconstruct the odd square wave  sq(x) = sign(sin 2 pi x)  from its first N harmonics. Its sine
series (symbolic first, then the picture):

    sq(x) = (4 / pi) * sum_{k odd} sin(2 pi k x) / k,     b_k = 4 / (pi k)  (k odd), 0 (k even).

Two exact facts this figure verifies numerically:
  * L2 reconstruction error  ||sq - S_N||_2  decreases monotonically as N grows (adding an
    orthogonal harmonic can only shrink the residual; Gibbs overshoot is an L-infinity effect,
    not L2).
  * Parseval / energy identity.  Signal energy over one period is  int_0^1 sq^2 dx = 1.  For a
    sine series the energy equals  (1/2) sum_k b_k^2 , and  (1/2) * (16/pi^2) * sum_{k odd} 1/k^2
    = (1/2)(16/pi^2)(pi^2/8) = 1.  Partial sums match to a few percent once N is moderate.

Reference: none (standard Fourier synthesis picture). This is an analysis / line plot, not an
equal-aspect geometry figure, so it builds its own matplotlib axes and hands the figure to
save_preview.
Run: uv run --with matplotlib --with shapely python research/kakeya/figures/fourier_transform.py
"""
import math

import numpy as np
from _shared import COLORS, math_check, save_preview


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
    # dense grid over one period for L2 integrals via the trapezoid rule
    x = np.linspace(0.0, 1.0, 20001)
    f = square_wave(x)
    energy = np.trapezoid(f * f, x)  # = 1 exactly

    k_top = 49  # 25 odd harmonics; tail ~ 1/(2*49) => Parseval within ~1%
    ks, bk = coeffs(k_top)
    parseval = 0.5 * np.sum(bk**2)

    # L2 error as harmonics accumulate (odd k only add anything)
    n_list = list(range(1, k_top + 1, 2))
    errors = []
    for n in n_list:
        s = partial_sum(x, n)
        errors.append(math.sqrt(max(np.trapezoid((f - s) ** 2, x), 0.0)))
    errors = np.array(errors)
    monotone = bool(np.all(np.diff(errors) < 1e-9))

    math_check(
        "Fourier synthesis of a square wave",
        [
            ("transform", "f_hat(xi) = int f(x) e^{-2 pi i x xi} dx"),
            ("series", "sq(x) = (4/pi) sum_{k odd} sin(2 pi k x)/k"),
            ("signal energy  int_0^1 sq^2", f"{energy:.4f}  (exact 1)"),
            (f"Parseval (1/2)sum b_k^2, k<= {k_top}", f"{parseval:.4f}  ({100*parseval/energy:.1f}% of energy)"),
            ("Parseval within a few percent?", f"{'YES' if abs(parseval-energy) < 0.03*energy else 'NO'}  (|diff| {abs(parseval-energy):.4f})"),
            ("L2 error N=1  vs  N=49", f"{errors[0]:.4f}  ->  {errors[-1]:.4f}"),
            ("L2 error monotone decreasing?", "YES" if monotone else "NO"),
        ],
    )

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 3, figsize=(15.5, 4.6))

    # (a) square wave + partial sums for increasing N
    ax[0].plot(x, f, color=COLORS["guide"], lw=1.6, label="square wave")
    shown = [1, 3, 7, 15, 49]
    blues = plt.cm.viridis(np.linspace(0.15, 0.85, len(shown)))
    for c, n in zip(blues, shown, strict=True):
        ax[0].plot(x, partial_sum(x, n), color=c, lw=1.3, label=f"N={n}")
    ax[0].set_title("signal = sum of sines")
    ax[0].set_xlabel("x")
    ax[0].set_ylabel("amplitude")
    ax[0].set_xlim(0, 1)
    ax[0].set_ylim(-1.4, 1.4)
    ax[0].legend(fontsize=7, loc="upper right", ncol=2)

    # (b) coefficient spectrum (odd harmonics only)
    odd = ks % 2 == 1
    ax[1].vlines(ks[odd], 0, bk[odd], color=COLORS["needle"], lw=1.4)
    ax[1].scatter(ks[odd], bk[odd], s=16, color=COLORS["accent"], zorder=3)
    ax[1].plot(ks[odd], 4.0 / (math.pi * ks[odd]), color=COLORS["muted"], lw=0.9, ls="--", label="4/(pi k)")
    ax[1].set_title("spectrum  b_k")
    ax[1].set_xlabel("frequency k")
    ax[1].set_ylabel("coefficient")
    ax[1].set_xlim(0, k_top + 1)
    ax[1].legend(fontsize=8)

    # (c) L2 error decreasing with N
    ax[2].plot(n_list, errors, marker="o", ms=4, color=COLORS["accent"], lw=1.4)
    ax[2].set_title("L2 error decreases with N")
    ax[2].set_xlabel("harmonics N")
    ax[2].set_ylabel("|| sq - S_N ||_2")
    ax[2].set_ylim(0, errors[0] * 1.1)
    ax[2].grid(True, alpha=0.25)

    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
