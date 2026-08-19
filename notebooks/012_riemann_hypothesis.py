"""
Riemann: the zeros, the critical line, and two thirds of them.

A guided walk through the Riemann hypothesis following the research note in
`research/riemann/riemann.md`: the primes and the zeta function, the nontrivial zeros and
the critical line, the explicit formula that ties zeros to primes, the ladder of proven
proportions on the line, and the August 2026 argument (Claude / Anthropic) that makes
Montgomery's pair correlation unconditional and certifies at least two thirds of the zeros
on the line by finite linear algebra.

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
        base_layout,
        style_subplot_axes,
    )

    return COLORS, base_layout, go, make_subplots, np, style_subplot_axes


@app.cell
def _(np):
    """The first 300 ordinates gamma_k of the nontrivial zeros rho = 1/2 + i gamma_k."""
    ZEROS = np.array(
        [
            14.1347,
            21.022,
            25.0109,
            30.4249,
            32.9351,
            37.5862,
            40.9187,
            43.3271,
            48.0052,
            49.7738,
            52.9703,
            56.4462,
            59.347,
            60.8318,
            65.1125,
            67.0798,
            69.5464,
            72.0672,
            75.7047,
            77.1448,
            79.3374,
            82.9104,
            84.7355,
            87.4253,
            88.8091,
            92.4919,
            94.6513,
            95.8706,
            98.8312,
            101.3179,
            103.7255,
            105.4466,
            107.1686,
            111.0295,
            111.8747,
            114.3202,
            116.2267,
            118.7908,
            121.3701,
            122.9468,
            124.2568,
            127.5167,
            129.5787,
            131.0877,
            133.4977,
            134.7565,
            138.116,
            139.7362,
            141.1237,
            143.1118,
            146.001,
            147.4228,
            150.0535,
            150.9253,
            153.0247,
            156.1129,
            157.5976,
            158.85,
            161.189,
            163.0307,
            165.5371,
            167.1844,
            169.0945,
            169.912,
            173.4115,
            174.7542,
            176.4414,
            178.3774,
            179.9165,
            182.2071,
            184.8745,
            185.5988,
            187.2289,
            189.4162,
            192.0267,
            193.0797,
            195.2654,
            196.8765,
            198.0153,
            201.2648,
            202.4936,
            204.1897,
            205.3947,
            207.9063,
            209.5765,
            211.6909,
            213.3479,
            214.547,
            216.1695,
            219.0676,
            220.7149,
            221.4307,
            224.007,
            224.9833,
            227.4214,
            229.3374,
            231.2502,
            231.9872,
            233.6934,
            236.5242,
            237.7698,
            239.5555,
            241.0492,
            242.8233,
            244.0709,
            247.137,
            248.102,
            249.5737,
            251.0149,
            253.07,
            255.3063,
            256.3807,
            258.6104,
            259.8744,
            260.8051,
            263.5739,
            265.5579,
            266.615,
            267.9219,
            269.9704,
            271.4941,
            273.4596,
            275.5875,
            276.452,
            278.2507,
            279.2293,
            282.4651,
            283.2112,
            284.836,
            286.6674,
            287.9119,
            289.5799,
            291.8463,
            293.5584,
            294.9654,
            295.5733,
            297.9793,
            299.8403,
            301.6493,
            302.6967,
            304.8644,
            305.7289,
            307.2195,
            310.1095,
            311.1651,
            312.4278,
            313.9853,
            315.4756,
            317.7348,
            318.8531,
            321.1601,
            322.1446,
            323.467,
            324.8629,
            327.4439,
            329.0331,
            329.9532,
            331.4745,
            333.6454,
            334.2114,
            336.8419,
            338.34,
            339.8582,
            341.0423,
            342.0549,
            344.6617,
            346.3479,
            347.2727,
            349.3163,
            350.4084,
            351.8786,
            353.4889,
            356.0176,
            357.1513,
            357.9527,
            359.7438,
            361.2894,
            363.3313,
            364.736,
            366.2127,
            367.9936,
            368.9684,
            370.0509,
            373.0619,
            373.8649,
            375.8259,
            376.3241,
            378.4367,
            379.873,
            381.4845,
            383.4435,
            384.9561,
            385.8613,
            387.2229,
            388.8461,
            391.4561,
            392.2451,
            393.4277,
            395.5829,
            396.3819,
            397.9187,
            399.9851,
            401.8392,
            402.8619,
            404.2364,
            405.1344,
            407.5815,
            408.9472,
            410.5139,
            411.9723,
            413.2627,
            415.0188,
            415.4552,
            418.3877,
            419.8614,
            420.6438,
            422.0767,
            423.7166,
            425.0699,
            427.2088,
            428.1279,
            430.3287,
            431.3013,
            432.1386,
            433.8892,
            436.161,
            437.5817,
            438.6217,
            439.9184,
            441.6832,
            442.9045,
            444.3193,
            446.8606,
            447.4417,
            449.1485,
            450.1269,
            451.4033,
            453.9867,
            454.9747,
            456.3284,
            457.9039,
            459.5134,
            460.0879,
            462.0654,
            464.0573,
            465.6715,
            466.5703,
            467.439,
            469.536,
            470.7737,
            472.7992,
            473.8352,
            475.6003,
            476.769,
            478.0753,
            478.9422,
            481.8303,
            482.8348,
            483.8514,
            485.5391,
            486.5287,
            488.3806,
            489.6618,
            491.3988,
            493.3144,
            493.958,
            495.3588,
            496.4297,
            498.5808,
            500.3091,
            501.6044,
            502.2763,
            504.4998,
            505.4152,
            506.4642,
            508.8007,
            510.2642,
            511.5623,
            512.6231,
            513.669,
            515.4351,
            517.5897,
            518.2342,
            520.1063,
            521.5252,
            522.4567,
            523.9605,
            525.0774,
            527.9036,
            528.4062,
            529.8062,
            530.8669,
            532.6882,
            533.7796,
            535.6643,
            537.0698,
            538.4285,
            540.2132,
            540.6314,
            541.8474,
        ]
    )
    return (ZEROS,)


@app.cell
def _(np):
    """Shared number-theory, spectral, and animation helpers for the Riemann notebook."""
    import math

    def play_pause(label, duration=110, y=1.12):
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

    def primes_up_to(n):
        """All primes up to n by a boolean sieve."""
        if n < 2:
            return np.array([], dtype=int)
        sieve = np.ones(n + 1, dtype=bool)
        sieve[:2] = False
        for p in range(2, int(n**0.5) + 1):
            if sieve[p]:
                sieve[p * p :: p] = False
        return np.flatnonzero(sieve)

    def von_mangoldt(n):
        """Lambda(k) for k = 0..n: log p if k is a prime power p^m, else 0."""
        lam = np.zeros(n + 1)
        for p in primes_up_to(n):
            lp = math.log(p)
            pk = p
            while pk <= n:
                lam[pk] = lp
                pk *= p
        return lam

    def prime_staircase(primes, xs):
        """The counting function pi(x): number of primes up to each x."""
        return np.searchsorted(primes, xs, side="right").astype(float)

    def logarithmic_integral(xs):
        """Li(x) = int_2^x dt/log t by cumulative trapezoid, with xs[0] = 2."""
        integrand = 1.0 / np.log(xs)
        seg = 0.5 * (integrand[1:] + integrand[:-1]) * np.diff(xs)
        return np.concatenate(([0.0], np.cumsum(seg)))

    def zeta_real(s, terms=400):
        """zeta(s) on the real axis (s > 1) by Euler-Maclaurin: fast and accurate."""
        s = np.asarray(s, dtype=float)
        n = np.arange(1, terms + 1)
        head = np.sum(n[:, None] ** (-s[None, :]), axis=0)
        tail = terms ** (1 - s) / (s - 1) - 0.5 * terms ** (-s) + (s / 12.0) * terms ** (-s - 1)
        return head + tail

    def partial_euler(primes, s):
        """The partial Euler product prod_p (1 - p^-s)^-1 over the given primes."""
        out = np.ones_like(s)
        for p in primes:
            out = out / (1.0 - float(p) ** (-s))
        return out

    def theta_rs(t):
        """Riemann-Siegel theta(t), asymptotic expansion."""
        return t / 2 * np.log(t / (2 * np.pi)) - t / 2 - np.pi / 8 + 1 / (48 * t) + 7 / (5760 * t**3)

    def hardy_Z(ts):
        """Hardy's Z(t) with |Z(t)| = |zeta(1/2+it)|, via the Riemann-Siegel main sum + first correction."""
        ts = np.atleast_1d(ts).astype(float)
        out = np.zeros_like(ts)
        for i, tv in enumerate(ts):
            if tv < 1.0:
                out[i] = 0.0
                continue
            big = np.sqrt(tv / (2 * np.pi))
            nn = int(np.floor(big))
            th = theta_rs(tv)
            s = 0.0
            for n in range(1, nn + 1):
                s += math.cos(th - tv * math.log(n)) / math.sqrt(n)
            main = 2 * s
            p = big - nn
            c0 = math.cos(2 * np.pi * (p * p - p - 1 / 16)) / math.cos(2 * np.pi * p)
            out[i] = main + (-1) ** (nn - 1) * (tv / (2 * np.pi)) ** (-0.25) * c0
        return out

    def psi_true(xs, lam):
        """The Chebyshev function psi(x) = sum_{n<=x} Lambda(n)."""
        return np.array([float(lam[: min(math.floor(x), len(lam) - 1) + 1].sum()) for x in xs])

    def psi_explicit(xs, gammas):
        """The explicit-formula partial sum psi_K(x) = x - log 2pi - 0.5 log(1-x^-2) - sum 2 Re(x^rho/rho)."""
        smooth = xs - math.log(2 * np.pi) - 0.5 * np.log1p(-(xs**-2.0))
        if len(gammas) == 0:
            return smooth
        rho = 0.5 + 1j * gammas
        osc = 2.0 * np.real(np.power.outer(xs, rho) / rho).sum(axis=1)
        return smooth - osc

    def unfold(gammas):
        """Rescale ordinates to mean spacing 1: w_k = gamma_k log(gamma_k/2pi) / 2pi."""
        return gammas * np.log(gammas / (2 * np.pi)) / (2 * np.pi)

    def montgomery_R2(u):
        """The pair-correlation form factor 1 - (sin pi u / pi u)^2 (Montgomery / GUE)."""
        x = np.pi * np.asarray(u, dtype=float)
        sinc = np.where(np.abs(x) < 1e-12, 1.0, np.sin(x) / np.where(x == 0, 1.0, x))
        return 1 - sinc**2

    def pair_density(w, n, edges):
        """Histogram density of unfolded differences among the first n zeros, normalised to mean 1."""
        ww = w[:n]
        ww = (ww - ww[0]) * (n - 1) / (ww[-1] - ww[0])
        d = np.abs(ww[:, None] - ww[None, :])[np.triu_indices(n, k=1)]
        d = d[(d > 0) & (d <= edges[-1])]
        counts, _ = np.histogram(d, bins=edges)
        return counts / (n * (edges[1] - edges[0]))

    SQRT2 = math.sqrt(2.0)

    def H_flat(lam):
        """Certified simple-on-line proportion from the flat window: 2 - 1/lam - lam/3; H(1) = 2/3."""
        return 2.0 - 1.0 / lam - lam / 3.0

    def c_star(lam):
        """Montgomery-Taylor form factor sqrt2 tan(theta)/(1 + theta tan(theta)), theta = lam/sqrt2."""
        theta = lam / SQRT2
        return SQRT2 * np.tan(theta) / (1.0 + theta * np.tan(theta))

    def H_opt(lam):
        """Optimal-window proportion 2 - 1/c*(lam); H_opt(1) = 0.6725."""
        return 2.0 - 1.0 / c_star(lam)

    def H_d(lam):
        """Certified distinct-zero proportion (1 + H(lam))/2; H_d(1) = 5/6."""
        return (1.0 + H_flat(lam)) / 2.0

    def positive_index(mat, tol=1e-9):
        """Number of strictly positive eigenvalues of a real symmetric matrix."""
        w = np.linalg.eigvalsh((mat + mat.T) / 2)
        return int(np.sum(w > tol))

    def random_psd_sum(dim, rank, rng):
        """Random positive-semidefinite matrix as a sum of `rank` rank-one outer products."""
        p = np.zeros((dim, dim))
        for _ in range(rank):
            v = rng.standard_normal(dim)
            p += np.outer(v, v)
        return p

    def random_signature_block(dim, n_pos, n_neg, rng):
        """Random real-symmetric matrix with exactly n_pos positive and n_neg negative eigenvalues."""
        q, _ = np.linalg.qr(rng.standard_normal((dim, dim)))
        diag = np.zeros(dim)
        diag[:n_pos] = rng.uniform(0.2, 2.0, n_pos)
        diag[n_pos : n_pos + n_neg] = -rng.uniform(0.2, 2.0, n_neg)
        return q @ np.diag(diag) @ q.T

    return (
        H_d,
        H_flat,
        H_opt,
        SQRT2,
        c_star,
        hardy_Z,
        logarithmic_integral,
        math,
        montgomery_R2,
        pair_density,
        partial_euler,
        play_pause,
        positive_index,
        prime_staircase,
        primes_up_to,
        psi_explicit,
        psi_true,
        random_psd_sum,
        random_signature_block,
        unfold,
        von_mangoldt,
        zeta_real,
    )


