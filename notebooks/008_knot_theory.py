"""
Knot Theory: The Mathematics of Tangles and Topology

An introduction to knot theory from its origins in 19th-century physics to modern
applications in DNA biology and quantum computing, covering knot diagrams, crossings,
invariants, and the Reidemeister moves.
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

    from math_explorations.visualization import (
        COLORS,
        SCENE_THEME,
        base_layout,
        create_timeline,
        style_subplot_axes,
    )

    return COLORS, SCENE_THEME, base_layout, create_timeline, go, make_subplots, np, style_subplot_axes


@app.cell
def _(np):
    def trefoil_xy(t):
        x = (np.sin(t) + 2 * np.sin(2 * t)) / 3.2
        y = (np.cos(t) - 2 * np.cos(2 * t)) / 3.2
        return x, y

    return (trefoil_xy,)


@app.cell
def _(mo):
    mo.md(r"""
    # Knot Theory: The Mathematics of Tangles and Topology

    *"A knot is a closed curve in space that does not intersect itself. The fundamental
    problem of knot theory is to determine when two knots are the same."*
    — W. B. Raymond Lickorish, *An Introduction to Knot Theory* (1997)

    ---

    ## What is a Knot?

    In everyday life, a knot is formed when you tangle a piece of string.
    In mathematics, a **knot** is a closed loop in three-dimensional space—imagine
    taking a piece of string, knotting it however you like, then gluing the two ends together.

    The central question of knot theory: **when are two knots really the same?**

    Two knots are **equivalent** if one can be continuously deformed into the other
    without cutting or passing strands through each other. This is surprisingly hard to
    determine—a loop that looks hopelessly tangled might secretly be an unknot
    (a simple closed loop with no real knotting at all).

    **What you'll learn:**
    - How knots are encoded as diagrams with crossings (vertices)
    - The three Reidemeister moves that relate equivalent diagrams
    - Knot invariants: numbers and polynomials that distinguish knots
    - Tricolorability and why the trefoil cannot be untangled
    - Applications in DNA biology, chemistry, and quantum physics
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part I: A Journey Through History

    ### Ancient Beginnings: Knots Before Mathematics

    Long before knot theory existed as a mathematical discipline, humans used knots
    for practical and decorative purposes. **Celtic knotwork** (400–900 CE) features
    intricate interlaced patterns with no free ends—mathematical knots in disguise.

    Ancient Peruvian **quipus** (600–1400 CE) encoded numerical information in knotted
    strings, suggesting a deep intuition that knot structure carries information.

    ### Gauss and the Linking Number (1833)

    The first mathematical treatment of knots came from **Carl Friedrich Gauss** (1777–1855).
    He introduced the **linking number**—an integer that measures how many times two
    closed curves wind around each other. For two curves $C_1$ and $C_2$:

    $$\text{lk}(C_1, C_2) = \frac{1}{4\pi} \oint_{C_1} \oint_{C_2}
    \frac{(\mathbf{r}_1 - \mathbf{r}_2)}{|\mathbf{r}_1 - \mathbf{r}_2|^3}
    \cdot (d\mathbf{r}_1 \times d\mathbf{r}_2)$$

    Gauss recognized that this integral is always an integer and is unchanged under
    continuous deformations—the first **knot invariant**.

    ### Lord Kelvin's Vortex Atoms (1867)

    The real birth of knot theory as a research program came from an unlikely source:
    **physics**. Lord Kelvin (William Thomson) proposed that atoms were knots in the
    luminiferous ether—the hypothetical medium thought to carry light. Different elements
    would correspond to different knots: hydrogen the simplest, helium slightly more complex.

    This theory was wrong, but it motivated **Peter Guthrie Tait** to begin the first
    systematic tabulation of knots (1876–1885). Tait classified all knots with up to
    7 crossings, laying the groundwork for modern knot tables.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Reidemeister and the Foundations (1926)

    The modern mathematical framework was established by **Kurt Reidemeister** (1893–1971),
    who proved a fundamental theorem: two knot diagrams represent the same knot
    if and only if one can be transformed into the other by a sequence of three
    simple moves—now called **Reidemeister moves**.

    This reduced an infinite topological problem (deformations of curves in 3D space)
    to a combinatorial problem (manipulating planar diagrams by local rules).

    ### The Jones Polynomial Revolution (1984)

    For decades, knot theory remained a niche field. Then in 1984, **Vaughan Jones**
    discovered a powerful new invariant—the **Jones polynomial**—using ideas from
    quantum physics (von Neumann algebras and statistical mechanics).

    This was revolutionary for several reasons:
    - It distinguished knots that all previous invariants could not tell apart
    - It connected knot theory to quantum field theory
    - It led directly to **topological quantum field theory** (Witten, 1989)
    - It earned Jones the **Fields Medal** in 1990

    ### DNA Topology and Applications (1980s–present)

    In the 1980s, molecular biologists discovered that DNA forms knots during
    replication and gene regulation. **Topoisomerases**—enzymes that cut and
    rejoin DNA strands—perform precise knot-theoretic operations. Understanding
    these enzymes requires knot theory.

    Today knot theory appears in:
    - **Biochemistry**: DNA and protein folding
    - **Materials science**: molecular knots and links
    - **Quantum computing**: topological qubits are protected by knot-like structures
    - **Statistical mechanics**: exactly solvable models

    ### Timeline

    | Year | Event |
    |------|-------|
    | 1833 | Gauss defines the linking number |
    | 1867 | Kelvin proposes vortex atom theory; Tait begins knot tables |
    | 1926 | Reidemeister proves his theorem on knot diagrams |
    | 1928 | Alexander defines the Alexander polynomial |
    | 1984 | Jones discovers the Jones polynomial |
    | 1990 | Jones receives Fields Medal; Witten connects knots to quantum field theory |
    | 1996 | DNA topoisomerases explained using knot theory |
    """)
    return


@app.cell
def _(create_timeline):
    create_timeline(
        [
            (1833, "Gauss\nlinking number", 1),
            (1867, "Kelvin vortex\natoms / Tait tables", -1),
            (1926, "Reidemeister\ntheorem", 1),
            (1928, "Alexander\npolynomial", -1),
            (1984, "Jones\npolynomial", 1),
            (1990, "Fields Medal\n(Jones) + Witten", -1),
            (1996, "DNA topology\nexplained", 1),
        ],
        title="History of Knot Theory",
        x_range=(1815, 2008),
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part II: Knots, Diagrams, and Crossings

    ### The Mathematical Definition

    Formally, a **knot** is a smooth embedding of the circle $S^1$ into three-dimensional
    space $\mathbb{R}^3$ (or equivalently the 3-sphere $S^3$):

    $$K: S^1 \hookrightarrow \mathbb{R}^3$$

    The image $K(S^1)$ is a closed curve with no self-intersections.

    Two knots $K_1$ and $K_2$ are **equivalent** (ambient isotopic) if there exists
    a continuous deformation of $\mathbb{R}^3$ taking $K_1$ to $K_2$. Intuitively:
    you can stretch, bend, and move the knot in any way, but you cannot cut it or
    pass it through itself.

    The simplest knot is the **unknot** $U$—just a plain circle with no crossings.
    Proving that a given knot *is* the unknot can be surprisingly hard.

    ### Knot Diagrams

    Working in 3D space is difficult, so we project knots onto a plane. A
    **knot diagram** is a generic planar projection where:

    - Strands cross transversally (not tangentially)
    - At each crossing, we indicate which strand passes **over** and which passes **under**
      using a break in the understrand

    The break convention: the strand that is broken (has a gap) goes **under**; the
    continuous strand goes **over**.

    A single knot has infinitely many diagrams—any projection from a generic direction gives one.
    The challenge: determine when two different-looking diagrams represent the same knot.
    """)
    return


