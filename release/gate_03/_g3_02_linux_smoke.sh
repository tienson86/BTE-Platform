#!/bin/sh
# G3-02 Linux release smoke — not a high-frequency healthcheck.
# Run from repository root or /app inside the API image.
set -eu
ROOT=$(CDPATH= cd -- "$(dirname "$0")/../.." && pwd)
cd "$ROOT"
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"
python -m pip check
python "$ROOT/release/gate_03/_g3_02_linux_smoke.py"
