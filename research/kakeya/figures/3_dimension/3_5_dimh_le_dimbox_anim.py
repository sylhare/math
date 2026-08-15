"""Animation: dim_H <= dim_box, with one case where the two agree and one where they differ.

Two sets get the same two-phase treatment (kakeya.md 3b, "always dim_H <= dim_box"):

  LEFT   E = {0} U {1/n : n = 1..Nmax}   (countable dust piling up at 0)
  RIGHT  the middle-thirds Cantor set     (self-similar)

Phase 1 (Minkowski box-count): shrink a uniform delta-grid and count occupied cells N(delta).
  * {1/n}:  N(delta) ~ delta^-1/2  (points at spacing 1/(n(n+1)) resolve until n ~ delta^-1/2,
            then the tail fills every cell near 0), so the log-log slope climbs toward 1/2.
  * Cantor: N(3^-m) = 2^m exactly, slope = log2/log3 = 0.6309.

Phase 2 (Hausdorff adaptive cover): allow covers of any sizes and minimise sum (diam)^s.
  * {1/n}:  cover the whole tail [0, 1/M] by one interval (cost (1/M)^s) plus M-1 tiny
            intervals on the isolated points (cost -> 0 as their width eps -> 0); as M -> inf
            the cost -> 0 for every s > 0, so dim_H = 0.
  * Cantor: the natural cover of 2^m intervals already gives sum (2*3^-s)^m = 1 at s = dim,
            adaptivity buys nothing, so dim_H = dim_box = log2/log3.

Gap dim_box - dim_H = 1/2 on the left (the distinction bites), 0 on the right.

Run: PYTHONPATH=research/kakeya/figures uv run --with matplotlib --with shapely --with pillow \
     python research/kakeya/figures/3_dimension/3_5_dimh_le_dimbox_anim.py
"""

import math

import numpy as np
from _shared import COLORS, math_check, save_gif
from matplotlib.animation import FuncAnimation

NMAX = 20000  # E = {0} U {1/n : n=1..NMAX}
LEFT_KS = [3, 4, 5, 6, 7, 8, 9, 10]  # left uniform grid delta = 2^-k
RIGHT_MS = [1, 2, 3, 4, 5, 6]  # Cantor level m, delta = 3^-m
ADAPT_M = [4, 8, 16, 32, 64]  # Hausdorff adaptive: [0,1/M] + (M-1) tiny intervals
S_LEFT = 0.3  # any s > 0 gives dim_H({1/n}) = 0
DIM_C = math.log(2) / math.log(3)  # Cantor dimension, log2/log3 = 0.6309
DIM_BOX_LEFT = 0.5  # theoretical box dimension of {1/n}

START_HOLD = 7
MID_HOLD = 5
END_HOLD = 8
HBAR = 1.0  # bar height for the set strips


# Geometry / counting (pure numpy)
def occupied_cells_1overn(delta: float) -> int:
    """Exact count of side-delta cells on [0,1] meeting E = {0} U {1/n}, n=1..NMAX."""
    n = np.arange(1, NMAX + 1)
    cells = set(np.floor((1.0 / n) / delta).astype(np.int64).tolist())
    cells.add(0)  # the accumulation point 0
    return len(cells)


def occupied_indices_1overn(delta: float) -> set[int]:
    n = np.arange(1, NMAX + 1)
    cells = set(np.floor((1.0 / n) / delta).astype(np.int64).tolist())
    cells.add(0)
    return cells


def cantor_intervals(m: int) -> list[tuple[float, float]]:
    """The 2^m intervals of length 3^-m at Cantor level m (the natural cover)."""
    iv = [(0.0, 1.0)]
    for _ in range(m):
        nxt = []
        for a, b in iv:
            t = (b - a) / 3.0
            nxt.append((a, a + t))
            nxt.append((b - t, b))
        iv = nxt
    return iv


