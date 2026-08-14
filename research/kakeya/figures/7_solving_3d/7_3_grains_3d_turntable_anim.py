"""Turntable of Guth's grain slabs in a fat-tube box (kakeya.md section 7c).

Rotating (azimuth 0 -> 360) view of parallel grain slabs of size delta x c x c (delta << c << 1)
tiling a wireframe fat-tube box [0,1] x [0,c] x [0,c]. Grains are one tube thick (delta-thin along
the tube axis X), span the c x c cross-section, and are pairwise disjoint (share only zero-volume
faces), so every point lies in at most one grain. Only the camera moves; the geometry is built once.
Run: uv run --with matplotlib --with shapely python research/kakeya/figures/grains_3d_turntable_anim.py
"""
import numpy as np
from _shared import COLORS, math_check, save_gif

FRAMES = 72  # turntable: azimuth step 360 / 72 = 5 degrees


# Geometry (replicated locally from grains_3d.py; do not import it)
def grain_boxes(delta: float, c: float, x_starts) -> list[tuple]:
    """Axis-aligned grains delta x c x c inside a fat tube [0,1] x [0,c] x [0,c].
    Each grain is delta-thin along the tube axis X and spans the c x c cross-section."""
    return [(x0, x0 + delta, 0.0, c, 0.0, c) for x0 in x_starts]


def box_pairwise_overlap(a: tuple, b: tuple) -> float:
    """Overlap VOLUME of two axis-aligned boxes (x0,x1,y0,y1,z0,z1)."""
    ox = max(0.0, min(a[1], b[1]) - max(a[0], b[0]))
    oy = max(0.0, min(a[3], b[3]) - max(a[2], b[2]))
    oz = max(0.0, min(a[5], b[5]) - max(a[4], b[4]))
    return ox * oy * oz


def _draw_box_wire(ax, box, color, lw=1.2, alpha=1.0):
    x0, x1, y0, y1, z0, z1 = box
    xs, ys, zs = (x0, x1), (y0, y1), (z0, z1)
    corners = np.array([[x, y, z] for x in xs for y in ys for z in zs])
    edges = [(0, 1), (0, 2), (0, 4), (1, 3), (1, 5), (2, 3),
             (2, 6), (3, 7), (4, 5), (4, 6), (5, 7), (6, 7)]
    for a, b in edges:
        ax.plot(*zip(corners[a], corners[b], strict=True), color=color, lw=lw, alpha=alpha)


def _draw_box_solid(ax, box, color, alpha=0.55):
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    x0, x1, y0, y1, z0, z1 = box
    v = {
        "xlo": [(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)],
        "xhi": [(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)],
        "ylo": [(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)],
        "yhi": [(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)],
        "zlo": [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)],
        "zhi": [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)],
    }
    pc = Poly3DCollection(list(v.values()), facecolor=color, edgecolor=color, alpha=alpha, linewidths=0.6)
    ax.add_collection3d(pc)


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (registers 3d projection)

    # Static geometry (built once; only the camera animates)
    delta3d, c = 0.05, 0.30
    fat_tube = (0.0, 1.0, 0.0, c, 0.0, c)
    x_starts = [0.08, 0.26, 0.44, 0.62, 0.80]
    grains = grain_boxes(delta3d, c, x_starts)

    max_overlap = max((box_pairwise_overlap(grains[i], grains[j])
                       for i in range(len(grains)) for j in range(i + 1, len(grains))), default=0.0)
    starts = sorted(x_starts)
    max_mult = 1 if all(starts[i] + delta3d <= starts[i + 1] + 1e-12 for i in range(len(starts) - 1)) else 2

    # Invariant assertions
    assert delta3d < c < 1.0, f"need delta << c << 1, got {delta3d}, {c}"
    assert delta3d <= c / 4.0, f"delta should be well below c: {delta3d} vs {c}"
    assert max_overlap < 1e-9, f"grains must be pairwise-disjoint, max overlap {max_overlap}"
    assert max_mult == 1, f"each point should lie in at most one grain, got {max_mult}"

    math_check(
        "grain slabs turntable: delta x c x c, disjoint in the fat tube",
        [
            ("grain size", f"delta x c x c = {delta3d} x {c} x {c}   (delta << c << 1: {delta3d} << {c} << 1)"),
            ("grains drawn", f"{len(grains)}  (tile the fat tube along its length; ~1/delta in the limit)"),
            ("grains DISJOINT", f"max pairwise overlap volume = {max_overlap:.6f}  (want 0)"),
            ("point in few grains", f"max grains through any point = {max_mult}  (want 1)"),
            ("one tube thick", "delta-thin along the tube axis X; c x c across the cross-section"),
        ],
    )

    # Preview scene
    fig = plt.figure(figsize=(6.6, 6.0))
    ax = fig.add_subplot(1, 1, 1, projection="3d")
    _draw_box_wire(ax, fat_tube, COLORS["guide"], lw=1.3)
    for g in grains:
        _draw_box_solid(ax, g, COLORS["accent"], alpha=0.6)
    # a few thin tubes running lengthwise
    for (y, z) in [(0.09, 0.18), (0.20, 0.09), (0.15, 0.24), (0.24, 0.20)]:
        ax.plot([0, 1], [y, y], [z, z], color=COLORS["outer"], lw=0.9, alpha=0.85)
    ax.set_box_aspect((1.0, c, c))
    ax.set_xlim(0.0, 1.0); ax.set_ylim(0.0, c); ax.set_zlim(0.0, c)
    ax.set_axis_off()
    ax.set_title("grains = delta x c x c slabs, one tube thick, disjoint in the fat tube", fontsize=9)

    def update(i):
        ax.view_init(elev=18, azim=i * (360.0 / FRAMES))
        return ()

    anim = FuncAnimation(fig, update, frames=FRAMES, interval=60, blit=False)
    print("wrote", save_gif(anim, fps=18, dpi=90))


if __name__ == "__main__":
    main()
