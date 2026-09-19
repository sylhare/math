"""Figure: the two lineages side by side, Levinson's mollifier vs Montgomery's gaps.

Left panel, Levinson's method:
    |zeta(1/2 + it)|                         the modulus along the critical line
    mollified copy                           a smoothed / damped version whose sign changes are counted
    on-line zeros                            ticks at gamma_k where the modulus touches zero
Convey: mollify zeta and count the sign changes (zeros) of the smoothed function.

Right panel, Montgomery's method:
    unfolded ordinates w_k                   ticks on a line, mean spacing 1 after unfolding
    gaps w_{k+1} - w_k                       the statistics that carry the information
Convey: study the statistics of the gaps between zeros, not the zeros one at a time.

Reproduces the two lineages: Levinson reached the 2020 record 5/12 = 0.4167; Montgomery's
pair correlation gave the conditional 2/3 = 0.6667.

Run: PYTHONPATH=research/riemann/figures uv run --with matplotlib --with mpmath --with pillow \
     python research/riemann/figures/5_two_methods/5_1_mollifier_vs_paircorrelation.py
"""

import math

import numpy as np
from _shared import COLORS, ZETA_ZEROS, math_check, plot_axes, save_preview

T_LO, T_HI = 10.0, 40.0


def zeta_modulus(ts: np.ndarray) -> np.ndarray:
    """|zeta(1/2 + it)| on the grid ts, via mpmath."""
    import mpmath

    return np.array([float(abs(mpmath.zeta(mpmath.mpc(0.5, t)))) for t in ts])


def moving_average(y: np.ndarray, k: int) -> np.ndarray:
    """Centred moving average of width k, the schematic mollified modulus."""
    kernel = np.ones(k) / k
    return np.convolve(y, kernel, mode="same")


def unfold(gammas: np.ndarray) -> np.ndarray:
    """Unfold ordinates by w = gamma*log(gamma/2pi)/2pi so the mean spacing is 1."""
    return gammas * np.log(gammas / (2 * math.pi)) / (2 * math.pi)


def main():
    grid = np.linspace(T_LO, T_HI, 1400)
    modulus = zeta_modulus(grid)
    mollified = moving_average(modulus, 61)
    zeros_in = ZETA_ZEROS[(ZETA_ZEROS >= T_LO) & (ZETA_ZEROS <= T_HI)]

    w = unfold(ZETA_ZEROS[:25])
    gaps = np.diff(w)

    assert zeros_in.size == 6, f"expected 6 zeros in [{T_LO},{T_HI}], got {zeros_in.size}"

    math_check(
        "Two lineages: mollifier (Levinson) and pair correlation (Montgomery)",
        [
            ("Levinson mollifier: 2020 record", "5/12 = 0.4167 (PRZZ, held since 2020)"),
            ("Montgomery pair correlation", "conditional 2/3 = 0.6667 (simple zeros)"),
            ("zeros gamma_k in [10, 40]", ", ".join(f"{g:.3f}" for g in zeros_in)),
            ("count of on-line zeros drawn", f"{zeros_in.size}"),
            ("unfolded mean gap (low heights)", f"{gaps.mean():.3f} (approaches 1 as T grows)"),
        ],
    )

    fig, axes = plot_axes(2, figsize=(12.4, 5.2))
    axl, axr = axes

    axl.plot(grid, modulus, color=COLORS["zero"], lw=1.4, label=r"$|\zeta(\frac{1}{2}+it)|$")
    axl.plot(grid, mollified, color=COLORS["guide"], lw=1.8, label="mollified")
    axl.plot(zeros_in, np.zeros_like(zeros_in), "v", color=COLORS["line"], ms=8, label="on-line zeros")
    for g in zeros_in:
        axl.axvline(g, color=COLORS["muted"], lw=0.7, ls=":")
    axl.set_xlim(T_LO, T_HI)
    axl.set_ylim(-0.3, modulus.max() * 1.05)
    axl.set_xlabel("t")
    axl.set_ylabel("modulus")
    axl.set_title("Levinson: mollify and count")
    axl.legend(loc="upper right", framealpha=0.9)

    axr.hlines(0.0, w[0] - 0.5, w[-1] + 0.5, color=COLORS["line"], lw=1.2)
    axr.vlines(w, -0.35, 0.35, color=COLORS["zero"], lw=1.6)
    for i in (3, 9, 16):
        mid = 0.5 * (w[i] + w[i + 1])
        axr.annotate(
            "",
            xy=(w[i + 1], 0.55),
            xytext=(w[i], 0.55),
            arrowprops=dict(arrowstyle="<->", color=COLORS["guide"], lw=1.2),
        )
        axr.text(mid, 0.7, f"{gaps[i]:.2f}", ha="center", va="bottom", fontsize=8, color=COLORS["guide"])
    axr.plot(0.5 * (w[:-1] + w[1:]), gaps - 1.6, "o-", color=COLORS["prime"], ms=3, lw=1.0, label="gap sizes")
    axr.axhline(-1.6 + 1.0, color=COLORS["muted"], lw=0.8, ls="--")
    axr.text(w[-1], -1.6 + 1.0, " mean 1", va="center", fontsize=8, color=COLORS["muted"])
    axr.set_xlim(w[0] - 0.5, w[-1] + 0.5)
    axr.set_ylim(-1.9, 1.1)
    axr.set_xlabel("unfolded height w")
    axr.set_yticks([])
    axr.set_title("Montgomery: gaps between zeros")
    axr.legend(loc="lower right", framealpha=0.9)

    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
