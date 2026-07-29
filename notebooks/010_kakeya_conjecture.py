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

    The deltoid got the area down to $\pi/8$. **Besicovitch** showed you can do far better:
    there is no smallest area at all — a needle can point in every direction while sweeping as
    little area as you want. Two shortcuts look like they should get you there. Neither works,
    and it is worth seeing why before the real construction.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Tempting shortcut #1 — fold it out of the plane (against the rules)

    Here is a picture that makes "zero area" feel obvious — and it is **wrong** for Kakeya, so
    treat it only as a loose intuition, never a method. The needle may **never leave the table**;
    the move below lifts it into the air, which the problem forbids.

    It is still worth seeing. Pin one end of the needle to the table and tip it upward: its
    **shadow on the floor shrinks toward a single point**. Swing it over the top and lay it back
    down facing a new way, and that shadow only ever traces two thin lines — so the needle
    changes direction while its **floor footprint stays essentially zero**. The animation below
    is exactly this (illegal) maneuver.

    The real, *in-plane* trick — **overlapping translated copies** — is the one we build in a
    moment. Since
    sliding a shape within the plane never changes the directions inside it, the pieces pile onto
    one another so every direction survives while the shared area is counted only once, and
    iterating drives that area to zero. (Relatedly, in the *turning* version of the puzzle, a
    needle sliding along its own length paints no new area — a legitimate, perfectly flat "free"
    move for repositioning between tiny rotations.)
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
    _fig.update_layout(**base_layout(height=560, scene=_scene))
    _fig.update_layout(updatemenus=play_pause("▶ Fold & turn"))
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Tempting shortcut #2 — spin the *table* instead

    A natural next guess: leave the needle alone and **spin the table** underneath it. Does
    turning the plane dodge the area?

    No — and it is worth seeing why. Area is always measured **on the table**, and spinning
    the table merely relabels which way is "north." Relative to the table the needle still
    points every way and still sweeps the **whole disk**, area $\pi/4$ all over again. On the
    left we hold the needle fixed and rotate the table; on the right is that exact motion drawn
    in the table's own frame — the naive circle, no shortcut.
    """)
    return


@app.cell
def _(COLORS, base_layout, go, make_subplots, np, play_pause, style_subplot_axes):
    # Rotating the table is NOT a shortcut: area is measured on the table, so in the table's
    # own frame the fixed needle still sweeps the full disk (pi/4) -- same as plain spinning.
    _n = 36
    _ang = np.linspace(0, np.pi, _n)

    _vals = [-0.6, -0.3, 0.0, 0.3, 0.6]
    _segs = []
    for _c in _vals:
        _segs.append(((_c, -0.6), (_c, 0.6)))
        _segs.append(((-0.6, _c), (0.6, _c)))

    def _grid_trace(th, ax):
        _co, _si = np.cos(th), np.sin(th)
        _xs, _ys = [], []
        for _p0, _p1 in _segs:
            _xs += [_co * _p0[0] - _si * _p0[1], _co * _p1[0] - _si * _p1[1], None]
            _ys += [_si * _p0[0] + _co * _p0[1], _si * _p1[0] + _co * _p1[1], None]
        return go.Scatter(
            x=_xs, y=_ys, mode="lines", line={"color": "#7d8ba3", "width": 1.2},
            xaxis=ax[0], yaxis=ax[1], showlegend=False, name="table",
        )

    def _diam(k):  # the fixed lab needle, expressed in the table's (rotating) frame
        _th = -_ang[k]
        return [-0.5 * np.cos(_th), 0.5 * np.cos(_th)], [-0.5 * np.sin(_th), 0.5 * np.sin(_th)]

    def _accum_disk(k, ax):
        _xs, _ys = [], []
        for _j in range(k + 1):
            _x, _y = _diam(_j)
            _xs += [_x[0], _x[1], None]
            _ys += [_y[0], _y[1], None]
        return go.Scatter(
            x=_xs, y=_ys, mode="lines", line={"color": COLORS["primary"], "width": 1},
            opacity=0.35, xaxis=ax[0], yaxis=ax[1], showlegend=False, name="swept",
        )

    def _cur_disk(k, ax):
        _x, _y = _diam(k)
        return go.Scatter(
            x=_x, y=_y, mode="lines", line={"color": COLORS["secondary"], "width": 5},
            xaxis=ax[0], yaxis=ax[1], showlegend=False, name="needle",
        )

    _LA, _TB = ("x", "y"), ("x2", "y2")
    _fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=("Lab frame: spin the table, hold the needle", "On the table: still the whole disk (π/4)"),
    )

    _fig.add_trace(_grid_trace(0.0, _LA), row=1, col=1)  # 0: rotating table (anim)
    _fig.add_trace(  # 1: fixed lab needle (static)
        go.Scatter(
            x=[-0.5, 0.5], y=[0, 0], mode="lines", line={"color": COLORS["secondary"], "width": 6},
            xaxis="x", yaxis="y", showlegend=False, name="needle",
        ),
        row=1, col=1,
    )

    _dt = np.linspace(0, 2 * np.pi, 200)
    _fig.add_trace(  # 2: disk outline (static)
        go.Scatter(
            x=0.5 * np.cos(_dt), y=0.5 * np.sin(_dt), mode="lines", fill="toself",
            fillcolor="rgba(0, 212, 255, 0.10)", line={"color": COLORS["grid"], "width": 1.5},
            xaxis="x2", yaxis="y2", showlegend=False, name="disk",
        ),
        row=1, col=2,
    )
    _fig.add_trace(_accum_disk(0, _TB), row=1, col=2)  # 3
    _fig.add_trace(_cur_disk(0, _TB), row=1, col=2)  # 4

    _fig.frames = [
        go.Frame(data=[_grid_trace(_ang[_k], _LA), _accum_disk(_k, _TB), _cur_disk(_k, _TB)],
                 traces=[0, 3, 4], name=str(_k))
        for _k in range(1, _n)
    ]

    _fig.update_layout(
        **base_layout(title="Rotating the Table Is No Shortcut — On the Table It's Still the Full Disk", height=440)
    )
    _fig.update_xaxes(range=[-0.9, 0.9], row=1, col=1, scaleanchor="y", constrain="domain")
    _fig.update_yaxes(range=[-0.9, 0.9], row=1, col=1)
    _fig.update_xaxes(range=[-0.8, 0.8], row=1, col=2, scaleanchor="y2", constrain="domain")
    _fig.update_yaxes(range=[-0.8, 0.8], row=1, col=2)
    style_subplot_axes(_fig)
    _fig.update_layout(updatemenus=play_pause("▶ Spin table"))
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### The real trick — slice and slide

    Both shortcuts fail for the same reason: you can't dodge area by leaving the table or
    turning it. So stay in the plane and use one fact:

    > **Translating a shape does not change the set of directions it contains.**

    Take a triangle — it holds needles pointing across a whole fan of directions — slice it
    down the middle into two sub-triangles, and **slide them until they overlap**. The union
    still covers every direction in the fan, but its area is smaller, because the overlap is
    counted once instead of twice. Do this on finer and finer slices (the **Perron tree**) and
    the total area keeps dropping toward zero while the directions stay put.

    Press **▶ Slice & Slide**: the triangle is cut down the middle, then the halves slide
    together and overlap. The bold needles in each half start on their own side and *land on
    the other*, yet keep their exact angle the whole way — even as the shared footprint, and
    its area, shrink against the dotted outline of the original triangle.

    **Reading the two panels.** *Left* is the geometry: the two halves and their needles. The
    halves close together **once** — they do not wobble back and forth — and each needle just
    **slides sideways, keeping its tilt**; nothing here turns. This is not the tiny-back-and-forth
    of turning a needle; it is the area trick, and what changes is only the shared footprint.
    *Right* keeps score — it plots the **total area the halves cover together** (their union,
    the *y*-axis) against **how far you've slid them** (the *x*-axis: `s = 0` is flush into the
    whole triangle, negative is pulled apart, positive is overlapping). The moving star marks
    where the left panel is right now: as the halves overlap it slides **down** the curve, the
    area dropping from `0.5` (the full triangle, no savings) toward its minimum, while the
    needles never turn. **Area shrinks; directions stay.**

    One slice only gets you so far; iterating it (the Perron tree) is what drives the area to
    zero — you'll see that full slice-and-slide-to-nothing in the three-way comparison in Part VI.
    """)
    return


