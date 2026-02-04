"""
Set Theory: The Foundation of Modern Mathematics

An exploration of sets, their axioms, operations,
relations, and the structures that underpin all of mathematics.
"""

import marimo

__generated_with = "0.19.6"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
        # Set Theory: The Foundation of Modern Mathematics

        *"A set is a Many that allows itself to be thought of as a One."*
        — Georg Cantor (1883)

        ---

        Set theory is the **bedrock** upon which all of modern mathematics is built.
        Numbers, functions, geometric spaces, algebraic structures—everything can be
        constructed from sets and their relationships.

        In this notebook, we'll explore:
        - **What sets are** and how to describe them
        - **The axioms** that govern set theory (ZFC)
        - **Operations** on sets: union, intersection, complement
        - **Relations and functions**: mappings between sets
        - **Identity elements**: the special "zero-like" elements
        - **Transitivity** and other fundamental properties
        - **How elements move** between sets through functions

        Let's build mathematics from the ground up.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The Birth of Set Theory: A Historical Journey

        ### Georg Cantor's Revolution (1870s-1880s)

        **Georg Cantor (1845-1918)** created set theory while studying trigonometric series.
        His radical idea: treat infinite collections as completed mathematical objects.

        Before Cantor, mathematicians viewed infinity as a *process* (always growing).
        Cantor showed we could compare different *sizes* of infinity—a shocking discovery
        that revolutionized mathematics but was met with fierce opposition.

        **Leopold Kronecker** famously attacked Cantor's work, calling him a "corrupter
        of youth." Despite this, Cantor's ideas eventually triumphed.

        ### Russell's Paradox (1901)

        **Bertrand Russell** discovered a devastating paradox in naive set theory.
        Consider the set $R$ of all sets that do not contain themselves:

        $$R = \{x : x \notin x\}$$

        **Question**: Is $R \in R$?

        - If $R \in R$, then by definition of $R$, we have $R \notin R$. Contradiction!
        - If $R \notin R$, then by definition of $R$, we have $R \in R$. Contradiction!

        This paradox showed that naive "anything goes" set theory leads to contradictions.

        ### The Axiomatization (1908-1922)

        **Ernst Zermelo** and **Abraham Fraenkel** developed a careful axiomatic
        foundation for set theory, now called **ZFC** (Zermelo-Fraenkel with Choice).
        These axioms restrict what sets can exist, avoiding paradoxes while preserving
        the power to do mathematics.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What is a Set?

        ### The Intuitive Definition

        A **set** is a well-defined collection of distinct objects, called **elements**
        or **members**. We write $a \in A$ to mean "$a$ is an element of $A$."

        ### Notation and Examples

        | Notation | Meaning | Example |
        |----------|---------|---------|
        | $\{a, b, c\}$ | Set with elements $a, b, c$ | $\{1, 2, 3\}$ |
        | $\{x : P(x)\}$ | Set of $x$ satisfying property $P$ | $\{x : x > 0\}$ |
        | $a \in A$ | $a$ is a member of $A$ | $2 \in \{1, 2, 3\}$ |
        | $a \notin A$ | $a$ is not a member of $A$ | $4 \notin \{1, 2, 3\}$ |
        | $\emptyset$ or $\{\}$ | The empty set | $\{x : x \neq x\}$ |
        | $A \subseteq B$ | $A$ is a subset of $B$ | $\{1, 2\} \subseteq \{1, 2, 3\}$ |
        | $A = B$ | Sets are equal | $\{1, 2\} = \{2, 1\}$ |

        ### Key Properties

        1. **Order doesn't matter**: $\{1, 2, 3\} = \{3, 1, 2\}$
        2. **No duplicates**: $\{1, 1, 2\} = \{1, 2\}$
        3. **Elements can be anything**: numbers, functions, even other sets!

        ### Important Sets

        | Symbol | Name | Elements |
        |--------|------|----------|
        | $\mathbb{N}$ | Natural numbers | $\{0, 1, 2, 3, \ldots\}$ |
        | $\mathbb{Z}$ | Integers | $\{\ldots, -2, -1, 0, 1, 2, \ldots\}$ |
        | $\mathbb{Q}$ | Rational numbers | $\{p/q : p, q \in \mathbb{Z}, q \neq 0\}$ |
        | $\mathbb{R}$ | Real numbers | All points on the number line |
        | $\mathbb{C}$ | Complex numbers | $\{a + bi : a, b \in \mathbb{R}\}$ |
        """
    )
    return


@app.cell
def _():
    import numpy as np
    import plotly.graph_objects as go
    return go, np


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The Axioms of Set Theory (ZFC)

        The **Zermelo-Fraenkel axioms with Choice** (ZFC) form the standard foundation
        for mathematics. Let's explore each axiom and what it allows us to do.

        ### Axiom 1: Extensionality

        > **Two sets are equal if and only if they have the same elements.**

        $$\forall A \, \forall B \, [A = B \iff \forall x \, (x \in A \iff x \in B)]$$

        **What it means**: A set is completely determined by its elements—nothing else
        matters. Two sets with identical members are the same set.

        **Example**: $\{1, 2, 3\} = \{3, 2, 1\} = \{1, 1, 2, 3\}$

        ---

        ### Axiom 2: Empty Set

        > **There exists a set with no elements.**

        $$\exists \emptyset \, \forall x \, (x \notin \emptyset)$$

        **What it means**: The empty set $\emptyset$ exists. It's the unique set containing
        nothing—the "zero" of set theory.

        **Importance**: The empty set is the starting point for constructing all other sets.
        It's the **identity element** for union: $A \cup \emptyset = A$.

        ---

        ### Axiom 3: Pairing

        > **For any two sets, there exists a set containing exactly those two.**

        $$\forall a \, \forall b \, \exists C \, \forall x \, (x \in C \iff x = a \lor x = b)$$

        **What it means**: Given sets $a$ and $b$, we can form $\{a, b\}$.

        **Special case**: When $a = b$, we get the singleton $\{a\}$.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Axiom 4: Union

        > **For any set of sets, there exists a set containing all their elements.**

        $$\forall \mathcal{F} \, \exists U \, \forall x \, (x \in U \iff \exists A \in \mathcal{F} \, (x \in A))$$

        **What it means**: Given a collection $\mathcal{F} = \{A, B, C, \ldots\}$, we can form
        $\bigcup \mathcal{F} = A \cup B \cup C \cup \ldots$

        ---

        ### Axiom 5: Power Set

        > **For any set, there exists a set of all its subsets.**

        $$\forall A \, \exists P \, \forall x \, (x \in P \iff x \subseteq A)$$

        **What it means**: The power set $\mathcal{P}(A)$ contains every possible subset of $A$.

        **Example**: $\mathcal{P}(\{1, 2\}) = \{\emptyset, \{1\}, \{2\}, \{1, 2\}\}$

        **Size**: If $|A| = n$, then $|\mathcal{P}(A)| = 2^n$.

        ---

        ### Axiom 6: Infinity

        > **There exists an infinite set.**

        $$\exists I \, [\emptyset \in I \land \forall x \, (x \in I \Rightarrow x \cup \{x\} \in I)]$$

        **What it means**: There exists a set containing $\emptyset$, and whenever it contains
        $x$, it also contains $x \cup \{x\}$. This gives us:
        - $\emptyset$ (representing 0)
        - $\{\emptyset\}$ (representing 1)
        - $\{\emptyset, \{\emptyset\}\}$ (representing 2)
        - And so on... This constructs $\mathbb{N}$!
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Axiom 7: Separation (Specification)

        > **Given a set and a property, we can form the subset of elements satisfying that property.**

        $$\forall A \, \exists B \, \forall x \, (x \in B \iff x \in A \land \phi(x))$$

        **What it means**: We can "carve out" subsets using properties, but only from
        *existing* sets—we can't form arbitrary collections.

        **This avoids Russell's Paradox**: We can only form $\{x \in A : x \notin x\}$,
        not $\{x : x \notin x\}$. The paradox disappears!

        ---

        ### Axiom 8: Replacement

        > **If we apply a function to every element of a set, the results form a set.**

        $$\forall A \, [\forall x \in A \, \exists ! y \, \phi(x, y)] \Rightarrow \exists B \, \forall y \, (y \in B \iff \exists x \in A \, \phi(x, y))$$

        **What it means**: Functions preserve "set-ness." If $A$ is a set and $f$ is a
        function, then $\{f(x) : x \in A\}$ is also a set.

        ---

        ### Axiom 9: Regularity (Foundation)

        > **Every non-empty set contains an element disjoint from itself.**

        $$\forall A \, [A \neq \emptyset \Rightarrow \exists x \in A \, (x \cap A = \emptyset)]$$

        **What it means**: No set can contain itself. There are no infinite descending
        chains $\ldots \in A_3 \in A_2 \in A_1 \in A_0$.

        ---

        ### Axiom 10: Choice

        > **Given a collection of non-empty sets, we can choose one element from each.**

        **What it means**: There exists a "choice function" for any family of non-empty sets.
        This axiom is independent of the others and has surprising consequences!
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Set Operations: Building New Sets from Old

        The fundamental operations on sets are **union**, **intersection**, **complement**,
        and **difference**. These form the algebra of sets.

        ### Definitions

        Let $A$ and $B$ be sets, and let $U$ be a universal set containing both.

        | Operation | Notation | Definition |
        |-----------|----------|------------|
        | **Union** | $A \cup B$ | $\{x : x \in A \lor x \in B\}$ |
        | **Intersection** | $A \cap B$ | $\{x : x \in A \land x \in B\}$ |
        | **Complement** | $A^c$ or $\overline{A}$ | $\{x \in U : x \notin A\}$ |
        | **Difference** | $A \setminus B$ | $\{x : x \in A \land x \notin B\}$ |
        | **Symmetric Diff.** | $A \triangle B$ | $(A \setminus B) \cup (B \setminus A)$ |

        ### The Identity Elements

        Just as numbers have identity elements (0 for addition, 1 for multiplication),
        sets have identity elements for their operations:

        | Operation | Identity Element | Property |
        |-----------|------------------|----------|
        | Union $\cup$ | $\emptyset$ (empty set) | $A \cup \emptyset = A$ |
        | Intersection $\cap$ | $U$ (universal set) | $A \cap U = A$ |
        | Symmetric Diff. $\triangle$ | $\emptyset$ | $A \triangle \emptyset = A$ |

        **The empty set is the "zero" of set theory**—it's the neutral element that
        leaves other sets unchanged under union.
        """
    )
    return


