# Lean for formula validation

A sandbox for checking math with the [Lean](https://lean-lang.org) proof assistant.
A LaTeX formula only looks right; Lean checks it against definitions and either accepts
the proof or points at the hole. Self-contained: nothing here touches `../notebooks`.

- `Examples/Basics.lean` — arithmetic, algebra, induction, logic. No library.
- `Examples/Trig.lean` — the Pythagorean identity and angle-addition formulas from
  `notebooks/007_trigonometry.py`, proved against [Mathlib](https://leanprover-community.github.io/).
- `bridge/lean_check.py` — runs a Lean snippet, returns pass/fail. The link to Python.
- `demo/notebook_lean_demo.py` — a marimo notebook where each formula renders as LaTeX **and**
  gets validated by Lean live.

## Install

Lean is managed by `elan` (like `rustup`). One command installs everything:

```bash
curl https://elan.lean-lang.org/elan-init.sh -sSf | sh -s -- -y
source ~/.elan/env          # or restart your shell
```

`lean-toolchain` pins Lean `v4.32.2`; `elan` fetches it automatically on first use.

## Build

`Basics.lean` needs no library, so `lean` checks it directly. Silence means it passed:

```bash
lean Examples/Basics.lean          # exit 0 = every statement proved
```

`Trig.lean` uses Mathlib. Download the prebuilt cache once (~2 GB), then build:

```bash
lake exe cache get                 # prebuilt Mathlib .olean files, skips a long compile
lake build                         # compiles Examples/, verifies every theorem
```

To see a failure, change `4` to `5` in `Basics.lean` and rerun: Lean reports the exact
goal it could not close.

## The Python bridge and notebook

The bridge compiles a snippet and reports the result:

```bash
uv run python bridge/lean_check.py     # self-test: verified / error / verified
```

The notebook pairs rendered LaTeX with a live Lean badge (green = verified, red = rejected):

```bash
uv run marimo edit lean/demo/notebook_lean_demo.py     # from the repo root
```

The first check per session starts the toolchain (~2 s); Mathlib snippets import one module
rather than all of Mathlib, so they stay fast.

## How LaTeX and Lean line up

Same claim, two forms. The LaTeX is for the reader; the Lean is for the machine:

| LaTeX (rendered)                  | Lean (checked)                                       |
| --------------------------------- | ---------------------------------------------------- |
| `\sin^2\theta + \cos^2\theta = 1` | `example (θ : ℝ) : sin θ ^ 2 + cos θ ^ 2 = 1 := ...` |
| `2 + 2 = 4`                       | `example : 2 + 2 = 4 := rfl`                         |

There is no automatic LaTeX-to-Lean translation: you write both, and the bridge guarantees
the Lean side actually holds. Mathlib names for common results are searchable via
[Loogle](https://loogle.lean-lang.org) and [Moogle](https://www.moogle.ai).

## Docs

- Lean manual — https://lean-lang.org/documentation/
- Theorem Proving in Lean 4 (the book) — https://leanprover.github.io/theorem_proving_in_lean4/
- Mathematics in Lean (tutorial) — https://leanprover-community.github.io/mathematics_in_lean/
- Mathlib docs (search lemmas) — https://leanprover-community.github.io/mathlib4_docs/
- Natural Number Game (learn by playing) — https://adam.math.hhu.de/#/g/leanprover-community/nng4
