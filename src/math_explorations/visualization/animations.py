"""Plotly animation builders for calculus visualizations."""

from typing import Callable
import numpy as np
import plotly.graph_objects as go
from .styles import DARK_THEME, COLORS, ANIMATION_SETTINGS


def create_secant_to_tangent(
    f: Callable[[float], float],
    f_prime: Callable[[float], float],
    x0: float,
    x_range: tuple[float, float] = (-3, 3),
    h_values: list[float] | None = None,
    num_points: int = 300,
) -> go.Figure:
    """
    Create interactive visualization showing secant line approaching tangent.

    Args:
        f: Function to visualize
        f_prime: Derivative function
        x0: Point of tangency
        x_range: Range for x-axis
        h_values: Values of h for slider (decreasing toward 0)
        num_points: Points for function curve

    Returns:
        Plotly Figure with slider
    """
    if h_values is None:
        h_values = [2.0, 1.5, 1.0, 0.75, 0.5, 0.3, 0.2, 0.1, 0.05, 0.01]

    x = np.linspace(x_range[0], x_range[1], num_points)
    y = np.array([f(xi) for xi in x])
    y0 = f(x0)
    true_slope = f_prime(x0)

    fig = go.Figure()

    # Function curve (static)
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode="lines",
        line={"color": COLORS["primary"], "width": 3},
        name="f(x)",
    ))

    # Tangent line (static reference)
    x_tan = np.array([x_range[0], x_range[1]])
    y_tan = y0 + true_slope * (x_tan - x0)
    fig.add_trace(go.Scatter(
        x=x_tan, y=y_tan,
        mode="lines",
        line={"color": COLORS["tertiary"], "width": 2, "dash": "dash"},
        name=f"Tangent (slope={true_slope:.4f})",
        visible=True,
    ))

    # Initial secant line
    h = h_values[0]
    x1 = x0 + h
    y1 = f(x1)
    secant_slope = (y1 - y0) / h

    x_sec = np.array([x_range[0], x_range[1]])
    y_sec = y0 + secant_slope * (x_sec - x0)

    fig.add_trace(go.Scatter(
        x=x_sec, y=y_sec,
        mode="lines",
        line={"color": COLORS["quaternary"], "width": 2},
        name=f"Secant (h={h:.2f}, slope={secant_slope:.4f})",
    ))

    # Points
    fig.add_trace(go.Scatter(
        x=[x0], y=[y0],
        mode="markers",
        marker={"color": COLORS["secondary"], "size": 12},
        name="Fixed point",
    ))

    fig.add_trace(go.Scatter(
        x=[x1], y=[y1],
        mode="markers",
        marker={"color": COLORS["quaternary"], "size": 10},
        name="Moving point",
    ))

    # Create slider steps
    steps = []
    for h in h_values:
        x1 = x0 + h
        y1 = f(x1)
        slope = (y1 - y0) / h
        y_sec = y0 + slope * (x_sec - x0)

        step = {
            "method": "update",
            "args": [
                {
                    "x": [x, x_tan, x_sec, [x0], [x1]],
                    "y": [y, y_tan, y_sec, [y0], [y1]],
                },
                {"title": f"h = {h:.4f}, Secant slope = {slope:.4f}, Tangent slope = {true_slope:.4f}"}
            ],
            "label": f"{h:.2f}",
        }
        steps.append(step)

    sliders = [{
        "active": 0,
        "currentvalue": {"prefix": "h = ", "visible": True, "xanchor": "center"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.05,
        "xanchor": "left",
        "steps": steps,
        "bgcolor": COLORS["paper"],
        "bordercolor": COLORS["grid"],
        "font": {"color": COLORS["text"]},
    }]

    fig.update_layout(
        **DARK_THEME,
        title=f"Secant → Tangent at x = {x0}",
        xaxis_title="x",
        yaxis_title="y",
        sliders=sliders,
        showlegend=True,
    )

    return fig


def animate_limit_process(
    f: Callable[[float], float],
    f_prime: Callable[[float], float],
    x0: float,
    x_range: tuple[float, float] = (-3, 3),
    num_frames: int = 60,
    num_points: int = 300,
) -> go.Figure:
    """
    Create animated visualization of the limit process (h → 0).

    Args:
        f: Function to visualize
        f_prime: Derivative function
        x0: Point of tangency
        x_range: Range for x-axis
        num_frames: Number of animation frames
        num_points: Points for function curve

    Returns:
        Plotly Figure with play/pause animation
    """
    x = np.linspace(x_range[0], x_range[1], num_points)
    y = np.array([f(xi) for xi in x])
    y0 = f(x0)
    true_slope = f_prime(x0)

    # h values decreasing exponentially
    h_values = np.exp(np.linspace(np.log(2), np.log(0.01), num_frames))

    fig = go.Figure()

    # Static function curve
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode="lines",
        line={"color": COLORS["primary"], "width": 3},
        name="f(x)",
    ))

    # Tangent line (target)
    x_line = np.array([x_range[0], x_range[1]])
    y_tan = y0 + true_slope * (x_line - x0)
    fig.add_trace(go.Scatter(
        x=x_line, y=y_tan,
        mode="lines",
        line={"color": COLORS["tertiary"], "width": 2, "dash": "dash"},
        name="Tangent line",
    ))

    # Initial secant
    h = h_values[0]
    slope = (f(x0 + h) - y0) / h
    y_sec = y0 + slope * (x_line - x0)
    fig.add_trace(go.Scatter(
        x=x_line, y=y_sec,
        mode="lines",
        line={"color": COLORS["quaternary"], "width": 3},
        name="Secant line",
    ))

    # Fixed point
    fig.add_trace(go.Scatter(
        x=[x0], y=[y0],
        mode="markers",
        marker={"color": COLORS["secondary"], "size": 14},
        name="Point of tangency",
    ))

    # Moving point
    fig.add_trace(go.Scatter(
        x=[x0 + h], y=[f(x0 + h)],
        mode="markers",
        marker={"color": COLORS["quaternary"], "size": 10},
        name="Approaching point",
    ))

    # Create frames
    frames = []
    for i, h in enumerate(h_values):
        x1 = x0 + h
        y1 = f(x1)
        slope = (y1 - y0) / h
        y_sec = y0 + slope * (x_line - x0)

        frame = go.Frame(
            data=[
                go.Scatter(x=x, y=y),  # Function (unchanged)
                go.Scatter(x=x_line, y=y_tan),  # Tangent (unchanged)
                go.Scatter(x=x_line, y=y_sec),  # Secant (animated)
                go.Scatter(x=[x0], y=[y0]),  # Fixed point
                go.Scatter(x=[x1], y=[y1]),  # Moving point
            ],
            name=str(i),
            layout={"title": f"h = {h:.4f} | Slope = {slope:.4f} → {true_slope:.4f}"}
        )
        frames.append(frame)

    fig.frames = frames

    # Animation controls
    fig.update_layout(
        **DARK_THEME,
        title=f"The Limit Process: h → 0 at x = {x0}",
        xaxis_title="x",
        yaxis_title="y",
        updatemenus=[{
            "type": "buttons",
            "showactive": False,
            "y": 1.15,
            "x": 0.5,
            "xanchor": "center",
            "buttons": [
                {
                    "label": "▶ Play",
                    "method": "animate",
                    "args": [
                        None,
                        {
                            "frame": {"duration": ANIMATION_SETTINGS["frame_duration"], "redraw": True},
                            "fromcurrent": True,
                            "transition": {"duration": ANIMATION_SETTINGS["transition_duration"]}
                        }
                    ]
                },
                {
                    "label": "⏸ Pause",
                    "method": "animate",
                    "args": [
                        [None],
                        {
                            "frame": {"duration": 0, "redraw": False},
                            "mode": "immediate",
                            "transition": {"duration": 0}
                        }
                    ]
                },
                {
                    "label": "↺ Reset",
                    "method": "animate",
                    "args": [
                        ["0"],
                        {
                            "frame": {"duration": 0, "redraw": True},
                            "mode": "immediate",
                        }
                    ]
                }
            ],
            "font": {"color": COLORS["text"]},
            "bgcolor": COLORS["paper"],
            "bordercolor": COLORS["grid"],
        }],
        sliders=[{
            "active": 0,
            "steps": [
                {"args": [[str(i)], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}],
                 "label": f"{h:.2f}", "method": "animate"}
                for i, h in enumerate(h_values[::max(1, len(h_values)//10)])
            ],
            "x": 0.05,
            "len": 0.9,
            "xanchor": "left",
            "y": -0.05,
            "currentvalue": {"prefix": "h ≈ ", "visible": True, "xanchor": "center"},
            "bgcolor": COLORS["paper"],
            "font": {"color": COLORS["text"]},
        }]
    )

    return fig


def create_tangent_line_plot(
    f: Callable[[float], float],
    f_prime: Callable[[float], float],
    x_range: tuple[float, float] = (-3, 3),
    initial_x: float = 0,
    num_points: int = 300,
) -> go.Figure:
    """
    Create interactive plot with draggable tangent point.

    Args:
        f: Function to visualize
        f_prime: Derivative function
        x_range: Range for x-axis
        initial_x: Initial x position for tangent
        num_points: Points for function curve

    Returns:
        Plotly Figure with slider for tangent point
    """
    x = np.linspace(x_range[0], x_range[1], num_points)
    y = np.array([f(xi) for xi in x])

    # Create slider positions
    x_positions = np.linspace(x_range[0] + 0.5, x_range[1] - 0.5, 30)

    fig = go.Figure()

    # Function curve
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode="lines",
        line={"color": COLORS["primary"], "width": 3},
        name="f(x)",
    ))

    # Initial tangent
    x0 = initial_x
    y0 = f(x0)
    slope = f_prime(x0)
    x_tan = np.array([x_range[0], x_range[1]])
    y_tan = y0 + slope * (x_tan - x0)

    fig.add_trace(go.Scatter(
        x=x_tan, y=y_tan,
        mode="lines",
        line={"color": COLORS["tertiary"], "width": 2, "dash": "dash"},
        name=f"Tangent (slope={slope:.3f})",
    ))

    fig.add_trace(go.Scatter(
        x=[x0], y=[y0],
        mode="markers",
        marker={"color": COLORS["quaternary"], "size": 14, "symbol": "circle"},
        name="Touch point",
    ))

    # Create slider steps
    steps = []
    for x0 in x_positions:
        y0 = f(x0)
        slope = f_prime(x0)
        y_tan = y0 + slope * (x_tan - x0)

        step = {
            "method": "update",
            "args": [
                {"x": [x, x_tan, [x0]], "y": [y, y_tan, [y0]]},
                {"title": f"Tangent at x = {x0:.2f} | Slope = {slope:.3f}"}
            ],
            "label": f"{x0:.1f}",
        }
        steps.append(step)

    fig.update_layout(
        **DARK_THEME,
        title=f"Tangent at x = {initial_x:.2f} | Slope = {f_prime(initial_x):.3f}",
        xaxis_title="x",
        yaxis_title="y",
        sliders=[{
            "active": len(x_positions) // 2,
            "currentvalue": {"prefix": "x = ", "visible": True},
            "pad": {"b": 10, "t": 50},
            "steps": steps,
            "bgcolor": COLORS["paper"],
            "font": {"color": COLORS["text"]},
        }],
    )

    return fig


