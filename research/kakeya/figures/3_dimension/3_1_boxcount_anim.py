"""Animation: Minkowski box-counting dimension as delta shrinks (section 3a of ../kakeya.md).

Mirrors dimension_boxcount.py in motion. delta shrinks through 1/2, 1/4, ..., 1/64 over two sets:

  * a unit segment   -> covering box count  N(delta) = delta^-1   (dimension 1)
  * a filled unit sq -> covering box count  N(delta) = delta^-2   (dimension 2)

The delta-grid, the shaded covering boxes and the running count animate on the left/middle panels;
the right panel plots log N against log(1/delta), a point per delta, and fits the slope. The two
point-clouds ride lines of slope 1 (segment) and 2 (square): those slopes ARE the box dimensions

    dim_box K = lim_{delta->0} log N(delta) / log(1/delta).

Geometric honesty: N is measured by actually testing every grid box against the set (Liang-Barsky
for the segment), not asserted; the invariant N(seg)=1/delta, N(sq)=(1/delta)^2 is checked per delta.

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/boxcount_anim.py
"""
import math

import numpy as np
from _shared import COLORS, math_check, save_gif
from matplotlib.animation import FuncAnimation

DELTAS = [1 / 2, 1 / 4, 1 / 8, 1 / 16, 1 / 32, 1 / 64]
HOLD = 6          # frames held per delta stage
END_HOLD = 8      # extra hold on the final (finest) stage
SEG_Y = 0.55      # horizontal unit segment, strictly inside one grid row


# --- geometry: pure-numpy box-counting (honest measurement, mirrors the static figure) ----
def _seg_hits_box(p0, p1, xmin, xmax, ymin, ymax):
    """Liang-Barsky: does segment p0->p1 meet the closed axis-aligned box? (touch counts)."""
    x0, y0 = p0
    dx, dy = p1[0] - x0, p1[1] - y0
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, x0 - xmin), (dx, xmax - x0), (-dy, y0 - ymin), (dy, ymax - y0)):
        if abs(p) < 1e-15:
            if q < 0:
                return False
            continue
        r = q / p
        if p < 0:
            t0 = max(t0, r)
        else:
            t1 = min(t1, r)
        if t0 > t1:
            return False
    return True


def boxcount_segment(p0, p1, delta):
    """Boxes of side delta (grid over [0,1]^2) the segment meets; returns (count, hit indices)."""
    n = round(1.0 / delta)
    hits = [(i, j) for i in range(n) for j in range(n)
            if _seg_hits_box(p0, p1, i * delta, (i + 1) * delta, j * delta, (j + 1) * delta)]
    return len(hits), hits


