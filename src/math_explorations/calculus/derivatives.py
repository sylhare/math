"""Symbolic derivative computations using SymPy."""

from typing import Callable
import sympy as sp
from sympy import Symbol, Expr, diff, simplify, latex, lambdify


def derivative(expr: Expr | str, var: Symbol | str = "x") -> Expr:
    """
    Compute the derivative of an expression.

    Args:
        expr: SymPy expression or string to differentiate
        var: Variable to differentiate with respect to

    Returns:
        The derivative as a SymPy expression
    """
    if isinstance(var, str):
        var = sp.Symbol(var)
    if isinstance(expr, str):
        expr = sp.sympify(expr)
    return simplify(diff(expr, var))


def nth_derivative(expr: Expr | str, var: Symbol | str = "x", n: int = 1) -> Expr:
    """
    Compute the nth derivative of an expression.

    Args:
        expr: SymPy expression or string to differentiate
        var: Variable to differentiate with respect to
        n: Order of derivative

    Returns:
        The nth derivative as a SymPy expression
    """
    if isinstance(var, str):
        var = sp.Symbol(var)
    if isinstance(expr, str):
        expr = sp.sympify(expr)
    return simplify(diff(expr, var, n))


def partial_derivative(expr: Expr | str, *vars: Symbol | str) -> Expr:
    """
    Compute partial derivatives with respect to multiple variables.

    Args:
        expr: SymPy expression or string
        vars: Variables to differentiate with respect to (in order)

    Returns:
        The partial derivative as a SymPy expression
    """
    if isinstance(expr, str):
        expr = sp.sympify(expr)

    result = expr
    for var in vars:
        if isinstance(var, str):
            var = sp.Symbol(var)
        result = diff(result, var)
    return simplify(result)


def derivative_at_point(
    expr: Expr | str,
    var: Symbol | str = "x",
    point: float = 0.0
) -> float:
    """
    Evaluate the derivative at a specific point.

    Args:
        expr: SymPy expression or string
        var: Variable to differentiate with respect to
        point: Point at which to evaluate

    Returns:
        Numerical value of the derivative at the point
    """
    if isinstance(var, str):
        var = sp.Symbol(var)
    if isinstance(expr, str):
        expr = sp.sympify(expr)

    deriv = derivative(expr, var)
    return float(deriv.subs(var, point))


def symbolic_derivative_steps(expr: Expr | str, var: Symbol | str = "x") -> list[dict]:
    """
    Show step-by-step derivative computation.

    Args:
        expr: SymPy expression or string
        var: Variable to differentiate with respect to

    Returns:
        List of dictionaries with 'rule', 'expression', and 'latex' keys
    """
    if isinstance(var, str):
        var = sp.Symbol(var)
    if isinstance(expr, str):
        expr = sp.sympify(expr)

    steps = []

    # Initial expression
    steps.append({
        "rule": "Original function",
        "expression": expr,
        "latex": latex(expr),
    })

    # Compute derivative
    deriv = diff(expr, var)

    # Identify the rule used (simplified detection)
    rule_name = _identify_rule(expr, var)

    steps.append({
        "rule": rule_name,
        "expression": deriv,
        "latex": latex(deriv),
    })

    # Simplified form
    simplified = simplify(deriv)
    if simplified != deriv:
        steps.append({
            "rule": "Simplify",
            "expression": simplified,
            "latex": latex(simplified),
        })

    return steps


def _identify_rule(expr: Expr, var: Symbol) -> str:
    """Identify which differentiation rule applies."""
    if expr.is_polynomial(var):
        if expr.is_Pow and expr.exp.is_number:
            return "Power Rule: d/dx[x^n] = nx^(n-1)"
        return "Power Rule (polynomial)"

    if expr.is_Add:
        return "Sum Rule: d/dx[f + g] = f' + g'"

    if expr.is_Mul:
        # Check if it's a constant times a function
        const_part = [arg for arg in expr.args if arg.is_number]
        if const_part:
            return "Constant Multiple Rule: d/dx[cf] = c·f'"
        return "Product Rule: d/dx[fg] = f'g + fg'"

    if expr.is_Pow:
        base, exp = expr.as_base_exp()
        if base == sp.E:
            return "Exponential Rule: d/dx[e^x] = e^x"
        if var in exp.free_symbols:
            return "Logarithmic Differentiation"
        return "Power Rule"

    func_name = expr.func.__name__ if hasattr(expr, "func") else ""
    rules = {
        "sin": "Trig Rule: d/dx[sin(x)] = cos(x)",
        "cos": "Trig Rule: d/dx[cos(x)] = -sin(x)",
        "tan": "Trig Rule: d/dx[tan(x)] = sec²(x)",
        "log": "Log Rule: d/dx[ln(x)] = 1/x",
        "exp": "Exponential Rule: d/dx[e^x] = e^x",
    }

    if func_name in rules:
        # Check if chain rule needed
        if expr.args and expr.args[0] != var:
            return f"{rules[func_name]} + Chain Rule"
        return rules[func_name]

    return "Differentiation"


def create_derivative_function(expr: Expr | str, var: Symbol | str = "x") -> Callable:
    """
    Create a numerical function for the derivative.

    Args:
        expr: SymPy expression or string
        var: Variable

    Returns:
        Callable function that computes the derivative numerically
    """
    if isinstance(var, str):
        var = sp.Symbol(var)
    if isinstance(expr, str):
        expr = sp.sympify(expr)

    deriv = derivative(expr, var)
    return lambdify(var, deriv, modules=["numpy"])


def create_function(expr: Expr | str, var: Symbol | str = "x") -> Callable:
    """
    Create a numerical function from a SymPy expression.

    Args:
        expr: SymPy expression or string
        var: Variable

    Returns:
        Callable function for numerical evaluation
    """
    if isinstance(var, str):
        var = sp.Symbol(var)
    if isinstance(expr, str):
        expr = sp.sympify(expr)

    return lambdify(var, expr, modules=["numpy"])
