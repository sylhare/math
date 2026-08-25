"""Animation: a synthetic stress test of the signature accounting behind the certificate.

Mirror of framework/certificate.py's synthetic_certificate on real symmetric matrices of size d = 60.
A fixed pool of s = 20 orthonormal rank-one positive-semidefinite blocks plays the on-line points
(the matrix P); p signature-(1,1) blocks, each of growing depth, play the off-line pairs (the matrix
Q). As the frame advances p grows 0..20 and the pairs deepen; we read the positive index n_+(G) of
G = P + Q.

Sylvester's law of inertia gives n_+(G) <= s + p: restricting a form cannot manufacture positive
directions, so the positive eigenvalue count never exceeds the on-line points plus one per off-line
pair. Two regimes are visible. Shallow pairs (depth < 1) add a genuine positive direction each, so
n_+ rises while the certified on-line count n_+ - p sits exactly at the truth s = 20. Deep pairs
(depth > 1) compete with on-line directions and cancel them: n_+ saturates, the ceiling s + p keeps
rising, and the certified on-line count n_+ - p falls. It never exceeds the truth. Deepening off-line
pairs only ever lowers the certified on-line count.

Run: PYTHONPATH=research/riemann/figures uv run --with matplotlib --with mpmath --with pillow \
  python research/riemann/figures/7_numerical_framework/7_2_synthetic_certificate_anim.py
"""

import numpy as np
from _shared import COLORS, math_check, save_gif
from matplotlib.animation import FuncAnimation

D = 60
S = 20
P_MAX = 20
DEPTH_LO, DEPTH_HI = 0.5, 2.5
RNG = np.random.default_rng(20260810)


def positive_index(H, tol=1e-9):
    """Number of strictly positive eigenvalues of a real symmetric matrix."""
    w = np.linalg.eigvalsh((H + H.T) / 2.0)
    return int(np.sum(w > tol))


def build_frames():
    """Precompute (p, depth, n_plus) with a fixed on-line P and p deepening off-line blocks.

    The on-line directions are orthonormal, so P has s unit positive eigenvalues. Off-line block i is
    signature (1, 1): its negative direction is the i-th on-line direction (an off-line pair competing
    with an on-line point) scaled by depth d_i, its positive direction is a fresh orthogonal one. Once
    d_i > 1 that pair cancels the on-line point it sits on.
    """
    basis, _ = np.linalg.qr(RNG.standard_normal((D, D)))
    online = [basis[:, k : k + 1] for k in range(S)]
    P = sum(v @ v.T for v in online)
    depths = np.array([DEPTH_LO + i * (DEPTH_HI - DEPTH_LO) / (P_MAX - 1) for i in range(P_MAX)])
    blocks = []
    for i in range(P_MAX):
        vneg = online[i]
        wpos = basis[:, S + i : S + i + 1]
        blocks.append(depths[i] * (-(vneg @ vneg.T) + (wpos @ wpos.T)))
    ps = np.arange(P_MAX + 1)
    n_plus = []
    for p in ps:
        Q = sum(blocks[:p]) if p > 0 else np.zeros((D, D))
        n_plus.append(positive_index(P + Q))
    frame_depth = np.concatenate([[0.0], depths])
    return ps, frame_depth, np.array(n_plus)


def main():
    ps, depth, n_plus = build_frames()
    ceiling = S + ps
    certified = n_plus - ps

    for p, npl in zip(ps, n_plus, strict=True):
        assert npl <= S + p, f"Sylvester bound violated at p={p}: n_+={npl} > s+p={S + p}"
    assert np.all(certified <= S), "certified on-line count exceeded the truth"
    assert certified[-1] < certified[0], "deepening should lower the certified on-line count"

    math_check(
        "synthetic certificate: n_+ <= s + p (Sylvester)",
        [
            ("d, fixed on-line count s", f"{D}, {S}"),
            ("n_+ at p=0 (Q=0)", f"{int(n_plus[0])}  (= s)"),
            ("n_+ at p=20 (deep pairs)", f"{int(n_plus[-1])}"),
            ("Sylvester ceiling s+p at p=20", f"{int(ceiling[-1])}"),
            ("n_+ <= s+p over all frames", f"{bool(np.all(n_plus <= ceiling))}"),
            ("certified n_+ - p <= s always", f"{bool(np.all(certified <= S))}  (max {int(certified.max())})"),
            ("deepening lowers certified count", f"{int(certified[0])} -> {int(certified[-1])}  (never above s)"),
        ],
    )

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7.8, 5.2))
    ax.grid(True, color="#e6e6e6", lw=0.8)
    ax.set_axisbelow(True)

    ax.plot(ps, ceiling, color=COLORS["muted"], lw=1.4, ls="--", label=r"Sylvester ceiling $s+p$")
    ax.axhline(S, color=COLORS["onlinepos"], lw=1.8, label=r"true on-line count $s=20$")
    (npl_line,) = ax.plot([], [], color=COLORS["offline"], lw=2.2, marker="o", ms=4, label=r"positive index $n_+(G)$")
    (cert_line,) = ax.plot([], [], color=COLORS["prime"], lw=2.2, marker="o", ms=4, label=r"certified $n_+ - p$")
    readout = ax.text(0.03, 0.30, "", transform=ax.transAxes, va="top", ha="left", fontsize=11, color=COLORS["guide"])

    ax.set_xlim(-0.5, P_MAX + 0.5)
    ax.set_ylim(0, S + P_MAX + 2)
    ax.set_xlabel("off-line pairs p  (depth grows with p)")
    ax.set_ylabel("count")
    ax.set_title("The certificate never lies")
    ax.legend(loc="upper left", fontsize=9)

    order = list(range(len(ps))) + [len(ps) - 1] * 6

    def update(i):
        k = order[i]
        npl_line.set_data(ps[: k + 1], n_plus[: k + 1])
        cert_line.set_data(ps[: k + 1], certified[: k + 1])
        readout.set_text(
            f"p = {int(ps[k])}   depth = {depth[k]:.2f}\n"
            f"$n_+$ = {int(n_plus[k])} $\\leq$ s+p = {int(ceiling[k])}\n"
            f"certified $n_+ - p$ = {int(certified[k])} $\\leq$ {S}"
        )
        return npl_line, cert_line, readout

    anim = FuncAnimation(fig, update, frames=len(order), interval=200, blit=False)
    print("wrote", save_gif(anim, fps=6, dpi=100))


if __name__ == "__main__":
    main()
