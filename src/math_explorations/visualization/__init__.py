"""Visualization module - Plotly animations and function plots."""

from .styles import DARK_THEME, apply_dark_theme, get_color_palette
from .function_plots import (
    plot_function,
    plot_derivative_comparison,
    plot_tangent_line,
    plot_secant_line,
)
from .animations import (
    create_secant_to_tangent,
    animate_limit_process,
    create_tangent_line_plot,
    animate_power_rule,
    animate_chain_rule,
    animate_projectile_motion,
    create_optimization_plot,
    animate_area_accumulation,
)

__all__ = [
    "DARK_THEME",
    "apply_dark_theme",
    "get_color_palette",
    "plot_function",
    "plot_derivative_comparison",
    "plot_tangent_line",
    "plot_secant_line",
    "create_secant_to_tangent",
    "animate_limit_process",
    "create_tangent_line_plot",
    "animate_power_rule",
    "animate_chain_rule",
    "animate_projectile_motion",
    "create_optimization_plot",
    "animate_area_accumulation",
]
