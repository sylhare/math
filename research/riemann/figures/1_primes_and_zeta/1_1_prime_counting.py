"""Figure: the prime-counting staircase against its two approximations.

    pi(x)       = #{p prime : p <= x}                        the staircase, +1 at each prime
    x / log x   ~ pi(x)                                      prime number theorem density
    Li(x)       = int_2^x dt / log t                         the sharper guess (quadrature)
    E(x)        = pi(x) - Li(x)                              the error the whole subject controls

Reproduces pi(1000) = 168, Li(1000) ~ 177.6, 1000/log(1000) ~ 144.8.

Run: PYTHONPATH=research/riemann/figures uv run --with matplotlib --with mpmath --with pillow \
     python research/riemann/figures/1_primes_and_zeta/1_1_prime_counting.py
"""

import math

import numpy as np
from _shared import COLORS, math_check, plot_axes, primes_up_to, save_preview

XMAX = 1000


def prime_staircase(primes: np.ndarray, xs: np.ndarray) -> np.ndarray:
    """pi(x) sampled on xs: the number of primes <= x at each grid point."""
    return np.searchsorted(primes, xs, side="right").astype(float)


def logarithmic_integral(xs: np.ndarray) -> np.ndarray:
    """Li(x) = int_2^x dt/log t by cumulative trapezoid on the grid xs (xs[0] = 2)."""
    integrand = 1.0 / np.log(xs)
    widths = np.diff(xs)
    seg = 0.5 * (integrand[1:] + integrand[:-1]) * widths
    return np.concatenate(([0.0], np.cumsum(seg)))


def main():
    import mpmath

    primes = primes_up_to(XMAX)
    grid = np.linspace(2.0, XMAX, 40000)
    pi_grid = prime_staircase(primes, grid)
    li_grid = logarithmic_integral(grid)
    xlog_grid = grid / np.log(grid)

    pi_1000 = int(prime_staircase(primes, np.array([XMAX]))[0])
    li_1000 = float(li_grid[-1])
    xlog_1000 = float(XMAX / math.log(XMAX))
    offset_li_1000 = float(mpmath.li(XMAX))

    assert pi_1000 == 168, f"pi(1000) = {pi_1000}, expected 168"
    assert abs(li_1000 - (offset_li_1000 - float(mpmath.li(2)))) < 1e-2, "int_2^x = li(x) - li(2)"

    math_check(
        "Counting the primes: pi(x) vs x/log x vs Li(x)",
        [
            ("pi(1000) = #primes <= 1000", f"{pi_1000}   (want 168)"),
            ("Li(1000) = int_2^1000 dt/log t", f"{li_1000:.2f}   (article's lower limit 2)"),
            ("li(1000) = int_0^1000 dt/log t", f"{offset_li_1000:.2f}   (want ~177.6; differs by li(2)~1.05)"),
            ("1000 / log(1000)", f"{xlog_1000:.2f}   (want ~144.8)"),
            ("error E(1000) = pi - Li", f"{pi_1000 - li_1000:.2f}   (the wobble Part 3 controls)"),
            (
                "Li closer than x/log x",
                f"|pi-Li|={abs(pi_1000 - li_1000):.1f} < |pi-x/log x|={abs(pi_1000 - xlog_1000):.1f}",
            ),
        ],
    )

    fig, ax = plot_axes(figsize=(7.4, 5.4))
    ax.plot(grid, pi_grid, color=COLORS["prime"], lw=1.8, label=r"$\pi(x)$")
    ax.plot(grid, li_grid, color=COLORS["guide"], lw=1.6, label=r"$\mathrm{Li}(x)=\int_2^x dt/\log t$")
    ax.plot(grid, xlog_grid, color=COLORS["muted"], lw=1.6, ls="--", label=r"$x/\log x$")

    ax.set_xlim(0, XMAX)
    ax.set_ylim(0, max(pi_grid.max(), li_grid.max()) * 1.05)
    ax.set_xlabel("x")
    ax.set_ylabel("count")
    ax.set_title("Counting the primes")
    ax.legend(loc="upper left", framealpha=0.9)

    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