@app.cell
def _(COLORS, base_layout, go, make_subplots, np, style_subplot_axes):
    _t = np.linspace(0, 2 * np.pi, 500)

    _knots = [
        ("The Unknot (0 crossings)", np.cos(_t), np.sin(_t), COLORS["primary"]),
        (
            "Trefoil Knot (3 crossings)",
            np.sin(_t) + 2 * np.sin(2 * _t),
            np.cos(_t) - 2 * np.cos(2 * _t),
            COLORS["secondary"],
        ),
        (
            "Figure-8 Knot (4 crossings)",
            (2 + np.cos(2 * _t)) * np.cos(3 * _t) / 4,
            (2 + np.cos(2 * _t)) * np.sin(3 * _t) / 4,
            COLORS["tertiary"],
        ),
    ]

    _fig = make_subplots(
        rows=1,
        cols=3,
        subplot_titles=[k[0] for k in _knots],
        horizontal_spacing=0.05,
    )

    for _col, (_, _x, _y, _c) in enumerate(_knots, 1):
        _fig.add_trace(
            go.Scatter(
                x=_x,
                y=_y,
                mode="lines",
                line={"color": _c, "width": 3},
                showlegend=False,
            ),
            row=1,
            col=_col,
        )
        _fig.update_xaxes(scaleanchor=f"y{_col if _col > 1 else ''}", row=1, col=_col)

    _fig.update_layout(**base_layout(title="Classic Knots (Parametric Projections)", height=350))
    style_subplot_axes(_fig)
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    The three most fundamental knots. Note that the curves above are *parametric projections*—
    the actual diagrams must also specify which strand goes over at each crossing.

    ### Vertices: Crossings in Knot Diagrams

    In knot theory, the word **vertex** (plural: **vertices**) refers to the crossing
    points in a knot diagram—the places where two strands of the projection meet.
    Each vertex has exactly two strands passing through it, one over and one under.

    At each crossing, we assign a **sign** based on orientation:

    A **positive crossing** (right-handed, $+1$) looks like this: if you rotate the
    overstrand clockwise to align with the understrand, you turn less than 180°.

    A **negative crossing** (left-handed, $-1$) is the mirror image.

    $$\text{writhe}(D) = \sum_{\text{crossings}} \text{sign}(\text{crossing})$$

    The **writhe** is the sum of all crossing signs. It is *not* a knot invariant
    (it changes under Reidemeister move I), but it plays a role in computing invariants.

    ### The Crossing Number

    The **crossing number** $c(K)$ of a knot $K$ is the minimum number of crossings
    over all possible diagrams of $K$.

    | Knot | Crossing Number | Name |
    |------|-----------------|------|
    | $U$ | 0 | Unknot |
    | $3_1$ | 3 | Trefoil |
    | $4_1$ | 4 | Figure-8 |
    | $5_1$ | 5 | Cinquefoil (torus knot) |
    | $5_2$ | 5 | Three-twist knot |

    Knots are classified by crossing number, with subscripts for knots sharing the
    same crossing number. There are 1 knot with 0 crossings, 1 with 3, 1 with 4,
    2 with 5, 3 with 6, 7 with 7, and so on.
    """)
    return


@app.cell
def _(COLORS, base_layout, go, make_subplots, np, style_subplot_axes):
    _fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=["Positive Crossing (+1)", "Negative Crossing (−1)"],
    )

    def _crossing_traces(fig, row, col, sign):
        # Over strand: goes left to right (or right to left for negative)
        # Under strand: goes up to down, with a gap near center
        gap = 0.18

        if sign == 1:
            # Positive: overstrand goes from bottom-left to top-right
            # Understrand goes from top-left to bottom-right (broken at center)
            ox = np.linspace(-1, 1, 100)
            oy = ox.copy()
            ux1 = np.linspace(-1, -gap, 40)
            uy1 = -ux1
            ux2 = np.linspace(gap, 1, 40)
            uy2 = -ux2
            over_color = COLORS["primary"]
            under_color = COLORS["secondary"]
        else:
            # Negative: overstrand goes from bottom-right to top-left
            ox = np.linspace(-1, 1, 100)
            oy = -ox.copy()
            ux1 = np.linspace(-1, -gap, 40)
            uy1 = ux1.copy()
            ux2 = np.linspace(gap, 1, 40)
            uy2 = ux2.copy()
            over_color = COLORS["secondary"]
            under_color = COLORS["primary"]

        fig.add_trace(
            go.Scatter(
                x=ox,
                y=oy,
                mode="lines",
                line={"color": over_color, "width": 6},
                name="overstrand",
                showlegend=False,
            ),
            row=row,
            col=col,
        )
        fig.add_trace(
            go.Scatter(
                x=ux1,
                y=uy1,
                mode="lines",
                line={"color": under_color, "width": 6},
                name="understrand",
                showlegend=False,
            ),
            row=row,
            col=col,
        )
        fig.add_trace(
            go.Scatter(
                x=ux2,
                y=uy2,
                mode="lines",
                line={"color": under_color, "width": 6},
                showlegend=False,
            ),
            row=row,
            col=col,
        )

        # Arrows to show orientation
        arrow_x = 0.5 if sign == 1 else -0.5
        arrow_dx = 0.3 if sign == 1 else -0.3
        fig.add_annotation(
            x=arrow_x + arrow_dx,
            y=arrow_x + arrow_dx if sign == 1 else -(arrow_x + arrow_dx),
            ax=arrow_x,
            ay=arrow_x if sign == 1 else -arrow_x,
            xref=f"x{col}",
            yref=f"y{col}",
            axref=f"x{col}",
            ayref=f"y{col}",
            arrowhead=2,
            arrowcolor=over_color,
            arrowwidth=2,
        )

    _crossing_traces(_fig, 1, 1, 1)
    _crossing_traces(_fig, 1, 2, -1)

    _fig.update_layout(**base_layout(title="Crossing Signs (Vertices in Knot Diagrams)", height=350))
    style_subplot_axes(_fig)
    for _c in range(1, 3):
        _fig.update_xaxes(range=[-1.3, 1.3], row=1, col=_c)
        _fig.update_yaxes(range=[-1.3, 1.3], scaleanchor=f"x{_c}", row=1, col=_c)

    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    **How to determine the sign of a crossing:**

    Orient the knot (choose a direction of travel along the strand). At a crossing:

    1. Point your right hand's fingers from the **overstrand direction** toward the
       **understrand direction** (rotating through the smaller angle)
    2. If your thumb points **up** (out of the page): **positive crossing** (+1)
    3. If your thumb points **down** (into the page): **negative crossing** (−1)

    Equivalently: at a positive crossing, the overstrand goes from lower-left to upper-right;
    at a negative crossing, from lower-right to upper-left (when both strands are oriented
    consistently).
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part III: The Reidemeister Moves

    ### The Central Theorem

    **Reidemeister's Theorem (1926)**: Two knot diagrams $D_1$ and $D_2$ represent
    equivalent knots if and only if $D_1$ can be transformed into $D_2$ by a finite
    sequence of **Reidemeister moves** (and planar isotopies—smooth deformations
    of the diagram not changing crossings).

    This is a profound reduction: instead of asking about all possible 3D deformations
    of a curve, we only need to consider three local moves on the 2D diagram.

    ### The Three Moves

    **Reidemeister Move I (Twist)**: A small loop can be created or removed.
    This changes the number of crossings by 1 and changes the writhe.

    $$\text{[loop with one crossing]} \longleftrightarrow \text{[no crossing]}$$

    **Reidemeister Move II (Poke)**: Two strands can be pushed through or past each other,
    creating or removing two crossings of opposite sign.

    $$\text{[two crossings of opposite sign]} \longleftrightarrow \text{[no crossings]}$$

    **Reidemeister Move III (Slide)**: A strand can be slid over or under a crossing.
    This preserves the number of crossings.

    $$\text{[strand over crossing]} \longleftrightarrow \text{[strand over crossing, rearranged]}$$

    A **knot invariant** is any quantity that is preserved under all three Reidemeister moves.
    This is how we prove that two knots are *different*: compute an invariant that gives
    different values for each.
    """)
    return