@app.cell
def _(mo):
    mo.md(
        r"""
        # Riemann: the zeros, the critical line, and two thirds of them

        The primes $2, 3, 5, 7, 11, \dots$ thin out as you go, but not smoothly. Riemann's 1859
        idea was to study that irregularity through a single analytic object, the zeta function,
        and to reduce the whole question to the location of its zeros. The **Riemann hypothesis**
        is the claim that they all lie on one vertical line.

        This notebook follows the thread from the primes to an August 2026 theorem that at least
        two thirds of those zeros do lie on the line:

        1. the primes and the zeta function;
        2. the zeros, the functional equation, and the critical line;
        3. the explicit formula: zeros *are* the primes, transformed;
        4. measuring progress: the proportion on the line;
        5. two methods, and why one had stalled;
        6. the 2026 argument: a finite piece of Weil's form;
        7. a numerical framework that reproduces the bound;
        8. how far this road can go;
        9. how it was found, and what it is not.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 1. The primes and the zeta function

        Write $\pi(x)$ for the number of primes up to $x$. The **prime number theorem** (Hadamard,
        de la Vallee Poussin, 1896) says $\pi(x) \sim x/\log x$, and the sharper guess is the
        logarithmic integral $\operatorname{Li}(x) = \int_2^x dt/\log t$:

        $$
        \begin{aligned}
        \pi(x) &\sim \frac{x}{\log x}                 && \text{density of primes near } x \text{ is about } 1/\log x \\
        \pi(x) &= \operatorname{Li}(x) + E(x)         && \operatorname{Li}(x) \text{ is the closer estimate} \\
        E(x)   &= \text{the error we want to control.}
        \end{aligned}
        $$

        The whole subject is the size of $E(x)$.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, logarithmic_integral, np, prime_staircase, primes_up_to, style_subplot_axes):
    _xmax = 1000
    _xs = np.linspace(2.0, _xmax, 4000)
    _primes = primes_up_to(_xmax)
    _pi = prime_staircase(_primes, _xs)
    _xlog = _xs / np.log(_xs)
    _li = logarithmic_integral(_xs)

    _fig = go.Figure()
    _fig.add_trace(
        go.Scatter(
            x=_xs,
            y=_pi,
            mode="lines",
            line={"color": COLORS["quaternary"], "width": 2.5, "shape": "hv"},
            name="π(x)  (primes up to x)",
        )
    )
    _fig.add_trace(
        go.Scatter(x=_xs, y=_li, mode="lines", line={"color": COLORS["primary"], "width": 2}, name="Li(x)  (closer)")
    )
    _fig.add_trace(
        go.Scatter(
            x=_xs,
            y=_xlog,
            mode="lines",
            line={"color": COLORS["secondary"], "width": 2, "dash": "dash"},
            name="x / log x",
        )
    )

    _fig.update_layout(**base_layout(title="Counting the primes: π(1000) = 168", height=460))
    _fig.update_xaxes(title_text="x")
    _fig.update_yaxes(title_text="count")
    style_subplot_axes(_fig, show_ticklabels=True)
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The staircase $\pi(x)$ jumps by one at each prime. Both $x/\log x$ and the closer
        $\operatorname{Li}(x)$ track it; every wobble of the staircase away from
        $\operatorname{Li}(x)$ is the error $E(x)$, which the zeros of zeta govern.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The primes enter zeta through **Euler's product**, an analytic encoding of unique
        factorisation. For $\operatorname{Re} s > 1$,

        $$
        \begin{aligned}
        \zeta(s) &= \sum_{n=1}^{\infty} n^{-s}                    && \text{a Dirichlet series, convergent for } \operatorname{Re} s > 1 \\
                 &= \prod_{p \text{ prime}} \frac{1}{1 - p^{-s}}  && \text{every integer factors into primes in one way.}
        \end{aligned}
        $$

        That product form is the reason a statement about zeta is a statement about the primes.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, np, partial_euler, primes_up_to, style_subplot_axes, zeta_real):
    _s = np.linspace(1.2, 4.0, 400)
    _primes = primes_up_to(30)
    _zeta = zeta_real(_s)

    _fig = go.Figure()
    _fig.add_trace(go.Scatter(x=_s, y=_zeta, mode="lines", line={"color": COLORS["text"], "width": 3}, name="ζ(s)"))
    _palette = [COLORS["accent3"], COLORS["tertiary"], COLORS["primary"], COLORS["quaternary"]]
    for _k, _col in zip([1, 2, 3, 5], _palette, strict=False):
        _fig.add_trace(
            go.Scatter(
                x=_s,
                y=partial_euler(_primes[:_k], _s),
                mode="lines",
                line={"color": _col, "width": 1.8, "dash": "dot"},
                name=f"product over first {_k} prime" + ("s" if _k > 1 else ""),
            )
        )

    _fig.update_layout(**base_layout(title="Partial Euler products climbing to ζ(s)", height=440))
    _fig.update_xaxes(title_text="s")
    _fig.update_yaxes(title_text="value", range=[0.8, 5.0])
    style_subplot_axes(_fig, show_ticklabels=True)
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Each dotted curve is the product over the first few primes; truncating at more primes
        climbs toward the solid $\zeta(s)$ on the real axis. Even a handful of primes already
        approximates zeta.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 2. The zeros, the functional equation, and the critical line

        The series only converges for $\operatorname{Re} s > 1$, but zeta extends to a single
        analytic function on the whole plane (one pole, at $s = 1$). The continuation satisfies a
        reflection, the **functional equation**, cleanest in the completed form:

        $$
        \begin{aligned}
        \xi(s) &:= \tfrac12 s(s-1)\,\pi^{-s/2}\,\Gamma\!\left(\tfrac{s}{2}\right)\zeta(s) && \text{the completed zeta, entire} \\
        \xi(s) &= \xi(1 - s)                                                              && \text{symmetry across } \operatorname{Re} s = \tfrac12.
        \end{aligned}
        $$

        The Gamma factor forces zeta to vanish at $s = -2, -4, -6, \dots$: the **trivial zeros**,
        understood. Everything else lives in the **critical strip** $0 < \operatorname{Re} s < 1$,
        and the functional equation makes it symmetric about the **critical line**
        $\operatorname{Re} s = \tfrac12$. Riemann computed the first few zeros, found them all on
        that line, and called it "sehr wahrscheinlich" (very probable) that they all are.

        > **The Riemann hypothesis.** Every nontrivial zero $\rho = \beta + i\gamma$ of $\zeta(s)$
        > has $\beta = \tfrac12$.
        """
    )
    return


