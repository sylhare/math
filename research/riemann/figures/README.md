# Riemann figure experiments: framework + catalog

Each mathematically-valid figure is **one self-contained file**. A file computes its data from the
formulas in `../riemann.md` (and the zero ordinates in `_shared.py`), validates numerically, and
renders a preview PNG (statics) or GIF (animations). Same contract as the Kakeya figures: get the
*form* right and *proven against the math* here first.

Coverage goal: **every formula and every named result** in `../riemann.md` gets its own figure.

## Layout: grouped by the article structure, ordered by name

Figures live in one subfolder per part of `../riemann.md`, and each file is prefixed `P_N_` so
sorting by name gives the reading order:

```
1_primes_and_zeta/     2_zeros_critical_line/   3_why_it_matters/      4_proportion_ladder/
5_two_methods/         6_weil_form_argument/    7_numerical_framework/ 8_pushing_further/
```

`_shared.py` (helpers + zero table), `README.md`, and `reference/` (third-party images, do not ship)
stay at the root.

## How to run

Scripts import `_shared` from the figures root, so put that root on `PYTHONPATH`:

```
PYTHONPATH=research/riemann/figures \
  uv run --with matplotlib --with mpmath python research/riemann/figures/<part>/<name>.py
```

Statics output `<name>.png`; animations output `<name>_anim.gif` via `_shared.save_gif`. Every run
prints a `MATH CHECK` block. Regenerate all (or some) with the driver, which sets `PYTHONPATH`:

```
bash research/riemann/figures/regenerate.sh                     # all figures
bash research/riemann/figures/regenerate.sh <part>/<name>.py    # only the given script(s)
```

## Rules (so figures can be owned independently without colliding)

1. **One figure = one file** named `P_N_topic`. Its only output is `P_N_topic.png` / `_anim.gif`.
2. **Reuse `_shared.py`** for the zero table (`ZETA_ZEROS`, `zeta_zeros`), arithmetic
   (`primes_up_to`, `von_mangoldt`, `psi`), palette (`COLORS`), preview (`plot_axes`,
   `save_preview`), reporting (`math_check`), and GIFs (`save_gif`). **Do not edit `_shared.py` or
   another figure file**; if you need a new helper, define it locally.
3. **Math is pure numpy / mpmath**; matplotlib only for preview.
4. **Every file ends by printing a `MATH CHECK`** whose numbers reproduce `../riemann.md`; animations
   also **assert the animated invariant** (needle length has no analogue here: assert e.g. moment
   ratios, `Z(t)` sign changes, or the certificate inequality).
5. **Two validations per figure**: *math* (numbers match the research) and *look* (the plot reads
   clearly; add an `ALTERNATIVES:` note if a truer object cannot be drawn).
6. **Honesty over drama**: the numerical certificates certify nothing new at small height (RH is
   verified there); say so. Render the finite identity, print the real readout.
7. **Fully visible**: set axis limits from the whole final data with padding.
8. Deletions: dev-mcp `safe_remove` (recoverable), never `rm`.

Colour logic (mirror the article): primes / arithmetic side `COLORS["prime"]` (blue); zeros / the
critical line `zero` (red) and `line` (black); hypothetical off-line zeros `offline` (orange);
on-line positive contribution `onlinepos` (green); strips/bands faint `region`; axes/arrows `guide`.

---

## Catalog

Static `[S]` and animation `[A]` per concept. Each: math (formula) | validation.

### 1_primes_and_zeta

- `1_1_prime_counting` [S] - staircase `pi(x)` vs `x/log x` vs `Li(x)=int_2^x dt/log t`; the wobble
  is the error `E(x)`. | primes by sieve; Li by quadrature.
- `1_2_euler_product` [S] - `zeta(s)=sum n^-s = prod_p (1-p^-s)^-1`; partial products over the first
  primes converging to `zeta` on the real axis `s in (1, 4]`. | partial sums vs partial products.

### 2_zeros_critical_line

