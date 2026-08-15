"""Fefferman's ball-multiplier geometry (kakeya.md 5b).

Two dual pictures:
  Frequency: r x r^2 rectangles tangent to the unit circle |xi| = 1 (long side r along the tangent,
             thickness r^2 radial; inner edge at distance 1 from the centre).
  Physical:  dual (1/r) x (1/r^2) tubes through the origin, piling up there.

  frequency rectangle   r x r^2,     aspect r : r^2 = 1 : r
  physical tube         1/r^2 x 1/r, aspect 1/r^2 : 1/r = 1 : r
  duality               (r)(1/r) = 1,  (r^2)(1/r^2) = 1

N = 12 slabs tile the circle (chord r = 2 sin(pi/N)); physical panel draws 6 distinct orientations
(opposite tangent points share a tube).

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/fefferman_ball_multiplier.py
"""
import math

import numpy as np
from _shared import COLORS, circle, math_check, new_axes, save_preview


def freq_rectangle(phi: float, r: float, r2: float) -> np.ndarray:
    """Corners of an r x r^2 rectangle tangent to the unit circle at angle phi (inner long edge r on
    the tangent at p = (cos phi, sin phi); extends radially outward by r^2)."""
    n = np.array([math.cos(phi), math.sin(phi)])   # outward radial unit normal
    t = np.array([-math.sin(phi), math.cos(phi)])  # tangential unit, along long side
    p = n                                          # touch point on the unit circle
    return np.array([
        p - (r / 2) * t,
        p + (r / 2) * t,
        p + (r / 2) * t + r2 * n,
        p - (r / 2) * t + r2 * n,
    ])


def phys_tube(phi: float, r: float, r2: float) -> np.ndarray:
    """Corners of the dual (1/r) x (1/r^2) tube through the origin (long axis 1/r^2 radial, width
    1/r tangential)."""
    n = np.array([math.cos(phi), math.sin(phi)])
    t = np.array([-math.sin(phi), math.cos(phi)])
    half_len = 0.5 / r2
    half_wid = 0.5 / r
    return np.array([
        -half_len * n - half_wid * t,
        +half_len * n - half_wid * t,
        +half_len * n + half_wid * t,
        -half_len * n + half_wid * t,
    ])


def dist_center_to_inner_edge(rect: np.ndarray) -> float:
    """Perpendicular distance from the origin to the (inner) long edge line of a freq rectangle."""
    a, b = rect[0], rect[1]           # inner long edge endpoints
    d = b - a
    d = d / np.linalg.norm(d)
    normal = np.array([-d[1], d[0]])  # unit normal to the edge
    return abs(float(np.dot(a, normal)))


