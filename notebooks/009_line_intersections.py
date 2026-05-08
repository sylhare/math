"""
Line Intersections: Where Lines Meet, Vectors, and Vertices

A journey from the simplest geometric question — do two lines cross? — through
parametric representations, vector algebra, determinants, and the emergence of
the vertex as the mathematical atom of intersection.
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
        plot_directed_graph,
        style_subplot_axes,
    )

    return (
        COLORS,
        SCENE_THEME,
        base_layout,
        create_timeline,
        go,
        make_subplots,
        np,
        plot_directed_graph,
        style_subplot_axes,
    )


@app.cell
def _(mo):
    mo.md(r"""
    # Line Intersections: Where Lines Meet, Vectors, and Vertices

    *"There is no branch of mathematics, however abstract, which may not someday
    be applied to phenomena of the real world."*
    — Nikolai Lobachevsky

    ---

    ## The Oldest Question in Geometry

    Two straight lines are drawn on a plane. Do they cross? If so, where?

    This question is perhaps the most ancient in all of mathematics. It appears in
    Euclid's *Elements* (300 BCE), underlies every map grid, every architectural
    blueprint, every computer graphics pipeline. And yet the answer is richer
    than it first appears: it connects slope to determinants, direction to cross
    products, and a single crossing point to the algebraic concept of a **vertex**.

    **What you'll learn:**
    - Three ways to represent a line (slope-intercept, general, parametric)
    - How to find the intersection of two lines algebraically
    - Why the determinant is the right tool — and what it means geometrically
    - Vectors as the natural language for lines in any dimension
    - What happens in 3D: skew lines, the minimum-distance problem
    - The vertex: the intersection point as a graph-theoretic and topological object
    - How this all connects back to crossings in knot diagrams
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part I: A Brief History

    ### Euclid's Parallel Postulate (300 BCE)

    Euclid's fifth postulate — the **parallel postulate** — is the statement that
    gave geometers trouble for two millennia:

    > *If a line segment intersects two straight lines forming two interior angles
    > on the same side that are less than two right angles, then the two lines,
    > if extended indefinitely, meet on that side.*

    In modern terms: two non-parallel lines in a plane **always** intersect.
    The struggle to prove this from the other four postulates eventually led
    Gauss, Bolyai, and Lobachevsky to invent **non-Euclidean geometry** (1830s),
    where the postulate is simply false.

    ### Descartes and the Coordinate Revolution (1637)

    **René Descartes** gave us coordinates in his *La Géométrie* (1637). The key
    insight: every point in the plane corresponds to a pair of numbers $(x, y)$,
    and every line corresponds to an equation $ax + by = c$.

    This transformed geometry into algebra. Finding an intersection became
    **solving a system of two equations in two unknowns** — something Descartes
    could do symbolically.

    ### Vectors Arrive (19th century)

    **Hamilton** (1843) and **Grassmann** (1844) developed the algebra of vectors
    independently. Vectors gave a cleaner language for lines: instead of an equation,
    a line is a **point plus a direction**.

    This vector view generalizes effortlessly to any number of dimensions —
    something that slope-intercept form cannot do.
    """)
    return


@app.cell
def _(create_timeline):
    create_timeline(
        [
            (-300, "Euclid\nParallel postulate", 1),
            (1637, "Descartes\nCoordinates", -1),
            (1750, "Cramer\nCramer's rule", 1),
            (1843, "Hamilton\nVectors (quaternions)", -1),
            (1844, "Grassmann\nExterior algebra", 1),
            (1990, "Computational\ngeometry matures", -1),
        ],
        title="History of Line Intersection Mathematics",
        x_range=(-500, 2100),
        height=300,
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part II: Three Ways to Write a Line

    A line is a one-dimensional object embedded in the plane. There are three
    standard algebraic representations, each suited to different tasks.

    ### 1. Slope-Intercept Form

    $$y = mx + b$$

    Here $m$ is the **slope** (rise over run) and $b$ is the **y-intercept**
    (where the line crosses the vertical axis).

    **Advantages**: intuitive, easy to graph.
    **Disadvantages**: cannot represent vertical lines ($x = c$); awkward for
    intersections; does not generalize to 3D.

    ### 2. General (Implicit) Form

    $$ax + by = c \quad\text{(or equivalently } ax + by + d = 0\text{)}$$

    Here $(a, b)$ is the **normal vector** to the line — a vector perpendicular
    to the line's direction.

    **Advantages**: handles vertical lines; symmetric treatment of $x$ and $y$;
    natural for determinant-based intersection.
    **Disadvantages**: less geometrically intuitive.

    ### 3. Parametric Form

    $$\mathbf{r}(t) = \mathbf{p} + t\,\mathbf{d} = \begin{pmatrix} p_x \\ p_y \end{pmatrix} + t \begin{pmatrix} d_x \\ d_y \end{pmatrix}$$

    Here $\mathbf{p}$ is any **point on the line** and $\mathbf{d}$ is the
    **direction vector**. The parameter $t \in \mathbb{R}$ sweeps out all points.

    **Advantages**: generalizes directly to 3D and higher; natural for "travel
    along a line"; handles all orientations equally.
    **Disadvantages**: the representation is not unique ($\mathbf{p}$ and $\mathbf{d}$
    can both be scaled or shifted).

    ### Converting Between Forms

    | From | To | Method |
    |------|----|--------|
    | Slope-intercept $y = mx + b$ | General | $-mx + y = b$, so $a = -m$, $b_\text{coef} = 1$, $c = b$ |
    | General $ax + by = c$ | Parametric | Point: $(c/a, 0)$; Direction: $(b, -a)$ |
    | Parametric $\mathbf{p} + t\mathbf{d}$ | General | Normal $\mathbf{n} = (-d_y, d_x)$; then $\mathbf{n} \cdot \mathbf{r} = \mathbf{n} \cdot \mathbf{p}$ |

    The direction vector $\mathbf{d} = (d_x, d_y)$ and the normal vector
    $\mathbf{n} = (-d_y, d_x)$ are always **perpendicular**: $\mathbf{d} \cdot \mathbf{n} = 0$.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Interactive: Three Representations of the Same Line
    """)
    return


@app.cell
def _(mo):
    line_slope = mo.ui.slider(start=-3.0, stop=3.0, step=0.1, value=1.0, label="Slope m", show_value=True)
    line_intercept = mo.ui.slider(start=-4.0, stop=4.0, step=0.5, value=1.0, label="y-intercept b", show_value=True)
    return line_intercept, line_slope


@app.cell
def _(line_intercept, line_slope, mo):
    mo.hstack([line_slope, line_intercept], justify="start", gap=2)
    return


