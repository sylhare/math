# Kakeya: the problem, the constructions, and the math

The line of reasoning from the simplest model to the 2025 theorem, with the exact math and a figure
for every step:

1. the Kakeya (needle) problem;
2. Kakeya sets in 2D: circle -> deltoid -> Pal triangle -> Perron sprouting -> Besicovitch, the
   shear-and-overlap move that drives the area to zero;
3. dimension: Minkowski (box-counting) first, then Hausdorff (with a fractal example);
4. the dimension of the 2D Kakeya solution (it is 2, even at zero area);
5. the Kakeya conjecture (dimension `n`) and the harmonic-analysis tower resting on it (Fourier,
   Fefferman, restriction, Bochner-Riesz, local smoothing);
6. the 3D conjecture and what Minkowski dimension 3 means for tubes;
7. solving 3D: tubes, sticky vs non-sticky, Guth's graininess/grains, and the compression bound.

Figures referenced below live in `figures/<part>/`; each is a numpy/shapely construction validated
against the formula it illustrates.

---

## Sources (scientific articles cited for the mathematics)

Every theorem, construction, and formula below is sourced from the scientific literature.

- **Jonathan Hickman**, *"The Kakeya Conjecture: where does it come from and why is it important?"*,
  arXiv:2512.09842 (2025), HTML `https://arxiv.org/html/2512.09842v1`. Primary source for the
  Fourier/Fefferman story, Bochner-Riesz, the Wolff axiom, and the sticky reduction.
- **Joshua Zahl**, *"A Survey of the Kakeya conjecture, 2000-2025"*, arXiv:2512.09397. Source for the
  "Besicovitch compression phenomenon" framing and the modern dimension-lower-bound history.
- **Hong Wang, Joshua Zahl**, *"Volume estimates for unions of convex sets, and the Kakeya set
  conjecture in three dimensions"*, arXiv:2502.17655 (2025). The `R^3` theorem itself.
- **Terence Tao**, *"The three-dimensional Kakeya conjecture, after Wang and Zahl"* (2025),
  `https://terrytao.wordpress.com/2025/02/25/the-three-dimensional-kakeya-conjecture-after-wang-and-zahl/`.
  Precise discretized language for grains, stickiness, and induction on scales (incl. the
  lossy-induction / "Chinese whispers" framing).
- **Larry Guth**, *"The Kakeya conjecture, after Wang and Zahl"*, arXiv:2604.03416 (grain = "grains in
  a piece of wood"; slabs `1 x N^sigma x N^sigma`); and Guth, *"Degree reduction and graininess for
  Kakeya-type sets in R^3"*, arXiv:1402.0518 (origin of graininess via the polynomial method).
- **Zeev Dvir**, *"On the size of Kakeya sets in finite fields"*, J. Amer. Math. Soc. 22 (2009): the
  finite-field Kakeya theorem via the polynomial method (a low-degree polynomial vanishing on a
  Besicovitch set must be identically zero), the technique Guth later carried into `R^n`.
- **K. J. Falconer**, *The Geometry of Fractal Sets* (CUP, 1985), pp. 96-99: rigorous Perron-tree
  construction and area estimate; and **Falconer**, *Fractal Geometry*, for the Minkowski/Hausdorff
  dimension definitions and the self-similar dimension formula.
- **Terence Tao**, *"Recent progress on the restriction conjecture"*, arXiv:math/0311181: statement
  of the restriction/extension conjecture and its link to Kakeya.
- **D. Beltran, J. Hickman, C. D. Sogge**, *"Variable coefficient Wolff-type inequalities and sharp
  local smoothing estimates for wave equations on manifolds"* (and Sogge, *Fourier Integrals in
  Classical Analysis*): statement of the local smoothing conjecture.
- **Charles Fefferman**, *"The multiplier problem for the ball"*, Ann. of Math. 94 (1971): the ball
  multiplier counterexample built from Besicovitch geometry.
- **International Mathematical Union**, *Fields Medals 2026*,
  `https://www.mathunion.org/imu-awards/fields-medal/fields-medals-2026`: Hong Wang awarded the
  Fields Medal on 23 July 2026 for contributions to harmonic analysis and geometric measure theory,
  including the proof of the three-dimensional Kakeya conjecture. See also N. Wolchover,
  *"Hong Wang Wins 2026 Fields Medal, the Third Woman Ever"*, Quanta Magazine (23 July 2026).
- **Wikipedia**, *Kakeya set* `https://en.wikipedia.org/wiki/Kakeya_conjecture` (convenience index for
  the classical constructions and the dimension-lower-bound timeline; primary sources above).

Key primary result to cite: **Hong Wang and Joshua Zahl (2025)** proved every Kakeya set in
`R^3` has Hausdorff and Minkowski dimension 3. The 2D case was settled in the 1970s (Davies).

---

## 1. The Kakeya needle problem

Sōichi Kakeya, 1917: take a needle (a unit line segment) lying on a table. Rotate it so that it
points, at some moment, in **every** direction, i.e. turn it a full half-turn. What is the smallest
**area** it can sweep out while doing so?

That is the first question: it is about *motion* (a needle turning), and the "smallest area" is the
puzzle. The needle has fixed length 1; it only translates and rotates, never growing or shrinking.

Three obvious ideas all fail, and seeing why points the right way. Shrinking the disc fails: a
smaller disc cannot hold the needle pointing sideways at all. Squeezing the disc into an ellipse
fails: the horizontal extremes still need the full unit width. Pivoting about an endpoint instead
of the center only changes which disc you get, not its size. Every cheap idea keeps the needle
*rotating in place*, and rotating in place is what fills area. Kakeya himself guessed the answer
was the deltoid below; the real answer needs the needle to *travel* while it turns.

![A unit needle turning through every direction inside the disc and the deltoid; length stays exactly 1.](figures/1_needle_problem/1_1_needle_rotation_anim.gif)

Two closely related objects, distinct because the math differs:

- **Kakeya needle set**: a set inside which the unit needle can be *continuously rotated* through a
  full turn. This is the "moving needle" object. Its infimal area is **0** but it is never attained
  (you can get arbitrarily small, but not zero, if continuous motion is required).
- **Besicovitch set** (a.k.a. Kakeya set in the modern sense): a set that merely *contains* a unit
  segment in every direction, with no requirement that the needle move continuously between them.
  Here the infimal area is **0 and attained**: there exist Besicovitch sets of measure zero.

Modern definition to state explicitly (Hickman, Def. 1.1):

> A compact set `K ⊆ R^n` is a **Kakeya set** if for every direction `ω ∈ S^{n-1}` there is a
> position `a ∈ R^n` such that the segment `ℓ_{ω,a} := {a + tω : 0 ≤ t ≤ 1} ⊆ K`.

---

## 2. Kakeya sets in 2D: the walk from circle to zero area

A chain of "good, but we can do better" moves: each shape is a real answer, and each leaves a
specific gap the next one closes.