def animate_power_rule(
    max_n: int = 5,
    x_range: tuple[float, float] = (-2, 2),
    num_points: int = 200,
) -> go.Figure:
    """
    Animate the power rule showing f(x) = x^n and f'(x) = nx^(n-1).

    Args:
        max_n: Maximum power to show
        x_range: Range for x-axis
        num_points: Points for curves

    Returns:
        Plotly Figure with animation
    """
    x = np.linspace(x_range[0], x_range[1], num_points)

    fig = go.Figure()

    # Initial traces (n=1)
    y_f = x ** 1
    y_fp = np.ones_like(x)

    fig.add_trace(go.Scatter(
        x=x, y=y_f,
        mode="lines",
        line={"color": COLORS["primary"], "width": 3},
        name="f(x) = x^n",
    ))

    fig.add_trace(go.Scatter(
        x=x, y=y_fp,
        mode="lines",
        line={"color": COLORS["secondary"], "width": 3},
        name="f'(x) = nx^(n-1)",
    ))

    # Create frames for each n
    frames = []
    for n in range(1, max_n + 1):
        y_f = x ** n
        y_fp = n * x ** (n - 1) if n > 0 else np.zeros_like(x)

        # Clip for display
        y_f = np.clip(y_f, -20, 20)
        y_fp = np.clip(y_fp, -20, 20)

        frame = go.Frame(
            data=[
                go.Scatter(x=x, y=y_f),
                go.Scatter(x=x, y=y_fp),
            ],
            name=str(n),
            layout={"title": f"Power Rule: f(x) = x^{n}, f'(x) = {n}x^{n-1}"}
        )
        frames.append(frame)

    fig.frames = frames

    # Create slider
    steps = []
    for n in range(1, max_n + 1):
        step = {
            "args": [[str(n)], {"frame": {"duration": 300, "redraw": True}, "mode": "immediate"}],
            "label": str(n),
            "method": "animate",
        }
        steps.append(step)

    fig.update_layout(
        **DARK_THEME,
        title="Power Rule: f(x) = x^1, f'(x) = 1",
        xaxis_title="x",
        yaxis_title="y",
        yaxis_range=[-10, 10],
        sliders=[{
            "active": 0,
            "currentvalue": {"prefix": "n = ", "visible": True},
            "pad": {"b": 10, "t": 60},
            "steps": steps,
            "bgcolor": COLORS["paper"],
            "font": {"color": COLORS["text"]},
        }],
        updatemenus=[{
            "type": "buttons",
            "showactive": False,
            "y": 1.15,
            "x": 0.5,
            "xanchor": "center",
            "buttons": [
                {
                    "label": "▶ Animate",
                    "method": "animate",
                    "args": [None, {"frame": {"duration": 800}, "transition": {"duration": 300}}]
                }
            ],
            "font": {"color": COLORS["text"]},
            "bgcolor": COLORS["paper"],
        }],
    )

    return fig


