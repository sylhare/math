"""Kakeya needle set as a glowing starburst on a dark ground (method #5).

Dense rays leave a bright core and reach outward, their length modulated by a three-fold
lobe so they run long toward the corner directions (90/210/330 deg) and short along the
edges. Each ray is stacked from wide+faint to thin+bright strokes to fake a bloom, so the
overlapping centres read as a solid rounded triangle. Single yellow, no edges, full turn.

Run: uv run --with matplotlib --with shapely --with pillow python research/kakeya/figures/2_kakeya_2d/2_6_5_glow_rays_dark.py
"""
import math
import os

import numpy as np

YELLOW = "#f4e37a"
DARK = "#0b0b12"
CORNERS_DEG = (90.0, 210.0, 330.0)     # three-fold spike directions
N_RAYS = 1000                          # rays over the full turn
L_MIN, L_MAX = 0.50, 1.30              # edge-length vs corner-length of a ray
CORE_R = 0.42                          # radius of the solid glowing core
SEED = 5

# bloom stack: (linewidth, alpha) from wide+faint to thin+bright
BLOOM = [(5.5, 0.018), (3.2, 0.040), (1.8, 0.10), (0.9, 0.30), (0.5, 0.85)]


def _lobe(theta):
    """Three-fold weight in [0,1], peaking at the corner directions, sharpened."""
    return (0.5 * (1.0 + np.cos(3.0 * (theta - math.radians(90.0))))) ** 1.7


def build_rays(rng):
    """Return (segments, r_out) for rays from the core out to a lobe-modulated tip."""
    theta = np.linspace(0.0, 2.0 * math.pi, N_RAYS, endpoint=False)
    theta = theta + rng.normal(0.0, 0.006, N_RAYS)        # tiny angular jitter -> shaggy edge
    lobe = _lobe(theta)
    jitter = 0.80 + 0.34 * rng.random(N_RAYS)             # per-ray length scatter
    r_out = (L_MIN + (L_MAX - L_MIN) * lobe) * jitter
    r_core = CORE_R * (0.55 + 0.72 * _lobe(theta))         # rounded-triangle core boundary
    r_in = r_core * (0.35 + 0.35 * rng.random(N_RAYS))    # start inside the core so it glows
    cx, cy = np.cos(theta), np.sin(theta)
    p0 = np.column_stack([r_in * cx, r_in * cy])
    p1 = np.column_stack([r_out * cx, r_out * cy])
    segs = np.stack([p0, p1], axis=1)
    return segs, r_out


def core_polygon(n=720):
    """Rounded apex-up triangle: a disc bulged out toward the three corner directions."""
    theta = np.linspace(0.0, 2.0 * math.pi, n, endpoint=False)
    r = CORE_R * (0.55 + 0.72 * _lobe(theta))
    return np.column_stack([r * np.cos(theta), r * np.sin(theta)])


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection

    rng = np.random.default_rng(SEED)
    segs, r_out = build_rays(rng)
    core = core_polygon()

    print("\n=== MATH CHECK: glow rays (dark, method #5) ===")
    print(f"  rays              : {N_RAYS} over the full turn (a ray in every direction)")
    print(f"  three-fold spikes : lobe peaks at {CORNERS_DEG} deg, len {L_MIN:.2f}..{L_MAX:.2f}")
    print(f"  max reach         : {r_out.max():.3f}   min reach : {r_out.min():.3f}")
    print("  bloom             : " + " -> ".join(f"lw{w}/a{a}" for w, a in BLOOM))
    print("=" * 46)

    reach = float(r_out.max()) * 1.06
    fig, ax = plt.subplots(figsize=(6.71, 5.86))
    fig.patch.set_facecolor(DARK)
    ax.set_facecolor(DARK)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-reach, reach)
    ax.set_ylim(-reach * 0.90, reach * 1.02)

    # solid glowing core underneath the rays
    ax.fill(core[:, 0], core[:, 1], facecolor=YELLOW, edgecolor="none", zorder=1)

    # stacked bloom passes: same segments, wide+faint first, thin+bright last
    for lw, alpha in BLOOM:
        lc = LineCollection(segs, colors=YELLOW, linewidths=lw, alpha=alpha,
                            capstyle="round", antialiaseds=True, zorder=2)
        lc.set_rasterized(True)
        ax.add_collection(lc)

    out = os.path.splitext(os.path.abspath(__file__))[0] + ".png"
    fig.savefig(out, dpi=150, facecolor=DARK, bbox_inches="tight", pad_inches=0.0)
    print("wrote", out)


if __name__ == "__main__":
    main()
