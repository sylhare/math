import marimo

__generated_with = "0.9.0"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import plotly.graph_objects as go
    import sympy as sp
    from sympy import Symbol, sin, cos, exp, sqrt, integrate
    import polars as pl
    from scipy import integrate as sci_integrate
    return go, mo, np, pl, sp, cos, exp, sin, sqrt, Symbol, integrate, sci_integrate


@app.cell
def _(mo):
    mo.md(
        r"""
        # Integrals and the Accumulation of Change
        ## From Ancient Geometry to Modern Computation

        *"The integral calculus is nothing but an assemblage of all those quantities which we have
        gained by differentiating, and which we desire to integrate again."*
        — Johann Bernoulli

        ---

        This notebook explores **integration**—the mathematics of accumulation. While derivatives
        tell us about instantaneous rates of change, integrals tell us about **total accumulated
        quantities**: areas, volumes, distances traveled, work done, and much more.

        **What you'll learn:**
        - How ancient mathematicians approximated areas without calculus
        - The connection between area and antiderivatives (the Fundamental Theorem)
        - Numerical methods for computing integrals
        - Real-world applications: physics, probability, and engineering
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Part I: The Ancient Quest for Area

        ### Measuring the Unmeasurable

        Long before calculus, mathematicians struggled with a fundamental question:
        **How do you find the area of a curved shape?**

        For rectangles and triangles, the answer is simple—just multiply base times height
        (or half of that for triangles). But what about circles? Parabolas? Arbitrary curves?

        The ancient Greeks developed ingenious methods to tackle this problem, laying the
        groundwork for integral calculus two thousand years before Newton and Leibniz.

        ### Archimedes and the Method of Exhaustion (c. 250 BCE)

        **Archimedes of Syracuse** was perhaps the greatest mathematician of antiquity. He
        developed the **method of exhaustion**—a technique for finding areas by filling a
        shape with simpler shapes (usually triangles or rectangles) until the gaps are
        "exhausted."

        His most famous result: the area of a circle is $\pi r^2$.

        **How he did it:**
        1. Inscribe a polygon (like a hexagon) inside the circle
        2. Circumscribe another polygon outside the circle
        3. The circle's area is trapped between the two polygon areas
        4. As you add more sides, the polygons squeeze closer to the circle
        5. The limit of this process gives the exact area

        This is essentially the same idea as Riemann sums—2000 years early!

        > 📚 **Primary Source**: [Archimedes' "Measurement of a Circle"](https://www.math.ubc.ca/~cass/archimedes/circle.html)
        """
    )
    return


