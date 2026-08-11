"""r -> 0 limit of Fefferman's ball-multiplier geometry (kakeya.md 5b).

As r = 2 sin(pi/N) shrinks (N slabs grows):
  (a) FREQUENCY: N slabs of size r x r^2 tangent to the unit circle (long side r along the tangent,
      thickness r^2 radial), thinner as r -> 0.
  (b) PHYSICAL: dual 1/r x 1/r^2 tubes through the origin, drawn normalised to unit length (width r).

Each slab's inner edge stays at distance 1 from the centre; aspects r:r^2 and 1/r^2:1/r equal 1/r.

Run: uv run --with matplotlib --with shapely python research/kakeya/figures/fefferman_shrink_anim.py
"""
import math

import numpy as np
from _shared import COLORS, circle, math_check, save_gif
from matplotlib.animation import FuncAnimation

N_MIN, N_MAX = 8, 60  # slab-count range
HOLD = 10  # frames held at the finest scale


def freq_rectangle(phi: float, r: float, r2: float) -> np.ndarray:
    """Corners of an r x r^2 rectangle tangent to the unit circle at angle phi (inner long edge on
    the tangent line, distance 1 from the centre; extends radially outward by r^2)."""
    n = np.array([math.cos(phi), math.sin(phi)])   # outward radial normal
    t = np.array([-math.sin(phi), math.cos(phi)])  # tangential (along long side)
    p = n
    return np.array([p - (r / 2) * t, p + (r / 2) * t,
                     p + (r / 2) * t + r2 * n, p - (r / 2) * t + r2 * n])


def phys_tube(phi: float, r: float, r2: float) -> np.ndarray:
    """Corners of the dual (1/r) x (1/r^2) tube through the origin (long axis 1/r^2 radial, width
    1/r tangential)."""
    n = np.array([math.cos(phi), math.sin(phi)])
    t = np.array([-math.sin(phi), math.cos(phi)])
    half_len, half_wid = 0.5 / r2, 0.5 / r
    return np.array([-half_len * n - half_wid * t, half_len * n - half_wid * t,
                     half_len * n + half_wid * t, -half_len * n + half_wid * t])


def dist_center_to_inner_edge(rect: np.ndarray) -> float:
    a, b = rect[0], rect[1]
    d = b - a
    d = d / np.linalg.norm(d)
    normal = np.array([-d[1], d[0]])
    return abs(float(np.dot(a, normal)))


def n_schedule() -> np.ndarray:
    up = np.arange(N_MIN, N_MAX + 1)
    return np.concatenate([up, np.full(HOLD, N_MAX)]).astype(int)


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ns = n_schedule()

    # --- validation across every frame: tangency = 1, both aspects = 1/r ----------------------
    max_tangent_err = 0.0
    max_aspect_err = 0.0
    for n_rect in ns:
        r = 2.0 * math.sin(math.pi / n_rect)  # chord tiling the circle
        r2 = r * r
        phis = np.linspace(0.0, 2 * math.pi, int(n_rect), endpoint=False)
        for phi in phis:
            d = dist_center_to_inner_edge(freq_rectangle(phi, r, r2))
            max_tangent_err = max(max_tangent_err, abs(d - 1.0))
        freq_aspect = r / r2          # r : r^2  ->  1/r
        phys_aspect = (1 / r2) / (1 / r)  # 1/r^2 : 1/r  ->  1/r
        max_aspect_err = max(max_aspect_err, abs(freq_aspect - 1 / r), abs(phys_aspect - 1 / r))

    r_min = 2.0 * math.sin(math.pi / N_MAX)
    math_check(
        "Fefferman shrink r -> 0  (slabs tangent, dual tubes pile up)",
        [
            ("frames", f"{len(ns)}"),
            ("N slabs range", f"{N_MIN} -> {N_MAX}"),
            ("r = 2 sin(pi/N) range", f"{2 * math.sin(math.pi / N_MIN):.4f} -> {r_min:.4f}  (-> 0)"),
            ("tangency: dist(centre, inner edge)=1", f"max err {max_tangent_err:.2e}  (< 1e-9 ok)"),
            ("freq r:r^2 and phys 1/r^2:1/r == 1/r", f"max err {max_aspect_err:.2e}  (< 1e-9 ok)"),
            ("as r->0", "more, thinner slabs; dual tubes thin + pile at 0"),
        ],
    )
    assert max_tangent_err < 1e-9 and max_aspect_err < 1e-9

    fig, ax = plt.subplots(1, 2, figsize=(11, 5.6))
    for a in ax:
        a.set_aspect("equal"); a.axis("off")

    # frequency limits from the actual largest slab (fattest at N_MIN), so nothing is clipped
    _fext = 0.0
    for _n in ns:
        _r = 2.0 * math.sin(math.pi / int(_n)); _r2 = _r * _r
        for _phi in np.linspace(0.0, 2 * math.pi, int(_n), endpoint=False):
            _fext = max(_fext, float(np.max(np.linalg.norm(freq_rectangle(_phi, _r, _r2), axis=1))))
    _flim = _fext * 1.08

    disc = circle(1.0, 400)
    ring = np.vstack([disc, disc[:1]])
    ax[0].set_xlim(-_flim, _flim); ax[0].set_ylim(-_flim, _flim)
    ax[0].set_title(r"Frequency: $r\times r^2$ slabs tangent to $|\xi|=1$")
    ax[1].set_xlim(-0.62, 0.62); ax[1].set_ylim(-0.62, 0.62)
    ax[1].set_title(r"Physical: dual $1/r\times 1/r^2$ tubes pile up at $0$")
    ax[0].fill(disc[:, 0], disc[:, 1], color="#f4e37a", alpha=0.55, zorder=0)
    ax[0].plot(ring[:, 0], ring[:, 1], color=COLORS["accent"], lw=2.0, zorder=3)

    artists = []

    def update(i):
        for art in artists:
            art.remove()
        artists.clear()
        n_rect = int(ns[i])
        r = 2.0 * math.sin(math.pi / n_rect)
        r2 = r * r
        # frequency slabs (true scale on the unit circle)
        for phi in np.linspace(0.0, 2 * math.pi, n_rect, endpoint=False):
            rect = np.vstack([freq_rectangle(phi, r, r2), freq_rectangle(phi, r, r2)[0]])
            (p,) = ax[0].fill(rect[:, 0], rect[:, 1], color="#c8d0f0", alpha=0.7, zorder=1)
            (e,) = ax[0].plot(rect[:, 0], rect[:, 1], color=COLORS["outer"], lw=0.8, zorder=2)
            artists.extend([p, e])
        # physical dual tubes, normalised to unit length (multiply by r2): length 1, width r
        for phi in np.linspace(0.0, math.pi, n_rect // 2, endpoint=False):
            tube = phys_tube(phi, r, r2) * r2
            tube = np.vstack([tube, tube[0]])
            (p,) = ax[1].fill(tube[:, 0], tube[:, 1], color=COLORS["outer"], alpha=0.20, zorder=1)
            artists.append(p)
        txt = ax[0].text(0.02, 0.97, f"N = {n_rect},   r = {r:.3f}", transform=ax[0].transAxes,
                         va="top", fontsize=11, color=COLORS["outer"])
        artists.append(txt)
        return artists

    anim = FuncAnimation(fig, update, frames=len(ns), interval=90, blit=False)
    print("wrote", save_gif(anim, fps=12, dpi=95))


if __name__ == "__main__":
    main()
