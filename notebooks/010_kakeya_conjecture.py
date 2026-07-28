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

    def spherical_spiral(n, turns=6):
        """Return (dx, dy, dz) along a smooth pole-to-pole spiral over the unit sphere.

        Unlike the Fibonacci spread (great for *even* coverage but which jumps ~137°
        in longitude between consecutive points), here successive samples are close
        together — so a needle stepping through them sweeps smoothly instead of
        shaking in place.
        """
        t = np.linspace(0, 1, n)
        dz = np.cos(np.pi * t)  # north pole (+1) -> south pole (-1), even in polar angle
        ring = np.sqrt(np.clip(1 - dz * dz, 0, 1))
        theta = 2 * np.pi * turns * t
        return ring * np.cos(theta), ring * np.sin(theta), dz

    def needle_segments(dirs):
        """None-separated coordinate lists of unit segments through the origin.

        ``dirs`` is a tuple of direction-component arrays — ``(dx, dy)`` in 2D or
        ``(dx, dy, dz)`` in 3D — one output list per component, ready for a single
        Scatter/Scatter3d "lines" trace.
        """
        coords = [[] for _ in dirs]
        for k in range(len(dirs[0])):
            for axis, comp in zip(coords, dirs):
                axis += [-0.5 * comp[k], 0.5 * comp[k], None]
        return coords

    def sphere_surface(go, radius=0.5, color="#00d4ff", opacity=0.12):
        """A faint translucent sphere — the set of all directions the tips trace out."""
        u = np.linspace(0, 2 * np.pi, 48)
        v = np.linspace(0, np.pi, 24)
        sx = radius * np.outer(np.cos(u), np.sin(v))
        sy = radius * np.outer(np.sin(u), np.sin(v))
        sz = radius * np.outer(np.ones_like(u), np.cos(v))
        return go.Surface(
            x=sx,
            y=sy,
            z=sz,
            showscale=False,
            opacity=opacity,
            colorscale=[[0, color], [1, color]],
            hoverinfo="skip",
            showlegend=False,
            name="sphere of directions",
        )

    def in_triangle(px, py, tri):
        """Boolean mask: which (px, py) grid points lie inside triangle ``tri``."""
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
        if abs(denom) < 1e-15:
            return np.zeros(px.shape, dtype=bool)
        u = (d11 * d20 - d01 * d21) / denom
        v = (d00 * d21 - d01 * d20) / denom
        return (u >= 0) & (v >= 0) & (u + v <= 1)

    def union_area(tris, gx, gy):
        """Rasterised area of the union of ``tris`` over the meshgrids ``gx``, ``gy``."""
        mask = np.zeros(gx.shape, dtype=bool)
        for t in tris:
            mask |= in_triangle(gx, gy, t)
        return float(mask.sum() * (gx[0, 1] - gx[0, 0]) * (gy[1, 0] - gy[0, 0]))

    def perron_stages(base, levels, alpha=0.16, steps=8):
        """Perron tree: repeatedly slice every triangle in half and slide the halves to overlap.

        Translation can't change the directions inside a piece, so the direction-fan stays
        fully covered — but the shared area keeps dropping. Returns a list of
        ``(triangles, level)`` snapshots, with the slide animated within each level.
        """
        def _slide(tris, sigma):
            out = []
            for b0, b1, apex in tris:
                m = (b0 + b1) / 2.0
                d = np.array([sigma * alpha * (b1[0] - b0[0]), 0.0])
                out.append(np.array([b0, m, apex]) + d)
                out.append(np.array([m, b1, apex]) - d)
            return out

        fracs = np.linspace(0.0, 1.0, steps)
        stages = [(base, 0)]
        current = base
        for lvl in range(1, levels + 1):
            for sig in fracs:
                stages.append((_slide(current, sig), lvl))
            current = _slide(current, 1.0)
        return stages

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

    return (
        fibonacci_sphere,
        needle_segments,
        perron_stages,
        play_pause,
        spherical_spiral,
        sphere_surface,
        union_area,
    )


