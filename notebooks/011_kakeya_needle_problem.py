"""
Kakeya: from a turning needle to the three-dimensional theorem.

A guided walk through the Kakeya problem following the research note in
`research/kakeya/kakeya.md`: the 1917 needle puzzle, the plane constructions that drive
the swept area to zero, dimension as the ruler that replaces area, the harmonic-analysis
tower that rests on the problem, and the 2025 Wang-Zahl proof of the three-dimensional
conjecture (Hong Wang, 2026 Fields Medal).

Status: draft
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
    """Shared geometry and animation helpers for the Kakeya notebook."""
    import functools
    import math

    SQRT3 = math.sqrt(3.0)

    def play_pause(label, duration=90, y=1.12):
        """A Plotly play/pause button pair driving a frame animation."""
        return [
            {
                "type": "buttons",
                "showactive": False,
                "y": y,
                "x": 0.5,
                "xanchor": "center",
                "buttons": [
                    {
                        "label": label,
                        "method": "animate",
                        "args": [
                            None,
                            {
                                "frame": {"duration": duration, "redraw": True},
                                "fromcurrent": True,
                                "transition": {"duration": 0},
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

    def unit_needle(cx, cy, angle, length=1.0):
        """Endpoints of a segment of given length centred at (cx, cy) at angle (radians)."""
        dx, dy = 0.5 * length * math.cos(angle), 0.5 * length * math.sin(angle)
        return np.array([cx - dx, cx + dx]), np.array([cy - dy, cy + dy])

    def circle(r=0.5, n=240, cx=0.0, cy=0.0):
        """Points on a circle of radius r centred at (cx, cy)."""
        t = np.linspace(0, 2 * math.pi, n)
        return cx + r * np.cos(t), cy + r * np.sin(t)

    def deltoid(b=0.25, n=400):
        """The three-cusped hypocycloid: chord length 4b, enclosed area 2 pi b^2."""
        t = np.linspace(0, 2 * math.pi, n)
        return 2 * b * np.cos(t) + b * np.cos(2 * t), 2 * b * np.sin(t) - b * np.sin(2 * t)

    def deltoid_point_dir(t, b=0.25):
        """A boundary point of the deltoid at parameter t and its unit tangent direction."""
        p = np.array([2 * b * math.cos(t) + b * math.cos(2 * t), 2 * b * math.sin(t) - b * math.sin(2 * t)])
        d = np.array([-2 * b * math.sin(t) - 2 * b * math.sin(2 * t), 2 * b * math.cos(t) - 2 * b * math.cos(2 * t)])
        nrm = np.linalg.norm(d)
        if nrm < 1e-9:
            t += 1e-2
            d = np.array(
                [-2 * b * math.sin(t) - 2 * b * math.sin(2 * t), 2 * b * math.cos(t) - 2 * b * math.cos(2 * t)]
            )
            nrm = np.linalg.norm(d)
        return p, d / nrm

    def line_polygon_chord(p, d, bx, by):
        """The chord cut from a closed polygon (bx, by) by the line through p in direction d."""
        n = np.array([-d[1], d[0]])
        f = (np.column_stack([bx, by]) - p) @ n
        s = (np.column_stack([bx, by]) - p) @ d
        hits = []
        for i in range(len(bx) - 1):
            f0, f1 = f[i], f[i + 1]
            if f0 == 0.0:
                hits.append(s[i])
            if (f0 < 0) != (f1 < 0):
                w = f0 / (f0 - f1)
                hits.append(s[i] + w * (s[i + 1] - s[i]))
        if len(hits) < 2:
            return p - 0.5 * d, p + 0.5 * d
        lo, hi = min(hits), max(hits)
        return p + lo * d, p + hi * d

    @functools.lru_cache(maxsize=8)
    def _deltoid_boundary(b, n):
        """Cached deltoid boundary (identical for fixed b, so it is built once per call site)."""
        return deltoid(b, n)

    def deltoid_needle(t, b=0.25):
        """Endpoints of the unit needle held tangent to the deltoid at parameter t."""
        p, d = deltoid_point_dir(t, b)
        bx, by = _deltoid_boundary(b, 500)
        e0, e1 = line_polygon_chord(p, d, bx, by)
        return np.array([e0[0], e1[0]]), np.array([e0[1], e1[1]])

    def equilateral_h1():
        """Equilateral triangle of height 1 (Pal's convex minimum), rows [baseL, baseR, apex]."""
        return np.array([[-1.0 / SQRT3, 0.0], [1.0 / SQRT3, 0.0], [0.0, 1.0]])

    def tri_mask(gx, gy, tri):
        """Boolean mask of grid points inside triangle tri (3x2) via barycentric signs."""
        (ax, ay), (bx, by), (cx, cy) = tri
        d = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
        if abs(d) < 1e-15:
            return np.zeros(gx.shape, bool)
        a = ((by - cy) * (gx - cx) + (cx - bx) * (gy - cy)) / d
        bb = ((cy - ay) * (gx - cx) + (ax - cx) * (gy - cy)) / d
        c = 1.0 - a - bb
        return (a >= -1e-9) & (bb >= -1e-9) & (c >= -1e-9)

    def perron_pieces(nlev, alpha, apex, base_half):
        """Perron sub-triangles after nlev rounds of pairwise cut-and-shift (overlap fraction alpha)."""
        xs = np.linspace(-base_half, base_half, 2**nlev + 1)
        ap = np.array(apex)
        groups = [[np.array([[xs[i], 0.0], [xs[i + 1], 0.0], ap])] for i in range(2**nlev)]
        w = (2 * base_half) / 2**nlev
        for _ in range(nlev):
            step = 0.5 * alpha * w
            nxt = []
            for i in range(0, len(groups), 2):
                left = [t + np.array([step, 0.0]) for t in groups[i]]
                right = [t + np.array([-step, 0.0]) for t in groups[i + 1]]
                nxt.append(left + right)
            groups = nxt
            w *= 1.0 + alpha
        return [t for g in groups for t in g]

    def union_area(tris, gx, gy, cell_area):
        """Rasterised area of the union of triangles over the grid (gx, gy)."""
        mask = np.zeros(gx.shape, bool)
        for t in tris:
            mask |= tri_mask(gx, gy, t)
        return float(mask.sum() * cell_area), mask

    def rot2d(pts, deg, ctr):
        """Rotate points (N x 2) by deg degrees about centre ctr."""
        th = math.radians(deg)
        r = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
        return (np.asarray(pts) - ctr) @ r.T + ctr

    return (
        SQRT3,
        circle,
        deltoid,
        deltoid_needle,
        equilateral_h1,
        line_polygon_chord,
        math,
        perron_pieces,
        play_pause,
        rot2d,
        tri_mask,
        union_area,
        unit_needle,
    )


@app.cell
def _(mo):
    mo.md(
        r"""
        # Kakeya: from a turning needle to the three-dimensional theorem

        In 1917 Sōichi Kakeya asked a tabletop question: lay a needle of length 1 flat on a
        table and turn it until it has pointed in **every** direction. What is the *smallest
        area* it can sweep while doing so?

        The honest answer overturns what "smallest" should even mean. Following that thread
        leads from a plane puzzle to a stack of central results in modern analysis, and closing
        its three-dimensional case earned Hong Wang a share of the 2026 Fields Medal. The path,
        one beat resting on the last:

        1. the needle problem, and the two objects it splits into;
        2. plane constructions that drive the area to zero;
        3. dimension, the ruler that replaces area;
        4. the plane answer: area 0, dimension 2;
        5. the harmonic-analysis tower that rests on it;
        6. the three-dimensional conjecture, and why space is harder;
        7. the 2025 machinery that closed it;
        8. dimension four and up, still open.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 1. The needle problem

        The needle has fixed length 1. It only slides and turns, never growing or shrinking, and
        it stays flat on the table. The puzzle is about waste: turning the needle paints table,
        and we want to paint as little as possible while still facing every direction.

        The obvious answer spins the needle about its middle and fills a disc. The cheap ways to
        shrink that disc all fail, and seeing why points the right way: a smaller disc cannot hold
        the needle pointing sideways, squeezing it to an ellipse still needs the full unit width at
        the extremes, and pivoting about an endpoint only trades one disc for another. Every cheap
        idea keeps the needle *rotating in place*, and rotating in place is what fills area. Kakeya
        himself guessed one could do better, with the curved **deltoid**.
        """
    )
    return


@app.cell
def _(
    COLORS,
    base_layout,
    circle,
    deltoid,
    deltoid_needle,
    go,
    make_subplots,
    math,
    np,
    play_pause,
    style_subplot_axes,
    unit_needle,
):
    _frames_n = 36
    _ts = np.linspace(0, math.pi, _frames_n)
    _dt = np.linspace(0, 2 * math.pi, _frames_n)

    _dx, _dy = deltoid(0.25, 400)

    def _disc_trail(k):
        _x, _y = [], []
        for _j in range(k + 1):
            _nx, _ny = unit_needle(0.0, 0.0, _ts[_j])
            _x += [_nx[0], _nx[1], None]
            _y += [_ny[0], _ny[1], None]
        return go.Scatter(
            x=_x, y=_y, mode="lines", line={"color": "rgba(0,212,255,0.25)", "width": 1}, showlegend=False
        )

    def _delt_trail(k):
        _x, _y = [], []
        for _j in range(k + 1):
            _nx, _ny = deltoid_needle(_dt[_j])
            _x += [_nx[0], _nx[1], None]
            _y += [_ny[0], _ny[1], None]
        return go.Scatter(
            x=_x, y=_y, mode="lines", line={"color": "rgba(255,107,107,0.25)", "width": 1}, showlegend=False
        )

    _fig = make_subplots(rows=1, cols=2, subplot_titles=("Spin in a disc  (area π/4)", "Turn in a deltoid  (area π/8)"))

    _cx, _cy = circle(0.5, 200)
    _fig.add_trace(
        go.Scatter(
            x=_cx,
            y=_cy,
            mode="lines",
            fill="toself",
            fillcolor="rgba(0,212,255,0.08)",
            line={"color": COLORS["grid"]},
            showlegend=False,
        ),
        row=1,
        col=1,
    )
    _fig.add_trace(_disc_trail(0), row=1, col=1)
    _n0x, _n0y = unit_needle(0.0, 0.0, _ts[0])
    _fig.add_trace(
        go.Scatter(x=_n0x, y=_n0y, mode="lines", line={"color": COLORS["primary"], "width": 6}, showlegend=False),
        row=1,
        col=1,
    )

    _fig.add_trace(
        go.Scatter(
            x=_dx,
            y=_dy,
            mode="lines",
            fill="toself",
            fillcolor="rgba(255,107,107,0.08)",
            line={"color": COLORS["grid"]},
            showlegend=False,
        ),
        row=1,
        col=2,
    )
    _fig.add_trace(_delt_trail(0), row=1, col=2)
    _m0x, _m0y = deltoid_needle(_dt[0])
    _fig.add_trace(
        go.Scatter(x=_m0x, y=_m0y, mode="lines", line={"color": COLORS["secondary"], "width": 6}, showlegend=False),
        row=1,
        col=2,
    )

    _frames = []
    for _k in range(_frames_n):
        _nx, _ny = unit_needle(0.0, 0.0, _ts[_k])
        _mx, _my = deltoid_needle(_dt[_k])
        _frames.append(
            go.Frame(
                data=[_disc_trail(_k), go.Scatter(x=_nx, y=_ny), _delt_trail(_k), go.Scatter(x=_mx, y=_my)],
                traces=[1, 2, 4, 5],
                name=str(_k),
            )
        )
    _fig.frames = _frames

    _fig.update_layout(**base_layout(title="Same turn, half the area", height=460))
    for _c in (1, 2):
        _fig.update_xaxes(
            range=[-0.8, 0.8],
            scaleanchor="y" if _c == 1 else "y2",
            constrain="domain",
            showticklabels=False,
            row=1,
            col=_c,
        )
        _fig.update_yaxes(range=[-0.8, 0.8], showticklabels=False, row=1, col=_c)
    style_subplot_axes(_fig)
    _fig.update_layout(updatemenus=play_pause("▶ Turn the needle"))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Both needles are unit length and point in every direction. Every position they pass through
        stays drawn, so the two footprints build up as you play: the disc on the left, the deltoid
        on the right. The deltoid covers half the room the disc does.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The disc spins the needle about its middle: the tips reach only $r = \tfrac12$, so it
        paints a disc of radius one half. The deltoid lets the needle *slide along its own
        length* as it turns, so it never repaints the same sliver twice, and that saving is
        exactly the factor of two.

        $$
        \begin{aligned}
        A_{\text{disc}} &= \pi r^2                        && \text{area of a disc of radius } r \\
                        &= \pi\left(\tfrac12\right)^2      && \text{tips reach only } r = \tfrac12 \\
                        &= \tfrac{\pi}{4} \approx 0.785 \\[4pt]
        A_{\text{deltoid}} &= 2\pi b^2                     && \text{deltoid, rolling radius } b \\
                        &= 2\pi\left(\tfrac14\right)^2     && \text{unit chord } 4b = 1 \Rightarrow b = \tfrac14 \\
                        &= \tfrac{\pi}{8} \approx 0.393 = \tfrac12 A_{\text{disc}}.
        \end{aligned}
        $$

        The deltoid really turns the needle, and it beats the disc. But is it the minimum? It is
        not, and answering properly forces a split the puzzle hides.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Two objects, because the math differs

        Everything downstream depends on distinguishing them:

        - **Kakeya needle set:** a set inside which the needle can be *continuously rotated*
          through a full turn (a real physical turn). Its infimal area is **0 but never
          attained**: you can go as small as you like, never to zero.
        - **Besicovitch set** (the modern *Kakeya set*): a set that merely *contains* a unit
          segment in every direction, with no requirement that you slide between them. Here the
          area can be **exactly 0**.

        > A compact set $K \subseteq \mathbb{R}^n$ is a **Kakeya set** if for every direction
        > $\omega \in S^{n-1}$ there is a position $a$ with the segment
        > $\{a + t\omega : 0 \le t \le 1\} \subseteq K$.

        The deltoid is a needle set. To reach zero area we drop the "keep turning" requirement
        and chase the Besicovitch version, then glue the pieces back together at the end.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 2. Plane constructions: shrinking the area

        A chain of "good, but we can do better" moves. First a step that looks backwards.

        Among **convex** shapes (no dents), Pal (1921) showed the smallest needle set is the
        equilateral triangle of height 1, area $1/\sqrt3 \approx 0.577$. That is larger than the
        deltoid, and that is the point: **convexity is a handicap**, because a convex shape must
        be used in one piece. The triangle is not a better final answer, it is a better *part*:
        cut it apart and the pieces can overlap.
        """
    )
    return


@app.cell
def _(
    COLORS,
    SQRT3,
    base_layout,
    circle,
    deltoid,
    deltoid_needle,
    equilateral_h1,
    go,
    make_subplots,
    math,
    np,
    style_subplot_axes,
    unit_needle,
):
    _fig = make_subplots(
        rows=1,
        cols=3,
        subplot_titles=("Disc  π/4 ≈ 0.785", "Deltoid  π/8 ≈ 0.393", "Pal triangle  1/√3 ≈ 0.577"),
    )

    _cx, _cy = circle(0.5, 200)
    _fig.add_trace(
        go.Scatter(
            x=_cx,
            y=_cy,
            mode="lines",
            fill="toself",
            fillcolor="rgba(0,212,255,0.10)",
            line={"color": COLORS["grid"]},
            showlegend=False,
        ),
        row=1,
        col=1,
    )
    for _a in np.linspace(0, math.pi, 12, endpoint=False):
        _nx, _ny = unit_needle(0.0, 0.0, _a)
        _fig.add_trace(
            go.Scatter(
                x=_nx, y=_ny, mode="lines", line={"color": COLORS["primary"], "width": 2}, opacity=0.6, showlegend=False
            ),
            row=1,
            col=1,
        )

    _dx, _dy = deltoid(0.25, 400)
    _fig.add_trace(
        go.Scatter(
            x=_dx,
            y=_dy,
            mode="lines",
            fill="toself",
            fillcolor="rgba(255,107,107,0.10)",
            line={"color": COLORS["grid"]},
            showlegend=False,
        ),
        row=1,
        col=2,
    )
    for _t in np.linspace(0, 2 * math.pi, 18, endpoint=False):
        _nx, _ny = deltoid_needle(_t)
        _fig.add_trace(
            go.Scatter(
                x=_nx,
                y=_ny,
                mode="lines",
                line={"color": COLORS["secondary"], "width": 2},
                opacity=0.6,
                showlegend=False,
            ),
            row=1,
            col=2,
        )

    _tri = equilateral_h1()
    _tx = [_tri[0, 0], _tri[1, 0], _tri[2, 0], _tri[0, 0]]
    _ty = [_tri[0, 1], _tri[1, 1], _tri[2, 1], _tri[0, 1]]
    _fig.add_trace(
        go.Scatter(
            x=_tx,
            y=_ty,
            mode="lines",
            fill="toself",
            fillcolor="rgba(149,225,211,0.12)",
            line={"color": COLORS["grid"]},
            showlegend=False,
        ),
        row=1,
        col=3,
    )
    _bl, _br, _ap = _tri
    _fig.add_trace(
        go.Scatter(
            x=[0.0, 0.0], y=[0.0, 1.0], mode="lines", line={"color": COLORS["accent1"], "width": 3}, showlegend=False
        ),
        row=1,
        col=3,
    )
    for _base in (_bl, _br):
        _d = (_ap - _base) / np.linalg.norm(_ap - _base)
        _e = _base + _d
        _fig.add_trace(
            go.Scatter(
                x=[_base[0], _e[0]],
                y=[_base[1], _e[1]],
                mode="lines",
                line={"color": COLORS["accent1"], "width": 3},
                showlegend=False,
            ),
            row=1,
            col=3,
        )

    _fig.update_layout(**base_layout(title="The three classic answers", height=380))
    for _c, _xr, _yr in (
        (1, [-0.62, 0.62], [-0.62, 0.62]),
        (2, [-0.8, 0.8], [-0.8, 0.8]),
        (3, [-0.72, 0.72], [-0.62, 1.05]),
    ):
        _fig.update_xaxes(
            range=_xr,
            scaleanchor=f"y{'' if _c == 1 else _c}",
            constrain="domain",
            showticklabels=False,
            row=1,
            col=_c,
        )
        _fig.update_yaxes(range=_yr, showticklabels=False, row=1, col=_c)
    style_subplot_axes(_fig)
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The three answers side by side, each with a unit needle placed honestly in it (in the disc
        a fan through the centre, in the deltoid tangent to the boundary, in the triangle along the
        altitude and the two slanted edges). Convexity costs: the triangle ($1/\sqrt3$) beats the
        disc but loses to the non-convex deltoid ($\pi/8$). There is an intermediate convex answer
        too, the Reuleaux triangle of width 1 (turn the needle by pivoting about its three corners),
        area $(\pi-\sqrt3)/2 \approx 0.705$, sitting between the disc and Pal's triangle.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### The one move that shrinks area: slide is free, only turning costs

        Everything below rests on a single asymmetry between the needle's two moves. Rotating a
        needle by an angle $\theta$ about a pivot sweeps a circular sector of area $\theta/2$.
        Sliding it *along its own length* sweeps nothing new: it stays on the same line.

        So directions are what cost area; position is free. Two triangles that each carry a fan
        of directions can be slid to **overlap**, and the overlap keeps every direction while
        occupying less room. Sliding a piece never changes the directions of the needles inside
        it, so no direction is ever lost. That is the whole engine.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, make_subplots, math, np, play_pause, style_subplot_axes):
    _n_rot = 24
    _n_slide = 16
    _thetas = np.linspace(0, math.pi / 3, _n_rot)
    _slides = np.linspace(0, 0.9, _n_slide)
    _pivot = np.array([-0.4, -0.2])

    def _sector(a1):
        _a = np.linspace(0, a1, 40)
        return go.Scatter(
            x=[_pivot[0], *(_pivot[0] + np.cos(_a)), _pivot[0]],
            y=[_pivot[1], *(_pivot[1] + np.sin(_a)), _pivot[1]],
            mode="lines",
            fill="toself",
            fillcolor="rgba(255,230,109,0.22)",
            line={"color": COLORS["quaternary"], "width": 1},
            showlegend=False,
        )

    def _needle_rot(a):
        _t = _pivot + np.array([math.cos(a), math.sin(a)])
        return go.Scatter(
            x=[_pivot[0], _t[0]],
            y=[_pivot[1], _t[1]],
            mode="lines",
            line={"color": COLORS["secondary"], "width": 6},
            showlegend=False,
        )

    def _needle_slide(s):
        _d = np.array([math.cos(math.pi / 3), math.sin(math.pi / 3)])
        _base = _pivot + s * _d
        return go.Scatter(
            x=[_base[0], _base[0] + _d[0]],
            y=[_base[1], _base[1] + _d[1]],
            mode="lines",
            line={"color": COLORS["secondary"], "width": 6},
            showlegend=False,
        )

    _fig = make_subplots(
        rows=1, cols=2, subplot_titles=("Rotate: sweeps a sector θ/2", "Slide along the axis: sweeps nothing")
    )
    _fig.add_trace(_sector(_thetas[0]), row=1, col=1)
    _fig.add_trace(_needle_rot(_thetas[0]), row=1, col=1)
    _full_sector = _sector(_thetas[-1])
    _full_sector.update(fillcolor="rgba(255,230,109,0.22)")
    _fig.add_trace(_full_sector, row=1, col=2)
    _fig.add_trace(_needle_slide(_slides[0]), row=1, col=2)

    _frames = []
    for _k in range(max(_n_rot, _n_slide)):
        _kr = min(_k, _n_rot - 1)
        _ks = min(_k, _n_slide - 1)
        _frames.append(
            go.Frame(
                data=[_sector(_thetas[_kr]), _needle_rot(_thetas[_kr]), _needle_slide(_slides[_ks])],
                traces=[0, 1, 3],
                name=str(_k),
            )
        )
    _fig.frames = _frames

    _fig.update_layout(**base_layout(title="Only turning paints", height=420))
    for _c in (1, 2):
        _fig.update_xaxes(
            range=[-0.7, 1.1],
            scaleanchor="y" if _c == 1 else "y2",
            constrain="domain",
            showticklabels=False,
            row=1,
            col=_c,
        )
        _fig.update_yaxes(range=[-0.5, 1.1], showticklabels=False, row=1, col=_c)
    style_subplot_axes(_fig)
    _fig.update_layout(updatemenus=play_pause("▶ Rotate, then slide"))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        On the left the needle rotates about a pivot and the swept sector (yellow) grows with the
        angle. On the right it slides along its own length and the swept region never grows. Turning
        is the only move that paints.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### The Perron tree: cut a triangle into slivers and overlap them

        Take the triangle of height 1. Split its base into $2^k$ equal pieces, giving $2^k$ thin
        sub-triangles that together still span the same 60-degree fan of directions (they all
        share the apex). Now translate them horizontally so consecutive ones overlap as much as
        possible while keeping their apex directions. The overlaps cut the total area. Each level
        adds only a fixed slice of fresh area, so iterating gives an area bound

        $$
        A_k \;\le\; (\text{const})\cdot A_0 \cdot \tfrac{1}{k} \;\longrightarrow\; 0
        \qquad (k \to \infty),
        $$

        and for any $\varepsilon > 0$ a Perron tree of area below $\varepsilon$ still holds a
        unit segment in every direction of the fan.
        """
    )
    return