def animate_chain_rule(
    outer: Callable[[np.ndarray], np.ndarray],
    inner: Callable[[np.ndarray], np.ndarray],
    outer_prime: Callable[[np.ndarray], np.ndarray],
    inner_prime: Callable[[np.ndarray], np.ndarray],
    x_range: tuple[float, float] = (-2, 2),
    num_points: int = 200,
    title: str = "Chain Rule: (f∘g)'(x) = f'(g(x)) · g'(x)",
) -> go.Figure:
    """
    Visualize the chain rule with composite functions.

    Args:
        outer: Outer function f
        inner: Inner function g
        outer_prime: Derivative of outer function
        inner_prime: Derivative of inner function
        x_range: Range for x-axis
        num_points: Points for curves
        title: Plot title

    Returns:
        Plotly Figure showing composition and derivative
    """
    x = np.linspace(x_range[0], x_range[1], num_points)

    # Compute functions
    g_x = inner(x)
    f_g_x = outer(g_x)  # Composite: f(g(x))
    chain_deriv = outer_prime(g_x) * inner_prime(x)  # f'(g(x)) * g'(x)

    # Clip extreme values
    f_g_x = np.clip(f_g_x, -20, 20)
    chain_deriv = np.clip(chain_deriv, -20, 20)

    fig = go.Figure()

    # Inner function g(x)
    fig.add_trace(go.Scatter(
        x=x, y=np.clip(g_x, -20, 20),
        mode="lines",
        line={"color": COLORS["accent1"], "width": 2},
        name="g(x) - inner",
    ))

    # Composite f(g(x))
    fig.add_trace(go.Scatter(
        x=x, y=f_g_x,
        mode="lines",
        line={"color": COLORS["primary"], "width": 3},
        name="f(g(x)) - composite",
    ))

    # Derivative of composite
    fig.add_trace(go.Scatter(
        x=x, y=chain_deriv,
        mode="lines",
        line={"color": COLORS["secondary"], "width": 3},
        name="(f∘g)'(x) = f'(g(x))·g'(x)",
    ))

    fig.update_layout(
        **DARK_THEME,
        title=title,
        xaxis_title="x",
        yaxis_title="y",
        yaxis_range=[-10, 10],
        showlegend=True,
    )

    return fig


