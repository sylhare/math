"""Function visualization utilities."""

from typing import Callable
import numpy as np
import plotly.graph_objects as go
from .styles import DARK_THEME, COLORS, get_trace_style


def plot_function(
    f: Callable[[np.ndarray], np.ndarray],
    x_range: tuple[float, float] = (-5, 5),
    num_points: int = 500,
    title: str = "",
    x_label: str = "x",
    y_label: str = "y",
    name: str = "f(x)",
    show_grid: bool = True,
) -> go.Figure:
    """
    Create a plot of a single function.

    Args:
        f: Function to plot
        x_range: (min, max) for x-axis
        num_points: Number of points to plot
        title: Plot title
        x_label: Label for x-axis
        y_label: Label for y-axis
        name: Name for legend
        show_grid: Whether to show grid lines

    Returns:
        Plotly Figure object
    """
    x = np.linspace(x_range[0], x_range[1], num_points)

    # Handle potential discontinuities
    with np.errstate(divide="ignore", invalid="ignore"):
        y = f(x)
        y = np.where(np.abs(y) > 1e10, np.nan, y)

    fig = go.Figure()

    style = get_trace_style("function")
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode=style["mode"],
        line=style["line"],
        name=name,
        hovertemplate=f"{name}: (%{{x:.3f}}, %{{y:.3f}})<extra></extra>",
    ))

    fig.update_layout(
        **DARK_THEME,
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        showlegend=True,
        hovermode="closest",
    )

    if not show_grid:
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)

    return fig


def plot_derivative_comparison(
    f: Callable[[np.ndarray], np.ndarray],
    f_prime: Callable[[np.ndarray], np.ndarray],
    x_range: tuple[float, float] = (-5, 5),
    num_points: int = 500,
    title: str = "Function and Its Derivative",
    f_name: str = "f(x)",
    f_prime_name: str = "f'(x)",
) -> go.Figure:
    """
    Plot a function alongside its derivative.

    Args:
        f: Original function
        f_prime: Derivative function
        x_range: (min, max) for x-axis
        num_points: Number of points
        title: Plot title
        f_name: Name for function in legend
        f_prime_name: Name for derivative in legend

    Returns:
        Plotly Figure object
    """
    x = np.linspace(x_range[0], x_range[1], num_points)

    with np.errstate(divide="ignore", invalid="ignore"):
        y = f(x)
        y_prime = f_prime(x)
        y = np.where(np.abs(y) > 1e10, np.nan, y)
        y_prime = np.where(np.abs(y_prime) > 1e10, np.nan, y_prime)

    fig = go.Figure()

    # Original function
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode="lines",
        line={"color": COLORS["primary"], "width": 3},
        name=f_name,
        hovertemplate=f"{f_name}: (%{{x:.3f}}, %{{y:.3f}})<extra></extra>",
    ))

    # Derivative
    fig.add_trace(go.Scatter(
        x=x,
        y=y_prime,
        mode="lines",
        line={"color": COLORS["secondary"], "width": 3},
        name=f_prime_name,
        hovertemplate=f"{f_prime_name}: (%{{x:.3f}}, %{{y:.3f}})<extra></extra>",
    ))

    fig.update_layout(
        **DARK_THEME,
        title=title,
        xaxis_title="x",
        yaxis_title="y",
        showlegend=True,
        hovermode="x unified",
    )

    return fig