@app.cell
def _(COLORS, base_layout, go, line_intercept, line_slope, np):
    _m = line_slope.value
    _b = line_intercept.value

    _x = np.linspace(-6, 6, 300)
    _y = _m * _x + _b

    # Direction vector and normal
    _d = np.array([1, _m]) / np.sqrt(1 + _m**2)
    _n = np.array([-_m, 1]) / np.sqrt(1 + _m**2)

    _fig = go.Figure()

    # The line
    _fig.add_trace(
        go.Scatter(
            x=_x,
            y=_y,
            mode="lines",
            line={"color": COLORS["primary"], "width": 3},
            name=f"y = {_m:.1f}x + {_b:.1f}",
        )
    )

    # y-intercept point
    _fig.add_trace(
        go.Scatter(
            x=[0],
            y=[_b],
            mode="markers+text",
            marker={"color": COLORS["quaternary"], "size": 12},
            text=[f"(0, {_b:.1f})"],
            textposition="middle right",
            textfont={"color": COLORS["quaternary"], "size": 11},
            name="y-intercept",
        )
    )

    # Direction vector (from origin)
    _scale = 1.5
    _fig.add_trace(
        go.Scatter(
            x=[0, _scale * _d[0]],
            y=[_b, _b + _scale * _d[1]],
            mode="lines+markers",
            line={"color": COLORS["secondary"], "width": 3},
            marker={"symbol": "arrow", "size": 12, "angleref": "previous", "color": COLORS["secondary"]},
            name=f"d = ({_d[0]:.2f}, {_d[1]:.2f})",
        )
    )

    # Normal vector
    _fig.add_trace(
        go.Scatter(
            x=[0, _scale * _n[0]],
            y=[_b, _b + _scale * _n[1]],
            mode="lines+markers",
            line={"color": COLORS["tertiary"], "width": 3},
            marker={"symbol": "arrow", "size": 12, "angleref": "previous", "color": COLORS["tertiary"]},
            name=f"n = ({_n[0]:.2f}, {_n[1]:.2f})",
        )
    )

    # Axes
    _fig.add_hline(y=0, line_color=COLORS["text_secondary"], line_width=1)
    _fig.add_vline(x=0, line_color=COLORS["text_secondary"], line_width=1)

    # General form text
    _a_coef = -_m
    _b_coef = 1.0
    _c_coef = _b
    _general = f"{_a_coef:.1f}x + {_b_coef:.1f}y = {_c_coef:.1f}"

    _fig.update_layout(
        **base_layout(
            title=f"Slope-intercept: y = {_m:.1f}x + {_b:.1f}  |  General: {_general}  |  Parametric: (0,{_b:.1f}) + t·({_d[0]:.2f},{_d[1]:.2f})",
            xaxis={
                "gridcolor": COLORS["grid"],
                "zerolinecolor": COLORS["text_secondary"],
                "range": [-6, 6],
                "title": "x",
            },
            yaxis={
                "gridcolor": COLORS["grid"],
                "zerolinecolor": COLORS["text_secondary"],
                "range": [-6, 6],
                "title": "y",
                "scaleanchor": "x",
            },
            height=480,
        )
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    The **direction vector** (red arrow) points along the line — it has slope $m$.
    The **normal vector** (teal arrow) is perpendicular to the line — it points in
    the direction of fastest increase of the general form $ax + by$.

    Notice that $\mathbf{d} \cdot \mathbf{n} = 0$ always — they are orthogonal by construction.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part III: Finding the Intersection — Algebra

    ### Two Lines in Slope-Intercept Form

    Given:
    $$L_1: y = m_1 x + b_1 \qquad L_2: y = m_2 x + b_2$$

    At the intersection, both equations hold simultaneously:
    $$m_1 x + b_1 = m_2 x + b_2$$

    Rearranging:
    $$(m_1 - m_2)x = b_2 - b_1$$

    If $m_1 \neq m_2$ (lines are not parallel):
    $$\boxed{x^* = \frac{b_2 - b_1}{m_1 - m_2}, \qquad y^* = m_1 x^* + b_1}$$

    ### Two Lines in General Form — Enter the Determinant

    Given:
    $$L_1: a_1 x + b_1 y = c_1 \qquad L_2: a_2 x + b_2 y = c_2$$

    This is a **system of two linear equations**. Write it as a matrix equation:

    $$\begin{pmatrix} a_1 & b_1 \\ a_2 & b_2 \end{pmatrix} \begin{pmatrix} x \\ y \end{pmatrix} = \begin{pmatrix} c_1 \\ c_2 \end{pmatrix}$$

    The solution exists (and is unique) when the matrix is invertible — i.e., when its
    **determinant** is non-zero:

    $$D = \det\begin{pmatrix} a_1 & b_1 \\ a_2 & b_2 \end{pmatrix} = a_1 b_2 - a_2 b_1 \neq 0$$

    By **Cramer's Rule**:

    $$\boxed{x^* = \frac{\det\begin{pmatrix} c_1 & b_1 \\ c_2 & b_2 \end{pmatrix}}{D} = \frac{c_1 b_2 - c_2 b_1}{D}, \qquad y^* = \frac{\det\begin{pmatrix} a_1 & c_1 \\ a_2 & c_2 \end{pmatrix}}{D} = \frac{a_1 c_2 - a_2 c_1}{D}}$$

    ### The Three Cases

    | Determinant $D$ | Geometry | Algebraic meaning |
    |-----------------|----------|-------------------|
    | $D \neq 0$ | Lines intersect at exactly one point | System has unique solution |
    | $D = 0$, $c_1 b_2 \neq c_2 b_1$ | Lines are parallel (no intersection) | System is inconsistent |
    | $D = 0$, $c_1 b_2 = c_2 b_1$ | Lines are coincident (same line) | System has infinitely many solutions |

    The determinant $D = a_1 b_2 - a_2 b_1$ is the **area of the parallelogram** formed
    by the normal vectors $(a_1, b_1)$ and $(a_2, b_2)$. When $D = 0$, the normals are
    parallel — which means the lines are parallel (or the same).
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### The Simplest Implementation

    Converting any line $y = mx + b$ to general form ($a = -m$, $b_\text{coef} = 1$, $c = b$)
    and applying the determinant check gives a function that handles every case — including
    vertical lines — with no special-casing:

    ```python
    def intersect_2d(a1, b1, c1, a2, b2, c2):
        # Lines: a1*x + b1*y = c1  and  a2*x + b2*y = c2
        D = a1*b2 - a2*b1
        if D == 0:
            return None          # parallel or coincident
        x = (c1*b2 - c2*b1) / D
        y = (a1*c2 - a2*c1) / D
        return x, y
    ```

    Three cases, two multiplications to check, two more to solve.
    Vertical line $x = k$ is simply $a=1, b=0, c=k$ — no special case needed.
    """)
    return


@app.cell
def _(COLORS, base_layout, go, make_subplots, np, style_subplot_axes):
    _fig = make_subplots(
        rows=1,
        cols=3,
        subplot_titles=[
            "D ≠ 0  →  Intersecting",
            "D = 0  →  Parallel",
            "D = 0  →  Coincident",
        ],
        horizontal_spacing=0.08,
    )

    _x = np.linspace(-3, 3, 100)

    # Case 1: Intersecting  (L1: y = x, L2: y = -x + 1)
    _fig.add_trace(
        go.Scatter(
            x=_x, y=_x, mode="lines", line={"color": COLORS["primary"], "width": 3}, name="L₁", showlegend=False
        ),
        row=1,
        col=1,
    )
    _fig.add_trace(
        go.Scatter(
            x=_x, y=-_x + 1, mode="lines", line={"color": COLORS["secondary"], "width": 3}, name="L₂", showlegend=False
        ),
        row=1,
        col=1,
    )
    _fig.add_trace(
        go.Scatter(
            x=[0.5],
            y=[0.5],
            mode="markers",
            marker={"color": COLORS["quaternary"], "size": 14},
            name="vertex",
            showlegend=False,
        ),
        row=1,
        col=1,
    )
    _fig.add_annotation(
        x=0.5,
        y=-2.5,
        text="D = (−1)(1) − (1)(1) = −2",
        font={"color": COLORS["quaternary"], "size": 11},
        showarrow=False,
        xref="x1",
        yref="y1",
    )

    # Case 2: Parallel  (L1: y = x, L2: y = x + 2)
    _fig.add_trace(
        go.Scatter(x=_x, y=_x, mode="lines", line={"color": COLORS["primary"], "width": 3}, showlegend=False),
        row=1,
        col=2,
    )
    _fig.add_trace(
        go.Scatter(x=_x, y=_x + 2, mode="lines", line={"color": COLORS["secondary"], "width": 3}, showlegend=False),
        row=1,
        col=2,
    )
    _fig.add_annotation(
        x=0,
        y=-2.5,
        text="D = (−1)(1) − (−1)(1) = 0",
        font={"color": COLORS["secondary"], "size": 11},
        showarrow=False,
        xref="x2",
        yref="y2",
    )

    # Case 3: Coincident  (same line drawn twice, slightly offset for visibility)
    _fig.add_trace(
        go.Scatter(x=_x, y=_x, mode="lines", line={"color": COLORS["primary"], "width": 6}, showlegend=False),
        row=1,
        col=3,
    )
    _fig.add_trace(
        go.Scatter(
            x=_x, y=_x, mode="lines", line={"color": COLORS["secondary"], "width": 2, "dash": "dash"}, showlegend=False
        ),
        row=1,
        col=3,
    )
    _fig.add_annotation(
        x=0,
        y=-2.5,
        text="D = 0  and  c₁b₂ = c₂b₁",
        font={"color": COLORS["tertiary"], "size": 11},
        showarrow=False,
        xref="x3",
        yref="y3",
    )

    _fig.update_layout(
        **base_layout(title="The Three Cases — All Detected by the Determinant D = a₁b₂ − a₂b₁", height=350)
    )
    style_subplot_axes(_fig)
    for _c in range(1, 4):
        _fig.update_xaxes(range=[-3, 3], zerolinecolor=COLORS["text_secondary"], row=1, col=_c)
        _fig.update_yaxes(range=[-3, 3], scaleanchor=f"x{_c}", row=1, col=_c)
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Interactive Line Intersection
    """)
    return


