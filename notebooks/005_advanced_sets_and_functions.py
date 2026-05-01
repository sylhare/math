"""
Advanced Sets and Functions: Beyond Infinity

An exploration of ordinal numbers, cardinal arithmetic,
the Axiom of Choice, construction of number systems, and lattice theory.
Building on the foundations from 004_set_theory.py.
"""

import marimo

__generated_with = "0.19.6"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import numpy as np
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    from math_explorations.visualization import COLORS, base_layout
    return COLORS, base_layout, go, make_subplots, np


@app.cell
def _(mo):
    mo.md(
        r"""
        # Advanced Sets and Functions: Beyond Infinity

        *"No one shall expel us from the Paradise that Cantor has created."*
        — David Hilbert (1926)

        ---

        ## Cantor's Paradise

        In the late 19th century, **Georg Cantor** embarked on one of the most audacious
        intellectual journeys in history. He dared to ask: *Can we count beyond infinity?
        Are all infinities the same size?*

        His answers shocked the mathematical world. Cantor discovered that there are
        **different sizes of infinity**—infinitely many of them! Some infinities are
        genuinely larger than others.

        But this paradise came at a price. **Leopold Kronecker**, one of the most
        influential mathematicians of the time, called Cantor a "corrupter of youth"
        and worked to block his career. Cantor suffered severe depression and died
        in a sanatorium.

        Yet his ideas triumphed. When David Hilbert gave his famous defense of Cantor's
        work, he declared that no one would ever drive mathematicians from this paradise
        of infinite sets. Today, Cantor's set theory is the foundation of all mathematics.

        In this notebook, we'll explore the deeper structures Cantor and his successors
        discovered: ordinal numbers, cardinal arithmetic, the controversial Axiom of Choice,
        and how to build all of mathematics from nothing but sets.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What We'll Explore

        This notebook builds on [Set Theory (004)](./004_set_theory.html) to explore:

        | Section | Topic | Key Question |
        |---------|-------|--------------|
        | 1 | **Ordinal Numbers** | How do we count steps in infinite processes? |
        | 2 | **Cardinal Arithmetic** | What happens when we add, multiply, or exponentiate infinities? |
        | 3 | **Axiom of Choice** | Can we always make infinitely many choices? |
        | 4 | **Constructing Numbers** | Can we build ℕ, ℤ, ℚ, ℝ from pure sets? |
        | 5 | **Advanced Functions** | What is a function space? When do sets have equal size? |
        | 6 | **Lattice Theory** | What structures emerge from partial orders? |

        ### Prerequisites

        You should be familiar with:
        - Basic set operations (union, intersection, power set)
        - Relations and functions
        - The concept of bijection and cardinality
        - The ZFC axioms (especially Infinity and Power Set)

        Let's begin our journey beyond the finite!
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        # Part 1: Ordinal Numbers

        *"An ordinal is a way to count steps in a process, even an infinite process."*

        ---

        ## The Problem Cantor Faced (1883)

        Cantor was studying infinite series and needed a way to describe **positions**
        in infinite sequences. The natural numbers 0, 1, 2, 3, ... work fine for finite
        counting, but what comes *after* all the natural numbers?

        Think about it: if you've counted through ALL natural numbers, what position
        are you at now? It can't be a natural number—you've passed them all!

        Cantor's insight: we need **new numbers** to describe positions beyond the finite.
        These are the **ordinal numbers**.

        ### The Key Distinction

        - **Cardinal numbers** answer: "How many?" (measuring SIZE)
        - **Ordinal numbers** answer: "What position?" (measuring ORDER)

        For finite sets, these coincide. The set {a, b, c} has cardinality 3, and if we
        list them in order, the positions are 0, 1, 2 (or 1st, 2nd, 3rd).

        But for infinite sets, cardinals and ordinals behave very differently!
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Von Neumann's Elegant Construction (1923)

        **John von Neumann**, at age 19, found a beautiful way to build ordinal numbers
        from pure sets. His idea: **each ordinal IS the set of all smaller ordinals**.

        ### Building from Nothing

        We start with absolutely nothing—the empty set:

        $$0 = \emptyset = \{\}$$

        "Zero is emptiness itself."

        Now, what's the set of all ordinals less than 1? Just {0}:

        $$1 = \{0\} = \{\emptyset\}$$

        "One is the set containing nothing—but containing nothing IS something!"

        What's the set of all ordinals less than 2? It's {0, 1}:

        $$2 = \{0, 1\} = \{\emptyset, \{\emptyset\}\}$$

        "Two is the set of all ordinals before it."

        The pattern continues:

        $$3 = \{0, 1, 2\} = \{\emptyset, \{\emptyset\}, \{\emptyset, \{\emptyset\}\}\}$$

        $$n = \{0, 1, 2, \ldots, n-1\}$$

        **Each ordinal contains its entire history!**
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### The Nested Structure of Ordinals

        Let's write out the first few ordinals in full set notation:

        | n | Set Form | Simplified |
        |---|----------|------------|
        | 0 | {} | ∅ |
        | 1 | {{}} | {∅} |
        | 2 | {{}, {{}}} | {∅, {∅}} |
        | 3 | {{}, {{}}, {{}, {{}}}} | {∅, {∅}, {∅, {∅}}} |

        Notice: To write 4 in full, we'd need to write out 0, 1, 2, and 3 inside it!
        The notation grows exponentially.

        **Key insight**: The natural number n, when written as a von Neumann ordinal,
        contains 2ⁿ pairs of braces. Mathematics is built from nothing but
        emptiness and the concept of "collection."
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, np):
    # Visualize Von Neumann ordinal construction
    _fig = go.Figure()

    # Create nested set visualization
    _ordinals = [
        ("0 = ∅", 0, COLORS["tertiary"], "{}"),
        ("1 = {0}", 1, COLORS["primary"], "{∅}"),
        ("2 = {0,1}", 2, COLORS["secondary"], "{∅, {∅}}"),
        ("3 = {0,1,2}", 3, COLORS["highlight"], "{∅, {∅}, {∅,{∅}}}"),
    ]

    for _i, (_label, _val, _color, _setform) in enumerate(_ordinals):
        # Draw concentric circles showing nesting
        _r = 0.8 + _i * 0.6
        _theta = [_t * 3.14159 / 50 for _t in range(101)]
        _x = [_r * np.cos(_t) for _t in _theta]
        _y = [_r * np.sin(_t) for _t in _theta]

        _fig.add_trace(go.Scatter(
            x=_x, y=_y,
            mode="lines",
            line=dict(color=_color, width=3),
            name=_label,
        ))

        # Label
        _fig.add_annotation(
            x=_r + 0.3, y=0,
            text=_label,
            font=dict(size=12, color=_color),
            showarrow=False,
        )

    _fig.add_annotation(
        x=0, y=-3.5,
        text="Each ordinal contains all previous ordinals",
        font=dict(size=14, color=COLORS["text_secondary"]),
        showarrow=False,
    )

    _fig.update_layout(**base_layout(
        title=dict(text="Von Neumann Ordinals: Building Numbers from Sets", font=dict(color=COLORS["text"], size=16)),
        xaxis=dict(visible=False, range=[-4, 5]),
        yaxis=dict(visible=False, range=[-4, 3.5], scaleanchor="x"),
        height=400,
        showlegend=True,
    ))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The concentric semicircles represent the first four von Neumann ordinals (0, 1, 2, 3). Each ordinal is literally the set of all smaller ordinals—so 2 contains both 0 and 1 inside it. The nesting shows how each number "contains its entire history," building all of mathematics from nothing but the empty set.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The Successor Operation

        Given any ordinal α, we can form its **successor**:

        $$S(\alpha) = \alpha \cup \{\alpha\}$$

        In plain English: "To get the next ordinal, take everything you have and add
        yourself to the collection."

        **Examples:**
        - $S(0) = 0 \cup \{0\} = \emptyset \cup \{\emptyset\} = \{\emptyset\} = 1$
        - $S(1) = 1 \cup \{1\} = \{0\} \cup \{1\} = \{0, 1\} = 2$
        - $S(2) = 2 \cup \{2\} = \{0, 1\} \cup \{2\} = \{0, 1, 2\} = 3$

        This gives us all the **successor ordinals**: 1, 2, 3, 4, ...

        But wait—if we keep taking successors forever, we generate ALL natural numbers.
        What ordinal comes *after* all of them?
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The First Limit Ordinal: ω

        After all the natural numbers comes **omega** (ω), the first **limit ordinal**.

        $$\omega = \{0, 1, 2, 3, 4, \ldots\} = \mathbb{N}$$

        **ω is NOT a successor!** There's no ordinal α where S(α) = ω. Instead, ω is
        the **limit** of the sequence 0, 1, 2, 3, ...

        Think of it this way: ω is like the horizon. No matter how many steps you take
        (1, 2, 3, ...), you never reach it by taking "one more step." But it's still
        there—the first position beyond all finite positions.

        ### But We're Not Done!

        After ω comes ω + 1:

        $$\omega + 1 = S(\omega) = \omega \cup \{\omega\} = \{0, 1, 2, \ldots, \omega\}$$

        Then ω + 2, ω + 3, and so on...

        Eventually we reach another limit: **ω · 2** (omega times two)—the first ordinal
        beyond ω, ω+1, ω+2, ...

        The ordinals keep going: ω·3, ω², ω³, ω^ω, ω^ω^ω, ...

        **There's no end to the ordinals!**
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Ordinal Hierarchy Summary

        Here's the structure of small ordinals:

        | Level | Ordinals | Description |
        |-------|----------|-------------|
        | Finite | 0, 1, 2, ..., n, ... | Natural numbers |
        | ω | ω | First limit ordinal |
        | ω + finite | ω+1, ω+2, ..., ω+n, ... | Successors of ω |
        | ω·2 | ω·2 | Second copy of ω |
        | ω·n | ω·3, ω·4, ..., ω·n, ... | Finite multiples of ω |
        | ω² | ω² | "ω copies of ω" |
        | ω^n | ω³, ω⁴, ..., ω^n, ... | Higher powers |
        | ω^ω | ω^ω | ω to the ω power |
        | ε₀ | ε₀ = ω^ω^ω^... | First "epsilon number" |

        Each level is dwarfed by the next. And ε₀ is just the beginning—there are
        ordinals so large they cannot be described in ordinary notation!
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, np):
    # Animated ordinal number line
    _fig = go.Figure()

    # Positions for ordinals on a "number line"
    # We'll compress infinite distances for visualization
    _ordinals_display = [
        (0, "0"), (1, "1"), (2, "2"), (3, "3"), (4, "..."),
        (6, "ω"), (7, "ω+1"), (8, "ω+2"), (9, "..."),
        (11, "ω·2"), (12, "ω·2+1"), (13, "..."),
        (15, "ω²"), (16, "..."),
    ]

    # Draw number line
    _fig.add_trace(go.Scatter(
        x=[0, 17], y=[0, 0],
        mode="lines",
        line=dict(color=COLORS["muted"], width=2),
        showlegend=False,
    ))

    # Add tick marks and labels
    for _pos, _label in _ordinals_display:
        # Tick mark
        _fig.add_trace(go.Scatter(
            x=[_pos, _pos], y=[-0.2, 0.2],
            mode="lines",
            line=dict(color=COLORS["primary"], width=2),
            showlegend=False,
        ))
        # Label
        _color = COLORS["secondary"] if "ω" in _label else COLORS["tertiary"]
        _fig.add_annotation(
            x=_pos, y=-0.5,
            text=_label,
            font=dict(size=12, color=_color),
            showarrow=False,
        )

    # Add breaks to show gaps
    for _gap_x in [5, 10, 14]:
        _fig.add_trace(go.Scatter(
            x=[_gap_x - 0.3, _gap_x + 0.3], y=[0, 0],
            mode="lines",
            line=dict(color=COLORS["background"], width=8),
            showlegend=False,
        ))

    # Annotations
    _fig.add_annotation(x=3, y=1, text="Finite ordinals", font=dict(size=11, color=COLORS["tertiary"]), showarrow=False)
    _fig.add_annotation(x=7, y=1, text="First infinite ordinals", font=dict(size=11, color=COLORS["secondary"]), showarrow=False)
    _fig.add_annotation(x=15, y=1, text="Beyond ω·n", font=dict(size=11, color=COLORS["highlight"]), showarrow=False)

    _fig.update_layout(**base_layout(
        title=dict(text="The Ordinal Number Line: Counting Beyond Infinity", font=dict(color=COLORS["text"], size=16)),
        xaxis=dict(visible=False, range=[-1, 18]),
        yaxis=dict(visible=False, range=[-1.5, 2]),
        height=300,
    ))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        This number line extends counting beyond infinity. The finite ordinals (0, 1, 2, 3...) lead up to ω (omega), the first infinite ordinal. But the counting doesn't stop there—after ω come ω+1, ω+2, and eventually ω·2, ω², and beyond. The gaps between sections indicate that infinitely many positions have been compressed for display.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Ordinal Arithmetic is Non-Commutative!

        Here's a surprising fact that shows ordinals aren't like regular numbers:

        $$1 + \omega = \omega \quad \text{but} \quad \omega + 1 > \omega$$

        **Wait, what?** Addition isn't commutative for ordinals?!

        ### The Train Car Analogy

        Think of ordinals as train cars. The ordinal α + β means: "First lay out the
        train cars for α, then attach the train cars for β at the end."

        **1 + ω**: First one car (labeled 0), then infinitely many cars (labeled 0, 1, 2, ...).
        But the first car just gets absorbed—the result looks exactly like ω cars in a row.
        The lone car at the front doesn't change the "order type."

        **ω + 1**: First infinitely many cars, then ONE more at the end. This extra car
        sits at a position beyond all the ω cars. It's genuinely different from ω!

        $$\omega + 1 = \{0, 1, 2, 3, \ldots, \omega\}$$

        The ω sits at the END, a new maximum element that ω didn't have.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, make_subplots):
    # Visualize 1 + ω vs ω + 1
    _fig = make_subplots(rows=2, cols=1, subplot_titles=["1 + ω = ω", "ω + 1 > ω"], vertical_spacing=0.3)

    # 1 + ω: one car then omega cars
    _y1 = 0
    # The "1" car
    _fig.add_trace(go.Scatter(
        x=[0], y=[_y1], mode="markers+text",
        marker=dict(size=30, color=COLORS["secondary"], symbol="square"),
        text=["1"], textposition="middle center",
        textfont=dict(size=10, color="white"),
        showlegend=False,
    ), row=1, col=1)
    # The omega cars
    for _i in range(8):
        _fig.add_trace(go.Scatter(
            x=[_i + 1.5], y=[_y1], mode="markers+text",
            marker=dict(size=30, color=COLORS["tertiary"], symbol="square"),
            text=[str(_i)], textposition="middle center",
            textfont=dict(size=10, color="white"),
            showlegend=False,
        ), row=1, col=1)
    _fig.add_annotation(x=10, y=_y1, text="... = ω", font=dict(size=14, color=COLORS["tertiary"]), showarrow=False, row=1, col=1)

    # ω + 1: omega cars then one car
    _y2 = 0
    for _i in range(8):
        _fig.add_trace(go.Scatter(
            x=[_i], y=[_y2], mode="markers+text",
            marker=dict(size=30, color=COLORS["tertiary"], symbol="square"),
            text=[str(_i)], textposition="middle center",
            textfont=dict(size=10, color="white"),
            showlegend=False,
        ), row=2, col=1)
    _fig.add_annotation(x=8.5, y=_y2, text="...", font=dict(size=14, color=COLORS["tertiary"]), showarrow=False, row=2, col=1)
    # The "+1" car at the end
    _fig.add_trace(go.Scatter(
        x=[10], y=[_y2], mode="markers+text",
        marker=dict(size=30, color=COLORS["secondary"], symbol="square"),
        text=["ω"], textposition="middle center",
        textfont=dict(size=10, color="white"),
        showlegend=False,
    ), row=2, col=1)
    _fig.add_annotation(x=11, y=_y2, text="← NEW!", font=dict(size=12, color=COLORS["secondary"]), showarrow=False, row=2, col=1)

    _fig.update_xaxes(visible=False, range=[-1, 12])
    _fig.update_yaxes(visible=False, range=[-1, 1])
    _fig.update_layout(**base_layout(
        title=dict(text="Ordinal Addition is NOT Commutative", font=dict(color=COLORS["text"], size=16)),
        height=350,
    ))
    _fig.update_annotations(font=dict(color=COLORS["text"]))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The top row shows "1 + ω"—placing one element (red) before infinitely many (teal). Surprisingly, this equals just ω, because the single element gets "absorbed" into the infinite sequence. The bottom row shows "ω + 1"—infinitely many elements followed by ONE more at the end. This creates something genuinely new: a sequence with a last element, which ω alone doesn't have. This demonstrates that ordinal addition is not commutative!
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Why Ordinals Matter: Transfinite Induction

        The real power of ordinals is that they let us do **induction beyond ℕ**.

        **Ordinary induction** proves P(n) for all natural numbers:
        1. Prove P(0) (base case)
        2. Prove P(n) → P(n+1) (inductive step)
        3. Conclude P(n) for all n ∈ ℕ

        **Transfinite induction** proves P(α) for all ordinals:
        1. Prove P(0) (base case)
        2. Prove P(α) → P(α+1) (successor case)
        3. Prove: if P(β) for all β < λ, then P(λ) (limit case)
        4. Conclude P(α) for all ordinals α

        The limit case is new! For limit ordinals like ω, we can't just use "P(predecessor)"
        because limit ordinals have no immediate predecessor.

        ### Why It Works

        Every non-empty class of ordinals has a **minimum element**. This is because
        ordinals are **well-ordered**—a property that makes induction valid.

        If P failed somewhere, the class of failures would have a minimum α. But then
        P holds for all β < α, so by our induction rules, P(α) holds. Contradiction!
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Proof: Every Ordinal is Well-Ordered

        **Theorem**: The elements of any ordinal α (viewed as a set) are well-ordered by ∈.

        **Proof** (sketch):

        We prove this by transfinite induction on α.

        **Base case (α = 0)**: The empty set ∅ is trivially well-ordered—it has no elements!

        **Successor case (α = β + 1)**: Assume β is well-ordered. Then α = β ∪ {β}.
        Any non-empty subset of α either:
        - Is contained in β (use the well-ordering of β to find its minimum), or
        - Contains β (then β itself is the minimum of that part)

        Either way, we find a minimum.

        **Limit case (α is a limit)**: Assume every β < α is well-ordered.
        Let S ⊆ α be non-empty. Pick any s ∈ S.
        Then S ∩ (s + 1) is a non-empty subset of the successor ordinal s + 1.
        By the successor case, it has a minimum. This minimum is also the minimum of S.

        Therefore, every ordinal is well-ordered. ∎

        **This is why ordinals are fundamental**: they capture the essence of well-ordering.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Types of Ordinals

        Ordinals come in three flavors:

        **1. Zero**: The empty ordinal 0 = ∅.

        **2. Successor ordinals**: α + 1 = S(α) for some ordinal α.
        Examples: 1, 2, 3, ..., ω+1, ω+2, ..., ω·2+1, ...

        **3. Limit ordinals**: Non-zero ordinals that are NOT successors.
        Examples: ω, ω·2, ω², ω^ω, ...

        Limit ordinals are where things get interesting—they have no immediate
        predecessor. You can approach them but never "reach" them with successor.

        **The ε (epsilon) numbers** are special limit ordinals where ε = ω^ε.
        The smallest is ε₀ = ω^ω^ω^... (infinite tower).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        # Part 2: Cardinal Arithmetic

        *"Some infinities are bigger than other infinities."*
        — John Green (paraphrasing Cantor)

        ---

        ## Cantor's Shocking Discovery (1874)

        While studying trigonometric series, Cantor made a discovery that changed
        mathematics forever: **the real numbers ℝ cannot be put in one-to-one
        correspondence with the natural numbers ℕ**.

        This means ℝ is "more infinite" than ℕ!

        Cantor used the Hebrew letter **aleph (ℵ)** to denote infinite cardinals:

        - $\aleph_0$ (aleph-null) = |ℕ| = the "smallest" infinity
        - $\aleph_1$ = the next larger cardinal
        - $\aleph_2, \aleph_3, \ldots$ = ever larger infinities

        He also discovered $2^{\aleph_0} = |\mathbb{R}|$ — the **continuum**.

        But is $2^{\aleph_0} = \aleph_1$? This became Hilbert's **First Problem** (1900)
        and led to one of the most surprising results in the history of mathematics.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Cardinal Addition: Combining Infinities

        **Definition**: For cardinals κ and λ, their sum κ + λ is the cardinality of
        the **disjoint union** of a set of size κ and a set of size λ.

        $$\kappa + \lambda = |A \sqcup B| \text{ where } |A| = \kappa, |B| = \lambda$$

        ### The Surprising Result

        $$\aleph_0 + \aleph_0 = \aleph_0$$

        Two countable infinities combine to give... the same countable infinity!

        **Proof**: We need a bijection from ℕ ⊔ ℕ to ℕ.

        Think of two copies of ℕ as "even-labeled" and "odd-labeled":
        - First copy: 0, 1, 2, 3, ... → map to 0, 2, 4, 6, ...
        - Second copy: 0, 1, 2, 3, ... → map to 1, 3, 5, 7, ...

        Together they perfectly cover all of ℕ! So |ℕ ⊔ ℕ| = |ℕ|.

        **Interleaving**: We "weave" the two infinite lists together:
        $$a_0, b_0, a_1, b_1, a_2, b_2, \ldots$$

        In general, for any infinite cardinal κ: $\kappa + \kappa = \kappa$.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Absorption Laws for Cardinals

        For infinite cardinals, addition behaves strangely:

        **Theorem**: For any infinite cardinal κ and any cardinal λ ≤ κ:
        $$\kappa + \lambda = \kappa$$

        The larger cardinal "absorbs" the smaller one!

        **Proof idea**: If |A| = κ and |B| = λ ≤ κ, we can find an injection B → A.
        Then A ⊔ B can be mapped bijectively to A by "spreading out" the elements.

        **Examples**:
        - ℵ₀ + 1 = ℵ₀ (adding one element to ℕ doesn't change its size)
        - ℵ₀ + ℵ₀ = ℵ₀ (two countable sets combine to countable)
        - 𝔠 + ℵ₀ = 𝔠 (adding countably many reals to ℝ doesn't change size)
        - 𝔠 + 𝔠 = 𝔠 (two copies of ℝ have same cardinality as ℝ)

        This is radically different from finite arithmetic!
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go):
    # Visualize cardinal addition: interleaving
    _fig = go.Figure()

    # First copy of N (top)
    for _i in range(6):
        _fig.add_trace(go.Scatter(
            x=[_i * 2], y=[2], mode="markers+text",
            marker=dict(size=35, color=COLORS["tertiary"]),
            text=[f"a{_i}"], textposition="middle center",
            textfont=dict(size=11, color=COLORS["background"]),
            showlegend=False,
        ))

    # Second copy of N (middle)
    for _i in range(6):
        _fig.add_trace(go.Scatter(
            x=[_i * 2], y=[0], mode="markers+text",
            marker=dict(size=35, color=COLORS["secondary"]),
            text=[f"b{_i}"], textposition="middle center",
            textfont=dict(size=11, color=COLORS["background"]),
            showlegend=False,
        ))

    # Interleaved result (bottom)
    _labels = ["a0", "b0", "a1", "b1", "a2", "b2", "a3", "b3", "a4", "b4", "a5", "b5"]
    _colors = [COLORS["tertiary"], COLORS["secondary"]] * 6
    for _i, (_lbl, _col) in enumerate(zip(_labels, _colors)):
        _fig.add_trace(go.Scatter(
            x=[_i * 0.9], y=[-2], mode="markers+text",
            marker=dict(size=30, color=_col),
            text=[_lbl], textposition="middle center",
            textfont=dict(size=9, color=COLORS["background"]),
            showlegend=False,
        ))

    # Arrows showing interleaving
    for _i in range(6):
        # From top to bottom
        _fig.add_annotation(
            x=_i * 0.9 * 2, y=-1.5, ax=_i * 2, ay=1.5,
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=1.5, arrowcolor=COLORS["tertiary"], opacity=0.5,
        )
        # From middle to bottom
        _fig.add_annotation(
            x=_i * 0.9 * 2 + 0.9, y=-1.5, ax=_i * 2, ay=-0.5,
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=1.5, arrowcolor=COLORS["secondary"], opacity=0.5,
        )

    # Labels
    _fig.add_annotation(x=-1.5, y=2, text="ℕ₁:", font=dict(size=14, color=COLORS["tertiary"]), showarrow=False)
    _fig.add_annotation(x=-1.5, y=0, text="ℕ₂:", font=dict(size=14, color=COLORS["secondary"]), showarrow=False)
    _fig.add_annotation(x=-1.5, y=-2, text="ℕ:", font=dict(size=14, color=COLORS["primary"]), showarrow=False)
    _fig.add_annotation(x=12, y=2, text="...", font=dict(size=14, color=COLORS["tertiary"]), showarrow=False)
    _fig.add_annotation(x=12, y=0, text="...", font=dict(size=14, color=COLORS["secondary"]), showarrow=False)
    _fig.add_annotation(x=11, y=-2, text="...", font=dict(size=14, color=COLORS["primary"]), showarrow=False)

    _fig.update_layout(**base_layout(
        title=dict(text="Cardinal Addition: ℵ₀ + ℵ₀ = ℵ₀ (Interleaving)", font=dict(color=COLORS["text"], size=16)),
        xaxis=dict(visible=False, range=[-3, 14]),
        yaxis=dict(visible=False, range=[-3.5, 3.5]),
        height=400,
    ))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        This demonstrates that ℵ₀ + ℵ₀ = ℵ₀ through interleaving. The top two rows represent two separate copies of the natural numbers. By weaving them together—taking one element from each in alternation—we create a single sequence at the bottom that contains all elements from both. This bijection proves that two countably infinite sets combined still have countable cardinality.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Cardinal Multiplication: The Cantor Pairing Function

        **Definition**: For cardinals κ and λ, their product κ · λ is the cardinality
        of the **Cartesian product** of a set of size κ and a set of size λ.

        $$\kappa \cdot \lambda = |A \times B| \text{ where } |A| = \kappa, |B| = \lambda$$

        ### Another Surprise

        $$\aleph_0 \cdot \aleph_0 = \aleph_0$$

        An infinite grid has the same cardinality as a single infinite line!

        **Proof**: We need a bijection from ℕ × ℕ to ℕ.

        Cantor's **pairing function** does exactly this:

        $$\pi(m, n) = \frac{(m + n)(m + n + 1)}{2} + n$$

        This function traverses ℕ × ℕ along **diagonals**:
        - Diagonal 0: (0,0) → 0
        - Diagonal 1: (1,0), (0,1) → 1, 2
        - Diagonal 2: (2,0), (1,1), (0,2) → 3, 4, 5
        - And so on...

        Every point (m, n) gets a unique natural number!
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Why the Pairing Function Works

        The Cantor pairing function uses the fact that we can traverse ℕ × ℕ along
        **diagonals**. On diagonal k, we have all points (m, n) with m + n = k.

        Diagonal k has k + 1 points: (0, k), (1, k-1), (2, k-2), ..., (k, 0).

        The total number of points on diagonals 0, 1, ..., k-1 is:
        $$1 + 2 + 3 + \ldots + k = \frac{k(k+1)}{2}$$

        So for point (m, n) on diagonal k = m + n:
        - Start of diagonal k: position k(k+1)/2
        - Position within diagonal: n steps along
        - Final position: k(k+1)/2 + n = (m+n)(m+n+1)/2 + n
        **This proves ℕ × ℕ is countable!** And by extension, ℚ is countable
        (each rational is essentially a pair of integers).
        """
    )
    return


