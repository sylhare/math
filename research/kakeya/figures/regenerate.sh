#!/usr/bin/env bash
#
# Regenerate every Kakeya figure from its source script:
#   - static figures -> <name>.png   (via _shared.save_preview)
#   - animations     -> <name>.gif   (via _shared.save_gif)
#
# Usage:
#   bash research/kakeya/figures/regenerate.sh            # regenerate all figures
#   bash research/kakeya/figures/regenerate.sh <file.py>  # regenerate only the given script(s)
#
# Scripts import `_shared` from the figures root, so PYTHONPATH is set to it here.

cd "$(git rev-parse --show-toplevel)" || exit 1
ROOT="$(pwd)"
FIGDIR="research/kakeya/figures"
export PYTHONPATH="$ROOT/$FIGDIR"
RUN=(uv run --with matplotlib --with shapely --with pillow python)
fail=0

run_one() {  # $1 = path to a figure script (repo-relative)
  echo ">> $1"
  if ! "${RUN[@]}" "$1" >/dev/null; then echo "   FAILED: $1"; fail=1; fi
}

if [ "$#" -gt 0 ]; then
  for f in "$@"; do run_one "$f"; done
else
  # every figure script except the shared helpers and the frozen Perron attempts
  # (2_4_perron_attempt*: preserved dead ends with hardcoded output names, not regenerated)
  for f in $(find "$FIGDIR" -name "*.py" ! -name "_shared.py" ! -name "2_4_perron_attempt*.py" | sort); do
    run_one "$f"
  done
fi

find "$FIGDIR" -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null
if [ "$fail" -eq 0 ]; then echo "OK: figures regenerated"; else echo "DONE with FAILURES"; fi
exit "$fail"
