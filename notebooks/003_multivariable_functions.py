"""
Multivariable Functions: From Flat Maps to Mountain Landscapes

An exploration of functions with multiple variables,
their geometric meaning, partial derivatives, and multiple integrals.
"""

import marimo

__generated_with = "0.19.6"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
        # Multivariable Functions: From Flat Maps to Mountain Landscapes

        *"The book of nature is written in the language of mathematics, and its characters
        are triangles, circles, and other geometric figures."* — Galileo Galilei

        ---

        In our previous explorations, we studied functions of a single variable: $f(x)$.
        These describe quantities that depend on just one input—the height of a ball
        depending on time, or the temperature depending on position along a rod.

        But the real world is richer. Temperature varies across a *surface*, not just a line.
        The pressure in the atmosphere depends on both latitude and altitude. The gravitational
        potential at any point in space depends on three coordinates.

        **Welcome to the world of multivariable functions.**

        In this notebook, we'll explore:
        - **Functions of two variables**: $f(x, y)$ — surfaces in 3D space
        - **Partial derivatives**: How functions change in each direction
        - **The gradient**: The direction of steepest ascent
        - **Multiple integrals**: Computing volumes and more
        - **Applications**: From heat flow to optimization
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The Historical Journey: Why Multiple Variables?

        ### The 18th Century Revolution

        The study of functions with multiple variables emerged from the practical needs of
        **physics and engineering** in the 18th century. As scientists tackled increasingly
        complex problems, single-variable calculus proved insufficient.

        **Leonhard Euler (1707-1783)** was among the first to systematically study functions
        of several variables. Working in St. Petersburg and Berlin, Euler developed much of
        the notation and techniques we still use today. He introduced the concept of
        **partial derivatives** and applied them to problems in mechanics and fluid flow.

        **Joseph-Louis Lagrange (1736-1813)** took these ideas further, developing the
        **calculus of variations**—finding functions that optimize certain quantities. His work
        on mechanics led to the Lagrangian formulation of physics, which remains central to
        modern theoretical physics.

        **Pierre-Simon Laplace (1749-1827)** applied multivariable calculus to celestial
        mechanics and probability theory. The famous **Laplace equation** $\nabla^2 f = 0$
        describes everything from gravitational potentials to steady-state heat distribution.

        ### The Physical Motivation

        Why did these mathematicians need multiple variables? Consider these physical problems:

        | Problem | Variables | Function |
        |---------|-----------|----------|
        | Temperature in a plate | Position $(x, y)$ | $T(x, y)$ |
        | Gravitational potential | Position $(x, y, z)$ | $\phi(x, y, z)$ |
        | Air pressure | Latitude, altitude | $P(\theta, h)$ |
        | Wave amplitude | Position, time | $u(x, t)$ |

        The mathematics of multiple variables wasn't abstract curiosity—it was **essential
        for understanding the physical world**.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What is a Function of Two Variables?

        A function $f(x, y)$ takes **two inputs** and produces **one output**:

        $$f: \mathbb{R}^2 \to \mathbb{R}$$

        For each point $(x, y)$ in the plane, $f(x, y)$ gives us a height. The collection
        of all points $(x, y, f(x, y))$ forms a **surface** in three-dimensional space.

        Think of it like a **topographical map**:
        - The $(x, y)$ plane is the map (like looking down at terrain from above)
        - The value $f(x, y)$ is the elevation at each point
        - The surface is the actual terrain itself

        ### Examples of Multivariable Functions

        | Function | Formula | Shape |
        |----------|---------|-------|
        | Paraboloid | $f(x,y) = x^2 + y^2$ | Bowl opening upward |
        | Saddle | $f(x,y) = x^2 - y^2$ | Horse saddle shape |
        | Plane | $f(x,y) = ax + by + c$ | Flat tilted surface |
        | Gaussian | $f(x,y) = e^{-(x^2+y^2)}$ | Bell curve in 2D |
        | Ripples | $f(x,y) = \sin(3\sqrt{x^2+y^2})$ | Circular waves |

        Let's visualize these surfaces to build intuition.
        """
    )
    return


@app.cell
def _():
    import numpy as np
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    return go, make_subplots, np


@app.cell
def _(mo):
    # Surface selector
    surface_selector = mo.ui.dropdown(
        options={
            "Paraboloid: x² + y²": "paraboloid",
            "Saddle: x² - y²": "saddle",
            "Gaussian: e^(-(x²+y²))": "gaussian",
            "Ripples: sin(3√(x²+y²))": "ripples",
            "Plane: x + y": "plane",
            "Monkey Saddle: x³ - 3xy²": "monkey_saddle",
        },
        value="Paraboloid: x² + y²",
        label="Select a surface to explore:",
    )
    return (surface_selector,)


@app.cell
def _(mo, surface_selector):
    mo.md(
        f"""
        ### Interactive Surface Explorer

        {surface_selector}

        Use the dropdown above to explore different types of surfaces. Each surface has
        unique geometric properties that we'll analyze throughout this notebook.
        """
    )
    return


@app.cell
def _(go, np, surface_selector):
    # Create meshgrid
    _x = np.linspace(-2, 2, 50)
    _y = np.linspace(-2, 2, 50)
    _X, _Y = np.meshgrid(_x, _y)

    # Define surfaces
    _surfaces = {
        "paraboloid": (_X**2 + _Y**2, "Bowl Shape (Paraboloid)", "x² + y²"),
        "saddle": (_X**2 - _Y**2, "Saddle Point", "x² - y²"),
        "gaussian": (np.exp(-(_X**2 + _Y**2)), "Gaussian Bell", "e^(-(x²+y²))"),
        "ripples": (np.sin(np.sqrt(_X**2 + _Y**2 + 0.01) * 3), "Circular Ripples", "sin(3√(x²+y²))"),
        "plane": (_X + _Y, "Inclined Plane", "x + y"),
        "monkey_saddle": (_X**3 - 3*_X*_Y**2, "Monkey Saddle", "x³ - 3xy²"),
    }

    _selected = surface_selector.value
    _Z, _title, _formula = _surfaces[_selected]

    _fig = go.Figure(data=[
        go.Surface(
            x=_X, y=_Y, z=_Z,
            colorscale="Viridis",
            showscale=True,
            colorbar=dict(title=dict(text="f(x,y)", font=dict(color="#a0a0a0")), tickfont=dict(color="#a0a0a0")),
        )
    ])

    _fig.update_layout(
        title=dict(text=f"{_title}: f(x,y) = {_formula}", font=dict(color="#eaeaea")),
        scene=dict(
            xaxis=dict(title=dict(text="x", font=dict(color="#a0a0a0")), backgroundcolor="#1a1a2e", gridcolor="#2d3a4f"),
            yaxis=dict(title=dict(text="y", font=dict(color="#a0a0a0")), backgroundcolor="#1a1a2e", gridcolor="#2d3a4f"),
            zaxis=dict(title=dict(text="f(x,y)", font=dict(color="#a0a0a0")), backgroundcolor="#1a1a2e", gridcolor="#2d3a4f"),
            bgcolor="#1a1a2e",
        ),
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#1a1a2e",
        height=500,
        margin=dict(l=0, r=0, t=40, b=0),
    )
    _fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Understanding the Visualization

        This 3D surface displays a function of two variables. The horizontal $(x, y)$ plane represents all possible inputs, while the height at each point shows the output $f(x, y)$. Colors indicate elevation—purple regions are low values, yellow regions are high values.

        **What you're seeing:**
        - The horizontal plane represents all possible $(x, y)$ inputs
        - The height at each point shows the function value $f(x, y)$
        - Colors indicate elevation (purple = low, yellow = high)

        **Key observations for each surface:**
        - **Paraboloid**: Has a single minimum at the origin—like a bowl
        - **Saddle**: Curves up in one direction, down in another—a "pass" between mountains
        - **Gaussian**: A smooth bump, common in probability and physics
        - **Ripples**: Shows how radial distance creates wave patterns
        - **Monkey Saddle**: Has *three* "legs" instead of two—enough for a monkey's tail!

        These surfaces aren't just mathematical curiosities. The paraboloid describes
        the potential energy of a spring in 2D. The saddle point appears in optimization
        and game theory. The Gaussian is fundamental to statistics and quantum mechanics.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Contour Maps: A Bird's Eye View

        Another way to visualize $f(x, y)$ is through **contour maps** (also called
        **level curves**). These are the curves where $f(x, y) = c$ for various constants $c$.

        If you've ever read a topographical map, you've seen contour lines. Each line
        represents a constant elevation. Where lines are **close together**, the terrain
        is **steep**. Where they're **far apart**, the terrain is **gentle**.

        Contour maps were first systematically used by **Edmund Halley** (of comet fame)
        in 1701 to show magnetic declination across the Atlantic Ocean. The technique was
        later adopted for showing elevation and has become essential in cartography,
        meteorology (isobars for pressure), and physics (equipotential lines).

        ### The Mathematics of Level Curves

        A level curve is defined by:
        $$f(x, y) = c$$

        This implicit equation defines a curve in the $(x, y)$ plane. For example:
        - For $f(x,y) = x^2 + y^2$, level curves are circles $x^2 + y^2 = c$
        - For $f(x,y) = x^2 - y^2$, level curves are hyperbolas $x^2 - y^2 = c$
        """
    )
    return


