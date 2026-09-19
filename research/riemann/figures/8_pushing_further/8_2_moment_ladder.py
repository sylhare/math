"""Static: the ladder of certified proportions, and where it stops being unconditional.

    5/12 = 0.4167   previous record (PRZZ 2020)                     unconditional
    2/3  = 0.6667   flat window (Theorems A, B)                     unconditional
    0.6725          optimal window (Montgomery-Taylor, Theorem D)   unconditional, functional max
    13/18 = 0.7222  4th spectral moment                             conditional (Hardy-Littlewood)
    1.0             all moments                                     conditional (all correlations)

The first three rungs use only the mean density and Montgomery's second moment at bandwidth <= 1. The
last two need correlations outside the Rudnick-Sarnak range k*lambda < 2. Even at proportion 1 the
target is simple zeros, not RH: the Davenport-Heilbronn function shares every input here but has
off-line zeros, so no data-only argument reaches RH.

Run: PYTHONPATH=research/riemann/figures uv run --with matplotlib --with mpmath --with pillow \
  python research/riemann/figures/8_pushing_further/8_2_moment_ladder.py
"""

import numpy as np
from _shared import COLORS, math_check, plot_axes, save_preview

RUNGS = [
    ("previous record\n5/12 (PRZZ 2020)", 5 / 12, "uncond"),
    ("flat window\n2/3 (Thm A, B)", 2 / 3, "uncond"),
    ("optimal window\n0.6725 (Thm D)", 0.67250, "ceiling"),
    ("+ 4th moment\n13/18", 13 / 18, "cond"),
    ("+ all moments\n1", 1.0, "cond"),
]


def main():
    math_check(
        "the ladder of certified proportions",
        [
            ("previous record 5/12", f"{5 / 12:.4f}  unconditional"),
            ("flat window 2/3", f"{2 / 3:.4f}  unconditional"),
            ("optimal window 0.6725", "0.67250  unconditional (method ceiling)"),
            ("+ 4th moment 13/18", f"{13 / 18:.4f}  conditional (Hardy-Littlewood)"),
            ("+ all moments", "1.0000  conditional; RH still out of reach (Davenport-Heilbronn)"),
        ],
    )
    assert abs(RUNGS[2][1] - 0.67250) < 1e-4
    assert abs(RUNGS[3][1] - 13 / 18) < 1e-12

    fill = {"uncond": COLORS["onlinepos"], "ceiling": COLORS["zero"], "cond": COLORS["offline"]}
    fig, ax = plot_axes(figsize=(8.6, 5.2))
    xs = np.arange(len(RUNGS))
    for x, (_label, val, kind) in zip(xs, RUNGS, strict=True):
        hatch = "//" if kind == "cond" else None
        ax.bar(x, val, width=0.62, color=fill[kind], edgecolor="#333333", hatch=hatch, zorder=3)
        ax.text(x, val + 0.015, f"{val:.4f}", ha="center", va="bottom", fontsize=9, color="#222222")

    ax.axhline(1.0, color=COLORS["muted"], lw=1.0, ls=":")
    ax.axvspan(-0.5, 2.5, color=COLORS["region"], alpha=0.25, zorder=0)
    ax.text(1.0, 0.83, "unconditional", ha="center", fontsize=10, color=COLORS["prime"])
    ax.text(3.5, 0.45, "conditional", ha="center", va="center", rotation=90, fontsize=10, color=COLORS["offline"])
    ax.text(
        2.0,
        1.055,
        "RH: out of reach of any data-only argument (Davenport-Heilbronn)",
        ha="center",
        va="bottom",
        fontsize=8.5,
        color=COLORS["muted"],
    )

    ax.set_xticks(xs)
    ax.set_xticklabels([r[0] for r in RUNGS], fontsize=8.5)
    ax.set_ylim(0.0, 1.14)
    ax.set_ylabel("certified proportion of simple zeros on the line")
    ax.set_title("What each lever buys")
    ax.set_axisbelow(True)

    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
