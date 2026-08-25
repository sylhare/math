"""Figure: Euler's product approaching zeta on the real axis.

    zeta(s) = sum_{n>=1} n^-s = prod_{p prime} (1 - p^-s)^-1        Re s > 1
    P_k(s)  = prod over the first k primes of (1 - p^-s)^-1          partial product

The partial products rise to zeta from below as k grows (each factor > 1 is still missing).
Reproduces zeta(2) = pi^2/6 ~ 1.6449 and the product over primes up to 30 at s=2.

Run: PYTHONPATH=research/riemann/figures uv run --with matplotlib --with mpmath --with pillow \
     python research/riemann/figures/1_primes_and_zeta/1_2_euler_product.py
"""

import math

import numpy as np
from _shared import COLORS, math_check, plot_axes, primes_up_to, save_preview

K_VALUES = [1, 2, 3, 5]


def partial_product(primes: np.ndarray, s: np.ndarray) -> np.ndarray:
    """P(s) = prod_p (1 - p^-s)^-1 over the given primes, evaluated on the array s."""
    out = np.ones_like(s)
    for p in primes:
        out = out * 1.0 / (1.0 - float(p) ** (-s))
    return out


def main():
    import mpmath

    svals = np.linspace(1.2, 4.0, 400)
    primes = primes_up_to(30)

    zeta_true = np.array([float(mpmath.zeta(s)) for s in svals])
    curves = {k: partial_product(primes[:k], svals) for k in K_VALUES}

    zeta2 = math.pi**2 / 6.0
    prod30_at2 = float(partial_product(primes, np.array([2.0]))[0])

    for k in K_VALUES:
        assert np.all(curves[k] <= zeta_true + 1e-9), f"P_{k} must stay below zeta"
    assert abs(prod30_at2 - zeta2) < 2e-2, f"product to 30 at s=2 = {prod30_at2}, off zeta(2)"

    math_check(
        "Euler's product: partial products rise to zeta from below",
        [
            ("zeta(2) = pi^2/6", f"{zeta2:.4f}   (want 1.6449)"),
            ("mpmath zeta(2)", f"{float(mpmath.zeta(2)):.4f}"),
            (
                "product over primes <= 30 at s=2",
                f"{prod30_at2:.4f}   (matches zeta(2) to {abs(prod30_at2 - zeta2):.1e})",
            ),
            (
                "P_1(2) .. P_5(2) rising",
                "  ".join(f"{float(partial_product(primes[:k], np.array([2.0]))[0]):.4f}" for k in K_VALUES),
            ),
            ("P_k <= zeta for all k, s", "yes (each missing factor > 1)"),
        ],
    )

    fig, ax = plot_axes(figsize=(7.4, 5.4))
    ax.plot(svals, zeta_true, color=COLORS["zero"], lw=2.2, label=r"$\zeta(s)$")
    shades = np.linspace(0.75, 0.25, len(K_VALUES))
    for k, sh in zip(K_VALUES, shades, strict=True):
        ax.plot(
            svals, curves[k], color=COLORS["prime"], lw=1.5, alpha=float(sh), label=rf"$P_{{{k}}}(s)$, first {k} primes"
        )

    ax.set_xlim(svals[0], svals[-1])
    ax.set_ylim(1.0, max(zeta_true) * 1.05)
    ax.set_xlabel("s")
    ax.set_ylabel("value")
    ax.set_title("Euler's product")
    ax.legend(loc="upper right", framealpha=0.9)

    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
