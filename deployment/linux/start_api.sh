#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

mkdir -p logs reports applications/data

set -a
# shellcheck disable=SC1091
[[ -f deployment/env/development.env ]] && . deployment/env/development.env
set +a

export HOST="${HOST:-127.0.0.1}"
export PORT="${API_PORT:-${PORT:-8000}}"
export BTE_LOG_LEVEL="${BTE_LOG_LEVEL:-INFO}"
export BTE_STORAGE_BACKEND="${BTE_STORAGE_BACKEND:-json}"
export BTE_DATA_DIR="${BTE_DATA_DIR:-applications/data}"
export BTE_LICENSE_PATH="${BTE_LICENSE_PATH:-applications/data/licenses.json}"
export BTE_REPORT_PATH="${BTE_REPORT_PATH:-reports}"

PYTHON="python3"
[[ -x .venv/bin/python ]] && PYTHON=".venv/bin/python"

echo "Starting BTE API on ${HOST}:${PORT} ..."
exec "$PYTHON" -m uvicorn applications.api.app:app --host "$HOST" --port "$PORT" \
  >> logs/api.log 2>&1