@app.cell
def _(COLORS, ZEROS, base_layout, go, np, style_subplot_axes):
    _trivial = np.array([-2, -4, -6, -8, -10])
    _gam = ZEROS[:12]

    _fig = go.Figure()
    _fig.add_shape(type="rect", x0=0, x1=1, y0=-46, y1=46, fillcolor="rgba(0,212,255,0.07)", line={"width": 0})
    _fig.add_vline(x=0.5, line={"color": COLORS["quaternary"], "width": 2, "dash": "dash"})
    _fig.add_annotation(
        x=0.5, y=44, text="critical line  Re s = 1/2", showarrow=False, font={"color": COLORS["quaternary"], "size": 12}
    )

    _fig.add_trace(
        go.Scatter(
            x=_trivial,
            y=np.zeros_like(_trivial),
            mode="markers",
            marker={"color": COLORS["muted"], "size": 9, "symbol": "x"},
            name="trivial zeros",
        )
    )
    _fig.add_trace(
        go.Scatter(
            x=[1],
            y=[0],
            mode="markers",
            marker={"color": COLORS["secondary"], "size": 12, "symbol": "diamond"},
            name="pole at s = 1",
        )
    )
    _fig.add_trace(
        go.Scatter(
            x=np.full_like(_gam, 0.5),
            y=_gam,
            mode="markers",
            marker={"color": COLORS["primary"], "size": 8},
            name="nontrivial zeros",
        )
    )
    _fig.add_trace(
        go.Scatter(
            x=np.full_like(_gam, 0.5),
            y=-_gam,
            mode="markers",
            marker={"color": COLORS["primary"], "size": 8},
            showlegend=False,
        )
    )

    _fig.update_layout(**base_layout(title="The critical strip: trivial zeros, the pole, and the line", height=560))
    _fig.update_xaxes(title_text="Re s", range=[-11.5, 2.5])
    _fig.update_yaxes(title_text="Im s", range=[-46, 46])
    style_subplot_axes(_fig, show_ticklabels=True)
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The trivial zeros sit at $s = -2, -4, \dots$ and the pole at $s = 1$. The first twelve
        nontrivial zeros (and their conjugates) are stacked on the dashed critical line
        $\operatorname{Re} s = \tfrac12$. The hypothesis is the claim that this column never leans
        off the line.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The honest way to *see* zeros on the line is Hardy's $Z(t)$, a real function of a real
        variable with $|Z(t)| = |\zeta(\tfrac12 + it)|$, so a zero on the line is an ordinary
        **sign change** of $Z$. Hardy (1914) proved there are infinitely many such crossings; the
        hypothesis is that there are no *other* zeros anywhere in the strip.
        """
    )
    return


@app.cell
def _(COLORS, ZEROS, base_layout, go, hardy_Z, np, play_pause, style_subplot_axes):
    _tmax = 50.0
    _ts = np.linspace(0.5, _tmax, 360)
    _z = hardy_Z(_ts)
    _gam = np.array([_g for _g in ZEROS if _g <= _tmax])

    _n_frames = 40
    _schedule = [0] * 3 + list(range(1, _n_frames + 1)) + [_n_frames] * 5

    def _curve(fi):
        _tnow = 0.5 + (_schedule[fi] / _n_frames) * (_tmax - 0.5)
        _m = _ts <= _tnow
        return go.Scatter(x=_ts[_m], y=_z[_m], mode="lines", line={"color": COLORS["primary"], "width": 2.5})

    def _marks(fi):
        _tnow = 0.5 + (_schedule[fi] / _n_frames) * (_tmax - 0.5)
        _g = _gam[_gam <= _tnow]
        return go.Scatter(
            x=_g,
            y=np.zeros_like(_g),
            mode="markers",
            marker={"color": COLORS["secondary"], "size": 9},
            showlegend=False,
        )

    _fig = go.Figure()
    _fig.add_hline(y=0, line={"color": COLORS["muted"], "width": 1})
    _fig.add_trace(_curve(0))
    _fig.add_trace(_marks(0))

    _fig.frames = [
        go.Frame(data=[_curve(_fi), _marks(_fi)], traces=[1, 2], name=str(_fi)) for _fi in range(len(_schedule))
    ]

    _fig.update_layout(**base_layout(title="Hardy Z(t): each sign change is a zero on the line", height=440))
    _fig.update_xaxes(title_text="t  (height on the critical line)", range=[0, _tmax])
    _fig.update_yaxes(title_text="Z(t)", range=[-3.5, 4.5])
    style_subplot_axes(_fig, show_ticklabels=True)
    _fig.update_layout(updatemenus=play_pause("▶ Scan up the line"))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Scanning up the line, each red dot marks a sign change of $Z(t)$, a zero with
        $\beta = \tfrac12$. The first ten land at $\gamma_1 = 14.13,\ \gamma_2 = 21.02, \dots$,
        the same heights stacked on the strip above. ($Z$ here is the Riemann-Siegel
        approximation, accurate enough to place every crossing.)
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The functional equation also pins the *shape* of any hypothetical off-line zero. If $\rho$
        is a zero, so are $1 - \bar\rho$ (across the line), $\bar\rho$ (across the real axis), and
        $1 - \rho$. So off-line zeros come in quadruples; on the line the quadruple collapses to a
        conjugate pair $\tfrac12 \pm i\gamma$. That $\rho \leftrightarrow 1 - \bar\rho$ pairing is
        the whole hinge of the 2026 argument in Part 6.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, make_subplots, style_subplot_axes):
    _fig = make_subplots(rows=1, cols=2, subplot_titles=("Off-line zero: a quadruple", "On the line: a conjugate pair"))
    for _c in (1, 2):
        _fig.add_vline(x=0.5, line={"color": COLORS["quaternary"], "width": 1.5, "dash": "dash"}, row=1, col=_c)
        _fig.add_hline(y=0, line={"color": COLORS["muted"], "width": 1}, row=1, col=_c)

    _off = [(0.75, 20.0), (0.25, 20.0), (0.75, -20.0), (0.25, -20.0)]
    _rectx = [0.75, 0.25, 0.25, 0.75, 0.75]
    _recty = [20.0, 20.0, -20.0, -20.0, 20.0]
    _fig.add_trace(
        go.Scatter(
            x=_rectx,
            y=_recty,
            mode="lines",
            line={"color": COLORS["secondary"], "width": 1, "dash": "dot"},
            showlegend=False,
        ),
        row=1,
        col=1,
    )
    _fig.add_trace(
        go.Scatter(
            x=[p[0] for p in _off],
            y=[p[1] for p in _off],
            mode="markers",
            marker={"color": COLORS["secondary"], "size": 11},
            showlegend=False,
        ),
        row=1,
        col=1,
    )

    _fig.add_trace(
        go.Scatter(
            x=[0.5, 0.5],
            y=[14.13, -14.13],
            mode="markers",
            marker={"color": COLORS["primary"], "size": 11},
            showlegend=False,
        ),
        row=1,
        col=2,
    )

    _fig.update_layout(**base_layout(title="Functional-equation symmetry", height=420))
    for _c in (1, 2):
        _fig.update_xaxes(title_text="Re s", range=[0, 1], row=1, col=_c)
        _fig.update_yaxes(title_text="Im s", range=[-30, 30], row=1, col=_c)
    style_subplot_axes(_fig, show_ticklabels=True)
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Left: an off-line zero drags three partners into a rectangle straddling the line and the
        real axis. Right: on the line the four collapse to the conjugate pair $\tfrac12 \pm i\gamma$.
        The $\rho \leftrightarrow 1 - \bar\rho$ pairing (reflection across the line) is the hinge of
        Part 6.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 3. Why the zeros matter: the explicit formula

        The zeros are not a curiosity: they *are* the primes, transformed. Von Mangoldt's
        **explicit formula** makes the dictionary exact. With the prime-power counting function
        $\psi(x) = \sum_{p^m \le x} \log p$,

        $$
        \psi(x) = x - \sum_{\rho} \frac{x^{\rho}}{\rho} - \log(2\pi) - \tfrac12 \log\!\left(1 - x^{-2}\right),
        $$

        the sum running over all nontrivial zeros. The main term $x$ is the prime number theorem;
        each zero $\rho = \beta + i\gamma$ adds an oscillation $x^{\rho}/\rho$ of size $x^{\beta}$
        and frequency $\gamma$. **The zeros are the harmonics of the primes.**
        """
    )
    return


