"""
The Kakeya Conjecture: Turning a Needle in Vanishing Space

A guided-discovery walk through the Kakeya needle problem — from the 1917 tabletop
puzzle about the smallest area a needle can sweep, through the leap from a single moving
needle to a static pile of needles, to dimension as the right ruler and the 2025 proof of
the three-dimensional conjecture by Hong Wang and Joshua Zahl.
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
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## The puzzle

    Lay an infinitely thin, one-inch needle flat on a table. Turn it until it has pointed in
    **every** direction, then set it down. What is the *smallest area* the needle can sweep
    while doing so?

    The puzzle is really about waste. Moving the needle across the table increases the ground
    it covers (which we want to consume as little as possible). So it is a contest: face every
    direction, yet paint over as little table as you can.

    You might expect a tidy smallest shape with a clean number attached. There isn't one. The
    answer quietly overturns what "smallest" should even mean here, and settling it carried
    mathematicians from a 1917 tabletop puzzle to the plane, and then, a century later, to three
    dimensions, where the last piece earned a Fields Medal in 2026.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Initial spin

    This is the start of the problem. Pin the needle through its middle and spin it around like the
    hand of a clock. Round it goes, pointing every which way, and by the time it comes back it has
    swept out a full **disk**.

    Perfectly good, and perfectly wasteful: at any instant the needle is only a thin sliver, yet
    turning it paints the whole disk.

    Pinned at its middle, the needle's tips reach only half an inch out, so the swept disk has radius $r = \tfrac{1}{2}$.
    Start from the area of a circle and put that radius in:

    $$
    \begin{aligned}
    A &= \pi r^2 && \text{area of a circle of radius } r \\
      &= \pi \left(\tfrac{1}{2}\right)^2 && \text{the tips reach only } r = \tfrac{1}{2} \\
      &= \frac{\pi}{4} \\
      &\approx 0.785
    \end{aligned}
    $$
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

    def _accum(k):
        # Draw EVERY needle line so far, not just the current one -- the whole family of directions.
        _xs, _ys = [], []
        for _j in range(k + 1):
            _x, _y = _needle(_angles[_j])
            _xs += [_x[0], _x[1], None]
            _ys += [_y[0], _y[1], None]
        return go.Scatter(
            x=_xs,
            y=_ys,
            mode="lines",
            line={"color": COLORS["accent1"], "width": 1},
            opacity=0.5,
            showlegend=False,
            name="every direction so far",
        )

    _nx0, _ny0 = _needle(_angles[0])

    _fig = go.Figure()
    _fig.add_trace(  # 0: swept disk (static)
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
    _fig.add_trace(_accum(0))  # 1: every needle line drawn so far
    _fig.add_trace(  # 2: the current needle
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
    for _k in range(len(_angles)):
        _nx, _ny = _needle(_angles[_k])
        _frames.append(
            go.Frame(
                data=[_accum(_k), go.Scatter(x=_nx, y=_ny)],
                traces=[1, 2],
                name=f"{np.degrees(_angles[_k]):.0f}",
            )
        )
    _fig.frames = _frames

    _fig.update_layout(
        **base_layout(
            title="Spin it",
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
    A needle pivots about its centre and fills a disk. Every position it passes through is drawn,
    so you see the whole family of directions at once, not just one needle.

    It faces every direction, but the whole disk gets painted, area π/4.
    This is the baseline everything below has to beat.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## What if we tipped it off the table?

    A tempting shortcut: pin one end and tilt the needle up into the air.

    Its shadow on the table shrinks to almost nothing, so you swing it over the top and set it down facing a new
    way for next to no footprint.
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
            x=[0, _tx],
            y=[0, _ty],
            z=[0, _tz],
            mode="lines",
            line={"color": COLORS["secondary"], "width": 10},
            name="needle",
        )

    def _cone(k):
        _tx, _ty, _tz = _tip(k)
        return go.Cone(
            x=[_tx],
            y=[_ty],
            z=[_tz],
            u=[_tx],
            v=[_ty],
            w=[_tz],
            sizemode="absolute",
            sizeref=0.16,
            anchor="tip",
            showscale=False,
            colorscale=[[0, COLORS["quaternary"]], [1, COLORS["quaternary"]]],
            name="direction",
        )

    def _shadow_path(k):
        _sx = [np.cos(_states[_j][2]) * _states[_j][0] for _j in range(k + 1)]
        _sy = [np.cos(_states[_j][2]) * _states[_j][1] for _j in range(k + 1)]
        return go.Scatter3d(
            x=_sx,
            y=_sy,
            z=[0] * len(_sx),
            mode="lines",
            line={"color": COLORS["primary"], "width": 8},
            name="floor shadow (≈ zero area)",
        )

    def _shadow_dot(k):
        _tx, _ty, _tz = _tip(k)
        return go.Scatter3d(
            x=[_tx],
            y=[_ty],
            z=[0],
            mode="markers",
            marker={"color": COLORS["primary"], "size": 5},
            showlegend=False,
            name="shadow",
        )

    _fu = np.array([-1.1, 1.1])
    _FX, _FY = np.meshgrid(_fu, _fu)
    _fig = go.Figure()
    _fig.add_trace(  # trace 0: the floor (z = 0), static
        go.Surface(
            x=_FX,
            y=_FY,
            z=np.zeros((2, 2)),
            showscale=False,
            opacity=0.12,
            colorscale=[[0, COLORS["grid"]], [1, COLORS["grid"]]],
            hoverinfo="skip",
            showlegend=False,
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
    _fig.update_layout(**base_layout(title="Tip it up (illegal)", height=560, scene=_scene))
    _fig.update_layout(updatemenus=play_pause("▶ Fold & turn"))
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    The needle pivots up out of the plane and its floor shadow collapses toward a point.
    Direction changes for almost no footprint, but only by leaving the table.

    And that's the catch, the needle **left the table** ❌

    The whole problem lives in the plane, we need to keep the needle on the table at all time.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## What if we spin the table instead?

    Since moving the needle cost us area, what if we use the table to move instead.
    We could have either the needle stay still while the table move,
    or have the table and the needle move at the same time.

    So that the needle either point in all direction of the table without moving in the plan,
    or it points in all direction of the plan without moving from the table.
    """)
    return


