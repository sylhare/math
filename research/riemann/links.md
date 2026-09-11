# Riemann: sources and links

## Primary result (2026)

- **Claude / Anthropic**, *"More than two thirds of the zeros of the Riemann zeta function lie on
  the critical line"* (10 Aug 2026). PDF:
  `https://www-cdn.anthropic.com/564f962e60643842f5fcb4a17c9dbc8f608f1c37.pdf`
- **Anthropic**, *"Learning more about Claude's mathematical capabilities"* (research post):
  `https://www.anthropic.com/research/riemann-zeta`
- Verified leaderboard for the unconditional record: `https://www.riemannzeta.fun/`
- Lean 4 formalisation `Zeta23`: Apache-licensed repository accompanying the paper (329 files;
  statements against Mathlib `riemannZeta`).

## Scientific sources (the mathematics)

- **B. Riemann**, *"Ueber die Anzahl der Primzahlen unter einer gegebenen Grosse"* (1859): the zeta
  function, the functional equation, and the hypothesis.
- **H. L. Montgomery**, *"The pair correlation of zeros of the zeta function"*, Proc. Sympos. Pure
  Math. 24 (1973), 181-193: the pair-correlation method and the form factor `F(alpha)`.
- **A. Weil** (1952), **E. Bombieri**, *"Remarks on Weil's quadratic functional..."*, Rend. Mat.
  Acc. Lincei 11 (2000), and **H. Yoshida** (1992): the Hermitian form whose positivity is the
  hypothesis, and whose negative index counts off-line zeros.
- **N. Levinson**, *"More than one third of zeros of Riemann's zeta-function are on sigma=1/2"*,
  Adv. Math. 13 (1974): the mollifier method (`1/3`). **D. R. Heath-Brown** (1979): simplicity.
- **J. B. Conrey**, *"More than two fifths of the zeros of the Riemann zeta function are on the
  critical line"*, J. Reine Angew. Math. 399 (1989): `2/5`.
- **H. M. Bui, J. B. Conrey, M. P. Young** (2011); **S. Feng** (2012); **K. Pratt, N. Robles,
  A. Zaharescu, D. Zeindler**, *"More than five-twelfths of the zeros..."* (2020): the record
  `5/12 = 0.4166...`, arXiv:1002.4127 lineage.
- **S. Baluyot, D. A. Goldston, A. I. Suriajaya, C. L. Turnage-Butterbaugh** (Acta Arithmetica,
  2024) and **D. A. Goldston, A. I. Suriajaya**, *"Zeta zeros on the critical line"* (2025-2026,
  arXiv:2511.20059): the unconditional pair-correlation second moment. See also **Aryan** (2022),
  arXiv:2501.14545 (pair correlation, proportions of simple and critical zeros).
- **A. M. Odlyzko**, tables of zeta zeros; **LMFDB** `https://www.lmfdb.org/zeros/zeta/`: the
  numerical zero ordinates used in the figures and framework.

## Popular explainers (the 2026 result)

- Anthropic research post (above); DataCamp, *"Claude Tried the Riemann Hypothesis. Here's What
  Happened."*; explainx.ai, *"Claude Riemann Result: 41.6% to 67.2%"*; XenoSpectrum, *"...Breaks
  Through the 41% Wall"*; kingy.ai, *"Claude's 67% Riemann-Zeta Result, Explained"*.
- **VibeMathed** / riemannzeta.fun: the open, machine-checked record and its baseline.

## Classical background

- **H. Davenport**, *Multiplicative Number Theory*: the explicit formula, `N(T)`, and the prime
  number theorem error term.
- **E. C. Titchmarsh** (rev. Heath-Brown), *The Theory of the Riemann Zeta-Function*: Hardy's
  `Z`-function, the functional equation, and critical-line results.
- **Wikipedia**, *Riemann hypothesis* `https://en.wikipedia.org/wiki/Riemann_hypothesis` (index for
  the classical statements; primary sources above).

## Reference images (`figures/reference/`)

None shipped: every figure here is generated from the formulas in `riemann.md` and the zero
ordinates in `figures/_shared.py`. If third-party plots are added later (e.g. LMFDB zero plots),
document them here with their source URL, as the Kakeya `reference/` folder does.
