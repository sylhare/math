"""
Trigonometry: The Mathematics of Circles and Waves

An exploration of trigonometric functions from ancient astronomy to modern
applications, covering the unit circle, identities, equations, and calculus
connections with interactive visualizations.
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
    return go, make_subplots, np


@app.cell
def _(mo):
    mo.md(
        r"""
        # Trigonometry: The Mathematics of Circles and Waves

        *"The study of trigonometry... will enable us to understand how waves and oscillations
        pervade all of nature."*
        — Joseph Fourier (1822)

        ---

        ## The Ancient Art of Measuring Triangles

        The word **trigonometry** comes from the Greek *trigonon* (triangle) and *metron* (measure).
        But don't let the name fool you—trigonometry is far more than measuring triangles.
        It's the mathematics of **circles**, **waves**, and **periodic phenomena**.

        From the rhythmic pulsing of your heart to the orbits of distant planets, from sound waves
        to electrical signals, trigonometry provides the language to describe anything that repeats.

        **What you'll learn:**
        - How ancient astronomers invented trigonometry to map the heavens
        - The unit circle: the foundation of all trigonometric functions
        - Key identities that simplify complex expressions
        - How to solve trigonometric equations
        - The connection to calculus: derivatives of sine and cosine
        - Applications in physics: simple harmonic motion
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Part I: A Journey Through History

        ### The Babylonians (2000-500 BCE): Watching the Sky

        Long before the Greeks, Babylonian astronomers tracked the movements of celestial bodies
        with remarkable precision. They divided the circle into **360 degrees**—a choice we still
        use today, likely because 360 is close to the number of days in a year and has many divisors.

        They created tables relating the length of a shadow to the time of day—an early application
        of trigonometric thinking, though they lacked formal trigonometric functions.

        ### Hipparchus of Nicaea (190-120 BCE): Father of Trigonometry

        The Greek astronomer **Hipparchus** is often called the "father of trigonometry."
        Working in Rhodes, he created the first **chord tables**—precursors to modern sine tables.

        Given a circle of radius $R$, the *chord* of an angle $\theta$ is the straight-line distance
        between two points on the circle separated by that angle. Hipparchus computed these lengths
        for angles from 0° to 180° in steps of 7.5°.

        His motivation? **Astronomy.** To predict eclipses and planetary positions, you need to
        solve spherical triangles—and that requires trigonometry.

        > **Key insight**: Trigonometry was born not from abstract mathematics, but from the
        > practical need to understand the heavens.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Ptolemy's Almagest (150 CE)

        The astronomer **Claudius Ptolemy** wrote the *Almagest*, the most influential astronomy
        text of antiquity. It contained an extensive chord table and the theorem that bears his name.

        Ptolemy's chord function relates to our modern sine:

        $$\text{chord}(\theta) = 2R \sin\left(\frac{\theta}{2}\right)$$

        For a unit circle ($R = 1$), the chord of $\theta$ equals $2\sin(\theta/2)$.

        ### Indian Mathematicians (500-1200 CE): The Birth of Sine

        The transformation from chords to *sines* happened in India. Mathematicians like
        **Aryabhata** (476-550 CE) and **Brahmagupta** (598-668 CE) introduced the **half-chord**
        (*ardha-jya* or *jya* for short), which corresponds to our modern sine function.

        The word "sine" itself is a linguistic accident: when Arabic scholars translated Indian
        texts, they transliterated *jya* as *jiba*. Later Latin translators, unfamiliar with the
        Arabic term, confused it with *jaib* (meaning "bay" or "fold"), which they translated
        as *sinus*—Latin for "bay" or "curve."

        So "sine" ultimately derives from a mistranslation of a Sanskrit word!

        ### Islamic Golden Age (800-1400 CE)

        Islamic mathematicians refined trigonometry further:
        - **Al-Khwarizmi** (780-850 CE) wrote tables of sines and tangents
        - **Al-Battani** (858-929 CE) introduced the cotangent function
        - **Nasir al-Din al-Tusi** (1201-1274 CE) wrote the first treatise treating trigonometry
          as a discipline separate from astronomy
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### European Renaissance and Modern Notation

        **Regiomontanus** (1436-1476) wrote *De triangulis omnimodis*, the first systematic
        European textbook on trigonometry.

        But our modern notation came from **Leonhard Euler** (1707-1783), the most prolific
        mathematician in history. Euler:
        - Standardized $\sin$, $\cos$, $\tan$ as function names
        - Introduced radian measure
        - Discovered the profound identity $e^{i\theta} = \cos\theta + i\sin\theta$

        This last formula, known as **Euler's formula**, reveals that exponentials, trigonometry,
        and complex numbers are all deeply connected—perhaps the most beautiful equation in
        mathematics.

        ### Timeline Summary

        | Period | Contributors | Key Development |
        |--------|--------------|-----------------|
        | 2000 BCE | Babylonians | 360-degree circle, shadow tables |
        | 190-120 BCE | Hipparchus | First chord tables |
        | 150 CE | Ptolemy | Comprehensive chord tables in *Almagest* |
        | 500 CE | Aryabhata | Half-chord (sine) concept |
        | 800-1200 CE | Al-Khwarizmi, Al-Battani | Tangent, cotangent; refined tables |
        | 1464 | Regiomontanus | First European trig textbook |
        | 1748 | Euler | Modern notation, radian measure |
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Part II: The Unit Circle

        ### The Foundation of Everything

        The **unit circle** is a circle of radius 1 centered at the origin. It's the foundation
        of all trigonometry because it provides a geometric definition of sine and cosine that
        works for *any* angle—not just acute angles in triangles.

        For any angle $\theta$, draw a ray from the origin at that angle. Where it intersects
        the unit circle, the point has coordinates $(\cos\theta, \sin\theta)$.

        $$\boxed{(\cos\theta, \sin\theta) = \text{coordinates of point on unit circle at angle } \theta}$$

        This definition immediately gives us:
        - $\cos\theta$ = horizontal coordinate (x-value)
        - $\sin\theta$ = vertical coordinate (y-value)

        Since the point lies on a circle of radius 1, we always have:
        $$\cos^2\theta + \sin^2\theta = 1$$

        This is the **Pythagorean identity**—the most fundamental identity in trigonometry.
        """
    )
    return


@app.cell
def _(mo):
    unit_circle_angle = mo.ui.slider(
        start=0, stop=360, step=5, value=45,
        label="Angle (degrees)",
        show_value=True,
    )
    return (unit_circle_angle,)


@app.cell
def _(mo, unit_circle_angle):
    mo.hstack([
        mo.md("### Interactive Unit Circle"),
        unit_circle_angle,
    ])
    return


@app.cell
def _(go, np, unit_circle_angle):
    _theta_deg = unit_circle_angle.value
    _theta_rad = np.radians(_theta_deg)
    _cos_val = np.cos(_theta_rad)
    _sin_val = np.sin(_theta_rad)

    # Create unit circle
    _circle_theta = np.linspace(0, 2 * np.pi, 100)
    _circle_x = np.cos(_circle_theta)
    _circle_y = np.sin(_circle_theta)

    _fig = go.Figure()

    # Unit circle
    _fig.add_trace(go.Scatter(
        x=_circle_x, y=_circle_y,
        mode='lines',
        line={'color': '#4ecdc4', 'width': 2},
        name='Unit circle',
        hoverinfo='skip'
    ))

    # Angle arc
    _arc_theta = np.linspace(0, _theta_rad, 50)
    _arc_r = 0.2
    _fig.add_trace(go.Scatter(
        x=_arc_r * np.cos(_arc_theta),
        y=_arc_r * np.sin(_arc_theta),
        mode='lines',
        line={'color': '#ffe66d', 'width': 2},
        name=f'θ = {_theta_deg}°',
        hoverinfo='skip'
    ))

    # Radius to point
    _fig.add_trace(go.Scatter(
        x=[0, _cos_val], y=[0, _sin_val],
        mode='lines',
        line={'color': '#00d4ff', 'width': 3},
        name='Radius',
        hoverinfo='skip'
    ))

    # Point on circle
    _fig.add_trace(go.Scatter(
        x=[_cos_val], y=[_sin_val],
        mode='markers+text',
        marker={'color': '#ff6b6b', 'size': 14},
        text=[f'({_cos_val:.3f}, {_sin_val:.3f})'],
        textposition='top right',
        textfont={'color': '#ff6b6b', 'size': 12},
        name='Point (cos θ, sin θ)',
    ))

    # Projections
    # Vertical line (cos θ)
    _fig.add_trace(go.Scatter(
        x=[_cos_val, _cos_val], y=[0, _sin_val],
        mode='lines',
        line={'color': '#ff6b6b', 'width': 2, 'dash': 'dash'},
        name=f'sin θ = {_sin_val:.3f}',
    ))

    # Horizontal line (sin θ)
    _fig.add_trace(go.Scatter(
        x=[0, _cos_val], y=[_sin_val, _sin_val],
        mode='lines',
        line={'color': '#95e1d3', 'width': 2, 'dash': 'dash'},
        name=f'cos θ = {_cos_val:.3f}',
    ))

    # Axes
    _fig.add_hline(y=0, line_color='#a0a0a0', line_width=1)
    _fig.add_vline(x=0, line_color='#a0a0a0', line_width=1)

    _fig.update_layout(
        minreducedwidth=300,
        paper_bgcolor='#1a1a2e',
        plot_bgcolor='#16213e',
        font={'color': '#eaeaea', 'family': 'JetBrains Mono, monospace'},
        title=f'θ = {_theta_deg}° = {_theta_rad:.3f} rad | cos θ = {_cos_val:.3f} | sin θ = {_sin_val:.3f}',
        xaxis={
            'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0',
            'title': 'x = cos θ', 'range': [-1.5, 1.5],
            'scaleanchor': 'y', 'scaleratio': 1
        },
        yaxis={
            'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0',
            'title': 'y = sin θ', 'range': [-1.5, 1.5]
        },
        showlegend=True,
        legend={'bgcolor': 'rgba(22, 33, 62, 0.8)', 'font': {'size': 10}},
        height=500,
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The unit circle visualization shows how sine and cosine are defined geometrically.
        As you drag the slider, the point moves around the circle, and its coordinates
        trace out the values of cosine (x-coordinate) and sine (y-coordinate).

        **Key observations:**
        - At 0°: $(\cos 0°, \sin 0°) = (1, 0)$
        - At 90°: $(\cos 90°, \sin 90°) = (0, 1)$
        - At 180°: $(\cos 180°, \sin 180°) = (-1, 0)$
        - At 270°: $(\cos 270°, \sin 270°) = (0, -1)$
        - At 360°: We're back at $(1, 0)$—the functions are periodic!
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Radians vs Degrees

        There are two common ways to measure angles:

        **Degrees**: A full circle is 360°. This is convenient for everyday use (right angles
        are 90°, straight angles are 180°), but the number 360 is arbitrary.

        **Radians**: A full circle is $2\pi$ radians. One radian is the angle where the arc
        length equals the radius. This is the "natural" unit for angles in mathematics and
        physics because it simplifies many formulas.

        **Conversion formulas:**

        $$\theta_{\text{rad}} = \theta_{\text{deg}} \times \frac{\pi}{180}$$

        $$\theta_{\text{deg}} = \theta_{\text{rad}} \times \frac{180}{\pi}$$

        | Degrees | Radians | Decimal |
        |---------|---------|---------|
        | 0° | 0 | 0.000 |
        | 30° | $\pi/6$ | 0.524 |
        | 45° | $\pi/4$ | 0.785 |
        | 60° | $\pi/3$ | 1.047 |
        | 90° | $\pi/2$ | 1.571 |
        | 180° | $\pi$ | 3.142 |
        | 270° | $3\pi/2$ | 4.712 |
        | 360° | $2\pi$ | 6.283 |

        **Why radians?** In calculus, the derivative formulas $\frac{d}{dx}\sin x = \cos x$ and
        $\frac{d}{dx}\cos x = -\sin x$ only work when $x$ is in radians. If $x$ is in degrees,
        you get extra factors of $\pi/180$.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Special Angles and Their Values

        Certain angles appear so frequently that their sine and cosine values are worth memorizing.
        These come from simple geometric constructions:

        | Angle | Degrees | sin θ | cos θ | tan θ |
        |-------|---------|-------|-------|-------|
        | 0 | 0° | 0 | 1 | 0 |
        | $\pi/6$ | 30° | $\frac{1}{2}$ | $\frac{\sqrt{3}}{2}$ | $\frac{1}{\sqrt{3}}$ |
        | $\pi/4$ | 45° | $\frac{\sqrt{2}}{2}$ | $\frac{\sqrt{2}}{2}$ | 1 |
        | $\pi/3$ | 60° | $\frac{\sqrt{3}}{2}$ | $\frac{1}{2}$ | $\sqrt{3}$ |
        | $\pi/2$ | 90° | 1 | 0 | undefined |

        **Memory trick**: Notice that sine increases from 0 to 1 as the angle goes from 0° to 90°,
        while cosine decreases from 1 to 0. They're "mirror images" in a sense—in fact,
        $\cos\theta = \sin(90° - \theta)$.

        **Where do these values come from?**
        - 45°: An isoceles right triangle has legs of equal length. If the hypotenuse is 1,
          each leg is $1/\sqrt{2} = \sqrt{2}/2$.
        - 30° and 60°: Cut an equilateral triangle in half. The half-triangle has angles 30-60-90
          and sides in ratio $1 : \sqrt{3} : 2$.
        """
    )
    return


