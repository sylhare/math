/-
Basics: simple statements Lean checks with no external library.

Compile this file on its own (no Mathlib needed):
    lean Examples/Basics.lean
Silence = every statement below is a machine-checked proof. Break one
(change `4` to `5`) and Lean reports the exact goal it could not close.
-/

-- 1. Arithmetic. `rfl` = "both sides reduce to the same value".
example : 2 + 2 = 4 := rfl

-- 2. A false statement does NOT compile. Uncomment to see the error:
-- example : 2 + 2 = 5 := rfl

-- 3. Algebra over the naturals, proved by a decision procedure.
example (n : Nat) : n + 0 = n := by simp

-- 4. A named theorem with a real proof (induction on n).
theorem add_comm_nat (m n : Nat) : m + n = n + m := by
  induction n with
  | zero => simp
  | succ k ih => rw [Nat.add_succ, ih, Nat.succ_add]

-- 5. Logic: the statement is the type, the proof is a term inhabiting it.
theorem modus_ponens (P Q : Prop) (hpq : P → Q) (hp : P) : Q := hpq hp

-- 6. Existence: to prove "there is an n with n > 3" you must supply one.
example : ∃ n : Nat, n > 3 := ⟨4, by decide⟩
