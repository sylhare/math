"""
Live math, validated by Lean.

Each statement below is shown twice: rendered as LaTeX (what a reader sees) and
sent to Lean as a proof (what a machine checks). The green badge means Lean
accepted the proof; red means it found a hole. Nothing here is wired to the
notebooks under `../notebooks` - this file stands alone.

Run:  uv run marimo run lean/demo/notebook_lean_demo.py
Edit: uv run marimo edit lean/demo/notebook_lean_demo.py
"""

import marimo

__generated_with = "0.19.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import sys
    from pathlib import Path

    import marimo as mo

    # Make the bridge importable without installing anything (bridge is one level up).
    sys.path.insert(0, str(Path(__file__).parent.parent / "bridge"))
    from lean_check import check

    return check, mo


@app.cell
def _(check, mo):
    def verified(latex: str, snippet: str):
        """Render a claim as LaTeX and a Lean badge reporting whether it holds."""
        result = check(snippet)
        if result.ok and not result.has_sorry:
            kind, label = "success", "verified by Lean"
        elif result.has_sorry:
            kind, label = "warn", "compiles, but a proof is stubbed with `sorry`"
        else:
            kind, label = "danger", "Lean rejected this"
        parts = [
            mo.md(rf"$$ {latex} $$"),
            mo.md(f"```lean\n{snippet}\n```"),
            mo.callout(mo.md(f"**{label}** &middot; {result.seconds:.1f}s"), kind=kind),
        ]
        if not result.ok:
            parts.append(mo.md(f"Lean says:\n```\n{result.output}\n```"))
        return mo.vstack(parts)

    return (verified,)


@app.cell
def _(mo):
    mo.md(
        r"""
        # Live math, validated by Lean

        A LaTeX formula only *looks* right. Below, each formula is also handed to the
        Lean proof assistant, which checks it against its definitions and reports back.
        The first time a cell runs it starts the Lean toolchain, so give it a moment.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"## Simple statements (no library needed)")
    return


@app.cell
def _(verified):
    verified(r"2 + 2 = 4", "example : 2 + 2 = 4 := rfl")
    return


@app.cell
def _(verified):
    # `decide` runs a decision procedure; Lean confirms the inequality.
    verified(r"\exists\, n \in \mathbb{N},\; n > 3", "example : ∃ n : Nat, n > 3 := ⟨4, by decide⟩")
    return


@app.cell
def _(verified):
    # A false claim: Lean cannot close the goal, so the badge turns red.
    verified(r"2 + 2 = 5", "example : 2 + 2 = 5 := rfl")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## A theorem from `notebooks/007_trigonometry.py`

        Part IV of the trigonometry notebook states the Pythagorean identity and shows
        `cos²θ + sin²θ ≈ 1` for one slider angle. Lean proves it for **every** real
        angle at once, using Mathlib's definitions of sine and cosine.
        """
    )
    return


@app.cell
def _(verified):
    verified(
        r"\sin^2\theta + \cos^2\theta = 1",
        "import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic\n"
        "open Real\n"
        "example (θ : ℝ) : sin θ ^ 2 + cos θ ^ 2 = 1 := sin_sq_add_cos_sq θ",
    )
    return


@app.cell
def _(verified):
    # Angle-addition, derived rather than quoted: `ring` closes the algebra.
    verified(
        r"\sin(\alpha - \beta) = \sin\alpha\cos\beta - \cos\alpha\sin\beta",
        "import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic\n"
        "open Real\n"
        "example (α β : ℝ) : sin (α - β) = sin α * cos β - cos α * sin β := by\n"
        "  rw [sub_eq_add_neg, sin_add, cos_neg, sin_neg]; ring",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Try it

        Edit the Lean below and press **Check**. Break the proof (change `4` to `5`,
        delete the `ring`) and watch the badge turn red with Lean's actual error.
        """
    )
    return


@app.cell
def _(mo):
    editor = mo.ui.text_area(
        value="example : 7 * 6 = 42 := by decide",
        rows=6,
        full_width=True,
    ).form(submit_button_label="Check")
    editor
    return (editor,)


@app.cell
def _(check, editor, mo):
    mo.stop(editor.value is None, mo.md("*Edit above and press Check.*"))

    _r = check(editor.value)
    _kind = "success" if _r.ok and not _r.has_sorry else ("warn" if _r.has_sorry else "danger")
    _msg = f"**{_r.status}** &middot; {_r.seconds:.1f}s"
    _body = mo.md(_msg) if _r.ok else mo.md(f"{_msg}\n\n```\n{_r.output}\n```")
    mo.callout(_body, kind=_kind)
    return


if __name__ == "__main__":
    app.run()
