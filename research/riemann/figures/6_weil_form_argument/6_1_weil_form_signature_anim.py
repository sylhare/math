"""Animation: the signature of the finite Weil form G = P + Q built one contribution at a time.

Small real symmetric d x d model (d = 30):
    on-line point    -> a * v v^T           rank-one positive-semidefinite block, one POSITIVE eigenvalue
    off-line pair    -> a u1 u1^T - b u2 u2^T   signature-(1,1) block, one positive + one NEGATIVE
Sequence: add ~15 on-line points, then ~8 off-line pairs. Each frame shows the sorted eigenvalue
spectrum coloured by sign (green +, red -, gray ~0) and the readout n_plus, s, p.

Sylvester's law of inertia: restricting a form cannot manufacture positive directions, so the
number of positive eigenvalues obeys n_plus <= s + p. Asserted on every frame.

Run: PYTHONPATH=research/riemann/figures uv run --with matplotlib --with mpmath --with pillow \
     python research/riemann/figures/6_weil_form_argument/6_1_weil_form_signature_anim.py
"""

import numpy as np
from _shared import COLORS, math_check, save_gif

DIM = 30
N_ONLINE = 15
N_OFFLINE = 8
EPS = 1e-6


def unit(rng: np.random.Generator) -> np.ndarray:
    """A random real unit vector in R^DIM."""
    v = rng.standard_normal(DIM)
    return v / np.linalg.norm(v)


def build_steps(rng: np.random.Generator):
    """List of (kind, block) contributions: N_ONLINE on-line points then N_OFFLINE off-line pairs."""
    steps = []
    for _ in range(N_ONLINE):
        v = unit(rng)
        a = 0.6 + 0.8 * rng.random()
        steps.append(("online", a * np.outer(v, v)))
    for _ in range(N_OFFLINE):
        u1 = unit(rng)
        u2 = rng.standard_normal(DIM)
        u2 = u2 - (u2 @ u1) * u1
        u2 = u2 / np.linalg.norm(u2)
        a = 0.6 + 0.8 * rng.random()
        b = 0.6 + 0.8 * rng.random()
        steps.append(("offline", a * np.outer(u1, u1) - b * np.outer(u2, u2)))
    return steps


def sign_colors(eigs: np.ndarray) -> list[str]:
    """Colour each eigenvalue: green positive, red negative, gray near zero."""
    out = []
    for e in eigs:
        if e > EPS:
            out.append(COLORS["onlinepos"])
        elif e < -EPS:
            out.append(COLORS["zero"])
        else:
            out.append(COLORS["muted"])
    return out


def main():
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    rng = np.random.default_rng(1859)
    steps = build_steps(rng)

    spectra, states = [], []
    G = np.zeros((DIM, DIM))
    s = p = 0
    for kind, block in steps:
        G = G + block
        if kind == "online":
            s += 1
        else:
            p += 1
        eigs = np.sort(np.linalg.eigvalsh(G))[::-1]
        n_plus = int((eigs > EPS).sum())
        assert n_plus <= s + p, f"Sylvester violated: n_plus={n_plus} > s+p={s + p}"
        spectra.append(eigs)
        states.append((kind, s, p, n_plus))

    n_plus_final = states[-1][3]

    math_check(
        "Signature of the finite form G = P + Q",
        [
            ("model size d", f"{DIM} x {DIM} real symmetric"),
            ("on-line point -> block", "a v v^T : rank 1, one POSITIVE eigenvalue"),
            ("off-line pair -> block", "a u1u1^T - b u2u2^T : signature (1,1), one + one -"),
            ("after all steps: s, p", f"s = {N_ONLINE}, p = {N_OFFLINE}"),
            ("n_plus (positive eigenvalues)", f"{n_plus_final}"),
            ("Sylvester n_plus <= s + p", f"{n_plus_final} <= {N_ONLINE + N_OFFLINE}  (holds every frame)"),
        ],
    )

    ymin = min(sp.min() for sp in spectra)
    ymax = max(sp.max() for sp in spectra)
    pad = 0.1 * (ymax - ymin)

    fig, ax = plt.subplots(figsize=(7.4, 5.0))
    ax.grid(True, axis="y", color="#e6e6e6", lw=0.8)
    ax.set_axisbelow(True)
    idx = np.arange(DIM)
    bars = ax.bar(idx, np.zeros(DIM), color=COLORS["muted"])
    ax.axhline(0.0, color=COLORS["line"], lw=1.0)
    ax.set_xlim(-0.7, DIM - 0.3)
    ax.set_ylim(ymin - pad, ymax + pad)
    ax.set_xlabel("eigenvalue index (sorted)")
    ax.set_ylabel("eigenvalue")
    ax.set_title("Signature of the finite form")
    readout = ax.text(0.98, 0.96, "", transform=ax.transAxes, va="top", ha="right", fontsize=10, color=COLORS["guide"])

    handles = [
        plt.Line2D([0], [0], color=COLORS["onlinepos"], lw=6, label="positive"),
        plt.Line2D([0], [0], color=COLORS["zero"], lw=6, label="negative"),
    ]
    ax.legend(handles=handles, loc="lower left", framealpha=0.9)

    def update(frame):
        eigs = spectra[frame]
        cols = sign_colors(eigs)
        for b, h, c in zip(bars, eigs, cols, strict=True):
            b.set_height(h)
            b.set_color(c)
        kind, s_, p_, n_plus = states[frame]
        readout.set_text(f"adding {kind}\ns = {s_}   p = {p_}\nn+ = {n_plus}   (s+p = {s_ + p_})")
        return [*bars, readout]

    anim = FuncAnimation(fig, update, frames=len(spectra), interval=450, blit=False)
    print("wrote", save_gif(anim, fps=3, dpi=100))


if __name__ == "__main__":
    main()
