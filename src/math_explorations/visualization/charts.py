"""Reusable chart components for notebooks."""

from typing import Any

import plotly.graph_objects as go

from .styles import COLORS, base_layout


def create_timeline(
    events: list[tuple[int, str, int]],
    title: str = "Timeline",
    x_range: tuple[float, float] | None = None,
    height: int = 320,
) -> go.Figure:
    """Create an alternating timeline chart.

    Args:
        events: List of ``(year, label, side)`` tuples.
            *side* is ``1`` (above axis) or ``-1`` (below axis).
        title: Chart title.
        x_range: Optional ``(min, max)`` for x-axis (auto-computed if *None*).
        height: Chart height in pixels.
    """
    years = [e[0] for e in events]
    has_bce = any(y < 0 for y in years)

    if x_range is None:
        span = max(years) - min(years) or 100
        padding = span * 0.08
        x_range = (min(years) - padding, max(years) + padding)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=list(x_range), y=[0, 0],
        mode="lines", line={"color": COLORS["text_secondary"], "width": 2},
        showlegend=False, hoverinfo="skip",
    ))

    for yr, lbl, side in events:
        color = COLORS["primary"] if side == 1 else COLORS["secondary"]
        fig.add_trace(go.Scatter(
            x=[yr, yr], y=[0, side * 0.55],
            mode="lines", line={"color": color, "width": 2},
            showlegend=False, hoverinfo="skip",
        ))
        fig.add_trace(go.Scatter(
            x=[yr], y=[0],
            mode="markers", marker={"color": color, "size": 10},
            showlegend=False,
            hovertemplate=f'{yr}: {lbl.replace(chr(10), " ")}<extra></extra>',
        ))

        year_text = f"{abs(yr)} BCE" if yr < 0 else str(yr)
        fig.add_annotation(
            x=yr, y=side * 0.65,
            text=f"<b>{year_text}</b><br>{lbl}",
            font={"color": color, "size": 10},
            showarrow=False,
            align="center",
        )

    tick_kwargs: dict[str, Any] = {"tickvals": years}
    if has_bce:
        tick_kwargs["ticktext"] = [
            f"{abs(y)} BCE" if y < 0 else str(y) for y in years
        ]

    fig.update_layout(**base_layout(
        title=title,
        height=height,
        xaxis={
            "gridcolor": COLORS["grid"],
            "zerolinecolor": COLORS["grid"],
            "range": list(x_range),
            "title": "Year",
            **tick_kwargs,
        },
        yaxis={"visible": False, "range": [-1.3, 1.3]},
    ))
    return fig
