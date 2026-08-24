"""Animation: the convex answers, a unit needle turning in circle -> Reuleaux -> triangle (kakeya.md 2a-2c).

Accromath: "Pour le cercle, l'aiguille ne fait que tourner autour d'un meme point. En lui permettant de
tourner autour de plusieurs points, on ameliore notre resultat avec un triangle de Reuleaux. Si
maintenant, on fait tourner et bouger l'aiguille dans un triangle equilateral, alors le resultat
devient plus interessant."

Three panels, the same unit needle turning through every direction, accumulating its positions so the
region fills in; the area drops left to right:

  circle (spin about the centre)         area pi/4      = 0.785
  Reuleaux triangle (pivot about 3 pts)  area (pi-sqrt3)/2 = 0.705
  equilateral triangle (pivot + shift)   area 1/sqrt3   = 0.577

Run: PYTHONPATH=research/kakeya/figures uv run --with matplotlib --with shapely --with pillow \
     python research/kakeya/figures/2_kakeya_2d/2_1_3_convex_answers_anim.py
"""

import math

import numpy as np
from _shared import COLORS, circle, math_check, save_gif

STEPS = 20  # frames per 60-degree pivot (and for the circle half-turn)
END_HOLD = 8

# Circle: needle length 1 spun about its midpoint -> disc radius 1/2
DISC_R = 0.5


def circle_needles():
    out = []
    for a in np.linspace(0.0, math.pi, 3 * STEPS):
        d = np.array([math.cos(a), math.sin(a)])
        out.append((-0.5 * d, 0.5 * d))
    return out


# Reuleaux triangle of width 1: pivot the width-segment about each vertex
RV = np.array([[math.cos(math.radians(d)), math.sin(math.radians(d))] for d in (90, 210, 330)]) / math.sqrt(3.0)


def _arc(center, p0, p1, r=1.0, n=60):
    a0 = math.atan2(p0[1] - center[1], p0[0] - center[0])
    a1 = math.atan2(p1[1] - center[1], p1[0] - center[0])
    if a1 < a0:
        a1 += 2 * math.pi
    a = np.linspace(a0, a1, n)
    return np.column_stack([center[0] + r * np.cos(a), center[1] + r * np.sin(a)])


def reuleaux_outline():
    # each arc is centred at a vertex, radius 1, spanning the other two vertices
    segs = [_arc(RV[0], RV[1], RV[2]), _arc(RV[1], RV[2], RV[0]), _arc(RV[2], RV[0], RV[1])]
    return np.vstack(segs)


def reuleaux_needles():
    out = []
    for i, v in enumerate(RV):
        p, q = RV[(i + 1) % 3], RV[(i + 2) % 3]  # the two far vertices on the opposite arc
        a0 = math.atan2(p[1] - v[1], p[0] - v[0])
        a1 = math.atan2(q[1] - v[1], q[0] - v[0])
        if a1 < a0:
            a1 += 2 * math.pi
        for a in np.linspace(a0, a1, STEPS):
            out.append((v.copy(), v + np.array([math.cos(a), math.sin(a)])))  # length exactly 1
    return out


# Equilateral triangle of height 1: pivot the height-segment about each vertex
TH_APEX = np.array([0.0, 1.0])
TH_BL = np.array([-1.0 / math.sqrt(3.0), 0.0])
TH_BR = np.array([1.0 / math.sqrt(3.0), 0.0])
TVERTS = [TH_APEX, TH_BL, TH_BR]


def tri_needles():
    out = []
    for v in TVERTS:
        others = [u for u in TVERTS if not np.array_equal(u, v)]
        a0 = math.atan2(others[0][1] - v[1], others[0][0] - v[0])
        a1 = math.atan2(others[1][1] - v[1], others[1][0] - v[0])
        if a1 < a0:
            a0, a1 = a1, a0
        if a1 - a0 > math.pi:
            a0, a1 = a1, a0 + 2 * math.pi
        for a in np.linspace(a0, a1, STEPS):
            out.append((v.copy(), v + np.array([math.cos(a), math.sin(a)])))  # length exactly 1
    return out