![The three classic 2D answers and their areas: disc pi/4, deltoid pi/8, Pal's equilateral triangle 1/sqrt3.](figures/2_kakeya_2d/2_1_needle_shapes.png)

### 2a. The circle (the obvious first answer)

Spin the needle about its **midpoint**. Every point within distance `1/2` of the center is covered,
so the swept region is a disc of radius `r = 1/2`.

$$
\begin{aligned}
A_{\text{disc}} &= \pi r^2                       && \text{area of a disc of radius } r \\
                &= \pi \left(\tfrac{1}{2}\right)^2 && \text{the needle reaches only } r = \tfrac12 \\
                &= \frac{\pi}{4} \approx 0.785.
\end{aligned}
$$

Good: it certainly turns the needle through every direction. Gap: it is wasteful. The center is
covered over and over; the needle does not need a solid disc.

### 2b. The deltoid (turn it, do not just spin it)

Instead of pivoting about the midpoint, let the needle stay **tangent** to a curve while both ends
move. What this buys: the needle now *slides along its own direction* as it turns, so positions
already swept are not swept again, and that saving is exactly what halves the area below (slide
versus rotate is the asymmetry the whole area story rests on; Section 2d makes it precise). The
envelope is a **three-cusped hypocycloid (deltoid)**: the curve traced by a point on a
circle of radius `b` rolling inside a circle of radius `3b`.

Parametric form, with rolling-circle radius `b`:

$$
x(t) = 2b\cos t + b\cos 2t, \qquad y(t) = 2b\sin t - b\sin 2t, \qquad t \in [0, 2\pi).
$$

![A circle of radius b rolling inside a circle of radius 3b; a marked point on the rolling rim traces the deltoid, the tricuspid curve tangent to the needle in every direction.](figures/2_kakeya_2d/2_1_2_deltoid_rolling_anim.gif)

The segment of any tangent line cut off inside the deltoid has **constant length `4b`**. For a unit
needle set `4b = 1`, so `b = 1/4`. The enclosed area of a deltoid is `2\pi b^2`, hence

$$
\begin{aligned}
A_{\text{deltoid}} &= 2\pi b^2                    && \text{area of a deltoid, rolling radius } b \\
                   &= 2\pi \left(\tfrac{1}{4}\right)^2 && \text{unit chord } 4b = 1 \Rightarrow b = \tfrac14 \\
                   &= \frac{\pi}{8} \approx 0.393
                   = \tfrac12 A_{\text{disc}}.
\end{aligned}
$$

So the deltoid is exactly **half** the disc's area. Good: the needle really
turns inside it. Gap: is the deltoid the *minimum*? It is not.

### 2c. Pal: the smallest *convex* set

Julius Pal (1921): among **convex** sets, the smallest Kakeya set is the **equilateral triangle of
height 1**.

$$
\begin{aligned}
\text{height } h &= 1, \quad \text{side } s = \tfrac{2}{\sqrt3} \\
A_{\triangle} &= \tfrac{\sqrt3}{4}\, s^2
             = \tfrac{\sqrt3}{4}\cdot \tfrac{4}{3}
             = \frac{1}{\sqrt3} \approx 0.577.
\end{aligned}
$$

Among convex sets the needle can also turn in a **Reuleaux triangle** of width 1, pivoting about its
three corners, area `(\pi-\sqrt3)/2 \approx 0.705`, between the disc and Pal's triangle. The same unit
needle turns in all three convex answers, and the area drops from the disc to the triangle:

![The same unit needle turning in the three convex answers: spinning about one point fills the disc (pi/4); pivoting about three corners fills the Reuleaux triangle ((pi-sqrt3)/2); the equilateral triangle of height 1 is smaller still (1/sqrt3).](figures/2_kakeya_2d/2_1_3_convex_answers_anim.gif)

Convexity is the enemy: `0.577 < 0.785` (disc) but `> 0.393` (the deltoid is non-convex already, so
it beats the convex bound). This looks like a step backwards, and that is exactly why it matters.
The triangle is not a better final answer; it is a better *part*. A convex shape must be kept whole,
but a triangle can be cut into pieces and the pieces rearranged, and rearranging is where the area
is won. Dropping convexity lets the area collapse, which motivates cutting the shape apart and
overlapping the pieces.

### 2d. The one trick that makes area shrink: shear + overlap (Pal join / Perron sprouting)

Everything that shrinks the area rests on one asymmetry between the two ways a needle can move
(the deltoid above already exploited it quietly; from here on it is pushed to the extreme). Sliding
a needle along its own length sweeps no new area (it stays on the same line), while rotating it by an
angle `θ` sweeps a circular sector of area `θ/2`. Position is nearly free; only direction costs area, so
every trick below spends rotation as sparingly as it can.

![The needle first rotates about an endpoint, filling a sector of area theta/2; then it slides along its own axis and the swept area does not change. Rotation is what costs area; sliding a needle along its own length is free.](figures/2_kakeya_2d/2_2_0_rotate_vs_translate_anim.gif)

The shear-and-overlap move that drives the area down lives here. Two moves:

- **Directions are cheap to keep, position is free to change.** A unit segment in a given direction
  can sit *anywhere*; only its direction matters for the Kakeya condition. So we may slide pieces on
  top of one another. Overlap is free area savings: two triangles that each carry a fan of
  directions, translated to overlap, still carry the union of those directions but occupy less area.

- **Pal join (a.k.a. Pal worm).** *Lemma:* given two **parallel** unit segments `G1, G2` and any
  `ε > 0`, there is a set `J` with `area(J) < ε` inside which the needle can be moved continuously
  from `G1` to `G2`. Idea: slide the needle far out along its own direction (almost free area,
  a long thin sliver), rotate by a tiny angle way out where the pivot is cheap, translate, and come
  back. This lets a needle *travel* continuously between segments, upgrading a Besicovitch set into a
  Kakeya **needle** set.

![Pal join: the needle detours far out along its own direction, turns where pivoting is cheap, then returns; the swept area shrinks with the detour distance. Static and [animation](figures/2_kakeya_2d/2_2_pal_join_anim.gif).](figures/2_kakeya_2d/2_2_pal_join.png)

**Perron tree (the sprouting construction).** Start with a triangle of height 1 (which already
contains segments spanning a fan of directions, like the Pal triangle). Split its base into `2^k`
equal pieces, giving `2^k` thin subtriangles that together still cover the same fan of directions.
Now translate each subtriangle horizontally so that consecutive ones **overlap** as much as
possible while keeping their apex directions. The overlaps cut the total area. Each of the `k`
levels of subdivision adds only a fixed slice of fresh area, so iterating the
pairwise sprouting/overlap over the `k` levels gives a total area of the resulting "tree" satisfying a
bound of the form

$$
A_k \;\le\; \big(\text{const}\big)\cdot A_0 \cdot \tfrac{1}{k}\ \longrightarrow\ 0
\quad\text{as } k\to\infty,
$$

so for any `ε > 0` a Perron tree with area `< ε` exists while still containing a unit segment in
every direction of the original fan (a 60-degree fan for one triangle).

![Building the tree step by step: the needle sweeps the triangle's 60-degree fan, the base is subdivided into 2^6 sub-triangles, then they sprout to overlap; the footprint falls to 44% while the fan of directions stays 60 degrees. The [sprouting animation](figures/2_kakeya_2d/2_4_perron_sprout_anim.gif) shows the cut-and-shift moves themselves, level by level.](figures/2_kakeya_2d/2_4_perron_steps_anim.gif)

The 60-degree span is an artifact of using one triangle's fan, not a real limit: three rotated copies
(0, 60, 120 degrees) cover all 180 degrees of directions. The reason to press on is that the
sprouting already shows the area is not bounded below by any positive number.

### 2e. Besicovitch: exactly zero area

Assemble a full set of directions from rotated Perron trees: an equilateral (60-degree) tree covers a
60-degree range of directions, so **three** rotated copies (0, 60, 120 degrees) tile the full 180
degrees of directions (a direction and its reverse are the same); six copies give the familiar
symmetric six-pointed star. Then take the construction to the limit `k → ∞`. Besicovitch (1919/1928):

> There exists a Kakeya (Besicovitch) set `K ⊆ R^2` with `|K| = 0` (Lebesgue measure zero).

![Building the six-pointed star, step by step: one Perron tree carries a 60-degree fan, and rotated copies dropped in every 60 degrees spread that fan around the circle (three copies already cover all 180 directions, six close up the symmetric star). A needle then sweeps every direction inside the finished star; a gauge tracks the directions covered. The [assembly animation](figures/2_kakeya_2d/2_5_1_besicovitch_assembly_anim.gif) drops the three rotated copies in one by one; the [construction animation](figures/2_kakeya_2d/2_5_2_kakeya_construction_anim.gif) runs the whole pipeline from equilateral triangle to union.](figures/2_kakeya_2d/2_5_5_besicovitch_star_build_anim.gif)

![Documented pipeline: subdivide the base into 2^n triangles (shared apex), overlap bases (sprout) into one Perron tree, then three trees rotated 120 deg about the centroid = a Besicovitch set.](figures/2_kakeya_2d/2_4_perron_wiki_construction.png)

Side by side, the non-convex answers, the concave counterpart of the convex chain in 2c: the deltoid
turns a needle tangent to its three cusps, the Perron tree shrinks a triangle's footprint while keeping
its 60-degree fan, and three trees assemble into the six-pointed Besicovitch star that points a needle
in every direction.

![Three non-convex Kakeya shapes with a unit needle placed honestly in each: for every direction it is a real unit chord of the shape, so it both rotates and translates the way a needle really moves through a Kakeya set, never pivoting about one point. The deltoid (area pi/8) holds the needle tangent; the Perron tree (footprint 44% of the triangle) holds it along each branch of the same 60-degree fan; the six-pointed Besicovitch star (three trees) holds one in every direction, area to 0 in the limit.](figures/2_kakeya_2d/2_1_4_nonconvex_answers_anim.gif)

For the *needle* (continuous-rotation) version, Pal joins glue the pieces; the area can be made
arbitrarily small but **not** zero (a Kakeya needle set cannot have measure zero, a general fact).
The intuition: continuous turning means that at every instant the needle covers a genuine little
sector of nearby directions, and sewing those sectors together forces a positive amount of swept
area at every scale, no matter how cleverly the detours are arranged (heuristic; the rigorous
statement is a theorem).
Van Alphen (1942) fit arbitrarily small needle sets inside a disc of radius `2 + ε`; Cunningham
(1971) improved this to a simply-connected needle set of arbitrarily small area inside the **unit
disc** (radius 1), the smallest disc that can hold a unit segment at all. The distinction:
**measure zero for "contains a segment in every direction"; only
arbitrarily-small-but-positive for "a needle you can actually turn."**

![How Pal joins do the gluing: the tree holds a needle in every direction but in separate branches. To carry the needle from one branch to the next, slide it out along its own axis (free), make the small turn far out where a tiny angle suffices, then slide back into the next branch. Chaining the joins across every branch rotates the needle continuously through the fan; only the little turn slivers add area, so the tree plus the fringe is a needle set of small positive area.](figures/2_kakeya_2d/2_5_4_pal_tree_needle_set_anim.gif)

![The Kakeya needle set: a unit segment in every direction, drawn as a filled silhouette, a solid triangle with Perron-tree branches at the corners.](figures/2_kakeya_2d/2_6_kakeya_needle_set_anim.gif)

### 2f. How fast the area shrinks

The Besicovitch area `→ 0`, but slowly. A fixed-fraction overlap schedule plateaus at about **47% of
the triangle** (a self-similar fixed point). Reaching `0` needs the Perron / Schoenberg / Keich shift
schedule, and even then the decay is on the order of `1/log N` for `N = 2^n` subtriangles (Keich's
sharp bound; Falconer pp. 96-99):

$$
A_N \ \sim\ \frac{c}{\log N}\ \longrightarrow\ 0 \qquad (N = 2^n \to \infty).
$$

So the area can be driven below any `ε`, but only logarithmically slowly: it cannot be shown
collapsing all the way to zero on screen.

![Shrinking the area by Perron cut-and-shift: the core shears thin (area 100% -> ~22% of the triangle) while every direction is kept.](figures/2_kakeya_2d/2_7_kakeya_area_shrink_anim.gif)

---

## 3. Dimension: the right way to say "still big"

The zero-area result forces the question: a Besicovitch set has no area,
yet it feels large (it has segments pointing everywhere). The trap to avoid: "measure zero" does
**not** mean small in every sense. The rational numbers have measure zero and are everywhere
dense; the Cantor set has measure zero and is uncountable. Area is one ruler, and it reports zero
for all of these, but zero area only means "no thickness," not "no points." A concrete picture
(Paris-Saclay): the set is a pile of mikado sticks dropped not at random but arranged so cleverly that
one points in every direction while the pile takes almost no room. Area sees only "almost no room" and
reports zero; it cannot tell that clever pile from an empty table. We need **dimension**, and it should
be introduced in two stages.

![Measure zero means no thickness, not no points: the rationals, the Cantor set, and a Besicovitch set all have cover length shrinking to zero (left), yet each is still large in another sense, dense, uncountable, and all-directions respectively (right).](figures/3_dimension/3_0_measure_zero_not_small.png)

### 3a. Minkowski (box-counting) dimension first

Cover the set with a grid of boxes of side `δ` and count how many boxes `N(δ)` it meets.

$$
\dim_{\text{box}} K \;=\; \lim_{\delta \to 0^+} \frac{\log N(\delta)}{\log(1/\delta)},
\qquad\text{equivalently}\qquad N(\delta) \sim \delta^{-d}.
$$

Check with `δ = 1/10`:

$$
\begin{aligned}
\text{segment (length 1):} \quad & N(\delta) = \delta^{-1} = 10 && d = 1,\\
\text{unit square:} \quad & N(\delta) = \delta^{-2} = 100 && d = 2.
\end{aligned}
$$

Equivalent "fattening" form used in the proofs (Hickman): fatten `K` to its `δ`-neighbourhood
`N_δ K` and watch its area. `K` has Minkowski dimension `n` when the area shrinks slower than any
power of `δ`:

$$
|N_\delta K| \ \ge\ c_\varepsilon\, \delta^{\varepsilon}\quad\text{for every }\varepsilon>0.
$$

Even though `|N_δ K| → 0`, it does so slower than any `δ^ε`, so the "true dimension" is full. This is
the exact sense in which a zero-area set is still `n`-dimensional.

![Box-counting at shrinking delta: a segment needs N ~ 1/delta boxes (d=1), a square N ~ 1/delta^2 (d=2); the log-log slope is the dimension. Static and [animation](figures/3_dimension/3_1_boxcount_anim.gif).](figures/3_dimension/3_1_dimension_boxcount.png)

### 3b. Hausdorff dimension (many scales at once), with a fractal example

Box-counting uses **one** box size everywhere. Hausdorff lets the cover use boxes of **different**
sizes, big where the set is sparse and small where it is dense. For `s ≥ 0`,

$$
\mathcal{H}^s_\delta(E) = \inf\Big\{ \sum_i (\operatorname{diam} U_i)^s :
E \subseteq \bigcup_i U_i,\ \operatorname{diam} U_i \le \delta \Big\},
\qquad
\mathcal{H}^s(E) = \lim_{\delta\to 0^+}\mathcal{H}^s_\delta(E),
$$

and the **Hausdorff dimension** is the single threshold `s` where `H^s` jumps from `∞` to `0`:

$$
\dim_H E = \inf\{ s \ge 0 : \mathcal{H}^s(E) = 0 \} = \sup\{ s \ge 0 : \mathcal{H}^s(E) = \infty \}.
$$

Always `dim_H E ≤ dim_box E`. Hausdorff is the finer (smaller-or-equal) notion, so a Hausdorff
statement is stronger than the Minkowski one.

![Minkowski uses one box size delta (count N(delta)); Hausdorff allows any sizes <= delta; H^s jumps from +inf to 0 at s = dim_H, and dim_H <= dim_box.](figures/3_dimension/3_3_hausdorff_minkowski.png)

The jump is not an idealization: on a concrete self-similar set it is a closed-form fact. The Cantor
middle-thirds set is `2` copies at scale `1/3`, and its natural depth-`m` cover is `2^m` intervals of
length `3^{-m}`, so the Hausdorff sum of that cover is exactly

$$
\begin{aligned}
\sum_i (\operatorname{diam} U_i)^s &= 2^m\,(3^{-m})^s
   && \text{natural level-}m\text{ cover of the Cantor set} \\
   &= \big(2\cdot 3^{-s}\big)^m
   && \text{a geometric series in } m \text{ with base } 2\cdot 3^{-s} .
\end{aligned}
$$

The base `2·3^{-s}` is `> 1` below `s = \log 2/\log 3`, `< 1` above it, and exactly `1` at that
threshold. So sweeping `s` swings the sum from huge to tiny, and deepening the cover (`m → ∞`) sends
`(2·3^{-s})^m` to `+∞` for `s < dim_H` and to `0` for `s > dim_H`, sharpening into the step at
`s = \log 2/\log 3 ≈ 0.6309`. That threshold is the Hausdorff dimension, read off as the one exponent
the sum refuses to send to `0` or `∞`.

![The H^s jump made watchable: a gauge tracks the cover sum on the Cantor dust (left) while the depth-m curves stack up (right), and only the exponent s = dim_H = log2/log3 keeps the sum from running off to infinity or zero.](figures/3_dimension/3_4_hausdorff_sweep_anim.gif)

**Fractal example** (self-similar sets have an easy dimension). If a set is made of
`N` copies of itself each scaled by factor `1/r`, then `dim = log N / log r`:

$$
\begin{aligned}
\text{Cantor middle-thirds set:} \quad & N=2,\ r=3 && \dim = \tfrac{\log 2}{\log 3} \approx 0.6309,\\
\text{Sierpinski triangle:} \quad & N=3,\ r=2 && \dim = \tfrac{\log 3}{\log 2} \approx 1.5850,\\
\text{Koch curve:} \quad & N=4,\ r=3 && \dim = \tfrac{\log 4}{\log 3} \approx 1.2619.
\end{aligned}
$$

The Sierpinski triangle (`≈ 1.585`, strictly between 1 and 2) is the cleanest single visual: a shape
that is "more than a curve, less than a filled region," which is exactly the flavor a Besicovitch set
turns out to have in higher dimensions. For these self-similar examples `dim_H = dim_box`, so it is a
safe place to show both agreeing before Kakeya shows a case where the distinction bites.

![Self-similar fractals by iteration depth: Sierpinski (dim log3/log2 ~ 1.585) and Koch (dim log4/log3 ~ 1.262). Static and [animation](figures/3_dimension/3_2_fractal_iterate_anim.gif).](figures/3_dimension/3_2_dimension_fractal.png)

On these self-similar sets the two dimensions agree, but in general they need not, and the gap is
exactly what makes a Hausdorff statement stronger than a Minkowski one. The countable set
`E = {0} ∪ {1/n : n ≥ 1}` is the cleanest split. Its points pile up at `0`, so a uniform `δ`-grid must
spend about `δ^{-1/2}` boxes resolving the pile-up (`dim_box = 1/2`), while a single interval can
swallow the whole tail `[0, 1/M]` for the Hausdorff cover and drive the sum to `0` (`dim_H = 0`). Same
set, two rulers, `dim_H = 0 < 1/2 = dim_box`. The Cantor set gains nothing from adaptivity and the two
coincide, which is why "always `dim_H ≤ dim_box`" can be a strict inequality: proving the Hausdorff
version of Kakeya is genuinely more than proving the Minkowski version.

![Two side-by-side box-count sweeps: the dust {0} U {1/n} (left) settles at slope 1/2 under the uniform grid but collapses to 0 once the cover adapts, while the Cantor set (right) lands both rulers together at log2/log3.](figures/3_dimension/3_5_dimh_le_dimbox_anim.gif)

---

## 4. Dimension of the 2D Kakeya solution

Roy Davies (1971) reframed Kakeya in this language and settled 2D:

> Every Kakeya set `K ⊆ R^2` has **Hausdorff and Minkowski dimension 2**, even though it can have
> area (2D Lebesgue measure) zero.

Davies (1971) proved the dimension-2 statement. The clean overlap mechanism behind the modern proof
(the `δ²/sin θ` estimate below) is Cordoba's `L²`/bush argument (1977). The mechanism: fatten each
segment into a `δ`-thin rectangle.
Compute the area of the intersection of two such rectangles as a function of the angle `θ` between
them. Two `1 × δ` rectangles crossing at angle `θ` overlap in area

$$
|R_1 \cap R_2| \ \approx\ \frac{\delta^2}{\sin\theta}\qquad(\text{small }\delta),
$$

so rectangles pointing in well-separated directions barely overlap. Summed over all pairs, the
overlaps are small, which **forces the union to be large and spread out**: you cannot compress the
set below full dimension. That bound on how much a Kakeya set can be compressed is the seed of the
modern framing (Section 7).

![A fan of 1 x delta rectangles at delta-separated angles; two at angle theta overlap ~ delta^2/sin theta, so the union stays spread out. Static and [animation](figures/4_kakeya_dimension/4_1_davies_fan_anim.gif).](figures/4_kakeya_dimension/4_1_davies_rectangles.png)

The overlap bound says the union cannot be compressed; box-counting it says what that buys, directly.
Take the honest Perron cut-and-shift pile from Section 2f and read it with two rulers at once as the
resolution `δ` shrinks: the shapely-measured area `|K_n|` slides toward `0` (the `1/\log N` decay),
while the count of `δ`-boxes the pile meets keeps growing like a solid region,

$$
\begin{aligned}
N(\delta) &\sim \delta^{-d}
   && \text{box count of the fattened pile} \\
\frac{\log N(\delta)}{\log(1/\delta)} &\ \longrightarrow\ 2
   && \text{slope tracks the filled square, not the needle} .
\end{aligned}
$$

On the log-log plot the pile's curve stays parallel to the slope-`2` (filled square) line and peels
off the slope-`1` (single needle) line. The slope climbs toward `2` only `loglog`-slowly, so at these
finite resolutions it reads about `1.66` and is still rising: area and dimension pull in opposite
directions, which is what `area 0, dimension 2` means.

![One Perron pile with two live readouts as delta shrinks: the shapely-measured area ticking down (left) and the log-log box count (right) holding a slope that hugs the filled-square line and pulls off the single-needle line.](figures/4_kakeya_dimension/4_2_area_dimension_boxcount_anim.gif)

The result: **area 0, dimension 2.** The set is invisible to area but fills the plane in the sense of
dimension. This is not a contradiction but two different questions getting two different answers.
"How much paint to cover it?" asks area, and the answer is none: the pile has no thickness. "How
many boxes to find it?" asks dimension, and the answer is all of them: at any resolution the pile
meets essentially every box a solid square would. Zero area and full dimension are the same clever
pile seen by two rulers, one blind to it and one not.

Settling the plane raises two questions, and they organize the rest of the article. First, does the
same hold in every dimension: that is the Kakeya conjecture, taken up for `n = 3` in Sections 6 and 7.
Second, why would a fact about needles matter outside geometry: because this small geometric statement
is the floor of a tower of Fourier-analytic conjectures, which is what turned a 1917 puzzle into a
load-bearing problem in modern analysis. Section 5 builds that tower before the higher-dimensional
geometry resumes.

---

## 5. The Kakeya conjecture and the harmonic-analysis tower

### 5a. The conjecture, named and stated

> **Kakeya conjecture.** Every Kakeya set `K ⊆ R^n` has Hausdorff and Minkowski dimension `n`.

In words: a set containing a unit segment in every direction must have the full dimension of the
space it lives in, no matter how small its volume. It is proven for `n = 2` (Davies) and, as of 2025,
`n = 3` (Wang-Zahl). Open for `n ≥ 4`.

**Kakeya maximal function conjecture** (the analytic form the proofs actually chase; the version the
harmonic analysts use): for the maximal average over `δ`-tubes,

$$
\| f^{*}_\delta \|_{L^n(S^{n-1})} \ \le\ C_\varepsilon\, \delta^{-\varepsilon}\, \| f \|_{L^n(R^n)}
\qquad \text{for all } \varepsilon > 0.
$$

In words: for each direction `ω`, average `|f|` over the *best* `δ`-tube pointing along `ω` (the one
where the average is largest); that best-per-direction average is `f*_δ(ω)`. The conjecture says
this greedy tube-averaging barely amplifies anything: only a `δ^{−ε}` loss, slower than any power.
The link to dimension is contrapositive. If a Kakeya set could be compressed below full dimension,
an `f` concentrated on it would have large tube averages in *every* direction at once, making
`f*_δ` big on the whole sphere and breaking the bound. So the analytic conjecture is exactly the
statement that Besicovitch compression cannot beat full dimension.

![delta-tubes through a common point and the maximal-average heatmap over a tube family; the [animation](figures/5_conjecture_tower/5_1_kakeya_maximal_anim.gif) sweeps one probe tube through every direction and builds the per-direction average curve, whose peak is the maximal function.](figures/5_conjecture_tower/5_1_kakeya_maximal.png)

### 5b. Fourier building blocks

The tower is stated in Fourier terms, so fix the pieces it uses, each with a plain-words reading
first. The Fourier transform is a **recipe book**: any signal is a stack of pure tones, `f̂(ξ)`
records how much of each tone `ξ` the recipe calls for, and the inverse transform stacks the tones
back into the signal. A **plane wave** is one pure tone spread over the whole plane: its wavefronts
are flat, perpendicular to `ξ`, spaced by the wavelength `1/|ξ|`. The **uncertainty principle**
is reciprocal zooming: squeeze a wave into a narrow frequency range and it must spread out in
space, like a light beam that can be narrow or straight but not both. Formally, any function is a
superposition of plane waves via the Fourier transform and its inverse:

$$
\widehat{f}(\xi) = \int_{R^n} f(x)\, e^{-2\pi i x\cdot\xi}\, dx,
\qquad
f(x) = \int_{R^n} \widehat{f}(\xi)\, e^{2\pi i x\cdot\xi}\, d\xi .
$$

![A signal as a sum of harmonics and its spectrum; more harmonics reconstruct a square wave (Gibbs overshoot). Static and [animation](figures/5_conjecture_tower/5_2_fourier_partial_sums_anim.gif).](figures/5_conjecture_tower/5_2_fourier_transform.png)

A single plane wave `x ↦ e^{2πi x·ξ}` has flat **wavefronts perpendicular to `ξ`**, spaced by the
wavelength `1/|ξ|`; higher frequency packs the fronts tighter.

![Level sets of cos(2 pi x . xi) in the plane: fronts perpendicular to xi, spacing 1/|xi|. Static and [animation](figures/5_conjecture_tower/5_3_plane_wave_anim.gif).](figures/5_conjecture_tower/5_3_plane_wave.png)

**Uncertainty principle.** A bump supported on an `r × s` box in frequency is spread over the dual
`1/r × 1/s` box in physical space (reciprocal side lengths, area product `~ 1`):

$$
\text{frequency box } r \times s \quad\longleftrightarrow\quad \text{physical spread } \tfrac1r \times \tfrac1s .
$$

![Dual rectangles: a thin r x s frequency box corresponds to a long 1/r x 1/s physical box through the origin. Static and [animation](figures/5_conjecture_tower/5_4_uncertainty_anim.gif).](figures/5_conjecture_tower/5_4_uncertainty_principle.png)

This reciprocity is the bridge to Kakeya: a thin, curved sliver of frequency becomes a long, thin
tube in physical space (in Wang's phrase, each wave lives on one of the long thin tubes), and tubes in
many directions are exactly a Besicovitch configuration.

### 5c. Why anyone outside geometry cares: Fefferman, 1971

Fefferman asked the most basic convergence question there is. To rebuild a signal from its Fourier
recipe, you sum the tones one cutoff at a time; the natural higher-dimensional cutoff is a ball
(keep every tone with `|ξ| ≤ R`, then let `R → ∞`). Does the partial sum settle down to the true
signal, in the average (`L^p`) sense? For `p = 2` the energy bookkeeping says yes. His
answer for every other `p` is **no**, and the reason is the needle puzzle.

Formally, Fefferman used a Besicovitch/Perron construction to **disprove** the natural higher-dimensional
"ball multiplier" guess: for `n ≥ 2` and `p ≠ 2`, the partial Fourier integral over a ball,
`S_R^{ball} f`, does **not** converge to `f` in `L^p(R^n)` as `R → ∞`. Where do the needles come
from? The boundary of the frequency ball is *curved*, and by the uncertainty principle of Section 5b
a thin curved sliver of frequency dualizes to a long thin tube in physical space, one tube per
tangent direction of the sphere. The counterexample runs on
exactly Kakeya geometry: thin frequency slabs tangent to the sphere pile up in
physical space the way needles pile up in a Besicovitch set, so a geometry puzzle controls the
convergence of Fourier series in higher dimensions.

![Fefferman: r x r^2 frequency slabs tangent to the unit circle, whose dual 1/r x 1/r^2 tubes pile up over a Perron tree. Static and [animation](figures/5_conjecture_tower/5_5_fefferman_shrink_anim.gif).](figures/5_conjecture_tower/5_5_fefferman_ball_multiplier.png)

### 5d. The tower

A tower of conjectures with Kakeya at the **bottom** (weakest, implied by all the others).
Implication order: **local smoothing ⟹ Bochner-Riesz ⟹ restriction ⟹ Kakeya.** Proving Kakeya is
*necessary* for all of them (if Kakeya failed, the whole tower would fall), and the *techniques* that
prove Kakeya are hoped to climb upward. Each rung below gets a plain-words question before its
formula.

![The implication tower local smoothing => Bochner-Riesz => restriction => Kakeya, Kakeya at the base (known n=2, open n>=3).](figures/5_conjecture_tower/5_9_conjecture_tower.png)

**(i) Restriction conjecture** (Stein). In plain words: take a function living only on a curved
surface, say a ripple pattern on a sphere, and let it radiate as waves into the whole space. How
quickly must the radiated wave die out? With the extension operator on the sphere
`E g(x) = ∫_{S^{n-1}} g(ω) e^{2πi x·ω} dσ(ω)`,

$$
\| E g \|_{L^q(R^n)} \ \lesssim\ \| g \|_{L^\infty(S^{n-1})}
\qquad\text{for all } q > \frac{2n}{n-1}.
$$

The threshold `q > 2n/(n-1)` is sharp: the extension of a bump decays like `|x|^{-(n-1)/2}` (the
Fourier transform of surface measure), so `Eg ∈ L^q ⟺ q·(n-1)/2 > n ⟺ q > 2n/(n-1)`. Proven `n = 2`
(Fefferman 1970 / Zygmund 1974); open `n ≥ 3` for the sphere. It asks how the Fourier transform
behaves when restricted to a curved surface.

![Extension operator on the paraboloid/sphere: wave packets tangent to the surface; the L^q bound holds for q > 2n/(n-1).](figures/5_conjecture_tower/5_6_restriction_conjecture.png)

**(ii) Bochner-Riesz conjecture.** In plain words: Fefferman showed the sharp ball cutoff rings
like a badly tuned instrument; can you fix it by softening the cutoff, fading tones out gently near
the boundary instead of chopping them? Smooth the ball cutoff with an exponent `α ≥ 0`:

$$
B_R^{\alpha} f(x) := \int_{B(0,R)} e^{2\pi i x\cdot\xi}\Big(1 - \tfrac{|\xi|^2}{R^2}\Big)^{\alpha}
\widehat{f}(\xi)\, d\xi .
$$

`α = 0` is Fefferman's failing ball multiplier. The conjecture: as soon as `α > 0`, there is a range
of `p` (beyond the trivial `p = 2`) for which `‖B_R^α f − f‖_{L^p(R^n)} → 0`. This is the "clean up /
smooth the edges of a signal without introducing distortion" step. Proven `n = 2`
(Carleson-Sjolin 1972); open `n ≥ 3`. **Bochner-Riesz ⟹ Kakeya** (Fefferman-style: a low-dimensional
Kakeya set would build a counterexample overwhelming the `α > 0` smoothing).

![Bochner-Riesz multiplier (1 - |xi|^2/R^2)_+^alpha: the ball cutoff (alpha=0) smoothed as alpha grows. Static and [animation](figures/5_conjecture_tower/5_7_bochner_riesz_anim.gif).](figures/5_conjecture_tower/5_7_bochner_riesz.png)

**(iii) Local smoothing conjecture** (Sogge, 1991), top of the tower. In plain words: freeze a wave
at one instant and it can spike badly; watch it over a short time interval instead and the spikes
move around, so the *time average* is smoother than any frozen frame. The conjecture asks exactly
how much smoothness this averaging buys. It is about the wave equation via the
half-wave propagator `e^{it√(-Δ)}` (so `u(x,t) = e^{it√(-Δ)} f` solves the wave equation):

$$
\Big(\int_1^2 \big\| e^{it\sqrt{-\Delta}} f \big\|_{L^p(R^n)}^{p}\, dt\Big)^{1/p}
\ \lesssim\ \| f \|_{L^p_{\,s_p - \sigma}(R^n)},
\qquad s_p = (n-1)\Big|\tfrac12 - \tfrac1p\Big|,
$$

for all `σ < 1/p` when `p ≥ 2n/(n-1)` (and `σ < s_p` for `2 < p ≤ 2n/(n-1)`). Plain reading: averaging
the wave in time buys back regularity that a single time-slice cannot; the hardest case is the
endpoint `p = 2n/(n-1)`, where it says `‖u‖_{L^p(R^n×[1,2])} ≤ C_ε ‖f‖_{W^{ε,p}}` for every `ε > 0`.
This is "how waves propagate in space," and it is the strongest: **local smoothing ⟹ Bochner-Riesz,
restriction, and Kakeya** (Tao). Known for `n = 2` (Guth-Wang-Zhang 2020); open `n ≥ 3`.

![A point-source wavefront concentrates on the light cone |x| = t; averaging in time buys back regularity. Static and [animation](figures/5_conjecture_tower/5_8_wavefront_cone_anim.gif).](figures/5_conjecture_tower/5_8_local_smoothing_wave.png)

In one line: Kakeya is the geometric floor of this tower. Points (a segment's worth) versus tubes
(fattened segments) is the same bookkeeping as waves concentrated along light rays, which is why a
needle problem governs the Fourier transform and the wave equation.

Why should a geometry fact control an analysis fact at all? The reflex "Fourier analysis is
calculus, where does geometry enter" has a concrete answer: the uncertainty principle turns every
frequency question into a question about how tubes in many directions pack in space, and packing
tubes is exactly Kakeya. The implication order also has a direction worth pausing on. Kakeya is the
*weakest* statement, so it is the easiest to prove and the first to check; but that is also why it
is necessary: every stronger conjecture assumes it. A counterexample to Kakeya would refute the
whole tower at once, which is why the 1917 puzzle became load-bearing.

---

## 6. The 3D conjecture and what Minkowski dimension 3 means for tubes

> **3D Kakeya conjecture (now a theorem, Wang-Zahl 2025).** Every Kakeya set in `R^3` has Minkowski
> and Hausdorff dimension 3.

The move that makes the problem concrete: in the plane the mikado sticks were infinitely thin, but
for counting purposes give each stick a little thickness. Discretized picture. Fatten every segment
into a **`δ`-tube**: a cylinder of
length 1 and radius `δ` (dimensions `δ × δ × 1`). Because directions are `δ`-separated on the sphere
`S^2`, there are about `δ^{-2}` tubes. The conjecture, in the maximal/measure form, says the union is
essentially as large as it can be:

$$
\Big| \bigcup_{T \in \mathbb{T}} T \Big| \ \gtrsim_\varepsilon\ \delta^{\varepsilon}\quad\text{(morally } \sim 1),
\qquad \#\mathbb{T} \sim \delta^{-2},\ |T| = \delta^2 .
$$

The naive hope is that different directions mean small overlap, so the union's volume should be
about the number of tubes times one tube's volume, `δ^{-2}·δ^2 ~ 1`. The whole difficulty is that
this hope is exactly what can fail: Besicovitch's construction is precisely a way to make tubes in
different directions overlap so much that the union collapses far below the naive count. The
conjecture says the collapse can cost the *volume* everything but cannot cost the *dimension*
anything.

![A bundle of delta x delta x 1 tubes in delta-separated directions on S^2 (count ~ delta^-2); two in different directions are skew and miss. Static and [animation](figures/6_3d_conjecture/6_1_tubes_3d_turntable_anim.gif).](figures/6_3d_conjecture/6_1_tubes_3d.png)

"Dimension 3" means: **halving the tube thickness `δ` removes at most a sliver of the union's
volume** (the volume does not drop like a positive power of `δ`). Equivalently `|N_δ K| ≥ c_ε δ^ε`.

That sentence has a numeric shape. Halving `δ` multiplies the tube count by `4` and divides each
tube's volume by `4`, so the total tube content is pinned across scales:

$$
\begin{aligned}
\#\mathbb{T}\cdot|T| &\sim \delta^{-2}\cdot \delta^{2} = 1
   && \text{content is scale-invariant} \\
|N_\delta K| &\sim \delta^{\,3 - d}
   && \text{how much of that content the union keeps, at dimension } d .
\end{aligned}
$$

Dimension `d = 3` is the case `3 - d = 0`: the union's volume stays bounded away from `0` as `δ → 0`. A
dimension-`5/2` set would have `3 - d = 1/2` and shed about `29\%` of its volume at every halving,
draining to `0`. So "dimension 3" is exactly "refining the tubes cannot drain the union."

![The tube bundle refined across four halvings of delta, read by two meters: the content #T times |T| held flat at one (top), and the union volume that stays lit for the dimension-3 marker but visibly drains for the dimension-5/2 one (bottom).](figures/6_3d_conjecture/6_2_refine_union_anim.gif)

Why 3D is genuinely harder than 2D (Hickman): in the plane, two lines in different directions
almost always **cross**. In space, two tubes in different directions generically **miss** each other
(two generic lines in `R^3` do not intersect). So the 2D argument "different directions force
crossings force spread-out area" has no direct analogue. The content of the 3D conjecture is exactly:
*a family of tubes in different directions cannot overlap too much*, and you must control **all**
configurations at once, not one nice arrangement.

Swept out, that failure is vivid: turn one tube through every direction past a fixed probe tube and
the shortest gap between their axes stays open, pinching to zero only at the isolated instants when the
two directions align. A cloud of randomly placed pairs is overwhelmingly skew. This is why the plane's
crossing argument evaporates, and why the 3D proof reaches for the Wolff axiom below instead of
crossings.

![One tube swept through every direction past a fixed probe with its axis gap plotted (left) and a cloud of random tube pairs (right): the gap stays open on about 95 percent of directions and roughly 90 percent of random pairs are skew, so the crossing that drove the 2D proof is the exception in space.](figures/6_3d_conjecture/6_3_skew_generic_anim.gif)

Two axioms/definitions the proof leans on (Hickman):

- **Direction-separated** (`Def. 5.3`): the core-line directions of the tubes form a `δ`-separated
  subset of `S^2`.
- **Wolff axiom** (`Def. 5.6`): for every rectangular prism `R ⊆ R^3`,
  `#{T ∈ 𝕋 : T ⊆ R} ≤ δ^{-2} |R|`. (No prism swallows more tubes than its volume allows; it rules out
  the degenerate "all tubes inside one slab" cheat.)

![A prism and the tubes it may contain: the Wolff axiom caps this at delta^-2 |R|, giving the (n+2)/2 = 5/2 bound in R^3.](figures/7_solving_3d/7_1_wolff_axiom.png)

Read as a capacity law it is concrete: thinning the prism shrinks `|R|`, so the cap `δ^{-2}|R|` drops and
the slab can legally hold fewer tubes. Packing all `δ^{-2}` tubes into one thin slab, the degenerate
cheat, is exactly the configuration a count above `δ^{-2}|R|` forbids.

![A slab thinning beside a meter comparing the cap delta^-2 |R| to the tube count: the count tracks under the cap as the slab thins, and the final over-stuffed thin slab (9 tubes against a cap of 3) is the forbidden all-tubes-in-one-slab case.](figures/7_solving_3d/7_1_1_wolff_axiom_anim.gif)

This is how the axiom moves the problem forward. With no crossings to lean on, the Wolff axiom trades
the question "which tube meets which" for a single local cap: no prism holds more tubes than its
volume allows. That condition is checkable one prism at a time, needs no global arrangement, and by
itself keeps the tubes from concentrating. From it together with direction-separation, Wolff (1995)
extracted the first bound past the trivial ones, dimension `≥ 5/2`.

Dimension lower-bound history in `R^3`: Wolff `≥ (n+2)/2 = 5/2` (1995); Katz-Laba-Tao Minkowski
`> 5/2` (2000); Katz-Zahl Hausdorff `≥ 5/2 + ε` (2017); Wang-Zahl `= 3` (2025).

![The R^3 dimension lower bound over time: 5/2 (Wolff 1995) climbing to 3 (Wang-Zahl 2025).](figures/7_solving_3d/7_5_dimension_timeline.png)

---

## 7. Solving 3D: tubes, sticky vs non-sticky, grains, compression

The Wolff axiom stalls at `5/2`, a full half-dimension short of `3`: capping the crudest concentration
(all tubes in one slab) is not the same as ruling out the finer ways tubes can still overlap. Closing
that gap is the Wang-Zahl argument, here at explainer resolution (Tao's blog, Hickman Section 5). Two
ideas do the work: **reduce to sticky sets**, then handle the geometry with **grains**, glued by
**induction on scales**.

### 7a. Representing a Kakeya set as tubes, and the two regimes

The question driving this section: zoom out a little, so the thin tubes blur into fatter ones, and
ask how the thin tubes sit inside the fat ones. Take the `δ^{-2}` direction-separated `δ`-tubes.
Look at them at an **intermediate scale** `δ ≤ ρ ≤ 1`
by fattening each `δ`-tube into a `ρ`-tube (`ρ × ρ × 1`). How do the thin tubes distribute among the
fat tubes? Two extreme behaviors:

- **Sticky.** Thin tubes clump inside fat tubes as much as possible. Each `ρ`-tube contains about
  `(ρ/δ)^2` thin tubes, and there are about `ρ^{-2}` fat tubes:

  $$
  \#\{ T \in \mathbb{T} : T \subseteq T_\rho \} \ \sim\ \Big(\tfrac{\rho}{\delta}\Big)^2
  \qquad\text{for every fat tube } T_\rho \text{ and every scale } \delta \le \rho \le 1.
  $$

  This is Hickman's `Def. 5.8`. Sticky sets are **statistically self-similar** across scales: the
  same picture repeats as you zoom, so they are rigid and highly structured. Operationally: *"if two
  thin tubes point in nearly the same direction, they also sit near each other in space"*, like a
  comb, whose teeth stay together because they are parallel.

- **Non-sticky.** Thin tubes scatter; tubes with nearly equal directions can wander far apart. No
  clean self-similarity, the hard case: a pile of sticks tossed at random rather than a comb.

![Sticky vs non-sticky occupancy of a fat tube: sticky packs ~ (rho/delta)^2 thin tubes (self-similar across scales), non-sticky scatters. Static and [animation](figures/7_solving_3d/7_2_sticky_morph_anim.gif).](figures/7_solving_3d/7_2_sticky_vs_nonsticky.png)

Why start with sticky (the "more information = easier" step): stickiness is a lot of extra
structure, so the induction hypothesis can be applied cleanly at both the fat scale `ρ` and inside
each fat tube, and the two multiplicity bounds multiply consistently. This is not cheating:
proving the sticky case first is a reconnaissance that shows the conjecture holds in the regime
where you can compute, and it identifies exactly which enemy remains, the scattered configurations
that refuse to look like combs. Assuming stickiness the
conjecture is *intuitively* the tractable case, and Wang-Zahl proved the **sticky Kakeya conjecture in
`R^3`** first (2022), which was strong evidence the full thing was in reach.

### 7b. The key innovation: sticky reduction

Hickman calls this the single most important move (`Thm. 5.9`, the "sticky reduction"):

> To prove the (strong/discretized) Kakeya bound it **suffices to assume the tubes are sticky.**

So the whole problem collapses onto the structured case. But the reduction is not free: reducing a
general configuration to a sticky one is where the real difficulty moved, and it needs the non-sticky
geometry to be understood, which is where grains enter. Note the sticky case that `Thm. 5.9` reduces
to is a more refined discretized statement than the 2022 *sticky Kakeya* theorem (arXiv:2210.09581);
that is why 2022 did not immediately give 2025.

### 7c. Larry Guth's graininess (the non-sticky handle)

The tool that finds the grains has a clear origin, and it is worth naming because it is a case of one
model unlocking another. The Kakeya conjecture has a **finite-field version**: replace `R^n` by the
vector space `F_q^n` over a finite field and a Besicovitch set by one containing a line in every
direction. Dvir (2009) settled that version outright with the **polynomial method**: a low-degree
polynomial vanishing on a small Besicovitch set would have to vanish identically, so the set cannot be
small. The finite-field proof does not carry over to `R^n` (the Euclidean difficulty, overlaps across
every scale, has no finite-field analogue), but the polynomial method it introduced does, and Guth
carried it into Euclidean space.

Guth (2014, polynomial method) showed any near-counterexample must be **grainy**. Why a new object
at all? Because counting tubes directly is hopeless: two tubes can cross, miss, or run nearly
parallel at every scale, and there is no usable bound on how a *pair* of thin tubes overlaps. The
escape is to stop counting tubes and count *clumps* of tubes instead. Precisely (Guth's
formulation): for tubes of length `N` and radius 1 whose union has volume `N^{3-σ}`, with a
three-directions-at-every-point condition, at scale `N^σ` the tubes cluster into **rectangular slabs
("grains") of dimensions `1 × N^σ × N^σ`**. In the `δ`-normalized picture used by Wang-Zahl, a grain
is a thin prism

$$
\text{grain} \ \approx\ \delta \times c \times c \qquad (\delta \ll c \ll 1),
$$

i.e. **one tube thick, a few times wider, but much shorter than the tubes** that run through it
lengthwise. The name is deliberate (Guth): think of the grain in a piece of wood, many tubes lying
along the grain. A wood analogy runs through this section: tubes are the fibers, a grain is a slab
cut with the grain, and the structural facts below say the slabs tile each log but slabs from
different logs cannot coincide too much.

![Grains: delta x c x c slabs, one tube thick, disjoint within a fat tube; no point lies in too many grains. Static and [animation](figures/7_solving_3d/7_3_grains_3d_turntable_anim.gif).](figures/7_solving_3d/7_3_grains_3d.png)

The structural facts Wang-Zahl exploit (Tao):

- Within a **single** fat tube, the grains are **essentially disjoint** (they tile the tube), and no
  longer grains exist (the width `c` is maximal). So a point sees few grains per fat tube.
- Grains from **different** fat tubes can overlap, but **not too much**: grains from one part of the
  Kakeya set cannot have large intersection with grains from another part. Equivalently, **no point
  in space lies in too many grains.**

The move that makes the proof work: **stop tracking individual tubes and track grains instead.**
Grains are fewer and their overlaps are enumerable; after rescaling, an arrangement of grains looks
locally like an arrangement of `ρ × ρ × 1` tubes (a smaller Kakeya problem), which is what lets the
induction feed on itself.

### 7d. Compression, quantified

"Compression" in plain terms: total tube-content is the amount of pasta you started
with, the union is the size of the pot you managed to fit it into, and compression is packing more
and more pasta into an arbitrarily small pot by overlapping the strands. Formally (Zahl's survey,
the **Besicovitch compression phenomenon**):

> For every `η > 0` there is a `δ > 0` and a set of rectangles of dimensions `1 × δ` pointing in
> `δ`-separated directions whose areas **sum to at least 1**, yet whose **union has measure `< η`**.

That is compression made numeric: total tube-content `≳ 1`, actual footprint `< η`. The Kakeya
conjecture is precisely the statement that this compression **cannot go too far**: the union may be
small but its *dimension* stays maximal. The graininess bound "no point lies in too many grains" is
the quantitative ceiling on compression: it caps how much the tubes can overlap, hence how far the
set can be compressed.

The Perron pile from Section 2 already exhibits this numerically. Its `2^n` pieces are only
translated, so their areas always sum to the original triangle (content stays pinned at `1`) while the
measured union falls like `1/\log N`. Content over footprint is the compression: it climbs, but only
`log N`-slowly (about `1.3x` at `n = 1` to `4x` at `n = 8`), so compression is real yet bounded, which
is the ceiling the conjecture asserts.

![Left: the Perron pile with content, footprint, and compression readouts; right: the pinned content line and the falling footprint line, the shaded gap between them widening with depth.](figures/7_solving_3d/7_6_compression_anim.gif)

### 7e. Induction on scales, and why graininess controls the loss

The finish is **induction on scales**: assume the dimension bound `K(d)` at one scale and bootstrap to
`K(d + α)` for a fixed gain `α > 0`; repeat until `d` reaches 3. The bookkeeping device is the
**multiplicity** `μ`: the number of tubes covering a typical point, that is, how badly the tubes
pile on top of one another. Bounding the union's size from below is the same as bounding `μ` from
above, so the whole game is controlling pile-up as you pass from one scale to the next.

The historical trap (Tao's **Chinese-whispers** analogy, or a rumor passed down a line of people,
each retelling losing a little): each induction step leaks a little, and over many scales the
accumulated loss makes the conclusion worthless. Naively the per-step
multiplicity bound is wasteful,

$$
\mu \ \lesssim\ \mu_{\text{fat}} \cdot \mu_{\text{fine}} ,
$$

which loses too much. Wang-Zahl's fix uses grains to replace the fat-tube multiplicity by the
multiplicity of the **actual union** of thin tubes inside a fat tube:

$$
\mu \ \lesssim\ \mu_{\text{coarse}} \cdot \mu_{\text{fine}},
\qquad \mu_{\text{coarse}} = \text{multiplicity of } \bigcup_{T \subseteq T_\rho} T .
$$

Because grains within one fat tube are disjoint, `μ_coarse` is strictly smaller than `μ_fat`, and the
step **gains** `α` instead of losing. Graininess controls the loss, turning a lossy induction into
one that ratchets the dimension estimate up to exactly 3.

![Induction on scales: the estimate ratchets 2.5 -> 3; graininess keeps each step gaining instead of leaking. Static and [animation](figures/7_solving_3d/7_4_induction_ratchet_anim.gif).](figures/7_solving_3d/7_4_induction_on_scales.png)

### 7f. The result and the payoff

$$
\boxed{\ \text{Wang-Zahl (2025): every Kakeya set in } R^3 \text{ has Hausdorff and Minkowski dimension } 3.\ }
$$

It does not by itself prove restriction / Bochner-Riesz / local smoothing (the implication only
runs downward: the tower needs Kakeya, but Kakeya does not give back the tower), but it removes the
geometric floor's uncertainty and gives the techniques (sticky reduction, grains, induction on
scales) that people now hope to carry up the tower. Hong Wang received the 2026 Fields Medal for this
work with Zahl.

---

## Formula reference

- Needle length fixed at 1 (translation and rotation only).
- Disc `= π/4 ≈ 0.785`; deltoid `= π/8 ≈ 0.393` (exactly half), hypocycloid `b = 1/4`, chord `4b = 1`,
  area `2πb^2`; Pal convex triangle `= 1/√3 ≈ 0.577`.
- Perron tree: `2^k` subtriangles overlapped on shear, area `→ 0` like `~1/log(2^k)`; one triangle
  spans a 60-degree fan, three rotations (0/60/120) span all directions.
- Besicovitch: measure exactly 0 (contains a segment in every direction); needle (continuous-rotation)
  sets are arbitrarily small but positive measure (Pal joins; fit in the unit disc, Cunningham 1971).
- Box-counting at `δ = 1/10`: segment `10` boxes (`d=1`), square `100` boxes (`d=2`).
- Fractal dims: Cantor `log2/log3 ≈ 0.6309`, Sierpinski `log3/log2 ≈ 1.585`, Koch `log4/log3 ≈ 1.2619`.
- Two `1×δ` rectangles at angle `θ` overlap `≈ δ^2 / sin θ` (2D Davies engine).
- 3D tubes: `δ×δ×1`, count `~δ^{-2}`, target union `≳ δ^ε` (dim 3); Wolff axiom `#{T ⊆ R} ≤ δ^{-2}|R|`.
- Sticky: `(ρ/δ)^2` thin tubes per `ρ`-tube, `~ρ^{-2}` fat tubes.
- Grain: `δ × c × c` prism (`δ ≪ c ≪ 1`), disjoint within a fat tube, no point in too many grains.
- Restriction `‖Eg‖_{L^q} ≲ ‖g‖_∞`, `q > 2n/(n-1)`; Bochner-Riesz `B_R^α`; local smoothing
  `(∫_1^2 ‖e^{it√-Δ}f‖_p^p)^{1/p} ≲ ‖f‖_{L^p_{s_p-σ}}`, `s_p=(n-1)|1/2-1/p|`. Order:
  local smoothing ⟹ Bochner-Riesz ⟹ restriction ⟹ Kakeya.