@app.cell
def _(go, np):
    # Special angles visualization on unit circle
    _special_angles = [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330]

    _circle_theta = np.linspace(0, 2 * np.pi, 100)
    _circle_x = np.cos(_circle_theta)
    _circle_y = np.sin(_circle_theta)

    _fig = go.Figure()

    # Unit circle
    _fig.add_trace(go.Scatter(
        x=_circle_x, y=_circle_y,
        mode='lines',
        line={'color': '#4ecdc4', 'width': 2},
        name='Unit circle',
        hoverinfo='skip'
    ))

    # Special angles
    for _angle in _special_angles:
        _rad = np.radians(_angle)
        _x = np.cos(_rad)
        _y = np.sin(_rad)

        # Point
        _fig.add_trace(go.Scatter(
            x=[_x], y=[_y],
            mode='markers',
            marker={'color': '#ff6b6b', 'size': 10},
            name=f'{_angle}°',
            showlegend=False,
            hovertemplate=f'{_angle}°<br>cos = {_x:.3f}<br>sin = {_y:.3f}<extra></extra>'
        ))

        # Label
        _label_r = 1.15
        _fig.add_annotation(
            x=_label_r * _x, y=_label_r * _y,
            text=f'{_angle}°',
            font={'color': '#ffe66d', 'size': 10},
            showarrow=False,
        )

    # Axes
    _fig.add_hline(y=0, line_color='#a0a0a0', line_width=1)
    _fig.add_vline(x=0, line_color='#a0a0a0', line_width=1)

    _fig.update_layout(
        minreducedwidth=300,
        paper_bgcolor='#1a1a2e',
        plot_bgcolor='#16213e',
        font={'color': '#eaeaea', 'family': 'JetBrains Mono, monospace'},
        title='Special Angles on the Unit Circle',
        xaxis={
            'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0',
            'range': [-1.4, 1.4], 'scaleanchor': 'y'
        },
        yaxis={
            'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0',
            'range': [-1.4, 1.4]
        },
        showlegend=False,
        height=500,
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        This diagram shows all the commonly used special angles on the unit circle.
        Hover over any point to see its exact coordinates—these are the cosine and sine
        values for that angle. Notice the symmetries:

        - **Quadrant I** (0° to 90°): Both sin and cos are positive
        - **Quadrant II** (90° to 180°): Sin positive, cos negative
        - **Quadrant III** (180° to 270°): Both negative
        - **Quadrant IV** (270° to 360°): Sin negative, cos positive

        The mnemonic "All Students Take Calculus" helps remember which functions are positive
        in each quadrant (All, Sine, Tangent, Cosine).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Part III: The Trigonometric Functions

        ### Definitions

        The six trigonometric functions are defined as follows. For a point $(x, y)$ on
        the unit circle at angle $\theta$:

        **Primary functions:**

        $$\begin{aligned}
        \sin\theta &= y \\
        \cos\theta &= x \\
        \tan\theta &= \frac{y}{x} = \frac{\sin\theta}{\cos\theta}
        \end{aligned}$$

        **Reciprocal functions:**

        $$\begin{aligned}
        \csc\theta &= \frac{1}{\sin\theta} \\
        \sec\theta &= \frac{1}{\cos\theta} \\
        \cot\theta &= \frac{1}{\tan\theta} = \frac{\cos\theta}{\sin\theta}
        \end{aligned}$$

        ### Right Triangle Interpretation

        For acute angles (0° < θ < 90°), these definitions agree with the familiar
        "SOH-CAH-TOA" ratios in a right triangle:

        $$\sin\theta = \frac{\text{opposite}}{\text{hypotenuse}} \quad\quad
        \cos\theta = \frac{\text{adjacent}}{\text{hypotenuse}} \quad\quad
        \tan\theta = \frac{\text{opposite}}{\text{adjacent}}$$

        But the unit circle definition is more general—it works for any angle, including
        negative angles and angles greater than 360°.
        """
    )
    return


@app.cell
def _(mo):
    trig_function_dropdown = mo.ui.dropdown(
        options={
            "sin(x)": "sin",
            "cos(x)": "cos",
            "tan(x)": "tan",
            "csc(x)": "csc",
            "sec(x)": "sec",
            "cot(x)": "cot",
        },
        value="sin(x)",
        label="Choose a function:",
    )
    return (trig_function_dropdown,)


@app.cell
def _(mo, trig_function_dropdown):
    mo.hstack([
        mo.md("### Trigonometric Function Explorer"),
        trig_function_dropdown,
    ])
    return


@app.cell
def _(go, np, trig_function_dropdown):
    _func_name = trig_function_dropdown.value

    _x = np.linspace(-2 * np.pi, 2 * np.pi, 1000)

    _func_map = {
        "sin": (np.sin, "sin(x)", [-1.5, 1.5]),
        "cos": (np.cos, "cos(x)", [-1.5, 1.5]),
        "tan": (np.tan, "tan(x)", [-5, 5]),
        "csc": (lambda x: 1 / np.sin(x), "csc(x) = 1/sin(x)", [-5, 5]),
        "sec": (lambda x: 1 / np.cos(x), "sec(x) = 1/cos(x)", [-5, 5]),
        "cot": (lambda x: 1 / np.tan(x), "cot(x) = cos(x)/sin(x)", [-5, 5]),
    }

    _func, _label, _y_range = _func_map[_func_name]

    with np.errstate(divide='ignore', invalid='ignore'):
        _y = _func(_x)
        _y = np.where(np.abs(_y) > 10, np.nan, _y)

    _fig = go.Figure()

    _fig.add_trace(go.Scatter(
        x=_x, y=_y,
        mode='lines',
        line={'color': '#00d4ff', 'width': 3},
        name=_label,
    ))

    # Mark key points for sin and cos
    if _func_name in ["sin", "cos"]:
        _key_x = np.array([-2*np.pi, -3*np.pi/2, -np.pi, -np.pi/2, 0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
        _key_y = _func(_key_x)
        _fig.add_trace(go.Scatter(
            x=_key_x, y=_key_y,
            mode='markers',
            marker={'color': '#ff6b6b', 'size': 8},
            name='Key points',
        ))

    _fig.add_hline(y=0, line_color='#a0a0a0', line_width=1)
    _fig.add_vline(x=0, line_color='#a0a0a0', line_width=1)

    # Add vertical asymptotes for tan, cot, sec, csc
    if _func_name in ["tan", "sec"]:
        for _k in range(-2, 3):
            _asymp = np.pi/2 + _k * np.pi
            if -2*np.pi <= _asymp <= 2*np.pi:
                _fig.add_vline(x=_asymp, line_color='#ff6b6b', line_width=1, line_dash='dash')
    elif _func_name in ["cot", "csc"]:
        for _k in range(-2, 3):
            _asymp = _k * np.pi
            if -2*np.pi <= _asymp <= 2*np.pi:
                _fig.add_vline(x=_asymp, line_color='#ff6b6b', line_width=1, line_dash='dash')

    _fig.update_layout(
        minreducedwidth=300,
        paper_bgcolor='#1a1a2e',
        plot_bgcolor='#16213e',
        font={'color': '#eaeaea', 'family': 'JetBrains Mono, monospace'},
        title=f'Graph of {_label}',
        xaxis={
            'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'zerolinewidth': 2,
            'title': 'x (radians)',
            'tickvals': [-2*np.pi, -3*np.pi/2, -np.pi, -np.pi/2, 0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi],
            'ticktext': ['-2π', '-3π/2', '-π', '-π/2', '0', 'π/2', 'π', '3π/2', '2π'],
        },
        yaxis={
            'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'zerolinewidth': 2,
            'title': f'{_label}', 'range': _y_range
        },
        showlegend=True,
        legend={'bgcolor': 'rgba(22, 33, 62, 0.8)', 'orientation': 'h', 'yanchor': 'bottom', 'y': -0.2, 'xanchor': 'center', 'x': 0.5},
        margin={'l': 40, 'r': 40, 't': 50, 'b': 100},
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        **Properties of trigonometric functions:**

        | Function | Domain | Range | Period |
        |----------|--------|-------|--------|
        | $\sin x$ | All real numbers | $[-1, 1]$ | $2\pi$ |
        | $\cos x$ | All real numbers | $[-1, 1]$ | $2\pi$ |
        | $\tan x$ | $x \neq \frac{\pi}{2} + n\pi$ | All real numbers | $\pi$ |
        | $\csc x$ | $x \neq n\pi$ | $(-\infty, -1] \cup [1, \infty)$ | $2\pi$ |
        | $\sec x$ | $x \neq \frac{\pi}{2} + n\pi$ | $(-\infty, -1] \cup [1, \infty)$ | $2\pi$ |
        | $\cot x$ | $x \neq n\pi$ | All real numbers | $\pi$ |

        **Even and odd functions:**
        - $\cos(-x) = \cos(x)$ — cosine is **even** (symmetric about y-axis)
        - $\sin(-x) = -\sin(x)$ — sine is **odd** (symmetric about origin)
        - $\tan(-x) = -\tan(x)$ — tangent is **odd**
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Transformations: Amplitude, Period, and Phase

        The general sinusoidal function has the form:

        $$y = A \sin(Bx + C) + D$$

        Each parameter controls a different aspect:

        - **A** (Amplitude): Vertical stretch/compression. Height of waves is $|A|$.
        - **B** (Frequency): Horizontal stretch/compression. Period = $\frac{2\pi}{|B|}$.
        - **C** (Phase shift): Horizontal shift. Shift = $-\frac{C}{B}$.
        - **D** (Vertical shift): Shifts the midline up/down.

        Use the sliders below to explore how each parameter affects the wave.
        """
    )
    return


