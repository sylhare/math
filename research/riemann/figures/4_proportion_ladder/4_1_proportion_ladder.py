"""Static: the proven lower bound on the proportion of zeros on the critical line, by year.

Horizontal bars for each rung of the ladder kappa = liminf N_0(T)/N(T), against the faint full
bar to 1.0 (RH: 100%). The 2026 bar (Theorem A, 2/3) is drawn in the zero colour, with a tick at
the optimised 0.6725.

Run: PYTHONPATH=research/riemann/figures uv run --with matplotlib --with mpmath --with pillow \
  python research/riemann/figures/4_proportion_ladder/4_1_proportion_ladder.py
"""

import numpy as np
from _shared import COLORS, math_check, plot_axes, save_preview

RUNGS = [
    ("Selberg", 1942, 0.03, "> 0", COLORS["guide"]),
    ("Levinson", 1974, 1.0 / 3.0, "1/3", COLORS["prime"]),
    ("Conrey", 1989, 2.0 / 5.0, "2/5", COLORS["prime"]),
    ("PRZZ", 2020, 5.0 / 12.0, "5/12", COLORS["prime"]),
    ("Claude", 2026, 2.0 / 3.0, "2/3", COLORS["zero"]),
]
OPT_2026 = 0.6725


def main():
    math_check(
        "proportion ladder",
        [
            ("Levinson 1/3", f"{1 / 3:.4f}"),
            ("Conrey 2/5", f"{2 / 5:.4f}"),
            ("PRZZ 5/12", f"{5 / 12:.5f}"),
            ("Claude 2/3", f"{2 / 3:.5f}"),
            ("optimised", f"{OPT_2026:.4f}"),
            ("RH target", "1.0000"),
        ],
    )

    fig, ax = plot_axes(figsize=(8.0, 5.0))
    ys = np.arange(len(RUNGS))

    ax.barh(ys, 1.0, color=COLORS["region"], alpha=0.35, height=0.62, zorder=1)
    for y, (_, _, val, _, color) in zip(ys, RUNGS, strict=True):
        ax.barh(y, val, color=color, height=0.62, zorder=2)

    for y, (name, year, val, txt, _) in zip(ys, RUNGS, strict=True):
        label = txt if txt.startswith(">") else f"{txt} = {val:.4f}"
        ax.text(val + 0.012, y, label, va="center", ha="left", fontsize=10)
        ax.text(-0.012, y, f"{name} {year}", va="center", ha="right", fontsize=10)

    opt_y = ys[-1]
    ax.plot([OPT_2026, OPT_2026], [opt_y - 0.31, opt_y + 0.31], color=COLORS["line"], lw=1.8, zorder=3)
    ax.annotate(
        f"opt. {OPT_2026:.4f}",
        xy=(OPT_2026, opt_y + 0.31),
        xytext=(OPT_2026 + 0.02, opt_y + 0.55),
        fontsize=9,
        color=COLORS["line"],
        arrowprops=dict(arrowstyle="->", color=COLORS["line"], lw=1.0),
    )
    ax.text(1.0, ys[0] - 0.7, "RH: 100%", va="center", ha="right", fontsize=10, color=COLORS["muted"])

    ax.set_xlim(0.0, 1.05)
    ax.set_ylim(-1.0, len(RUNGS) - 0.2)
    ax.set_yticks([])
    ax.set_xlabel(r"proven lower bound $\kappa = \liminf N_0(T)/N(T)$")
    ax.set_title("Proportion proven on the critical line")

    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