def main():
    # Left set: uniform box counts (exact)
    left_deltas = [2.0 ** (-k) for k in LEFT_KS]
    left_N = [occupied_cells_1overn(d) for d in left_deltas]
    left_cells = [occupied_indices_1overn(d) for d in left_deltas]
    left_lx = [math.log(1.0 / d) for d in left_deltas]
    left_ly = [math.log(N) for N in left_N]
    left_slope = float(np.polyfit(left_lx, left_ly, 1)[0])

    # Cantor set: uniform box counts (closed form)
    right_deltas = [3.0 ** (-m) for m in RIGHT_MS]
    right_N = [2**m for m in RIGHT_MS]
    right_ivs = [cantor_intervals(m) for m in RIGHT_MS]
    right_lx = [math.log(1.0 / d) for d in right_deltas]
    right_ly = [math.log(N) for N in right_N]
    right_slope = float(np.polyfit(right_lx, right_ly, 1)[0])

    # Adaptive Hausdorff cover costs
    # left: eps -> 0 limit of (1/M)^s + (M-1) eps^s  is  (1/M)^s ; take M -> inf.
    left_cost = [(1.0 / M) ** S_LEFT for M in ADAPT_M]
    # right: natural cover sum (2 * 3^-s)^m at s = dim  == 1  for every level.
    right_cost = [(2.0 * 3.0 ** (-DIM_C)) ** m for m in RIGHT_MS]

    # Validation (assert the relations the figure draws)
    # (1) {1/n} box-count slope trends to 1/2 on exact counts, N strictly grows as delta shrinks.
    assert all(left_N[i] < left_N[i + 1] for i in range(len(left_N) - 1)), (
        "occupied-cell count must strictly increase as delta shrinks"
    )
    assert 0.42 < left_slope < 0.58, f"box-count slope {left_slope:.4f} not in (0.42, 0.58)"

    # (2) adaptive cost (1/M)^s strictly decreasing to < 1e-2 as M -> inf (eps already -> 0).
    big_M = [*ADAPT_M, 10**4, 10**7]
    big_cost = [(1.0 / M) ** S_LEFT for M in big_M]
    assert all(big_cost[i] > big_cost[i + 1] for i in range(len(big_cost) - 1)), (
        "adaptive cost (1/M)^s must strictly decrease in M"
    )
    assert big_cost[-1] < 1e-2, f"adaptive cost at M={big_M[-1]} is {big_cost[-1]:.4f}, not < 1e-2"
    # and the tiny-interval term vanishes as eps -> 0 (so the limit really is (1/M)^s):
    tail_term = [(ADAPT_M[-1] - 1) * eps**S_LEFT for eps in (1e-4, 1e-8, 1e-16)]
    assert all(tail_term[i] > tail_term[i + 1] for i in range(len(tail_term) - 1)) and tail_term[-1] < 1e-2, (
        "(M-1) eps^s must vanish as eps -> 0"
    )

    # (3) Cantor: N(3^-m) == 2^m exactly (m=1..8); slope == log2/log3; adaptive sum == 1 (no gain).
    for m in range(1, 9):
        assert len(cantor_intervals(m)) == 2**m, f"Cantor level {m} must have 2^m intervals"
    assert abs(right_slope - DIM_C) < 1e-6, f"Cantor slope {right_slope} != log2/log3"
    assert all(abs(c - 1.0) < 1e-9 for c in right_cost), "Cantor natural-cover sum must be 1 at s=dim"

    # (4) ordering dim_H <= dim_box in both; gaps 0.5 (left) and 0.0 (right), both >= 0.
    gap_left = DIM_BOX_LEFT - 0.0
    gap_right = DIM_C - DIM_C
    assert gap_left >= 0 and gap_right >= 0, "dim_H <= dim_box must hold in both cases"
    assert abs(gap_left - 0.5) < 1e-12 and abs(gap_right) < 1e-12

    math_check(
        "differ {1/n}: dim_box=1/2 vs dim_H=0;  agree Cantor: both log2/log3",
        [
            ("{1/n} occupied cells N(delta)", "  ".join(f"1/{2**k}:{N}" for k, N in zip(LEFT_KS, left_N, strict=True))),
            ("{1/n} box slope (fit -> 1/2)", f"{left_slope:.4f}   (want in (0.42,0.58))"),
            ("{1/n} adaptive (1/M)^0.3, M=4..64", "  ".join(f"{c:.3f}" for c in left_cost) + "  -> 0"),
            ("{1/n} adaptive at M=1e7", f"(1/M)^0.3 = {big_cost[-1]:.4f}   (< 1e-2)"),
            ("{1/n}: dim_H = 0,  dim_box = 1/2", f"gap = {gap_left:.4f}"),
            ("Cantor N(3^-m), m=1..6", "  ".join(str(N) for N in right_N) + "  (= 2^m)"),
            ("Cantor box slope", f"{right_slope:.4f} = log2/log3 = {DIM_C:.4f}"),
            ("Cantor adaptive sum (2*3^-s)^m", "  ".join(f"{c:.3f}" for c in right_cost) + "  (= 1)"),
            ("Cantor: dim_H = dim_box = log2/log3", f"gap = {gap_right:.4f}"),
            ("ordering", "dim_H <= dim_box holds in both (gaps 0.5 and 0.0, both >= 0)"),
        ],
    )

    # Figure
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.patches as mpatches
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(13.5, 7.6))
    gs = fig.add_gridspec(
        2, 2, height_ratios=[1.0, 1.15], hspace=0.42, wspace=0.22, left=0.06, right=0.975, top=0.9, bottom=0.09
    )
    ax_setL = fig.add_subplot(gs[0, 0])
    ax_setR = fig.add_subplot(gs[0, 1])
    ax_plotL = fig.add_subplot(gs[1, 0])
    ax_plotR = fig.add_subplot(gs[1, 1])
    fig.suptitle("dim_H <= dim_box:  {1/n} differ (0.5 vs 0),  Cantor agree", fontsize=14, y=0.965)

    def _bar(ax, x0, w, color, alpha, z=1):
        ax.add_patch(
            mpatches.Rectangle(
                (x0, 0.0), w, HBAR, facecolor=color, edgecolor=color, alpha=alpha, linewidth=0.3, zorder=z
            )
        )

    def strip_axes(ax):
        ax.set_xlim(-0.02, 1.02)
        ax.set_ylim(-0.15, 1.2)
        ax.set_yticks([])
        ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
        ax.tick_params(labelsize=8)
        ax.spines[["top", "right", "left"]].set_visible(False)

    # build the frame schedule: [box0]*START + box + [boxN]*MID + adapt + [adaptK]*END
    box_descs = [("box", i) for i in range(len(LEFT_KS))]
    adapt_descs = [("adapt", j) for j in range(len(ADAPT_M))]
    schedule = (
        [box_descs[0]] * START_HOLD
        + box_descs
        + [box_descs[-1]] * MID_HOLD
        + adapt_descs
        + [adapt_descs[-1]] * END_HOLD
    )

    # dot positions for 1/n (a visible sample; the crowd near 0 shows the pile-up)
    dots_x = np.array([1.0 / n for n in range(1, 121)])

    def draw_left_set(desc):
        ax_setL.cla()
        strip_axes(ax_setL)
        ax_setL.set_xlabel("x", fontsize=8, labelpad=1)
        kind, idx = desc
        if kind == "box":
            delta = left_deltas[idx]
            cells = left_cells[idx]
            for c in cells:  # occupied cells light up
                _bar(ax_setL, c * delta, delta, COLORS["region"], 0.9)
            if 1.0 / delta <= 40:  # grid only while it stays legible
                for t in np.arange(0, 1.0 + delta / 2, delta):
                    ax_setL.plot([t, t], [0, HBAR], color=COLORS["muted"], lw=0.35, zorder=2)
            ax_setL.plot(dots_x, np.full_like(dots_x, 0.5 * HBAR), "o", color=COLORS["needle"], ms=2.6, zorder=3)
            ax_setL.set_title(
                f"{{1/n}}: uniform grid delta = 1/{round(1 / delta)},  N = {left_N[idx]} cells", fontsize=10
            )
        else:
            M = ADAPT_M[idx]
            _bar(ax_setL, 0.0, 1.0 / M, COLORS["region"], 0.9)  # one interval swallows the tail
            for k in range(1, M):  # M-1 tiny intervals on 1/1..1/(M-1)
                _bar(ax_setL, 1.0 / k - 0.0025, 0.005, COLORS["accent"], 0.95, z=4)
            ax_setL.plot(dots_x, np.full_like(dots_x, 0.5 * HBAR), "o", color=COLORS["needle"], ms=2.6, zorder=3)
            ax_setL.annotate(
                "[0, 1/M]",
                xy=(1.0 / M, 1.02),
                xytext=(1.0 / M + 0.08, 1.12),
                fontsize=8,
                color=COLORS["guide"],
                arrowprops=dict(arrowstyle="->", color=COLORS["guide"], lw=0.8),
            )
            ax_setL.set_title(f"{{1/n}}: [0, 1/{M}] + {M - 1} tiny  (dim_H = 0)", fontsize=10)

    def draw_right_set(desc):
        ax_setR.cla()
        strip_axes(ax_setR)
        ax_setR.set_xlabel("x", fontsize=8, labelpad=1)
        kind, idx = desc
        if kind == "box":
            ridx = min(idx, len(RIGHT_MS) - 1)  # Cantor has fewer levels than the left ladder
            m = RIGHT_MS[ridx]
            for a, b in right_ivs[ridx]:
                _bar(ax_setR, a, b - a, COLORS["region"], 0.95)
            ax_setR.set_title(f"Cantor: delta = 1/3^{m},  N = {right_N[ridx]} = 2^{m}", fontsize=10)
        else:
            m = RIGHT_MS[-1]
            for a, b in right_ivs[-1]:  # natural cover already optimal
                _bar(ax_setR, a, b - a, COLORS["region"], 0.55)
                _bar(ax_setR, a, b - a, COLORS["accent"], 0.9)
            ax_setR.set_title(f"Cantor: natural cover optimal  (dim_H = {DIM_C:.4f})", fontsize=10)

    def draw_left_plot(desc):
        ax_plotL.cla()
        ax_plotL.grid(True, color=COLORS["muted"], alpha=0.25, lw=0.5)
        kind, idx = desc
        if kind == "box":
            upto = idx + 1
            ax_plotL.set_xlim(0, left_lx[-1] + 0.4)
            ax_plotL.set_ylim(0, left_ly[-1] + 0.5)
            ax_plotL.set_xlabel("log(1/delta)", fontsize=9)
            ax_plotL.set_ylabel("log N", fontsize=9)
            ax_plotL.plot(left_lx[:upto], left_ly[:upto], "-o", color=COLORS["needle"], ms=5)
            ax_plotL.plot(left_lx[upto - 1], left_ly[upto - 1], "o", color=COLORS["needle"], ms=11, mfc="none", mew=2)
            if upto >= 2:
                m = float(np.polyfit(left_lx[:upto], left_ly[:upto], 1)[0])
                ax_plotL.set_title(f"{{1/n}} box-count: slope {m:.3f} -> 1/2", fontsize=10)
            else:
                ax_plotL.set_title("{1/n} box-count: slope -> 1/2", fontsize=10)
        else:
            upto = idx + 1
            xs = [math.log2(M) for M in ADAPT_M]
            ax_plotL.set_xlim(1.5, xs[-1] + 0.5)
            ax_plotL.set_ylim(-0.05, 0.75)
            ax_plotL.set_xlabel("log2 M", fontsize=9)
            ax_plotL.set_ylabel("sum (diam)^s", fontsize=9)
            ax_plotL.axhline(0.0, color=COLORS["guide"], lw=0.8, ls="--")
            ax_plotL.plot(xs[:upto], left_cost[:upto], "-o", color=COLORS["accent"], ms=5)
            ax_plotL.plot(xs[upto - 1], left_cost[upto - 1], "o", color=COLORS["accent"], ms=11, mfc="none", mew=2)
            ax_plotL.set_title(f"{{1/n}} Hausdorff s={S_LEFT}: (1/M)^s = {left_cost[upto - 1]:.3f} -> 0", fontsize=10)
            ax_plotL.text(
                0.03,
                0.06,
                "gap = dim_box - dim_H = 0.5",
                transform=ax_plotL.transAxes,
                fontsize=10,
                color=COLORS["outer"],
            )

    def draw_right_plot(desc):
        ax_plotR.cla()
        ax_plotR.grid(True, color=COLORS["muted"], alpha=0.25, lw=0.5)
        kind, idx = desc
        if kind == "box":
            upto = min(idx + 1, len(RIGHT_MS))  # Cantor ladder is shorter; stop adding points
            ax_plotR.set_xlim(0, right_lx[-1] + 0.4)
            ax_plotR.set_ylim(0, right_ly[-1] + 0.5)
            ax_plotR.set_xlabel("log(1/delta)", fontsize=9)
            ax_plotR.set_ylabel("log N", fontsize=9)
            ax_plotR.plot(right_lx[:upto], right_ly[:upto], "-o", color=COLORS["needle"], ms=5)
            ax_plotR.plot(right_lx[upto - 1], right_ly[upto - 1], "o", color=COLORS["needle"], ms=11, mfc="none", mew=2)
            if upto >= 2:
                m = float(np.polyfit(right_lx[:upto], right_ly[:upto], 1)[0])
                ax_plotR.set_title(f"Cantor box-count: slope {m:.4f} = log2/log3", fontsize=10)
            else:
                ax_plotR.set_title("Cantor box-count: slope = log2/log3", fontsize=10)
        else:
            ax_plotR.set_xlim(right_lx[0] - 0.3, right_lx[-1] + 0.4)
            ax_plotR.set_ylim(-0.05, 1.35)
            ax_plotR.set_xlabel("log(1/delta)", fontsize=9)
            ax_plotR.set_ylabel("sum (diam)^s at s=dim", fontsize=9)
            ax_plotR.axhline(1.0, color=COLORS["guide"], lw=0.8, ls="--")
            ax_plotR.plot(right_lx, right_cost, "-o", color=COLORS["accent"], ms=5)
            ax_plotR.set_title("Cantor Hausdorff: sum = 1, no gain", fontsize=10)
            ax_plotR.text(
                0.03,
                0.06,
                "gap = dim_box - dim_H = 0.0",
                transform=ax_plotR.transAxes,
                fontsize=10,
                color=COLORS["outer"],
            )

    def update(fi):
        desc = schedule[fi]
        draw_left_set(desc)
        draw_right_set(desc)
        draw_left_plot(desc)
        draw_right_plot(desc)
        return []

    anim = FuncAnimation(fig, update, frames=len(schedule), interval=150, blit=False)
    print("wrote", save_gif(anim, fps=8, dpi=95))


if __name__ == "__main__":
    main()