def main():
    cN, rN, tN = circle_needles(), reuleaux_needles(), tri_needles()
    areas = (math.pi / 4, (math.pi - math.sqrt(3.0)) / 2, 1.0 / math.sqrt(3.0))

    # Every needle has length exactly 1
    for name, lst in (("circle", cN), ("reuleaux", rN), ("triangle", tN)):
        mx = max(abs(np.linalg.norm(b - a) - 1.0) for a, b in lst)
        assert mx < 1e-9, f"{name}: every needle must have length 1 (err {mx:.1e})"

    math_check(
        "convex answers: needle turns in circle -> Reuleaux -> triangle, area drops",
        [
            ("circle (disc r=1/2)", f"area pi/4 = {areas[0]:.3f}"),
            ("Reuleaux (width 1)", f"area (pi-sqrt3)/2 = {areas[1]:.3f}  (< pi/4)"),
            ("equilateral (height 1)", f"area 1/sqrt3 = {areas[2]:.3f}  (< Reuleaux)"),
            ("needle", "length exactly 1 in all three (fixed)"),
            ("motion", "circle: 1 pivot point; Reuleaux/triangle: pivot about each of 3 vertices"),
        ],
    )

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    disc = circle(DISC_R, 200)
    reul = reuleaux_outline()
    tri = np.array([TH_APEX, TH_BL, TH_BR, TH_APEX])

    fig, axes = plt.subplots(1, 3, figsize=(13.2, 5.0))
    titles = [f"circle: spin about a point\narea pi/4 = {areas[0]:.3f}",
              f"Reuleaux: pivot about 3 points\narea (pi-sqrt3)/2 = {areas[1]:.3f}",
              f"equilateral triangle\narea 1/sqrt3 = {areas[2]:.3f}"]
    outlines = [disc, reul, tri]
    needle_lists = [cN, rN, tN]
    # Recentre each shape on its centroid (only the height-1 triangle sits off-origin, centroid y=1/3)
    # so all three line up horizontally and vertically inside one shared, symmetric axis box.
    off = [np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, -1.0 / 3.0])]
    outlines = [outlines[j] + off[j] for j in range(3)]
    needle_lists = [[(a + off[j], b + off[j]) for a, b in needle_lists[j]] for j in range(3)]
    # Size each panel to its own shape's radius (same 1.18 margin as the non-convex figure) so both
    # answer gifs render each shape at the same on-screen size, with the three panels aligned.
    lim = [float(np.max(np.hypot(o[:, 0], o[:, 1]))) * 1.18 for o in outlines]
    nframes = max(len(cN), len(rN), len(tN))
    frames = list(range(nframes)) + [nframes - 1] * END_HOLD

    def update(fi):
        k = frames[fi]
        for j, ax in enumerate(axes):
            ax.cla()
            ax.set_aspect("equal")
            ax.axis("off")
            ax.set_xlim(-lim[j], lim[j])
            ax.set_ylim(-lim[j], lim[j])
            ax.plot(outlines[j][:, 0], outlines[j][:, 1], color=COLORS["guide"], lw=1.4)
            lst = needle_lists[j]
            upto = min(k + 1, len(lst))
            step = max(1, upto // 60)
            for a, b in lst[:upto:step]:  # accumulated needle fan
                ax.plot([a[0], b[0]], [a[1], b[1]], color=COLORS["needle"], lw=0.6, alpha=0.25)
            a, b = lst[upto - 1]
            ax.plot([a[0], b[0]], [a[1], b[1]], color=COLORS["accent"], lw=2.6, zorder=4)  # current needle
            ax.set_title(titles[j], fontsize=10)
        return []

    anim = FuncAnimation(fig, update, frames=len(frames), interval=90, blit=False)
    print("wrote", save_gif(anim, fps=12, dpi=92))


if __name__ == "__main__":
    main()