@app.cell
def _(go, np, surface_selector):
    # Create contour plot for selected surface
    _x = np.linspace(-2, 2, 100)
    _y = np.linspace(-2, 2, 100)
    _X, _Y = np.meshgrid(_x, _y)

    _surfaces = {
        "paraboloid": (_X**2 + _Y**2, "Paraboloid Contours"),
        "saddle": (_X**2 - _Y**2, "Saddle Point Contours"),
        "gaussian": (np.exp(-(_X**2 + _Y**2)), "Gaussian Contours"),
        "ripples": (np.sin(np.sqrt(_X**2 + _Y**2 + 0.01) * 3), "Ripple Contours"),
        "plane": (_X + _Y, "Plane Contours"),
        "monkey_saddle": (_X**3 - 3*_X*_Y**2, "Monkey Saddle Contours"),
    }

    _selected = surface_selector.value
    _Z, _title = _surfaces[_selected]

    _fig_contour = go.Figure(data=[
        go.Contour(
            x=_x, y=_y, z=_Z,
            colorscale="Viridis",
            contours=dict(
                showlabels=True,
                labelfont=dict(size=10, color="white"),
            ),
            colorbar=dict(title=dict(text="f(x,y)", font=dict(color="#a0a0a0")), tickfont=dict(color="#a0a0a0")),
        )
    ])

    _fig_contour.update_layout(
        title=dict(text=_title, font=dict(color="#eaeaea")),
        xaxis=dict(title=dict(text="x", font=dict(color="#a0a0a0")), gridcolor="#2d3a4f", zerolinecolor="#4a5568", tickfont=dict(color="#a0a0a0")),
        yaxis=dict(title=dict(text="y", font=dict(color="#a0a0a0")), gridcolor="#2d3a4f", zerolinecolor="#4a5568", tickfont=dict(color="#a0a0a0"), scaleanchor="x"),
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#1a1a2e",
        height=450,
    )
    _fig_contour
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Reading the Contour Map

        This is a bird's-eye view of the surface, showing level curves (contour lines) where the function has constant values. Each labeled curve represents all $(x, y)$ points where $f(x, y)$ equals that particular value—like elevation lines on a topographic map.

        **What the contour map tells us:**
        - **Concentric circles** (paraboloid): The function increases uniformly in all directions
        - **Hyperbolas** (saddle): The function increases in one direction, decreases in another
        - **Parallel lines** (plane): The function changes at a constant rate
        - **Closely spaced lines**: Steep gradient (rapid change)
        - **Widely spaced lines**: Gentle gradient (slow change)

        **Physical intuition**: Imagine pouring water on the surface. Water flows
        perpendicular to contour lines, always heading downhill. This perpendicular
        direction is the **gradient**—which we'll explore soon.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Partial Derivatives: Measuring Change in Each Direction

        ### The Fundamental Question

        For a function of one variable, the derivative $\frac{df}{dx}$ tells us the rate
        of change. But for $f(x, y)$, change depends on **which direction** we move!

        - Moving in the $x$-direction while keeping $y$ fixed
        - Moving in the $y$-direction while keeping $x$ fixed
        - Moving diagonally
        - Moving in any arbitrary direction

        **Partial derivatives** handle the first two cases. They measure the rate of change
        in one variable while treating all other variables as constants.

        ### Definition of Partial Derivatives

        The **partial derivative with respect to $x$**:
        $$\frac{\partial f}{\partial x} = \lim_{h \to 0} \frac{f(x+h, y) - f(x, y)}{h}$$

        The **partial derivative with respect to $y$**:
        $$\frac{\partial f}{\partial y} = \lim_{h \to 0} \frac{f(x, y+h) - f(x, y)}{h}$$

        The symbol $\partial$ (called "partial" or "curly d") was introduced by **Adrien-Marie
        Legendre** in 1786, though the concept was developed earlier by Euler and others.

        ### Computing Partial Derivatives

        To find $\frac{\partial f}{\partial x}$:
        1. Treat $y$ as a constant
        2. Differentiate with respect to $x$ using normal rules

        **Example**: For $f(x, y) = x^2 y + \sin(y)$:
        - $\frac{\partial f}{\partial x} = 2xy$ (treating $y$ as constant)
        - $\frac{\partial f}{\partial y} = x^2 + \cos(y)$ (treating $x$ as constant)
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Geometric Interpretation

        The partial derivative $\frac{\partial f}{\partial x}$ at a point $(a, b)$ is the
        **slope of the tangent line** to the surface in the $x$-direction.

        Imagine slicing the surface with a vertical plane parallel to the $xz$-plane
        (keeping $y = b$ constant). You get a curve. The partial derivative is the slope
        of this curve at $x = a$.

        Similarly, $\frac{\partial f}{\partial y}$ is the slope when slicing parallel to
        the $yz$-plane.

        Let's visualize this by showing the tangent plane at a point on our surface.
        """
    )
    return


@app.cell
def _(mo):
    # Point selector for tangent plane
    point_x_slider = mo.ui.slider(
        start=-1.5, stop=1.5, step=0.1, value=0.5, label="x₀"
    )
    point_y_slider = mo.ui.slider(
        start=-1.5, stop=1.5, step=0.1, value=0.5, label="y₀"
    )
    return point_x_slider, point_y_slider


@app.cell
def _(mo, point_x_slider, point_y_slider):
    mo.md(
        f"""
        ### Interactive Tangent Plane Visualization

        Adjust the point $(x_0, y_0)$ to see how the tangent plane changes:

        **Point coordinates:** {point_x_slider} {point_y_slider}

        The tangent plane at $(x_0, y_0)$ is given by:
        $$z = f(x_0, y_0) + \\frac{{\\partial f}}{{\\partial x}}(x - x_0) + \\frac{{\\partial f}}{{\\partial y}}(y - y_0)$$
        """
    )
    return


@app.cell
def _(go, np, point_x_slider, point_y_slider):
    # Visualize tangent plane for paraboloid f(x,y) = x² + y²
    _x = np.linspace(-2, 2, 40)
    _y = np.linspace(-2, 2, 40)
    _X, _Y = np.meshgrid(_x, _y)
    _Z = _X**2 + _Y**2  # Paraboloid

    # Point of tangency
    _x0 = point_x_slider.value
    _y0 = point_y_slider.value
    _z0 = _x0**2 + _y0**2

    # Partial derivatives at the point
    _fx = 2 * _x0  # ∂f/∂x = 2x
    _fy = 2 * _y0  # ∂f/∂y = 2y

    # Tangent plane: z = z0 + fx*(x-x0) + fy*(y-y0)
    _x_plane = np.linspace(_x0 - 1, _x0 + 1, 20)
    _y_plane = np.linspace(_y0 - 1, _y0 + 1, 20)
    _Xp, _Yp = np.meshgrid(_x_plane, _y_plane)
    _Zp = _z0 + _fx * (_Xp - _x0) + _fy * (_Yp - _y0)

    _fig_tangent = go.Figure()

    # Surface
    _fig_tangent.add_trace(go.Surface(
        x=_X, y=_Y, z=_Z,
        colorscale="Viridis",
        opacity=0.8,
        showscale=False,
        name="Surface",
    ))

    # Tangent plane
    _fig_tangent.add_trace(go.Surface(
        x=_Xp, y=_Yp, z=_Zp,
        colorscale=[[0, "#ff6b6b"], [1, "#ff6b6b"]],
        opacity=0.6,
        showscale=False,
        name="Tangent Plane",
    ))

    # Point of tangency
    _fig_tangent.add_trace(go.Scatter3d(
        x=[_x0], y=[_y0], z=[_z0],
        mode="markers",
        marker=dict(size=8, color="#00d4ff"),
        name="Point",
    ))

    _fig_tangent.update_layout(
        title=dict(
            text=f"Tangent Plane at ({_x0:.1f}, {_y0:.1f}) | ∂f/∂x = {_fx:.2f}, ∂f/∂y = {_fy:.2f}",
            font=dict(color="#eaeaea"),
        ),
        scene=dict(
            xaxis=dict(title=dict(text="x", font=dict(color="#a0a0a0")), backgroundcolor="#1a1a2e", gridcolor="#2d3a4f"),
            yaxis=dict(title=dict(text="y", font=dict(color="#a0a0a0")), backgroundcolor="#1a1a2e", gridcolor="#2d3a4f"),
            zaxis=dict(title=dict(text="f(x,y)", font=dict(color="#a0a0a0")), backgroundcolor="#1a1a2e", gridcolor="#2d3a4f"),
            bgcolor="#1a1a2e",
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.2)),
        ),
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#1a1a2e",
        height=500,
        showlegend=False,
        margin=dict(l=0, r=0, t=40, b=0),
    )
    _fig_tangent
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### What the Visualization Shows

        - **Blue surface**: The paraboloid $f(x, y) = x^2 + y^2$
        - **Red plane**: The tangent plane at the selected point
        - **Cyan dot**: The point of tangency

        **Observe how:**
        - At the origin $(0, 0)$, the tangent plane is horizontal (both partial derivatives are zero)
        - As you move away from the origin, the plane tilts more steeply
        - The partial derivatives $\frac{\partial f}{\partial x} = 2x$ and $\frac{\partial f}{\partial y} = 2y$
          determine how much the plane tilts in each direction

        The tangent plane is the **best linear approximation** to the surface near the point—
        just as the tangent line was the best linear approximation to a curve.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The Gradient: The Direction of Steepest Ascent

        ### Combining Partial Derivatives

        The partial derivatives tell us rates of change in the $x$ and $y$ directions.
        But what about other directions? And which direction gives the **fastest** change?

        The answer is the **gradient**, denoted $\nabla f$ (read "del f" or "grad f"):

        $$\nabla f = \left( \frac{\partial f}{\partial x}, \frac{\partial f}{\partial y} \right)$$

        The gradient is a **vector** that:
        1. **Points in the direction of steepest ascent**
        2. **Has magnitude equal to the rate of change in that direction**

        ### Physical Intuition

        Imagine you're standing on a hillside and want to climb as steeply as possible.
        The gradient vector points exactly in that direction. Its length tells you how
        steep the climb will be.

        Conversely, $-\nabla f$ points **downhill**—the direction water would flow.

        ### The Gradient and Contour Lines

        A beautiful fact: **the gradient is always perpendicular to level curves**.

        Why? Because level curves are lines of constant $f$. Moving along a level curve,
        $f$ doesn't change. The direction of maximum change must be perpendicular to this.

        This is why water flows perpendicular to contour lines on a map—it follows $-\nabla f$.
        """
    )
    return


