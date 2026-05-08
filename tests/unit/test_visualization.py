from math_explorations.visualization.animations import create_secant_to_tangent, create_tangent_line_plot
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
