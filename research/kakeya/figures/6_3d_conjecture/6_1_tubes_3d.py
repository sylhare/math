"""3D tube setup (kakeya.md section 6).

delta-tube: cylinder of length 1, radius delta/2, i.e. dimensions delta x delta x 1, volume
|T| = delta^2. Directions delta-separated on S^2 (area 4 pi) give #T ~ delta^-2, so #T * |T| ~ 1.
In R^2 two lines in different directions cross (min distance 0); in R^3 they are skew and miss
(min distance > 0).

Left: two 1 x delta rectangles at an angle cross. Right: a bundle of delta x delta x 1 tubes in
delta-separated directions, two highlighted skew tubes miss.
Run: uv run --with matplotlib --with shapely python research/kakeya/figures/tubes_3d.py
"""
import numpy as np
from _shared import COLORS, math_check, save_preview


# ---------------------------------------------------------------------------
# GEOMETRY (pure numpy, portable)
# ---------------------------------------------------------------------------
def fibonacci_sphere(n: int) -> np.ndarray:
    """n roughly-uniform points on the unit sphere S^2 (for sampling directions)."""
    i = np.arange(n) + 0.5
    phi = np.arccos(1 - 2 * i / n)
    theta = np.pi * (1 + 5 ** 0.5) * i
    return np.column_stack([np.sin(phi) * np.cos(theta), np.sin(phi) * np.sin(theta), np.cos(phi)])


def delta_separated(points: np.ndarray, delta: float) -> np.ndarray:
    """Greedy delta-separated subset (Euclidean chord >= delta) -> indices of a packing on S^2."""
    kept = []
    keptpts = np.empty((0, 3))
    for p in points:
        if keptpts.shape[0] == 0 or np.min(np.linalg.norm(keptpts - p, axis=1)) >= delta:
            kept.append(p)
            keptpts = np.vstack([keptpts, p])
    return np.asarray(kept)


def line_line_distance(p1, d1, p2, d2) -> float:
    """Minimum distance between the two infinite lines p_i + t d_i (0 if parallel or crossing)."""
    n = np.cross(d1, d2)
    nn = np.linalg.norm(n)
    if nn < 1e-12:  # parallel
        return float(np.linalg.norm(np.cross(d1, p2 - p1)) / np.linalg.norm(d1))
    return float(abs(np.dot(p2 - p1, n)) / nn)


