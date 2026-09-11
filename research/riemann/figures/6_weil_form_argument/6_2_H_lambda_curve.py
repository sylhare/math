"""Figure: the closed forms the finite Weil form certifies, as functions of bandwidth lambda.

    H(lambda)     = 2 - 1/lambda - lambda/3        proportion on the line (flat window)   H(1) = 2/3
    H_opt(lambda) = 2 - 1/c*_lambda                same, optimal window                   H_opt(1) = 0.6725
    H_d(lambda)   = (1 + H(lambda)) / 2            proportion of distinct zeros           H_d(1) = 5/6
    F(lambda)     = lambda / (1 + lambda^2/3)      the moment ratio target                F(1) = 3/4

with c*_lambda = sqrt2 tan(theta)/(1 + theta tan(theta)), theta = lambda/sqrt2 (Montgomery-Taylor).
The optimal window sits just above the flat one and reaches 0.6725 at lambda = 1, a maximum of the
functional at bandwidth one (no window does better). The previous record 5/12 = 0.4167 (PRZZ 2020) is
a faint reference.

Run: PYTHONPATH=research/riemann/figures uv run --with matplotlib --with mpmath --with pillow \
     python research/riemann/figures/6_weil_form_argument/6_2_H_lambda_curve.py
"""

import numpy as np
from _shared import COLORS, math_check, plot_axes, save_preview

LAM_LO, LAM_HI = 0.3, 1.0
SQRT2 = np.sqrt(2.0)
CEILING = 0.67250
PREV_RECORD = 5.0 / 12.0


def H(lam):
    """H(lambda) = 2 - 1/lambda - lambda/3, the on-line proportion the flat window certifies."""
    return 2.0 - 1.0 / lam - lam / 3.0


def c_star(lam):
    """Montgomery-Taylor form factor c*_lambda = sqrt2 tan(theta)/(1 + theta tan(theta))."""
    theta = lam / SQRT2
    return SQRT2 * np.tan(theta) / (1.0 + theta * np.tan(theta))


def H_opt(lam):
    """H_opt(lambda) = 2 - 1/c*_lambda, the optimal-window on-line proportion."""
    return 2.0 - 1.0 / c_star(lam)


def H_d(lam):
    """H_d(lambda) = (1 + H(lambda)) / 2, the distinct-zero proportion."""
    return (1.0 + H(lam)) / 2.0


def F(lam):
    """F(lambda) = lambda / (1 + lambda^2/3), the trace-moment ratio target."""
    return lam / (1.0 + lam * lam / 3.0)


def main():
    lam = np.linspace(LAM_LO, LAM_HI, 400)
    h, hopt, hd, f = H(lam), H_opt(lam), H_d(lam), F(lam)

    h1, hopt1, hd1, f1 = H(1.0), H_opt(1.0), H_d(1.0), F(1.0)
    assert abs(h1 - 2 / 3) < 1e-12, f"H(1) = {h1}, expected 2/3"
    assert abs(hopt1 - CEILING) < 1e-4, f"H_opt(1) = {hopt1}, expected 0.67250"
    assert abs(hd1 - 5 / 6) < 1e-12, f"H_d(1) = {hd1}, expected 5/6"
    assert abs(f1 - 3 / 4) < 1e-12, f"F(1) = {f1}, expected 3/4"

    math_check(
        "What the finite form certifies: H, H_opt, H_d, F at lambda = 1",
        [
            ("H(1) = 2 - 1 - 1/3 (flat window)", f"{h1:.4f}   (want 2/3 = 0.6667)"),
            ("H_opt(1) = 2 - 1/c*_1 (optimal window)", f"{hopt1:.5f}   (Montgomery-Taylor 0.67250)"),
            ("H_d(1) = (1 + 2/3)/2", f"{hd1:.4f}   (want 5/6 = 0.8333)"),
            ("F(1) = 1/(1 + 1/3)", f"{f1:.4f}   (want 3/4 = 0.75)"),
            ("functional max at lambda = 1", f"{CEILING:.5f}   (no window beats Montgomery-Taylor)"),
            ("previous record 5/12 (PRZZ 2020)", f"{PREV_RECORD:.5f}"),
        ],
    )

    fig, ax = plot_axes(figsize=(7.6, 5.4))
    ax.plot(lam, hd, color=COLORS["prime"], lw=2.0, label=r"$H_d(\lambda)=\frac{1+H}{2}$")
    ax.plot(lam, f, color=COLORS["guide"], lw=2.0, label=r"$F(\lambda)=\frac{\lambda}{1+\lambda^2/3}$")
    ax.plot(lam, hopt, color=COLORS["onlinepos"], lw=1.6, ls="--", label=r"$H_{\mathrm{opt}}(\lambda)=2-1/c^*_\lambda$")
    ax.plot(lam, h, color=COLORS["zero"], lw=2.2, label=r"$H(\lambda)=2-\frac{1}{\lambda}-\frac{\lambda}{3}$")

    ax.plot([1.0], [h1], "o", color=COLORS["zero"], ms=7, zorder=5)
    ax.annotate(
        r"$H(1)=\frac{2}{3}$",
        xy=(1.0, h1),
        xytext=(0.74, h1 - 0.10),
        fontsize=11,
        color=COLORS["zero"],
        arrowprops=dict(arrowstyle="->", color=COLORS["zero"], lw=1.2),
    )
    ax.plot([1.0], [hopt1], "o", color=COLORS["onlinepos"], ms=6, zorder=5)
    ax.annotate(
        "optimal window\n0.6725 (ceiling)",
        xy=(1.0, hopt1),
        xytext=(0.62, hopt1 + 0.07),
        fontsize=8.5,
        color=COLORS["onlinepos"],
        arrowprops=dict(arrowstyle="->", color=COLORS["onlinepos"], lw=1.0),
    )
    ax.axhline(PREV_RECORD, color=COLORS["muted"], lw=1.0, ls=":")
    ax.text(LAM_LO + 0.01, PREV_RECORD + 0.006, "previous record 5/12", fontsize=8.5, color=COLORS["muted"])

    ax.set_xlim(LAM_LO, LAM_HI)
    ax.set_ylim(0.0, 0.9)
    ax.set_xlabel(r"bandwidth $\lambda$")
    ax.set_ylabel("certified proportion")
    ax.set_title("What the finite form certifies")
    ax.legend(loc="upper left", framealpha=0.9)

    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
