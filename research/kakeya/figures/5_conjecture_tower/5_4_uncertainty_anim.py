"""Animation: the uncertainty principle as a Gaussian narrowing in x, widening in xi (Hickman Fig 5).

Mirror of the static `uncertainty_principle.py`, set in motion. Sweep the width of a Gaussian
g(x) = exp(-x^2 / (2 sigma^2)) (physical std sigma_x = sigma). Its Fourier transform is again
Gaussian, with frequency std

    sigma_xi = 1 / (2 pi sigma),

so the two widths are reciprocal. As sigma shrinks the bump in x narrows while its transform in xi
widens, and the dual "uncertainty box" (sigma_x wide, sigma_xi tall) swaps aspect from short-and-wide
to tall-and-narrow while keeping the same area.

INVARIANT asserted at the end: the product  sigma_x * sigma_xi = 1 / (2 pi)  is held constant across
ALL frames (min and max of the measured product are printed and pinned to 1/(2 pi)). sigma_xi is
measured by FFT of the sampled Gaussian, not just quoted.

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/uncertainty_anim.py
"""
import math

import numpy as np
from _shared import COLORS, math_check, save_gif
from matplotlib.animation import FuncAnimation


def gaussian_freq_std(sigma: float) -> tuple[float, float]:
    """FFT g(x)=exp(-x^2/2sigma^2) and return (measured, analytic 1/(2 pi sigma)) frequency std."""
    L, n = 40.0 * sigma, 8192  # wide, fine window so tails and bins are well resolved
    x = np.linspace(-L / 2, L / 2, n, endpoint=False)
    dx = x[1] - x[0]
    g = np.exp(-(x**2) / (2 * sigma**2))
    ghat = np.abs(np.fft.fftshift(np.fft.fft(g))) * dx
    xi = np.fft.fftshift(np.fft.fftfreq(n, d=dx))
    w = ghat / ghat.sum()  # treat |g_hat| as a mass distribution (>= 0 here)
    mean = np.sum(w * xi)
    std = math.sqrt(np.sum(w * (xi - mean) ** 2))
    return std, 1.0 / (2 * math.pi * sigma)


def main():
    target = 1.0 / (2 * math.pi)
    sigmas = np.linspace(1.4, 0.35, 34)  # narrowing sweep

    products, sxi_meas = [], []
    for sg in sigmas:
        m, _ = gaussian_freq_std(sg)
        sxi_meas.append(m)
        products.append(sg * m)
    products = np.array(products)
    sxi_meas = np.array(sxi_meas)

    within = bool(np.all(np.abs(products - target) < 0.02 * target))

    math_check(
        "uncertainty principle: Gaussian sweep (animated)",
        [
            ("g(x)", "exp(-x^2 / (2 sigma^2)),   sigma_xi = 1/(2 pi sigma)"),
            ("sigma sweep", f"{sigmas[0]:.3f}  ->  {sigmas[-1]:.3f}  ({len(sigmas)} frames, narrowing)"),
            ("sigma_x * sigma_xi target", f"1/(2 pi) = {target:.5f}"),
            ("product min / max over frames", f"{products.min():.5f} / {products.max():.5f}"),
            ("product constant ~ 1/(2 pi)?", "YES" if within else "NO"),
            ("2 pi * product (want ~1)", f"min {2*math.pi*products.min():.4f}  max {2*math.pi*products.max():.4f}"),
        ],
    )
    assert within, "sigma_x * sigma_xi must stay ~1/(2 pi) across all frames"

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    fig, ax = plt.subplots(1, 2, figsize=(12.5, 5.2))

    # (a) the dual Gaussians
    xx = np.linspace(-4, 4, 800)
    gx, = ax[0].plot([], [], color=COLORS["accent"], lw=2.0, label="g(x)  (physical)")
    gh, = ax[0].plot([], [], color=COLORS["outer"], lw=2.0, label="g_hat(xi)  (frequency)")
    ax[0].set_xlim(-4, 4)
    ax[0].set_ylim(0, 1.08)
    ax[0].set_xlabel("x   or   xi")
    ax[0].set_ylabel("amplitude")
    ax[0].legend(fontsize=9, loc="upper right")

    # (b) the uncertainty box: sigma_x wide x sigma_xi tall, constant area
    smax = float(sigmas.max())
    box = Rectangle((0, 0), 1, 1, facecolor=COLORS["region"], edgecolor=COLORS["needle"], lw=1.8)
    ax[1].add_patch(box)
    ax[1].axhline(0, color=COLORS["muted"], lw=0.6)
    ax[1].axvline(0, color=COLORS["muted"], lw=0.6)
    ax[1].set_xlim(-0.1, smax * 1.15)
    ax[1].set_ylim(-0.1, smax * 1.15)
    ax[1].set_aspect("equal")
    ax[1].set_xlabel("sigma_x  (physical width)")
    ax[1].set_ylabel("sigma_xi  (frequency width)")

    def update(i):
        sg = float(sigmas[i])
        sxi = float(sxi_meas[i])
        ax[0].set_title(f"sigma = {sg:.3f}:  narrow in x  <=>  wide in xi")
        gx.set_data(xx, np.exp(-(xx**2) / (2 * sg**2)))
        gh.set_data(xx, np.exp(-2 * math.pi**2 * sg**2 * xx**2))
        box.set_width(sg)
        box.set_height(sxi)
        ax[1].set_title(f"box  sigma_x * sigma_xi = {sg*sxi:.4f}  (= 1/(2 pi) = {target:.4f})")
        return gx, gh, box

    anim = FuncAnimation(fig, update, frames=len(sigmas), interval=140, blit=False)
    print("wrote", save_gif(anim, fps=8, dpi=95))


if __name__ == "__main__":
    main()
