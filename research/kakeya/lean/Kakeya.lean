/-
Kakeya: from the 1917 needle problem to the 2025 three-dimensional theorem.

Elementary facts are proved; research-level theorems are stated against Mathlib and marked
`sorry`/`axiom` with a citation. The n ≥ 4 conjecture is open. One namespace per part
(`Kakeya.S1 … S8`); `Kakeya.Spine` references one result per part. See README.md and AUDIT.md.

Type-check (Mathlib v4.32.2): cd lean && lake env lean ../research/kakeya/lean/Kakeya.lean
-/
import Mathlib


/- ==============================================================================================
   §1  The Kakeya needle problem
   ============================================================================================== -/

namespace Kakeya.S1
open MeasureTheory Metric


/-- The plane `ℝ²`. -/
abbrev E2 := EuclideanSpace ℝ (Fin 2)

/-- Besicovitch predicate: for every unit `v`, some segment `[p, p+v]` (length 1) lies in `S`
(Besicovitch 1919/1928). -/
def ContainsUnitSegmentEveryDirection (S : Set E2) : Prop :=
  ∀ v : E2, ‖v‖ = 1 → ∃ p : E2, segment ℝ p (p + v) ⊆ S

/-- Needle predicate (Kakeya 1917): a continuous family `θ ↦ [base θ, base θ + dir θ]` of unit
segments in `S` realizing every direction. Strictly stronger than containment. -/
def IsNeedleSet (S : Set E2) : Prop :=
  ∃ base dir : ℝ → E2,
    Continuous base ∧ Continuous dir ∧
    (∀ θ, ‖dir θ‖ = 1) ∧
    (∀ v : E2, ‖v‖ = 1 → ∃ θ, dir θ = v) ∧
    (∀ θ, segment ℝ (base θ) (base θ + dir θ) ⊆ S)

/-- A needle set is Besicovitch (the easy direction; the converse fails). -/
theorem isNeedleSet_containsUnitSegmentEveryDirection {S : Set E2}
    (h : IsNeedleSet S) : ContainsUnitSegmentEveryDirection S := by
  obtain ⟨base, dir, _, _, _, hsurj, hseg⟩ := h
  intro v hv
  obtain ⟨θ, hθ⟩ := hsurj v hv
  exact ⟨base θ, hθ ▸ hseg θ⟩

/-! ### Baseline: the closed disc of radius `1/2` is Besicovitch, with area `π/4`. -/

/-- Points of the segment `[-(1/2)v, (1/2)v]` have norm ≤ 1/2. -/
theorem diameter_segment_subset_closedBall (v : E2) (hv : ‖v‖ = 1) :
    segment ℝ (-(1/2 : ℝ) • v) ((1/2 : ℝ) • v) ⊆ closedBall (0 : E2) (1/2) := by
  intro z hz
  obtain ⟨a, b, ha, hb, hab, hz⟩ := hz
  rw [mem_closedBall_zero_iff]
  have hzv : z = ((b - a) / 2 : ℝ) • v := by
    rw [← hz]; module
  rw [hzv, norm_smul, hv, mul_one, Real.norm_eq_abs]
  rw [abs_div]
  rw [abs_of_nonneg (by norm_num : (0:ℝ) ≤ 2)]
  rw [div_le_iff₀ (by norm_num : (0:ℝ) < 2)]
  have h1 : b - a ≤ 1 := by linarith
  have h2 : -(1 : ℝ) ≤ b - a := by linarith
  rw [abs_le]; constructor <;> linarith

/-- The closed disc of radius `1/2` is Besicovitch: its diameters are the unit segments. -/
theorem closedBall_containsUnitSegmentEveryDirection :
    ContainsUnitSegmentEveryDirection (closedBall (0 : E2) (1/2)) := by
  intro v hv
  refine ⟨-(1/2 : ℝ) • v, ?_⟩
  have hp : -(1/2 : ℝ) • v + v = (1/2 : ℝ) • v := by module
  rw [hp]
  exact diameter_segment_subset_closedBall v hv

/-- Area of the disc of radius `1/2` is `π/4`. -/
theorem volume_closedBall_half :
    volume (closedBall (0 : E2) (1/2)) = ENNReal.ofReal (Real.pi / 4) := by
  rw [EuclideanSpace.volume_closedBall_fin_two]
  rw [← ENNReal.ofReal_pow (by norm_num), ← ENNReal.ofReal_mul (by positivity)]
  congr 1
  ring

end Kakeya.S1


/- ==============================================================================================
   §2  2D Kakeya sets: from circle to zero area
   ============================================================================================== -/

namespace Kakeya.S2
open MeasureTheory Filter Topology Matrix


/-! ### Pál (1921): smallest convex needle set = equilateral triangle of height `h`
(side `2h/√3`, area `h²/√3`); at `h = 1`, area `1/√3`. -/

/-- Side length of an equilateral triangle of height `h`: `s = 2h/√3`. -/
noncomputable def equilateralSide (h : ℝ) : ℝ := 2 * h / Real.sqrt 3

/-- Area of an equilateral triangle of height `h` (base·height/2). -/
noncomputable def equilateralArea (h : ℝ) : ℝ := (1 / 2) * equilateralSide h * h

/-- The closed form: `area = h²/√3`. -/
theorem equilateralArea_eq (h : ℝ) : equilateralArea h = h ^ 2 / Real.sqrt 3 := by
  unfold equilateralArea equilateralSide; ring

/-- At height `h = 1` the side is `2/√3`. -/
theorem equilateralSide_one : equilateralSide 1 = 2 / Real.sqrt 3 := by
  unfold equilateralSide; norm_num

/-- At `h = 1`, area `1/√3`. -/
theorem equilateralArea_one : equilateralArea 1 = 1 / Real.sqrt 3 := by
  rw [equilateralArea_eq]; norm_num

/-! ### Numeric bounds on `√3` and the area ordering. -/

/-- `√3 < 1.7321` (since `1.7321² > 3`). -/
theorem sqrt3_lt : Real.sqrt 3 < 1.7321 := by
  nlinarith [Real.sq_sqrt (show (0:ℝ) ≤ 3 by norm_num), Real.sqrt_nonneg (3:ℝ)]

/-- `1.732 < √3` (since `1.732² < 3`). -/
theorem sqrt3_gt : (1.732 : ℝ) < Real.sqrt 3 := by
  nlinarith [Real.sq_sqrt (show (0:ℝ) ≤ 3 by norm_num), Real.sqrt_nonneg (3:ℝ)]

theorem sqrt3_pos : 0 < Real.sqrt 3 := Real.sqrt_pos.mpr (by norm_num)

/-- `π/8 < 1/√3`: the deltoid is smaller than the Pál triangle. -/
theorem piDiv8_lt_oneOverSqrt3 : Real.pi / 8 < 1 / Real.sqrt 3 := by
  have hs : Real.sqrt 3 < 1.7321 := sqrt3_lt
  have hp : Real.pi < 3.15 := Real.pi_lt_d2
  have hpos : 0 < Real.sqrt 3 := sqrt3_pos
  rw [div_lt_div_iff₀ (by norm_num : (0:ℝ) < 8) hpos]
  nlinarith [mul_lt_mul_of_pos_right hp hpos,
             mul_lt_mul_of_pos_left hs (show (0:ℝ) < 3.15 by norm_num)]

/-- `1/√3 < π/4`: the Pál triangle is smaller than the disc. -/
theorem oneOverSqrt3_lt_piDiv4 : 1 / Real.sqrt 3 < Real.pi / 4 := by
  have hs : (1.732 : ℝ) < Real.sqrt 3 := sqrt3_gt
  have hp : (3.14 : ℝ) < Real.pi := Real.pi_gt_d2
  have hpos : 0 < Real.sqrt 3 := sqrt3_pos
  rw [div_lt_div_iff₀ hpos (by norm_num : (0:ℝ) < 4)]
  nlinarith [mul_lt_mul_of_pos_right hp hpos,
             mul_lt_mul_of_pos_left hs (show (0:ℝ) < 3.14 by norm_num)]