@app.cell
def _(COLORS, ZEROS, base_layout, go, math, np, play_pause, psi_explicit, psi_true, style_subplot_axes, von_mangoldt):
    _xs = np.linspace(2.0, 50.0, 500)
    _lam = von_mangoldt(50)
    _true = psi_true(_xs, _lam)
    _kmax = 40
    _curves = [psi_explicit(_xs, ZEROS[:_k]) for _k in range(_kmax + 1)]
    _schedule = list(range(_kmax + 1)) + [_kmax] * 6

    _fig = go.Figure()
    _fig.add_trace(
        go.Scatter(
            x=_xs, y=_true, mode="lines", line={"color": COLORS["muted"], "width": 2, "shape": "hv"}, name="true ψ(x)"
        )
    )
    _fig.add_trace(
        go.Scatter(
            x=_xs,
            y=_curves[0],
            mode="lines",
            line={"color": COLORS["primary"], "width": 2.5},
            name="explicit-formula sum",
        )
    )

    _fig.frames = [
        go.Frame(
            data=[go.Scatter(x=_xs, y=_curves[_schedule[_fi]])],
            traces=[1],
            name=str(_fi),
            layout={"title": {"text": f"Rebuilding ψ(x) from {_schedule[_fi]} zero pairs"}},
        )
        for _fi in range(len(_schedule))
    ]

    _fig.update_layout(**base_layout(title="Rebuilding ψ(x) from 0 zero pairs", height=460))
    _fig.update_xaxes(title_text="x", range=[2, 50])
    _fig.update_yaxes(title_text="ψ(x)", range=[-2, 55])
    style_subplot_axes(_fig, show_ticklabels=True)
    _fig.update_layout(updatemenus=play_pause("▶ Add zero pairs"))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Start from the straight line $x$ and add the wave $2\operatorname{Re}(x^{\rho}/\rho)$ from
        each zero pair: the running sum sharpens into the true staircase (grey), jumping by
        $\log p$ at each prime power. Primes and zeros are two views of the same object.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        This is why the *position* of the zeros is the whole game. A zero's contribution has size
        $x^{\beta}$, so

        $$
        \begin{aligned}
        \psi(x) - x &= -\sum_{\rho} \frac{x^{\rho}}{\rho} + O(1)   && \text{the prime error is the zero sum} \\
        |\psi(x) - x| &\ll x^{\Theta}\log^2 x,                     && \Theta = \sup_{\rho}\operatorname{Re}\rho \text{ (rightmost zero)} \\
        \text{RH} &\iff \Theta = \tfrac12 \iff |\psi(x) - x| \ll x^{1/2}\log^2 x. && \text{smallest possible error.}
        \end{aligned}
        $$

        The hypothesis is exactly the statement that the primes are as evenly distributed as they
        possibly could be: a single zero off the line at $\beta > \tfrac12$ would widen the error
        band from $x^{1/2}$ to $x^{\beta}$. So "how far right does a zero sit?" is the question,
        and pinning *most* zeros to the line is real progress on the primes.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, np, style_subplot_axes, von_mangoldt):
    _xhi = 1000
    _lam = von_mangoldt(_xhi)
    _cum = np.cumsum(_lam)
    _xs = np.arange(2, _xhi + 1)
    _err = _cum[2 : _xhi + 1] - _xs
    _rh = 1.5 * _xs**0.5
    _off = 1.5 * _xs**0.7

    _fig = go.Figure()
    _fig.add_trace(
        go.Scatter(
            x=_xs,
            y=_off,
            mode="lines",
            line={"color": COLORS["secondary"], "width": 1.5, "dash": "dash"},
            name="±x^0.7  (a zero off the line)",
        )
    )
    _fig.add_trace(
        go.Scatter(
            x=_xs,
            y=-_off,
            mode="lines",
            line={"color": COLORS["secondary"], "width": 1.5, "dash": "dash"},
            showlegend=False,
        )
    )
    _fig.add_trace(
        go.Scatter(
            x=_xs,
            y=_rh,
            mode="lines",
            line={"color": COLORS["primary"], "width": 2},
            name="±x^0.5  (RH: narrowest band)",
        )
    )
    _fig.add_trace(
        go.Scatter(x=_xs, y=-_rh, mode="lines", line={"color": COLORS["primary"], "width": 2}, showlegend=False)
    )
    _fig.add_trace(
        go.Scatter(x=_xs, y=_err, mode="lines", line={"color": COLORS["quaternary"], "width": 1.5}, name="ψ(x) − x")
    )

    _fig.update_layout(**base_layout(title="The rightmost zero sets the prime error band", height=440))
    _fig.update_xaxes(title_text="x")
    _fig.update_yaxes(title_text="ψ(x) − x", range=[-90, 90])
    style_subplot_axes(_fig, show_ticklabels=True)
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The error $\psi(x) - x$ (gold) stays inside an envelope $x^{\Theta}$. On the hypothesis
        $\Theta = \tfrac12$ (the narrow band); a single zero at $\beta = 0.7$ would widen it to the
        dashed $x^{0.7}$ band. Bounding the *proportion* of zeros on the line is a first grip on
        this envelope.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 4. Measuring progress: the proportion on the line

        Since the hypothesis is out of reach, the field measures partial progress. Count zeros by
        height. The total $N(T)$ is known exactly (Riemann-von Mangoldt); $N_0(T)$ counts those on
        the line:

        $$
        \begin{aligned}
        N(T)   &= \frac{T}{2\pi}\log\frac{T}{2\pi} - \frac{T}{2\pi} + O(\log T) && \text{all nontrivial zeros up to height } T \\
        N_0(T) &= \#\{\rho : 0 < \gamma \le T,\ \beta = \tfrac12\}              && \text{those on the critical line} \\
        \kappa &= \liminf_{T \to \infty} \frac{N_0(T)}{N(T)}                    && \text{the guaranteed fraction on the line.}
        \end{aligned}
        $$

        The hypothesis is $\kappa = 1$. Short of that, the history of proven lower bounds is a
        ladder, and the 2026 result is its latest rung, the largest single step in the table.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, style_subplot_axes):
    _rungs = [
        ("Selberg 1942", 0.03, "> 0", COLORS["muted"]),
        ("Levinson 1974", 1 / 3, "1/3", COLORS["tertiary"]),
        ("Conrey 1989", 2 / 5, "2/5", COLORS["tertiary"]),
        ("PRZZ 2020", 5 / 12, "5/12", COLORS["primary"]),
        ("Claude 2026", 2 / 3, "2/3 (opt. 0.6725)", COLORS["secondary"]),
    ]
    _names = [r[0] for r in _rungs]
    _vals = [r[1] for r in _rungs]
    _labels = [r[2] for r in _rungs]
    _cols = [r[3] for r in _rungs]

    _fig = go.Figure()
    _fig.add_trace(
        go.Bar(
            x=_vals,
            y=_names,
            orientation="h",
            marker={"color": _cols},
            text=_labels,
            textposition="outside",
            showlegend=False,
        )
    )
    _fig.add_vline(x=1.0, line={"color": COLORS["quaternary"], "width": 2, "dash": "dash"})
    _fig.add_annotation(
        x=1.0, y=4.4, text="RH: 100%", showarrow=False, font={"color": COLORS["quaternary"], "size": 12}
    )

    _fig.update_layout(**base_layout(title="The proportion ladder: κ from 1/3 to 2/3", height=420))
    _fig.update_xaxes(title_text="certified proportion on the line", range=[0, 1.12])
    style_subplot_axes(_fig, show_ticklabels=True)
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Each bar is the proven lower bound $\kappa$ at its date, against the $100\%$ (dashed) the
        hypothesis claims. The record held at $5/12 = 41.66\%$ from 2020; the 2026 argument raises
        the guarantee to $2/3$ (optimised $0.6725$). The gap to $100\%$ is not shown to be off the
        line, only not yet certified (Part 9).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 5. Two methods: mollifier and pair correlation

        Every rung from Levinson to PRZZ uses **Levinson's method**: multiply zeta by a
        **mollifier**, a short Dirichlet polynomial tuned to tame it near the line, and count sign
        changes of the smoothed real function. Refining the mollifier carried $1/3 \to 2/5 \to
        5/12$, and then it stalled at $0.4166$ for fifty years.

        The other lineage is **Montgomery (1973)**: instead of locating zeros one at a time, study
        their pairwise statistics. The gaps between zeros *repel*, following the same law as the
        eigenvalue spacings of a random Hermitian matrix, and that repulsion is the raw material the
        2026 argument measures.
        """
    )
    return


@app.cell
def _(COLORS, ZEROS, base_layout, go, montgomery_R2, np, pair_density, play_pause, style_subplot_axes, unfold):
    _w = unfold(ZEROS)
    _umax = 3.0
    _bins = 45
    _edges = np.linspace(0.0, _umax, _bins + 1)
    _centres = 0.5 * (_edges[:-1] + _edges[1:])
    _curve_u = np.linspace(1e-6, _umax, 400)
    _curve = montgomery_R2(_curve_u)

    _counts = [40, 80, 140, 220, 300]

    _fig = go.Figure()
    _fig.add_trace(
        go.Bar(
            x=_centres,
            y=pair_density(_w, _counts[0], _edges),
            marker={"color": "rgba(0,212,255,0.55)"},
            name="normalised gaps",
        )
    )
    _fig.add_trace(
        go.Scatter(
            x=_curve_u,
            y=_curve,
            mode="lines",
            line={"color": COLORS["secondary"], "width": 3},
            name="1 − (sin πu / πu)²",
        )
    )

    _fig.frames = [
        go.Frame(
            data=[go.Bar(x=_centres, y=pair_density(_w, _n, _edges))],
            traces=[0],
            name=str(_n),
            layout={"title": {"text": f"Pair correlation from {_n} zeros"}},
        )
        for _n in _counts
    ]

    _fig.update_layout(**base_layout(title="Pair correlation from 40 zeros", height=460))
    _fig.update_xaxes(title_text="normalised gap u", range=[0, _umax])
    _fig.update_yaxes(title_text="density", range=[0, 1.5])
    style_subplot_axes(_fig, show_ticklabels=True)
    _fig.update_layout(updatemenus=play_pause("▶ Add more zeros"), bargap=0.05)
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Histogram of the gaps between real zero heights, unfolded to mean spacing 1. As more zeros
        enter, the bars settle onto Montgomery's curve $1 - (\sin \pi u / \pi u)^2$: the dip to $0$
        at $u = 0$ is the repulsion the second moment measures.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Under the hypothesis, Montgomery read a second moment off this curve and concluded that at
        least $2/3$ of the zeros are simple. The $2/3$ comes from a one-line integer inequality,
        $m^2 \ge 2m - 1$: a multiple zero costs the second moment more than it pays the count.
        Every such number was **conditional on the hypothesis**, because the argument reads the
        "zero side" as a sum over *real* ordinates, which needs the zeros on the line to begin
        with.

        Between 2022 and 2026, Baluyot-Goldston-Suriajaya-Turnage-Butterbaugh and
        Goldston-Suriajaya showed that Montgomery's *prime side* (the arithmetic half of the second
        moment) is a mean value of a Dirichlet polynomial of length $\le T$, hence
        **unconditional**: it holds for the sum over *all* zeros, on the line or not. They isolated
        the one remaining obstacle, the termwise positivity of the zero side that fails off the
        line. Part 6 removes it.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 6. The 2026 argument: a finite piece of Weil's form

        The argument uses no mollifier. It makes Montgomery's pair correlation unconditional by
        replacing the one place the hypothesis was used (the positivity of the zero side) with
        linear algebra.

        **Weil's form.** Package Weil's explicit formula as a Hermitian pairing on test functions:

        $$
        W(f, g) = \sum_{\rho} m_{\rho}\, \hat f(\gamma_{\rho})\, \overline{\hat g(\gamma_{\rho})},
        \qquad W(f, f) \ge 0 \text{ for all } f \iff \text{RH}.
        $$

        Testing positivity everywhere is as hard as the hypothesis. Instead, restrict $W$ to a
        small, explicit family $V$ of $d \approx \lambda N$ modulated windows and study the
        $d \times d$ matrix $G$. Three facts are then available.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        **(Z) Zero side.** By the functional equation $G = P + Q$: each distinct on-line point is a
        rank-one **positive** block in $P$; each off-line pair $\{\rho, 1 - \bar\rho\}$ is a block
        of signature $(1, 1)$ in $Q$ (one positive, one negative eigenvalue). An on-line zero
        pushes the form up; an off-line pair pushes it up once and down once. By **Sylvester's law
        of inertia**, the number of positive eigenvalues of $G$ is at most $s + p$ ($s$ on-line
        points, $p$ off-line pairs).

        **(P) Prime side.** The two moments of $G$ are, by the explicit formula, integrals over
        prime powers, and by the 2022-24 work they are **unconditional**:

        $$
        \operatorname{tr} G = (1 + o(1))\,N,
        \qquad
        \|G\|_F^2 = \operatorname{tr} G^2 = \left(\tfrac{1}{\lambda} + \tfrac{\lambda}{3} + o(1)\right)N.
        $$

        **(L) Linear algebra.** The rank-trace inequality
        $r \ge 2\operatorname{tr}P + 4\operatorname{tr}Q - 4b - \|P + Q\|_F^2$ is the matrix
        analogue of $m^2 \ge 2m - 1$. Feeding (Z) and (P) into it, the number $s$ of distinct
        on-line points satisfies

        $$
        \begin{aligned}
        s &\ge \left(2 - \frac{1}{\lambda} - \frac{\lambda}{3} - o(1)\right)N = (H(\lambda) - o(1))N, \\
        H(1) &= \tfrac23.
        \end{aligned}
        $$

        That is Theorem A: $\liminf N_0(T)/N(T) \ge 2/3$.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, np, play_pause, positive_index, style_subplot_axes):
    _dim = 30
    _n_online = 15
    _n_offline = 8
    _rng = np.random.default_rng(1859)

    def _unit():
        _v = _rng.standard_normal(_dim)
        return _v / np.linalg.norm(_v)

    _blocks = []
    for _ in range(_n_online):
        _v = _unit()
        _blocks.append(("online", (0.6 + 0.8 * _rng.random()) * np.outer(_v, _v)))
    for _ in range(_n_offline):
        _u1 = _unit()
        _u2 = _rng.standard_normal(_dim)
        _u2 -= (_u2 @ _u1) * _u1
        _u2 /= np.linalg.norm(_u2)
        _a, _b = 0.6 + 0.8 * _rng.random(), 0.6 + 0.8 * _rng.random()
        _blocks.append(("offline", _a * np.outer(_u1, _u1) - _b * np.outer(_u2, _u2)))

    _G = np.zeros((_dim, _dim))
    _states = []
    _s_count = _p_count = 0
    for _kind, _blk in _blocks:
        _G = _G + _blk
        if _kind == "online":
            _s_count += 1
        else:
            _p_count += 1
        _eigs = np.sort(np.linalg.eigvalsh((_G + _G.T) / 2))[::-1]
        _states.append((_eigs.copy(), positive_index(_G), _s_count, _p_count, _kind))

    def _bars(state):
        _eigs, _nplus, _s, _p, _kind = state
        _cols = [
            COLORS["tertiary"] if _e > 1e-9 else (COLORS["secondary"] if _e < -1e-9 else COLORS["muted"])
            for _e in _eigs
        ]
        return go.Bar(x=list(range(1, _dim + 1)), y=_eigs, marker={"color": _cols}, showlegend=False)

    def _readout(state):
        _eigs, _nplus, _s, _p, _kind = state
        return go.Scatter(
            x=[_dim * 0.62],
            y=[max(_eigs) * 0.8 + 0.5],
            mode="text",
            text=[f"n₊ = {_nplus} ≤ s + p = {_s} + {_p} = {_s + _p}"],
            textfont={"color": COLORS["highlight"], "size": 14},
            showlegend=False,
        )

    _fig = go.Figure()
    _fig.add_trace(_bars(_states[0]))
    _fig.add_trace(_readout(_states[0]))
    _fig.frames = [
        go.Frame(
            data=[_bars(_st), _readout(_st)],
            traces=[0, 1],
            name=str(_i),
            layout={"title": {"text": f"Adding {_st[4]} block {_i + 1}/{len(_states)}"}},
        )
        for _i, _st in enumerate(_states)
    ]

    _fig.update_layout(**base_layout(title="G = P + Q: signs of the eigenvalues (green +, red −)", height=460))
    _fig.update_xaxes(title_text="eigenvalue index")
    _fig.update_yaxes(title_text="eigenvalue", range=[-2.5, 9])
    style_subplot_axes(_fig, show_ticklabels=True)
    _fig.update_layout(updatemenus=play_pause("▶ Add the blocks", duration=350))
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Each added on-line point stacks a positive (green) direction; each off-line pair adds one
        positive and one negative (red). The readout tracks the positive index $n_+$ against the
        Sylvester ceiling $s + p$: counting positive eigenvalues against the fixed trace and
        Frobenius norm is what pins two thirds of the zeros to the line, with no positivity assumed
        off it.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        No mollifier, no zero-density estimate, no zero-free region, and no assumption that any
        zero is on the line. The same inequality with the simple points on the rank side gives
        Theorem B (the $2/3$ are simple *and* on the line) and Theorem C ($5/6$ of the zeros are
        distinct). Optimising the test window (Montgomery-Taylor, still bandwidth $\le 1$) sharpens
        the constants to $0.6725$, $0.6725$, $0.83625$ (Theorem D), with the same values for a
        Dirichlet $L$-function (Theorem E):

        $$
        H(\lambda) = 2 - \frac{1}{\lambda} - \frac{\lambda}{3},
        \qquad H_d(\lambda) = \frac{1 + H(\lambda)}{2},
        \qquad F(\lambda) = \frac{\lambda}{1 + \lambda^2/3}.
        $$
        """
    )
    return