def plot_tangent_line(
    f: Callable[[float], float],
    f_prime: Callable[[float], float],
    x0: float,
    x_range: tuple[float, float] = (-5, 5),
    num_points: int = 500,
    title: str = "",
    tangent_extent: float = 2.0,
) -> go.Figure:
    """
    Plot a function with a tangent line at a specific point.

    Args:
        f: Function to plot
        f_prime: Derivative function
        x0: Point of tangency
        x_range: (min, max) for x-axis
        num_points: Number of points
        title: Plot title
        tangent_extent: How far tangent line extends from point

    Returns:
        Plotly Figure object
    """
    x = np.linspace(x_range[0], x_range[1], num_points)

    with np.errstate(divide="ignore", invalid="ignore"):
        y = np.array([f(xi) for xi in x])
        y = np.where(np.abs(y) > 1e10, np.nan, y)

    y0 = f(x0)
    slope = f_prime(x0)

    # Tangent line: y - y0 = slope * (x - x0)
    x_tangent = np.array([x0 - tangent_extent, x0 + tangent_extent])
    y_tangent = y0 + slope * (x_tangent - x0)

    fig = go.Figure()

    # Function
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode="lines",
        line={"color": COLORS["primary"], "width": 3},
        name="f(x)",
    ))

    # Tangent line
    fig.add_trace(go.Scatter(
        x=x_tangent,
        y=y_tangent,
        mode="lines",
        line={"color": COLORS["tertiary"], "width": 2, "dash": "dash"},
        name=f"Tangent at x={x0}",
    ))

    # Point of tangency
    fig.add_trace(go.Scatter(
        x=[x0],
        y=[y0],
        mode="markers",
        marker={"color": COLORS["quaternary"], "size": 12, "symbol": "circle"},
        name=f"({x0:.2f}, {y0:.2f})",
        hovertemplate=f"Point: ({x0:.3f}, {y0:.3f})<br>Slope: {slope:.3f}<extra></extra>",
    ))

    if not title:
        title = f"Tangent Line at x = {x0} (slope = {slope:.3f})"

    fig.update_layout(
        **DARK_THEME,
        title=title,
        xaxis_title="x",
        yaxis_title="y",
        showlegend=True,
    )

    return fig


def plot_secant_line(
    f: Callable[[float], float],
    x0: float,
    x1: float,
    x_range: tuple[float, float] = (-5, 5),
    num_points: int = 500,
    title: str = "",
) -> go.Figure:
    """
    Plot a function with a secant line between two points.

    Args:
        f: Function to plot
        x0: First x-coordinate
        x1: Second x-coordinate
        x_range: (min, max) for x-axis
        num_points: Number of points
        title: Plot title

    Returns:
        Plotly Figure object
    """
    x = np.linspace(x_range[0], x_range[1], num_points)

    with np.errstate(divide="ignore", invalid="ignore"):
        y = np.array([f(xi) for xi in x])
        y = np.where(np.abs(y) > 1e10, np.nan, y)

    y0, y1 = f(x0), f(x1)
    slope = (y1 - y0) / (x1 - x0) if x1 != x0 else 0

    # Extend secant line slightly beyond points
    padding = 0.5
    x_secant = np.array([x0 - padding, x1 + padding])
    y_secant = y0 + slope * (x_secant - x0)

    fig = go.Figure()

    # Function
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode="lines",
        line={"color": COLORS["primary"], "width": 3},
        name="f(x)",
    ))

    # Secant line
    fig.add_trace(go.Scatter(
        x=x_secant,
        y=y_secant,
        mode="lines",
        line={"color": COLORS["quaternary"], "width": 2, "dash": "dot"},
        name="Secant line",
    ))

    # Points
    fig.add_trace(go.Scatter(
        x=[x0, x1],
        y=[y0, y1],
        mode="markers",
        marker={"color": COLORS["secondary"], "size": 10},
        name="Endpoints",
        hovertemplate="(%{x:.3f}, %{y:.3f})<extra></extra>",
    ))

    if not title:
        title = f"Secant Line: slope = {slope:.4f}"

    fig.update_layout(
        **DARK_THEME,
        title=title,
        xaxis_title="x",
        yaxis_title="y",
        showlegend=True,
    )

    return fig


def plot_multiple_functions(
    functions: list[tuple[Callable, str]],
    x_range: tuple[float, float] = (-5, 5),
    num_points: int = 500,
    title: str = "",
) -> go.Figure:
    """
    Plot multiple functions on the same axes.

    Args:
        functions: List of (function, name) tuples
        x_range: (min, max) for x-axis
        num_points: Number of points
        title: Plot title

    Returns:
        Plotly Figure object
    """
    x = np.linspace(x_range[0], x_range[1], num_points)
    colors = [
        COLORS["primary"], COLORS["secondary"], COLORS["tertiary"],
        COLORS["quaternary"], COLORS["accent1"], COLORS["accent2"],
    ]

    fig = go.Figure()

    for i, (f, name) in enumerate(functions):
        with np.errstate(divide="ignore", invalid="ignore"):
            y = np.array([f(xi) for xi in x])
            y = np.where(np.abs(y) > 1e10, np.nan, y)

        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            mode="lines",
            line={"color": colors[i % len(colors)], "width": 3},
            name=name,
        ))

    fig.update_layout(
        **DARK_THEME,
        title=title,
        xaxis_title="x",
        yaxis_title="y",
        showlegend=True,
    )

    return fig
