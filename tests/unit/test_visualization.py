from math_explorations.visualization.animations import (
    animate_area_accumulation,
    animate_chain_rule,
    animate_limit_process,
    animate_power_rule,
    animate_projectile_motion,
    create_optimization_plot,
    create_secant_to_tangent,
    create_tangent_line_plot,
)
from math_explorations.visualization.function_plots import plot_derivative_comparison, plot_function
from math_explorations.visualization.styles import COLORS, base_layout, get_color_palette, get_trace_style


def test_get_color_palette():
    palette = get_color_palette()
    assert len(palette) >= 4
    assert COLORS["primary"] in palette


def test_get_trace_style():
    func_style = get_trace_style("function")
    assert func_style["line"]["color"] == COLORS["primary"]

    deriv_style = get_trace_style("derivative")
    assert deriv_style["line"]["color"] == COLORS["secondary"]

    unknown_style = get_trace_style("unknown")
    assert unknown_style == get_trace_style("function")


def test_base_layout():
    layout = base_layout(title="Test Title", height=500)
    assert layout["paper_bgcolor"] == COLORS["background"]
    assert layout["title"] == "Test Title"
    assert layout["height"] == 500


def test_plot_function():
    f = lambda x: x**2
    fig = plot_function(f, x_range=(-2, 2), title="Square")
    assert len(fig.data) == 1
    assert fig.data[0].name == "f(x)"
    assert fig.layout.title.text == "Square"


def test_plot_derivative_comparison():
    f = lambda x: x**2
    df = lambda x: 2 * x
    fig = plot_derivative_comparison(f, df, title="Comparison")
    assert len(fig.data) == 2
    assert fig.data[0].name == "f(x)"
    assert fig.data[1].name == "f'(x)"


def test_create_secant_to_tangent():
    f = lambda x: x**2
    df = lambda x: 2 * x
    fig = create_secant_to_tangent(f, df, x0=1.0)
    assert len(fig.data) >= 3
    assert "sliders" in fig.layout
    assert fig.layout.sliders[0].steps[0].label == "2.00"


def test_create_tangent_line_plot():
    f = lambda x: x**2
    df = lambda x: 2 * x
    fig = create_tangent_line_plot(f, df, initial_x=1.0)
    assert len(fig.data) == 3
    assert "sliders" in fig.layout


def test_animate_limit_process():
    fig = animate_limit_process(lambda x: x**2, lambda x: 2 * x, x0=1.0)
    assert len(fig.data) >= 1
    assert len(fig.frames) > 0


def test_animate_power_rule():
    fig = animate_power_rule(max_n=4)
    assert len(fig.data) >= 1
    assert len(fig.frames) > 0


def test_animate_chain_rule():
    import numpy as np

    fig = animate_chain_rule(np.sin, lambda x: x**2, np.cos, lambda x: 2 * x)
    assert len(fig.data) >= 1
    assert fig.layout.title.text


def test_animate_projectile_motion():
    fig = animate_projectile_motion(v0=20.0, angle=45.0)
    assert len(fig.data) >= 1
    assert fig.layout.title.text


def test_create_optimization_plot():
    fig = create_optimization_plot(lambda x: x**3 - 3 * x, lambda x: 3 * x**2 - 3, lambda x: 6 * x)
    assert len(fig.data) >= 1
    assert fig.layout.title.text


def test_animate_area_accumulation():
    # Regression: DARK_THEME already carries a "title" key, so passing title=
    # in the same update_layout call raised TypeError. Must build without error.
    fig = animate_area_accumulation(lambda x: x**2, x_range=(0, 2))
    assert len(fig.data) >= 1
    assert len(fig.frames) > 0
    assert fig.layout.title.text == "Riemann Sum: n = 5 rectangles"