@app.cell
def _(go, np):
    # Visualize Archimedes' method of exhaustion for a circle
    def _create_exhaustion_demo():
        """Show polygons approximating a circle."""
        theta = np.linspace(0, 2 * np.pi, 100)
        circle_x = np.cos(theta)
        circle_y = np.sin(theta)

        n_sides_options = [4, 6, 8, 12, 24, 48]

        fig = go.Figure()

        # Circle
        fig.add_trace(go.Scatter(
            x=circle_x, y=circle_y,
            mode='lines',
            line={'color': '#00d4ff', 'width': 3},
            name='Circle (area = π)',
            fill='toself',
            fillcolor='rgba(0, 212, 255, 0.2)',
        ))

        # Initial inscribed polygon
        n = n_sides_options[0]
        angles = np.linspace(0, 2 * np.pi, n + 1)
        poly_x = np.cos(angles)
        poly_y = np.sin(angles)
        area = 0.5 * n * np.sin(2 * np.pi / n)

        fig.add_trace(go.Scatter(
            x=poly_x, y=poly_y,
            mode='lines',
            line={'color': '#ff6b6b', 'width': 2},
            name=f'Inscribed polygon',
            fill='toself',
            fillcolor='rgba(255, 107, 107, 0.3)',
        ))

        # Create slider steps
        steps = []
        for n in n_sides_options:
            angles = np.linspace(0, 2 * np.pi, n + 1)
            poly_x = np.cos(angles)
            poly_y = np.sin(angles)
            area = 0.5 * n * np.sin(2 * np.pi / n)
            error = abs(np.pi - area) / np.pi * 100

            step = {
                "method": "update",
                "args": [
                    {"x": [circle_x, poly_x], "y": [circle_y, poly_y]},
                    {"title": f"n = {n} sides | Polygon area = {area:.6f} | π = {np.pi:.6f} | Error: {error:.2f}%"}
                ],
                "label": str(n),
            }
            steps.append(step)

        fig.update_layout(
            paper_bgcolor='#16213e',
            plot_bgcolor='#1a1a2e',
            font={'color': '#eaeaea', 'family': 'JetBrains Mono, monospace'},
            title=f"n = {n_sides_options[0]} sides | Polygon area = {0.5 * n_sides_options[0] * np.sin(2 * np.pi / n_sides_options[0]):.6f} | π = {np.pi:.6f}",
            xaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'scaleanchor': 'y'},
            yaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0'},
            showlegend=True,
            legend={'bgcolor': 'rgba(22, 33, 62, 0.8)', 'orientation': 'h', 'yanchor': 'bottom', 'y': -0.15, 'xanchor': 'center', 'x': 0.5},
        margin={'l': 40, 'r': 40, 't': 50, 'b': 80},
            sliders=[{
                "active": 0,
                "currentvalue": {"prefix": "Sides: ", "visible": True},
                "pad": {"b": 10, "t": 50},
                "steps": steps,
                "bgcolor": "#16213e",
                "font": {"color": "#eaeaea"},
            }],
        )

        return fig

    _create_exhaustion_demo()
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        **What this shows:** The blue circle represents the true shape whose area we want to find (π for a unit circle). The red polygon is inscribed inside it, providing a lower bound approximation. As you increase the number of sides, the polygon fills more of the circle, and its area approaches π.

        **Archimedes' Insight:**

        Use the slider above to increase the number of polygon sides. Notice how:
        - With just 4 sides (square), the approximation is rough (~2.0 vs π ≈ 3.14159)
        - With 24 sides, we're within about 1% of the true area
        - With 48 sides, the error drops to about 0.3%

        Archimedes used 96-sided polygons to prove that $3\frac{10}{71} < \pi < 3\frac{1}{7}$,
        a result that stood for centuries!

        The method of exhaustion was rigorous but tedious. Each new shape required a
        custom geometric argument. What mathematicians needed was a **general method**—
        and that wouldn't come until the 17th century.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Part II: The Birth of Integral Calculus

        ### Cavalieri's Principle (1635)

        **Bonaventura Cavalieri** made a crucial conceptual leap: he imagined shapes as
        made up of infinitely many infinitely thin slices (he called them "indivisibles").

        **Cavalieri's Principle**: If two solids have equal cross-sectional areas at every
        height, they have equal volumes.

        This seems obvious, but it was revolutionary. It allowed mathematicians to compare
        volumes of very different shapes by comparing their slices.

        ### The Area Under a Parabola

        Cavalieri and others tackled the problem of finding the area under $y = x^2$ from
        $x = 0$ to $x = b$. This was a major challenge of the era.

        **The approach:**
        1. Divide the interval $[0, b]$ into $n$ equal parts, each of width $\Delta x = \frac{b}{n}$
        2. Build rectangles with heights determined by the function
        3. Sum the rectangle areas
        4. Take the limit as $n \to \infty$

        **The calculation:**
        $$\text{Sum} = \sum_{i=1}^{n} \left(\frac{ib}{n}\right)^2 \cdot \frac{b}{n} = \frac{b^3}{n^3} \sum_{i=1}^{n} i^2$$

        Using the formula $\sum_{i=1}^{n} i^2 = \frac{n(n+1)(2n+1)}{6}$:

        $$= \frac{b^3}{n^3} \cdot \frac{n(n+1)(2n+1)}{6} = \frac{b^3(n+1)(2n+1)}{6n^2}$$

        As $n \to \infty$:
        $$\lim_{n \to \infty} \frac{b^3(n+1)(2n+1)}{6n^2} = \frac{b^3 \cdot 2}{6} = \frac{b^3}{3}$$

        **The area under $y = x^2$ from 0 to $b$ is $\frac{b^3}{3}$!**

        This result was known before calculus, but proving it required clever algebra.
        The Fundamental Theorem would make such calculations trivial.
        """
    )
    return


@app.cell
def _(go, np):
    # Animate the Riemann sum converging for x^2
    def _animate_riemann_convergence():
        """Animate Riemann sums converging to the integral."""
        a, b = 0, 2
        x_curve = np.linspace(a, b, 200)
        y_curve = x_curve ** 2
        true_area = b**3 / 3

        n_values = [2, 4, 8, 16, 32, 64]

        fig = go.Figure()

        # Function curve
        fig.add_trace(go.Scatter(
            x=x_curve, y=y_curve,
            mode='lines',
            line={'color': '#00d4ff', 'width': 3},
            name='f(x) = x²',
        ))

        # Initial rectangles
        n = n_values[0]
        dx = (b - a) / n
        x_left = np.array([a + i * dx for i in range(n)])
        heights = (x_left + dx) ** 2  # Right endpoint
        area = np.sum(heights * dx)

        # Add rectangles as individual shapes for better visualization
        for i in range(n):
            fig.add_shape(
                type="rect",
                x0=x_left[i], x1=x_left[i] + dx,
                y0=0, y1=heights[i],
                fillcolor="rgba(78, 205, 196, 0.5)",
                line=dict(color="#4ecdc4", width=1),
            )

        # Create frames
        frames = []
        for n in n_values:
            dx = (b - a) / n
            x_left = np.array([a + i * dx for i in range(n)])
            heights = (x_left + dx) ** 2
            area = np.sum(heights * dx)
            error = abs(true_area - area) / true_area * 100

            # Create shapes for this frame
            shapes = []
            for i in range(n):
                shapes.append(dict(
                    type="rect",
                    x0=x_left[i], x1=x_left[i] + dx,
                    y0=0, y1=heights[i],
                    fillcolor="rgba(78, 205, 196, 0.5)",
                    line=dict(color="#4ecdc4", width=1),
                ))

            frame = go.Frame(
                data=[go.Scatter(x=x_curve, y=y_curve)],
                layout={"shapes": shapes,
                        "title": f"n = {n} rectangles | Sum = {area:.4f} | True = {true_area:.4f} | Error: {error:.1f}%"},
                name=str(n),
            )
            frames.append(frame)

        fig.frames = frames

        fig.update_layout(
            paper_bgcolor='#16213e',
            plot_bgcolor='#1a1a2e',
            font={'color': '#eaeaea', 'family': 'JetBrains Mono, monospace'},
            title=f"n = {n_values[0]} rectangles | Sum = {np.sum((np.array([a + i * (b-a)/n_values[0] for i in range(n_values[0])]) + (b-a)/n_values[0]) ** 2 * (b-a)/n_values[0]):.4f}",
            xaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'title': 'x', 'range': [-0.2, 2.5]},
            yaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'title': 'y', 'range': [-0.2, 5]},
            showlegend=True,
            legend={'bgcolor': 'rgba(22, 33, 62, 0.8)', 'orientation': 'h', 'yanchor': 'bottom', 'y': -0.15, 'xanchor': 'center', 'x': 0.5},
        margin={'l': 40, 'r': 40, 't': 50, 'b': 80},
            updatemenus=[{
                "type": "buttons",
                "showactive": False,
                "y": 1.15,
                "x": 0.5,
                "xanchor": "center",
                "buttons": [
                    {"label": "▶ Animate", "method": "animate",
                     "args": [None, {"frame": {"duration": 800}, "transition": {"duration": 300}}]},
                ],
                "font": {"color": "#eaeaea"},
                "bgcolor": "#16213e",
            }],
            sliders=[{
                "active": 0,
                "steps": [{"args": [[str(n)], {"frame": {"duration": 0}, "mode": "immediate"}],
                          "label": str(n), "method": "animate"} for n in n_values],
                "x": 0.05, "len": 0.9,
                "currentvalue": {"prefix": "Rectangles: ", "visible": True},
                "bgcolor": "#16213e", "font": {"color": "#eaeaea"},
            }],
        )

        return fig

    _animate_riemann_convergence()
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        **What this shows:** This animation demonstrates how Riemann sums converge to the exact integral. The blue curve is $f(x) = x^2$, and the teal rectangles approximate the area under the curve. As the number of rectangles increases, the approximation improves.

        **What the animation shows:**

        Press **Animate** or use the slider to see how the Riemann sum improves:

        - With 2 rectangles, the error is substantial (the rectangles overshoot significantly)
        - With 8 rectangles, the error drops noticeably
        - With 64 rectangles, we're getting quite close to the true value

        The rectangles are using the **right endpoint rule**—each rectangle's height
        is determined by the function value at its right edge. Other choices
        (left endpoint, midpoint) give different approximations that also converge
        to the same limit.

        **The key insight**: As $n \to \infty$, ALL reasonable rectangle schemes
        converge to the same value. This limit is the **definite integral**.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Part III: The Fundamental Theorem of Calculus

        ### The Revolutionary Connection

        In the 1660s and 1670s, Newton and Leibniz independently discovered something
        remarkable: **differentiation and integration are inverse operations**.

        This is the **Fundamental Theorem of Calculus**, and it changed mathematics forever.

        ### Statement of the Theorem

        The theorem has two parts:

        **Part 1 (Differentiation undoes integration):**
        If $F(x) = \int_a^x f(t) \, dt$, then $F'(x) = f(x)$

        In words: If you integrate a function and then differentiate the result,
        you get back the original function.

        **Part 2 (Integration undoes differentiation):**
        If $F'(x) = f(x)$, then $\int_a^b f(x) \, dx = F(b) - F(a)$

        In words: To compute a definite integral, find ANY antiderivative $F$ of $f$,
        then subtract: $F(b) - F(a)$.

        ### Why This Is Revolutionary

        Before this theorem, computing $\int_0^2 x^2 \, dx$ required:
        1. Dividing into $n$ rectangles
        2. Summing $\frac{b^3}{n^3} \sum_{i=1}^{n} i^2$
        3. Using the formula for $\sum i^2$
        4. Taking a limit

        After this theorem:
        1. The antiderivative of $x^2$ is $\frac{x^3}{3}$ (since $\frac{d}{dx}\frac{x^3}{3} = x^2$)
        2. Therefore: $\int_0^2 x^2 \, dx = \frac{2^3}{3} - \frac{0^3}{3} = \frac{8}{3} - 0 = \frac{8}{3}$

        **Done in two lines!** This is why calculus was such a breakthrough.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Understanding Why It Works

        The Fundamental Theorem connects two seemingly different concepts:
        - **Area** (a geometric quantity)
        - **Antiderivatives** (a symbolic/algebraic concept)

        Here's the intuition:

        Consider the **area function** $A(x) = \int_a^x f(t) \, dt$, which gives the area
        under $f$ from $a$ to $x$.

        **Question**: How does this area change when we move from $x$ to $x + h$?

        The new area is $A(x + h) = \int_a^{x+h} f(t) \, dt$.

        The **change in area** is:
        $$A(x+h) - A(x) = \int_x^{x+h} f(t) \, dt$$

        For small $h$, this is approximately a rectangle with width $h$ and height $f(x)$:
        $$A(x+h) - A(x) \approx f(x) \cdot h$$

        Therefore:
        $$A'(x) = \lim_{h \to 0} \frac{A(x+h) - A(x)}{h} = f(x)$$

        **The derivative of the area function is the original function!**

        This means the area function $A(x)$ is an antiderivative of $f(x)$.
        """
    )
    return


