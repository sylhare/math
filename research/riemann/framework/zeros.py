"""Cached loader for the ordinates gamma_k of the nontrivial zeros rho = 1/2 + i gamma_k.

mpmath.zetazero is exact but slow, so the first few thousand ordinates are computed once and cached
to ``zeros_cache.npy`` next to this file. Used by the framework and (indirectly) the figures.

Run directly to precompute the cache: uv run --with numpy --with mpmath python .../framework/zeros.py 1200
"""

from __future__ import annotations

import os
import sys

import numpy as np

CACHE = os.path.join(os.path.dirname(__file__), "zeros_cache.npy")


def load_zeros(n: int) -> np.ndarray:
    """First ``n`` positive ordinates gamma_k, cached across calls and runs."""
    cached = np.load(CACHE) if os.path.exists(CACHE) else np.empty(0)
    if len(cached) >= n:
        return cached[:n]
    import mpmath

    mpmath.mp.dps = 15
    gammas = np.array([float(mpmath.im(mpmath.zetazero(k))) for k in range(1, n + 1)])
    np.save(CACHE, gammas)
    return gammas


def unfold(gammas: np.ndarray) -> np.ndarray:
    """Rescale ordinates so the mean spacing is 1: w_k = gamma_k * log(gamma_k / 2pi) / (2pi)."""
    return gammas * np.log(gammas / (2 * np.pi)) / (2 * np.pi)


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1200
    g = load_zeros(n)
    print(f"cached {len(g)} zeros to {CACHE}; last gamma = {g[-1]:.4f}")
