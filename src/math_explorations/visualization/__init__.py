"""Visualization module - Plotly animations and function plots."""

from .animations import (
    animate_area_accumulation,
    animate_chain_rule,
    animate_limit_process,
    animate_power_rule,
    animate_projectile_motion,
    create_optimization_plot,
    create_secant_to_tangent,
    create_tangent_line_plot,
)
from .charts import create_timeline
from .function_plots import (
    plot_derivative_comparison,
    plot_directed_graph,
    plot_function,
    plot_secant_line,
    plot_tangent_line,
    plot_unit_circle,
    plot_venn_diagram,
)
from .styles import (
    COLORS,
    DARK_THEME,
    SCENE_THEME,
    apply_dark_theme,
    base_layout,
    get_color_palette,
    style_subplot_axes,
)

__all__ = [
    "COLORS",
    "DARK_THEME",
    "SCENE_THEME",
    "animate_area_accumulation",
    "animate_chain_rule",
    "animate_limit_process",
    "animate_power_rule",
    "animate_projectile_motion",
    "apply_dark_theme",
    "base_layout",
    "create_optimization_plot",
    "create_secant_to_tangent",
    "create_tangent_line_plot",
    "create_timeline",
    "get_color_palette",
    "plot_derivative_comparison",
    "plot_directed_graph",
    "plot_function",
    "plot_secant_line",
    "plot_tangent_line",
    "plot_unit_circle",
    "plot_venn_diagram",
    "style_subplot_axes",
]
