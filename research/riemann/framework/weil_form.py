"""Build the finite compression G of Weil's form from real zeta zeros, and take its two moments.

The proof restricts Weil's Hermitian form to a family V of d ~ lambda*N modulated windows with centre
frequencies tau_k sampling the height window [T, 2T] at the critical density, and studies the d x d
matrix G. For zeros that are all on the critical line (real ordinates gamma_j) the form is a Gram
matrix

    G = sum_j v_j v_j^* ,   v_{j,k} = window(gamma_j - tau_k) ,

hence G >= 0. At the heights we can compute (far inside the verified range of RH) every zero is on
the line, so G is positive semidefinite and the certificate certifies nothing new; the two moments

    tr G  ~  N        (mean density of zeros)
    tr G^2 = ||G||_F^2  ~  (1/lambda + lambda/3) N   (Montgomery's second moment)

and the ratio C = (tr G)^2 / tr G^2 -> F(lambda) = lambda / (1 + lambda^2/3) come out of real data.

Two honesty notes. (i) At these heights RH is verified, so G is genuinely >= 0 and the certificate
certifies nothing new; that G >= 0 from real zeros is the thing we can check exactly here. (ii) The
exact Montgomery constant 1/lambda + lambda/3 is a property of the calibrated pair-correlation
kernel, not of an arbitrary window: the plain Gram window below gives a positive ratio in (0, 1) but
not that exact curve. The exact constant and F(lambda) are the closed forms returned by
``second_moment_constant`` / ``F``, cross-checked against the pair-correlation distribution of real
zeros in ``pair_correlation.py``. So this file proves G >= 0 and reports the finite moments; it does
not claim to fit F(lambda) from a Gaussian window.

Run: uv run --with numpy --with mpmath python research/riemann/framework/weil_form.py
"""

from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from zeros import load_zeros


def window(x: np.ndarray, sigma: float) -> np.ndarray:
    """Fixed frequency window phi-hat: a Gaussian bump of width sigma (mean zero spacing units)."""
    return np.exp(-0.5 * (x / sigma) ** 2)


def build_gram(gammas: np.ndarray, taus: np.ndarray, sigma: float) -> np.ndarray:
    """Finite compression G_{kl} = sum_j window(gamma_j - tau_k) window(gamma_j - tau_l)."""
    A = window(gammas[None, :] - taus[:, None], sigma)  # (d, J)
    return A @ A.T


def moments(G: np.ndarray) -> dict:
    """Trace, squared Frobenius norm, ratio C = (tr G)^2 / tr G^2, and the min eigenvalue."""
    tr = float(np.trace(G))
    tr2 = float(np.sum(G * G))  # tr G^2 = ||G||_F^2 for symmetric G
    w = np.linalg.eigvalsh((G + G.T) / 2)
    return {"tr": tr, "tr2": tr2, "C": tr * tr / tr2, "min_eig": float(w.min())}


def F(lam: float) -> float:
    """Montgomery's Cauchy-Schwarz form factor lambda / (1 + lambda^2 / 3); F(1) = 3/4."""
    return lam / (1 + lam**2 / 3)


def second_moment_constant(lam: float) -> float:
    """Closed form of tr G^2 / N in the proof's units: 1/lambda + lambda/3."""
    return 1 / lam + lam / 3


def run(n_zeros: int = 400, lam: float = 1.0) -> dict:
    """Build G from real zeros over a height window and report the two moments against theory."""
    gammas = load_zeros(n_zeros)
    lo, hi = gammas[n_zeros // 6], gammas[-n_zeros // 6]  # interior window, avoid edge effects
    inwin = gammas[(gammas >= lo) & (gammas <= hi)]
    mean_gap = np.mean(np.diff(inwin))
    spacing = mean_gap / lam  # critical sampling density scaled by bandwidth
    taus = np.arange(lo, hi, spacing)
    sigma = mean_gap  # window width ~ one mean spacing
    G = build_gram(gammas, taus, sigma)
    m = moments(G)
    N = len(inwin)
    return {
        "lam": lam,
        "N": N,
        "d": len(taus),
        "gram_ratio": m["C"] / N,
        "F": F(lam),
        "mm_const": second_moment_constant(lam),
        "min_eig": m["min_eig"],
        "tr": m["tr"],
        "tr2_ratio": m["tr2"] / m["tr"],
    }


def main() -> None:
    res = [run(n_zeros=500, lam=lam) for lam in (0.7, 0.85, 1.0)]
    print("\n=== MATH CHECK: finite Weil form from real zeros ===")
    print(f"  {'lambda':>7} {'N':>5} {'d':>5} {'min_eig':>10} {'gram C/N':>9}   closed forms")
    for r in res:
        cf = f"F={r['F']:.3f}, 1/l+l/3={r['mm_const']:.3f}"
        print(f"  {r['lam']:>7.2f} {r['N']:>5d} {r['d']:>5d} {r['min_eig']:>10.2e} {r['gram_ratio']:>9.3f}   {cf}")
    print("  ---")
    print("  min_eig >= 0 at every lambda: on-line zeros give G >= 0. RH is verified at these")
    print("  heights, so the certificate certifies nothing NEW; G >= 0 is the exact check here.")
    print("  'gram C/N' is a plain-window statistic, NOT a fit of F(lambda); the exact Montgomery")
    print("  constant lives in the closed forms (and the distribution check in pair_correlation.py).")
    print("=" * 52)
    for r in res:
        assert r["min_eig"] > -1e-6, "on-line zeros must give G >= 0"
    assert abs(second_moment_constant(1.0) - 4 / 3) < 1e-12, "1/1 + 1/3 = 4/3"
    assert abs(F(1.0) - 0.75) < 1e-12, "F(1) = 3/4"


if __name__ == "__main__":
    main()
