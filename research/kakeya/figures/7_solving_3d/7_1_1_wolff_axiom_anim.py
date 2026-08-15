"""Animation: the Wolff axiom as a capacity law (kakeya.md section 6, Hickman Def. 5.6).

For every rectangular prism R in R^3 and a direction-separated family of delta-tubes,

    #{ T in T : T subset of R }  <=  delta^-2 |R|      (each tube has volume delta^2, overlaps bounded).

Read as a capacity: a prism of volume |R| holds at most delta^-2 |R| tubes. Thinning the slab shrinks
|R|, so the cap drops and the slab can legally hold fewer tubes. The axiom rules out the degenerate
packing "all delta^-2 tubes into one thin slab": that count exceeds delta^-2 |R|.

Left: a slab R (1 x 1 x Lz) thinning, holding a direction-separated bush of tubes up to its cap.
Right: a meter, cap delta^-2 |R| vs the tube count, count staying under the cap; then a forbidden
frame that over-stuffs the thin slab (count > cap, flagged).

With delta = 1/3 (delta^-2 = 9) and |R| = Lz, the cap is 9*Lz, integer at the chosen depths.
Wolff's resulting R^3 dimension lower bound (1995): (n+2)/2 = 5/2.

Run: PYTHONPATH=research/kakeya/figures uv run --with matplotlib --with shapely --with pillow \
     python research/kakeya/figures/7_solving_3d/7_1_1_wolff_axiom_anim.py
"""

import numpy as np
from _shared import COLORS, math_check, save_gif

DELTA = 1.0 / 3.0  # delta^-2 = 9
LX = LY = 1.0
# slab thicknesses so the cap 9*Lz is an integer 9,7,5,4,3; then the forbidden over-stuff
LZ_LEGAL = [9 / 9, 7 / 9, 5 / 9, 4 / 9, 3 / 9]
CHEAT_LZ = 3 / 9  # thinnest legal slab (cap 3) crammed with all 9 tubes -> violates
CHEAT_COUNT = 9
HOLD = 5
END_HOLD = 8


# Geometry (pure numpy)
def bush_tubes(n):
    """n direction-separated in-plane tubes through the origin: distinct directions in [0, pi)."""
    angles = np.linspace(0.0, np.pi, n, endpoint=False)
    return [np.array([np.cos(a), np.sin(a), 0.0]) for a in angles]


