"""R^3 Kakeya dimension lower-bound milestones revealed over the years (kakeya.md beat 6).

Motion version of `dimension_timeline.py`. A marker climbs toward the dashed y = 3 line, revealing
the Hausdorff / Minkowski lower bounds one milestone at a time:
  * Wolff (1995):          >= 5/2   = (n+2)/2      (Hausdorff & Minkowski)
  * Katz-Laba-Tao (2000):  > 5/2                   (Minkowski)
  * Katz-Zahl (2017):      >= 5/2 + eps            (Hausdorff)
  * Wang-Zahl (2025):      = 3                      (Hausdorff & Minkowski: the conjecture)

Bounds just above 5/2 are drawn with a small offset so they do not collide. Final marker lands at 3.
Run: uv run --with matplotlib --with shapely python research/kakeya/figures/dimension_timeline_anim.py
"""
import numpy as np
from _shared import COLORS, math_check, save_gif
from matplotlib.animation import FuncAnimation

# (year, plotted y, symbolic value, true lower bound used for the invariant, name, notion)
EVENTS = [
    (1995, 2.5, "5/2", 2.5, "Wolff", "Hausdorff & Minkowski"),
    (2000, 2.53, "> 5/2", 2.5, "Katz-Laba-Tao", "Minkowski"),
    (2017, 2.57, "5/2 + eps", 2.5, "Katz-Zahl", "Hausdorff"),
    (2025, 3.0, "3", 3.0, "Wang-Zahl", "Hausdorff & Minkowski"),
]


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    years = [e[0] for e in EVENTS]
    plotted = [e[1] for e in EVENTS]

    # --- INVARIANT assertions ------------------------------------------------
    assert [e[2] for e in EVENTS] == ["5/2", "> 5/2", "5/2 + eps", "3"]
    assert [e[3] for e in EVENTS] == [2.5, 2.5, 2.5, 3.0]  # exact lower bounds
    assert EVENTS[-1][1] == 3.0                            # final marker at dimension 3

    math_check(
        "R^3 Kakeya lower-bound milestones (animated reveal)",
        [
            ("Wolff 1995", "dim >= 5/2 = 2.5          (n+2)/2, Hausdorff & Minkowski"),
            ("Katz-Laba-Tao 2000", "dim > 5/2                 Minkowski (strict)"),
            ("Katz-Zahl 2017", "dim >= 5/2 + eps          Hausdorff"),
            ("Wang-Zahl 2025", "dim = 3                   Hausdorff & Minkowski (the theorem)"),
            ("final marker", f"y = {EVENTS[-1][1]}  (dimension 3 = the Kakeya conjecture in R^3)"),
        ],
    )

    # Build the frame schedule: reveal event 0, then travel + hold for each later milestone.
    SUB, HOLD, H0, HEND = 16, 8, 8, 18
    frames = [(years[0], plotted[0], 1)] * H0
    for e in range(1, len(EVENTS)):
        for s in np.linspace(0, 1, SUB, endpoint=False):
            x = years[e - 1] + s * (years[e] - years[e - 1])
            y = plotted[e - 1] + s * (plotted[e] - plotted[e - 1])
            frames.append((x, y, e))          # events 0..e-1 revealed while travelling
        frames += [(years[e], plotted[e], e + 1)] * HOLD
    frames += [(years[-1], plotted[-1], len(EVENTS))] * HEND

    fig, ax = plt.subplots(figsize=(10.5, 6.0))

    def update(fi):
        mx, my, nrev = frames[fi]
        ax.clear()
        ax.axhline(3.0, color=COLORS["accent"], ls="--", lw=1.3, alpha=0.75)
        ax.text(1994, 3.01, "dimension 3 = full (the Kakeya conjecture in R^3)",
                color=COLORS["accent"], fontsize=10, va="bottom")
        ax.axhline(2.5, color=COLORS["guide"], ls=":", lw=0.9, alpha=0.6)
        ax.text(1994, 2.495, "5/2", color=COLORS["guide"], fontsize=9, va="top")

        if nrev >= 2:  # connecting climb among revealed milestones
            ax.plot(years[:nrev], plotted[:nrev], color=COLORS["guide"], lw=1.0, alpha=0.5, zorder=1)

        for yr, y, sym, _lb, name, notion in EVENTS[:nrev]:
            final = name == "Wang-Zahl"
            col = COLORS["accent"] if final else COLORS["outer"]
            ax.scatter([yr], [y], s=130 if final else 80, color=col, zorder=3,
                       edgecolor="white", linewidth=1.0)
            rel = "=" if (final or sym == "5/2") else ">="
            ax.annotate(f"{name} ({yr})\ndim {rel} {sym}\n{notion}",
                        xy=(yr, y), xytext=(yr, y + 0.06), ha="center", va="bottom",
                        fontsize=9.5, color=col, fontweight="bold" if final else "normal")

        ax.scatter([mx], [my], s=70, color=COLORS["accent"], zorder=5, edgecolor="white", linewidth=1.2)

        ax.set_xlabel("year")
        ax.set_ylabel("proven lower bound on dim (Kakeya sets in R^3)")
        ax.set_xlim(1992, 2034)  # right margin so the centred Wang-Zahl (2025) label stays on-canvas
        ax.set_ylim(2.42, 3.18)
        ax.set_yticks([2.5, 2.75, 3.0])
        ax.set_yticklabels(["5/2", "2.75", "3"])
        ax.set_xticks(years)
        ax.set_title("Kakeya in R^3: the dimension lower bound, 1995 -> 2025", fontsize=12)
        ax.grid(True, axis="y", alpha=0.15)
        return []

    anim = FuncAnimation(fig, update, frames=len(frames), interval=60, blit=False)
    print("wrote", save_gif(anim, fps=15, dpi=95))


if __name__ == "__main__":
    main()
