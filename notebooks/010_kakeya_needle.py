"""
Kakeya: a turning needle, zero area, and full dimension.

A fresh walk through the Kakeya problem following `research/kakeya/kakeya.md`: the 1917
needle puzzle, the plane constructions that drive the swept area to zero, dimension as the
ruler that replaces area, the harmonic-analysis tower that rests on the problem, and the
2025 Wang-Zahl proof of the three-dimensional case (Hong Wang, 2026 Fields Medal).

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
    """Shared geometry helpers for the Kakeya notebook."""
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

    def needle_at(cx, cy, angle, length=1.0):
        """Endpoints of a segment of given length centred at (cx, cy) pointing at angle."""
        _hx, _hy = 0.5 * length * math.cos(angle), 0.5 * length * math.sin(angle)
        return np.array([cx - _hx, cx + _hx]), np.array([cy - _hy, cy + _hy])

    def circle(r=0.5, n=240, cx=0.0, cy=0.0):
        """Points tracing a circle of radius r centred at (cx, cy)."""
        _t = np.linspace(0, 2 * math.pi, n)
        return cx + r * np.cos(_t), cy + r * np.sin(_t)

    def deltoid(b=0.25, n=400):
        """The three-cusped hypocycloid at parameter samples: chord 4b, enclosed area 2 pi b^2."""
        _t = np.linspace(0, 2 * math.pi, n)
        return 2 * b * np.cos(_t) + b * np.cos(2 * _t), 2 * b * np.sin(_t) - b * np.sin(2 * _t)

    def deltoid_point_tangent(t, b=0.25):
        """A boundary point of the deltoid at parameter t and its unit tangent direction."""
        _p = np.array([2 * b * math.cos(t) + b * math.cos(2 * t), 2 * b * math.sin(t) - b * math.sin(2 * t)])
        _d = np.array([-2 * b * math.sin(t) - 2 * b * math.sin(2 * t), 2 * b * math.cos(t) - 2 * b * math.cos(2 * t)])
        _nrm = np.linalg.norm(_d)
        if _nrm < 1e-9:
            t += 1e-2
            _d = np.array(
                [-2 * b * math.sin(t) - 2 * b * math.sin(2 * t), 2 * b * math.cos(t) - 2 * b * math.cos(2 * t)]
            )
            _nrm = np.linalg.norm(_d)
        return _p, _d / _nrm

    def _polygon_chord(p, d, bx, by):
        """Endpoints where the line through p in direction d crosses the closed polygon (bx, by)."""
        _n = np.array([-d[1], d[0]])
        _f = (np.column_stack([bx, by]) - p) @ _n
        _s = (np.column_stack([bx, by]) - p) @ d
        _hits = []
        for _i in range(len(bx) - 1):
            _f0, _f1 = _f[_i], _f[_i + 1]
            if (_f0 < 0) != (_f1 < 0):
                _w = _f0 / (_f0 - _f1)
                _hits.append(_s[_i] + _w * (_s[_i + 1] - _s[_i]))
        if len(_hits) < 2:
            return p - 0.5 * d, p + 0.5 * d
        return p + min(_hits) * d, p + max(_hits) * d

    def deltoid_needle(t, b=0.25):
        """Endpoints of the unit needle held tangent to the deltoid at parameter t (chord 4b = 1)."""
        _p, _d = deltoid_point_tangent(t, b)
        _bx, _by = deltoid(b, 500)
        _e0, _e1 = _polygon_chord(_p, _d, _bx, _by)
        return np.array([_e0[0], _e1[0]]), np.array([_e0[1], _e1[1]])

    def fit_unit_chord(theta, bx, by):
        """Endpoints of a unit needle at angle theta, centred in the longest chord of polygon (bx, by)."""
        _u = np.array([math.cos(theta), math.sin(theta)])
        _perp = np.array([-math.sin(theta), math.cos(theta)])
        _best, _mid = 0.0, np.zeros(2)
        for _c in np.linspace(-0.75, 0.75, 61):
            _e0, _e1 = _polygon_chord(_c * _perp, _u, bx, by)
            _len = float(np.hypot(_e1[0] - _e0[0], _e1[1] - _e0[1]))
            if _len > _best:
                _best, _mid = _len, 0.5 * (_e0 + _e1)
        _a, _b = _mid - 0.5 * _u, _mid + 0.5 * _u
        return np.array([_a[0], _b[0]]), np.array([_a[1], _b[1]])

    def equilateral_h1():
        """Equilateral triangle of height 1 (Pal's convex minimum): rows [baseL, baseR, apex]."""
        return np.array([[-1.0 / SQRT3, 0.0], [1.0 / SQRT3, 0.0], [0.0, 1.0]])

    def tri_mask(gx, gy, tri):
        """Boolean mask of grid points inside triangle tri (3x2) via barycentric signs."""
        (_ax, _ay), (_bx, _by), (_cx, _cy) = tri
        _den = (_by - _cy) * (_ax - _cx) + (_cx - _bx) * (_ay - _cy)
        if abs(_den) < 1e-15:
            return np.zeros(gx.shape, bool)
        _a = ((_by - _cy) * (gx - _cx) + (_cx - _bx) * (gy - _cy)) / _den
        _b = ((_cy - _ay) * (gx - _cx) + (_ax - _cx) * (gy - _cy)) / _den
        _c = 1.0 - _a - _b
        return (_a >= -1e-9) & (_b >= -1e-9) & (_c >= -1e-9)

    def perron_pieces(nlev, alpha, apex, base_half):
        """Sub-triangles after nlev rounds of pairwise cut-and-shift with overlap fraction alpha."""
        _xs = np.linspace(-base_half, base_half, 2**nlev + 1)
        _ap = np.array(apex)
        _groups = [[np.array([[_xs[_i], 0.0], [_xs[_i + 1], 0.0], _ap])] for _i in range(2**nlev)]
        _w = (2 * base_half) / 2**nlev
        for _ in range(nlev):
            _step = 0.5 * alpha * _w
            _nxt = []
            for _i in range(0, len(_groups), 2):
                _left = [_t + np.array([_step, 0.0]) for _t in _groups[_i]]
                _right = [_t + np.array([-_step, 0.0]) for _t in _groups[_i + 1]]
                _nxt.append(_left + _right)
            _groups = _nxt
            _w *= 1.0 + alpha
        return [_t for _g in _groups for _t in _g]

    def union_fraction(tris, gx, gy, cell_area):
        """Rasterised area of the union of triangles over grid (gx, gy) and its boolean mask."""
        _mask = np.zeros(gx.shape, bool)
        for _t in tris:
            _mask |= tri_mask(gx, gy, _t)
        return float(_mask.sum() * cell_area), _mask

    def rot2d(pts, deg, ctr):
        """Rotate points (N x 2) by deg degrees about centre ctr."""
        _th = math.radians(deg)
        _r = np.array([[math.cos(_th), -math.sin(_th)], [math.sin(_th), math.cos(_th)]])
        return (np.asarray(pts) - ctr) @ _r.T + ctr

    return (
        SQRT3,
        circle,
        deltoid,
        deltoid_needle,
        equilateral_h1,
        fit_unit_chord,
        math,
        needle_at,
        perron_pieces,
        play_pause,
        rot2d,
        union_fraction,
    )


@app.cell
def _(mo):
    mo.md(
        r"""
        # Kakeya: a turning needle, zero area, and full dimension

        In 1917 Sōichi Kakeya asked a tabletop question. Lay a needle of length 1 flat on a table
        and turn it until it has pointed in **every** direction. What is the *smallest area* it can
        sweep while doing so?

        The honest answer breaks the question. There is no smallest area: you can always do better,
        driving the swept region as close to nothing as you like. Chasing that limit turns a plane
        puzzle into a statement about dimension, then into the floor of a tower of results in Fourier
        analysis, and its three-dimensional case, closed in 2025, earned Hong Wang a share of the
        2026 Fields Medal.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 1. The needle problem

        The needle keeps its length 1. It may slide and turn, never stretch, and it stays flat. The
        puzzle is about waste: turning paints table, and we want to paint as little as possible while
        still facing every direction.

        The reflex answer spins the needle about its middle. The tips reach out to radius $r =
        \tfrac12$, so the swept region is a disc:

        $$
        \begin{aligned}
        A_{\text{disc}} &= \pi r^2                    && \text{area of a disc of radius } r \\
                        &= \pi\left(\tfrac12\right)^2  && \text{the tips reach only } r = \tfrac12 \\
                        &= \tfrac{\pi}{4} \approx 0.785 .
        \end{aligned}
        $$

        The cheap ways to shrink that disc all fail: a smaller disc cannot hold the needle pointing
        sideways, an ellipse still needs the full unit width at its extremes, and pivoting about an
        endpoint only swaps one disc for another. Every cheap idea keeps the needle turning *in
        place*, and turning in place is what wastes area.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, circle, go, make_subplots, math, needle_at, np, play_pause, style_subplot_axes):
    _gu = np.linspace(-0.62, 0.62, 76)
    _GX, _GY = np.meshgrid(_gu, _gu)
    _angles = np.linspace(0, math.pi, 22, endpoint=False)
    _halfw = 0.025

    _cov = np.zeros(_GX.shape)
    _covs = []
    for _a in _angles:
        _ux, _uy = math.cos(_a), math.sin(_a)
        _along = _GX * _ux + _GY * _uy
        _across = -_GX * _uy + _GY * _ux
        _cov = _cov + ((np.abs(_across) <= _halfw) & (np.abs(_along) <= 0.5)).astype(float)
        _z = _cov.copy()
        _z[_z == 0] = np.nan
        _covs.append(_z)

    def _fan_upto(k):
        _x, _y = [], []
        for _j in range(k + 1):
            _nx, _ny = needle_at(0.0, 0.0, _angles[_j])
            _x += [_nx[0], _nx[1], None]
            _y += [_ny[0], _ny[1], None]
        return _x, _y

    _fig = make_subplots(
        rows=1, cols=2, subplot_titles=("The needle sweeps every direction", "How often each point is painted")
    )
    _dx, _dy = circle(0.5, 200)
    _fig.add_trace(
        go.Scatter(x=_dx, y=_dy, mode="lines", line={"color": COLORS["grid"]}, showlegend=False), row=1, col=1
    )
    _fx0, _fy0 = _fan_upto(0)
    _fig.add_trace(
        go.Scatter(
            x=_fx0, y=_fy0, mode="lines", line={"color": COLORS["primary"], "width": 1}, opacity=0.5, showlegend=False
        ),
        row=1,
        col=1,
    )
    _n0x, _n0y = needle_at(0.0, 0.0, _angles[0])
    _fig.add_trace(
        go.Scatter(x=_n0x, y=_n0y, mode="lines", line={"color": COLORS["secondary"], "width": 5}, showlegend=False),
        row=1,
        col=1,
    )
    _fig.add_trace(
        go.Heatmap(
            x=_gu,
            y=_gu,
            z=_covs[0],
            zmin=1,
            zmax=len(_angles),
            colorscale="Inferno",
            colorbar={"title": {"text": "paints"}, "len": 0.8},
            hoverinfo="skip",
        ),
        row=1,
        col=2,
    )

    _frames = []
    for _k in range(len(_angles)):
        _fx, _fy = _fan_upto(_k)
        _nx, _ny = needle_at(0.0, 0.0, _angles[_k])
        _frames.append(
            go.Frame(
                data=[go.Scatter(x=_fx, y=_fy), go.Scatter(x=_nx, y=_ny), go.Heatmap(z=_covs[_k])],
                traces=[1, 2, 3],
                name=str(_k),
            )
        )
    _fig.frames = _frames

    _fig.update_layout(**base_layout(title="Spinning in place paints the middle over and over", height=430))
    _fig.update_xaxes(range=[-0.62, 0.62], scaleanchor="y", constrain="domain", showticklabels=False, row=1, col=1)
    _fig.update_yaxes(range=[-0.62, 0.62], showticklabels=False, row=1, col=1)
    _fig.update_xaxes(range=[-0.62, 0.62], scaleanchor="y2", constrain="domain", showticklabels=False, row=1, col=2)
    _fig.update_yaxes(range=[-0.62, 0.62], showticklabels=False, row=1, col=2)
    style_subplot_axes(_fig)
    _fig.update_layout(updatemenus=play_pause("▶ Sweep the needle"))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Play it: the needle sweeps every direction about its centre, and the right panel colours each
        point by how many positions have covered it. The rim is touched once, the centre by nearly all
        of them. The disc is a real answer, but it repaints its middle endlessly. The needle never
        needed a solid disc, and the way to spend less is to stop turning in place.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Two objects, because the mathematics differs

        Pushing toward "as small as possible" splits the puzzle in two, and everything downstream
        depends on the split:

        - **Kakeya needle set:** a set inside which the needle can be *continuously rotated* through
          a full turn, a genuine physical turn. Its infimal area is **0 but never attained**: you can
          go as small as you like, never to zero.
        - **Besicovitch set** (the modern *Kakeya set*): a set that merely *contains* a unit segment
          in every direction, with no requirement that you slide between them. Here the area can be
          **exactly 0**.

        > A compact set $K \subseteq \mathbb{R}^n$ is a **Kakeya set** if for every direction
        > $\omega \in S^{n-1}$ there is a position $a$ with the segment
        > $\{a + t\omega : 0 \le t \le 1\} \subseteq K$.

        Section 2 chases the Besicovitch version to zero, then glues the pieces back into a needle set
        at the end.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 2. Plane constructions: shrinking the area

        ### The convex answers, and where they bottom out

        The intuitive answers keep the shape **convex** (no dents). Spinning fills the disc; a
        Reuleaux triangle of width 1, turned by pivoting about its three corners, does better; and Pal
        (1921) proved the smallest convex answer of all is the equilateral triangle of height 1:

        $$
        \begin{aligned}
        A_{\text{disc}}    &= \tfrac{\pi}{4} \approx 0.785             && \text{spin about the centre} \\
        A_{\text{Reuleaux}} &= \tfrac{\pi - \sqrt3}{2} \approx 0.705   && \text{pivot about three corners} \\
        A_{\triangle}      &= \tfrac{1}{\sqrt3} \approx 0.577          && \text{Pal's convex minimum} .
        \end{aligned}
        $$

        The area drops, but $1/\sqrt3$ is a floor: no convex shape beats it. That floor is the clue.
        """
    )
    return


@app.cell
def _(
    COLORS,
    SQRT3,
    base_layout,
    circle,
    equilateral_h1,
    fit_unit_chord,
    go,
    make_subplots,
    math,
    np,
    play_pause,
    style_subplot_axes,
):
    def _reuleaux(width=1.0, n=90):
        _h = SQRT3 / 2.0 * width
        _va = np.array([0.0, _h * 2 / 3])
        _vb = np.array([-width / 2, -_h / 3])
        _vc = np.array([width / 2, -_h / 3])
        _x, _y = [], []
        for _c, _p, _q in ((_va, _vb, _vc), (_vb, _vc, _va), (_vc, _va, _vb)):
            _a0 = math.atan2(_p[1] - _c[1], _p[0] - _c[0])
            _a1 = math.atan2(_q[1] - _c[1], _q[0] - _c[0])
            if _a1 < _a0:
                _a1 += 2 * math.pi
            _t = np.linspace(_a0, _a1, n)
            _x += list(_c[0] + width * np.cos(_t))
            _y += list(_c[1] + width * np.sin(_t))
        return np.array(_x), np.array(_y)

    _cx, _cy = circle(0.5, 200)
    _ux, _uy = _reuleaux(1.0)
    _tri = equilateral_h1()
    _tx = np.array([_tri[0, 0], _tri[1, 0], _tri[2, 0], _tri[0, 0]])
    _ty = np.array([_tri[0, 1], _tri[1, 1], _tri[2, 1], _tri[0, 1]])
    _shapes = [
        (_cx, _cy, "rgba(0,212,255,0.10)"),
        (_ux, _uy, "rgba(78,205,196,0.12)"),
        (_tx, _ty, "rgba(149,225,211,0.12)"),
    ]

    _angles = np.linspace(0, math.pi, 30, endpoint=False)
    _needles = [[fit_unit_chord(_a, _bx, _by) for _a in _angles] for _bx, _by, _ in _shapes]

    _fig = make_subplots(
        rows=1,
        cols=3,
        subplot_titles=("Disc  π/4 ≈ 0.785", "Reuleaux  (π−√3)/2 ≈ 0.705", "Pal triangle  1/√3 ≈ 0.577"),
    )
    for _c, (_sx, _sy, _fill) in enumerate(_shapes, start=1):
        _fig.add_trace(
            go.Scatter(
                x=_sx,
                y=_sy,
                mode="lines",
                fill="toself",
                fillcolor=_fill,
                line={"color": COLORS["grid"]},
                showlegend=False,
            ),
            row=1,
            col=_c,
        )
        _nx0, _ny0 = _needles[_c - 1][0]
        _fig.add_trace(
            go.Scatter(x=_nx0, y=_ny0, mode="lines", line={"color": COLORS["secondary"], "width": 5}, showlegend=False),
            row=1,
            col=_c,
        )

    _frames = []
    for _k in range(len(_angles)):
        _data = [go.Scatter(x=_needles[_s][_k][0], y=_needles[_s][_k][1]) for _s in range(3)]
        _frames.append(go.Frame(data=_data, traces=[1, 3, 5], name=str(_k)))
    _fig.frames = _frames

    _fig.update_layout(**base_layout(title="A unit needle turns in each convex answer", height=380))
    for _c, _xr, _yr in (
        (1, [-0.62, 0.62], [-0.62, 0.62]),
        (2, [-0.62, 0.62], [-0.55, 0.75]),
        (3, [-0.72, 0.72], [-0.2, 1.05]),
    ):
        _fig.update_xaxes(
            range=_xr, scaleanchor=f"y{'' if _c == 1 else _c}", constrain="domain", showticklabels=False, row=1, col=_c
        )
        _fig.update_yaxes(range=_yr, showticklabels=False, row=1, col=_c)
    style_subplot_axes(_fig)
    _fig.update_layout(updatemenus=play_pause("▶ Turn the needle"))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Play it: the unit needle turns through every direction inside each convex shape, so all three
        are genuine needle sets. The area falls from the disc to the Reuleaux triangle to Pal's
        triangle, yet Pal proved the triangle is the smallest convex answer. To get below $1/\sqrt3$
        we have to give up convexity.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Break convexity: the deltoid

        A convex shape has to be used in one piece, and that is the handicap. Allow a dent and you can
        do better. Kakeya's own guess keeps the needle **tangent to a curve** so both ends move: now
        it *slides along its own length* as it turns, never repainting the sliver it just left. The
        curve is a three-cusped hypocycloid, traced by a point on a circle of radius $b$ rolling
        inside a circle of radius $3b$:

        $$
        x(t) = 2b\cos t + b\cos 2t, \qquad y(t) = 2b\sin t - b\sin 2t .
        $$

        Its tangent chord always has length $4b$, so a unit needle needs $b = \tfrac14$, and the area
        drops below the convex floor:

        $$
        \begin{aligned}
        A_{\text{deltoid}} &= 2\pi b^2                       && \text{area of a deltoid, rolling radius } b \\
                           &= 2\pi\left(\tfrac14\right)^2     && \text{unit chord } 4b = 1 \Rightarrow b = \tfrac14 \\
                           &= \tfrac{\pi}{8} \approx 0.393    && < \tfrac{1}{\sqrt3}\text{, beating every convex answer} .
        \end{aligned}
        $$
        """
    )
    return


@app.cell
def _(COLORS, base_layout, circle, deltoid, deltoid_needle, go, math, np, play_pause, style_subplot_axes):
    _b = 0.25
    _phis = np.linspace(0, 2 * math.pi, 48)
    _dx, _dy = deltoid(_b, 400)

    def _rolling(phi):
        _cxr, _cyr = 2 * _b * math.cos(phi), 2 * _b * math.sin(phi)
        _rx, _ry = circle(_b, 60, _cxr, _cyr)
        return _rx, _ry, _cxr, _cyr

    def _arc_to(phi, k):
        _t = np.linspace(0, phi, max(2, k))
        return 2 * _b * np.cos(_t) + _b * np.cos(2 * _t), 2 * _b * np.sin(_t) - _b * np.sin(2 * _t)

    _fig = go.Figure()
    _bx, _by = circle(3 * _b, 200)
    _fig.add_trace(go.Scatter(x=_bx, y=_by, mode="lines", line={"color": COLORS["grid"], "width": 1}, showlegend=False))
    _fig.add_trace(
        go.Scatter(
            x=_dx, y=_dy, mode="lines", line={"color": COLORS["muted"], "width": 1, "dash": "dot"}, showlegend=False
        )
    )
    _rx0, _ry0, _cx0, _cy0 = _rolling(_phis[0])
    _fig.add_trace(
        go.Scatter(x=_rx0, y=_ry0, mode="lines", line={"color": COLORS["tertiary"], "width": 1.5}, showlegend=False)
    )
    _ax0, _ay0 = _arc_to(_phis[0], 2)
    _fig.add_trace(
        go.Scatter(x=_ax0, y=_ay0, mode="lines", line={"color": COLORS["primary"], "width": 3}, showlegend=False)
    )
    _nx0, _ny0 = deltoid_needle(_phis[0], _b)
    _fig.add_trace(
        go.Scatter(x=_nx0, y=_ny0, mode="lines", line={"color": COLORS["secondary"], "width": 6}, showlegend=False)
    )

    _frames = []
    for _k, _phi in enumerate(_phis):
        _rx, _ry, _cxr, _cyr = _rolling(_phi)
        _ax, _ay = _arc_to(_phi, _k + 2)
        _nx, _ny = deltoid_needle(_phi, _b)
        _frames.append(
            go.Frame(
                data=[go.Scatter(x=_rx, y=_ry), go.Scatter(x=_ax, y=_ay), go.Scatter(x=_nx, y=_ny)],
                traces=[2, 3, 4],
                name=str(_k),
            )
        )
    _fig.frames = _frames

    _fig.update_layout(**base_layout(title="Rolling a circle traces the deltoid (area π/8)", height=520))
    _fig.update_xaxes(range=[-0.85, 0.85], scaleanchor="y", constrain="domain", showticklabels=False)
    _fig.update_yaxes(range=[-0.85, 0.85], showticklabels=False)
    style_subplot_axes(_fig)
    _fig.update_layout(updatemenus=play_pause("▶ Roll the circle"))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The small teal circle rolls inside the large one; the cyan curve is the point it traces, the
        deltoid. The coral needle stays tangent, its ends riding the cusps, turning through every
        direction while sliding along itself. One dent, and it beats every convex answer.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### One move does all the shrinking: slide is free, only turning costs

        Every construction below rests on a single asymmetry between the needle's two moves. Rotating
        by an angle $\theta$ about a pivot sweeps a sector of area $\theta/2$. Sliding along its own
        length sweeps nothing new: the needle stays on the same line. Directions cost area, position
        is free. So two triangles that each carry a fan of directions can be slid to **overlap**,
        keeping every direction while taking less room.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, make_subplots, math, np, play_pause, style_subplot_axes):
    _pivot = np.array([-0.35, -0.15])
    _thetas = np.linspace(0, math.pi / 3, 24)
    _slides = np.linspace(0.0, 0.9, 24)

    def _sector(a1):
        _a = np.linspace(0, a1, 40)
        return (
            [_pivot[0], *(_pivot[0] + np.cos(_a)), _pivot[0]],
            [_pivot[1], *(_pivot[1] + np.sin(_a)), _pivot[1]],
        )

    def _needle_rot(a):
        return [_pivot[0], _pivot[0] + math.cos(a)], [_pivot[1], _pivot[1] + math.sin(a)]

    def _needle_slide(s):
        _d = np.array([math.cos(math.pi / 3), math.sin(math.pi / 3)])
        _base = _pivot + s * _d
        return [_base[0], _base[0] + _d[0]], [_base[1], _base[1] + _d[1]]

    _fig = make_subplots(
        rows=1, cols=2, subplot_titles=("Rotate: sweeps a sector θ/2", "Slide along the axis: sweeps nothing")
    )
    _sx, _sy = _sector(_thetas[0])
    _fig.add_trace(
        go.Scatter(
            x=_sx,
            y=_sy,
            mode="lines",
            fill="toself",
            fillcolor="rgba(255,230,109,0.22)",
            line={"color": COLORS["quaternary"], "width": 1},
            showlegend=False,
        ),
        row=1,
        col=1,
    )
    _rx, _ry = _needle_rot(_thetas[0])
    _fig.add_trace(
        go.Scatter(x=_rx, y=_ry, mode="lines", line={"color": COLORS["secondary"], "width": 6}, showlegend=False),
        row=1,
        col=1,
    )
    _fsx, _fsy = _sector(_thetas[-1])
    _fig.add_trace(
        go.Scatter(
            x=_fsx,
            y=_fsy,
            mode="lines",
            fill="toself",
            fillcolor="rgba(74,85,104,0.18)",
            line={"color": COLORS["muted"], "width": 1},
            showlegend=False,
        ),
        row=1,
        col=2,
    )
    _slx, _sly = _needle_slide(_slides[0])
    _fig.add_trace(
        go.Scatter(x=_slx, y=_sly, mode="lines", line={"color": COLORS["secondary"], "width": 6}, showlegend=False),
        row=1,
        col=2,
    )

    _frames = []
    for _k in range(len(_thetas)):
        _sx, _sy = _sector(_thetas[_k])
        _rx, _ry = _needle_rot(_thetas[_k])
        _slx, _sly = _needle_slide(_slides[_k])
        _frames.append(
            go.Frame(
                data=[go.Scatter(x=_sx, y=_sy), go.Scatter(x=_rx, y=_ry), go.Scatter(x=_slx, y=_sly)],
                traces=[0, 1, 3],
                name=str(_k),
            )
        )
    _fig.frames = _frames

    _fig.update_layout(**base_layout(title="Only turning paints", height=420))
    for _c in (1, 2):
        _fig.update_xaxes(
            range=[-0.6, 1.15],
            scaleanchor="y" if _c == 1 else "y2",
            constrain="domain",
            showticklabels=False,
            row=1,
            col=_c,
        )
        _fig.update_yaxes(range=[-0.45, 1.15], showticklabels=False, row=1, col=_c)
    style_subplot_axes(_fig)
    _fig.update_layout(updatemenus=play_pause("▶ Rotate, then slide"))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Left: rotating about a pivot, the swept sector (yellow) grows with the angle. Right: sliding
        the needle along its own axis, the region never grows past the grey sliver it started in.
        Turning is the only move that costs area, so a construction should spend as little turning as
        it can.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### The Perron tree: cut the triangle into slivers and overlap them

        Take the triangle of height 1. Split its base into $2^k$ equal pieces, giving $2^k$ thin
        sub-triangles that together still span the same 60-degree fan (they share the apex). Slide
        them horizontally so consecutive ones overlap as much as possible without losing their apex
        directions. Each level of subdivision adds only a fixed slice of fresh area, so iterating
        drives the footprint down:

        $$
        A_k \;\le\; (\text{const})\cdot A_0 \cdot \tfrac{1}{k} \;\longrightarrow\; 0
        \qquad (k \to \infty),
        $$

        while a unit segment survives in every direction of the fan.
        """
    )
    return