def tube_frame(direction):
    u = direction / np.linalg.norm(direction)
    tmp = np.array([1.0, 0.0, 0.0]) if abs(u[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
    v = np.cross(u, tmp)
    v /= np.linalg.norm(v)
    w = np.cross(u, v)
    return u, v, w


def tube_surface(direction, length, radius, n_theta=14):
    u, v, w = tube_frame(direction)
    theta = np.linspace(0, 2 * np.pi, n_theta)
    s = np.linspace(-length / 2, length / 2, 2)
    S, T = np.meshgrid(s, theta)
    X = S * u[0] + radius * (np.cos(T) * v[0] + np.sin(T) * w[0])
    Y = S * u[1] + radius * (np.cos(T) * v[1] + np.sin(T) * w[1])
    Z = S * u[2] + radius * (np.cos(T) * v[2] + np.sin(T) * w[2])
    return X, Y, Z


def prism_edges(lx, ly, lz):
    hx, hy, hz = lx / 2, ly / 2, lz / 2
    c = np.array([[sx * hx, sy * hy, sz * hz] for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)])
    return [(c[i], c[j]) for i in range(8) for j in range(i + 1, 8) if np.sum(np.abs(c[i] - c[j]) > 1e-9) == 1]


def cap(lz):
    return DELTA**-2 * (LX * LY * lz)


def main():
    # stages: (Lz, tube count, legal?)  -- legal packs count = cap; the cheat over-stuffs the thin slab
    stages = [dict(lz=lz, count=round(cap(lz)), legal=True) for lz in LZ_LEGAL]
    stages.append(dict(lz=CHEAT_LZ, count=CHEAT_COUNT, legal=False))

    # --- assertions: legal counts respect the cap and fall with |R|; the cheat violates it ---
    caps = [cap(s["lz"]) for s in stages]
    for i, s in enumerate(stages):
        if s["legal"]:
            assert s["count"] <= caps[i] + 1e-9, f"legal slab must respect the cap: {s['count']} > {caps[i]}"
    legal_caps = [cap(s["lz"]) for s in stages if s["legal"]]
    assert all(legal_caps[i] < legal_caps[i - 1] for i in range(1, len(legal_caps))), "cap must fall as Lz shrinks"
    cheat = stages[-1]
    assert cheat["count"] > cap(cheat["lz"]) + 1e-9, "the cheat must exceed the cap (forbidden)"

    math_check(
        "Wolff axiom  #{T in R} <= delta^-2 |R|   (capacity law)",
        [
            ("delta", f"{DELTA:.4f}   delta^-2 = {DELTA**-2:.0f}"),
            ("slab R", f"{LX} x {LY} x Lz,  |R| = Lz,  cap = delta^-2 |R| = 9 Lz"),
            *[
                (f"legal Lz = {s['lz']:.3f}", f"cap {cap(s['lz']):.0f}, tubes {s['count']}  -> {s['count']} <= {cap(s['lz']):.0f}  OK")
                for s in stages
                if s["legal"]
            ],
            ("cap falls with the slab", f"{legal_caps[0]:.0f} -> {legal_caps[-1]:.0f}  as Lz {LZ_LEGAL[0]:.2f} -> {LZ_LEGAL[-1]:.2f}"),
            ("forbidden cheat", f"Lz {CHEAT_LZ:.3f}, cap {cap(CHEAT_LZ):.0f}, tubes {CHEAT_COUNT}  -> {CHEAT_COUNT} > {cap(CHEAT_LZ):.0f}  VIOLATES"),
            ("Wolff R^3 bound (n+2)/2", "5/2  (n=3)  -> dim >= 5/2 (Wolff 1995)"),
        ],
    )

    # Figure
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    radius = DELTA / 2.0
    fig = plt.figure(figsize=(12.6, 6.3))
    fig.suptitle("Wolff axiom: a slab holds at most delta^-2 |R| tubes", fontsize=13)
    axL = fig.add_subplot(1, 2, 1, projection="3d")
    axR = fig.add_subplot(1, 2, 2)

    frame_stage = [0] * HOLD + list(range(len(stages))) + [len(stages) - 1] * END_HOLD
    cap_max = cap(LZ_LEGAL[0])  # 9, the full cap for the meter y-axis

    def update(fi):
        s = stages[frame_stage[fi]]
        lz, count, legal = s["lz"], s["count"], s["legal"]
        col = COLORS["outer"] if legal else COLORS["accent"]

        # LEFT: the slab + the bush of direction-separated tubes it holds
        axL.cla()
        for a, b in prism_edges(LX, LY, lz):
            axL.plot(*zip(a, b, strict=False), color=COLORS["guide"], lw=1.0, alpha=0.9)
        for d in bush_tubes(count):
            X, Y, Z = tube_surface(d, 1.0, radius)
            axL.plot_surface(X, Y, Z, color=COLORS["accent"], alpha=0.6, linewidth=0)
        axL.set_box_aspect((1.0, 1.0, 0.7))
        axL.set_xlim(-0.6, 0.6)
        axL.set_ylim(-0.6, 0.6)
        axL.set_zlim(-0.45, 0.45)
        axL.view_init(elev=20, azim=-60)
        axL.set_xticklabels([])
        axL.set_yticklabels([])
        axL.set_zticklabels([])
        axL.set_title(f"slab R = 1 x 1 x {lz:.2f},  |R| = {lz:.2f}", fontsize=10, color=col)

        # RIGHT: capacity meter (cap outline vs tube count fill)
        axR.cla()
        axR.set_xlim(-0.6, 1.6)
        axR.set_ylim(0, cap_max + 0.8)
        axR.set_xticks([0, 1])
        axR.set_xticklabels(["cap  delta^-2 |R|", "tubes in R"])
        axR.set_ylabel("number of tubes")
        axR.grid(True, axis="y", color=COLORS["muted"], alpha=0.25, lw=0.5)
        thebar = cap(lz)
        axR.bar(0, thebar, width=0.6, facecolor="none", edgecolor=COLORS["guide"], lw=2.0, hatch="//")
        axR.bar(1, count, width=0.6, facecolor=col, edgecolor=col, alpha=0.75)
        axR.text(0, thebar + 0.2, f"{thebar:.0f}", ha="center", va="bottom", fontsize=12, color=COLORS["guide"])
        axR.text(1, count + 0.2, f"{count}", ha="center", va="bottom", fontsize=12, color=col, weight="bold")
        verdict = f"{count} <= {thebar:.0f}   within capacity" if legal else f"{count} > {thebar:.0f}   FORBIDDEN"
        axR.set_title(verdict, fontsize=11, color=col, weight="bold")
        if not legal:
            axR.axhline(thebar, color=COLORS["accent"], ls="--", lw=1.2)
            axR.text(1, thebar - 0.35, "over the cap:\nall tubes in one thin slab", ha="center", va="top",
                     fontsize=9, color=COLORS["accent"])
        return []

    anim = FuncAnimation(fig, update, frames=len(frame_stage), interval=150, blit=False)
    print("wrote", save_gif(anim, fps=6, dpi=95))


if __name__ == "__main__":
    main()
