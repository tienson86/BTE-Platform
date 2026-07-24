"""SQLite CaseRepository (stdlib sqlite3)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from applications.case_management.models import CaseModel
from applications.storage.interfaces.case_repository import CaseRepository
from applications.storage.interfaces.repository import (
    CaseFilter,
    Page,
    PageResult,
    paginate,
)
from applications.storage.json._filters import match_case
from applications.storage.sqlite.database import SQLiteDatabase

_JSON_FIELDS = (
    "input_snapshot",
    "calendar_result",
    "bazi_result",
    "pattern_result",
    "score_result",
    "interpretation_result",
    "report_result",
    "narrative_result",
)


class SQLiteCaseRepository(CaseRepository):
    """Case CRUD / search on SQLite."""

    def __init__(self, database: SQLiteDatabase | Path | str) -> None:
        self.db = (
            database
            if isinstance(database, SQLiteDatabase)
            else SQLiteDatabase(database)
        )

    def create(self, entity: CaseModel) -> CaseModel:
        """Insert case."""
        with self.db.connect() as conn:
            try:
                conn.execute(
                    """
                    INSERT INTO cases (
                        case_id, customer_id, created_at, engine_version,
                        input_snapshot_json, calendar_result_json,
                        bazi_result_json, pattern_result_json,
                        score_result_json, interpretation_result_json,
                        report_result_json, narrative_result_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    self._row_params(entity),
                )
                conn.commit()
            except Exception as exc:
                raise ValueError(f"Case already exists: {entity.case_id}") from exc
        return entity

    def get(self, entity_id: str) -> CaseModel | None:
        """Fetch by id."""
        with self.db.connect() as conn:
            row = conn.execute(
                "SELECT * FROM cases WHERE case_id = ?",
                (entity_id,),
            ).fetchone()
        return self._from_row(row) if row else None

    def list(self) -> list[CaseModel]:
        """List newest first."""
        with self.db.connect() as conn:
            rows = conn.execute(
                "SELECT * FROM cases ORDER BY created_at DESC"
            ).fetchall()
        return [self._from_row(row) for row in rows]

    def update(self, entity: CaseModel) -> CaseModel:
        """Replace case."""
        with self.db.connect() as conn:
            cursor = conn.execute(
                """
                UPDATE cases SET
                    customer_id = ?, created_at = ?, engine_version = ?,
                    input_snapshot_json = ?, calendar_result_json = ?,
                    bazi_result_json = ?, pattern_result_json = ?,
                    score_result_json = ?, interpretation_result_json = ?,
                    report_result_json = ?, narrative_result_json = ?
                WHERE case_id = ?
                """,
                (
                    entity.customer_id,
                    entity.created_at,
                    entity.engine_version,
                    *[
                        json.dumps(getattr(entity, name) or {}, ensure_ascii=False)
                        for name in _JSON_FIELDS
                    ],
                    entity.case_id,
                ),
            )
            conn.commit()
            if cursor.rowcount == 0:
                raise KeyError(f"Case not found: {entity.case_id}")
        return entity

    def delete(self, entity_id: str) -> bool:
        """Delete by id."""
        with self.db.connect() as conn:
            cursor = conn.execute(
                "DELETE FROM cases WHERE case_id = ?",
                (entity_id,),
            )
            conn.commit()
            return cursor.rowcount > 0

    def list_by_customer(self, customer_id: str) -> list[CaseModel]:
        """Cases for one customer."""
        with self.db.connect() as conn:
            rows = conn.execute(
                """
                SELECT * FROM cases
                WHERE customer_id = ?
                ORDER BY created_at DESC
                """,
                (customer_id,),
            ).fetchall()
        return [self._from_row(row) for row in rows]

    def search(
        self,
        filters: CaseFilter | None = None,
        *,
        page: Page | None = None,
    ) -> PageResult[CaseModel]:
        """Filter after load for parity with JSON backend."""
        filters = filters or CaseFilter()
        items = [case for case in self.list() if match_case(case, filters)]
        effective = page or Page(page=1, page_size=max(len(items), 1))
        return paginate(items, effective)

    @staticmethod
    def _row_params(entity: CaseModel) -> tuple[Any, ...]:
        return (
            entity.case_id,
            entity.customer_id,
            entity.created_at,
            entity.engine_version,
            *[
                json.dumps(getattr(entity, name) or {}, ensure_ascii=False)
                for name in _JSON_FIELDS
            ],
        )

    @staticmethod
    def _from_row(row: object) -> CaseModel:
        data = dict(row)  # type: ignore[arg-type]
        payload: dict[str, Any] = {
            "case_id": data["case_id"],
            "customer_id": data["customer_id"],
            "created_at": data["created_at"],
            "engine_version": data["engine_version"],
        }
        for name in _JSON_FIELDS:
            payload[name] = json.loads(data.get(f"{name}_json") or "{}")
        return CaseModel.from_dict(payload)
