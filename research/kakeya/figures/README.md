# Kakeya figure experiments: framework + catalog

Each mathematically-valid figure is **one self-contained file**. A file computes its geometry from
the formulas in `../kakeya.md`, validates numerically, and renders a preview PNG (statics) or GIF
(animations). This is the staging ground for the marimo notebook: get the *form* right and *proven
against the math* here first, then port the numpy geometry into plotly cells.

Coverage goal: **every formula and every named mathematician** in `../kakeya.md` gets its own figure.

## Layout: grouped by the article structure, ordered by name

Figures live in one subfolder per part of `../kakeya.md`, and each file is prefixed `P_N_` so
sorting by name gives the reading order:

```
1_needle_problem/      2_kakeya_2d/       3_dimension/        4_kakeya_dimension/
5_conjecture_tower/    6_3d_conjecture/   7_solving_3d/
```

`_shared.py` (helpers), `README.md`, and `reference/` (third-party article images, do not ship) stay
at the root. The Perron-tree working attempts live beside the figure they explored
(`2_kakeya_2d/2_4_perron_attempt*.py` and `2_4_perron_attempts_README.md`), not in a separate folder.

## How to run

Scripts import `_shared` from the figures root, so put that root on `PYTHONPATH`:

```
PYTHONPATH=research/kakeya/figures \
  uv run --with matplotlib --with shapely python research/kakeya/figures/<part>/<name>.py
```

Statics output `<name>.png` next to the file; animations output `<name>.gif` via
`_shared.save_gif`. Every run prints a `MATH CHECK` block. (Attempts are self-contained and do not
need `PYTHONPATH`.)

Regenerate every figure (or just some) with the driver, which sets `PYTHONPATH` itself:

```
bash research/kakeya/figures/regenerate.sh                     # all figures
bash research/kakeya/figures/regenerate.sh <part>/<name>.py    # only the given script(s)
```

## Rules (so many agents can each own one figure without colliding)

1. **One figure = one file** named `P_N_topic`. Its only output is `P_N_topic.png` / `.gif`.
2. **Reuse `_shared.py`** for geometry (`equilateral`, `unit_needle`, `deltoid`, `circle`,
   `triangle_fan_degrees`), validation (`union_area`, `poly`), styling (`COLORS`), preview
   (`new_axes`, `save_preview`), reporting (`math_check`), and GIFs (`save_gif`). **Do not edit
   `_shared.py` or another figure file**; if you need a new helper, define it locally.
3. **Geometry is pure numpy**; matplotlib/shapely only for offline validation + preview.
4. **Every file ends by printing a `MATH CHECK`** whose numbers reproduce `../kakeya.md`; animations
   also **assert the animated invariant** (needle length stays 1, wave speed constant, area readout).
5. **Two validations per figure**: *math* (numbers match the research) and *look* (silhouette matches
   the `reference/` image; if not, add an `ALTERNATIVES:` note and, if cheap, extra panels).
6. **Honesty over drama**: when a true object cannot be drawn (measure-zero set, area/dimension in a
   limit), render the *minimum visible* approximation and print the real readout with a note.
7. **Fully visible**: set axis limits from the whole final geometry (with padding) so nothing is cut
   at the plot box, and 3D limits large enough to contain length-1 tubes.
8. Deletions: dev-mcp `safe_remove` (recoverable), never `rm`. Keep `reference/` and the attempts.

Colour logic (mirror the articles): needles/family `COLORS["needle"]`, swept region faint `region`,
inner/thin tubes + grains `accent` (red), outer/thick tubes `outer` (blue), arrows/wireframe `guide`.

---

## Catalog

Static `[S]` and animation `[A]` per concept. Each: math (formula) | reference image | validation.

### 1_needle_problem

- `1_1_needle_rotation_anim` [A] - a unit needle turning through every direction in the disc
  (`A=pi/4`) and the deltoid (`A=pi/8`), accumulating the swept family; length == 1 every frame. |
  wiki_kakeya_needle_deltoid.gif

### 2_kakeya_2d

- `2_1_needle_shapes` [S] - disc `A=pi/4`; deltoid `x=2b cos t+b cos2t, y=2b sin t-b sin2t`, b=1/4,
  chord `4b=1`, `A=2 pi b^2=pi/8`; equilateral (base 1) `A=sqrt3/4`. | fig1a/1b/1c
- `2_1_2_deltoid_rolling_anim` [A] - deltoid drawn by a radius-b circle rolling inside a radius-3b
  circle; marked rim point traces it, tangent chord 4b=1, area 2 pi b^2 = pi/8. | accromath kakeya-cercles1
- `2_1_3_convex_answers_anim` [A] - one fixed unit needle turning in circle (pi/4) -> Reuleaux width 1
  ((pi-sqrt3)/2) -> equilateral height 1 (1/sqrt3); accumulates positions, area drops. | accromath kakeya1/2/3
- `2_2_0_rotate_vs_translate_anim` [A] - the core asymmetry (Accromath): rotating a needle by theta
  sweeps a sector of area `theta/2`, sliding it along its own axis sweeps area 0 (across would cost
  `1 x s`). Position is nearly free, only rotation costs area; the lead-in to the Pal detour. | accromath
