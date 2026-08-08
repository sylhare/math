"""Run a Lean snippet through this project's toolchain and report the result.

The bridge is what lets a notebook show *validated* math: pass a Lean snippet,
get back whether Lean accepted it, the compiler output, and how long it took.
Snippets with `import Mathlib...` resolve against the built cache, so Mathlib
lemmas are available.

CLI self-test:  uv run python bridge/lean_check.py
"""

from __future__ import annotations

import os
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent  # the `lean/` Lake project
ELAN_BIN = Path.home() / ".elan" / "bin"


@dataclass
class CheckResult:
    ok: bool  # Lean accepted the snippet with no errors
    has_sorry: bool  # compiled, but a proof was stubbed with `sorry`
    output: str  # combined compiler stdout+stderr (errors/warnings)
    seconds: float

    @property
    def status(self) -> str:
        if not self.ok:
            return "error"
        return "incomplete (sorry)" if self.has_sorry else "verified"


def _env() -> dict[str, str]:
    env = os.environ.copy()
    if ELAN_BIN.is_dir():
        env["PATH"] = f"{ELAN_BIN}{os.pathsep}{env.get('PATH', '')}"
    return env


def check(snippet: str, timeout: int = 180) -> CheckResult:
    """Compile `snippet` with `lake env lean`. Returns a CheckResult."""
    # Write into the project dir so Lake resolves the manifest and Mathlib oleans.
    with tempfile.NamedTemporaryFile("w", suffix=".lean", dir=PROJECT_ROOT, delete=False, encoding="utf-8") as f:
        f.write(snippet)
        tmp = Path(f.name)
    try:
        start = time.perf_counter()
        proc = subprocess.run(
            ["lake", "env", "lean", tmp.name],
            cwd=PROJECT_ROOT,
            env=_env(),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        seconds = time.perf_counter() - start
        output = (proc.stdout + proc.stderr).strip()
        return CheckResult(
            ok=proc.returncode == 0,
            has_sorry="sorry" in output.lower(),
            output=output,
            seconds=seconds,
        )
    finally:
        tmp.unlink(missing_ok=True)


if __name__ == "__main__":
    cases = {
        "true arithmetic": "example : 2 + 2 = 4 := rfl",
        "false arithmetic": "example : 2 + 2 = 5 := rfl",
        "pythagorean identity (Mathlib)": (
            "import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic\n"
            "open Real\n"
            "example (θ : ℝ) : sin θ ^ 2 + cos θ ^ 2 = 1 := sin_sq_add_cos_sq θ"
        ),
    }
    for name, snip in cases.items():
        r = check(snip)
        print(f"[{r.status:>18}] {name}  ({r.seconds:.1f}s)")
        if not r.ok:
            print("    " + r.output.replace("\n", "\n    "))
