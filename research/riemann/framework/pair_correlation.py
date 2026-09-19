"""Montgomery's pair correlation of real zeta zeros: the arithmetic input, seen directly.

The second moment the proof uses is Montgomery's pair correlation. Its shape is already visible in
the real zeros: after unfolding the ordinates to mean spacing 1, the density of differences between
zeros follows

    R_2(u) = 1 - (sin(pi u) / (pi u))^2 ,

the same law as the eigenvalue spacings of a random Hermitian matrix. The dip to 0 at u = 0 is the
repulsion between zeros that the second moment measures.

This module computes the empirical pair correlation from the cached zeros and checks it against
R_2(u): near u = 0 the density is suppressed (repulsion), and away from 0 it settles near 1.

Run: uv run --with numpy --with mpmath python research/riemann/framework/pair_correlation.py
"""

from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from zeros import load_zeros, unfold


def montgomery_R2(u: np.ndarray) -> np.ndarray:
    """The pair-correlation form 1 - (sin pi u / pi u)^2 (GUE / Montgomery)."""
    x = np.pi * u
    sinc = np.where(np.abs(x) < 1e-12, 1.0, np.sin(x) / np.where(x == 0, 1.0, x))
    return 1 - sinc**2


def empirical_pair_correlation(n_zeros: int, u_max: float = 3.0, bins: int = 60) -> tuple:
    """Histogram of unfolded zero differences in (0, u_max]; returns (centres, density)."""
    w = unfold(load_zeros(n_zeros))
    diffs = []
    for i in range(len(w)):
        d = w[i + 1 :] - w[i]
        diffs.append(d[d <= u_max])
    diffs = np.concatenate(diffs)
    edges = np.linspace(0, u_max, bins + 1)
    counts, _ = np.histogram(diffs, bins=edges)
    width = edges[1] - edges[0]
    density = counts / (len(w) * width)
    centres = (edges[:-1] + edges[1:]) / 2
    return centres, density


def main() -> None:
    centres, density = empirical_pair_correlation(1200)
    model = montgomery_R2(centres)
    near = centres < 0.5
    far = centres > 1.5
    print("\n=== MATH CHECK: pair correlation of real zeros ===")
    rows = [
        ("zeros used", "1200 (cached)"),
        (
            "mean density near u<0.5 (repulsion)",
            f"{density[near].mean():.3f}  (R_2 ~ {model[near].mean():.3f}: suppressed)",
        ),
        ("mean density far u>1.5", f"{density[far].mean():.3f}  (R_2 ~ {model[far].mean():.3f}: near 1)"),
        ("R_2(u) = 1 - (sin pi u / pi u)^2", "Montgomery / GUE law"),
    ]
    w = max(len(r[0]) for r in rows)
    for a, b in rows:
        print(f"  {a.ljust(w)} : {b}")
    print("=" * 50)
    assert density[near].mean() < density[far].mean(), "zeros must repel: near-zero density suppressed"
    assert density[far].mean() > 0.6, "far density should settle near 1"


if __name__ == "__main__":
    main()