@app.cell
def _(mo):
    # Set operation selector
    operation_selector = mo.ui.dropdown(
        options={
            "Union: A ∪ B": "union",
            "Intersection: A ∩ B": "intersection",
            "Difference: A \\ B": "difference",
            "Symmetric Difference: A △ B": "symmetric_difference",
            "Complement: Aᶜ": "complement",
        },
        value="Union: A ∪ B",
        label="Select operation:",
    )
    return (operation_selector,)


@app.cell
def _(mo, operation_selector):
    mo.md(
        f"""
        ### Interactive Venn Diagram

        Visualize set operations with Venn diagrams. The highlighted region shows the result.

        {operation_selector}
        """
    )
    return


@app.cell
def _(go, np, operation_selector):
    # Create Venn diagram visualization
    _theta = np.linspace(0, 2*np.pi, 100)
    _r = 1.0

    # Circle A (left)
    _ax, _ay = -0.5, 0
    _circle_a_x = _ax + _r * np.cos(_theta)
    _circle_a_y = _ay + _r * np.sin(_theta)

    # Circle B (right)
    _bx, _by = 0.5, 0
    _circle_b_x = _bx + _r * np.cos(_theta)
    _circle_b_y = _by + _r * np.sin(_theta)

    # Create figure
    _fig_venn = go.Figure()

    # Get operation type
    _op = operation_selector.value

    # Define colors based on operation
    _colors = {
        "union": {"a_only": "#4ecdc4", "b_only": "#4ecdc4", "both": "#4ecdc4"},
        "intersection": {"a_only": "rgba(100,100,100,0.3)", "b_only": "rgba(100,100,100,0.3)", "both": "#ff6b6b"},
        "difference": {"a_only": "#4ecdc4", "b_only": "rgba(100,100,100,0.3)", "both": "rgba(100,100,100,0.3)"},
        "symmetric_difference": {"a_only": "#4ecdc4", "b_only": "#4ecdc4", "both": "rgba(100,100,100,0.3)"},
        "complement": {"a_only": "rgba(100,100,100,0.3)", "b_only": "#4ecdc4", "both": "rgba(100,100,100,0.3)"},
    }
    _c = _colors[_op]

    # Add filled regions (simplified representation)
    # Circle A
    _fig_venn.add_trace(go.Scatter(
        x=_circle_a_x, y=_circle_a_y,
        fill="toself",
        fillcolor=_c["a_only"],
        line=dict(color="#00d4ff", width=2),
        name="A",
        opacity=0.7,
    ))

    # Circle B
    _fig_venn.add_trace(go.Scatter(
        x=_circle_b_x, y=_circle_b_y,
        fill="toself",
        fillcolor=_c["b_only"],
        line=dict(color="#ff6b6b", width=2),
        name="B",
        opacity=0.7,
    ))

    # Add labels
    _fig_venn.add_annotation(x=-0.9, y=0, text="A", font=dict(size=20, color="#00d4ff"), showarrow=False)
    _fig_venn.add_annotation(x=0.9, y=0, text="B", font=dict(size=20, color="#ff6b6b"), showarrow=False)

    # Operation result text
    _op_text = {
        "union": "A ∪ B = {x : x ∈ A or x ∈ B}",
        "intersection": "A ∩ B = {x : x ∈ A and x ∈ B}",
        "difference": "A \\ B = {x : x ∈ A and x ∉ B}",
        "symmetric_difference": "A △ B = {x : x ∈ A xor x ∈ B}",
        "complement": "Aᶜ = {x ∈ U : x ∉ A}",
    }

    _fig_venn.update_layout(
        minreducedwidth=300,
        title=dict(text=_op_text[_op], font=dict(color="#eaeaea", size=16)),
        xaxis=dict(visible=False, range=[-2.5, 2.5]),
        yaxis=dict(visible=False, range=[-1.8, 1.8], scaleanchor="x"),
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#1a1a2e",
        height=350,
        showlegend=True,
        legend=dict(font=dict(color="#a0a0a0"), orientation='h', yanchor='bottom', y=-0.15, xanchor='center', x=0.5),
        margin=dict(l=40, r=40, t=50, b=80),
    )
    _fig_venn
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The two overlapping circles represent sets $A$ (cyan, left) and $B$ (red, right). The highlighted region shows the result of the selected set operation. The overlapping area in the middle contains elements that belong to both sets—this is $A \cap B$, the intersection.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Algebraic Properties of Set Operations

        Set operations satisfy many algebraic laws, similar to arithmetic:

        **Commutative Laws:**
        $$A \cup B = B \cup A \qquad A \cap B = B \cap A$$

        **Associative Laws:**
        $$(A \cup B) \cup C = A \cup (B \cup C) \qquad (A \cap B) \cap C = A \cap (B \cap C)$$

        **Distributive Laws:**
        $$A \cap (B \cup C) = (A \cap B) \cup (A \cap C)$$
        $$A \cup (B \cap C) = (A \cup B) \cap (A \cup C)$$

        **Identity Laws:**
        $$A \cup \emptyset = A \qquad A \cap U = A$$

        **Complement Laws:**
        $$A \cup A^c = U \qquad A \cap A^c = \emptyset$$

        **De Morgan's Laws:**
        $$(A \cup B)^c = A^c \cap B^c \qquad (A \cap B)^c = A^c \cup B^c$$

        These laws make the power set $\mathcal{P}(U)$ into a **Boolean algebra**—a
        fundamental structure in logic and computer science.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Relations: Connecting Elements

        A **relation** describes how elements of sets are connected. Relations are the
        foundation for understanding functions, orderings, and equivalences.

        ### Definition

        A **relation** $R$ from set $A$ to set $B$ is a subset of the Cartesian product:

        $$R \subseteq A \times B = \{(a, b) : a \in A, b \in B\}$$

        We write $a \, R \, b$ or $(a, b) \in R$ to mean "$a$ is related to $b$."

        ### Examples of Relations

        | Relation | Set | Definition |
        |----------|-----|------------|
        | Less than ($<$) | $\mathbb{R} \times \mathbb{R}$ | $\{(x, y) : x < y\}$ |
        | Divides ($\mid$) | $\mathbb{Z} \times \mathbb{Z}$ | $\{(a, b) : a \text{ divides } b\}$ |
        | Congruence mod $n$ | $\mathbb{Z} \times \mathbb{Z}$ | $\{(a, b) : n \mid (a - b)\}$ |
        | Subset ($\subseteq$) | $\mathcal{P}(S) \times \mathcal{P}(S)$ | $\{(A, B) : A \subseteq B\}$ |

        ### Properties of Relations on a Set $A$

        A relation $R \subseteq A \times A$ can have special properties:

        | Property | Definition | Example |
        |----------|------------|---------|
        | **Reflexive** | $\forall a \in A: a \, R \, a$ | $\leq$ (everything $\leq$ itself) |
        | **Symmetric** | $a \, R \, b \Rightarrow b \, R \, a$ | $=$ (equality is symmetric) |
        | **Antisymmetric** | $a \, R \, b \land b \, R \, a \Rightarrow a = b$ | $\leq$ |
        | **Transitive** | $a \, R \, b \land b \, R \, c \Rightarrow a \, R \, c$ | $<$ (if $a < b$ and $b < c$, then $a < c$) |
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Transitivity: The Chain Property

        **Transitivity** is one of the most important properties a relation can have.
        It captures the idea that relationships can "chain together."

        ### Formal Definition

        A relation $R$ on set $A$ is **transitive** if:

        $$\forall a, b, c \in A: \quad (a \, R \, b \land b \, R \, c) \Rightarrow a \, R \, c$$

        ### Intuitive Understanding

        Think of transitivity as "if I can get from $a$ to $b$, and from $b$ to $c$,
        then I can get from $a$ to $c$."

        **Transitive relations:**
        - $<$ on numbers: if $a < b$ and $b < c$, then $a < c$
        - $\subseteq$ on sets: if $A \subseteq B$ and $B \subseteq C$, then $A \subseteq C$
        - "is an ancestor of" on people

        **Non-transitive relations:**
        - "is a friend of" (your friend's friend isn't necessarily your friend)
        - "is one meter away from"
        - "is the parent of"

        ### The Transitive Closure

        Given any relation $R$, we can construct its **transitive closure** $R^+$—the
        smallest transitive relation containing $R$. We add $(a, c)$ whenever there's
        a "path" from $a$ to $c$ through $R$.

        $$R^+ = R \cup R^2 \cup R^3 \cup \ldots$$

        where $R^n = \{(a, c) : \exists b_1, \ldots, b_{n-1}: a \, R \, b_1 \, R \, b_2 \, R \ldots R \, b_{n-1} \, R \, c\}$
        """
    )
    return


@app.cell
def _(go, np):
    # Visualize transitivity with an animated diagram
    # Show how a → b and b → c implies a → c

    _fig_trans = go.Figure()

    # Node positions
    _nodes = {"a": (-1.5, 0), "b": (0, 1), "c": (1.5, 0)}

    # Draw nodes
    for _name, (_x, _y) in _nodes.items():
        _fig_trans.add_trace(go.Scatter(
            x=[_x], y=[_y],
            mode="markers+text",
            marker=dict(size=40, color="#4ecdc4"),
            text=[_name],
            textposition="middle center",
            textfont=dict(size=20, color="#1a1a2e"),
            showlegend=False,
        ))

    # Arrow from a to b
    _fig_trans.add_annotation(
        x=_nodes["b"][0] - 0.15, y=_nodes["b"][1] - 0.1,
        ax=_nodes["a"][0] + 0.15, ay=_nodes["a"][1] + 0.1,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=3, arrowcolor="#00d4ff",
    )
    _fig_trans.add_annotation(x=-0.9, y=0.65, text="a R b", font=dict(size=14, color="#00d4ff"), showarrow=False)

    # Arrow from b to c
    _fig_trans.add_annotation(
        x=_nodes["c"][0] - 0.15, y=_nodes["c"][1] + 0.1,
        ax=_nodes["b"][0] + 0.15, ay=_nodes["b"][1] - 0.1,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=3, arrowcolor="#00d4ff",
    )
    _fig_trans.add_annotation(x=0.9, y=0.65, text="b R c", font=dict(size=14, color="#00d4ff"), showarrow=False)

    # Arrow from a to c (the transitive consequence)
    _fig_trans.add_annotation(
        x=_nodes["c"][0] - 0.15, y=_nodes["c"][1],
        ax=_nodes["a"][0] + 0.15, ay=_nodes["a"][1],
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=3, arrowcolor="#ff6b6b",
    )
    _fig_trans.add_annotation(x=0, y=-0.4, text="⟹ a R c (by transitivity)", font=dict(size=14, color="#ff6b6b"), showarrow=False)

    _fig_trans.update_layout(
        minreducedwidth=300,
        title=dict(text="Transitivity: If a R b and b R c, then a R c", font=dict(color="#eaeaea")),
        xaxis=dict(visible=False, range=[-2.5, 2.5]),
        yaxis=dict(visible=False, range=[-1, 1.8], scaleanchor="x"),
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#1a1a2e",
        height=350,
    )
    _fig_trans
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        This diagram illustrates the transitive property: if $a$ is related to $b$ (blue arrow), and $b$ is related to $c$ (blue arrow), then transitivity guarantees that $a$ is related to $c$ (red arrow). The red arrow represents the relationship that "must exist" due to transitivity—it's a logical consequence of the first two relationships.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Proof: Transitivity of Subset Relation

        Let's prove that $\subseteq$ is transitive.

        **Theorem**: For any sets $A$, $B$, $C$: if $A \subseteq B$ and $B \subseteq C$, then $A \subseteq C$.

        **Proof**:

        Let $A$, $B$, $C$ be sets with $A \subseteq B$ and $B \subseteq C$.

        We need to show $A \subseteq C$, i.e., $\forall x: x \in A \Rightarrow x \in C$.

        Let $x \in A$ be arbitrary. We must show $x \in C$.

        1. Since $x \in A$ and $A \subseteq B$, we have $x \in B$. (Definition of subset)

        2. Since $x \in B$ and $B \subseteq C$, we have $x \in C$. (Definition of subset)

        Therefore $x \in C$. Since $x$ was arbitrary, $A \subseteq C$. $\square$

        **This proof pattern appears everywhere**: to show $X \subseteq Y$, take an arbitrary
        element of $X$ and show it belongs to $Y$.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Equivalence Relations and Partitions

        An **equivalence relation** combines reflexivity, symmetry, and transitivity
        to create a notion of "sameness" that partitions a set into groups.

        ### Definition

        A relation $\sim$ on set $A$ is an **equivalence relation** if it is:
        1. **Reflexive**: $a \sim a$ for all $a \in A$
        2. **Symmetric**: $a \sim b \Rightarrow b \sim a$
        3. **Transitive**: $a \sim b \land b \sim c \Rightarrow a \sim c$

        ### Equivalence Classes

        For an equivalence relation $\sim$ on $A$, the **equivalence class** of $a$ is:

        $$[a] = \{x \in A : x \sim a\}$$

        All elements equivalent to $a$ are grouped together.

        ### Examples

        | Equivalence Relation | Equivalence Classes |
        |---------------------|---------------------|
        | Equality ($=$) | Each element in its own class: $[a] = \{a\}$ |
        | Congruence mod 3 | $[0] = \{\ldots, -3, 0, 3, 6, \ldots\}$, $[1] = \{\ldots, -2, 1, 4, \ldots\}$, $[2] = \{\ldots, -1, 2, 5, \ldots\}$ |
        | Same birthday | All people born on the same day |

        ### The Fundamental Theorem

        **Theorem**: Equivalence relations and partitions are two views of the same thing.

        An equivalence relation $\sim$ on $A$ induces a **partition** of $A$—a collection
        of disjoint non-empty subsets whose union is $A$.

        Conversely, every partition induces an equivalence relation: $a \sim b$ iff
        $a$ and $b$ are in the same partition block.
        """
    )
    return


