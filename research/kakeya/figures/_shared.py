"""Shared helpers for Kakeya figure experiments.

Every figure file imports from here so geometry, validation, and styling are defined once (no
duplication across figures). Run any figure with the ephemeral deps:

    uv run --with matplotlib --with shapely python research/kakeya/figures/<name>.py

Design split (so the work ports to the notebook cleanly):
  * GEOMETRY   -> pure numpy, no plotting.  This is the part that gets re-expressed in plotly in the
                  actual marimo notebook.  Keep it framework-free.
  * VALIDATION -> shapely (exact polygon area / overlap) + analytic checks.  Offline only.
  * PREVIEW    -> matplotlib PNG next to the figure file.  Offline only, just to eyeball the form.

A figure is "valid" when its printed MATH CHECK block matches the formulas in ../kakeya.md.
"""
from __future__ import annotations

import inspect
import math
import os

import numpy as np

# --- palette (mirror the article conventions; see ../links.md) -------------------------
COLORS = {
    "needle": "#1f77b4",   # unit segments / the family
    "region": "#9ecae1",   # swept area, faint
    "accent": "#d62728",   # inner/thin tubes, grains (Guth uses red)
    "outer": "#3457d5",    # thick/outer tubes (Guth uses blue)
    "guide": "#555555",    # arrows, axes, wireframe
    "muted": "#999999",
}
SQRT3 = math.sqrt(3.0)


# =====================================================================================
# GEOMETRY (pure numpy, portable)
# =====================================================================================
def equilateral(base: float = 1.0, x0: float = 0.0, y0: float = 0.0) -> np.ndarray:
    """Vertices of an equilateral triangle, base [x0, x0+base] on y=y0, apex above the middle.
    Apex angle = 60 deg, so it carries unit segments over a 60 deg fan of directions."""
    h = SQRT3 / 2.0 * base
    return np.array([[x0, y0], [x0 + base, y0], [x0 + base / 2.0, y0 + h]])


def unit_needle(cx: float, cy: float, angle_rad: float, length: float = 1.0) -> np.ndarray:
    """Endpoints of a straight needle of fixed `length` centred at (cx, cy) at `angle_rad`."""
    dx, dy = 0.5 * length * math.cos(angle_rad), 0.5 * length * math.sin(angle_rad)
    return np.array([[cx - dx, cy - dy], [cx + dx, cy + dy]])


def deltoid(b: float = 0.25, n: int = 400) -> np.ndarray:
    """Three-cusped hypocycloid, rolling radius b (tangent chord length 4b, enclosed area 2*pi*b^2).
    For a unit needle use b = 1/4 -> chord 1, area pi/8."""
    t = np.linspace(0, 2 * math.pi, n, endpoint=False)  # no duplicate closing vertex
    return np.column_stack([2 * b * np.cos(t) + b * np.cos(2 * t),
                            2 * b * np.sin(t) - b * np.sin(2 * t)])


def circle(r: float = 0.5, n: int = 400, cx: float = 0.0, cy: float = 0.0) -> np.ndarray:
    t = np.linspace(0, 2 * math.pi, n, endpoint=False)  # no duplicate closing vertex
    return np.column_stack([cx + r * np.cos(t), cy + r * np.sin(t)])


def triangle_fan_degrees(tri: np.ndarray) -> tuple[float, float]:
    """Range of directions (deg, in [0,180)) of segments from the base edge to the apex.
    `tri` rows: [baseL, baseR, apex]."""
    (bl, br, ap) = tri
    a1 = math.degrees(math.atan2(ap[1] - bl[1], ap[0] - bl[0])) % 180.0
    a2 = math.degrees(math.atan2(ap[1] - br[1], ap[0] - br[0])) % 180.0
    return (min(a1, a2), max(a1, a2))


# =====================================================================================
# VALIDATION (shapely + analytic)
# =====================================================================================
def poly(points: np.ndarray):
    from shapely.geometry import Polygon

    return Polygon([tuple(p) for p in points])


def union_area(polys) -> float:
    from shapely.ops import unary_union

    return unary_union(list(polys)).area


# =====================================================================================
# PREVIEW + REPORTING
# =====================================================================================
def new_axes(ncols: int = 1, figsize=None):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, ncols, figsize=figsize or (5.5 * ncols, 5.5))
    axes = np.atleast_1d(axes)
    for ax in axes:
        ax.set_aspect("equal")
        ax.axis("off")
    return fig, (axes[0] if ncols == 1 else axes)


def save_preview(fig, dpi: int = 140) -> str:
    """Save `<callerfile>.png` next to the calling figure module and return the path."""
    caller = inspect.stack()[1].filename
    out = os.path.splitext(caller)[0] + ".png"
    fig.tight_layout()
    fig.savefig(out, dpi=dpi)
    return out


def save_gif(anim, fps: int = 20, dpi: int = 100) -> str:
    """Save `<callerfile>.gif` next to the calling module via PillowWriter; return the path.
    Keep frames modest (<= ~120) and dpi ~100 so GIFs stay a few MB."""
    from matplotlib.animation import PillowWriter

    caller = inspect.stack()[1].filename
    out = os.path.splitext(caller)[0] + ".gif"
    anim.save(out, writer=PillowWriter(fps=fps), dpi=dpi)
    return out


def math_check(title: str, rows: list[tuple[str, str]]) -> None:
    """Print a standardized validation block: (claim, value/verdict) rows."""
    print(f"\n=== MATH CHECK: {title} ===")
    w = max((len(r[0]) for r in rows), default=0)
    for claim, value in rows:
        print(f"  {claim.ljust(w)} : {value}")
    print("=" * (len(title) + 18))