@app.cell
def _(mo):
    mo.md(r"""
    # The Kakeya Conjecture: Turning a Needle in Vanishing Space

    *"This thing doesn't need hyping up. It's a once-in-a-century kind of result."*
    — Nets Katz, on the 2025 proof

    ---

    ## A Puzzle That Looks Too Simple

    > Imagine turning a car until it has faced every compass
    > direction, then parking it. You'd expect to need a roundabout's worth of tarmac —
    > yet the astonishing answer is that you can do it in almost *no* space at all.

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

    > A hundred-year relay race: each mathematician carries the
    > idea a little further, from a 1917 doodle on paper to a 2026 Fields Medal.

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

    > The clumsy way to face every direction is to spin on the
    > spot like a clock's hand — it works, but it hogs an entire disk of space.

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

    > Give the needle a curved "skateboard bowl" to ride and it
    > can turn the whole way round using only half the room.

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

    def _deltoid_pt(u):
        return _scale * (2 * np.cos(u) + np.cos(2 * u)), _scale * (2 * np.sin(u) - np.sin(2 * u))

    def _tangent_chord(t):
        # The tangent line at parameter t re-meets the deltoid at parameters -t/2 and
        # pi - t/2; the segment it cuts off is the needle, and its length is always 1.
        # (Closed form — no root-finding, so it stays smooth through the three cusps.)
        ax, ay = _deltoid_pt(-t / 2)
        bx, by = _deltoid_pt(np.pi - t / 2)
        return [ax, bx], [ay, by]

    _bt = np.linspace(0, 2 * np.pi, 900)
    _bx, _by = _deltoid_pt(_bt)

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

    > Sliding a shape never changes the directions tucked inside it — so you can overlap
    > the slices like two paper cut-outs laid on the same spot: every direction is still
    > there, but the shared area is counted only once, letting the footprint melt toward zero.

    The deltoid and triangle are pretty, but Besicovitch showed there is **no lower
    bound at all**. The engine is a single observation:

    > **Translating a shape does not change the set of directions it contains.**

    So take a triangle (it contains needles pointing across a whole fan of directions),
    slice it down the middle into two sub-triangles, and **slide them so they overlap**.
    The union still covers every direction in the fan — but its area has shrunk, because
    the overlap is now counted only once. Repeat this recursively (the **Perron tree**)
    and the area tumbles toward zero while the directional coverage is untouched.

    Press **▶ Iterate** to run the **Perron tree**: each round slices *every* triangle in
    half and slides the halves to overlap. Because translation never changes the directions
    inside a piece, the full fan of directions stays covered the whole time — yet the shared
    area keeps tumbling (watch the readout). One slice alone barely dents it; the shrinking
    only really bites once you iterate, and in the limit of infinitely many slices it reaches
    **zero**.
    """)
    return