def animate_projectile_motion(
    v0: float = 20.0,
    angle: float = 45.0,
    g: float = 9.8,
    num_frames: int = 50,
) -> go.Figure:
    """
    Animate projectile motion showing position, velocity, and acceleration.

    Args:
        v0: Initial velocity (m/s)
        angle: Launch angle (degrees)
        g: Gravitational acceleration (m/s^2)
        num_frames: Number of animation frames

    Returns:
        Plotly Figure with animation
    """
    theta = np.radians(angle)
    vx = v0 * np.cos(theta)
    vy = v0 * np.sin(theta)

    # Time of flight
    t_flight = 2 * vy / g
    t = np.linspace(0, t_flight, num_frames)

    # Position
    x = vx * t
    y = vy * t - 0.5 * g * t ** 2

    # Velocity components
    vx_t = np.full_like(t, vx)
    vy_t = vy - g * t

    fig = go.Figure()

    # Trajectory
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode="lines",
        line={"color": COLORS["primary"], "width": 2, "dash": "dot"},
        name="Trajectory",
    ))

    # Current position
    fig.add_trace(go.Scatter(
        x=[x[0]], y=[y[0]],
        mode="markers",
        marker={"color": COLORS["quaternary"], "size": 15},
        name="Position",
    ))

    # Velocity vector (scaled)
    scale = 0.3
    fig.add_trace(go.Scatter(
        x=[x[0], x[0] + scale * vx_t[0]],
        y=[y[0], y[0] + scale * vy_t[0]],
        mode="lines+markers",
        line={"color": COLORS["secondary"], "width": 3},
        marker={"symbol": "arrow", "size": 10, "angleref": "previous"},
        name="Velocity",
    ))

    # Create frames
    frames = []
    for i in range(len(t)):
        frame = go.Frame(
            data=[
                go.Scatter(x=x[:i+1], y=y[:i+1]),  # Trajectory up to current point
                go.Scatter(x=[x[i]], y=[y[i]]),  # Position
                go.Scatter(
                    x=[x[i], x[i] + scale * vx_t[i]],
                    y=[y[i], y[i] + scale * vy_t[i]]
                ),  # Velocity vector
            ],
            name=str(i),
            layout={"title": f"t = {t[i]:.2f}s | v = ({vx_t[i]:.1f}, {vy_t[i]:.1f}) m/s"}
        )
        frames.append(frame)

    fig.frames = frames

    fig.update_layout(
        **DARK_THEME,
        title=f"Projectile Motion: v₀ = {v0} m/s, θ = {angle}°",
        xaxis_title="x (m)",
        yaxis_title="y (m)",
        yaxis_scaleanchor="x",
        yaxis_scaleratio=1,
        xaxis_range=[-1, max(x) * 1.1],
        yaxis_range=[-1, max(y) * 1.3],
        updatemenus=[{
            "type": "buttons",
            "showactive": False,
            "y": 1.15,
            "x": 0.5,
            "xanchor": "center",
            "buttons": [
                {
                    "label": "▶ Launch",
                    "method": "animate",
                    "args": [None, {"frame": {"duration": 50}, "transition": {"duration": 0}}]
                },
                {
                    "label": "⏸ Pause",
                    "method": "animate",
                    "args": [[None], {"frame": {"duration": 0}, "mode": "immediate"}]
                },
            ],
            "font": {"color": COLORS["text"]},
            "bgcolor": COLORS["paper"],
        }],
    )

    return fig


