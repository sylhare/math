"""Animation: the Hausdorff sum jump on the Cantor middle-thirds set (kakeya.md 3b).

The middle-thirds Cantor set is self-similar with N = 2 copies at ratio r = 3, so
dim_H = dim_box = log 2 / log 3 ~ 0.6309. Its natural level-m cover is exactly 2^m
intervals of length 3^-m, so the Hausdorff sum of that cover has a closed form:

    sum (diam U_i)^s  =  2^m * (3^-m)^s  =  (2 * 3^-s)^m .

Because 2*3^-s > 1 for s < dim, = 1 at s = dim, and < 1 for s > dim, sweeping the
exponent s takes the sum from large to small, and deepening the cover m sharpens that
transition into a jump from +inf to 0, pinned to 1 exactly at s = dim_H.

Phase 1 (fixed depth m=4, sweep s): a marker traces the m=4 curve, the gauge reads
the sum. Phase 2 (fixed s, grow depth): the depth curves m=1..6 accumulate on the
right, all crossing the same fixed point (dim_H, 1) and steepening toward a step.

Run: uv run --with matplotlib --with shapely --with pillow python research/kakeya/figures/3_dimension/3_4_hausdorff_sweep_anim.py
"""
import math

import numpy as np
from _shared import COLORS, math_check, save_gif
from matplotlib.animation import FuncAnimation

N_COPIES = 2                       # self-similar copies (Cantor middle-thirds)
RATIO = 3                          # contraction ratio 1/3
DIM = math.log(N_COPIES) / math.log(RATIO)   # = log2/log3 ~ 0.6309

PHASE1_M = 4                       # fixed depth while sweeping s
PHASE2_S = 0.5                     # fixed exponent (< dim) while growing depth
M_MAX = 6                          # deepest cover in phase 2
DUST_LEVEL = 6                     # display level of the Cantor dust on the left

S_LO, S_HI = 0.30, 1.00
N_SWEEP = 40                       # s-steps in phase 1
PH2_HOLD = 4                       # frames per depth step in phase 2
HOLD = 7                           # leading hold
END_HOLD = 8                       # trailing hold

Y_TOP = 5.0                        # right-panel y ceiling (curves clipped above)


def hausdorff_sum(s, m):
    """Closed form: sum (diam U_i)^s over the natural level-m cover = (2 * 3^-s)^m."""
    return (N_COPIES * RATIO ** (-s)) ** m


def cantor_intervals(level):
    """The 2^level surviving intervals (start, length) of the middle-thirds set."""
    intervals = [(0.0, 1.0)]
    for _ in range(level):
        nxt = []
        for a, length in intervals:
            third = length / 3.0
            nxt.append((a, third))
            nxt.append((a + 2.0 * third, third))
        intervals = nxt
    return intervals


