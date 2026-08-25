"""Animation: rebuild the prime-power staircase psi(x) from the zeros.

The true Chebyshev staircase psi(x) = sum_{p^m <= x} log p (muted steps) is fixed, and the
explicit-formula approximation

    psi_K(x) = x - log(2 pi) - 0.5 log(1 - x^-2) - sum_{k=1}^K 2 Re(x^rho_k / rho_k),

with rho_k = 1/2 + i gamma_k over the first K zero ordinates, sharpens onto it as K grows.

Run: PYTHONPATH=research/riemann/figures uv run --with matplotlib --with mpmath --with pillow \
  python research/riemann/figures/3_why_it_matters/3_1_explicit_formula_anim.py
"""

import math

import numpy as np
from _shared import COLORS, ZETA_ZEROS, math_check, plot_axes, psi, save_gif, von_mangoldt
from matplotlib.animation import FuncAnimation

X_LO, X_HI = 2.0, 50.0
K_MAX = 40
GRID = 900


def psi_approx(x, gammas):
    """Explicit-formula partial sum psi_K(x) over the given zero ordinates gammas."""
    rho = 0.5 + 1j * gammas
    smooth = x - math.log(2 * math.pi) - 0.5 * np.log1p(-(x**-2.0))
    osc = np.zeros_like(x)
    if len(gammas):
        contrib = np.power.outer(x, rho) / rho
        osc = 2.0 * np.real(contrib).sum(axis=1)
    return smooth - osc


def main():
    xs = np.linspace(X_LO, X_HI, GRID)
    lam = von_mangoldt(math.ceil(X_HI))
    true_psi = np.array([psi(x, lam) for x in xs])

    curves = [psi_approx(xs, ZETA_ZEROS[:k]) for k in range(K_MAX + 1)]
    l2 = [float(np.sqrt(np.mean((c - true_psi) ** 2))) for c in curves]

    err_k1, err_k40 = l2[1], l2[K_MAX]
    assert err_k40 < err_k1, f"L2 error did not decrease: K1={err_k1}, K40={err_k40}"

    math_check(
        "explicit formula rebuilds psi(x)",
        [
            ("psi jumps by log 2 at x=2,4,8,16,32", f"log 2 = {math.log(2):.4f}"),
            ("psi jumps by log 3 at x=3,9,27", f"log 3 = {math.log(3):.4f}"),
            ("psi jumps by log 5 at x=5,25", f"log 5 = {math.log(5):.4f}"),
            ("L2 error at K=1", f"{err_k1:.4f}"),
            ("L2 error at K=40", f"{err_k40:.4f}"),
            ("error decreased K=1 -> K=40", f"{err_k1:.4f} > {err_k40:.4f}  -> True"),
        ],
    )

    all_vals = np.concatenate([true_psi, *curves])
    pad = 0.05 * (all_vals.max() - all_vals.min())
    y_lo, y_hi = all_vals.min() - pad, all_vals.max() + pad

    fig, ax = plot_axes(figsize=(7.6, 5.2))
    ax.plot(xs, true_psi, color=COLORS["muted"], lw=1.6, label=r"true $\psi(x)$")
    (live,) = ax.plot([], [], color=COLORS["zero"], lw=2.0, label=r"$\psi_K(x)$")
    readout = ax.text(0.03, 0.95, "", transform=ax.transAxes, va="top", ha="left", fontsize=12, color=COLORS["zero"])
    ax.set_xlim(X_LO, X_HI)
    ax.set_ylim(y_lo, y_hi)
    ax.set_xlabel("x")
    ax.set_ylabel(r"$\psi$")
    ax.set_title("Primes from the zeros")
    ax.legend(loc="lower right")

    frames = list(range(K_MAX + 1)) + [K_MAX] * 6

    def update(i):
        k = frames[i]
        live.set_data(xs, curves[k])
        readout.set_text(f"K = {k} zero pairs\nL2 = {l2[k]:.3f}")
        return live, readout

    anim = FuncAnimation(fig, update, frames=len(frames), interval=120, blit=False)
    print("wrote", save_gif(anim, fps=12, dpi=100))


if __name__ == "__main__":
    main()
