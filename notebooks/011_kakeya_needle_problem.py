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

    def deltoid_needle(t, b=0.25):
        """Endpoints of the unit needle held tangent to the deltoid at parameter t."""
        p, d = deltoid_point_dir(t, b)
        bx, by = deltoid(b, 500)
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

        The obvious answer spins the needle about its middle and fills a disc. Kakeya himself
        guessed one could do better, with the curved **deltoid**.
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
            range=[-0.62, 0.62],
            scaleanchor="y" if _c == 1 else "y2",
            constrain="domain",
            showticklabels=False,
            row=1,
            col=_c,
        )
        _fig.update_yaxes(range=[-0.62, 0.62], showticklabels=False, row=1, col=_c)
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
    for _c, _rng in ((1, 0.62), (2, 0.62), (3, 0.72)):
        _fig.update_xaxes(
            range=[-_rng, _rng],
            scaleanchor=f"y{'' if _c == 1 else _c}",
            constrain="domain",
            showticklabels=False,
            row=1,
            col=_c,
        )
        _fig.update_yaxes(range=[-0.62, 1.05] if _c == 3 else [-_rng, _rng], showticklabels=False, row=1, col=_c)
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
        disc but loses to the non-convex deltoid ($\pi/8$).
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
        in area as small as you like, but never zero.
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

        Area zero does not mean small in every sense. The rational numbers have zero length yet
        sit everywhere; the Cantor set has zero length yet is uncountable. Zero area means "no
        thickness," not "no points."

        The right ruler is **dimension**, measured by how the number of small boxes needed to
        cover a set grows as the boxes shrink. Cover with a grid of side $\delta$ and count the
        boxes $N(\delta)$ the set meets:

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

    def _seg_boxes(delta):
        _n = round(1.0 / delta)
        _cols = set()
        for _i in range(_n):
            _cols.add((_i, int(0.55 / delta)))
        return _n, _cols

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
    _union = [_width + 0.9 * (1 - math.exp(-0.6 * (m - 1))) for m in _counts]
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
        Left: a fan of $1 \times \delta$ rectangles at separated angles. Right: as directions are
        added, the summed area (coral) climbs in step with the count, but the union (cyan) saturates
        because the crossings barely overlap. Thin pieces, large union: the set stays spread out.
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
        to Kakeya would topple the whole tower. Fefferman (1971) used a Besicovitch construction
        to disprove the natural higher-dimensional "ball multiplier," showing that the plainest way
        of rebuilding a signal from its Fourier recipe fails in dimension 2 and up, and the failure
        is the needle puzzle in disguise.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, np, style_subplot_axes):
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
    style_subplot_axes(_fig)
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Each rung implies the one below it, so Kakeya sits at the base as the weakest and widest
        block. The plane case ($n = 2$) is known all the way up; every rung is still open in higher
        dimensions.
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
def _(COLORS, base_layout, create_timeline, go, style_subplot_axes):
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
    style_subplot_axes(_fig)
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
