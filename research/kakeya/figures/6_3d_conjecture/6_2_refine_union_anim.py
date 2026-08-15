"""Animation: refining the delta-tube bundle cannot drain the union (kakeya.md section 6).

Halving delta replaces every fat tube by ~4x as many thinner tubes in nearby delta-separated
directions, so the EXACT content stays put:

    #T * |T|  =  (#delta-separated directions) * delta^2  ~  const   (measured, not modelled).

Dimension 3 is exactly the statement that the union inherits this: its leftover-volume meter

    |N_delta K|  ~  delta^(3 - d)

stays pinned near 1 (exponent 3 - d = 0) instead of dimming like a dimension 5/2 set would
(exponent 1/2, losing ~29% per halving toward a sheet).

Left: a slowly turning bundle of delta x delta x 1 tubes; halving delta thins each tube (radius
delta/2) and multiplies the count by four, yet the union silhouette barely moves.
Right: two stacked volume-meters vs the delta ladder. Meter A = the exact content (flat ~1).
Meter B = the dimension-3 curve (flat) against a dimension-5/2 reference (dims).

Reuses the S^2 packing and tube geometry from 6_1_tubes_3d.py.

Run: PYTHONPATH=research/kakeya/figures uv run --with matplotlib --with shapely --with pillow \
     python research/kakeya/figures/6_3d_conjecture/6_2_refine_union_anim.py
"""
import importlib.util
import os

import numpy as np
from _shared import COLORS, math_check, save_gif
from matplotlib.animation import FuncAnimation

# Reuse 6_1's S^2 packing + tube geometry (no side effects on import)
_p = os.path.join(os.path.dirname(__file__), "6_1_tubes_3d.py")
_spec = importlib.util.spec_from_file_location("tubes_6_1", _p)
_m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_m)
fibonacci_sphere = _m.fibonacci_sphere
delta_separated = _m.delta_separated
tube_surface = _m.tube_surface

DELTAS = [0.2, 0.1, 0.05, 0.025]     # the delta ladder (halved each step)
N_SAMPLES = 90000                    # S^2 samples: enough that delta=0.025 is not truncated
EPS = 0.05                           # dim-3 allowed floor |N_delta| >= c_eps delta^eps
DRAWN = [14, 26, 42, 64]             # representative tubes drawn per stage (capped for legibility)
STAGE_HOLD = 9                       # frames held per delta stage (tickers readable)
END_HOLD = 8                         # trailing hold on the finest stage


