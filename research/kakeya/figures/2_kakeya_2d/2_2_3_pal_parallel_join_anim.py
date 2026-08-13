"""Animation: moving a needle between two parallel lines, parallelogram vs the far detour (kakeya.md 2d).

Accromath, kakeya14-16: to slide a unit needle from one line to a parallel line a distance d away, the
obvious region is a parallelogram of area L*d. Far better (kakeya16): slide the needle ALONG its own
axis (area 0), make the turn far out where a small angle alpha suffices, then slide back. Only the two
small rotations cost area, 2 * (1/2 L^2 alpha) = L^2 alpha, and "plus le deplacement est grand, plus
l'angle est petit": the detour can be pushed out to make alpha, hence the area, as small as wanted.

Phase 0 shows the parallelogram (area L*d). Then the needle travels the detour, accumulating only the
two rotation sectors.

Run: PYTHONPATH=research/kakeya/figures uv run --with matplotlib --with shapely --with pillow \
     python research/kakeya/figures/2_kakeya_2d/2_2_3_pal_parallel_join_anim.py
"""

import math

import numpy as np
from _shared import COLORS, math_check, poly, save_gif

L = 1.0  # needle length
D_SEP = 0.5  # distance between the two parallel lines
ALPHA = 0.28  # turn angle far out (rad)
DETOUR = 1.4  # how far right the needle slides before turning
U = np.array([-math.cos(ALPHA), math.sin(ALPHA)])  # diagonal direction after the first turn

E = np.array([DETOUR + 1.0, 0.0])  # first pivot (far-right end on the bottom line)
LAM = D_SEP / math.sin(ALPHA)  # slide up the diagonal until the pivot end reaches y = d
PIVOT2 = E + LAM * U  # second pivot, on the top line y = d
TARGET = np.array([PIVOT2[0] - 0.18, D_SEP])  # final needle right-end on the top line

N1, N2, N3, N4, N5 = 12, 12, 12, 12, 10
HOLD0, END_HOLD = 8, 8


def wedge(center, a0, a1, r=L, n=24):
    """Sector polygon at `center`, radius r, sweeping angle a0 -> a1 (radians)."""
    a = np.linspace(a0, a1, n)
    pts = [tuple(center), *[(center[0] + r * math.cos(t), center[1] + r * math.sin(t)) for t in a]]
    return np.array(pts)