- `2_1_critical_strip` [S] - complex plane: trivial zeros `-2,-4,...`, pole at `1`, first 10
  nontrivial zeros on `Re s = 1/2` at `gamma_k`; strip `0<Re s<1` shaded. | ZETA_ZEROS.
- `2_2_zeta_on_line_anim` [A] - Hardy `Z(t)`, `|Z(t)|=|zeta(1/2+it)|`, scanned up `t`; sign changes
  = on-line zeros; assert a sign change straddles each `gamma_k`. | mpmath `siegelz` or `zeta`.
- `2_3_functional_equation` [S] - the quadruple `{rho, 1-bar rho, bar rho, 1-rho}`; on the line it
  collapses to `1/2 +- i gamma`. The `rho<->1-bar rho` pairing used in Part 6. | reflection algebra.

### 3_why_it_matters

- `3_1_explicit_formula_anim` [A] - rebuild `psi(x)` from `psi(x)=x - sum_rho x^rho/rho - ...`,
  adding zero pairs one at a time; assert partial sum -> psi at prime powers. | `von_mangoldt`, zeros.
- `3_2_pnt_error` [S] - `psi(x)-x` inside the envelope `+-x^Theta`; RH gives `Theta=1/2`; a single
  off-line zero at `beta>1/2` widens the band to `x^beta`. | psi vs x; band curves.

### 4_proportion_ladder

- `4_1_proportion_ladder` [S] - bars `1/3 (1974)`, `2/5 (1989)`, `5/12=0.4166 (2020)`, `2/3`,
  `0.6725 (2026)` against `100%` (RH). | the six constants.

### 5_two_methods

- `5_1_mollifier_vs_paircorrelation` [S] - two panels: Levinson (mollify `zeta*M`, count sign
  changes) vs Montgomery (gap statistics). Schematic. | conceptual.
- `5_2_pair_correlation_anim` [A] - histogram of normalised gaps of real zeros building up to
  Montgomery's `1-(sin pi u/pi u)^2`; assert histogram -> curve in L1. | needs many zeros (mpmath).

### 6_weil_form_argument

- `6_1_weil_form_signature_anim` [A] - `G=P+Q`: on-line points add positive rank-1 blocks, off-line
  pairs add signature `(1,1)`; track `n_+(G)` vs `s+p`. Synthetic small matrices. | eig signs.
- `6_2_H_lambda_curve` [S] - `H(lambda)=2-1/lambda-lambda/3`, the optimal-window `H_opt=2-1/c*_lambda`,
  `H_d`, `F(lambda)=lambda/(1+lambda^2/3)`; mark `H(1)=2/3` and the method ceiling `0.6725` (optimal
  window, no window beats it). | closed forms.

### 7_numerical_framework

- `7_1_moments_convergence` [S] - `tr G/N -> 1` and `C=(tr G)^2/tr G^2` approaching `F(lambda)` from
  real-zero-built forms at several heights; reproduce Table (2) `C/N ~ 0.757-0.766` at `lambda=1`. |
  framework/build_form.
- `7_2_synthetic_certificate_anim` [A] - replace on-line zeros by off-line pairs of growing depth;
  certificate `2C-N'` falls below 0, never exceeds true `s_1`; assert `n_+ <= s+p` each frame. |
  synthetic configs.

### 8_pushing_further

- `8_1_bandwidth_ceiling` [S] - optimal-window `H_opt(lambda)` vs bandwidth; shade unconditional
  `lambda<=1` (ceiling `0.6725`), dashed conditional `lambda>1` with `0.70/0.80 -> lambda~1.04/1.27`
  and `0.90` above the reach of this single-window family. | c*_lambda + the targets.
- `8_2_moment_ladder` [S] - the discrete rungs `5/12 -> 2/3 -> 0.6725` (unconditional) `-> 13/18 -> 1`
  (conditional, Hardy-Littlewood), with the Davenport-Heilbronn identifiability limit at RH. | closed
  forms + fractions.