@app.cell
def _(mo):
    l1_slope = mo.ui.slider(start=-4.0, stop=4.0, step=0.25, value=1.0, label="L₁ slope m₁", show_value=True)
    l1_intercept = mo.ui.slider(start=-4.0, stop=4.0, step=0.5, value=-1.0, label="L₁ intercept b₁", show_value=True)
    l2_slope = mo.ui.slider(start=-4.0, stop=4.0, step=0.25, value=-0.5, label="L₂ slope m₂", show_value=True)
    l2_intercept = mo.ui.slider(start=-4.0, stop=4.0, step=0.5, value=2.0, label="L₂ intercept b₂", show_value=True)
    return l1_intercept, l1_slope, l2_intercept, l2_slope


@app.cell
def _(l1_intercept, l1_slope, l2_intercept, l2_slope, mo):
    mo.vstack(
        [
            mo.hstack([l1_slope, l1_intercept], justify="start", gap=2),
            mo.hstack([l2_slope, l2_intercept], justify="start", gap=2),
        ]
    )
    return


@app.cell
def _(COLORS, base_layout, go, l1_intercept, l1_slope, l2_intercept, l2_slope, np):
    _m1, _b1 = l1_slope.value, l1_intercept.value
    _m2, _b2 = l2_slope.value, l2_intercept.value

    _x = np.linspace(-7, 7, 400)

    _fig = go.Figure()

    _fig.add_trace(
        go.Scatter(
            x=_x,
            y=_m1 * _x + _b1,
            mode="lines",
            line={"color": COLORS["primary"], "width": 3},
            name=f"L₁: y = {_m1:.2f}x + {_b1:.1f}",
        )
    )
    _fig.add_trace(
        go.Scatter(
            x=_x,
            y=_m2 * _x + _b2,
            mode="lines",
            line={"color": COLORS["secondary"], "width": 3},
            name=f"L₂: y = {_m2:.2f}x + {_b2:.1f}",
        )
    )

    _tol = 1e-9
    _denom = _m1 - _m2

    if abs(_denom) < _tol:
        if abs(_b1 - _b2) < _tol:
            _status = "COINCIDENT — infinitely many intersections"
            _status_color = COLORS["quaternary"]
        else:
            _status = "PARALLEL — no intersection"
            _status_color = COLORS["secondary"]
    else:
        _xi = (_b2 - _b1) / _denom
        _yi = _m1 * _xi + _b1
        _fig.add_trace(
            go.Scatter(
                x=[_xi],
                y=[_yi],
                mode="markers+text",
                marker={"color": COLORS["quaternary"], "size": 14},
                text=[f"  ({_xi:.2f}, {_yi:.2f})"],
                textposition="middle right",
                textfont={"color": COLORS["quaternary"], "size": 12},
                name="Intersection",
            )
        )
        _D = (-_m1) * 1 - (-_m2) * 1  # det of [[−m1, 1],[−m2, 1]]
        _status = f"Intersection: ({_xi:.2f}, {_yi:.2f})  |  det D = {_D:.2f}"
        _status_color = COLORS["tertiary"]

    _fig.add_hline(y=0, line_color=COLORS["text_secondary"], line_width=1)
    _fig.add_vline(x=0, line_color=COLORS["text_secondary"], line_width=1)

    _fig.update_layout(
        **base_layout(
            title=_status,
            title_font={"color": _status_color},
            xaxis={
                "gridcolor": COLORS["grid"],
                "zerolinecolor": COLORS["text_secondary"],
                "range": [-7, 7],
                "title": "x",
            },
            yaxis={
                "gridcolor": COLORS["grid"],
                "zerolinecolor": COLORS["text_secondary"],
                "range": [-7, 7],
                "title": "y",
                "scaleanchor": "x",
            },
            height=500,
        )
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    Try setting $m_1 = m_2$ (same slope): the lines become parallel and the title
    changes to "PARALLEL". The determinant $D = m_2 - m_1$ becomes zero.

    **Geometric intuition for the determinant**: The two lines have normal vectors
    $\mathbf{n}_1 = (-m_1, 1)$ and $\mathbf{n}_2 = (-m_2, 1)$.
    The determinant $D = (-m_1)(1) - (-m_2)(1) = m_2 - m_1$ is the area of the
    parallelogram they span. Zero area means the normals point in the same direction
    — the lines are parallel.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part IV: The Determinant — Geometry Behind the Formula

    ### Why the $2 \times 2$ Determinant is an Area

    The **determinant** of a $2 \times 2$ matrix is:

    $$\det\begin{pmatrix} a & b \\ c & d \end{pmatrix} = ad - bc$$

    Geometrically, if we think of the rows as vectors $\mathbf{u} = (a, b)$ and
    $\mathbf{v} = (c, d)$, then $|\det| = $ **area of the parallelogram** with
    sides $\mathbf{u}$ and $\mathbf{v}$.

    The **sign** tells us orientation:
    - Positive: $\mathbf{v}$ is to the left of $\mathbf{u}$ (counterclockwise)
    - Negative: $\mathbf{v}$ is to the right of $\mathbf{u}$ (clockwise)
    - Zero: $\mathbf{u}$ and $\mathbf{v}$ are parallel (parallelogram has zero area)

    $$\det\begin{pmatrix} a_1 & b_1 \\ a_2 & b_2 \end{pmatrix} = 0 \iff \text{the two rows are parallel} \iff \text{the two lines are parallel}$$

    ### Cramer's Rule, Visualized

    When solving $A\mathbf{x} = \mathbf{c}$, Cramer's rule replaces each column of $A$
    with $\mathbf{c}$ and divides by $\det(A)$:

    $$x^* = \frac{\det\begin{pmatrix} c_1 & b_1 \\ c_2 & b_2 \end{pmatrix}}{\det\begin{pmatrix} a_1 & b_1 \\ a_2 & b_2 \end{pmatrix}}$$

    This is a ratio of areas. The numerator is the area of the parallelogram formed
    by the right-hand side and the second column; the denominator is the area formed
    by both columns of $A$. The ratio is invariant under shearing — a deep geometric fact.
    """)
    return


@app.cell
def _(COLORS, base_layout, go, np):
    _u = np.array([3.0, 1.0])
    _v = np.array([1.0, 2.5])
    _det = _u[0] * _v[1] - _u[1] * _v[0]

    _fig = go.Figure()

    # Parallelogram
    _corners_x = [0, _u[0], _u[0] + _v[0], _v[0], 0]
    _corners_y = [0, _u[1], _u[1] + _v[1], _v[1], 0]
    _fig.add_trace(
        go.Scatter(
            x=_corners_x,
            y=_corners_y,
            mode="lines",
            fill="toself",
            fillcolor="rgba(0, 212, 255, 0.2)",
            line={"color": COLORS["primary"], "width": 2},
            name=f"Area = |det| = {abs(_det):.2f}",
            hoverinfo="skip",
        )
    )

    # Vector u
    _fig.add_trace(
        go.Scatter(
            x=[0, _u[0]],
            y=[0, _u[1]],
            mode="lines+markers",
            line={"color": COLORS["secondary"], "width": 4},
            marker={"symbol": "arrow", "size": 14, "angleref": "previous", "color": COLORS["secondary"]},
            name=f"u = ({_u[0]:.0f}, {_u[1]:.0f})",
        )
    )

    # Vector v
    _fig.add_trace(
        go.Scatter(
            x=[0, _v[0]],
            y=[0, _v[1]],
            mode="lines+markers",
            line={"color": COLORS["tertiary"], "width": 4},
            marker={"symbol": "arrow", "size": 14, "angleref": "previous", "color": COLORS["tertiary"]},
            name=f"v = ({_v[0]:.0f}, {_v[1]:.0f})",
        )
    )

    # Area label
    _cx = (_u[0] + _v[0]) / 2
    _cy = (_u[1] + _v[1]) / 2
    _fig.add_annotation(
        x=_cx,
        y=_cy,
        text=f"Area = {abs(_det):.2f}",
        font={"color": COLORS["quaternary"], "size": 14},
        showarrow=False,
    )

    _fig.add_annotation(
        x=2.5,
        y=-0.5,
        text=f"det = ({_u[0]:.0f})({_v[1]:.0f}) − ({_u[1]:.0f})({_v[0]:.0f}) = {_det:.2f}",
        font={"color": COLORS["quaternary"], "size": 13},
        showarrow=False,
    )

    _fig.add_hline(y=0, line_color=COLORS["text_secondary"], line_width=1)
    _fig.add_vline(x=0, line_color=COLORS["text_secondary"], line_width=1)

    _fig.update_layout(
        **base_layout(
            title="The Determinant as a Parallelogram Area",
            xaxis={
                "gridcolor": COLORS["grid"],
                "zerolinecolor": COLORS["text_secondary"],
                "range": [-0.5, 5.5],
                "title": "x",
                "scaleanchor": "y",
            },
            yaxis={
                "gridcolor": COLORS["grid"],
                "zerolinecolor": COLORS["text_secondary"],
                "range": [-1, 5],
                "title": "y",
            },
            height=420,
        )
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    The determinant equals the **signed area** of the parallelogram. This is the
    core geometric fact that makes linear algebra work: the determinant measures
    how much a linear transformation scales areas.

    For line intersection: when $D = 0$, the two normal vectors are collinear —
    they span a flat (zero-area) parallelogram — and the lines are parallel.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part V: Vectors — The Natural Language of Lines

    ### Points vs. Vectors

    A **point** $P = (x, y)$ specifies a location.

    A **vector** $\mathbf{v} = (v_x, v_y)$ specifies a displacement — a direction
    and a magnitude. Vectors can be added, scaled, and multiplied; points cannot.

    A line is most naturally described as:
    $$\mathbf{r}(t) = \mathbf{p} + t\,\mathbf{d}$$

    where $\mathbf{p}$ is a **position vector** (a fixed point on the line, viewed
    as a vector from the origin) and $\mathbf{d}$ is a **direction vector**.

    ### The Dot Product and Angles

    The **dot product** of two vectors $\mathbf{u} = (u_x, u_y)$ and $\mathbf{v} = (v_x, v_y)$:

    $$\mathbf{u} \cdot \mathbf{v} = u_x v_x + u_y v_y = |\mathbf{u}||\mathbf{v}|\cos\theta$$

    where $\theta$ is the angle between them. Key facts:
    - $\mathbf{u} \cdot \mathbf{v} = 0 \iff \mathbf{u} \perp \mathbf{v}$ (perpendicular)
    - $\mathbf{u} \cdot \mathbf{v} = |\mathbf{u}||\mathbf{v}| \iff \mathbf{u} \parallel \mathbf{v}$ (parallel, same direction)

    **The normal form of a line**: a line through point $\mathbf{p}$ with normal $\mathbf{n}$
    is the set of all points $\mathbf{r}$ satisfying:
    $$\mathbf{n} \cdot (\mathbf{r} - \mathbf{p}) = 0$$

    Expanding: $\mathbf{n} \cdot \mathbf{r} = \mathbf{n} \cdot \mathbf{p}$, which is $ax + by = c$ in general form.

    ### Finding Intersection via Parametric Equations

    Given two lines:
    $$L_1: \mathbf{r} = \mathbf{p}_1 + t\,\mathbf{d}_1 \qquad L_2: \mathbf{r} = \mathbf{p}_2 + s\,\mathbf{d}_2$$

    At the intersection, the position vectors are equal:
    $$\mathbf{p}_1 + t\,\mathbf{d}_1 = \mathbf{p}_2 + s\,\mathbf{d}_2$$

    This gives two scalar equations (one for each coordinate):
    $$p_{1x} + t\,d_{1x} = p_{2x} + s\,d_{2x}$$
    $$p_{1y} + t\,d_{1y} = p_{2y} + s\,d_{2y}$$

    Solving for $t$ and $s$ gives the parameter values at the intersection.
    The intersection point is $\mathbf{r}^* = \mathbf{p}_1 + t^*\mathbf{d}_1$.

    The parameters $t^*$ and $s^*$ also tell us **where on each line** the
    intersection occurs: $t^* = 0.5$ means "halfway between $\mathbf{p}_1$ and
    $\mathbf{p}_1 + \mathbf{d}_1$."
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Interactive: Parametric Intersection
    """)
    return


