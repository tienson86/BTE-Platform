"""Durable, account-scoped snapshots of completed customer analyses."""
from __future__ import annotations
import json
import os
import sqlite3
from contextlib import contextmanager
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

def archive_path() -> Path:
    return Path(os.environ.get("BTE_ANALYSIS_ARCHIVE_PATH") or
                Path(__file__).resolve().parents[3] / "data" / "analysis_archive.sqlite3")

@contextmanager
def _connect():
    path = archive_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path), timeout=30)
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=FULL")
        conn.execute("CREATE TABLE IF NOT EXISTS analyses (owner TEXT NOT NULL, id TEXT NOT NULL, saved_at TEXT NOT NULL, snapshot TEXT NOT NULL, PRIMARY KEY(owner,id))")
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def save_snapshot(owner: str, row: dict[str, Any]) -> None:
    if not owner.startswith("user:"):
        raise ValueError("Hồ sơ mới phải thuộc tài khoản đăng nhập")
    identifier = str(row.get("analysis_id") or row.get("id") or "").strip()
    if not identifier or not isinstance(row.get("data"), dict):
        raise ValueError("Hồ sơ thiếu mã phân tích hoặc dữ liệu kết quả")
    from applications.api.auth.dependencies import get_user_service
    actor = get_user_service().store.get_by_id(owner.removeprefix("user:"))
    snapshot = dict(row, id=identifier, analysis_id=identifier)
    # Creator fields come from the authenticated owner, never imported client metadata.
    snapshot.update(owner_user_id=owner.removeprefix("user:"),
                    creator_username=actor.username if actor else "",
                    creator_display_name=getattr(actor, "display_name", "") if actor else "")
    saved_at = str(row.get("saved_at") or row.get("created_at") or datetime.now(timezone.utc).isoformat())
    snapshot.update(saved_at=saved_at, created_at=saved_at)
    with _connect() as conn:
        conn.execute("INSERT OR IGNORE INTO analyses VALUES (?,?,?,?)", (owner, identifier, saved_at, json.dumps(snapshot, ensure_ascii=False)))
        from applications.api.services.van_han_source_index import create_index, index_row
        create_index(conn)
        stored=conn.execute("SELECT snapshot FROM analyses WHERE owner=? AND id=?",(owner,identifier)).fetchone()
        index_row(conn,owner,json.loads(stored[0]))

    logging.getLogger(__name__).info("archive.saved owner=%s analysis_id=%s", owner, identifier)

def list_snapshots(owner: str) -> list[dict[str, Any]]:
    with _connect() as conn:
        rows = conn.execute("SELECT snapshot FROM analyses WHERE owner=? ORDER BY saved_at DESC,id DESC", (owner,)).fetchall()
    return [json.loads(row[0]) for row in rows]

def delete_snapshots(owner: str) -> None:
    with _connect() as conn:
        conn.execute("DELETE FROM analyses WHERE owner=?", (owner,))


def get_snapshot(owner: str, analysis_id: str) -> dict[str, Any] | None:
    """Read one record only inside the authenticated owner's archive."""
    with _connect() as conn:
        row = conn.execute("SELECT snapshot FROM analyses WHERE owner=? AND id=?", (owner, analysis_id)).fetchone()
    return json.loads(row[0]) if row else None