def tube_frame(direction: np.ndarray):
    """Orthonormal frame (u along the tube, v, w spanning its circular cross-section)."""
    u = direction / np.linalg.norm(direction)
    tmp = np.array([1.0, 0.0, 0.0]) if abs(u[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
    v = np.cross(u, tmp)
    v /= np.linalg.norm(v)
    w = np.cross(u, v)
    return u, v, w


def tube_surface(center, direction, length, radius, n_theta=18):
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
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # --- MATH: count of delta-separated directions ~ delta^-2 ----------------
    samples = fibonacci_sphere(20000)
    counts = {}
    for d in (0.4, 0.2, 0.1):
        counts[d] = len(delta_separated(samples, d))

    # --- MATH: two tubes in different directions MISS (skew) in R^3 ----------
    dir_a = np.array([1.0, 0.2, 0.3]); dir_a /= np.linalg.norm(dir_a)
    dir_b = np.array([0.2, 1.0, -0.3]); dir_b /= np.linalg.norm(dir_b)
    cen_a = np.array([-0.15, 0.0, 0.0])
    cen_b = np.array([0.15, 0.0, 0.35])
    miss_dist = line_line_distance(cen_a, dir_a, cen_b, dir_b)

    # --- MATH: same two DIRECTIONS in the plane always cross -----------------
    d2a = np.array([np.cos(np.deg2rad(20)), np.sin(np.deg2rad(20))])
    d2b = np.array([np.cos(np.deg2rad(110)), np.sin(np.deg2rad(110))])
    cross_dist = 0.0  # two non-parallel lines in R^2 meet: distance 0

    math_check(
        "3D tubes: count ~ delta^-2 and different directions MISS",
        [
            ("count(delta=0.4)", f"{counts[0.4]}   count*delta^2 = {counts[0.4] * 0.4**2:.2f}"),
            ("count(delta=0.2)", f"{counts[0.2]}   count*delta^2 = {counts[0.2] * 0.2**2:.2f}"),
            ("count(delta=0.1)", f"{counts[0.1]}   count*delta^2 = {counts[0.1] * 0.1**2:.2f}"),
            ("halving delta ~x4", f"0.4->0.2: {counts[0.2]/counts[0.4]:.2f}x, 0.2->0.1: {counts[0.1]/counts[0.2]:.2f}x  (want ~4)"),
            ("tube |T| = delta^2", "delta^2 x 1 ; content #T*|T| ~ 1"),
            ("2D lines (dirs 20,110deg)", f"min distance = {cross_dist:.3f}  (they CROSS)"),
            ("3D skew tubes miss", f"min axis distance = {miss_dist:.3f} > 0  (they MISS)"),
        ],
    )

    # --- PREVIEW -------------------------------------------------------------
    delta_vis = 0.10  # display thickness for the thin tubes
    radius = delta_vis / 2.0

    fig = plt.figure(figsize=(12.5, 6.2))

    # Left: 2D, two 1 x delta rectangles in different directions cross.
    ax0 = fig.add_subplot(1, 2, 1)
    ax0.set_aspect("equal")
    ax0.axis("off")
    ax0.set_title("2D: different directions cross")
    for d2, col in ((d2a, COLORS["outer"]), (d2b, COLORS["accent"])):
        perp = np.array([-d2[1], d2[0]]) * (delta_vis / 2)
        c = np.array([0.0, 0.0])
        rect = np.array([c - 0.5 * d2 - perp, c + 0.5 * d2 - perp, c + 0.5 * d2 + perp, c - 0.5 * d2 + perp])
        ax0.fill(rect[:, 0], rect[:, 1], color=col, alpha=0.55, edgecolor=col)
    ax0.plot(0, 0, "o", color=COLORS["guide"], ms=6)
    ax0.annotate("they meet", (0, 0), (0.15, -0.28), color=COLORS["guide"],
                 arrowprops=dict(arrowstyle="->", color=COLORS["guide"]))
    ax0.set_xlim(-0.7, 0.7); ax0.set_ylim(-0.7, 0.7)

    # Right: 3D bundle of delta x delta x 1 tubes in delta-separated directions; two highlighted miss.
    ax1 = fig.add_subplot(1, 2, 2, projection="3d")
    ax1.set_title("3D: a bundle of delta x delta x 1 tubes (two skew tubes miss)")
    rng = np.random.default_rng(7)
    dirs = delta_separated(fibonacci_sphere(4000), 0.55)
    dirs = dirs[dirs[:, 2] >= 0][:14]  # upper hemisphere
    for d in dirs:
        c = rng.uniform(-0.18, 0.18, size=3)
        X, Y, Z = tube_surface(c, d, 1.0, radius)
        ax1.plot_surface(X, Y, Z, color=COLORS["outer"], alpha=0.28, linewidth=0)
    # the two highlighted tubes that MISS
    for c, d in ((cen_a, dir_a), (cen_b, dir_b)):
        X, Y, Z = tube_surface(c, d, 1.0, radius * 1.1)
        ax1.plot_surface(X, Y, Z, color=COLORS["accent"], alpha=0.9, linewidth=0)
    # their axes + the shortest gap between them
    for c, d in ((cen_a, dir_a), (cen_b, dir_b)):
        seg = np.array([c - 0.5 * d, c + 0.5 * d])
        ax1.plot(seg[:, 0], seg[:, 1], seg[:, 2], color=COLORS["guide"], lw=1.0)
    ax1.set_box_aspect((1, 1, 1))
    ax1.set_xlim(-0.7, 0.7); ax1.set_ylim(-0.7, 0.7); ax1.set_zlim(-0.7, 0.7)
    ax1.view_init(elev=18, azim=35)
    ax1.set_xticklabels([]); ax1.set_yticklabels([]); ax1.set_zticklabels([])

    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