@app.cell
def _(mo):
    p1x = mo.ui.slider(start=-4.0, stop=4.0, step=0.5, value=-3.0, label="p₁ x", show_value=True)
    p1y = mo.ui.slider(start=-4.0, stop=4.0, step=0.5, value=-1.0, label="p₁ y", show_value=True)
    d1x = mo.ui.slider(start=-3.0, stop=3.0, step=0.25, value=2.0, label="d₁ x", show_value=True)
    d1y = mo.ui.slider(start=-3.0, stop=3.0, step=0.25, value=1.0, label="d₁ y", show_value=True)
    p2x = mo.ui.slider(start=-4.0, stop=4.0, step=0.5, value=-2.0, label="p₂ x", show_value=True)
    p2y = mo.ui.slider(start=-4.0, stop=4.0, step=0.5, value=3.0, label="p₂ y", show_value=True)
    d2x = mo.ui.slider(start=-3.0, stop=3.0, step=0.25, value=1.0, label="d₂ x", show_value=True)
    d2y = mo.ui.slider(start=-3.0, stop=3.0, step=0.25, value=-2.0, label="d₂ y", show_value=True)
    return d1x, d1y, d2x, d2y, p1x, p1y, p2x, p2y


@app.cell
def _(d1x, d1y, d2x, d2y, mo, p1x, p1y, p2x, p2y):
    mo.vstack(
        [
            mo.md("**Line 1** (blue): r = p₁ + t·d₁"),
            mo.hstack([p1x, p1y, d1x, d1y], justify="start", gap=2),
            mo.md("**Line 2** (red): r = p₂ + s·d₂"),
            mo.hstack([p2x, p2y, d2x, d2y], justify="start", gap=2),
        ]
    )
    return


