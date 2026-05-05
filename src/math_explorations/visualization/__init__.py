"""Visualization module - Plotly animations and function plots."""

from .styles import (
    COLORS,
    DARK_THEME,
    SCENE_THEME,
    apply_dark_theme,
    base_layout,
    get_color_palette,
    style_subplot_axes,
)
from .charts import create_timeline
from .function_plots import (
    plot_function,
    plot_derivative_comparison,
    plot_tangent_line,
    plot_secant_line,
    plot_directed_graph,
    plot_venn_diagram,
    plot_unit_circle,
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
    "COLORS",
    "DARK_THEME",
    "SCENE_THEME",
    "apply_dark_theme",
    "base_layout",
    "get_color_palette",
    "style_subplot_axes",
    "create_timeline",
    "plot_function",
    "plot_derivative_comparison",
    "plot_tangent_line",
    "plot_secant_line",
    "plot_directed_graph",
    "plot_venn_diagram",
    "plot_unit_circle",
    "create_secant_to_tangent",
    "animate_limit_process",
    "create_tangent_line_plot",
    "animate_power_rule",
    "animate_chain_rule",
    "animate_projectile_motion",
    "create_optimization_plot",
    "animate_area_accumulation",
]