@app.cell
def _(mo):
    amp_slider = mo.ui.slider(start=0.5, stop=3, step=0.1, value=1, label="A (amplitude)", show_value=True)
    freq_slider = mo.ui.slider(start=0.5, stop=4, step=0.1, value=1, label="B (frequency)", show_value=True)
    phase_slider = mo.ui.slider(start=-np.pi, stop=np.pi, step=0.1, value=0, label="C (phase)", show_value=True)
    shift_slider = mo.ui.slider(start=-2, stop=2, step=0.1, value=0, label="D (vertical shift)", show_value=True)
    return amp_slider, freq_slider, phase_slider, shift_slider


@app.cell
def _(amp_slider, freq_slider, mo, phase_slider, shift_slider):
    mo.vstack([
        mo.md("### Wave Transformer: $y = A\\sin(Bx + C) + D$"),
        mo.hstack([amp_slider, freq_slider], justify="start", gap=2),
        mo.hstack([phase_slider, shift_slider], justify="start", gap=2),
    ])
    return


@app.cell
def _(amp_slider, freq_slider, go, np, phase_slider, shift_slider):
    _A = amp_slider.value
    _B = freq_slider.value
    _C = phase_slider.value
    _D = shift_slider.value

    _x = np.linspace(-2 * np.pi, 2 * np.pi, 500)
    _y_base = np.sin(_x)
    _y_transformed = _A * np.sin(_B * _x + _C) + _D

    _period = 2 * np.pi / abs(_B)
    _phase_shift = -_C / _B

    _fig = go.Figure()

    # Base sine wave
    _fig.add_trace(go.Scatter(
        x=_x, y=_y_base,
        mode='lines',
        line={'color': '#4ecdc4', 'width': 2, 'dash': 'dash'},
        name='sin(x) (reference)',
    ))

    # Transformed wave
    _fig.add_trace(go.Scatter(
        x=_x, y=_y_transformed,
        mode='lines',
        line={'color': '#00d4ff', 'width': 3},
        name=f'y = {_A:.1f}·sin({_B:.1f}x + {_C:.1f}) + {_D:.1f}',
    ))

    # Midline
    _fig.add_trace(go.Scatter(
        x=[-2*np.pi, 2*np.pi], y=[_D, _D],
        mode='lines',
        line={'color': '#ffe66d', 'width': 1, 'dash': 'dot'},
        name=f'Midline y = {_D:.1f}',
    ))

    _fig.update_layout(
        minreducedwidth=300,
        paper_bgcolor='#1a1a2e',
        plot_bgcolor='#16213e',
        font={'color': '#eaeaea', 'family': 'JetBrains Mono, monospace'},
        title=f'Period = {_period:.2f} | Phase shift = {_phase_shift:.2f}',
        xaxis={
            'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0',
            'title': 'x',
            'tickvals': [-2*np.pi, -np.pi, 0, np.pi, 2*np.pi],
            'ticktext': ['-2π', '-π', '0', 'π', '2π'],
        },
        yaxis={
            'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0',
            'title': 'y', 'range': [-5, 5]
        },
        showlegend=True,
        legend={'bgcolor': 'rgba(22, 33, 62, 0.8)', 'orientation': 'h', 'yanchor': 'bottom', 'y': -0.2, 'xanchor': 'center', 'x': 0.5},
        margin={'l': 40, 'r': 40, 't': 50, 'b': 100},
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The dashed teal curve is the reference $\sin(x)$ while the solid blue curve shows
        your transformed function. Experiment with the parameters:

        - **Increase A** to make taller waves
        - **Increase B** to compress waves (more oscillations in the same space)
        - **Change C** to shift the wave left or right
        - **Change D** to move the whole wave up or down
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Part IV: Fundamental Identities

        ### The Pythagorean Identity

        The most fundamental trigonometric identity comes directly from the unit circle:

        $$\boxed{\sin^2\theta + \cos^2\theta = 1}$$

        **Proof**: Any point on the unit circle satisfies $x^2 + y^2 = 1$. Since
        $x = \cos\theta$ and $y = \sin\theta$, we get $\cos^2\theta + \sin^2\theta = 1$.

        From this, we can derive two related identities by dividing:

        Divide by $\cos^2\theta$: $\quad \tan^2\theta + 1 = \sec^2\theta$

        Divide by $\sin^2\theta$: $\quad 1 + \cot^2\theta = \csc^2\theta$
        """
    )
    return


@app.cell
def _(mo):
    pythag_angle = mo.ui.slider(
        start=0, stop=360, step=5, value=30,
        label="Angle θ (degrees)",
        show_value=True,
    )
    return (pythag_angle,)


@app.cell
def _(mo, pythag_angle):
    mo.hstack([
        mo.md("### Pythagorean Identity Visualization"),
        pythag_angle,
    ])
    return


@app.cell
def _(go, np, pythag_angle):
    _theta_deg = pythag_angle.value
    _theta_rad = np.radians(_theta_deg)
    _cos_val = np.cos(_theta_rad)
    _sin_val = np.sin(_theta_rad)

    _fig = go.Figure()

    # Unit circle
    _circle_theta = np.linspace(0, 2 * np.pi, 100)
    _fig.add_trace(go.Scatter(
        x=np.cos(_circle_theta), y=np.sin(_circle_theta),
        mode='lines',
        line={'color': '#4ecdc4', 'width': 2},
        name='Unit circle',
        hoverinfo='skip'
    ))

    # Right triangle
    _fig.add_trace(go.Scatter(
        x=[0, _cos_val, _cos_val, 0],
        y=[0, 0, _sin_val, 0],
        mode='lines',
        fill='toself',
        fillcolor='rgba(0, 212, 255, 0.2)',
        line={'color': '#00d4ff', 'width': 2},
        name='Right triangle',
    ))

    # Labels for sides
    _fig.add_annotation(x=_cos_val/2, y=-0.1, text=f'cos θ = {_cos_val:.3f}',
                        font={'color': '#95e1d3', 'size': 12}, showarrow=False)
    _fig.add_annotation(x=_cos_val+0.1, y=_sin_val/2, text=f'sin θ = {_sin_val:.3f}',
                        font={'color': '#ff6b6b', 'size': 12}, showarrow=False)
    _fig.add_annotation(x=_cos_val/2-0.1, y=_sin_val/2+0.1, text='1',
                        font={'color': '#ffe66d', 'size': 14}, showarrow=False)

    # Point on circle
    _fig.add_trace(go.Scatter(
        x=[_cos_val], y=[_sin_val],
        mode='markers',
        marker={'color': '#ff6b6b', 'size': 12},
        showlegend=False,
    ))

    # Verification text
    _sum = _cos_val**2 + _sin_val**2
    _fig.add_annotation(
        x=0, y=-1.3,
        text=f'cos²θ + sin²θ = {_cos_val:.3f}² + {_sin_val:.3f}² = {_sum:.6f} ≈ 1',
        font={'color': '#ffe66d', 'size': 14},
        showarrow=False
    )

    _fig.update_layout(
        minreducedwidth=300,
        paper_bgcolor='#1a1a2e',
        plot_bgcolor='#16213e',
        font={'color': '#eaeaea', 'family': 'JetBrains Mono, monospace'},
        title=f'Pythagorean Identity: sin²θ + cos²θ = 1',
        xaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'range': [-1.5, 1.5], 'scaleanchor': 'y'},
        yaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'range': [-1.5, 1.5]},
        showlegend=False,
        height=500,
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The visualization shows how the Pythagorean identity is just the Pythagorean theorem
        applied to the right triangle formed by dropping a perpendicular from the point on
        the unit circle to the x-axis.

        The triangle has:
        - Hypotenuse = 1 (radius of unit circle)
        - Horizontal leg = $\cos\theta$
        - Vertical leg = $\sin\theta$

        By Pythagoras: $(\cos\theta)^2 + (\sin\theta)^2 = 1^2$
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Reciprocal and Quotient Identities

        **Reciprocal identities:**

        $$\begin{aligned}
        \csc\theta &= \frac{1}{\sin\theta} \\
        \sec\theta &= \frac{1}{\cos\theta} \\
        \cot\theta &= \frac{1}{\tan\theta}
        \end{aligned}$$

        **Quotient identities:**

        $$\tan\theta = \frac{\sin\theta}{\cos\theta} \quad\quad \cot\theta = \frac{\cos\theta}{\sin\theta}$$

        ### Even/Odd Identities

        $$\begin{aligned}
        \cos(-\theta) &= \cos\theta \\
        \sin(-\theta) &= -\sin\theta \\
        \tan(-\theta) &= -\tan\theta
        \end{aligned}$$

        These follow from the symmetry of the unit circle:
        - Reflecting a point $(x, y)$ across the x-axis gives $(x, -y)$
        - If the original point is at angle $\theta$, the reflection is at angle $-\theta$
        - The x-coordinate (cosine) stays the same; the y-coordinate (sine) changes sign

        ### Cofunction Identities

        $$\sin\left(\frac{\pi}{2} - \theta\right) = \cos\theta \quad\quad \cos\left(\frac{\pi}{2} - \theta\right) = \sin\theta$$

        These say that sine and cosine are "cofunctions"—each is the other evaluated at the
        complementary angle (angles that add to 90°).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Part V: Angle Addition and Double Angle Formulas

        ### Angle Addition Formulas

        These are perhaps the most important identities after the Pythagorean identity:

        $$\boxed{\sin(\alpha + \beta) = \sin\alpha\cos\beta + \cos\alpha\sin\beta}$$

        $$\boxed{\cos(\alpha + \beta) = \cos\alpha\cos\beta - \sin\alpha\sin\beta}$$

        **Subtraction versions** (replace $\beta$ with $-\beta$):

        $$\sin(\alpha - \beta) = \sin\alpha\cos\beta - \cos\alpha\sin\beta$$

        $$\cos(\alpha - \beta) = \cos\alpha\cos\beta + \sin\alpha\sin\beta$$

        **Tangent addition:**

        $$\tan(\alpha + \beta) = \frac{\tan\alpha + \tan\beta}{1 - \tan\alpha\tan\beta}$$
        """
    )
    return


