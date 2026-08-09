#!/usr/bin/env bash
# BTE backup — data, reports, config examples. No secrets required in-tree.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUT_DIR="${BTE_BACKUP_DIR:-$ROOT/backups}"
ARCHIVE="$OUT_DIR/bte-backup-$STAMP.tar.gz"
STAGE="$(mktemp -d)"

mkdir -p "$OUT_DIR" "$STAGE/data" "$STAGE/reports" "$STAGE/config"

if [[ -d "$ROOT/applications/data" ]]; then
  cp -a "$ROOT/applications/data/." "$STAGE/data/" || true
fi
if [[ -d "$ROOT/reports" ]]; then
  cp -a "$ROOT/reports/." "$STAGE/reports/" || true
fi

cp -a "$ROOT/deployment/docker/docker-compose.dev.yml" "$STAGE/config/" 2>/dev/null || true
cp -a "$ROOT/deployment/docker/docker-compose.beta.yml" "$STAGE/config/" 2>/dev/null || true
cp -a "$ROOT/deployment/docker/docker-compose.production.yml" "$STAGE/config/" 2>/dev/null || true
cp -a "$ROOT/deployment/docker/.env.example" "$STAGE/config/" 2>/dev/null || true
cp -a "$ROOT/deployment/docker/.env.production.example" "$STAGE/config/" 2>/dev/null || true
cp -a "$ROOT/deployment/nginx" "$STAGE/config/nginx" 2>/dev/null || true

{
  echo "git=$(git -C "$ROOT" rev-parse HEAD 2>/dev/null || echo unknown)"
  echo "created_utc=$STAMP"
} > "$STAGE/knowledge-manifest.txt"

tar -czf "$ARCHIVE" -C "$STAGE" .
rm -rf "$STAGE"
sha256sum "$ARCHIVE" > "$ARCHIVE.sha256" 2>/dev/null || shasum -a 256 "$ARCHIVE" > "$ARCHIVE.sha256"
echo "$ARCHIVE"