@app.cell
def _(COLORS, base_layout, go, np, perron_stages, play_pause, union_area):
    # The Perron tree (built in the shared helpers): recursively slice every triangle in half
    # and slide the halves to overlap. Each slice preserves the direction-fan, yet the shared
    # area keeps dropping. We rasterise the true union area so the readout is honest.
    _gx = np.linspace(-0.65, 0.65, 220)
    _gy = np.linspace(-0.05, 1.05, 180)
    _GX, _GY = np.meshgrid(_gx, _gy)

    _base = [np.array([[-0.5, 0.0], [0.5, 0.0], [0.0, 1.0]])]
    _stages = perron_stages(_base, levels=5)

    def _poly_trace(tris):
        _x, _y = [], []
        for _t in tris:
            _x += [_t[0, 0], _t[1, 0], _t[2, 0], _t[0, 0], None]
            _y += [_t[0, 1], _t[1, 1], _t[2, 1], _t[0, 1], None]
        return go.Scatter(
            x=_x, y=_y, mode="lines", fill="toself", fillcolor="rgba(0, 212, 255, 0.18)",
            line={"color": COLORS["primary"], "width": 1}, showlegend=False, name="Perron tree",
        )

    def _label_trace(tris, level):
        _n = 2**level
        return go.Scatter(
            x=[0.0], y=[1.14], mode="text",
            text=[f"level {level}  ·  {_n} triangle{'s' if _n > 1 else ''}  ·  area ≈ {union_area(tris, _GX, _GY):.3f}"],
            textfont={"color": COLORS["highlight"], "size": 15}, showlegend=False,
        )

    _fig = go.Figure()
    _fig.add_trace(_poly_trace(_stages[0][0]))  # trace 0
    _fig.add_trace(_label_trace(*_stages[0]))  # trace 1
    _fig.frames = [
        go.Frame(data=[_poly_trace(_t), _label_trace(_t, _lv)], traces=[0, 1], name=str(_i))
        for _i, (_t, _lv) in enumerate(_stages)
    ]

    _fig.update_layout(
        **base_layout(
            title="Perron Tree: Keep Slicing & Sliding — the Area Tumbles Toward Zero",
            height=520,
            xaxis={"range": [-0.65, 0.65], "scaleanchor": "y", "constrain": "domain", "showticklabels": False},
            yaxis={"range": [-0.05, 1.25], "showticklabels": False},
        )
    )
    _fig.update_layout(updatemenus=play_pause("▶ Iterate"))
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
    ### An intuition: "stealing" the third dimension

    Here's a great way to *feel* why zero area isn't absurd — think of **folding the needle
    up out of the plane**. Pin one end to the table and tip the needle upward: its **shadow
    on the floor shrinks toward a single point**. Now swing it over the top and lay it back
    down pointing a completely new way. The needle has **changed direction**, but its shadow
    only ever traced two thin lines — so on the floor it used **essentially zero area**.

    That's a genuine 3D move (a segment really can be reoriented while sweeping almost no
    footprint). The catch: Kakeya's puzzle forbids leaving the table. So Besicovitch has to
    pull off the *same* zero-area magic staying perfectly flat — by sliding the needle along
    its **own length**, which is the in-the-plane version of "shrinking it to a dot" (a needle
    gliding along the line it already sits on paints no new area).
    """)
    return


@app.cell
def _(COLORS, SCENE_THEME, base_layout, go, np, play_pause):
    # "Fold to a dot" intuition: a needle pinned at the origin tips up to vertical (its floor
    # shadow shrinks to a point), swings over the top, and lays back down pointing a NEW way.
    # The shadow only ever sweeps two thin radii -> zero floor area, yet the direction changed.
    _phis = np.linspace(0, np.pi / 2, 26)
    _states = [(1.0, 0.0, _p) for _p in _phis] + [(0.0, 1.0, _p) for _p in _phis[::-1]]

    def _tip(k):
        _ax, _ay, _phi = _states[k]
        return np.cos(_phi) * _ax, np.cos(_phi) * _ay, np.sin(_phi)

    def _needle(k):
        _tx, _ty, _tz = _tip(k)
        return go.Scatter3d(
            x=[0, _tx], y=[0, _ty], z=[0, _tz], mode="lines",
            line={"color": COLORS["secondary"], "width": 10}, name="needle",
        )

    def _cone(k):
        _tx, _ty, _tz = _tip(k)
        return go.Cone(
            x=[_tx], y=[_ty], z=[_tz], u=[_tx], v=[_ty], w=[_tz],
            sizemode="absolute", sizeref=0.16, anchor="tip", showscale=False,
            colorscale=[[0, COLORS["quaternary"]], [1, COLORS["quaternary"]]], name="direction",
        )

    def _shadow_path(k):
        _sx = [np.cos(_states[_j][2]) * _states[_j][0] for _j in range(k + 1)]
        _sy = [np.cos(_states[_j][2]) * _states[_j][1] for _j in range(k + 1)]
        return go.Scatter3d(
            x=_sx, y=_sy, z=[0] * len(_sx), mode="lines",
            line={"color": COLORS["primary"], "width": 8}, name="floor shadow (≈ zero area)",
        )

    def _shadow_dot(k):
        _tx, _ty, _tz = _tip(k)
        return go.Scatter3d(
            x=[_tx], y=[_ty], z=[0], mode="markers",
            marker={"color": COLORS["primary"], "size": 5}, showlegend=False, name="shadow",
        )

    _fu = np.array([-1.1, 1.1])
    _FX, _FY = np.meshgrid(_fu, _fu)
    _fig = go.Figure()
    _fig.add_trace(  # trace 0: the floor (z = 0), static
        go.Surface(
            x=_FX, y=_FY, z=np.zeros((2, 2)), showscale=False, opacity=0.12,
            colorscale=[[0, COLORS["grid"]], [1, COLORS["grid"]]], hoverinfo="skip", showlegend=False,
        )
    )
    _fig.add_trace(_shadow_path(0))  # 1
    _fig.add_trace(_needle(0))  # 2
    _fig.add_trace(_cone(0))  # 3
    _fig.add_trace(_shadow_dot(0))  # 4

    _fig.frames = [
        go.Frame(data=[_shadow_path(_k), _needle(_k), _cone(_k), _shadow_dot(_k)], traces=[1, 2, 3, 4], name=str(_k))
        for _k in range(1, len(_states))
    ]

    _scene = {
        **SCENE_THEME,
        "xaxis": {**SCENE_THEME["xaxis"], "range": [-1.1, 1.1], "title": "x (floor)"},
        "yaxis": {**SCENE_THEME["yaxis"], "range": [-1.1, 1.1], "title": "y (floor)"},
        "zaxis": {**SCENE_THEME["zaxis"], "range": [-0.05, 1.1], "title": "up"},
        "aspectmode": "manual",
        "aspectratio": {"x": 2, "y": 2, "z": 1},
    }
    _fig.update_layout(
        **base_layout(
            title="Change Direction for Free: Stand the Needle Up → its Floor Shadow Vanishes",
            height=560,
            scene=_scene,
        )
    )
    _fig.update_layout(updatemenus=play_pause("▶ Fold & turn"))
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part V: What Does "Dimension" Even Mean?

    > Dimension is a shape's *appetite for space* as you zoom in:
    > how fast the number of tiles needed to cover it grows as the tiles shrink.

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
    **So what is that slope actually telling us?** Halve the size of your covering boxes
    and watch how the count multiplies:

    - A **line** (1D): halving the boxes roughly **doubles** the count ($2 = 2^1$) → slope **1**.
    - A **filled patch** (2D): halving the boxes roughly **quadruples** it ($4 = 2^2$) → slope **2**.

    The little exponent on that "$2^{\,?}$" *is* the dimension. Crucially it need **not** be a
    whole number — which is exactly why dimension can measure spiky, fractal, in-between sets
    that the labels "1, 2, 3" cannot.

    **And here's why it matters for Kakeya.** A Besicovitch set has **zero area**, so your gut
    says it must behave like a thin 1D scribble. But its box-count still **quadruples** every
    time you halve the ruler — slope **2**, the same explosive growth as a *solid* patch. So it
    fills no area at all, yet carries the full dimension of the plane. That clash — *"takes up no
    space"* (area $= 0$) versus *"detail multiplies as fast as a solid region"* (dimension $= 2$)
    — is the entire heart of the Kakeya conjecture, and what all the hard work is fighting over.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part VI: The Conjecture, and the 2D Answer

    > On a flat table you can make the needle's trail weigh
    > nothing — yet it stays stubbornly two-dimensional, as "wide" as the table itself.

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
def _(COLORS, base_layout, go, needle_segments, np):
    # A 2D "bush": unit segments in many directions through a common point.
    _dirs = np.linspace(0, np.pi, 60, endpoint=False)
    _bx, _by = needle_segments((np.cos(_dirs), np.sin(_dirs)))

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
    ### The cheap way vs. the expensive way to turn

    This is the crux — and it's *not* the same as spinning in a circle. Watch all three
    needles below face **every** direction, but pay wildly different amounts of area:

    - **Left — pivot on the spot.** The needle turns about its centre. It does point every
      way, but it paints the *entire disk*: area $\pi/4 \approx 0.785$. This is "rotating in
      a circle."
    - **Middle — slide *and* turn.** The needle rolls around a deltoid, sliding as it turns.
      Same directions covered, yet it paints only $\pi/8 \approx 0.393$ — half as much —
      because sliding a needle *along its own length* adds no new area (it just retraces the
      line it already sits on). That "free" in-and-out slide is the whole idea.
    - **Right — slice & slide (Perron tree).** Push that same idea to the limit: chop the
      region into ever-finer overlapping slivers and the painted area tumbles toward
      **zero** — Besicovitch's result (Part IV).

    Watch all three fill: identical directions, wildly different paint. *(In 3D the circle
    of directions becomes a whole sphere — the next section.)*
    """)
    return


