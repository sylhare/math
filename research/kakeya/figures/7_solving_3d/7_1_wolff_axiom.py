"""Wolff axiom (kakeya.md section 6, Hickman Def. 5.6).

For every rectangular prism R in R^3 and a direction-separated family of delta-tubes,
    #{ T in T : T subset of R }  <=  delta^-2 |R| .
Each tube has |T| = delta^2 and tubes in R overlap boundedly, so #tubes <~ delta^-2 |R|.
Wolff's resulting R^3 dimension lower bound (1995): (n+2)/2 = (3+2)/2 = 5/2.

Two slab prisms R at the same delta: satisfying (count <= delta^-2 |R|) and forbidden (a thinner
slab with count > delta^-2 |R|).
Run: uv run --with matplotlib --with shapely python research/kakeya/figures/wolff_axiom.py
"""
import numpy as np
from _shared import COLORS, math_check, save_preview


# Geometry (pure numpy, portable)
def prism_volume(dims) -> float:
    """Volume |R| of an axis-aligned rectangular prism of side lengths (Lx, Ly, Lz)."""
    lx, ly, lz = dims
    return lx * ly * lz


def wolff_bound(delta: float, dims) -> float:
    """The Wolff cap on tube count inside R:  delta^-2 |R|."""
    return delta ** -2 * prism_volume(dims)


def slab_tubes(dims, delta, n, rng):
    """n unit tubes (center, direction) with distinct in-plane directions lying in the slab plane
    z in [-Lz/2, Lz/2]; length 1, radius delta/2."""
    lx, ly, lz = dims
    angles = np.linspace(0.0, np.pi, n, endpoint=False)  # distinct directions in [0, pi)
    tubes = []
    for a in angles:
        d = np.array([np.cos(a), np.sin(a), 0.0])
        z = rng.uniform(-(lz / 2 - delta / 2), (lz / 2 - delta / 2)) if lz > delta else 0.0
        c = np.array([rng.uniform(-0.05, 0.05), rng.uniform(-0.05, 0.05), z])
        tubes.append((c, d))
    return tubes


def tube_frame(direction: np.ndarray):
    u = direction / np.linalg.norm(direction)
    tmp = np.array([1.0, 0.0, 0.0]) if abs(u[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
    v = np.cross(u, tmp)
    v /= np.linalg.norm(v)
    w = np.cross(u, v)
    return u, v, w


def tube_surface(center, direction, length, radius, n_theta=16):
    u, v, w = tube_frame(direction)
    theta = np.linspace(0, 2 * np.pi, n_theta)
    s = np.linspace(-length / 2, length / 2, 2)
    S, T = np.meshgrid(s, theta)
    X = center[0] + S * u[0] + radius * (np.cos(T) * v[0] + np.sin(T) * w[0])
    Y = center[1] + S * u[1] + radius * (np.cos(T) * v[1] + np.sin(T) * w[1])
    Z = center[2] + S * u[2] + radius * (np.cos(T) * v[2] + np.sin(T) * w[2])
    return X, Y, Z


def prism_edges(dims):
    """12 edges (pairs of corners) of the axis-aligned box centred at the origin."""
    lx, ly, lz = (d / 2 for d in dims)
    c = np.array([[sx * lx, sy * ly, sz * lz] for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)])
    edges = []
    for i in range(8):
        for j in range(i + 1, 8):
            if np.sum(np.abs(c[i] - c[j]) > 1e-9) == 1:  # differ in exactly one coordinate
                edges.append((c[i], c[j]))
    return edges


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    delta = 0.1
    n_wolff = (3 + 2) / 2  # (n+2)/2 in R^3

    # Satisfying slab: count <= delta^-2 |R|
    dims_ok = (1.2, 1.2, 0.30)
    bound_ok = wolff_bound(delta, dims_ok)     # 100 * 0.432 = 43.2
    n_ok = 18

    # Forbidden slab: count > delta^-2 |R|
    dims_bad = (1.2, 1.2, 0.12)
    bound_bad = wolff_bound(delta, dims_bad)   # 100 * 0.1728 = 17.28
    n_bad = 26

    math_check(
        "Wolff axiom  #{T in R} <= delta^-2 |R|",
        [
            ("delta", f"{delta}   delta^-2 = {delta**-2:.0f}"),
            ("satisfying slab R", f"dims {dims_ok}, |R| = {prism_volume(dims_ok):.3f}"),
            ("  bound delta^-2|R|", f"{bound_ok:.1f}   tube count = {n_ok}   -> {n_ok} <= {bound_ok:.1f}  OK"),
            ("forbidden slab R", f"dims {dims_bad}, |R| = {prism_volume(dims_bad):.3f}"),
            ("  bound delta^-2|R|", f"{bound_bad:.1f}   tube count = {n_bad}   -> {n_bad} > {bound_bad:.1f}  VIOLATES"),
            ("Wolff R^3 bound (n+2)/2", f"{n_wolff}  (n=3)  -> dim >= 5/2 (Wolff 1995)"),
        ],
    )

    # Preview
    radius = delta / 2.0
    fig = plt.figure(figsize=(12.5, 6.2))

    for idx, (dims, n, _bound, ok, title) in enumerate(
        [
            (dims_ok, n_ok, bound_ok, True, f"satisfying:  {n_ok} tubes <= delta^-2|R| = {bound_ok:.0f}"),
            (dims_bad, n_bad, bound_bad, False, f"forbidden:  {n_bad} tubes > delta^-2|R| = {bound_bad:.0f}"),
        ]
    ):
        ax = fig.add_subplot(1, 2, idx + 1, projection="3d")
        ax.set_title(title, color=(COLORS["outer"] if ok else COLORS["accent"]))
        for a, b in prism_edges(dims):
            ax.plot(*zip(a, b, strict=False), color=COLORS["outer"], lw=1.1, alpha=0.9)
        rng = np.random.default_rng(3 if ok else 4)
        for c, d in slab_tubes(dims, delta, n, rng):
            X, Y, Z = tube_surface(c, d, 1.0, radius)
            ax.plot_surface(X, Y, Z, color=COLORS["accent"], alpha=0.55, linewidth=0)
        ax.set_box_aspect((1.2, 1.2, 0.7))
        ax.set_xlim(-0.75, 0.75); ax.set_ylim(-0.75, 0.75); ax.set_zlim(-0.4, 0.4)
        ax.view_init(elev=22, azim=-60)
        ax.set_xticklabels([]); ax.set_yticklabels([]); ax.set_zticklabels([])

    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
