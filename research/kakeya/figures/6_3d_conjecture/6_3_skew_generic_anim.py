"""Animation: generic lines in R^3 are skew (they MISS), while in R^2 they always cross.

The 2D Kakeya engine leans on "two segments in different directions meet, so the union has to
spread out". That crossing is vacuous in space: a fixed grey PROBE line and a coloured line whose
direction sweeps a great circle over S^2 keep a positive gap

    dist(l1, l2) = |(p2 - p1) . (d1 x d2)| / |d1 x d2|,

which only pinches to 0 at the isolated (codim-1) directions where (p2 - p1) . (d1 x d2) = 0.
A cloud of random delta-tube pairs is overwhelmingly skew, so crossings cannot carry the argument
in R^3 and one needs the Wolff axiom instead.

Left  (3D turntable): fixed probe tube + swept coloured tube, live dist readout, shortest-gap
                      segment, red flash at the isolated crossing directions.
Inset A (2D): two lines through the origin at 20 and 110 deg, always meeting (distance 0).
Inset B (Monte-Carlo): 200 random axis pairs, red = axes within delta, blue = skew miss.

Run: PYTHONPATH=research/kakeya/figures uv run --with matplotlib --with shapely --with pillow \
     python research/kakeya/figures/6_3d_conjecture/6_3_skew_generic_anim.py
"""
import math

import numpy as np
from _shared import COLORS, math_check, save_gif
from matplotlib.animation import FuncAnimation

N_SWEEP = 72        # coloured-tube directions along the great circle
HOLD = 8            # frames held at the start
END_HOLD = 8        # frames held at the end
DELTA_MC = 0.10     # Monte-Carlo tube radius scale: axes within DELTA_MC count as a crossing
N_MC = 200          # random axis pairs
CUBE = 2.0          # random centers uniform in [-CUBE/2, CUBE/2]^3
FLASH = 0.03        # dist below this flashes the swept tube red (near a crossing)


# ---------------------------------------------------------------------------
# GEOMETRY (pure numpy, portable; line_line_distance reused from 6_1)
# ---------------------------------------------------------------------------
def fibonacci_sphere(n: int) -> np.ndarray:
    """n roughly-uniform points on the unit sphere S^2 (for sampling directions)."""
    i = np.arange(n) + 0.5
    phi = np.arccos(1 - 2 * i / n)
    theta = np.pi * (1 + 5 ** 0.5) * i
    return np.column_stack([np.sin(phi) * np.cos(theta), np.sin(phi) * np.sin(theta), np.cos(phi)])


def line_line_distance(p1, d1, p2, d2) -> float:
    """Minimum distance between the infinite lines p_i + t d_i (0 if parallel or crossing)."""
    n = np.cross(d1, d2)
    nn = np.linalg.norm(n)
    if nn < 1e-12:  # parallel
        return float(np.linalg.norm(np.cross(d1, p2 - p1)) / np.linalg.norm(d1))
    return float(abs(np.dot(p2 - p1, n)) / nn)


def line_closest_points(p1, d1, p2, d2):
    """Foot points of the shortest segment between the two infinite lines (for drawing the gap)."""
    r = p1 - p2
    a, b, c = float(d1 @ d1), float(d1 @ d2), float(d2 @ d2)
    d, e = float(d1 @ r), float(d2 @ r)
    denom = a * c - b * b
    if abs(denom) < 1e-12:  # parallel
        t, s = 0.0, e / c
    else:
        t, s = (b * e - c * d) / denom, (a * e - b * d) / denom
    return p1 + t * d1, p2 + s * d2