@app.cell
def _(COLORS, base_layout, go, make_subplots, np, perron_stages, play_pause, style_subplot_axes, union_area):
    # Three ways to point a needle in every direction, side by side:
    #   pivot on the spot -> fills the whole disk (pi/4);  slide & turn on a deltoid -> pi/8;
    #   slice & slide (Perron) -> tumbles toward 0. Same directions, wildly different area.
    _n = 48
    _scale = 0.25

    def _deltoid_pt(u):
        return _scale * (2 * np.cos(u) + np.cos(2 * u)), _scale * (2 * np.sin(u) - np.sin(2 * u))

    _ang = np.linspace(0, np.pi, _n)  # left: centred diameter turning a half-turn
    _dc, _ds = np.cos(_ang), np.sin(_ang)

    def _diam(k):
        return [-0.5 * _dc[k], 0.5 * _dc[k]], [-0.5 * _ds[k], 0.5 * _ds[k]]

    _tt = np.linspace(0, 2 * np.pi, _n)  # middle: tangent chord of the deltoid

    def _chord(k):
        _ax, _ay = _deltoid_pt(-_tt[k] / 2)
        _bx, _by = _deltoid_pt(np.pi - _tt[k] / 2)
        return [_ax, _bx], [_ay, _by]

    def _accum_trace(fn, k, ax):
        # Every needle position up to frame k -> shows the region the needle has swept.
        _xs, _ys = [], []
        for _j in range(k + 1):
            _x, _y = fn(_j)
            _xs += [_x[0], _x[1], None]
            _ys += [_y[0], _y[1], None]
        return go.Scatter(
            x=_xs, y=_ys, mode="lines", line={"color": COLORS["primary"], "width": 1},
            opacity=0.35, xaxis=ax[0], yaxis=ax[1], showlegend=False, name="swept",
        )

    def _cur_trace(fn, k, ax):
        _x, _y = fn(k)
        return go.Scatter(
            x=_x, y=_y, mode="lines", line={"color": COLORS["secondary"], "width": 5},
            xaxis=ax[0], yaxis=ax[1], showlegend=False, name="needle",
        )

    # Right panel: Perron tree (centred vertically to share the same window), sampled so it
    # keeps subdividing across the frames while the disk and deltoid fill.
    _pbase = [np.array([[-0.5, -0.5], [0.5, -0.5], [0.0, 0.5]])]
    _pstages = perron_stages(_pbase, levels=5)
    _pgx = np.linspace(-0.8, 0.8, 200)
    _pgy = np.linspace(-0.8, 0.8, 200)
    _PGX, _PGY = np.meshgrid(_pgx, _pgy)

    def _pstage(k):
        return _pstages[min(len(_pstages) - 1, int(round(k / (_n - 1) * (len(_pstages) - 1))))]

    def _perron_trace(k, ax):
        _tris, _ = _pstage(k)
        _x, _y = [], []
        for _t in _tris:
            _x += [_t[0, 0], _t[1, 0], _t[2, 0], _t[0, 0], None]
            _y += [_t[0, 1], _t[1, 1], _t[2, 1], _t[0, 1], None]
        return go.Scatter(
            x=_x, y=_y, mode="lines", fill="toself", fillcolor="rgba(149, 225, 211, 0.20)",
            line={"color": COLORS["accent1"], "width": 1}, xaxis=ax[0], yaxis=ax[1], showlegend=False, name="perron",
        )

    def _perron_label(k, ax):
        _tris, _ = _pstage(k)
        return go.Scatter(
            x=[0.0], y=[0.68], mode="text", text=[f"area ≈ {union_area(_tris, _PGX, _PGY):.3f}"],
            textfont={"color": COLORS["highlight"], "size": 13}, xaxis=ax[0], yaxis=ax[1], showlegend=False,
        )

    _P1, _P2, _P3 = ("x", "y"), ("x2", "y2"), ("x3", "y3")
    _fig = make_subplots(
        rows=1,
        cols=3,
        subplot_titles=(
            "Pivot on the spot → π/4 ≈ 0.785",
            "Slide & turn → π/8 ≈ 0.393",
            "Slice & slide (Perron) → 0",
        ),
    )

    _dt = np.linspace(0, 2 * np.pi, 200)
    _fig.add_trace(  # 0: swept disk (static fill)
        go.Scatter(
            x=0.5 * np.cos(_dt), y=0.5 * np.sin(_dt), mode="lines", fill="toself",
            fillcolor="rgba(0, 212, 255, 0.10)", line={"color": COLORS["grid"], "width": 1.5},
            xaxis="x", yaxis="y", showlegend=False, name="disk",
        ),
        row=1, col=1,
    )
    _fig.add_trace(_accum_trace(_diam, 0, _P1), row=1, col=1)  # 1
    _fig.add_trace(_cur_trace(_diam, 0, _P1), row=1, col=1)  # 2

    _bxo, _byo = _deltoid_pt(np.linspace(0, 2 * np.pi, 400))
    _fig.add_trace(  # 3: deltoid region (static fill)
        go.Scatter(
            x=_bxo, y=_byo, mode="lines", fill="toself",
            fillcolor="rgba(255, 230, 109, 0.10)", line={"color": COLORS["grid"], "width": 1.5},
            xaxis="x2", yaxis="y2", showlegend=False, name="deltoid",
        ),
        row=1, col=2,
    )
    _fig.add_trace(_accum_trace(_chord, 0, _P2), row=1, col=2)  # 4
    _fig.add_trace(_cur_trace(_chord, 0, _P2), row=1, col=2)  # 5

    _fig.add_trace(_perron_trace(0, _P3), row=1, col=3)  # 6
    _fig.add_trace(_perron_label(0, _P3), row=1, col=3)  # 7

    _fig.frames = [
        go.Frame(
            data=[_accum_trace(_diam, _k, _P1), _cur_trace(_diam, _k, _P1),
                  _accum_trace(_chord, _k, _P2), _cur_trace(_chord, _k, _P2),
                  _perron_trace(_k, _P3), _perron_label(_k, _P3)],
            traces=[1, 2, 4, 5, 6, 7],
            name=str(_k),
        )
        for _k in range(1, _n)
    ]

    _fig.update_layout(
        **base_layout(
            title="Same Directions, Very Different Area: Disk vs. Deltoid vs. Perron Tree",
            height=430,
        )
    )
    for _col in (1, 2, 3):
        _fig.update_xaxes(
            range=[-0.8, 0.8], row=1, col=_col,
            scaleanchor="y" if _col == 1 else f"y{_col}", constrain="domain",
        )
        _fig.update_yaxes(range=[-0.8, 0.8], row=1, col=_col)
    style_subplot_axes(_fig)
    _fig.update_layout(updatemenus=play_pause("▶ Turn"))
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part VII: Into Three Dimensions

    > Now play the same game in mid-air: the needle must aim at
    > every star in the sky, sweeping out a whole *sphere* of directions.

    In space, a Kakeya set contains a unit segment pointing in *every* direction of the
    sphere. Drag the plot below to rotate it: this is a 3D **bush**, a genuine Kakeya
    set that (like its 2D cousin) can have volume zero.

    The conjecture claims that despite its wispy, measure-zero appearance, its dimension
    is the full $3$. Proving that turned out to be extraordinarily hard.
    """)
    return


@app.cell
def _(COLORS, SCENE_THEME, base_layout, fibonacci_sphere, go, needle_segments, sphere_surface):
    # A 3D "bush": unit segments through the origin, directions sampled evenly on the sphere.
    _n = 240
    _dx, _dy, _dz = fibonacci_sphere(_n)
    _lx, _ly, _lz = needle_segments((_dx, _dy, _dz))

    _fig = go.Figure()
    # The tips of every segment sit on this sphere of radius 1/2 — the "shape" of directions.
    _fig.add_trace(sphere_surface(go, color=COLORS["accent3"], opacity=0.10))
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
    needle spiralling over the whole sphere of directions. Keep three things in view:

    - The **needle** (thick coral line) always passes through the origin, so it is a
      *diameter* of the faint sphere. The **yellow arrow** on its leading tip shows which
      way it currently points — watch the arrow to see the direction change.
    - The faint **sphere of radius $\tfrac12$** is the "shape" that makes it work: *every*
      point on it is one direction the needle must eventually hit.
    - The bright **dots** accumulate where the tip has already been — the needle's job is
      done only once they cover the entire sphere.
    """)
    return