def main():
    s_sweep = np.linspace(S_LO, S_HI, N_SWEEP)
    s_plot = np.linspace(S_LO, S_HI, 240)
    dust = cantor_intervals(DUST_LEVEL)

    # Validation: everything from the closed form, nothing measured
    # (1) fixed point: 2 * 3^-dim == 1
    fixed_pt = N_COPIES * RATIO ** (-DIM)
    assert abs(fixed_pt - 1.0) < 1e-12, "2*3^-dim must equal 1 (the fixed point)"

    # (2) pinned to 1 at s = dim for every depth
    pin_err = max(abs(hausdorff_sum(DIM, m) - 1.0) for m in range(1, M_MAX + 1))
    assert pin_err < 1e-9, "H^s sum must equal 1 at s=dim for every m"

    # (3) monotone in m: diverge below dim, collapse above dim
    below = [hausdorff_sum(0.5, m) for m in range(1, M_MAX + 1)]
    above = [hausdorff_sum(0.75, m) for m in range(1, M_MAX + 1)]
    assert all(below[k] < below[k + 1] for k in range(len(below) - 1)), \
        "at s=0.5<dim the sum (2*3^-s)^m must strictly increase in m"
    assert all(above[k] > above[k + 1] for k in range(len(above) - 1)), \
        "at s=0.75>dim the sum (2*3^-s)^m must strictly decrease in m"

    # (4) threshold as m->inf: +inf for s<dim, 0 for s>dim (m=1 vs m=20 signs)
    assert hausdorff_sum(0.5, 20) > hausdorff_sum(0.5, 1) > 1.0, "s<dim must diverge"
    assert hausdorff_sum(0.75, 20) < hausdorff_sum(0.75, 1) < 1.0, "s>dim must collapse"
    assert hausdorff_sum(0.75, 40) < 0.02, "s>dim must head to 0 as m grows"

    tbl_below = "  ".join(f"m={m}:{hausdorff_sum(0.5, m):.4f}" for m in (1, 2, 4, 6))
    tbl_above = "  ".join(f"m={m}:{hausdorff_sum(0.75, m):.4f}" for m in (1, 2, 4, 6))
    math_check(
        "Hausdorff H^s jump on the Cantor set, sum = (2*3^-s)^m",
        [
            ("Cantor set", f"N={N_COPIES} copies, ratio r={RATIO}"),
            ("dim_H = dim_box = log2/log3", f"{DIM:.6f}"),
            ("fixed point 2*3^-dim", f"{fixed_pt:.12f}  (want 1, err {abs(fixed_pt-1):.1e})"),
            ("pinned at s=dim, all m in 1..6", f"max |sum - 1| = {pin_err:.1e}  (< 1e-9)"),
            ("s=0.50 < dim, rising in m", tbl_below),
            ("s=0.75 > dim, falling in m", tbl_above),
            ("threshold s=0.5:  m=1 -> m=20", f"{hausdorff_sum(0.5,1):.3f} -> {hausdorff_sum(0.5,20):.3f}  (+inf)"),
            ("threshold s=0.75: m=1 -> m=20", f"{hausdorff_sum(0.75,1):.3f} -> {hausdorff_sum(0.75,20):.3f}  (-> 0)"),
        ],
    )

    # Frame plan: leading hold + phase 1 sweep + phase 2 depths + trailing hold
    states = []
    for sv in s_sweep:
        states.append(("sweep", float(sv), PHASE1_M))
    for m in range(1, M_MAX + 1):
        for _ in range(PH2_HOLD):
            states.append(("depth", PHASE2_S, m))
    frames = [0] * HOLD + list(range(len(states))) + [len(states) - 1] * END_HOLD

    # Figure
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.patches as mpatches
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 2, figsize=(13.0, 5.7))
    fig.suptitle("H^s sum = (2 * 3^-s)^m,   jump at s = dim_H", fontsize=13)

    # gauge geometry on the left panel (log-scaled bar to the side of the dust)
    GX0, GX1 = 1.06, 1.22          # gauge x-extent
    GY = 0.52                      # gauge baseline (value = 1)
    GH = 0.34                      # half-height of the gauge
    LMAX = 1.2                     # log10 clip for the bar

    def draw_left(m, s):
        ax[0].cla()
        ax[0].set_xlim(-0.05, 1.30)
        ax[0].set_ylim(0.0, 1.0)
        ax[0].set_aspect("auto")
        ax[0].axis("off")

        cover = cantor_intervals(m)
        # highlighted current cover intervals (2^m of length 3^-m)
        for a, length in cover:
            ax[0].add_patch(mpatches.Rectangle(
                (a, 0.40), length, 0.24, facecolor=COLORS["region"],
                edgecolor=COLORS["accent"], linewidth=0.4, alpha=0.85, zorder=2))
        # the fixed-level Cantor dust drawn on top (the fractal itself)
        for a, length in dust:
            ax[0].plot([a + length / 2.0], [0.52], marker="|", ms=9,
                       color=COLORS["needle"], mew=1.1, zorder=3)
        ax[0].text(0.5, 0.80, f"Cantor cover: 2^{m} = {2**m} intervals of 3^-{m}",
                   ha="center", va="center", fontsize=10, color=COLORS["guide"])
        ax[0].text(0.5, 0.24, f"level-{DUST_LEVEL} dust shown; sum = (2*3^-s)^m",
                   ha="center", va="center", fontsize=8.5, color=COLORS["muted"])

        # Log-scaled gauge bar: sum = (2*3^-s)^m
        val = hausdorff_sum(s, m)
        lg = math.log10(val)
        h = max(-1.0, min(1.0, lg / LMAX)) * GH
        gcol = COLORS["accent"] if lg >= 0 else COLORS["outer"]
        if h >= 0:
            ax[0].add_patch(mpatches.Rectangle((GX0, GY), GX1 - GX0, h,
                            facecolor=gcol, edgecolor="none", alpha=0.9, zorder=2))
        else:
            ax[0].add_patch(mpatches.Rectangle((GX0, GY + h), GX1 - GX0, -h,
                            facecolor=gcol, edgecolor="none", alpha=0.9, zorder=2))
        # baseline = value 1
        ax[0].plot([GX0 - 0.01, GX1 + 0.01], [GY, GY], color=COLORS["guide"],
                   lw=1.0, ls="--", zorder=3)
        ax[0].text(GX1 + 0.015, GY, "=1", va="center", fontsize=8, color=COLORS["guide"])
        state = "huge" if lg > 0.02 else ("tiny" if lg < -0.02 else "= 1")
        ax[0].text((GX0 + GX1) / 2.0, GY + GH + 0.06, f"sum = {val:.3f}",
                   ha="center", fontsize=9, color=gcol)
        ax[0].text((GX0 + GX1) / 2.0, GY - GH - 0.06, state,
                   ha="center", va="top", fontsize=8.5, color=gcol)

    def draw_right(kind, s, m_cur):
        ax[1].cla()
        ax[1].set_xlim(S_LO, S_HI)
        ax[1].set_ylim(0.0, Y_TOP)
        ax[1].set_xlabel("exponent s")
        ax[1].set_ylabel("H^s sum  = (2*3^-s)^m")
        ax[1].grid(True, color=COLORS["muted"], alpha=0.25, lw=0.5)
        # fixed structure: crossing lines and the fixed point
        ax[1].axvline(DIM, color=COLORS["guide"], ls="--", lw=1.0)
        ax[1].axhline(1.0, color=COLORS["guide"], ls="--", lw=1.0)
        ax[1].plot([DIM], [1.0], "o", color=COLORS["guide"], ms=6, zorder=6)
        ax[1].text(DIM + 0.01, Y_TOP - 0.35, f"s = dim_H = {DIM:.4f}",
                   color=COLORS["guide"], fontsize=9)

        if kind == "sweep":
            yv = np.clip([hausdorff_sum(sv, PHASE1_M) for sv in s_plot], 0, Y_TOP)
            ax[1].plot(s_plot, yv, color=COLORS["needle"], lw=2.0,
                       label=f"m = {PHASE1_M}")
            cur = hausdorff_sum(s, PHASE1_M)
            ax[1].plot([s], [min(cur, Y_TOP)], "o", color=COLORS["accent"],
                       ms=11, mfc="none", mew=2, zorder=7)
            ax[1].plot([s, s], [0, min(cur, Y_TOP)], color=COLORS["accent"],
                       lw=0.8, ls=":", zorder=5)
            ax[1].set_title(f"phase 1: sweep s at fixed depth m = {PHASE1_M}",
                            fontsize=11)
            ax[1].legend(loc="upper right", fontsize=9)
        else:
            for m in range(1, m_cur + 1):
                yv = np.clip([hausdorff_sum(sv, m) for sv in s_plot], 0, Y_TOP)
                is_cur = (m == m_cur)
                ax[1].plot(s_plot, yv,
                           color=COLORS["accent"] if is_cur else COLORS["needle"],
                           lw=1.2 + 0.28 * m,
                           alpha=1.0 if is_cur else 0.25 + 0.11 * m,
                           zorder=4 + m)
                ax[1].text(S_LO + 0.005, min(hausdorff_sum(S_LO, m), Y_TOP - 0.15),
                           f"m={m}", fontsize=8,
                           color=COLORS["accent"] if is_cur else COLORS["needle"],
                           va="top")
            ax[1].set_title(f"phase 2: depths m = 1..{m_cur} accumulate "
                            f"(steepen to a step)", fontsize=11)

    def update(fi):
        kind, s, m = states[frames[fi]]
        draw_left(m, s)
        draw_right(kind, s, m)
        return []

    anim = FuncAnimation(fig, update, frames=len(frames), interval=130, blit=False)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    print("wrote", save_gif(anim, fps=8, dpi=95))


if __name__ == "__main__":
    main()
