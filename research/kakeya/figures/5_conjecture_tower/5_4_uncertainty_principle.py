"""Figure: the uncertainty principle as dual rectangles (Hickman Fig 5, Part 4).

A function whose Fourier transform is concentrated on a frequency box of side lengths  r x s
cannot itself be concentrated: in physical space it must spread over the reciprocal box of side
lengths  (1/r) x (1/s)  through the origin. Concentrated in frequency <=> spread in space, one axis
at a time. This is the geometry every wave packet obeys, so it is the reason a delta-tube in space
corresponds to a delta^{-1}-slab in frequency (the picture the Kakeya / Fefferman story is built on
in ../kakeya.md).

Symbolic first: with the transform  f_hat(xi) = int f(x) e^{-2 pi i x xi} dx, a frequency box of
sides r, s pairs with a physical box of sides 1/r, 1/s, so the products of dual side lengths are

    r * (1/r) = 1,      s * (1/s) = 1.

Backing it with a 1D Gaussian. Take  g(x) = exp(-x^2 / (2 sigma^2))  (physical std = sigma). Its
transform is again Gaussian,  g_hat(xi) = sigma sqrt(2 pi) exp(-2 pi^2 sigma^2 xi^2), with frequency
std  sigma_xi = 1 / (2 pi sigma).  So the two widths are reciprocal up to the 2 pi convention
constant:

    sigma * sigma_xi = 1 / (2 pi),      (2 pi) * sigma * sigma_xi = 1  (Gaussian saturates Heisenberg).

We verify sigma_xi by computing g_hat numerically (FFT) and measuring its standard deviation.

Reference: Hickman Fig 5 (not downloaded; redrawn from the description). Schematic boxes + 1D
Gaussian pair; builds its own matplotlib axes.
Run: uv run --with matplotlib --with shapely python research/kakeya/figures/uncertainty_principle.py
"""
import math

import numpy as np
from _shared import COLORS, math_check, save_preview


def gaussian_freq_std(sigma: float) -> tuple[float, float]:
    """Numerically FFT g(x)=exp(-x^2/2sigma^2) and return (measured, analytic) frequency std."""
    L, n = 40.0 * sigma, 8192  # wide, fine window so tails and bins are well resolved
    x = np.linspace(-L / 2, L / 2, n, endpoint=False)
    dx = x[1] - x[0]
    g = np.exp(-(x**2) / (2 * sigma**2))
    ghat = np.abs(np.fft.fftshift(np.fft.fft(g))) * dx
    xi = np.fft.fftshift(np.fft.fftfreq(n, d=dx))
    w = ghat / ghat.sum()  # treat |g_hat| as a mass distribution (it is >= 0 here)
    mean = np.sum(w * xi)
    std = math.sqrt(np.sum(w * (xi - mean) ** 2))
    return std, 1.0 / (2 * math.pi * sigma)