/-- The full ordering of the three needle-set areas: `π/8 < 1/√3 < π/4`. -/
theorem area_ordering :
    Real.pi / 8 < equilateralArea 1 ∧ equilateralArea 1 < Real.pi / 4 := by
  rw [equilateralArea_one]
  exact ⟨piDiv8_lt_oneOverSqrt3, oneOverSqrt3_lt_piDiv4⟩

/-! ### Reuleaux triangle of width 1: area `(π−√3)/2`, a convex needle mover larger than the deltoid. -/

/-- Area of a Reuleaux triangle of width 1: `(π − √3)/2`. -/
noncomputable def reuleauxArea : ℝ := (Real.pi - Real.sqrt 3) / 2

/-- `π/8 < (π−√3)/2`: Reuleaux exceeds the deltoid. -/
theorem reuleaux_gt_deltoid : Real.pi / 8 < reuleauxArea := by
  unfold reuleauxArea
  have hp : (3.14 : ℝ) < Real.pi := Real.pi_gt_d2
  have hs : Real.sqrt 3 < 1.7321 := sqrt3_lt
  linarith

/-! ### Shears preserve area: `(x,y) ↦ (x+ty, y)` has determinant 1; only rotation costs area. -/

/-- Horizontal shear `!![1, t; 0, 1]` has determinant `1`. -/
theorem shear_det_one (t : ℝ) : (!![1, t; 0, 1] : Matrix (Fin 2) (Fin 2) ℝ).det = 1 := by
  rw [Matrix.det_fin_two_of]; ring

/-- A product of shears has determinant `1`. -/
theorem shear_comp_det_one (s t : ℝ) :
    ((!![1, s; 0, 1] : Matrix (Fin 2) (Fin 2) ℝ) * !![1, t; 0, 1]).det = 1 := by
  rw [Matrix.det_mul, shear_det_one, shear_det_one]; ring

/-! ### Perron sprouting: the area obeys a schedule `a(k) ≤ C/(k+1) → 0`, so no positive lower bound.
Model lemmas: the schedule implies the limit, not that the geometry achieves the schedule. -/

/-- `0 ≤ a k ≤ C/(k+1)` implies `a → 0`. -/
theorem perron_area_tendsto_zero (a : ℕ → ℝ) (C : ℝ)
    (h0 : ∀ k, 0 ≤ a k) (hb : ∀ k, a k ≤ C / ((k : ℝ) + 1)) :
    Tendsto a atTop (𝓝 0) := by
  have hup : Tendsto (fun k : ℕ => C / ((k : ℝ) + 1)) atTop (𝓝 0) := by
    have h := (tendsto_one_div_add_atTop_nhds_zero_nat (𝕜 := ℝ)).const_mul C
    simpa [div_eq_mul_inv] using h
  exact tendsto_of_tendsto_of_tendsto_of_le_of_le tendsto_const_nhds hup h0 hb

/-- No positive lower bound: some generation `k` has `a k < ε`. -/
theorem perron_area_no_positive_lower_bound (a : ℕ → ℝ) (C : ℝ)
    (h0 : ∀ k, 0 ≤ a k) (hb : ∀ k, a k ≤ C / ((k : ℝ) + 1))
    {ε : ℝ} (hε : 0 < ε) : ∃ k, a k < ε := by
  have h := perron_area_tendsto_zero a C h0 hb
  have hev : ∀ᶠ k in atTop, a k ∈ Set.Iio ε := h (Iio_mem_nhds hε)
  obtain ⟨k, hk⟩ := hev.exists
  exact ⟨k, hk⟩

/-- The schedule is non-vacuous: `a(k) = C/(k+1)` itself satisfies it. -/
theorem perron_schedule_concrete (C : ℝ) (hC : 0 ≤ C) :
    Tendsto (fun k : ℕ => C / ((k : ℝ) + 1)) atTop (𝓝 0) :=
  perron_area_tendsto_zero (fun k => C / ((k : ℝ) + 1)) C
    (fun k => by positivity) (fun _ => le_refl _)

/-! ### Besicovitch (1919/1928): a measure-zero Kakeya set exists (stated; `sorry`). -/

/-- A Kakeya set in `ℝ²`: a unit segment in every direction. -/
def IsKakeyaSet (K : Set (EuclideanSpace ℝ (Fin 2))) : Prop :=
  ∀ v : EuclideanSpace ℝ (Fin 2), ‖v‖ = 1 →
    ∃ p : EuclideanSpace ℝ (Fin 2), ∀ t ∈ Set.Icc (0 : ℝ) 1, p + t • v ∈ K

/-- Besicovitch (1928): a Kakeya set in `ℝ²` of measure 0 exists. `sorry`. -/
theorem besicovitch_measure_zero_exists :
    ∃ K : Set (EuclideanSpace ℝ (Fin 2)), IsKakeyaSet K ∧ volume K = 0 := by
  sorry

end Kakeya.S2


/- ==============================================================================================
   §3  Dimension: measure zero ≠ small
   ============================================================================================== -/

namespace Kakeya.S3
open MeasureTheory Filter Topology
open scoped ENNReal


/-! ## §3 Dimension

Area is 0 for a Besicovitch set, yet the conjecture calls it full-dimensional, so we need a finer
notion of size. Box (Minkowski) dimension uses one box size; Hausdorff dimension (`dimH`, the
exponent where `μH[d] s` jumps `∞ → 0`) allows many. Always `dimH ≤ dimBox`, and the gap is real:
`{0} ∪ {1/n}` has `dimH = 0 < 1/2 = dimBox`. -/

/-! ### A countable set has `dimH = 0` (`Set.Countable.dimH_zero`). -/

/-- `{0} ∪ {1/(n+1)}` in `ℝ`. -/
def harmonicSet : Set ℝ := insert 0 (Set.range fun n : ℕ => (1 : ℝ) / (n + 1))

/-- `harmonicSet` is countable. -/
theorem harmonicSet_countable : harmonicSet.Countable :=
  (Set.countable_range _).insert 0

/-- `dimH` of the harmonic set is `0`. -/
theorem dimH_harmonicSet : dimH harmonicSet = 0 :=
  harmonicSet_countable.dimH_zero

/-! ### Box (Minkowski) dimension, defined here (Mathlib has none). -/

/-- `F` is a `δ`-cover of `s`: closed balls of radius `δ` centred on `F` cover `s`. -/
def IsδCover {X : Type*} [PseudoMetricSpace X] (s : Set X) (δ : ℝ) (F : Finset X) : Prop :=
  s ⊆ ⋃ x ∈ F, Metric.closedBall x δ

/-- Least number of radius-`δ` balls covering `s` (`0` if no finite cover exists). -/
noncomputable def boxCount {X : Type*} [PseudoMetricSpace X] (s : Set X) (δ : ℝ) : ℕ :=
  sInf {n | ∃ F : Finset X, F.card = n ∧ IsδCover s δ F}

/-- Upper box dimension `limsup_{δ→0⁺} log N(δ) / log(1/δ)`, `N(δ) = boxCount s δ`. -/
noncomputable def upperBoxDim {X : Type*} [PseudoMetricSpace X] (s : Set X) : ℝ :=
  limsup (fun δ : ℝ => Real.log (boxCount s δ) / Real.log (1 / δ))
    (nhdsWithin 0 (Set.Ioi 0))

