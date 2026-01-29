#!/bin/bash
# Export marimo notebooks to HTML and generate index page
# This script just calls the Python export module

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"
uv run python -m math_explorations.export