@app.cell
def _(go, np):
    # Visualize the area function and its derivative
    def _visualize_area_function():
        """Show A(x) and its derivative."""
        x = np.linspace(0, 3, 300)

        # f(t) = t (linear for simplicity)
        f = x  # f(x) = x

        # A(x) = integral from 0 to x of t dt = x²/2
        A = x**2 / 2

        # A'(x) = f(x) = x
        A_prime = x

        fig = go.Figure()

        # Area function
        fig.add_trace(go.Scatter(
            x=x, y=A,
            mode='lines',
            line={'color': '#00d4ff', 'width': 3},
            name='A(x) = ∫₀ˣ t dt = x²/2',
        ))

        # Original function (which equals A'(x))
        fig.add_trace(go.Scatter(
            x=x, y=f,
            mode='lines',
            line={'color': '#ff6b6b', 'width': 3},
            name="f(x) = x = A'(x)",
        ))

        # Add annotation
        fig.add_annotation(
            x=2, y=2,
            text="The derivative of the area<br>equals the original function!",
            showarrow=True,
            arrowhead=2,
            ax=50, ay=-50,
            font={'color': '#eaeaea'},
        )

        fig.update_layout(
            paper_bgcolor='#16213e',
            plot_bgcolor='#1a1a2e',
            font={'color': '#eaeaea', 'family': 'JetBrains Mono, monospace'},
            title="Fundamental Theorem: A'(x) = f(x)",
            xaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'title': 'x'},
            yaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'title': 'y'},
            showlegend=True,
            legend={'bgcolor': 'rgba(22, 33, 62, 0.8)', 'orientation': 'h', 'yanchor': 'bottom', 'y': -0.15, 'xanchor': 'center', 'x': 0.5},
        margin={'l': 40, 'r': 40, 't': 50, 'b': 80},
        )

        return fig

    _visualize_area_function()
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        **What this shows:** This visualization illustrates the Fundamental Theorem of Calculus. The blue curve shows the accumulated area function $A(x)$—the integral from 0 to $x$. The red line shows the original function $f(x) = x$. The key insight is that $A'(x) = f(x)$: the derivative of the area function equals the original function.

        **Reading the graph:**

        - **Blue curve**: The area function $A(x) = \int_0^x t \, dt = \frac{x^2}{2}$
        - **Red line**: The original function $f(x) = x$, which also equals $A'(x)$

        Notice that the red line gives the **slope** of the blue curve at each point.
        When $x = 2$:
        - The area is $A(2) = \frac{2^2}{2} = 2$ (blue curve's height)
        - The slope of the blue curve is $A'(2) = 2$ (red line's height)

        This visual confirms the Fundamental Theorem: the rate of change of accumulated
        area equals the height of the function being integrated.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Part IV: Computing Integrals

        ### The Antiderivative Table

        Thanks to the Fundamental Theorem, we can compute definite integrals by finding
        antiderivatives. Here are the most important ones:

        | Function $f(x)$ | Antiderivative $F(x)$ | Verification: $F'(x) = f(x)$ |
        |-----------------|----------------------|------------------------------|
        | $x^n$ (n ≠ -1) | $\frac{x^{n+1}}{n+1}$ | $\frac{d}{dx}\frac{x^{n+1}}{n+1} = x^n$ ✓ |
        | $\frac{1}{x}$ | $\ln|x|$ | $\frac{d}{dx}\ln|x| = \frac{1}{x}$ ✓ |
        | $e^x$ | $e^x$ | $\frac{d}{dx}e^x = e^x$ ✓ |
        | $\sin(x)$ | $-\cos(x)$ | $\frac{d}{dx}(-\cos x) = \sin x$ ✓ |
        | $\cos(x)$ | $\sin(x)$ | $\frac{d}{dx}\sin x = \cos x$ ✓ |
        | $\sec^2(x)$ | $\tan(x)$ | $\frac{d}{dx}\tan x = \sec^2 x$ ✓ |
        | $\frac{1}{1+x^2}$ | $\arctan(x)$ | $\frac{d}{dx}\arctan x = \frac{1}{1+x^2}$ ✓ |

        **Important:** Antiderivatives are only unique up to a constant! If $F(x)$ is an
        antiderivative of $f(x)$, so is $F(x) + C$ for any constant $C$. This is why we
        write $\int f(x)\,dx = F(x) + C$ for indefinite integrals.

        ### Worked Examples

        **Example 1:** $\int_1^3 x^2 \, dx$

        Antiderivative of $x^2$ is $\frac{x^3}{3}$

        $$\begin{aligned}
        \int_1^3 x^2 \, dx &= \left[\frac{x^3}{3}\right]_1^3 \\
        &= \frac{3^3}{3} - \frac{1^3}{3} \\
        &= \frac{27}{3} - \frac{1}{3} \\
        &= \frac{26}{3}
        \end{aligned}$$

        **Example 2:** $\int_0^{\pi} \sin(x) \, dx$

        Antiderivative of $\sin(x)$ is $-\cos(x)$

        $$\begin{aligned}
        \int_0^{\pi} \sin(x) \, dx &= \left[-\cos(x)\right]_0^{\pi} \\
        &= -\cos(\pi) - (-\cos(0)) \\
        &= -(-1) - (-1) \\
        &= 1 + 1 = 2
        \end{aligned}$$

        **Example 3:** $\int_1^e \frac{1}{x} \, dx$

        Antiderivative of $\frac{1}{x}$ is $\ln(x)$

        $$\begin{aligned}
        \int_1^e \frac{1}{x} \, dx &= \left[\ln(x)\right]_1^e \\
        &= \ln(e) - \ln(1) \\
        &= 1 - 0 = 1
        \end{aligned}$$
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Interactive Integral Calculator

        Let's verify these calculations visually. Select a function and bounds to see
        both the geometric area and the computed integral.
        """
    )
    return


@app.cell
def _(mo):
    integral_function = mo.ui.dropdown(
        options={
            "x²": ("x**2", "x^2"),
            "x³": ("x**3", "x^3"),
            "sin(x)": ("sin(x)", r"\sin(x)"),
            "cos(x)": ("cos(x)", r"\cos(x)"),
            "eˣ": ("exp(x)", "e^x"),
            "1/x": ("1/x", r"\frac{1}{x}"),
            "√x": ("sqrt(x)", r"\sqrt{x}"),
        },
        value="x²",
        label="Function f(x):",
    )
    lower_bound = mo.ui.slider(start=-2.0, stop=2.0, step=0.1, value=0.0, label="Lower bound a:")
    upper_bound = mo.ui.slider(start=-2.0, stop=4.0, step=0.1, value=2.0, label="Upper bound b:")
    return integral_function, lower_bound, upper_bound


@app.cell
def _(integral_function, lower_bound, upper_bound, mo):
    mo.hstack([
        mo.vstack([integral_function, lower_bound, upper_bound]),
    ])
    return


@app.cell
def _(integral_function, lower_bound, upper_bound, go, np, sp, Symbol, integrate):
    _x = Symbol('x')
    _expr_str, _latex_str = integral_function.value
    _expr = sp.sympify(_expr_str)
    _f = sp.lambdify(_x, _expr, modules=['numpy'])

    _a = lower_bound.value
    _b = upper_bound.value

    # Compute integral symbolically
    try:
        _antideriv = integrate(_expr, _x)
        _definite = integrate(_expr, (_x, _a, _b))
        _result = float(_definite.evalf())
        _antideriv_str = sp.latex(_antideriv)
    except Exception:
        _result = None
        _antideriv_str = "?"

    # Generate plot data
    _x_plot = np.linspace(min(_a, _b) - 0.5, max(_a, _b) + 0.5, 300)
    with np.errstate(divide='ignore', invalid='ignore'):
        _y_plot = _f(_x_plot)
        _y_plot = np.where(np.abs(_y_plot) > 100, np.nan, _y_plot)

    # Area region
    _x_fill = np.linspace(_a, _b, 100)
    with np.errstate(divide='ignore', invalid='ignore'):
        _y_fill = _f(_x_fill)
        _y_fill = np.where(np.abs(_y_fill) > 100, np.nan, _y_fill)

    _fig = go.Figure()

    # Filled area
    _fig.add_trace(go.Scatter(
        x=np.concatenate([_x_fill, _x_fill[::-1]]),
        y=np.concatenate([_y_fill, np.zeros_like(_y_fill)]),
        fill='toself',
        fillcolor='rgba(78, 205, 196, 0.4)',
        line={'color': 'rgba(78, 205, 196, 0)'},
        name=f'Area = {_result:.4f}' if _result else 'Area',
        hoverinfo='skip',
    ))

    # Function curve
    _fig.add_trace(go.Scatter(
        x=_x_plot, y=_y_plot,
        mode='lines',
        line={'color': '#00d4ff', 'width': 3},
        name=f'f(x) = {_latex_str}',
    ))

    # Bounds
    _fig.add_vline(x=_a, line_dash="dash", line_color="#ff6b6b", annotation_text=f"a = {_a}")
    _fig.add_vline(x=_b, line_dash="dash", line_color="#ff6b6b", annotation_text=f"b = {_b}")

    _title = f"∫ from {_a} to {_b} of {_latex_str} dx = {_result:.4f}" if _result else f"∫ from {_a} to {_b}"

    _fig.update_layout(
        paper_bgcolor='#16213e',
        plot_bgcolor='#1a1a2e',
        font={'color': '#eaeaea', 'family': 'JetBrains Mono, monospace'},
        title=_title,
        xaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'title': 'x'},
        yaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'title': 'y'},
        showlegend=True,
        legend={'bgcolor': 'rgba(22, 33, 62, 0.8)', 'orientation': 'h', 'yanchor': 'bottom', 'y': -0.15, 'xanchor': 'center', 'x': 0.5},
        margin={'l': 40, 'r': 40, 't': 50, 'b': 80},
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        **What this shows:** This interactive calculator computes and visualizes definite integrals. The blue curve is the selected function, the shaded teal region represents the integral (area between the curve and the x-axis), and the red dashed lines mark the integration bounds $a$ and $b$.

        **Try different functions and bounds:**

        - For $\int_0^2 x^2 \, dx$, you should get $\frac{8}{3} \approx 2.667$
        - For $\int_0^{\pi} \sin(x) \, dx$, set bounds to 0 and 3.14 to get approximately 2
        - Notice how negative areas (below the x-axis) subtract from the total

        **Key insight:** The integral gives **signed area**—regions below the x-axis
        contribute negative area. This is why $\int_0^{2\pi} \sin(x) \, dx = 0$ even
        though there's clearly area under the curve!
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Part V: Numerical Integration

        ### When Antiderivatives Don't Exist

        Not every function has a nice antiderivative. Famous examples include:

        - $\int e^{-x^2} dx$ — The Gaussian integral (crucial for probability)
        - $\int \frac{\sin(x)}{x} dx$ — The sine integral
        - $\int \sqrt{1 + x^4} dx$ — No elementary form

        For these, we need **numerical methods**—algorithms that approximate the
        integral to any desired accuracy.

        ### Method 1: Rectangle Rule (Riemann Sums)

        We've already seen this: divide into $n$ rectangles and sum their areas.

        $$\int_a^b f(x) \, dx \approx \sum_{i=1}^{n} f(x_i) \cdot \Delta x$$

        where $\Delta x = \frac{b-a}{n}$ and $x_i$ is some point in the $i$-th subinterval.

        **Error**: $O(1/n)$ — to halve the error, double the rectangles.

        ### Method 2: Trapezoidal Rule

        Instead of rectangles, use trapezoids that connect adjacent function values.

        $$\int_a^b f(x) \, dx \approx \frac{\Delta x}{2} \left[ f(x_0) + 2f(x_1) + 2f(x_2) + \cdots + 2f(x_{n-1}) + f(x_n) \right]$$

        **Error**: $O(1/n^2)$ — to halve the error, multiply $n$ by $\sqrt{2}$.

        ### Method 3: Simpson's Rule

        Use parabolas instead of lines to connect points. This requires an even number of
        subintervals.

        $$\int_a^b f(x) \, dx \approx \frac{\Delta x}{3} \left[ f(x_0) + 4f(x_1) + 2f(x_2) + 4f(x_3) + \cdots + 4f(x_{n-1}) + f(x_n) \right]$$

        **Error**: $O(1/n^4)$ — dramatically better! To halve the error, multiply $n$ by $\sqrt[4]{2} \approx 1.19$.

        Simpson's Rule is remarkably accurate for smooth functions.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Comparing Numerical Methods

        Let's see how these methods compare on a function where we know the exact answer.
        We'll integrate $f(x) = x^2$ from 0 to 1, where the exact answer is $\frac{1}{3}$.
        """
    )
    return