- `2_2_pal_join` [S] + `2_2_pal_join_anim` [A] - Pal-join: connect two parallel unit needles with
  area < eps via a far detour; swept area decreasing with detour distance. | (wiki_needle_set.gif)
- `2_2_3_pal_parallel_join_anim` [A] - moving a needle between two parallel lines: naive parallelogram
  `L*d` vs the far detour (slide free + two small sectors `2*(1/2 L^2 alpha)`); area shrinks with the
  detour. | accromath kakeya14/15/16
- `2_3_cut_and_shift` [S] - one bisect+overlap step; shift **arrows**; area(after) < area(before),
  directions preserved. | hickman_fig2a/2b
- `2_4_perron_tree` [S] + `2_4_perron_sprout_anim` [A] - 60 deg apex fan; 3 rotations -> 180 deg;
  cut-and-shift reduces area; true area->0 ~1/log N (Keich), min visible form. | fig3, wiki_perron_tree
- `2_4_perron_wiki_construction` [S] - documented pipeline: subdivide base into 2^n (shared apex) ->
  overlap bases (sprout) -> three trees rotated 120 deg (Besicovitch set). | wiki_perron_tree.svg
  - `2_4_perron_attempt1_topdown_subtree_shift`, `2_4_perron_attempt2_bottomup_asymmetric`,
    `2_4_perron_attempt3_bottomup_symmetric` (+ `2_4_perron_attempts_README.md`) - preserved dead
    ends; each writes its own render PNG. See the attempts README for what each taught us.
- `2_5_1_besicovitch_assembly` [S] + `2_5_1_besicovitch_assembly_anim` [A] - all-direction set from 3
  rotated Perron trees; coverage verified over all 180 one-degree bins; `|K|=0` is a limit, min visible
  approx with area readout. | wiki_needle_set.gif
- `2_5_2_kakeya_construction_anim` [A] - the whole construction in one animation: triangle -> subdivide
  base into 2^6 -> sprout (live area %) -> union three trees rotated 120 deg; direction coverage 0..180
  asserted. Primary construction figure (supersedes the assembly-only anim). | wiki_needle_set.gif
- `2_6_kakeya_needle_set_anim` [A] - Wikipedia needle-set image: solid triangle + corner Perron-tree
  branches + edge fringe, drawn as the filled union silhouette, built up by granularity. |
  wiki_kakeya_needle_set.gif
- `2_7_kakeya_area_shrink_anim` [A] - shrinking the area by Perron cut-and-shift (depth n=0->9),
  measured area 100% -> ~22% of the triangle while every direction is kept; -> 0 only ~1/log N. |
  (companion to 2_6)

### 3_dimension

- `3_1_dimension_boxcount` [S] + `3_1_boxcount_anim` [A] - Minkowski `N(delta)~delta^-d`,
  `d=log N/log(1/delta)`; delta shrinking, covering boxes + count + log-log point. | (grid overlay)
- `3_2_dimension_fractal` [S] + `3_2_fractal_iterate_anim` [A] - Hausdorff `dim=log N/log r`: Cantor
  log2/log3, Sierpinski log3/log2=1.585, Koch log4/log3=1.2619; built by iteration depth. | (redraw)
- `3_3_hausdorff_minkowski` [S] - Minkowski (one box size delta) vs Hausdorff (any sizes <= delta) on
  a Koch curve, and the `H^s` jump from +inf to 0 at `s = dim_H` (`dim_H <= dim_box`). | (redraw)
- `3_4_hausdorff_sweep_anim` [A] - the `H^s` jump made concrete on the Cantor set: sum of the natural
  depth-m cover is exactly `(2 3^-s)^m`; sweep `s` (huge->tiny) then deepen `m` (sharpen to the step),
  pinned to 1 at `s = dim_H = log2/log3`. Closed form, nothing measured. | (animated 3_3)
- `3_5_dimh_le_dimbox_anim` [A] - a case where the two dimensions genuinely differ: dust `{0} U {1/n}`
  has `dim_box = 1/2` (uniform grid wastes cells on the pile-up at 0) but `dim_H = 0` (one interval
  swallows the tail); Cantor set: adaptivity buys nothing, both `log2/log3`. | (redraw)

### 4_kakeya_dimension

- `4_1_davies_rectangles` [S] + `4_1_davies_fan_anim` [A] - two `1 x delta` rectangles at angle theta
  overlap `~delta^2/sin theta`; small overlaps force a spread-out union: area 0 but dimension 2. | (redraw)
- `4_2_area_dimension_boxcount_anim` [A] - the direct "area 0, dimension 2": one honest Perron pile
  (the 2_7 sprout) read by two rulers as delta shrinks - measured area slides toward 0 while the
  log-log box-count slope stays parallel to slope 2 and peels off slope 1 (climbs `loglog`-slowly,
  ~1.66 at these scales). | (companion to 2_7, 4_1)

### 5_conjecture_tower