@app.cell
def _(go, np):
    # Visualize gradient field on contour plot
    _x = np.linspace(-2, 2, 100)
    _y = np.linspace(-2, 2, 100)
    _X, _Y = np.meshgrid(_x, _y)
    _Z = _X**2 + _Y**2  # Paraboloid

    # Gradient vectors (computed on coarser grid)
    _xg = np.linspace(-1.8, 1.8, 8)
    _yg = np.linspace(-1.8, 1.8, 8)
    _Xg, _Yg = np.meshgrid(_xg, _yg)
    _U = 2 * _Xg  # ∂f/∂x
    _V = 2 * _Yg  # ∂f/∂y

    # Normalize for display
    _mag = np.sqrt(_U**2 + _V**2) + 0.01
    _U_norm = _U / _mag * 0.3
    _V_norm = _V / _mag * 0.3

    _fig_grad = go.Figure()

    # Contours
    _fig_grad.add_trace(go.Contour(
        x=_x, y=_y, z=_Z,
        colorscale="Viridis",
        contours=dict(showlabels=True, labelfont=dict(size=10, color="white")),
        showscale=False,
    ))

    # Gradient arrows using annotations (Plotly doesn't have built-in quiver)
    for _i in range(len(_xg)):
        for _j in range(len(_yg)):
            if _mag[_j, _i] > 0.1:  # Skip very small vectors
                _fig_grad.add_annotation(
                    x=_Xg[_j, _i] + _U_norm[_j, _i],
                    y=_Yg[_j, _i] + _V_norm[_j, _i],
                    ax=_Xg[_j, _i],
                    ay=_Yg[_j, _i],
                    xref="x", yref="y",
                    axref="x", ayref="y",
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1.5,
                    arrowwidth=2,
                    arrowcolor="#ff6b6b",
                )

    _fig_grad.update_layout(
        title=dict(text="Gradient Field ∇f for f(x,y) = x² + y²", font=dict(color="#eaeaea")),
        xaxis=dict(title=dict(text="x", font=dict(color="#a0a0a0")), gridcolor="#2d3a4f", zerolinecolor="#4a5568", range=[-2.2, 2.2], tickfont=dict(color="#a0a0a0")),
        yaxis=dict(title=dict(text="y", font=dict(color="#a0a0a0")), gridcolor="#2d3a4f", zerolinecolor="#4a5568", range=[-2.2, 2.2], scaleanchor="x", tickfont=dict(color="#a0a0a0")),
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#1a1a2e",
        height=500,
    )
    _fig_grad
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Reading the Gradient Field

        The red arrows represent the gradient vector $\nabla f$ at each point, overlaid on the contour map. Each arrow points in the direction of steepest ascent (where the function increases fastest), and its length indicates how steep that climb is. Notice how arrows always point perpendicular to the contour lines.

        The red arrows show the gradient $\nabla f = (2x, 2y)$ at various points:

        - **At the origin**: The gradient is zero (the minimum of the bowl)
        - **Away from origin**: Arrows point outward, away from the minimum
        - **Arrow direction**: Perpendicular to the circular contour lines
        - **Arrow length**: Longer arrows where contours are closer (steeper regions)

        **Physical interpretation**: If this surface represented a potential energy landscape,
        objects would roll in the direction of $-\nabla f$ (downhill, toward the origin).

        ### Applications of the Gradient

        | Field | Application |
        |-------|-------------|
        | Physics | Force = $-\nabla V$ (potential energy) |
        | Machine Learning | Gradient descent optimization |
        | Fluid Dynamics | Flow direction in potential flow |
        | Image Processing | Edge detection (high gradient = edge) |
        | Economics | Direction of maximum utility increase |
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The Saddle Point: Where Calculus Gets Interesting

        ### A Critical Point That's Not an Extremum

        For functions of one variable, if $f'(x) = 0$, we have either a maximum, minimum,
        or inflection point. For functions of multiple variables, the situation is richer.

        Consider the **saddle function** $f(x, y) = x^2 - y^2$:

        - $\frac{\partial f}{\partial x} = 2x = 0$ at $x = 0$
        - $\frac{\partial f}{\partial y} = -2y = 0$ at $y = 0$

        So both partial derivatives are zero at the origin—it's a **critical point**. But:
        - Moving in the $x$-direction: $f(x, 0) = x^2$ has a **minimum**
        - Moving in the $y$-direction: $f(0, y) = -y^2$ has a **maximum**

        This is a **saddle point**—neither a maximum nor a minimum. It looks like a
        mountain pass between two peaks.

        ### The Second Derivative Test (2D Version)

        To classify critical points, we use the **Hessian matrix**:

        $$H = \begin{pmatrix} f_{xx} & f_{xy} \\ f_{yx} & f_{yy} \end{pmatrix}$$

        The **discriminant** is $D = f_{xx} \cdot f_{yy} - (f_{xy})^2$:
        - $D > 0$ and $f_{xx} > 0$: **Local minimum**
        - $D > 0$ and $f_{xx} < 0$: **Local maximum**
        - $D < 0$: **Saddle point**
        - $D = 0$: Test inconclusive
        """
    )
    return


@app.cell
def _(go, np):
    # Animated saddle point visualization
    _x = np.linspace(-2, 2, 30)  # Reduced resolution for smaller file size
    _y = np.linspace(-2, 2, 30)
    _X, _Y = np.meshgrid(_x, _y)
    _Z = _X**2 - _Y**2

    # Create slices through the saddle - only animate the slice, not the surface
    _frames = []
    _angles = np.linspace(0, 2*np.pi, 30)  # Reduced frames for smaller file size

    for _angle in _angles:
        # Slice along direction at angle
        _t = np.linspace(-2, 2, 50)
        _slice_x = _t * np.cos(_angle)
        _slice_y = _t * np.sin(_angle)
        _slice_z = _slice_x**2 - _slice_y**2

        # Only include the changing traces in frames (not the static surface)
        _frames.append(go.Frame(
            data=[
                go.Scatter3d(
                    x=_slice_x, y=_slice_y, z=_slice_z,
                    mode="lines",
                    line=dict(color="#00d4ff", width=6),
                ),
            ],
            traces=[1],  # Only update trace index 1 (the slice)
            name=str(_angle),
        ))

    _t_init = np.linspace(-2, 2, 50)
    _fig_saddle = go.Figure(
        data=[
            go.Surface(x=_X, y=_Y, z=_Z, colorscale="RdBu", showscale=False, opacity=0.7),
            go.Scatter3d(
                x=_t_init * np.cos(0), y=_t_init * np.sin(0), z=(_t_init * np.cos(0))**2 - (_t_init * np.sin(0))**2,
                mode="lines", line=dict(color="#00d4ff", width=6),
            ),
            go.Scatter3d(x=[0], y=[0], z=[0], mode="markers", marker=dict(size=8, color="#ffff00")),
        ],
        frames=_frames,
    )

    _fig_saddle.update_layout(
        title=dict(text="Saddle Point: f(x,y) = x² - y² (Rotating Slice)", font=dict(color="#eaeaea")),
        scene=dict(
            xaxis=dict(title=dict(text="x", font=dict(color="#a0a0a0")), backgroundcolor="#1a1a2e", gridcolor="#2d3a4f", range=[-2, 2]),
            yaxis=dict(title=dict(text="y", font=dict(color="#a0a0a0")), backgroundcolor="#1a1a2e", gridcolor="#2d3a4f", range=[-2, 2]),
            zaxis=dict(title=dict(text="f(x,y)", font=dict(color="#a0a0a0")), backgroundcolor="#1a1a2e", gridcolor="#2d3a4f", range=[-4, 4]),
            bgcolor="#1a1a2e",
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.0)),
        ),
        paper_bgcolor="#1a1a2e",
        height=500,
        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                y=0,
                x=0.1,
                xanchor="right",
                buttons=[
                    dict(label="▶ Play", method="animate",
                         args=[None, dict(frame=dict(duration=50, redraw=True), fromcurrent=True)]),
                    dict(label="⏸ Pause", method="animate",
                         args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")]),
                ],
            )
        ],
    )
    _fig_saddle
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### What the Animation Shows

        The cyan curve shows a **cross-section** of the saddle surface as we rotate
        around the origin:

        - **Along the x-axis** (angle = 0): The curve is $z = x^2$, a parabola opening **upward**
        - **Along the y-axis** (angle = 90°): The curve is $z = -y^2$, a parabola opening **downward**
        - **At 45°**: The curve passes through zero, transitioning between the two behaviors

        This is why saddle points are tricky in optimization—a descent algorithm might
        think it found a minimum when approaching from one direction, only to discover
        it can go lower from another direction.

        **Physical analogy**: A mountain pass is a saddle point. It's the lowest point
        between two peaks (minimum in one direction) but the highest point along the
        valley floor (maximum in the perpendicular direction).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Double Integrals: Measuring Volume Under Surfaces

        ### From Area to Volume

        Just as single integrals measure **area** under a curve, double integrals measure
        **volume** under a surface.

        The **double integral** of $f(x, y)$ over a region $R$:

        $$\iint_R f(x, y) \, dA = \iint_R f(x, y) \, dx \, dy$$

        ### Historical Development

        The theory of multiple integrals was developed in the late 18th and early 19th
        centuries. **Joseph-Louis Lagrange** and **Pierre-Simon Laplace** developed many
        techniques for computing them, driven by problems in celestial mechanics and
        probability theory.

        **Carl Friedrich Gauss** (1777-1855) made crucial contributions, including the
        famous **Gauss's theorem** (divergence theorem) that relates volume integrals to
        surface integrals—a profound connection between local and global properties.

        ### Computing Double Integrals

        For a rectangular region $R = [a, b] \times [c, d]$:

        $$\iint_R f(x, y) \, dA = \int_a^b \int_c^d f(x, y) \, dy \, dx$$

        We compute **iterated integrals**—first integrating with respect to $y$ (treating
        $x$ as constant), then with respect to $x$.

        **Fubini's Theorem** tells us we can integrate in either order:
        $$\int_a^b \int_c^d f(x, y) \, dy \, dx = \int_c^d \int_a^b f(x, y) \, dx \, dy$$
        """
    )
    return