def main():
    n_rect = 12
    r = 2.0 * math.sin(math.pi / n_rect)  # chord so the slabs tile the circle
    r2 = r * r
    phis = np.linspace(0.0, 2 * math.pi, n_rect, endpoint=False)

    freq_rects = [freq_rectangle(p, r, r2) for p in phis]
    dists = [dist_center_to_inner_edge(R) for R in freq_rects]
    max_tangent_err = max(abs(d - 1.0) for d in dists)

    # dual tubes: opposite angles give the same origin-centred tube -> 6 distinct orientations
    phys_phis = np.linspace(0.0, math.pi, n_rect // 2, endpoint=False)
    phys_tubes = [phys_tube(p, r, r2) for p in phys_phis]

    math_check(
        "Fefferman ball multiplier (freq x phys duality)",
        [
            ("N rectangles", f"{n_rect}"),
            ("r  (long side, = 2 sin(pi/N))", f"{r:.4f}"),
            ("r^2  (short side)", f"{r2:.4f}"),
            ("freq aspect  r : r^2", f"{r:.4f} : {r2:.4f}  = {r / r2:.4f} : 1  (want 1/r = {1 / r:.4f})"),
            ("phys tube  length 1/r^2", f"{1 / r2:.4f}"),
            ("phys tube  width  1/r", f"{1 / r:.4f}"),
            ("phys aspect  1/r^2 : 1/r", f"{1 / r2:.4f} : {1 / r:.4f}  = {(1 / r2) / (1 / r):.4f} : 1  (want 1/r = {1 / r:.4f})"),
            ("duality  r * (1/r)", f"{r * (1 / r):.6f}  (want 1)"),
            ("duality  r^2 * (1/r^2)", f"{r2 * (1 / r2):.6f}  (want 1)"),
            ("tangency: dist(centre, inner edge)", f"min {min(dists):.6f}  max {max(dists):.6f}  (want 1)"),
            ("max tangency error", f"{max_tangent_err:.2e}  (< 1e-9 ok)"),
        ],
    )

    fig, ax = new_axes(2, figsize=(12, 6))

    # frequency side: unit circle + tangent r x r^2 slabs
    disc = circle(1.0, 400)
    ax[0].fill(disc[:, 0], disc[:, 1], color="#f4e37a", alpha=0.55, zorder=0)  # B(0,1), yellow
    ax[0].plot(np.append(disc[:, 0], disc[0, 0]), np.append(disc[:, 1], disc[0, 1]),
               color=COLORS["accent"], lw=2.2, zorder=3)
    for rect in freq_rects:
        poly_xy = np.vstack([rect, rect[0]])
        ax[0].fill(poly_xy[:, 0], poly_xy[:, 1], color="#c8d0f0", alpha=0.7, zorder=1)
        ax[0].plot(poly_xy[:, 0], poly_xy[:, 1], color=COLORS["outer"], lw=1.1, zorder=2)
    # labels: r along the top slab inner edge, r^2 as its thickness, theta at the right, B(0,1)
    top = freq_rects[3]  # a slab near the top (phi = 90 deg for N=12)
    a, b = top[0], top[1]
    mid = (a + b) / 2
    ax[0].annotate("", xy=tuple(b), xytext=tuple(a),
                   arrowprops=dict(arrowstyle="<->", color=COLORS["guide"], lw=1.0))
    ax[0].text(mid[0], mid[1] + 0.12, r"$r$", ha="center", va="bottom", fontsize=14)
    c, d = top[0], top[3]  # right short edge (thickness r^2), so its label clears the r label
    ax[0].annotate("", xy=tuple(d), xytext=tuple(c),
                   arrowprops=dict(arrowstyle="<->", color=COLORS["guide"], lw=1.0))
    ax[0].text(d[0] + 0.14, (c[1] + d[1]) / 2, r"$r^2$", ha="left", va="center", fontsize=13)
    ax[0].text(1.42, 0.30, r"$\theta$", fontsize=15)
    ax[0].text(0.0, 0.0, r"$B(0,1)$", ha="center", va="center", fontsize=15)
    ax[0].set_title("Frequency side: $r \\times r^2$ slabs tangent to $|\\xi|=1$")
    ax[0].set_xlim(-1.55, 1.75)
    ax[0].set_ylim(-1.55, 1.55)

    # physical side: dual 1/r x 1/r^2 tubes piling up at the origin
    for tube in phys_tubes:
        poly_xy = np.vstack([tube, tube[0]])
        ax[1].fill(poly_xy[:, 0], poly_xy[:, 1], color=COLORS["outer"], alpha=0.22, zorder=1)
        ax[1].plot(poly_xy[:, 0], poly_xy[:, 1], color=COLORS["outer"], lw=1.1, zorder=2)
    lim = 0.5 / r2 + 0.35
    ax[1].text(1.62 * (0.5 / r), 0.0, r"$T$", fontsize=15, va="center")
    # 1/r width bracket on the vertical-looking tube (phi = pi/2 tube: long along y)
    vtube = phys_tube(math.pi / 2, r, r2)
    bl, br = vtube[3], vtube[0]  # a short (width 1/r) edge at the bottom
    ax[1].annotate("", xy=tuple(br), xytext=tuple(bl),
                   arrowprops=dict(arrowstyle="<->", color=COLORS["guide"], lw=1.0))
    ax[1].text((bl[0] + br[0]) / 2, bl[1] - 0.18, r"$1/r$", ha="center", va="top", fontsize=13)
    ax[1].annotate("", xy=(lim - 0.12, 0.5 / r2), xytext=(lim - 0.12, -0.5 / r2),
                   arrowprops=dict(arrowstyle="<->", color=COLORS["guide"], lw=1.0))
    ax[1].text(lim - 0.02, 0.0, r"$1/r^2$", ha="left", va="center", fontsize=13)
    ax[1].set_title("Physical side: dual $1/r \\times 1/r^2$ tubes pile up at $0$")
    ax[1].set_xlim(-lim - 0.1, lim + 0.5)
    ax[1].set_ylim(-lim - 0.1, lim + 0.1)

    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
