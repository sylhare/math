"""Static: the prime error psi(x)-x inside the envelope x^Theta.

psi(x)-x (from the von Mangoldt cumulative minus x) sits inside the envelope +/- c x^Theta with
Theta = sup Re(rho) the rightmost zero. On the hypothesis Theta = 1/2, the narrowest possible band;
a single zero at beta = 0.7 would widen it to the outer x^0.7 curve. The same constant c is used
for both so the shapes compare directly.

Run: PYTHONPATH=research/riemann/figures uv run --with matplotlib --with mpmath --with pillow \
  python research/riemann/figures/3_why_it_matters/3_2_pnt_error.py
"""

import numpy as np
from _shared import COLORS, math_check, plot_axes, save_preview, von_mangoldt

X_HI = 1000
C_BAND = 1.5
THETA_RH = 0.5
BETA = 0.7


def main():
    lam = von_mangoldt(X_HI)
    cum = np.cumsum(lam)
    xs = np.arange(2, X_HI + 1)
    err = cum[2 : X_HI + 1] - xs

    rh_band = C_BAND * xs**THETA_RH
    off_band = C_BAND * xs**BETA

    max_abs_err = float(np.max(np.abs(err)))
    within_rh = bool(np.all(np.abs(err) <= rh_band))

    math_check(
        "prime error band",
        [
            ("Theta = sup Re(rho) controls the band", "rightmost zero ordinate"),
            ("RH gives Theta=1/2, band ~ x^0.5", "narrowest possible envelope"),
            ("zero at beta=0.7 widens band to ~ x^0.7", "outer envelope"),
            ("shared constant c", f"{C_BAND}"),
            ("max |psi(x)-x| on [2,1000]", f"{max_abs_err:.4f}"),
            ("stays within x^0.5 RH band", f"{within_rh}"),
        ],
    )

    fig, ax = plot_axes(figsize=(7.8, 5.2))
    ax.axhline(0.0, color=COLORS["guide"], lw=0.8)
    ax.plot(xs, off_band, color=COLORS["offline"], lw=1.4, ls="--", label=r"$\beta=0.7$ band $\sim x^{0.7}$")
    ax.plot(xs, -off_band, color=COLORS["offline"], lw=1.4, ls="--")
    ax.plot(xs, rh_band, color=COLORS["zero"], lw=1.6, label=r"RH band $\sim x^{0.5}$")
    ax.plot(xs, -rh_band, color=COLORS["zero"], lw=1.6)
    ax.plot(xs, err, color=COLORS["prime"], lw=1.0, label=r"$\psi(x)-x$")

    top = float(off_band.max())
    ax.set_xlim(2, X_HI)
    ax.set_ylim(-1.1 * top, 1.1 * top)
    ax.set_xlabel("x")
    ax.set_ylabel(r"$\psi(x)-x$")
    ax.set_title("The prime error band")
    ax.legend(loc="upper left")

    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
