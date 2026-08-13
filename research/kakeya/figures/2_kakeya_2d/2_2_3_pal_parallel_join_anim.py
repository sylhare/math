"""Animation: moving a needle between two parallel lines, parallelogram vs the far detour (kakeya.md 2d).

Accromath, kakeya14-16: to slide a unit needle from one line to a parallel line a distance d away, the
obvious region is a parallelogram of area L*d. Far better (kakeya16): slide the needle ALONG its own
axis (area 0), make the turn far out where a small angle alpha suffices, then slide back. Only the two
small rotations cost area, 2 * (1/2 L^2 alpha) = L^2 alpha, and "plus le deplacement est grand, plus
l'angle est petit": push the detour out to make alpha, hence the area, as small as wanted.

Phase 0 shows the parallelogram (area L*d); then the needle travels the detour, accumulating only the
two rotation sectors. Axis limits are taken from the whole choreography so nothing is clipped.

Run: PYTHONPATH=research/kakeya/figures uv run --with matplotlib --with shapely --with pillow \
     python research/kakeya/figures/2_kakeya_2d/2_2_3_pal_parallel_join_anim.py
"""

import math

import numpy as np
from _shared import COLORS, math_check, poly, save_gif

L = 1.0  # needle length
D_SEP = 0.5  # distance between the two parallel lines
ALPHA = 0.30  # turn angle far out (rad)
DETOUR = 1.1  # how far right the needle slides before turning

U = np.array([-math.cos(ALPHA), math.sin(ALPHA)])  # diagonal direction after the first turn
E = np.array([DETOUR + 1.0, 0.0])  # first pivot (far-right end on the bottom line)
LAM = D_SEP / math.sin(ALPHA)  # slide up the diagonal until the pivot end reaches y = d
PIVOT2 = E + LAM * U  # second pivot, on the top line y = d
TARGET = np.array([PIVOT2[0] - 0.15, D_SEP])  # final needle right-end on the top line
START = (np.array([0.0, 0.0]), np.array([1.0, 0.0]))  # bottom needle, pointing right

N1, N2, N3, N4, N5 = 14, 12, 14, 12, 12
HOLD0, END_HOLD = 8, 8


def needle(phase, f):
    """Needle endpoints (A, B) at fraction f of the given phase."""
    if phase == 0:
        return START
    if phase == 1:  # slide right along the bottom line (free)
        sx = DETOUR * f
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
    endR = PIVOT2 + (TARGET - PIVOT2) * f  # phase 5: slide left along the top line (free)
    return (endR, endR + np.array([-1.0, 0.0]))


def wedge(center, a0, a1, r=L, n=28):
    a = np.linspace(a0, a1, n)
    return np.array([tuple(center), *[(center[0] + r * math.cos(t), center[1] + r * math.sin(t)) for t in a]])


def main():
    par_area = L * D_SEP
    sector_area = 0.5 * L**2 * ALPHA
    detour_area = 2 * sector_area
    assert detour_area < par_area, "the detour must beat the parallelogram"
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

    plan = [(0, HOLD0), (1, N1), (2, N2), (3, N3), (4, N4), (5, N5)]
    frames = [(p, (i + 1) / n) for p, n in plan for i in range(n)] + [(5, 1.0)] * END_HOLD

    par = np.array([START[0], START[1], TARGET, TARGET + np.array([-1.0, 0.0])])

    # --- bounding box over the WHOLE choreography (so nothing is clipped) -----------------
    pts = [par]
    for p, _ in plan:
        for i in range(21):
            A, B = needle(p, i / 20)
            pts.append(np.array([A, B]))
    pts.append(wedge(E, math.pi, math.pi - ALPHA))
    pts.append(wedge(PIVOT2, math.pi, math.pi - ALPHA))
    allp = np.vstack(pts)
    x0, y0 = allp.min(0)
    x1, y1 = allp.max(0)
    mx, my = 0.12 * (x1 - x0), 0.18 * (y1 - y0)
    xlo, xhi, ylo, yhi = x0 - mx, x1 + mx, y0 - my, y1 + my

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    # figure aspect matches the data box so nothing is squished
    w = 9.5
    h = max(3.2, w * (yhi - ylo) / (xhi - xlo)) + 0.5
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_aspect("equal")
    ax.axis("off")

    def update(fi):
        phase, f = frames[fi]
        ax.cla()
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(xlo, xhi)
        ax.set_ylim(ylo, yhi)
        ax.plot([xlo, xhi], [0, 0], color=COLORS["muted"], lw=0.9, alpha=0.6)
        ax.plot([xlo, xhi], [D_SEP, D_SEP], color=COLORS["muted"], lw=0.9, alpha=0.6)
        ax.plot([START[0][0], START[1][0]], [0, 0], color=COLORS["needle"], lw=3.0, alpha=0.3)
        ax.plot([TARGET[0], TARGET[0] - 1.0], [D_SEP, D_SEP], color=COLORS["needle"], lw=3.0, alpha=0.3)

        if phase == 0:
            ax.fill(par[:, 0], par[:, 1], facecolor=COLORS["region"], edgecolor=COLORS["outer"], lw=1.3, alpha=0.7)
            ax.set_title(f"naive parallelogram: area = L d = {par_area:.2f}", fontsize=12)
        else:
            if phase >= 2:
                th1 = ALPHA if phase > 2 else ALPHA * f
                w1 = wedge(E, math.pi, math.pi - th1)
                ax.fill(w1[:, 0], w1[:, 1], facecolor=COLORS["accent"], edgecolor="none", alpha=0.85, zorder=2)
            if phase >= 4:
                th2 = ALPHA if phase > 4 else ALPHA * f
                w2 = wedge(PIVOT2, math.pi, math.pi - th2)
                ax.fill(w2[:, 0], w2[:, 1], facecolor=COLORS["accent"], edgecolor="none", alpha=0.85, zorder=2)
            area_now = detour_area if phase >= 4 else (sector_area if phase >= 2 else 0.0)
            ax.set_title(f"detour: slide (free) + two small turns, area = {area_now:.2f}", fontsize=12)

        A, B = needle(phase, f)
        ax.plot([A[0], B[0]], [A[1], B[1]], color=COLORS["needle"], lw=3.6, zorder=4, solid_capstyle="round")
        return []

    anim = FuncAnimation(fig, update, frames=len(frames), interval=100, blit=False)
    print("wrote", save_gif(anim, fps=10, dpi=100))


if __name__ == "__main__":
    main()