@app.cell
def _(COLORS, base_layout, go, make_subplots, np, style_subplot_axes):
    _fig = make_subplots(
        rows=1,
        cols=3,
        subplot_titles=["Move I: Twist", "Move II: Poke", "Move III: Slide"],
        horizontal_spacing=0.08,
    )

    # Move I: a loop (before) → straight strand (after)
    # Show "before" with a small loop
    _t = np.linspace(0, 2 * np.pi, 200)
    # Loop: a tight spiral that comes back
    _loop_t = np.linspace(-np.pi / 2, 3 * np.pi / 2, 300)
    _loop_x = 0.3 * np.cos(_loop_t)
    _loop_y = _loop_t / (2 * np.pi) - 0.5 * np.ones_like(_loop_t) + 0.3 * np.sin(_loop_t)

    # Straight strand (incoming) below the loop
    _s1_x = np.array([-0.8, -0.05])
    _s1_y = np.array([-0.8, -0.4])
    # Straight strand (outgoing) above
    _s2_x = np.array([0.05, 0.8])
    _s2_y = np.array([0.4, 0.8])

    _fig.add_trace(
        go.Scatter(
            x=np.concatenate([_s1_x, [np.nan], _loop_x, [np.nan], _s2_x]),
            y=np.concatenate([_s1_y, [np.nan], _loop_y, [np.nan], _s2_y]),
            mode="lines",
            line={"color": COLORS["primary"], "width": 3},
            showlegend=False,
        ),
        row=1,
        col=1,
    )

    # Arrow between: ↔
    _fig.add_annotation(
        x=0.0,
        y=0.0,
        text="<b>⟺</b>",
        font={"color": COLORS["quaternary"], "size": 20},
        showarrow=False,
        xref="x1",
        yref="y1",
    )

    # Straight strand
    _fig.add_trace(
        go.Scatter(
            x=[-0.8, 0.8],
            y=[-0.8, 0.8],
            mode="lines",
            line={"color": COLORS["tertiary"], "width": 3, "dash": "dot"},
            showlegend=False,
        ),
        row=1,
        col=1,
    )

    # Move II: two crossings → separated strands
    # Before: two strands crossing twice
    _t2 = np.linspace(0, np.pi, 100)
    _arc1_x = -0.5 + 0.5 * np.cos(_t2 + np.pi)
    _arc1_y = 0.5 * np.sin(_t2)
    _arc2_x = 0.5 + 0.5 * np.cos(_t2)
    _arc2_y = 0.5 * np.sin(_t2)

    _fig.add_trace(
        go.Scatter(
            x=np.concatenate([[-0.9], _arc1_x, _arc2_x, [0.9]]),
            y=np.concatenate([[0], _arc1_y, _arc2_y, [0]]),
            mode="lines",
            line={"color": COLORS["primary"], "width": 3},
            showlegend=False,
        ),
        row=1,
        col=2,
    )

    # Straight lines
    _fig.add_trace(
        go.Scatter(
            x=[-0.9, 0.9],
            y=[0.5, 0.5],
            mode="lines",
            line={"color": COLORS["secondary"], "width": 3},
            showlegend=False,
        ),
        row=1,
        col=2,
    )

    _fig.add_annotation(
        x=0.0,
        y=-0.5,
        text="<b>⟺</b>",
        font={"color": COLORS["quaternary"], "size": 20},
        showarrow=False,
        xref="x2",
        yref="y2",
    )

    _fig.add_trace(
        go.Scatter(
            x=[-0.9, 0.9],
            y=[-0.6, -0.6],
            mode="lines",
            line={"color": COLORS["primary"], "width": 3, "dash": "dot"},
            showlegend=False,
        ),
        row=1,
        col=2,
    )
    _fig.add_trace(
        go.Scatter(
            x=[-0.9, 0.9],
            y=[-0.9, -0.9],
            mode="lines",
            line={"color": COLORS["secondary"], "width": 3, "dash": "dot"},
            showlegend=False,
        ),
        row=1,
        col=2,
    )

    # Move III: slide a strand over a crossing
    # Triangle of three strands
    _fig.add_trace(
        go.Scatter(
            x=[-0.7, 0, 0.7, -0.7],
            y=[-0.6, 0.6, -0.6, -0.6],
            mode="lines",
            line={"color": COLORS["primary"], "width": 3},
            showlegend=False,
        ),
        row=1,
        col=3,
    )
    _fig.add_trace(
        go.Scatter(
            x=[-0.9, 0.9],
            y=[0.1, 0.1],
            mode="lines",
            line={"color": COLORS["secondary"], "width": 3},
            showlegend=False,
        ),
        row=1,
        col=3,
    )

    _fig.add_annotation(
        x=0.0,
        y=-0.3,
        text="<b>⟺</b>",
        font={"color": COLORS["quaternary"], "size": 20},
        showarrow=False,
        xref="x3",
        yref="y3",
    )

    _fig.add_trace(
        go.Scatter(
            x=[-0.7, 0, 0.7, -0.7],
            y=[0.6, -0.6, 0.6, 0.6],
            mode="lines",
            line={"color": COLORS["primary"], "width": 3, "dash": "dot"},
            showlegend=False,
        ),
        row=1,
        col=3,
    )
    _fig.add_trace(
        go.Scatter(
            x=[-0.9, 0.9],
            y=[-0.1, -0.1],
            mode="lines",
            line={"color": COLORS["secondary"], "width": 3, "dash": "dot"},
            showlegend=False,
        ),
        row=1,
        col=3,
    )

    _fig.update_layout(**base_layout(title="The Three Reidemeister Moves (solid ↔ dashed)", height=380))
    style_subplot_axes(_fig)
    for _c in range(1, 4):
        _fig.update_xaxes(range=[-1.1, 1.1], row=1, col=_c)
        _fig.update_yaxes(range=[-1.1, 1.1], row=1, col=_c)

    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    **Key observations:**

    - **Move I** changes the writhe (crossing sum) by ±1, so writhe is NOT an invariant
    - **Move II** preserves the writhe (the two new crossings have opposite signs)
    - **Move III** preserves both the writhe and crossing count

    Any quantity left unchanged by all three moves is a valid knot invariant.

    **The hard part**: Move I is local and easy. Move II creates/removes two crossings
    that cancel. Move III is the tricky one—it corresponds to the triangle inequality
    in braid theory and is the most computationally complex.

    Proving something is a knot invariant requires checking it is preserved under
    all three moves. This is often done algebraically.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part IV: Knot Invariants

    ### What is an Invariant?

    A **knot invariant** is a function $f$ defined on knots such that
    if $K_1 \sim K_2$ (equivalent knots), then $f(K_1) = f(K_2)$.

    Equivalently (by Reidemeister's theorem): $f$ is an invariant if it is unchanged
    by all three Reidemeister moves.

    **Important**: $f(K_1) = f(K_2)$ does NOT necessarily mean $K_1 \sim K_2$.
    An invariant can fail to distinguish non-equivalent knots. A **complete invariant**
    would satisfy the converse—but no simple complete invariant is known.

    ### The Unknotting Number

    The **unknotting number** $u(K)$ is the minimum number of crossing changes
    (switching a crossing from over to under or vice versa) needed to convert $K$
    into the unknot.

    - $u(\text{unknot}) = 0$
    - $u(\text{trefoil}) = 1$
    - $u(\text{figure-8}) = 1$
    - $u(\text{cinquefoil}) = 2$

    Computing the unknotting number is notoriously hard—it is not even known for
    all knots with 10 or fewer crossings.

    ### The Determinant of a Knot

    The **determinant** $\det(K)$ is an integer invariant computed from the knot
    diagram. For a knot with $n$ crossings, build an $n \times n$ matrix from the
    crossing relations, remove one row and column, and take the absolute value of
    the determinant.

    | Knot | Determinant |
    |------|-------------|
    | Unknot $U$ | 1 |
    | Trefoil $3_1$ | 3 |
    | Figure-8 $4_1$ | 5 |
    | Cinquefoil $5_1$ | 5 |
    | $5_2$ | 7 |

    Notice that the trefoil has determinant 3—this means **the trefoil is not the unknot**.
    Also notice that $5_1$ and $4_1$ both have determinant 5, so the determinant alone
    cannot distinguish them. We need more powerful invariants.
    """)
    return


@app.cell
def _(COLORS, base_layout, go, make_subplots, np, style_subplot_axes):
    _knots = ["Unknot", "Trefoil\n3₁", "Figure-8\n4₁", "Cinquefoil\n5₁", "5₂"]
    _crossing_numbers = [0, 3, 4, 5, 5]
    _determinants = [1, 3, 5, 5, 7]
    _unknotting = [0, 1, 1, 2, 1]

    _x = np.arange(len(_knots))
    _colors_cn = [COLORS["tertiary"], COLORS["primary"], COLORS["primary"], COLORS["primary"], COLORS["primary"]]
    _colors_det = [
        COLORS["tertiary"],
        COLORS["secondary"],
        COLORS["secondary"],
        COLORS["quaternary"],
        COLORS["secondary"],
    ]
    _colors_un = [COLORS["tertiary"], COLORS["accent1"], COLORS["accent1"], COLORS["quaternary"], COLORS["accent1"]]

    _fig = make_subplots(
        rows=1,
        cols=3,
        subplot_titles=["Crossing Number c(K)", "Determinant det(K)", "Unknotting Number u(K)"],
        horizontal_spacing=0.12,
    )

    for _col, (_vals, _colors, _name) in enumerate(
        [
            (_crossing_numbers, _colors_cn, "c(K)"),
            (_determinants, _colors_det, "det(K)"),
            (_unknotting, _colors_un, "u(K)"),
        ],
        1,
    ):
        _fig.add_trace(
            go.Bar(
                x=["U", "3₁", "4₁", "5₁", "5₂"],
                y=_vals,
                marker_color=_colors,
                text=_vals,
                textposition="outside",
                textfont={"color": COLORS["text"], "size": 13},
                name=_name,
                showlegend=False,
            ),
            row=1,
            col=_col,
        )

    _fig.update_layout(**base_layout(title="Comparing Knot Invariants for Classic Knots", height=380))
    style_subplot_axes(_fig, show_ticklabels=True)
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    The chart shows that no single invariant distinguishes all five knots:
    - Determinant 5 appears for both $4_1$ and $5_1$
    - Unknotting number 1 appears for $3_1$, $4_1$, and $5_2$

    This is why knot theorists keep discovering new invariants—each one captures
    different information about the knot's structure.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part V: Tricolorability

    ### A Simple but Powerful Invariant

    **Tricolorability** is one of the most elegant knot invariants—it requires
    no algebra, just colored pencils.

    A knot diagram is **tricolorable** if we can color each arc (a strand from one
    underpass to the next underpass) with one of three colors such that:

    1. **At least two different colors are used**
    2. **At every crossing**, the three arcs meeting at the crossing are either
       **all the same color** or **all different colors**

    An arc in a knot diagram runs from one undercrossing to the next undercrossing
    (passing over any crossings in between).

    **Theorem**: If a knot diagram is tricolorable, then every diagram of the same
    knot is tricolorable. (Proof: check that each Reidemeister move preserves
    tricolorability.)

    **Consequence**: Tricolorability is a knot invariant!

    ### The Trefoil is Not the Unknot

    - The **unknot** has only one arc. With the rule above, we cannot use two different
      colors—so the unknot is **not tricolorable**.

    - The **trefoil** has three arcs (one between each pair of crossings). We can color
      them three different colors, satisfying the rules at every crossing.

    Since the unknot is not tricolorable but the trefoil is, **the trefoil cannot be
    equivalent to the unknot**. The trefoil is genuinely knotted!

    This is a remarkable fact: tricolorability gives an elementary proof that the trefoil
    is a non-trivial knot, with no advanced topology required.
    """)
    return


