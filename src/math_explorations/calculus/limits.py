"""Limit calculations for derivative foundations."""

from typing import Callable
import numpy as np
import sympy as sp
from sympy import Symbol, Expr, limit as sp_limit, oo, latex


def limit(
    expr: Expr | str,
    var: Symbol | str,
    point: float | Expr,
    direction: str = "+-"
) -> Expr:
    """
    Compute the limit of an expression.

    Args:
        expr: SymPy expression or string
        var: Variable approaching the limit
        point: Value being approached (can be oo for infinity)
        direction: '+' for right, '-' for left, '+-' for both

    Returns:
        The limit as a SymPy expression
    """
    if isinstance(var, str):
        var = sp.Symbol(var)
    if isinstance(expr, str):
        expr = sp.sympify(expr)

    return sp_limit(expr, var, point, direction)


def limit_definition_derivative(
    expr: Expr | str,
    var: Symbol | str = "x",
    point: Symbol | str | float | None = None
) -> Expr:
    """
    Compute derivative using limit definition: lim[h→0] (f(x+h) - f(x))/h

    Args:
        expr: SymPy expression or string
        var: Variable
        point: Optional point to evaluate at (returns expression if None)

    Returns:
        The derivative computed via limit definition
    """
    if isinstance(var, str):
        var = sp.Symbol(var)
    if isinstance(expr, str):
        expr = sp.sympify(expr)

    h = sp.Symbol("h")

    # f(x+h)
    f_plus_h = expr.subs(var, var + h)

    # Difference quotient
    diff_quotient = (f_plus_h - expr) / h

    # Take limit as h → 0
    deriv = sp_limit(diff_quotient, h, 0)

    if point is not None:
        return deriv.subs(var, point)
    return deriv


def secant_slope(
    f: Callable[[float], float],
    x: float,
    h: float
) -> float:
    """
    Calculate the slope of a secant line.

    Args:
        f: Function to evaluate
        x: Base x-coordinate
        h: Distance to second point

    Returns:
        Slope of the secant line: (f(x+h) - f(x)) / h
    """
    if abs(h) < 1e-15:
        raise ValueError("h is too small, would cause numerical instability")
    return (f(x + h) - f(x)) / h


def tangent_slope(
    f: Callable[[float], float],
    x: float,
    h: float = 1e-8
) -> float:
    """
    Approximate the slope of the tangent line using central difference.

    Args:
        f: Function to evaluate
        x: Point of tangency
        h: Small step for numerical derivative

    Returns:
        Approximate slope of the tangent line
    """
    return (f(x + h) - f(x - h)) / (2 * h)


def secant_slopes_sequence(
    f: Callable[[float], float],
    x: float,
    h_values: list[float] | None = None
) -> list[dict]:
    """
    Generate a sequence of secant slopes approaching the tangent.

    Args:
        f: Function to evaluate
        x: Base x-coordinate
        h_values: List of h values (defaults to decreasing sequence)

    Returns:
        List of dicts with 'h', 'slope', 'x2', 'y1', 'y2' keys
    """
    if h_values is None:
        h_values = [1.0, 0.5, 0.25, 0.1, 0.05, 0.01, 0.001, 0.0001]

    y1 = f(x)
    results = []

    for h in h_values:
        x2 = x + h
        y2 = f(x2)
        slope = (y2 - y1) / h

        results.append({
            "h": h,
            "slope": slope,
            "x1": x,
            "x2": x2,
            "y1": y1,
            "y2": y2,
        })

    return results


def difference_quotient_expression(expr: Expr | str, var: Symbol | str = "x") -> dict:
    """
    Create the difference quotient expression for display.

    Args:
        expr: SymPy expression
        var: Variable

    Returns:
        Dict with 'numerator', 'denominator', 'full', and 'latex' keys
    """
    if isinstance(var, str):
        var = sp.Symbol(var)
    if isinstance(expr, str):
        expr = sp.sympify(expr)

    h = sp.Symbol("h")
    f_plus_h = expr.subs(var, var + h)

    numerator = f_plus_h - expr
    denominator = h
    full = numerator / denominator

    return {
        "numerator": numerator,
        "denominator": denominator,
        "full": full,
        "simplified": sp.simplify(full),
        "latex_full": latex(full),
        "latex_simplified": latex(sp.simplify(full)),
    }


def numerical_limit_table(
    f: Callable[[float], float],
    x: float,
    approaching: str = "both"
) -> list[dict]:
    """
    Create a table showing function values approaching a limit.

    Args:
        f: Function to evaluate
        x: Point being approached
        approaching: 'left', 'right', or 'both'

    Returns:
        List of dicts with 'x' and 'f(x)' values
    """
    offsets = [1, 0.5, 0.1, 0.05, 0.01, 0.005, 0.001, 0.0001]
    results = []

    if approaching in ("left", "both"):
        for offset in reversed(offsets):
            xi = x - offset
            try:
                yi = f(xi)
                results.append({"x": xi, "f(x)": yi, "direction": "left"})
            except (ValueError, ZeroDivisionError):
                results.append({"x": xi, "f(x)": "undefined", "direction": "left"})

    if approaching in ("right", "both"):
        for offset in offsets:
            xi = x + offset
            try:
                yi = f(xi)
                results.append({"x": xi, "f(x)": yi, "direction": "right"})
            except (ValueError, ZeroDivisionError):
                results.append({"x": xi, "f(x)": "undefined", "direction": "right"})

    return results