def main():
    seg_p0, seg_p1 = np.array([0.0, SEG_Y]), np.array([1.0, SEG_Y])

    # precompute (once) the honest box count + hit boxes for every delta stage
    stages = []
    for delta in DELTAS:
        n = round(1.0 / delta)
        n_seg, hits_seg = boxcount_segment(seg_p0, seg_p1, delta)
        n_sq = n * n
        stages.append(dict(delta=delta, n=n, n_seg=n_seg, hits_seg=hits_seg, n_sq=n_sq))

    # invariant + log-log data
    logs_x = [math.log(1.0 / s["delta"]) for s in stages]
    logs_seg = [math.log(s["n_seg"]) for s in stages]
    logs_sq = [math.log(s["n_sq"]) for s in stages]
    slope_seg = float(np.polyfit(logs_x, logs_seg, 1)[0])
    slope_sq = float(np.polyfit(logs_x, logs_sq, 1)[0])

    rows = []
    ok = True
    for s in stages:
        want_seg, want_sq = round(1.0 / s["delta"]), round(1.0 / s["delta"]) ** 2
        good = s["n_seg"] == want_seg and s["n_sq"] == want_sq
        ok = ok and good
        rows.append((f"delta=1/{s['n']:<2d}",
                     f"N_seg={s['n_seg']:<4d}(=1/d {want_seg})  "
                     f"N_sq={s['n_sq']:<5d}(=(1/d)^2 {want_sq})  {'OK' if good else 'BAD'}"))
    assert ok, "box counts must equal 1/delta and (1/delta)^2 at every stage"
    assert abs(slope_seg - 1.0) < 1e-9 and abs(slope_sq - 2.0) < 1e-9

    math_check(
        "box-counting dimension: N(delta) ~ delta^-d, slope = d",
        [
            *rows,
            ("fitted slope, segment", f"{slope_seg:.4f}   (want 1)"),
            ("fitted slope, square", f"{slope_sq:.4f}   (want 2)"),
            ("dim_box = lim log N / log(1/delta)", "1 (segment), 2 (square)"),
        ],
    )

    # ---- figure ----
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 3, figsize=(15.5, 5.3))
    for a in (ax[0], ax[1]):
        a.set_aspect("equal")
        a.set_xticks([]); a.set_yticks([])
    axL = ax[2]  # log-log panel

    def draw_grid_axes(a):
        a.set_xlim(-0.05, 1.05); a.set_ylim(-0.05, 1.05)
        a.set_xticks([]); a.set_yticks([])

    frame_stage = []
    for k in range(len(stages)):
        frame_stage += [k] * HOLD
    frame_stage += [len(stages) - 1] * END_HOLD

    def update(fi):
        s = stages[frame_stage[fi]]
        upto = frame_stage[fi] + 1
        delta, n = s["delta"], s["n"]

        # left: unit segment + covering boxes
        ax[0].cla(); draw_grid_axes(ax[0])
        for (i, j) in s["hits_seg"]:
            ax[0].fill([i * delta, (i + 1) * delta, (i + 1) * delta, i * delta],
                       [j * delta, j * delta, (j + 1) * delta, (j + 1) * delta],
                       color=COLORS["region"], alpha=0.75, zorder=1)
        for kk in range(n + 1):
            ax[0].plot([0, 1], [kk * delta, kk * delta], color=COLORS["muted"], lw=0.4, zorder=2)
            ax[0].plot([kk * delta, kk * delta], [0, 1], color=COLORS["muted"], lw=0.4, zorder=2)
        ax[0].plot([0, 1], [SEG_Y, SEG_Y], color=COLORS["needle"], lw=3.0, zorder=3)
        ax[0].set_title(f"unit segment,  delta=1/{n}\nN = {s['n_seg']} = 1/delta   (d = 1)")

        # middle: unit square (every box covered) + grid
        ax[1].cla(); draw_grid_axes(ax[1])
        ax[1].fill([0, 1, 1, 0], [0, 0, 1, 1], color=COLORS["region"], alpha=0.75, zorder=1)
        for kk in range(n + 1):
            ax[1].plot([0, 1], [kk * delta, kk * delta], color=COLORS["muted"], lw=0.4, zorder=2)
            ax[1].plot([kk * delta, kk * delta], [0, 1], color=COLORS["muted"], lw=0.4, zorder=2)
        ax[1].fill([0, 1, 1, 0], [0, 0, 1, 1], facecolor="none",
                   edgecolor=COLORS["needle"], lw=2.2, zorder=3)
        ax[1].set_title(f"unit square,  delta=1/{n}\nN = {s['n_sq']} = (1/delta)^2   (d = 2)")

        # right: log N vs log(1/delta), a point per delta so far, slope fits
        axL.cla()
        axL.set_xlim(0, logs_x[-1] + 0.5)
        axL.set_ylim(0, logs_sq[-1] + 0.5)
        axL.set_xlabel("log(1/delta)"); axL.set_ylabel("log N")
        axL.grid(True, color=COLORS["muted"], alpha=0.25, lw=0.5)
        xs = logs_x[:upto]
        axL.plot(xs, logs_seg[:upto], "-o", color=COLORS["needle"], ms=5, label="segment (slope 1)")
        axL.plot(xs, logs_sq[:upto], "-o", color=COLORS["accent"], ms=5, label="square (slope 2)")
        axL.plot(logs_x[upto - 1], logs_seg[upto - 1], "o", color=COLORS["needle"],
                 ms=11, mfc="none", mew=2)
        axL.plot(logs_x[upto - 1], logs_sq[upto - 1], "o", color=COLORS["accent"],
                 ms=11, mfc="none", mew=2)
        if upto >= 2:
            m1 = float(np.polyfit(xs, logs_seg[:upto], 1)[0])
            m2 = float(np.polyfit(xs, logs_sq[:upto], 1)[0])
            axL.set_title(f"log-log slope -> box dimension\nsegment {m1:.3f},   square {m2:.3f}")
        else:
            axL.set_title("log-log slope -> box dimension")
        axL.legend(loc="upper left", fontsize=9)
        return []

    anim = FuncAnimation(fig, update, frames=len(frame_stage), interval=180, blit=False)
    print("wrote", save_gif(anim, fps=6, dpi=95))


if __name__ == "__main__":
    main()