def main():
    par_area = L * D_SEP  # parallelogram area
    sector_area = 0.5 * L**2 * ALPHA  # one rotation sector
    detour_area = 2 * sector_area  # total swept area of the clever move

    assert detour_area < par_area, "the detour must beat the parallelogram"
    # measured sector area matches 1/2 L^2 alpha
    meas = poly(wedge(E, math.pi, math.pi - ALPHA, n=200)).area
    assert abs(meas - sector_area) / sector_area < 0.01, "sector area must be 1/2 L^2 alpha"

    math_check(
        "parallel-needle move: parallelogram L*d vs detour 2*(1/2 L^2 alpha)",
        [
            ("needle / separation", f"L = {L}, d = {D_SEP}"),
            ("turn angle far out", f"alpha = {ALPHA:.3f} rad = {math.degrees(ALPHA):.1f} deg"),
            ("parallelogram area", f"L*d = {par_area:.3f}"),
            ("one rotation sector", f"1/2 L^2 alpha = {sector_area:.3f}  (measured {meas:.3f})"),
            ("detour swept area", f"2 sectors = {detour_area:.3f}  (< {par_area:.3f})"),
            ("shrinks how", "push the detour out -> smaller alpha -> area -> 0 (slides are free)"),
        ],
    )

    # --- choreography: needle endpoints (A, B) through the phases -------------------------
    start = (np.array([0.0, 0.0]), np.array([1.0, 0.0]))  # bottom needle, pointing right

    def needle(phase, f):
        if phase == 0:  # hold at start
            return start
        if phase == 1:  # slide right along the bottom line (free)
            sx = (DETOUR) * f
            return (np.array([sx, 0.0]), np.array([sx + 1.0, 0.0]))
        if phase == 2:  # rotate about E by alpha (cost: sector 1)
            th = ALPHA * f
            return (E.copy(), E + np.array([-math.cos(th), math.sin(th)]))
        if phase == 3:  # slide up the diagonal (free)
            s = LAM * f
            return (E + s * U, E + np.array([-math.cos(ALPHA), math.sin(ALPHA)]) + s * U)
        if phase == 4:  # rotate about PIVOT2 back to flat (cost: sector 2)
            th = ALPHA * (1 - f)
            return (PIVOT2.copy(), PIVOT2 + np.array([-math.cos(th), math.sin(th)]))
        # phase 5: slide left along the top line to the target (free)
        endR = PIVOT2 + (TARGET - PIVOT2) * f
        return (endR, endR + np.array([-1.0, 0.0]))

    plan = [(0, HOLD0), (1, N1), (2, N2), (3, N3), (4, N4), (5, N5)]
    frames = []
    for phase, n in plan:
        for i in range(n):
            frames.append((phase, (i + 1) / n))
    frames += [(5, 1.0)] * END_HOLD

    # ---- figure -------------------------------------------------------------------------
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    xs = [start[0][0], E[0], PIVOT2[0], TARGET[0] - 1.0]
    xlo, xhi = min(xs) - 0.2, max(xs) + 0.3
    fig, ax = plt.subplots(figsize=(9.2, 4.2))
    ax.set_aspect("equal")
    ax.axis("off")

    par = np.array([start[0], start[1], TARGET, TARGET + np.array([-1.0, 0.0])])  # parallelogram

    def update(fi):
        phase, f = frames[fi]
        ax.cla()
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(xlo, xhi)
        ax.set_ylim(-0.45, D_SEP + 0.55)
        # the two parallel lines
        ax.plot([xlo, xhi], [0, 0], color=COLORS["muted"], lw=0.8, alpha=0.6)
        ax.plot([xlo, xhi], [D_SEP, D_SEP], color=COLORS["muted"], lw=0.8, alpha=0.6)
        # start and target needles (ghosts)
        ax.plot([start[0][0], start[1][0]], [0, 0], color=COLORS["needle"], lw=2.5, alpha=0.35)
        ax.plot([TARGET[0], TARGET[0] - 1.0], [D_SEP, D_SEP], color=COLORS["needle"], lw=2.5, alpha=0.35)

        if phase == 0:  # show the naive parallelogram
            ax.fill(par[:, 0], par[:, 1], facecolor=COLORS["region"], edgecolor=COLORS["outer"], lw=1.2, alpha=0.7)
            ax.set_title(f"naive parallelogram: area = L*d = {par_area:.2f}", fontsize=11)
        else:
            # accumulated rotation sectors (the only cost)
            if phase >= 2:
                w1 = wedge(E, math.pi, math.pi - (ALPHA if phase > 2 else ALPHA * f))
                ax.fill(w1[:, 0], w1[:, 1], facecolor=COLORS["accent"], edgecolor="none", alpha=0.8, zorder=2)
            if phase >= 4:
                th = ALPHA if phase > 4 else ALPHA * f
                w2 = wedge(PIVOT2, math.pi, math.pi - th)
                ax.fill(w2[:, 0], w2[:, 1], facecolor=COLORS["accent"], edgecolor="none", alpha=0.8, zorder=2)
            swept = detour_area * (min(phase, 4) >= 2) if phase >= 2 else 0.0
            ax.set_title(f"detour: slide (free) + two small turns, area = {swept:.2f}", fontsize=11)

        A, B = needle(phase, f)
        ax.plot([A[0], B[0]], [A[1], B[1]], color=COLORS["needle"], lw=3.0, zorder=4)
        return []

    anim = FuncAnimation(fig, update, frames=len(frames), interval=90, blit=False)
    print("wrote", save_gif(anim, fps=11, dpi=95))


if __name__ == "__main__":
    main()