@app.cell
def _(COLORS, SQRT3, base_layout, go, make_subplots, np, perron_pieces, play_pause, style_subplot_axes, union_area):
    _nlev = 6
    _apex = (0.0, 1.0)
    _base_half = 1.0 / SQRT3
    _gu = np.linspace(-1.3, 1.3, 180)
    _gv = np.linspace(-0.05, 1.05, 90)
    _GX, _GY = np.meshgrid(_gu, _gv)
    _cellA = (_gu[1] - _gu[0]) * (_gv[1] - _gv[0])

    _alphas = np.linspace(0.0, 0.6, 16)
    _base_area, _ = union_area(perron_pieces(_nlev, 0.0, _apex, _base_half), _GX, _GY, _cellA)

    def _tree_traces(alpha):
        _tris = perron_pieces(_nlev, alpha, _apex, _base_half)
        _x, _y = [], []
        for _t in _tris:
            _x += [_t[0, 0], _t[1, 0], _t[2, 0], None]
            _y += [_t[0, 1], _t[1, 1], _t[2, 1], None]
        _area, _ = union_area(_tris, _GX, _GY, _cellA)
        return _x, _y, _area

    def _fan_dial(pct):
        return go.Scatter(
            x=[-0.92],
            y=[0.98],
            mode="text",
            text=[f"footprint {pct:.0f}%   fan 60°"],
            textfont={"color": COLORS["highlight"], "size": 14},
            textposition="middle right",
            showlegend=False,
        )

    _x0, _y0, _a0 = _tree_traces(_alphas[0])

    _fig = go.Figure()
    _fig.add_trace(
        go.Scatter(
            x=_x0,
            y=_y0,
            mode="lines",
            fill="toself",
            fillcolor="rgba(0,212,255,0.18)",
            line={"color": COLORS["primary"], "width": 0.8},
            showlegend=False,
        )
    )
    _fig.add_trace(_fan_dial(100.0))

    _frames = []
    for _k, _al in enumerate(_alphas):
        _xx, _yy, _ar = _tree_traces(_al)
        _frames.append(
            go.Frame(data=[go.Scatter(x=_xx, y=_yy), _fan_dial(100.0 * _ar / _base_area)], traces=[0, 1], name=str(_k))
        )
    _fig.frames = _frames

    _fig.update_layout(**base_layout(title="Perron tree: overlap the slivers", height=520))
    _fig.update_xaxes(range=[-1.3, 1.3], scaleanchor="y", constrain="domain", showticklabels=False)
    _fig.update_yaxes(range=[-0.1, 1.1], showticklabels=False)
    style_subplot_axes(_fig)
    _fig.update_layout(updatemenus=play_pause("▶ Sprout the tree"))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        As the overlap grows the footprint (readout, top left) shrinks well below the original
        triangle, while the fan of directions stays locked at 60 degrees: every sliver keeps its
        apex, so no direction is lost. Area is being spent, directions are being kept.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The 60-degree span is an artefact of using one triangle's fan, not a real limit. An
        equilateral tree covers 60 degrees of directions, so **three** rotated copies (0, 60,
        120 degrees) cover all 180 (a direction and its reverse are the same), and six copies
        close up into a symmetric six-pointed star. Take the sprouting to the limit inside each
        copy, and Besicovitch (1919) gets the payoff:

        > There is a Kakeya (Besicovitch) set $K \subseteq \mathbb{R}^2$ with area $|K| = 0$.

        For the *needle* version, Pal joins glue the branches together (slide the needle far out,
        turn where a tiny angle suffices, slide back), so the needle can be turned continuously
        in area as small as you like, but never zero. Van Alphen (1942), then Cunningham (1971),
        even fit these arbitrarily small needle sets inside the **unit disc** (radius 1), the
        smallest disc that can hold a unit segment at all.
        """
    )
    return


@app.cell
def _(COLORS, SQRT3, base_layout, go, np, perron_pieces, play_pause, rot2d, style_subplot_axes):
    _nlev = 5
    _apex = (0.0, 1.0)
    _base_half = 1.0 / SQRT3
    _tris = perron_pieces(_nlev, 0.6, _apex, _base_half)
    _allpts = np.vstack(_tris)
    _ctr = _allpts.mean(axis=0)
    _rots = [0, 60, 120, 180, 240, 300]

    def _copies_traces(m):
        _x, _y = [], []
        for _r in _rots[:m]:
            for _t in _tris:
                _rt = rot2d(_t, _r, _ctr)
                _x += [_rt[0, 0], _rt[1, 0], _rt[2, 0], None]
                _y += [_rt[0, 1], _rt[1, 1], _rt[2, 1], None]
        return _x, _y

    _steps = [1, 2, 3, 6]
    _labels = ["1 tree, 60°", "2 trees, 120°", "3 trees, 180° (all directions)", "6 trees, symmetric star"]

    _x0, _y0 = _copies_traces(1)
    _fig = go.Figure()
    _fig.add_trace(
        go.Scatter(
            x=_x0,
            y=_y0,
            mode="lines",
            fill="toself",
            fillcolor="rgba(255,107,107,0.16)",
            line={"color": COLORS["secondary"], "width": 0.6},
            showlegend=False,
        )
    )

    _frames = []
    for _k, _m in enumerate(_steps):
        _xx, _yy = _copies_traces(_m)
        _frames.append(
            go.Frame(
                data=[go.Scatter(x=_xx, y=_yy)],
                traces=[0],
                name=_labels[_k],
                layout={"title": {"text": f"Besicovitch star: {_labels[_k]}"}},
            )
        )
    _fig.frames = _frames

    _fig.update_layout(**base_layout(title="Besicovitch star: 1 tree, 60°", height=520))
    _fig.update_xaxes(range=[_ctr[0] - 1.35, _ctr[0] + 1.35], scaleanchor="y", constrain="domain", showticklabels=False)
    _fig.update_yaxes(range=[_ctr[1] - 1.35, _ctr[1] + 1.35], showticklabels=False)
    style_subplot_axes(_fig)
    _fig.update_layout(updatemenus=play_pause("▶ Drop in the copies", duration=650))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Each play step drops in another rotated copy of the tree. Three copies (0, 60, 120 degrees)
        already cover all 180 directions; six close up into the symmetric six-pointed star. Every
        copy still has vanishing area, so the whole star does too, while now holding a needle in
        every direction.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The area falls toward zero, but slowly: even the sharp Perron / Keich schedule only
        decays like $1/\log N$ for $N = 2^n$ slivers, so it cannot be shown collapsing all the
        way to zero on screen. The set has no area, yet it clearly still holds a needle pointing
        everywhere. Area is reporting "nothing there" about something substantial. That is a
        signal that area is the wrong ruler.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 3. Dimension: the right way to say "still big"

        A Besicovitch set has zero area yet plainly holds a needle in every direction, so "zero
        area" cannot mean "nothing there." Zero measure is no thickness, not no points: the rational
        numbers have zero length yet sit everywhere, and the Cantor set (throw out the middle third,
        forever) has zero length yet is uncountable.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, make_subplots, style_subplot_axes):
    def _cantor_levels(depth):
        _levels = [[(0.0, 1.0)]]
        for _ in range(depth):
            _nxt = []
            for _a, _b in _levels[-1]:
                _t = (_b - _a) / 3.0
                _nxt += [(_a, _a + _t), (_b - _t, _b)]
            _levels.append(_nxt)
        return _levels

    _depth = 6
    _levels = _cantor_levels(_depth)
    _lengths = [(2.0 / 3.0) ** _m for _m in range(_depth + 1)]

    _fig = make_subplots(rows=1, cols=2, subplot_titles=("The Cantor set, refined", "total covering length → 0"))
    for _m, _ivs in enumerate(_levels):
        _x, _y = [], []
        for _a, _b in _ivs:
            _x += [_a, _b, None]
            _y += [-_m, -_m, None]
        _fig.add_trace(
            go.Scatter(x=_x, y=_y, mode="lines", line={"color": COLORS["primary"], "width": 4}, showlegend=False),
            row=1,
            col=1,
        )
    _fig.add_trace(
        go.Scatter(
            x=list(range(_depth + 1)),
            y=_lengths,
            mode="lines+markers",
            line={"color": COLORS["secondary"], "width": 3},
            showlegend=False,
        ),
        row=1,
        col=2,
    )

    _fig.update_layout(**base_layout(title="Measure zero, still substantial", height=380))
    _fig.update_xaxes(range=[-0.02, 1.02], showticklabels=False, row=1, col=1)
    _fig.update_yaxes(range=[-_depth - 0.5, 0.5], showticklabels=False, row=1, col=1)
    _fig.update_xaxes(title_text="refinement depth m", row=1, col=2)
    _fig.update_yaxes(title_text="length (2/3)ᵐ", row=1, col=2)
    style_subplot_axes(_fig, show_ticklabels=True)
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The Cantor set after $m$ rounds of removing middle thirds: $2^m$ intervals of length
        $3^{-m}$, so its total length is $(2/3)^m \to 0$. It ends with zero length yet uncountably
        many points. Length (like area) reports "nothing there" about a set that is still
        substantial, which is exactly why we reach for a finer ruler.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        So area is the wrong ruler. The right one is **dimension**, measured by how the number of
        small boxes needed to cover a set grows as the boxes shrink. Cover with a grid of side
        $\delta$ and count the boxes $N(\delta)$ the set meets:

        $$
        \dim_{\text{box}} K = \lim_{\delta \to 0^+} \frac{\log N(\delta)}{\log(1/\delta)},
        \qquad N(\delta) \sim \delta^{-d}.
        $$

        A line needs twice as many boxes when you halve their size (exponent 1); a filled square
        needs four times as many (exponent 2). The slope of $\log N$ against $\log(1/\delta)$ is
        the dimension.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, make_subplots, np, style_subplot_axes):
    _deltas = [0.25, 0.2, 0.125, 0.1, 0.0625, 0.05]

    def _sq_boxes(delta):
        _n = round(1.0 / delta)
        return _n * _n

    _seg_N = [round(1.0 / d) for d in _deltas]
    _sq_N = [_sq_boxes(d) for d in _deltas]
    _inv = [1.0 / d for d in _deltas]

    _fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=(
            "Grid over a segment and a square (δ = 0.1)",
            "log N versus log(1/δ): the slope is the dimension",
        ),
    )

    _d = 0.1
    _n = round(1.0 / _d)
    _grid_x, _grid_y = [], []
    for _i in range(_n + 1):
        _grid_x += [_i * _d, _i * _d, None, 0, 1, None]
        _grid_y += [0, 1, None, _i * _d, _i * _d, None]
    _fig.add_trace(
        go.Scatter(x=_grid_x, y=_grid_y, mode="lines", line={"color": COLORS["grid"], "width": 0.6}, showlegend=False),
        row=1,
        col=1,
    )
    _row = int(0.55 / _d)
    _sx, _sy = [], []
    for _i in range(_n):
        _sx += [_i * _d, (_i + 1) * _d, (_i + 1) * _d, _i * _d, _i * _d, None]
        _sy += [_row * _d, _row * _d, (_row + 1) * _d, (_row + 1) * _d, _row * _d, None]
    _fig.add_trace(
        go.Scatter(
            x=_sx,
            y=_sy,
            mode="lines",
            fill="toself",
            fillcolor="rgba(0,212,255,0.35)",
            line={"color": COLORS["primary"], "width": 0.5},
            showlegend=False,
            name="segment boxes",
        ),
        row=1,
        col=1,
    )
    _fig.add_trace(
        go.Scatter(
            x=[0, 1],
            y=[0.555, 0.555],
            mode="lines",
            line={"color": COLORS["secondary"], "width": 3},
            name="segment",
            showlegend=False,
        ),
        row=1,
        col=1,
    )

    _lx = np.log(_inv)
    _fig.add_trace(
        go.Scatter(
            x=_lx,
            y=np.log(_seg_N),
            mode="lines+markers",
            line={"color": COLORS["secondary"], "width": 3},
            name="segment (slope 1)",
        ),
        row=1,
        col=2,
    )
    _fig.add_trace(
        go.Scatter(
            x=_lx,
            y=np.log(_sq_N),
            mode="lines+markers",
            line={"color": COLORS["primary"], "width": 3},
            name="square (slope 2)",
        ),
        row=1,
        col=2,
    )

    _fig.update_layout(**base_layout(title="Box-counting the dimension", height=430))
    _fig.update_xaxes(range=[-0.05, 1.05], scaleanchor="y", constrain="domain", showticklabels=False, row=1, col=1)
    _fig.update_yaxes(range=[-0.05, 1.05], showticklabels=False, row=1, col=1)
    _fig.update_xaxes(title_text="log(1/δ)", row=1, col=2)
    _fig.update_yaxes(title_text="log N(δ)", row=1, col=2)
    style_subplot_axes(_fig, show_ticklabels=True)
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Left: at $\delta = 0.1$ the segment meets 10 boxes, the filled square meets all 100. Right:
        plotting $\log N$ against $\log(1/\delta)$, the segment rides a slope-1 line and the square
        a slope-2 line. That slope is the dimension.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        That exponent can come out fractional, and a fraction is exactly what "between a line and
        a surface" means. Self-similar sets make it concrete: a set built from $N$ copies of
        itself each scaled by $1/r$ has dimension $\log N / \log r$.

        $$
        \begin{aligned}
        \text{Cantor set:} \quad & N=2,\ r=3 && \dim = \tfrac{\log 2}{\log 3} \approx 0.631 \\
        \text{Sierpinski triangle:} \quad & N=3,\ r=2 && \dim = \tfrac{\log 3}{\log 2} \approx 1.585 \\
        \text{Koch curve:} \quad & N=4,\ r=3 && \dim = \tfrac{\log 4}{\log 3} \approx 1.262.
        \end{aligned}
        $$

        The Sierpinski triangle, at $\approx 1.585$, is the cleanest picture of "more than a
        curve, less than a filled region," which is the flavour a Besicovitch set turns out to
        have. (There are two flavours of dimension: Minkowski uses one box size, Hausdorff allows
        many; Hausdorff is the finer, harder one the conjecture asks for. On self-similar sets
        they agree.)
        """
    )
    return


