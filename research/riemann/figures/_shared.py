"""Shared number-theory data, validation, and styling helpers for the Riemann figures.

Mirror of the Kakeya figures framework: pure-numpy math, matplotlib only for preview,
every script ends with a printed ``MATH CHECK`` block.

Run: uv run --with matplotlib --with mpmath python research/riemann/figures/<part>/<name>.py
"""

from __future__ import annotations

import inspect
import math
import os

import numpy as np

# Palette (mirrors the article's colour logic)
COLORS = {
    "prime": "#1f77b4",  # primes / arithmetic side
    "zero": "#d62728",  # nontrivial zeros / the critical line
    "line": "#111111",  # the critical line Re s = 1/2
    "offline": "#ff7f0e",  # hypothetical off-line zeros
    "region": "#9ecae1",  # strips / bands, faint
    "onlinepos": "#2ca02c",  # on-line (positive) contribution
    "guide": "#555555",  # axes, arrows
    "muted": "#999999",
}

# Imaginary parts gamma_k > 0 of the first nontrivial zeros rho = 1/2 + i*gamma_k
# (six-decimal standard values; the conjugates -gamma_k are also zeros).
ZETA_ZEROS = np.array(
    [
        14.134725,
        21.022040,
        25.010858,
        30.424876,
        32.935062,
        37.586178,
        40.918719,
        43.327073,
        48.005151,
        49.773832,
        52.970321,
        56.446248,
        59.347044,
        60.831779,
        65.112544,
        67.079811,
        69.546402,
        72.067158,
        75.704691,
        77.144840,
        79.337375,
        82.910381,
        84.735493,
        87.425275,
        88.809111,
        92.491899,
        94.651344,
        95.870634,
        98.831194,
        101.317851,
        103.725539,
        105.446623,
        107.168611,
        111.029536,
        111.874659,
        114.320221,
        116.226680,
        118.790783,
        121.370125,
        122.946829,
        124.256819,
        127.516684,
        129.578704,
        131.087689,
        133.497737,
        134.756510,
        138.116042,
        139.736209,
        141.123707,
        143.111846,
    ]
)


def zeta_zeros(n: int) -> np.ndarray:
    """First ``n`` positive ordinates gamma_k. Uses the table for n<=50, else mpmath."""
    if n <= len(ZETA_ZEROS):
        return ZETA_ZEROS[:n]
    import mpmath

    return np.array([float(mpmath.im(mpmath.zetazero(k))) for k in range(1, n + 1)])


def primes_up_to(n: int) -> np.ndarray:
    """Primes <= n by a simple sieve."""
    if n < 2:
        return np.array([], dtype=int)
    sieve = np.ones(n + 1, dtype=bool)
    sieve[:2] = False
    for p in range(2, int(n**0.5) + 1):
        if sieve[p]:
            sieve[p * p :: p] = False
    return np.flatnonzero(sieve)


def von_mangoldt(n: int) -> np.ndarray:
    """Array Lambda(k), k=0..n: log p if k is a prime power p^m, else 0."""
    lam = np.zeros(n + 1)
    for p in primes_up_to(n):
        lp = math.log(p)
        pk = p
        while pk <= n:
            lam[pk] = lp
            pk *= p
    return lam


def psi(x: float, lam: np.ndarray) -> float:
    """Chebyshev psi(x) = sum_{p^m <= x} log p, from a precomputed von Mangoldt array."""
    k = min(math.floor(x), len(lam) - 1)
    return float(lam[: k + 1].sum())


# Preview + reporting (identical contract to the Kakeya framework)
def plot_axes(ncols: int = 1, figsize=None, equal: bool = False):
    """Standard matplotlib axes with a light grid; ``equal`` for complex-plane figures."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, ncols, figsize=figsize or (6.2 * ncols, 5.2))
    axes = np.atleast_1d(axes)
    for ax in axes:
        ax.grid(True, color="#e6e6e6", lw=0.8)
        ax.set_axisbelow(True)
        if equal:
            ax.set_aspect("equal")
    return fig, (axes[0] if ncols == 1 else axes)


def save_preview(fig, dpi: int = 140) -> str:
    """Save ``<callerfile>.png`` next to the calling module; return the path."""
    caller = inspect.stack()[1].filename
    out = os.path.splitext(caller)[0] + ".png"
    fig.tight_layout()
    fig.savefig(out, dpi=dpi)
    return out


def save_gif(anim, fps: int = 18, dpi: int = 100) -> str:
    """Save ``<callerfile>.gif`` next to the calling module via PillowWriter; return the path."""
    from matplotlib.animation import PillowWriter

    caller = inspect.stack()[1].filename
    out = os.path.splitext(caller)[0] + ".gif"
    anim.save(out, writer=PillowWriter(fps=fps), dpi=dpi)
    return out


def math_check(title: str, rows: list[tuple[str, str]]) -> None:
    """Print a standardized validation block: (claim, value/verdict) rows."""
    print(f"\n=== MATH CHECK: {title} ===")
    w = max((len(r[0]) for r in rows), default=0)
    for claim, value in rows:
        print(f"  {claim.ljust(w)} : {value}")
    print("=" * (len(title) + 18))