@app.cell
def _(COLORS, base_layout, go, np, trefoil_xy):
    # Crossing parameter values (approximate, where projection self-intersects)
    # For the standard trefoil projection the three crossings occur near:
    _cross_t = [0.52, 0.52 + 2 * np.pi / 3, 0.52 + 4 * np.pi / 3]
    _gap = 0.22  # half-gap in t around each crossing for the break

    # Build arc segments: arc i runs from cross_t[i] + gap to cross_t[(i+1)%3] - gap
    _arc_colors = [COLORS["secondary"], COLORS["primary"], COLORS["tertiary"]]
    _arc_labels = ["Arc 1", "Arc 2", "Arc 3"]

    _fig = go.Figure()

    for _i in range(3):
        _t_start = _cross_t[_i] + _gap
        _t_end = _cross_t[(_i + 1) % 3] - _gap + (2 * np.pi if (_i + 1) % 3 == 0 else 0)
        if _t_end < _t_start:
            _t_end += 2 * np.pi
        _seg_t = np.linspace(_t_start % (2 * np.pi), _t_end % (2 * np.pi), 120)
        # Handle wrap-around
        if _t_end > 2 * np.pi:
            _seg_t = np.concatenate(
                [
                    np.linspace(_t_start, 2 * np.pi, 80),
                    np.linspace(0, _t_end - 2 * np.pi, 80),
                ]
            )
        _sx, _sy = trefoil_xy(_seg_t)
        _mx, _my = trefoil_xy(np.array([(_t_start + _t_end) / 2]))
        _fig.add_trace(
            go.Scatter(
                x=_sx,
                y=_sy,
                mode="lines",
                line={"color": _arc_colors[_i], "width": 7},
                name=_arc_labels[_i],
            )
        )
        _fig.add_annotation(
            x=float(_mx[0]) * 1.25,
            y=float(_my[0]) * 1.25,
            text=f"<b>{_arc_labels[_i]}</b>",
            font={"color": _arc_colors[_i], "size": 13},
            showarrow=False,
        )

    # Mark the three vertex crossings
    for _i, _ct in enumerate(_cross_t):
        _vx, _vy = trefoil_xy(np.array([_ct]))
        _fig.add_trace(
            go.Scatter(
                x=[float(_vx[0])],
                y=[float(_vy[0])],
                mode="markers",
                marker={"color": COLORS["quaternary"], "size": 16, "symbol": "circle"},
                showlegend=_i == 0,
                name="Vertex (crossing)",
                hovertemplate=f"Vertex {_i + 1}<extra></extra>",
            )
        )

    _fig.update_layout(
        **base_layout(
            title="Trefoil Knot: Three Arcs (colored) and Three Vertices (yellow)",
            xaxis={"visible": False, "range": [-1.4, 1.4], "scaleanchor": "y"},
            yaxis={"visible": False, "range": [-1.4, 1.4]},
            height=400,
        )
    )
    _fig
    return