@app.cell
def _(go, np):
    # Visualize equivalence classes for mod 3
    _fig_equiv = go.Figure()

    # Create three equivalence classes
    _classes = {
        "[0]": {"elements": [-6, -3, 0, 3, 6, 9], "color": "#4ecdc4", "y": 2},
        "[1]": {"elements": [-5, -2, 1, 4, 7, 10], "color": "#ff6b6b", "y": 0},
        "[2]": {"elements": [-4, -1, 2, 5, 8, 11], "color": "#ffd93d", "y": -2},
    }

    for _name, _data in _classes.items():
        _x_pos = list(range(len(_data["elements"])))
        _fig_equiv.add_trace(go.Scatter(
            x=_x_pos,
            y=[_data["y"]] * len(_data["elements"]),
            mode="markers+text",
            marker=dict(size=35, color=_data["color"]),
            text=[str(_e) for _e in _data["elements"]],
            textposition="middle center",
            textfont=dict(size=12, color="#1a1a2e"),
            name=_name,
        ))
        # Class label
        _fig_equiv.add_annotation(
            x=-1, y=_data["y"],
            text=_name,
            font=dict(size=16, color=_data["color"]),
            showarrow=False,
        )

    # Draw boxes around each class
    for _name, _data in _classes.items():
        _fig_equiv.add_shape(
            type="rect",
            x0=-0.5, x1=5.5,
            y0=_data["y"] - 0.6, y1=_data["y"] + 0.6,
            line=dict(color=_data["color"], width=2),
            fillcolor=f"rgba{tuple(list(int(_data['color'][i:i+2], 16) for i in (1, 3, 5)) + [0.1])}",
        )

    _fig_equiv.update_layout(
        minreducedwidth=300,
        title=dict(text="Equivalence Classes for Congruence mod 3 on ℤ", font=dict(color="#eaeaea")),
        xaxis=dict(visible=False, range=[-2, 6.5]),
        yaxis=dict(visible=False, range=[-3.5, 3.5]),
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#1a1a2e",
        height=350,
        showlegend=True,
        legend=dict(font=dict(color="#a0a0a0"), orientation='h', yanchor='bottom', y=-0.15, xanchor='center', x=0.5),
        margin=dict(l=40, r=40, t=50, b=80),
    )
    _fig_equiv
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The integers are partitioned into three equivalence classes based on their remainder when divided by 3. Each colored row contains all integers that are equivalent to each other modulo 3: the teal row $[0]$ contains multiples of 3, the red row $[1]$ contains numbers with remainder 1, and the yellow row $[2]$ contains numbers with remainder 2. Every integer belongs to exactly one class—no overlaps, no gaps.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Functions: Mappings Between Sets

        A **function** is a special kind of relation that assigns to each element of
        one set exactly one element of another set.

        ### Definition

        A **function** $f: A \to B$ is a relation $f \subseteq A \times B$ such that:

        $$\forall a \in A \, \exists ! \, b \in B: (a, b) \in f$$

        We write $f(a) = b$ instead of $(a, b) \in f$.

        **Components:**
        - $A$ is the **domain** (source set)
        - $B$ is the **codomain** (target set)
        - $f(A) = \{f(a) : a \in A\}$ is the **range** or **image**

        ### Function Notation

        | Notation | Meaning |
        |----------|---------|
        | $f: A \to B$ | $f$ is a function from $A$ to $B$ |
        | $a \mapsto f(a)$ | Element $a$ maps to $f(a)$ |
        | $f(a)$ | The image of $a$ under $f$ |
        | $f^{-1}(b)$ | The preimage of $b$: $\{a \in A : f(a) = b\}$ |

        ### The Role of the Identity Element

        For functions, there's a special function that acts like "zero" or "one":

        The **identity function** $\text{id}_A: A \to A$ defined by $\text{id}_A(a) = a$

        It satisfies: $f \circ \text{id}_A = f$ and $\text{id}_B \circ f = f$

        The identity function is the "do nothing" mapping—the neutral element for
        function composition.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Types of Functions

        Functions are classified by how they map elements:

        | Type | Definition | Visual |
        |------|------------|--------|
        | **Injective** (one-to-one) | $f(a_1) = f(a_2) \Rightarrow a_1 = a_2$ | Different inputs → different outputs |
        | **Surjective** (onto) | $\forall b \in B \, \exists a \in A: f(a) = b$ | Every output is hit |
        | **Bijective** | Both injective and surjective | Perfect pairing |

        ### Why These Matter

        - **Injective**: No information is lost; we can potentially recover the input
        - **Surjective**: The function "covers" all of $B$
        - **Bijective**: Sets $A$ and $B$ have the same "size" (cardinality)

        ### Inverse Functions

        A function $f: A \to B$ has an **inverse** $f^{-1}: B \to A$ if and only if
        $f$ is bijective.

        The inverse satisfies:
        $$f^{-1}(f(a)) = a \quad \text{and} \quad f(f^{-1}(b)) = b$$

        **Example**: $f(x) = 2x + 1$ has inverse $f^{-1}(y) = \frac{y-1}{2}$
        """
    )
    return


@app.cell
def _(mo):
    # Function type selector
    func_type_selector = mo.ui.dropdown(
        options={
            "Injective (one-to-one)": "injective",
            "Surjective (onto)": "surjective",
            "Bijective (both)": "bijective",
            "Neither": "neither",
        },
        value="Bijective (both)",
        label="Select function type:",
    )
    return (func_type_selector,)


@app.cell
def _(func_type_selector, mo):
    mo.md(
        f"""
        ### Interactive Function Visualization

        See how different function types map elements between sets.

        {func_type_selector}
        """
    )
    return


@app.cell
def _(func_type_selector, go):
    # Visualize function mappings
    _func_type = func_type_selector.value

    _fig_func = go.Figure()

    # Define domain and codomain positions
    _domain_x = 0
    _codomain_x = 3

    # Define mappings based on function type
    if _func_type == "injective":
        _domain = ["a", "b", "c"]
        _codomain = ["1", "2", "3", "4"]
        _mappings = [("a", "1"), ("b", "3"), ("c", "4")]
        _desc = "Injective: different inputs → different outputs. Element '2' is not hit."
    elif _func_type == "surjective":
        _domain = ["a", "b", "c", "d"]
        _codomain = ["1", "2", "3"]
        _mappings = [("a", "1"), ("b", "2"), ("c", "3"), ("d", "2")]
        _desc = "Surjective: every output is hit. Two inputs map to '2'."
    elif _func_type == "bijective":
        _domain = ["a", "b", "c"]
        _codomain = ["1", "2", "3"]
        _mappings = [("a", "1"), ("b", "2"), ("c", "3")]
        _desc = "Bijective: perfect one-to-one correspondence."
    else:  # neither
        _domain = ["a", "b", "c"]
        _codomain = ["1", "2", "3"]
        _mappings = [("a", "1"), ("b", "1"), ("c", "2")]
        _desc = "Neither: 'a' and 'b' both map to '1', and '3' is not hit."

    # Draw domain elements
    _domain_ys = {_e: 2 - _i * 1.2 for _i, _e in enumerate(_domain)}
    for _e, _y in _domain_ys.items():
        _fig_func.add_trace(go.Scatter(
            x=[_domain_x], y=[_y],
            mode="markers+text",
            marker=dict(size=35, color="#4ecdc4"),
            text=[_e],
            textposition="middle center",
            textfont=dict(size=16, color="#1a1a2e"),
            showlegend=False,
        ))

    # Draw codomain elements
    _codomain_ys = {_e: 2 - _i * 1.2 for _i, _e in enumerate(_codomain)}
    for _e, _y in _codomain_ys.items():
        # Check if this element is hit
        _hit = any(_m[1] == _e for _m in _mappings)
        _color = "#ff6b6b" if _hit else "rgba(255, 107, 107, 0.3)"
        _fig_func.add_trace(go.Scatter(
            x=[_codomain_x], y=[_y],
            mode="markers+text",
            marker=dict(size=35, color=_color),
            text=[_e],
            textposition="middle center",
            textfont=dict(size=16, color="#1a1a2e" if _hit else "#666666"),
            showlegend=False,
        ))

    # Draw mapping arrows
    for _a, _b in _mappings:
        _fig_func.add_annotation(
            x=_codomain_x - 0.25, y=_codomain_ys[_b],
            ax=_domain_x + 0.25, ay=_domain_ys[_a],
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=2, arrowsize=1.2, arrowwidth=2, arrowcolor="#00d4ff",
        )

    # Labels
    _fig_func.add_annotation(x=_domain_x, y=3, text="Domain A", font=dict(size=14, color="#4ecdc4"), showarrow=False)
    _fig_func.add_annotation(x=_codomain_x, y=3, text="Codomain B", font=dict(size=14, color="#ff6b6b"), showarrow=False)

    _fig_func.update_layout(
        minreducedwidth=300,
        title=dict(text=_desc, font=dict(color="#eaeaea", size=14)),
        xaxis=dict(visible=False, range=[-1, 4]),
        yaxis=dict(visible=False, range=[-3, 4]),
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#1a1a2e",
        height=400,
    )
    _fig_func
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Blue arrows show how each element in the domain $A$ (teal circles) maps to an element in the codomain $B$ (red circles). Bright red circles are "hit" by at least one arrow; faded circles are not mapped to by any element. This visualization lets you see whether the function is injective (no two arrows hit the same target), surjective (every target is hit), or bijective (both).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Cardinality: Comparing Set Sizes

        **Cardinality** measures the "size" of a set. For finite sets, this is just
        the number of elements. But for infinite sets, things get interesting.

        ### Finite Cardinality

        For a finite set $A$, the cardinality $|A|$ is the number of elements.

        **Examples:**
        - $|\{a, b, c\}| = 3$
        - $|\emptyset| = 0$
        - $|\mathcal{P}(\{1, 2\})| = 4$

        ### Comparing Infinite Sets

        **Cantor's insight**: Two sets have the same cardinality if there exists a
        **bijection** between them.

        $$|A| = |B| \iff \exists f: A \xrightarrow{\text{bijection}} B$$

        ### Surprising Results

        **Theorem**: $|\mathbb{N}| = |\mathbb{Z}|$ (naturals and integers have the same size!)

        **Proof**: Define the bijection $f: \mathbb{N} \to \mathbb{Z}$ by:
        $$f(n) = \begin{cases} n/2 & \text{if } n \text{ is even} \\ -(n+1)/2 & \text{if } n \text{ is odd} \end{cases}$$

        This maps: $0 \mapsto 0, 1 \mapsto -1, 2 \mapsto 1, 3 \mapsto -2, 4 \mapsto 2, \ldots$

        **Theorem**: $|\mathbb{N}| = |\mathbb{Q}|$ (rationals are also countable!)

        **Theorem**: $|\mathbb{N}| < |\mathbb{R}|$ (reals are "more infinite" than naturals!)

        This last result uses **Cantor's diagonal argument**—one of the most beautiful
        proofs in all of mathematics.
        """
    )
    return


