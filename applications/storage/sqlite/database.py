"""SQLite connection helpers (stdlib only — no ORM)."""

from __future__ import annotations

import sqlite3
from pathlib import Path

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY,
    full_name TEXT NOT NULL,
    gender TEXT,
    birth_datetime TEXT,
    timezone TEXT,
    language TEXT,
    phone TEXT,
    email TEXT,
    notes TEXT,
    tags_json TEXT NOT NULL DEFAULT '[]',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cases (
    case_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    created_at TEXT NOT NULL,
    engine_version TEXT NOT NULL,
    input_snapshot_json TEXT NOT NULL DEFAULT '{}',
    calendar_result_json TEXT NOT NULL DEFAULT '{}',
    bazi_result_json TEXT NOT NULL DEFAULT '{}',
    pattern_result_json TEXT NOT NULL DEFAULT '{}',
    score_result_json TEXT NOT NULL DEFAULT '{}',
    interpretation_result_json TEXT NOT NULL DEFAULT '{}',
    report_result_json TEXT NOT NULL DEFAULT '{}',
    narrative_result_json TEXT NOT NULL DEFAULT '{}',
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE INDEX IF NOT EXISTS idx_customers_created_at ON customers(created_at);
CREATE INDEX IF NOT EXISTS idx_customers_email ON customers(email);
CREATE INDEX IF NOT EXISTS idx_customers_phone ON customers(phone);
CREATE INDEX IF NOT EXISTS idx_cases_customer_id ON cases(customer_id);
CREATE INDEX IF NOT EXISTS idx_cases_created_at ON cases(created_at);
"""


class SQLiteDatabase:
    """Thin sqlite3 wrapper for WP12 persistence."""

    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_schema()

    def connect(self) -> sqlite3.Connection:
        """Open a connection with row factory."""
        conn = sqlite3.connect(str(self.path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _ensure_schema(self) -> None:
        with self.connect() as conn:
            conn.executescript(SCHEMA_SQL)
            conn.commit()