@app.cell
def _(COLORS, base_layout, go, make_subplots, np, play_pause, style_subplot_axes):
    # Show the construction *happening*: start from ONE triangle, cut it down the middle,
    # then slide the two halves together until they overlap. Each half only ever TRANSLATES
    # -- so a needle that starts on one side lands on the other side pointing the exact same
    # way (its direction never changes), yet the shared footprint (and its area) shrinks.
    _apex = np.array([0.5, 1.0])
    _whole = np.array([[0.0, 0.0], [1.0, 0.0], _apex])  # the original, un-cut triangle
    _left = np.array([[0.0, 0.0], [0.5, 0.0], _apex])  # left half-triangle
    _right = np.array([[0.5, 0.0], [1.0, 0.0], _apex])  # right half-triangle

    def _shift(tri, dx):
        out = tri.copy()
        out[:, 0] = out[:, 0] + dx
        return out

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

    _gx = np.linspace(-0.4, 1.4, 340)
    _gy = np.linspace(-0.05, 1.05, 230)
    _GX, _GY = np.meshgrid(_gx, _gy)
    _cell = (_gx[1] - _gx[0]) * (_gy[1] - _gy[0])

    def _union_area(s):
        _ins = _in_triangle(_GX, _GY, _shift(_left, s)) | _in_triangle(_GX, _GY, _shift(_right, -s))
        return float(_ins.sum() * _cell)

    # A few BOLD needles inside each half -- a small fan of directions. Each rides rigidly
    # with its half: it starts on one side and lands on the other, angle unchanged.
    _tips = np.array([0.35, 0.7, 0.95])

    def _needles(base_x, edge_x, s):
        _xs, _ys_out = [], []
        for _y in _tips:
            _xs += [base_x + s, edge_x + s, None]
            _ys_out += [0.0, _y, None]
        return _xs, _ys_out

    def _outline(tri):
        return [*list(tri[:, 0]), tri[0, 0]], [*list(tri[:, 1]), tri[0, 1]]

    def _tri_trace(tri, col, fill):
        _ox, _oy = _outline(tri)
        return go.Scatter(
            x=_ox, y=_oy, mode="lines", fill="toself", fillcolor=fill,
            line={"color": col, "width": 2}, xaxis="x", yaxis="y", showlegend=False,
        )

    def _needle_trace(xs, ys, col):
        return go.Scatter(
            x=xs, y=ys, mode="lines", line={"color": col, "width": 4},
            xaxis="x", yaxis="y", showlegend=False, name="needles",
        )

    def _label_trace(text):
        return go.Scatter(
            x=[0.5], y=[1.2], mode="text", text=[f"<b>{text}</b>"],
            textfont={"color": COLORS["text"], "size": 14}, xaxis="x", yaxis="y", showlegend=False,
        )

    def _frame_traces(s, label):
        _lx, _lyy = _needles(0.0, 0.5, s)
        _rx, _ryy = _needles(1.0, 0.5, -s)
        _area = _union_area(s)
        return [
            _tri_trace(_shift(_left, s), COLORS["primary"], "rgba(0, 212, 255, 0.28)"),
            _tri_trace(_shift(_right, -s), COLORS["secondary"], "rgba(255, 107, 107, 0.28)"),
            _needle_trace(_lx, _lyy, COLORS["accent1"]),
            _needle_trace(_rx, _ryy, COLORS["quaternary"]),
            _label_trace(label),
            go.Scatter(
                x=[s], y=[_area], mode="markers", xaxis="x2", yaxis="y2",
                marker={"color": COLORS["accent1"], "size": 14, "symbol": "star"}, name="current",
            ),
            go.Scatter(
                x=[s], y=[_area + 0.02], mode="text", text=[f"area {_area:.3f}"], xaxis="x2", yaxis="y2",
                textfont={"color": COLORS["text"], "size": 13}, showlegend=False,
            ),
        ]

    # Frame schedule: first a "slice" phase (halves sit slightly apart so you see the cut),
    # then a "slide" phase (halves close in and overlap). s < 0 = apart, s > 0 = overlapping.
    _slice_label = "1. Slice the triangle down the middle → two halves"
    _slide_label = "2. Slide the halves together → they overlap, area shrinks"
    _steps = [(_sv, _slice_label) for _sv in np.linspace(-0.09, 0.0, 6)]
    _steps += [(_sv, _slide_label) for _sv in np.linspace(0.0, 0.25, 22)[1:]]

    _curve_s = np.linspace(-0.09, 0.25, 70)
    _curve_a = [_union_area(_sv) for _sv in _curve_s]

    _fig = make_subplots(
        rows=1,
        cols=2,
        column_widths=[0.58, 0.42],
        subplot_titles=("Cut one triangle, slide the halves to overlap", "Total area covered as they overlap"),
    )

    # index 0: static dotted outline of the ORIGINAL triangle, so the shrinkage is visible.
    _wx, _wy = _outline(_whole)
    _fig.add_trace(
        go.Scatter(
            x=_wx, y=_wy, mode="lines", line={"color": COLORS["muted"], "width": 1.5, "dash": "dot"},
            xaxis="x", yaxis="y", showlegend=False, name="original triangle",
        ),
        row=1,
        col=1,
    )

    _init = _frame_traces(_steps[0][0], _steps[0][1])
    _fig.add_trace(_init[0], row=1, col=1)  # 1: left half
    _fig.add_trace(_init[1], row=1, col=1)  # 2: right half
    _fig.add_trace(_init[2], row=1, col=1)  # 3: left needles
    _fig.add_trace(_init[3], row=1, col=1)  # 4: right needles
    _fig.add_trace(_init[4], row=1, col=1)  # 5: phase label
    _fig.add_trace(  # 6: static area curve
        go.Scatter(
            x=_curve_s, y=_curve_a, mode="lines",
            line={"color": COLORS["muted"], "width": 3}, name="union area",
        ),
        row=1,
        col=2,
    )
    _fig.add_trace(_init[5], row=1, col=2)  # 7: moving star
    _fig.add_trace(_init[6], row=1, col=2)  # 8: area readout

    _fig.frames = [
        go.Frame(data=_frame_traces(_sv, _lbl), traces=[1, 2, 3, 4, 5, 7, 8], name=str(_i))
        for _i, (_sv, _lbl) in enumerate(_steps)
    ]

    _fig.update_layout(
        **base_layout(
            title="Slice-and-Slide: Overlapping the Halves Shrinks the Area",
            height=470,
        )
    )
    _fig.update_xaxes(range=[-0.4, 1.4], row=1, col=1, scaleanchor="y", constrain="domain")
    _fig.update_yaxes(range=[-0.08, 1.32], row=1, col=1)
    _fig.update_xaxes(title_text="slide s  (apart ← 0 → overlapping)", range=[-0.11, 0.27], row=1, col=2)
    _fig.update_yaxes(title_text="area", range=[min(_curve_a) - 0.03, max(_curve_a) + 0.03], row=1, col=2)
    style_subplot_axes(_fig, show_ticklabels=True)
    _fig.update_layout(updatemenus=play_pause("▶ Slice & Slide"))
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
    ### Could you actually turn a real needle this way?

    **On a flat table, yes — really.** Take an ordinary rigid needle and you can turn it through
    every direction while sweeping less area than any amount you name: a hundredth of a square
    inch, a millionth, less. It is the same back-and-forth you do reversing a car out of a tight
    spot — lots of small slides between tiny turns. Sliding a needle along its own length adds no
    area, so most of the motion is free, and the more you break it up the smaller the swept area
    gets. Area *exactly* zero is the limit of infinitely many ever-smaller slides: you can get as
    close as you want, but you cannot finish it by hand.

    **The conjecture asks something else, and it is abstract.** Kakeya, Davies, and Wang–Zahl do
    not ask what motion you make. They ask how big the set of points the needle touches is —
    measured by dimension, not by anything you can act out. Dimension is not something you do; it
    is a property of the finished set.

    Say the needle glows and scorches the table everywhere it passes. Turn it through every
    direction as tightly as you can and the scorch can end up covering no area at all — yet zoom
    in anywhere and it is still as detailed and space-filling as a solid patch, the detail growing
    under magnification just like a full 2D region. No area, but as two-dimensional as the table.
    That is the contradiction the conjecture is about.

    **In 3D it is the same thing one step up.** Now the needle points at every direction on a
    sphere; the scorch still fills no volume, but Wang and Zahl proved it stays fully
    three-dimensional. There is no neat motion to act out here — think of a laser you swing to hit
    every star in the sky, and ask how tangled the set of beams has to be. That is what the 2025
    proof pinned down.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    Here is that motion. The needle turns all the way around by a run of small moves: a tiny
    turn, then a free slide along its own length (out, then back), then the next tiny turn. Pick a
    step size — the smaller it is, the more turns and slides it takes, and the smoother the sweep.
    The faint spokes are every direction the needle has pointed so far.

    Watch what a smaller step does *not* do: the swept region stays a full **disk**, and it does
    not shrink. That is the honest catch — here every turn pivots around the same spot, so the
    needle always sweeps the whole fan no matter how fine the steps. Making the turns tiny is not
    what saves area. What saves area is sliding overlapping copies onto each other — the
    slice-and-slide trick from earlier. Turning small and shrinking the area are two different
    moves; the full construction combines them, doing each tiny turn inside one of the thin,
    overlapping triangles so the trail never fills the disk.
    """)
    return


@app.cell
def _(COLORS, base_layout, go, np):
    # The turning motion itself: swing the needle around by MANY small in-place turns, with a
    # free slide along its own length (out and back) between turns. Buttons pick the step size;
    # smaller step -> more turns and slides. Faint spokes = every direction struck so far. (This
    # is the motion; shrinking the trail's AREA is the slice-and-slide trick from Part IV.)
    _half = 0.5
    _slide = 0.6
    _theta = np.pi  # turn through 180 deg -> every direction
    _steps_deg = [30, 15, 7.5]

    def _dvec(a):
        return np.array([np.cos(a), np.sin(a)])

    def _needle(a, off):
        _d = _dvec(a)
        _c = off * _d
        return go.Scatter(x=[_c[0] - _half * _d[0], _c[0] + _half * _d[0]],
                          y=[_c[1] - _half * _d[1], _c[1] + _half * _d[1]],
                          mode="lines", line={"color": COLORS["secondary"], "width": 6}, showlegend=False)

    def _trail(angles):
        _xs, _ys = [], []
        for _a in angles:
            _d = _dvec(_a)
            _xs += [-_half * _d[0], _half * _d[0], None]
            _ys += [-_half * _d[1], _half * _d[1], None]
        return go.Scatter(x=_xs, y=_ys, mode="lines", line={"color": COLORS["accent3"], "width": 1},
                          opacity=0.45, showlegend=False)

    def _label(a, turns):
        return go.Scatter(x=[0.0], y=[0.9], mode="text",
                          text=[f"<b>pointed in {np.degrees(a):.0f}° so far · {turns} tiny turns</b>"],
                          textfont={"color": COLORS["text"], "size": 13}, showlegend=False)

    # Build one time-sequence of poses per step size: each turn = rotate in place, slide out, slide back.
    _groups = []
    for _sd in _steps_deg:
        _n = int(round(np.degrees(_theta) / _sd))
        _poses = []
        for _i in range(_n + 1):
            _a = _theta * _i / _n
            _poses.append((_a, 0.0, _i))
            if _i < _n:
                _poses.append((_a, _slide, _i))
                _poses.append((_a, 0.0, _i))
        _groups.append((_sd, _n, _poses))

    def _angles_upto(i, n):
        return [_theta * _j / n for _j in range(i + 1)]

    _fig = go.Figure()
    _a0, _off0, _i0 = _groups[0][2][0]
    _fig.add_trace(_trail(_angles_upto(0, _groups[0][1])))  # 0 trail
    _fig.add_trace(_needle(_a0, _off0))  # 1 needle
    _fig.add_trace(_label(0.0, 1))  # 2 label
    _fig.add_trace(go.Scatter(x=[0.0], y=[0.0], mode="markers",
                              marker={"color": COLORS["quaternary"], "size": 7}, showlegend=False))  # 3 pivot

    _frames, _names = [], {}
    for _gi, (_sd, _n, _poses) in enumerate(_groups):
        _keys = []
        for _k, (_a, _off, _i) in enumerate(_poses):
            _nm = f"g{_gi}_{_k}"
            _keys.append(_nm)
            _frames.append(go.Frame(
                data=[_trail(_angles_upto(_i, _n)), _needle(_a, _off), _label(_a, max(_i, 1))],
                traces=[0, 1, 2], name=_nm))
        _names[_sd] = _keys
    _fig.frames = _frames

    def _btn(sd):
        return {"label": f"▶ {sd:g}° steps", "method": "animate",
                "args": [_names[sd], {"frame": {"duration": 80, "redraw": True},
                                      "transition": {"duration": 55}, "mode": "immediate", "fromcurrent": False}]}

    _buttons = [_btn(_sd) for _sd in _steps_deg] + [
        {"label": "❚❚ Pause", "method": "animate",
         "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}]}]

    _fig.update_layout(**base_layout(title="Tiny Steps Make the Turn Smooth — but Not Smaller", height=470))
    _fig.update_xaxes(range=[-1.2, 1.2], scaleanchor="y", constrain="domain",
                      gridcolor=COLORS["grid"], zerolinecolor=COLORS["grid"], showticklabels=False)
    _fig.update_yaxes(range=[-0.8, 1.05], gridcolor=COLORS["grid"], zerolinecolor=COLORS["grid"], showticklabels=False)
    _fig.update_layout(updatemenus=[{"type": "buttons", "showactive": False, "y": 1.15, "x": 0.5,
                                     "xanchor": "center", "direction": "right", "buttons": _buttons}])
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Part V: What Does "Dimension" Even Mean?

    > Zoom into a shape and watch how fast new detail keeps showing up. Along a line it shows up
    > slowly; across a filled patch it shows up fast. **Dimension is the number that measures that
    > rate** — and it need not be a whole number.

    Take the glowing needle's scorch again. Is it "really" a thin 1D scribble, or a 2D region?
    Zooming in decides it: if the scorch keeps looking as packed with detail as a solid patch, no
    matter how far you magnify, it is two-dimensional — even when it covers no area.

    The [**box-counting dimension**](https://en.wikipedia.org/wiki/Minkowski%E2%80%93Bouligand_dimension)
    turns "how fast detail shows up" into a number. Lay a grid of tiles of side $\varepsilon$ over
    the shape, count how many tiles it touches, $N(\varepsilon)$, then shrink the tiles and see how
    fast that count climbs:

    $$\dim_{\mathrm B}(E) = \lim_{\varepsilon \to 0} \frac{\log N(\varepsilon)}{\log(1/\varepsilon)}.$$

    The closely related **Hausdorff dimension** ($\dim_{\mathrm H}(E) = \inf\{\, s \ge 0 :
    \mathcal H^{s}(E) = 0 \,\}$) is the one used in the conjecture. On the log–log plot below the
    **slope** *is* the dimension: a segment gives slope $\approx 1$, a filled triangle $\approx 2$.
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

    def _perron_needle(k, ax):
        # A unit needle pivoting about the apex, turning through the fan of directions the
        # region supports — so you can see a needle turning inside the shrinking area.
        _psi = -0.46 + 0.92 * k / (_n - 1)  # ~ ±27deg, the triangle's edge directions
        return go.Scatter(
            x=[0.0, np.sin(_psi)], y=[0.5, 0.5 - np.cos(_psi)], mode="lines",
            line={"color": COLORS["secondary"], "width": 5}, xaxis=ax[0], yaxis=ax[1], showlegend=False, name="needle",
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
    _fig.add_trace(_perron_needle(0, _P3), row=1, col=3)  # 8

    _fig.frames = [
        go.Frame(
            data=[_accum_trace(_diam, _k, _P1), _cur_trace(_diam, _k, _P1),
                  _accum_trace(_chord, _k, _P2), _cur_trace(_chord, _k, _P2),
                  _perron_trace(_k, _P3), _perron_label(_k, _P3), _perron_needle(_k, _P3)],
            traces=[1, 2, 4, 5, 6, 7, 8],
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
    ### Three ways to picture why the dimension is forced up

    You have seen what a 3D Kakeya set looks like. So why must it stay fully three-dimensional,
    however thin it appears? Every argument — the first ones and the 2025 proof alike — rests on
    one building block and then gets cleverer about using it. The three views below are that
    escalation, so read them in order; the two parts after this turn them into real theorems.

    A needle is a line segment; thicken it a little and it becomes a thin **tube**, the strip of
    space one needle covers.

    1. **Two tubes barely overlap** — the raw fact everything is built on.
    2. **Bush → hairbrush** — the simplest ways to spend that fact, and how the first bounds
       (dimension $2$, then $5/2$) were won.
    3. **Comb it sticky** — the arrangement that finally forced the dimension all the way to $3$.

    Each plays slowly; press a button and watch the needles move.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    **1 — the raw fact.** Two needles that point in different directions can only cross in a tiny
    patch. Widen the angle between the two needles below and the patch they share (highlighted)
    shrinks fast; the right panel plots that shared area. Because every pair of differently-aimed
    needles shares so little, you cannot stack a needle for every direction onto one spot — the
    tubes are pushed apart and end up covering real area. Everything below is a way of spending
    this one fact.
    """)
    return


