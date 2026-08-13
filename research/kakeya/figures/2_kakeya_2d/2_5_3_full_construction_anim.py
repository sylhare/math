"""Animation: the whole 2D construction in one, all steps of kakeya19 (kakeya.md 2d-2e).

One continuous story, top to bottom of the Accromath kakeya19 figure:
  1. the triangle carries a 60-degree fan; the needle sweeps it.
  2. CUT the base into 2^n thin sub-triangles (all share the apex).
  3. SHIFT the pieces to overlap (the sprout): the footprint shrinks into the Perron tree.
  4. PAL JOIN: the small back-and-forth that turns the needle cheaply, slide out along the axis
     (free), rotate a little far out, slide back, so the needle can be turned continuously (a needle
     set), not merely contained (a Besicovitch set).

Run: PYTHONPATH=research/kakeya/figures uv run --with matplotlib --with shapely --with pillow \
     python research/kakeya/figures/2_kakeya_2d/2_5_3_full_construction_anim.py
"""

import math

import numpy as np
from _shared import COLORS, math_check, save_gif
from shapely.affinity import translate as shp_translate
from shapely.geometry import Polygon
from shapely.ops import unary_union

APEX = np.array([0.0, 1.0])  # height-1 triangle: unit needles from the apex fit
HB = 1.0 / math.sqrt(3.0)  # half base
NLEV = 4
TRI = Polygon([(-HB, 0.0), (HB, 0.0), tuple(APEX)])
TRI_AREA = TRI.area
AR = math.atan2(-1.0, HB)  # apex -> right corner
AL = math.atan2(-1.0, -HB)  # apex -> left corner

# Pal-join detour parameters (phase 4), done above the apex where a small angle suffices
PAL_ALPHA = 0.33
PAL_OUT = 1.1


def subdivided():
    xs = np.linspace(-HB, HB, 2**NLEV + 1)
    return [Polygon([(xs[i], 0.0), (xs[i + 1], 0.0), tuple(APEX)]) for i in range(2**NLEV)]


def sprout(alpha):
    pieces = [[p] for p in subdivided()]
    w = 2 * HB / 2**NLEV
    for _ in range(NLEV):
        step = 0.5 * alpha * w
        pieces = [
            [shp_translate(p, xoff=+step) for p in pieces[i]] + [shp_translate(p, xoff=-step) for p in pieces[i + 1]]
            for i in range(0, len(pieces), 2)
        ]
        w *= 1.0 + alpha
    return unary_union([p for g in pieces for p in g])


def wedge(center, a0, a1, r=1.0, n=24):
    a = np.linspace(a0, a1, n)
    return np.array([tuple(center), *[(center[0] + r * math.cos(t), center[1] + r * math.sin(t)) for t in a]])