@app.cell
def _(go):
    # Visualize the bijection between N and Z
    _fig_card = go.Figure()

    # Natural numbers (top row)
    _naturals = list(range(8))
    for _i, _n in enumerate(_naturals):
        _fig_card.add_trace(go.Scatter(
            x=[_i], y=[1],
            mode="markers+text",
            marker=dict(size=35, color="#4ecdc4"),
            text=[str(_n)],
            textposition="middle center",
            textfont=dict(size=14, color="#1a1a2e"),
            showlegend=False,
        ))

    # Integers (bottom row)
    _integers = [0, -1, 1, -2, 2, -3, 3, -4]
    for _i, _z in enumerate(_integers):
        _fig_card.add_trace(go.Scatter(
            x=[_i], y=[-1],
            mode="markers+text",
            marker=dict(size=35, color="#ff6b6b"),
            text=[str(_z)],
            textposition="middle center",
            textfont=dict(size=14, color="#1a1a2e"),
            showlegend=False,
        ))

    # Draw arrows showing the bijection
    for _i in range(len(_naturals)):
        _fig_card.add_annotation(
            x=_i, y=-0.6,
            ax=_i, ay=0.6,
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=2, arrowsize=1.2, arrowwidth=2, arrowcolor="#00d4ff",
        )

    # Labels
    _fig_card.add_annotation(x=-1, y=1, text="ℕ:", font=dict(size=18, color="#4ecdc4"), showarrow=False)
    _fig_card.add_annotation(x=-1, y=-1, text="ℤ:", font=dict(size=18, color="#ff6b6b"), showarrow=False)
    _fig_card.add_annotation(x=8.5, y=1, text="...", font=dict(size=18, color="#4ecdc4"), showarrow=False)
    _fig_card.add_annotation(x=8.5, y=-1, text="...", font=dict(size=18, color="#ff6b6b"), showarrow=False)

    _fig_card.update_layout(
        minreducedwidth=300,
        title=dict(text="Bijection showing |ℕ| = |ℤ|: The integers are countable!", font=dict(color="#eaeaea")),
        xaxis=dict(visible=False, range=[-1.5, 9]),
        yaxis=dict(visible=False, range=[-2, 2]),
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#1a1a2e",
        height=300,
    )
    _fig_card
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The top row displays natural numbers $\mathbb{N} = \{0, 1, 2, 3, \ldots\}$, and the bottom row shows integers $\mathbb{Z} = \{\ldots, -2, -1, 0, 1, 2, \ldots\}$. The arrows demonstrate a bijection: we can pair every natural number with a unique integer. By alternating between positive and negative integers ($0 \mapsto 0$, $1 \mapsto -1$, $2 \mapsto 1$, $3 \mapsto -2$, etc.), we prove these infinite sets have the same cardinality.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Cantor's Diagonal Argument

        **Theorem**: The real numbers are **uncountable**—there's no bijection $\mathbb{N} \to \mathbb{R}$.

        **Proof** (by contradiction):

        Suppose we could list all real numbers in $[0, 1)$:
        $$r_0 = 0.d_{00}d_{01}d_{02}d_{03}\ldots$$
        $$r_1 = 0.d_{10}d_{11}d_{12}d_{13}\ldots$$
        $$r_2 = 0.d_{20}d_{21}d_{22}d_{23}\ldots$$
        $$\vdots$$

        Construct a new number $x = 0.x_0 x_1 x_2 \ldots$ where:
        $$x_n = \begin{cases} 5 & \text{if } d_{nn} \neq 5 \\ 6 & \text{if } d_{nn} = 5 \end{cases}$$

        The number $x$ differs from $r_n$ in the $n$-th decimal place for every $n$.

        Therefore $x \neq r_n$ for all $n$, so $x$ is not in our list.

        **Contradiction!** Our list cannot contain all real numbers. $\square$

        ### The Hierarchy of Infinities

        | Cardinality | Symbol | Examples |
        |-------------|--------|----------|
        | Countable | $\aleph_0$ | $\mathbb{N}$, $\mathbb{Z}$, $\mathbb{Q}$ |
        | Continuum | $\mathfrak{c} = 2^{\aleph_0}$ | $\mathbb{R}$, $\mathcal{P}(\mathbb{N})$, $(0,1)$ |
        | Larger | $2^{\mathfrak{c}}$, etc. | $\mathcal{P}(\mathbb{R})$, ... |

        Cantor proved: for any set $A$, we have $|A| < |\mathcal{P}(A)|$.

        **There are infinitely many sizes of infinity!**
        """
    )
    return


@app.cell
def _(go):
    # Visualize Cantor's diagonal argument
    _fig_diag = go.Figure()

    # Sample list of "real numbers" (just first few digits)
    _numbers = [
        [3, 1, 4, 1, 5, 9],
        [2, 7, 1, 8, 2, 8],
        [1, 4, 1, 4, 2, 1],
        [0, 5, 7, 7, 2, 1],
        [6, 9, 3, 1, 4, 7],
        [9, 8, 7, 6, 5, 4],
    ]

    # Draw the grid
    for _i, _row in enumerate(_numbers):
        for _j, _d in enumerate(_row):
            # Highlight diagonal
            _is_diag = _i == _j
            _color = "#ff6b6b" if _is_diag else "#4ecdc4"
            _size = 30 if _is_diag else 25

            _fig_diag.add_trace(go.Scatter(
                x=[_j], y=[-_i],
                mode="markers+text",
                marker=dict(size=_size, color=_color),
                text=[str(_d)],
                textposition="middle center",
                textfont=dict(size=12, color="#1a1a2e"),
                showlegend=False,
            ))

    # Show the constructed number
    _diagonal = [_numbers[_i][_i] for _i in range(6)]
    _new_digits = [5 if _d != 5 else 6 for _d in _diagonal]

    _fig_diag.add_annotation(x=-1.5, y=-7, text="Diagonal:", font=dict(size=14, color="#ff6b6b"), showarrow=False)
    _fig_diag.add_annotation(x=2.5, y=-7, text="".join(map(str, _diagonal)), font=dict(size=14, color="#ff6b6b"), showarrow=False)

    _fig_diag.add_annotation(x=-1.5, y=-8, text="New number:", font=dict(size=14, color="#ffd93d"), showarrow=False)
    _fig_diag.add_annotation(x=2.5, y=-8, text="0." + "".join(map(str, _new_digits)) + "...", font=dict(size=14, color="#ffd93d"), showarrow=False)

    # Row labels
    for _i in range(6):
        _fig_diag.add_annotation(x=-1, y=-_i, text=f"r{_i} = 0.", font=dict(size=12, color="#a0a0a0"), showarrow=False)

    _fig_diag.update_layout(
        minreducedwidth=300,
        title=dict(text="Cantor's Diagonal Argument: Constructing a number not in any list", font=dict(color="#eaeaea")),
        xaxis=dict(visible=False, range=[-2.5, 6.5]),
        yaxis=dict(visible=False, range=[-9, 1]),
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#1a1a2e",
        height=450,
    )
    _fig_diag
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        This grid represents a hypothetical list of all real numbers. Each row is a decimal expansion, and the red diagonal highlights the $n$-th digit of the $n$-th number. By constructing a new number that differs from each row at its diagonal position, we create a real number not in our list—proving that no list can contain all reals. This is Cantor's brilliant diagonal argument for the uncountability of $\mathbb{R}$.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Algebraic Structures on Sets

        Sets become truly powerful when we add **operations** and **special elements**.
        These create algebraic structures with rich properties.

        ### Groups, Rings, and Fields

        | Structure | Components | Examples |
        |-----------|------------|----------|
        | **Monoid** | Set + associative operation + identity | $(\mathbb{N}, +, 0)$ |
        | **Group** | Monoid + inverses | $(\mathbb{Z}, +, 0)$ |
        | **Ring** | Two operations (addition, multiplication) | $(\mathbb{Z}, +, \times)$ |
        | **Field** | Ring where non-zero elements have multiplicative inverses | $(\mathbb{R}, +, \times)$ |

        ### The Identity Element

        Every algebraic structure has **identity elements**—the "zero-like" elements
        that leave other elements unchanged:

        **Additive identity**: $a + 0 = a$ for all $a$

        **Multiplicative identity**: $a \cdot 1 = a$ for all $a$

        ### Group Axioms

        A **group** $(G, \cdot)$ satisfies:

        1. **Closure**: $a, b \in G \Rightarrow a \cdot b \in G$
        2. **Associativity**: $(a \cdot b) \cdot c = a \cdot (b \cdot c)$
        3. **Identity**: $\exists e \in G: e \cdot a = a \cdot e = a$ for all $a$
        4. **Inverses**: $\forall a \in G \, \exists a^{-1} \in G: a \cdot a^{-1} = a^{-1} \cdot a = e$

        **Theorem**: The identity element in a group is **unique**.

        **Proof**: Suppose $e$ and $e'$ are both identity elements.
        Then $e = e \cdot e' = e'$. $\square$
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Homomorphisms: Structure-Preserving Maps

        A **homomorphism** is a function between algebraic structures that preserves
        the operations. It's how elements "move" between sets while respecting structure.

        ### Definition

        A function $\phi: G \to H$ between groups is a **homomorphism** if:

        $$\phi(a \cdot b) = \phi(a) \cdot \phi(b) \quad \text{for all } a, b \in G$$

        ### Key Properties of Homomorphisms

        **Theorem**: If $\phi: G \to H$ is a homomorphism, then:

        1. $\phi(e_G) = e_H$ (identity maps to identity)
        2. $\phi(a^{-1}) = \phi(a)^{-1}$ (inverses map to inverses)

        **Proof of (1)**:
        $$\phi(e_G) = \phi(e_G \cdot e_G) = \phi(e_G) \cdot \phi(e_G)$$

        Multiply both sides by $\phi(e_G)^{-1}$:
        $$e_H = \phi(e_G) \quad \square$$

        ### Types of Homomorphisms

        | Type | Definition |
        |------|------------|
        | **Monomorphism** | Injective homomorphism |
        | **Epimorphism** | Surjective homomorphism |
        | **Isomorphism** | Bijective homomorphism |
        | **Endomorphism** | Homomorphism from a structure to itself |
        | **Automorphism** | Isomorphism from a structure to itself |

        ### The Isomorphism Concept

        Two structures are **isomorphic** if there's an isomorphism between them.
        Isomorphic structures are "essentially the same"—they have identical algebraic
        properties, just with different labels.
        """
    )
    return