@app.cell
def _(COLORS, base_layout, go, make_subplots, np, play_pause, style_subplot_axes):
    _R = 0.5
    _phis = np.concatenate([np.zeros(3), np.linspace(0.0, np.pi, 40), np.full(4, np.pi)])

    _vals = [-0.6, -0.3, 0.0, 0.3, 0.6]
    _segs = []
    for _c in _vals:
        _segs.append(((_c, -0.6), (_c, 0.6)))
        _segs.append(((-0.6, _c), (0.6, _c)))

    def _grid_trace(th, xa, ya):
        _co, _si = np.cos(th), np.sin(th)
        _xs, _ys = [], []
        for _p0, _p1 in _segs:
            _xs += [_co * _p0[0] - _si * _p0[1], _co * _p1[0] - _si * _p1[1], None]
            _ys += [_si * _p0[0] + _co * _p0[1], _si * _p1[0] + _co * _p1[1], None]
        return go.Scatter(
            x=_xs,
            y=_ys,
            mode="lines",
            line={"color": "#7d8ba3", "width": 1.2},
            xaxis=xa,
            yaxis=ya,
            showlegend=False,
            name="table",
        )

    def _needle_trace(th, xa, ya):
        # a diameter through the pivot, pointing at lab-angle th
        _co, _si = np.cos(th), np.sin(th)
        return go.Scatter(
            x=[-_R * _co, _R * _co],
            y=[-_R * _si, _R * _si],
            mode="lines",
            line={"color": COLORS["secondary"], "width": 6},
            xaxis=xa,
            yaxis=ya,
            showlegend=False,
            name="needle",
        )

    def _wedge(a0, a1):
        # filled sector of the radius-_R disk between lab-angles a0 and a1, apex at the pivot
        _a = np.linspace(a0, a1, 40)
        return [0.0, *(_R * np.cos(_a)), 0.0], [0.0, *(_R * np.sin(_a)), 0.0]

    def _painted(phi, xa, ya):
        # table-material touched so far: two opposite wedges of angular width phi, since both ends
        # of the diameter paint at once. Full disk at phi = pi.
        _x, _y = [], []
        for _base in (0.0, np.pi):
            _wx, _wy = _wedge(_base, _base + phi)
            _x += [*_wx, None]
            _y += [*_wy, None]
        return go.Scatter(
            x=_x,
            y=_y,
            mode="lines",
            fill="toself",
            fillcolor="rgba(0, 212, 255, 0.16)",
            line={"color": COLORS["primary"], "width": 1},
            xaxis=xa,
            yaxis=ya,
            showlegend=False,
            name="painted so far",
        )

    def _readout(area, xa, ya):
        return go.Scatter(
            x=[0.0],
            y=[0.82],
            mode="text",
            text=[f"painted area ≈ {area:.3f}"],
            textfont={"color": COLORS["highlight"], "size": 14},
            xaxis=xa,
            yaxis=ya,
            showlegend=False,
        )

    _fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=("Needle glued to the table", "Needle held in the position"),
    )
    # left panel (glued): grid and needle rotate together, nothing gets painted
    _fig.add_trace(_grid_trace(_phis[0], "x", "y"), row=1, col=1)  # 0 anim
    _fig.add_trace(_needle_trace(_phis[0], "x", "y"), row=1, col=1)  # 1 anim (turns with table)
    _fig.add_trace(_readout(0.0, "x", "y"), row=1, col=1)  # 2 anim (stays 0)
    # right panel (held): grid turns, needle fixed, table-material paints the disk
    _fig.add_trace(_grid_trace(_phis[0], "x2", "y2"), row=1, col=2)  # 3 anim
    _fig.add_trace(_painted(_phis[0], "x2", "y2"), row=1, col=2)  # 4 anim
    _fig.add_trace(_needle_trace(0.0, "x2", "y2"), row=1, col=2)  # 5 static (fixed diameter)
    _fig.add_trace(_readout(0.0, "x2", "y2"), row=1, col=2)  # 6 anim

    _fig.frames = [
        go.Frame(
            data=[
                _grid_trace(_p, "x", "y"),
                _needle_trace(_p, "x", "y"),
                _readout(0.0, "x", "y"),
                _grid_trace(_p, "x2", "y2"),
                _painted(_p, "x2", "y2"),
                _readout(0.25 * _p, "x2", "y2"),  # fraction phi/pi of the disk area pi * _R**2
            ],
            traces=[0, 1, 2, 3, 4, 6],
            name=str(_k),
        )
        for _k, _p in enumerate(_phis)
    ]

    _fig.update_layout(**base_layout(title="Spin the table", height=470))
    for _c in (1, 2):
        _fig.update_xaxes(
            range=[-0.9, 0.9],
            scaleanchor="y" if _c == 1 else "y2",
            constrain="domain",
            showticklabels=False,
            row=1,
            col=_c,
        )
        _fig.update_yaxes(range=[-0.9, 0.95], showticklabels=False, row=1, col=_c)
    style_subplot_axes(_fig)
    _fig.update_layout(updatemenus=play_pause("▶ Spin the table"))
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    Two ways to spin the table, both watched from the room.
    - On the **left** the needle is _glued_ to the table and rides along with it: it always lies on the same sliver of table, area stays zero.
      - The needle never turns *relative to the table*.
      - While the area is zero, it only ever point in one direction and thus fails to solve the problem.
    - On the **right** the needle is held still in the room while the table turns beneath it: watch the table-points it passes over fill in.
      - Relative to the table, it's the needle that's spinning. So no area gained here.

    We considered different moving options to reduce the area, but none worked so far.
    Let's dive deeper and explore what move are remaining for us to try.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Sliding is free

    Here is something legal that costs nothing: **slide the needle along its
    own length.** It just retraces the line it already sits on, so it paints no new area, a free
    repositioning.

    So don't only pivot, *slide as you turn*. Ride the needle around the inside of a curved shape
    (a **deltoid**) and it faces every direction using only $\pi/8 \approx 0.393$, half the disk.

    $$
    \begin{aligned}
    A &= \frac{\pi}{8} L^2 && \text{deltoid area for a needle of length } L \\
      &= \frac{\pi}{8} && \text{a unit needle, } L = 1 \\
      &\approx 0.393
    \end{aligned}
    $$
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

    def _accum(k):
        # Draw EVERY tangent-chord needle so far -- the whole family of directions filling the deltoid.
        _xs, _ys = [], []
        for _j in range(k + 1):
            _x, _y = _tangent_chord(_angles[_j])
            _xs += [_x[0], _x[1], None]
            _ys += [_y[0], _y[1], None]
        return go.Scatter(
            x=_xs,
            y=_ys,
            mode="lines",
            line={"color": COLORS["accent1"], "width": 1},
            opacity=0.5,
            showlegend=False,
            name="every direction so far",
        )

    _nx0, _ny0 = _tangent_chord(_angles[0])

    _fig = go.Figure()
    _fig.add_trace(  # 0: deltoid outline (static)
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
    _fig.add_trace(_accum(0))  # 1: every tangent-chord needle so far
    _fig.add_trace(  # 2: the current needle
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
    for _k in range(len(_angles)):
        _nx, _ny = _tangent_chord(_angles[_k])
        _frames.append(
            go.Frame(
                data=[_accum(_k), go.Scatter(x=_nx, y=_ny)],
                traces=[1, 2],
                name=f"{np.degrees(_angles[_k]):.0f}",
            )
        )
    _fig.frames = _frames

    _fig.update_layout(
        **base_layout(
            title="Deltoid",
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
    The needle stays a tangent chord of the deltoid, turning through every direction while
    sliding along its own length. Every position is drawn, so you see the whole family of
    directions filling the deltoid, not just one needle. Each slide reuses table it has already
    covered instead of painting fresh, and that reuse is the saving: the same directions as the
    disk, in half the area.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Slice and slide

    **The second move, and it is the first one scaled up.** Sliding let a single needle reuse its
    *own* track, and that alone halved the disk. Now let *different* directions share a track too.

    Think of a **triangle** as one needle pivoting about its top tip: swung between the two sides
    it points across a whole fan of directions, and at every angle it is the **same length**. So
    one triangle already holds that fan of needles. Cut that **triangular patch of table** down
    the middle (the patch, not the needle) into two thinner triangles, and **slide them until they
    overlap.** Each half carries its fan along unchanged, so together they still cover the whole
    fan, but the overlap is table counted once instead of twice, so the footprint shrinks.
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

    # A triangle stands for ONE needle pivoting about its top tip (the apex): swung through the
    # fan between the two sides, it points across a range of directions, EVERY position the same
    # length. So the bold needles below all share one length _L and only differ in angle; each
    # rides rigidly with its half as it slides, so its length and direction never change.
    _apex_y = 1.0
    _L = 0.95  # every drawn needle has this same length
    # The directions each half covers: from the apex to its two base corners.
    _left_angs = np.linspace(np.arctan2(-1.0, -0.5), np.arctan2(-1.0, 0.0), 3)
    _right_angs = np.linspace(np.arctan2(-1.0, 0.0), np.arctan2(-1.0, 0.5), 3)

    def _needles(apex_x, angs):
        _xs, _ys_out = [], []
        for _a in angs:
            _xs += [apex_x, apex_x + _L * np.cos(_a), None]
            _ys_out += [_apex_y, _apex_y + _L * np.sin(_a), None]
        return _xs, _ys_out

    def _outline(tri):
        return [*list(tri[:, 0]), tri[0, 0]], [*list(tri[:, 1]), tri[0, 1]]

    def _tri_trace(tri, col, fill):
        _ox, _oy = _outline(tri)
        return go.Scatter(
            x=_ox,
            y=_oy,
            mode="lines",
            fill="toself",
            fillcolor=fill,
            line={"color": col, "width": 2},
            xaxis="x",
            yaxis="y",
            showlegend=False,
        )

    def _needle_trace(xs, ys, col):
        return go.Scatter(
            x=xs,
            y=ys,
            mode="lines",
            line={"color": col, "width": 4},
            xaxis="x",
            yaxis="y",
            showlegend=False,
            name="needles",
        )

    def _arrows(apex_x, angs, col):
        # Arrowheads at each needle tip, angled along the needle so its DIRECTION is visible and
        # stays fixed as the half slides. Marker angle is clockwise from "up", so 90 - heading.
        _tx = [apex_x + _L * np.cos(_a) for _a in angs]
        _ty = [_apex_y + _L * np.sin(_a) for _a in angs]
        _headings = np.degrees(angs)
        return go.Scatter(
            x=_tx,
            y=_ty,
            mode="markers",
            marker={"symbol": "arrow", "size": 13, "angle": list(90.0 - _headings), "angleref": "up", "color": col},
            xaxis="x",
            yaxis="y",
            showlegend=False,
            name="direction",
        )

    def _label_trace(text):
        return go.Scatter(
            x=[0.5],
            y=[1.2],
            mode="text",
            text=[f"<b>{text}</b>"],
            textfont={"color": COLORS["text"], "size": 14},
            xaxis="x",
            yaxis="y",
            showlegend=False,
        )

    def _frame_traces(s, label):
        _lx, _lyy = _needles(0.5 + s, _left_angs)
        _rx, _ryy = _needles(0.5 - s, _right_angs)
        _area = _union_area(s)
        return [
            _tri_trace(_shift(_left, s), COLORS["primary"], "rgba(0, 212, 255, 0.28)"),
            _tri_trace(_shift(_right, -s), COLORS["secondary"], "rgba(255, 107, 107, 0.28)"),
            _needle_trace(_lx, _lyy, COLORS["accent1"]),
            _needle_trace(_rx, _ryy, COLORS["quaternary"]),
            _arrows(0.5 + s, _left_angs, COLORS["accent1"]),
            _arrows(0.5 - s, _right_angs, COLORS["quaternary"]),
            _label_trace(label),
            go.Scatter(
                x=[s],
                y=[_area],
                mode="markers",
                xaxis="x2",
                yaxis="y2",
                marker={"color": COLORS["accent1"], "size": 14, "symbol": "star"},
                name="current",
            ),
            go.Scatter(
                x=[s],
                y=[_area + 0.02],
                mode="text",
                text=[f"area {_area:.3f}"],
                xaxis="x2",
                yaxis="y2",
                textfont={"color": COLORS["text"], "size": 13},
                showlegend=False,
            ),
        ]

    # Frame schedule: first a "slice" phase (halves sit slightly apart so you see the cut),
    # then a "slide" phase (halves close in and overlap). s < 0 = apart, s > 0 = overlapping.
    _slice_label = "1. Slice"
    _slide_label = "2. Slide & overlap"
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
            x=_wx,
            y=_wy,
            mode="lines",
            line={"color": COLORS["muted"], "width": 1.5, "dash": "dot"},
            xaxis="x",
            yaxis="y",
            showlegend=False,
            name="original triangle",
        ),
        row=1,
        col=1,
    )

    _init = _frame_traces(_steps[0][0], _steps[0][1])
    _fig.add_trace(_init[0], row=1, col=1)  # 1: left half
    _fig.add_trace(_init[1], row=1, col=1)  # 2: right half
    _fig.add_trace(_init[2], row=1, col=1)  # 3: left needles
    _fig.add_trace(_init[3], row=1, col=1)  # 4: right needles
    _fig.add_trace(_init[4], row=1, col=1)  # 5: left direction arrows
    _fig.add_trace(_init[5], row=1, col=1)  # 6: right direction arrows
    _fig.add_trace(_init[6], row=1, col=1)  # 7: phase label
    _fig.add_trace(  # 8: static area curve
        go.Scatter(
            x=_curve_s,
            y=_curve_a,
            mode="lines",
            line={"color": COLORS["muted"], "width": 3},
            name="union area",
        ),
        row=1,
        col=2,
    )
    _fig.add_trace(_init[7], row=1, col=2)  # 9: moving star
    _fig.add_trace(_init[8], row=1, col=2)  # 10: area readout

    _fig.frames = [
        go.Frame(data=_frame_traces(_sv, _lbl), traces=[1, 2, 3, 4, 5, 6, 7, 9, 10], name=str(_i))
        for _i, (_sv, _lbl) in enumerate(_steps)
    ]

    _fig.update_layout(
        **base_layout(
            title="Slice and slide",
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
    The animation cuts the triangle in half and slides the halves over each other. Watch the
    **arrows**: they mark each needle's direction, and they never budge as the halves move. So
    every direction is still there at the end, yet the area readout on the right keeps dropping.
    The reason is the overlap: where the two halves cover the same patch of table, that patch is
    counted once but reused by needles pointing several different ways at once. Shared table is
    saved table.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    **The two moves are one idea.** Sliding lets a needle reuse its own track; slicing lets
    different directions share a track. Both work for the same reason: **moving a piece never
    changes the directions inside it**, so the footprint can shrink while every direction stays put
    (no leaving the plane, no spinning the world). And it compounds: slice each piece again and
    slide again (the **Perron tree**), and the area keeps falling.

    We have shrunk the *table* the needle would need. But we did it by sliding patches around, not
    by turning a needle. The original 1917 question was about an actual needle sweeping through
    every direction. Does a real needle fit inside this shrunken region, and can it turn all the
    way around in there?
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    It does. Here is a real needle actually **turning** through every direction inside that
    shrinking region. Iterate slice-and-slide into a full **Perron tree**, and thread thin
    **corridors** (Pál's *joins*) between the pieces so the needle can cross from one to the next:
    it makes each small turn inside a piece, slides down a corridor, and turns again. It covers
    every direction while sweeping only a tiny area, smaller with every extra slice. This is the
    original 1917 question answered, a real needle turning in almost no area.
    """)
    return


@app.cell
def _(COLORS, base_layout, go, np):
    # The needle turns inside a Perron tree: it swings through a small range of directions in each
    # thin, overlapping piece, sliding along its own length (free) to the next. The faint fans are
    # the pieces (radius = needle length) -- exactly what the needle sweeps; they overlap, so their
    # union is smaller than one plain fan, and smaller still with more slices. Fit and shrink were
    # checked numerically. One fan spans < 180 deg; a full half-turn stitches several together.
    _H, _B, _alpha, _L0 = 1.0, 1.7, 0.34, 0.9
    _apex0 = np.array([0.0, _H])

    def _ang(a, p):
        return np.arctan2(p[1] - a[1], p[0] - a[0])

    def _build(level):
        _leaves = [
            dict(
                apex=_apex0.copy(),
                bL=np.array([-_B, 0.0]),
                bR=np.array([_B, 0.0]),
                aL=_ang(_apex0, np.array([-_B, 0.0])),
                aR=_ang(_apex0, np.array([_B, 0.0])),
            )
        ]
        for _ in range(level):
            _nxt = []
            for _lf in _leaves:
                _a, _bL, _bR = _lf["apex"], _lf["bL"], _lf["bR"]
                _m = (_bL + _bR) / 2.0
                _s = np.array([_alpha * (_bR[0] - _m[0]), 0.0])
                _nxt.append(dict(apex=_a + _s, bL=_bL + _s, bR=_m + _s, aL=_ang(_a, _bL), aR=_ang(_a, _m)))
                _nxt.append(dict(apex=_a - _s, bL=_m - _s, bR=_bR - _s, aL=_ang(_a, _m), aR=_ang(_a, _bR)))
            _leaves = _nxt
        _leaves.sort(key=lambda lf: lf["aL"] + lf["aR"])
        return _leaves

    _gx = np.linspace(-1.2, 1.2, 240)
    _gy = np.linspace(-0.05, 1.05, 130)
    _GX, _GY = np.meshgrid(_gx, _gy)
    _cellA = (_gx[1] - _gx[0]) * (_gy[1] - _gy[0])

    def _swept_area(leaves):
        _mask = np.zeros(_GX.shape, bool)
        for _lf in leaves:
            _dx, _dy = _GX - _lf["apex"][0], _GY - _lf["apex"][1]
            _lo, _hi = min(_lf["aL"], _lf["aR"]), max(_lf["aL"], _lf["aR"])
            _mask |= (
                (np.hypot(_dx, _dy) <= _L0)
                & (np.arctan2(_dy, _dx) >= _lo - 1e-9)
                & (np.arctan2(_dy, _dx) <= _hi + 1e-9)
            )
        return float(_mask.sum() * _cellA)

    def _u(t):
        return np.array([np.cos(t), np.sin(t)])

    def _sectors(leaves):
        _xs, _ys = [], []
        for _lf in leaves:
            _arc = np.linspace(_lf["aL"], _lf["aR"], 16)
            _xs += [_lf["apex"][0], *(_lf["apex"][0] + _L0 * np.cos(_arc)), _lf["apex"][0], None]
            _ys += [_lf["apex"][1], *(_lf["apex"][1] + _L0 * np.sin(_arc)), _lf["apex"][1], None]
        return go.Scatter(
            x=_xs,
            y=_ys,
            mode="lines",
            fill="toself",
            fillcolor="rgba(149,225,211,0.13)",
            line={"color": COLORS["accent1"], "width": 0.8},
            opacity=0.85,
            showlegend=False,
        )

    def _needle(apex, t):
        _e = apex + _L0 * _u(t)
        return go.Scatter(
            x=[apex[0], _e[0]],
            y=[apex[1], _e[1]],
            mode="lines",
            line={"color": COLORS["secondary"], "width": 6},
            showlegend=False,
        )

    def _label(level, area):
        return go.Scatter(
            x=[0.0],
            y=[1.3],
            mode="text",
            text=[f"<b>{2**level} slices · area ≈ {area:.2f}</b>"],
            textfont={"color": COLORS["text"], "size": 13},
            showlegend=False,
        )

    def _poses_for(level):
        _leaves = _build(level)
        _seq = []
        for _li, _lf in enumerate(_leaves):
            for _t in np.linspace(_lf["aL"], _lf["aR"], 7):
                _seq.append((_lf["apex"], _t))
            if _li < len(_leaves) - 1:
                _nx = _leaves[_li + 1]
                for _f in np.linspace(0.0, 1.0, 3)[1:]:
                    _seq.append((_lf["apex"] + _f * (_nx["apex"] - _lf["apex"]), _lf["aR"]))
        return _leaves, _seq

    _levels = [1, 2, 3]
    _data = {_L: _poses_for(_L) for _L in _levels}
    _areas = {_L: _swept_area(_data[_L][0]) for _L in _levels}

    _fig = go.Figure()
    _lv1, _seq1 = _data[1]
    _fig.add_trace(_sectors(_lv1))  # 0 the overlapping pieces (what the needle sweeps)
    _fig.add_trace(_needle(*_seq1[0]))  # 1 current needle
    _fig.add_trace(_label(1, _areas[1]))  # 2 label

    _frames, _names = [], {}
    for _L in _levels:
        _leaves, _seq = _data[_L]
        _keys = []
        for _k in range(len(_seq)):
            _nm = f"L{_L}_{_k}"
            _keys.append(_nm)
            _frames.append(
                go.Frame(
                    data=[_sectors(_leaves), _needle(*_seq[_k]), _label(_L, _areas[_L])], traces=[0, 1, 2], name=_nm
                )
            )
        _names[_L] = _keys
    _fig.frames = _frames

    def _btn(level):
        return {
            "label": f"▶ {2**level} slices",
            "method": "animate",
            "args": [
                _names[level],
                {
                    "frame": {"duration": 85, "redraw": True},
                    "transition": {"duration": 0},
                    "mode": "immediate",
                    "fromcurrent": False,
                },
            ],
        }

    _buttons = [_btn(_L) for _L in _levels] + [
        {
            "label": "❚❚ Pause",
            "method": "animate",
            "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}],
        }
    ]

    _fig.update_layout(**base_layout(title="A real needle, turning", height=470))
    _fig.update_xaxes(
        range=[-1.15, 1.15],
        scaleanchor="y",
        constrain="domain",
        gridcolor=COLORS["grid"],
        zerolinecolor=COLORS["grid"],
        showticklabels=False,
    )
    _fig.update_yaxes(range=[-0.1, 1.42], gridcolor=COLORS["grid"], zerolinecolor=COLORS["grid"], showticklabels=False)
    _fig.update_layout(
        updatemenus=[
            {
                "type": "buttons",
                "showactive": False,
                "y": 1.14,
                "x": 0.5,
                "xanchor": "center",
                "direction": "right",
                "buttons": _buttons,
            }
        ]
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    The needle makes each small turn inside one thin fan, then slides along its own length to the
    next. The fans overlap, so the region it needs is far smaller than a plain spin, and the area
    readout drops with every extra slice. Each added slice buys a smaller region, and nothing in
    the construction says where to stop. So how small can it get?
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## …but it never quite hits zero

    As small as you like: a millionth of the disk, a billionth, smaller. And yet **never exactly
    zero**, because a sliver of area always stays behind, no matter how fine the slices.

    Here is why. To *turn*, a needle moves
    continuously: its 31° pose has to sit right next to its 30° pose, so it must sweep every
    position in between, and that swept-through ground is exactly the sliver that never vanishes.

    > **Turning forces the needle through every position in between, and sweeping them costs area.
    > Motion itself is what pins the area above zero.**

    Which points straight at the only way out: stop moving.
    """)
    return


@app.cell
def _(COLORS, base_layout, go, np, perron_stages, play_pause, union_area):
    # Area, never zero: build a Perron tree and, across frames of increasing subdivision, plot
    # the tree of triangles with a running (rasterised) area readout. Slicing shrinks the area
    # toward -- but never onto -- zero, because moving a real needle always leaves a sliver.
    _pbase = [np.array([[-0.55, -0.5], [0.55, -0.5], [0.0, 0.5]])]
    _stages = perron_stages(_pbase, levels=5)

    _gx = np.linspace(-0.9, 0.9, 220)
    _gy = np.linspace(-0.7, 0.7, 200)
    _GX, _GY = np.meshgrid(_gx, _gy)

    def _tree_trace(tris):
        _x, _y = [], []
        for _t in tris:
            _x += [_t[0, 0], _t[1, 0], _t[2, 0], _t[0, 0], None]
            _y += [_t[0, 1], _t[1, 1], _t[2, 1], _t[0, 1], None]
        return go.Scatter(
            x=_x,
            y=_y,
            mode="lines",
            fill="toself",
            fillcolor="rgba(149, 225, 211, 0.22)",
            line={"color": COLORS["accent1"], "width": 1},
            showlegend=False,
            name="Perron tree",
        )

    def _readout(tris, level):
        _a = union_area(tris, _GX, _GY)
        return go.Scatter(
            x=[0.0],
            y=[0.62],
            mode="text",
            text=[f"<b>level {level} · area ≈ {_a:.3f}</b>"],
            textfont={"color": COLORS["highlight"], "size": 15},
            showlegend=False,
        )

    _tris0, _lvl0 = _stages[0]
    _fig = go.Figure()
    _fig.add_trace(_tree_trace(_tris0))  # 0
    _fig.add_trace(_readout(_tris0, _lvl0))  # 1

    _fig.frames = [
        go.Frame(data=[_tree_trace(_tris), _readout(_tris, _lvl)], traces=[0, 1], name=str(_i))
        for _i, (_tris, _lvl) in enumerate(_stages)
    ]

    _fig.update_layout(**base_layout(title="Area, never zero", height=470))
    _fig.update_xaxes(
        range=[-0.9, 0.9],
        scaleanchor="y",
        constrain="domain",
        gridcolor=COLORS["grid"],
        zerolinecolor=COLORS["grid"],
        showticklabels=False,
    )
    _fig.update_yaxes(range=[-0.7, 0.75], gridcolor=COLORS["grid"], zerolinecolor=COLORS["grid"], showticklabels=False)
    _fig.update_layout(updatemenus=play_pause("▶ Slice finer"))
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    As the slice count climbs, the running area readout falls and falls but never reaches 0.
    The last sliver is exactly what the next idea removes.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Stop moving the needle at all

    Here is the move: **stop turning one needle.** Instead, put down a
    *separate* needle for each direction, all at once, and look at the whole collection together.
    A needle at 0°, another at 1°, another at 89°, and so on, like a boxful of matchsticks tossed
    on the table so that between them they point every possible way. (A true such set needs one for
    *every* direction, a whole continuum, but the boxful is the picture to hold.)
    """)
    return


@app.cell
def _(COLORS, base_layout, go, np):
    # A STILL schema (no animation): a handful of needles, one per direction, laid out separately.
    # This is "the form" -- a collection of needles, one per angle -- that the next animation then
    # slides together. Just the picture; nothing moves here.
    _angs = [0, 30, 60, 90, 120, 150]
    _cols = [
        COLORS["primary"],
        COLORS["secondary"],
        COLORS["accent1"],
        COLORS["accent3"],
        COLORS["quaternary"],
        COLORS["tertiary"],
    ]
    _centres = [(-1.4, 0.55), (0.0, 0.55), (1.4, 0.55), (-1.4, -0.75), (0.0, -0.75), (1.4, -0.75)]
    _fig = go.Figure()
    for _adeg, _ctr, _col in zip(_angs, _centres, _cols):
        _t = np.radians(_adeg)
        _cx, _cy = _ctr
        _fig.add_trace(
            go.Scatter(
                x=[_cx - 0.45 * np.cos(_t), _cx + 0.45 * np.cos(_t)],
                y=[_cy - 0.45 * np.sin(_t), _cy + 0.45 * np.sin(_t)],
                mode="lines",
                line={"color": _col, "width": 6},
                showlegend=False,
            )
        )
        _fig.add_trace(
            go.Scatter(
                x=[_cx],
                y=[_cy - 0.62],
                mode="text",
                text=[f"{_adeg}°"],
                textfont={"color": COLORS["text_secondary"], "size": 15},
                showlegend=False,
            )
        )
    _fig.update_layout(**base_layout(title="One needle per direction", height=360))
    _fig.update_xaxes(
        range=[-2.2, 2.2],
        scaleanchor="y",
        constrain="domain",
        showgrid=False,
        zeroline=False,
        showticklabels=False,
    )
    _fig.update_yaxes(range=[-1.6, 1.15], showgrid=False, zeroline=False, showticklabels=False)
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    Six needles, six directions, just lying there. Nothing is turning, and nothing is even a
    single object anymore. So the old knot, *how can it change direction without moving?*, has
    nothing to grab: there is no "it" to change. There is simply a needle at 30° and, separately,
    a needle at 31°.

    Now bring back the free slide, with no motion to pay for. Each needle is one-dimensional, a
    full inch long but with no width at all, and sliding it never changes the way it points. Slide
    them all to overlap as much as possible: each stays a full inch long, so the collection still
    spans about a needle's length, but the shared ground is counted once, so the footprint shrinks.
    With no continuous path to keep, nothing stops it going all the way to zero, while a needle
    still points in every direction. Reaching *exactly* zero, not merely as-small-as-you-like, is
    what turns this from a measuring contest into a much stranger question.
    """)
    return


@app.cell
def _(COLORS, base_layout, go, np):
    # "Overlap every direction": one needle per direction, laid down at once. Each needle keeps its
    # ANGLE throughout; only its CENTRE moves. Centres start spread on a ring of radius R and slide
    # to R ~ 0, so the needles pile onto each other. A running area readout (rasterised
    # point-in-rectangle mask) shows the union footprint collapsing as the overlaps -- counted once
    # -- take over. Many frames + slow playback + a phase label so the collapse is easy to follow.
    _N = 48
    _dirs = np.linspace(0.0, np.pi, _N, endpoint=False)
    _ux, _uy = np.cos(_dirs), np.sin(_dirs)  # needle axis (direction), fixed per needle
    _w = 0.05  # needle thickness
    _half = 0.5  # half length -> unit needle

    # Spread the centres around a full ring so they start well separated.
    _cang = 2.0 * _dirs
    _cdx, _cdy = np.cos(_cang), np.sin(_cang)

    _gx = np.linspace(-1.8, 1.8, 240)
    _gy = np.linspace(-1.8, 1.8, 240)
    _GX, _GY = np.meshgrid(_gx, _gy)
    _cellA = (_gx[1] - _gx[0]) * (_gy[1] - _gy[0])

    def _union_area(R):
        _mask = np.zeros(_GX.shape, dtype=bool)
        for _i in range(_N):
            _cx, _cy = R * _cdx[_i], R * _cdy[_i]
            _dx, _dy = _GX - _cx, _GY - _cy
            _along = _dx * _ux[_i] + _dy * _uy[_i]
            _perp = -_dx * _uy[_i] + _dy * _ux[_i]
            _mask |= (np.abs(_along) <= _half) & (np.abs(_perp) <= _w / 2)
        return float(_mask.sum() * _cellA)

    def _needle_trace(R):
        _xs, _ys = [], []
        for _i in range(_N):
            _cx, _cy = R * _cdx[_i], R * _cdy[_i]
            _xs += [_cx - _half * _ux[_i], _cx + _half * _ux[_i], None]
            _ys += [_cy - _half * _uy[_i], _cy + _half * _uy[_i], None]
        return go.Scatter(
            x=_xs,
            y=_ys,
            mode="lines",
            line={"color": COLORS["primary"], "width": 2},
            opacity=0.75,
            showlegend=False,
            name="needles",
        )

    def _readout(R):
        return go.Scatter(
            x=[0.0],
            y=[1.62],
            mode="text",
            text=[f"footprint area ≈ {_union_area(R):.2f}"],
            textfont={"color": COLORS["highlight"], "size": 16},
            showlegend=False,
        )

    # Hold at the start and end, and step R slowly in between, so the collapse is legible.
    _Rs = np.concatenate([np.full(3, 1.15), np.linspace(1.15, 0.05, 34), np.full(4, 0.05)])

    _fig = go.Figure()
    _fig.add_trace(_needle_trace(_Rs[0]))  # 0
    _fig.add_trace(_readout(_Rs[0]))  # 1

    _fig.frames = [
        go.Frame(data=[_needle_trace(_R), _readout(_R)], traces=[0, 1], name=str(_i)) for _i, _R in enumerate(_Rs)
    ]

    _fig.update_layout(**base_layout(title="Overlap every direction", height=560))
    _fig.update_xaxes(
        range=[-1.8, 1.8],
        scaleanchor="y",
        constrain="domain",
        gridcolor=COLORS["grid"],
        zerolinecolor=COLORS["grid"],
        showticklabels=False,
    )
    _fig.update_yaxes(range=[-1.8, 1.85], gridcolor=COLORS["grid"], zerolinecolor=COLORS["grid"], showticklabels=False)
    _fig.update_layout(
        updatemenus=[
            {
                "type": "buttons",
                "showactive": False,
                "y": 1.1,
                "x": 0.5,
                "xanchor": "center",
                "buttons": [
                    {
                        "label": "▶ Slide them together",
                        "method": "animate",
                        "args": [
                            None,
                            {
                                "frame": {"duration": 200, "redraw": True},
                                "fromcurrent": True,
                                "transition": {"duration": 150},
                            },
                        ],
                    },
                    {
                        "label": "❚❚ Pause",
                        "method": "animate",
                        "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}],
                    },
                ],
            }
        ]
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    One needle per direction, laid down at once, then slid to overlap as much as possible. Every
    needle keeps its direction, so all directions remain. The set still reaches about as far as a
    single needle, but its overlaps are counted once, so the footprint keeps dropping as they pile
    up (the readout tracks it), reaching exactly zero in the continuum limit of one needle for
    every direction:

    $$
    \begin{aligned}
    &K \subset \mathbb{R}^2 && \text{a set in the plane} \\
    &K \text{ contains a unit segment in every direction} && \text{a Besicovitch set} \\
    &|K| = 0 && \text{yet zero area}
    \end{aligned}
    $$

    This object has a name. A set that contains a unit segment in every direction is a
    **Besicovitch set** (also called a **Kakeya set**), and we have just built one with zero area.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## From area to dimension

    If the smallest sets have zero area, then "minimise the area" has a trivial answer, zero,
    and area can no longer tell these sets apart or say how substantial they still are. We need
    a finer ruler.

    Zoom in on that zero-area scorch. Under magnification it stays as intricate as a *solid
    patch*: new detail keeps appearing just as fast as it would inside a filled region, however
    far you zoom. The right ruler measures that: **dimension**, how fast detail multiplies as
    you shrink your measuring box, not how much area is covered.

    And the result that names the subject: the planar Besicovitch set has **zero area but
    dimension exactly 2** (Davies, 1971). No area, yet as two-dimensional as the table itself.
    That clash is what the conjecture is about:

    > **The Kakeya conjecture.** Every Besicovitch set in $\mathbb{R}^n$ has full dimension $n$:
    > however thin it looks, it is as high-dimensional as the whole space around it.

    Davies settled the plane, $n = 2$. That was the easy case; three dimensions held out for
    fifty years.

    $$
    \begin{aligned}
    \dim_{\mathrm B}(E) &= \lim_{\varepsilon \to 0} \frac{\log N(\varepsilon)}{\log(1/\varepsilon)} && \text{box-counting dimension} \\
    \dim_{\mathrm H}(E) &= \inf\{\, s \ge 0 : \mathcal H^{s}(E) = 0 \,\} && \text{Hausdorff dimension}
    \end{aligned}
    $$
    """)
    return


@app.cell
def _(COLORS, base_layout, go, np):
    # Box-counting: a 1D segment (slope ~1), a 2D filled triangle (slope ~2), and -- the payoff --
    # a Besicovitch pile: a dense field of UNIT SEGMENTS, one per direction across a full fan,
    # their centres spread over a small disk. It is built from 1D needles, yet its box-count grows
    # like a solid 2D region -- slope close to 2, tracking the filled triangle, not the segment.
    _rng = np.random.default_rng(1)

    def _box_count(points, eps):
        keys = set()
        inv = 1.0 / eps
        for px, py in points:
            keys.add((int(np.floor(px * inv)), int(np.floor(py * inv))))
        return len(keys)

    _tline = np.linspace(0, 1, 40000)
    _segment = np.column_stack([_tline, 0.6 * _tline])  # a slanted segment (dim 1)

    _grid = np.linspace(0, 1, 700)
    _gu, _gv = np.meshgrid(_grid, _grid)
    _gu, _gv = _gu.ravel(), _gv.ravel()
    _mask = _gu + _gv <= 1.0
    _triangle = np.column_stack([_gu[_mask], _gv[_mask]])  # filled triangle (dim 2)

    # Besicovitch pile: 400 unit segments, one per direction, centres scattered over a disk.
    _Ndir = 400
    _pdirs = np.linspace(0.0, np.pi, _Ndir, endpoint=False)
    _pang = _rng.random(_Ndir) * 2 * np.pi
    _prad = 0.5 * np.sqrt(_rng.random(_Ndir))
    _pcx, _pcy = _prad * np.cos(_pang), _prad * np.sin(_pang)
    _ps = np.linspace(-0.5, 0.5, 160)
    _pile = np.column_stack(
        [
            (_pcx[:, None] + _ps[None, :] * np.cos(_pdirs)[:, None]).ravel(),
            (_pcy[:, None] + _ps[None, :] * np.sin(_pdirs)[:, None]).ravel(),
        ]
    )
    _pile = _pile - _pile.min(axis=0)
    _pile = _pile / _pile.max()  # normalise into ~unit box for a fair box-count

    _epsilons = np.array([1 / 2, 1 / 4, 1 / 8, 1 / 16, 1 / 32, 1 / 64])
    _seg_counts = np.array([_box_count(_segment, e) for e in _epsilons])
    _tri_counts = np.array([_box_count(_triangle, e) for e in _epsilons])
    _pile_counts = np.array([_box_count(_pile, e) for e in _epsilons])

    _log_inv_eps = np.log(1 / _epsilons)
    _seg_slope = np.polyfit(_log_inv_eps, np.log(_seg_counts), 1)[0]
    _tri_slope = np.polyfit(_log_inv_eps, np.log(_tri_counts), 1)[0]
    _pile_slope = np.polyfit(_log_inv_eps, np.log(_pile_counts), 1)[0]

    _fig = go.Figure()
    _fig.add_trace(
        go.Scatter(
            x=_log_inv_eps,
            y=np.log(_seg_counts),
            mode="lines+markers",
            line={"color": COLORS["primary"], "width": 3},
            marker={"size": 9},
            name=f"segment, slope ≈ {_seg_slope:.2f} (dim 1)",
        )
    )
    _fig.add_trace(
        go.Scatter(
            x=_log_inv_eps,
            y=np.log(_tri_counts),
            mode="lines+markers",
            line={"color": COLORS["secondary"], "width": 3},
            marker={"size": 9},
            name=f"filled triangle, slope ≈ {_tri_slope:.2f} (dim 2)",
        )
    )
    _fig.add_trace(
        go.Scatter(
            x=_log_inv_eps,
            y=np.log(_pile_counts),
            mode="lines+markers",
            line={"color": COLORS["quaternary"], "width": 3, "dash": "dot"},
            marker={"size": 9},
            name=f"Besicovitch pile, slope ≈ {_pile_slope:.2f}",
        )
    )
    _fig.update_layout(
        **base_layout(
            title="Counting boxes",
            height=460,
            xaxis={"title": "log(1/ε)"},
            yaxis={"title": "log N(ε)"},
        )
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    Cover each shape with boxes of side ε and watch the tally grow as the boxes shrink. On a
    log–log plot the slope is the dimension: the single segment climbs at about 1, the filled
    patch roughly twice as steeply, and the zero-area pile rides up with the filled patch, not the
    segment. No area, yet the detail of a solid region.
    (Finite sampling reads both 2D slopes a little below 2, but the pile clearly tracks the patch.)
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## The same construction, one dimension up

    Everything you just built transfers. In space the needle must aim at every direction on a
    whole **sphere**. Drop one needle per direction and slide them to overlap as much as they can,
    exactly as on the table: each keeps its direction, the overlaps are counted once, and the
    pile fills **zero volume** while still holding every direction.
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
            title="Sphere of directions",
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
    A single needle sweeps until it has pointed at every direction on the sphere; its tip traces
    out the whole surface. Every one of those directions needs its own needle in the pile.
    """)
    return


@app.cell
def _(COLORS, SCENE_THEME, base_layout, fibonacci_sphere, go, np, play_pause):
    # "Overlap to zero volume": one unit segment per sphere-direction, each keeping its DIRECTION
    # while its CENTRE slides from a spread-out sphere of radius R to a common point (a bush). A
    # running volume readout (voxel-count of the thickened segments on a coarse 3D grid) shows the
    # union volume collapsing as the tubes overlap -- the 3D twin of "Overlap every direction".
    _N = 55
    _dx, _dy, _dz = fibonacci_sphere(_N)
    _dirs = np.column_stack([_dx, _dy, _dz])  # direction (fixed) of each needle
    _r = 0.1  # tube radius for the volume estimate

    # Voxel grid for the coarse volume readout (wide enough to hold the spread-out tubes).
    _g = np.linspace(-1.4, 1.4, 46)
    _VX, _VY, _VZ = np.meshgrid(_g, _g, _g, indexing="ij")
    _P = np.column_stack([_VX.ravel(), _VY.ravel(), _VZ.ravel()])
    _vcell = (_g[1] - _g[0]) ** 3

    def _volume(R):
        _occ = np.zeros(_P.shape[0], dtype=bool)
        for _i in range(_N):
            _c = R * _dirs[_i]  # centre spread along its own direction
            _a = _c - 0.5 * _dirs[_i]
            _b = _c + 0.5 * _dirs[_i]
            _ab = _b - _a
            _t = np.clip(((_P - _a) @ _ab) / (_ab @ _ab), 0.0, 1.0)
            _proj = _a + _t[:, None] * _ab
            _occ |= np.sum((_P - _proj) ** 2, axis=1) <= _r * _r
        return float(_occ.sum() * _vcell)

    def _segments(R):
        _xs, _ys, _zs = [], [], []
        for _i in range(_N):
            _c = R * _dirs[_i]
            _xs += [_c[0] - 0.5 * _dirs[_i][0], _c[0] + 0.5 * _dirs[_i][0], None]
            _ys += [_c[1] - 0.5 * _dirs[_i][1], _c[1] + 0.5 * _dirs[_i][1], None]
            _zs += [_c[2] - 0.5 * _dirs[_i][2], _c[2] + 0.5 * _dirs[_i][2], None]
        return go.Scatter3d(
            x=_xs,
            y=_ys,
            z=_zs,
            mode="lines",
            line={"color": COLORS["primary"], "width": 3},
            opacity=0.6,
            name="needles",
        )

    _Rs = np.linspace(0.8, 0.0, 10)
    _vols = {round(float(_R), 4): _volume(_R) for _R in _Rs}

    _fig = go.Figure()
    _fig.add_trace(_segments(_Rs[0]))  # 0

    _fig.frames = [go.Frame(data=[_segments(_R)], traces=[0], name=str(_i)) for _i, _R in enumerate(_Rs)]

    _bound = 1.4
    _scene = {
        **SCENE_THEME,
        "xaxis": {**SCENE_THEME["xaxis"], "range": [-_bound, _bound]},
        "yaxis": {**SCENE_THEME["yaxis"], "range": [-_bound, _bound]},
        "zaxis": {**SCENE_THEME["zaxis"], "range": [-_bound, _bound]},
        "aspectmode": "cube",
    }
    _v0 = _vols[round(float(_Rs[0]), 4)]
    _v1 = _vols[round(float(_Rs[-1]), 4)]
    _fig.update_layout(
        **base_layout(
            title="Overlap to zero volume",
            height=560,
            scene=_scene,
        )
    )
    _fig.add_annotation(
        text=f"tube volume: spread ≈ {_v0:.3f}  →  overlapped ≈ {_v1:.3f}",
        showarrow=False,
        x=0.5,
        y=1.0,
        xref="paper",
        yref="paper",
        font={"color": COLORS["highlight"], "size": 14},
    )
    _fig.update_layout(updatemenus=play_pause("▶ Slide together"))
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    The needles, one per sphere-direction, slide to overlap as much as they can. Each keeps its
    direction, so all directions remain, but the overlaps counted once keep driving the volume
    down (the readout tracks it), reaching zero in the continuum limit, just as the area did in
    the plane.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    The same picture as before, now in space: a pile that fills no volume yet points every way.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Zero volume, dimension three

    Zoom into the zero-volume pile and, just like the flat scorch, it keeps throwing up new detail
    as fast as a solid block would, however far you go. By the box-counting ruler its slope heads
    toward **3**: no volume, yet as three-dimensional as the space around it. In the plane this was
    both true and provable: Davies settled it. Everyone believed the same held in space; **proving
    it was the problem that stood for over fifty years.**
    """)
    return


@app.cell
def _(COLORS, base_layout, fibonacci_sphere, go, np):
    # "Zoom in space": box-count calibration objects in 3D -- a line (slope ~1), a flat sheet
    # (slope ~2) and a solid block (slope ~3) -- plus a 3D Besicovitch sample: unit segments
    # across many sphere-directions, centres spread through a small cloud so the union fills
    # space. Each series is labelled with its HONESTLY measured slope.
    _rng = np.random.default_rng(0)

    def _box_count3(pts, eps):
        inv = 1.0 / eps
        keys = set()
        for px, py, pz in pts:
            keys.add((int(np.floor(px * inv)), int(np.floor(py * inv)), int(np.floor(pz * inv))))
        return len(keys)

    _t = np.linspace(0, 1, 12000)
    _line = np.column_stack([_t, 0.3 + 0.0 * _t, 0.6 + 0.0 * _t])  # a line (dim 1)

    _su = np.linspace(0, 1, 260)
    _sU, _sV = np.meshgrid(_su, _su)
    _sheet = np.column_stack([_sU.ravel(), _sV.ravel(), np.full(_sU.size, 0.5)])  # flat sheet (dim 2)

    _gb = np.linspace(0, 1, 90)  # dense grid so the block does not saturate the box-count
    _BX, _BY, _BZ = np.meshgrid(_gb, _gb, _gb)
    _block = np.column_stack([_BX.ravel(), _BY.ravel(), _BZ.ravel()])  # solid block (dim 3)

    # 3D Besicovitch approximation: a unit segment in every sphere-direction, centres spread
    # over a small cloud so the union is a genuine space-filling tangle (not a single bush).
    _Ndir = 900
    _bx, _by, _bz = fibonacci_sphere(_Ndir)
    _bdirs = np.column_stack([_bx, _by, _bz])
    _centres = 0.55 * (_rng.random((_Ndir, 3)) - 0.5)
    _s = np.linspace(-0.5, 0.5, 220)
    _kpts = _centres[:, None, :] + _s[None, :, None] * _bdirs[:, None, :]
    _kak = _kpts.reshape(-1, 3)
    _kak = _kak - _kak.min(axis=0)
    _kak = _kak / _kak.max()  # normalise into ~unit box

    _epsilons = np.array([1 / 2, 1 / 4, 1 / 8, 1 / 16, 1 / 32])
    _log_inv_eps = np.log(1 / _epsilons)

    def _series(pts):
        _counts = np.array([_box_count3(pts, e) for e in _epsilons])
        _slope = np.polyfit(_log_inv_eps, np.log(_counts), 1)[0]
        return _counts, _slope

    _line_c, _line_s = _series(_line)
    _sheet_c, _sheet_s = _series(_sheet)
    _block_c, _block_s = _series(_block)
    _kak_c, _kak_s = _series(_kak)

    _fig = go.Figure()
    _fig.add_trace(
        go.Scatter(
            x=_log_inv_eps,
            y=np.log(_line_c),
            mode="lines+markers",
            line={"color": COLORS["primary"], "width": 3},
            marker={"size": 9},
            name=f"line, slope ≈ {_line_s:.2f}",
        )
    )
    _fig.add_trace(
        go.Scatter(
            x=_log_inv_eps,
            y=np.log(_sheet_c),
            mode="lines+markers",
            line={"color": COLORS["secondary"], "width": 3},
            marker={"size": 9},
            name=f"flat sheet, slope ≈ {_sheet_s:.2f}",
        )
    )
    _fig.add_trace(
        go.Scatter(
            x=_log_inv_eps,
            y=np.log(_block_c),
            mode="lines+markers",
            line={"color": COLORS["accent3"], "width": 3},
            marker={"size": 9},
            name=f"solid block, slope ≈ {_block_s:.2f}",
        )
    )
    _fig.add_trace(
        go.Scatter(
            x=_log_inv_eps,
            y=np.log(_kak_c),
            mode="lines+markers",
            line={"color": COLORS["quaternary"], "width": 3, "dash": "dot"},
            marker={"size": 9},
            name=f"Besicovitch pile, slope ≈ {_kak_s:.2f}",
        )
    )
    _fig.update_layout(
        **base_layout(
            title="Zoom in space",
            height=460,
            xaxis={"title": "log(1/ε)"},
            yaxis={"title": "log N(ε)"},
        )
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    Box-count the pile in space as the boxes shrink. On a log–log plot the line, flat sheet and
    solid block climb at rates near 1, 2 and 3, and the Besicovitch pile rides up with the solid
    block, well clear of the flat sheet. As in the plane, one dimension up: no volume, yet the
    detail of a solid region. (Finite sampling reads every slope a little low, but
    the pile clearly tracks the block.)
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    So why was space so much harder than the plane? The next views are the mechanism, and they are
    the 2D moves one size up.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Two tubes barely overlap

    Thicken a needle and it becomes a thin **tube**. Here is the single fact every 3D argument is
    built from: two tubes pointing in different directions cross only in a tiny patch, and that
    patch shrinks fast as the angle between them grows. So you can't stack a tube for every
    direction onto one spot; they push apart and fill real space. Every bound below spends this one
    fact.
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
        return [
            {
                "type": "buttons",
                "showactive": False,
                "y": 1.12,
                "x": 0.5,
                "xanchor": "center",
                "buttons": [
                    {
                        "label": label,
                        "method": "animate",
                        "args": [
                            None,
                            {
                                "frame": {"duration": dur, "redraw": True},
                                "fromcurrent": True,
                                "transition": {"duration": int(dur * 0.6)},
                            },
                        ],
                    },
                    {
                        "label": "❚❚ Pause",
                        "method": "animate",
                        "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}],
                    },
                ],
            }
        ]

    def _dirvec(a):
        return np.array([np.cos(a), np.sin(a)]), np.array([-np.sin(a), np.cos(a)])

    def _tube(a, col, fill):
        _u, _v = _dirvec(a)
        _c = np.array(
            [
                (_L / 2) * _u + (_w / 2) * _v,
                (_L / 2) * _u - (_w / 2) * _v,
                -(_L / 2) * _u - (_w / 2) * _v,
                -(_L / 2) * _u + (_w / 2) * _v,
            ]
        )
        return go.Scatter(
            x=[*_c[:, 0], _c[0, 0]],
            y=[*_c[:, 1], _c[0, 1]],
            mode="lines",
            fill="toself",
            fillcolor=fill,
            line={"color": col, "width": 1},
            xaxis="x",
            yaxis="y",
            showlegend=False,
        )

    def _needle(a, col):
        _u, _ = _dirvec(a)
        return go.Scatter(
            x=[-(_L / 2) * _u[0], (_L / 2) * _u[0]],
            y=[-(_L / 2) * _u[1], (_L / 2) * _u[1]],
            mode="lines",
            line={"color": col, "width": 4},
            xaxis="x",
            yaxis="y",
            showlegend=False,
        )

    def _patch(theta):
        _H = theta / 2
        _M = np.array([[-np.sin(_H), np.cos(_H)], [np.sin(_H), np.cos(_H)]])
        _pts = np.array(
            [np.linalg.solve(_M, np.array([_s1 * _w / 2, _s2 * _w / 2])) for _s1 in (1, -1) for _s2 in (1, -1)]
        )
        _pts = _pts[np.argsort(np.arctan2(_pts[:, 1], _pts[:, 0]))]
        return go.Scatter(
            x=[*_pts[:, 0], _pts[0, 0]],
            y=[*_pts[:, 1], _pts[0, 1]],
            mode="lines",
            fill="toself",
            fillcolor=COLORS["quaternary"],
            line={"color": COLORS["quaternary"], "width": 1},
            xaxis="x",
            yaxis="y",
            showlegend=False,
        )

    def _tiplabel(a, col, txt):
        _u, _ = _dirvec(a)
        return go.Scatter(
            x=[(_L / 2 + 0.14) * _u[0]],
            y=[(_L / 2 + 0.14) * _u[1]],
            mode="text",
            text=[txt],
            textfont={"color": col, "size": 12},
            xaxis="x",
            yaxis="y",
            showlegend=False,
        )

    def _anglelabel(theta):
        return go.Scatter(
            x=[0.0],
            y=[1.72],
            mode="text",
            text=[f"<b>{np.degrees(theta):.0f}° apart</b>"],
            textfont={"color": COLORS["text"], "size": 14},
            xaxis="x",
            yaxis="y",
            showlegend=False,
        )

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
            go.Scatter(
                x=[np.degrees(theta)],
                y=[_share(theta)],
                mode="markers",
                marker={"color": COLORS["quaternary"], "size": 14, "symbol": "star"},
                xaxis="x2",
                yaxis="y2",
                showlegend=False,
            ),
        ]

    _thetas = np.linspace(np.radians(16), np.radians(90), 26)
    _shares = [_share(_t) for _t in _thetas]

    _fig = make_subplots(
        rows=1,
        cols=2,
        column_widths=[0.55, 0.45],
        subplot_titles=("Two needles and the patch they share", "Shared patch shrinks as the angle grows"),
    )
    _fig.add_trace(
        go.Scatter(
            x=np.degrees(_thetas),
            y=_shares,
            mode="lines",
            line={"color": COLORS["muted"], "width": 3},
            showlegend=False,
        ),
        row=1,
        col=2,
    )  # 0 static curve
    _init = _frame(_thetas[0])
    for _t in _init[:-1]:
        _fig.add_trace(_t, row=1, col=1)  # 1..8 left panel
    _fig.add_trace(_init[-1], row=1, col=2)  # 9 moving star

    _fig.frames = [
        go.Frame(data=_frame(_t), traces=[1, 2, 3, 4, 5, 6, 7, 8, 9], name=str(_i)) for _i, _t in enumerate(_thetas)
    ]

    _fig.update_layout(**base_layout(title="Two tubes", height=470))
    _fig.update_xaxes(range=[-1.5, 1.5], row=1, col=1, scaleanchor="y", constrain="domain")
    _fig.update_yaxes(range=[-1.5, 1.95], row=1, col=1)
    _fig.update_xaxes(title_text="angle between the needles (degrees)", range=[12, 94], row=1, col=2)
    _fig.update_yaxes(title_text="shared area", range=[0, max(_shares) * 1.1], row=1, col=2)
    style_subplot_axes(_fig, show_ticklabels=True)
    _fig.update_layout(updatemenus=_menu("▶ Widen the angle", 260))
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    Widen the angle between two tubes and the patch they share shrinks fast (the readout tracks
    it). Differently-aimed tubes barely overlap, so a tube for every direction has to spread out.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Bush, hairbrush, and the sticky comb

    Spend the fact the simplest way and you get a **bush**: pin a needle, turn it through every
    direction, and since the tubes can't pile up the bush must spread, forcing dimension $\ge 2$.
    Let the pinned end slide along a line as it turns and the bushes stack into a **hairbrush**,
    pushing the bound to $5/2$ (Wolff, 1995).

    The step that finally reached the full **3** rhymes with a move you already know. The hardest
    piles to rule out are the **sticky** ones: needles pointing almost the same way already sit
    almost together, so the tubes line up and the overlap fact bites as hard as it can. That
    lined-up shape is slice-and-slide one dimension up. The proof does not rearrange anything,
    though: Wang and Zahl showed the sticky pile is the worst case, and that in it the tubes are
    forced to fill dimension 3.
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
        return [
            {
                "type": "buttons",
                "showactive": False,
                "y": 1.12,
                "x": 0.5,
                "xanchor": "center",
                "buttons": [
                    {
                        "label": label,
                        "method": "animate",
                        "args": [None, {"frame": {"duration": dur, "redraw": True}, "fromcurrent": True}],
                    },
                    {
                        "label": "❚❚ Pause",
                        "method": "animate",
                        "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}],
                    },
                ],
            }
        ]

    def _seg(cx, cy, a, half):
        return [cx - half * np.cos(a), cx + half * np.cos(a)], [cy - half * np.sin(a), cy + half * np.sin(a)]

    def _trail(states, half, ax, opacity):
        _xs, _ys = [], []
        for _cx, _cy, _a in states:
            _x, _y = _seg(_cx, _cy, _a, half)
            _xs += [_x[0], _x[1], None]
            _ys += [_y[0], _y[1], None]
        return go.Scatter(
            x=_xs,
            y=_ys,
            mode="lines",
            line={"color": COLORS["accent3"], "width": 1},
            opacity=opacity,
            xaxis=ax[0],
            yaxis=ax[1],
            showlegend=False,
        )

    def _cur(cx, cy, a, half, ax):
        _x, _y = _seg(cx, cy, a, half)
        return go.Scatter(
            x=_x,
            y=_y,
            mode="lines",
            line={"color": COLORS["secondary"], "width": 5},
            xaxis=ax[0],
            yaxis=ax[1],
            showlegend=False,
        )

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

    _fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=(
            "Bush: pivot in place, face every direction  (dim ≥ 2)",
            "Hairbrush: pivot while sliding along a handle  (dim ≥ 5/2)",
        ),
    )
    _init = _frame(0)
    _fig.add_trace(_init[0], row=1, col=1)  # 0 left trail
    _fig.add_trace(_init[1], row=1, col=1)  # 1 left needle
    _fig.add_trace(
        go.Scatter(
            x=[0.0],
            y=[0.0],
            mode="markers",
            marker={"color": COLORS["quaternary"], "size": 10},
            xaxis="x",
            yaxis="y",
            showlegend=False,
        ),
        row=1,
        col=1,
    )  # 2 pivot
    _fig.add_trace(_init[2], row=1, col=2)  # 3 right trail
    _fig.add_trace(_init[3], row=1, col=2)  # 4 right needle
    _fig.add_trace(
        go.Scatter(
            x=[_hx0, _hx1],
            y=[0.0, 0.0],
            mode="lines",
            line={"color": COLORS["quaternary"], "width": 4},
            xaxis="x2",
            yaxis="y2",
            showlegend=False,
        ),
        row=1,
        col=2,
    )  # 5 handle

    _fig.frames = [go.Frame(data=_frame(_k), traces=[0, 1, 3, 4], name=str(_k)) for _k in range(_K + 1)]

    _fig.update_layout(**base_layout(title="Bush → hairbrush", height=460))
    _fig.update_xaxes(range=[-0.8, 0.8], row=1, col=1, scaleanchor="y", constrain="domain")
    _fig.update_yaxes(range=[-0.8, 0.8], row=1, col=1)
    _fig.update_xaxes(range=[-1.6, 1.6], row=1, col=2, scaleanchor="y2", constrain="domain")
    _fig.update_yaxes(range=[-0.75, 0.75], row=1, col=2)
    style_subplot_axes(_fig)
    _fig.update_layout(updatemenus=_menu("▶ Turn the needle", 130))
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    Left: a needle pivots through every direction, tracing a bush (dimension $\ge 2$). Right: the
    same pivot while the root slides along a handle, stacking a hairbrush (dimension $\ge 5/2$).
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
        return [
            {
                "type": "buttons",
                "showactive": False,
                "y": 1.12,
                "x": 0.5,
                "xanchor": "center",
                "buttons": [
                    {
                        "label": label,
                        "method": "animate",
                        "args": [
                            None,
                            {
                                "frame": {"duration": dur, "redraw": True},
                                "fromcurrent": True,
                                "transition": {"duration": int(dur * 0.7)},
                            },
                        ],
                    },
                    {
                        "label": "❚❚ Pause",
                        "method": "animate",
                        "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}],
                    },
                ],
            }
        ]

    def _lerp(c1, c2, f):
        return tuple(round(c1[_i] + (c2[_i] - c1[_i]) * f) for _i in range(3))

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
            _out.append(
                go.Scatter(
                    x=[_cx - _half * np.cos(_a), _cx + _half * np.cos(_a)],
                    y=[_cy - _half * np.sin(_a), _cy + _half * np.sin(_a)],
                    mode="lines",
                    line={"color": _cols[_i], "width": 4},
                    showlegend=False,
                )
            )
        return _out

    def _label(p):
        if p < 0.02:
            _t = "scattered"
        elif p > 0.98:
            _t = "combed neat (sticky)"
        else:
            _t = "sliding into place"
        return go.Scatter(
            x=[0.0],
            y=[1.5],
            mode="text",
            text=[f"<b>{_t}</b>"],
            textfont={"color": COLORS["text"], "size": 14},
            showlegend=False,
        )

    _ps = [0.0] * 4 + list(np.linspace(0.0, 1.0, 22)) + [1.0] * 6

    _fig = go.Figure()
    for _tr in _needles(0.0):
        _fig.add_trace(_tr)
    _fig.add_trace(_label(0.0))

    _fig.frames = [go.Frame(data=[*_needles(_p), _label(_p)], name=str(_i)) for _i, _p in enumerate(_ps)]

    _fig.update_layout(**base_layout(title="Comb it sticky", height=520))
    _fig.update_xaxes(
        range=[-1.35, 1.35],
        scaleanchor="y",
        constrain="domain",
        gridcolor=COLORS["grid"],
        zerolinecolor=COLORS["grid"],
        showticklabels=False,
    )
    _fig.update_yaxes(range=[-1.0, 1.7], gridcolor=COLORS["grid"], zerolinecolor=COLORS["grid"], showticklabels=False)
    _fig.update_layout(updatemenus=_menu("▶ Comb it neat", 220))
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    The needles slide into groups where nearby directions sit close together, which is
    slice-and-slide in space. Nothing rotates, so every direction stays; this is the shape the
    volume estimate needs.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Fifty years of bounds, then the 2025 proof

    For decades the proven bound only crept: trivial 1, bush 2, Wolff's hairbrush $5/2$, then
    Katz–Łaba–Tao just past $5/2$ (2000), and there it stalled for a quarter-century, the summit
    at 3 out of reach. In 2025 **Hong Wang and Joshua Zahl** closed the gap with the sticky comb
    above, proving every zero-volume pile in space has dimension exactly **3**. Wang was awarded a
    Fields Medal in 2026.
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
    ]
    _values = [1.0, 2.0, 2.5, 2.51]
    _colors = [COLORS["muted"], COLORS["accent3"], COLORS["tertiary"], COLORS["quaternary"]]

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
            title="The fifty-year climb",
            height=460,
            yaxis={"title": "proven dim_H ≥", "range": [0, 3.3]},
        )
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    Each bar is the best proven bound at its time (1, 2, 5/2, 5/2+ε), stuck below the
    dashed line at 3 for twenty-five years until the 2025 result reached it.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Where it stops: dimension four and up

    Strikingly, the proof is special to three dimensions. In dimension 4 and higher the direct
    analogue of the key estimate is false (you can pack tubes near a low-degree surface), so the
    full conjecture there is still **open**. The needle has only just begun to turn.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## A century of the needle: who proved what, and when

    > A hundred-year relay race: each mathematician carries the idea a little further, from a
    > 1917 doodle on paper to a 2026 Fields Medal.

    - **Kakeya poses the puzzle (1917).**
      [**Sōichi Kakeya**](https://en.wikipedia.org/wiki/S%C5%8Dichi_Kakeya) asked for the region
      of least area inside which a unit segment can be *continuously* rotated through a full
      half-turn, returning to its original line reversed.
    - **Besicovitch drops the bombshell (1919–1928).**
      [**Abram Besicovitch**](https://en.wikipedia.org/wiki/Abram_Samoilovitch_Besicovitch),
      working on a different problem, found a set that contains a unit segment in every direction
      yet has **area zero**. His slice-and-slide idea was later streamlined by **Oskar Perron**
      into *Perron trees*, using joins introduced by **Gyula Pál**.
    - **The question is reborn as dimension (mid-20th century).** A measure-zero set can still be
      "large" in a subtler sense, so mathematicians replaced area with
      [**Hausdorff dimension**](https://en.wikipedia.org/wiki/Hausdorff_dimension) and conjectured
      that a Kakeya set in $\mathbb{R}^n$ must have the full dimension $n$.
    - **The plane falls (1971).** **Roy Davies** proved every Besicovitch set in the plane has
      Hausdorff dimension exactly $2$; **Córdoba** later gave a cleaner geometric proof and
      **Oberlin** sharpened it to Fourier dimension $2$.
      ([**Jean Bourgain**](https://en.wikipedia.org/wiki/Jean_Bourgain) made his mark on the
      higher-dimensional versions.)
    - **Three dimensions resist for fifty years (1995–2025).** **Thomas Wolff** (1995) reached
      dimension $\tfrac{5}{2}$ with the *hairbrush* argument; **Katz–Łaba–Tao** (2000) nudged past
      it. Then in **February 2025**,
      [**Hong Wang**](https://www.nyu.edu/about/news-publications/news/2026/july/nyu-professor-hong-wang-wins-fields-medal.html)
      (NYU / IHES) and **Joshua Zahl** (UBC) proved every Kakeya set in $\mathbb{R}^3$ has
      dimension exactly $3$; in **2026** the result earned Wang a
      [**Fields Medal**](https://en.wikipedia.org/wiki/Fields_Medal).
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

    ## Why Anyone Cares

    > That little needle turns out to be a hidden gear driving
    > machinery all over mathematics, from how waves ripple to how secret codes hold up.

    A puzzle about turning a needle would be a curiosity if it stayed alone. It doesn't.
    The geometry of *lines pointing in many directions* is a hidden skeleton beneath a
    surprising amount of mathematics:

    - **Harmonic analysis.** Kakeya sits directly below the **restriction** and
      **Bochner–Riesz** conjectures and the behaviour of the Fourier transform.
      [**Charles Fefferman**](https://en.wikipedia.org/wiki/Charles_Fefferman) used a
      Besicovitch set to *disprove* the ball multiplier conjecture (1971), the discovery
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
      (1971), 417–421: the 2D dimension result.
    - Terence Tao, *From rotating needles to stability of waves* (survey), Notices of
      the AMS: [terrytao.wordpress.com/kakeya.pdf](https://terrytao.wordpress.com/wp-content/uploads/2009/08/kakeya.pdf)
    - Zeev Dvir, *On the size of Kakeya sets in finite fields* (2008), the polynomial
      method: [arxiv.org/abs/0803.2336](https://arxiv.org/abs/0803.2336)
    - Wikipedia, *Kakeya set*:
      [en.wikipedia.org/wiki/Kakeya_set](https://en.wikipedia.org/wiki/Kakeya_set)

    ---

    Not bad for a puzzle about turning a needle on a tabletop.
    """)
    return


if __name__ == "__main__":
    app.run()