def main():
    d0 = DELTAS[0]
    deltas = np.array(DELTAS)

    # Math: the measured invariants
    # #directions = size of a chord-delta separated packing on S^2 (grows ~4x per halving).
    samples = fibonacci_sphere(N_SAMPLES)
    counts = np.array([len(delta_separated(samples, d)) for d in DELTAS], dtype=float)

    # |T| = delta^2 (a delta x delta x 1 tube); content #T*|T| = counts * delta^2 ~ const.
    tube_vol = deltas ** 2
    content = counts * tube_vol
    content_norm = content / content[0]

    growth = counts[1:] / counts[:-1]            # want ~4 per halving
    vol_ratio = tube_vol[1:] / tube_vol[:-1]     # exactly 1/4 per halving
    content_spread = content.max() / content.min()

    # Meter B: leftover-volume law |N_delta K| = delta^(3 - d), normalized to the coarsest delta.
    # dim 3 (exponent 0): flat, with an allowed floor delta^eps (droops <= 2^-eps/step).
    # dim 5/2 (exponent 1/2): steps down by 2^-1/2 = 0.7071 per halving (dims toward a sheet).
    dim3_meter = np.ones_like(deltas)                      # delta^(3-3) = delta^0, flat
    dim3_floor = (deltas / d0) ** EPS                      # c_eps delta^eps: max sliver removed
    dim52_meter = (deltas / d0) ** 0.5                     # delta^(3-2.5) = delta^0.5

    ratio_dim3 = dim3_meter[1:] / dim3_meter[:-1]
    ratio_dim52 = dim52_meter[1:] / dim52_meter[:-1]

    # Fitted exponent of the law delta^(3-d): slope of log|N| vs log delta.
    fit_exp_dim3 = float(np.polyfit(np.log(deltas), np.log(deltas ** (3 - 3.0)), 1)[0])
    fit_exp_dim52 = float(np.polyfit(np.log(deltas), np.log(deltas ** (3 - 2.5)), 1)[0])

    # Assertions on the drawn invariants
    assert ((growth > 3.2) & (growth < 4.5)).all(), \
        f"#directions must grow ~4x per halving, got {growth}"
    assert np.allclose(vol_ratio, 0.25, atol=1e-12), \
        f"|T|=delta^2 must divide by 4 each halving, got {vol_ratio}"
    assert content_spread < 2.0, \
        f"content #T*|T| must be roughly constant (max/min < 2), got {content_spread:.3f}"
    assert np.allclose(ratio_dim52, 2 ** -0.5, atol=1e-6), \
        f"dim 5/2 meter must halve-step by 2^-1/2, got {ratio_dim52}"
    assert (ratio_dim3 >= 2 ** (-EPS) - 1e-9).all(), \
        f"dim 3 meter must stay lit (ratio >= 2^-eps), got {ratio_dim3}"
    assert abs(fit_exp_dim3 - 0.0) < 1e-6 and abs(fit_exp_dim52 - 0.5) < 1e-6, \
        f"fitted 3-d exponent must be 0 (dim 3) and 0.5 (dim 5/2), got {fit_exp_dim3}, {fit_exp_dim52}"

    math_check(
        "refine delta: content pinned ~1, dim 3 meter stays lit vs dim 5/2 dims",
        [
            (f"delta={DELTAS[0]}", f"#T={counts[0]:.0f}   |T|=delta^2={tube_vol[0]:.4f}   "
                                   f"content={content[0]:.3f}"),
            (f"delta={DELTAS[1]}", f"#T={counts[1]:.0f}   |T|=delta^2={tube_vol[1]:.4f}   "
                                   f"content={content[1]:.3f}   #T x{growth[0]:.2f}"),
            (f"delta={DELTAS[2]}", f"#T={counts[2]:.0f}   |T|=delta^2={tube_vol[2]:.4f}   "
                                   f"content={content[2]:.3f}   #T x{growth[1]:.2f}"),
            (f"delta={DELTAS[3]}", f"#T={counts[3]:.0f}   |T|=delta^2={tube_vol[3]:.4f}   "
                                   f"content={content[3]:.3f}   #T x{growth[2]:.2f}"),
            ("#T growth per halving", f"{np.round(growth, 2).tolist()}  (want in 3.2..4.5, ~4)"),
            ("|T| ratio per halving", f"{np.round(vol_ratio, 4).tolist()}  (exactly 0.25)"),
            ("content #T*|T| spread", f"max/min = {content_spread:.3f}  (< 2, roughly constant)"),
            ("Meter B dim 3 (delta^0)", f"ratio/step {np.round(ratio_dim3, 4).tolist()}  "
                                        f"(>= 2^-eps={2 ** -EPS:.4f}, stays lit)"),
            ("Meter B dim 5/2 (delta^0.5)", f"ratio/step {np.round(ratio_dim52, 4).tolist()}  "
                                            f"(= 2^-1/2 = {2 ** -0.5:.4f}, dims 29%)"),
            ("fitted 3-d exponent", f"dim 3 -> {fit_exp_dim3:.6f} (0),  "
                                    f"dim 5/2 -> {fit_exp_dim52:.6f} (0.5)"),
        ],
    )

    # Figure
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # A fixed pool of well-spread upper-hemisphere directions; per stage we DRAW a subset
    # (thinner as delta shrinks). Centers are fixed so only radius + count change per stage.
    pool = delta_separated(fibonacci_sphere(8000), 0.22)
    pool = pool[pool[:, 2] >= 0.03][: max(DRAWN)]
    rng = np.random.default_rng(11)
    centers = rng.uniform(-0.16, 0.16, size=(len(pool), 3))

    # faint sphere = the pinned union silhouette (tubes of length 1 fill a ball of radius ~1/2)
    _u = np.linspace(0, 2 * np.pi, 40)
    _v = np.linspace(0, np.pi, 20)
    _sx = 0.52 * np.outer(np.cos(_u), np.sin(_v))
    _sy = 0.52 * np.outer(np.sin(_u), np.sin(_v))
    _sz = 0.52 * np.outer(np.ones_like(_u), np.cos(_v))

    fig = plt.figure(figsize=(13.0, 6.6))
    gs = fig.add_gridspec(2, 2, width_ratios=[1.28, 1.0], hspace=0.32, wspace=0.16)
    axL = fig.add_subplot(gs[:, 0], projection="3d")
    axA = fig.add_subplot(gs[0, 1])
    axB = fig.add_subplot(gs[1, 1])
    fig.suptitle("halve delta:  #T x4,  |T| /4,  content pinned ~ 1", fontsize=13)

    stage_x = np.arange(len(DELTAS))
    xt_labels = [f"{d:g}" for d in DELTAS]

    frames_stage = []
    for k in range(len(DELTAS)):
        frames_stage += [k] * STAGE_HOLD
    frames_stage += [len(DELTAS) - 1] * END_HOLD

    def draw_left(k, azim):
        axL.cla()
        delta = DELTAS[k]
        radius = delta / 2.0
        # pinned union silhouette (constant across stages)
        axL.plot_surface(_sx, _sy, _sz, color=COLORS["region"], alpha=0.06, linewidth=0)
        # representative thinning tubes
        for j in range(DRAWN[k]):
            X, Y, Z = tube_surface(centers[j], pool[j], 1.0, radius)
            axL.plot_surface(X, Y, Z, color=COLORS["outer"], alpha=0.30, linewidth=0)
        axL.set_box_aspect((1, 1, 1))
        axL.set_xlim(-0.6, 0.6); axL.set_ylim(-0.6, 0.6); axL.set_zlim(-0.6, 0.6)
        axL.view_init(elev=18, azim=azim)
        axL.set_xticklabels([]); axL.set_yticklabels([]); axL.set_zticklabels([])
        axL.set_title(f"delta = {delta:g},  radius delta/2\n"
                      f"#T = {counts[k]:.0f}   (showing {DRAWN[k]})", fontsize=11)

    def draw_meter_a(upto):
        axA.cla()
        xs = stage_x[:upto]
        axA.axhline(1.0, color=COLORS["muted"], lw=0.8, ls=":")
        axA.bar(xs, content_norm[:upto], width=0.55, color=COLORS["outer"], alpha=0.55)
        axA.plot(xs, content_norm[:upto], "-o", color=COLORS["outer"], ms=5)
        axA.set_xlim(-0.5, len(DELTAS) - 0.5); axA.set_ylim(0, 1.35)
        axA.set_xticks(stage_x); axA.set_xticklabels(xt_labels)
        axA.set_ylabel("content #T*|T|")
        axA.grid(True, axis="y", color=COLORS["muted"], alpha=0.25, lw=0.5)
        axA.set_title("Meter A: content = #T*delta^2  (flat ~ 1)", fontsize=10)

    def draw_meter_b(upto):
        axB.cla()
        xs = stage_x[:upto]
        # allowed floor delta^eps (faint dashed reference)
        axB.plot(stage_x, dim3_floor, ls="--", lw=1.0, color=COLORS["muted"],
                 label=f"allowed floor delta^eps (eps={EPS:g})")
        axB.plot(xs, dim3_meter[:upto], "-o", color=COLORS["outer"], ms=5,
                 label="dim 3: 3-d = 0  (stays lit)")
        axB.plot(xs, dim52_meter[:upto], "-o", color=COLORS["accent"], ms=5,
                 label="dim 5/2: 3-d = 1/2  (dims 29%/step)")
        if upto >= 1:
            axB.plot(stage_x[upto - 1], dim3_meter[upto - 1], "o", color=COLORS["outer"],
                     ms=11, mfc="none", mew=2)
            axB.plot(stage_x[upto - 1], dim52_meter[upto - 1], "o", color=COLORS["accent"],
                     ms=11, mfc="none", mew=2)
        axB.set_xlim(-0.5, len(DELTAS) - 0.5); axB.set_ylim(0, 1.15)
        axB.set_xticks(stage_x); axB.set_xticklabels(xt_labels)
        axB.set_xlabel("delta"); axB.set_ylabel("|N_delta K|  (rel.)")
        axB.grid(True, axis="y", color=COLORS["muted"], alpha=0.25, lw=0.5)
        axB.legend(loc="lower left", fontsize=7.5)
        axB.set_title("Meter B: |N_delta K| ~ delta^(3-d)", fontsize=10)

    def update(fi):
        k = frames_stage[fi]
        azim = 32 + fi * 1.1
        draw_left(k, azim)
        draw_meter_a(k + 1)
        draw_meter_b(k + 1)
        return []

    anim = FuncAnimation(fig, update, frames=len(frames_stage), interval=140, blit=False)
    print("wrote", save_gif(anim, fps=8, dpi=95))


if __name__ == "__main__":
    main()
