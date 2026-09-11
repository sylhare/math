# Riemann: the zeros, the critical line, and two thirds of them

The line of reasoning from "how are the primes spread out?" to the August 2026 theorem that at
least two thirds of the zeros of the zeta function lie on the critical line, with the exact math and
a figure for every step:

1. the primes and the zeta function: the counting problem Riemann started from;
2. the nontrivial zeros, the functional equation, and the critical line (the Riemann hypothesis
   stated);
3. why the zeros matter: the explicit formula ties them to the primes, and their position controls
   the error in the prime number theorem;
4. measuring progress: the proportion `N_0(T)/N(T)` on the line, and the ladder Selberg -> Levinson
   -> Conrey -> Pratt-Robles-Zaharescu-Zeindler -> 2026;
5. the two methods: Levinson's mollifier and Montgomery's pair correlation;
6. the 2026 argument: Weil's explicit formula as a Hermitian form, its positivity is the hypothesis,
   and a finite piece of it certifies `2/3` (optimised `0.6725`) by linear algebra alone;
7. a numerical framework that rebuilds the finite form from real zeros and reproduces the bound;
8. what it would take to push past `2/3`, and the ceiling of this method;
9. how the result was found, formalised, and what it is not.

Figures referenced below live in `figures/<part>/`; each is a numpy construction validated against
the formula it illustrates. A runnable reconstruction of the argument's finite linear algebra lives
in `framework/`, and a Lean 4 attempt at the statements and the linear-algebra core in `lean/`.

---

## Sources (scientific articles cited for the mathematics)

Every theorem, constant, and formula below is sourced from the literature; see `links.md` for URLs.

- **Claude (Anthropic)**, *"More than two thirds of the zeros of the Riemann zeta function lie on
  the critical line"* (10 August 2026). The primary result and its proof: Theorems A (at least
  `2/3` of zeros on the line), B (`2/3` simple and on the line), C (`5/6` distinct), D (optimised
  constants `0.6725`, `0.6725`, `0.83625`), E (Dirichlet `L`-functions). The argument, its Lean 4
  formalisation (`Zeta23`), and the account of its discovery are in this paper.
- **H. Montgomery**, *"The pair correlation of zeros of the zeta function"*, Proc. Sympos. Pure
  Math. 24 (1973): the pair-correlation method, the form factor `F(alpha)`, and the conditional
  `2/3` for simple zeros. **Montgomery-Taylor** (1975) and **Cheer-Goldston** (1993): the optimised
  `0.6725`, `0.6727` under the hypothesis.