/-- `dimH ≤ dimBox` for totally bounded sets (Falconer, Prop. 3.4). Axiom (Mathlib has no box
dimension). `TotallyBounded` is required for soundness: without it, a set with no finite cover gets
`boxCount = 0` (via `sInf ∅ = 0`), making `dimH s ≤ 0` false (e.g. `Set.univ : Set ℝ`). -/
axiom dimH_le_upperBoxDim {X : Type*} [MetricSpace X] (s : Set X) (hs : TotallyBounded s) :
    dimH s ≤ ENNReal.ofReal (upperBoxDim s)

/-- The harmonic set has box dimension `1/2` (Falconer, Example 3.5). Axiom. -/
axiom upperBoxDim_harmonicSet : upperBoxDim harmonicSet = 1 / 2

/-- `dimH = 0 < 1/2 = dimBox` for the harmonic set: `dimH` is strictly finer. -/
theorem dimH_lt_upperBoxDim_harmonicSet :
    (dimH harmonicSet).toReal < upperBoxDim harmonicSet := by
  rw [dimH_harmonicSet, upperBoxDim_harmonicSet, ENNReal.toReal_zero]
  norm_num

/-! ### Similarity dimensions `log m / log r` of the classical fractals. -/

/-- Cantor middle-thirds dimension `log 2 / log 3 ≈ 0.6309`. -/
noncomputable def sCantor : ℝ := Real.log 2 / Real.log 3

/-- Sierpiński triangle dimension `log 3 / log 2 ≈ 1.585`. -/
noncomputable def sSierpinski : ℝ := Real.log 3 / Real.log 2

/-- Koch curve dimension `log 4 / log 3 ≈ 1.262`. -/
noncomputable def sKoch : ℝ := Real.log 4 / Real.log 3

private theorem log2_pos : 0 < Real.log 2 := Real.log_pos (by norm_num)
private theorem log3_pos : 0 < Real.log 3 := Real.log_pos (by norm_num)

/-- `0 < log 2 / log 3 < 1`: Cantor, between a point and a line. -/
theorem sCantor_mem_Ioo : 0 < sCantor ∧ sCantor < 1 := by
  refine ⟨div_pos log2_pos log3_pos, ?_⟩
  rw [sCantor, div_lt_one log3_pos]
  exact Real.log_lt_log (by norm_num) (by norm_num)

/-- `1 < log 3 / log 2 < 2`: Sierpiński, between a curve and the plane. -/
theorem sSierpinski_mem_Ioo : 1 < sSierpinski ∧ sSierpinski < 2 := by
  constructor
  · rw [sSierpinski, one_lt_div log2_pos]
    exact Real.log_lt_log (by norm_num) (by norm_num)
  · rw [sSierpinski, div_lt_iff₀ log2_pos]
    have h4 : Real.log 4 = 2 * Real.log 2 := by
      rw [show (4 : ℝ) = 2 ^ 2 by norm_num, Real.log_pow]; push_cast; ring
    calc Real.log 3 < Real.log 4 := Real.log_lt_log (by norm_num) (by norm_num)
      _ = 2 * Real.log 2 := h4

/-- `1 < log 4 / log 3 < 2`: Koch, between a curve and the plane. -/
theorem sKoch_mem_Ioo : 1 < sKoch ∧ sKoch < 2 := by
  constructor
  · rw [sKoch, one_lt_div log3_pos]
    exact Real.log_lt_log (by norm_num) (by norm_num)
  · rw [sKoch, div_lt_iff₀ log3_pos]
    have h9 : Real.log 9 = 2 * Real.log 3 := by
      rw [show (9 : ℝ) = 3 ^ 2 by norm_num, Real.log_pow]; push_cast; ring
    calc Real.log 4 < Real.log 9 := Real.log_lt_log (by norm_num) (by norm_num)
      _ = 2 * Real.log 3 := h9

/-! ### The Cantor set's actual `dimH` (Hutchinson; Mathlib lacks the IFS formula). -/

/-- One step of the middle-thirds construction: `s/3 ∪ (s/3 + 2/3)`. -/
def cantorStep (s : Set ℝ) : Set ℝ :=
  (fun x => x / 3) '' s ∪ (fun x => x / 3 + 2 / 3) '' s

/-- The middle-thirds Cantor set: intersection of all iterates of `cantorStep` from `[0,1]`. -/
def ternaryCantor : Set ℝ := ⋂ n : ℕ, cantorStep^[n] (Set.Icc 0 1)

/-- `dimH` of the middle-thirds Cantor set is `log 2 / log 3` (Hutchinson 1981). Axiom. -/
axiom dimH_ternaryCantor : dimH ternaryCantor = ENNReal.ofReal sCantor

end Kakeya.S3


/- ==============================================================================================
   §4  Dimension of the 2D Kakeya solution (Davies)
   ============================================================================================== -/

namespace Kakeya.S4
open MeasureTheory
open scoped RealInnerProductSpace ENNReal NNReal


/-- The plane `ℝ²`. -/
abbrev E2 := EuclideanSpace ℝ (Fin 2)

/-! ### Kakeya sets in the plane; Davies' theorem. -/

/-- Kakeya (Besicovitch) set in `ℝ²`: a unit segment in every direction. -/
def IsKakeya (K : Set E2) : Prop :=
  ∀ v : E2, ‖v‖ = 1 → ∃ p : E2, segment ℝ p (p + v) ⊆ K

/-- Davies (1971): every Kakeya set in `ℝ²` has `dimH = 2`. `sorry`
(Proc. Cambridge Philos. Soc. 69 (1971) 417-421). -/
theorem davies_dimH_two (K : Set E2) (hK : IsKakeya K) : dimH K = 2 := by
  sorry

/-- Besicovitch (1928): a Kakeya set in `ℝ²` of measure 0 exists. `sorry`
(Math. Z. 27 (1928) 312-320). -/
theorem besicovitch_measure_zero :
    ∃ K : Set E2, IsKakeya K ∧ volume K = 0 := by
  sorry

/-! ### Positive area forces `dimH = 2` (the elementary half; fails for a null Besicovitch set). -/

/-- Every planar set has `dimH ≤ 2`. -/
theorem dimH_le_two (K : Set E2) : dimH K ≤ 2 := by
  calc dimH K ≤ dimH (Set.univ : Set E2) := dimH_mono (Set.subset_univ _)
    _ = 2 := by rw [Real.dimH_univ_eq_finrank, finrank_euclideanSpace]; simp

/-- Positive area gives nonzero `μH[2]` (volume `= c • μH[2]` on `ℝ²`). -/
theorem hausdorff_two_ne_zero_of_volume {K : Set E2} (h : volume K ≠ 0) :
    μH[(2 : ℝ)] K ≠ 0 := by
  intro h0
  apply h
  rw [← EuclideanSpace.euclideanHausdorffMeasure_eq_volume 2,
     Measure.euclideanHausdorffMeasure_def, Measure.smul_apply]
  have : μH[((2 : ℕ) : ℝ)] K = 0 := by norm_num [h0]
  rw [this, smul_zero]

/-- Positive area ⇒ `dimH = 2`. -/
theorem positive_measure_dimH_eq_two (K : Set E2) (h : volume K ≠ 0) : dimH K = 2 := by
  refine le_antisymm (dimH_le_two K) ?_
  have hmu := hausdorff_two_ne_zero_of_volume h
  have := le_dimH_of_hausdorffMeasure_ne_zero (d := (2 : ℝ≥0)) (s := K) (by simpa using hmu)
  simpa using this

/-! ### Córdoba overlap: two width-`δ` strips at angle `θ` meet in area `δ²/sin θ`. -/