@app.cell
def _(mo):
    # Sliders for Riemann sum visualization
    nx_slider = mo.ui.slider(start=2, stop=20, step=1, value=5, label="Divisions in x")
    ny_slider = mo.ui.slider(start=2, stop=20, step=1, value=5, label="Divisions in y")
    return nx_slider, ny_slider


@app.cell
def _(mo, nx_slider, ny_slider):
    mo.md(
        f"""
        ### Visualizing Double Integrals with Riemann Sums

        Just as we approximated single integrals with rectangles, we approximate double
        integrals with **rectangular boxes** (prisms).

        Adjust the number of divisions: {nx_slider} {ny_slider}

        **Region**: $[0, 2] \\times [0, 2]$
        **Function**: $f(x, y) = x^2 + y^2$
        """
    )
    return


@app.cell
def _(go, np, nx_slider, ny_slider):
    # Double integral Riemann sum visualization
    _nx = nx_slider.value
    _ny = ny_slider.value

    # Region [0, 2] x [0, 2]
    _a, _b = 0, 2
    _c, _d = 0, 2

    _dx = (_b - _a) / _nx
    _dy = (_d - _c) / _ny

    # Create boxes
    _fig_riemann2d = go.Figure()

    # Fine surface for reference
    _x_fine = np.linspace(_a, _b, 50)
    _y_fine = np.linspace(_c, _d, 50)
    _X_fine, _Y_fine = np.meshgrid(_x_fine, _y_fine)
    _Z_fine = _X_fine**2 + _Y_fine**2

    _fig_riemann2d.add_trace(go.Surface(
        x=_X_fine, y=_Y_fine, z=_Z_fine,
        colorscale="Viridis",
        opacity=0.3,
        showscale=False,
    ))

    # Riemann boxes
    _volume_sum = 0
    for _i in range(_nx):
        for _j in range(_ny):
            _xi = _a + (_i + 0.5) * _dx  # midpoint
            _yj = _c + (_j + 0.5) * _dy
            _zij = _xi**2 + _yj**2

            _volume_sum += _zij * _dx * _dy

            # Box vertices
            _x0, _x1 = _a + _i * _dx, _a + (_i + 1) * _dx
            _y0, _y1 = _c + _j * _dy, _c + (_j + 1) * _dy

            # Top face of box
            _fig_riemann2d.add_trace(go.Mesh3d(
                x=[_x0, _x1, _x1, _x0],
                y=[_y0, _y0, _y1, _y1],
                z=[_zij, _zij, _zij, _zij],
                color="#00d4ff",
                opacity=0.7,
                showscale=False,
            ))

    # True integral value: ∫∫ (x² + y²) dA over [0,2]x[0,2]
    # = ∫₀² ∫₀² (x² + y²) dy dx = ∫₀² [x²y + y³/3]₀² dx
    # = ∫₀² (2x² + 8/3) dx = [2x³/3 + 8x/3]₀² = 16/3 + 16/3 = 32/3
    _true_value = 32 / 3

    _fig_riemann2d.update_layout(
        title=dict(
            text=f"Double Integral Riemann Sum: {_nx}×{_ny} boxes | Sum = {_volume_sum:.4f} | True = {_true_value:.4f}",
            font=dict(color="#eaeaea"),
        ),
        scene=dict(
            xaxis=dict(title=dict(text="x", font=dict(color="#a0a0a0")), backgroundcolor="#1a1a2e", gridcolor="#2d3a4f", range=[0, 2.2]),
            yaxis=dict(title=dict(text="y", font=dict(color="#a0a0a0")), backgroundcolor="#1a1a2e", gridcolor="#2d3a4f", range=[0, 2.2]),
            zaxis=dict(title=dict(text="f(x,y)", font=dict(color="#a0a0a0")), backgroundcolor="#1a1a2e", gridcolor="#2d3a4f", range=[0, 10]),
            bgcolor="#1a1a2e",
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.0)),
        ),
        paper_bgcolor="#1a1a2e",
        height=500,
        showlegend=False,
    )
    _fig_riemann2d
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Understanding the Riemann Sum Visualization

        The cyan boxes approximate the volume under the surface $f(x,y) = x^2 + y^2$. Each box has its base on the $(x, y)$ plane and extends up to the function's value at that point. As you increase the number of divisions, the boxes become smaller and more numerous, fitting the curved surface more accurately.

        Each box represents a contribution to the volume:
        - **Base area**: $\Delta x \times \Delta y$ (the small rectangle in the $xy$-plane)
        - **Height**: $f(x_i, y_j)$ (function value at the sample point)
        - **Volume contribution**: $f(x_i, y_j) \cdot \Delta x \cdot \Delta y$

        **Total approximation**: Sum of all box volumes

        **As divisions increase**:
        - More, smaller boxes
        - Better approximation to the true volume
        - Riemann sum converges to the true integral

        **Exact calculation** for $f(x,y) = x^2 + y^2$ over $[0,2] \times [0,2]$:

        $$\begin{aligned}
        \int_0^2 \int_0^2 (x^2 + y^2) \, dy \, dx &= \int_0^2 \left[ x^2 y + \frac{y^3}{3} \right]_0^2 dx \\
        &= \int_0^2 \left( 2x^2 + \frac{8}{3} \right) dx \\
        &= \left[ \frac{2x^3}{3} + \frac{8x}{3} \right]_0^2 \\
        &= \frac{16}{3} + \frac{16}{3} = \frac{32}{3} \approx 10.667
        \end{aligned}$$
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Applications: Heat Conduction and the Laplacian

        ### Fourier's Heat Equation

        One of the most important applications of multivariable calculus is **heat
        conduction**. In 1822, **Jean-Baptiste Joseph Fourier** published his masterwork
        on heat flow, introducing what we now call the **heat equation**:

        $$\frac{\partial T}{\partial t} = \alpha \nabla^2 T$$

        where $T(x, y, t)$ is temperature, $\alpha$ is thermal diffusivity, and
        $\nabla^2 = \frac{\partial^2}{\partial x^2} + \frac{\partial^2}{\partial y^2}$
        is the **Laplacian operator**.

        ### The Laplacian: Measuring "Difference from Average"

        The Laplacian $\nabla^2 f$ measures how much $f$ at a point differs from the
        average of $f$ in a small neighborhood:

        - $\nabla^2 f > 0$: The point is **lower** than its surroundings (like a valley)
        - $\nabla^2 f < 0$: The point is **higher** than its surroundings (like a peak)
        - $\nabla^2 f = 0$: The point equals its local average (**harmonic function**)

        **Physical meaning for heat**: Heat flows from high to low temperature. If a point
        is cooler than its surroundings ($\nabla^2 T > 0$), heat flows in, warming it.
        If hotter ($\nabla^2 T < 0$), heat flows out, cooling it.

        Let's visualize steady-state heat distribution on a plate.
        """
    )
    return


@app.cell
def _(go, np):
    # Solve Laplace equation on a square plate with boundary conditions
    # Using iterative relaxation method (Gauss-Seidel)

    _n = 50  # Grid size
    _T = np.zeros((_n, _n))

    # Boundary conditions
    _T[0, :] = 100  # Top edge hot
    _T[-1, :] = 0   # Bottom edge cold
    _T[:, 0] = np.linspace(0, 100, _n)  # Left edge gradient
    _T[:, -1] = np.linspace(0, 100, _n)  # Right edge gradient

    # Iterative solution (Laplace equation: ∇²T = 0)
    for _iter in range(500):
        _T_old = _T.copy()
        for _i in range(1, _n-1):
            for _j in range(1, _n-1):
                _T[_i, _j] = 0.25 * (_T[_i+1, _j] + _T[_i-1, _j] + _T[_i, _j+1] + _T[_i, _j-1])
        # Check for convergence
        if np.max(np.abs(_T - _T_old)) < 1e-6:
            break

    _x = np.linspace(0, 1, _n)
    _y = np.linspace(0, 1, _n)

    _fig_heat = go.Figure(data=[
        go.Heatmap(
            x=_x, y=_y, z=_T,
            colorscale="Thermal",
            colorbar=dict(title=dict(text="T (°C)", font=dict(color="#a0a0a0")), tickfont=dict(color="#a0a0a0")),
        )
    ])

    _fig_heat.update_layout(
        title=dict(text="Steady-State Temperature Distribution (Laplace Equation)", font=dict(color="#eaeaea")),
        xaxis=dict(title=dict(text="x", font=dict(color="#a0a0a0")), gridcolor="#2d3a4f", tickfont=dict(color="#a0a0a0")),
        yaxis=dict(title=dict(text="y", font=dict(color="#a0a0a0")), gridcolor="#2d3a4f", scaleanchor="x", tickfont=dict(color="#a0a0a0")),
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#1a1a2e",
        height=450,
    )
    _fig_heat
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Understanding the Heat Distribution

        This heatmap displays the steady-state temperature distribution on a square metal plate, computed by solving Laplace's equation $\nabla^2 T = 0$. The colors represent temperature: red/yellow regions are hot (near 100°C), while dark/purple regions are cool (near 0°C). Heat has reached equilibrium—no more flow occurs.

        **Boundary conditions:**
        - **Top edge**: Held at 100°C (red)
        - **Bottom edge**: Held at 0°C (dark)
        - **Side edges**: Linear gradient from bottom to top

        **Steady-state solution:**
        - Heat has stopped flowing (equilibrium)
        - Temperature at each interior point equals average of neighbors ($\nabla^2 T = 0$)
        - Smooth gradient from hot to cold regions

        This is the **Laplace equation** in action—one of the most important partial
        differential equations in physics. It appears in:
        - Electrostatics (electric potential)
        - Fluid mechanics (velocity potential)
        - Gravitation (gravitational potential)
        - Steady-state diffusion
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Gradient Descent: Optimization in Multiple Dimensions

        ### Finding Minima with the Gradient

        One of the most important applications of multivariable calculus today is
        **optimization**. Given a function $f(x, y)$, how do we find its minimum?

        The **gradient descent** algorithm uses a simple idea:
        1. Start at some point $(x_0, y_0)$
        2. Compute the gradient $\nabla f$
        3. Take a step in the direction of $-\nabla f$ (downhill)
        4. Repeat until convergence

        Mathematically:
        $$(x_{n+1}, y_{n+1}) = (x_n, y_n) - \eta \nabla f(x_n, y_n)$$

        where $\eta$ is the **learning rate** (step size).

        ### Why This Works

        The gradient points uphill—in the direction of steepest ascent. So $-\nabla f$
        points downhill. By repeatedly stepping downhill, we descend toward a minimum.

        **Caveat**: Gradient descent finds **local** minima, not necessarily global ones.
        For non-convex functions (like neural network loss surfaces), this is a major
        challenge in machine learning.

        Let's visualize gradient descent on a simple function.
        """
    )
    return