@app.cell
def _(COLORS, SQRT3, base_layout, go, np, perron_pieces, play_pause, style_subplot_axes, union_fraction):
    _nlev = 6
    _apex = (0.0, 1.0)
    _base_half = 1.0 / SQRT3
    _gu = np.linspace(-1.3, 1.3, 180)
    _gv = np.linspace(-0.05, 1.05, 90)
    _GX, _GY = np.meshgrid(_gu, _gv)
    _cellA = (_gu[1] - _gu[0]) * (_gv[1] - _gv[0])
    _alphas = np.linspace(0.0, 0.6, 16)
    _base_area, _ = union_fraction(perron_pieces(_nlev, 0.0, _apex, _base_half), _GX, _GY, _cellA)

    def _tree(alpha):
        _tris = perron_pieces(_nlev, alpha, _apex, _base_half)
        _x, _y = [], []
        for _t in _tris:
            _x += [_t[0, 0], _t[1, 0], _t[2, 0], None]
            _y += [_t[0, 1], _t[1, 1], _t[2, 1], None]
        _ar, _ = union_fraction(_tris, _GX, _GY, _cellA)
        return _x, _y, _ar

    def _label(pct):
        return go.Scatter(
            x=[-1.2],
            y=[0.98],
            mode="text",
            text=[f"footprint {pct:.0f}%   fan 60°"],
            textfont={"color": COLORS["highlight"], "size": 14},
            textposition="middle right",
            showlegend=False,
        )

    _x0, _y0, _a0 = _tree(_alphas[0])
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
    _fig.add_trace(_label(100.0))

    _frames = []
    for _k, _al in enumerate(_alphas):
        _xx, _yy, _ar = _tree(_al)
        _frames.append(
            go.Frame(data=[go.Scatter(x=_xx, y=_yy), _label(100.0 * _ar / _base_area)], traces=[0, 1], name=str(_k))
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
        As the overlap grows the footprint (top-left readout) drops well below the original triangle,
        while the fan of directions stays locked at 60 degrees, because every sliver keeps its apex.
        Area is spent; directions are kept.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Besicovitch: exactly zero area

        A 60-degree fan is only an artefact of one triangle. Three rotated Perron trees (0, 60, 120
        degrees) cover all 180 directions (a direction and its reverse are the same); six copies
        close into a symmetric star. Take the sprouting to the limit inside each copy, and
        Besicovitch (1919) gets the payoff:

        > There is a Kakeya (Besicovitch) set $K \subseteq \mathbb{R}^2$ with area $|K| = 0$.

        For the *needle* version, Pal joins glue the branches (slide the needle far out, turn where a
        tiny angle suffices, slide back), so the needle turns continuously in area as small as you
        like but never zero. Van Alphen (1942), then Cunningham (1971), fit such needle sets inside
        the **unit disc**, the smallest disc that can hold a unit segment at all.
        """
    )
    return


@app.cell
def _(COLORS, SQRT3, base_layout, go, np, perron_pieces, play_pause, rot2d, style_subplot_axes):
    _nlev = 5
    _apex = (0.0, 1.0)
    _base_half = 1.0 / SQRT3
    _tris = perron_pieces(_nlev, 0.6, _apex, _base_half)
    _ctr = np.vstack(_tris).mean(axis=0)
    _rots = [0, 60, 120, 180, 240, 300]

    def _copies(m):
        _x, _y = [], []
        for _r in _rots[:m]:
            for _t in _tris:
                _rt = rot2d(_t, _r, _ctr)
                _x += [_rt[0, 0], _rt[1, 0], _rt[2, 0], None]
                _y += [_rt[0, 1], _rt[1, 1], _rt[2, 1], None]
        return _x, _y

    _steps = [1, 2, 3, 6]
    _labels = ["1 tree · 60°", "2 trees · 120°", "3 trees · 180° (all directions)", "6 trees · symmetric star"]

    _x0, _y0 = _copies(1)
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
        _xx, _yy = _copies(_m)
        _frames.append(
            go.Frame(
                data=[go.Scatter(x=_xx, y=_yy)],
                traces=[0],
                name=_labels[_k],
                layout={"title": {"text": f"Besicovitch star: {_labels[_k]}"}},
            )
        )
    _fig.frames = _frames

    _fig.update_layout(**base_layout(title="Besicovitch star: 1 tree · 60°", height=520))
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
        Each play step drops in another rotated copy of the tree. Three cover all 180 directions;
        six close into the star. Every copy has vanishing area, so the whole star does too, while now
        holding a needle in every direction. The area falls only like $1/\log N$ for $N = 2^n$
        slivers, too slowly to watch it reach zero, yet it clearly still holds a needle pointing
        everywhere. Something with no area is still substantial, which is the signal that area is the
        wrong ruler.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 3. Dimension: the right way to say "still big"

        A Besicovitch set has zero area yet plainly holds a needle in every direction, so "zero area"
        cannot mean "nothing there." Zero measure is no thickness, not no points: the rationals have
        zero length yet sit everywhere, and the Cantor set (throw out the middle third, forever) has
        zero length yet is uncountable.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, make_subplots, play_pause, style_subplot_axes):
    def _cantor(depth):
        _levels = [[(0.0, 1.0)]]
        for _ in range(depth):
            _nxt = []
            for _a, _b in _levels[-1]:
                _t = (_b - _a) / 3.0
                _nxt += [(_a, _a + _t), (_b - _t, _b)]
            _levels.append(_nxt)
        return _levels

    _depth = 6
    _levels = _cantor(_depth)
    _lengths = [(2.0 / 3.0) ** _m for _m in range(_depth + 1)]

    def _upto(m):
        _x, _y = [], []
        for _mm in range(m + 1):
            for _a, _b in _levels[_mm]:
                _x += [_a, _b, None]
                _y += [-_mm, -_mm, None]
        return _x, _y

    _fig = make_subplots(rows=1, cols=2, subplot_titles=("The Cantor set, refined", "total length (2/3)ᵐ → 0"))
    _x0, _y0 = _upto(0)
    _fig.add_trace(
        go.Scatter(x=_x0, y=_y0, mode="lines", line={"color": COLORS["primary"], "width": 4}, showlegend=False),
        row=1,
        col=1,
    )
    _fig.add_trace(
        go.Scatter(
            x=[0],
            y=_lengths[:1],
            mode="lines+markers",
            line={"color": COLORS["secondary"], "width": 3},
            showlegend=False,
        ),
        row=1,
        col=2,
    )

    _frames = []
    for _m in range(_depth + 1):
        _xx, _yy = _upto(_m)
        _frames.append(
            go.Frame(
                data=[go.Scatter(x=_xx, y=_yy), go.Scatter(x=list(range(_m + 1)), y=_lengths[: _m + 1])],
                traces=[0, 1],
                name=str(_m),
            )
        )
    _fig.frames = _frames

    _fig.update_layout(**base_layout(title="Measure zero, still substantial", height=380))
    _fig.update_xaxes(range=[-0.02, 1.02], showticklabels=False, row=1, col=1)
    _fig.update_yaxes(range=[-_depth - 0.5, 0.5], showticklabels=False, row=1, col=1)
    _fig.update_xaxes(title_text="refinement depth m", range=[-0.3, _depth + 0.3], row=1, col=2)
    _fig.update_yaxes(title_text="length", range=[0, 1.05], row=1, col=2)
    style_subplot_axes(_fig, show_ticklabels=True)
    _fig.update_layout(updatemenus=play_pause("▶ Remove middle thirds", duration=650))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        After $m$ rounds the Cantor set is $2^m$ intervals of length $3^{-m}$, total length $(2/3)^m
        \to 0$, yet uncountably many points remain. Length, like area, reports "nothing there" about
        a set that is still substantial. We need a finer ruler.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Box-counting (Minkowski) dimension

        Cover the set with a grid of boxes of side $\delta$ and count the boxes $N(\delta)$ it meets:

        $$
        \dim_{\text{box}} K = \lim_{\delta \to 0^+} \frac{\log N(\delta)}{\log(1/\delta)},
        \qquad N(\delta) \sim \delta^{-d}.
        $$

        Halving the box size doubles the count for a line (exponent 1) and quadruples it for a filled
        square (exponent 2). The slope of $\log N$ against $\log(1/\delta)$ is the dimension.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, make_subplots, np, style_subplot_axes):
    _deltas = [0.25, 0.2, 0.125, 0.1, 0.0625, 0.05]
    _seg_N = [round(1.0 / _d) for _d in _deltas]
    _sq_N = [round(1.0 / _d) ** 2 for _d in _deltas]
    _lx = np.log([1.0 / _d for _d in _deltas])

    _fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=("Grid over a segment and a square (δ = 0.1)", "log N vs log(1/δ): the slope is the dimension"),
    )
    _d = 0.1
    _n = round(1.0 / _d)
    _gx, _gy = [], []
    for _i in range(_n + 1):
        _gx += [_i * _d, _i * _d, None, 0, 1, None]
        _gy += [0, 1, None, _i * _d, _i * _d, None]
    _fig.add_trace(
        go.Scatter(x=_gx, y=_gy, mode="lines", line={"color": COLORS["grid"], "width": 0.6}, showlegend=False),
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
        ),
        row=1,
        col=1,
    )
    _fig.add_trace(
        go.Scatter(
            x=[0, 1], y=[0.555, 0.555], mode="lines", line={"color": COLORS["secondary"], "width": 3}, showlegend=False
        ),
        row=1,
        col=1,
    )

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
        Left: at $\delta = 0.1$ the segment meets 10 boxes, the filled square all 100. Right: on the
        log-log plot the segment rides a slope-1 line and the square a slope-2 line. That slope is
        the dimension.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The slope can come out fractional, which is exactly what "between a line and a surface" means.
        Self-similar sets make it concrete: a set built from $N$ copies of itself each scaled by
        $1/r$ has dimension $\log N / \log r$.

        $$
        \begin{aligned}
        \text{Cantor set:} \quad & N=2,\ r=3 && \dim = \tfrac{\log 2}{\log 3} \approx 0.631 \\
        \text{Sierpinski triangle:} \quad & N=3,\ r=2 && \dim = \tfrac{\log 3}{\log 2} \approx 1.585 \\
        \text{Koch curve:} \quad & N=4,\ r=3 && \dim = \tfrac{\log 4}{\log 3} \approx 1.262 .
        \end{aligned}
        $$
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, math, np, play_pause, style_subplot_axes):
    def _koch(depth):
        _pts = [np.array([0.0, 0.0]), np.array([1.0, 0.0])]
        _rot = np.array(
            [
                [math.cos(math.radians(60)), -math.sin(math.radians(60))],
                [math.sin(math.radians(60)), math.cos(math.radians(60))],
            ]
        )
        for _ in range(depth):
            _out = [_pts[0]]
            for _i in range(len(_pts) - 1):
                _p, _q = _pts[_i], _pts[_i + 1]
                _dd = _q - _p
                _a, _b = _p + _dd / 3.0, _p + 2 * _dd / 3.0
                _out += [_a, _a + _rot @ (_b - _a), _b, _q]
            _pts = _out
        return np.array(_pts)

    _curves = [_koch(_d) for _d in range(5)]
    _fig = go.Figure()
    _fig.add_trace(
        go.Scatter(
            x=_curves[0][:, 0],
            y=_curves[0][:, 1],
            mode="lines",
            line={"color": COLORS["primary"], "width": 1.8},
            showlegend=False,
        )
    )
    _fig.frames = [
        go.Frame(
            data=[go.Scatter(x=_curves[_d][:, 0], y=_curves[_d][:, 1])],
            traces=[0],
            name=str(_d),
            layout={"title": {"text": f"Koch curve, depth {_d}  (dim → log4/log3 ≈ 1.262)"}},
        )
        for _d in range(5)
    ]
    _fig.update_layout(**base_layout(title="Koch curve, depth 0  (dim → log4/log3 ≈ 1.262)", height=360))
    _fig.update_xaxes(range=[-0.05, 1.05], scaleanchor="y", constrain="domain", showticklabels=False)
    _fig.update_yaxes(range=[-0.05, 0.5], showticklabels=False)
    style_subplot_axes(_fig)
    _fig.update_layout(updatemenus=play_pause("▶ Refine the curve", duration=650))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Each play step refines the Koch curve one level: every straight third sprouts a scaled copy of
        the whole, four copies at scale $1/3$, so its dimension is $\log 4/\log 3 \approx 1.262$,
        strictly between a line and a surface. The Sierpinski triangle ($\log 3/\log 2 \approx 1.585$)
        has the same flavour; rather than just draw it, we count its boxes next to pin the dimension
        down directly.
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
        _p = (_p + _verts[_rng.integers(0, 3, size=16000)]) / 2.0
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

    def _cells(cells, delta):
        _x, _y = [], []
        for _i, _j in cells:
            _x += [_i * delta, (_i + 1) * delta, (_i + 1) * delta, _i * delta, _i * delta, None]
            _y += [_j * delta, _j * delta, (_j + 1) * delta, (_j + 1) * delta, _j * delta, None]
        return _x, _y

    _fig = make_subplots(
        rows=1, cols=2, subplot_titles=("Grid of side δ over the Sierpinski triangle", "log N(δ) vs log(1/δ)")
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
    _cx0, _cy0 = _cells(_occ[0], _deltas[0])
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
            name="slope 1",
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
            name="slope 2",
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
        _cx, _cy = _cells(_occ[_k], _deltas[_k])
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
        about three times as many, so the log-log point climbs a track between the slope-1 and
        slope-2 guides, settling near $\log 3/\log 2 \approx 1.585$. Counting boxes agrees with the
        copy-counting formula.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Hausdorff: the finer ruler the conjecture asks for

        Box-counting uses one box size everywhere. Hausdorff lets the cover use boxes of different
        sizes and, for an exponent $s$, measures the cheapest such cover $\mathcal{H}^s$. As $s$
        sweeps up, $\mathcal{H}^s$ jumps from $\infty$ to $0$ at one threshold, the Hausdorff
        dimension. On the Cantor set the depth-$m$ cover is $2^m$ intervals of length $3^{-m}$, so

        $$
        \sum_i (\operatorname{diam} U_i)^s = 2^m (3^{-m})^s = \big(2 \cdot 3^{-s}\big)^m,
        $$

        a geometric series whose base passes through 1 at $s = \log 2/\log 3$. Always $\dim_H \le
        \dim_{\text{box}}$, so a Hausdorff statement is the stronger one, and Kakeya is stated for
        this finer dimension.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, math, np, play_pause, style_subplot_axes):
    _s = np.linspace(0.35, 0.95, 240)
    _thr = math.log(2) / math.log(3)
    _ms = [1, 2, 3, 4, 6, 8, 10, 12, 14]

    def _cover_sum(m):
        return (2.0 * 3.0 ** (-_s)) ** m

    _fig = go.Figure()
    _fig.add_trace(
        go.Scatter(
            x=_s, y=_cover_sum(_ms[0]), mode="lines", line={"color": COLORS["primary"], "width": 2.5}, showlegend=False
        )
    )
    _fig.add_vline(x=_thr, line={"color": COLORS["secondary"], "width": 2, "dash": "dash"})
    _fig.add_hline(y=1.0, line={"color": COLORS["muted"], "width": 1, "dash": "dot"})
    _fig.frames = [
        go.Frame(
            data=[go.Scatter(x=_s, y=_cover_sum(_m))],
            traces=[0],
            name=str(_m),
            layout={"title": {"text": f"Hausdorff cover sum, depth m = {_m}"}},
        )
        for _m in _ms
    ]
    _fig.update_layout(**base_layout(title=f"Hausdorff cover sum, depth m = {_ms[0]}", height=440))
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
    _fig.update_layout(updatemenus=play_pause("▶ Deepen the cover", duration=650))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The cover sum $(2 \cdot 3^{-s})^m$ against $s$. As the depth $m$ grows, it runs to infinity
        below $s = \log 2/\log 3$ and collapses to zero above it, sharpening into a step. Only at the
        threshold does it hold near 1. The exponent it refuses to send to $0$ or $\infty$ is the
        Hausdorff dimension.

        On self-similar sets the two rulers agree, but not in general. For $\{0\} \cup \{1/n : n \ge
        1\}$ the points pile up at 0, so a uniform grid needs about $\delta^{-1/2}$ boxes ($\dim_{
        \text{box}} = 1/2$), while a single interval swallows the tail for a Hausdorff cover
        ($\dim_H = 0$). That gap is why proving the Hausdorff Kakeya is genuinely more than the
        Minkowski one.
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
        rectangle. Two crossing at angle $\theta$ overlap in area

        $$
        |R_1 \cap R_2| \approx \frac{\delta^2}{\sin\theta} \qquad (\text{small } \delta),
        $$

        so rectangles in well-separated directions barely overlap. Summed over all pairs the overlaps
        stay small, which forces the union to stay spread out: it cannot be compressed below full
        dimension.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, make_subplots, math, np, play_pause, style_subplot_axes):
    _width = 0.06
    _counts = [1, 4, 8, 16, 28]

    def _rect(a):
        _hl, _hw = 0.5, _width / 2.0
        _c = np.array([[-_hl, -_hw], [_hl, -_hw], [_hl, _hw], [-_hl, _hw], [-_hl, -_hw]])
        _co, _si = math.cos(a), math.sin(a)
        _p = _c @ np.array([[_co, -_si], [_si, _co]]).T
        return _p[:, 0], _p[:, 1]

    def _fan(m):
        _x, _y = [], []
        for _a in np.linspace(0, math.pi, m, endpoint=False):
            _rx, _ry = _rect(_a)
            _x += [*_rx, None]
            _y += [*_ry, None]
        return _x, _y

    _gu = np.linspace(-0.6, 0.6, 220)
    _GX, _GY = np.meshgrid(_gu, _gu)
    _cellA = (_gu[1] - _gu[0]) ** 2

    def _union(m):
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
    _summed = [_m * _width for _m in _counts]
    _un = [_union(_m) for _m in _counts]
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
            y=_un,
            mode="lines+markers",
            line={"color": COLORS["primary"], "width": 3},
            name="union (stays spread)",
        ),
        row=1,
        col=2,
    )

    _frames = []
    for _m in _counts:
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
        from the drawn rectangles: the summed area (coral) climbs linearly, while the union (cyan)
        grows to fill the disc and stays there. Thin pieces, stubbornly large union.

        So the same clever pile answers two questions two ways. "How much paint to cover it?" is area,
        and the answer is none. "How many boxes to find it?" is dimension, and the answer is all of
        them. **Area 0, dimension 2** is not a contradiction, just two rulers on one set, and the
        fact that the union resists compression is the seed of everything in higher dimensions.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 5. Why anyone cares: the harmonic-analysis tower

        A needle puzzle stops being a curiosity here. It sits at the **bottom** of a tower of
        conjectures in Fourier analysis (the mathematics of breaking a signal into pure tones), from
        weakest to strongest:

        $$
        \text{local smoothing} \Rightarrow \text{Bochner-Riesz} \Rightarrow \text{restriction} \Rightarrow \text{Kakeya}.
        $$

        Kakeya is the weakest, so every stronger one needs it: a single counterexample to Kakeya
        would topple the whole tower. The bridge is the **uncertainty principle**: a thin sliver in
        frequency corresponds to a long thin tube in space, and tubes pointing every which way are
        exactly a Besicovitch configuration.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go):
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
            x=0, y=_lvl + 0.5, text="⇓ implies", showarrow=False, font={"color": COLORS["muted"], "size": 11}
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
        Each rung implies the one below, so Kakeya is the widest, weakest block at the base. The plane
        case ($n = 2$) is known all the way up; every rung is open in higher dimensions. The rest of
        the section unpacks the base and the bridge.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### The analytic form: the Kakeya maximal function

        The version harmonic analysts chase averages $|f|$ over the *best* $\delta$-tube in each
        direction $\omega$, calling that $f^{*}_\delta(\omega)$. The conjecture says this greedy
        tube-averaging barely amplifies anything, only a loss slower than any power of $\delta$:

        $$
        \| f^{*}_\delta \|_{L^n(S^{n-1})} \le C_\varepsilon\, \delta^{-\varepsilon}\, \| f \|_{L^n(\mathbb{R}^n)}
        \qquad \text{for every } \varepsilon > 0.
        $$

        If a Kakeya set could be squeezed below full dimension, an $f$ concentrated on it would have
        large tube averages in every direction at once, breaking the bound. The analytic conjecture
        is exactly the statement that Besicovitch compression cannot beat full dimension.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, make_subplots, math, np, play_pause, style_subplot_axes):
    _gu = np.linspace(-1.0, 1.0, 120)
    _GX, _GY = np.meshgrid(_gu, _gu)
    _f = np.zeros_like(_GX)
    for _bx, _by, _sig, _amp in ((-0.35, 0.1, 0.18, 1.0), (0.3, -0.25, 0.14, 0.85), (0.05, 0.45, 0.12, 0.6)):
        _f += _amp * np.exp(-((_GX - _bx) ** 2 + (_GY - _by) ** 2) / (2 * _sig**2))
    _angles = np.linspace(0, math.pi, 30, endpoint=False)
    _width = 0.12
    _offsets = np.linspace(-0.8, 0.8, 21)

    def _best(a):
        _u = np.array([math.cos(a), math.sin(a)])
        _perp = np.array([-math.sin(a), math.cos(a)])
        _al = _GX * _u[0] + _GY * _u[1]
        _ac = _GX * _perp[0] + _GY * _perp[1]
        _bv, _bc = 0.0, 0.0
        for _c in _offsets:
            _m = (np.abs(_ac - _c) <= _width / 2) & (np.abs(_al) <= 0.5)
            if _m.any():
                _v = float(_f[_m].mean())
                if _v > _bv:
                    _bv, _bc = _v, _c
        return _bv, _bc

    _star = np.array([_best(_a) for _a in _angles])
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
        rows=1, cols=2, subplot_titles=("A δ-tube swept over |f|", "f*(ω): best tube-average vs direction")
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
                data=[go.Scatter(x=_px, y=_py), go.Scatter(x=np.degrees(_angles[: _k + 1]), y=_fstar[: _k + 1])],
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
        Left: a fixed $|f|$ (three blobs) with a $\delta$-tube swept through every direction, snapping
        to the offset where its average is largest. Right: that best-per-direction average
        $f^{*}_\delta(\omega)$. The conjecture bounds this whole curve at once.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### The bridge: uncertainty turns frequency slivers into tubes

        A plane wave $e^{2\pi i x\cdot\xi}$ is one pure tone spread across space, its flat wavefronts
        perpendicular to $\xi$ and spaced by $1/|\xi|$. The **uncertainty principle** is reciprocal
        zooming: a bump on an $r \times s$ box in frequency spreads over the dual $\tfrac1r \times
        \tfrac1s$ box in space. Thin in frequency means long in space, so a sliver tangent to a
        curved frequency surface becomes a long thin tube, one per tangent direction.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, make_subplots, math, np, play_pause, style_subplot_axes):
    _gu = np.linspace(-1, 1, 200)
    _GX, _GY = np.meshgrid(_gu, _gu)
    _xi = np.array([4.0, 2.0])

    def _box(xh, yh):
        return [-xh, xh, xh, -xh, -xh], [-yh, -yh, yh, yh, -yh]

    _xhs = np.linspace(0.3, 0.05, 14)

    _fig = make_subplots(
        rows=1, cols=2, subplot_titles=("Plane wave: fronts ⟂ ξ, spacing 1/|ξ|", "Uncertainty: thin freq ↔ long tube")
    )
    _fig.add_trace(
        go.Heatmap(
            x=_gu,
            y=_gu,
            z=np.cos(2 * math.pi * (_xi[0] * _GX + _xi[1] * _GY)),
            colorscale="RdBu",
            showscale=False,
            hoverinfo="skip",
        ),
        row=1,
        col=1,
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
        col=1,
    )
    _fbx, _fby = _box(_xhs[0], 0.32)
    _fig.add_trace(
        go.Scatter(
            x=_fbx,
            y=_fby,
            mode="lines",
            fill="toself",
            fillcolor="rgba(255,107,107,0.30)",
            line={"color": COLORS["secondary"], "width": 2},
            name="frequency",
        ),
        row=1,
        col=2,
    )
    _pbx, _pby = _box(0.09 / _xhs[0], 0.22)
    _fig.add_trace(
        go.Scatter(
            x=_pbx,
            y=_pby,
            mode="lines",
            fill="toself",
            fillcolor="rgba(0,212,255,0.18)",
            line={"color": COLORS["primary"], "width": 2},
            name="physical",
        ),
        row=1,
        col=2,
    )

    _frames = []
    for _k, _xh in enumerate(_xhs):
        _fbx, _fby = _box(_xh, 0.32)
        _pbx, _pby = _box(0.09 / _xh, 0.22)
        _frames.append(
            go.Frame(data=[go.Scatter(x=_fbx, y=_fby), go.Scatter(x=_pbx, y=_pby)], traces=[2, 3], name=str(_k))
        )
    _fig.frames = _frames

    _fig.update_layout(**base_layout(title="A plane wave and the reciprocal boxes", height=380))
    _fig.update_xaxes(range=[-1, 1], scaleanchor="y", constrain="domain", showticklabels=False, row=1, col=1)
    _fig.update_yaxes(range=[-1, 1], showticklabels=False, row=1, col=1)
    _fig.update_xaxes(range=[-2, 2], scaleanchor="y2", constrain="domain", showticklabels=False, row=1, col=2)
    _fig.update_yaxes(range=[-1.1, 1.1], showticklabels=False, row=1, col=2)
    style_subplot_axes(_fig)
    _fig.update_layout(updatemenus=play_pause("▶ Thin the frequency box"))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Left: one plane wave; the arrow points along $\xi$ and the stripes are its wavefronts. Right,
        play it: as the frequency box (coral) is thinned, its physical dual (cyan) stretches into a
        long tube. Slivers tangent to a curved surface dualize to a needle in every direction.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Fefferman, 1971: where the tube geometry first bit

        To rebuild a signal you sum its tones one cutoff at a time; the natural higher-dimensional
        cutoff is a **ball** ($|\xi| \le R$, then $R \to \infty$). For $p = 2$ it converges;
        Fefferman showed that for every other $p$ it fails, and the reason is the needle puzzle. The
        ball's boundary is curved, so each thin slab tangent to it dualizes to a long tube, and those
        tubes pile up exactly as needles in a Besicovitch set.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, circle, go, make_subplots, math, np, play_pause, style_subplot_axes):
    _r = 0.12
    _hl_freq, _th_freq = _r / 2.0, _r**2
    _tube_L, _tube_w = 0.9, 0.9 * _r
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

    def _tube(a_deg):
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
        subplot_titles=("Frequency: r × r² slabs tangent to the ball", "Space: dual tubes, length : width = 1/r"),
    )
    _fig.add_trace(
        go.Scatter(x=_cx, y=_cy, mode="lines", line={"color": COLORS["grid"]}, showlegend=False), row=1, col=1
    )
    for _adeg in np.arange(0, 360, 15):
        _sx, _sy = _slab(_adeg)
        _fig.add_trace(
            go.Scatter(
                x=_sx,
                y=_sy,
                mode="lines",
                fill="toself",
                fillcolor="rgba(255,107,107,0.30)",
                line={"color": COLORS["secondary"], "width": 0.5},
                showlegend=False,
            ),
            row=1,
            col=1,
        )
    for _adeg in np.arange(0, 180, 15):
        _tx, _ty = _tube(_adeg)
        _fig.add_trace(
            go.Scatter(
                x=_tx,
                y=_ty,
                mode="lines",
                fill="toself",
                fillcolor="rgba(0,212,255,0.10)",
                line={"color": COLORS["primary"], "width": 0.4},
                showlegend=False,
            ),
            row=1,
            col=2,
        )

    _sweep = np.linspace(0, 180, 24, endpoint=False)
    _hsx, _hsy = _slab(_sweep[0])
    _fig.add_trace(
        go.Scatter(
            x=_hsx,
            y=_hsy,
            mode="lines",
            fill="toself",
            fillcolor="rgba(255,230,109,0.95)",
            line={"color": COLORS["highlight"], "width": 2},
            showlegend=False,
        ),
        row=1,
        col=1,
    )
    _htx, _hty = _tube(_sweep[0])
    _fig.add_trace(
        go.Scatter(
            x=_htx,
            y=_hty,
            mode="lines",
            fill="toself",
            fillcolor="rgba(255,230,109,0.5)",
            line={"color": COLORS["highlight"], "width": 2},
            showlegend=False,
        ),
        row=1,
        col=2,
    )

    _frames = []
    for _k, _adeg in enumerate(_sweep):
        _hsx, _hsy = _slab(_adeg)
        _htx, _hty = _tube(_adeg)
        _frames.append(
            go.Frame(data=[go.Scatter(x=_hsx, y=_hsy), go.Scatter(x=_htx, y=_hty)], traces=[37, 38], name=str(_k))
        )
    _fig.frames = _frames

    _fig.update_layout(**base_layout(title="Fefferman's ball multiplier: each slab dualizes to a tube", height=400))
    _fig.update_xaxes(range=[-1.4, 1.4], scaleanchor="y", constrain="domain", showticklabels=False, row=1, col=1)
    _fig.update_yaxes(range=[-1.4, 1.4], showticklabels=False, row=1, col=1)
    _fig.update_xaxes(range=[-1.1, 1.1], scaleanchor="y2", constrain="domain", showticklabels=False, row=1, col=2)
    _fig.update_yaxes(range=[-1.1, 1.1], showticklabels=False, row=1, col=2)
    style_subplot_axes(_fig)
    _fig.update_layout(updatemenus=play_pause("▶ Sweep the pair"))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Left: slabs tangent to the frequency ball, each $r$ wide along the tangent and $r^2$ thick
        radially. Right: the dual of each slab is a tube pointing radially with length $1/r^2$ and
        width $1/r$, so its length-to-width ratio is exactly $1/r$ (both panels to one scale). Play it:
        the highlighted slab sweeps the boundary while its dual tube sweeps the directions, one slab to
        one tube. The tubes point every which way through the origin, a Besicovitch configuration, and
        Fefferman turned that pile-up into a genuine counterexample: the sharp ball cutoff fails in
        $L^p$ for $p \ne 2$, $n \ge 2$.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### The three rungs above Kakeya

        Each is stronger than the one below, and each has a plain reading.

        **Restriction** (Stein): a wave built only from a curved surface's tones must leak energy and
        fade. With the extension operator $E g(x) = \int_{S^{n-1}} g(\omega) e^{2\pi i x\cdot\omega}
        d\sigma(\omega)$, the conjecture is $\|E g\|_{L^q(\mathbb{R}^n)} \lesssim \|g\|_{L^\infty}$
        for $q > 2n/(n-1)$. Known $n=2$, open $n \ge 3$.

        **Bochner-Riesz**: soften the ball cutoff with an exponent $\alpha \ge 0$, fading tones out
        near the boundary. At $\alpha = 0$ it is Fefferman's failing cutoff; the conjecture says any
        $\alpha > 0$ restores convergence for a range of $p$. Known $n=2$, open $n \ge 3$, and it
        implies Kakeya.

        **Local smoothing** (Sogge, the top): a wave averaged over a short time interval is smoother
        than at any frozen instant. It implies Bochner-Riesz, restriction, and Kakeya. Known $n=2$
        (Guth-Wang-Zhang 2020), open $n \ge 3$.
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
    _fig.frames = [
        go.Frame(
            data=[go.Scatter(x=_u, y=_mult(_al))],
            traces=[0],
            name=f"{_al:.2f}",
            layout={"title": {"text": f"Bochner-Riesz multiplier (1 − |ξ|²/R²)₊^α,  α = {_al:.2f}"}},
        )
        for _al in _alphas
    ]
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
        already restores convergence for a range of $p$. The uncertainty principle is what ties all
        of these back to how tubes in many directions pack, which is Kakeya.
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

        Fatten every segment into a **$\delta$-tube** of dimensions $\delta \times \delta \times 1$.
        Directions are $\delta$-separated on the sphere $S^2$, so there are about $\delta^{-2}$ tubes,
        and the total tube content is pinned:

        $$
        \#\mathbb{T} \cdot |T| \sim \delta^{-2} \cdot \delta^2 = 1,
        \qquad |N_\delta K| \sim \delta^{\,3 - d}.
        $$

        Dimension $d = 3$ is the case $3 - d = 0$: refining the tubes cannot drain the union. But
        space is genuinely harder than the plane: two lines in different directions almost always
        **cross** in the plane, while in space two tubes generically **miss** (skew lines), so the 2D
        crossing argument has no analogue.
        """
    )
    return


