import pytest
import sympy as sp
import numpy as np
from math_explorations.calculus.derivatives import (
    derivative,
    nth_derivative,
    partial_derivative,
    derivative_at_point,
    symbolic_derivative_steps,
    create_derivative_function,
    create_function
)
from math_explorations.calculus.limits import (
    limit,
    limit_definition_derivative,
    secant_slope,
    tangent_slope,
    secant_slopes_sequence,
    difference_quotient_expression,
    numerical_limit_table
)

def test_derivative_basic():
    x = sp.Symbol("x")
    expr = x**2
    assert derivative(expr, x) == 2*x
    assert derivative("x**3", "x") == 3*x**2

def test_nth_derivative():
    x = sp.Symbol("x")
    assert nth_derivative(x**3, x, 2) == 6*x
    assert nth_derivative("sin(x)", "x", 2) == -sp.sin(x)

def test_partial_derivative():
    x, y = sp.symbols("x y")
    expr = x**2 * y + y**3
    assert partial_derivative(expr, x) == 2*x*y
    assert partial_derivative(expr, y) == x**2 + 3*y**2
    assert partial_derivative(expr, x, y) == 2*x

def test_derivative_at_point():
    assert derivative_at_point("x**2", "x", 3.0) == 6.0
    assert derivative_at_point("sin(x)", "x", 0.0) == 1.0

def test_symbolic_derivative_steps():
    steps = symbolic_derivative_steps("x**2", "x")
    assert len(steps) >= 2
    assert steps[0]["rule"] == "Original function"
    assert "Power Rule" in steps[1]["rule"]

def test_limit_basic():
    x = sp.Symbol("x")
    assert limit("sin(x)/x", x, 0) == 1
    assert limit(1/x, x, sp.oo) == 0

def test_limit_definition_derivative():
    x = sp.Symbol("x")
    assert limit_definition_derivative("x**2", x) == 2*x
    assert limit_definition_derivative("x**2", x, 3) == 6

def test_secant_slope():
    f = lambda x: x**2
    assert secant_slope(f, 1.0, 0.1) == pytest.approx(2.1)
    with pytest.raises(ValueError, match="h is too small"):
        secant_slope(f, 1.0, 1e-16)

def test_tangent_slope():
    f = lambda x: x**2
    assert tangent_slope(f, 2.0) == pytest.approx(4.0)

def test_secant_slopes_sequence():
    f = lambda x: x**2
    results = secant_slopes_sequence(f, 1.0, [0.1, 0.01])
    assert len(results) == 2
    assert results[0]["h"] == 0.1
    assert results[0]["slope"] == pytest.approx(2.1)

def test_difference_quotient_expression():
    x = sp.Symbol("x")
    h = sp.Symbol("h")
    res = difference_quotient_expression("x**2", x)
    assert res["numerator"] == (x + h)**2 - x**2
    assert res["simplified"] == 2*x + h

def test_numerical_limit_table():
    f = lambda x: x**2
    res = numerical_limit_table(f, 2.0, approaching="both")
    # 8 offsets for left, 8 for right = 16
    assert len(res) == 16
    assert res[0]["direction"] == "left"
    assert res[-1]["direction"] == "right"

def test_create_functions():
    f = create_function("x**2", "x")
    assert f(3) == 9
    
    df = create_derivative_function("x**2", "x")
    assert df(3) == 6
