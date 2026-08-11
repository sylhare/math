"""Turntable of the 3D tube bundle (kakeya.md section 6).

Rotating (azimuth 0 -> 360) view of a bundle of delta x delta x 1 tubes in delta-separated
directions on S^2. Each tube has volume |T| = delta^2; #T ~ delta^-2, so #T * |T| ~ 1. Two red
skew tubes miss (min axis distance > 0), whereas two R^2 lines in different directions cross.
Only the camera moves; the geometry is built once.
Run: uv run --with matplotlib --with shapely python research/kakeya/figures/tubes_3d_turntable_anim.py
"""
import numpy as np
from _shared import COLORS, math_check, save_gif

FRAMES = 72  # turntable: azimuth step 360 / 72 = 5 degrees


# GEOMETRY (replicated locally from tubes_3d.py; do not import it)
def fibonacci_sphere(n: int) -> np.ndarray:
    """n roughly-uniform points on the unit sphere S^2 (for sampling directions)."""
    i = np.arange(n) + 0.5
    phi = np.arccos(1 - 2 * i / n)
    theta = np.pi * (1 + 5 ** 0.5) * i
    return np.column_stack([np.sin(phi) * np.cos(theta), np.sin(phi) * np.sin(theta), np.cos(phi)])


def delta_separated(points: np.ndarray, delta: float) -> np.ndarray:
    """Greedy delta-separated subset (chord >= delta) -> a packing on S^2."""
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
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (registers 3d projection)

    # --- MATH: count of delta-separated directions ~ delta^-2 ----------------
    samples = fibonacci_sphere(20000)
    counts = {d: len(delta_separated(samples, d)) for d in (0.4, 0.2, 0.1)}

    # --- MATH: two tubes in different directions MISS (skew) in R^3 ----------
    dir_a = np.array([1.0, 0.2, 0.3]); dir_a /= np.linalg.norm(dir_a)
    dir_b = np.array([0.2, 1.0, -0.3]); dir_b /= np.linalg.norm(dir_b)
    cen_a = np.array([-0.15, 0.0, 0.0])
    cen_b = np.array([0.15, 0.0, 0.35])
    miss_dist = line_line_distance(cen_a, dir_a, cen_b, dir_b)

    contents = [counts[d] * d ** 2 for d in (0.4, 0.2, 0.1)]
    # count ~ delta^-2  <=>  count*delta^2 is O(1), roughly constant across delta
    assert all(1.0 < ctd < 30.0 for ctd in contents), f"count*delta^2 not O(1): {contents}"
    assert max(contents) / min(contents) < 2.0, f"count*delta^2 not roughly constant: {contents}"
    assert counts[0.1] > counts[0.2] > counts[0.4], "count must grow as delta shrinks"
    assert miss_dist > 1e-3, f"red tubes must be skew (min distance > 0), got {miss_dist}"

    math_check(
        "3D tube bundle turntable: count ~ delta^-2, red pair skew (miss)",
        [
            ("count(delta=0.4)", f"{counts[0.4]}   count*delta^2 = {counts[0.4] * 0.4**2:.2f}"),
            ("count(delta=0.2)", f"{counts[0.2]}   count*delta^2 = {counts[0.2] * 0.2**2:.2f}"),
            ("count(delta=0.1)", f"{counts[0.1]}   count*delta^2 = {counts[0.1] * 0.1**2:.2f}"),
            ("count ~ delta^-2", f"0.4->0.2: {counts[0.2]/counts[0.4]:.2f}x, 0.2->0.1: {counts[0.1]/counts[0.2]:.2f}x  (want ~4)"),
            ("tube |T| = delta^2", "delta x delta x 1 ; content #T*|T| ~ 1"),
            ("red skew tubes miss", f"min axis distance = {miss_dist:.4f} > 0  (they MISS; 2D lines would cross)"),
        ],
    )

    # --- STATIC GEOMETRY (built once; only the camera animates) --------------
    delta_vis = 0.10  # display thickness for the thin tubes
    radius = delta_vis / 2.0

    fig = plt.figure(figsize=(6.4, 6.4))
    ax = fig.add_subplot(1, 1, 1, projection="3d")
    ax.set_title("3D bundle of delta x delta x 1 tubes (red pair is skew: they miss)", fontsize=10)

    rng = np.random.default_rng(7)
    dirs = delta_separated(fibonacci_sphere(4000), 0.55)
    dirs = dirs[dirs[:, 2] >= 0][:14]  # upper hemisphere
    for d in dirs:
        c = rng.uniform(-0.18, 0.18, size=3)
        X, Y, Z = tube_surface(c, d, 1.0, radius)
        ax.plot_surface(X, Y, Z, color=COLORS["outer"], alpha=0.28, linewidth=0)
    # the two highlighted skew tubes that MISS
    for c, d in ((cen_a, dir_a), (cen_b, dir_b)):
        X, Y, Z = tube_surface(c, d, 1.0, radius * 1.1)
        ax.plot_surface(X, Y, Z, color=COLORS["accent"], alpha=0.9, linewidth=0)
    # their axes (guide)
    for c, d in ((cen_a, dir_a), (cen_b, dir_b)):
        seg = np.array([c - 0.5 * d, c + 0.5 * d])
        ax.plot(seg[:, 0], seg[:, 1], seg[:, 2], color=COLORS["guide"], lw=1.0)

    ax.set_box_aspect((1, 1, 1))
    # length-1 tubes off-centred up to 0.18 reach ~0.73; widen so the wireframe box contains them
    ax.set_xlim(-0.85, 0.85); ax.set_ylim(-0.85, 0.85); ax.set_zlim(-0.85, 0.85)
    ax.set_xticklabels([]); ax.set_yticklabels([]); ax.set_zticklabels([])

    def update(i):
        ax.view_init(elev=18, azim=i * (360.0 / FRAMES))
        return ()

    anim = FuncAnimation(fig, update, frames=FRAMES, interval=60, blit=False)
    print("wrote", save_gif(anim, fps=18, dpi=90))


if __name__ == "__main__":
    main()