@app.cell
def _(COLORS, base_layout, d1x, d1y, d2x, d2y, go, np, p1x, p1y, p2x, p2y):
    _p1 = np.array([p1x.value, p1y.value])
    _d1 = np.array([d1x.value, d1y.value])
    _p2 = np.array([p2x.value, p2y.value])
    _d2 = np.array([d2x.value, d2y.value])

    _t_range = np.linspace(-4, 4, 200)
    _L1 = _p1[:, None] + np.outer(_d1, _t_range)
    _L2 = _p2[:, None] + np.outer(_d2, _t_range)

    _fig = go.Figure()

    # Lines
    _fig.add_trace(
        go.Scatter(
            x=_L1[0],
            y=_L1[1],
            mode="lines",
            line={"color": COLORS["primary"], "width": 3},
            name=f"L₁: ({_p1[0]:.1f},{_p1[1]:.1f}) + t·({_d1[0]:.2f},{_d1[1]:.2f})",
        )
    )
    _fig.add_trace(
        go.Scatter(
            x=_L2[0],
            y=_L2[1],
            mode="lines",
            line={"color": COLORS["secondary"], "width": 3},
            name=f"L₂: ({_p2[0]:.1f},{_p2[1]:.1f}) + s·({_d2[0]:.2f},{_d2[1]:.2f})",
        )
    )

    # Base points
    _fig.add_trace(
        go.Scatter(
            x=[_p1[0]],
            y=[_p1[1]],
            mode="markers",
            marker={"color": COLORS["primary"], "size": 10, "symbol": "square"},
            name="p₁",
            showlegend=True,
        )
    )
    _fig.add_trace(
        go.Scatter(
            x=[_p2[0]],
            y=[_p2[1]],
            mode="markers",
            marker={"color": COLORS["secondary"], "size": 10, "symbol": "square"},
            name="p₂",
            showlegend=True,
        )
    )

    # Solve for intersection: p1 + t*d1 = p2 + s*d2
    # [d1 | -d2] [t; s] = p2 - p1
    _A = np.array([[_d1[0], -_d2[0]], [_d1[1], -_d2[1]]])
    _b_vec = _p2 - _p1
    _D = _A[0, 0] * _A[1, 1] - _A[0, 1] * _A[1, 0]

    _tol = 1e-9
    if abs(_D) < _tol:
        _title = "PARALLEL lines — no intersection (D = 0)"
        _title_color = COLORS["secondary"]
    else:
        _t_star = (_b_vec[0] * _A[1, 1] - _b_vec[1] * _A[0, 1]) / _D
        _s_star = (_A[0, 0] * _b_vec[1] - _A[1, 0] * _b_vec[0]) / _D
        _inter = _p1 + _t_star * _d1

        _fig.add_trace(
            go.Scatter(
                x=[_inter[0]],
                y=[_inter[1]],
                mode="markers+text",
                marker={"color": COLORS["quaternary"], "size": 16},
                text=[f"  ({_inter[0]:.2f}, {_inter[1]:.2f})"],
                textposition="middle right",
                textfont={"color": COLORS["quaternary"], "size": 12},
                name=f"Vertex (t={_t_star:.2f}, s={_s_star:.2f})",
            )
        )
        _title = f"Intersection: ({_inter[0]:.2f}, {_inter[1]:.2f})  |  t = {_t_star:.2f}, s = {_s_star:.2f}  |  D = {_D:.2f}"
        _title_color = COLORS["tertiary"]

    _fig.add_hline(y=0, line_color=COLORS["text_secondary"], line_width=1)
    _fig.add_vline(x=0, line_color=COLORS["text_secondary"], line_width=1)

    _fig.update_layout(
        **base_layout(
            title=_title,
            title_font={"color": _title_color},
            xaxis={
                "gridcolor": COLORS["grid"],
                "zerolinecolor": COLORS["text_secondary"],
                "range": [-7, 7],
                "title": "x",
                "scaleanchor": "y",
            },
            yaxis={
                "gridcolor": COLORS["grid"],
                "zerolinecolor": COLORS["text_secondary"],
                "range": [-7, 7],
                "title": "y",
            },
            height=500,
        )
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    The square markers show the **base points** $\mathbf{p}_1$ and $\mathbf{p}_2$.
    The yellow dot is the intersection — the **vertex** where both lines meet.

    The parameters $t^*$ and $s^*$ in the title tell you where on each line
    the crossing occurs. For instance, $t^* = 1.5$ means the intersection is
    1.5 direction-lengths past $\mathbf{p}_1$ along $\mathbf{d}_1$.

    The system $[\mathbf{d}_1 \;|\; {-\mathbf{d}_2}]\begin{pmatrix}t\\s\end{pmatrix} = \mathbf{p}_2 - \mathbf{p}_1$
    has determinant $D = d_{1x}(-d_{2y}) - d_{1y}(-d_{2x}) = d_{2x}d_{1y} - d_{1x}d_{2y}$,
    which is $\mathbf{d}_2 \times \mathbf{d}_1$ (the negative of $\mathbf{d}_1 \times \mathbf{d}_2$).
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part VI: The Cross Product and Orientation

    ### 2D Cross Product (Scalar)

    In 2D, the "cross product" of $\mathbf{u} = (u_x, u_y)$ and $\mathbf{v} = (v_x, v_y)$
    is defined as the scalar:

    $$\mathbf{u} \times \mathbf{v} = u_x v_y - u_y v_x = \det\begin{pmatrix} u_x & u_y \\ v_x & v_y \end{pmatrix}$$

    This is exactly the signed area of the parallelogram with sides $\mathbf{u}$ and $\mathbf{v}$.

    **Key uses for intersection:**
    - $\mathbf{d}_1 \times \mathbf{d}_2 = 0 \iff$ lines are parallel
    - The **sign** of $(\mathbf{p}_2 - \mathbf{p}_1) \times \mathbf{d}_1$ tells you which
      side of $L_1$ the point $\mathbf{p}_2$ lies on

    ### 3D Cross Product (Vector)

    In 3D, the cross product of $\mathbf{u} = (u_x, u_y, u_z)$ and $\mathbf{v} = (v_x, v_y, v_z)$
    is a **vector** perpendicular to both:

    $$\mathbf{u} \times \mathbf{v} = \begin{pmatrix} u_y v_z - u_z v_y \\ u_z v_x - u_x v_z \\ u_x v_y - u_y v_x \end{pmatrix}$$

    The magnitude $|\mathbf{u} \times \mathbf{v}| = |\mathbf{u}||\mathbf{v}|\sin\theta$ is
    the area of the parallelogram, and the direction follows the **right-hand rule**.

    ### Orientation of Three Points

    The cross product lets us determine if three points $A$, $B$, $C$ turn
    **left** (counterclockwise) or **right** (clockwise):

    $$\text{orientation}(A, B, C) = \text{sign}\big((\mathbf{B} - \mathbf{A}) \times (\mathbf{C} - \mathbf{A})\big)$$

    - Positive: left turn (counterclockwise)
    - Negative: right turn (clockwise)
    - Zero: $A$, $B$, $C$ are collinear

    This orientation test is the basis of computational geometry algorithms
    (convex hull, Delaunay triangulation, line segment intersection).
    """)
    return


@app.cell
def _(COLORS, base_layout, go, make_subplots, np, style_subplot_axes):
    _A = np.array([0.0, 0.0])
    _B = np.array([3.0, 1.0])
    _C_ccw = np.array([2.0, 3.0])
    _C_cw = np.array([2.0, -1.5])

    _fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=["Left Turn (CCW, cross > 0)", "Right Turn (CW, cross < 0)"],
    )

    for _col, (_C, _clr) in enumerate([(_C_ccw, COLORS["tertiary"]), (_C_cw, COLORS["secondary"])], 1):
        _cross = (_B[0] - _A[0]) * (_C[1] - _A[1]) - (_B[1] - _A[1]) * (_C[0] - _A[0])

        _fig.add_trace(
            go.Scatter(
                x=[_A[0], _B[0], _C[0], _A[0]],
                y=[_A[1], _B[1], _C[1], _A[1]],
                mode="lines+markers",
                fill="toself",
                fillcolor=f"rgba({int(_clr[1:3], 16)},{int(_clr[3:5], 16)},{int(_clr[5:7], 16)},0.25)",
                line={"color": _clr, "width": 2},
                marker={"size": 10, "color": _clr},
                showlegend=False,
            ),
            row=1,
            col=_col,
        )

        for _pt, _lbl, _off in [(_A, "A", (-0.2, -0.2)), (_B, "B", (0.1, -0.2)), (_C, "C", (0.1, 0.1))]:
            _fig.add_annotation(
                x=_pt[0] + _off[0],
                y=_pt[1] + _off[1],
                text=f"<b>{_lbl}</b>",
                font={"color": COLORS["quaternary"], "size": 14},
                showarrow=False,
                xref=f"x{_col}",
                yref=f"y{_col}",
            )

        _fig.add_annotation(
            x=1.5,
            y=-0.5,
            text=f"cross = {_cross:.1f}",
            font={"color": _clr, "size": 13},
            showarrow=False,
            xref=f"x{_col}",
            yref=f"y{_col}",
        )

    _fig.update_layout(**base_layout(title="Orientation: Sign of the Cross Product", height=380))
    style_subplot_axes(_fig)
    for _c in range(1, 3):
        _fig.update_xaxes(zerolinecolor=COLORS["text_secondary"], range=[-0.5, 4], row=1, col=_c)
        _fig.update_yaxes(zerolinecolor=COLORS["text_secondary"], range=[-2, 4], row=1, col=_c)

    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part VII: Lines in 3D — Skew Lines

    ### New Possibilities in 3D

    In the plane, two distinct lines either intersect or are parallel.
    In 3D, there is a third possibility: **skew lines** — lines that are
    neither parallel nor intersecting. They pass each other at a distance.

    Think of two roads on different levels of a highway interchange, going
    in different directions: they neither cross nor are they parallel.

    ### The Three Cases in 3D

    Given two lines:
    $$L_1: \mathbf{r} = \mathbf{p}_1 + t\,\mathbf{d}_1 \qquad L_2: \mathbf{r} = \mathbf{p}_2 + s\,\mathbf{d}_2$$

    **Test for parallelism**: $\mathbf{d}_1 \times \mathbf{d}_2 = \mathbf{0}$
    (direction vectors are proportional).

    **Test for intersection**: Solve $\mathbf{p}_1 + t\mathbf{d}_1 = \mathbf{p}_2 + s\mathbf{d}_2$.
    This is 3 equations in 2 unknowns — generically overdetermined. If a solution
    $(t^*, s^*)$ exists, the lines intersect.

    **Test for skewness**: Not parallel, and no solution exists. The minimum
    distance between skew lines is:

    $$d = \frac{|(\mathbf{p}_2 - \mathbf{p}_1) \cdot (\mathbf{d}_1 \times \mathbf{d}_2)|}{|\mathbf{d}_1 \times \mathbf{d}_2|}$$

    The cross product $\mathbf{d}_1 \times \mathbf{d}_2$ gives the direction of the
    **common perpendicular** — the shortest segment connecting the two lines.
    """)
    return