@app.cell
def _(COLORS, base_layout, go, make_subplots, np, style_subplot_axes):
    # LENS 1 -- two needles, thickened into tubes, and the patch they share. Widening the angle
    # theta shrinks the shared patch like w^2 / sin(theta): differently-aimed needles barely
    # overlap, so a needle for every direction must spread out and cover real area.
    _w = 0.22  # needle thickness (the tube width)
    _L = 2.6  # needle length

    def _menu(label, dur):
        return [{"type": "buttons", "showactive": False, "y": 1.12, "x": 0.5, "xanchor": "center", "buttons": [
            {"label": label, "method": "animate",
             "args": [None, {"frame": {"duration": dur, "redraw": True}, "fromcurrent": True,
                             "transition": {"duration": int(dur * 0.6)}}]},
            {"label": "❚❚ Pause", "method": "animate",
             "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}]},
        ]}]

    def _dirvec(a):
        return np.array([np.cos(a), np.sin(a)]), np.array([-np.sin(a), np.cos(a)])

    def _tube(a, col, fill):
        _u, _v = _dirvec(a)
        _c = np.array([(_L / 2) * _u + (_w / 2) * _v, (_L / 2) * _u - (_w / 2) * _v,
                       -(_L / 2) * _u - (_w / 2) * _v, -(_L / 2) * _u + (_w / 2) * _v])
        return go.Scatter(x=[*_c[:, 0], _c[0, 0]], y=[*_c[:, 1], _c[0, 1]], mode="lines",
                          fill="toself", fillcolor=fill, line={"color": col, "width": 1},
                          xaxis="x", yaxis="y", showlegend=False)

    def _needle(a, col):
        _u, _ = _dirvec(a)
        return go.Scatter(x=[-(_L / 2) * _u[0], (_L / 2) * _u[0]], y=[-(_L / 2) * _u[1], (_L / 2) * _u[1]],
                          mode="lines", line={"color": col, "width": 4}, xaxis="x", yaxis="y", showlegend=False)

    def _patch(theta):
        _H = theta / 2
        _M = np.array([[-np.sin(_H), np.cos(_H)], [np.sin(_H), np.cos(_H)]])
        _pts = np.array([np.linalg.solve(_M, np.array([_s1 * _w / 2, _s2 * _w / 2]))
                         for _s1 in (1, -1) for _s2 in (1, -1)])
        _pts = _pts[np.argsort(np.arctan2(_pts[:, 1], _pts[:, 0]))]
        return go.Scatter(x=[*_pts[:, 0], _pts[0, 0]], y=[*_pts[:, 1], _pts[0, 1]], mode="lines",
                          fill="toself", fillcolor=COLORS["quaternary"],
                          line={"color": COLORS["quaternary"], "width": 1},
                          xaxis="x", yaxis="y", showlegend=False)

    def _tiplabel(a, col, txt):
        _u, _ = _dirvec(a)
        return go.Scatter(x=[(_L / 2 + 0.14) * _u[0]], y=[(_L / 2 + 0.14) * _u[1]], mode="text",
                          text=[txt], textfont={"color": col, "size": 12}, xaxis="x", yaxis="y", showlegend=False)

    def _anglelabel(theta):
        return go.Scatter(x=[0.0], y=[1.72], mode="text",
                          text=[f"<b>the two needles differ by {np.degrees(theta):.0f}°</b>"],
                          textfont={"color": COLORS["text"], "size": 14}, xaxis="x", yaxis="y", showlegend=False)

    def _share(theta):
        return _w * _w / np.sin(theta)

    def _frame(theta):
        return [
            _tube(theta / 2, COLORS["primary"], "rgba(0,212,255,0.20)"),
            _tube(-theta / 2, COLORS["secondary"], "rgba(255,107,107,0.20)"),
            _patch(theta),
            _needle(theta / 2, COLORS["primary"]),
            _needle(-theta / 2, COLORS["secondary"]),
            _tiplabel(theta / 2, COLORS["primary"], "needle A"),
            _tiplabel(-theta / 2, COLORS["secondary"], "needle B"),
            _anglelabel(theta),
            go.Scatter(x=[np.degrees(theta)], y=[_share(theta)], mode="markers",
                       marker={"color": COLORS["quaternary"], "size": 14, "symbol": "star"},
                       xaxis="x2", yaxis="y2", showlegend=False),
        ]

    _thetas = np.linspace(np.radians(16), np.radians(90), 26)
    _shares = [_share(_t) for _t in _thetas]

    _fig = make_subplots(rows=1, cols=2, column_widths=[0.55, 0.45],
        subplot_titles=("Two needles and the patch they share", "Shared patch shrinks as the angle grows"))
    _fig.add_trace(go.Scatter(x=np.degrees(_thetas), y=_shares, mode="lines",
        line={"color": COLORS["muted"], "width": 3}, showlegend=False), row=1, col=2)  # 0 static curve
    _init = _frame(_thetas[0])
    for _t in _init[:-1]:
        _fig.add_trace(_t, row=1, col=1)  # 1..8 left panel
    _fig.add_trace(_init[-1], row=1, col=2)  # 9 moving star

    _fig.frames = [go.Frame(data=_frame(_t), traces=[1, 2, 3, 4, 5, 6, 7, 8, 9], name=str(_i))
                   for _i, _t in enumerate(_thetas)]

    _fig.update_layout(**base_layout(title="Lens 1 — Two needles, different directions, tiny overlap", height=470))
    _fig.update_xaxes(range=[-1.5, 1.5], row=1, col=1, scaleanchor="y", constrain="domain")
    _fig.update_yaxes(range=[-1.5, 1.95], row=1, col=1)
    _fig.update_xaxes(title_text="angle between the needles (degrees)", range=[12, 94], row=1, col=2)
    _fig.update_yaxes(title_text="shared area", range=[0, max(_shares) * 1.1], row=1, col=2)
    style_subplot_axes(_fig, show_ticklabels=True)
    _fig.update_layout(updatemenus=_menu("▶ Widen the angle (slow)", 260))
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    **2 — the first ways to spend it.** Pin a needle at one point and turn it through every
    direction: the faint copies it leaves fill out a **bush**. By the fact above those tubes
    can't all pile up, so the bush is forced to spread — which already pins the dimension at
    $\ge 2$. Now let the needle keep turning while its pinned end slides along a line: the bushes
    stack into a **hairbrush**, and accounting for that extra spread pushed the bound up to
    $5/2$. Same fact as Lens 1, arranged to squeeze out more.
    """)
    return


@app.cell
def _(COLORS, base_layout, go, make_subplots, np, style_subplot_axes):
    # LENS 2 -- a turning needle traces out the classical shapes. Left: pivot in place, one
    # sweep -> a "bush" (Cordoba, dim >= 2). Right: pivot while the root slides along a handle,
    # several sweeps -> a "hairbrush" (Wolff 1995, dim >= 5/2). The bold needle is the current
    # position; faint copies are where it has already been.
    _K = 44
    _sweeps = 3
    _hx0, _hx1 = -1.05, 1.05

    def _menu(label, dur):
        return [{"type": "buttons", "showactive": False, "y": 1.12, "x": 0.5, "xanchor": "center", "buttons": [
            {"label": label, "method": "animate",
             "args": [None, {"frame": {"duration": dur, "redraw": True}, "fromcurrent": True}]},
            {"label": "❚❚ Pause", "method": "animate",
             "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}]},
        ]}]

    def _seg(cx, cy, a, half):
        return [cx - half * np.cos(a), cx + half * np.cos(a)], [cy - half * np.sin(a), cy + half * np.sin(a)]

    def _trail(states, half, ax, opacity):
        _xs, _ys = [], []
        for _cx, _cy, _a in states:
            _x, _y = _seg(_cx, _cy, _a, half)
            _xs += [_x[0], _x[1], None]
            _ys += [_y[0], _y[1], None]
        return go.Scatter(x=_xs, y=_ys, mode="lines", line={"color": COLORS["accent3"], "width": 1},
                          opacity=opacity, xaxis=ax[0], yaxis=ax[1], showlegend=False)

    def _cur(cx, cy, a, half, ax):
        _x, _y = _seg(cx, cy, a, half)
        return go.Scatter(x=_x, y=_y, mode="lines", line={"color": COLORS["secondary"], "width": 5},
                          xaxis=ax[0], yaxis=ax[1], showlegend=False)

    def _left_states(k):
        return [(0.0, 0.0, np.pi * _j / _K) for _j in range(k + 1)]

    def _right_states(k):
        return [(_hx0 + (_hx1 - _hx0) * _j / _K, 0.0, (np.pi * _sweeps * _j / _K) % np.pi) for _j in range(k + 1)]

    def _frame(k):
        _ls, _rs = _left_states(k), _right_states(k)
        return [
            _trail(_ls, 0.5, ("x", "y"), 0.55),
            _cur(*_ls[-1], 0.5, ("x", "y")),
            _trail(_rs, 0.42, ("x2", "y2"), 0.4),
            _cur(*_rs[-1], 0.42, ("x2", "y2")),
        ]

    _fig = make_subplots(rows=1, cols=2,
        subplot_titles=("Bush — pivot in place, face every direction  (dim ≥ 2)",
                        "Hairbrush — pivot while sliding along a handle  (dim ≥ 5/2)"))
    _init = _frame(0)
    _fig.add_trace(_init[0], row=1, col=1)  # 0 left trail
    _fig.add_trace(_init[1], row=1, col=1)  # 1 left needle
    _fig.add_trace(go.Scatter(x=[0.0], y=[0.0], mode="markers", marker={"color": COLORS["quaternary"], "size": 10},
                              xaxis="x", yaxis="y", showlegend=False), row=1, col=1)  # 2 pivot
    _fig.add_trace(_init[2], row=1, col=2)  # 3 right trail
    _fig.add_trace(_init[3], row=1, col=2)  # 4 right needle
    _fig.add_trace(go.Scatter(x=[_hx0, _hx1], y=[0.0, 0.0], mode="lines",
                              line={"color": COLORS["quaternary"], "width": 4},
                              xaxis="x2", yaxis="y2", showlegend=False), row=1, col=2)  # 5 handle

    _fig.frames = [go.Frame(data=_frame(_k), traces=[0, 1, 3, 4], name=str(_k)) for _k in range(_K + 1)]

    _fig.update_layout(**base_layout(title="Lens 2 — A turning needle builds a bush, then a hairbrush", height=460))
    _fig.update_xaxes(range=[-0.8, 0.8], row=1, col=1, scaleanchor="y", constrain="domain")
    _fig.update_yaxes(range=[-0.8, 0.8], row=1, col=1)
    _fig.update_xaxes(range=[-1.6, 1.6], row=1, col=2, scaleanchor="y2", constrain="domain")
    _fig.update_yaxes(range=[-0.75, 0.75], row=1, col=2)
    style_subplot_axes(_fig)
    _fig.update_layout(updatemenus=_menu("▶ Turn the needle (slow)", 130))
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    **3 — the arrangement that finished it.** Bush and hairbrush are blunt, and they stall short
    of $3$. The last push needs the tubes laid out so the overlap-accounting from Lens 1 is as
    tight as it can possibly be. Sliding a needle never changes the direction it points — only
    where it sits — and Wang and Zahl use that freedom to comb a messy pile of needles into a tidy
    one. Watch the needles slide from scattered positions into groups where needles pointing
    almost the same way end up almost on top of each other — a **sticky** set. Colour tracks
    direction, so the tidy state is the one where each colour gathers together. Proving the bound
    for these combed sets, then showing that *any* set can be combed this way without losing
    dimension, is the 2025 result — dimension exactly $3$.
    """)
    return


