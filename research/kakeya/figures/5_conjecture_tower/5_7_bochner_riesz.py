"""Bochner-Riesz multiplier profile (kakeya.md 5c-ii).

Radial multiplier m^alpha_R(xi) = (1 - |xi|^2 / R^2)_+^alpha, (.)_+ = max(., 0). alpha = 0 is
Fefferman's hard-edge ball multiplier; larger alpha rounds the edge. Radial slice at R = 1:

    m^alpha(x) = (1 - x^2)_+^alpha .

Left: alpha = 1/4 slice (corner with slope -> -inf at x = +-1). Right: alpha = 0, 1/4, 1 overlaid.

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/bochner_riesz.py
"""
import numpy as np
from _shared import COLORS, math_check, new_axes, save_preview


def profile(x: np.ndarray, alpha: float, radius: float = 1.0) -> np.ndarray:
    """m^alpha_R(x) = (1 - x^2 / R^2)_+^alpha along a radial slice."""
    base = np.clip(1.0 - (x / radius) ** 2, 0.0, None)
    return base ** alpha


def main():
    alpha = 0.25
    samples = np.array([-1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5])
    got = profile(samples, alpha)
    expected = np.array([0.0, 0.0, 0.75 ** 0.25, 1.0, 0.75 ** 0.25, 0.0, 0.0])
    max_err = float(np.max(np.abs(got - expected)))

    # corner at x = +-1: interior slope is finite, but as x -> 1^- the slope blows up
    def slope(x0, h=1e-6):
        return (profile(np.array([x0]), alpha)[0] - profile(np.array([x0 - h]), alpha)[0]) / h

    slope_interior = slope(0.5)      # finite
    slope_near_one = slope(1.0 - 1e-4)  # large negative -> vertical tangent (corner)

    math_check(
        "Bochner-Riesz profile  (1 - x^2)_+^{1/4}",
        [
            ("m^alpha(x) = (1 - x^2)_+^alpha", f"alpha = {alpha}"),
            ("m(0)", f"{got[3]:.6f}  (want 1)"),
            ("m(+-0.5) = 0.75^{1/4}", f"{got[2]:.6f}  (want {0.75 ** 0.25:.6f})"),
            ("m(+-1)", f"{got[5]:.6f}  (want 0)"),
            ("m(+-1.5)  (outside support)", f"{got[6]:.6f}  (want 0)"),
            ("max |profile - (1-x^2)^{1/4}|", f"{max_err:.2e}  (< 1e-12 ok)"),
            ("continuity at x=1", f"m(1)={got[5]:.6f}, m(1.5)={got[6]:.6f}  (both 0)"),
            ("slope at x=0.5  (finite, interior)", f"{slope_interior:.3f}"),
            ("slope at x->1^-  (corner, -> -inf)", f"{slope_near_one:.1f}"),
        ],
    )

    fig, ax = new_axes(2, figsize=(13, 4.2))
    for a in ax:
        a.set_aspect("auto")
        a.axis("on")
        for spine in ("top", "right", "left", "bottom"):
            a.spines[spine].set_visible(False)

    x = np.linspace(-1.6, 1.6, 800)

    # left panel: alpha = 1/4 slice, dotted box, +-R marks
    axis_lw = 1.1
    for a in ax:
        a.annotate("", xy=(1.62, 0), xytext=(-1.62, 0),
                   arrowprops=dict(arrowstyle="->", color="k", lw=axis_lw))
        a.annotate("", xy=(0, 1.28), xytext=(0, -0.06),
                   arrowprops=dict(arrowstyle="->", color="k", lw=axis_lw))
        a.text(1.63, -0.02, r"$\xi$", ha="left", va="top", fontsize=13)
        a.set_xlim(-1.75, 1.8)
        a.set_ylim(-0.12, 1.35)
        a.set_xticks([])
        a.set_yticks([])

    ax[0].plot([-1, -1, 1, 1], [0, 1, 1, 0], ":", color=COLORS["guide"], lw=1.2)  # dotted box, height 1
    ax[0].plot(x, profile(x, alpha), color="blue", lw=2.6)
    ax[0].text(-1.0, -0.02, r"$-R$", ha="center", va="top", fontsize=13)
    ax[0].text(1.0, -0.02, r"$R$", ha="center", va="top", fontsize=13)
    ax[0].set_title(r"$m^{\alpha}_R(\xi)=(1-|\xi|^2/R^2)_+^{\alpha}$,  $\alpha=\frac{1}{4}$")

    # right panel: overlay alpha = 0, 1/4, 1
    styles = [(0.0, COLORS["accent"], r"$\alpha=0$"),
              (0.25, "blue", r"$\alpha=\frac{1}{4}$"),
              (1.0, COLORS["outer"], r"$\alpha=1$")]
    for a_val, col, lab in styles:
        y = profile(x, a_val)
        if a_val == 0.0:  # hard edges of the indicator (vertical jumps)
            xin = x[np.abs(x) <= 1]
            ax[1].plot(xin, np.ones_like(xin), color=col, lw=2.4, label=lab)
            ax[1].plot([-1, -1], [0, 1], color=col, lw=2.4)
            ax[1].plot([1, 1], [0, 1], color=col, lw=2.4)
        else:
            ax[1].plot(x, y, color=col, lw=2.4, label=lab)
    ax[1].text(-1.0, -0.02, r"$-R$", ha="center", va="top", fontsize=13)
    ax[1].text(1.0, -0.02, r"$R$", ha="center", va="top", fontsize=13)
    ax[1].legend(loc="upper right", frameon=False, fontsize=12)
    ax[1].set_title(r"rounding the edge as $\alpha$ grows:  $\alpha=0,\ \frac{1}{4},\ 1$")

    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