@app.cell
def _(mo):
    skew_t = mo.ui.slider(start=0.0, stop=1.0, step=0.05, value=0.5, label="Separation (skewness)", show_value=True)
    return (skew_t,)


@app.cell
def _(mo, skew_t):
    mo.hstack([mo.md("### 3D: Intersecting vs Skew Lines"), skew_t])
    return


@app.cell
def _(COLORS, SCENE_THEME, base_layout, go, np, skew_t):
    _sep = skew_t.value  # 0 = intersecting, 1 = fully skew

    _t_range = np.linspace(-2, 2, 100)

    # Line 1: along x-axis, in z=0 plane
    _p1 = np.array([0.0, 0.0, 0.0])
    _d1 = np.array([1.0, 0.0, 0.0])

    # Line 2: direction (0,1,0), displaced in z by sep, in x by sep
    _p2 = np.array([0.0, -2.0, _sep * 1.5])
    _d2 = np.array([0.0, 1.0, 0.0])

    _L1 = _p1[:, None] + np.outer(_d1, _t_range)
    _L2 = _p2[:, None] + np.outer(_d2, _t_range)

    _fig = go.Figure()

    _fig.add_trace(
        go.Scatter3d(
            x=_L1[0],
            y=_L1[1],
            z=_L1[2],
            mode="lines",
            line={"color": COLORS["primary"], "width": 6},
            name="Line 1",
        )
    )
    _fig.add_trace(
        go.Scatter3d(
            x=_L2[0],
            y=_L2[1],
            z=_L2[2],
            mode="lines",
            line={"color": COLORS["secondary"], "width": 6},
            name="Line 2",
        )
    )

    # Cross product for common perpendicular
    _cross = np.cross(_d1, _d2)
    _cross_norm_sq = np.dot(_cross, _cross)

    if _cross_norm_sq < 1e-12:
        _status_3d = "Parallel"
    else:
        _diff = _p2 - _p1
        _dist = abs(np.dot(_diff, _cross)) / np.sqrt(_cross_norm_sq)

        if _sep < 0.01:
            _status_3d = "Intersecting (distance = 0)"
            # Mark intersection
            _fig.add_trace(
                go.Scatter3d(
                    x=[0],
                    y=[0],
                    z=[0],
                    mode="markers",
                    marker={"color": COLORS["quaternary"], "size": 10},
                    name="Vertex",
                )
            )
        else:
            _status_3d = f"Skew — minimum distance = {_dist:.3f}"
            # Draw common perpendicular
            # Closest points: solve system
            _b_3d = _p2 - _p1
            _e = np.dot(_d1, _d1)
            _f = np.dot(_d1, _d2)
            _g = np.dot(_d2, _d2)
            _denom_3d = _e * _g - _f * _f
            if abs(_denom_3d) > 1e-12:
                _t_close = (np.dot(_b_3d, _d1) * _g - np.dot(_b_3d, _d2) * _f) / _denom_3d
                _s_close = (np.dot(_b_3d, _d1) * _f - np.dot(_b_3d, _d2) * _e) / _denom_3d
                _q1 = _p1 + _t_close * _d1
                _q2 = _p2 + _s_close * _d2
                _fig.add_trace(
                    go.Scatter3d(
                        x=[_q1[0], _q2[0]],
                        y=[_q1[1], _q2[1]],
                        z=[_q1[2], _q2[2]],
                        mode="lines+markers",
                        line={"color": COLORS["quaternary"], "width": 4, "dash": "dash"},
                        marker={"color": COLORS["quaternary"], "size": 8},
                        name=f"Min. distance = {_dist:.3f}",
                    )
                )

    _scene = {
        **SCENE_THEME,
        "xaxis": {**SCENE_THEME["xaxis"], "title": "x"},
        "yaxis": {**SCENE_THEME["yaxis"], "title": "y"},
        "zaxis": {**SCENE_THEME["zaxis"], "title": "z"},
    }
    _fig.update_layout(**base_layout(title=_status_3d, scene=_scene, height=480))
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    Drag the "Separation" slider from 0 to 1: the lines start intersecting and
    gradually become skew. The yellow dashed segment is the **common perpendicular**
    — the shortest path between the two lines. In 3D graphics and robotics, this
    minimum-distance calculation appears everywhere (collision detection, robot kinematics).

    The formula $d = |(\mathbf{p}_2 - \mathbf{p}_1) \cdot (\mathbf{d}_1 \times \mathbf{d}_2)| / |\mathbf{d}_1 \times \mathbf{d}_2|$
    is the projection of the displacement vector onto the common perpendicular direction.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part VIII: The Vertex — Intersection as a Structural Atom

    ### What is a Vertex?

    The word **vertex** (Latin: "top", "turning point") has several related meanings
    across mathematics, all tracing back to the idea of an intersection:

    **In geometry**: A vertex is a corner — the intersection of two edges of a
    polygon or polyhedron. A triangle has 3 vertices; a cube has 8.

    **In graph theory**: A **graph** $G = (V, E)$ consists of a set of **vertices**
    $V$ and **edges** $E$. An edge connects two vertices. The intersection of two edges
    is only meaningful at a vertex; edges in a graph have no notion of where they "cross"
    in space — only which vertices they connect.

    **In knot theory** (from Notebook 008): A vertex in a knot diagram is a crossing —
    the point where two strands of the projection appear to intersect. The over/under
    information specifies which strand is actually passing in front.

    **In combinatorics**: Vertices are the fundamental discrete unit. The study of which
    vertices are connected (adjacency) leads to graph coloring, spanning trees, network
    flows — all independent of any geometric embedding.

    ### The Intersection Point IS the Vertex

    When two line segments meet at a point, that point is a vertex. This connects:

    $$\text{line intersection} \xrightarrow{\text{discrete}} \text{vertex in a graph}$$

    A **planar graph** is one that can be drawn in the plane with edges meeting only at vertices
    (no crossing edges). The condition "edges don't cross except at vertices" is exactly
    the condition that each apparent crossing is a genuine vertex, not an accidental one.

    **Euler's formula** for connected planar graphs:
    $$V - E + F = 2$$
    where $V$ = vertices, $E$ = edges, $F$ = faces (including the outer face).
    This is a topological invariant — it does not depend on how the graph is drawn.
    """)
    return


@app.cell
def _(COLORS, base_layout, plot_directed_graph):
    # Schlegel diagram (planar graph of a cube)
    _vertices = {
        "A": (0, 0),
        "B": (3, 0),
        "C": (2, 1),
        "D": (1, 1),
        "E": (0, 3),
        "F": (3, 3),
        "G": (2, 2),
        "H": (1, 2),
    }
    _edges = [
        # Outer square
        ("A", "B"),
        ("B", "F"),
        ("F", "E"),
        ("E", "A"),
        # Inner square
        ("D", "C"),
        ("C", "G"),
        ("G", "H"),
        ("H", "D"),
        # Connecting edges
        ("A", "D"),
        ("B", "C"),
        ("F", "G"),
        ("E", "H"),
    ]

    _fig = plot_directed_graph(
        nodes=_vertices,
        edges=_edges,
        node_size=14,
        node_color=COLORS["secondary"],
        edge_color=COLORS["tertiary"],
        text_color=COLORS["quaternary"],
        title="Planar Graph: Cube Projection — Euler's Formula V − E + F = 2",
        show_arrows=False,
    )

    _V = len(_vertices)
    _E = len(_edges)
    _F = _E - _V + 2  # Euler's formula
    _fig.add_annotation(
        x=1.5,
        y=-0.5,
        text=f"V = {_V},  E = {_E},  F = {_F}  →  V − E + F = {_V - _E + _F}",
        font={"color": COLORS["quaternary"], "size": 14},
        showarrow=False,
    )

    _fig.update_layout(
        **base_layout(
            title="Planar Graph: Cube Projection — Euler's Formula V − E + F = 2",
            xaxis={
                "gridcolor": COLORS["grid"],
                "zerolinecolor": COLORS["grid"],
                "range": [-0.5, 3.5],
                "showticklabels": False,
                "scaleanchor": "y",
            },
            yaxis={
                "gridcolor": COLORS["grid"],
                "zerolinecolor": COLORS["grid"],
                "range": [-1, 3.5],
                "showticklabels": False,
            },
            height=420,
        )
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    Euler's formula $V - E + F = 2$ holds for any connected planar graph,
    regardless of how it is drawn. For the cube: $8 - 12 + 6 = 2$. ✓

    The key requirement: edges intersect **only at vertices**. An accidental
    crossing in the drawing would create a false vertex and violate the formula.
    This is why planarity matters: it ensures every apparent intersection is
    a genuine structural vertex.

    ### Vertices, Crossings, and Knots

    In Notebook 008 we saw that a knot diagram has **vertices** at every
    crossing — points where the projection of a 3D curve crosses itself.
    These are **not** true intersections of the curve in 3D (the curve has no
    self-intersections there); they are artifacts of the 2D projection.

    | Context | "Vertex" means | Lines involved |
    |---------|---------------|----------------|
    | Geometry | Corner of polygon | Two edge-lines |
    | Graph theory | Node in $G = (V,E)$ | No geometric lines — abstract |
    | Knot diagram | Crossing of projection | Two strand-lines in the diagram |
    | Computer graphics | Polygon corner | Two edge vectors |
    | Linear algebra | Solution of $Ax = b$ | $n$ hyperplanes in $\mathbb{R}^n$ |

    In every case, the vertex is the **place where constraints meet** — where
    the question "what satisfies all conditions simultaneously?" has an answer.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part IX: The Angle Between Lines

    ### Angle from Direction Vectors

    Two lines have direction vectors $\mathbf{d}_1$ and $\mathbf{d}_2$.
    The **acute angle** $\theta$ between the lines satisfies:

    $$\cos\theta = \frac{|\mathbf{d}_1 \cdot \mathbf{d}_2|}{|\mathbf{d}_1||\mathbf{d}_2|}$$

    (We take the absolute value because a line has two directions; we want the
    angle in $[0°, 90°]$.)

    - $\theta = 0°$: lines are parallel ($\mathbf{d}_1 \parallel \mathbf{d}_2$)
    - $\theta = 90°$: lines are perpendicular ($\mathbf{d}_1 \cdot \mathbf{d}_2 = 0$)

    ### Perpendicular Lines

    Two lines are **perpendicular** iff their direction vectors satisfy $\mathbf{d}_1 \cdot \mathbf{d}_2 = 0$,
    or equivalently their slopes satisfy:

    $$m_1 \cdot m_2 = -1 \quad \text{(in 2D, for non-vertical lines)}$$

    This means: if $L_1$ has slope $m$, the perpendicular line has slope $-1/m$.
    The product is $-1$ because rotating a vector 90° maps $(d_x, d_y) \mapsto (-d_y, d_x)$,
    and the slope of the rotated vector is $d_x / (-d_y) = -1/(d_y/d_x) = -1/m$.
    """)
    return


