#!/usr/bin/env bash
# Usage: restore.sh <archive.tar.gz> <target-dir> [--verify]
set -euo pipefail

ARCHIVE="${1:?archive required}"
TARGET="${2:?target directory required}"
VERIFY="${3:-}"

mkdir -p "$TARGET"
tar -tzf "$ARCHIVE" >/dev/null
tar -xzf "$ARCHIVE" -C "$TARGET"

if [[ "$VERIFY" == "--verify" ]]; then
  test -f "$TARGET/knowledge-manifest.txt"
  test -d "$TARGET/data"
  test -d "$TARGET/config"
  echo "verify_ok $TARGET"
  exit 0
fi

echo "extracted $ARCHIVE -> $TARGET"
echo "Next: stop api/portal, copy data/ into volume, start, smoke /health /version"