@app.cell
def _(mo):
    arc1_color = mo.ui.dropdown(
        options={"Red": "red", "Blue": "blue", "Green": "green"},
        value="Red",
        label="Arc 1 (top)",
    )
    arc2_color = mo.ui.dropdown(
        options={"Red": "red", "Blue": "blue", "Green": "green"},
        value="Blue",
        label="Arc 2 (lower-left)",
    )
    arc3_color = mo.ui.dropdown(
        options={"Red": "red", "Blue": "blue", "Green": "green"},
        value="Green",
        label="Arc 3 (lower-right)",
    )
    return arc1_color, arc2_color, arc3_color


@app.cell
def _(arc1_color, arc2_color, arc3_color, mo):
    mo.vstack(
        [
            mo.md("### Trefoil Tricolorability Explorer"),
            mo.hstack([arc1_color, arc2_color, arc3_color], justify="start", gap=2),
        ]
    )
    return


@app.cell
def _(COLORS, arc1_color, arc2_color, arc3_color, base_layout, go, np, trefoil_xy):
    _c1 = arc1_color.value
    _c2 = arc2_color.value
    _c3 = arc3_color.value

    _color_map = {
        "red": COLORS["secondary"],
        "blue": COLORS["primary"],
        "green": COLORS["tertiary"],
    }
    _hex1 = _color_map[_c1]
    _hex2 = _color_map[_c2]
    _hex3 = _color_map[_c3]

    # Check validity
    _colors_used = {_c1, _c2, _c3}
    _valid_at_crossings = True
    for _pair in [(_c1, _c2, _c3), (_c2, _c3, _c1), (_c3, _c1, _c2)]:
        _s = set(_pair)
        if not (_s == {_c1, _c2, _c3} or len(_s) == 1):
            _valid_at_crossings = False
            break

    _uses_multiple = len(_colors_used) > 1
    _is_tricolorable = _valid_at_crossings and _uses_multiple

    # Draw trefoil with colored arcs
    # Arc 1: top arc
    _t1 = np.linspace(np.pi / 6, 5 * np.pi / 6, 100)
    _t2 = np.linspace(5 * np.pi / 6, 9 * np.pi / 6, 100)
    _t3 = np.linspace(9 * np.pi / 6, 13 * np.pi / 6, 100)

    _x1, _y1 = trefoil_xy(_t1)
    _x2, _y2 = trefoil_xy(_t2)
    _x3, _y3 = trefoil_xy(_t3)

    _fig = go.Figure()

    _fig.add_trace(
        go.Scatter(
            x=_x1,
            y=_y1,
            mode="lines",
            line={"color": _hex1, "width": 7},
            name=f"Arc 1 ({_c1})",
        )
    )
    _fig.add_trace(
        go.Scatter(
            x=_x2,
            y=_y2,
            mode="lines",
            line={"color": _hex2, "width": 7},
            name=f"Arc 2 ({_c2})",
        )
    )
    _fig.add_trace(
        go.Scatter(
            x=_x3,
            y=_y3,
            mode="lines",
            line={"color": _hex3, "width": 7},
            name=f"Arc 3 ({_c3})",
        )
    )

    _status_color = COLORS["tertiary"] if _is_tricolorable else COLORS["secondary"]
    _status = "VALID tricoloring ✓" if _is_tricolorable else "INVALID — check crossing rules ✗"
    if not _uses_multiple:
        _status = "INVALID — must use at least 2 colors ✗"

    _fig.add_annotation(
        x=0,
        y=-1.1,
        text=f"<b>{_status}</b>",
        font={"color": _status_color, "size": 15},
        showarrow=False,
    )

    _fig.update_layout(
        **base_layout(
            title="Trefoil Knot — Color Each Arc",
            xaxis={
                "gridcolor": COLORS["grid"],
                "zerolinecolor": COLORS["text_secondary"],
                "showticklabels": False,
                "range": [-1.3, 1.3],
                "scaleanchor": "y",
            },
            yaxis={
                "gridcolor": COLORS["grid"],
                "zerolinecolor": COLORS["text_secondary"],
                "showticklabels": False,
                "range": [-1.3, 1.3],
            },
            height=480,
        )
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    Try the coloring Red/Blue/Green for the three arcs—it satisfies both rules and
    proves the trefoil is tricolorable. Try using only one color—it violates rule 1.
    Try Red/Red/Blue—it violates rule 2 (two arcs the same, one different at a crossing).

    **The crossing rule in detail:** At each crossing of the trefoil, three arcs meet:
    the overstrand (which forms one arc) and the two parts of the understrand (which
    form two different arcs). The rule says these three arcs must be all the same color
    or all different colors.

    **Fox's theorem**: A knot $K$ is tricolorable if and only if $\det(K)$ is divisible by 3.

    | Knot | det(K) | 3 \| det? | Tricolorable? |
    |------|--------|-----------|---------------|
    | Unknot | 1 | No | No |
    | Trefoil $3_1$ | 3 | Yes | **Yes** |
    | Figure-8 $4_1$ | 5 | No | No |
    | Cinquefoil $5_1$ | 5 | No | No |
    | $5_2$ | 7 | No | No |
    | $8_{18}$ | 21 | Yes | **Yes** |

    This connects the elementary coloring argument to the algebraic determinant invariant.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part VI: Polynomial Invariants

    ### The Alexander Polynomial (1928)

    **James Alexander** discovered the first polynomial invariant in 1928. For each
    oriented knot $K$, the **Alexander polynomial** $\Delta_K(t)$ is a Laurent polynomial
    (integer coefficients, possibly negative powers of $t$) defined up to units $\pm t^n$.

    The polynomial is computed from the **Seifert matrix** of the knot—a matrix built
    from a surface bounded by the knot (a **Seifert surface**).

    | Knot | $\Delta_K(t)$ |
    |------|---------------|
    | Unknot | $1$ |
    | Trefoil $3_1$ | $t^{-1} - 1 + t$ |
    | Figure-8 $4_1$ | $-t^{-1} + 3 - t$ |
    | Cinquefoil $5_1$ | $t^{-2} - t^{-1} + 1 - t + t^2$ |
    | $5_2$ | $2t^{-1} - 3 + 2t$ |

    **Evaluating at $t = -1$** gives the determinant: $\Delta_K(-1) = \pm \det(K)$.
    This connects the polynomial to the simpler integer invariant.

    **Limitation**: The Alexander polynomial cannot distinguish a knot from its mirror
    image. The trefoil and its mirror image (left-handed vs. right-handed trefoil)
    have the same Alexander polynomial.

    ### The Jones Polynomial (1984)

    **Vaughan Jones** discovered a far more powerful polynomial invariant. The
    **Jones polynomial** $V_K(t)$ is also a Laurent polynomial, but it *can* distinguish
    a knot from its mirror image in many cases.

    | Knot | $V_K(t)$ |
    |------|----------|
    | Unknot | $1$ |
    | Left trefoil $\overline{3_1}$ | $-t^{-4} + t^{-3} + t^{-1}$ |
    | Right trefoil $3_1$ | $-t^4 + t^3 + t$ |
    | Figure-8 $4_1$ | $t^2 - t + 1 - t^{-1} + t^{-2}$ |

    Notice that the left and right trefoils have *different* Jones polynomials
    (one replaces $t$ by $t^{-1}$ in the other). This proves the two trefoils are
    genuinely different knots—neither can be deformed into the other!

    **The Kauffman bracket** is a key tool for computing the Jones polynomial.
    It assigns a polynomial to any unoriented knot diagram via local "skein" rules
    at each crossing.
    """)
    return


@app.cell
def _(COLORS, base_layout, go, np):
    _t_vals = np.linspace(-2, 2, 400)

    # Alexander polynomials
    def _alex_trefoil(t):
        return t ** (-1) - 1 + t

    def _alex_figure8(t):
        return -(t ** (-1)) + 3 - t

    def _alex_unknot(t):
        return np.ones_like(t)

    _fig = go.Figure()

    _fig.add_trace(
        go.Scatter(
            x=_t_vals,
            y=_alex_unknot(_t_vals),
            mode="lines",
            line={"color": COLORS["tertiary"], "width": 3},
            name="Unknot: Δ(t) = 1",
        )
    )
    _fig.add_trace(
        go.Scatter(
            x=_t_vals,
            y=_alex_trefoil(_t_vals),
            mode="lines",
            line={"color": COLORS["secondary"], "width": 3},
            name="Trefoil: Δ(t) = t⁻¹ − 1 + t",
        )
    )
    _fig.add_trace(
        go.Scatter(
            x=_t_vals,
            y=_alex_figure8(_t_vals),
            mode="lines",
            line={"color": COLORS["primary"], "width": 3},
            name="Figure-8: Δ(t) = −t⁻¹ + 3 − t",
        )
    )

    # Mark t = -1 values
    for _f, _label, _color, _det in [
        (_alex_unknot, "det=1", COLORS["tertiary"], 1),
        (_alex_trefoil, "det=3", COLORS["secondary"], 3),
        (_alex_figure8, "det=5", COLORS["primary"], 5),
    ]:
        _y_val = _f(np.array([-1.0]))[0]
        _fig.add_trace(
            go.Scatter(
                x=[-1],
                y=[_y_val],
                mode="markers+text",
                marker={"color": _color, "size": 12},
                text=[f" {_label}"],
                textposition="middle right",
                textfont={"color": _color, "size": 11},
                showlegend=False,
            )
        )

    _fig.add_vline(x=-1, line_color=COLORS["quaternary"], line_width=1, line_dash="dash")
    _fig.add_annotation(
        x=-1,
        y=6,
        text="t = −1<br>(gives determinant)",
        font={"color": COLORS["quaternary"], "size": 12},
        showarrow=False,
        xshift=60,
    )

    _fig.update_layout(
        **base_layout(
            title="Alexander Polynomials (evaluated at t = −1 gives the determinant)",
            xaxis={
                "gridcolor": COLORS["grid"],
                "zerolinecolor": COLORS["text_secondary"],
                "title": "t",
                "range": [-2, 2],
            },
            yaxis={
                "gridcolor": COLORS["grid"],
                "zerolinecolor": COLORS["text_secondary"],
                "title": "Δ(t)",
                "range": [-5, 8],
            },
            height=420,
        )
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    The graph shows that at $t = -1$, the three Alexander polynomials evaluate to
    $\pm 1, \pm 3, \pm 5$—the determinants of the respective knots.

    **The skein relation** provides a recursive way to compute polynomial invariants.
    For the Alexander polynomial:

    $$\Delta_{K_+}(t) - \Delta_{K_-}(t) = (t^{1/2} - t^{-1/2}) \Delta_{K_0}(t)$$

    Here $K_+$, $K_-$, and $K_0$ are three knots that differ only at a single crossing:
    - $K_+$: positive crossing
    - $K_-$: negative crossing
    - $K_0$: the crossing is "smoothed" (two strands reconnected without crossing)

    This turns the problem of computing a knot invariant into a recursive procedure.
    """)
    return