@app.cell
def _(mo, np, pl):
    # Compare numerical integration methods
    def _f(x):
        return x ** 2

    _a, _b = 0, 1
    _exact = 1/3

    _results = []
    for _n in [4, 8, 16, 32, 64, 128]:
        _dx = (_b - _a) / _n
        _x = np.linspace(_a, _b, _n + 1)
        _y = _f(_x)

        # Rectangle (midpoint)
        _x_mid = np.linspace(_a + _dx/2, _b - _dx/2, _n)
        _rect = np.sum(_f(_x_mid)) * _dx
        _rect_err = abs(_rect - _exact)

        # Trapezoidal
        _trap = _dx * (0.5 * _y[0] + np.sum(_y[1:-1]) + 0.5 * _y[-1])
        _trap_err = abs(_trap - _exact)

        # Simpson's (requires even n)
        if _n % 2 == 0:
            _simp_coeffs = np.ones(_n + 1)
            _simp_coeffs[1:-1:2] = 4
            _simp_coeffs[2:-1:2] = 2
            _simp = _dx / 3 * np.sum(_simp_coeffs * _y)
            _simp_err = abs(_simp - _exact)
        else:
            _simp = None
            _simp_err = None

        _results.append({
            "n": _n,
            "Rectangle Error": f"{_rect_err:.2e}",
            "Trapezoid Error": f"{_trap_err:.2e}",
            "Simpson Error": f"{_simp_err:.2e}" if _simp_err else "N/A",
        })

    _df = pl.DataFrame(_results)

    mo.vstack([
        mo.md(r"""
**Numerical Integration Accuracy for $\int_0^1 x^2 \, dx = \frac{1}{3}$**

The table shows absolute errors for each method:
        """),
        mo.ui.table(_df),
        mo.md(r"""
**Observations:**

- Rectangle error decreases by ~4× when n doubles (that's $O(1/n^2)$ for midpoint rule)
- Trapezoid error also decreases by ~4× when n doubles ($O(1/n^2)$)
- Simpson's error decreases by ~16× when n doubles ($O(1/n^4)$) — much faster!

With just 16 subintervals, Simpson's rule is accurate to 10 decimal places for this polynomial!
        """),
    ])
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Visualizing the Methods

        Let's see how each method approximates the area geometrically.
        """
    )
    return


@app.cell
def _(go, np):
    # Visualize different numerical integration methods
    def _visualize_methods():
        """Compare rectangle, trapezoid, and Simpson's rule visually."""
        a, b = 0, 2
        n = 4

        x_curve = np.linspace(a, b, 200)
        y_curve = x_curve ** 2

        dx = (b - a) / n
        x_pts = np.linspace(a, b, n + 1)
        y_pts = x_pts ** 2

        fig = go.Figure()

        # Function curve
        fig.add_trace(go.Scatter(
            x=x_curve, y=y_curve,
            mode='lines',
            line={'color': '#00d4ff', 'width': 4},
            name='f(x) = x²',
        ))

        # Trapezoids
        for i in range(n):
            fig.add_trace(go.Scatter(
                x=[x_pts[i], x_pts[i], x_pts[i+1], x_pts[i+1], x_pts[i]],
                y=[0, y_pts[i], y_pts[i+1], 0, 0],
                fill='toself',
                fillcolor='rgba(255, 107, 107, 0.3)',
                line={'color': '#ff6b6b', 'width': 2},
                name='Trapezoid' if i == 0 else None,
                showlegend=(i == 0),
            ))

        # Points
        fig.add_trace(go.Scatter(
            x=x_pts, y=y_pts,
            mode='markers',
            marker={'color': '#ffe66d', 'size': 12},
            name='Sample points',
        ))

        # Calculate areas
        trap_area = dx * (0.5 * y_pts[0] + np.sum(y_pts[1:-1]) + 0.5 * y_pts[-1])
        exact_area = b**3 / 3

        fig.update_layout(
            paper_bgcolor='#16213e',
            plot_bgcolor='#1a1a2e',
            font={'color': '#eaeaea', 'family': 'JetBrains Mono, monospace'},
            title=f"Trapezoidal Rule (n={n}): Approx = {trap_area:.4f}, Exact = {exact_area:.4f}",
            xaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'title': 'x'},
            yaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'title': 'y'},
            showlegend=True,
            legend={'bgcolor': 'rgba(22, 33, 62, 0.8)', 'orientation': 'h', 'yanchor': 'bottom', 'y': -0.15, 'xanchor': 'center', 'x': 0.5},
        margin={'l': 40, 'r': 40, 't': 50, 'b': 80},
        )

        return fig

    _visualize_methods()
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        **What this shows:** This visualization displays the trapezoidal rule for numerical integration. The blue curve is $f(x) = x^2$, and the red trapezoids connect adjacent sample points with straight lines. The yellow dots mark where we sample the function. The area under the trapezoids approximates the integral.

        **The geometry of numerical integration:**

        The trapezoids (red) connect the sample points with straight lines.
        This captures the shape better than rectangles because it accounts for
        the function's slope.

        Simpson's rule goes further—it fits a parabola through every three
        consecutive points. Since $x^2$ is itself a parabola, Simpson's rule
        gives the **exact answer** for quadratic functions!
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Part VI: Applications of Integration

        ### Application 1: Computing Areas

        The most direct application—finding the area of regions bounded by curves.

        **Example**: Area between $y = x^2$ and $y = x$

        First, find where they intersect: $x^2 = x \Rightarrow x(x-1) = 0 \Rightarrow x = 0$ or $x = 1$

        Between these points, $x > x^2$ (the line is above the parabola), so:

        $$\begin{aligned}
        \text{Area} &= \int_0^1 (x - x^2) \, dx \\
        &= \left[ \frac{x^2}{2} - \frac{x^3}{3} \right]_0^1 \\
        &= \frac{1}{2} - \frac{1}{3} = \frac{1}{6}
        \end{aligned}$$
        """
    )
    return


@app.cell
def _(go, np):
    # Visualize area between curves
    _x = np.linspace(-0.2, 1.3, 200)
    _y1 = _x  # y = x
    _y2 = _x ** 2  # y = x²

    _x_fill = np.linspace(0, 1, 100)
    _y1_fill = _x_fill
    _y2_fill = _x_fill ** 2

    _fig = go.Figure()

    # Fill between curves
    _fig.add_trace(go.Scatter(
        x=np.concatenate([_x_fill, _x_fill[::-1]]),
        y=np.concatenate([_y1_fill, _y2_fill[::-1]]),
        fill='toself',
        fillcolor='rgba(78, 205, 196, 0.5)',
        line={'width': 0},
        name='Area = 1/6',
    ))

    # Curves
    _fig.add_trace(go.Scatter(x=_x, y=_y1, mode='lines', line={'color': '#ff6b6b', 'width': 3}, name='y = x'))
    _fig.add_trace(go.Scatter(x=_x, y=_y2, mode='lines', line={'color': '#00d4ff', 'width': 3}, name='y = x²'))

    # Intersection points
    _fig.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1],
        mode='markers',
        marker={'color': '#ffe66d', 'size': 12},
        name='Intersections',
    ))

    _fig.update_layout(
        paper_bgcolor='#16213e',
        plot_bgcolor='#1a1a2e',
        font={'color': '#eaeaea', 'family': 'JetBrains Mono, monospace'},
        title="Area Between y = x and y = x²",
        xaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'title': 'x'},
        yaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'title': 'y'},
        showlegend=True,
        legend={'bgcolor': 'rgba(22, 33, 62, 0.8)', 'orientation': 'h', 'yanchor': 'bottom', 'y': -0.15, 'xanchor': 'center', 'x': 0.5},
        margin={'l': 40, 'r': 40, 't': 50, 'b': 80},
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        **What this shows:** The shaded teal region represents the area trapped between two curves: the line $y = x$ (red) and the parabola $y = x^2$ (blue). The yellow dots mark where the curves intersect at $x = 0$ and $x = 1$. To find this area, we integrate the difference of the functions: $\int_0^1 (x - x^2) dx = \frac{1}{6}$.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Application 2: Physics — Work and Energy

        In physics, **work** is force times distance. But what if the force varies?

        $$W = \int_a^b F(x) \, dx$$

        **Example**: Stretching a spring

        Hooke's Law says the force needed to stretch a spring is $F(x) = kx$, where $k$ is
        the spring constant and $x$ is the displacement from equilibrium.

        The work to stretch a spring from $x = 0$ to $x = d$:

        $$W = \int_0^d kx \, dx = \left[ \frac{kx^2}{2} \right]_0^d = \frac{kd^2}{2}$$

        This is where the formula $E = \frac{1}{2}kx^2$ for elastic potential energy comes from!
        """
    )
    return


