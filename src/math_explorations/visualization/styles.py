"""Consistent dark theme styling for all visualizations."""

from typing import Any

# Dark theme color palette
COLORS = {
    "background": "#1a1a2e",
    "paper": "#16213e",
    "text": "#eaeaea",
    "text_secondary": "#a0a0a0",
    "grid": "#2d3a4f",
    "primary": "#00d4ff",  # Cyan - main function
    "secondary": "#ff6b6b",  # Coral - derivative
    "tertiary": "#4ecdc4",  # Teal - tangent lines
    "quaternary": "#ffe66d",  # Yellow - points of interest
    "accent1": "#95e1d3",  # Mint
    "accent2": "#f38181",  # Salmon
    "accent3": "#aa96da",  # Lavender
    "accent4": "#fcbad3",  # Pink
    "highlight": "#ffd93d",  # Gold - highlights and labels
    "muted": "#4a5568",  # Dark gray - subtle lines
    "surface": "#2a2a3e",  # Dark navy - card/surface backgrounds
    "muted_fill": "rgba(100,100,100,0.3)",  # Translucent gray - empty/neutral fill regions
}

# Plotly layout template
DARK_THEME: dict[str, Any] = {
    "paper_bgcolor": COLORS["background"],
    "plot_bgcolor": COLORS["paper"],
    "font": {
        "family": "JetBrains Mono, Fira Code, monospace",
        "size": 14,
        "color": COLORS["text"],
    },
    "title": {
        "font": {
            "size": 20,
            "color": COLORS["text"],
        },
        "x": 0.5,
        "xanchor": "center",
    },
    "xaxis": {
        "gridcolor": COLORS["grid"],
        "gridwidth": 1,
        "zerolinecolor": COLORS["text_secondary"],
        "zerolinewidth": 2,
        "tickfont": {"color": COLORS["text_secondary"]},
        "title": {"font": {"color": COLORS["text"]}},
    },
    "yaxis": {
        "gridcolor": COLORS["grid"],
        "gridwidth": 1,
        "zerolinecolor": COLORS["text_secondary"],
        "zerolinewidth": 2,
        "tickfont": {"color": COLORS["text_secondary"]},
        "title": {"font": {"color": COLORS["text"]}},
    },
    "legend": {
        "bgcolor": "rgba(22, 33, 62, 0.8)",
        "bordercolor": COLORS["grid"],
        "borderwidth": 1,
        "font": {"color": COLORS["text"]},
        "orientation": "h",
        "yanchor": "bottom",
        "y": -0.15,
        "xanchor": "center",
        "x": 0.5,
    },
    "margin": {"l": 40, "r": 40, "t": 50, "b": 80},
    "hoverlabel": {
        "bgcolor": COLORS["paper"],
        "bordercolor": COLORS["primary"],
        "font": {"color": COLORS["text"], "family": "JetBrains Mono, monospace"},
    },
}

# Animation settings
ANIMATION_SETTINGS: dict[str, Any] = {
    "frame_duration": 50,
    "transition_duration": 30,
    "redraw": True,
}

# Slider styling
SLIDER_STYLE: dict[str, Any] = {
    "bgcolor": COLORS["paper"],
    "bordercolor": COLORS["grid"],
    "borderwidth": 1,
    "tickcolor": COLORS["text_secondary"],
    "font": {"color": COLORS["text"]},
    "activebgcolor": COLORS["primary"],
}


def apply_dark_theme(fig: Any) -> Any:
    """Apply the dark theme to a Plotly figure."""
    fig.update_layout(**DARK_THEME)
    return fig


def get_color_palette() -> list[str]:
    """Return a list of colors for multi-series plots."""
    return [
        COLORS["primary"],
        COLORS["secondary"],
        COLORS["tertiary"],
        COLORS["quaternary"],
        COLORS["accent1"],
        COLORS["accent2"],
        COLORS["accent3"],
        COLORS["accent4"],
    ]


SCENE_THEME: dict[str, Any] = {
    "bgcolor": COLORS["paper"],
    "xaxis": {"gridcolor": COLORS["grid"], "color": COLORS["text_secondary"], "showticklabels": False},
    "yaxis": {"gridcolor": COLORS["grid"], "color": COLORS["text_secondary"], "showticklabels": False},
    "zaxis": {"gridcolor": COLORS["grid"], "color": COLORS["text_secondary"], "showticklabels": False},
}


def base_layout(**overrides: Any) -> dict[str, Any]:
    """Return base layout kwargs for responsive, mobile-friendly charts.

    Usage: ``fig.update_layout(**base_layout(title="…", height=400))``
    """
    layout: dict[str, Any] = {
        "minreducedwidth": 300,
        "paper_bgcolor": COLORS["background"],
        "plot_bgcolor": COLORS["paper"],
        "font": {"color": COLORS["text"], "family": "JetBrains Mono, monospace"},
        "legend": {"bgcolor": "rgba(22, 33, 62, 0.8)", "font": {"size": 12}},
        "margin": {"l": 20, "r": 20, "t": 50, "b": 40},
    }
    layout.update(overrides)
    return layout


def style_subplot_axes(fig: Any, show_ticklabels: bool = False) -> None:
    """Apply dark theme axes and annotation fonts to all subplots."""
    fig.update_xaxes(
        gridcolor=COLORS["grid"],
        zerolinecolor=COLORS["grid"],
        showticklabels=show_ticklabels,
    )
    fig.update_yaxes(
        gridcolor=COLORS["grid"],
        zerolinecolor=COLORS["grid"],
        showticklabels=show_ticklabels,
    )
    for ann in getattr(fig.layout, "annotations", ()):
        ann["font"] = {"color": COLORS["quaternary"], "size": 13}


def get_trace_style(trace_type: str = "function") -> dict[str, Any]:
    """Get consistent trace styling based on type."""
    styles = {
        "function": {
            "line": {"color": COLORS["primary"], "width": 3},
            "mode": "lines",
        },
        "derivative": {
            "line": {"color": COLORS["secondary"], "width": 3},
            "mode": "lines",
        },
        "tangent": {
            "line": {"color": COLORS["tertiary"], "width": 2, "dash": "dash"},
            "mode": "lines",
        },
        "secant": {
            "line": {"color": COLORS["quaternary"], "width": 2, "dash": "dot"},
            "mode": "lines",
        },
        "point": {
            "marker": {"color": COLORS["quaternary"], "size": 12, "symbol": "circle"},
            "mode": "markers",
        },
        "area": {
            "fillcolor": "rgba(0, 212, 255, 0.3)",
            "line": {"color": COLORS["primary"], "width": 1},
        },
    }
    return styles.get(trace_type, styles["function"])
