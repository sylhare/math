"""
The Kakeya Conjecture: Turning a Needle in Vanishing Space

An exploration of the Kakeya needle problem — from a 1917 geometry puzzle about the
smallest area needed to rotate a needle, through Besicovitch's measure-zero sets and
the reframing in terms of dimension, to the 2D resolution by Davies and the
celebrated 2025 proof of the three-dimensional conjecture by Hong Wang and Joshua Zahl.
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

    return (
        COLORS,
        SCENE_THEME,
        base_layout,
        create_timeline,
        go,
        make_subplots,
        np,
        style_subplot_axes,
    )


@app.cell
def _(np):
    # Shared helpers, defined once and reused across the figure cells below.

    def fibonacci_sphere(n):
        """Return (dx, dy, dz) unit direction vectors spread evenly over the sphere."""
        i = np.arange(n)
        golden_angle = np.pi * (3.0 - np.sqrt(5.0))
        dz = 1 - (i + 0.5) * 2.0 / n
        ring = np.sqrt(np.clip(1 - dz * dz, 0, 1))
        theta = golden_angle * i
        return ring * np.cos(theta), ring * np.sin(theta), dz

    def play_pause(play_label):
        """Return a Plotly play/pause button pair for a frame animation."""
        return [
            {
                "type": "buttons",
                "showactive": False,
                "y": 1.1,
                "x": 0.5,
                "xanchor": "center",
                "buttons": [
                    {
                        "label": play_label,
                        "method": "animate",
                        "args": [None, {"frame": {"duration": 60, "redraw": True}, "fromcurrent": True}],
                    },
                    {
                        "label": "❚❚ Pause",
                        "method": "animate",
                        "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}],
                    },
                ],
            }
        ]

    return fibonacci_sphere, play_pause


@app.cell
def _(mo):
    mo.md(r"""
    # The Kakeya Conjecture: Turning a Needle in Vanishing Space

    *"This thing doesn't need hyping up. It's a once-in-a-century kind of result."*
    — Nets Katz, on the 2025 proof

    ---

    ## A Puzzle That Looks Too Simple

    Lay an infinitely thin, one-inch needle flat on a table. Now rotate it until it
    has pointed in **every** direction, then set it back down. What is the *smallest
    area* the needle can sweep out while doing so?

    Sōichi Kakeya asked exactly this in **1917**. The instinctive answer — spin it
    about its centre — sweeps a disk. But it turns out you can be cleverer, and the
    honest answer is astonishing: **the area can be made as close to zero as you like.**

    That single fact opened a rabbit hole that took *over a century* to fully explore.
    Along the way the question mutated from *"how small can the area be?"* into
    *"how small can the **dimension** be?"* — and that harder question, the **Kakeya
    conjecture**, was only settled in three dimensions in **2025**.

    **What you'll explore in this notebook:**
    - The needle problem, and why the naive circular answer is far from optimal
    - Besicovitch's shocking measure-zero construction (the *slice-and-slide* trick)
    - Why mathematicians swapped *area* for *dimension* — and what dimension even means
    - The **2D** story: who solved which version, and how
    - Interactive **3D** animations of what a Kakeya set actually looks like
    - The **2025** breakthrough of Wang & Zahl, and why it stops dead at dimension 3
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part I: A Century of the Needle

    ### Kakeya poses the puzzle (1917)

    [**Sōichi Kakeya**](https://en.wikipedia.org/wiki/S%C5%8Dichi_Kakeya) (掛谷 宗一), a
    Japanese mathematician, asked for the region of least area inside which a unit line
    segment can be *continuously* rotated through a full half-turn (180°), returning to
    its original line reversed.

    ### Besicovitch drops the bombshell (1919–1928)

    The Russian mathematician
    [**Abram Besicovitch**](https://en.wikipedia.org/wiki/Abram_Samoilovitch_Besicovitch),
    working on a completely different problem about the integrability of functions,
    discovered a construction of a
    [set](https://en.wikipedia.org/wiki/Kakeya_set) that contains a unit segment in
    **every** direction yet has **area zero**. Such a set is now called a **Besicovitch
    set**. His *slice-and-slide* idea (later streamlined by **Oskar Perron** into *Perron
    trees*, using joins introduced by **Gyula Pál**) showed the needle-turning area can be
    shrunk below any positive bound.

    ### The question is reborn as *dimension* (mid-20th century)

    A measure-zero set can still be "large" in a subtler sense. Mathematicians replaced
    *area* with [**Hausdorff dimension**](https://en.wikipedia.org/wiki/Hausdorff_dimension)
    and conjectured: a Kakeya set in $\mathbb{R}^n$ must have the *full* dimension $n$,
    even if its measure is zero.

    ### The plane falls (1971)

    **Roy Davies** proved the conjecture in $\mathbb{R}^2$: every Besicovitch set in the
    plane has Hausdorff dimension exactly $2$. Later, **Córdoba** gave a cleaner geometric
    proof, and **Oberlin** sharpened the result all the way to *Fourier* dimension $2$.
    ([Jean Bourgain](https://en.wikipedia.org/wiki/Jean_Bourgain), by contrast, made his
    mark on the *higher*-dimensional versions.)

    ### Three dimensions resist for 50 years (1995–2025)

    **Thomas Wolff** (1995) reached dimension $\tfrac{5}{2}$ with the *hairbrush*
    argument; **Katz–Łaba–Tao** (2000) nudged past it. Then in **February 2025**,
    [**Hong Wang**](https://www.nyu.edu/about/news-publications/news/2026/july/nyu-professor-hong-wang-wins-fields-medal.html)
    (NYU / IHES) and **Joshua Zahl** (UBC) posted a proof that closes the gap: every
    Kakeya set in $\mathbb{R}^3$ has dimension exactly $3$. In **2026** the result earned
    Wang a [**Fields Medal**](https://en.wikipedia.org/wiki/Fields_Medal) — only the third
    ever awarded to a woman.
    """)
    return


@app.cell
def _(create_timeline):
    create_timeline(
        [
            (1917, "Kakeya\nPoses the needle problem", 1),
            (1921, "Pál\nJoins between segments", -1),
            (1928, "Besicovitch / Perron\nMeasure-zero sets", 1),
            (1971, "Davies\nDimension 2 in the plane", -1),
            (1995, "Wolff\nHairbrush: dim ≥ 5/2", 1),
            (2025, "Wang & Zahl\nDimension 3 solved", -1),
            (2026, "Hong Wang\nFields Medal", 1),
        ],
        title="A Timeline of the Kakeya Problem",
        x_range=(1905, 2045),
        height=320,
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part II: The Naive Answer — Just Spin It

    The most obvious way to point a needle in every direction is to spin it about its
    midpoint. A unit needle centred at the origin sweeps out a **disk of radius
    $\tfrac{1}{2}$**, so the area is

    $$A_{\text{circle}} = \pi \left(\tfrac{1}{2}\right)^2 = \frac{\pi}{4} \approx 0.785.$$

    Press **▶ Rotate** below to watch it turn. This is our baseline — everything that
    follows beats it.
    """)
    return


@app.cell
def _(COLORS, base_layout, go, np, play_pause):
    # Naive solution: rotate a unit needle about its centre -> sweeps a disk of radius 1/2.
    _angles = np.linspace(0, np.pi, 37)
    _disk_t = np.linspace(0, 2 * np.pi, 120)
    _disk_x = 0.5 * np.cos(_disk_t)
    _disk_y = 0.5 * np.sin(_disk_t)

    def _needle(theta):
        return [-0.5 * np.cos(theta), 0.5 * np.cos(theta)], [-0.5 * np.sin(theta), 0.5 * np.sin(theta)]

    _nx0, _ny0 = _needle(_angles[0])

    _fig = go.Figure()
    _fig.add_trace(
        go.Scatter(
            x=_disk_x,
            y=_disk_y,
            mode="lines",
            line={"color": COLORS["grid"], "width": 2},
            fill="toself",
            fillcolor="rgba(0, 212, 255, 0.12)",
            name="swept disk (area π/4)",
        )
    )
    _fig.add_trace(
        go.Scatter(
            x=_nx0,
            y=_ny0,
            mode="lines+markers",
            line={"color": COLORS["secondary"], "width": 6},
            marker={"color": COLORS["quaternary"], "size": 6},
            name="unit needle",
        )
    )

    _frames = []
    for _th in _angles:
        _nx, _ny = _needle(_th)
        _frames.append(
            go.Frame(
                data=[
                    go.Scatter(x=_disk_x, y=_disk_y),
                    go.Scatter(x=_nx, y=_ny),
                ],
                name=f"{np.degrees(_th):.0f}",
            )
        )
    _fig.frames = _frames

    _fig.update_layout(
        **base_layout(
            title="Naive Solution: Spin the Needle → Disk of Area π/4 ≈ 0.785",
            height=460,
            xaxis={"range": [-0.75, 0.75], "scaleanchor": "y", "constrain": "domain"},
            yaxis={"range": [-0.75, 0.75]},
        )
    )
    _fig.update_layout(updatemenus=play_pause("▶ Rotate"))
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part III: Doing Better — the Deltoid

    We can already beat the disk with a classical shape: the
    [**deltoid**](https://en.wikipedia.org/wiki/Deltoid_curve), a three-cusped
    hypocycloid. A needle can be turned all the way around while staying inside it,
    because every tangent line of the deltoid cuts a chord of *constant length* — the
    needle simply rides along these tangent chords.

    Scaled to a unit needle, the deltoid has area

    $$A_{\text{deltoid}} = \frac{\pi}{8} \approx 0.393,$$

    exactly **half** the disk. The deltoid is *not convex*; if you insist on a convex
    region, **Pál** (1921) showed the smallest is the **equilateral triangle of
    height 1**, with area $\tfrac{1}{\sqrt 3} \approx 0.577$.

    Below, the moving red needle is always a tangent chord of the fixed deltoid.
    """)
    return


@app.cell
def _(COLORS, base_layout, go, np, play_pause):
    # Deltoid (3-cusped hypocycloid), scaled so the tangent chord (the needle) has length 1.
    _scale = 0.25  # raw chord length is 4; scale to a unit needle
    _bt = np.linspace(0, 2 * np.pi, 900)
    _bx = _scale * (2 * np.cos(_bt) + np.cos(2 * _bt))
    _by = _scale * (2 * np.sin(_bt) - np.sin(2 * _bt))

    def _tangent_chord(t):
        px = _scale * (2 * np.cos(t) + np.cos(2 * t))
        py = _scale * (2 * np.sin(t) - np.sin(2 * t))
        dx = -2 * np.sin(t) - 2 * np.sin(2 * t)
        dy = 2 * np.cos(t) - 2 * np.cos(2 * t)
        norm = np.hypot(dx, dy)
        if norm < 1e-9:  # cusp: pick an arbitrary direction
            dx, dy, norm = 1.0, 0.0, 1.0
        ux, uy = dx / norm, dy / norm
        nx_, ny_ = -uy, ux  # perpendicular unit vector to the tangent line
        s = (_bx - px) * nx_ + (_by - py) * ny_
        cross_x, cross_y = [], []
        for i in range(len(s) - 1):
            if s[i] == 0.0 or (s[i] < 0) != (s[i + 1] < 0):
                denom = s[i] - s[i + 1]
                if denom == 0:
                    continue
                f = s[i] / denom
                cross_x.append(_bx[i] + f * (_bx[i + 1] - _bx[i]))
                cross_y.append(_by[i] + f * (_by[i + 1] - _by[i]))
        if len(cross_x) < 2:  # fallback: length-1 segment centred on the tangent point
            return [px - 0.5 * ux, px + 0.5 * ux], [py - 0.5 * uy, py + 0.5 * uy]
        cx = np.array(cross_x)
        cy = np.array(cross_y)
        best_i, best_j, best_d = 0, 1, -1.0
        for i in range(len(cx)):
            for j in range(i + 1, len(cx)):
                d = (cx[i] - cx[j]) ** 2 + (cy[i] - cy[j]) ** 2
                if d > best_d:
                    best_d, best_i, best_j = d, i, j
        return [cx[best_i], cx[best_j]], [cy[best_i], cy[best_j]]

    _angles = np.linspace(0, 2 * np.pi, 37)
    _nx0, _ny0 = _tangent_chord(_angles[0])

    _fig = go.Figure()
    _fig.add_trace(
        go.Scatter(
            x=_bx,
            y=_by,
            mode="lines",
            line={"color": COLORS["primary"], "width": 3},
            fill="toself",
            fillcolor="rgba(0, 212, 255, 0.10)",
            name="deltoid (area π/8)",
        )
    )
    _fig.add_trace(
        go.Scatter(
            x=_nx0,
            y=_ny0,
            mode="lines+markers",
            line={"color": COLORS["secondary"], "width": 6},
            marker={"color": COLORS["quaternary"], "size": 6},
            name="needle = tangent chord",
        )
    )

    _frames = []
    for _th in _angles:
        _nx, _ny = _tangent_chord(_th)
        _frames.append(
            go.Frame(data=[go.Scatter(x=_bx, y=_by), go.Scatter(x=_nx, y=_ny)], name=f"{np.degrees(_th):.0f}")
        )
    _fig.frames = _frames

    _fig.update_layout(
        **base_layout(
            title="A Needle Turning Inside a Deltoid → Area π/8 ≈ 0.393",
            height=480,
            xaxis={"range": [-0.9, 0.9], "scaleanchor": "y", "constrain": "domain"},
            yaxis={"range": [-0.9, 0.9]},
        )
    )
    _fig.update_layout(updatemenus=play_pause("▶ Turn"))
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part IV: Besicovitch — Shrinking the Area to Nothing

    The deltoid and triangle are pretty, but Besicovitch showed there is **no lower
    bound at all**. The engine is a single observation:

    > **Translating a shape does not change the set of directions it contains.**

    So take a triangle (it contains needles pointing across a whole fan of directions),
    slice it down the middle into two sub-triangles, and **slide them so they overlap**.
    The union still covers every direction in the fan — but its area has shrunk, because
    the overlap is now counted only once. Repeat this recursively (the **Perron tree**)
    and the area tumbles toward zero while the directional coverage is untouched.

    Drag the slider to slide the two halves together and watch the union area fall.
    """)
    return


@app.cell
def _(mo):
    besicovitch_slide = mo.ui.slider(
        start=0.0, stop=0.45, step=0.03, value=0.24, label="Slide the halves together", show_value=True
    )
    besicovitch_slide
    return (besicovitch_slide,)


@app.cell
def _(COLORS, base_layout, besicovitch_slide, go, make_subplots, np, style_subplot_axes):
    # Two halves of a unit triangle, slid together so they overlap.
    # Translation preserves the directions each half contains, but the union area shrinks.
    _apex = np.array([0.5, 1.0])
    _left = np.array([[0.0, 0.0], [0.5, 0.0], _apex])  # left half-triangle
    _right = np.array([[0.5, 0.0], [1.0, 0.0], _apex])  # right half-triangle

    def _shift(tri, dx):
        out = tri.copy()
        out[:, 0] = out[:, 0] + dx
        return out

    _s = float(besicovitch_slide.value)
    _L = _shift(_left, _s)  # slide left half rightward
    _R = _shift(_right, -_s)  # slide right half leftward

    def _in_triangle(px, py, tri):
        (ax, ay), (bx, by), (cx, cy) = tri
        v0x, v0y = cx - ax, cy - ay
        v1x, v1y = bx - ax, by - ay
        v2x, v2y = px - ax, py - ay
        d00 = v0x * v0x + v0y * v0y
        d01 = v0x * v1x + v0y * v1y
        d11 = v1x * v1x + v1y * v1y
        d20 = v2x * v0x + v2y * v0y
        d21 = v2x * v1x + v2y * v1y
        denom = d00 * d11 - d01 * d01
        u = (d11 * d20 - d01 * d21) / denom
        v = (d00 * d21 - d01 * d20) / denom
        return (u >= 0) & (v >= 0) & (u + v <= 1)

    # Union area by rasterisation
    _gx = np.linspace(-0.2, 1.2, 420)
    _gy = np.linspace(-0.05, 1.05, 330)
    _GX, _GY = np.meshgrid(_gx, _gy)
    _inside = _in_triangle(_GX, _GY, _L) | _in_triangle(_GX, _GY, _R)
    _cell = (_gx[1] - _gx[0]) * (_gy[1] - _gy[0])
    _area = float(_inside.sum() * _cell)

    # Area-vs-slide curve
    _slides = np.linspace(0.0, 0.45, 16)
    _areas = []
    for _sv in _slides:
        _Ls = _shift(_left, _sv)
        _Rs = _shift(_right, -_sv)
        _ins = _in_triangle(_GX, _GY, _Ls) | _in_triangle(_GX, _GY, _Rs)
        _areas.append(float(_ins.sum() * _cell))

    _fig = make_subplots(
        rows=1,
        cols=2,
        column_widths=[0.55, 0.45],
        subplot_titles=("The two overlapping halves", "Union area vs. slide"),
    )

    for _tri, _name, _col in ((_L, "left half", COLORS["primary"]), (_R, "right half", COLORS["secondary"])):
        _fig.add_trace(
            go.Scatter(
                x=[*list(_tri[:, 0]), _tri[0, 0]],
                y=[*list(_tri[:, 1]), _tri[0, 1]],
                mode="lines",
                fill="toself",
                fillcolor="rgba(0, 212, 255, 0.28)" if _col == COLORS["primary"] else "rgba(255, 107, 107, 0.28)",
                line={"color": _col, "width": 2},
                name=_name,
            ),
            row=1,
            col=1,
        )

    _fig.add_trace(
        go.Scatter(
            x=_slides,
            y=_areas,
            mode="lines+markers",
            line={"color": COLORS["quaternary"], "width": 3},
            marker={"size": 6},
            name="union area",
        ),
        row=1,
        col=2,
    )
    _fig.add_trace(
        go.Scatter(
            x=[_s],
            y=[_area],
            mode="markers",
            marker={"color": COLORS["accent1"], "size": 14, "symbol": "star"},
            name="current",
        ),
        row=1,
        col=2,
    )

    _fig.update_layout(
        **base_layout(
            title=f"Slice-and-Slide: union area ≈ {_area:.3f} (from 0.500 for the whole triangle)",
            height=440,
        )
    )
    _fig.update_xaxes(range=[-0.2, 1.2], row=1, col=1, scaleanchor="y", constrain="domain")
    _fig.update_yaxes(range=[-0.05, 1.05], row=1, col=1)
    _fig.update_xaxes(title_text="slide amount", row=1, col=2)
    _fig.update_yaxes(title_text="area", row=1, col=2)
    style_subplot_axes(_fig, show_ticklabels=True)
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    Each slide keeps every direction the two halves originally covered, yet the union
    shrinks. Iterating this on ever-finer slices is the **Perron tree**, and in the
    limit it produces a genuine **Besicovitch set**:

    $$K \subset \mathbb{R}^2, \quad K \text{ contains a unit segment in every direction}, \quad |K| = 0.$$

    So *measure* is a dead end — every Besicovitch set has area zero. To measure how
    "big" these thorny sets really are, we need a finer ruler: **dimension**.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part V: What Does "Dimension" Even Mean?

    A line has dimension 1, a filled square dimension 2. The
    [**box-counting dimension**](https://en.wikipedia.org/wiki/Minkowski%E2%80%93Bouligand_dimension)
    makes this precise: cover the set with a grid of boxes of side $\varepsilon$ and
    count how many boxes $N(\varepsilon)$ the set touches. The dimension is the rate at
    which that count grows as the boxes shrink:

    $$\dim_{\mathrm B}(E) = \lim_{\varepsilon \to 0} \frac{\log N(\varepsilon)}{\log(1/\varepsilon)}.$$

    The closely related **Hausdorff dimension** is defined through coverings by sets of
    varying size, $\dim_{\mathrm H}(E) = \inf\{\, s \ge 0 : \mathcal H^{s}(E) = 0 \,\}$,
    and is the one used in the conjecture. On the log–log plot below, the **slope** of
    the line *is* the dimension: a segment gives slope $\approx 1$, a filled triangle
    slope $\approx 2$.
    """)
    return


@app.cell
def _(COLORS, base_layout, go, np):
    # Box-counting dimension: count occupied ε-boxes for a 1D segment and a 2D filled triangle.
    def _box_count(points, eps):
        keys = set()
        inv = 1.0 / eps
        for px, py in points:
            keys.add((int(np.floor(px * inv)), int(np.floor(py * inv))))
        return len(keys)

    _tline = np.linspace(0, 1, 20000)
    _segment = np.column_stack([_tline, 0.6 * _tline])  # a slanted segment (dim 1)

    # A filled triangle sampled on a fine deterministic grid (dim 2).
    _grid = np.linspace(0, 1, 400)
    _gu, _gv = np.meshgrid(_grid, _grid)
    _gu, _gv = _gu.ravel(), _gv.ravel()
    _mask = _gu + _gv <= 1.0
    _triangle = np.column_stack([_gu[_mask], _gv[_mask]])

    _epsilons = np.array([1 / 2, 1 / 4, 1 / 8, 1 / 16, 1 / 32, 1 / 64, 1 / 128])
    _seg_counts = np.array([_box_count(_segment, e) for e in _epsilons])
    _tri_counts = np.array([_box_count(_triangle, e) for e in _epsilons])

    _log_inv_eps = np.log(1 / _epsilons)
    _seg_slope = np.polyfit(_log_inv_eps, np.log(_seg_counts), 1)[0]
    _tri_slope = np.polyfit(_log_inv_eps, np.log(_tri_counts), 1)[0]

    _fig = go.Figure()
    _fig.add_trace(
        go.Scatter(
            x=_log_inv_eps,
            y=np.log(_seg_counts),
            mode="lines+markers",
            line={"color": COLORS["primary"], "width": 3},
            marker={"size": 9},
            name=f"segment — slope ≈ {_seg_slope:.2f} (dim 1)",
        )
    )
    _fig.add_trace(
        go.Scatter(
            x=_log_inv_eps,
            y=np.log(_tri_counts),
            mode="lines+markers",
            line={"color": COLORS["secondary"], "width": 3},
            marker={"size": 9},
            name=f"filled triangle — slope ≈ {_tri_slope:.2f} (dim 2)",
        )
    )
    _fig.update_layout(
        **base_layout(
            title="Box-Counting: the Slope of log N(ε) vs log(1/ε) Is the Dimension",
            height=440,
            xaxis={"title": "log(1/ε)"},
            yaxis={"title": "log N(ε)"},
        )
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part VI: The Conjecture, and the 2D Answer

    With dimension in hand, the modern **Kakeya conjecture** is a single clean line:

    $$\text{Every Kakeya set } K \subset \mathbb{R}^n \text{ has } \dim_{\mathrm H}(K) = \dim_{\mathrm M}(K) = n.$$

    Zero area, but *full dimension* — as spiky and pervasive as the ambient space itself.

    **The plane ($n = 2$) — solved, in several ways:**

    | Version of the question | Answer | By whom |
    |---|---|---|
    | Smallest **convex** turning region | equilateral triangle, area $1/\sqrt3$ | **Pál** (1921) |
    | Smallest turning **area** at all | can be made arbitrarily small | **Besicovitch / Perron** (1928) |
    | Hausdorff **dimension** of a Besicovitch set | exactly $2$ | **Davies** (1971) |
    | New proofs & strengthenings | dimension $2$; Fourier dimension $2$ | **Córdoba, Bourgain, Oberlin** |

    The heart of Davies' lower bound is a **duality**: a set of segments in many
    directions corresponds to a set of *points* seen along many directions. If the
    Kakeya set were low-dimensional, those directions would have to collapse — which is
    impossible in the plane. The picture below shows the "bush" of unit segments in many
    directions through a common point that these arguments analyse.
    """)
    return


@app.cell
def _(COLORS, base_layout, go, np):
    # A 2D "bush": unit segments in many directions through a common point.
    _dirs = np.linspace(0, np.pi, 60, endpoint=False)
    _bx, _by = [], []
    for _th in _dirs:
        _bx += [-0.5 * np.cos(_th), 0.5 * np.cos(_th), None]
        _by += [-0.5 * np.sin(_th), 0.5 * np.sin(_th), None]

    _fig = go.Figure()
    _fig.add_trace(
        go.Scatter(
            x=_bx,
            y=_by,
            mode="lines",
            line={"color": COLORS["primary"], "width": 1},
            opacity=0.7,
            name="60 unit segments",
        )
    )
    _fig.add_trace(
        go.Scatter(
            x=[0],
            y=[0],
            mode="markers",
            marker={"color": COLORS["quaternary"], "size": 10},
            name="common point",
        )
    )
    _fig.update_layout(
        **base_layout(
            title="A 2D 'Bush': a Unit Segment in Every Direction",
            height=440,
            xaxis={"range": [-0.65, 0.65], "scaleanchor": "y", "constrain": "domain"},
            yaxis={"range": [-0.65, 0.65]},
        )
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part VII: Into Three Dimensions

    In space, a Kakeya set contains a unit segment pointing in *every* direction of the
    sphere. Drag the plot below to rotate it: this is a 3D **bush**, a genuine Kakeya
    set that (like its 2D cousin) can have volume zero.

    The conjecture claims that despite its wispy, measure-zero appearance, its dimension
    is the full $3$. Proving that turned out to be extraordinarily hard.
    """)
    return


@app.cell
def _(COLORS, SCENE_THEME, base_layout, fibonacci_sphere, go):
    # A 3D "bush": unit segments through the origin, directions sampled evenly on the sphere.
    _n = 240
    _dx, _dy, _dz = fibonacci_sphere(_n)

    _lx, _ly, _lz = [], [], []
    for _k in range(_n):
        _lx += [-0.5 * _dx[_k], 0.5 * _dx[_k], None]
        _ly += [-0.5 * _dy[_k], 0.5 * _dy[_k], None]
        _lz += [-0.5 * _dz[_k], 0.5 * _dz[_k], None]

    _fig = go.Figure()
    _fig.add_trace(
        go.Scatter3d(
            x=_lx,
            y=_ly,
            z=_lz,
            mode="lines",
            line={"color": COLORS["primary"], "width": 2},
            opacity=0.6,
            name="240 unit segments",
        )
    )
    _fig.update_layout(
        **base_layout(
            title="A 3D Kakeya 'Bush' — a Unit Segment in Every Direction (drag to rotate)",
            height=560,
            scene=SCENE_THEME,
        )
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    To *feel* the "every direction" requirement, the animation below sends a single unit
    needle spiralling over the whole sphere of directions. The faint dots mark where the
    needle has already pointed — together they trace out the full sphere of directions
    that a Kakeya set must accommodate.
    """)
    return


@app.cell
def _(COLORS, SCENE_THEME, base_layout, fibonacci_sphere, go, play_pause):
    # Animate one needle sweeping over all directions on the sphere; accumulate its tips.
    _n = 64
    _dx, _dy, _dz = fibonacci_sphere(_n)

    _fig = go.Figure()
    _fig.add_trace(
        go.Scatter3d(
            x=[-0.5 * _dx[0], 0.5 * _dx[0]],
            y=[-0.5 * _dy[0], 0.5 * _dy[0]],
            z=[-0.5 * _dz[0], 0.5 * _dz[0]],
            mode="lines",
            line={"color": COLORS["secondary"], "width": 8},
            name="needle",
        )
    )
    _fig.add_trace(
        go.Scatter3d(
            x=[0.5 * _dx[0]],
            y=[0.5 * _dy[0]],
            z=[0.5 * _dz[0]],
            mode="markers",
            marker={"color": COLORS["primary"], "size": 2},
            opacity=0.5,
            name="directions covered",
        )
    )

    _frames = []
    for _k in range(1, _n):
        _frames.append(
            go.Frame(
                data=[
                    go.Scatter3d(
                        x=[-0.5 * _dx[_k], 0.5 * _dx[_k]],
                        y=[-0.5 * _dy[_k], 0.5 * _dy[_k]],
                        z=[-0.5 * _dz[_k], 0.5 * _dz[_k]],
                    ),
                    go.Scatter3d(
                        x=list(0.5 * _dx[: _k + 1]),
                        y=list(0.5 * _dy[: _k + 1]),
                        z=list(0.5 * _dz[: _k + 1]),
                    ),
                ],
                name=str(_k),
            )
        )
    _fig.frames = _frames

    _fig.update_layout(
        **base_layout(
            title="One Needle Sweeping Every 3D Direction",
            height=560,
            scene=SCENE_THEME,
        )
    )
    _fig.update_layout(updatemenus=play_pause("▶ Sweep"))
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part VIII: Fifty Years of Chipping Away

    In 3D, mathematicians could not reach dimension $3$ directly — they crept up on it
    with better and better *lower bounds*. Each new idea proved "the dimension is at
    least $d$" for a larger $d$:

    - **Bush argument** (Córdoba-style): every direction gives a segment through a busy
      point, forcing $\dim \ge \tfrac{n+1}{2} = 2$ in 3D.
    - **Wolff's hairbrush** (1995): stack many bushes along a segment to get
      $\dim \ge \tfrac{n+2}{2} = \tfrac{5}{2}$.
    - **Katz–Łaba–Tao** (2000): a hard-won $\tfrac{5}{2} + \varepsilon$, showing $5/2$
      was not the end.
    - **Wang–Zahl** (2025): the finish line, $\dim = 3$.

    The bar chart shows how each method moved the needle — and how the last step closed
    a gap that had stood for a quarter-century.
    """)
    return


@app.cell
def _(COLORS, base_layout, go):
    # Proven Hausdorff-dimension lower bounds for Kakeya sets in R^3 over time.
    _labels = [
        "Trivial\n(contains a line)",
        "Bush\n(n+1)/2",
        "Wolff hairbrush\n(n+2)/2",
        "Katz–Łaba–Tao\n5/2 + ε",
        "Wang–Zahl 2025\n(full)",
    ]
    _values = [1.0, 2.0, 2.5, 2.51, 3.0]
    _colors = [COLORS["muted"], COLORS["accent3"], COLORS["tertiary"], COLORS["quaternary"], COLORS["secondary"]]

    _fig = go.Figure()
    _fig.add_trace(
        go.Bar(
            x=_labels,
            y=_values,
            marker_color=_colors,
            text=[f"{v:.2f}".rstrip("0").rstrip(".") if v != 2.51 else "5/2 + ε" for v in _values],
            textposition="outside",
            name="proven lower bound",
        )
    )
    _fig.add_hline(
        y=3.0,
        line_dash="dash",
        line_color=COLORS["highlight"],
        annotation_text="conjectured dimension = 3",
        annotation_font_color=COLORS["highlight"],
    )
    _fig.update_layout(
        **base_layout(
            title="Lower Bounds on Kakeya Dimension in ℝ³ Through Time",
            height=460,
            yaxis={"title": "proven dim_H ≥", "range": [0, 3.3]},
        )
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part IX: The 2025 Breakthrough

    In February 2025, **Hong Wang** and **Joshua Zahl** posted
    [*Volume estimates for unions of convex sets, and the Kakeya set conjecture in three
    dimensions*](https://arxiv.org/abs/2502.17655) (127 pages), proving:

    $$\text{Every Kakeya set } K \subset \mathbb{R}^3 \text{ has } \dim_{\mathrm H}(K) = \dim_{\mathrm M}(K) = 3.$$

    Two ideas carried the proof (see
    [Tao's exposition](https://terrytao.wordpress.com/2025/02/25/the-three-dimensional-kakeya-conjecture-after-wang-and-zahl/)):

    1. **The sticky case first.** Following a strategy of **Katz–Tao**, they first handle
       *sticky* Kakeya sets — ones where nearby directions stay geometrically close, so
       the tubes line up into an approximately self-similar structure. This case was
       settled in earlier work with new *grains* and *induction-on-scales* estimates.
    2. **Reducing the general case to the sticky case.** The genuinely new step —
       described by Larry Guth as the part that "seemed completely out of reach" — shows
       any Kakeya set can be deformed toward a sticky one without shrinking its dimension.

    In July **2026**, the [International Mathematical Union awarded Hong Wang a Fields
    Medal](https://www.nyu.edu/about/news-publications/news/2026/july/nyu-professor-hong-wang-wins-fields-medal.html)
    at the Philadelphia ICM, largely for this work — making her the third woman to win
    mathematics' most famous prize.

    ### Why it stops at three

    Strikingly, the theorem is **special to $n = 3$**. In dimensions $n \ge 4$ the direct
    analogue of their key volume estimate is *false*: one can pack tubes into the
    neighbourhood of a low-degree algebraic variety, producing counterexamples to the
    intermediate statements. The full Kakeya conjecture for $n \ge 4$ remains **open** —
    the needle has only just begun to turn.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Why Anyone Cares

    A puzzle about turning a needle would be a curiosity if it stayed alone. It doesn't.
    The geometry of *lines pointing in many directions* is a hidden skeleton beneath a
    surprising amount of mathematics:

    - **Harmonic analysis.** Kakeya sits directly below the **restriction** and
      **Bochner–Riesz** conjectures and the behaviour of the Fourier transform.
      [**Charles Fefferman**](https://en.wikipedia.org/wiki/Charles_Fefferman) used a
      Besicovitch set to *disprove* the ball multiplier conjecture (1971) — the discovery
      that turned a geometry curiosity into a central object of analysis.
    - **PDE.** Sharp estimates for the **wave** and **Schrödinger** equations rely on
      Kakeya-type bounds on how wave packets can concentrate.
    - **Number theory & combinatorics.** The finite-field Kakeya problem (posed by Wolff,
      solved by [**Zeev Dvir**](https://arxiv.org/abs/0803.2336) in 2008 with a
      stunningly short polynomial-method argument) feeds into **seeded extractors** and
      coding theory in computer science.

    A single inch-long needle, turned just so, reaches all the way from a 1917 puzzle to
    the frontiers of analysis, number theory, and cryptography.

    ---

    ## References & Further Reading

    **The 2025 three-dimensional proof**

    - Hong Wang & Joshua Zahl, *Volume estimates for unions of convex sets, and the
      Kakeya set conjecture in three dimensions* (arXiv, Feb 2025):
      [arxiv.org/abs/2502.17655](https://arxiv.org/abs/2502.17655)
    - Terence Tao, *The three-dimensional Kakeya conjecture, after Wang and Zahl*:
      [terrytao.wordpress.com](https://terrytao.wordpress.com/2025/02/25/the-three-dimensional-kakeya-conjecture-after-wang-and-zahl/)
    - Quanta Magazine, *'Once in a Century' Proof Settles Math's Kakeya Conjecture*:
      [quantamagazine.org](https://www.quantamagazine.org/once-in-a-century-proof-settles-maths-kakeya-conjecture-20250314/)
    - UBC Mathematics, *Josh Zahl and Hong Wang Prove the Kakeya Conjecture in Three
      Dimensions*:
      [math.ubc.ca](https://www.math.ubc.ca/news-events/news/mar-4-2025-josh-zahl-and-hong-wang-prove-kakeya-conjecture-three-dimensions)
    - Scientific American, *The Kakeya Conjecture … Is Solved in Three Dimensions*:
      [scientificamerican.com](https://www.scientificamerican.com/article/the-kakeya-conjecture-a-decades-old-math-problem-is-solved-in-three/)

    **The 2026 Fields Medal**

    - NYU, *NYU Professor Hong Wang Wins Fields Medal*:
      [nyu.edu](https://www.nyu.edu/about/news-publications/news/2026/july/nyu-professor-hong-wang-wins-fields-medal.html)
    - IHES, *Hong Wang, Permanent Professor at IHES, awarded the 2026 Fields Medal*:
      [ihes.fr](https://www.ihes.fr/en/hong-wang2026-fields-medal/)

    **Background & history**

    - R. O. Davies, *Some remarks on the Kakeya problem*, Proc. Camb. Phil. Soc. **69**
      (1971), 417–421 — the 2D dimension result.
    - Terence Tao, *From rotating needles to stability of waves* (survey), Notices of
      the AMS: [terrytao.wordpress.com/kakeya.pdf](https://terrytao.wordpress.com/wp-content/uploads/2009/08/kakeya.pdf)
    - Zeev Dvir, *On the size of Kakeya sets in finite fields* (2008) — the polynomial
      method: [arxiv.org/abs/0803.2336](https://arxiv.org/abs/0803.2336)
    - Wikipedia, *Kakeya set*:
      [en.wikipedia.org/wiki/Kakeya_set](https://en.wikipedia.org/wiki/Kakeya_set)

    ---

    Not bad for a puzzle about turning a needle on a tabletop.
    """)
    return


if __name__ == "__main__":
    app.run()