@app.cell
def _(go, np):
    # Visualize work done stretching a spring
    _k = 100  # Spring constant (N/m)
    _d = 0.5  # Stretch distance (m)

    _x = np.linspace(0, _d, 100)
    _F = _k * _x

    _fig = go.Figure()

    # Force curve with area
    _fig.add_trace(go.Scatter(
        x=np.concatenate([_x, _x[::-1]]),
        y=np.concatenate([_F, np.zeros_like(_F)]),
        fill='toself',
        fillcolor='rgba(255, 107, 107, 0.4)',
        line={'width': 0},
        name=f'Work = {0.5 * _k * _d**2:.1f} J',
    ))

    _fig.add_trace(go.Scatter(
        x=_x, y=_F,
        mode='lines',
        line={'color': '#ff6b6b', 'width': 3},
        name='F(x) = kx',
    ))

    _fig.update_layout(
        paper_bgcolor='#16213e',
        plot_bgcolor='#1a1a2e',
        font={'color': '#eaeaea', 'family': 'JetBrains Mono, monospace'},
        title=f"Work Done Stretching a Spring (k = {_k} N/m)",
        xaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'title': 'Displacement x (m)'},
        yaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'title': 'Force F (N)'},
        showlegend=True,
        legend={'bgcolor': 'rgba(22, 33, 62, 0.8)', 'orientation': 'h', 'yanchor': 'bottom', 'y': -0.15, 'xanchor': 'center', 'x': 0.5},
        margin={'l': 40, 'r': 40, 't': 50, 'b': 80},
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        **What this shows:** The red line represents the force required to stretch a spring as a function of displacement (Hooke's Law: $F = kx$). The shaded area under this line equals the work done—the energy stored in the spring. Since force increases linearly with displacement, the area is a triangle with area $\frac{1}{2} \times base \times height = \frac{1}{2}kd^2$.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Application 3: Probability — The Normal Distribution

        The **normal distribution** (bell curve) is ubiquitous in statistics. Its probability
        density function is:

        $$f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}$$

        where $\mu$ is the mean and $\sigma$ is the standard deviation.

        The probability of a value falling between $a$ and $b$ is:

        $$P(a < X < b) = \int_a^b f(x) \, dx$$

        This integral has **no closed form**! We must use numerical methods or tables.

        **The famous 68-95-99.7 rule:**
        - 68% of values fall within 1 standard deviation of the mean
        - 95% fall within 2 standard deviations
        - 99.7% fall within 3 standard deviations

        These percentages come from numerically evaluating the integral!
        """
    )
    return


@app.cell
def _(go, np, sci_integrate):
    # Visualize the normal distribution
    _mu = 0
    _sigma = 1

    def _normal_pdf(x, mu, sigma):
        return 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))

    _x = np.linspace(-4, 4, 300)
    _y = _normal_pdf(_x, _mu, _sigma)

    # Calculate probabilities
    _p_1sigma, _ = sci_integrate.quad(lambda x: _normal_pdf(x, _mu, _sigma), -1, 1)
    _p_2sigma, _ = sci_integrate.quad(lambda x: _normal_pdf(x, _mu, _sigma), -2, 2)
    _p_3sigma, _ = sci_integrate.quad(lambda x: _normal_pdf(x, _mu, _sigma), -3, 3)

    _fig = go.Figure()

    # Full curve
    _fig.add_trace(go.Scatter(
        x=_x, y=_y,
        mode='lines',
        line={'color': '#00d4ff', 'width': 3},
        name='Normal PDF',
    ))

    # 1 sigma region
    _x_1s = np.linspace(-1, 1, 100)
    _y_1s = _normal_pdf(_x_1s, _mu, _sigma)
    _fig.add_trace(go.Scatter(
        x=np.concatenate([_x_1s, _x_1s[::-1]]),
        y=np.concatenate([_y_1s, np.zeros_like(_y_1s)]),
        fill='toself',
        fillcolor='rgba(78, 205, 196, 0.6)',
        line={'width': 0},
        name=f'±1σ: {_p_1sigma*100:.1f}%',
    ))

    # 2 sigma region (extra parts)
    for _sign in [-1, 1]:
        _x_2s = np.linspace(_sign * 1, _sign * 2, 50)
        _y_2s = _normal_pdf(_x_2s, _mu, _sigma)
        _fig.add_trace(go.Scatter(
            x=np.concatenate([_x_2s, _x_2s[::-1]]),
            y=np.concatenate([_y_2s, np.zeros_like(_y_2s)]),
            fill='toself',
            fillcolor='rgba(255, 107, 107, 0.4)',
            line={'width': 0},
            name=f'±2σ region' if _sign == -1 else None,
            showlegend=(_sign == -1),
        ))

    _fig.add_annotation(x=0, y=0.2, text=f"68%", showarrow=False, font={'color': '#eaeaea', 'size': 16})
    _fig.add_annotation(x=1.5, y=0.08, text=f"13.5%", showarrow=False, font={'color': '#eaeaea', 'size': 12})
    _fig.add_annotation(x=-1.5, y=0.08, text=f"13.5%", showarrow=False, font={'color': '#eaeaea', 'size': 12})

    _fig.update_layout(
        paper_bgcolor='#16213e',
        plot_bgcolor='#1a1a2e',
        font={'color': '#eaeaea', 'family': 'JetBrains Mono, monospace'},
        title="Standard Normal Distribution: The 68-95-99.7 Rule",
        xaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'title': 'x (standard deviations from mean)'},
        yaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'title': 'Probability density'},
        showlegend=True,
        legend={'bgcolor': 'rgba(22, 33, 62, 0.8)', 'orientation': 'h', 'yanchor': 'bottom', 'y': -0.15, 'xanchor': 'center', 'x': 0.5},
        margin={'l': 40, 'r': 40, 't': 50, 'b': 80},
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        **What this shows:** The bell curve displays the probability density function of the normal distribution. The area under any portion of the curve equals the probability of a random value falling in that range. The shaded regions visualize the famous 68-95-99.7 rule.

        **Understanding the visualization:**

        - The **teal region** covers ±1 standard deviation from the mean, containing 68% of the probability
        - The **red regions** extend to ±2 standard deviations, adding another ~27% (total 95%)
        - The remaining 5% is in the tails beyond ±2σ

        This is why statisticians use 2 standard deviations as a common threshold for
        "statistical significance"—only 5% of random variation falls that far from the mean.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Application 4: Computing Volumes

        Integration extends to 3D through **volumes of revolution**. If you rotate a curve
        around an axis, you can compute the resulting volume using integration.

        **Disk Method**: Rotating $y = f(x)$ around the x-axis from $a$ to $b$:

        $$V = \pi \int_a^b [f(x)]^2 \, dx$$

        Each cross-section is a disk with radius $f(x)$, so area $\pi[f(x)]^2$.

        **Example**: Volume of a cone

        A cone can be generated by rotating the line $y = \frac{r}{h}x$ around the x-axis
        from $x = 0$ to $x = h$:

        $$\begin{aligned}
        V &= \pi \int_0^h \left(\frac{r}{h}x\right)^2 dx \\
        &= \pi \frac{r^2}{h^2} \int_0^h x^2 \, dx \\
        &= \pi \frac{r^2}{h^2} \cdot \frac{h^3}{3} \\
        &= \frac{\pi r^2 h}{3}
        \end{aligned}$$

        This is the familiar formula: Volume of cone = $\frac{1}{3} \times$ base area $\times$ height!
        """
    )
    return