@app.cell
def _(COLORS, H_d, H_flat, H_opt, base_layout, go, np, style_subplot_axes):
    _lam = np.linspace(0.3, 1.0, 400)

    _fig = go.Figure()
    _fig.add_hline(y=5 / 12, line={"color": COLORS["muted"], "width": 1.5, "dash": "dot"})
    _fig.add_annotation(
        x=0.34,
        y=5 / 12 + 0.03,
        text="previous record 5/12",
        showarrow=False,
        font={"color": COLORS["muted"], "size": 11},
    )
    _fig.add_trace(
        go.Scatter(
            x=_lam,
            y=H_d(_lam),
            mode="lines",
            line={"color": COLORS["accent3"], "width": 2, "dash": "dash"},
            name="H_d(λ)  distinct → 5/6",
        )
    )
    _fig.add_trace(
        go.Scatter(
            x=_lam,
            y=H_opt(_lam),
            mode="lines",
            line={"color": COLORS["primary"], "width": 3},
            name="optimal window → 0.6725",
        )
    )
    _fig.add_trace(
        go.Scatter(
            x=_lam,
            y=H_flat(_lam),
            mode="lines",
            line={"color": COLORS["secondary"], "width": 3},
            name="flat window H(λ) → 2/3",
        )
    )
    _fig.add_trace(
        go.Scatter(
            x=[1.0, 1.0],
            y=[H_flat(1.0), H_opt(1.0)],
            mode="markers",
            marker={"color": COLORS["quaternary"], "size": 10},
            showlegend=False,
        )
    )

    _fig.update_layout(**base_layout(title="The certified proportion versus bandwidth λ", height=440))
    _fig.update_xaxes(title_text="bandwidth λ", range=[0.3, 1.05])
    _fig.update_yaxes(title_text="certified proportion", range=[0.2, 0.9])
    style_subplot_axes(_fig, show_ticklabels=True)
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The flat window $H(\lambda)$ reaches $2/3$ at the full bandwidth $\lambda = 1$; the optimal
        Montgomery-Taylor window sits just above it at $0.6725$; $H_d$ gives the distinct-zero count
        ($5/6$ at $\lambda = 1$). All clear the previous record $5/12$ (dotted).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 7. A numerical framework that reproduces the bound

        The finite object of Part 6 is small and explicit, so its one non-classical step, the
        rank-trace inequality, can be checked directly. (At the heights reachable here the
        hypothesis is already verified, so these certificates certify nothing *new*; the point is
        that the finite linear algebra the proof rests on is self-checking.)

        **The rank-trace inequality holds, always.** For random symmetric $P \succeq 0$ of rank
        $\le r$ and $Q$ with at most $b$ positive eigenvalues, the slack
        $r - (2\operatorname{tr}P + 4\operatorname{tr}Q - 4b - \|P+Q\|_F^2)$ should never be
        negative. It is the matrix analogue of $m^2 \ge 2m - 1$.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, np, random_psd_sum, random_signature_block, style_subplot_axes):
    _rng = np.random.default_rng(20260810)

    _slacks = []
    for _ in range(4000):
        _d = int(_rng.integers(2, 9))
        _r = int(_rng.integers(0, _d + 1))
        _b = int(_rng.integers(0, _d + 1))
        _P = random_psd_sum(_d, _r, _rng) if _r > 0 else np.zeros((_d, _d))
        _npos = int(_rng.integers(0, _b + 1))
        _nneg = int(_rng.integers(0, _d - _npos + 1))
        _Q = random_signature_block(_d, _npos, _nneg, _rng) if (_npos + _nneg) > 0 else np.zeros((_d, _d))
        _S = _P + _Q
        _rhs = 2 * np.trace(_P) + 4 * np.trace(_Q) - 4 * _b - float(np.sum(_S * _S))
        _slacks.append(_r - _rhs)
    _slacks = np.array(_slacks)
    _violations = int(np.sum(_slacks < -1e-6))

    _fig = go.Figure()
    _fig.add_trace(go.Histogram(x=_slacks, nbinsx=60, marker={"color": "rgba(78,205,196,0.6)"}, showlegend=False))
    _fig.add_vline(x=0.0, line={"color": COLORS["secondary"], "width": 2, "dash": "dash"})
    _fig.add_annotation(
        x=0.0,
        y=1.0,
        yref="paper",
        yanchor="top",
        text=f"  slack = 0   ·   {_violations} violations / {len(_slacks)} trials",
        showarrow=False,
        font={"color": COLORS["highlight"], "size": 13},
        xanchor="left",
    )

    _fig.update_layout(**base_layout(title="Rank-trace inequality: slack ≥ 0 on every random instance", height=420))
    _fig.update_xaxes(title_text="slack  r − (rank-trace right-hand side)")
    _fig.update_yaxes(title_text="count")
    style_subplot_axes(_fig, show_ticklabels=True)
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The slack over thousands of random and adversarial instances sits entirely to the right of
        zero (dashed): zero violations. The one non-classical step of the proof is a plain fact
        about matrices.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        **The certificate never lies.** By Sylvester's law the positive index obeys
        $n_+ \le s + p$, so $n_+ - p$ is a lower bound on the on-line count $s$. Replace true
        on-line points by synthetic off-line pairs of growing depth (holding the total fixed): the
        certified count $n_+ - p$ falls in step with the true $s$ and never rises above it. Each
        off-line pair, one positive direction and one negative, lowers the certificate by exactly
        one, mirroring the signature-$(1,1)$ accounting.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, np, positive_index, random_psd_sum, random_signature_block, style_subplot_axes):
    _dim = 60
    _rng = np.random.default_rng(20260810)

    _configs = [(30, 0, 0.0), (24, 6, 0.5), (18, 12, 1.0), (12, 18, 1.5), (6, 24, 2.0), (0, 30, 2.5)]
    _true_online = []
    _certified = []
    _labels = []
    for _s, _p, _depth in _configs:
        _P = random_psd_sum(_dim, _s, _rng)
        _Q = np.zeros((_dim, _dim))
        for _ in range(_p):
            _Q += _depth * random_signature_block(_dim, 1, 1, _rng)
        _true_online.append(_s)
        _certified.append(positive_index(_P + _Q) - _p)
        _labels.append(f"s={_s}, p={_p}")

    _fig = go.Figure()
    _fig.add_trace(go.Bar(x=_labels, y=_true_online, marker={"color": COLORS["tertiary"]}, name="true on-line count s"))
    _fig.add_trace(
        go.Scatter(
            x=_labels,
            y=_certified,
            mode="markers",
            marker={"color": COLORS["secondary"], "size": 13, "symbol": "diamond"},
            name="certified count  n₊ − p",
        )
    )

    _fig.update_layout(**base_layout(title="The certificate never exceeds the truth", height=420))
    _fig.update_xaxes(title_text="configuration (more / deeper off-line pairs →)")
    _fig.update_yaxes(title_text="on-line count", range=[-2, 33])
    style_subplot_axes(_fig, show_ticklabels=True)
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Across configurations that trade on-line points for off-line pairs, the certified count
        (diamonds, $n_+ - p$) sits on or below the true on-line count $s$ (bars). Pairing or
        multiplicity always lowers the certificate; in no configuration does it exceed the truth.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 8. How far this road can go

        Is $2/3$ the best the method gives? Everything the certificate does reduces to one
        scale-free functional of a window $v \ge 0$ and the bandwidth $\lambda$:

        $$
        c_\lambda(v) = \frac{\lambda\,(\int v)^2}{\int v^2 + \lambda^2 \iint |s - s'|\,v(s)\,v(s')\,ds\,ds'},
        \qquad H = 2 - \frac{1}{c_\lambda(v)}.
        $$

        The flat window gives $c_1 = 3/4$, hence $H = 2/3$. Maximising over $v$ at $\lambda = 1$
        gives the Montgomery-Taylor window $v^*(s) = \cos(\sqrt2\, s)$ with
        $c_1^* = 0.7533$, hence $H = 0.6725$: a genuine **maximum**, not a lower bound. Two
        moments alone cannot beat the flat window (the sharp Chebyshev-Markov cap is exactly
        $F(1) = 3/4$). So there are only two ways past $0.6725$, and both leave the finite
        certificate.
        """
    )
    return


@app.cell
def _(COLORS, H_opt, SQRT2, base_layout, c_star, go, math, np, style_subplot_axes):
    _pole = math.pi / SQRT2
    _lam_known = np.linspace(0.55, 1.0, 200)
    _lam_cond = np.linspace(1.0, _pole - 1e-3, 320)

    _fig = go.Figure()
    _fig.add_hline(y=0.90, line={"color": COLORS["muted"], "width": 1.5, "dash": "dot"})
    _fig.add_annotation(
        x=0.72,
        y=0.915,
        text="0.90 (above the single-window ceiling)",
        showarrow=False,
        font={"color": COLORS["muted"], "size": 11},
    )
    _fig.add_trace(
        go.Scatter(
            x=_lam_known,
            y=H_opt(_lam_known),
            mode="lines",
            line={"color": COLORS["primary"], "width": 4},
            name="λ ≤ 1  (unconditional)",
        )
    )
    _fig.add_trace(
        go.Scatter(
            x=_lam_cond,
            y=H_opt(_lam_cond),
            mode="lines",
            line={"color": COLORS["secondary"], "width": 3, "dash": "dash"},
            name="λ > 1  (Montgomery's conjecture)",
        )
    )
    _fig.add_trace(
        go.Scatter(
            x=[1.0],
            y=[H_opt(1.0)],
            mode="markers+text",
            marker={"color": COLORS["quaternary"], "size": 11},
            text=["0.6725"],
            textposition="bottom right",
            textfont={"color": COLORS["quaternary"]},
            showlegend=False,
        )
    )
    _fig.add_trace(
        go.Scatter(
            x=[1.043, 1.265],
            y=[0.70, 0.80],
            mode="markers+text",
            marker={"color": COLORS["accent1"], "size": 9, "symbol": "square"},
            text=["0.70", "0.80"],
            textposition="top left",
            textfont={"color": COLORS["accent1"], "size": 11},
            showlegend=False,
        )
    )

    _fig.update_layout(**base_layout(title="Proportion versus bandwidth: the ceiling of the method", height=460))
    _fig.update_xaxes(title_text="bandwidth λ", range=[0.5, _pole])
    _fig.update_yaxes(title_text="certified proportion", range=[0.35, 0.98])
    style_subplot_axes(_fig, show_ticklabels=True)
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The optimal window certifies $0.6725$ at the largest proven bandwidth $\lambda = 1$ (solid,
        unconditional). The dashed continuation reaches $0.70$ and $0.80$ only past $\lambda = 1$,
        inside Montgomery's open pair-correlation range, and $0.90$ sits above the single-window
        ceiling near $0.889$.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The two levers, in one picture below:

        1. **Add a higher moment.** A fourth-moment certificate would lift the simple-zero count to
           $13/18 = 0.722$, but each moment past the second is a Hardy-Littlewood prime-correlation
           conjecture, outside the unconditional range.
        2. **Extend the bandwidth past $\lambda = 1$.** This reaches $0.70$ at $\lambda \approx 1.04$
           and $0.80$ at $\lambda \approx 1.27$, but that is exactly Montgomery's open
           pair-correlation conjecture, and the single-window curve tops out near $0.889$, so even
           granting it, $0.90$ is out of reach for this family.

        Both prongs land outside the finite certificate.
        """
    )
    return


