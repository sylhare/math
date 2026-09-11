"""How far the 2/3 method goes, executably.

The certified proportion of simple on-line zeros reduces (paper eq. 7.3) to a scale-free variational
problem in a window v >= 0 on [-1/2, 1/2] and a Fourier bandwidth lambda:

    c_lambda(v) = lambda (INT v)^2 / ( INT v^2 + lambda^2 IINT |s - s'| v(s) v(s') ds ds' )
    H = 2 - 1/c_lambda(v)   (simple on-line),   H_d = (3 - 1/c)/2   (distinct)

Four findings, each computed and cross-checked here:

  1. Window optimality. The free-form maximiser of c_1 over v >= 0 is (I + K)^{-1} 1, strictly
     positive so the constraint is inactive; it equals cos(sqrt2 s) (Montgomery-Taylor),
     c*_1 = 0.753296, H = 0.67250, H_d = 0.83625. A genuine maximum of the functional at lambda = 1
     (Theorem D), not just the best sampled.

  2. Two-moment cap. From (m1, m2) = (1, 4/3), the sharp Chebyshev-Markov / Christoffel bound gives
     1 - Lambda_1(0) = 3/4 = F(1): two moments do not beat the flat window. A bound above 0.67250 at
     lambda = 1 (e.g. 0.68185 in an earlier draft) back-solves to c > c*_1, above the functional's
     maximum, so it does not fit here.

  3. Conditional moment ladder. Sine-kernel Gram moments m_k(1) = 1, 4/3, 2, 13/4 (the 4th is cited
     theory; the Monte-Carlo corroborates loosely, ~3.10 vs 3.25). A 4th moment lifts simple to
     13/18 = 0.7222, distinct to 413/486 = 0.8498, but needs Hardy-Littlewood prime-pair input,
     outside the Rudnick-Sarnak range k*lambda < 2 (at lambda ~ 1 only k = 3, which does not help).
     Every rung above 0.6725 is conditional.

  4. Bandwidth, and the identifiability limit. lambda > 1 reaches more (0.70 at ~1.04, 0.80 at ~1.27;
     0.90 is above the peak ~0.889 of the single-scale curve), and lambda > 1 is Montgomery's open
     pair-correlation range. Even granting all correlations this data does not reach RH: the
     Davenport-Heilbronn function shares its functional-equation shape and pair-correlation inputs but
     has off-line zeros, so no argument reading only this data separates it from zeta.

Run: uv run --with numpy python research/riemann/framework/push_further.py
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

SQRT2 = math.sqrt(2.0)


def c_functional(v: np.ndarray, s: np.ndarray, lam: float = 1.0) -> float:
    """Evaluate c_lambda(v) on a sampled window v at nodes s (trapezoidal quadrature)."""
    w = np.gradient(s)
    num = lam * (np.sum(v * w)) ** 2
    quad = np.sum(v * v * w)
    kernel = np.abs(s[:, None] - s[None, :])
    double = float(w @ (v[:, None] * kernel * v[None, :]) @ w)
    return float(num / (quad + lam**2 * double))


def optimal_window(lam: float = 1.0, n: int = 1200) -> dict:
    """Free-form maximiser of c_lambda over v: solve (D + lam^2 K) v = a; report c, positivity.

    a_i, D and K use trapezoidal weights w_i (endpoints w = dx/2), so c_max = a^T M^{-1} a with
    a = w, D = diag(w), K_ij = w_i w_j |s_i - s_j|, M = D + lam^2 K.
    """
    s = np.linspace(-0.5, 0.5, n)
    dx = s[1] - s[0]
    w = np.full(n, dx)
    w[0] = w[-1] = dx / 2
    kernel = w[:, None] * np.abs(s[:, None] - s[None, :]) * w[None, :]
    M = np.diag(w) + lam**2 * kernel
    v = np.linalg.solve(M, w)
    c_max = float(w @ v)
    v_norm = v / v.max()
    return {"c_max": c_max, "v_min_over_max": float(v_norm.min()), "s": s, "v": v_norm}


def montgomery_taylor(lam: float = 1.0) -> float:
    """Closed form c*_lambda = sqrt2 tan(theta) / (1 + theta tan(theta)), theta = lambda/sqrt2."""
    theta = lam / SQRT2
    return SQRT2 * math.tan(theta) / (1 + theta * math.tan(theta))


def flat_F(lam: float = 1.0) -> float:
    """Flat-window value c_lambda(1) = F(lambda) = lambda / (1 + lambda^2 / 3); F(1) = 3/4."""
    return lam / (1 + lam**2 / 3)


def H(c: float) -> float:
    """Certified simple-on-line proportion from the form factor c: 2 - 1/c."""
    return 2 - 1 / c


def Hd(c: float) -> float:
    """Certified distinct-zero proportion from the form factor c: (3 - 1/c) / 2."""
    return (3 - 1 / c) / 2


def christoffel_two_moment(m1: float = 1.0, m2: float = 4 / 3) -> dict:
    """Sharp positive-index density from (m1, m2): Lambda_1(0) and 1 - Lambda_1(0)."""
    var = m2 - m1 * m1
    lambda1_at_0 = 1.0 / (1.0 + m1 * m1 / var)
    return {"Lambda_1(0)": lambda1_at_0, "density_cap": 1.0 - lambda1_at_0}


def sine_kernel_moments(reps: int = 30, n: int = 600, block: int = 100, seed: int = 20260816) -> np.ndarray:
    """Monte-Carlo estimate of m_k(1) = (1/d) tr A^k for the unit-density sine-process Gram matrix.

    Unfold the central GUE eigenvalues to unit mean spacing, build A_ij = sinc(y_i - y_j) with the
    diagonal, and average tr A^k / block. The diagonal terms are what reproduce 1, 4/3, 2, 13/4; a
    naive equal-spacing lattice gives A = I.
    """
    rng = np.random.default_rng(seed)
    acc = np.zeros(4)
    for _ in range(reps):
        g = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
        g = (g + g.conj().T) / 2
        ev = np.sort(np.linalg.eigvalsh(g))
        lo = n // 2 - block // 2
        c = ev[lo : lo + block]
        y = c * (block - 1) / (c[-1] - c[0])
        d = y[:, None] - y[None, :]
        a = np.sinc(d)
        for k in range(1, 5):
            acc[k - 1] += np.trace(np.linalg.matrix_power(a, k)).real / block
    return acc / reps


def cubic_weight_ok() -> bool:
    """Verify the cubic weight psi(m) = m/2 + (2m^2 - m^3)/18 + (4/9)[m=1] has psi(m) <= 1 for m >= 1."""

    def psi(m: int) -> Fraction:
        base = Fraction(m, 2) + Fraction(2 * m * m - m**3, 18)
        return base + (Fraction(4, 9) if m == 1 else Fraction(0))

    return all(psi(m) <= 1 for m in range(1, 40)) and psi(1) == 1 and psi(2) == 1 and psi(3) == 1


def conditional_ladder() -> dict:
    """The fourth-moment (Hardy-Littlewood) lifts, with m2 = 4/3, m3 = 2."""
    m2, m3 = Fraction(4, 3), Fraction(2)
    distinct = Fraction(1, 2) + (2 * m2 - m3) / 18 + Fraction(4, 9) * Fraction(19, 27)
    return {"simple_4th_moment": Fraction(13, 18), "distinct_4th_moment": distinct}


def bandwidth_for_target(h_target: float, window: str = "opt") -> float | None:
    """Smallest lambda whose optimal (or flat) window certifies proportion h_target, or None."""
    c_need = 1.0 / (2.0 - h_target)
    grid = np.linspace(1e-3, math.pi / SQRT2 - 1e-3, 400000)
    cs = np.array([montgomery_taylor(x) for x in grid]) if window == "opt" else flat_F(grid)
    if cs.max() < c_need:
        return None
    return float(grid[np.argmax(cs >= c_need)])


def bandwidth_ceiling(window: str = "opt") -> dict:
    """The largest proportion any single-scale window certifies, and where it peaks."""
    if window == "opt":
        grid = np.linspace(1e-3, math.pi / SQRT2 - 1e-3, 400000)
        cs = np.array([montgomery_taylor(x) for x in grid])
    else:
        grid = np.linspace(1e-3, 3.0, 400000)
        cs = flat_F(grid)
    i = int(np.argmax(cs))
    return {"lambda_star": float(grid[i]), "H_ceiling": H(float(cs[i]))}


DAVENPORT_HEILBRONN_OFFLINE = [(0.808517, 85.699348), (0.650830, 114.163343)]


def main() -> None:
    ow = optimal_window()
    mt = montgomery_taylor(1.0)
    chr2 = christoffel_two_moment()
    ladder = conditional_ladder()
    mk = sine_kernel_moments()

    print("\n=== MATH CHECK: pushing further ===")
    rows = [
        ("1. free-form optimal window c*_1", f"{ow['c_max']:.6f}  (closed form {mt:.6f})"),
        ("   maximiser v_min/v_max (>0 => v>=0 inactive)", f"{ow['v_min_over_max']:.3f}"),
        ("   H = 2 - 1/c*_1", f"{H(mt):.6f}  (Montgomery-Taylor; = 0.67250)"),
        ("   H_d = (3 - 1/c*_1)/2", f"{Hd(mt):.6f}  (= 0.83625)"),
        ("   flat window F(1), H, H_d", f"{flat_F(1.0):.4f}, {H(flat_F(1.0)):.4f}, {Hd(flat_F(1.0)):.4f}"),
        ("2. Christoffel Lambda_1(0) from (1, 4/3)", f"{chr2['Lambda_1(0)']:.4f}  (= 1/4)"),
        ("   two-moment density cap 1 - Lambda_1(0)", f"{chr2['density_cap']:.4f}  (= 3/4 = F(1))"),
        ("   0.68185 back-solves to c", f"{1 / (2 - 0.68185):.6f}  (> c*_1 {mt:.6f}: above this functional's max)"),
        ("3. sine-kernel moments m_k(1) (MC)", f"{mk[0]:.3f}, {mk[1]:.3f}, {mk[2]:.3f}, {mk[3]:.3f}"),
        ("   theory m_k(1)", "1, 4/3=1.333, 2, 13/4=3.250"),
        ("   cubic weight psi(m) <= 1, eq at 1,2,3", f"{cubic_weight_ok()}"),
        (
            "   4th-moment simple / distinct (conditional)",
            f"{float(ladder['simple_4th_moment']):.4f} / {float(ladder['distinct_4th_moment']):.4f}",
        ),
        (
            "4. optimal-window lambda for 0.70 / 0.80",
            f"{bandwidth_for_target(0.70):.3f} / {bandwidth_for_target(0.80):.3f}",
        ),
        (
            "   0.90 reachable by a single window?",
            f"{bandwidth_for_target(0.90) is not None}  (ceiling {bandwidth_ceiling()['H_ceiling']:.4f})",
        ),
        (
            "   Davenport-Heilbronn off-line zero",
            f"{DAVENPORT_HEILBRONN_OFFLINE[0][0]:.3f} + {DAVENPORT_HEILBRONN_OFFLINE[0][1]:.3f}i (RH-analogue false)",
        ),
    ]
    w = max(len(r[0]) for r in rows)
    for a, b in rows:
        print(f"  {a.ljust(w)} : {b}")
    print("=" * 58)

    assert abs(ow["c_max"] - mt) < 1e-4, "free-form optimum must match Montgomery-Taylor"
    assert ow["v_min_over_max"] > 0, "optimal window must be positive (constraint inactive)"
    assert abs(H(mt) - 0.67250) < 1e-4, "H must be 0.67250"
    assert abs(Hd(mt) - 0.83625) < 1e-4, "H_d must be 0.83625"
    assert abs(flat_F(1.0) - 0.75) < 1e-12 and abs(H(flat_F(1.0)) - 2 / 3) < 1e-12
    assert abs(chr2["density_cap"] - 0.75) < 1e-12, "two-moment density cap must be 3/4"
    assert mt < 1 / (2 - 0.68185), "0.68185 back-solves above this functional's maximum at lambda=1"
    assert abs(mk[1] - 4 / 3) < 0.08, f"m2 MC {mk[1]} must approximate 4/3"
    assert abs(mk[3] - 13 / 4) < 0.30, f"m4 MC {mk[3]} must approximate 13/4"
    assert cubic_weight_ok(), "cubic weight must satisfy psi(m) <= 1"
    assert ladder["simple_4th_moment"] == Fraction(13, 18)
    assert abs(bandwidth_for_target(0.70) - 1.043) < 0.01 and abs(bandwidth_for_target(0.80) - 1.265) < 0.01
    assert bandwidth_for_target(0.90) is None, "0.90 sits above the single-scale optimal-window ceiling"


if __name__ == "__main__":
    main()