@app.cell
def _(go, np):
    # Geometric proof of angle addition
    _alpha = np.pi / 6  # 30 degrees
    _beta = np.pi / 4   # 45 degrees

    _fig = go.Figure()

    # Unit circle
    _circle_theta = np.linspace(0, 2 * np.pi, 100)
    _fig.add_trace(go.Scatter(
        x=np.cos(_circle_theta), y=np.sin(_circle_theta),
        mode='lines',
        line={'color': '#4ecdc4', 'width': 2},
        hoverinfo='skip',
        showlegend=False,
    ))

    # Angle alpha
    _fig.add_trace(go.Scatter(
        x=[0, np.cos(_alpha)], y=[0, np.sin(_alpha)],
        mode='lines',
        line={'color': '#00d4ff', 'width': 3},
        name=f'α = 30°',
    ))

    # Angle alpha + beta
    _fig.add_trace(go.Scatter(
        x=[0, np.cos(_alpha + _beta)], y=[0, np.sin(_alpha + _beta)],
        mode='lines',
        line={'color': '#ff6b6b', 'width': 3},
        name=f'α + β = 75°',
    ))

    # Points
    _fig.add_trace(go.Scatter(
        x=[np.cos(_alpha)], y=[np.sin(_alpha)],
        mode='markers+text',
        marker={'color': '#00d4ff', 'size': 10},
        text=['P(cos α, sin α)'],
        textposition='top right',
        textfont={'size': 10, 'color': '#00d4ff'},
        showlegend=False,
    ))

    _fig.add_trace(go.Scatter(
        x=[np.cos(_alpha + _beta)], y=[np.sin(_alpha + _beta)],
        mode='markers+text',
        marker={'color': '#ff6b6b', 'size': 10},
        text=['Q(cos(α+β), sin(α+β))'],
        textposition='top right',
        textfont={'size': 10, 'color': '#ff6b6b'},
        showlegend=False,
    ))

    # Arcs for angles
    _arc_alpha = np.linspace(0, _alpha, 30)
    _fig.add_trace(go.Scatter(
        x=0.2*np.cos(_arc_alpha), y=0.2*np.sin(_arc_alpha),
        mode='lines',
        line={'color': '#00d4ff', 'width': 2},
        showlegend=False,
    ))

    _arc_beta = np.linspace(_alpha, _alpha + _beta, 30)
    _fig.add_trace(go.Scatter(
        x=0.3*np.cos(_arc_beta), y=0.3*np.sin(_arc_beta),
        mode='lines',
        line={'color': '#ffe66d', 'width': 2},
        name=f'β = 45°',
    ))

    # Verification
    _sin_sum = np.sin(_alpha + _beta)
    _sin_formula = np.sin(_alpha)*np.cos(_beta) + np.cos(_alpha)*np.sin(_beta)

    _fig.add_annotation(
        x=0, y=-1.3,
        text=f'sin(75°) = sin(30°)cos(45°) + cos(30°)sin(45°) = {_sin_sum:.4f}',
        font={'color': '#ffe66d', 'size': 12},
        showarrow=False,
    )

    _fig.update_layout(
        minreducedwidth=300,
        paper_bgcolor='#1a1a2e',
        plot_bgcolor='#16213e',
        font={'color': '#eaeaea', 'family': 'JetBrains Mono, monospace'},
        title='Angle Addition: sin(α + β) = sin α cos β + cos α sin β',
        xaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'range': [-1.5, 1.5], 'scaleanchor': 'y'},
        yaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'range': [-1.5, 1.5]},
        legend={'bgcolor': 'rgba(22, 33, 62, 0.8)', 'font': {'size': 10}},
        height=500,
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The diagram shows angles α = 30° and β = 45° on the unit circle. The angle addition
        formula lets us compute sin(75°) and cos(75°) exactly, even though 75° isn't a
        "special" angle.

        **Example calculation:**

        $$\sin(75°) = \sin(30° + 45°) = \sin 30° \cos 45° + \cos 30° \sin 45°$$

        $$= \frac{1}{2} \cdot \frac{\sqrt{2}}{2} + \frac{\sqrt{3}}{2} \cdot \frac{\sqrt{2}}{2} = \frac{\sqrt{2} + \sqrt{6}}{4} \approx 0.966$$
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Double Angle Formulas

        Setting $\alpha = \beta$ in the addition formulas gives the **double angle formulas**:

        $$\boxed{\sin(2\theta) = 2\sin\theta\cos\theta}$$

        $$\boxed{\begin{aligned}
        \cos(2\theta) &= \cos^2\theta - \sin^2\theta \\
        &= 2\cos^2\theta - 1 \\
        &= 1 - 2\sin^2\theta
        \end{aligned}}$$

        $$\tan(2\theta) = \frac{2\tan\theta}{1 - \tan^2\theta}$$

        The three forms of the cosine double angle formula are all useful in different contexts.

        ### Half Angle Formulas

        Solving the double angle formulas for $\sin\theta$ and $\cos\theta$ (using $\theta = \phi/2$):

        $$\sin\left(\frac{\theta}{2}\right) = \pm\sqrt{\frac{1 - \cos\theta}{2}}$$

        $$\cos\left(\frac{\theta}{2}\right) = \pm\sqrt{\frac{1 + \cos\theta}{2}}$$

        The sign depends on which quadrant $\theta/2$ is in.

        ### Product-to-Sum Formulas

        $$\sin\alpha\cos\beta = \frac{1}{2}[\sin(\alpha + \beta) + \sin(\alpha - \beta)]$$

        $$\cos\alpha\cos\beta = \frac{1}{2}[\cos(\alpha - \beta) + \cos(\alpha + \beta)]$$

        $$\sin\alpha\sin\beta = \frac{1}{2}[\cos(\alpha - \beta) - \cos(\alpha + \beta)]$$

        These are particularly useful in calculus when integrating products of trig functions.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Part VI: Solving Trigonometric Equations

        ### Basic Equations

        To solve an equation like $\sin x = 0.5$, we need to find all angles whose sine is 0.5.

        **Step 1**: Find the principal solution (the "basic" answer)

        $\sin x = 0.5 \implies x = \arcsin(0.5) = \frac{\pi}{6}$ (or 30°)

        **Step 2**: Use symmetry to find other solutions in $[0, 2\pi)$

        Since $\sin(\pi - x) = \sin x$, we also have $x = \pi - \frac{\pi}{6} = \frac{5\pi}{6}$

        **Step 3**: Add periodicity to get all solutions

        Since sine has period $2\pi$, the complete solution is:

        $$x = \frac{\pi}{6} + 2\pi k \quad \text{or} \quad x = \frac{5\pi}{6} + 2\pi k, \quad k \in \mathbb{Z}$$

        This is called the **general solution**.
        """
    )
    return


@app.cell
def _(mo):
    equation_slider = mo.ui.slider(
        start=-1, stop=1, step=0.1, value=0.5,
        label="sin(x) = ",
        show_value=True,
    )
    return (equation_slider,)


@app.cell
def _(equation_slider, mo):
    mo.hstack([
        mo.md("### Equation Solver: $\\sin(x) = c$"),
        equation_slider,
    ])
    return


@app.cell
def _(equation_slider, go, np):
    _c = equation_slider.value

    _x = np.linspace(-2 * np.pi, 4 * np.pi, 1000)
    _y = np.sin(_x)

    _fig = go.Figure()

    # Sine curve
    _fig.add_trace(go.Scatter(
        x=_x, y=_y,
        mode='lines',
        line={'color': '#00d4ff', 'width': 3},
        name='sin(x)',
    ))

    # Horizontal line y = c
    _fig.add_trace(go.Scatter(
        x=[-2*np.pi, 4*np.pi], y=[_c, _c],
        mode='lines',
        line={'color': '#ff6b6b', 'width': 2, 'dash': 'dash'},
        name=f'y = {_c}',
    ))

    # Find solutions
    if abs(_c) <= 1:
        _principal = np.arcsin(_c)
        _solutions = []

        # Solutions in range [-2pi, 4pi]
        for _k in range(-2, 3):
            _sol1 = _principal + 2 * np.pi * _k
            _sol2 = np.pi - _principal + 2 * np.pi * _k
            if -2*np.pi <= _sol1 <= 4*np.pi:
                _solutions.append(_sol1)
            if -2*np.pi <= _sol2 <= 4*np.pi:
                _solutions.append(_sol2)

        _solutions = sorted(set(_solutions))

        # Mark solutions
        for _sol in _solutions:
            _fig.add_trace(go.Scatter(
                x=[_sol], y=[_c],
                mode='markers',
                marker={'color': '#ffe66d', 'size': 12, 'symbol': 'circle'},
                showlegend=False,
                hovertemplate=f'x = {_sol:.3f}<extra></extra>'
            ))

        _solution_text = f'Principal: x = {_principal:.3f} rad'
    else:
        _solution_text = 'No solution (|c| > 1)'

    _fig.add_annotation(
        x=np.pi, y=1.3,
        text=_solution_text,
        font={'color': '#ffe66d', 'size': 14},
        showarrow=False,
    )

    _fig.update_layout(
        minreducedwidth=300,
        paper_bgcolor='#1a1a2e',
        plot_bgcolor='#16213e',
        font={'color': '#eaeaea', 'family': 'JetBrains Mono, monospace'},
        title=f'Solutions to sin(x) = {_c}',
        xaxis={
            'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0',
            'title': 'x (radians)',
            'tickvals': [-2*np.pi, -np.pi, 0, np.pi, 2*np.pi, 3*np.pi, 4*np.pi],
            'ticktext': ['-2π', '-π', '0', 'π', '2π', '3π', '4π'],
        },
        yaxis={
            'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0',
            'title': 'y', 'range': [-1.5, 1.5]
        },
        showlegend=True,
        legend={'bgcolor': 'rgba(22, 33, 62, 0.8)', 'orientation': 'h', 'yanchor': 'bottom', 'y': -0.2, 'xanchor': 'center', 'x': 0.5},
        margin={'l': 40, 'r': 40, 't': 50, 'b': 100},
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The yellow dots show all solutions to $\sin(x) = c$ in the displayed range.
        Notice that:

        - When $|c| < 1$: infinitely many solutions, evenly spaced
        - When $|c| = 1$: solutions occur at peaks/troughs only
        - When $|c| > 1$: no solutions (sine never exceeds 1 in absolute value)

        The periodic nature of sine means that if $x_0$ is a solution, then so is $x_0 + 2\pi k$
        for any integer $k$.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Equations Involving Identities

        More complex equations often require using identities to simplify first.

        **Example**: Solve $2\sin^2 x - \sin x - 1 = 0$

        **Step 1**: This is a quadratic in $\sin x$. Let $u = \sin x$:
        $$2u^2 - u - 1 = 0$$

        **Step 2**: Factor:
        $$(2u + 1)(u - 1) = 0$$

        **Step 3**: Solve for $u$:
        $$u = -\frac{1}{2} \quad \text{or} \quad u = 1$$

        **Step 4**: Back-substitute:
        - $\sin x = 1 \implies x = \frac{\pi}{2} + 2\pi k$
        - $\sin x = -\frac{1}{2} \implies x = -\frac{\pi}{6} + 2\pi k$ or $x = \frac{7\pi}{6} + 2\pi k$

        ### Key Strategies

        1. **Isolate** a single trig function when possible
        2. **Use identities** to convert to a single function
        3. **Factor** if you have a quadratic or higher polynomial in a trig function
        4. **Check** your solutions in the original equation (squaring can introduce extraneous solutions)
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Part VII: Calculus Connection

        ### Derivatives of Trigonometric Functions

        One of the most beautiful results in calculus: the derivatives of sine and cosine
        are remarkably simple.

        $$\boxed{\frac{d}{dx}[\sin x] = \cos x}$$

        $$\boxed{\frac{d}{dx}[\cos x] = -\sin x}$$

        Notice the pattern:
        - Differentiating sine gives cosine
        - Differentiating cosine gives negative sine
        - Differentiating again gives negative cosine
        - And again gives positive sine

        After four derivatives, you're back where you started! This cyclic behavior is
        unique to sine and cosine (and their linear combinations).

        ### Other Trig Derivatives

        $$\frac{d}{dx}[\tan x] = \sec^2 x \quad\quad \frac{d}{dx}[\cot x] = -\csc^2 x$$

        $$\frac{d}{dx}[\sec x] = \sec x \tan x \quad\quad \frac{d}{dx}[\csc x] = -\csc x \cot x$$
        """
    )
    return