@app.cell
def _(go, np):
    # Visualize a homomorphism
    _fig_hom = go.Figure()

    # Domain: Z_6 (integers mod 6)
    _z6_elements = ["0", "1", "2", "3", "4", "5"]
    _z6_y = 1
    for _i, _e in enumerate(_z6_elements):
        _theta = 2 * 3.14159 * _i / 6 - 3.14159/2
        _x = 2 * np.cos(_theta) - 4
        _y = 2 * np.sin(_theta)
        _fig_hom.add_trace(go.Scatter(
            x=[_x], y=[_y],
            mode="markers+text",
            marker=dict(size=30, color="#4ecdc4"),
            text=[_e],
            textposition="middle center",
            textfont=dict(size=14, color="#1a1a2e"),
            showlegend=False,
        ))

    # Codomain: Z_3 (integers mod 3)
    _z3_elements = ["0", "1", "2"]
    for _i, _e in enumerate(_z3_elements):
        _theta = 2 * 3.14159 * _i / 3 - 3.14159/2
        _x = 1.5 * np.cos(_theta) + 4
        _y = 1.5 * np.sin(_theta)
        _fig_hom.add_trace(go.Scatter(
            x=[_x], y=[_y],
            mode="markers+text",
            marker=dict(size=35, color="#ff6b6b"),
            text=[_e],
            textposition="middle center",
            textfont=dict(size=14, color="#1a1a2e"),
            showlegend=False,
        ))

    # Labels
    _fig_hom.add_annotation(x=-4, y=3, text="ℤ₆", font=dict(size=20, color="#4ecdc4"), showarrow=False)
    _fig_hom.add_annotation(x=4, y=3, text="ℤ₃", font=dict(size=20, color="#ff6b6b"), showarrow=False)
    _fig_hom.add_annotation(x=0, y=2.5, text="φ(n) = n mod 3", font=dict(size=14, color="#00d4ff"), showarrow=False)

    # Arrow showing the homomorphism
    _fig_hom.add_annotation(
        x=1.5, y=0,
        ax=-1.5, ay=0,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowsize=2, arrowwidth=3, arrowcolor="#00d4ff",
    )

    _fig_hom.update_layout(
        minreducedwidth=300,
        title=dict(text="Homomorphism φ: ℤ₆ → ℤ₃ defined by φ(n) = n mod 3", font=dict(color="#eaeaea")),
        xaxis=dict(visible=False, range=[-7, 7]),
        yaxis=dict(visible=False, range=[-3, 4], scaleanchor="x"),
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#1a1a2e",
        height=400,
    )
    _fig_hom
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The left circle represents the group $\mathbb{Z}_6$ (integers modulo 6), and the right circle represents $\mathbb{Z}_3$ (integers modulo 3). The arrow shows the homomorphism $\phi(n) = n \mod 3$, which maps elements from the larger group to the smaller one while preserving the group operation. Notice that multiple elements in $\mathbb{Z}_6$ map to the same element in $\mathbb{Z}_3$ (e.g., both 0 and 3 map to 0).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Orderings: Partial and Total Orders

        **Orderings** are special relations that organize elements into hierarchies.
        They combine antisymmetry and transitivity to create structure.

        ### Partial Orders

        A **partial order** on set $A$ is a relation $\leq$ that is:
        1. **Reflexive**: $a \leq a$
        2. **Antisymmetric**: $a \leq b \land b \leq a \Rightarrow a = b$
        3. **Transitive**: $a \leq b \land b \leq c \Rightarrow a \leq c$

        A set with a partial order is called a **poset** (partially ordered set).

        **Examples of Partial Orders:**
        - $(\mathbb{R}, \leq)$: usual ordering on real numbers
        - $(\mathcal{P}(S), \subseteq)$: subsets ordered by inclusion
        - $(\mathbb{N}, \mid)$: divisibility ordering

        ### Total Orders

        A partial order is a **total order** if every two elements are comparable:

        $$\forall a, b: a \leq b \lor b \leq a$$

        **Example**: $(\mathbb{R}, \leq)$ is a total order—any two reals can be compared.

        **Non-example**: $(\mathcal{P}(\{1,2,3\}), \subseteq)$ is NOT total.
        $\{1\}$ and $\{2\}$ are incomparable (neither is a subset of the other).

        ### Important Elements in Posets

        | Element | Definition |
        |---------|------------|
        | **Minimum** | $m \leq a$ for all $a$ |
        | **Maximum** | $a \leq M$ for all $a$ |
        | **Minimal** | No element is strictly less |
        | **Maximal** | No element is strictly greater |
        """
    )
    return


@app.cell
def _(go, np):
    # Visualize a Hasse diagram for divisibility on {1,2,3,4,6,12}
    _fig_hasse = go.Figure()

    # Elements and their positions (Hasse diagram layout)
    _elements = {
        "1": (0, 0),
        "2": (-1.5, 1),
        "3": (1.5, 1),
        "4": (-1.5, 2),
        "6": (1.5, 2),
        "12": (0, 3),
    }

    # Edges (covering relations in divisibility)
    _edges = [
        ("1", "2"), ("1", "3"),
        ("2", "4"), ("2", "6"),
        ("3", "6"),
        ("4", "12"), ("6", "12"),
    ]

    # Draw edges first
    for _a, _b in _edges:
        _x0, _y0 = _elements[_a]
        _x1, _y1 = _elements[_b]
        _fig_hasse.add_trace(go.Scatter(
            x=[_x0, _x1], y=[_y0, _y1],
            mode="lines",
            line=dict(color="#4a5568", width=2),
            showlegend=False,
        ))

    # Draw nodes
    for _name, (_x, _y) in _elements.items():
        _fig_hasse.add_trace(go.Scatter(
            x=[_x], y=[_y],
            mode="markers+text",
            marker=dict(size=35, color="#4ecdc4"),
            text=[_name],
            textposition="middle center",
            textfont=dict(size=14, color="#1a1a2e"),
            showlegend=False,
        ))

    # Annotations
    _fig_hasse.add_annotation(x=0, y=-0.7, text="Minimum (1 divides all)", font=dict(size=12, color="#ff6b6b"), showarrow=False)
    _fig_hasse.add_annotation(x=0, y=3.7, text="Maximum (all divide 12)", font=dict(size=12, color="#ff6b6b"), showarrow=False)

    _fig_hasse.update_layout(
        minreducedwidth=300,
        title=dict(text="Hasse Diagram: Divisibility on {1, 2, 3, 4, 6, 12}", font=dict(color="#eaeaea")),
        xaxis=dict(visible=False, range=[-3, 3]),
        yaxis=dict(visible=False, range=[-1.2, 4.5]),
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#1a1a2e",
        height=400,
    )
    _fig_hasse
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        This Hasse diagram visualizes the divisibility relation on $\{1, 2, 3, 4, 6, 12\}$. Each line going upward means "divides"—so $2$ divides $4$, $4$ divides $12$, etc. The element $1$ is at the bottom (it divides everything), and $12$ is at the top (everything divides it). This is a partial order because not all pairs are comparable: for instance, $4$ and $6$ have no direct relationship (neither divides the other).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Well-Orderings and Induction

        A total order is a **well-ordering** if every non-empty subset has a minimum element.

        ### The Well-Ordering Theorem

        **Theorem** (equivalent to Axiom of Choice): Every set can be well-ordered.

        This is a remarkable and controversial result. For $\mathbb{R}$, no one has ever
        explicitly constructed such a well-ordering—we only know it exists!

        ### Structural Induction

        Well-orderings enable **induction**: to prove $P(x)$ for all $x$ in a well-ordered set:

        1. **Base case**: Prove $P(m)$ for the minimum element $m$
        2. **Inductive step**: Prove that if $P(y)$ for all $y < x$, then $P(x)$
        3. **Conclusion**: $P(x)$ holds for all $x$

        **Why it works**: If $P$ failed somewhere, consider the set $\{x : \neg P(x)\}$.
        By well-ordering, this set has a minimum $x_0$. But then $P(y)$ holds for all
        $y < x_0$, so by the inductive step, $P(x_0)$ holds. Contradiction!

        ### Transfinite Induction

        We can extend induction beyond $\mathbb{N}$ to any well-ordered set, including
        **ordinal numbers** that describe different "sizes" of well-orderings.

        This is the foundation for much of set theory and the study of infinite structures.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Summary: The Architecture of Sets

        ### The Axioms (ZFC)

        | Axiom | What it provides |
        |-------|------------------|
        | Extensionality | Sets are determined by elements |
        | Empty Set | The foundation: $\emptyset$ exists |
        | Pairing | Build $\{a, b\}$ from $a$ and $b$ |
        | Union | Combine families of sets |
        | Power Set | All subsets form a set |
        | Infinity | Infinite sets exist ($\mathbb{N}$) |
        | Separation | Carve out subsets by properties |
        | Replacement | Functions preserve "set-ness" |
        | Regularity | No circular membership |
        | Choice | Selection functions exist |

        ### Key Properties of Relations

        | Property | Definition | Example |
        |----------|------------|---------|
        | Reflexive | $a \, R \, a$ | $\leq$ |
        | Symmetric | $a \, R \, b \Rightarrow b \, R \, a$ | $=$ |
        | Antisymmetric | $a \, R \, b \land b \, R \, a \Rightarrow a = b$ | $\leq$ |
        | Transitive | $a \, R \, b \land b \, R \, c \Rightarrow a \, R \, c$ | $<$ |

        ### Identity Elements

        | Structure | Operation | Identity |
        |-----------|-----------|----------|
        | Sets | Union $\cup$ | $\emptyset$ |
        | Sets | Intersection $\cap$ | $U$ (universal) |
        | Functions | Composition $\circ$ | $\text{id}$ |
        | Numbers | Addition $+$ | $0$ |
        | Numbers | Multiplication $\times$ | $1$ |

        ### Historical Sources and Further Reading

        - [Set Theory from Cantor to Cohen (Kanamori)](https://math.bu.edu/people/aki/16.pdf)
        - [Zermelo's Axiomatization (1908)](https://www.jstor.org/stable/2369881)
        - [Halmos: Naive Set Theory](https://link.springer.com/book/10.1007/978-1-4757-1645-0)
        - [Enderton: Elements of Set Theory](https://www.elsevier.com/books/elements-of-set-theory/enderton/978-0-12-238440-0)
        - [3Blue1Brown: How big is infinity?](https://www.youtube.com/watch?v=s86-Z-CbaHA)
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

        ---

        **Next**: In our next exploration, we'll dive into **linear algebra**—vector spaces,
        linear transformations, and the geometric structures that underpin everything from
        physics to machine learning.
        """
    )
    return


if __name__ == "__main__":
    app.run()
