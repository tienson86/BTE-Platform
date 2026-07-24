"""SQLite CustomerRepository (stdlib sqlite3)."""

from __future__ import annotations

import json
from pathlib import Path

from applications.customer.models import CustomerModel
from applications.storage.interfaces.customer_repository import CustomerRepository
from applications.storage.interfaces.repository import (
    CustomerFilter,
    Page,
    PageResult,
    paginate,
)
from applications.storage.json._filters import match_customer
from applications.storage.sqlite.database import SQLiteDatabase


class SQLiteCustomerRepository(CustomerRepository):
    """Customer CRUD / search on SQLite."""

    def __init__(self, database: SQLiteDatabase | Path | str) -> None:
        self.db = (
            database
            if isinstance(database, SQLiteDatabase)
            else SQLiteDatabase(database)
        )

    def create(self, entity: CustomerModel) -> CustomerModel:
        """Insert customer."""
        with self.db.connect() as conn:
            try:
                conn.execute(
                    """
                    INSERT INTO customers (
                        customer_id, full_name, gender, birth_datetime,
                        timezone, language, phone, email, notes, tags_json,
                        created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    self._row_params(entity),
                )
                conn.commit()
            except Exception as exc:
                raise ValueError(
                    f"Customer already exists: {entity.customer_id}"
                ) from exc
        return entity

    def get(self, entity_id: str) -> CustomerModel | None:
        """Fetch by id."""
        with self.db.connect() as conn:
            row = conn.execute(
                "SELECT * FROM customers WHERE customer_id = ?",
                (entity_id,),
            ).fetchone()
        return self._from_row(row) if row else None

    def list(self) -> list[CustomerModel]:
        """List newest first."""
        with self.db.connect() as conn:
            rows = conn.execute(
                "SELECT * FROM customers ORDER BY created_at DESC"
            ).fetchall()
        return [self._from_row(row) for row in rows]

    def update(self, entity: CustomerModel) -> CustomerModel:
        """Replace customer."""
        entity.touch()
        with self.db.connect() as conn:
            cursor = conn.execute(
                """
                UPDATE customers SET
                    full_name = ?, gender = ?, birth_datetime = ?,
                    timezone = ?, language = ?, phone = ?, email = ?,
                    notes = ?, tags_json = ?, created_at = ?, updated_at = ?
                WHERE customer_id = ?
                """,
                (
                    entity.full_name,
                    entity.gender,
                    entity.birth_datetime,
                    entity.timezone,
                    entity.language,
                    entity.phone,
                    entity.email,
                    entity.notes,
                    json.dumps(entity.tags, ensure_ascii=False),
                    entity.created_at,
                    entity.updated_at,
                    entity.customer_id,
                ),
            )
            conn.commit()
            if cursor.rowcount == 0:
                raise KeyError(f"Customer not found: {entity.customer_id}")
        return entity

    def delete(self, entity_id: str) -> bool:
        """Delete by id."""
        with self.db.connect() as conn:
            cursor = conn.execute(
                "DELETE FROM customers WHERE customer_id = ?",
                (entity_id,),
            )
            conn.commit()
            return cursor.rowcount > 0

    def search(
        self,
        filters: CustomerFilter | None = None,
        *,
        page: Page | None = None,
    ) -> PageResult[CustomerModel]:
        """Filter in Python after load (keeps parity with JSON backend)."""
        filters = filters or CustomerFilter()
        items = [c for c in self.list() if match_customer(c, filters)]
        effective = page or Page(page=1, page_size=max(len(items), 1))
        return paginate(items, effective)

    @staticmethod
    def _row_params(entity: CustomerModel) -> tuple:
        return (
            entity.customer_id,
            entity.full_name,
            entity.gender,
            entity.birth_datetime,
            entity.timezone,
            entity.language,
            entity.phone,
            entity.email,
            entity.notes,
            json.dumps(entity.tags, ensure_ascii=False),
            entity.created_at,
            entity.updated_at,
        )

    @staticmethod
    def _from_row(row: object) -> CustomerModel:
        data = dict(row)  # type: ignore[arg-type]
        tags = json.loads(data.pop("tags_json") or "[]")
        data["tags"] = tags
        return CustomerModel.from_dict(data)