@app.cell
def _(mo):
    # Slider for Cantor pairing animation
    pairing_step = mo.ui.slider(
        start=0, stop=20, step=1, value=10,
        label="Number of points to show:"
    )
    return (pairing_step,)


@app.cell
def _(mo, pairing_step):
    mo.md(f"""
    ### Interactive: Cantor Pairing Function

    Watch how the pairing function zigzags through ℕ × ℕ:

    {pairing_step}
    """)
    return


@app.cell
def _(COLORS, base_layout, go, np, pairing_step):
    def _cantor_unpair(z):
        """Inverse of Cantor pairing function."""
        # Find which diagonal z is on
        w = int((np.sqrt(8 * z + 1) - 1) / 2)
        t = (w * w + w) // 2
        n = z - t
        m = w - n
        return m, n

    _num_points = pairing_step.value + 1
    _points = [_cantor_unpair(_i) for _i in range(_num_points)]

    _fig = go.Figure()

    # Draw grid
    for _i in range(7):
        _fig.add_trace(go.Scatter(
            x=[_i] * 7, y=list(range(7)),
            mode="markers",
            marker=dict(size=20, color="rgba(74, 85, 104, 0.3)"),
            showlegend=False,
        ))

    # Draw path
    if len(_points) > 1:
        _px = [_p[0] for _p in _points]
        _py = [_p[1] for _p in _points]
        _fig.add_trace(go.Scatter(
            x=_px, y=_py,
            mode="lines",
            line=dict(color=COLORS["primary"], width=2),
            showlegend=False,
        ))

    # Draw visited points with numbers
    for _idx, (_m, _n) in enumerate(_points):
        _fig.add_trace(go.Scatter(
            x=[_m], y=[_n],
            mode="markers+text",
            marker=dict(size=30, color=COLORS["tertiary"]),
            text=[str(_idx)],
            textposition="middle center",
            textfont=dict(size=10, color=COLORS["background"]),
            showlegend=False,
        ))

    # Axis labels
    _fig.add_annotation(x=3, y=-0.8, text="m", font=dict(size=14, color=COLORS["text_secondary"]), showarrow=False)
    _fig.add_annotation(x=-0.8, y=3, text="n", font=dict(size=14, color=COLORS["text_secondary"]), showarrow=False)

    _fig.update_layout(**base_layout(
        title=dict(text="Cantor Pairing: π(m,n) = ½(m+n)(m+n+1) + n", font=dict(color=COLORS["text"], size=16)),
        xaxis=dict(visible=False, range=[-1.5, 7]),
        yaxis=dict(visible=False, range=[-1.5, 7], scaleanchor="x"),
        height=450,
    ))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The Cantor pairing function maps every point (m, n) in the infinite grid ℕ × ℕ to a unique natural number. The path zigzags along diagonals: first (0,0), then (1,0), (0,1), then (2,0), (1,1), (0,2), and so on. Each numbered circle shows which natural number that grid point maps to. This proves ℕ × ℕ has the same cardinality as ℕ, so ℵ₀ · ℵ₀ = ℵ₀.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Cardinal Exponentiation: Counting Functions

        **Definition**: For cardinals κ and λ, the exponential κ^λ is the cardinality
        of the set of **all functions** from a set of size λ to a set of size κ.

        $$\kappa^\lambda = |B^A| \text{ where } |A| = \lambda, |B| = \kappa$$

        ### The Crucial Example: 2^ℵ₀

        What is $2^{\aleph_0}$? It's the cardinality of all functions from ℕ to {0, 1}.

        But a function f: ℕ → {0, 1} is just an **infinite binary sequence**:
        $$f(0)f(1)f(2)f(3)\ldots \in \{0, 1\}^\mathbb{N}$$

        Examples:
        - 000000... (all zeros)
        - 111111... (all ones)
        - 010101... (alternating)
        - 110100... (encodes some information)

        **Key insight**: Each real number in [0, 1] has a binary expansion!
        $$x = 0.b_1b_2b_3\ldots = \sum_{i=1}^\infty \frac{b_i}{2^i}$$

        So $2^{\aleph_0} = |\mathcal{P}(\mathbb{N})| = |\mathbb{R}|$ — the **continuum**!
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Cantor's Theorem: The Power Set is Always Bigger

        **Theorem** (Cantor, 1891): For any set A, $|A| < |\mathcal{P}(A)|$.

        In words: **There are always more subsets than elements.**

        This is true for finite sets: if |A| = n, then |P(A)| = 2^n > n.

        But it's also true for **infinite sets**! This is remarkable: we can always
        find a bigger infinity by taking the power set.

        ### The Diagonal Proof

        **Proof**: We show there's no surjection f: A → P(A).

        Suppose f: A → P(A) is any function. Define the **diagonal set**:

        $$D = \{a \in A : a \notin f(a)\}$$

        D is the set of elements that are NOT in their own image.

        **Claim**: D ≠ f(a) for any a ∈ A.

        **Why?** For any a:
        - If a ∈ D, then by definition of D, a ∉ f(a). So D ≠ f(a) (they differ on a).
        - If a ∉ D, then by definition of D, a ∈ f(a). So D ≠ f(a) (they differ on a).

        Either way, D is not in the range of f. So f is not surjective. ∎

        **This means**: $\aleph_0 < 2^{\aleph_0} < 2^{2^{\aleph_0}} < \ldots$

        **The hierarchy of infinities never ends!**
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Understanding the Diagonal Argument

        The key to Cantor's proof is the **self-referential** nature of the set D.

        For any proposed function f: A → P(A), we ask each element a:
        *"Are you in the set that f assigns to you?"*

        The set D collects all elements that answer "No."

        **Why D can't be in the range of f:**

        Suppose D = f(x) for some x ∈ A. Then:
        - If x ∈ D, then x ∈ f(x), but D = {a : a ∉ f(a)}, so x ∉ D. Contradiction!
        - If x ∉ D, then x ∉ f(x), but D = {a : a ∉ f(a)}, so x ∈ D. Contradiction!

        Either way we reach a contradiction. So D ≠ f(x) for any x.

        **The diagonal argument reappears throughout mathematics:**
        - Uncountability of ℝ
        - Undecidability of the halting problem
        - Gödel's incompleteness theorems
        - Russell's paradox (the original inspiration!)
        """
    )
    return


@app.cell
def _(mo):
    # Interactive demonstration of Cantor's theorem
    cantor_element = mo.ui.dropdown(
        options={"a": "a", "b": "b", "c": "c"},
        value="a",
        label="Select element to check:"
    )
    return (cantor_element,)


@app.cell
def _(cantor_element, mo):
    mo.md(f"""
    ### Interactive: Building the Diagonal Set

    Let A = {{a, b, c}} and consider this function f: A → P(A):
    - f(a) = {{a, b}}
    - f(b) = {{b}}
    - f(c) = {{a, c}}

    For each element, ask: "Is it in its own image?"
    - a ∈ f(a) = {{a, b}}? **Yes** (a is in {{a, b}})
    - b ∈ f(b) = {{b}}? **Yes** (b is in {{b}})
    - c ∈ f(c) = {{a, c}}? **Yes** (c is in {{a, c}})

    **D = {{x : x ∉ f(x)}} = ∅** (no elements satisfy the condition here)

    But notice: D = ∅ is NOT equal to f(a), f(b), or f(c)!

    {cantor_element}

    Check: Is D = f({cantor_element.value})?
    - f({cantor_element.value}) = {"{{a, b}}" if cantor_element.value == "a" else "{{b}}" if cantor_element.value == "b" else "{{a, c}}"}
    - D = ∅
    - **D ≠ f({cantor_element.value})**!    """)
    return


@app.cell
def _(COLORS, base_layout, go):
    # Visualization of Cantor's theorem proof
    _fig = go.Figure()

    # Create a table showing f(a), f(b), f(c) and membership
    _elements = ["a", "b", "c"]
    _images = ["{a, b}", "{b}", "{a, c}"]
    _in_own = ["✓", "✓", "✓"]
    _in_D = ["✗", "✗", "✗"]

    # Headers
    _headers = ["Element x", "f(x)", "x ∈ f(x)?", "x ∈ D?"]
    for _i, _h in enumerate(_headers):
        _fig.add_annotation(x=_i, y=4, text=_h, font=dict(size=12, color=COLORS["primary"], family="monospace"), showarrow=False)

    # Data rows
    for _row, (_e, _img, _own, _d) in enumerate(zip(_elements, _images, _in_own, _in_D)):
        _y = 3 - _row
        _fig.add_annotation(x=0, y=_y, text=_e, font=dict(size=14, color=COLORS["tertiary"]), showarrow=False)
        _fig.add_annotation(x=1, y=_y, text=_img, font=dict(size=12, color=COLORS["text_secondary"]), showarrow=False)
        _fig.add_annotation(x=2, y=_y, text=_own, font=dict(size=14, color=COLORS["tertiary"]), showarrow=False)
        _fig.add_annotation(x=3, y=_y, text=_d, font=dict(size=14, color=COLORS["secondary"]), showarrow=False)

    # Diagonal set result
    _fig.add_annotation(x=1.5, y=0, text="D = {x : x ∉ f(x)} = ∅", font=dict(size=14, color=COLORS["highlight"]), showarrow=False)
    _fig.add_annotation(x=1.5, y=-0.7, text="D is NOT in the range of f!", font=dict(size=12, color=COLORS["secondary"]), showarrow=False)

    _fig.update_layout(**base_layout(
        title=dict(text="Cantor's Diagonal Argument: Building the 'Missing' Set", font=dict(color=COLORS["text"], size=16)),
        xaxis=dict(visible=False, range=[-1, 4]),
        yaxis=dict(visible=False, range=[-1.5, 5]),
        height=350,
    ))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        This table illustrates Cantor's diagonal argument for proving |A| < |P(A)|. For each element x (rows), we ask: "Is x in the set f(x)?" The diagonal set D collects all elements that answer "No." In this example, all three elements are in their assigned sets, so D = ∅. But notice: D differs from f(a), f(b), and f(c)—proving D is not in the range of f. No matter what function f we try, we can always construct a "missing" set this way.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The Continuum Hypothesis

        Cantor knew that $\aleph_0 < 2^{\aleph_0}$. But he asked:

        **Is there a cardinal strictly between ℵ₀ and 2^ℵ₀?**

        The **Continuum Hypothesis (CH)** says: **No.**

        $$\text{CH}: \quad 2^{\aleph_0} = \aleph_1$$

        In other words, the continuum (the reals) is the "next" infinity after the naturals.

        ### The Shocking Resolution

        - **Gödel (1940)**: Proved that CH cannot be DISPROVED from ZFC.
        - **Cohen (1963)**: Proved that CH cannot be PROVED from ZFC.

        **CH is INDEPENDENT of ZFC!**

        This means there are two equally valid versions of set theory:
        - One where CH is true (no sets between ℕ and ℝ in size)
        - One where CH is false (there ARE sets of intermediate size)

        Mathematics has genuine **unsolvable problems**—not unsolved, but provably
        impossible to resolve with our current axioms.

        This was one of the most profound discoveries of 20th-century mathematics.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Cardinal Arithmetic Summary

        | Operation | Result | Why |
        |-----------|--------|-----|
        | $\aleph_0 + \aleph_0$ | $\aleph_0$ | Interleave two infinite sequences |
        | $\aleph_0 + n$ | $\aleph_0$ | Finite additions don't change infinity |
        | $\aleph_0 \cdot \aleph_0$ | $\aleph_0$ | Cantor pairing (diagonal traversal) |
        | $\aleph_0 \cdot n$ | $\aleph_0$ | n copies of ℕ still countable |
        | $2^{\aleph_0}$ | $\mathfrak{c}$ | Binary sequences = real numbers |
        | $n^{\aleph_0}$ | $\mathfrak{c}$ | n-ary sequences still continuum |
        | $\aleph_0^{\aleph_0}$ | $\mathfrak{c}$ | Sequences of naturals = reals |
        | $\mathfrak{c} + \mathfrak{c}$ | $\mathfrak{c}$ | Two copies of ℝ = ℝ |
        | $\mathfrak{c} \cdot \mathfrak{c}$ | $\mathfrak{c}$ | ℝ × ℝ = ℝ (space-filling curves) |
        | $2^{\mathfrak{c}}$ | $> \mathfrak{c}$ | Power set of ℝ is strictly larger |

        **Key principle**: For infinite cardinals κ ≥ ℵ₀:
        $$\kappa + \kappa = \kappa \cdot \kappa = \kappa$$

        But exponentiation creates genuinely larger cardinals!
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Aleph vs Beth Numbers

        There are two ways to index infinite cardinals:

        **Aleph numbers ℵ_α** are defined by well-ordering:
        - ℵ₀ = smallest infinite cardinal
        - ℵ₁ = next larger cardinal
        - ℵ₂ = next after that
        - ℵ_α = α-th infinite cardinal

        **Beth numbers ℶ_α** are defined by power sets:
        - ℶ₀ = ℵ₀
        - ℶ₁ = 2^ℶ₀ (power set of ℕ)
        - ℶ₂ = 2^ℶ₁ (power set of power set of ℕ)
        - ℶ_{α+1} = 2^ℶ_α

        **The Continuum Hypothesis** says: ℶ₁ = ℵ₁

        In other words: is the power set of ℕ the "next" infinity after ℵ₀?

        We know ℶ_α ≥ ℵ_α always. But whether they're equal is independent of ZFC!
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        # Part 3: The Axiom of Choice

        *"The Axiom of Choice is obviously true, the Well-Ordering Theorem is obviously false,
        and who can tell about Zorn's Lemma?"*
        — Jerry Bona (mathematical joke)

        ---

        ## Zermelo's Controversial Axiom (1904)

        In 1904, **Ernst Zermelo** proved something shocking: **every set can be well-ordered**.

        But his proof required a new axiom—the **Axiom of Choice (AC)**:

        > For any collection of non-empty sets, there exists a function that chooses
        > one element from each set.

        This sounds innocent, but mathematicians revolted! The axiom asserts existence
        without providing a construction. It says "a choice function exists" but doesn't
        tell us how to build one.

        For a finite collection, we can just pick elements one by one. But for an
        infinite collection? We need infinitely many choices simultaneously—and AC
        says we can always make them, even if we have no rule for choosing.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The Formal Statement

        **Axiom of Choice**: For any set $\mathcal{F}$ of non-empty sets, there exists
        a **choice function** $f$ such that $f(A) \in A$ for all $A \in \mathcal{F}$.

        $$\forall \mathcal{F}\, \Big[\big(\forall A \in \mathcal{F}: A \neq \emptyset\big) \Rightarrow \exists f: \mathcal{F} \to \bigcup\mathcal{F} \text{ with } f(A) \in A\Big]$$

        ### Why It's Needed

        **Example**: Consider the equivalence classes of real numbers modulo ℚ:
        $$[x] = \{x + q : q \in \mathbb{Q}\}$$

        There are uncountably many such classes. Can we pick one representative from each?

        Without AC, we cannot prove this is possible! There's no formula to select
        representatives—each class looks the same, with no distinguishing features.

        AC says: we can make all these choices, even without a rule.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### A Finite Example Where AC is "Obvious"

        Consider three non-empty boxes:
        - Box 1: {apple, banana}
        - Box 2: {car, bus, train}
        - Box 3: {red}

        A choice function picks one item from each:
        - f(Box 1) = apple
        - f(Box 2) = bus
        - f(Box 3) = red

        Easy! We can just... pick things.

        ### An Infinite Example Where AC is NOT Obvious

        Consider the equivalence classes of ℝ under the relation x ~ y iff x - y ∈ ℚ.

        Each class looks like {..., x-1, x-½, x, x+½, x+1, ...} for some x ∈ [0,1).

        There are uncountably many such classes, all looking "the same."
        How do we pick one representative from each?

        **There's no formula!** We need AC to assert that such a choice function exists.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, np):
    # Visualization of choice function
    _fig = go.Figure()

    # Draw collection of sets
    _sets = [
        ("A₁", [-3, -2.5], ["a", "b", "c"], COLORS["tertiary"]),
        ("A₂", [-0.5, 0], ["x", "y"], COLORS["secondary"]),
        ("A₃", [2, 2.5], ["p", "q", "r", "s"], COLORS["highlight"]),
    ]

    for _name, _x_range, _elements, _color in _sets:
        # Draw set boundary
        _cx = (_x_range[0] + _x_range[1]) / 2
        _r = (_x_range[1] - _x_range[0]) / 2 + 0.4
        _theta = [_t * 3.14159 / 50 for _t in range(101)]
        _xs = [_cx + _r * np.cos(_t) for _t in _theta]
        _ys = [_r * 0.8 * np.sin(_t) for _t in _theta]
        _fig.add_trace(go.Scatter(x=_xs, y=_ys, mode="lines", line=dict(color=_color, width=2), showlegend=False))

        # Draw elements
        for _i, _e in enumerate(_elements):
            _ex = _x_range[0] + (_i + 0.5) * (_x_range[1] - _x_range[0]) / len(_elements)
            _ey = 0
            _fig.add_trace(go.Scatter(
                x=[_ex], y=[_ey], mode="markers+text",
                marker=dict(size=20, color=_color),
                text=[_e], textposition="middle center",
                textfont=dict(size=10, color=COLORS["background"]),
                showlegend=False,
            ))

        # Set label
        _fig.add_annotation(x=_cx, y=1.2, text=_name, font=dict(size=14, color=_color), showarrow=False)

    # Draw choice function arrows
    _choices = [(-2.5, "b"), (-0.25, "y"), (2.4, "r")]
    for (_x, _lbl), (_, _x_range, _elements, _color) in zip(_choices, _sets):
        _fig.add_annotation(
            x=_x, y=-1.5, ax=_x, ay=-0.3,
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=2, arrowcolor=COLORS["primary"],
        )

    # Choice function result
    _fig.add_annotation(x=-0.25, y=-2, text="f: {A₁, A₂, A₃} → elements", font=dict(size=12, color=COLORS["primary"]), showarrow=False)
    _fig.add_annotation(x=-0.25, y=-2.5, text="f(A₁)=b, f(A₂)=y, f(A₃)=r", font=dict(size=11, color=COLORS["text_secondary"]), showarrow=False)

    _fig.update_layout(**base_layout(
        title=dict(text="Axiom of Choice: Selecting One Element from Each Set", font=dict(color=COLORS["text"], size=16)),
        xaxis=dict(visible=False, range=[-5, 5]),
        yaxis=dict(visible=False, range=[-3, 2]),
        height=350,
    ))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Three non-empty sets (A₁, A₂, A₃) each contain several elements. A choice function picks exactly one element from each set—here selecting b from A₁, y from A₂, and r from A₃. For finite collections this seems trivial, but the Axiom of Choice asserts that such a function exists even for infinite collections of sets, where we have no rule for choosing.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Equivalent Forms of AC

        The Axiom of Choice is equivalent to several other important principles.
        Each sounds different, but they're all logically the same!

        ### 1. Zorn's Lemma

        > If every chain in a partially ordered set has an upper bound,
        > then the poset has at least one maximal element.

        **Plain English**: "If you can always keep going up, eventually you'll hit a top."

        **Application**: Every vector space has a basis. (We can keep extending linearly
        independent sets until we can't anymore—Zorn guarantees a maximal one exists.)

        ### 2. Well-Ordering Theorem

        > Every set can be well-ordered.

        **Plain English**: "Any set, even ℝ, can be arranged with a 'first' element,
        a 'second' element, and so on—though we may never be able to describe the arrangement."

        **Shocking consequence**: There exists a well-ordering of ℝ, but no one has ever
        written one down, and no one ever will—it's provably non-constructive!

        ### 3. Hausdorff Maximal Principle

        > Every chain in a poset can be extended to a maximal chain.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Proof Sketch: Zorn's Lemma ⟹ AC

        Assume Zorn's Lemma. We want to prove AC.

        Given a collection F of non-empty sets, consider partial choice functions:
        - A partial choice function is a function f defined on a subcollection G ⊆ F
          where f(A) ∈ A for all A ∈ G.

        Order partial choice functions by extension: f ≤ g if g extends f.

        **Verify Zorn's hypotheses:**
        - The empty function is a lower bound.
        - Any chain of partial choice functions has an upper bound (take their union).

        **Apply Zorn's Lemma:** There exists a maximal partial choice function f*.

        **Claim:** f* is defined on all of F.

        *Proof:* If not, some A ∈ F is not in the domain of f*. Pick any a ∈ A
        (A is non-empty!). Extend f* by setting f*(A) = a. This contradicts maximality.

        Therefore f* is a total choice function. AC is proved! ∎
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go):
    # Diagram showing equivalence of AC forms
    _fig = go.Figure()

    # Nodes
    _nodes = {
        "AC": (0, 0),
        "Zorn": (-2, -1.5),
        "WO": (2, -1.5),
        "Hausdorff": (0, -2.5),
    }

    # Draw nodes
    for _name, (_x, _y) in _nodes.items():
        _fig.add_trace(go.Scatter(
            x=[_x], y=[_y], mode="markers+text",
            marker=dict(size=60, color=COLORS["tertiary"]),
            text=[_name], textposition="middle center",
            textfont=dict(size=11, color=COLORS["background"]),
            showlegend=False,
        ))

    # Draw double arrows (equivalences)
    _edges = [("AC", "Zorn"), ("AC", "WO"), ("Zorn", "Hausdorff"), ("WO", "Hausdorff")]
    for _a, _b in _edges:
        _x0, _y0 = _nodes[_a]
        _x1, _y1 = _nodes[_b]
        _fig.add_trace(go.Scatter(
            x=[_x0, _x1], y=[_y0, _y1], mode="lines",
            line=dict(color=COLORS["primary"], width=2),
            showlegend=False,
        ))

    _fig.add_annotation(x=0, y=1, text="All Four Are Logically Equivalent!", font=dict(size=14, color=COLORS["highlight"]), showarrow=False)
    _fig.add_annotation(x=-2, y=-3.2, text="If any one is true,\nall are true", font=dict(size=11, color=COLORS["text_secondary"]), showarrow=False)

    _fig.update_layout(**base_layout(
        title=dict(text="The Equivalence of Choice Principles", font=dict(color=COLORS["text"], size=16)),
        xaxis=dict(visible=False, range=[-4, 4]),
        yaxis=dict(visible=False, range=[-4, 2]),
        height=350,
    ))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Four fundamental principles are connected by lines, indicating logical equivalence: the Axiom of Choice (AC), Zorn's Lemma, the Well-Ordering Theorem (WO), and Hausdorff's Maximal Principle. These statements sound completely different—one about choosing elements, one about maximal elements in posets, one about ordering any set—yet proving any one of them automatically proves all the others.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The Banach-Tarski Paradox

        The Axiom of Choice has **bizarre consequences**. The most famous is the
        **Banach-Tarski Paradox** (1924):

        > A solid ball can be decomposed into a finite number of pieces (5 suffice)
        > and reassembled into TWO balls, each identical to the original!

        **How is this possible?**

        The "pieces" are not ordinary shapes—they're so strange and fragmented that
        they have no meaningful volume. AC allows us to construct these non-measurable
        sets, which defy our geometric intuition.

        The pieces are:
        1. Not continuous (they're scattered "dust")
        2. Have no defined volume (they're non-measurable)
        3. Can only be proven to exist using AC (no explicit construction)

        **This isn't a physical paradox**—it's a mathematical statement about abstract
        point sets. Real matter can't be rearranged this way!

        ### The Constructivist Objection

        Some mathematicians reject AC precisely because of such results. They argue:

        *"Existence without construction is meaningless. If we can't describe the
        choice function, it doesn't really exist."*

        Most mathematicians today accept AC—its usefulness outweighs the strangeness.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Consequences of AC

        | Result | Requires AC? | Notes |
        |--------|--------------|-------|
        | Every vector space has a basis | **Yes** | Can't prove without AC |
        | Every surjection has a right inverse | **Yes** | Needs to choose preimages |
        | Non-measurable sets exist | **Yes** | Vitali sets, Banach-Tarski |
        | Every set can be well-ordered | **Yes** | Equivalent to AC |
        | Countable unions of countable sets are countable | **Yes** | Needs countable AC |
        | Zorn's Lemma | **Yes** | Equivalent to AC |
        | Every filter extends to an ultrafilter | **Yes** | Important in logic |
        | Tychonoff's theorem (products of compact spaces) | **Yes** | Key in topology |

        **Without AC**, mathematics becomes more "constructive" but loses many convenient
        results. Most mathematicians accept AC as a pragmatic choice—pun intended!
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Degrees of Choice

        Not all versions of AC are equally strong:

        **AC_ω (Countable Choice)**: Choice functions exist for countable collections.
        - Much weaker than full AC
        - Implies: countable union of countable sets is countable
        - Accepted by more constructivists

        **AC_κ**: Choice functions exist for collections of size κ.

        **Dependent Choice (DC)**: Can make infinitely many dependent choices.
        - Stronger than AC_ω
        - Weaker than full AC
        - Sufficient for most of analysis

        **Full AC**: Choice functions exist for ANY collection.
        - Implies Well-Ordering Theorem
        - Implies Banach-Tarski paradox

        Many theorems that "need AC" actually only need DC or AC_ω.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        # Part 4: Constructing Number Systems

        *"What are numbers and what should they be?"*
        — Richard Dedekind, 1888

        ---

        ## The Foundational Crisis

        In the early 1900s, mathematicians faced a crisis: **What IS a number?**

        We use numbers constantly—1, 2, 3, π, √2—but what ARE they? Where do they
        come from? How do we know they exist?

        The ancient Greeks thought numbers were God-given. But modern mathematics
        demands rigorous foundations. Enter the **set-theoretic program**:

        > Build ALL of mathematics from nothing but sets and membership (∈).

        The result is remarkable: **every number you've ever used can be constructed
        from the empty set!**

        Let's trace this construction from nothing to the real numbers.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## ℕ: Natural Numbers (Von Neumann Construction)

        We've already seen this in Part 1. The natural numbers ARE ordinals:

        $$\mathbb{N} = \omega = \{0, 1, 2, 3, \ldots\}$$

        where each number is the set of all smaller numbers:

        | Number | Set Representation |
        |--------|-------------------|
        | 0 | ∅ |
        | 1 | {∅} |
        | 2 | {∅, {∅}} |
        | 3 | {∅, {∅}, {∅, {∅}}} |
        | n | {0, 1, 2, ..., n-1} |

        ### Addition on ℕ

        Define addition recursively using the successor S(n) = n ∪ {n}:
        - $n + 0 = n$
        - $n + S(m) = S(n + m)$

        **Example**: 2 + 2 = 2 + S(1) = S(2 + 1) = S(S(2 + 0)) = S(S(2)) = S(3) = 4
        ### Multiplication on ℕ

        Define multiplication using addition:
        - $n \cdot 0 = 0$
        - $n \cdot S(m) = n \cdot m + n$

        **Theorem**: ℕ with these operations satisfies the **Peano axioms**—so
        induction works, and we have ordinary arithmetic!
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## ℤ: Integers (Adding Negatives)

        **Problem**: ℕ has no negatives. Equations like x + 3 = 1 have no solution!

        **Solution**: Represent integers as **pairs of natural numbers**.

        ### The Construction

        Consider pairs (a, b) ∈ ℕ × ℕ. Think of (a, b) as representing "a minus b."

        **Examples**:
        - (5, 3) represents 5 - 3 = 2
        - (3, 5) represents 3 - 5 = -2
        - (0, 0) represents 0 - 0 = 0

        **But wait**: (5, 3) and (7, 5) both represent 2!

        So we need an **equivalence relation**:

        $$(a, b) \sim (c, d) \iff a + d = b + c$$

        (Cross-multiply to avoid subtraction in ℕ)

        **Definition**: $\mathbb{Z} = (\mathbb{N} \times \mathbb{N}) / {\sim}$

        The integers are equivalence classes of pairs.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, np):
    # Visualize integer equivalence classes
    _fig = go.Figure()

    # Draw grid of pairs
    for _a in range(6):
        for _b in range(6):
            # Compute which integer this represents
            _val = _a - _b
            # Color by value
            if _val > 0:
                _color = COLORS["tertiary"]  # positive
            elif _val < 0:
                _color = COLORS["secondary"]  # negative
            else:
                _color = COLORS["highlight"]  # zero

            _fig.add_trace(go.Scatter(
                x=[_a], y=[_b], mode="markers",
                marker=dict(size=25, color=_color, opacity=0.7),
                showlegend=False,
            ))

    # Draw diagonal lines for equivalence classes
    for _k in range(-5, 6):
        _x0 = max(0, _k)
        _y0 = max(0, -_k)
        _x1 = min(5, 5 + _k)
        _y1 = min(5, 5 - _k)
        _fig.add_trace(go.Scatter(
            x=[_x0, _x1], y=[_y0, _y1], mode="lines",
            line=dict(color="rgba(255,255,255,0.2)", width=1),
            showlegend=False,
        ))

    # Labels
    _fig.add_annotation(x=2.5, y=-1, text="a (first component)", font=dict(size=12, color=COLORS["text_secondary"]), showarrow=False)
    _fig.add_annotation(x=-1, y=2.5, text="b", font=dict(size=12, color=COLORS["text_secondary"]), showarrow=False, textangle=-90)

    # Legend
    _fig.add_annotation(x=7, y=5, text="Positive", font=dict(size=11, color=COLORS["tertiary"]), showarrow=False)
    _fig.add_annotation(x=7, y=4, text="Zero", font=dict(size=11, color=COLORS["highlight"]), showarrow=False)
    _fig.add_annotation(x=7, y=3, text="Negative", font=dict(size=11, color=COLORS["secondary"]), showarrow=False)

    _fig.add_annotation(x=2.5, y=6.5, text="Each diagonal = one integer", font=dict(size=12, color=COLORS["primary"]), showarrow=False)

    _fig.update_layout(**base_layout(
        title=dict(text="Integers as Equivalence Classes: (a,b) ~ (c,d) iff a+d = b+c", font=dict(color=COLORS["text"], size=14)),
        xaxis=dict(visible=False, range=[-1.5, 8]),
        yaxis=dict(visible=False, range=[-1.5, 7], scaleanchor="x"),
        height=400,
    ))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        This grid displays pairs (a, b) of natural numbers, where each pair represents the integer a - b. Points are colored by their integer value: teal for positive, yellow for zero, red for negative. Each diagonal line contains all pairs representing the same integer—for example, (3,1), (4,2), and (5,3) all lie on the same diagonal and all represent 2. The integers are formally defined as these diagonal equivalence classes.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Operations on ℤ

        **Addition**: $[(a, b)] + [(c, d)] = [(a + c, b + d)]$

        *In terms of "a - b": (a-b) + (c-d) = (a+c) - (b+d)*
        **Multiplication**: $[(a, b)] \cdot [(c, d)] = [(ac + bd, ad + bc)]$

        *Check*: (a-b)(c-d) = ac - ad - bc + bd = (ac + bd) - (ad + bc)
        **Additive Inverse**: $-[(a, b)] = [(b, a)]$

        *Check*: (a-b) + (b-a) = 0
        **Theorem**: ℤ is a **ring**—it has addition, subtraction, and multiplication
        with all the expected properties (commutative, associative, distributive).

        ### Embedding ℕ into ℤ

        We embed n ∈ ℕ as [(n, 0)] ∈ ℤ. This preserves addition and multiplication,
        so ℕ ⊂ ℤ in a meaningful sense.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## ℚ: Rational Numbers (Adding Division)

        **Problem**: ℤ has no fractions. Equations like 2x = 1 have no solution!

        **Solution**: Represent rationals as **pairs of integers**.

        ### The Construction

        Consider pairs (a, b) where a ∈ ℤ and b ∈ ℤ \ {0}. Think of (a, b) as "a/b."

        **Equivalence**: $(a, b) \sim (c, d) \iff a \cdot d = b \cdot c$

        (Cross-multiply to avoid division)

        **Definition**: $\mathbb{Q} = (\mathbb{Z} \times \mathbb{Z}^*) / {\sim}$

        ### Operations on ℚ

        **Addition**: $[(a, b)] + [(c, d)] = [(ad + bc, bd)]$

        **Multiplication**: $[(a, b)] \cdot [(c, d)] = [(ac, bd)]$

        **Multiplicative Inverse**: For $[(a, b)]$ with $a \neq 0$: $[(a, b)]^{-1} = [(b, a)]$

        **Theorem**: ℚ is a **field**—every non-zero element has a multiplicative inverse!

        We can now solve 2x = 1: x = 1/2 = [(1, 2)]
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Properties We Gain at Each Level

        | System | New Capability | Key Property |
        |--------|----------------|--------------|
        | ℕ | Counting | Well-ordered, induction works |
        | ℤ | Subtraction | Additive inverses exist |
        | ℚ | Division | Multiplicative inverses for non-zero |
        | ℝ | Limits | Completeness (no gaps) |

        Each step "closes" the previous system under a new operation:
        - ℤ = ℕ closed under subtraction
        - ℚ = ℤ closed under division
        - ℝ = ℚ closed under taking limits

        **The pattern**: We identify "what's missing" (negatives, fractions, limits)
        and construct a larger system that contains it.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## ℝ: Real Numbers (Filling the Gaps)

        **Problem**: ℚ has **holes**! The equation x² = 2 has no rational solution.

        **Proof**: Suppose √2 = p/q in lowest terms. Then p² = 2q², so p² is even,
        so p is even, so p = 2k, so 4k² = 2q², so q² is even, so q is even.
        But then p/q wasn't in lowest terms. Contradiction! ∎

        The rationals are **dense** (between any two rationals there's another) but
        not **complete** (some Cauchy sequences don't converge in ℚ).

        ### Dedekind's Brilliant Solution (1872)

        **Richard Dedekind** had a beautiful insight: a real number IS a way of
        **cutting** the rationals into two pieces.

        **Definition**: A **Dedekind cut** is a partition (L, R) of ℚ where:
        1. L and R are both non-empty
        2. L has no maximum element
        3. Every element of L is less than every element of R

        **The key insight**: The "gap" between L and R IS the real number!
        """
    )
    return


