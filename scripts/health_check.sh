#!/usr/bin/env bash
# Cross-platform helper entrypoints live under scripts/
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec bash "$ROOT/deployment/linux/health_check.sh"