def main():
    alphas = np.linspace(0.0, 0.6, 16)
    area_frac = [sprout(a).area / TRI_AREA for a in alphas]
    assert abs(area_frac[0] - 1.0) < 1e-6 and area_frac[-1] < 0.6, "sprout must cut area from 100%"
    pal_sector = 0.5 * PAL_ALPHA  # area of one small far-out rotation

    math_check(
        "full construction: fan -> cut -> shift (tree) -> pal join",
        [
            ("sub-triangles", f"2^{NLEV} = {2**NLEV} (shared apex, 60 deg fan)"),
            ("shift shrinks area", f"{area_frac[0] * 100:.0f}% -> {area_frac[-1] * 100:.0f}% of the triangle"),
            ("pal join far out", f"alpha = {PAL_ALPHA} rad, one small sector = {pal_sector:.3f} (shrinks with the detour)"),
            ("needle length", "1 in every phase (apex fan and the pal detour)"),
        ],
    )

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    tri_xy = np.array(TRI.exterior.coords)
    xs_div = np.linspace(-HB, HB, 2**NLEV + 1)
    u_down = np.array([0.0, -1.0])  # altitude direction (apex -> base midpoint)

    SWEEP, CUT, SHIFT, PAL, HOLD = 20, 8, len(alphas), 30, 8
    frames = ([("sweep", (i + 1) / SWEEP) for i in range(SWEEP)]
              + [("cut", 1.0)] * CUT
              + [("shift", i) for i in range(SHIFT)] + [("shift", SHIFT - 1)] * 4
              + [("pal", (i + 1) / PAL) for i in range(PAL)]
              + [("pal", 1.0)] * HOLD)

    fig, ax = plt.subplots(figsize=(6.4, 6.6))

    def fan_needle(frac):
        ang = AR + (AL - AR) * frac
        return APEX, APEX + np.array([math.cos(ang), math.sin(ang)])

    def draw_tree(alpha):
        g = sprout(alpha)
        for gg in (g.geoms if g.geom_type == "MultiPolygon" else [g]):
            ax.fill(*gg.exterior.xy, facecolor=COLORS["region"], edgecolor=COLORS["outer"], lw=0.7, alpha=0.7)

    def update(fi):
        kind, val = frames[fi]
        ax.cla()
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-0.95, 0.95)
        ax.set_ylim(-0.15, 2.05)

        if kind == "sweep":
            ax.fill(tri_xy[:, 0], tri_xy[:, 1], facecolor=COLORS["region"], edgecolor=COLORS["outer"], lw=1.2, alpha=0.6)
            for g in np.linspace(0.0, val, 6):
                a, b = fan_needle(g)
                ax.plot([a[0], b[0]], [a[1], b[1]], color=COLORS["needle"], lw=0.7, alpha=0.3)
            a, b = fan_needle(val)
            ax.plot([a[0], b[0]], [a[1], b[1]], color=COLORS["needle"], lw=3.0, zorder=4)
            ax.set_title("1. the triangle and its 60 deg fan", fontsize=12)

        elif kind == "cut":
            ax.fill(tri_xy[:, 0], tri_xy[:, 1], facecolor=COLORS["region"], edgecolor=COLORS["outer"], lw=1.2, alpha=0.6)
            for x in xs_div:
                ax.plot([x, APEX[0]], [0.0, APEX[1]], color=COLORS["guide"], lw=0.5, alpha=0.8)
            ax.set_title(f"2. cut the base into 2^{NLEV} = {2**NLEV} pieces", fontsize=12)

        elif kind == "shift":
            draw_tree(alphas[val])
            ax.set_title(f"3. shift to overlap: area {area_frac[val] * 100:.0f}% of the triangle", fontsize=12)

        else:  # pal join: slide out along the axis, small rotate far out, slide back
            draw_tree(alphas[-1])
            f = val
            base = APEX  # start the needle at the apex, pointing down the altitude
            if f < 0.4:  # slide out (up) along its own axis
                s = PAL_OUT * (f / 0.4)
                a = base - u_down * s
                b = a + u_down  # length 1, pointing down
                ax.plot([a[0], b[0]], [a[1], b[1]], color=COLORS["needle"], lw=3.0, zorder=4)
                ax.annotate("", xy=tuple(a), xytext=tuple(a + 0.35 * u_down),
                            arrowprops=dict(arrowstyle="->", color=COLORS["needle"], lw=1.4))
                ax.set_title("4. Pal join: slide out along the axis (free)", fontsize=12)
            elif f < 0.7:  # small rotation far out
                th = PAL_ALPHA * ((f - 0.4) / 0.3)
                top = base - u_down * PAL_OUT
                d = np.array([math.sin(th), -math.cos(th)])  # rotate the downward needle by th
                ax.fill(*wedge(top, -math.pi / 2, -math.pi / 2 + th).T, facecolor=COLORS["accent"], alpha=0.8, zorder=2)
                ax.plot([top[0], top[0] + d[0]], [top[1], top[1] + d[1]], color=COLORS["needle"], lw=3.0, zorder=4)
                ax.set_title("4. Pal join: rotate a little where it is cheap", fontsize=12)
            else:  # slide back, now pointing a touch differently
                s = PAL_OUT * (1 - (f - 0.7) / 0.3)
                top = base - u_down * PAL_OUT
                d = np.array([math.sin(PAL_ALPHA), -math.cos(PAL_ALPHA)])
                ax.fill(*wedge(top, -math.pi / 2, -math.pi / 2 + PAL_ALPHA).T, facecolor=COLORS["accent"], alpha=0.8, zorder=2)
                a = top + d * (PAL_OUT - s)
                ax.plot([a[0], a[0] + d[0]], [a[1], a[1] + d[1]], color=COLORS["needle"], lw=3.0, zorder=4)
                ax.annotate("", xy=tuple(a + d), xytext=tuple(a + 0.65 * d),
                            arrowprops=dict(arrowstyle="->", color=COLORS["needle"], lw=1.4))
                ax.set_title("4. Pal join: slide back, the needle has turned", fontsize=12)
        return []

    anim = FuncAnimation(fig, update, frames=len(frames), interval=110, blit=False)
    print("wrote", save_gif(anim, fps=9, dpi=95))


if __name__ == "__main__":
    main()
