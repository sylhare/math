"""Static: the proportion this certificate can reach, as a function of Fourier bandwidth lambda.

The optimal (Montgomery-Taylor) window certifies H_opt(lambda) = 2 - 1/c*_lambda, with
c*_lambda = sqrt2 tan(theta)/(1 + theta tan(theta)), theta = lambda/sqrt2. For lambda <= 1 the input is
unconditional and the curve tops out at H_opt(1) = 0.67250, a maximum of the functional at bandwidth
one (paper sec 7.1). Beyond it the input is Montgomery's pair correlation for alpha > 1 (open):
0.70 needs lambda ~ 1.04, 0.80 needs ~ 1.27. This single-scale family does not reach 0.90 at any
bandwidth (its curve peaks near ~0.889 at the pole lambda = pi/sqrt2), which bounds the construction,
not the problem.

Run: PYTHONPATH=research/riemann/figures uv run --with matplotlib --with mpmath --with pillow \
  python research/riemann/figures/8_pushing_further/8_1_bandwidth_ceiling.py
"""

import numpy as np
from _shared import COLORS, math_check, plot_axes, save_preview

SQRT2 = np.sqrt(2.0)
POLE = np.pi / SQRT2
UNCOND = (1.0, 0.67250)
TARGETS = [(1.043, 0.70), (1.265, 0.80)]


def c_star(lam):
    """Montgomery-Taylor form factor c*_lambda = sqrt2 tan(theta)/(1 + theta tan(theta))."""
    theta = lam / SQRT2
    return SQRT2 * np.tan(theta) / (1.0 + theta * np.tan(theta))


def H_opt(lam):
    """Optimal-window on-line proportion H_opt(lambda) = 2 - 1/c*_lambda."""
    return 2.0 - 1.0 / c_star(lam)


def main():
    ceiling = H_opt(POLE - 1e-4)
    math_check(
        "bandwidth ceiling and the targets beyond lambda = 1",
        [
            ("H_opt(1) unconditional ceiling", f"{H_opt(1.0):.5f}  (= 0.67250, Montgomery-Taylor)"),
            ("0.70 needs bandwidth", f"lambda ~ {TARGETS[0][0]:.3f}"),
            ("0.80 needs bandwidth", f"lambda ~ {TARGETS[1][0]:.3f}"),
            ("0.90 by this single-window family", f"above its curve ceiling {ceiling:.4f} at pole {POLE:.3f}"),
        ],
    )
    assert abs(H_opt(1.0) - UNCOND[1]) < 1e-4
    assert H_opt(POLE - 1e-4) < 0.90, "0.90 must be above the single-window ceiling"

    fig, ax = plot_axes(figsize=(8.4, 5.4))

    ax.axvspan(0.55, 1.0, color=COLORS["region"], alpha=0.35, zorder=0)
    ax.text(
        0.72, 0.05, "unconditional: $\\lambda \\leq 1$", ha="center", va="bottom", fontsize=10, color=COLORS["prime"]
    )

    lam_known = np.linspace(0.55, 1.0, 200)
    ax.plot(
        lam_known, H_opt(lam_known), color=COLORS["zero"], lw=2.6, label=r"$H_{\mathrm{opt}}(\lambda)=2-1/c^*_\lambda$"
    )
    lam_cond = np.linspace(1.0, 2.05, 320)
    ax.plot(lam_cond, H_opt(lam_cond), color=COLORS["offline"], lw=2.2, ls="--", label="conditional ($\\lambda>1$)")

    ax.plot([UNCOND[0]], [UNCOND[1]], "o", color=COLORS["zero"], ms=7, zorder=5)
    ax.annotate(
        "ceiling 0.67250\n(no window beats this)",
        xy=UNCOND,
        xytext=(0.58, 0.50),
        fontsize=9,
        color=COLORS["zero"],
        arrowprops=dict(arrowstyle="->", color=COLORS["zero"], lw=1.0),
    )
    for lam, prop in TARGETS:
        ax.plot([lam], [prop], "s", color=COLORS["offline"], ms=7, zorder=5)
        ax.text(
            lam + 0.03,
            prop,
            f"{prop:.2f} at $\\lambda\\approx{lam:.2f}$",
            fontsize=9,
            color=COLORS["offline"],
            va="center",
        )

    ax.axhline(0.90, color=COLORS["muted"], lw=1.0, ls=":")
    ax.text(
        1.7,
        0.905,
        "0.90: above this single-window family",
        fontsize=8.5,
        color=COLORS["muted"],
        va="bottom",
        ha="center",
    )
    ax.text(
        1.55,
        0.34,
        "needs prime-pair correlations\nbeyond bandwidth 1 (open)",
        ha="center",
        va="center",
        fontsize=9,
        color=COLORS["guide"],
    )

    ax.set_xlim(0.5, 2.05)
    ax.set_ylim(0.0, 0.98)
    ax.set_xlabel(r"pair-correlation bandwidth $\lambda$")
    ax.set_ylabel("achievable proportion on the line")
    ax.set_title("How far the method can reach")
    ax.legend(loc="lower right", fontsize=9)

    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