@app.cell
def _(COLORS, base_layout, go, make_subplots, np, style_subplot_axes):
    _fig = make_subplots(
        rows=1,
        cols=3,
        subplot_titles=["K₊  (positive crossing)", "K₋  (negative crossing)", "K₀  (smoothed / 0-resolution)"],
        horizontal_spacing=0.08,
    )

    _gap = 0.18

    def _add_crossing(fig, col, kind):
        # kind: '+', '-', '0'
        # All: two strands passing through origin region
        # Strand A goes from bottom-left to top-right (for +), top-left to bottom-right (for -)
        # Strand B is the other; broken at center for understrand

        if kind == "+":
            # Over: bottom-left → top-right  (slope +1)
            # Under (broken): top-left → bottom-right  (slope -1)
            o_x = np.linspace(-1, 1, 80)
            o_y = o_x.copy()
            u1_x = np.linspace(-1, -_gap, 30)
            u1_y = -u1_x
            u2_x = np.linspace(_gap, 1, 30)
            u2_y = -u2_x
            oc, uc = COLORS["primary"], COLORS["secondary"]
        elif kind == "-":
            # Over: top-left → bottom-right  (slope -1)
            # Under (broken): bottom-left → top-right  (slope +1)
            o_x = np.linspace(-1, 1, 80)
            o_y = -o_x.copy()
            u1_x = np.linspace(-1, -_gap, 30)
            u1_y = u1_x.copy()
            u2_x = np.linspace(_gap, 1, 30)
            u2_y = u2_x.copy()
            oc, uc = COLORS["secondary"], COLORS["primary"]
        else:  # '0' smoothing: two arcs, no crossing
            # Top arc: connects (-1, +1) to (+1, +1) curving upward
            _th1 = np.linspace(np.pi, 0, 60)
            o_x = np.cos(_th1)
            o_y = np.sin(_th1) * 0.6 + 0.5
            # Bottom arc: connects (-1, -1) to (+1, -1) curving downward
            _th2 = np.linspace(np.pi, 2 * np.pi, 60)
            u1_x = np.cos(_th2)
            u1_y = np.sin(_th2) * 0.6 - 0.5
            u2_x = np.array([])
            u2_y = np.array([])
            oc = uc = COLORS["tertiary"]

        fig.add_trace(
            go.Scatter(x=o_x, y=o_y, mode="lines", line={"color": oc, "width": 6}, showlegend=False), row=1, col=col
        )
        fig.add_trace(
            go.Scatter(x=u1_x, y=u1_y, mode="lines", line={"color": uc, "width": 6}, showlegend=False), row=1, col=col
        )
        if len(u2_x):
            fig.add_trace(
                go.Scatter(x=u2_x, y=u2_y, mode="lines", line={"color": uc, "width": 6}, showlegend=False),
                row=1,
                col=col,
            )

    _add_crossing(_fig, 1, "+")
    _add_crossing(_fig, 2, "-")
    _add_crossing(_fig, 3, "0")

    _fig.update_layout(
        **base_layout(title="Skein Triple: the three local diagrams related by the skein relation", height=320)
    )
    style_subplot_axes(_fig)
    for _c in range(1, 4):
        _fig.update_xaxes(range=[-1.3, 1.3], row=1, col=_c)
        _fig.update_yaxes(range=[-1.3, 1.3], row=1, col=_c)
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part VII: 3D Knot Visualization

    ### Knots as Curves in Space

    So far we have seen 2D projections (diagrams). Knots live in 3D space, and
    visualizing them there can provide intuition about their structure.

    Common parametric representations:

    **Torus knots** $T(p,q)$ wind $p$ times around the "longitude" and $q$ times
    around the "meridian" of a torus:

    $$x(t) = (R + r\cos(qt))\cos(pt)$$
    $$y(t) = (R + r\cos(qt))\sin(pt)$$
    $$z(t) = r\sin(qt)$$

    The trefoil is the torus knot $T(2,3)$.
    """)
    return


@app.cell
def _(mo):
    knot_selector = mo.ui.dropdown(
        options={
            "Trefoil T(2,3)": "trefoil",
            "Cinquefoil T(2,5)": "cinquefoil",
            "Torus knot T(3,4)": "t34",
            "Figure-8 knot": "fig8",
        },
        value="Trefoil T(2,3)",
        label="Choose a knot:",
    )
    return (knot_selector,)


@app.cell
def _(knot_selector, mo):
    mo.hstack(
        [
            mo.md("### 3D Knot Explorer"),
            knot_selector,
        ]
    )
    return


@app.cell
def _(COLORS, SCENE_THEME, base_layout, go, knot_selector, np):
    _choice = knot_selector.value
    _t = np.linspace(0, 2 * np.pi, 600)

    def _torus_knot(R, r, p, q, t):
        return (R + r * np.cos(q * t)) * np.cos(p * t), (R + r * np.cos(q * t)) * np.sin(p * t), r * np.sin(q * t)

    if _choice == "trefoil":
        _x, _y, _z = _torus_knot(3, 1, 2, 3, _t)
        _title = "Trefoil Knot T(2,3)"
        _color = COLORS["secondary"]
    elif _choice == "cinquefoil":
        _x, _y, _z = _torus_knot(3, 1, 2, 5, _t)
        _title = "Cinquefoil T(2,5)"
        _color = COLORS["quaternary"]
    elif _choice == "t34":
        _x, _y, _z = _torus_knot(3, 1, 3, 4, _t)
        _title = "Torus Knot T(3,4)"
        _color = COLORS["accent1"]
    else:  # figure-8
        _x = (2 + np.cos(2 * _t)) * np.cos(3 * _t)
        _y = (2 + np.cos(2 * _t)) * np.sin(3 * _t)
        _z = np.sin(4 * _t)
        _title = "Figure-8 Knot"
        _color = COLORS["tertiary"]

    _fig = go.Figure()

    _fig.add_trace(
        go.Scatter3d(
            x=_x,
            y=_y,
            z=_z,
            mode="lines",
            line={"color": _color, "width": 6},
            name=_title,
        )
    )

    _fig.update_layout(
        **base_layout(
            title=_title + " (drag to rotate)",
            scene=SCENE_THEME,
            height=500,
        )
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    Drag the 3D plot to rotate and explore the knot from different angles.

    **Torus knots** all live on the surface of a torus (donut shape). The torus knot
    $T(p,q)$ winds $p$ times around the big circle and $q$ times around the small
    circle. Two torus knots $T(p,q)$ and $T(q,p)$ are equivalent.
    When $\gcd(p,q)=1$, $T(p,q)$ is a knot; otherwise it is a link
    with $\gcd(p,q)$ components. $T(p,q) \neq T(p', q')$
    unless $\{p,q\} = \{p', q'\}$.

    **Torus knot invariants:**
    - Crossing number: $c(T(2,n)) = n$ for odd $n \geq 3$
    - The genus (complexity of the bounding surface): $g(T(p,q)) = \frac{(p-1)(q-1)}{2}$
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part VIII: Links and Multi-component Systems

    ### Beyond Single Knots

    A **link** is a collection of knots in 3D space that may be interlinked.
    Each individual knot in a link is a **component**. If the components can be
    completely separated (no interlinking), the link is called a **split link**.

    The simplest non-trivial link: **the Hopf link** consists of two circles,
    each passing through the other. The linking number is $\pm 1$.

    The **Borromean rings** are three circles arranged so that no two are linked,
    but all three together cannot be separated. Removing any one ring frees the
    other two. This is a remarkable topological property.

    $$\text{lk}(C_1, C_2) = \text{lk}(C_2, C_3) = \text{lk}(C_1, C_3) = 0$$

    ...yet the three rings are inseparable.

    ### Links in Chemistry and Biology

    **Catenanes** are molecules in which rings are mechanically interlocked—
    chemical Hopf links. They have been synthesized since the 1960s.

    **DNA replication** creates interlinked DNA circles (catenated molecules)
    that must be separated by **topoisomerase II**, which cuts both strands of
    one DNA molecule, passes the other through, and reseals—computing a crossing
    change in knot theory.

    The enzyme's action on DNA topology directly corresponds to Reidemeister moves!
    Mathematicians and biologists collaborate to understand these mechanisms.
    """)
    return