@app.cell
def _(go, np):
    # Visualize volume of revolution
    _h = 3  # height
    _r = 1  # base radius

    # The line y = (r/h)x
    _x_line = np.linspace(0, _h, 50)
    _y_line = (_r / _h) * _x_line

    # Create the cone surface
    _theta = np.linspace(0, 2 * np.pi, 50)
    _X, _THETA = np.meshgrid(_x_line, _theta)
    _R = (_r / _h) * _X
    _Y = _R * np.cos(_THETA)
    _Z = _R * np.sin(_THETA)

    _fig = go.Figure()

    # Cone surface
    _fig.add_trace(go.Surface(
        x=_X, y=_Y, z=_Z,
        colorscale=[[0, '#00d4ff'], [1, '#4ecdc4']],
        showscale=False,
        opacity=0.8,
        name='Cone',
    ))

    # The generating line
    _fig.add_trace(go.Scatter3d(
        x=_x_line, y=_y_line, z=np.zeros_like(_x_line),
        mode='lines',
        line={'color': '#ff6b6b', 'width': 6},
        name='y = (r/h)x',
    ))

    _volume = np.pi * _r**2 * _h / 3

    _fig.update_layout(
        paper_bgcolor='#16213e',
        plot_bgcolor='#1a1a2e',
        font={'color': '#eaeaea', 'family': 'JetBrains Mono, monospace'},
        title=f"Cone from y = (r/h)x rotated about x-axis | V = πr²h/3 = {_volume:.3f}",
        scene=dict(
            xaxis={'backgroundcolor': '#1a1a2e', 'gridcolor': '#2d3a4f', 'title': 'x'},
            yaxis={'backgroundcolor': '#1a1a2e', 'gridcolor': '#2d3a4f', 'title': 'y'},
            zaxis={'backgroundcolor': '#1a1a2e', 'gridcolor': '#2d3a4f', 'title': 'z'},
            bgcolor='#1a1a2e',
        ),
        showlegend=True,
        legend={'bgcolor': 'rgba(22, 33, 62, 0.8)', 'orientation': 'h', 'yanchor': 'bottom', 'y': -0.15, 'xanchor': 'center', 'x': 0.5},
        margin={'l': 40, 'r': 40, 't': 50, 'b': 80},
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        **What this shows:** This 3D surface represents a cone created by rotating a straight line around the x-axis. The disk method computes the volume by integrating the areas of circular cross-sections—each thin slice is a disk whose radius depends on position along the axis.

        **The 3D visualization shows:**

        - The **red line** is the generating curve $y = \frac{r}{h}x$
        - When rotated around the x-axis, it sweeps out a **cone**
        - The integral sums up all the infinitesimally thin circular disks

        You can drag to rotate the view and see the cone from different angles.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Part VII: Monte Carlo Integration

        ### When All Else Fails: Random Sampling

        For very complex integrals, especially in high dimensions, traditional numerical
        methods become impractical. **Monte Carlo integration** offers a powerful alternative:
        use random sampling!

        **The idea:**
        1. Generate random points uniformly in a region containing the area of interest
        2. Count how many points fall under the curve
        3. The integral is approximately (fraction under curve) × (total region area)

        **Why it works:** By the Law of Large Numbers, the fraction of random points in a
        region converges to the region's area as a fraction of the whole.

        ### Example: Estimating π

        Consider a quarter circle of radius 1 inscribed in a unit square.
        - Square area = 1
        - Quarter circle area = $\frac{\pi}{4}$

        If we throw random darts at the square:
        $$\frac{\text{darts in circle}}{\text{total darts}} \approx \frac{\pi/4}{1} = \frac{\pi}{4}$$

        Therefore: $\pi \approx 4 \times \frac{\text{darts in circle}}{\text{total darts}}$
        """
    )
    return


@app.cell
def _(mo):
    n_points_slider = mo.ui.slider(
        start=100, stop=10000, step=100, value=1000,
        label="Number of random points:",
        show_value=True,
    )
    return n_points_slider,


@app.cell
def _(mo, n_points_slider):
    mo.hstack([
        mo.md("### Monte Carlo Estimation of π"),
        n_points_slider,
    ])
    return


@app.cell
def _(go, np, n_points_slider):
    np.random.seed(42)  # For reproducibility
    _n = n_points_slider.value

    # Generate random points
    _x = np.random.uniform(0, 1, _n)
    _y = np.random.uniform(0, 1, _n)

    # Check if inside quarter circle
    _inside = _x**2 + _y**2 <= 1
    _n_inside = np.sum(_inside)
    _pi_estimate = 4 * _n_inside / _n

    # Quarter circle curve
    _theta = np.linspace(0, np.pi/2, 100)
    _circle_x = np.cos(_theta)
    _circle_y = np.sin(_theta)

    _fig = go.Figure()

    # Points outside
    _fig.add_trace(go.Scatter(
        x=_x[~_inside], y=_y[~_inside],
        mode='markers',
        marker={'color': '#ff6b6b', 'size': 3, 'opacity': 0.5},
        name=f'Outside: {_n - _n_inside}',
    ))

    # Points inside
    _fig.add_trace(go.Scatter(
        x=_x[_inside], y=_y[_inside],
        mode='markers',
        marker={'color': '#4ecdc4', 'size': 3, 'opacity': 0.5},
        name=f'Inside: {_n_inside}',
    ))

    # Quarter circle
    _fig.add_trace(go.Scatter(
        x=_circle_x, y=_circle_y,
        mode='lines',
        line={'color': '#00d4ff', 'width': 3},
        name='Quarter circle',
    ))

    _error = abs(_pi_estimate - np.pi) / np.pi * 100

    _fig.update_layout(
        paper_bgcolor='#16213e',
        plot_bgcolor='#1a1a2e',
        font={'color': '#eaeaea', 'family': 'JetBrains Mono, monospace'},
        title=f"π ≈ 4 × {_n_inside}/{_n} = {_pi_estimate:.6f} | True π = {np.pi:.6f} | Error: {_error:.2f}%",
        xaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'scaleanchor': 'y', 'range': [-0.05, 1.05]},
        yaxis={'gridcolor': '#2d3a4f', 'zerolinecolor': '#a0a0a0', 'range': [-0.05, 1.05]},
        showlegend=True,
        legend={'bgcolor': 'rgba(22, 33, 62, 0.8)', 'orientation': 'h', 'yanchor': 'bottom', 'y': -0.15, 'xanchor': 'center', 'x': 0.5},
        margin={'l': 40, 'r': 40, 't': 50, 'b': 80},
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        **What this shows:** Random points are scattered uniformly across the unit square. Points inside the quarter circle (teal) and outside (red) are colored differently. The ratio of points inside to total points approximates $\pi/4$, since the quarter circle has area $\pi/4$ within the unit square.

        **Experiment with the slider:**

        - With 100 points, the estimate varies wildly (high variance)
        - With 1000 points, we're typically within 2-3% of π
        - With 10000 points, we're usually within 1%

        **Monte Carlo error** decreases as $O(1/\sqrt{n})$—to halve the error, you need
        4× as many points. This is slower than Simpson's rule for low dimensions, but
        Monte Carlo **doesn't get worse** as dimensions increase!

        For a 10-dimensional integral, Simpson's rule would need billions of points,
        while Monte Carlo still works with thousands. This is why Monte Carlo methods
        are essential in physics, finance, and machine learning.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Summary

        We've traced the development of integration from ancient geometry to modern computation:

        ### The Core Ideas

        1. **The Problem**: How to find areas and accumulated quantities

        2. **Ancient Methods**: Method of exhaustion (Archimedes), indivisibles (Cavalieri)

        3. **The Breakthrough**: The Fundamental Theorem of Calculus
           $$\int_a^b f(x) \, dx = F(b) - F(a) \text{ where } F'(x) = f(x)$$

        4. **Numerical Methods**: When antiderivatives don't exist
           - Rectangle/Trapezoid rules: $O(1/n^2)$ error
           - Simpson's rule: $O(1/n^4)$ error
           - Monte Carlo: $O(1/\sqrt{n})$ error, but scales to high dimensions

        5. **Applications**:
           - Area between curves
           - Work and energy in physics
           - Probability distributions
           - Volumes of revolution

        ### The Big Picture

        Integration answers the question: **What is the total?**

        - Total area under a curve
        - Total distance traveled (integral of velocity)
        - Total work done (integral of force)
        - Total probability (integral of density)

        Together with differentiation, integration forms the complete toolkit of calculus—
        the mathematics of change and accumulation that underlies all of modern science.

        ---

        ## Further Resources

        ### Video Series
        - [3Blue1Brown: Integration and the Fundamental Theorem](https://www.youtube.com/watch?v=rfG8ce4nNh0)
        - [Khan Academy: Integral Calculus](https://www.khanacademy.org/math/integral-calculus)

        ### Books
        - Stewart, *Calculus: Early Transcendentals*, Chapters 5-8
        - Strang, *Calculus* (free at MIT OpenCourseWare)

        ### Historical Sources
        - [Archimedes' Works](https://www.math.ubc.ca/~cass/archimedes/)
        - [The History of the Calculus](https://mathshistory.st-andrews.ac.uk/HistTopics/The_rise_of_calculus/)
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        *"Nature laughs at the difficulties of integration."*
        — Pierre-Simon Laplace

        (But thanks to numerical methods, we can laugh along with her!)
        """
    )
    return


if __name__ == "__main__":
    app.run()