@app.cell
def _(COLORS, base_layout, go, style_subplot_axes):
    _rungs = [
        ("5/12\nPRZZ 2020", 5 / 12, "uncond"),
        ("2/3\nThm A, B", 2 / 3, "uncond"),
        ("0.6725\nThm D", 0.6725, "ceiling"),
        ("13/18\n+ 4th moment", 13 / 18, "cond"),
        ("1\n+ all moments", 1.0, "cond"),
    ]
    _colmap = {"uncond": COLORS["tertiary"], "ceiling": COLORS["secondary"], "cond": COLORS["accent2"]}
    _names = [r[0] for r in _rungs]
    _vals = [r[1] for r in _rungs]
    _cols = [_colmap[r[2]] for r in _rungs]
    _patterns = ["", "", "", "/", "/"]

    _fig = go.Figure()
    _fig.add_trace(
        go.Bar(
            x=_names,
            y=_vals,
            marker={"color": _cols, "pattern": {"shape": _patterns}},
            text=[f"{v:.3f}" for v in _vals],
            textposition="outside",
            showlegend=False,
        )
    )
    _fig.add_vrect(x0=-0.5, x1=2.5, fillcolor="rgba(78,205,196,0.08)", line={"width": 0})
    _fig.add_annotation(
        x=1,
        y=1.08,
        text="unconditional (bandwidth ≤ 1)",
        showarrow=False,
        font={"color": COLORS["tertiary"], "size": 11},
    )
    _fig.add_annotation(
        x=3.5, y=1.08, text="conditional", showarrow=False, font={"color": COLORS["accent2"], "size": 11}
    )

    _fig.update_layout(**base_layout(title="What each lever buys", height=440))
    _fig.update_yaxes(title_text="certified proportion", range=[0, 1.16])
    style_subplot_axes(_fig, show_ticklabels=True)
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The first three rungs use only the mean density and the second moment at bandwidth
        $\le 1$, and are unconditional; $0.6725$ is the ceiling of that data. The hatched $13/18$
        and $1$ rungs need higher correlations (Hardy-Littlewood) and are conditional. Even at
        proportion $1$ the claim is simple zeros on the line, not the hypothesis.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 9. How it was found, and what it is not

        **Authorship.** The paper's author is a large language model developed by Anthropic. An
        Anthropic staff member posed the problem (attempt the Riemann hypothesis, inside Claude
        Code) and left the mathematics to the model. A first pass produced and discarded roughly
        650 ideas; on the second, the model spent about 36 hours coordinating around 60 subagents,
        which ran some 2,400 shell commands and wrote hundreds of Python scripts, cross-checking
        numerical claims against known zeros and reviewing each other's reasoning. The cross-domain
        step was recognising that the unconditional pair-correlation prime side (BGSTB) could be
        married to Bombieri's Weil-form signature count, a combination no one had tried. Ralph
        Furman and Levent Alpoge take responsibility for its communication; Brian Conrey and Dan
        Goldston examined it on short notice.

        **Verification.** A Lean 4 formalisation (`Zeta23`) accompanies the paper: the theorem
        statements are expressed against Mathlib's `riemannZeta`, and at the cited commit the
        theorem types carry no extra hypotheses and depend only on Lean's three standard axioms.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        **What it is not.** The paper states this plainly:

        - It has **no bearing on the Riemann hypothesis** in either direction. It produces lower
          bounds only: at least two thirds of the zeros are on the line, and nothing about the
          remaining third, which are not shown to be off the line, merely not reached by the
          certificate.
        - It is **not $67.25\%$ of the way to a proof.** A guaranteed proportion is not a completion
          meter. If it survives scrutiny the guarantee rises by about 25 points in one step, a
          genuine advance, and the distance to a proof is unchanged.
        - The techniques are **not expected to lead to a proof.** The inputs (functional equation,
          explicit formula, mean values of Dirichlet polynomials of length $\le T$) are insensitive
          to $o(N)$ off-line zeros, and are satisfied by objects (Davenport-Heilbronn functions)
          for which the analogue of the hypothesis is *false*. An argument built only from these
          inputs cannot tell those apart from zeta.

        The result is a large, clean step on the proportion ladder of Part 4, obtained by making an
        old conditional argument unconditional. It is not the summit, and Part 8 is the honest map
        of how far this road can go.

        ---

        **Sources**

        - Claude (Anthropic), *More than two thirds of the zeros of the Riemann zeta function lie
          on the critical line* (10 August 2026).
        - H. Montgomery, *The pair correlation of zeros of the zeta function*, Proc. Sympos. Pure
          Math. 24 (1973); Montgomery-Taylor (1975); Cheer-Goldston (1993).
        - S. Baluyot, D. Goldston, A. I. Suriajaya, C. Turnage-Butterbaugh (2024); Goldston-Suriajaya
          (2025-2026), the unconditional prime side.
        - E. Bombieri, *Remarks on Weil's quadratic functional* (2000); A. Weil (1952); H. Yoshida
          (1992).
        - N. Levinson (1974); J. B. Conrey (1989); Pratt-Robles-Zaharescu-Zeindler (2020), the
          $5/12$ record; A. Selberg (1942); G. H. Hardy (1914).
        """
    )
    return


if __name__ == "__main__":
    app.run()