@app.cell
def _(mo):
    # Starting point and learning rate controls
    gd_x0_slider = mo.ui.slider(start=-1.5, stop=1.5, step=0.1, value=1.2, label="Start x")
    gd_y0_slider = mo.ui.slider(start=-1.5, stop=1.5, step=0.1, value=1.2, label="Start y")
    gd_lr_slider = mo.ui.slider(start=0.01, stop=0.5, step=0.01, value=0.1, label="Learning rate η")
    return gd_lr_slider, gd_x0_slider, gd_y0_slider


@app.cell
def _(gd_lr_slider, gd_x0_slider, gd_y0_slider, mo):
    mo.md(
        f"""
        ### Interactive Gradient Descent

        Watch the algorithm descend toward the minimum of $f(x, y) = x^2 + y^2$:

        {gd_x0_slider} {gd_y0_slider} {gd_lr_slider}
        """
    )
    return


@app.cell
def _(gd_lr_slider, gd_x0_slider, gd_y0_slider, go, np):
    # Gradient descent animation
    _x0 = gd_x0_slider.value
    _y0 = gd_y0_slider.value
    _lr = gd_lr_slider.value

    # Function: f(x,y) = x² + y²
    # Gradient: (2x, 2y)

    _path = [(_x0, _y0)]
    _x, _y = _x0, _y0

    for _step in range(50):
        _gx = 2 * _x
        _gy = 2 * _y
        _x = _x - _lr * _gx
        _y = _y - _lr * _gy
        _path.append((_x, _y))
        if _gx**2 + _gy**2 < 1e-6:
            break

    _path = np.array(_path)
    _z_path = _path[:, 0]**2 + _path[:, 1]**2

    # Surface - reduced resolution for smaller file size
    _xs = np.linspace(-2, 2, 30)
    _ys = np.linspace(-2, 2, 30)
    _Xs, _Ys = np.meshgrid(_xs, _ys)
    _Zs = _Xs**2 + _Ys**2

    # Create frames for animation - only include changing traces, not the static surface
    _frames = []
    # Sample every few steps to reduce number of frames
    _step_indices = list(range(0, len(_path), max(1, len(_path) // 30)))
    if _step_indices[-1] != len(_path) - 1:
        _step_indices.append(len(_path) - 1)

    for _k in _step_indices[1:]:  # Skip first (it's the initial state)
        _frames.append(go.Frame(
            data=[
                go.Scatter3d(
                    x=_path[:_k+1, 0], y=_path[:_k+1, 1], z=_z_path[:_k+1],
                    mode="lines+markers",
                    line=dict(color="#ff6b6b", width=4),
                    marker=dict(size=4, color="#ff6b6b"),
                ),
                go.Scatter3d(
                    x=[_path[_k, 0]], y=[_path[_k, 1]], z=[_z_path[_k]],
                    mode="markers",
                    marker=dict(size=8, color="#00d4ff"),
                ),
            ],
            traces=[1, 2],  # Only update trace indices 1 and 2 (path and current point)
            name=str(_k),
        ))

    _fig_gd = go.Figure(
        data=[
            go.Surface(x=_Xs, y=_Ys, z=_Zs, colorscale="Viridis", opacity=0.6, showscale=False),
            go.Scatter3d(
                x=[_path[0, 0]], y=[_path[0, 1]], z=[_z_path[0]],
                mode="lines+markers",
                line=dict(color="#ff6b6b", width=4),
                marker=dict(size=4, color="#ff6b6b"),
            ),
            go.Scatter3d(
                x=[_path[0, 0]], y=[_path[0, 1]], z=[_z_path[0]],
                mode="markers",
                marker=dict(size=8, color="#00d4ff"),
            ),
        ],
        frames=_frames,
    )

    _fig_gd.update_layout(
        title=dict(
            text=f"Gradient Descent: {len(_path)} steps to reach ({_path[-1, 0]:.3f}, {_path[-1, 1]:.3f})",
            font=dict(color="#eaeaea"),
        ),
        scene=dict(
            xaxis=dict(title=dict(text="x", font=dict(color="#a0a0a0")), backgroundcolor="#1a1a2e", gridcolor="#2d3a4f", range=[-2, 2]),
            yaxis=dict(title=dict(text="y", font=dict(color="#a0a0a0")), backgroundcolor="#1a1a2e", gridcolor="#2d3a4f", range=[-2, 2]),
            zaxis=dict(title=dict(text="f(x,y)", font=dict(color="#a0a0a0")), backgroundcolor="#1a1a2e", gridcolor="#2d3a4f", range=[0, 8]),
            bgcolor="#1a1a2e",
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.0)),
        ),
        paper_bgcolor="#1a1a2e",
        height=500,
        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                y=0,
                x=0.1,
                xanchor="right",
                buttons=[
                    dict(label="▶ Descend", method="animate",
                         args=[None, dict(frame=dict(duration=100, redraw=True), fromcurrent=True)]),
                    dict(label="⏸ Pause", method="animate",
                         args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")]),
                ],
            )
        ],
    )
    _fig_gd
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Observations on Gradient Descent

        The animation traces the path of gradient descent as it rolls downhill on the paraboloid surface. The red line shows the algorithm's trajectory, and the cyan dot marks the current position. Starting from your chosen point, each step moves in the direction of steepest descent (opposite the gradient), eventually reaching the minimum at the origin.

        **Try different settings:**
        - **Large learning rate** ($\eta > 0.3$): May overshoot and oscillate
        - **Small learning rate** ($\eta < 0.05$): Converges slowly but steadily
        - **Starting far from minimum**: Takes more steps to converge

        **Key insight**: The optimal learning rate depends on the function's curvature.
        This is why adaptive methods like **Adam** (used in deep learning) adjust the
        learning rate automatically.

        **Connection to physics**: Gradient descent mimics a ball rolling downhill on a
        surface, but without momentum. Adding momentum (as in **SGD with momentum**)
        often improves convergence.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Polar and Cylindrical Coordinates

        ### Beyond Cartesian Coordinates

        Sometimes Cartesian coordinates $(x, y)$ aren't the most natural choice. For
        problems with **circular symmetry**, **polar coordinates** are often better:

        $$x = r\cos\theta, \quad y = r\sin\theta$$

        where $r$ is the distance from the origin and $\theta$ is the angle from the
        positive $x$-axis.

        ### The Jacobian: Changing Variables in Integrals

        When changing coordinates in a double integral, we need the **Jacobian**—a
        correction factor for how areas transform:

        $$\iint f(x, y) \, dx \, dy = \iint f(r\cos\theta, r\sin\theta) \cdot r \, dr \, d\theta$$

        The factor $r$ is the Jacobian for polar coordinates. It accounts for the fact
        that area elements are **larger** at greater distances from the origin.

        **Why $r$?** Consider a small box in polar coordinates with sides $dr$ and $d\theta$.
        Its area is approximately $r \cdot dr \cdot d\theta$, not just $dr \cdot d\theta$,
        because the arc length at radius $r$ is $r \cdot d\theta$.

        ### Example: Area of a Circle

        Computing the area of a circle $x^2 + y^2 \leq R^2$ using polar coordinates:

        $$\begin{aligned}
        A &= \iint dx \, dy \\
        &= \int_0^{2\pi} \int_0^R r \, dr \, d\theta \\
        &= \int_0^{2\pi} \frac{R^2}{2} \, d\theta = \pi R^2
        \end{aligned}$$

        The symmetry makes the calculation trivial in polar coordinates!
        """
    )
    return


@app.cell
def _(go, np):
    # Visualize polar coordinate grid and Jacobian
    _fig_polar = go.Figure()

    # Polar grid lines
    _r_lines = np.linspace(0.2, 2, 10)
    _theta_lines = np.linspace(0, 2*np.pi, 13)

    # Radial lines
    for _theta in _theta_lines[:-1]:
        _r = np.linspace(0, 2, 50)
        _px = _r * np.cos(_theta)
        _py = _r * np.sin(_theta)
        _fig_polar.add_trace(go.Scatter(
            x=_px, y=_py, mode="lines",
            line=dict(color="#4a5568", width=1),
            showlegend=False,
        ))

    # Circular arcs
    for _r in _r_lines:
        _theta = np.linspace(0, 2*np.pi, 100)
        _cx = _r * np.cos(_theta)
        _cy = _r * np.sin(_theta)
        _fig_polar.add_trace(go.Scatter(
            x=_cx, y=_cy, mode="lines",
            line=dict(color="#4a5568", width=1),
            showlegend=False,
        ))

    # Highlight a small area element
    _r1, _r2 = 1.0, 1.2
    _t1, _t2 = np.pi/6, np.pi/4

    # Area element boundary
    _t_arc = np.linspace(_t1, _t2, 20)
    _outer_arc_x = _r2 * np.cos(_t_arc)
    _outer_arc_y = _r2 * np.sin(_t_arc)
    _inner_arc_x = _r1 * np.cos(_t_arc)
    _inner_arc_y = _r1 * np.sin(_t_arc)

    _element_x = list(_inner_arc_x) + list(_outer_arc_x[::-1]) + [_inner_arc_x[0]]
    _element_y = list(_inner_arc_y) + list(_outer_arc_y[::-1]) + [_inner_arc_y[0]]

    _fig_polar.add_trace(go.Scatter(
        x=_element_x, y=_element_y,
        fill="toself",
        fillcolor="rgba(0, 212, 255, 0.5)",
        line=dict(color="#00d4ff", width=2),
        name="Area element r·dr·dθ",
    ))

    # Labels
    _fig_polar.add_annotation(x=1.5, y=0.5, text="r", font=dict(size=14, color="#a0a0a0"), showarrow=False)
    _fig_polar.add_annotation(x=0.5, y=0.5, text="θ", font=dict(size=14, color="#a0a0a0"), showarrow=False)
    _fig_polar.add_annotation(x=1.3, y=0.75, text="dA = r dr dθ", font=dict(size=12, color="#00d4ff"), showarrow=False)

    _fig_polar.update_layout(
        title=dict(text="Polar Coordinates: Area Element dA = r dr dθ", font=dict(color="#eaeaea")),
        xaxis=dict(title=dict(text="x", font=dict(color="#a0a0a0")), gridcolor="#2d3a4f", zerolinecolor="#4a5568", range=[-2.2, 2.2], scaleanchor="y", tickfont=dict(color="#a0a0a0")),
        yaxis=dict(title=dict(text="y", font=dict(color="#a0a0a0")), gridcolor="#2d3a4f", zerolinecolor="#4a5568", range=[-2.2, 2.2], tickfont=dict(color="#a0a0a0")),
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#1a1a2e",
        height=450,
        showlegend=True,
        legend=dict(font=dict(color="#a0a0a0"), orientation='h', yanchor='bottom', y=-0.15, xanchor='center', x=0.5),
        margin=dict(l=40, r=40, t=50, b=80),
    )
    _fig_polar
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Understanding the Area Element

        This diagram illustrates the polar coordinate grid, where position is described by distance $r$ from the origin and angle $\theta$ from the positive $x$-axis. The highlighted cyan region is a small "area element"—notice it's not a rectangle but a wedge-shaped piece. Its area depends on $r$, which explains the Jacobian factor in polar integration.

        The cyan region shows a small area element in polar coordinates:
        - **Radial extent**: $dr$ (change in radius)
        - **Angular extent**: $d\theta$ (change in angle)
        - **Arc length**: $r \cdot d\theta$ (at radius $r$)
        - **Area**: $dA \approx dr \cdot (r \cdot d\theta) = r \, dr \, d\theta$

        **Key insight**: The factor $r$ is crucial! Without it, we'd be saying all the
        thin wedges have the same area regardless of distance from the origin—clearly wrong.

        This is the **Jacobian determinant** in action:

        $$J = \begin{vmatrix} \frac{\partial x}{\partial r} & \frac{\partial x}{\partial \theta} \\ \frac{\partial y}{\partial r} & \frac{\partial y}{\partial \theta} \end{vmatrix} = \begin{vmatrix} \cos\theta & -r\sin\theta \\ \sin\theta & r\cos\theta \end{vmatrix} = r$$
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The Gaussian Integral: A Beautiful Application

        ### The Most Famous Integral

        One of the most beautiful applications of multivariable calculus is computing
        the **Gaussian integral**:

        $$I = \int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}$$

        This integral is impossible to compute directly in Cartesian coordinates—there's
        no elementary antiderivative for $e^{-x^2}$. But using polar coordinates, it
        becomes elegant.

        ### The Clever Trick

        Instead of computing $I$ directly, compute $I^2$:

        $$I^2 = \int_{-\infty}^{\infty} e^{-x^2} dx \cdot \int_{-\infty}^{\infty} e^{-y^2} dy = \iint_{\mathbb{R}^2} e^{-(x^2+y^2)} dx \, dy$$

        Now switch to polar coordinates where $x^2 + y^2 = r^2$:

        $$I^2 = \int_0^{2\pi} \int_0^{\infty} e^{-r^2} \cdot r \, dr \, d\theta$$

        The inner integral is now tractable with $u = r^2$:

        $$\int_0^{\infty} r e^{-r^2} dr = \frac{1}{2} \int_0^{\infty} e^{-u} du = \frac{1}{2}$$

        Therefore:

        $$I^2 = 2\pi \cdot \frac{1}{2} = \pi \quad \Rightarrow \quad I = \sqrt{\pi}$$

        **This is why $\sqrt{\pi}$ appears everywhere in probability and statistics!**
        """
    )
    return