@app.cell
def _(mo):
    deriv_point = mo.ui.slider(
        start=-2 * np.pi, stop=2 * np.pi, step=0.1, value=np.pi/4,
        label="Point x₀",
        show_value=True,
    )
    return (deriv_point,)


@app.cell
def _(deriv_point, mo):
    mo.hstack([
        mo.md("### Derivative Visualization: Tangent Line on sin(x)"),
        deriv_point,
    ])
    return


@app.cell
def _(deriv_point, go, np):
    _x0 = deriv_point.value
    _y0 = np.sin(_x0)
    _slope = np.cos(_x0)  # Derivative at x0

    _x = np.linspace(-2 * np.pi, 2 * np.pi, 500)
    _y = np.sin(_x)

    # Tangent line
    _x_tan = np.array([_x0 - 1.5, _x0 + 1.5])
    _y_tan = _y0 + _slope * (_x_tan - _x0)

    _fig = go.Figure()

    # Sine curve
    _fig.add_trace(go.Scatter(
        x=_x, y=_y,
        mode='lines',
        line={'color': '#00d4ff', 'width': 3},
        name='sin(x)',
    ))

    # Tangent line
    _fig.add_trace(go.Scatter(
        x=_x_tan, y=_y_tan,
        mode='lines',
        line={'color': '#ff6b6b', 'width': 2},
        name=f'Tangent (slope = cos({_x0:.2f}) = {_slope:.3f})',
    ))

    # Point of tangency
    _fig.add_trace(go.Scatter(
        x=[_x0], y=[_y0],
        mode='markers',
        marker={'color': '#ffe66d', 'size': 12},
        name=f'({_x0:.2f}, {_y0:.3f})',
    ))

    _fig.update_layout(
        minreducedwidth=300,
        paper_bgcolor='#1a1a2e',
        plot_bgcolor='#16213e',
        font={'color': '#eaeaea', 'family': 'JetBrains Mono, monospace'},
        title=f"d/dx[sin x] = cos x | At x = {_x0:.2f}: slope = {_slope:.3f}",
        xaxis={
            'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0',
            'title': 'x',
            'tickvals': [-2*np.pi, -np.pi, 0, np.pi, 2*np.pi],
            'ticktext': ['-2π', '-π', '0', 'π', '2π'],
        },
        yaxis={
            'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0',
            'title': 'y', 'range': [-2, 2]
        },
        showlegend=True,
        legend={'bgcolor': 'rgba(22, 33, 62, 0.8)', 'orientation': 'h', 'yanchor': 'bottom', 'y': -0.2, 'xanchor': 'center', 'x': 0.5},
        margin={'l': 40, 'r': 40, 't': 50, 'b': 100},
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Move the slider to see how the tangent line changes along the sine curve.
        Notice:

        - When $\sin x$ is at a maximum ($x = \pi/2$), the slope is 0 (horizontal tangent)
        - When $\sin x$ is increasing, the slope (cosine) is positive
        - When $\sin x$ is decreasing, the slope (cosine) is negative
        - The slope is steepest (±1) where the curve crosses zero
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### The Fundamental Limit

        To prove that $\frac{d}{dx}\sin x = \cos x$, we need to evaluate:

        $$\frac{d}{dx}\sin x = \lim_{h \to 0} \frac{\sin(x + h) - \sin x}{h}$$

        Using the angle addition formula:

        $$= \lim_{h \to 0} \frac{\sin x \cos h + \cos x \sin h - \sin x}{h}$$

        $$= \lim_{h \to 0} \left[ \sin x \cdot \frac{\cos h - 1}{h} + \cos x \cdot \frac{\sin h}{h} \right]$$

        This requires two key limits:

        $$\boxed{\lim_{h \to 0} \frac{\sin h}{h} = 1}$$

        $$\lim_{h \to 0} \frac{\cos h - 1}{h} = 0$$

        The first limit is fundamental—it's why radians are the "natural" unit for angles.
        """
    )
    return


@app.cell
def _(mo):
    limit_slider = mo.ui.slider(
        start=0.01, stop=1, step=0.01, value=0.5,
        label="h value",
        show_value=True,
    )
    return (limit_slider,)


@app.cell
def _(limit_slider, mo):
    mo.hstack([
        mo.md("### Limit Demonstration: $\\lim_{h \\to 0} \\frac{\\sin h}{h} = 1$"),
        limit_slider,
    ])
    return


@app.cell
def _(go, limit_slider, np):
    _h = limit_slider.value

    _fig = go.Figure()

    # Unit circle
    _circle_theta = np.linspace(0, 2 * np.pi, 100)
    _fig.add_trace(go.Scatter(
        x=np.cos(_circle_theta), y=np.sin(_circle_theta),
        mode='lines',
        line={'color': '#4ecdc4', 'width': 2},
        name='Unit circle',
        hoverinfo='skip'
    ))

    # Arc from 0 to h
    _arc = np.linspace(0, _h, 50)
    _fig.add_trace(go.Scatter(
        x=np.cos(_arc), y=np.sin(_arc),
        mode='lines',
        line={'color': '#ffe66d', 'width': 4},
        name=f'Arc length = h = {_h:.3f}',
    ))

    # sin(h) - vertical line
    _fig.add_trace(go.Scatter(
        x=[np.cos(_h), np.cos(_h)], y=[0, np.sin(_h)],
        mode='lines',
        line={'color': '#ff6b6b', 'width': 3},
        name=f'sin(h) = {np.sin(_h):.4f}',
    ))

    # Radius to point
    _fig.add_trace(go.Scatter(
        x=[0, np.cos(_h)], y=[0, np.sin(_h)],
        mode='lines',
        line={'color': '#00d4ff', 'width': 2},
        showlegend=False,
    ))

    # Point
    _fig.add_trace(go.Scatter(
        x=[np.cos(_h)], y=[np.sin(_h)],
        mode='markers',
        marker={'color': '#ff6b6b', 'size': 10},
        showlegend=False,
    ))

    # Ratio annotation
    _ratio = np.sin(_h) / _h
    _fig.add_annotation(
        x=0.5, y=-0.3,
        text=f'sin(h)/h = {np.sin(_h):.4f}/{_h:.3f} = {_ratio:.6f}',
        font={'color': '#ffe66d', 'size': 14},
        showarrow=False,
    )

    _fig.update_layout(
        minreducedwidth=300,
        paper_bgcolor='#1a1a2e',
        plot_bgcolor='#16213e',
        font={'color': '#eaeaea', 'family': 'JetBrains Mono, monospace'},
        title=f'As h → 0: sin(h)/h → 1',
        xaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'range': [-0.2, 1.3], 'scaleanchor': 'y'},
        yaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'range': [-0.5, 1.1]},
        legend={'bgcolor': 'rgba(22, 33, 62, 0.8)', 'font': {'size': 10}},
        height=450,
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The visualization compares:
        - **Arc length** (h, in yellow): the distance along the circle
        - **sin(h)** (in red): the vertical distance

        As h approaches 0, these two lengths become nearly equal, so their ratio approaches 1.
        This is the geometric intuition behind the fundamental limit.

        Decrease the slider toward 0 and watch the ratio approach 1.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Connection to Notebook 001

        The derivative formulas for sine and cosine are essential for understanding:
        - Simple harmonic motion (pendulums, springs)
        - Waves and oscillations
        - Signal processing
        - Solutions to differential equations

        In the functions and derivatives notebook, we saw that the derivative tells us
        the instantaneous rate of change. For $y = \sin x$:
        - When the curve is rising, $\cos x > 0$
        - When the curve is falling, $\cos x < 0$
        - When the curve is at a peak or trough, $\cos x = 0$

        This is the calculus perspective on the relationship between sine and cosine.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Part VIII: Applications

        ### Simple Harmonic Motion

        When a mass on a spring oscillates, or a pendulum swings (for small angles),
        the motion is described by:

        $$x(t) = A\cos(\omega t + \phi)$$

        where:
        - $x(t)$ is the position at time $t$
        - $A$ is the **amplitude** (maximum displacement)
        - $\omega$ is the **angular frequency** (how fast it oscillates)
        - $\phi$ is the **phase** (where in the cycle it starts)

        The velocity is the derivative:
        $$v(t) = x'(t) = -A\omega\sin(\omega t + \phi)$$

        And the acceleration:
        $$\begin{aligned}
        a(t) &= x''(t) \\
        &= -A\omega^2\cos(\omega t + \phi) \\
        &= -\omega^2 x(t)
        \end{aligned}$$

        The last form reveals that the acceleration is proportional to position but opposite
        in direction—this is what makes the motion oscillate!
        """
    )
    return