@app.cell
def _(COLORS, SQRT3, base_layout, go, make_subplots, math, np, style_subplot_axes):
    def _sierpinski(depth):
        _base = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, SQRT3 / 2.0]])
        _tris = [_base]
        for _ in range(depth):
            _nxt = []
            for _a, _b, _c in _tris:
                _mab, _mbc, _mca = (_a + _b) / 2, (_b + _c) / 2, (_c + _a) / 2
                _nxt += [np.array([_a, _mab, _mca]), np.array([_mab, _b, _mbc]), np.array([_mca, _mbc, _c])]
            _tris = _nxt
        return _tris

    def _koch(depth):
        _pts = [np.array([0.0, 0.0]), np.array([1.0, 0.0])]
        _ang = math.radians(60)
        _rot = np.array([[math.cos(_ang), -math.sin(_ang)], [math.sin(_ang), math.cos(_ang)]])
        for _ in range(depth):
            _out = [_pts[0]]
            for _i in range(len(_pts) - 1):
                _p, _q = _pts[_i], _pts[_i + 1]
                _d = _q - _p
                _a, _b = _p + _d / 3.0, _p + 2 * _d / 3.0
                _apex = _a + _rot @ (_b - _a)
                _out += [_a, _apex, _b, _q]
            _pts = _out
        return np.array(_pts)

    _fig = make_subplots(
        rows=1, cols=2, subplot_titles=("Sierpinski triangle  (dim ≈ 1.585)", "Koch curve  (dim ≈ 1.262)")
    )
    _sx, _sy = [], []
    for _t in _sierpinski(6):
        _sx += [_t[0, 0], _t[1, 0], _t[2, 0], _t[0, 0], None]
        _sy += [_t[0, 1], _t[1, 1], _t[2, 1], _t[0, 1], None]
    _fig.add_trace(
        go.Scatter(
            x=_sx,
            y=_sy,
            mode="lines",
            fill="toself",
            fillcolor="rgba(170,150,218,0.5)",
            line={"color": COLORS["accent3"], "width": 0.4},
            showlegend=False,
        ),
        row=1,
        col=1,
    )

    _k = _koch(4)
    _fig.add_trace(
        go.Scatter(
            x=_k[:, 0], y=_k[:, 1], mode="lines", line={"color": COLORS["primary"], "width": 1.5}, showlegend=False
        ),
        row=1,
        col=2,
    )

    _fig.update_layout(**base_layout(title="Fractional dimension", height=360))
    _fig.update_xaxes(range=[-0.05, 1.05], scaleanchor="y", constrain="domain", showticklabels=False, row=1, col=1)
    _fig.update_yaxes(range=[-0.05, 0.95], showticklabels=False, row=1, col=1)
    _fig.update_xaxes(range=[-0.05, 1.05], scaleanchor="y2", constrain="domain", showticklabels=False, row=1, col=2)
    _fig.update_yaxes(range=[-0.15, 0.55], showticklabels=False, row=1, col=2)
    style_subplot_axes(_fig)
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Two self-similar sets drawn to depth. The Sierpinski triangle (three half-size copies,
        dimension $\log 3/\log 2 \approx 1.585$) and the Koch curve (four third-size copies,
        dimension $\log 4/\log 3 \approx 1.262$) both sit strictly between a line and a surface.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Box-counting a fractal (Minkowski)

        The copy-counting formula asserted those dimensions; box-counting checks them directly, and
        this is the Minkowski dimension in action on a genuinely fractal set. Lay a grid of side
        $\delta$ over the actual Sierpinski triangle and count the boxes $N(\delta)$ it meets, then
        shrink $\delta$. A curve would multiply its box count by 2 at each halving, a filled region
        by 4. The Sierpinski multiplies by about **3**, and

        $$
        \frac{\log N(\delta)}{\log(1/\delta)} \ \longrightarrow\ \frac{\log 3}{\log 2} \approx 1.585,
        $$

        the same value the copies gave. The slope lands between the segment's 1 and the square's 2,
        exactly where a shape "between a line and a surface" should.
        """
    )
    return


@app.cell
def _(COLORS, SQRT3, base_layout, go, make_subplots, np, play_pause, style_subplot_axes):
    _rng = np.random.default_rng(0)
    _verts = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, SQRT3 / 2.0]])
    _p = _rng.random((16000, 2)) * 0.2
    _acc = []
    for _s in range(36):
        _idx = _rng.integers(0, 3, size=16000)
        _p = (_p + _verts[_idx]) / 2.0
        if _s >= 6:
            _acc.append(_p.copy())
    _pts = np.concatenate(_acc)
    _draw = _pts[:: max(1, len(_pts) // 2500)]

    _ks = [1, 2, 3, 4, 5]
    _deltas = [2.0 ** (-_k) for _k in _ks]
    _occ = [np.unique(np.floor(_pts / _d).astype(np.int64), axis=0) for _d in _deltas]
    _counts = [len(_c) for _c in _occ]
    _logx = np.log([1.0 / _d for _d in _deltas])
    _logy = np.log(_counts)

    def _cell_rects(cells, delta):
        _x, _y = [], []
        for _i, _j in cells:
            _x += [_i * delta, (_i + 1) * delta, (_i + 1) * delta, _i * delta, _i * delta, None]
            _y += [_j * delta, _j * delta, (_j + 1) * delta, (_j + 1) * delta, _j * delta, None]
        return _x, _y

    _fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=("Grid of side δ over the Sierpinski triangle", "log N(δ) vs log(1/δ): the slope"),
    )
    _fig.add_trace(
        go.Scatter(
            x=_draw[:, 0],
            y=_draw[:, 1],
            mode="markers",
            marker={"color": COLORS["accent3"], "size": 1.5},
            showlegend=False,
        ),
        row=1,
        col=1,
    )
    _cx0, _cy0 = _cell_rects(_occ[0], _deltas[0])
    _fig.add_trace(
        go.Scatter(
            x=_cx0,
            y=_cy0,
            mode="lines",
            fill="toself",
            fillcolor="rgba(0,212,255,0.14)",
            line={"color": COLORS["primary"], "width": 0.6},
            showlegend=False,
        ),
        row=1,
        col=1,
    )
    _xr = np.array([_logx[0] - 0.2, _logx[-1] + 0.2])
    _fig.add_trace(
        go.Scatter(
            x=_xr,
            y=_logy[0] + 1.0 * (_xr - _logx[0]),
            mode="lines",
            line={"color": COLORS["muted"], "width": 1.5, "dash": "dot"},
            name="slope 1 (segment)",
        ),
        row=1,
        col=2,
    )
    _fig.add_trace(
        go.Scatter(
            x=_xr,
            y=_logy[0] + 2.0 * (_xr - _logx[0]),
            mode="lines",
            line={"color": COLORS["muted"], "width": 1.5, "dash": "dot"},
            name="slope 2 (square)",
        ),
        row=1,
        col=2,
    )
    _fig.add_trace(
        go.Scatter(
            x=_logx[:1],
            y=_logy[:1],
            mode="lines+markers",
            line={"color": COLORS["secondary"], "width": 3},
            name="Sierpinski",
        ),
        row=1,
        col=2,
    )

    _frames = []
    for _k in range(len(_ks)):
        _cx, _cy = _cell_rects(_occ[_k], _deltas[_k])
        _sl = np.polyfit(_logx[: _k + 1], _logy[: _k + 1], 1)[0] if _k >= 1 else float("nan")
        _title = f"Box-counting the Sierpinski: δ = 1/{2 ** _ks[_k]}, N = {_counts[_k]}" + (
            f", slope ≈ {_sl:.2f}" if _k >= 1 else ""
        )
        _frames.append(
            go.Frame(
                data=[go.Scatter(x=_cx, y=_cy), go.Scatter(x=_logx[: _k + 1], y=_logy[: _k + 1])],
                traces=[1, 4],
                name=str(_k),
                layout={"title": {"text": _title}},
            )
        )
    _fig.frames = _frames

    _fig.update_layout(
        **base_layout(title=f"Box-counting the Sierpinski: δ = 1/{2 ** _ks[0]}, N = {_counts[0]}", height=440)
    )
    _fig.update_xaxes(range=[-0.02, 1.02], scaleanchor="y", constrain="domain", showticklabels=False, row=1, col=1)
    _fig.update_yaxes(range=[-0.02, 0.9], showticklabels=False, row=1, col=1)
    _fig.update_xaxes(title_text="log(1/δ)", row=1, col=2)
    _fig.update_yaxes(title_text="log N(δ)", row=1, col=2)
    style_subplot_axes(_fig, show_ticklabels=True)
    _fig.update_layout(updatemenus=play_pause("▶ Shrink δ"))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The shaded boxes are the ones the fractal actually meets. Each halving of $\delta$ lights up
        about three times as many (not two, not four), so the log-log point climbs a track that hugs
        neither the slope-1 (segment) nor the slope-2 (square) guide but settles between them near
        $\log 3/\log 2 \approx 1.585$. Box-counting the pixels agrees with the copy-counting formula.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Hausdorff: the finer ruler the conjecture asks for

        Box-counting uses **one** box size everywhere. Hausdorff lets the cover use boxes of
        **different** sizes, and for an exponent $s$ it measures $\mathcal{H}^s$, the cheapest such
        cover. As $s$ sweeps up, $\mathcal{H}^s$ jumps from $\infty$ to $0$ at a single threshold,
        and that threshold is the **Hausdorff dimension**. On the Cantor set the depth-$m$ cover has
        $2^m$ intervals of length $3^{-m}$, so its cover sum is exactly

        $$
        \sum_i (\operatorname{diam} U_i)^s = 2^m (3^{-m})^s = \big(2 \cdot 3^{-s}\big)^m,
        $$

        a geometric series whose base passes through 1 at $s = \log 2/\log 3$. Below it the sum runs
        to infinity, above it collapses to zero. Always $\dim_H \le \dim_{\text{box}}$, so a Hausdorff
        statement is the stronger one, and the Kakeya conjecture is stated for this finer dimension.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, math, np, style_subplot_axes):
    _s = np.linspace(0.35, 0.95, 240)
    _thr = math.log(2) / math.log(3)

    _fig = go.Figure()
    for _m, _op in ((1, 0.35), (3, 0.55), (6, 0.75), (12, 1.0)):
        _fig.add_trace(
            go.Scatter(
                x=_s,
                y=(2.0 * 3.0 ** (-_s)) ** _m,
                mode="lines",
                line={"color": COLORS["primary"], "width": 2},
                opacity=_op,
                name=f"depth m = {_m}",
            )
        )
    _fig.add_vline(x=_thr, line={"color": COLORS["secondary"], "width": 2, "dash": "dash"})
    _fig.add_hline(y=1.0, line={"color": COLORS["muted"], "width": 1, "dash": "dot"})

    _fig.update_layout(**base_layout(title="Hausdorff: the cover sum jumps at s = log2/log3", height=440))
    _fig.update_xaxes(title_text="exponent s")
    _fig.update_yaxes(title_text="cover sum  Σ (diam)ˢ", type="log", range=[-1.6, 1.8])
    style_subplot_axes(_fig, show_ticklabels=True)
    _fig.add_annotation(
        x=_thr,
        y=1.65,
        text="dim_H = log2/log3 ≈ 0.631",
        showarrow=False,
        font={"color": COLORS["secondary"], "size": 12},
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The Cantor cover sum $(2 \cdot 3^{-s})^m$ against $s$, at deepening $m$. Only at the threshold
        $s = \log 2/\log 3$ does it hold near 1; below it the deepening curves run up to infinity,
        above it they fall to zero. The step sharpens with $m$, and the exponent it refuses to send
        to $0$ or $\infty$ is the Hausdorff dimension. This is the ruler the conjecture uses, and it
        is the harder one to pin down.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        On self-similar sets like the Cantor dust the two rulers land on the same number, so they
        look interchangeable. They are not. Take the countable set $E = \{0\} \cup \{1/n : n \ge 1\}$:
        its points pile up at $0$, so a uniform $\delta$-grid must spend about $\delta^{-1/2}$ boxes
        resolving the pile-up ($\dim_{\text{box}} = 1/2$), while a single interval can swallow the
        whole tail $[0, 1/M]$ for a Hausdorff cover and drive the sum to $0$ ($\dim_H = 0$). Same set,
        two rulers, $\dim_H = 0 < 1/2 = \dim_{\text{box}}$. That gap is exactly why proving the
        Hausdorff version of Kakeya is genuinely more than proving the Minkowski version.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 4. The plane answer: area 0, dimension 2

        Davies (1971) reframed the puzzle in this language and settled the plane:

        > Every Kakeya set $K \subseteq \mathbb{R}^2$ has Hausdorff and Minkowski **dimension 2**,
        > even though it can have area zero.

        The mechanism (Cordoba's overlap estimate): fatten each segment into a $1 \times \delta$
        rectangle. Two such rectangles crossing at angle $\theta$ overlap in area

        $$
        |R_1 \cap R_2| \approx \frac{\delta^2}{\sin\theta} \qquad (\text{small } \delta),
        $$

        so rectangles in well-separated directions barely overlap. Summed over all pairs the
        overlaps are small, which **forces the union to stay spread out**: you cannot compress it
        below full dimension.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, make_subplots, math, np, play_pause, style_subplot_axes):
    def _rect(angle, width, length=1.0, cx=0.0, cy=0.0):
        _hl, _hw = length / 2.0, width / 2.0
        _c = np.array([[-_hl, -_hw], [_hl, -_hw], [_hl, _hw], [-_hl, _hw], [-_hl, -_hw]])
        _co, _si = math.cos(angle), math.sin(angle)
        _r = np.array([[_co, -_si], [_si, _co]])
        _p = _c @ _r.T + np.array([cx, cy])
        return _p[:, 0], _p[:, 1]

    _counts = [1, 4, 8, 16, 28]
    _width = 0.06

    def _fan(m):
        _x, _y = [], []
        for _a in np.linspace(0, math.pi, m, endpoint=False):
            _rx, _ry = _rect(_a, _width)
            _x += [*_rx, None]
            _y += [*_ry, None]
        return _x, _y

    _gu = np.linspace(-0.6, 0.6, 220)
    _GX, _GY = np.meshgrid(_gu, _gu)
    _cellA = (_gu[1] - _gu[0]) ** 2

    def _union_area_rects(m):
        _mask = np.zeros(_GX.shape, bool)
        for _a in np.linspace(0, math.pi, m, endpoint=False):
            _u = np.array([math.cos(_a), math.sin(_a)])
            _v = np.array([-math.sin(_a), math.cos(_a)])
            _mask |= (np.abs(_GX * _u[0] + _GY * _u[1]) <= 0.5) & (np.abs(_GX * _v[0] + _GY * _v[1]) <= _width / 2)
        return float(_mask.sum() * _cellA)

    _fig = make_subplots(
        rows=1,
        cols=2,
        column_widths=[0.55, 0.45],
        subplot_titles=("A fan of 1×δ rectangles", "Summed area vs union area"),
    )
    _x0, _y0 = _fan(_counts[0])
    _fig.add_trace(
        go.Scatter(
            x=_x0,
            y=_y0,
            mode="lines",
            fill="toself",
            fillcolor="rgba(78,205,196,0.25)",
            line={"color": COLORS["tertiary"], "width": 0.5},
            showlegend=False,
        ),
        row=1,
        col=1,
    )

    _summed = [m * _width for m in _counts]
    _union = [_union_area_rects(m) for m in _counts]
    _fig.add_trace(
        go.Scatter(
            x=_counts,
            y=_summed,
            mode="lines+markers",
            line={"color": COLORS["secondary"], "width": 3},
            name="Σ areas (piles up)",
        ),
        row=1,
        col=2,
    )
    _fig.add_trace(
        go.Scatter(
            x=_counts,
            y=_union,
            mode="lines+markers",
            line={"color": COLORS["primary"], "width": 3},
            name="union (stays spread)",
        ),
        row=1,
        col=2,
    )

    _frames = []
    for _k, _m in enumerate(_counts):
        _xx, _yy = _fan(_m)
        _frames.append(go.Frame(data=[go.Scatter(x=_xx, y=_yy)], traces=[0], name=str(_m)))
    _fig.frames = _frames

    _fig.update_layout(**base_layout(title="Small overlaps keep the union large", height=430))
    _fig.update_xaxes(range=[-0.75, 0.75], scaleanchor="y", constrain="domain", showticklabels=False, row=1, col=1)
    _fig.update_yaxes(range=[-0.75, 0.75], showticklabels=False, row=1, col=1)
    _fig.update_xaxes(title_text="number of directions", row=1, col=2)
    _fig.update_yaxes(title_text="area", row=1, col=2)
    style_subplot_axes(_fig, show_ticklabels=True)
    _fig.update_layout(updatemenus=play_pause("▶ Add directions"))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Left: a fan of $1 \times \delta$ rectangles at separated angles. Right, both areas measured
        from the drawn rectangles: the summed area (coral) climbs linearly with the count, while the
        union (cyan) grows to fill the disc of radius $\tfrac12$ (area $\pi/4$) and stays there. Each
        pair overlaps only $\sim \delta^2/\sin\theta$, so the union never collapses: thin pieces,
        stubbornly large union.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        So the same clever pile answers two questions two ways. "How much paint to cover it?" is
        area, and the answer is none: the pile has no thickness. "How many boxes to find it?" is
        dimension, and the answer is all of them: at any resolution the pile meets essentially
        every box a solid square would. **Area 0, dimension 2** is not a contradiction, it is two
        rulers reporting on the same set. That the union cannot be compressed below full
        dimension is the seed of everything that follows in higher dimensions.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 5. Why anyone cares: the harmonic-analysis tower

        Here a needle puzzle stops being a curiosity. It sits at the **bottom** of a tower of
        central conjectures in Fourier analysis (the mathematics of breaking a signal into pure
        tones). The bridge is the **uncertainty principle**: a thin sliver in frequency
        corresponds to a long thin tube in space, and tubes pointing every which way are exactly
        a Besicovitch configuration.

        The tower's rungs, from weakest to strongest:

        $$
        \text{local smoothing} \Rightarrow \text{Bochner-Riesz} \Rightarrow \text{restriction} \Rightarrow \text{Kakeya}.
        $$

        Kakeya is the *weakest* statement, so every stronger one needs it: a single counterexample
        to Kakeya would topple the whole tower. The diagram below is the map; the rest of the
        section then builds it from the floor up, first Kakeya's own analytic form, then the Fourier
        vocabulary the rungs are stated in, then Fefferman's 1971 counterexample that first tied the
        puzzle to analysis, and finally the three stronger rungs themselves.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, np):
    _rungs = [
        ("Kakeya", "geometry: needles / tubes", 0, "known n≤3, open n≥4", COLORS["secondary"]),
        ("restriction", "Fourier transform on a curved surface", 1, "known n=2", COLORS["tertiary"]),
        ("Bochner-Riesz", "softened frequency cutoff", 2, "known n=2", COLORS["primary"]),
        ("local smoothing", "wave equation, averaged in time", 3, "known n=2", COLORS["quaternary"]),
    ]
    _fig = go.Figure()
    for _name, _gloss, _lvl, _status, _col in _rungs:
        _w = 3.4 - 0.5 * _lvl
        _fig.add_trace(
            go.Scatter(
                x=[-_w / 2, _w / 2, _w / 2, -_w / 2, -_w / 2],
                y=[_lvl - 0.32, _lvl - 0.32, _lvl + 0.32, _lvl + 0.32, _lvl - 0.32],
                mode="lines",
                fill="toself",
                fillcolor=_col,
                opacity=0.30,
                line={"color": _col, "width": 2},
                showlegend=False,
            )
        )
        _fig.add_annotation(
            x=0, y=_lvl + 0.09, text=f"<b>{_name}</b>", showarrow=False, font={"color": COLORS["text"], "size": 15}
        )
        _fig.add_annotation(
            x=0,
            y=_lvl - 0.16,
            text=f"{_gloss}  ·  {_status}",
            showarrow=False,
            font={"color": COLORS["text_secondary"], "size": 10},
        )
    for _lvl in range(3):
        _fig.add_annotation(
            x=0,
            y=_lvl + 0.5,
            ax=0,
            ay=_lvl + 0.5,
            text="⇓ implies",
            showarrow=False,
            font={"color": COLORS["muted"], "size": 11},
        )

    _fig.update_layout(**base_layout(title="The tower, Kakeya at the base", height=460))
    _fig.update_xaxes(range=[-2.0, 2.0], visible=False)
    _fig.update_yaxes(range=[-0.6, 3.7], visible=False)
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Each rung implies the one below it, so Kakeya sits at the base as the weakest and widest
        block. The plane case ($n = 2$) is known all the way up; every rung is still open in higher
        dimensions. We build up to each rung below, after the Fourier tools they are written in.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The version the harmonic analysts actually chase is the **Kakeya maximal function
        conjecture**. For each direction $\omega$, average $|f|$ over the *best* $\delta$-tube
        pointing along $\omega$ (the one where the average is largest); call that best-per-direction
        value $f^{*}_\delta(\omega)$. The conjecture says this greedy tube-averaging barely amplifies
        anything, only a loss slower than any power of $\delta$:

        $$
        \| f^{*}_\delta \|_{L^n(S^{n-1})} \ \le\ C_\varepsilon\, \delta^{-\varepsilon}\, \| f \|_{L^n(\mathbb{R}^n)}
        \qquad \text{for every } \varepsilon > 0.
        $$

        The link to dimension is contrapositive: if a Kakeya set could be squeezed below full
        dimension, an $f$ concentrated on it would have large tube averages in *every* direction at
        once, making $f^{*}_\delta$ big across the whole sphere and breaking the bound. So the
        analytic conjecture is exactly the statement that Besicovitch compression cannot beat full
        dimension.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, make_subplots, math, np, play_pause, style_subplot_axes):
    _gu = np.linspace(-1.0, 1.0, 120)
    _GX, _GY = np.meshgrid(_gu, _gu)
    _blobs = [(-0.35, 0.1, 0.18, 1.0), (0.3, -0.25, 0.14, 0.85), (0.05, 0.45, 0.12, 0.6)]
    _f = np.zeros_like(_GX)
    for _bx, _by, _sig, _amp in _blobs:
        _f += _amp * np.exp(-((_GX - _bx) ** 2 + (_GY - _by) ** 2) / (2 * _sig**2))

    _angles = np.linspace(0, math.pi, 30, endpoint=False)
    _width = 0.12
    _offsets = np.linspace(-0.8, 0.8, 21)

    def _best_tube(a):
        _u = np.array([math.cos(a), math.sin(a)])
        _perp = np.array([-math.sin(a), math.cos(a)])
        _along = _GX * _u[0] + _GY * _u[1]
        _across = _GX * _perp[0] + _GY * _perp[1]
        _best, _bestc = 0.0, 0.0
        for _c in _offsets:
            _mask = (np.abs(_across - _c) <= _width / 2) & (np.abs(_along) <= 0.5)
            if _mask.any():
                _val = float(_f[_mask].mean())
                if _val > _best:
                    _best, _bestc = _val, _c
        return _best, _bestc

    _star = np.array([_best_tube(_a) for _a in _angles])
    _fstar, _cbest = _star[:, 0], _star[:, 1]

    def _probe(a, c):
        _u = np.array([math.cos(a), math.sin(a)])
        _perp = np.array([-math.sin(a), math.cos(a)])
        _ctr = c * _perp
        _corners = np.array(
            [
                _ctr - 0.5 * _u - (_width / 2) * _perp,
                _ctr + 0.5 * _u - (_width / 2) * _perp,
                _ctr + 0.5 * _u + (_width / 2) * _perp,
                _ctr - 0.5 * _u + (_width / 2) * _perp,
                _ctr - 0.5 * _u - (_width / 2) * _perp,
            ]
        )
        return _corners[:, 0], _corners[:, 1]

    _fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=("A δ-tube swept over |f|, best offset per direction", "f*(ω): best tube-average vs direction"),
    )
    _fig.add_trace(
        go.Heatmap(x=_gu, y=_gu, z=_f, colorscale="Viridis", showscale=False, hoverinfo="skip"), row=1, col=1
    )
    _px0, _py0 = _probe(_angles[0], _cbest[0])
    _fig.add_trace(
        go.Scatter(x=_px0, y=_py0, mode="lines", line={"color": COLORS["highlight"], "width": 2}, showlegend=False),
        row=1,
        col=1,
    )
    _fig.add_trace(
        go.Scatter(
            x=np.degrees(_angles[:1]),
            y=_fstar[:1],
            mode="lines+markers",
            line={"color": COLORS["secondary"], "width": 3},
            showlegend=False,
        ),
        row=1,
        col=2,
    )

    _frames = []
    for _k in range(len(_angles)):
        _px, _py = _probe(_angles[_k], _cbest[_k])
        _frames.append(
            go.Frame(
                data=[
                    go.Scatter(x=_px, y=_py),
                    go.Scatter(x=np.degrees(_angles[: _k + 1]), y=_fstar[: _k + 1]),
                ],
                traces=[1, 2],
                name=str(_k),
            )
        )
    _fig.frames = _frames

    _fig.update_layout(**base_layout(title="The Kakeya maximal function", height=430))
    _fig.update_xaxes(range=[-1, 1], scaleanchor="y", constrain="domain", showticklabels=False, row=1, col=1)
    _fig.update_yaxes(range=[-1, 1], showticklabels=False, row=1, col=1)
    _fig.update_xaxes(title_text="direction ω (degrees)", row=1, col=2)
    _fig.update_yaxes(title_text="f*(ω)", row=1, col=2)
    style_subplot_axes(_fig, show_ticklabels=True)
    _fig.update_layout(updatemenus=play_pause("▶ Sweep the probe tube"))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Left: a fixed test function $|f|$ (three bright blobs) with a $\delta$-tube swept through
        every direction, snapping to the offset where its average is largest. Right: that
        best-per-direction average $f^{*}_\delta(\omega)$, peaking where a tube can line up along the
        blobs. The conjecture bounds this whole curve at once; a Kakeya set squeezed below full
        dimension would let $f^{*}_\delta$ spike in *every* direction, which is what it forbids.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### The Fourier vocabulary the tower is stated in

        The tower is written in Fourier terms, so fix the pieces. The **Fourier transform** is a
        recipe book: any signal is a stack of pure tones, $\widehat{f}(\xi)$ records how much of
        each tone $\xi$ the recipe calls for, and the inverse transform stacks the tones back into
        the signal.

        $$
        \begin{aligned}
        \widehat{f}(\xi) &= \int_{\mathbb{R}^n} f(x)\, e^{-2\pi i x\cdot\xi}\, dx
           && \text{read off how much of tone } \xi \text{ the signal holds} \\
        f(x) &= \int_{\mathbb{R}^n} \widehat{f}(\xi)\, e^{2\pi i x\cdot\xi}\, d\xi
           && \text{stack the tones back into the signal.}
        \end{aligned}
        $$

        Summing the tones a few at a time already rebuilds the signal, with a telltale overshoot at
        jumps (the Gibbs ripple).
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, make_subplots, math, np, play_pause, style_subplot_axes):
    _x = np.linspace(-math.pi, math.pi, 600)
    _target = np.sign(np.sin(_x))
    _ks = list(range(1, 22, 2))

    def _partial(n_terms):
        _s = np.zeros_like(_x)
        for _k in _ks[:n_terms]:
            _s += (4.0 / (math.pi * _k)) * np.sin(_k * _x)
        return _s

    _amp = [4.0 / (math.pi * _k) for _k in _ks]

    _fig = make_subplots(
        rows=1,
        cols=2,
        column_widths=[0.62, 0.38],
        subplot_titles=("Square wave from its harmonics", "Amplitude spectrum 4/(πk)"),
    )
    _fig.add_trace(
        go.Scatter(
            x=_x,
            y=_target,
            mode="lines",
            line={"color": COLORS["muted"], "width": 1.5, "dash": "dot"},
            showlegend=False,
        ),
        row=1,
        col=1,
    )
    _fig.add_trace(
        go.Scatter(
            x=_x, y=_partial(1), mode="lines", line={"color": COLORS["primary"], "width": 2.5}, showlegend=False
        ),
        row=1,
        col=1,
    )
    _fig.add_trace(go.Bar(x=_ks[:1], y=_amp[:1], marker={"color": COLORS["secondary"]}, showlegend=False), row=1, col=2)

    _frames = []
    for _n in range(1, len(_ks) + 1):
        _frames.append(
            go.Frame(
                data=[go.Scatter(x=_x, y=_partial(_n)), go.Bar(x=_ks[:_n], y=_amp[:_n])],
                traces=[1, 2],
                name=str(_n),
            )
        )
    _fig.frames = _frames

    _fig.update_layout(**base_layout(title="A signal as a stack of pure tones", height=400))
    _fig.update_xaxes(showticklabels=False, row=1, col=1)
    _fig.update_yaxes(range=[-1.4, 1.4], showticklabels=False, row=1, col=1)
    _fig.update_xaxes(title_text="harmonic k", row=1, col=2)
    _fig.update_yaxes(title_text="amplitude", row=1, col=2)
    style_subplot_axes(_fig, show_ticklabels=True)
    _fig.update_layout(updatemenus=play_pause("▶ Add harmonics"))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Each play step adds the next odd harmonic. The partial sum (cyan) closes in on the square
        wave (dotted), while the spectrum on the right shows the tones it is made of. The overshoot
        near the jumps never quite vanishes: that is Gibbs, and it is the first hint that *how* you
        cut off the tones matters.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        A single **plane wave** $x \mapsto e^{2\pi i x\cdot\xi}$ is one pure tone spread across
        space: its wavefronts are flat, perpendicular to $\xi$, spaced by the wavelength $1/|\xi|$.
        Higher frequency packs the fronts tighter.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, make_subplots, math, np, style_subplot_axes):
    _gu = np.linspace(-1, 1, 200)
    _GX, _GY = np.meshgrid(_gu, _gu)

    def _wave(xi):
        return np.cos(2 * math.pi * (xi[0] * _GX + xi[1] * _GY))

    _lo = np.array([2.0, 1.0])
    _hi = np.array([5.0, 2.5])
    _fig = make_subplots(rows=1, cols=2, subplot_titles=("Low frequency: wide fronts", "High frequency: tight fronts"))
    for _c, _xi in ((1, _lo), (2, _hi)):
        _fig.add_trace(
            go.Heatmap(x=_gu, y=_gu, z=_wave(_xi), colorscale="RdBu", showscale=False, hoverinfo="skip"), row=1, col=_c
        )
        _u = _xi / np.linalg.norm(_xi)
        _fig.add_trace(
            go.Scatter(
                x=[0, 0.5 * _u[0]],
                y=[0, 0.5 * _u[1]],
                mode="lines+markers",
                line={"color": COLORS["highlight"], "width": 3},
                showlegend=False,
            ),
            row=1,
            col=_c,
        )
    _fig.update_layout(**base_layout(title="A plane wave: flat fronts ⟂ ξ, spacing 1/|ξ|", height=380))
    for _c in (1, 2):
        _fig.update_xaxes(
            range=[-1, 1], scaleanchor="y" if _c == 1 else "y2", constrain="domain", showticklabels=False, row=1, col=_c
        )
        _fig.update_yaxes(range=[-1, 1], showticklabels=False, row=1, col=_c)
    style_subplot_axes(_fig)
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The same tone at two frequencies. The arrow points along $\xi$; the stripes are the
        wavefronts, always perpendicular to it and spaced $1/|\xi|$ apart. Raising the frequency
        (right) packs the fronts closer, the reciprocity that the uncertainty principle makes exact
        next.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The **uncertainty principle** is reciprocal zooming: squeeze a wave into a narrow frequency
        range and it must spread out in space, like a beam that can be narrow or straight but not
        both. A bump on an $r \times s$ box in frequency spreads over the dual $\tfrac1r \times
        \tfrac1s$ box in space (reciprocal side lengths, area product $\sim 1$):

        $$
        \text{frequency box } r \times s \quad\longleftrightarrow\quad \text{physical spread } \tfrac1r \times \tfrac1s .
        $$

        This is the **bridge to Kakeya**: a thin, curved sliver of frequency becomes a long, thin
        tube in physical space, and tubes in many directions are exactly a Besicovitch
        configuration.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, make_subplots, np, play_pause, style_subplot_axes):
    _rs = np.linspace(0.5, 0.08, 16)
    _s = 0.35

    def _rect(xh, yh):
        return [-xh, xh, xh, -xh, -xh], [-yh, -yh, yh, yh, -yh]

    def _freq_box(r):
        return _rect(r / 2, _s / 2)

    def _phys_box(r):
        return _rect(0.2 / r, 0.2 / _s)

    _fig = make_subplots(rows=1, cols=2, subplot_titles=("Frequency box r × s", "Physical spread 1/r × 1/s"))
    _fx, _fy = _freq_box(_rs[0])
    _fig.add_trace(
        go.Scatter(
            x=_fx,
            y=_fy,
            mode="lines",
            fill="toself",
            fillcolor="rgba(255,107,107,0.30)",
            line={"color": COLORS["secondary"], "width": 2},
            showlegend=False,
        ),
        row=1,
        col=1,
    )
    _hx, _hy = _phys_box(_rs[0])
    _fig.add_trace(
        go.Scatter(
            x=_hx,
            y=_hy,
            mode="lines",
            fill="toself",
            fillcolor="rgba(0,212,255,0.20)",
            line={"color": COLORS["primary"], "width": 2},
            showlegend=False,
        ),
        row=1,
        col=2,
    )

    _frames = []
    for _k, _r in enumerate(_rs):
        _fx, _fy = _freq_box(_r)
        _hx, _hy = _phys_box(_r)
        _frames.append(go.Frame(data=[go.Scatter(x=_fx, y=_fy), go.Scatter(x=_hx, y=_hy)], traces=[0, 1], name=str(_k)))
    _fig.frames = _frames

    _fig.update_layout(**base_layout(title="Thin in frequency ⟺ long in space", height=380))
    _fig.update_xaxes(range=[-0.6, 0.6], scaleanchor="y", constrain="domain", showticklabels=False, row=1, col=1)
    _fig.update_yaxes(range=[-0.6, 0.6], showticklabels=False, row=1, col=1)
    _fig.update_xaxes(range=[-3, 3], showticklabels=False, row=1, col=2)
    _fig.update_yaxes(range=[-1.2, 1.2], showticklabels=False, row=1, col=2)
    style_subplot_axes(_fig)
    _fig.update_layout(updatemenus=play_pause("▶ Thin the frequency box"))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        As the frequency box (left, coral) is thinned, its dual in physical space (right, cyan)
        stretches into a long thin tube. That is the whole bridge in one picture: a sliver of
        frequency tangent to a curved surface dualizes to a needle-like tube, and a surface's worth
        of tangent directions gives a needle in every direction.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Fefferman, 1971: where the tube geometry first bit

        Fefferman asked the most basic convergence question there is. To rebuild a signal from its
        Fourier recipe you sum the tones one cutoff at a time; the natural higher-dimensional cutoff
        is a **ball** (keep every tone with $|\xi| \le R$, then let $R \to \infty$). For $p = 2$ the
        energy bookkeeping says the partial sums converge. Fefferman's answer for every other $p$ is
        **no**, and the reason is the needle puzzle. The boundary of the frequency ball is *curved*,
        so by the uncertainty principle each thin slab tangent to the sphere dualizes to a long thin
        tube, and those tubes pile up exactly as needles do in a Besicovitch set. A geometry puzzle
        controls the convergence of Fourier series in dimension 2 and up.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, circle, go, make_subplots, math, np, style_subplot_axes):
    _r = 0.12
    _hl_freq, _th_freq = _r / 2.0, _r**2
    _tube_L = 0.9
    _tube_w = _tube_L * _r
    _hi_deg = 45.0
    _cx, _cy = circle(1.0, 220)

    def _slab(a_deg):
        _a = math.radians(a_deg)
        _pt = np.array([math.cos(_a), math.sin(_a)])
        _tan = np.array([-math.sin(_a), math.cos(_a)])
        _corners = np.array(
            [
                _pt - _hl_freq * _tan,
                _pt + _hl_freq * _tan,
                _pt + _hl_freq * _tan + _th_freq * _pt,
                _pt - _hl_freq * _tan + _th_freq * _pt,
                _pt - _hl_freq * _tan,
            ]
        )
        return _corners[:, 0], _corners[:, 1]

    def _dual_tube(a_deg):
        _a = math.radians(a_deg)
        _rho = np.array([math.cos(_a), math.sin(_a)])
        _tan = np.array([-math.sin(_a), math.cos(_a)])
        _corners = np.array(
            [
                -_tube_L * _rho - _tube_w * _tan,
                _tube_L * _rho - _tube_w * _tan,
                _tube_L * _rho + _tube_w * _tan,
                -_tube_L * _rho + _tube_w * _tan,
                -_tube_L * _rho - _tube_w * _tan,
            ]
        )
        return _corners[:, 0], _corners[:, 1]

    _fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=(
            "Frequency: r × r² slabs tangent to the ball",
            "Space: dual tubes, length : width = 1/r",
        ),
    )
    _fig.add_trace(
        go.Scatter(x=_cx, y=_cy, mode="lines", line={"color": COLORS["grid"]}, showlegend=False), row=1, col=1
    )
    for _adeg in np.arange(0, 360, 15):
        _sx, _sy = _slab(_adeg)
        _is_hi = abs(_adeg - _hi_deg) < 1e-6
        _fig.add_trace(
            go.Scatter(
                x=_sx,
                y=_sy,
                mode="lines",
                fill="toself",
                fillcolor="rgba(255,230,109,0.9)" if _is_hi else "rgba(255,107,107,0.35)",
                line={"color": COLORS["highlight"] if _is_hi else COLORS["secondary"], "width": 1.6 if _is_hi else 0.5},
                showlegend=False,
            ),
            row=1,
            col=1,
        )
    for _adeg in np.arange(0, 180, 15):
        _tx, _ty = _dual_tube(_adeg)
        _is_hi = abs(_adeg - _hi_deg) < 1e-6
        _fig.add_trace(
            go.Scatter(
                x=_tx,
                y=_ty,
                mode="lines",
                fill="toself",
                fillcolor="rgba(255,230,109,0.35)" if _is_hi else "rgba(0,212,255,0.12)",
                line={"color": COLORS["highlight"] if _is_hi else COLORS["primary"], "width": 1.6 if _is_hi else 0.5},
                showlegend=False,
            ),
            row=1,
            col=2,
        )
    _fig.update_layout(**base_layout(title="Fefferman's ball multiplier: each slab dualizes to a tube", height=400))
    _fig.update_xaxes(range=[-1.4, 1.4], scaleanchor="y", constrain="domain", showticklabels=False, row=1, col=1)
    _fig.update_yaxes(range=[-1.4, 1.4], showticklabels=False, row=1, col=1)
    _fig.update_xaxes(range=[-1.1, 1.1], scaleanchor="y2", constrain="domain", showticklabels=False, row=1, col=2)
    _fig.update_yaxes(range=[-1.1, 1.1], showticklabels=False, row=1, col=2)
    style_subplot_axes(_fig)
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Left: slabs tangent to the frequency ball, each $r$ wide along the tangent and $r^2$ thick
        radially. Right: the dual of each slab is a tube pointing *radially*, length $1/r^2$ and
        width $1/r$, so its length-to-width ratio is exactly $1/r$ (both panels drawn to one
        consistent scale). The highlighted pair is one slab and the tube it becomes; antipodal slabs
        share a tube, so the boundary's directions give tubes pointing every which way through the
        origin, a Besicovitch configuration. Fefferman turned that pile-up into a genuine
        counterexample: the sharp ball cutoff fails to reconstruct signals in $L^p$ for $p \ne 2$,
        $n \ge 2$.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### The three rungs above Kakeya

        Back to the map. Each rung is a stronger statement resting on the one below, and each has a
        plain reading.

        **Restriction** (Stein). A wave built only from a curved surface's tones cannot stay bunched
        up: it has to leak energy and fade as it spreads. With the extension operator
        $E g(x) = \int_{S^{n-1}} g(\omega)\, e^{2\pi i x\cdot\omega}\, d\sigma(\omega)$,

        $$
        \| E g \|_{L^q(\mathbb{R}^n)} \ \lesssim\ \| g \|_{L^\infty(S^{n-1})}
        \qquad\text{for all } q > \tfrac{2n}{n-1}.
        $$

        The threshold $q > 2n/(n-1)$ is sharp (the extension of a bump decays like
        $|x|^{-(n-1)/2}$). Proven for $n = 2$, open for $n \ge 3$.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        **Bochner-Riesz.** Fefferman showed the sharp ball cutoff rings like a badly tuned
        instrument. Softening it, fading the tones out gently near the boundary with an exponent
        $\alpha \ge 0$, is meant to fix that:

        $$
        B_R^{\alpha} f(x) = \int_{B(0,R)} e^{2\pi i x\cdot\xi}
        \Big(1 - \tfrac{|\xi|^2}{R^2}\Big)^{\alpha} \widehat{f}(\xi)\, d\xi .
        $$

        At $\alpha = 0$ this is Fefferman's failing cutoff; the conjecture says that as soon as
        $\alpha > 0$ a range of $p$ beyond the trivial $p = 2$ has $\|B_R^\alpha f - f\|_{L^p} \to 0$.
        Proven for $n = 2$, open for $n \ge 3$, and **Bochner-Riesz $\Rightarrow$ Kakeya**.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, np, play_pause, style_subplot_axes):
    _u = np.linspace(0, 1.15, 300)
    _base = np.clip(1 - _u**2, 0, None)
    _alphas = np.linspace(0, 2, 17)

    def _mult(al):
        return _base**al if al > 0 else (_u <= 1).astype(float)

    _fig = go.Figure()
    _fig.add_trace(
        go.Scatter(x=_u, y=_mult(0.0), mode="lines", line={"color": COLORS["secondary"], "width": 3}, showlegend=False)
    )
    _fig.add_vline(x=1.0, line={"color": COLORS["muted"], "width": 1, "dash": "dot"})

    _frames = [
        go.Frame(
            data=[go.Scatter(x=_u, y=_mult(_al))],
            traces=[0],
            name=f"{_al:.2f}",
            layout={"title": {"text": f"Bochner-Riesz multiplier (1 − |ξ|²/R²)₊^α,  α = {_al:.2f}"}},
        )
        for _al in _alphas
    ]
    _fig.frames = _frames

    _fig.update_layout(**base_layout(title="Bochner-Riesz multiplier (1 − |ξ|²/R²)₊^α,  α = 0.00", height=400))
    _fig.update_xaxes(title_text="|ξ| / R")
    _fig.update_yaxes(title_text="multiplier weight", range=[-0.05, 1.08])
    style_subplot_axes(_fig, show_ticklabels=True)
    _fig.update_layout(updatemenus=play_pause("▶ Soften the cutoff"))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        At $\alpha = 0$ the multiplier is a hard step at $|\xi| = R$, Fefferman's failing cutoff. As
        $\alpha$ grows the edge fades in smoothly, and the conjecture is that any positive softening
        already restores convergence for a range of $p$.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        **Local smoothing** (Sogge, top of the tower). A wave frozen at one instant can spike badly;
        watched over a short time interval the spikes move around, so the *time average* is smoother
        than any frozen frame. For the half-wave propagator $e^{it\sqrt{-\Delta}}$,

        $$
        \Big(\int_1^2 \big\| e^{it\sqrt{-\Delta}} f \big\|_{L^p(\mathbb{R}^n)}^{p}\, dt\Big)^{1/p}
        \ \lesssim\ \| f \|_{L^p_{\,s_p - \sigma}},
        \qquad s_p = (n-1)\big|\tfrac12 - \tfrac1p\big|,
        $$

        averaging in time buys back regularity a single slice cannot. It is the strongest rung:
        **local smoothing $\Rightarrow$ Bochner-Riesz, restriction, and Kakeya** (Tao). Known for
        $n = 2$ (Guth-Wang-Zhang 2020), open for $n \ge 3$.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, circle, go, make_subplots, np, style_subplot_axes):
    _fig = make_subplots(
        rows=1, cols=2, subplot_titles=("Wavefronts |x| = t expanding", "Space-time: energy on the cone |x| = t")
    )
    for _t, _op in ((0.3, 0.4), (0.5, 0.6), (0.7, 0.8), (0.9, 1.0)):
        _wx, _wy = circle(_t, 160)
        _fig.add_trace(
            go.Scatter(
                x=_wx, y=_wy, mode="lines", line={"color": COLORS["primary"], "width": 2}, opacity=_op, showlegend=False
            ),
            row=1,
            col=1,
        )
    _fig.add_trace(
        go.Scatter(x=[0], y=[0], mode="markers", marker={"color": COLORS["highlight"], "size": 7}, showlegend=False),
        row=1,
        col=1,
    )
    _xx = np.linspace(-1, 1, 120)
    _fig.add_trace(
        go.Scatter(
            x=_xx, y=np.abs(_xx), mode="lines", line={"color": COLORS["secondary"], "width": 3}, showlegend=False
        ),
        row=1,
        col=2,
    )
    _fig.add_trace(
        go.Scatter(x=[0], y=[0], mode="markers", marker={"color": COLORS["highlight"], "size": 7}, showlegend=False),
        row=1,
        col=2,
    )
    _fig.update_layout(**base_layout(title="Local smoothing: a wavefront concentrated on the cone", height=380))
    _fig.update_xaxes(range=[-1, 1], scaleanchor="y", constrain="domain", showticklabels=False, row=1, col=1)
    _fig.update_yaxes(range=[-1, 1], showticklabels=False, row=1, col=1)
    _fig.update_xaxes(title_text="position x", row=1, col=2)
    _fig.update_yaxes(title_text="time t", range=[-0.05, 1.05], row=1, col=2)
    style_subplot_axes(_fig, show_ticklabels=True)
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Left: a point source sends out wavefronts $|x| = t$ that concentrate the wave's energy on
        expanding circles. Right, in space-time, that energy rides the light cone $|x| = t$ (the V).
        At a single time slice the wave can spike on the circle; averaging over the time interval
        smears the spike along the cone, which is the regularity local smoothing buys back.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Why should a geometry fact control an analysis fact? Because the uncertainty principle
        turns every frequency question into a question about how tubes in many directions pack in
        space, and packing tubes is exactly Kakeya. Points (a segment's worth) versus tubes
        (fattened segments) is the same bookkeeping as waves concentrated along light rays. That
        is how a 1917 puzzle became load-bearing.

        Settling the plane leaves the obvious question: does "zero volume, full dimension" hold in
        space too?
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 6. The three-dimensional conjecture

        > **3D Kakeya (now a theorem, Wang-Zahl 2025).** Every Kakeya set in $\mathbb{R}^3$ has
        > Minkowski and Hausdorff dimension 3.

        Fatten every segment into a **$\delta$-tube**: a cylinder of length 1 and radius $\delta$
        (dimensions $\delta \times \delta \times 1$). Directions are $\delta$-separated on the
        sphere $S^2$, so there are about $\delta^{-2}$ tubes, and the total tube content is pinned:

        $$
        \#\mathbb{T} \cdot |T| \sim \delta^{-2} \cdot \delta^2 = 1,
        \qquad |N_\delta K| \sim \delta^{\,3 - d}.
        $$

        Dimension $d = 3$ is exactly the case $3 - d = 0$: refining the tubes cannot drain the
        union. A dimension-$5/2$ set would shed about 29% of its volume at every halving of
        $\delta$, draining to zero.

        But three dimensions is genuinely harder than two: in the plane two lines in different
        directions almost always **cross**, while in space two tubes in different directions
        generically **miss** (skew lines pass by without touching). The 2D argument "different
        directions force crossings force spread" has no direct analogue.
        """
    )
    return