@app.cell
def _(COLORS, base_layout, go, np):
    # LENS 3 -- the sticky reduction as a physical "combing". Each needle keeps its DIRECTION
    # (angle fixed) while its centre slides from a scattered layout to a clustered one where
    # needles of nearby direction sit nearby (a Cantor-like map of angle -> position). Colour
    # encodes direction, so clustering shows up as colours gathering together.
    _N = 22
    _dirs = np.linspace(0.0, np.pi, _N, endpoint=False)
    _half = 0.26

    _gen_cx = 0.85 * np.cos(3.0 * _dirs)
    _gen_cy = 0.55 * np.sin(2.0 * _dirs)

    def _cantor(t, depth=4):
        _lo, _hi = -1.0, 1.0
        for _ in range(depth):
            _third = (_hi - _lo) / 3.0
            if t < 0.5:
                _hi, t = _lo + _third, t * 2.0
            else:
                _lo, t = _hi - _third, (t - 0.5) * 2.0
        return (_lo + _hi) / 2.0

    _stk_cx = np.array([_cantor(_d / np.pi) for _d in _dirs])

    def _menu(label, dur):
        return [{"type": "buttons", "showactive": False, "y": 1.12, "x": 0.5, "xanchor": "center", "buttons": [
            {"label": label, "method": "animate",
             "args": [None, {"frame": {"duration": dur, "redraw": True}, "fromcurrent": True,
                             "transition": {"duration": int(dur * 0.7)}}]},
            {"label": "❚❚ Pause", "method": "animate",
             "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}]},
        ]}]

    def _lerp(c1, c2, f):
        return tuple(int(round(c1[_i] + (c2[_i] - c1[_i]) * f)) for _i in range(3))

    def _col(t):
        _stops = [(0, 212, 255), (255, 230, 109), (255, 107, 107)]
        _r = _lerp(_stops[0], _stops[1], t * 2) if t < 0.5 else _lerp(_stops[1], _stops[2], (t - 0.5) * 2)
        return f"rgb{_r}"

    _cols = [_col(_i / (_N - 1)) for _i in range(_N)]

    def _needles(p):
        _out = []
        for _i in range(_N):
            _cx = (1 - p) * _gen_cx[_i] + p * _stk_cx[_i]
            _cy = (1 - p) * _gen_cy[_i]
            _a = _dirs[_i]
            _out.append(go.Scatter(
                x=[_cx - _half * np.cos(_a), _cx + _half * np.cos(_a)],
                y=[_cy - _half * np.sin(_a), _cy + _half * np.sin(_a)],
                mode="lines", line={"color": _cols[_i], "width": 4}, showlegend=False))
        return _out

    def _label(p):
        if p < 0.02:
            _t = "scattered — nearby directions land anywhere"
        elif p > 0.98:
            _t = "combed neat — nearby directions sit together (sticky)"
        else:
            _t = "sliding into place — every needle keeps its direction"
        return go.Scatter(x=[0.0], y=[1.5], mode="text", text=[f"<b>{_t}</b>"],
                          textfont={"color": COLORS["text"], "size": 14}, showlegend=False)

    _ps = [0.0] * 4 + list(np.linspace(0.0, 1.0, 22)) + [1.0] * 6

    _fig = go.Figure()
    for _tr in _needles(0.0):
        _fig.add_trace(_tr)
    _fig.add_trace(_label(0.0))

    _fig.frames = [go.Frame(data=[*_needles(_p), _label(_p)], name=str(_i)) for _i, _p in enumerate(_ps)]

    _fig.update_layout(**base_layout(title="Lens 3 — Comb any set sticky: the needles slide, directions stay", height=520))
    _fig.update_xaxes(range=[-1.35, 1.35], scaleanchor="y", constrain="domain",
                      gridcolor=COLORS["grid"], zerolinecolor=COLORS["grid"], showticklabels=False)
    _fig.update_yaxes(range=[-1.0, 1.7], gridcolor=COLORS["grid"], zerolinecolor=COLORS["grid"], showticklabels=False)
    _fig.update_layout(updatemenus=_menu("▶ Comb it neat (slow)", 220))
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