@app.cell
def _(COLORS, base_layout, go, make_subplots, np, style_subplot_axes):
    _fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=["Hopf Link (lk = 1)", "Borromean Rings"],
        horizontal_spacing=0.08,
    )

    # Hopf link: two interlocked circles
    _t = np.linspace(0, 2 * np.pi, 200)

    # Circle 1 (left, slightly back)
    _c1x = 0.7 * np.cos(_t) - 0.3
    _c1y = 0.7 * np.sin(_t)

    # Circle 2 (right, slightly front) - intersects circle 1
    _c2x = 0.7 * np.cos(_t) + 0.3
    _c2y = 0.7 * np.sin(_t)

    _fig.add_trace(
        go.Scatter(
            x=_c1x,
            y=_c1y,
            mode="lines",
            line={"color": COLORS["primary"], "width": 5},
            name="Component 1",
            showlegend=True,
        ),
        row=1,
        col=1,
    )

    _fig.add_trace(
        go.Scatter(
            x=_c2x,
            y=_c2y,
            mode="lines",
            line={"color": COLORS["secondary"], "width": 5},
            name="Component 2",
            showlegend=True,
        ),
        row=1,
        col=1,
    )

    # Borromean rings: three circles in characteristic arrangement
    # Three circles of radius 0.6 at 120° apart, slightly offset
    _r_bor = 0.65
    _centers = [
        (0, 0.5),
        (-0.45, -0.25),
        (0.45, -0.25),
    ]
    _bor_colors = [COLORS["primary"], COLORS["secondary"], COLORS["tertiary"]]
    _bor_names = ["Ring A", "Ring B", "Ring C"]

    for (_cx, _cy), _bc, _bn in zip(_centers, _bor_colors, _bor_names):
        _fig.add_trace(
            go.Scatter(
                x=_r_bor * np.cos(_t) + _cx,
                y=_r_bor * np.sin(_t) + _cy,
                mode="lines",
                line={"color": _bc, "width": 4},
                name=_bn,
                showlegend=False,
            ),
            row=1,
            col=2,
        )

    _fig.add_annotation(
        x=0,
        y=-1.1,
        text="Removing any ring frees the other two",
        font={"color": COLORS["quaternary"], "size": 11},
        showarrow=False,
        xref="x2",
        yref="y2",
    )

    _fig.update_layout(**base_layout(title="Links: Hopf Link and Borromean Rings", height=380))
    style_subplot_axes(_fig)
    for _c in range(1, 3):
        _fig.update_xaxes(range=[-1.3, 1.3], row=1, col=_c)
        _fig.update_yaxes(range=[-1.3, 1.3], row=1, col=_c)

    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part IX: Applications

    ### DNA Topology

    DNA in living cells is not a linear strand—it forms closed loops (in bacteria)
    or loops constrained by proteins (in eukaryotes). The topology of these loops
    matters enormously for biological function.

    **Supercoiling**: DNA can be over- or under-wound, creating torsional stress
    that affects gene expression. The **linking number** $\text{Lk}$ of the two
    DNA strands relates to the twist $\text{Tw}$ and writhe $\text{Wr}$:

    $$\text{Lk} = \text{Tw} + \text{Wr}$$

    This is **White's formula**—a deep theorem connecting a topological invariant
    (Lk) to geometric quantities (Tw and Wr).

    **Topoisomerases** manage DNA topology by:
    - **Type I**: Cut one strand, rotate, reseal. Changes Lk by ±1.
    - **Type II**: Cut both strands, pass a loop through, reseal. Changes Lk by ±2.

    Many antibiotics and cancer drugs target topoisomerases—understanding their
    mechanism requires knot theory!

    ### Quantum Computing: Topological Qubits

    Quantum computers are extremely sensitive to errors from environmental noise.
    **Topological quantum computing** (proposed by Kitaev, 1997) encodes information
    in the topology of quantum states, making it intrinsically protected from local errors.

    The key idea: certain particles called **anyons** in 2D quantum systems
    follow braiding statistics—the quantum state changes when anyons are moved around
    each other, and the change depends only on the *topology* of the path (the braid),
    not on its exact shape.

    A quantum gate is implemented by braiding anyons—a physical Reidemeister move!
    The computation is robust because small perturbations cannot change the topology
    of the braid.

    **Microsoft's Station Q** is one of several major research efforts to build
    topological qubits using **Majorana fermions** in semiconductor nanowires.

    ### Molecular Knots

    Chemists have synthesized molecular knots—actual knotted molecules:
    - **Trefoil knot** (1989, Dietrich-Buchecker & Sauvage): first molecular knot
    - **Figure-8 knot** (2012, Leigh group): first molecular figure-8 knot
    - **$8_{18}$ knot** (2020): most complex molecular knot to date

    These molecules have unique properties (chirality, mechanical strength) with
    potential applications in molecular machines and materials science.
    """)
    return


@app.cell
def _(COLORS, SCENE_THEME, base_layout, go, np):
    _t = np.linspace(0, 4 * np.pi, 400)

    # Two DNA strands (double helix simplified)
    _r = 0.3
    _rise = 1.5

    _strand1_x = _r * np.cos(_t)
    _strand1_y = _r * np.sin(_t)
    _strand1_z = _rise * _t / (2 * np.pi)

    _strand2_x = _r * np.cos(_t + np.pi)
    _strand2_y = _r * np.sin(_t + np.pi)
    _strand2_z = _rise * _t / (2 * np.pi)

    _fig = go.Figure()

    _fig.add_trace(
        go.Scatter3d(
            x=_strand1_x,
            y=_strand1_y,
            z=_strand1_z,
            mode="lines",
            line={"color": COLORS["primary"], "width": 5},
            name="Strand 1",
        )
    )
    _fig.add_trace(
        go.Scatter3d(
            x=_strand2_x,
            y=_strand2_y,
            z=_strand2_z,
            mode="lines",
            line={"color": COLORS["secondary"], "width": 5},
            name="Strand 2",
        )
    )

    # Add rungs (base pairs)
    _rung_indices = np.arange(0, len(_t), 25)
    for _i in _rung_indices:
        _fig.add_trace(
            go.Scatter3d(
                x=[_strand1_x[_i], _strand2_x[_i]],
                y=[_strand1_y[_i], _strand2_y[_i]],
                z=[_strand1_z[_i], _strand2_z[_i]],
                mode="lines",
                line={"color": COLORS["quaternary"], "width": 2},
                showlegend=False,
            )
        )

    _scene = {**SCENE_THEME, "zaxis": {**SCENE_THEME["zaxis"], "title": "Position along DNA"}}
    _fig.update_layout(
        **base_layout(
            title="DNA Double Helix: The linking number counts how the two strands wind around each other",
            scene=_scene,
            height=450,
        )
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    The DNA double helix completes approximately one full helical turn every
    10.5 base pairs. For a relaxed circular DNA with $N$ base pairs, the linking
    number is $\text{Lk}_0 \approx N/10.5$.

    When DNA is replicated, the two daughter chromosomes are topologically linked—
    catenated circles with linking number proportional to the chromosome length.
    Topoisomerase II must reduce this linking number to zero before the cell can divide.
    This is literally a problem in applied knot theory!
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part X: Summary and Reference

    ### Key Concepts

    **Knots and Diagrams:**
    - A knot = closed curve in $\mathbb{R}^3$ with no self-intersections
    - A knot diagram = planar projection with over/under crossing information
    - **Vertex (crossing)** = point where two strands meet in a diagram; each has a sign ±1
    - **Writhe** = sum of all crossing signs (not an invariant, changes under Move I)
    - **Arc** = strand between two consecutive undercrossings

    **Equivalence:**
    - Two knots are equivalent if one can be continuously deformed into the other
    - **Reidemeister's Theorem**: equivalence ⟺ sequence of three Reidemeister moves on diagrams
    - Move I: create/remove a loop (1 crossing)
    - Move II: push two strands together/apart (2 crossings)
    - Move III: slide a strand over a crossing (0 crossings changed)

    **Invariants:**
    - **Crossing number** $c(K)$: minimum crossings in any diagram
    - **Unknotting number** $u(K)$: minimum crossing changes to reach unknot
    - **Determinant** $\det(K) = |\Delta_K(-1)|$
    - **Tricolorability**: can arcs be 3-colored with the crossing rule?
    - **Alexander polynomial** $\Delta_K(t)$: first polynomial invariant (1928)
    - **Jones polynomial** $V_K(t)$: distinguishes mirror images (1984)

    **Applications:**
    - DNA topology and topoisomerase enzymes
    - Molecular knots in chemistry
    - Topological quantum computing
    - Statistical mechanics

    ### Knot Table: First Few Knots

    | Knot | $c(K)$ | $u(K)$ | $\det(K)$ | Tricolorable | Amphichiral? |
    |------|--------|--------|-----------|--------------|--------------|
    | $U$ | 0 | 0 | 1 | No | Yes |
    | $3_1$ | 3 | 1 | 3 | **Yes** | No |
    | $4_1$ | 4 | 1 | 5 | No | **Yes** |
    | $5_1$ | 5 | 2 | 5 | No | No |
    | $5_2$ | 5 | 1 | 7 | No | No |
    | $6_1$ | 6 | 1 | 9 | **Yes** | **Yes** |
    | $6_2$ | 6 | 1 | 11 | No | No |

    *Amphichiral* means the knot is equivalent to its mirror image.

    ### Further Reading

    **Books:**
    - Adams, *The Knot Book* — accessible introduction, highly recommended
    - Lickorish, *An Introduction to Knot Theory* — rigorous graduate text
    - Cromwell, *Knots and Links* — comprehensive modern treatment

    **Videos:**
    - [3Blue1Brown: The Trefoil Knot](https://www.youtube.com/watch?v=8DBhTXM_Br4)
    - [Numberphile: Knot Theory playlist](https://www.youtube.com/playlist?list=PLt5AfwLFPxWJeBgrNRBcohfEp8V5ALQJ1)

    **Interactive:**
    - [KnotInfo](https://www.indiana.edu/~knotinfo/) — comprehensive knot table with invariants
    - [KnotPlot](http://knotplot.com/) — 3D knot visualization software
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    *"Topology is precisely the mathematical discipline that allows the passage from local
    to global... Knot theory is the topology of curves, and it is one of the most
    beautiful and difficult branches of mathematics."*

    — Vladimir Arnold
    """)
    return


if __name__ == "__main__":
    app.run()
