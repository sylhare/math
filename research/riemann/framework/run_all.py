"""Run the whole framework: the linear-algebra core, the finite Weil form, pair correlation, the
certificate assembly, and the push-further ceiling analysis. Each sub-module prints its own MATH
CHECK block and asserts its invariants.

Run: uv run --with numpy --with mpmath python research/riemann/framework/run_all.py
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import certificate
import linear_algebra
import pair_correlation
import push_further
import weil_form


def main() -> None:
    print("#" * 60)
    print("# Riemann 2/3 argument: reproducible framework")
    print("#" * 60)
    linear_algebra.main()
    weil_form.main()
    pair_correlation.main()
    certificate.main()
    push_further.main()
    print("\nAll framework checks passed.")


if __name__ == "__main__":
    main()