@app.cell
def _(mo):
    shm_amp = mo.ui.slider(start=0.5, stop=2, step=0.1, value=1, label="Amplitude A", show_value=True)
    shm_freq = mo.ui.slider(start=0.5, stop=3, step=0.1, value=1, label="Frequency ω", show_value=True)
    return shm_amp, shm_freq


@app.cell
def _(mo, shm_amp, shm_freq):
    mo.vstack([
        mo.md("### Simple Harmonic Motion"),
        mo.hstack([shm_amp, shm_freq], justify="start", gap=2),
    ])
    return


@app.cell
def _(go, make_subplots, np, shm_amp, shm_freq):
    _A = shm_amp.value
    _omega = shm_freq.value

    _t = np.linspace(0, 4 * np.pi, 500)
    _x = _A * np.cos(_omega * _t)
    _v = -_A * _omega * np.sin(_omega * _t)
    _a = -_A * _omega**2 * np.cos(_omega * _t)

    _fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                         subplot_titles=['Position x(t)', 'Velocity v(t)', 'Acceleration a(t)'],
                         vertical_spacing=0.08)

    # Position
    _fig.add_trace(go.Scatter(
        x=_t, y=_x,
        mode='lines',
        line={'color': '#00d4ff', 'width': 2},
        name='x(t) = A cos(ωt)',
    ), row=1, col=1)

    # Velocity
    _fig.add_trace(go.Scatter(
        x=_t, y=_v,
        mode='lines',
        line={'color': '#4ecdc4', 'width': 2},
        name='v(t) = -Aω sin(ωt)',
    ), row=2, col=1)

    # Acceleration
    _fig.add_trace(go.Scatter(
        x=_t, y=_a,
        mode='lines',
        line={'color': '#ff6b6b', 'width': 2},
        name='a(t) = -Aω² cos(ωt)',
    ), row=3, col=1)

    _fig.update_layout(
        minreducedwidth=300,
        paper_bgcolor='#1a1a2e',
        plot_bgcolor='#16213e',
        font={'color': '#eaeaea', 'family': 'JetBrains Mono, monospace'},
        title=f'Simple Harmonic Motion: A = {_A}, ω = {_omega}',
        showlegend=True,
        legend={'bgcolor': 'rgba(22, 33, 62, 0.8)', 'orientation': 'h', 'yanchor': 'bottom', 'y': -0.15, 'xanchor': 'center', 'x': 0.5},
        height=600,
    )

    for _i in range(1, 4):
        _fig.update_xaxes(gridcolor='#2d3a4f', zerolinecolor='#a0a0a0', row=_i, col=1)
        _fig.update_yaxes(gridcolor='#2d3a4f', zerolinecolor='#a0a0a0', row=_i, col=1)

    _fig.update_xaxes(title_text='Time t', row=3, col=1)

    # Update subplot title colors
    for _annotation in _fig['layout']['annotations']:
        _annotation['font'] = {'color': '#eaeaea', 'size': 12}

    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        **Observations:**

        - **Position** (blue) oscillates between $+A$ and $-A$
        - **Velocity** (teal) is 90° out of phase with position
          - When position is at an extreme, velocity is zero
          - When position passes through zero, velocity is maximum
        - **Acceleration** (red) is 180° out of phase with position
          - Always points toward equilibrium (opposite sign to position)

        This is why the motion repeats: the acceleration always pushes the object back
        toward the center. It overshoots, then the acceleration reverses, and the cycle
        continues forever (in the idealized case with no friction).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Sound Waves and Music

        Sound is a pressure wave—air molecules oscillate back and forth as the wave passes.
        A pure musical tone is a sinusoidal pressure wave:

        $$p(t) = A\sin(2\pi f t)$$

        where $f$ is the frequency in Hertz (cycles per second).

        | Note | Frequency (Hz) |
        |------|----------------|
        | A4 (concert pitch) | 440 |
        | Middle C (C4) | 261.6 |
        | A above middle C (A5) | 880 |

        Each octave doubles the frequency. A5 (880 Hz) is one octave above A4 (440 Hz).

        ### Fourier's Revolutionary Insight

        In 1822, Joseph Fourier made one of the most important discoveries in mathematics:

        > *Any periodic function can be written as a sum of sines and cosines.*

        This means that even complex waveforms (like the sound of a violin or a human voice)
        can be decomposed into simple sinusoidal components. This is the basis of:

        - Audio compression (MP3, AAC)
        - Image compression (JPEG)
        - Signal processing
        - Quantum mechanics
        - Solving differential equations

        Fourier analysis is perhaps the most widely applied mathematical technique in
        science and engineering.
        """
    )
    return


@app.cell
def _(go, np):
    # Fourier series demonstration: square wave approximation
    _t = np.linspace(0, 2 * np.pi, 1000)

    _fig = go.Figure()

    # Square wave
    _square = np.sign(np.sin(_t))
    _fig.add_trace(go.Scatter(
        x=_t, y=_square,
        mode='lines',
        line={'color': '#4ecdc4', 'width': 2, 'dash': 'dash'},
        name='Square wave',
    ))

    # Fourier approximations
    _colors = ['#00d4ff', '#ffe66d', '#ff6b6b', '#95e1d3']
    for _n_terms, _color in zip([1, 3, 5, 15], _colors):
        _approx = np.zeros_like(_t)
        for _k in range(1, 2 * _n_terms, 2):  # Odd harmonics only
            _approx += (4 / np.pi) * (1 / _k) * np.sin(_k * _t)
        _fig.add_trace(go.Scatter(
            x=_t, y=_approx,
            mode='lines',
            line={'color': _color, 'width': 2},
            name=f'{_n_terms} term(s)',
        ))

    _fig.update_layout(
        minreducedwidth=300,
        paper_bgcolor='#1a1a2e',
        plot_bgcolor='#16213e',
        font={'color': '#eaeaea', 'family': 'JetBrains Mono, monospace'},
        title='Fourier Series: Approximating a Square Wave with Sines',
        xaxis={
            'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0',
            'title': 't',
            'tickvals': [0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi],
            'ticktext': ['0', 'π/2', 'π', '3π/2', '2π'],
        },
        yaxis={
            'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0',
            'title': 'f(t)', 'range': [-1.5, 1.5]
        },
        showlegend=True,
        legend={'bgcolor': 'rgba(22, 33, 62, 0.8)'},
        height=400,
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The graph shows how a square wave (dashed teal) can be approximated by adding
        sine waves. The Fourier series for a square wave is:

        $$f(t) = \frac{4}{\pi}\left(\sin t + \frac{\sin 3t}{3} + \frac{\sin 5t}{5} + \frac{\sin 7t}{7} + \cdots\right)$$

        With more terms, the approximation gets better, especially at the flat parts.
        The oscillations near the discontinuities (called **Gibbs phenomenon**) never
        completely disappear, but they get narrower.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Part IX: Summary and Reference

        ### Quick Reference: Identities

        **Pythagorean Identities:**
        $$\sin^2\theta + \cos^2\theta = 1$$
        $$\tan^2\theta + 1 = \sec^2\theta$$
        $$1 + \cot^2\theta = \csc^2\theta$$

        **Angle Addition:**
        $$\sin(\alpha \pm \beta) = \sin\alpha\cos\beta \pm \cos\alpha\sin\beta$$
        $$\cos(\alpha \pm \beta) = \cos\alpha\cos\beta \mp \sin\alpha\sin\beta$$

        **Double Angle:**
        $$\sin 2\theta = 2\sin\theta\cos\theta$$
        $$\begin{aligned}
        \cos 2\theta &= \cos^2\theta - \sin^2\theta \\
        &= 2\cos^2\theta - 1 \\
        &= 1 - 2\sin^2\theta
        \end{aligned}$$

        **Derivatives:**
        $$\frac{d}{dx}\sin x = \cos x \quad\quad \frac{d}{dx}\cos x = -\sin x$$
        $$\frac{d}{dx}\tan x = \sec^2 x \quad\quad \frac{d}{dx}\sec x = \sec x \tan x$$

        **Integrals:**
        $$\int \sin x \, dx = -\cos x + C \quad\quad \int \cos x \, dx = \sin x + C$$
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Historical Timeline

        | Date | Event |
        |------|-------|
        | ~2000 BCE | Babylonians use 360° circle |
        | ~190-120 BCE | Hipparchus creates chord tables |
        | ~150 CE | Ptolemy's Almagest |
        | ~500 CE | Aryabhata introduces sine (half-chord) |
        | ~800 CE | Al-Khwarizmi writes sine/tangent tables |
        | 1464 | Regiomontanus: first European trig textbook |
        | 1748 | Euler establishes modern notation |
        | 1822 | Fourier: periodic functions as sums of sines |

        ### Further Reading

        **Video Series:**
        - [3Blue1Brown: Essence of Trigonometry](https://www.youtube.com/watch?v=yBw67Fb31Cs) — Visual explanations
        - [Khan Academy: Trigonometry](https://www.khanacademy.org/math/trigonometry) — Comprehensive course

        **Books:**
        - Maor, *Trigonometric Delights* — History and surprising applications
        - Stewart, *Calculus* — Standard treatment with trig applications

        **Primary Sources:**
        - [Ptolemy's Almagest](https://archive.org/details/ptolemysalmagest0000ptol) — Original chord tables
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        *"I believe that the discovery that the trig functions can be developed as infinite
        series is one of the most beautiful achievements of all mathematics."*

        — Richard Courant
        """
    )
    return


if __name__ == "__main__":
    app.run()
