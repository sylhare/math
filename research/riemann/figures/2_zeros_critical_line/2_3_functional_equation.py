"""Figure: the functional-equation symmetry of the zeros.

    rho zero  =>  1 - conj(rho),  conj(rho),  1 - rho  are zeros too       the quadruple
    off the line  {rho, 1 - conj rho, conj rho, 1 - rho}                    four distinct points
    on the line   rho = 1/2 + i gamma  =>  {1/2 + i gamma, 1/2 - i gamma}   collapses to a pair

The two mirror lines are Re s = 1/2 (functional equation) and Im s = 0 (conjugation).
A hypothetical off-line zero drags three partners into a rectangle; an on-line zero has
only its conjugate.

Run: PYTHONPATH=research/riemann/figures uv run --with matplotlib --with mpmath --with pillow \
     python research/riemann/figures/2_zeros_critical_line/2_3_functional_equation.py
"""

from _shared import COLORS, math_check, plot_axes, save_preview

RHO_OFF = complex(0.75, 20.0)
RHO_ON = complex(0.5, 14.13)


def quadruple(rho: complex) -> list[complex]:
    """The four functional-equation / conjugation partners of rho."""
    return [rho, 1 - rho.conjugate(), rho.conjugate(), 1 - rho]


def main():
    off = quadruple(RHO_OFF)
    on = quadruple(RHO_ON)

    off_distinct = {(round(z.real, 6), round(z.imag, 6)) for z in off}
    on_distinct = {(round(z.real, 6), round(z.imag, 6)) for z in on}

    assert len(off_distinct) == 4, f"off-line rho should give 4 distinct partners, got {len(off_distinct)}"
    assert len(on_distinct) == 2, f"on-line rho should collapse to 2 points, got {len(on_distinct)}"
    assert (1 - RHO_OFF.conjugate()) == complex(0.25, 20.0), "1 - conj(rho) mirror across Re=1/2"

    math_check(
        "Symmetry of the zeros: quadruple off the line, pair on it",
        [
            ("off-line rho = 0.75 + 20i", "partners: " + ", ".join(f"{z.real:g}{z.imag:+g}i" for z in off)),
            ("off-line distinct points", f"{len(off_distinct)}   (a quadruple)"),
            ("1 - conj(rho)", f"{(1 - RHO_OFF.conjugate())}   (mirror across Re = 1/2)"),
            ("on-line rho = 0.5 + 14.13i", "partners: " + ", ".join(f"{z.real:g}{z.imag:+g}i" for z in on)),
            ("on-line distinct points", f"{len(on_distinct)}   (conjugate pair)"),
            ("mirror lines", "Re s = 1/2  and  Im s = 0"),
        ],
    )

    fig, axes = plot_axes(ncols=2, figsize=(11.0, 6.0), equal=True)
    ax_off, ax_on = axes

    def frame(ax):
        ax.axvline(0.5, color=COLORS["line"], lw=1.4, zorder=2)
        ax.axhline(0.0, color=COLORS["guide"], lw=0.9, ls="--", zorder=1)
        ax.set_xlim(-0.2, 1.2)
        ax.set_xlabel(r"$\mathrm{Re}\,s$")
        ax.set_ylabel(r"$\mathrm{Im}\,s$")

    frame(ax_off)
    rect_x = [z.real for z in [off[0], off[1], off[3], off[2], off[0]]]
    rect_y = [z.imag for z in [off[0], off[1], off[3], off[2], off[0]]]
    ax_off.plot(rect_x, rect_y, color=COLORS["offline"], lw=1.2, ls="-", alpha=0.7, zorder=3)
    ax_off.plot([z.real for z in off], [z.imag for z in off], "o", color=COLORS["offline"], ms=9, zorder=4)
    for z in off:
        ax_off.annotate(
            f"{z.real:g}{z.imag:+g}i",
            (z.real, z.imag),
            textcoords="offset points",
            xytext=(6, 6),
            fontsize=8,
            color=COLORS["guide"],
        )
    ax_off.set_ylim(-26, 26)
    ax_off.set_title("Off the line: quadruple")

    frame(ax_on)
    ax_on.plot([z.real for z in on], [z.imag for z in on], color=COLORS["zero"], lw=1.2, alpha=0.6, zorder=3)
    ax_on.plot([z.real for z in on], [z.imag for z in on], "o", color=COLORS["zero"], ms=9, zorder=4)
    for z in {(z.real, z.imag) for z in on}:
        ax_on.annotate(
            f"{z[0]:g}{z[1]:+g}i",
            (z[0], z[1]),
            textcoords="offset points",
            xytext=(8, 0),
            fontsize=8,
            color=COLORS["guide"],
        )
    ax_on.set_ylim(-20, 20)
    ax_on.set_title("On the line: conjugate pair")

    fig.suptitle("Symmetry of the zeros", fontsize=13)
    print("wrote", save_preview(fig))


if __name__ == "__main__":
    main()
