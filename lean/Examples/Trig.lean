/-
Trigonometry theorems taken from `notebooks/007_trigonometry.py`.

The notebook *states and visualizes* these identities. Here Lean *proves* them:
the notebook shows `cos²θ + sin²θ = 1.000000 ≈ 1` for one slider value; Lean
discharges it for every real θ at once, backed by Mathlib's definitions of sin/cos.

Needs Mathlib, so build through Lake:
    lake exe cache get   # once, downloads prebuilt Mathlib
    lake build
-/
import Mathlib

open Real

/-- Notebook Part IV, "The Pythagorean Identity": `sin²θ + cos²θ = 1`.
    This is Mathlib's `Real.sin_sq_add_cos_sq`; we just name it in the notebook's terms. -/
theorem pythagorean_identity (θ : ℝ) : sin θ ^ 2 + cos θ ^ 2 = 1 :=
  Real.sin_sq_add_cos_sq θ

/-- Notebook Part V, angle addition for sine. -/
theorem sin_add' (α β : ℝ) : sin (α + β) = sin α * cos β + cos α * sin β :=
  Real.sin_add α β

/-- Notebook Part V, angle addition for cosine. -/
theorem cos_add' (α β : ℝ) : cos (α + β) = cos α * cos β - sin α * sin β :=
  Real.cos_add α β

/-- Notebook Part V, subtraction version, *derived* from `sin_add` (not quoted).
    Lean checks each rewrite and `ring` closes the algebra. -/
theorem sin_sub' (α β : ℝ) : sin (α - β) = sin α * cos β - cos α * sin β := by
  rw [sub_eq_add_neg, Real.sin_add, Real.cos_neg, Real.sin_neg]
  ring

/-- Double-angle for sine, derived from angle addition: `sin 2α = 2 sinα cosα`. -/
theorem sin_two_mul' (α : ℝ) : sin (2 * α) = 2 * sin α * cos α := by
  rw [two_mul, Real.sin_add]
  ring