@app.cell
def _(go, np):
    # Visualize the Gaussian function in 2D
    _x = np.linspace(-3, 3, 80)
    _y = np.linspace(-3, 3, 80)
    _X, _Y = np.meshgrid(_x, _y)
    _Z = np.exp(-(_X**2 + _Y**2))

    _fig_gauss = go.Figure(data=[
        go.Surface(
            x=_X, y=_Y, z=_Z,
            colorscale="Plasma",
            showscale=True,
            colorbar=dict(title=dict(text="e^(-(x²+y²))", font=dict(color="#a0a0a0")), tickfont=dict(color="#a0a0a0")),
        )
    ])

    _fig_gauss.update_layout(
        title=dict(text="The 2D Gaussian: e^(-(x²+y²)) — Volume Under Surface = π", font=dict(color="#eaeaea")),
        scene=dict(
            xaxis=dict(title=dict(text="x", font=dict(color="#a0a0a0")), backgroundcolor="#1a1a2e", gridcolor="#2d3a4f"),
            yaxis=dict(title=dict(text="y", font=dict(color="#a0a0a0")), backgroundcolor="#1a1a2e", gridcolor="#2d3a4f"),
            zaxis=dict(title=dict(text="f(x,y)", font=dict(color="#a0a0a0")), backgroundcolor="#1a1a2e", gridcolor="#2d3a4f"),
            bgcolor="#1a1a2e",
        ),
        paper_bgcolor="#1a1a2e",
        height=500,
        margin=dict(l=0, r=0, t=40, b=0),
    )
    _fig_gauss
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### The Gaussian's Significance

        This 3D bell-shaped surface is the two-dimensional Gaussian function $e^{-(x^2+y^2)}$. It peaks at the origin (value 1) and decays smoothly toward zero in all directions. The total volume under this surface equals exactly $\pi$—a remarkable result that connects exponentials, geometry, and probability.

        The Gaussian function $e^{-x^2}$ and its normalized version (the **normal distribution**)
        appear throughout science:

        | Field | Application |
        |-------|-------------|
        | Statistics | Normal distribution, Central Limit Theorem |
        | Physics | Maxwell-Boltzmann distribution of molecular speeds |
        | Quantum Mechanics | Ground state of harmonic oscillator |
        | Signal Processing | Gaussian filters, smoothing |
        | Machine Learning | Gaussian processes, RBF kernels |
        | Finance | Black-Scholes option pricing |

        The fact that $\int e^{-x^2} dx = \sqrt{\pi}$ is not just a mathematical curiosity—it's
        the foundation for normalizing probability distributions and understanding randomness.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Summary: The Power of Multiple Variables

        ### What We've Learned

        | Concept | Definition | Significance |
        |---------|------------|--------------|
        | $f(x, y)$ | Function of two variables | Represents surfaces, fields, distributions |
        | Partial derivative | $\frac{\partial f}{\partial x}$ | Rate of change in one direction |
        | Gradient | $\nabla f = (f_x, f_y)$ | Direction of steepest ascent |
        | Tangent plane | $z = f(a,b) + f_x(x-a) + f_y(y-b)$ | Best linear approximation |
        | Double integral | $\iint f \, dA$ | Volume under surface |
        | Jacobian | $J = r$ (polar) | Coordinate transformation factor |

        ### The Big Picture

        Multivariable calculus extends the ideas of single-variable calculus to higher
        dimensions. The core concepts—limits, derivatives, integrals—generalize beautifully,
        but with richer geometric structure.

        **Partial derivatives** decompose change into components along coordinate axes.

        **The gradient** unifies these into a single vector pointing toward maximum increase.

        **Multiple integrals** allow us to compute volumes, masses, probabilities, and
        countless other quantities over regions in space.

        These tools are essential for:
        - **Physics**: Describing fields (electromagnetic, gravitational, temperature)
        - **Engineering**: Optimizing designs, analyzing stress and flow
        - **Machine Learning**: Training neural networks via gradient descent
        - **Economics**: Optimizing with multiple variables (resources, prices)
        - **Biology**: Modeling populations, diffusion, growth

        ### Historical Sources and Further Reading

        - [Euler's Works (Euler Archive)](https://scholarlycommons.pacific.edu/euler/)
        - [Lagrange's Mécanique Analytique](https://archive.org/details/mcaniqueanalyti00lagrgoog)
        - [Fourier's Théorie de la Chaleur](https://archive.org/details/thorieanalytiq00four)
        - [3Blue1Brown: Multivariable Calculus](https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr)
        - [MIT OpenCourseWare: Multivariable Calculus](https://ocw.mit.edu/courses/18-02sc-multivariable-calculus-fall-2010/)
        - [Khan Academy: Multivariable Calculus](https://www.khanacademy.org/math/multivariable-calculus)
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        *"Nature is written in mathematical language, and its characters are triangles,
        circles, and other geometric figures, without which it is humanly impossible to
        understand a single word of it; without these, one wanders about in a dark labyrinth."*

        — Galileo Galilei, Il Saggiatore (1623)

        ---

        **Next**: In our next exploration, we'll dive into **vector calculus**—line integrals,
        surface integrals, and the beautiful theorems of Green, Stokes, and Gauss that
        connect them all.
        """
    )
    return


if __name__ == "__main__":
    app.run()
