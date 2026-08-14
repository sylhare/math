"""Kakeya needle set as a starburst on a dark ground.

240 rays leave a bright centre over the full 360 deg turn; each ray reaches
r = R_MIN + (R_MAX - R_MIN) * (1 + cos(3*theta)) / 2, a three-fold lobe long toward the
corner directions (90/210/330 deg) and short along the edges. Each ray is drawn as a
wide-faint to thin-bright stack of strokes to bloom. Single yellow, no edges.

Run: uv run --with matplotlib --with shapely --with pillow python research/kakeya/figures/2_kakeya_2d/2_6_5_glow_dark.py
"""
import math

import numpy as np
from _shared import math_check, save_preview

YELLOW = "#f4e37a"
DARK = "#0b0b12"
CORNERS_DEG = (90.0, 210.0, 330.0)
N_RAYS = 240
R_MIN, R_MAX = 0.42, 1.25            # edge-length vs corner-length of a ray
R_IN = 0.05                          # inner start radius (near the centre)
CORE_R = 0.34                        # rounded-triangle core radius

# bloom stack: (linewidth, alpha) from wide+faint to thin+bright
BLOOM = [(6.0, 0.015), (3.4, 0.035), (1.9, 0.10), (1.0, 0.28), (0.5, 0.85)]


def _lobe(theta):
    """Three-fold weight in [0,1], peaking at the corner directions."""
    return 0.5 * (1.0 + np.cos(3.0 * (theta - math.radians(90.0))))


def build_rays():
    """(segments, r_out) for rays from R_IN out to a cos(3*theta) lobe-modulated tip."""
    theta = np.linspace(0.0, 2.0 * math.pi, N_RAYS, endpoint=False)
    r_out = R_MIN + (R_MAX - R_MIN) * _lobe(theta)
    cx, cy = np.cos(theta), np.sin(theta)
    p0 = np.column_stack([R_IN * cx, R_IN * cy])
    p1 = np.column_stack([r_out * cx, r_out * cy])
    return np.stack([p0, p1], axis=1), r_out


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

    segs, r_out = build_rays()
    core = core_polygon()

    reach = float(r_out.max()) * 1.06
    fig, ax = plt.subplots(figsize=(6.6, 6.6))
    fig.patch.set_facecolor(DARK)
    ax.set_facecolor(DARK)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-reach, reach)
    ax.set_ylim(-reach, reach)

    ax.fill(core[:, 0], core[:, 1], facecolor=YELLOW, edgecolor="none", zorder=1)
    for lw, alpha in BLOOM:
        lc = LineCollection(segs, colors=YELLOW, linewidths=lw, alpha=alpha,
                            capstyle="round", zorder=2)
        lc.set_rasterized(True)
        ax.add_collection(lc)

    math_check(
        "Kakeya needle set as a starburst (dark)",
        [
            ("rays", f"{N_RAYS} over the full turn: a ray in every direction (all 360 deg)"),
            ("lobe", f"r = {R_MIN:.2f} + {R_MAX - R_MIN:.2f}*(1+cos 3theta)/2, peaks at {CORNERS_DEG} deg"),
            ("reach", f"max {r_out.max():.3f}, min {r_out.min():.3f}"),
            ("bloom", " -> ".join(f"lw{w}/a{a}" for w, a in BLOOM)),
        ],
    )
    print("wrote", save_preview(fig, dpi=170))


if __name__ == "__main__":
    main()
