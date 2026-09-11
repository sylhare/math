# Lean 4 attempt at the 2/3 proportion result

`RiemannProportion.lean` states the 2026 result against Mathlib's `riemannZeta` and proves the parts
that are genuinely reproducible in Lean, honestly separating them from what is assumed. It is an
*attempt*, not the paper's full `Zeta23` formalisation.

## What compiles as real proofs (no `sorry`)

- `montgomery_m2_ge_2m_sub_1`, `montgomery_m2_ge_3m_sub_2` - Montgomery's integrality seeds
  (`m^2 >= 2m-1`, `3m <= m^2+2`), the arithmetic behind the `2/3` and `5/6` constants.
- `H_one : H 1 = 2/3`, `Hd_one : Hd 1 = 5/6`, `F_one : F 1 = 3/4`, and
  `certified_eq_H : 4 - 2 - (1/λ + λ/3) = H λ` - the closed-form certificate assembly of Part 6c.
- `trace_transpose_mul_self_nonneg : 0 <= (Aᵀ * A).trace` - the positive-semidefiniteness the zero
  side rests on (on-line case), as a genuine matrix proof.

## What is assumed (documented)

- `theoremA` / `theoremB` - the analytic main theorems, left as `sorry` (the paper's actual content).
- `rank_trace_inequality` - Lemma 3.2 in full generality, an `axiom` here (numerically verified to
  0 violations in `../framework/linear_algebra.py`; a Lean proof via von Neumann's trace inequality
  is future work).
- `weil_positivity_iff_RH` - the Weil / Bombieri / Yoshida equivalence `W >= 0 <=> RH`, an `axiom`.

At last check: exit 0, a single `sorry` warning (Theorem A), 3 real proofs, 2 documented axioms.

## Type-check

Uses the repository's pre-built Mathlib (v4.32.2) in the root `lean/` project, so nothing needs to be
rebuilt:

```
cd lean && lake env lean ../research/riemann/lean/RiemannProportion.lean
```

Expected output: exactly one line,
`RiemannProportion.lean:NN:8: warning: declaration uses 'sorry'` (Theorem A), and exit code 0.

To audit what the proofs depend on, add at the end of the file and re-run:

```
#print axioms RiemannProportion.montgomery_m2_ge_2m_sub_1
#print axioms RiemannProportion.trace_transpose_mul_self_nonneg
```

(the proved lemmas depend only on Lean's standard axioms; `theoremA` additionally reports `sorryAx`).