@app.cell
def _(COLORS, SCENE_THEME, base_layout, go, np, play_pause):
    def _fibonacci_sphere(n):
        _i = np.arange(n) + 0.5
        _phi = np.arccos(1 - 2 * _i / n)
        _theta = np.pi * (1 + 5**0.5) * _i
        return np.column_stack([np.sin(_phi) * np.cos(_theta), np.sin(_phi) * np.sin(_theta), np.cos(_phi)])

    def _delta_separated(points, delta):
        _kept = np.empty((0, 3))
        for _p in points:
            if _kept.shape[0] == 0 or np.min(np.linalg.norm(_kept - _p, axis=1)) >= delta:
                _kept = np.vstack([_kept, _p])
        return _kept

    def _tube_frame(direction):
        _u = direction / np.linalg.norm(direction)
        _tmp = np.array([1.0, 0.0, 0.0]) if abs(_u[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
        _v = np.cross(_u, _tmp)
        _v /= np.linalg.norm(_v)
        _w = np.cross(_u, _v)
        return _u, _v, _w

    def _tube(center, direction, radius=0.045, length=1.0):
        _u, _v, _w = _tube_frame(direction)
        _theta = np.linspace(0, 2 * np.pi, 12)
        _s = np.linspace(-length / 2, length / 2, 2)
        _S, _T = np.meshgrid(_s, _theta)
        _X = center[0] + _S * _u[0] + radius * (np.cos(_T) * _v[0] + np.sin(_T) * _w[0])
        _Y = center[1] + _S * _u[1] + radius * (np.cos(_T) * _v[1] + np.sin(_T) * _w[1])
        _Z = center[2] + _S * _u[2] + radius * (np.cos(_T) * _v[2] + np.sin(_T) * _w[2])
        return _X, _Y, _Z

    _rng = np.random.default_rng(7)
    _dirs = _delta_separated(_fibonacci_sphere(2500), 0.55)
    _dirs = _dirs[_dirs[:, 2] > 0][:14]

    _fig = go.Figure()
    for _d in _dirs:
        _c = _rng.uniform(-0.18, 0.18, 3)
        _X, _Y, _Z = _tube(_c, _d)
        _fig.add_trace(
            go.Surface(
                x=_X,
                y=_Y,
                z=_Z,
                showscale=False,
                opacity=0.85,
                colorscale=[[0, COLORS["primary"]], [1, COLORS["tertiary"]]],
                hoverinfo="skip",
                showlegend=False,
            )
        )

    _scene = {
        **SCENE_THEME,
        "aspectmode": "data",
        "camera": {"eye": {"x": 1.6, "y": 1.6, "z": 1.1}},
    }
    _fig.update_layout(
        **base_layout(title="δ×δ×1 tubes in δ-separated directions (skew, they miss)", height=560, scene=_scene)
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Drag to rotate: a bundle of $\delta \times \delta \times 1$ tubes pointing in
        $\delta$-separated directions. From most viewpoints the tubes pass one another without
        touching, the skew arrangement that the plane never has.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        With no crossings to lean on, the proof trades "which tube meets which" for a single
        local packing rule, the **Wolff axiom**: for every rectangular prism $R$,

        $$
        \#\{T \in \mathbb{T} : T \subseteq R\} \le \delta^{-2}\,|R|.
        $$

        No prism swallows more tubes than its volume allows. That rules out the degenerate "all
        tubes in one thin slab" cheat, is checkable one prism at a time, and needs no global
        arrangement. From it Wolff (1995) extracted the first bound past the trivial ones,
        dimension $\ge 5/2$. Then progress stalled there for decades.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 7. Solving three dimensions: sticky, grains, induction

        The Wolff axiom stalls at $5/2$, a half-dimension short of 3: capping the crudest
        concentration is not the same as ruling out the finer ways tubes overlap. Wang and Zahl
        (2025) closed the gap. Two ideas do the work.

        **Sticky reduction.** Zoom out so thin $\delta$-tubes blur into fatter $\rho$-tubes and
        ask how the thin ones sit inside the fat ones. In the **sticky** case they clump as much
        as possible: each fat tube holds about $(\rho/\delta)^2$ thin ones, and the picture repeats
        as you zoom (statistically self-similar, like a comb). In the **non-sticky** case they
        scatter, like tossed sticks. The key move (Hickman calls it the single most important
        step): it *suffices* to prove the bound for sticky tubes.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, make_subplots, np, style_subplot_axes):
    _rho, _delta = 0.25, 0.0625
    _k = round(_rho / _delta)
    _offs = (np.arange(_k) - (_k - 1) / 2) * _delta
    _gx, _gy = np.meshgrid(_offs, _offs)
    _sub = np.column_stack([_gx.ravel(), _gy.ravel()])
    _rng = np.random.default_rng(11)

    _fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=(f"Sticky: {_k * _k} thin tubes clump in the fat tube", "Non-sticky: same count, scattered"),
    )
    _fat_x = [-_rho / 2, _rho / 2, _rho / 2, -_rho / 2, -_rho / 2]
    _fat_y = [-_rho / 2, -_rho / 2, _rho / 2, _rho / 2, -_rho / 2]
    for _c in (1, 2):
        _fig.add_trace(
            go.Scatter(
                x=_fat_x, y=_fat_y, mode="lines", line={"color": COLORS["quaternary"], "width": 2}, showlegend=False
            ),
            row=1,
            col=_c,
        )
    _fig.add_trace(
        go.Scatter(
            x=_sub[:, 0], y=_sub[:, 1], mode="markers", marker={"color": COLORS["primary"], "size": 7}, showlegend=False
        ),
        row=1,
        col=1,
    )
    _scatter = _rng.uniform(-_rho / 2, _rho / 2, size=(_k * _k, 2))
    _fig.add_trace(
        go.Scatter(
            x=_scatter[:, 0],
            y=_scatter[:, 1],
            mode="markers",
            marker={"color": COLORS["secondary"], "size": 7},
            showlegend=False,
        ),
        row=1,
        col=2,
    )

    _fig.update_layout(**base_layout(title="Occupancy of a fat tube's cross-section", height=380))
    for _c in (1, 2):
        _fig.update_xaxes(
            range=[-0.16, 0.16],
            scaleanchor="y" if _c == 1 else "y2",
            constrain="domain",
            showticklabels=False,
            row=1,
            col=_c,
        )
        _fig.update_yaxes(range=[-0.16, 0.16], showticklabels=False, row=1, col=_c)
    style_subplot_axes(_fig)
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Cross-section of one fat tube. Left, sticky: the thin tubes fill it in a regular grid,
        about $(\rho/\delta)^2$ of them, the same picture at every zoom. Right, non-sticky: the
        same number scattered, with no repeating structure. The proof reduces to the sticky case.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        **Grains.** Counting tubes directly is hopeless (a pair can cross, miss, or run nearly
        parallel at every scale). Guth's graininess, carried from Dvir's finite-field polynomial
        method into Euclidean space, says a near-counterexample must cluster into thin slabs, one
        tube thick, wider but much shorter than the tubes running through them, like the grain in a
        piece of wood:

        $$
        \text{grain} \approx \delta \times c \times c \qquad (\delta \ll c \ll 1).
        $$

        Within one fat tube the grains are essentially disjoint (they tile it), and grains from
        different fat tubes cannot overlap too much: **no point lies in too many grains.** That is
        the quantitative ceiling on compression.

        **Compression, quantified.** The Perron pile already shows compression numerically: its
        $2^n$ pieces are only translated, so their areas always sum to the whole triangle
        (content pinned at 1) while the union falls like $1/\log N$. Content over footprint is the
        compression: it climbs, but only $\log N$-slowly. The conjecture says compression can cost
        the volume everything but the dimension nothing.
        """
    )
    return


@app.cell
def _(COLORS, SQRT3, base_layout, go, make_subplots, np, perron_pieces, style_subplot_axes, union_area):
    _apex = (0.0, 1.0)
    _base_half = 1.0 / SQRT3
    _gu = np.linspace(-1.3, 1.3, 170)
    _gv = np.linspace(-0.05, 1.05, 85)
    _GX, _GY = np.meshgrid(_gu, _gv)
    _cellA = (_gu[1] - _gu[0]) * (_gv[1] - _gv[0])

    _base_area, _ = union_area(perron_pieces(1, 0.0, _apex, _base_half), _GX, _GY, _cellA)
    _levels = list(range(1, 9))
    _content = [1.0 for _ in _levels]
    _footprint = []
    for _n in _levels:
        _ar, _ = union_area(perron_pieces(_n, 0.6, _apex, _base_half), _GX, _GY, _cellA)
        _footprint.append(_ar / _base_area)
    _compression = [_c / _f for _c, _f in zip(_content, _footprint)]

    _fig = make_subplots(specs=[[{"secondary_y": True}]])
    _fig.add_trace(
        go.Scatter(
            x=_levels,
            y=_content,
            mode="lines+markers",
            line={"color": COLORS["quaternary"], "width": 3},
            name="content (pinned = 1)",
        )
    )
    _fig.add_trace(
        go.Scatter(
            x=_levels,
            y=_footprint,
            mode="lines+markers",
            line={"color": COLORS["primary"], "width": 3},
            name="footprint (falls)",
        )
    )
    _fig.add_trace(
        go.Scatter(
            x=_levels,
            y=_compression,
            mode="lines+markers",
            line={"color": COLORS["secondary"], "width": 3, "dash": "dot"},
            name="compression = content/footprint",
        ),
        secondary_y=True,
    )

    _fig.update_layout(**base_layout(title="Compression climbs, but only log-slowly", height=420))
    _fig.update_xaxes(title_text="Perron level n  (N = 2ⁿ slivers)")
    _fig.update_yaxes(title_text="fraction of the triangle", secondary_y=False)
    _fig.update_yaxes(title_text="compression", secondary_y=True)
    style_subplot_axes(_fig, show_ticklabels=True)
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The content (yellow) stays pinned at 1 while the footprint (cyan) falls with each Perron
        level, so their ratio, the compression (coral, right axis), climbs. It grows only
        $\log N$-slowly: real compression, but bounded, which is the ceiling the conjecture asserts.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        **Induction on scales.** The finish assumes the dimension bound at one scale and
        bootstraps to a slightly better one, repeating until $d$ reaches 3. The danger (Tao's
        "Chinese whispers": a rumor passed down a line, each retelling losing a little) is that
        each step leaks and the accumulated loss makes the conclusion worthless. Because grains
        within a fat tube are disjoint, Wang-Zahl replace the wasteful multiplicity bound by the
        multiplicity of the actual union, and the step **gains** instead of leaking. Graininess
        turns a lossy induction into one that ratchets the estimate up to exactly 3.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, create_timeline, go):
    _events = [
        (1995, "Wolff<br>≥ 5/2", 1),
        (2000, "Katz-Laba-Tao<br>Minkowski > 5/2", -1),
        (2017, "Katz-Zahl<br>Hausdorff ≥ 5/2 + ε", 1),
        (2025, "Wang-Zahl<br>= 3", -1),
    ]
    _fig = create_timeline(_events, title="R³ dimension lower bound: 5/2 → 3", x_range=(1991, 2030), height=340)
    _fig.add_hline(y=0, line={"color": COLORS["muted"], "width": 1})
    _fig.update_layout(
        **base_layout(title="R³ dimension lower bound: 5/2 → 3 (Hong Wang, 2026 Fields Medal)", height=340)
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The lower bound on the dimension of a Kakeya set in space, over three decades: stuck at
        Wolff's $5/2$ from 1995, nudged past it by Katz-Laba-Tao (2000) and Katz-Zahl (2017), and
        finally taken to the full 3 by Wang-Zahl in 2025.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        $$
        \boxed{\text{Wang-Zahl (2025): every Kakeya set in } \mathbb{R}^3 \text{ has Hausdorff and Minkowski dimension } 3.}
        $$

        This does not by itself prove restriction, Bochner-Riesz, or local smoothing (the tower's
        implications only run downward). But it removes the geometric floor's uncertainty and hands
        up the techniques, sticky reduction, grains, and non-leaking induction, that people now
        hope to carry up the tower. Hong Wang received the 2026 Fields Medal for this work with
        Zahl.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 8. Dimension four and up, still open

        The conjecture does not change with dimension: a Kakeya set in $\mathbb{R}^n$ should have
        dimension $n$. What changes is that nobody can prove it for $n \ge 4$. The proven lower
        bounds all sit strictly below $n$, and that shortfall *is* the open problem:

        $$
        \begin{aligned}
        \dim_H K &\ge \tfrac{n+2}{2}                 && \text{Wolff (1995), the hairbrush bound} \\
        \dim_H K &\ge (2 - \sqrt2)(n - 4) + 3        && \text{Katz-Tao (2002),}\ 2 - \sqrt2 \approx 0.586.
        \end{aligned}
        $$

        The two bounds **cross exactly at $n = 4$**, where both give 3: Wolff wins for
        $n = 2, 3, 4$, and Katz-Tao overtakes it for $n \ge 5$. Against a conjectured value of $n$,
        every method still falls short, and no argument yet forces the ratio $\dim_H K / n$ to
        1.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, math, np, style_subplot_axes):
    _n = np.arange(2, 13)
    _wolff = (_n + 2) / 2
    _katz = (2 - math.sqrt(2)) * (_n - 4) + 3
    _full = _n.astype(float)

    _fig = go.Figure()
    _fig.add_trace(
        go.Scatter(
            x=_n,
            y=_full,
            mode="lines+markers",
            line={"color": COLORS["quaternary"], "width": 3, "dash": "dash"},
            name="conjectured  dim = n",
        )
    )
    _fig.add_trace(
        go.Scatter(
            x=_n, y=_wolff, mode="lines+markers", line={"color": COLORS["primary"], "width": 3}, name="Wolff  (n+2)/2"
        )
    )
    _fig.add_trace(
        go.Scatter(
            x=_n,
            y=_katz,
            mode="lines+markers",
            line={"color": COLORS["secondary"], "width": 3},
            name="Katz-Tao  0.586(n−4)+3",
        )
    )
    _fig.add_trace(
        go.Scatter(
            x=[4],
            y=[3],
            mode="markers+text",
            marker={"color": COLORS["highlight"], "size": 12},
            text=["cross at n=4"],
            textposition="top center",
            textfont={"color": COLORS["highlight"]},
            showlegend=False,
        )
    )

    _fig.update_layout(**base_layout(title="Every proven bound falls short of n", height=440))
    _fig.update_xaxes(title_text="dimension n")
    _fig.update_yaxes(title_text="proven / conjectured lower bound")
    style_subplot_axes(_fig, show_ticklabels=True)
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The two proven bounds (Wolff and Katz-Tao) both stay below the conjectured $\dim = n$
        (dashed), touching it only where they cross, at $n = 4$. Wolff leads for $n = 2, 3, 4$;
        Katz-Tao overtakes it from $n = 5$ on. The gap to the dashed line is the open problem.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Because the tower's implications run **downward**, proving the $n \ge 4$ Kakeya conjecture
        would not by itself settle restriction, Bochner-Riesz, or local smoothing: Kakeya is a
        necessary floor, not a sufficient hypothesis. What genuinely propagates outward is the
        *toolkit*. The proven **multilinear Kakeya theorem** (Bennett-Carbery-Tao, 2006) drives
        $\ell^2$ **decoupling** (Bourgain-Demeter, 2015), which proves the **Vinogradov mean value
        theorem** (Bourgain-Demeter-Guth, 2016) and from there reaches analytic number theory
        (sharper exponential-sum and Riemann zeta-growth bounds) and PDE (pointwise convergence of
        the Schrödinger flow, Du-Zhang, 2019). So the expected payoff of $n \ge 4$ is methodological
        momentum, not a single toppling domino.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The story so far, in one line: a motion puzzle, then concrete shapes shrink the area, then
        the area hits zero, then area is the wrong ruler, then dimension, then the plane is solved
        at dimension 2, then the tower explains why it matters, then space is harder, and finally
        the 2025 machinery closes three dimensions. Four and up wait for the next idea.

        ---

        **Sources**

        - J. Hickman, *The Kakeya Conjecture: where does it come from and why is it important?*,
          [arXiv:2512.09842](https://arxiv.org/abs/2512.09842) (2025).
        - J. Zahl, *A Survey of the Kakeya conjecture, 2000-2025*,
          [arXiv:2512.09397](https://arxiv.org/abs/2512.09397).
        - H. Wang & J. Zahl, *Volume estimates for unions of convex sets, and the Kakeya set
          conjecture in three dimensions*, [arXiv:2502.17655](https://arxiv.org/abs/2502.17655)
          (2025).
        - T. Tao, *The three-dimensional Kakeya conjecture, after Wang and Zahl*
          ([blog](https://terrytao.wordpress.com/2025/02/25/the-three-dimensional-kakeya-conjecture-after-wang-and-zahl/), 2025).
        - Z. Dvir, *On the size of Kakeya sets in finite fields*, J. Amer. Math. Soc. 22 (2009).
        - K. J. Falconer, *The Geometry of Fractal Sets* (CUP, 1985); C. Fefferman, *The
          multiplier problem for the ball*, Ann. of Math. 94 (1971).
        - R. O. Davies (1971), 2D dimension; International Mathematical Union, *Fields Medals 2026*.
        """
    )
    return


if __name__ == "__main__":
    app.run()