def tube_frame(direction: np.ndarray):
    """Orthonormal frame (u along the tube, v, w spanning its circular cross-section)."""
    u = direction / np.linalg.norm(direction)
    tmp = np.array([1.0, 0.0, 0.0]) if abs(u[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
    v = np.cross(u, tmp)
    v /= np.linalg.norm(v)
    w = np.cross(u, v)
    return u, v, w


def tube_surface(center, direction, length, radius, n_theta=16):
    """Cylinder surface (X, Y, Z) for a length x (2 radius) tube centred at `center`."""
    u, v, w = tube_frame(direction)
    theta = np.linspace(0, 2 * np.pi, n_theta)
    s = np.linspace(-length / 2, length / 2, 2)
    S, T = np.meshgrid(s, theta)
    X = center[0] + S * u[0] + radius * (np.cos(T) * v[0] + np.sin(T) * w[0])
    Y = center[1] + S * u[1] + radius * (np.cos(T) * v[1] + np.sin(T) * w[1])
    Z = center[2] + S * u[2] + radius * (np.cos(T) * v[2] + np.sin(T) * w[2])
    return X, Y, Z


def main():
    # --- fixed skew reference pair (same PROBE + tube as 6_1) -----------------
    dir_a = np.array([1.0, 0.2, 0.3]); dir_a /= np.linalg.norm(dir_a)   # PROBE direction
    dir_b = np.array([0.2, 1.0, -0.3]); dir_b /= np.linalg.norm(dir_b)  # sweep start direction
    cen_a = np.array([-0.15, 0.0, 0.0])   # PROBE center
    cen_b = np.array([0.15, 0.0, 0.35])   # swept-tube center (fixed offset)
    miss_dist = line_line_distance(cen_a, dir_a, cen_b, dir_b)

    # --- sweep d2 along a great circle e1 = dir_b, e2 orthonormal ------------
    w = cen_b - cen_a
    k = np.cross(w, dir_a)                 # crossing normal: dist = 0 iff d2 . k = 0
    e1 = dir_b
    e2 = np.cross(e1, dir_a); e2 /= np.linalg.norm(e2)
    # isolated crossing angles on the circle: (e1.k) cos phi + (e2.k) sin phi = 0
    alpha = math.atan2(float(e1 @ k), float(e2 @ k))
    phi_cross = sorted({(-alpha) % (2 * math.pi), (-alpha + math.pi) % (2 * math.pi)})

    base = np.linspace(0.0, 2 * math.pi, N_SWEEP, endpoint=False)
    phis = np.sort(np.concatenate([base, phi_cross]))   # land exactly on the crossings too

    def d2_of(phi):
        v = math.cos(phi) * e1 + math.sin(phi) * e2
        return v / np.linalg.norm(v)

    dirs2 = [d2_of(p) for p in phis]
    dists = np.array([line_line_distance(cen_a, dir_a, cen_b, d2) for d2 in dirs2])

    frac_open = float((dists > 1e-2).mean())          # away from crossings the gap stays open
    dip = float(dists.min())                          # pinches to ~0 at a crossing

    # --- Monte-Carlo: random pairs are overwhelmingly skew -------------------
    def mc_fraction(delta, seed=0):
        rng = np.random.default_rng(seed)

        def jdirs():
            d = fibonacci_sphere(N_MC) + rng.normal(0.0, 0.20, (N_MC, 3))
            return d / np.linalg.norm(d, axis=1, keepdims=True)

        d1s, d2s = jdirs(), jdirs()
        d2s = d2s[rng.permutation(N_MC)]
        c1s = rng.uniform(-CUBE / 2, CUBE / 2, (N_MC, 3))
        c2s = rng.uniform(-CUBE / 2, CUBE / 2, (N_MC, 3))
        ds = np.array([line_line_distance(c1s[i], d1s[i], c2s[i], d2s[i]) for i in range(N_MC)])
        return ds, float((ds < delta).mean())

    mc_ds, frac_cross = mc_fraction(DELTA_MC)
    _, frac_cross_half = mc_fraction(DELTA_MC / 2)
    miss_frac = 1.0 - frac_cross

    # --- 2D control: two non-parallel lines through the origin always meet ----
    d2a = np.array([math.cos(math.radians(20)), math.sin(math.radians(20))])
    d2b = np.array([math.cos(math.radians(110)), math.sin(math.radians(110))])
    cross_dist_2d = line_line_distance(np.array([0.0, 0.0, 0.0]),
                                       np.array([d2a[0], d2a[1], 0.0]),
                                       np.array([0.0, 0.0, 0.0]),
                                       np.array([d2b[0], d2b[1], 0.0]))

    # --- MATH CHECK: assert the drawn relations ------------------------------
    assert miss_dist > 1e-2, "the fixed 6_1 pair must MISS (positive axis distance)"
    assert frac_open > 0.90, "the 3D gap must stay open away from the isolated crossings"
    assert dip < 1e-2, "the gap must pinch to ~0 at the codim-1 crossing directions"
    assert cross_dist_2d < 1e-12, "two non-parallel lines in R^2 must meet (distance 0)"
    assert 0.80 < miss_frac < 0.98, "random pairs in R^3 must be overwhelmingly skew"
    assert frac_cross_half < frac_cross, "crossing fraction must scale DOWN as delta shrinks"

    math_check(
        "generic lines in R^3 are skew (miss); in R^2 they cross",
        [
            ("R^3 fixed pair (from 6_1)", f"min axis dist = {miss_dist:.3f} > 0   (they MISS)"),
            ("dist(l1,l2) formula", "|(p2-p1).(d1 x d2)| / |d1 x d2|"),
            ("sweep, gap stays open", f"{frac_open*100:.1f}% of {len(phis)} dirs have dist > 1e-2"),
            ("sweep, dip at crossing", f"min dist = {dip:.2e}  (isolated codim-1 events)"),
            ("crossing dirs on circle", f"phi = {phi_cross[0]:.3f}, {phi_cross[1]:.3f} rad (2 of them)"),
            ("R^2 two lines (20,110 deg)", f"min dist = {cross_dist_2d:.3e}  (they CROSS)"),
            (f"Monte-Carlo miss @ delta={DELTA_MC}", f"{miss_frac*100:.1f}% skew  ({int(frac_cross*N_MC)}/{N_MC} cross)"),
            ("crossing frac vs delta", f"delta={DELTA_MC}: {frac_cross:.3f}  ->  "
                                       f"delta={DELTA_MC/2}: {frac_cross_half:.3f}  (~O(delta))"),
            ("why 3D is hard", "no crossing engine; needs the Wolff axiom instead"),
        ],
    )

    # ---- figure -------------------------------------------------------------
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(13.0, 7.2))
    gs = fig.add_gridspec(2, 2, width_ratios=[1.75, 1.0], hspace=0.28, wspace=0.12)
    ax_main = fig.add_subplot(gs[:, 0], projection="3d")
    ax_a = fig.add_subplot(gs[0, 1])
    ax_b = fig.add_subplot(gs[1, 1])
    fig.suptitle("R^3: generic lines MISS (dist > 0);   R^2: always cross",
                 fontsize=13, y=0.97)

    radius = 0.05  # display tube radius (delta/2)

    # --- INSET A (static): two 2D lines through the origin cross at distance 0
    ax_a.set_aspect("equal"); ax_a.axis("off")
    for d2, col in ((d2a, COLORS["outer"]), (d2b, COLORS["accent"])):
        seg = np.array([-0.6 * d2, 0.6 * d2])
        ax_a.plot(seg[:, 0], seg[:, 1], color=col, lw=2.4)
    ax_a.plot(0, 0, "o", color=COLORS["guide"], ms=7, zorder=5)
    ax_a.annotate("meet: dist = 0.000", (0, 0), (-0.55, -0.5), color=COLORS["guide"],
                  fontsize=9, arrowprops=dict(arrowstyle="->", color=COLORS["guide"]))
    ax_a.set_xlim(-0.7, 0.7); ax_a.set_ylim(-0.7, 0.7)
    ax_a.set_title("R^2: different directions cross", fontsize=10)

    # --- INSET B (static): Monte-Carlo cloud of random axis pairs
    order = np.argsort(mc_ds)
    xs = np.arange(N_MC)
    cols = np.where(mc_ds[order] < DELTA_MC, COLORS["accent"], COLORS["outer"])
    ax_b.scatter(xs, mc_ds[order], s=12, c=cols, alpha=0.85, linewidths=0)
    ax_b.axhline(DELTA_MC, color=COLORS["guide"], lw=1.0, ls="--")
    ax_b.text(2, DELTA_MC * 1.15, f"delta = {DELTA_MC}", color=COLORS["guide"], fontsize=8)
    ax_b.set_ylim(0, max(0.5, float(np.quantile(mc_ds, 0.97))))
    ax_b.set_xlim(0, N_MC)
    ax_b.set_xlabel("random pair (sorted)", fontsize=8)
    ax_b.set_ylabel("axis distance", fontsize=8)
    ax_b.tick_params(labelsize=7)
    ax_b.grid(True, color=COLORS["muted"], alpha=0.25, lw=0.5)
    ax_b.set_title(f"200 random pairs: {miss_frac*100:.0f}% skew (miss)", fontsize=10)

    # probe (grey) axis is fixed
    probe_seg = np.array([cen_a - 0.5 * dir_a, cen_a + 0.5 * dir_a])
    tip_trail = np.array([0.62 * d for d in dirs2])  # swept-direction tips over S^2

    frames = [0] * HOLD + list(range(len(phis))) + [len(phis) - 1] * END_HOLD

    def update(fi):
        k_i = frames[fi]
        d2 = dirs2[k_i]
        dist = dists[k_i]
        crossing = dist < FLASH
        col = COLORS["accent"] if crossing else COLORS["outer"]

        ax_main.cla()
        ax_main.set_box_aspect((1, 1, 1))
        ax_main.set_xlim(-0.7, 0.7); ax_main.set_ylim(-0.7, 0.7); ax_main.set_zlim(-0.7, 0.7)
        ax_main.set_xticklabels([]); ax_main.set_yticklabels([]); ax_main.set_zticklabels([])
        azim = 30 + 0.35 * fi   # slow azimuth drift
        ax_main.view_init(elev=18, azim=azim)

        # faint trail of swept directions over the sphere
        ax_main.plot(tip_trail[:, 0], tip_trail[:, 1], tip_trail[:, 2],
                     color=COLORS["muted"], lw=0.7, alpha=0.5)

        # fixed grey PROBE tube + axis
        Xp, Yp, Zp = tube_surface(cen_a, dir_a, 1.0, radius)
        ax_main.plot_surface(Xp, Yp, Zp, color=COLORS["guide"], alpha=0.30, linewidth=0)
        ax_main.plot(probe_seg[:, 0], probe_seg[:, 1], probe_seg[:, 2],
                     color=COLORS["guide"], lw=1.4)

        # swept coloured tube + axis
        Xs, Ys, Zs = tube_surface(cen_b, d2, 1.0, radius * 1.1)
        ax_main.plot_surface(Xs, Ys, Zs, color=col, alpha=0.85, linewidth=0)
        swept_seg = np.array([cen_b - 0.5 * d2, cen_b + 0.5 * d2])
        ax_main.plot(swept_seg[:, 0], swept_seg[:, 1], swept_seg[:, 2], color=col, lw=1.4)

        # shortest-gap segment between the two axes
        f1, f2 = line_closest_points(cen_a, dir_a, cen_b, d2)
        ax_main.plot([f1[0], f2[0]], [f1[1], f2[1]], [f1[2], f2[2]],
                     color=COLORS["accent"] if crossing else COLORS["needle"],
                     lw=2.2, marker="o", ms=3)

        tag = "CROSS (dist -> 0)" if crossing else "skew: gap stays open"
        ax_main.set_title(f"dist(l1, l2) = {dist:.3f}\n{tag}", fontsize=11)
        return []

    anim = FuncAnimation(fig, update, frames=len(frames), interval=110, blit=False)
    print("wrote", save_gif(anim, fps=10, dpi=95))


if __name__ == "__main__":
    main()
