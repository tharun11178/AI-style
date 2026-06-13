#!/usr/bin/env bash
set -euo pipefail
# Change to script directory (backend)
cd "$(dirname "$0")"

# Ensure PYTHONPATH includes backend root so imports work
export PYTHONPATH="$PWD"

# Allow Render to provide PORT; fallback to 8000 when not set
PORT="${PORT:-8000}"

# Prefer venv python if present
if [ -x ".venv/bin/python" ]; then
  PYTHON_BIN=".venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="$(command -v python3)"
else
  PYTHON_BIN="$(command -v python)"
fi

exec "$PYTHON_BIN" -m uvicorn app.main:app --host 0.0.0.0 --port "$PORT" --app-dir .