def create_optimization_plot(
    f: Callable[[float], float],
    f_prime: Callable[[float], float],
    f_double_prime: Callable[[float], float],
    x_range: tuple[float, float] = (-3, 3),
    num_points: int = 300,
) -> go.Figure:
    """
    Create visualization for finding maxima/minima with second derivative test.

    Args:
        f: Function
        f_prime: First derivative
        f_double_prime: Second derivative
        x_range: Range for x-axis
        num_points: Points for curves

    Returns:
        Plotly Figure showing function, critical points, and concavity
    """
    x = np.linspace(x_range[0], x_range[1], num_points)
    y = np.array([f(xi) for xi in x])
    y_prime = np.array([f_prime(xi) for xi in x])
    y_double_prime = np.array([f_double_prime(xi) for xi in x])

    # Find critical points (where f'(x) ≈ 0)
    critical_points = []
    for i in range(1, len(x)):
        if y_prime[i-1] * y_prime[i] < 0:  # Sign change
            # Linear interpolation to find zero
            x_crit = x[i-1] - y_prime[i-1] * (x[i] - x[i-1]) / (y_prime[i] - y_prime[i-1])
            y_crit = f(x_crit)
            d2 = f_double_prime(x_crit)
            point_type = "Maximum" if d2 < 0 else "Minimum" if d2 > 0 else "Inflection"
            critical_points.append((x_crit, y_crit, d2, point_type))

    fig = go.Figure()

    # Function
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode="lines",
        line={"color": COLORS["primary"], "width": 3},
        name="f(x)",
    ))

    # First derivative
    fig.add_trace(go.Scatter(
        x=x, y=y_prime,
        mode="lines",
        line={"color": COLORS["secondary"], "width": 2},
        name="f'(x)",
    ))

    # Second derivative
    fig.add_trace(go.Scatter(
        x=x, y=y_double_prime,
        mode="lines",
        line={"color": COLORS["tertiary"], "width": 2, "dash": "dash"},
        name="f''(x)",
    ))

    # Critical points
    for x_c, y_c, d2, ptype in critical_points:
        color = COLORS["accent2"] if ptype == "Maximum" else COLORS["accent1"] if ptype == "Minimum" else COLORS["quaternary"]
        fig.add_trace(go.Scatter(
            x=[x_c], y=[y_c],
            mode="markers+text",
            marker={"color": color, "size": 14, "symbol": "star"},
            text=[ptype],
            textposition="top center",
            textfont={"color": color},
            name=f"{ptype} at x={x_c:.2f}",
            hovertemplate=f"{ptype}<br>x = {x_c:.3f}<br>f(x) = {y_c:.3f}<br>f''(x) = {d2:.3f}<extra></extra>",
        ))

    # Zero line for reference
    fig.add_hline(y=0, line_dash="dot", line_color=COLORS["text_secondary"], opacity=0.5)

    fig.update_layout(
        **DARK_THEME,
        title="Optimization: Finding Extrema with Derivatives",
        xaxis_title="x",
        yaxis_title="y",
        showlegend=True,
    )

    return fig