@app.cell
def _(mo):
    angle_m1 = mo.ui.slider(start=-3.0, stop=3.0, step=0.1, value=1.0, label="Slope of L₁", show_value=True)
    return (angle_m1,)


@app.cell
def _(angle_m1, mo):
    mo.hstack([mo.md("### Angle Between Two Lines"), angle_m1])
    return


@app.cell
def _(COLORS, angle_m1, base_layout, go, np):
    _m1 = angle_m1.value
    _m2_perp = -1.0 / _m1 if abs(_m1) > 1e-9 else float("inf")

    _x = np.linspace(-5, 5, 200)
    _y1 = _m1 * _x

    _d1 = np.array([1.0, _m1])
    _d2 = np.array([1.0, _m2_perp]) if abs(_m2_perp) < 100 else np.array([0.0, 1.0])

    _cos_th = abs(np.dot(_d1, _d2)) / (np.linalg.norm(_d1) * np.linalg.norm(_d2))
    _cos_th = min(_cos_th, 1.0)
    _theta_deg = np.degrees(np.arccos(_cos_th))

    _fig = go.Figure()

    # L1
    _fig.add_trace(
        go.Scatter(
            x=_x,
            y=_y1,
            mode="lines",
            line={"color": COLORS["primary"], "width": 3},
            name=f"L₁: slope = {_m1:.2f}",
        )
    )

    # Perpendicular line
    if abs(_m2_perp) < 100:
        _fig.add_trace(
            go.Scatter(
                x=_x,
                y=_m2_perp * _x,
                mode="lines",
                line={"color": COLORS["secondary"], "width": 3},
                name=f"L₂ ⊥ L₁: slope = {_m2_perp:.2f}",
            )
        )
    else:
        _fig.add_trace(
            go.Scatter(
                x=[0, 0],
                y=[-5, 5],
                mode="lines",
                line={"color": COLORS["secondary"], "width": 3},
                name="L₂ ⊥ L₁: vertical",
            )
        )

    # Direction vectors
    _scale = 1.8
    _d1n = _d1 / np.linalg.norm(_d1)
    _d2n = _d2 / np.linalg.norm(_d2)

    _fig.add_trace(
        go.Scatter(
            x=[0, _scale * _d1n[0]],
            y=[0, _scale * _d1n[1]],
            mode="lines+markers",
            line={"color": COLORS["primary"], "width": 4},
            marker={"symbol": "arrow", "size": 14, "angleref": "previous", "color": COLORS["primary"]},
            name=f"d₁ = ({_d1n[0]:.2f}, {_d1n[1]:.2f})",
        )
    )
    _fig.add_trace(
        go.Scatter(
            x=[0, _scale * _d2n[0]],
            y=[0, _scale * _d2n[1]],
            mode="lines+markers",
            line={"color": COLORS["secondary"], "width": 4},
            marker={"symbol": "arrow", "size": 14, "angleref": "previous", "color": COLORS["secondary"]},
            name=f"d₂ = ({_d2n[0]:.2f}, {_d2n[1]:.2f})",
        )
    )

    # Angle arc
    _ang1 = np.arctan2(_d1n[1], _d1n[0])
    _ang2 = np.arctan2(_d2n[1], _d2n[0])
    _arc_r = 0.6
    _arc_angles = np.linspace(min(_ang1, _ang2), max(_ang1, _ang2), 40)
    _fig.add_trace(
        go.Scatter(
            x=_arc_r * np.cos(_arc_angles),
            y=_arc_r * np.sin(_arc_angles),
            mode="lines",
            line={"color": COLORS["quaternary"], "width": 2},
            showlegend=False,
            hoverinfo="skip",
        )
    )

    _dot_prod = np.dot(_d1n, _d2n)
    _fig.add_annotation(
        x=0,
        y=-3.5,
        text=f"d₁·d₂ = {_dot_prod:.3f}  |  angle = {_theta_deg:.1f}°  |  m₁·m₂ = {_m1 * (_m2_perp if abs(_m2_perp) < 100 else 0):.2f}",
        font={"color": COLORS["quaternary"], "size": 13},
        showarrow=False,
    )

    _fig.add_hline(y=0, line_color=COLORS["text_secondary"], line_width=1)
    _fig.add_vline(x=0, line_color=COLORS["text_secondary"], line_width=1)

    _fig.update_layout(
        **base_layout(
            title=f"Perpendicular lines: d₁ · d₂ = {_dot_prod:.4f} ≈ 0",
            xaxis={
                "gridcolor": COLORS["grid"],
                "zerolinecolor": COLORS["text_secondary"],
                "range": [-5, 5],
                "title": "x",
                "scaleanchor": "y",
            },
            yaxis={
                "gridcolor": COLORS["grid"],
                "zerolinecolor": COLORS["text_secondary"],
                "range": [-5, 5],
                "title": "y",
            },
            height=500,
        )
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    The red line is always perpendicular to the blue one. As you change the slope,
    the perpendicular slope adjusts as $m_2 = -1/m_1$. Notice that the dot product
    of the direction vectors stays at 0 — that is the algebraic signature of perpendicularity.

    **Special cases:**
    - Horizontal line ($m_1 = 0$): perpendicular is vertical (undefined slope)
    - Vertical line: perpendicular is horizontal
    - $m_1 = 1$ (45°): perpendicular has slope $-1$ (also 45°, mirrored)
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part X: Summary — The Thread from Lines to Vertices

    ### Everything Connected

    We started with the most elementary question — "where do two lines cross?" —
    and found it sits at the intersection of several deep ideas:

    **Algebraically:**
    - A line intersection is the solution of a $2 \times 2$ linear system
    - The determinant controls existence: $D \neq 0$ ↔ unique intersection
    - Cramer's rule expresses the solution as a ratio of determinants (areas)

    **Vectorially:**
    - Lines are most naturally represented as $\mathbf{p} + t\mathbf{d}$
    - The dot product measures angles; the cross product measures orientation and area
    - In 3D, a third case appears: skew lines, with a minimum distance given by the cross product

    **Topologically:**
    - The intersection point is a **vertex** — the atom of intersection in all of mathematics
    - Euler's formula $V - E + F = 2$ counts vertices, edges, faces of any planar graph
    - In knot theory, vertices are crossings — controlled intersections that encode the knot's topology

    ### Quick Reference

    | Representation | Intersection method | Parallel condition |
    |----------------|--------------------|--------------------|
    | $y = mx + b$ | $x^* = (b_2-b_1)/(m_1-m_2)$ | $m_1 = m_2$ |
    | $ax + by = c$ | Cramer's rule | $\det = a_1b_2 - a_2b_1 = 0$ |
    | $\mathbf{p} + t\mathbf{d}$ | Solve $2 \times 2$ system | $\mathbf{d}_1 \times \mathbf{d}_2 = 0$ |
    | 3D parametric | Solve + check consistency | $\mathbf{d}_1 \times \mathbf{d}_2 = \mathbf{0}$ |

    | Condition | What it means |
    |-----------|--------------|
    | $\mathbf{u} \cdot \mathbf{v} = 0$ | $\mathbf{u}$ and $\mathbf{v}$ are perpendicular |
    | $\mathbf{u} \times \mathbf{v} = 0$ | $\mathbf{u}$ and $\mathbf{v}$ are parallel |
    | $\det A = 0$ | Rows of $A$ are parallel; system has no unique solution |
    | $m_1 m_2 = -1$ | Lines with slopes $m_1$ and $m_2$ are perpendicular |
    | $V - E + F = 2$ | Graph is connected and planar |

    ### Further Reading

    **Books:**
    - Strang, *Introduction to Linear Algebra* — determinants, systems, geometry
    - Axler, *Linear Algebra Done Right* — vectors and operators rigorously
    - de Berg et al., *Computational Geometry* — algorithms for line intersections

    **Videos:**
    - [3Blue1Brown: Essence of Linear Algebra](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab) — determinants as areas, visually
    - [3Blue1Brown: Cross products](https://www.youtube.com/watch?v=eu6i7WJeinw)
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    *"The intersection of two lines is such a simple thing that we barely notice
    it — and yet it is the seed from which determinants, vectors, topology, and
    graph theory all grow."*
    """)
    return


if __name__ == "__main__":
    app.run()
