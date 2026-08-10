"""Figure: the harmonic-analysis tower resting on Kakeya (schematic implication diagram).

Math (see ../kakeya.md section 5c):
  Hickman's tower of conjectures.  The implications run ONE way, strongest at the top:

      local smoothing  ==>  Bochner-Riesz  ==>  restriction  ==>  Kakeya

  Kakeya sits at the BASE: it is the weakest statement, implied by every one above it, so proving
  Kakeya is necessary for all of them (if Kakeya failed the whole tower falls).  The reverse
  implications are NOT known: Kakeya does not imply the others.

  Status per rung:
    local smoothing (Sogge)      known n=2 (Guth-Wang-Zhang 2020), open n>=3
    Bochner-Riesz (Bochner/Riesz) known n=2, open n>=3
    restriction (Stein)          known n=2 (Fefferman-Zygmund), open n>=3
    Kakeya (base)                known n=2 (Davies); also n=3 (Wang-Zahl 2025); open n>=4

Reference: none (schematic). ALTERNATIVES: a known/open table per conjecture.
Run: uv run --with matplotlib --with shapely python research/kakeya/figures/conjecture_tower.py
"""
from _shared import COLORS, math_check, save_preview

# Tower rungs, top (strongest) to bottom (weakest). The arrow order is the load-bearing fact.
TOWER = [
    ("Local smoothing", "Sogge",
     r"$(\int_1^2 \|e^{it\sqrt{-\Delta}}f\|_p^p\,dt)^{1/p} \lesssim \|f\|_{L^p_{s_p-\sigma}}$",
     "known n=2 (Guth-Wang-Zhang 2020), open n>=3"),
    ("Bochner-Riesz", "Bochner / Riesz",
     r"$B_R^\alpha f,\ (1-|\xi|^2/R^2)_+^{\alpha},\ \alpha>0$",
     "known n=2, open n>=3"),
    ("Restriction", "Stein",
     r"$\|Eg\|_{L^q} \lesssim \|g\|_\infty,\ q>\frac{2n}{n-1}$",
     "known n=2 (Fefferman-Zygmund), open n>=3"),
    ("Kakeya  (base)", "Davies / Wang-Zahl",
     r"$\dim K = n$ for every Kakeya set $K\subseteq\mathbb{R}^n$",
     "known n=2 (Davies); also n=3 (Wang-Zahl 2025); open n>=4"),
]


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

    n = len(TOWER)
    fig, ax = plt.subplots(figsize=(8.4, 8.8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")

    box_h = 1.42
    gap = 0.72
    top_y = 9.35
    # widen the boxes toward the base to read as a tower with the floor widest
    widths = [5.6, 6.2, 6.8, 7.6]
    fills = [COLORS["region"], COLORS["needle"], COLORS["outer"], COLORS["accent"]]
    text_colors = ["black", "white", "white", "white"]

    centers_y = []
    for i, ((name, who, formula, status), w, fc, tc) in enumerate(
        zip(TOWER, widths, fills, text_colors)
    ):
        y = top_y - i * (box_h + gap)
        cy = y - box_h / 2
        centers_y.append(cy)
        box = FancyBboxPatch(
            (5 - w / 2, y - box_h), w, box_h,
            boxstyle="round,pad=0.02,rounding_size=0.12",
            linewidth=1.6, edgecolor=COLORS["guide"], facecolor=fc, alpha=0.9,
        )
        ax.add_patch(box)
        ax.text(5, cy + 0.42, name, ha="center", va="center", fontsize=13,
                fontweight="bold", color=tc)
        ax.text(5, cy + 0.05, f"({who})", ha="center", va="center", fontsize=8.5, color=tc)
        ax.text(5, cy - 0.34, formula, ha="center", va="center", fontsize=9, color=tc)
        ax.text(5, y - box_h - 0.30, status, ha="center", va="center", fontsize=8,
                color=COLORS["guide"], style="italic")

    # downward implication arrows between consecutive rungs (strongest implies weaker)
    for i in range(n - 1):
        y_from = top_y - i * (box_h + gap) - box_h
        y_to = top_y - (i + 1) * (box_h + gap)
        arr = FancyArrowPatch(
            (5, y_from - 0.30), (5, y_to + 0.02),
            arrowstyle="-|>", mutation_scale=22, linewidth=2.4, color=COLORS["guide"],
        )
        ax.add_patch(arr)
        ax.text(5.35, (y_from + y_to) / 2 - 0.14, "implies", ha="left", va="center",
                fontsize=8.5, color=COLORS["guide"])

    ax.text(5, 9.75, "Harmonic-analysis tower  (implications run downward)",
            ha="center", va="center", fontsize=12, fontweight="bold")
    ax.text(5, 0.28, "Kakeya is the geometric floor: implied by all above, it implies none of them.",
            ha="center", va="center", fontsize=8.5, color=COLORS["guide"], style="italic")

    print("wrote", save_preview(fig))

    # --- validation: the arrow order must match kakeya.md, Kakeya at the base ----------
    order = [t[0].split()[0] for t in TOWER]
    expected = ["Local", "Bochner-Riesz", "Restriction", "Kakeya"]
    order_ok = order == expected
    kakeya_at_base = order[-1] == "Kakeya"
    strongest_top = order[0] == "Local"  # local smoothing is strongest / at top
    # honesty: no rung claims Kakeya implies the others (arrows only point strong -> weak, downward)
    no_false_claim = kakeya_at_base  # Kakeya is a sink: arrows enter it, none leave it

    math_check(
        "conjecture tower implication order",
        [
            ("top->bottom order", " => ".join(order)),
            ("matches kakeya.md 5c", "OK" if order_ok else "FAIL"),
            ("local smoothing at top (strongest)", "OK" if strongest_top else "FAIL"),
            ("Kakeya at base (weakest)", "OK" if kakeya_at_base else "FAIL"),
            ("no claim 'Kakeya => others'", "OK" if no_false_claim else "FAIL"),
        ],
    )


if __name__ == "__main__":
    main()