@app.cell
def _(COLORS, SCENE_THEME, base_layout, go, np):
    def _fib_sphere(n):
        _i = np.arange(n) + 0.5
        _phi = np.arccos(1 - 2 * _i / n)
        _theta = np.pi * (1 + 5**0.5) * _i
        return np.column_stack([np.sin(_phi) * np.cos(_theta), np.sin(_phi) * np.sin(_theta), np.cos(_phi)])

    def _sep(points, delta):
        _kept = np.empty((0, 3))
        for _p in points:
            if _kept.shape[0] == 0 or np.min(np.linalg.norm(_kept - _p, axis=1)) >= delta:
                _kept = np.vstack([_kept, _p])
        return _kept

    def _frame_vecs(direction):
        _u = direction / np.linalg.norm(direction)
        _tmp = np.array([1.0, 0.0, 0.0]) if abs(_u[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
        _v = np.cross(_u, _tmp)
        _v /= np.linalg.norm(_v)
        return _u, _v, np.cross(_u, _v)

    def _tube(center, direction, radius=0.045, length=1.0):
        _u, _v, _w = _frame_vecs(direction)
        _theta = np.linspace(0, 2 * np.pi, 12)
        _S, _T = np.meshgrid(np.linspace(-length / 2, length / 2, 2), _theta)
        _X = center[0] + _S * _u[0] + radius * (np.cos(_T) * _v[0] + np.sin(_T) * _w[0])
        _Y = center[1] + _S * _u[1] + radius * (np.cos(_T) * _v[1] + np.sin(_T) * _w[1])
        _Z = center[2] + _S * _u[2] + radius * (np.cos(_T) * _v[2] + np.sin(_T) * _w[2])
        return _X, _Y, _Z

    _rng = np.random.default_rng(7)
    _dirs = _sep(_fib_sphere(2500), 0.55)
    _dirs = _dirs[_dirs[:, 2] > 0][:14]
    _fig = go.Figure()
    for _d in _dirs:
        _X, _Y, _Z = _tube(_rng.uniform(-0.18, 0.18, 3), _d)
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
    _scene = {**SCENE_THEME, "aspectmode": "data", "camera": {"eye": {"x": 1.6, "y": 1.6, "z": 1.1}}}
    _fig.update_layout(
        **base_layout(title="δ×δ×1 tubes in δ-separated directions (skew, they miss)", height=560, scene=_scene)
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Drag to rotate: a bundle of $\delta \times \delta \times 1$ tubes in $\delta$-separated
        directions. From most viewpoints they pass one another without touching, the skew arrangement
        the plane never has. With no crossings to lean on, the proof trades "which tube meets which"
        for the **Wolff axiom**: for every prism $R$, $\#\{T \subseteq R\} \le \delta^{-2}|R|$. No
        prism swallows more tubes than its volume allows. From it Wolff (1995) got dimension $\ge
        5/2$, and progress stalled there for decades.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 7. Solving three dimensions: sticky, grains, induction

        The Wolff axiom stalls at $5/2$: capping the crudest concentration is not the same as ruling
        out the finer ways tubes overlap. Wang and Zahl (2025) closed the gap. Two ideas do the work.

        **Sticky reduction.** Zoom out so thin $\delta$-tubes blur into fatter $\rho$-tubes and ask
        how the thin ones sit inside the fat ones. In the **sticky** case they clump maximally, about
        $(\rho/\delta)^2$ per fat tube, and the picture repeats as you zoom (self-similar, like a
        comb). In the **non-sticky** case they scatter, like tossed sticks. Hickman calls it the
        single most important step: it *suffices* to prove the bound for sticky tubes.
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
        rows=1, cols=2, subplot_titles=(f"Sticky: {_k * _k} thin tubes clump", "Non-sticky: same count, scattered")
    )
    _fx = [-_rho / 2, _rho / 2, _rho / 2, -_rho / 2, -_rho / 2]
    _fy = [-_rho / 2, -_rho / 2, _rho / 2, _rho / 2, -_rho / 2]
    for _c in (1, 2):
        _fig.add_trace(
            go.Scatter(x=_fx, y=_fy, mode="lines", line={"color": COLORS["quaternary"], "width": 2}, showlegend=False),
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
    _sc = _rng.uniform(-_rho / 2, _rho / 2, size=(_k * _k, 2))
    _fig.add_trace(
        go.Scatter(
            x=_sc[:, 0], y=_sc[:, 1], mode="markers", marker={"color": COLORS["secondary"], "size": 7}, showlegend=False
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
        Cross-section of one fat tube. Left, sticky: the thin tubes fill it in a regular grid, the
        same picture at every zoom. Right, non-sticky: the same count scattered. The proof reduces to
        the sticky case, then handles the leftover geometry with grains.
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
        tube thick, wider but much shorter than the tubes through them, like the grain in wood:
        $\text{grain} \approx \delta \times c \times c$ with $\delta \ll c \ll 1$. Within a fat tube
        the grains tile disjointly, and no point lies in too many grains, the quantitative ceiling on
        compression.

        **Compression, quantified.** The Perron pile already shows it: its $2^n$ pieces are only
        translated, so their areas sum to the whole triangle (content pinned at 1) while the union
        falls like $1/\log N$. Content over footprint climbs, but only $\log N$-slowly.
        """
    )
    return


@app.cell
def _(COLORS, SQRT3, base_layout, go, make_subplots, np, perron_pieces, style_subplot_axes, union_fraction):
    _apex = (0.0, 1.0)
    _base_half = 1.0 / SQRT3
    _gu = np.linspace(-1.3, 1.3, 170)
    _gv = np.linspace(-0.05, 1.05, 85)
    _GX, _GY = np.meshgrid(_gu, _gv)
    _cellA = (_gu[1] - _gu[0]) * (_gv[1] - _gv[0])
    _base_area, _ = union_fraction(perron_pieces(1, 0.0, _apex, _base_half), _GX, _GY, _cellA)
    _levels = list(range(1, 9))
    _footprint = []
    for _n in _levels:
        _ar, _ = union_fraction(perron_pieces(_n, 0.6, _apex, _base_half), _GX, _GY, _cellA)
        _footprint.append(_ar / _base_area)
    _content = [1.0 for _ in _levels]
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
        Content (yellow) stays pinned at 1 while the footprint (cyan) falls with each Perron level, so
        their ratio, the compression (coral, right axis), climbs, but only $\log N$-slowly: real
        compression, yet bounded, which is the ceiling the conjecture asserts.

        **Induction on scales** finishes: assume the bound at one scale and bootstrap to a slightly
        better one, repeating until $d$ reaches 3. Because grains within a fat tube are disjoint,
        Wang-Zahl replace the wasteful multiplicity bound by the multiplicity of the actual union, so
        each step gains instead of leaking.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, create_timeline):
    _events = [
        (1995, "Wolff<br>≥ 5/2", 1),
        (2000, "Katz-Laba-Tao<br>Mink. > 5/2", -1),
        (2017, "Katz-Zahl<br>Hausd. ≥ 5/2 + ε", 1),
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

        $$
        \boxed{\text{Wang-Zahl (2025): every Kakeya set in } \mathbb{R}^3 \text{ has dimension } 3.}
        $$

        This does not by itself prove the tower above (the implications only run downward), but it
        removes the geometric floor's uncertainty and hands up the techniques, sticky reduction,
        grains, and non-leaking induction, that people hope to carry higher.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 8. Dimension four and up, still open

        The conjecture does not change with dimension: a Kakeya set in $\mathbb{R}^n$ should have
        dimension $n$. Nobody can prove it for $n \ge 4$. The proven lower bounds all sit strictly
        below $n$, and that shortfall is the open problem:

        $$
        \begin{aligned}
        \dim_H K &\ge \tfrac{n+2}{2}                 && \text{Wolff (1995), the hairbrush bound} \\
        \dim_H K &\ge (2 - \sqrt2)(n - 4) + 3        && \text{Katz-Tao (2002),}\ 2 - \sqrt2 \approx 0.586 .
        \end{aligned}
        $$

        The two cross exactly at $n = 4$, where both give 3: Wolff wins for $n = 2, 3, 4$, Katz-Tao
        overtakes for $n \ge 5$. Against a conjectured value of $n$, every method falls short.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, math, np, style_subplot_axes):
    _n = np.arange(2, 13)
    _wolff = (_n + 2) / 2
    _katz = (2 - math.sqrt(2)) * (_n - 4) + 3
    _fig = go.Figure()
    _fig.add_trace(
        go.Scatter(
            x=_n,
            y=_n.astype(float),
            mode="lines+markers",
            line={"color": COLORS["quaternary"], "width": 3, "dash": "dash"},
            name="conjectured dim = n",
        )
    )
    _fig.add_trace(
        go.Scatter(
            x=_n, y=_wolff, mode="lines+markers", line={"color": COLORS["primary"], "width": 3}, name="Wolff (n+2)/2"
        )
    )
    _fig.add_trace(
        go.Scatter(
            x=_n,
            y=_katz,
            mode="lines+markers",
            line={"color": COLORS["secondary"], "width": 3},
            name="Katz-Tao 0.586(n−4)+3",
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
        Both proven bounds stay below the conjectured $\dim = n$ (dashed), touching it only where they
        cross at $n = 4$. Wolff leads for $n = 2, 3, 4$; Katz-Tao overtakes from $n = 5$. The gap to
        the dashed line is the open problem.

        Because the tower's implications run downward, proving the $n \ge 4$ Kakeya would not by
        itself settle restriction, Bochner-Riesz, or local smoothing. What propagates outward is the
        toolkit: the proven multilinear Kakeya theorem drives $\ell^2$ decoupling (Bourgain-Demeter
        2015), which proves the Vinogradov mean value theorem and reaches analytic number theory and
        PDE. The expected payoff of $n \ge 4$ is methodological momentum, not a single toppling
        domino.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        In one line: a motion puzzle, then concrete shapes shrink the area, then the area hits zero,
        then area is the wrong ruler, then dimension, then the plane is solved at dimension 2, then
        the tower explains why it matters, then space is harder, and finally the 2025 machinery closes
        three dimensions. Four and up wait for the next idea.

        ---

        **Sources**

        - J. Hickman, *The Kakeya Conjecture: where does it come from and why is it important?*,
          [arXiv:2512.09842](https://arxiv.org/abs/2512.09842) (2025).
        - J. Zahl, *A Survey of the Kakeya conjecture, 2000-2025*,
          [arXiv:2512.09397](https://arxiv.org/abs/2512.09397).
        - H. Wang & J. Zahl, *Volume estimates for unions of convex sets, and the Kakeya set
          conjecture in three dimensions*, [arXiv:2502.17655](https://arxiv.org/abs/2502.17655) (2025).
        - T. Tao, *The three-dimensional Kakeya conjecture, after Wang and Zahl* (blog, 2025).
        - Z. Dvir, *On the size of Kakeya sets in finite fields*, J. Amer. Math. Soc. 22 (2009).
        - K. J. Falconer, *The Geometry of Fractal Sets* (CUP, 1985); C. Fefferman, *The multiplier
          problem for the ball*, Ann. of Math. 94 (1971).
        - R. O. Davies (1971), 2D dimension; International Mathematical Union, *Fields Medals 2026*.
        """
    )
    return


if __name__ == "__main__":
    app.run()
