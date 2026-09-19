# Framework: rebuilding the 2/3 argument, executably

A runnable reconstruction of the finite linear algebra behind Part 6 of `../riemann.md`. It does
**not** reprove the analytic inputs (Montgomery's unconditional prime side, the explicit formula);
those are cited theorems. It makes the *combinatorial core* executable and self-checking, and it
demonstrates the pieces that can be checked directly against real zeros.

What is proved here vs. assumed:

| piece | status in this framework |
| --- | --- |
| rank-trace inequality (Lemma 3.2) | **verified** on 20000 random + adversarial Hermitian instances |
| Sylvester positive-index bound `n_+ <= s + p` | **verified** on random instances and synthetic configs |
| `G >= 0` from on-line zeros | **verified** on the real zeros (RH holds at these heights) |
| Montgomery pair correlation `1 - (sin pi u/pi u)^2` | **reproduced** from 1200 real zeros (repulsion) |
| `H(lambda) = 2 - 1/lambda - lambda/3`, `H(1) = 2/3` | reproduced from the two moments (closed form) |
| unconditional prime side `tr G^2 = (1/lambda+lambda/3)N` | **cited** (BGSTB24); closed form only here |
| the equivalence `W >= 0 <=> RH` | **cited** (Weil, Bombieri, Yoshida) |

## Files

- `linear_algebra.py` - the core that replaces RH: the rank-trace inequality and Sylvester's law,
  verified numerically. This is the one non-classical step, and it is ordinary linear algebra.
- `zeros.py` - cached loader for the zero ordinates (`zeros_cache.npy`), via mpmath.
- `weil_form.py` - builds the finite compression `G` from real zeros; shows `G >= 0` and reports the
  two finite moments. Honest: it does not fit `F(lambda)` from a plain window.
- `pair_correlation.py` - Montgomery's pair correlation from real zeros; the repulsion dip at `u=0`.
- `certificate.py` - the Part-6c assembly: the two moments + block structure give `H(lambda)`, and a
  synthetic stress test confirming the certificate never exceeds the truth.
- `push_further.py` - Part 8: the functional `c_lambda(v)` and its free-form optimum
  (Montgomery-Taylor, `0.6725`, a maximum of the functional at bandwidth one), the two-moment
  Christoffel cap (`3/4`), the conditional moment ladder (`13/18` from the 4th moment), the bandwidth
  table (`0.90` above the single-window curve's ceiling), and the Davenport-Heilbronn identifiability
  limit. The earlier `0.68185` back-solves above the functional's maximum, so it does not fit here.
- `run_all.py` - runs all of the above; every sub-module asserts its own invariants.

## Run

```
uv run --with numpy --with mpmath python research/riemann/framework/run_all.py
```

First run computes and caches ~1200 zeros (a few minutes via mpmath); later runs are fast. To only
(re)build the cache:

```
uv run --with numpy --with mpmath python research/riemann/framework/zeros.py 1200
```

## Honesty note (same as the paper's Section 8)

At the heights reachable here (`gamma <~ 1000`) the Riemann hypothesis is verified, so `G` is
genuinely positive semidefinite and these certificates certify nothing *new*. The point is that the
finite identities the proof rests on, the two moments, the signature accounting, and the rank-trace
inequality, come out correctly on real data and on adversarial synthetic configurations. The jump
from `5/12` to `2/3` is the asymptotic (`T -> infinity`) statement of Theorems A-D, which no finite
computation can witness.