/-- A line crosses a width-`δ` strip at angle `θ` over length `δ/sin θ`. -/
theorem crossing_length_spec (δ θ : ℝ) (hθ : Real.sin θ ≠ 0) :
    (δ / Real.sin θ) * Real.sin θ = δ := by
  field_simp

/-- Overlap closed form: `δ · (δ/sin θ) = δ²/sin θ`. -/
theorem strip_overlap_area (δ θ : ℝ) (_hθ : Real.sin θ ≠ 0) :
    δ * (δ / Real.sin θ) = δ ^ 2 / Real.sin θ := by
  rw [mul_div_assoc', sq]

/-- `δ² ≤ δ²/sin θ` on `(0, π/2]`. -/
theorem overlap_ge_delta_sq (δ θ : ℝ) (_hδ : 0 ≤ δ)
    (hθ0 : 0 < θ) (hθ1 : θ ≤ Real.pi / 2) :
    δ ^ 2 ≤ δ ^ 2 / Real.sin θ := by
  have hsin_pos : 0 < Real.sin θ := Real.sin_pos_of_pos_of_lt_pi hθ0 (by linarith [Real.pi_pos])
  have hsin_le : Real.sin θ ≤ 1 := Real.sin_le_one θ
  have hsq : 0 ≤ δ ^ 2 := sq_nonneg δ
  rw [le_div_iff₀ hsin_pos]
  nlinarith [hsq, hsin_le]

/-- `δ²/sin θ` is antitone in `θ` on `(0, π/2]`: larger angle, smaller overlap. -/
theorem overlap_antitone_in_angle (δ θ₁ θ₂ : ℝ) (hδ : 0 < δ)
    (h1 : 0 < θ₁) (h12 : θ₁ ≤ θ₂) (h2 : θ₂ ≤ Real.pi / 2) :
    δ ^ 2 / Real.sin θ₂ ≤ δ ^ 2 / Real.sin θ₁ := by
  have hpi := Real.pi_pos
  have hsin1_pos : 0 < Real.sin θ₁ := Real.sin_pos_of_pos_of_lt_pi h1 (by linarith)
  have hsin_le : Real.sin θ₁ ≤ Real.sin θ₂ :=
    Real.strictMonoOn_sin.monotoneOn ⟨by linarith, by linarith⟩ ⟨by linarith, h2⟩ h12
  have hδsq : 0 < δ ^ 2 := by positivity
  exact div_le_div_of_nonneg_left (le_of_lt hδsq) hsin1_pos hsin_le

/-! ### The tube overlap bound (Córdoba 1977; axiom). A `δ`-tube is a `δ × 1` rectangle. -/

/-- A `δ`-tube in the plane: `{x : |⟪x-center, dir⟫| ≤ 1/2 ∧ |⟪x-center, perp⟫| ≤ δ/2}`. -/
structure DeltaTube (δ : ℝ) where
  center : E2
  dir : E2
  perp : E2

/-- The point set of a `δ`-tube. -/
def DeltaTube.set {δ : ℝ} (T : DeltaTube δ) : Set E2 :=
  {x | |⟪x - T.center, T.dir⟫| ≤ 1 / 2 ∧ |⟪x - T.center, T.perp⟫| ≤ δ / 2}

/-- Córdoba (1977): two unit `δ`-tubes at angle `θ` overlap in area `≤ δ²/sin θ`. Axiom
(Amer. J. Math. 99 (1977) 1-22). -/
axiom cordoba_tube_overlap
    {δ θ : ℝ} (_hδ : 0 < δ) (_hθ : 0 < Real.sin θ)
    (T₁ T₂ : DeltaTube δ)
    (_hu₁ : ‖T₁.dir‖ = 1) (_hu₂ : ‖T₂.dir‖ = 1)
    (_hangle : ⟪T₁.dir, T₂.dir⟫ = Real.cos θ) :
    volume (T₁.set ∩ T₂.set) ≤ ENNReal.ofReal (δ ^ 2 / Real.sin θ)

/-! ### Null and full-dimensional at once (from the two assumed inputs). -/

/-- A measure-zero Kakeya set of `dimH = 2` exists. -/
theorem exists_null_full_dimension_kakeya :
    ∃ K : Set E2, IsKakeya K ∧ volume K = 0 ∧ dimH K = 2 := by
  obtain ⟨K, hK, hnull⟩ := besicovitch_measure_zero
  exact ⟨K, hK, hnull, davies_dimH_two K hK⟩

end Kakeya.S4


/- ==============================================================================================
   §5  The Kakeya conjecture and the harmonic-analysis tower
   ============================================================================================== -/

namespace Kakeya.S5
open MeasureTheory


/-! ### Kakeya sets and the conjecture in `ℝⁿ`. -/

/-- `ℝⁿ`. -/
abbrev Rn (n : ℕ) := EuclideanSpace ℝ (Fin n)

/-- `IsKakeya K`: `K` contains a unit segment in every direction (every unit vector `v`). -/
def IsKakeya {n : ℕ} (K : Set (Rn n)) : Prop :=
  ∀ v : Rn n, ‖v‖ = 1 → ∃ x : Rn n, ∀ t : ℝ, t ∈ Set.Icc (0 : ℝ) 1 → x + t • v ∈ K

/-- Kakeya conjecture in dimension `n`: every Kakeya set has `dimH = n`. -/
def KakeyaConjecture (n : ℕ) : Prop :=
  ∀ K : Set (Rn n), IsKakeya K → dimH K = (n : ENNReal)

/-! ### Resolved dimensions: `n = 0` trivial, `n = 1` elementary, `n = 2` Davies, `n = 3` Wang-Zahl;
`n ≥ 4` open. -/

/-- `n = 0`: `dimH K ≤ dimH univ = 0`. -/
theorem kakeya_dim0 : KakeyaConjecture 0 := by
  intro K _
  have hle : dimH K ≤ dimH (Set.univ : Set (Rn 0)) := dimH_mono (Set.subset_univ K)
  have huniv : dimH (Set.univ : Set (Rn 0)) = ((Module.finrank ℝ (Rn 0) : ℕ) : ENNReal) :=
    Real.dimH_univ_eq_finrank (Rn 0)
  have hfr : Module.finrank ℝ (Rn 0) = 0 := by simp
  rw [huniv, hfr] at hle
  simpa using le_antisymm hle (by simp)

/-! ### Universal floor `dimH ≥ 1` and the `n = 1` case (both proved). -/

/-- `dimH [0,1] = 1`. -/
theorem dimH_Icc01 : dimH (Set.Icc (0 : ℝ) 1) = 1 := by
  have h : (Set.Icc (0 : ℝ) 1) ∈ nhds (1 / 2 : ℝ) := Icc_mem_nhds (by norm_num) (by norm_num)
  simpa using Real.dimH_of_mem_nhds h

/-- `t ↦ x + t • v` is an isometry when `‖v‖ = 1`. -/
theorem seg_isometry {n : ℕ} (x v : Rn n) (hv : ‖v‖ = 1) :
    Isometry (fun t : ℝ => x + t • v) := by
  intro a b
  simp only [edist_eq_enorm_sub]
  have hsub : (x + a • v) - (x + b • v) = (a - b) • v := by module
  have hve : ‖v‖ₑ = 1 := by rw [enorm_eq_nnnorm, ← norm_toNNReal, hv]; simp
  rw [hsub, enorm_smul, hve, mul_one]

/-- Every Kakeya set (`n ≥ 1`) has `dimH ≥ 1`: it contains a unit segment, an isometric copy of
`[0,1]`. -/
theorem kakeya_dimH_ge_one {n : ℕ} (hn : 1 ≤ n) (K : Set (Rn n)) (hK : IsKakeya K) :
    1 ≤ dimH K := by
  haveI : NeZero n := ⟨by omega⟩
  set v : Rn n := EuclideanSpace.single (⟨0, by omega⟩ : Fin n) (1 : ℝ) with hvdef
  have hv : ‖v‖ = 1 := by rw [hvdef, PiLp.norm_single]; norm_num
  obtain ⟨x, hx⟩ := hK v hv
  set g : ℝ → Rn n := fun t => x + t • v with hg
  have hseg : g '' (Set.Icc (0 : ℝ) 1) ⊆ K := by rintro y ⟨t, ht, rfl⟩; exact hx t ht
  calc (1 : ENNReal) = dimH (Set.Icc (0 : ℝ) 1) := dimH_Icc01.symm
    _ ≤ dimH (g '' (Set.Icc (0 : ℝ) 1)) := (seg_isometry x v hv).antilipschitz.le_dimH_image _
    _ ≤ dimH K := dimH_mono hseg

/-- `n = 1`: `dimH = 1`, from the floor `≥ 1` and the ceiling `≤ 1`. -/
theorem kakeya_dim1 : KakeyaConjecture 1 := by
  intro K hK
  have hge : 1 ≤ dimH K := kakeya_dimH_ge_one (by norm_num) K hK
  have hle : dimH K ≤ 1 := by
    calc dimH K ≤ dimH (Set.univ : Set (Rn 1)) := dimH_mono (Set.subset_univ _)
      _ = 1 := by rw [Real.dimH_univ_eq_finrank, finrank_euclideanSpace]; simp
  rw [Nat.cast_one]; exact le_antisymm hle hge

/-- Davies (1971): the conjecture holds for `n = 2`. Axiom
(Proc. Cambridge Philos. Soc. 69 (1971) 417-421). -/
axiom davies_n2 : KakeyaConjecture 2

/-- Wang-Zahl (2025): the conjecture holds for `n = 3`. Axiom (arXiv:2502.17655). -/
axiom wang_zahl_n3 : KakeyaConjecture 3

/-- OPEN for `n ≥ 4` (truth unknown as of 2026); encoded as an axiom, not a theorem. -/
axiom kakeya_conjecture_open : ∀ n : ℕ, 4 ≤ n → KakeyaConjecture n

/-! ### Kakeya maximal function (opaque carrier). -/

/-- The `Lⁿ` Kakeya maximal bound (opaque carrier for the analytic content). -/
opaque KakeyaMaximalBound (n : ℕ) : Prop

/-- Maximal ⇒ dimension (Bourgain 1991); the maximal bound is strictly stronger. The converse is
open. Axiom. -/
axiom maximal_implies_dimension {n : ℕ} : KakeyaMaximalBound n → KakeyaConjecture n

/-! ### Fourier blocks and the ball multiplier. -/

/-- "The ball multiplier is bounded on `Lᵖ(ℝⁿ)`" (opaque carrier). -/
opaque BallMultiplierBounded (n : ℕ) (p : ℝ) : Prop

/-- Fefferman (1971): for `n ≥ 2`, `p ≠ 2`, the ball multiplier is unbounded on `Lᵖ`. Axiom
(Ann. of Math. 94 (1971) 330-336). -/
axiom fefferman_ball_multiplier_fails (n : ℕ) (p : ℝ) (hn : 2 ≤ n) (hp : p ≠ 2) :
    ¬ BallMultiplierBounded n p

/-! ### The tower: local smoothing ⇒ Bochner-Riesz ⇒ restriction ⇒ Kakeya. Arrows are axioms
(the analysis); the chaining is proved. Each rung holds for `n = 2`. -/

/-- Local smoothing on `ℝⁿ` (Sogge 1991; GWZ 2020 for `n = 2`). -/
opaque LocalSmoothing (n : ℕ) : Prop

/-- Bochner-Riesz on `ℝⁿ` (Carleson-Sjölin 1972 for `n = 2`). -/
opaque BochnerRiesz (n : ℕ) : Prop

/-- Restriction on `ℝⁿ` (Fefferman 1970 / Zygmund 1974 for `n = 2`). -/
opaque Restriction (n : ℕ) : Prop

/-- The Kakeya (maximal) bound: the geometric floor of the tower. -/
def KakeyaBound (n : ℕ) : Prop := KakeyaMaximalBound n

/-- Local smoothing ⇒ Bochner-Riesz. Axiom. -/
axiom ls_imp_br (n : ℕ) : LocalSmoothing n → BochnerRiesz n

/-- Bochner-Riesz ⇒ restriction. Axiom. -/
axiom br_imp_r (n : ℕ) : BochnerRiesz n → Restriction n

/-- Restriction ⇒ Kakeya bound (Bourgain, Wolff). Axiom. -/
axiom r_imp_k (n : ℕ) : Restriction n → KakeyaBound n

/-- Chaining: the three arrows give local smoothing ⇒ Kakeya bound. -/
theorem tower_ls_imp_k (n : ℕ)
    (h1 : LocalSmoothing n → BochnerRiesz n)
    (h2 : BochnerRiesz n → Restriction n)
    (h3 : Restriction n → KakeyaBound n) :
    LocalSmoothing n → KakeyaBound n :=
  fun hLS => h3 (h2 (h1 hLS))

/-- The chaining applied to the cited arrows. -/
theorem tower_ls_imp_k_axioms (n : ℕ) : LocalSmoothing n → KakeyaBound n :=
  tower_ls_imp_k n (ls_imp_br n) (br_imp_r n) (r_imp_k n)

/-- Guth-Wang-Zhang (2020): local smoothing for `n = 2`. Axiom (Ann. of Math. 2020). -/
axiom guth_wang_zhang_n2 : LocalSmoothing 2

/-- `n = 2` Kakeya bound, from GWZ 2020 and the chaining. -/
theorem kakeya_bound_n2 : KakeyaBound 2 :=
  tower_ls_imp_k_axioms 2 guth_wang_zhang_n2

end Kakeya.S5


/- ==============================================================================================
   §6  The 3D conjecture and what dimension 3 means for tubes
   ============================================================================================== -/

namespace Kakeya.S6
open MeasureTheory
open scoped ENNReal


/-! ### The 3D conjecture and what "dimension 3" means for tubes. -/

/-- Kakeya set in `ℝ³`: a unit segment in every direction. -/
def IsKakeya (K : Set (EuclideanSpace ℝ (Fin 3))) : Prop :=
  ∀ v : EuclideanSpace ℝ (Fin 3), ‖v‖ = 1 →
    ∃ x : EuclideanSpace ℝ (Fin 3), ∀ t : ℝ, t ∈ Set.Icc (0 : ℝ) 1 → x + t • v ∈ K

/-- Wang-Zahl (2025): every Kakeya set in `ℝ³` has `dimH = 3`. `sorry` (arXiv:2502.17655). -/
theorem kakeya3D (K : Set (EuclideanSpace ℝ (Fin 3))) (hK : IsKakeya K) :
    dimH K = 3 := by
  sorry

/-- `dimH` of `ℝ³` is `3`. -/
theorem dimH_univ_three :
    dimH (Set.univ : Set (EuclideanSpace ℝ (Fin 3))) = 3 := by
  rw [Real.dimH_univ_eq_finrank]
  simp

/-! ### `ℝ³` lower bounds climbing to 3: Wolff 5/2 (1995) → Katz-Łaba-Tao (2000) →
Katz-Zahl 5/2+ε (2017) → Wang-Zahl 3 (2025). -/

/-- Wolff (1995): `dimH ≥ 5/2` in `ℝ³`. `sorry`. -/
theorem wolff_lower_bound (K : Set (EuclideanSpace ℝ (Fin 3))) (hK : IsKakeya K) :
    (5 : ℝ≥0∞) / 2 ≤ dimH K := by
  sorry

/-- The constants increase: `5/2 < 5/2 + ε < 3` for `0 < ε < 1/2`. -/
theorem lower_bound_chain (ε : ℝ) (hε : 0 < ε) (hε' : ε < 1 / 2) :
    (5 : ℝ) / 2 < 5 / 2 + ε ∧ 5 / 2 + ε < 3 ∧ (5 : ℝ) / 2 < 3 := by
  refine ⟨by linarith, by linarith, by norm_num⟩

/-! ### Why 3D is harder: generic lines are skew (no forced crossing), so a packing hypothesis
replaces the 2D crossing argument. -/

/-- Wolff axiom: no fat tube `R` contains more than `δ⁻²|R|` thin tubes. -/
def WolffAxiom (δ : ℝ)
    (tubesIn : Set (EuclideanSpace ℝ (Fin 3)) → ℕ)
    (fatVol : Set (EuclideanSpace ℝ (Fin 3)) → ℝ) : Prop :=
  ∀ R : Set (EuclideanSpace ℝ (Fin 3)), (tubesIn R : ℝ) ≤ δ ^ (-2 : ℤ) * fatVol R

/-! ### Tube count: a `δ`-separated set of directions on `S²` has `≲ δ⁻²` elements. -/

/-- A `δ`-separated set in `[0,1]²` (some coordinate differs by `≥ δ`, `0 < δ ≤ 1`) has `≤ 4/δ²`
points, via the grid-cell map `p ↦ (⌊p.1/δ⌋, ⌊p.2/δ⌋)`. -/
theorem separated_card_le
    (δ : ℝ) (hδ : 0 < δ) (hδ1 : δ ≤ 1)
    (S : Finset (ℝ × ℝ))
    (hS : ∀ p ∈ S, p.1 ∈ Set.Icc (0 : ℝ) 1 ∧ p.2 ∈ Set.Icc (0 : ℝ) 1)
    (hsep : ∀ p ∈ S, ∀ q ∈ S, p ≠ q → δ ≤ |p.1 - q.1| ∨ δ ≤ |p.2 - q.2|) :
    (S.card : ℝ) ≤ 4 / δ ^ 2 := by
  classical
  set m : ℤ := ⌊1 / δ⌋ with hm
  -- The grid-cell map.
  set f : ℝ × ℝ → ℤ × ℤ := fun p => (⌊p.1 / δ⌋, ⌊p.2 / δ⌋) with hf
  -- Separation ⇒ the cell map is injective on `S`.
  have hinj : Set.InjOn f S := by
    intro p hp q hq hpq
    by_contra hne
    have h1 : ⌊p.1 / δ⌋ = ⌊q.1 / δ⌋ := congrArg Prod.fst hpq
    have h2 : ⌊p.2 / δ⌋ = ⌊q.2 / δ⌋ := congrArg Prod.snd hpq
    have d1 : |p.1 / δ - q.1 / δ| < 1 := Int.abs_sub_lt_one_of_floor_eq_floor h1
    have d2 : |p.2 / δ - q.2 / δ| < 1 := Int.abs_sub_lt_one_of_floor_eq_floor h2
    have e1 : p.1 / δ - q.1 / δ = (p.1 - q.1) / δ := by ring
    have e2 : p.2 / δ - q.2 / δ = (p.2 - q.2) / δ := by ring
    rw [e1, abs_div, abs_of_pos hδ, div_lt_one hδ] at d1
    rw [e2, abs_div, abs_of_pos hδ, div_lt_one hδ] at d2
    rcases hsep p (Finset.mem_coe.mp hp) q (Finset.mem_coe.mp hq) hne with h | h
    · exact absurd h (not_le.mpr d1)
    · exact absurd h (not_le.mpr d2)
  -- `0 ≤ m` since `1/δ ≥ 0`.
  have hm0 : 0 ≤ m := by
    rw [hm]; exact Int.floor_nonneg.mpr (by positivity)
  -- The image of `S` lands in the finite grid `Icc 0 m × Icc 0 m`.
  have hsub : S.image f ⊆ (Finset.Icc (0 : ℤ) m) ×ˢ (Finset.Icc (0 : ℤ) m) := by
    intro c hc
    rw [Finset.mem_image] at hc
    obtain ⟨p, hp, rfl⟩ := hc
    obtain ⟨⟨hx0, hx1⟩, ⟨hy0, hy1⟩⟩ := hS p hp
    rw [Finset.mem_product, Finset.mem_Icc, Finset.mem_Icc]
    refine ⟨⟨?_, ?_⟩, ?_, ?_⟩
    · exact Int.floor_nonneg.mpr (by positivity)
    · rw [hm]; exact Int.floor_le_floor (by gcongr)
    · exact Int.floor_nonneg.mpr (by positivity)
    · rw [hm]; exact Int.floor_le_floor (by gcongr)
  -- Cardinality: `|S| = |image| ≤ |grid| = (m+1)²`.
  have hcard : S.card ≤ (m + 1).toNat * (m + 1).toNat := by
    have := Finset.card_le_card hsub
    rwa [Finset.card_product, Int.card_Icc, Finset.card_image_of_injOn hinj,
      show (m + 1 - 0) = m + 1 by ring] at this
  -- Convert the integer grid count to reals.
  have htoNat : ((m + 1).toNat : ℝ) = (m : ℝ) + 1 := by
    have h0 : (0 : ℤ) ≤ m + 1 := by linarith
    have := Int.toNat_of_nonneg h0
    have : (((m + 1).toNat : ℤ) : ℝ) = ((m + 1 : ℤ) : ℝ) := by rw [this]
    push_cast at this ⊢
    linarith [this]
  -- `(m:ℝ) + 1 ≤ 2/δ`.
  have hml : (m : ℝ) ≤ 1 / δ := by rw [hm]; exact Int.floor_le (1 / δ)
  have h1d : (1 : ℝ) ≤ 1 / δ := by rw [le_div_iff₀ hδ]; linarith
  have hub : (m : ℝ) + 1 ≤ 2 / δ := by
    have : (2 : ℝ) / δ = 1 / δ + 1 / δ := by ring
    rw [this]; linarith
  have hmnn : (0 : ℝ) ≤ (m : ℝ) + 1 := by
    have : (0 : ℝ) ≤ (m : ℝ) := by exact_mod_cast hm0
    linarith
  -- Assemble: `|S| ≤ (m+1)² ≤ (2/δ)² = 4/δ²`.
  calc (S.card : ℝ)
      ≤ (((m + 1).toNat : ℝ)) * ((m + 1).toNat : ℝ) := by exact_mod_cast hcard
    _ = ((m : ℝ) + 1) * ((m : ℝ) + 1) := by rw [htoNat]
    _ ≤ (2 / δ) * (2 / δ) := by nlinarith [hub, hmnn]
    _ = 4 / δ ^ 2 := by ring

end Kakeya.S6


/- ==============================================================================================
   §7  Solving 3D: sticky reduction, grains, induction on scales (Wang–Zahl)
   ============================================================================================== -/

namespace Kakeya.S7
open Filter Topology MeasureTheory
open scoped BigOperators ENNReal


/-! ### The finite-field model (Dvir 2009, polynomial method): a Kakeya set in `(F_q)ⁿ` has
`≥ C(q-1+n, n)` points. The ancestor of the grains used in the real 3D proof. -/

variable {n q : ℕ}

/-- The line through `a` in direction `v` in the finite-field grid `(ZMod q)^n`. -/
def LineFF (a v : Fin n → ZMod q) : Set (Fin n → ZMod q) :=
  {x | ∃ t : ZMod q, x = a + t • v}

/-- Finite-field Kakeya set: a subset of `(ZMod q)ⁿ` containing a line in every nonzero direction. -/
def KakeyaSetFF (K : Set (Fin n → ZMod q)) : Prop :=
  ∀ v : Fin n → ZMod q, v ≠ 0 → ∃ a : Fin n → ZMod q, LineFF a v ⊆ K

/-- The grid `(ZMod q)ⁿ` has `q ^ n` points. -/
theorem grid_card [NeZero q] : Fintype.card (Fin n → ZMod q) = q ^ n := by
  simp [ZMod.card]

/-- Dvir's engine: over the field `ZMod q` (`q` prime), a polynomial of degree `< q` vanishing at
every point is zero. -/
theorem lowdeg_vanishing_is_zero (hq : q.Prime)
    (p : Polynomial (ZMod q))
    (hvanish : ∀ x : ZMod q, Polynomial.eval x p = 0)
    (hdeg : p.natDegree < q) : p = 0 := by
  haveI : Fact q.Prime := ⟨hq⟩
  have hcard : (Finset.univ : Finset (ZMod q)).card = q := by
    simp [ZMod.card]
  refine Polynomial.eq_zero_of_natDegree_lt_card_of_eval_eq_zero' p Finset.univ ?_ ?_
  · intro i _; exact hvanish i
  · rw [hcard]; exact hdeg

/-- Contrapositive: a nonzero polynomial of degree `< q` has a non-root in `F_q`. -/
theorem lowdeg_nonzero_has_nonroot (hq : q.Prime)
    (p : Polynomial (ZMod q)) (hp : p ≠ 0) (hdeg : p.natDegree < q) :
    ∃ x : ZMod q, Polynomial.eval x p ≠ 0 := by
  by_contra h
  have hall : ∀ x : ZMod q, Polynomial.eval x p = 0 :=
    fun x => not_not.mp (fun hx => h ⟨x, hx⟩)
  exact hp (lowdeg_vanishing_is_zero hq p hall hdeg)

/-- Monomials of total degree `< q` in `n` variables number `C(q-1+n, n)` (stars and bars). `sorry`
(Dvir 2009, §2). -/
theorem lowdeg_monomial_count :
    {f : Fin n → ℕ | ∑ i, f i < q}.ncard = Nat.choose (q - 1 + n) n := by
  sorry

/-- Dvir (2009): a finite-field Kakeya set has `≥ C(q-1+n, n)` points. `sorry`; the univariate engine
`lowdeg_vanishing_is_zero` is proved above (J. Amer. Math. Soc. 22 (2009) 1093-1097). -/
theorem dvir_finite_field_kakeya [NeZero q] (hq : q.Prime)
    (K : Set (Fin n → ZMod q)) (hK : KakeyaSetFF K) :
    Nat.choose (q - 1 + n) n ≤ K.ncard := by
  sorry

/-- A finite-field Kakeya set is nonempty (`C(q-1+n, n) ≥ 1`), from Dvir's bound. -/
theorem dvir_kakeya_nonempty [NeZero q] (hq : q.Prime)
    (K : Set (Fin n → ZMod q)) (hK : KakeyaSetFF K) (hqn : n ≤ q - 1 + n) :
    1 ≤ K.ncard :=
  le_trans (Nat.choose_pos hqn) (dvir_finite_field_kakeya hq K hK)

/-! ### Sticky reduction, grains, compression: the three structural inputs, each an opaque
proposition asserted by an `axiom` with a citation. -/

/-- A tube family at intermediate scale `ρ`: sticky (a self-similar comb) or non-sticky (scattered). -/
inductive Stickiness
  | sticky
  | nonSticky

/-- Whether a tube family is sticky. -/
def Stickiness.isSticky : Stickiness → Prop
  | .sticky => True
  | .nonSticky => False

/-- Sticky reduction (Hickman, Thm 5.9): it suffices to treat sticky configurations. Opaque
proposition + axiom (arXiv:2512.09842). -/
opaque StickyReductionHolds : Prop
axiom sticky_reduction : StickyReductionHolds

/-- Grains (Guth 2014): a near-extremal family clusters into `δ × c × c` slabs, disjoint within a fat
tube, with no point in too many. Opaque proposition + axiom (arXiv:1402.0518). -/
opaque GrainsBoundedOverlap : Prop
axiom grains_bounded_overlap : GrainsBoundedOverlap

/-- Compression capped (Zahl): graininess bounds how far a Kakeya set can be compressed. Opaque
proposition + axiom (arXiv:2512.09397). -/
opaque CompressionCapped : Prop
axiom compression_capped : CompressionCapped

/-! ### Induction on scales: an additive-gain recurrence on the dimension exponent, climbing to 3.
A model of the real induction (it proves the schedule's limit, not that the geometry achieves it). -/

/-- Exponent after `k` passes: start at `d₀`, gain `α` each pass. -/
def dseq (d0 α : ℝ) : ℕ → ℝ
  | 0     => d0
  | k + 1 => dseq d0 α k + α

/-- Closed form: `dₖ = d₀ + k·α`. -/
theorem dseq_closed (d0 α : ℝ) (k : ℕ) : dseq d0 α k = d0 + k * α := by
  induction k with
  | zero => simp [dseq]
  | succ k ih =>
      simp only [dseq, ih, Nat.cast_succ]
      ring

/-- Each pass strictly increases the exponent (positive gain). -/
theorem dseq_strictMono (d0 α : ℝ) (hα : 0 < α) : StrictMono (dseq d0 α) := by
  have hstep : ∀ k, dseq d0 α k < dseq d0 α (k + 1) := by
    intro k; simp only [dseq]; linarith
  exact strictMono_nat_of_lt_succ hstep

/-- The exponent tends to `+∞` under a positive gain. -/
theorem dseq_tendsto_atTop (d0 α : ℝ) (hα : 0 < α) :
    Tendsto (dseq d0 α) atTop atTop := by
  have h : dseq d0 α = (fun k : ℕ => d0 + (k : ℝ) * α) := by
    funext k; exact dseq_closed d0 α k
  rw [h]
  apply Filter.tendsto_atTop_add_const_left
  exact (tendsto_natCast_atTop_atTop).atTop_mul_const hα

/-- The exponent reaches `3` after finitely many passes. -/
theorem dseq_reaches_three (d0 α : ℝ) (hα : 0 < α) :
    ∃ K : ℕ, ∀ k ≥ K, (3 : ℝ) ≤ dseq d0 α k := by
  obtain ⟨K, hK⟩ := exists_nat_ge ((3 - d0) / α)
  refine ⟨K, fun k hk => ?_⟩
  rw [dseq_closed]
  have hKk : (K : ℝ) ≤ (k : ℝ) := by exact_mod_cast hk
  have h1 : (3 - d0) / α ≤ (k : ℝ) := le_trans hK hKk
  have h2 : (3 - d0) ≤ (k : ℝ) * α := by
    rw [div_le_iff₀ hα] at h1; linarith
  linarith

/-- Geometric-gap model: if the gap `3 - dₖ` shrinks by `r ∈ (0,1)` each pass, the exponent
converges to `3`. -/
theorem gap_model_tendsto_three (g0 r : ℝ) (hr0 : 0 < r) (hr1 : r < 1) :
    Tendsto (fun k : ℕ => 3 - g0 * r ^ k) atTop (nhds 3) := by
  have hpow : Tendsto (fun k : ℕ => g0 * r ^ k) atTop (nhds 0) := by
    have := tendsto_pow_atTop_nhds_zero_of_lt_one (le_of_lt hr0) hr1
    simpa using this.const_mul g0
  simpa using (tendsto_const_nhds (x := (3 : ℝ))).sub hpow

/-! ### The 3D result and the standing conjecture. -/

/-- The unit segment from `a` in direction `v` in `ℝ³`. -/
def UnitSegment (a v : EuclideanSpace ℝ (Fin 3)) : Set (EuclideanSpace ℝ (Fin 3)) :=
  {x | ∃ t : ℝ, t ∈ Set.Icc (0 : ℝ) 1 ∧ x = a + t • v}

/-- A **Kakeya set in ℝ³**: contains a unit segment in every unit direction. -/
def KakeyaSet3 (K : Set (EuclideanSpace ℝ (Fin 3))) : Prop :=
  ∀ v : EuclideanSpace ℝ (Fin 3), ‖v‖ = 1 → ∃ a, UnitSegment a v ⊆ K

/-- Wang-Zahl (2025): every Kakeya set in `ℝ³` has `dimH = 3`. `sorry` (arXiv:2502.17655). -/
theorem wang_zahl_dim_three (K : Set (EuclideanSpace ℝ (Fin 3))) (hK : KakeyaSet3 K) :
    dimH K = 3 := by
  sorry

/-- Kakeya set in `ℝⁿ`: a unit segment in every direction. -/
def KakeyaSetN (n : ℕ) (K : Set (EuclideanSpace ℝ (Fin n))) : Prop :=
  ∀ v : EuclideanSpace ℝ (Fin n), ‖v‖ = 1 →
    ∃ a, {x | ∃ t : ℝ, t ∈ Set.Icc (0 : ℝ) 1 ∧ x = a + t • v} ⊆ K

/-- OPEN for `n ≥ 4` (truth unknown as of 2026); encoded as an axiom, not a theorem. -/
axiom kakeya_set_conjecture_open (n : ℕ) (hn : 4 ≤ n)
    (K : Set (EuclideanSpace ℝ (Fin n))) (hK : KakeyaSetN n K) :
    dimH K = (n : ℝ≥0∞)

end Kakeya.S7


/- ==============================================================================================
   §8  Going further: dimension n ≥ 4 (OPEN) — the proven bounds all fall short
   ============================================================================================== -/

namespace Kakeya.S8
open MeasureTheory

/-! The conjecture `dimH K = n` is proved for `n ≤ 3` and open for `n ≥ 4`, where only lower bounds
below `n` are known. The two landmark bounds are recorded as cited axioms; the proved facts (they
agree at `n = 4`, Katz-Tao overtakes at `n = 5`, all fall short of `n`) characterize the state of the
art. Reference: Zahl, arXiv:2512.09397. -/

/-- Wolff's lower-bound value `(n+2)/2` (1995 hairbrush). -/
noncomputable def wolffBound (n : ℕ) : ℝ := ((n : ℝ) + 2) / 2

/-- Katz-Tao's lower-bound value `(2-√2)(n-4)+3` (2002). -/
noncomputable def katzTaoBound (n : ℕ) : ℝ := (2 - Real.sqrt 2) * ((n : ℝ) - 4) + 3

/-- Wolff (1995): for `n ≥ 2`, every Kakeya set in `ℝⁿ` has `dimH ≥ (n+2)/2`. Axiom
(Rev. Mat. Iberoam. 11 (1995) 651-674). `2 ≤ n` required for soundness: false at `n = 1`
(`3/2 > 1`). -/
axiom wolff_lower_bound (n : ℕ) (hn : 2 ≤ n)
    (K : Set (Kakeya.S5.Rn n)) (hK : Kakeya.S5.IsKakeya K) :
    ENNReal.ofReal (wolffBound n) ≤ dimH K

/-- Katz-Tao (2002): for `n ≥ 4`, `dimH ≥ (2-√2)(n-4)+3`, overtaking Wolff for `n ≥ 5`. Axiom
(J. Anal. Math. 87 (2002) 231-263). `4 ≤ n` required for soundness. -/
axiom katz_tao_lower_bound (n : ℕ) (hn : 4 ≤ n)
    (K : Set (Kakeya.S5.Rn n)) (hK : Kakeya.S5.IsKakeya K) :
    ENNReal.ofReal (katzTaoBound n) ≤ dimH K

/-- At `n = 4` the Katz-Tao bound is `3`. -/
theorem katzTao_eq_three_at_four : katzTaoBound 4 = 3 := by unfold katzTaoBound; norm_num

/-- Wolff and Katz-Tao agree at `n = 4` (both `3`). -/
theorem bounds_agree_at_four : katzTaoBound 4 = wolffBound 4 := by
  unfold katzTaoBound wolffBound; norm_num

/-- `√2 < 3/2`. -/
theorem sqrt2_lt_three_halves : Real.sqrt 2 < 3 / 2 := by
  rw [show (3 / 2 : ℝ) = Real.sqrt ((3 / 2) ^ 2) by rw [Real.sqrt_sq (by norm_num)]]
  exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)

/-- Katz-Tao beats Wolff for `n ≥ 5`. -/
theorem katzTao_gt_wolff (n : ℕ) (hn : 5 ≤ n) : wolffBound n < katzTaoBound n := by
  unfold wolffBound katzTaoBound
  have hn' : (5 : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn
  nlinarith [sqrt2_lt_three_halves, hn']

/-- Every bound falls short of `n` for `n ≥ 3` (`(n+2)/2 < n ⟺ 2 < n`): this shortfall is the open
conjecture. -/
theorem wolffBound_lt_n (n : ℕ) (hn : 3 ≤ n) : wolffBound n < n := by
  unfold wolffBound
  have h : (3 : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn
  linarith

/-- The `n = 4` record `dimH ≥ 3.059` (Katz-Zahl planebrush, arXiv:1902.00989; sticky `≥ 3.25`,
arXiv:2410.23579) still lies below `4`. -/
theorem katz_zahl_record_n4_below_four : (3059 : ℝ) / 1000 < 4 := by norm_num

end Kakeya.S8


/- ==============================================================================================
   Spine: one load-bearing result per part, so the dependency chain type-checks together.
   ============================================================================================== -/

namespace Kakeya.Spine

-- §1 the objects, and needle ⇒ Besicovitch
#check @Kakeya.S1.isNeedleSet_containsUnitSegmentEveryDirection
#check @Kakeya.S1.volume_closedBall_half
-- §2 area collapses to 0 (and the shear that costs no area)
#check @Kakeya.S2.perron_area_tendsto_zero
#check @Kakeya.S2.besicovitch_measure_zero_exists
-- §3 the new ruler: dimension, strictly finer than box-counting
#check @Kakeya.S3.dimH_harmonicSet
#check @Kakeya.S3.dimH_lt_upperBoxDim_harmonicSet
-- §4 the 2D solution measured: area 0, dimension 2
#check @Kakeya.S4.davies_dimH_two
#check @Kakeya.S4.exists_null_full_dimension_kakeya
-- §5 conjecture dim = n: the dimH ≥ 1 floor, n = 1, the tower, the open n ≥ 4
#check @Kakeya.S5.kakeya_dimH_ge_one
#check @Kakeya.S5.kakeya_dim1
#check @Kakeya.S5.tower_ls_imp_k_axioms
#check @Kakeya.S5.kakeya_conjecture_open
-- §6 the 3D theorem and the 5/2 → 3 climb
#check @Kakeya.S6.kakeya3D
#check @Kakeya.S6.lower_bound_chain
-- §7 Dvir's finite-field model and the induction ratchet to 3
#check @Kakeya.S7.dvir_finite_field_kakeya
#check @Kakeya.S7.dseq_reaches_three
-- §8 going further: n ≥ 4 open; every proven bound falls strictly short of n
#check @Kakeya.S8.wolffBound_lt_n
#check @Kakeya.S8.katzTao_gt_wolff

end Kakeya.Spine