- **S. Baluyot, D. Goldston, A. I. Suriajaya, C. Turnage-Butterbaugh** (2024, Acta Arithmetica),
  and **Goldston-Suriajaya** (2025-2026): the pair-correlation second moment made unconditional
  (Montgomery's prime side holds for the sum over *all* zeros), and the isolation of the exact
  obstacle (off-line termwise positivity) that the 2026 paper removes. See also **Aryan** (2022).
- **E. Bombieri**, *"Remarks on Weil's quadratic functional in the theory of prime numbers"*,
  Rend. Mat. Acc. Lincei (2000): the Hermitian form on test functions whose positivity is
  equivalent to the hypothesis, and that its *negative* index counts off-line zeros. With
  **A. Weil** (1952) and **H. Yoshida** (1992).
- **N. Levinson**, *"More than one third of zeros of Riemann's zeta-function are on `sigma = 1/2`"*,
  Adv. Math. 13 (1974): the mollifier method and the constant `1/3`. **Heath-Brown** (1979): those
  zeros are simple. **J. B. Conrey** (1989): `> 2/5`. **Bui-Conrey-Young** (2011), **Feng** (2012),
  **Pratt-Robles-Zaharescu-Zeindler** (2020): the record `> 5/12 = 0.4166...`, held since 2020.
- **A. Selberg** (1942): a positive proportion lie on the line. **G. H. Hardy** (1914): infinitely
  many do. The **Riemann-von Mangoldt** formula for `N(T)`, and **Riemann**'s 1859 memoir.

Key primary result to cite: **Claude / Anthropic (10 Aug 2026)** proved unconditionally that
`liminf N_0(T)/N(T) >= 2/3`, and `>= 0.6725` with an optimised test family, improving the record
`5/12 = 0.4166...` of Pratt-Robles-Zaharescu-Zeindler (2020). This is **not** a proof of the
Riemann hypothesis (Part 9).

---

## 1. The primes and the zeta function

The primes `2, 3, 5, 7, 11, ...` thin out as you go, but not smoothly. Write `pi(x)` for the number
of primes up to `x`. Gauss and Legendre guessed, and Hadamard and de la Vallee Poussin proved in
1896 (the **prime number theorem**), that

$$
\begin{aligned}
\pi(x) &\sim \frac{x}{\log x}                 && \text{the density of primes near } x \text{ is about } 1/\log x \\
\pi(x) &= \operatorname{Li}(x) + E(x),        && \operatorname{Li}(x) = \int_2^x \frac{dt}{\log t} \text{ is the sharper guess} \\
E(x)   &= \text{the error we want to control.}
\end{aligned}
$$

The whole subject is about the size of that error `E(x)`. Riemann's 1859 idea was to study the
primes through a single analytic object. For `Re s > 1` define the **zeta function**

$$
\begin{aligned}
\zeta(s) &= \sum_{n=1}^{\infty} n^{-s}          && \text{a Dirichlet series, convergent for } \operatorname{Re} s > 1 \\
         &= \prod_{p \text{ prime}} \frac{1}{1 - p^{-s}} && \text{Euler's product: unique factorisation, rewritten.}
\end{aligned}
$$

The Euler product is where the primes enter: it is an analytic encoding of "every integer factors
into primes in one way". Taking a logarithmic derivative turns the product over primes into a sum
over prime powers, which is exactly the bridge used in Part 3.

![The prime-counting staircase pi(x) rising by 1 at each prime, against x/log x and the closer Li(x).](figures/1_primes_and_zeta/1_1_prime_counting.png)

*The staircase `pi(x)` counts primes; `x/log x` (prime number theorem) and the sharper
`Li(x)` track it. Every wobble of the staircase away from `Li(x)` is the error `E(x)` of Part 3,
and the zeros of `zeta` are exactly what governs it.*

![Partial Euler products over the first primes converging to zeta on the real axis.](figures/1_primes_and_zeta/1_2_euler_product.png)

*Truncating Euler's product at the first few primes already approximates `zeta(s)`; the product form
is the reason a statement about `zeta` is a statement about primes.*

---

## 2. The zeros, the functional equation, and the critical line

The series `sum n^{-s}` only converges for `Re s > 1`, but `zeta` extends to a single analytic
function on the whole plane (one pole, at `s = 1`). The continuation satisfies a reflection, the
**functional equation**, which in its symmetric form reads

$$
\begin{aligned}
\xi(s) &:= \tfrac{1}{2}s(s-1)\,\pi^{-s/2}\,\Gamma\!\left(\tfrac{s}{2}\right)\zeta(s) && \text{the completed zeta function, entire} \\
\xi(s) &= \xi(1 - s)                     && \text{symmetry across the line } \operatorname{Re} s = \tfrac{1}{2}.
\end{aligned}
$$

The Gamma factor forces `zeta` to vanish at `s = -2, -4, -6, \dots`: these are the **trivial zeros**,
and they are understood. Everything else lives in the **critical strip** `0 < Re s < 1`, and the
functional equation makes that strip symmetric: if `rho` is a zero, so are `1 - rho`, `bar{rho}`, and
`1 - bar{rho}`. The zeros therefore come in the quadruple `{rho, 1 - bar{rho}}` and its conjugate,
unless they sit on the axis of symmetry, the line `Re s = 1/2`, the **critical line**, where the
quadruple collapses to a conjugate pair.

Riemann computed the first few and observed they all lay on that line. His memoir called it "sehr
wahrscheinlich" (very probable) that they all do.

> **The Riemann hypothesis.** Every nontrivial zero `rho = beta + i gamma` of `zeta(s)` has
> `beta = 1/2`.

![The critical strip in the complex plane: trivial zeros on the negative axis, the pole at s=1, and the first nontrivial zeros stacked on the critical line Re s = 1/2.](figures/2_zeros_critical_line/2_1_critical_strip.png)

*Trivial zeros at `s = -2, -4, \dots`; the pole at `s = 1`; the nontrivial zeros (first ten shown)
on the line `Re s = 1/2` at heights `gamma_1 = 14.13, gamma_2 = 21.02, \dots`. The hypothesis is the
claim that this last column never leans off the line.*

The honest way to *see* the zeros on the line is Hardy's `Z`-function, a real function of a real
variable `t` with `|Z(t)| = |zeta(1/2 + it)|`, so that a zero on the line is an ordinary sign change
of `Z`.

![Hardy Z(t) along the critical line, its sign changes marking zeros on the line.](figures/2_zeros_critical_line/2_2_zeta_on_line_anim.gif)

*Scanning up the critical line: each sign change of `Z(t)` is a zero with `beta = 1/2`. Hardy (1914)
proved there are infinitely many such crossings; the hypothesis is that there are no *other* zeros
anywhere in the strip.*

![The functional-equation symmetry: a zero and its reflected partners across the line and the real axis.](figures/2_zeros_critical_line/2_3_functional_equation.png)

*A hypothetical off-line zero `rho` drags three partners with it: `1 - bar{rho}` (across the line),
`bar{rho}` (across the axis), `1 - rho`. On the critical line the four collapse to the conjugate
pair `1/2 \pm i gamma`. This `rho <-> 1 - bar{rho}` pairing is the whole hinge of Part 6.*

---

## 3. Why the zeros matter: the explicit formula

The reason the zeros are not a curiosity is that they *are* the primes, transformed. Von Mangoldt's
**explicit formula** makes the dictionary exact. Write the prime-power counting function

$$
\begin{aligned}
\psi(x) &= \sum_{p^m \le x} \log p = \sum_{n \le x} \Lambda(n) && \Lambda(n) = \log p \text{ if } n = p^m,\ 0 \text{ otherwise} \\
\psi(x) &= x - \sum_{\rho} \frac{x^{\rho}}{\rho} - \log(2\pi) - \tfrac{1}{2}\log\!\left(1 - x^{-2}\right) && \text{sum over all nontrivial zeros } \rho.
\end{aligned}
$$

Read it slowly. The main term `x` is the prime number theorem. The correction is a sum over the
zeros: each zero `rho = beta + i gamma` contributes an oscillation `x^{rho}/rho` whose *size* is
`x^{beta}` and whose *frequency* (in `log x`) is `gamma`. The zeros are the harmonics of the primes.

![Rebuilding the prime-power staircase psi(x) by adding the wave from each pair of zeros.](figures/3_why_it_matters/3_1_explicit_formula_anim.gif)

*Start from the straight line `x`. Add the oscillation from the first zero pair, then the second,
then more: the sum sharpens into the actual jumps of `psi(x)` at prime powers. Primes and zeros are
two views of the same object, exchanged by the explicit formula.*

This is also why the *position* of the zeros is the entire game. The size of a zero's contribution
is `x^{beta}`. Collecting the sum:

$$
\begin{aligned}
\psi(x) - x &= -\sum_{\rho} \frac{x^{\rho}}{\rho} + O(1)          && \text{the error term is the zero sum} \\
|\psi(x) - x| &\ll x^{\Theta}\log^2 x,                            && \Theta = \sup_{\rho}\operatorname{Re}\rho \text{ the rightmost zero} \\
\text{RH} &\iff \Theta = \tfrac{1}{2} \iff |\psi(x) - x| \ll x^{1/2}\log^2 x. && \text{smallest possible error.}
\end{aligned}
$$

So the Riemann hypothesis is exactly the statement that the primes are as evenly distributed as they
possibly could be: every zero off the line by `beta - 1/2` would inflate the prime error term by a
factor `x^{beta - 1/2}`. This is why "how far right does a zero sit?" is the question, and why a
theorem that pins *most* zeros to the line is real progress on the primes.

![The rightmost zero controls the prime error band: RH gives the narrowest possible envelope.](figures/3_why_it_matters/3_2_pnt_error.png)

*The error `psi(x) - x` sits inside an envelope `x^{Theta}`. On the hypothesis `Theta = 1/2`; a
single zero at `beta > 1/2` would widen the band to `x^{beta}`. Bounding the *proportion* of zeros
on the line is a first grip on this envelope.*

---

## 4. Measuring progress: the proportion on the line

Since the hypothesis is out of reach, the field measures partial progress. Count zeros by height:

$$
\begin{aligned}
N(T)   &= \#\{\rho = \beta + i\gamma : 0 < \gamma \le T\}          && \text{all nontrivial zeros up to height } T \\
N(T)   &= \frac{T}{2\pi}\log\frac{T}{2\pi} - \frac{T}{2\pi} + O(\log T) && \text{Riemann-von Mangoldt: the count is known exactly} \\
N_0(T) &= \#\{\rho : 0 < \gamma \le T,\ \beta = \tfrac{1}{2}\}     && \text{those on the critical line.}
\end{aligned}
$$

The Riemann hypothesis is `N_0(T) = N(T)` for all `T`. Short of that, one proves a **positive
proportion**:

$$
\kappa = \liminf_{T \to \infty} \frac{N_0(T)}{N(T)} \qquad \text{the guaranteed fraction on the line.}
$$

The history of `kappa` is a ladder, and the 2026 result is its latest rung:

$$
\begin{aligned}
\text{Hardy (1914)} &: N_0(T) \to \infty              && \text{infinitely many on the line} \\
\text{Selberg (1942)} &: \kappa > 0                   && \text{a positive proportion} \\
\text{Levinson (1974)} &: \kappa > \tfrac{1}{3}       && \text{mollifier method} \\
\text{Conrey (1989)} &: \kappa > \tfrac{2}{5}         && \text{refined mollifier} \\
\text{PRZZ (2020)} &: \kappa > \tfrac{5}{12} = 0.4166\ldots && \text{the record, held since 2020} \\
\text{Claude (2026)} &: \kappa \ge \tfrac{2}{3},\ \text{opt. } 0.6725 && \text{pair correlation made unconditional.}
\end{aligned}
$$

The jump from `5/12` to `2/3` is the largest single step in this table, and it comes from a
different lineage than everything above Selberg. That is the subject of Parts 5 and 6.

![The proportion ladder: bars from Levinson 1/3 to the 2026 value 0.6725, against the 100% the hypothesis asserts.](figures/4_proportion_ladder/4_1_proportion_ladder.png)

*Each bar is the proven lower bound `kappa` at its date, against the full height (`100%`) the
hypothesis claims. The record stood at `5/12 = 41.66%` from 2020; the 2026 argument raises the
guarantee to `2/3`, and `0.6725` with an optimised test family. The remaining gap to `100%` is not
shown to be off the line: it is simply not yet certified (Part 9).*

---

## 5. Two methods: mollifier and pair correlation

Every rung from Levinson to PRZZ uses **Levinson's method**: multiply `zeta` by a **mollifier**, a
short Dirichlet polynomial `M(s)` tuned to damp `zeta` near the line, and count sign changes of the
smoothed real function. Refining the mollifier is what carried `1/3 -> 2/5 -> 5/12`. The method is
powerful and delicate, and after fifty years it had stalled at `0.4166`.

![Levinson's mollifier tames zeta near the line so its real part's sign changes can be counted.](figures/5_two_methods/5_1_mollifier_vs_paircorrelation.png)

*Left, Levinson: mollify `zeta` and count sign changes of the smoothed function on the line. Right,
Montgomery: study the statistics of the *gaps* between zero heights `gamma`. The 2026 result lives
entirely on the right.*

The other lineage starts with **Montgomery (1973)**. Instead of locating zeros one at a time, he
studied their pairwise statistics. Under the hypothesis he evaluated a second moment over pairs of
zero heights and read off, from the **form factor** `F(alpha)` supported in `|alpha| <= 1`,

$$
\begin{aligned}
\sum_{\rho} m_{\rho}^2 &\le \left(\tfrac{4}{3} + o(1)\right)N(T) && \text{sum over distinct zeros, multiplicity } m_{\rho} \\
\Longrightarrow \quad N_{\text{simple}}(T) &\ge \left(\tfrac{2}{3} - o(1)\right)N(T). && \text{at least } 2/3 \text{ of the zeros are simple.}
\end{aligned}
$$

The `2/3` comes from a one-line integer inequality on the multiplicities, `m^2 \ge 2m - 1`: a
multiple zero costs the second moment more than it pays the count. Montgomery and Taylor (1975)
optimised the test function to `0.6725`. Every one of these numbers was **conditional on the
hypothesis**, because the argument reads the "zero side" as a sum over *real* ordinates, which needs
the zeros to be on the line to begin with.

The pair-correlation statistics are, remarkably, already visible in the real zeros.

![Montgomery's pair-correlation curve 1 - (sin pi u / pi u)^2 against the histogram of normalised gaps of real zeta zeros.](figures/5_two_methods/5_2_pair_correlation_anim.gif)

*Normalise the gaps between consecutive zero heights to average `1` and histogram them: they avoid
clustering exactly as Montgomery's curve `1 - (\sin \pi u / \pi u)^2` predicts (the same law as
eigenvalue spacings of random Hermitian matrices). This repulsion is the raw material the second
moment measures.*

Between 2022 and 2026, **Baluyot-Goldston-Suriajaya-Turnage-Butterbaugh** and **Goldston-Suriajaya**
showed that Montgomery's *prime side*, the arithmetic half of the second moment, is a mean value of
a Dirichlet polynomial of length `<= T` and is therefore **unconditional**: it holds for the sum
over *all* zeros, on the line or not. They isolated the one remaining obstacle precisely, the
termwise positivity of the zero side that fails off the line, and asked what would follow if it
could be removed. Part 6 is the answer.

---

## 6. The 2026 argument: a finite piece of Weil's form

The argument does not use Levinson's method at all. It makes Montgomery's pair correlation
unconditional, and it does so by replacing the one place the hypothesis was used, the positivity of
the zero side, with linear algebra.

### 6a. Weil's explicit formula as a Hermitian form

Weil's explicit formula says that for a test function `f`, a weighted sum of `hat f` over the zeros
equals a sum over prime powers plus archimedean terms. Package it as a bilinear pairing:

$$
\begin{aligned}
W(f, g) &= \sum_{\rho} m_{\rho}\, \hat f(\gamma_{\rho})\, \overline{\hat g(\gamma_{\rho})} && \text{a Hermitian form on test functions} \\
W(f, f) &\ge 0 \ \text{for all } f \iff \text{Riemann hypothesis.} && \text{(Weil 1952, Bombieri 2000, Yoshida 1992)}
\end{aligned}
$$

Positivity of `W` on the whole space of test functions is *equivalent* to the hypothesis. Testing it
everywhere is as hard as the hypothesis itself. The move is to test it on a small, explicit,
finite-dimensional family and see how much that finite piece alone can force.

### 6b. The finite compression

Take a family `V` of `d \approx \lambda N` test functions: modulated copies `phi(u) e^{i tau_k u}` of
one fixed window, with centre frequencies `tau_k` spread through the height window `[T, 2T]` at the
critical sampling density, with `0 < lambda <= 1` the normalised bandwidth. Let `G` be the
`d x d` real symmetric matrix of `W` restricted to `V` (a Gabor system's Gram matrix against the
explicit-formula kernel). Three facts about `G` are then available.

**(Z) Zero side, signature and rank.** By the functional equation `G = P + Q` where:

$$
\begin{aligned}
\text{each distinct on-line point } (\beta = \tfrac{1}{2}) &\longrightarrow \text{a rank-one } \textbf{positive} \text{ block in } P && P \succeq 0,\ \operatorname{rank} P \le s \\
\text{each off-line pair } \{\rho, 1 - \bar{\rho}\} &\longrightarrow \text{a block of signature } (1, 1) \text{ in } Q && 1 \text{ positive}, 1 \text{ negative eigenvalue}.
\end{aligned}
$$

An on-line zero pushes the form up; an off-line pair pushes it up once and down once. By
**Sylvester's law of inertia** (restricting a form cannot manufacture positive directions), the
number of positive eigenvalues of `G` is bounded by `s + p`, where `s` counts distinct on-line
points and `p` distinct off-line pairs. That the *negative* index of Weil's form counts off-line
zeros is Bombieri's (2000) observation; the argument uses the rank and the positive index.

**(P) Prime side, magnitude.** The trace and squared Frobenius norm of `G` are, by the explicit
formula, integrals of explicit kernels against the prime powers `n <= X = (T/2\pi)^{\lambda}` and the
Gamma factor. They are exactly Montgomery's first and second moments, and by BGSTB24 they are
**unconditional**:

$$
\begin{aligned}
\operatorname{tr} G &= \big(1 + o(1)\big)\,N && \text{first moment (mean density of zeros)} \\
\|G\|_F^2 = \operatorname{tr} G^2 &= \left(\frac{1}{\lambda} + \frac{\lambda}{3} + o(1)\right)N && \text{Montgomery's second moment, prime side.}
\end{aligned}
$$

**(L) Linear algebra.** For Hermitian `P \succeq 0` of rank `<= r` and Hermitian `Q` with at most `b`
positive eigenvalues, the rank-trace inequality (proved via von Neumann's trace inequality)

$$
\begin{aligned}
r &\ge 2\operatorname{tr}P + 4\operatorname{tr}Q - 4b - \|P + Q\|_F^2 && \text{the matrix analogue of } m^2 \ge 2m - 1
\end{aligned}
$$

is the exact linear-algebra shadow of Montgomery's integer inequality on multiplicities.

### 6c. Combining

Feed (Z) and (P) into (L). In units where an isolated simple zero has eigenvalue `1`, `tr G = N`,
`tr Q` and `b` contribute the off-line count, and the number `s` of distinct on-line points satisfies

$$
\begin{aligned}
s &\ge 4N - 2N - \left(\frac{1}{\lambda} + \frac{\lambda}{3}\right)N - o(N) && \text{substitute the two moments into (L)} \\
  &= \left(2 - \frac{1}{\lambda} - \frac{\lambda}{3} - o(1)\right)N \\
  &= \big(H(\lambda) - o(1)\big)N, && H(\lambda) := 2 - \frac{1}{\lambda} - \frac{\lambda}{3} \\
H(1) &= \tfrac{2}{3}. && \text{at full bandwidth } \lambda = 1.
\end{aligned}
$$

That is Theorem A: `liminf N_0(T)/N(T) \ge 2/3`. The same inequality, applied with the simple on-line
points on the rank side (the matrix analogue of `m^2 \ge 3m - 2`), gives Theorem B (the `2/3` are
simple *and* on the line) and Theorem C (`5/6` of the zeros are distinct). No mollifier, no
zero-density estimate, no zero-free region, and above all no assumption that any zero is on the line.

$$
\begin{aligned}
H(\lambda) &= 2 - \frac{1}{\lambda} - \frac{\lambda}{3}, & H_d(\lambda) &= \frac{1 + H(\lambda)}{2}, & F(\lambda) &= \frac{\lambda}{1 + \lambda^2/3}, \\
H(1) &= \tfrac{2}{3}, & H_d(1) &= \tfrac{5}{6}, & F(1) &= \tfrac{3}{4}.
\end{aligned}
$$

Optimising the test family (replacing the flat window by the Montgomery-Taylor kernel, still with
bandwidth `<= 1`) sharpens the three constants to `0.6725`, `0.6725`, `0.83625` (Theorem D), and the
same argument gives the same constants for a fixed primitive Dirichlet `L`-function (Theorem E).

![The constants as functions of bandwidth: H(lambda) rising to 2/3 at lambda=1, the optimal-window curve reaching 0.6725, and H_d, F.](figures/6_weil_form_argument/6_2_H_lambda_curve.png)

*`H(\lambda) = 2 - 1/\lambda - \lambda/3` is the bound the flat window gives; it reaches `2/3` at the
largest known bandwidth `\lambda = 1`. The optimal (Montgomery-Taylor) window `H_{\text{opt}}(\lambda)`
sits just above it and reaches `0.6725` at `\lambda = 1`. That value is a genuine maximum of the
functional at bandwidth one: no window does better (Part 8).*

![On-line zeros give positive rank-one blocks, off-line pairs give signature (1,1); the eigenvalue signs of the finite form G bound the on-line count.](figures/6_weil_form_argument/6_1_weil_form_signature_anim.gif)

*The finite form `G = P + Q`. On-line points stack up as positive directions (green); each off-line
pair adds one positive and one negative direction (signature `(1,1)`). Counting positive eigenvalues
against the fixed trace and Frobenius norm is what pins at least two thirds of the zeros to the
line, with no positivity assumed off it.*

---

## 7. A numerical framework that reproduces the bound

The finite object of Part 6 is small and completely explicit, so it can be built and checked
directly from the real zeros. The scripts in `framework/` do this; they are illustrative (the small
heights involved are far inside the range where the hypothesis is already verified, so the
certificates certify nothing *new*), but they reproduce every finite identity the proof rests on.

- **The two sides agree.** Building `G` from the first few thousand real zeros, and independently
  from the prime powers and the Gamma factor, gives the *same* matrix to `~10^{-8}` (the residual is
  the truncation of the zero sum). This is the explicit formula, checked numerically.
- **The moments hit their asymptotics.** `tr G / N -> 1` and the ratio `C = (tr G)^2 / tr G^2`
  approaches `F(\lambda)` from the predicted side: at `lambda = 1`, windows near height `10^4-10^6`,
  the framework reproduces `C/N` values `0.757-0.766` against `F(1) = 0.75`, matching the paper's
  Table (2).
- **The certificate never lies.** Replace the true (on-line) zeros by synthetic *off-line* pairs of
  increasing depth: the positive index and the rank-trace certificate drop, exactly tracking the
  signature-`(1,1)` accounting, and never certify more on-line points than are actually present.

![The two moments computed from real zeros converging to their asymptotic values, and C/N approaching F(lambda).](figures/7_numerical_framework/7_1_moments_convergence.png)

*The first two trace moments of `G`, built from real zeros, against the closed forms `1` and
`1/\lambda + \lambda/3`; the ratio `C/N` sits just above `F(\lambda)` as Part 6 predicts.*

![As true zeros are replaced by synthetic off-line pairs, the rank-trace certificate falls and never exceeds the true on-line count.](figures/7_numerical_framework/7_2_synthetic_certificate_anim.gif)

*A stress test of the signature accounting: deepening synthetic off-line pairs drives the certificate
`2C - N'` below zero, exactly as Sylvester's law demands. Pairing or multiplicity always lowers the
certificate at fixed `N`; in no configuration does it exceed the truth.*

The same three pieces (build the form, take two moments, apply the inertia inequality) are what the
Lean development in `lean/` states and, for the linear-algebra core, proves.

---

## 8. What it would take to push past two thirds

Is `2/3` the best this method gives? Everything the certificate does with the finite form reduces
(paper eq. 7.3) to one scale-free functional of a window `v \ge 0` on `[-\tfrac12, \tfrac12]` and the
Fourier bandwidth `\lambda`:

$$
\begin{aligned}
c_\lambda(v) &= \frac{\lambda \left(\int v\right)^2}{\int v^2 + \lambda^2 \iint |s - s'|\, v(s)\,v(s')\,ds\,ds'} && \text{the form factor the two moments produce} \\
H &= 2 - \frac{1}{c_\lambda(v)}, & H_d &= \frac{3 - 1/c_\lambda(v)}{2} && \text{simple on-line, and distinct.}
\end{aligned}
$$

The flat window `v \equiv 1` gives `c_1 = F(1) = 3/4`, hence `H = 2/3`. "Pushing further" is a question
about this functional, in four findings, each computed in `framework/push_further.py`.

**One: the best window is Montgomery-Taylor, and nothing beats it.** Maximising `c_1(v)` over
`v \ge 0` is a Rayleigh quotient for the operator `1 + \lambda^2 T` (with `T` the `|s - s'|` kernel);
the maximiser solves `v'' + 2v = 0`, giving `v^*(s) = \cos(\sqrt{2}\,s)`, the Montgomery-Taylor window.
The unconstrained optimum turns out to be strictly positive, so the constraint `v \ge 0` never binds,
and its value is

$$
\begin{aligned}
c^*_1 &= \frac{\sqrt{2}\,\tan(1/\sqrt2)}{1 + (1/\sqrt2)\tan(1/\sqrt2)} = 0.753296\ldots && \text{the optimal form factor} \\
H &= 2 - 1/c^*_1 = 0.67250\ldots, & H_d &= 0.83625\ldots && \text{Theorem D.}
\end{aligned}
$$

This is a maximum, not a lower bound: over all windows at `\lambda = 1`, `0.6725` is the most `c_1(v)`
returns.

**Two: two moments cannot do better than the optimal window.** The certificate reads only two
unconditional numbers off the form, the mean density and Montgomery's second moment,
`(m_1, m_2) = (1, \tfrac43)`. The sharpest possible use of exactly those two numbers is the
Chebyshev-Markov (Christoffel-function) bound, and it returns

$$
\begin{aligned}
\Lambda_1(0) &= \frac{1}{1 + m_1^2/(m_2 - m_1^2)} = \tfrac14 && \text{Christoffel value at } 0 \\
1 - \Lambda_1(0) &= \tfrac34 = F(1) && \text{the positive-index density cap.}
\end{aligned}
$$

The two-moment cap is *exactly* `F(1)`: no argument reading only `(m_1, m_2)` beats the flat-window
density, and the gain over it comes from the variational `|s - s'|` term. (So `0.6725` is the ceiling
of this two-moment, bandwidth-one data. The `0.68185` an earlier draft carried back-solves to
`c = 0.7586 > c^*_1`, above the functional's maximum at `\lambda = 1`, so it is not a two-moment bound
here.)

**Three: higher moments would help, but they are conditional.** The only way past `0.6725` inside
bandwidth `1` is to feed the certificate a *third* number, a higher moment of the form. The limiting
spectral moments of the sine-kernel Gram matrix are `m_k(1) = 1, \tfrac43, 2, \tfrac{13}{4}` for
`k \le 4` (the fourth is the theoretical value; the Monte-Carlo in the framework only corroborates it
loosely, `\approx 3.10` against `3.25`), and a fourth-moment certificate would lift the simple-zero
count to `\tfrac{13}{18} = 0.7222` and the distinct count to `\tfrac{413}{486} = 0.8498`. But the
fourth moment is not free: it
encodes a Hardy-Littlewood asymptotic for additive prime-pair correlations, which lives outside the
unconditional Rudnick-Sarnak range `k\lambda < 2`. At `\lambda \approx 1` that range admits only the
odd moment `k = 3`, and an odd moment does not lower the simple-zero bound. So the ladder past `2/3`
exists, but every rung above the optimal window is conditional.

![The ladder of certified proportions: 5/12, 2/3, 0.6725 unconditional, then 13/18 and 1 conditional, with RH out of reach.](figures/8_pushing_further/8_2_moment_ladder.png)

*What each lever buys. The first three rungs use only the mean density and the second moment at
bandwidth `\le 1`, and are unconditional; `0.6725` is the ceiling of that data. The `13/18` and `1`
rungs need higher correlations (Hardy-Littlewood) and are conditional. Even at proportion `1` the
claim is simple zeros on the line, not the hypothesis.*

**Four: more bandwidth is the other lever, and it is Montgomery's open conjecture.** The alternative
to more moments is more bandwidth. Reading the optimal-window curve past `\lambda = 1`:

$$
\begin{aligned}
\text{to reach } 0.70 &: \quad \lambda \approx 1.04 \\
\text{to reach } 0.80 &: \quad \lambda \approx 1.27 \\
\text{to reach } 0.90 &: \quad \text{above the single-scale ceiling } \approx 0.889.
\end{aligned}
$$

The optimal-window curve has its own ceiling near `0.889` at the pole `\lambda = \pi/\sqrt2`, so no
single-scale window reaches `0.90` at any bandwidth. That bounds this single-window construction, not
the problem: a different window family or a combination is not ruled out here. And getting `F(\alpha)`
on supports past `1` at all is the barrier Montgomery's pair-correlation conjecture sits behind, needing
prime correlations (of the Hardy-Littlewood type) that are themselves open.

![Achievable proportion versus Fourier bandwidth: the unconditional region lambda<=1 tops out at 0.6725, with 0.70 and 0.80 reachable only past the proven range and 0.90 above the single-window ceiling.](figures/8_pushing_further/8_1_bandwidth_ceiling.png)

*The proportion the optimal window certifies, as a function of the bandwidth `\lambda` of
pair-correlation data it may use. The solid arc at `\lambda \le 1` (shaded, unconditional) tops out at
`0.6725`. The dashed continuation shows `0.70` and `0.80` reachable only at `\lambda \approx 1.04,
1.27`, past the range of what is currently proven about prime correlations, and `0.90` above the reach
of this single-window family.*

So "push the proof further" is not one ask but a fork, and both prongs land outside the finite
certificate:

1. **Add a higher moment.** Buys `0.6725 \to 0.7222` (and more), but each moment past the second is a
   Hardy-Littlewood prime-correlation conjecture, not a linear-algebra improvement.
2. **Extend the bandwidth past `\lambda = 1`.** Buys `0.70, 0.80, \ldots`, and is exactly Montgomery's
   pair-correlation conjecture for `\alpha > 1`, a hard and separate problem.

Neither is a matter of a cleverer finite argument, and, as the next part records, neither can reach
the hypothesis itself even if granted.

---

## 9. How it was found, and what it is not

**Authorship.** The paper's author is a large language model developed by Anthropic. An Anthropic
staff member, Jarred Sumner, posed the problem (attempt the Riemann hypothesis, inside Claude Code)
and left the mathematics to the model. The first pass produced and discarded roughly 650 ideas.
On the second, the model spent about 36 hours coordinating around 60 subagents, which between them
ran some 2,400 shell commands and wrote hundreds of Python scripts, cross-checking numerical claims
against known zeros and reviewing each other's reasoning. The cross-domain step was recognising that
the unconditional pair-correlation prime side of Baluyot-Goldston-Suriajaya-Turnage-Butterbaugh could
be married to Bombieri's Weil-form signature count, a combination no one had tried. Ralph Furman and
Levent Alpoge studied the result and take responsibility for its communication; Brian Conrey and Dan
Goldston, experts in the area, examined it on short notice.

**Verification.** A Lean 4 formalisation (`Zeta23`) accompanies the paper: the theorem statements are
expressed directly against Mathlib's `riemannZeta`, and at the cited commit the theorem types carry
no extra hypotheses and the proofs depend only on Lean's three standard axioms. The main-term
constants were separately checked symbolically. (An open, independently rechecked leaderboard now
tracks the record.)

**What it is not.** This is the important part, and the paper states it plainly:

- It has **no bearing on the Riemann hypothesis** in either direction. The argument produces lower
  bounds only. It certifies that at least two thirds of the zeros are on the line and says nothing
  about the remaining third, which are not shown to be off the line, merely not reached by the
  certificate.
- It is **not `67.25%` of the way to a proof.** A guaranteed proportion is not a completion meter.
  If it survives scrutiny the guarantee rises by about `25.6` points in one step, a genuine advance,
  and the distance to a proof is unchanged.
- The techniques are **not expected to lead to a proof** of the hypothesis. The inputs (functional
  equation, explicit formula, mean values of Dirichlet polynomials of length `<= T`) are insensitive
  to `o(N)` off-line zeros, and are satisfied by objects (Davenport-Heilbronn functions, Epstein zeta
  functions of class number `> 1`) for which the analogue of the hypothesis is *false*. Any argument
  built only from these inputs therefore cannot prove the hypothesis, because it cannot tell these
  counterexamples apart from `zeta`.

The result is a large, clean step on the proportion ladder of Part 4, obtained by making an old
conditional argument unconditional. It is not the summit; Part 8 is the honest map of how far this
particular road can go.

---

## Formula reference

$$
\begin{aligned}
\zeta(s) &= \sum_{n \ge 1} n^{-s} = \prod_p (1 - p^{-s})^{-1} && \operatorname{Re} s > 1 \\
\xi(s) &= \tfrac{1}{2}s(s-1)\pi^{-s/2}\Gamma(s/2)\zeta(s), \quad \xi(s) = \xi(1-s) && \text{functional equation} \\
\psi(x) &= x - \sum_{\rho} \frac{x^{\rho}}{\rho} - \log 2\pi - \tfrac{1}{2}\log(1 - x^{-2}) && \text{explicit formula} \\
N(T) &= \frac{T}{2\pi}\log\frac{T}{2\pi} - \frac{T}{2\pi} + O(\log T) && \text{Riemann-von Mangoldt} \\
\kappa &= \liminf_{T\to\infty} N_0(T)/N(T) && \text{proportion on the line} \\
W(f,g) &= \sum_{\rho} m_{\rho}\hat f(\gamma_{\rho})\overline{\hat g(\gamma_{\rho})}, \quad W(f,f)\ge 0 \iff \text{RH} && \text{Weil's form} \\
\operatorname{tr} G &= (1+o(1))N, \quad \operatorname{tr} G^2 = \left(\tfrac{1}{\lambda}+\tfrac{\lambda}{3}+o(1)\right)N && \text{the two moments} \\
r &\ge 2\operatorname{tr}P + 4\operatorname{tr}Q - 4b - \|P+Q\|_F^2 && \text{rank-trace inequality (L)} \\
H(\lambda) &= 2 - \tfrac{1}{\lambda} - \tfrac{\lambda}{3}, \quad H(1) = \tfrac{2}{3}, \quad \text{opt. } 0.6725 && \text{the proportion certified} \\
H_d(\lambda) &= \tfrac{1+H(\lambda)}{2}, \quad H_d(1) = \tfrac{5}{6}, \quad \text{opt. } 0.83625 && \text{distinct zeros (Theorem C, D)} \\
c_\lambda(v) &= \frac{\lambda(\int v)^2}{\int v^2 + \lambda^2\!\iint |s-s'|vv}, \quad c^*_1 = 0.753296 && \text{form factor; optimal window (Part 8)} \\
\text{ceiling} &= 0.6725 \ (\lambda \le 1); \quad \tfrac{13}{18}\ (\text{4th moment, cond.}); \quad 0.70/0.80 \Rightarrow \lambda \approx 1.04/1.27 && \text{limits of the method (Part 8)}
\end{aligned}
$$