- `5_1_kakeya_maximal` [S] - Kakeya maximal function; conjecture
  `||f*_delta||_{L^n(S^{n-1})} <= C_eps delta^-eps ||f||_{L^n}`; delta-tubes through a common point. | (redraw)
- `5_2_fourier_transform` [S] + `5_2_fourier_partial_sums_anim` [A] - `f_hat(xi)=int f e^{-2 pi i x xi}`;
  reconstruct a square wave from N harmonics (Gibbs). | (redraw)
- `5_3_plane_wave` [S] + `5_3_plane_wave_anim` [A] - level sets of `cos(2 pi x . xi)`; wavelength
  `1/|xi|`, wavefronts perpendicular to xi; traveling wave. | hickman fig4 (redraw)
- `5_4_uncertainty_principle` [S] + `5_4_uncertainty_anim` [A] - dual boxes `r x s` <-> `1/r x 1/s`;
  Gaussian sigma vs 1/sigma. | hickman fig5 (redraw)
- `5_5_fefferman_ball_multiplier` [S] + `5_5_fefferman_shrink_anim` [A] - `r x r^2` frequency rectangles
  tangent to the unit circle, dual `1/r x 1/r^2` physical rectangles piling over a Perron tree. | fig6a/6b
- `5_6_restriction_conjecture` [S] - extension operator `Eg(x)=int_{S^{n-1}} g e^{2 pi i x.w}`;
  `||Eg||_{L^q}<~||g||_inf` for `q>2n/(n-1)`; wave packets tangent to the sphere. | (relate fig6)
- `5_7_bochner_riesz` [S] + `5_7_bochner_riesz_anim` [A] - multiplier `m^alpha_R=(1-|xi|^2/R^2)_+^alpha`;
  alpha sweeping the corner rounding. | hickman_fig8
- `5_8_local_smoothing_wave` [S] + `5_8_wavefront_cone_anim` [A] - half-wave `e^{it sqrt(-Delta)}`
  concentrates on the light cone `|x|=t`; `s_p=(n-1)|1/2-1/p|`; wavefront radius = t. | (redraw)
- `5_9_conjecture_tower` [S] - implication tower **local smoothing => Bochner-Riesz => restriction =>
  Kakeya**, Kakeya at the base; known n=2, open n>=3. | (schematic)

### 6_3d_conjecture

- `6_1_tubes_3d` [S] + `6_1_tubes_3d_turntable_anim` [A] - `delta x delta x 1` tubes, count `~delta^-2`,
  delta-separated directions on S^2; generic tubes are skew and MISS in R^3. | guth_fig1
- `6_2_refine_union_anim` [A] - what Minkowski dim 3 MEANS: halving delta gives `x4` tubes at `/4`
  volume so content `#T |T| ~ 1` is pinned; `|N_delta K| ~ delta^(3-d)`, so dim 3 (`3-d=0`) keeps the
  union volume lit while dim 5/2 sheds ~29% per halving. | (extends 6_1)
- `6_3_skew_generic_anim` [A] - why 3D is harder: sweep one tube through every direction past a fixed
  probe, the axis gap stays open and pinches to 0 only at isolated crossing angles; a Monte-Carlo
  cloud of pairs is overwhelmingly skew (no crossing argument, hence the Wolff axiom). | (extends 6_1)

### 7_solving_3d

- `7_1_wolff_axiom` [S] - Wolff axiom `#{T in R} <= delta^-2 |R|`; the `(n+2)/2 = 5/2` bound in R^3. | (redraw)
- `7_1_1_wolff_axiom_anim` [A] - the axiom as a capacity law: a slab thins, the cap `delta^-2 |R|` and
  the tube count both drop (count stays under the cap), then a forbidden frame over-stuffs the thin slab
  (9 tubes vs cap 3) = the all-tubes-in-one-slab cheat the axiom rules out. | (extends 7_1)
- `7_2_sticky_vs_nonsticky` [S] + `7_2_sticky_morph_anim` [A] - sticky: each rho-tube holds
  `~(rho/delta)^2` thin tubes; non-sticky scattered; morph between them. | (redraw)
- `7_3_grains_3d` [S] + `7_3_grains_3d_turntable_anim` [A] - grain = `delta x c x c` prism, one tube
  thick, disjoint within a fat tube; Besicovitch compression numbers. | guth_fig2/fig5
- `7_4_induction_on_scales` [S] + `7_4_induction_ratchet_anim` [A] - dimension ratchet `K(d) ->
  K(d+alpha)`, climb 2.5 -> 3; graininess controls the lossy-induction loss. | (redraw)
- `7_5_dimension_timeline` [S] + `7_5_dimension_timeline_anim` [A] - R^3 lower-bound history: Wolff 5/2
  (1995), Katz-Laba-Tao >5/2 (2000), Katz-Zahl 5/2+eps (2017), Wang-Zahl 3 (2025). | (timeline)
- `7_6_compression_anim` [A] - Besicovitch compression made numeric (section 7d): the sprout(n) pile
  only translates its `2^n` pieces, so summed piece area (content) is pinned at 1 while the union
  (footprint) falls `~1/log N`; compression = content/footprint climbs `1.3x -> 4x`, real but bounded.
  | (companion to 2_7)