@app.cell
def _(mo):
    # Interactive Dedekind cut slider
    cut_value = mo.ui.slider(
        start=0, stop=3, step=0.1, value=1.414,
        label="Cut position (approximating √2 ≈ 1.414):"
    )
    return (cut_value,)


@app.cell
def _(COLORS, base_layout, cut_value, go, np):
    # Visualize Dedekind cut
    _cut = cut_value.value
    _fig = go.Figure()

    # Draw number line
    _fig.add_trace(go.Scatter(
        x=[-0.5, 3.5], y=[0, 0], mode="lines",
        line=dict(color=COLORS["muted"], width=3),
        showlegend=False,
    ))

    # Sample rationals
    _rationals = [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3]

    for _q in _rationals:
        _color = COLORS["tertiary"] if _q < _cut else COLORS["secondary"]
        _label = "L" if _q < _cut else "R"
        _fig.add_trace(go.Scatter(
            x=[_q], y=[0], mode="markers",
            marker=dict(size=20, color=_color),
            showlegend=False,
        ))
        _fig.add_annotation(x=_q, y=-0.4, text=str(_q), font=dict(size=9, color=COLORS["text_secondary"]), showarrow=False)

    # Draw cut line
    _fig.add_trace(go.Scatter(
        x=[_cut, _cut], y=[-0.6, 0.6], mode="lines",
        line=dict(color=COLORS["highlight"], width=2, dash="dash"),
        showlegend=False,
    ))
    _fig.add_annotation(x=_cut, y=0.9, text=f"cut at {_cut:.3f}", font=dict(size=12, color=COLORS["highlight"]), showarrow=False)

    # Labels
    _fig.add_annotation(x=0.5, y=0.6, text="L (lower)", font=dict(size=12, color=COLORS["tertiary"]), showarrow=False)
    _fig.add_annotation(x=2.5, y=0.6, text="R (upper)", font=dict(size=12, color=COLORS["secondary"]), showarrow=False)

    _fig.update_layout(**base_layout(
        title=dict(text="Dedekind Cut: The gap between L and R IS the real number", font=dict(color=COLORS["text"], size=14)),
        xaxis=dict(visible=False, range=[-0.8, 4]),
        yaxis=dict(visible=False, range=[-1, 1.5]),
        height=300,
    ))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        A Dedekind cut partitions the rational numbers into two sets: L (lower, teal) containing all rationals below the cut, and R (upper, red) containing all rationals above. The dashed line marks where the cut occurs. For irrational numbers like √2, no rational sits exactly at the boundary—there's a "gap" between L and R. This gap IS the real number. By defining reals as cuts, we fill all the holes in the rationals.
        """
    )
    return


@app.cell
def _(cut_value, mo):
    mo.md(f"""
    ### Interactive: Dedekind Cut

    {cut_value}

    **For √2**, the Dedekind cut is:
    - **L** = {{q ∈ ℚ : q < 0 or q² < 2}} = "rationals whose square is less than 2"
    - **R** = {{q ∈ ℚ : q > 0 and q² > 2}} = "positive rationals whose square exceeds 2"

    No rational is at the boundary! The "gap" between L and R is √2 itself.

    Current cut approximation: **{cut_value.value:.3f}**
    - {cut_value.value:.3f}² = {cut_value.value**2:.4f}
    - Difference from 2: {abs(cut_value.value**2 - 2):.4f}
    """)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Why Dedekind Cuts Work

        **Theorem**: The set of Dedekind cuts forms a **complete ordered field**—the reals!

        **Operations**:
        - Addition: (L₁, R₁) + (L₂, R₂) = ({l₁ + l₂ : l₁ ∈ L₁, l₂ ∈ L₂}, ...)
        - Multiplication: More complex, handle signs carefully
        - Order: (L₁, R₁) < (L₂, R₂) iff L₁ ⊂ L₂

        **Completeness**: Every non-empty bounded set of cuts has a supremum (just take the union of all the L parts).

        **The real numbers are cuts in the rationals!**

        ### Alternative: Cauchy Sequences

        Another way to construct ℝ: take equivalence classes of Cauchy sequences in ℚ.

        Two sequences (aₙ) and (bₙ) are equivalent if |aₙ - bₙ| → 0.

        **√2** = the equivalence class of (1, 1.4, 1.41, 1.414, 1.4142, ...)

        Both constructions give the same ℝ (they're isomorphic).
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go):
    # Number system tower visualization
    _fig = go.Figure()

    _levels = [
        ("ℕ", 0, COLORS["tertiary"], "Natural numbers: 0, 1, 2, 3, ..."),
        ("ℤ", 1, COLORS["primary"], "Integers: ..., -2, -1, 0, 1, 2, ..."),
        ("ℚ", 2, COLORS["secondary"], "Rationals: fractions p/q"),
        ("ℝ", 3, COLORS["highlight"], "Reals: Dedekind cuts"),
    ]

    for _name, _y, _color, _desc in _levels:
        # Box
        _fig.add_shape(
            type="rect", x0=-2, x1=2, y0=_y - 0.35, y1=_y + 0.35,
            fillcolor=_color, opacity=0.2,
            line=dict(color=_color, width=2),
        )
        # Label
        _fig.add_annotation(x=-1.5, y=_y, text=_name, font=dict(size=24, color=_color), showarrow=False)
        _fig.add_annotation(x=0.5, y=_y, text=_desc, font=dict(size=11, color=COLORS["text_secondary"]), showarrow=False)

    # Inclusion arrows
    for _i in range(3):
        _fig.add_annotation(
            x=-1.5, y=_i + 0.6, ax=-1.5, ay=_i + 0.4,
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=2, arrowcolor=COLORS["text_secondary"],
        )

    _fig.add_annotation(x=-3, y=1.5, text="⊂", font=dict(size=30, color=COLORS["text_secondary"]), showarrow=False, textangle=90)

    _fig.update_layout(**base_layout(
        title=dict(text="The Number System Tower: Built from ∅", font=dict(color=COLORS["text"], size=16)),
        xaxis=dict(visible=False, range=[-4, 4]),
        yaxis=dict(visible=False, range=[-0.8, 4]),
        height=400,
    ))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The "number system tower" shows how each number system contains the previous one: natural numbers ℕ at the base, then integers ℤ (adding negatives), then rationals ℚ (adding fractions), then reals ℝ (filling gaps). Every level is built from sets—ultimately, even complex numbers trace back to the empty set ∅ through this construction.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        # Part 5: Advanced Function Topics

        *"A function space is the set of ALL possible functions between two sets."*

        ---

        ## Function Spaces

        We've seen that |B^A| = |B|^|A|. But what IS B^A as a set?

        **Definition**: The **function space** (or exponential) is:

        $$B^A = \{f : f \text{ is a function from } A \text{ to } B\}$$

        ### Examples

        **{0, 1}^{a, b}** = all functions from {a, b} to {0, 1}:

        | f | f(a) | f(b) |
        |---|------|------|
        | f₁ | 0 | 0 |
        | f₂ | 0 | 1 |
        | f₃ | 1 | 0 |
        | f₄ | 1 | 1 |

        There are 2² = 4 such functions.
        **Important Example**: $\{0, 1\}^\mathbb{N}$ = all infinite binary sequences

        This has cardinality $2^{\aleph_0} = \mathfrak{c}$ (the continuum).

        **Each binary sequence corresponds to a real number in [0, 1]!**
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go):
    # Visualize function space
    _fig = go.Figure()

    # Domain {a, b, c}
    _domain = ["a", "b", "c"]
    # Codomain {0, 1}
    _codomain = ["0", "1"]

    # Show a few sample functions
    _functions = [
        ("f₁", {"a": "0", "b": "0", "c": "0"}),
        ("f₂", {"a": "0", "b": "0", "c": "1"}),
        ("f₃", {"a": "0", "b": "1", "c": "0"}),
        ("f₄", {"a": "1", "b": "1", "c": "1"}),
    ]

    for _fi, (_fname, _fmap) in enumerate(_functions):
        _base_x = _fi * 3

        # Draw domain
        for _di, _d in enumerate(_domain):
            _fig.add_trace(go.Scatter(
                x=[_base_x], y=[2 - _di], mode="markers+text",
                marker=dict(size=25, color=COLORS["tertiary"]),
                text=[_d], textposition="middle center",
                textfont=dict(size=12, color=COLORS["background"]),
                showlegend=False,
            ))

        # Draw codomain
        for _ci, _c in enumerate(_codomain):
            _fig.add_trace(go.Scatter(
                x=[_base_x + 1.5], y=[1.5 - _ci], mode="markers+text",
                marker=dict(size=25, color=COLORS["secondary"]),
                text=[_c], textposition="middle center",
                textfont=dict(size=12, color=COLORS["background"]),
                showlegend=False,
            ))

        # Draw arrows
        for _di, _d in enumerate(_domain):
            _target = _fmap[_d]
            _ti = _codomain.index(_target)
            _fig.add_annotation(
                x=_base_x + 1.3, y=1.5 - _ti,
                ax=_base_x + 0.2, ay=2 - _di,
                xref="x", yref="y", axref="x", ayref="y",
                showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=1.5, arrowcolor=COLORS["primary"],
            )

        # Function name
        _fig.add_annotation(x=_base_x + 0.75, y=3, text=_fname, font=dict(size=12, color=COLORS["highlight"]), showarrow=False)

    _fig.add_annotation(x=5.5, y=-1, text="...and 4 more functions (2³ = 8 total)", font=dict(size=11, color=COLORS["text_secondary"]), showarrow=False)

    _fig.update_layout(**base_layout(
        title=dict(text="Function Space {0,1}^{a,b,c}: All 8 Functions", font=dict(color=COLORS["text"], size=14)),
        xaxis=dict(visible=False, range=[-1, 12]),
        yaxis=dict(visible=False, range=[-2, 4]),
        height=350,
    ))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Four different functions from the domain {a, b, c} to the codomain {0, 1} are displayed side by side. Each function is a complete assignment—every element in the domain has exactly one arrow going to the codomain. With 3 domain elements and 2 codomain values, there are 2³ = 8 possible functions total. The function space {0,1}^{a,b,c} is the set containing all 8 of these functions.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The Schröder-Bernstein Theorem

        One of the most useful theorems in set theory:

        **Theorem** (Schröder-Bernstein, 1898): If there exist injections
        $f: A \to B$ and $g: B \to A$, then $|A| = |B|$.

        **In plain English**: If A "fits inside" B (with room to spare), and B "fits
        inside" A (with room to spare), then A and B have the same size!

        ### Why This is Surprising

        Having two one-way injections doesn't obviously give you a bijection.
        For example:
        - f might miss some elements of B
        - g might miss some elements of A
        - But somehow, we can build a perfect matching!

        ### The Proof Idea

        1. **Follow the chains**: Start from any element and follow the mappings
           f and g alternately. Each element belongs to a "chain."

        2. **Classify chains**: Each chain either:
           - Extends infinitely in both directions
           - Has a "starting point" in A
           - Has a "starting point" in B

        3. **Build the bijection**:
           - For chains starting in A or infinite: use f
           - For chains starting in B: use g⁻¹

        This carefully constructed bijection proves |A| = |B|.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go):
    # Schröder-Bernstein visualization
    # Show two sets of the same infinite cardinality (represented finitely)
    # with injections in both directions
    _fig = go.Figure()

    # Set A: even numbers {0, 2, 4, 6, ...} represented by first few
    _A = ["0", "2", "4", "6"]
    _A_y = [3, 2, 1, 0]

    # Set B: natural numbers {0, 1, 2, 3, ...} represented by first few
    _B = ["0", "1", "2", "3", "4"]
    _B_y = [3.5, 2.5, 1.5, 0.5, -0.5]

    # Draw A (evens)
    for _i, (_a, _y) in enumerate(zip(_A, _A_y)):
        _fig.add_trace(go.Scatter(
            x=[0], y=[_y], mode="markers+text",
            marker=dict(size=30, color=COLORS["tertiary"]),
            text=[_a], textposition="middle center",
            textfont=dict(size=12, color=COLORS["background"]),
            showlegend=False,
        ))

    # Draw B (naturals)
    for _i, (_b, _y) in enumerate(zip(_B, _B_y)):
        _fig.add_trace(go.Scatter(
            x=[4], y=[_y], mode="markers+text",
            marker=dict(size=30, color=COLORS["secondary"]),
            text=[_b], textposition="middle center",
            textfont=dict(size=12, color=COLORS["background"]),
            showlegend=False,
        ))

    # Injection f: A → B (inclusion: 0→0, 2→2, 4→4, 6→6) - evens into naturals
    _f_arrows = [(0, 0), (1, 2), (2, 4)]  # 0→0, 2→2, 4→4
    for _ai, _bi in _f_arrows:
        _fig.add_annotation(
            x=3.7, y=_B_y[_bi], ax=0.3, ay=_A_y[_ai],
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=2, arrowsize=1.2, arrowwidth=2, arrowcolor=COLORS["primary"],
        )

    # Labels
    _fig.add_annotation(x=0, y=4.2, text="A = Evens", font=dict(size=12, color=COLORS["tertiary"]), showarrow=False)
    _fig.add_annotation(x=4, y=4.2, text="B = ℕ", font=dict(size=12, color=COLORS["secondary"]), showarrow=False)
    _fig.add_annotation(x=2, y=4.2, text="f: n ↦ n", font=dict(size=11, color=COLORS["primary"]), showarrow=False)
    _fig.add_annotation(x=2, y=-1.5, text="f: A ↪ B (inclusion)", font=dict(size=10, color=COLORS["primary"]), showarrow=False)
    _fig.add_annotation(x=2, y=-2, text="g: B ↪ A (n ↦ 2n)", font=dict(size=10, color=COLORS["highlight"]), showarrow=False)
    _fig.add_annotation(x=2, y=-2.7, text="Both injections exist ⟹ |A| = |B|", font=dict(size=11, color=COLORS["text_secondary"]), showarrow=False)

    _fig.update_layout(**base_layout(
        title=dict(text="Schröder-Bernstein: Evens ↔ Naturals", font=dict(color=COLORS["text"], size=14)),
        xaxis=dict(visible=False, range=[-1, 5]),
        yaxis=dict(visible=False, range=[-3.5, 5]),
        height=400,
    ))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The set A (even numbers) and set B (all natural numbers) are shown with an injection f from A to B (inclusion: each even maps to itself in ℕ). There's also an injection g from B to A (doubling: each natural maps to an even). Despite A being a "proper subset" of B, these two injections prove |A| = |B| by the Schröder-Bernstein theorem—both sets have the same infinite cardinality.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Application: |(0,1)| = |ℝ|

        We can prove the open interval (0, 1) has the same cardinality as ℝ
        using Schröder-Bernstein.

        **Injection f: (0, 1) → ℝ**: Just inclusion! Every x ∈ (0, 1) is also in ℝ.

        **Injection g: ℝ → (0, 1)**: Use $g(x) = \frac{1}{\pi}\arctan(x) + \frac{1}{2}$

        This maps all of ℝ into (0, 1):
        - g(-∞) → 0 (limit)
        - g(0) = 0.5
        - g(+∞) → 1 (limit)

        By Schröder-Bernstein, |(0, 1)| = |ℝ|.
        **We didn't need to find the explicit bijection!** The theorem guarantees
        one exists, even if we never write it down.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Fixed Points

        **Definition**: A **fixed point** of function f: A → A is an element x ∈ A
        where f(x) = x.

        The element stays in place under the function!

        ### Graphical Interpretation

        For f: ℝ → ℝ, fixed points are where the graph y = f(x) intersects y = x.

        **Examples**:
        - f(x) = x²: Fixed points at x = 0 and x = 1 (since 0² = 0 and 1² = 1)
        - f(x) = 2x: Only fixed point is x = 0
        - f(x) = x + 1: No fixed points! (x ≠ x + 1 for any x)

        ### Why Fixed Points Matter

        1. **Equilibria**: In dynamical systems, fixed points are stable states
        2. **Solutions**: Equation x = f(x) is solved by fixed points
        3. **Recursion**: Recursive definitions are fixed points of "definition operators"
        4. **Computer Science**: Denotational semantics, program analysis

        We'll see a powerful fixed-point theorem in the next section!
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, np):
    # Visualize fixed points
    _fig = go.Figure()

    _x = np.linspace(-0.5, 2, 200)

    # f(x) = x²
    _y_f = _x ** 2

    # y = x line
    _y_id = _x

    _fig.add_trace(go.Scatter(x=_x, y=_y_f, mode="lines", name="f(x) = x²", line=dict(color=COLORS["tertiary"], width=2)))
    _fig.add_trace(go.Scatter(x=_x, y=_y_id, mode="lines", name="y = x", line=dict(color=COLORS["secondary"], width=2, dash="dash")))

    # Mark fixed points
    _fig.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1], mode="markers",
        marker=dict(size=15, color=COLORS["highlight"], symbol="star"),
        name="Fixed points",
    ))

    _fig.add_annotation(x=0, y=-0.15, text="x=0", font=dict(size=11, color=COLORS["highlight"]), showarrow=False)
    _fig.add_annotation(x=1, y=1.15, text="x=1", font=dict(size=11, color=COLORS["highlight"]), showarrow=False)

    _fig.update_layout(**base_layout(
        title=dict(text="Fixed Points: Where f(x) = x", font=dict(color=COLORS["text"], size=16)),
        xaxis=dict(title="x", color=COLORS["text_secondary"], gridcolor="rgba(255,255,255,0.1)", range=[-0.5, 2]),
        yaxis=dict(title="y", color=COLORS["text_secondary"], gridcolor="rgba(255,255,255,0.1)", range=[-0.5, 2.5]),
        height=400,
    ))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The graph of f(x) = x² (teal curve) intersects the diagonal line y = x (red dashed) at two points: x = 0 and x = 1. These intersection points are the fixed points—values where f(x) = x. At x = 0, we have 0² = 0; at x = 1, we have 1² = 1. Fixed points are equilibrium states: applying the function doesn't change them.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        # Part 6: Lattice Theory

        *"A lattice is a poset where any two elements have a greatest lower bound and least upper bound."*

        ---

        ## Historical Context

        **Richard Dedekind** (1897) first studied these structures, calling them "Dualgruppen."
        **Garrett Birkhoff** developed modern lattice theory in the 1930s.

        Lattices appear everywhere:
        - Power sets ordered by inclusion
        - Integers ordered by divisibility
        - Subspaces of vector spaces
        - Propositions ordered by logical implication
        - Types in programming languages

        They're fundamental to **domain theory** in computer science, where they
        provide semantics for recursive definitions and programming languages.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Lattice Definition

        A **lattice** is a partially ordered set (L, ≤) where every pair of elements
        has both:

        - A **meet** (greatest lower bound): a ∧ b
        - A **join** (least upper bound): a ∨ b

        ### Meet and Join

        **Meet** a ∧ b is the largest element that is ≤ both a and b.
        - Think: "AND" or "intersection"

        **Join** a ∨ b is the smallest element that is ≥ both a and b.
        - Think: "OR" or "union"

        ### Examples

        | Lattice | Order | Meet | Join |
        |---------|-------|------|------|
        | (P(S), ⊆) | Inclusion | Intersection ∩ | Union ∪ |
        | (ℕ, ∣) | Divisibility | GCD | LCM |
        | ({T, F}, ⟹) | Implication | AND | OR |
        | Subspaces of V | Inclusion | Intersection | Span |
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go):
    # Visualize the power set lattice P({a,b})
    _fig = go.Figure()

    # Elements of P({a,b}) with positions
    _elements = {
        "∅": (0, 0),
        "{a}": (-1, 1),
        "{b}": (1, 1),
        "{a,b}": (0, 2),
    }

    # Edges (Hasse diagram)
    _edges = [("∅", "{a}"), ("∅", "{b}"), ("{a}", "{a,b}"), ("{b}", "{a,b}")]

    # Draw edges
    for _a, _b in _edges:
        _x0, _y0 = _elements[_a]
        _x1, _y1 = _elements[_b]
        _fig.add_trace(go.Scatter(
            x=[_x0, _x1], y=[_y0, _y1], mode="lines",
            line=dict(color=COLORS["muted"], width=2),
            showlegend=False,
        ))

    # Draw nodes
    for _name, (_x, _y) in _elements.items():
        _fig.add_trace(go.Scatter(
            x=[_x], y=[_y], mode="markers+text",
            marker=dict(size=40, color=COLORS["tertiary"]),
            text=[_name], textposition="middle center",
            textfont=dict(size=11, color=COLORS["background"]),
            showlegend=False,
        ))

    # Annotations for meet and join
    _fig.add_annotation(x=-2, y=1, text="{a} ∧ {b} = ∅\n(intersection)", font=dict(size=10, color=COLORS["secondary"]), showarrow=False, align="left")
    _fig.add_annotation(x=2, y=1, text="{a} ∨ {b} = {a,b}\n(union)", font=dict(size=10, color=COLORS["primary"]), showarrow=False, align="left")

    _fig.update_layout(**base_layout(
        title=dict(text="Power Set Lattice P({a,b})", font=dict(color=COLORS["text"], size=16)),
        xaxis=dict(visible=False, range=[-3.5, 3.5]),
        yaxis=dict(visible=False, range=[-0.5, 3]),
        height=350,
    ))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        This Hasse diagram displays the power set P({a,b}) ordered by inclusion. At the bottom is ∅ (empty set), at the top is {a,b} (the full set), and in the middle are the singletons {a} and {b}. Lines indicate the subset relation. The meet (greatest lower bound) of {a} and {b} is ∅ (their intersection), while their join (least upper bound) is {a,b} (their union). This is a complete lattice with four elements.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Lattice Properties

        ### Distributive Lattices

        A lattice is **distributive** if:
        $$a \wedge (b \vee c) = (a \wedge b) \vee (a \wedge c)$$
        $$a \vee (b \wedge c) = (a \vee b) \wedge (a \vee c)$$

        "Meet distributes over join, and vice versa."

        **Example**: Power sets P(S) are always distributive.

        ### Modular Lattices

        A lattice is **modular** if: whenever a ≤ c,
        $$a \vee (b \wedge c) = (a \vee b) \wedge c$$

        This is weaker than distributivity.

        **Example**: The lattice of subspaces of a vector space is modular but NOT distributive.

        ### Forbidden Sublattices

        - A lattice contains the **pentagon N₅** ⟹ NOT modular
        - A lattice contains the **diamond M₃** ⟹ NOT distributive (but may be modular)

        These "forbidden sublattices" characterize the properties!
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Why Distributivity Matters

        In a **distributive lattice**, we can simplify expressions just like in
        ordinary algebra:

        $$a \wedge (b \vee c) = (a \wedge b) \vee (a \wedge c)$$

        This is analogous to: $a \cdot (b + c) = a \cdot b + a \cdot c$

        **Boolean algebras** are distributive lattices with complements—they model:
        - Propositional logic (AND, OR, NOT)
        - Set operations (∩, ∪, complement)
        - Digital circuits (AND gates, OR gates)

        **Example of non-distributivity**: In the diamond M₃:
        - a ∧ (b ∨ c) = a ∧ 1 = a
        - (a ∧ b) ∨ (a ∧ c) = 0 ∨ 0 = 0

        Since a ≠ 0, the distributive law fails!
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, make_subplots):
    # Show N5 (pentagon) and M3 (diamond)
    _fig = make_subplots(rows=1, cols=2, subplot_titles=["N₅ (Pentagon) - Not Modular", "M₃ (Diamond) - Not Distributive"])

    # N5 Pentagon: 0 < a < b < 1, and separately 0 < c < 1, with c incomparable to a,b
    _n5_nodes = {"0": (0, 0), "a": (-0.5, 1), "b": (-0.5, 2), "c": (0.5, 1.5), "1": (0, 3)}
    _n5_edges = [("0", "a"), ("a", "b"), ("b", "1"), ("0", "c"), ("c", "1")]

    for _a, _b in _n5_edges:
        _x0, _y0 = _n5_nodes[_a]
        _x1, _y1 = _n5_nodes[_b]
        _fig.add_trace(go.Scatter(x=[_x0, _x1], y=[_y0, _y1], mode="lines", line=dict(color=COLORS["muted"], width=2), showlegend=False), row=1, col=1)

    for _name, (_x, _y) in _n5_nodes.items():
        _fig.add_trace(go.Scatter(x=[_x], y=[_y], mode="markers+text", marker=dict(size=30, color=COLORS["secondary"]), text=[_name], textposition="middle center", textfont=dict(size=12, color=COLORS["background"]), showlegend=False), row=1, col=1)

    # M3 Diamond
    _m3_nodes = {"0": (0, 0), "a": (-0.7, 1), "b": (0, 1), "c": (0.7, 1), "1": (0, 2)}
    _m3_edges = [("0", "a"), ("0", "b"), ("0", "c"), ("a", "1"), ("b", "1"), ("c", "1")]

    for _a, _b in _m3_edges:
        _x0, _y0 = _m3_nodes[_a]
        _x1, _y1 = _m3_nodes[_b]
        _fig.add_trace(go.Scatter(x=[_x0, _x1], y=[_y0, _y1], mode="lines", line=dict(color=COLORS["muted"], width=2), showlegend=False), row=1, col=2)

    for _name, (_x, _y) in _m3_nodes.items():
        _fig.add_trace(go.Scatter(x=[_x], y=[_y], mode="markers+text", marker=dict(size=30, color=COLORS["highlight"]), text=[_name], textposition="middle center", textfont=dict(size=12, color=COLORS["background"]), showlegend=False), row=1, col=2)

    _fig.update_xaxes(visible=False, range=[-1.5, 1.5])
    _fig.update_yaxes(visible=False, range=[-0.5, 3.5])
    _fig.update_layout(**base_layout(
        title=dict(text="Forbidden Sublattices", font=dict(color=COLORS["text"], size=16)),
        height=350,
    ))
    _fig.update_annotations(font=dict(color=COLORS["text"]))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Two "forbidden sublattices" that characterize lattice properties. The pentagon N₅ (left) has elements where the modular law fails—if a lattice contains N₅ as a sublattice, it's not modular. The diamond M₃ (right) has three incomparable middle elements—if a lattice contains M₃, it's not distributive. These small structures act as "obstructions" that reveal what properties a lattice lacks.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Complete Lattices

        A lattice is **complete** if EVERY subset (not just pairs) has a supremum and infimum.

        This means:
        - There's a **top element** ⊤ = sup(L) (the join of everything)
        - There's a **bottom element** ⊥ = inf(L) (the meet of everything)
        - Every subset S has sup(S) and inf(S)

        ### Examples

        | Lattice | Complete? | Notes |
        |---------|-----------|-------|
        | P(S) with ⊆ | **Yes** | ⊤ = S, ⊥ = ∅ |
        | [0, 1] with ≤ | **Yes** | ⊤ = 1, ⊥ = 0 |
        | (ℕ, ≤) | **No** | No top element! |
        | (ℕ, ∣) | **No** | No top element |

        Complete lattices are the natural setting for the powerful
        **Knaster-Tarski Fixed-Point Theorem**.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Examples of Complete Lattices

        **1. Power Sets P(S)**
        - ⊤ = S (the whole set)
        - ⊥ = ∅ (empty set)
        - sup(F) = ∪F (union of all sets in F)
        - inf(F) = ∩F (intersection of all sets in F)

        **2. Closed Intervals [a, b] ⊆ ℝ**
        - ⊤ = b
        - ⊥ = a
        - sup(S) = usual supremum (exists because bounded)
        - inf(S) = usual infimum

        **3. Divisibility on {1, 2, 3, 6} (divisors of 6)**
        - ⊤ = 6 (everything divides 6)
        - ⊥ = 1 (1 divides everything)
        - Complete because finite

        **NOT Complete: (ℕ, ≤)**
        - No top element! sup(ℕ) doesn't exist in ℕ.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The Knaster-Tarski Fixed-Point Theorem

        **Theorem** (Knaster-Tarski, 1928): Let L be a complete lattice and
        f: L → L be **monotone** (order-preserving: x ≤ y ⟹ f(x) ≤ f(y)).

        Then:
        1. f has at least one fixed point
        2. The set of fixed points Fix(f) is itself a complete lattice!

        ### The Proof Idea

        Let S = {x ∈ L : x ≤ f(x)} — elements that are "below their image."

        Let s = sup(S).

        **Claim**: f(s) = s.

        **Proof**:
        - For any x ∈ S: x ≤ s, so f(x) ≤ f(s) (monotonicity). Since x ≤ f(x),
          we have x ≤ f(s). So f(s) is an upper bound for S.
        - Since s = sup(S), we have s ≤ f(s).
        - So s ∈ S! Thus f(s) is an upper bound for S, hence s ≤ f(s).
        - But f(s) ≤ f(f(s)) (since s ≤ f(s) and f is monotone), so f(s) ∈ S.
        - Since s = sup(S) and f(s) ∈ S, we have f(s) ≤ s.
        - Therefore f(s) = s. ∎
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, np):
    # Visualize Knaster-Tarski iteration
    _fig = go.Figure()

    # Example: f(x) = sqrt(x) on [0, 1], starting from 0
    def _f(x):
        return np.sqrt(x) if x >= 0 else 0

    _x = 0.1
    _points = [_x]
    for _ in range(8):
        _x = _f(_x)
        _points.append(_x)

    # Draw lattice as [0, 1] interval
    _fig.add_trace(go.Scatter(
        x=[0, 1], y=[0, 0], mode="lines",
        line=dict(color=COLORS["muted"], width=4),
        showlegend=False,
    ))

    # Show iterations
    for _i, _p in enumerate(_points):
        _fig.add_trace(go.Scatter(
            x=[_p], y=[0], mode="markers",
            marker=dict(size=15 - _i, color=f"rgba(78, 205, 196, {1 - _i * 0.1})"),
            showlegend=False,
        ))
        if _i < 5:
            _fig.add_annotation(x=_p, y=0.15 + 0.1 * (_i % 2), text=f"f^{_i}(x₀)", font=dict(size=9, color=COLORS["text_secondary"]), showarrow=False)

    # Fixed point
    _fig.add_trace(go.Scatter(
        x=[1], y=[0], mode="markers",
        marker=dict(size=20, color=COLORS["secondary"], symbol="star"),
        name="Fixed point",
    ))
    _fig.add_annotation(x=1, y=-0.2, text="Fixed point: 1", font=dict(size=11, color=COLORS["secondary"]), showarrow=False)

    _fig.add_annotation(x=0.5, y=0.5, text="Iterating f(x) = √x from x₀ = 0.1", font=dict(size=12, color=COLORS["primary"]), showarrow=False)
    _fig.add_annotation(x=0.5, y=0.35, text="Converges to fixed point at x = 1", font=dict(size=11, color=COLORS["text_secondary"]), showarrow=False)

    _fig.update_layout(**base_layout(
        title=dict(text="Knaster-Tarski: Monotone Functions on Complete Lattices Have Fixed Points", font=dict(color=COLORS["text"], size=14)),
        xaxis=dict(title="[0, 1]", color=COLORS["text_secondary"], range=[-0.1, 1.2]),
        yaxis=dict(visible=False, range=[-0.4, 0.8]),
        height=300,
    ))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Starting from x₀ = 0.1 on the interval [0, 1], we repeatedly apply f(x) = √x. Each iteration moves us closer to the fixed point at x = 1 (marked with a star). The shrinking circles show the progression: f⁰(x₀), f¹(x₀), f²(x₀), etc. The Knaster-Tarski theorem guarantees that any monotone function on a complete lattice has such a fixed point, and iteration will converge to it.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Applications of Knaster-Tarski

        1. **Recursive Definitions**: Define factorial as the least fixed point of
           F(f)(n) = if n = 0 then 1 else n · f(n-1)

        2. **Denotational Semantics**: The meaning of a recursive program is the
           least fixed point of a "semantic operator"

        3. **Static Analysis**: Dataflow analysis computes fixed points of
           transfer functions on lattices of program states

        4. **Type Systems**: Type inference finds fixed points of constraint systems

        5. **Database Theory**: Recursive queries compute fixed points of operators

        The theorem guarantees these fixed points **exist**, even when we can't
        compute them directly!
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### The Least Fixed Point

        Knaster-Tarski actually gives us more: there's a **least** fixed point and a
        **greatest** fixed point.

        **Least Fixed Point (lfp)**:
        $$\text{lfp}(f) = \inf\{x : f(x) \leq x\}$$

        This is the smallest element x where f doesn't push us higher.

        **Greatest Fixed Point (gfp)**:
        $$\text{gfp}(f) = \sup\{x : x \leq f(x)\}$$

        This is the largest element x where f doesn't push us lower.

        **In computer science:**
        - lfp corresponds to "least defined" recursive definitions (partial functions)
        - gfp corresponds to "most defined" coinductive definitions (infinite data)

        For example, in a static analyzer:
        - lfp finds the smallest set of possible values (most precise analysis)
        - gfp finds the largest set of safe assumptions
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        # Summary and Connections

        ---

        ## What We've Learned

        | Topic | Key Insight |
        |-------|-------------|
        | **Ordinals** | Positions in well-orderings; enable transfinite induction |
        | **Cardinals** | Sizes of infinite sets; not all infinities are equal |
        | **Axiom of Choice** | Guarantees choice functions; equivalent to Zorn & Well-Ordering |
        | **Number Construction** | All numbers built from ∅ using sets |
        | **Function Spaces** | B^A = all functions A → B; connects to cardinality |
        | **Schröder-Bernstein** | Two injections imply bijection |
        | **Lattices** | Posets with meets and joins; foundation for CS theory |
        | **Knaster-Tarski** | Monotone functions on complete lattices have fixed points |

        ## Key Formulas

        | Concept | Formula |
        |---------|---------|
        | Successor ordinal | S(α) = α ∪ {α} |
        | Cantor pairing | π(m,n) = ½(m+n)(m+n+1) + n |
        | Cantor's theorem | \|A\| < \|P(A)\| always |
        | Cardinal power | \|B^A\| = \|B\|^{\|A\|} |
        | Dedekind cut for √2 | L = {q ∈ ℚ : q < 0 or q² < 2} |
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Historical Timeline

        | Year | Event |
        |------|-------|
        | **1872** | Dedekind cuts formalized |
        | **1874** | Cantor proves ℝ is uncountable |
        | **1883** | Transfinite ordinals introduced |
        | **1888** | Dedekind: "Was sind und was sollen die Zahlen?" |
        | **1891** | Cantor's diagonal argument |
        | **1898** | Schröder-Bernstein theorem |
        | **1901** | Russell's paradox discovered |
        | **1904** | Zermelo's well-ordering theorem (using AC) |
        | **1908** | Zermelo's axiomatization of set theory |
        | **1923** | Von Neumann ordinals |
        | **1928** | Knaster-Tarski fixed-point theorem |
        | **1940** | Gödel: CH consistent with ZFC |
        | **1963** | Cohen: CH independent of ZFC |
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The Big Picture: Why This Matters

        **For Foundations**: Set theory provides the common language for all mathematics.
        Every mathematical object—numbers, functions, spaces, groups—can be encoded as a set.

        **For Logic**: Ordinals measure proof complexity. The ordinal of a theory tells us
        how "strong" its induction principles are.

        **For Computer Science**: Lattices and fixed points are the mathematics of
        computation. They explain how recursive definitions work and how we can
        reason about programs.

        **For Philosophy**: The Continuum Hypothesis shows that mathematics has genuine
        limits. Some questions cannot be answered—not because we're not clever enough,
        but because the axioms themselves don't determine the answer.

        **The remarkable unity**: Cantor's seemingly abstract questions about infinity
        turn out to connect deeply to practical questions about computation, logic,
        and the nature of mathematical truth.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Connections to Other Mathematics

        **Ordinals in Proof Theory**: Ordinal analysis measures the "strength" of
        mathematical theories by their proof-theoretic ordinals.

        **Cardinals in Topology**: The weight of a topological space, the density
        character, and other cardinal invariants classify spaces.

        **Lattices in Computer Science**:
        - Domain theory (denotational semantics)
        - Type systems and subtyping
        - Static analysis and abstract interpretation
        - Database query optimization

        **Fixed Points in Programming**:
        - Recursive function definitions
        - Least/greatest fixed point semantics
        - Model checking and verification

        ## Further Reading

        **Primary Sources**:
        - Cantor's papers on transfinite numbers
        - Dedekind's "Was sind und was sollen die Zahlen?"
        - Zermelo's 1908 axiomatization

        **Modern Textbooks**:
        - Kunen: "Set Theory: An Introduction to Independence Proofs"
        - Jech: "Set Theory" (the comprehensive reference)
        - Enderton: "Elements of Set Theory" (accessible introduction)

        **Video Resources**:
        - 3Blue1Brown: "How big is infinity?"
        - Numberphile: Cantor's diagonal argument
        - PBS Infinite Series: Ordinal numbers
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        *"The essence of mathematics lies in its freedom."*
        — Georg Cantor

        *"No one shall expel us from the Paradise that Cantor has created."*
        — David Hilbert

        ---

        In this notebook, we've journeyed through Cantor's paradise—a realm where
        infinities come in different sizes, where numbers are built from nothing,
        and where the Axiom of Choice opens doors to both profound theorems and
        bewildering paradoxes.

        These ideas form the foundation of modern mathematics. Every time you use
        a real number, invoke a function, or reason about infinite structures,
        you're standing on the shoulders of Cantor, Dedekind, Zermelo, and the
        other pioneers who dared to take infinity seriously.

        **Next**: Explore linear algebra, where we'll see vector spaces, linear
        transformations, and the geometric structures that underpin physics,
        computer graphics, and machine learning.
        """
    )
    return


if __name__ == "__main__":
    app.run()