def main():
    r, s = 4.0, 1.5  # frequency-box side lengths
    fr, fs = 1.0 / r, 1.0 / s  # dual physical-box side lengths

    sigma = 0.8
    sigma_xi_meas, sigma_xi_exact = gaussian_freq_std(sigma)
    prod = sigma * sigma_xi_meas

    math_check(
        "uncertainty principle: dual rectangles",
        [
            ("transform", "f_hat(xi) = int f(x) e^{-2 pi i x xi} dx"),
            ("freq box sides  r x s", f"{r} x {s}"),
            ("phys box sides  (1/r) x (1/s)", f"{fr:.4f} x {fs:.4f}"),
            ("r * (1/r)", f"{r*fr:.4f}  (want 1)"),
            ("s * (1/s)", f"{s*fs:.4f}  (want 1)"),
            ("Gaussian sigma", f"{sigma}"),
            ("sigma_xi measured vs 1/(2 pi sigma)", f"{sigma_xi_meas:.4f}  vs  {sigma_xi_exact:.4f}"),
            ("sigma * sigma_xi", f"{prod:.4f}  (exact 1/(2 pi) = {1/(2*math.pi):.4f})"),
            ("2 pi * sigma * sigma_xi ~ 1", f"{2*math.pi*prod:.4f}"),
        ],
    )

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    fig, ax = plt.subplots(1, 3, figsize=(15.5, 5.0))

    # (a) frequency box r x s, centred at origin
    ax[0].add_patch(Rectangle((-r / 2, -s / 2), r, s, facecolor=COLORS["outer"], alpha=0.35, edgecolor=COLORS["outer"], lw=1.6))
    ax[0].axhline(0, color=COLORS["muted"], lw=0.6)
    ax[0].axvline(0, color=COLORS["muted"], lw=0.6)
    ax[0].annotate("", xy=(r / 2, -s / 2 - 0.35), xytext=(-r / 2, -s / 2 - 0.35), arrowprops=dict(arrowstyle="<->", color=COLORS["guide"]))
    ax[0].text(0, -s / 2 - 0.55, f"r = {r}", ha="center", va="top", fontsize=10)
    ax[0].annotate("", xy=(-r / 2 - 0.35, s / 2), xytext=(-r / 2 - 0.35, -s / 2), arrowprops=dict(arrowstyle="<->", color=COLORS["guide"]))
    ax[0].text(-r / 2 - 0.5, 0, f"s = {s}", ha="right", va="center", fontsize=10)
    ax[0].set_title("frequency box  r x s")
    ax[0].set_xlabel("xi_1")
    ax[0].set_ylabel("xi_2")
    ax[0].set_xlim(-r / 2 - 1.2, r / 2 + 1.2)
    ax[0].set_ylim(-r / 2 - 1.2, r / 2 + 1.2)
    ax[0].set_aspect("equal")

    # (b) dual physical box 1/r x 1/s, centred at origin (much taller than wide: reciprocal)
    ax[1].add_patch(Rectangle((-fr / 2, -fs / 2), fr, fs, facecolor=COLORS["accent"], alpha=0.35, edgecolor=COLORS["accent"], lw=1.6))
    ax[1].axhline(0, color=COLORS["muted"], lw=0.6)
    ax[1].axvline(0, color=COLORS["muted"], lw=0.6)
    ax[1].annotate("", xy=(fr / 2, -fs / 2 - 0.09), xytext=(-fr / 2, -fs / 2 - 0.09), arrowprops=dict(arrowstyle="<->", color=COLORS["guide"]))
    ax[1].text(0, -fs / 2 - 0.14, f"1/r = {fr:.3f}", ha="center", va="top", fontsize=10)
    ax[1].annotate("", xy=(-fr / 2 - 0.09, fs / 2), xytext=(-fr / 2 - 0.09, -fs / 2), arrowprops=dict(arrowstyle="<->", color=COLORS["guide"]))
    ax[1].text(-fr / 2 - 0.12, 0, f"1/s = {fs:.3f}", ha="right", va="center", fontsize=10)
    ax[1].set_title("dual physical box  (1/r) x (1/s)")
    ax[1].set_xlabel("x_1")
    ax[1].set_ylabel("x_2")
    lim = max(fr, fs) / 2 + 0.35
    ax[1].set_xlim(-lim, lim)
    ax[1].set_ylim(-lim, lim)
    ax[1].set_aspect("equal")

    # (c) 1D Gaussian pair: narrow in x <=> wide in xi
    xx = np.linspace(-4, 4, 800)
    ax[2].plot(xx, np.exp(-(xx**2) / (2 * sigma**2)), color=COLORS["accent"], lw=1.8, label=f"g(x), sigma={sigma}")
    ghat = np.exp(-2 * math.pi**2 * sigma**2 * xx**2)
    ax[2].plot(xx, ghat, color=COLORS["outer"], lw=1.8, label=f"g_hat(xi), sigma_xi={sigma_xi_exact:.3f}")
    ax[2].axvline(sigma, color=COLORS["accent"], ls="--", lw=0.8)
    ax[2].axvline(sigma_xi_exact, color=COLORS["outer"], ls="--", lw=0.8)
    ax[2].set_title("narrow in x  <=>  wide in xi")
    ax[2].set_xlabel("x  or  xi")
    ax[2].set_ylabel("amplitude")
    ax[2].set_xlim(-4, 4)
    ax[2].legend(fontsize=8)

    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