def animate_area_accumulation(
    f: Callable[[float], float],
    x_range: tuple[float, float] = (0, 3),
    max_rectangles: int = 50,
) -> go.Figure:
    """
    Animate Riemann sum showing area accumulation (teaser for integration).

    Args:
        f: Function to integrate
        x_range: Integration bounds
        max_rectangles: Maximum number of rectangles in animation

    Returns:
        Plotly Figure with animation
    """
    a, b = x_range
    x_curve = np.linspace(a, b, 200)
    y_curve = np.array([f(xi) for xi in x_curve])

    fig = go.Figure()

    # Function curve
    fig.add_trace(go.Scatter(
        x=x_curve, y=y_curve,
        mode="lines",
        line={"color": COLORS["primary"], "width": 3},
        name="f(x)",
        fill="tozeroy",
        fillcolor="rgba(0, 212, 255, 0.1)",
    ))

    # Initial rectangles
    n = 5
    dx = (b - a) / n
    x_bars = [a + i * dx for i in range(n)]
    heights = [f(xi + dx/2) for xi in x_bars]  # Midpoint rule

    fig.add_trace(go.Bar(
        x=[xi + dx/2 for xi in x_bars],
        y=heights,
        width=dx * 0.95,
        marker_color=COLORS["tertiary"],
        opacity=0.6,
        name="Riemann sum",
    ))

    # Create frames with increasing number of rectangles
    rect_counts = [5, 8, 12, 18, 25, 35, 50]
    frames = []

    for n in rect_counts:
        dx = (b - a) / n
        x_bars = [a + i * dx for i in range(n)]
        heights = [f(xi + dx/2) for xi in x_bars]
        area = sum(h * dx for h in heights)

        frame = go.Frame(
            data=[
                go.Scatter(x=x_curve, y=y_curve, fill="tozeroy", fillcolor="rgba(0, 212, 255, 0.1)"),
                go.Bar(
                    x=[xi + dx/2 for xi in x_bars],
                    y=heights,
                    width=dx * 0.95,
                    marker_color=COLORS["tertiary"],
                    opacity=0.6,
                ),
            ],
            name=str(n),
            layout={"title": f"Riemann Sum: n = {n} rectangles, Area ≈ {area:.4f}"}
        )
        frames.append(frame)

    fig.frames = frames

    # Slider
    steps = [
        {"args": [[str(n)], {"frame": {"duration": 500, "redraw": True}, "mode": "immediate"}],
         "label": str(n), "method": "animate"}
        for n in rect_counts
    ]

    fig.update_layout(
        **DARK_THEME,
        title=f"Riemann Sum: n = 5 rectangles",
        xaxis_title="x",
        yaxis_title="y",
        barmode="overlay",
        sliders=[{
            "active": 0,
            "currentvalue": {"prefix": "Rectangles: ", "visible": True},
            "pad": {"b": 10, "t": 60},
            "steps": steps,
            "bgcolor": COLORS["paper"],
            "font": {"color": COLORS["text"]},
        }],
        updatemenus=[{
            "type": "buttons",
            "showactive": False,
            "y": 1.15,
            "x": 0.5,
            "xanchor": "center",
            "buttons": [
                {
                    "label": "▶ Refine",
                    "method": "animate",
                    "args": [None, {"frame": {"duration": 800}, "transition": {"duration": 300}}]
                }
            ],
            "font": {"color": COLORS["text"]},
            "bgcolor": COLORS["paper"],
        }],
    )

    return fig