@app.cell
def _(COLORS, SCENE_THEME, base_layout, go, play_pause, spherical_spiral, sphere_surface):
    # Animate one needle sweeping over all directions on the sphere; accumulate its tips.
    # The needle is a diameter of the faint sphere: as it turns, its leading tip (the
    # arrow) paints the sphere, which *is* the "shape" of all directions to be covered.
    # A smooth spiral (not the Fibonacci spread) keeps consecutive frames close, so the
    # needle glides continuously instead of jittering.
    _n = 180
    _dx, _dy, _dz = spherical_spiral(_n, turns=6)

    def _needle_line(k):
        return go.Scatter3d(
            x=[-0.5 * _dx[k], 0.5 * _dx[k]],
            y=[-0.5 * _dy[k], 0.5 * _dy[k]],
            z=[-0.5 * _dz[k], 0.5 * _dz[k]],
            mode="lines",
            line={"color": COLORS["secondary"], "width": 10},
            name="needle",
        )

    def _arrow(k):
        # A cone at the leading tip, pointing along the needle — shows which way it faces.
        return go.Cone(
            x=[0.5 * _dx[k]],
            y=[0.5 * _dy[k]],
            z=[0.5 * _dz[k]],
            u=[_dx[k]],
            v=[_dy[k]],
            w=[_dz[k]],
            sizemode="absolute",
            sizeref=0.12,
            anchor="tip",
            showscale=False,
            colorscale=[[0, COLORS["quaternary"]], [1, COLORS["quaternary"]]],
            name="pointing direction",
        )

    def _covered(k):
        return go.Scatter3d(
            x=list(0.5 * _dx[: k + 1]),
            y=list(0.5 * _dy[: k + 1]),
            z=list(0.5 * _dz[: k + 1]),
            mode="markers",
            marker={"color": COLORS["primary"], "size": 4},
            opacity=0.85,
            name="directions covered",
        )

    _fig = go.Figure()
    _fig.add_trace(sphere_surface(go, color=COLORS["accent3"], opacity=0.10))  # trace 0: static
    _fig.add_trace(_needle_line(0))  # trace 1
    _fig.add_trace(_arrow(0))  # trace 2
    _fig.add_trace(_covered(0))  # trace 3

    # Frames update only the needle, its arrow, and the covered dots — never the sphere.
    _fig.frames = [
        go.Frame(data=[_needle_line(_k), _arrow(_k), _covered(_k)], traces=[1, 2, 3], name=str(_k))
        for _k in range(1, _n)
    ]

    # Lock the axis ranges and aspect so the box never rescales between frames —
    # otherwise Plotly autoranges to the growing cloud of dots and the scene appears
    # to zoom. With fixed ranges, only the needle moves.
    _bound = 0.65
    _scene = {
        **SCENE_THEME,
        "xaxis": {**SCENE_THEME["xaxis"], "range": [-_bound, _bound]},
        "yaxis": {**SCENE_THEME["yaxis"], "range": [-_bound, _bound]},
        "zaxis": {**SCENE_THEME["zaxis"], "range": [-_bound, _bound]},
        "aspectmode": "cube",
    }

    _fig.update_layout(
        **base_layout(
            title="One Needle Sweeping Every 3D Direction — its Tip Paints the Sphere",
            height=560,
            scene=_scene,
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

    > Like climbers inching up a rock face, each team plants a
    > flag a little higher — dimension 2, then 2½ — until the summit at 3.

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

    > The final pitch: Wang and Zahl showed any wild tangle of
    > needles can be quietly combed neat without losing its size — planting the flag at
    > the summit, dimension 3.

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

    > That little needle turns out to be a hidden gear driving
    > machinery all over mathematics — from how waves ripple to how secret codes hold up.

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
