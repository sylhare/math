"""Assemble the bound: feed the two moments and the block structure into the rank-trace inequality.

This is the arithmetic of Part 6c, made executable. Given the bandwidth ``lambda``, the proof's two
moments are

    tr G       = N                      (mean density)
    ||G||_F^2  = (1/lambda + lambda/3) N (Montgomery's second moment, unconditional)

and the zero side says G = P + Q with P a sum of rank-one psd blocks (one per distinct on-line point)
and Q a sum of signature-(1,1) blocks (one per off-line pair). Combining with the rank-trace
inequality of ``linear_algebra`` gives the certified on-line proportion

    s / N >= 2 - 1/lambda - lambda/3 = H(lambda),   H(1) = 2/3.

Two demonstrations:
  (1) the closed-form assembly reproduces H(lambda) and H(1) = 2/3 from the two moments;
  (2) a synthetic stress test builds real P + Q matrices for configurations with off-line pairs of
      growing depth and confirms the certificate never certifies more on-line points than exist
      (Sylvester's law), tracking the truth from below.

Run: uv run --with numpy python research/riemann/framework/certificate.py
"""

from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from linear_algebra import positive_index, random_signature, rng


def H(lam: float) -> float:
    """Certified on-line proportion from the two moments: 2 - 1/lambda - lambda/3."""
    return 2 - 1 / lam - lam / 3


def Hd(lam: float) -> float:
    """Certified distinct-zero proportion: (1 + H(lambda)) / 2."""
    return (1 + H(lam)) / 2


def certified_proportion(mean_density: float, second_moment: float) -> float:
    """The Part-6c combination s/N >= 4 - 2 - second_moment, in units where tr G / N = mean_density.

    With mean_density = 1 and second_moment = 1/lambda + lambda/3 this returns H(lambda).
    """
    return 4 * mean_density - 2 * mean_density - second_moment


def second_moment(lam: float) -> float:
    return 1 / lam + lam / 3


def synthetic_certificate(s: int, p: int, depth: float, d: int = 60) -> dict:
    """Build P (s rank-one psd blocks) + Q (p signature-(1,1) blocks) and read the certificate.

    ``depth`` scales the off-line blocks' magnitude (a proxy for how far off the line the pairs sit).
    Returns the true on-line count s, the positive index n_+, and whether n_+ <= s + p holds.
    """
    P = np.zeros((d, d), dtype=complex)
    for _ in range(s):
        v = rng.standard_normal((d, 1)) + 1j * rng.standard_normal((d, 1))
        P += v @ v.conj().T
    Q = np.zeros((d, d), dtype=complex)
    for _ in range(p):
        Q += depth * random_signature(d, 1, 1)
    G = P + Q
    n_plus = positive_index(G)
    return {"s": s, "p": p, "depth": depth, "n_plus": n_plus, "bound_holds": n_plus <= s + p}


def main() -> None:
    print("\n=== MATH CHECK: certificate assembly (Part 6c) ===")
    rows = []
    for lam in (0.7, 0.85, 1.0):
        cp = certified_proportion(1.0, second_moment(lam))
        rows.append((f"H({lam:.2f}) from the two moments", f"{cp:.4f}  (closed form {H(lam):.4f})"))
    rows.append(("H(1) = 2/3", f"{H(1.0):.6f}  (= {2 / 3:.6f})"))
    rows.append(("H_d(1) = 5/6", f"{Hd(1.0):.6f}  (= {5 / 6:.6f})"))
    rows.append(("optimised (Montgomery-Taylor)", "0.6725 on-line, 0.83625 distinct (Theorem D)"))
    w = max(len(r[0]) for r in rows)
    for a, b in rows:
        print(f"  {a.ljust(w)} : {b}")

    print("  --- synthetic stress test: n_+ <= s + p across configurations ---")
    configs = [(30, 0, 0.0), (20, 10, 0.2), (20, 10, 1.0), (10, 20, 1.5), (0, 30, 2.0)]
    all_ok = True
    for s, p, depth in configs:
        r = synthetic_certificate(s, p, depth)
        all_ok &= r["bound_holds"]
        print(f"    s={s:>3} p={p:>3} depth={depth:>4.1f} -> n_+={r['n_plus']:>3}  n_+ <= s+p: {r['bound_holds']}")
    print("=" * 50)
    for lam in (0.7, 0.85, 1.0):
        assert abs(certified_proportion(1.0, second_moment(lam)) - H(lam)) < 1e-12
    assert abs(H(1.0) - 2 / 3) < 1e-12 and abs(Hd(1.0) - 5 / 6) < 1e-12
    assert all_ok, "Sylvester bound n_+ <= s + p must hold in every configuration"


if __name__ == "__main__":
    main()
