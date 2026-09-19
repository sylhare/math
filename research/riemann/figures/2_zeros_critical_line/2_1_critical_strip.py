"""Figure: the critical strip in the complex plane.

    trivial zeros    s = -2, -4, -6, -8, -10           forced by the Gamma factor
    pole             s = 1
    critical strip   0 < Re s < 1                       everything nontrivial lives here
    critical line    Re s = 1/2                         the axis of the functional equation
    nontrivial zeros s = 1/2 + i gamma_k                first ten shown, at +-gamma_k

Reproduces gamma_1, gamma_2, gamma_3 = 14.13, 21.02, 25.01 from ZETA_ZEROS.

Run: PYTHONPATH=research/riemann/figures uv run --with matplotlib --with mpmath --with pillow \
     python research/riemann/figures/2_zeros_critical_line/2_1_critical_strip.py
"""

import numpy as np
from _shared import COLORS, ZETA_ZEROS, math_check, plot_axes, save_preview

TRIVIAL = np.array([-2, -4, -6, -8, -10])
N_SHOWN = 10


def main():
    gammas = ZETA_ZEROS[:N_SHOWN]

    assert abs(gammas[0] - 14.13) < 0.01, "gamma_1 should be ~14.13"
    assert abs(gammas[1] - 21.02) < 0.01, "gamma_2 should be ~21.02"
    assert abs(gammas[2] - 25.01) < 0.01, "gamma_3 should be ~25.01"
    assert np.all(TRIVIAL % 2 == 0) and np.all(TRIVIAL < 0), "trivial zeros are negative even"

    math_check(
        "The critical strip: zeros, line, pole",
        [
            (
                "gamma_1, gamma_2, gamma_3",
                f"{gammas[0]:.2f}, {gammas[1]:.2f}, {gammas[2]:.2f}   (want 14.13, 21.02, 25.01)",
            ),
            ("trivial zeros", ", ".join(str(int(t)) for t in TRIVIAL) + "   (negative even integers)"),
            ("critical strip", "0 < Re s < 1"),
            ("critical line", "Re s = 1/2"),
            ("pole of zeta", "s = 1"),
            ("nontrivial zeros shown", f"{N_SHOWN} pairs at (1/2, +-gamma_k)"),
        ],
    )

    fig, ax = plot_axes(figsize=(5.6, 8.4), equal=True)

    ax.axvspan(0.0, 1.0, color=COLORS["region"], alpha=0.45, zorder=0)
    ax.axvline(0.5, color=COLORS["line"], lw=1.6, zorder=2, label=r"critical line $\mathrm{Re}\,s=1/2$")
    ax.axhline(0.0, color=COLORS["guide"], lw=0.8, ls="--", zorder=1)

    ax.plot(TRIVIAL, np.zeros_like(TRIVIAL), "x", color=COLORS["muted"], ms=9, mew=2, zorder=3, label="trivial zeros")
    ax.plot([1.0], [0.0], marker="s", color=COLORS["guide"], ms=9, mfc="none", mew=2, zorder=4, label="pole at s = 1")

    gam = ZETA_ZEROS[:N_SHOWN]
    zeros_im = np.concatenate([gam, -gam])
    ax.plot(np.full_like(zeros_im, 0.5), zeros_im, "o", color=COLORS["zero"], ms=6, zorder=5, label="nontrivial zeros")

    ax.set_xlim(-12, 2.5)
    ax.set_ylim(-45, 45)
    ax.set_xlabel(r"$\mathrm{Re}\,s$")
    ax.set_ylabel(r"$\mathrm{Im}\,s$")
    ax.set_title("The critical strip")
    ax.legend(loc="upper left", framealpha=0.9, fontsize=8)

    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
