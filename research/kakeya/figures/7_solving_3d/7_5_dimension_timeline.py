"""R^3 Kakeya dimension lower-bound history (kakeya.md beat 6).

Hausdorff / Minkowski lower bounds for Kakeya sets in R^3:
  * Wolff (1995):          >= 5/2   = (n+2)/2      (Hausdorff & Minkowski)
  * Katz-Laba-Tao (2000):  > 5/2                   (Minkowski)
  * Katz-Zahl (2017):      >= 5/2 + eps            (Hausdorff)
  * Wang-Zahl (2025):      = 3                      (Hausdorff & Minkowski: the conjecture)

Bounds just above 5/2 are plotted with a small offset so they do not collide; their symbolic values
are annotated. Top dashed line is dimension 3.
Run: uv run --with matplotlib --with shapely python research/kakeya/figures/dimension_timeline.py
"""
from _shared import COLORS, math_check, save_preview

# (year, plotted y, symbolic value, name, notion)
EVENTS = [
    (1995, 2.5, "5/2", "Wolff", "Hausdorff & Minkowski"),
    (2000, 2.53, "> 5/2", "Katz-Laba-Tao", "Minkowski"),
    (2017, 2.57, "5/2 + eps", "Katz-Zahl", "Hausdorff"),
    (2025, 3.0, "3", "Wang-Zahl", "Hausdorff & Minkowski"),
]


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    math_check(
        "R^3 Kakeya dimension lower-bound history",
        [
            ("Wolff 1995", "dim >= 5/2 = 2.5          (n+2)/2, Hausdorff & Minkowski"),
            ("Katz-Laba-Tao 2000", "dim > 5/2                 Minkowski (strict)"),
            ("Katz-Zahl 2017", "dim >= 5/2 + eps          Hausdorff"),
            ("Wang-Zahl 2025", "dim = 3                   Hausdorff & Minkowski (the theorem)"),
            ("top line", "3  (full dimension of R^3 = the Kakeya conjecture)"),
        ],
    )

    fig, ax = plt.subplots(figsize=(10.5, 6.0))
    years = [e[0] for e in EVENTS]

    ax.axhline(3.0, color=COLORS["accent"], ls="--", lw=1.3, alpha=0.75)
    ax.text(1994, 3.01, "dimension 3 = full (the Kakeya conjecture in R^3)",
            color=COLORS["accent"], fontsize=10, va="bottom")
    # reference line at 5/2
    ax.axhline(2.5, color=COLORS["guide"], ls=":", lw=0.9, alpha=0.6)
    ax.text(1994, 2.495, "5/2", color=COLORS["guide"], fontsize=9, va="top")

    # connecting climb
    ax.plot(years, [e[1] for e in EVENTS], color=COLORS["guide"], lw=1.0, alpha=0.5, zorder=1)

    for yr, y, sym, name, notion in EVENTS:
        final = (name == "Wang-Zahl")
        col = COLORS["accent"] if final else COLORS["outer"]
        ax.scatter([yr], [y], s=130 if final else 80, color=col, zorder=3,
                   edgecolor="white", linewidth=1.0)
        va = "bottom"
        ax.annotate(f"{name} ({yr})\ndim {'=' if (final or sym == '5/2') else '>='} {sym}\n{notion}",
                    xy=(yr, y), xytext=(yr, y + 0.06), ha="center", va=va,
                    fontsize=9.5, color=col, fontweight="bold" if final else "normal")

    ax.set_xlabel("year")
    ax.set_ylabel("proven lower bound on dim (Kakeya sets in R^3)")
    ax.set_xlim(1992, 2029)
    ax.set_ylim(2.42, 3.18)
    ax.set_yticks([2.5, 2.75, 3.0])
    ax.set_yticklabels(["5/2", "2.75", "3"])
    ax.set_xticks(years)
    ax.set_title("Kakeya in R^3: the dimension lower bound, 1995 -> 2025", fontsize=12)
    ax.grid(True, axis="y", alpha=0.15)

    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
