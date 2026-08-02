"""Read-only loader for classical knowledge CSVs (``database/20_knowledge``)."""

from __future__ import annotations

import csv
import logging
from pathlib import Path

from engines.knowledge_engine.exceptions import KnowledgeLoadError, KnowledgeSchemaError
from engines.knowledge_engine.models import (
    KNOWLEDGE_FILES,
    REQUIRED_COLUMNS,
    KnowledgeRecord,
)

logger = logging.getLogger(__name__)

_REPO_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_DB = _REPO_ROOT / "database" / "20_knowledge"


class KnowledgeLoader:
    """Load, validate, and cache knowledge CSV records.

    Responsibilities:
    - read all topic CSVs
    - validate stable schema
    - cache parsed ``KnowledgeRecord`` lists per file
    - reject duplicate ids across the corpus

    Does not perform reasoning or retrieval ranking beyond load/index support.
    """

    def __init__(self, database_path: str | Path | None = None) -> None:
        """Create a loader bound to a knowledge database directory.

        Args:
            database_path: Path to ``database/20_knowledge``. Defaults to repo path.
        """
        self.database_path = Path(database_path) if database_path else _DEFAULT_DB
        self._file_cache: dict[str, list[KnowledgeRecord]] = {}
        self._all_cache: list[KnowledgeRecord] | None = None

    def load_all(self) -> list[KnowledgeRecord]:
        """Load every knowledge CSV, validate schema, and return all records.

        Returns:
            Cached list of ``KnowledgeRecord`` (may be empty when schema-only).

        Raises:
            KnowledgeLoadError: Missing directory or required file.
            KnowledgeSchemaError: Invalid header, empty id, bad types, or duplicate id.
        """
        if self._all_cache is not None:
            return list(self._all_cache)

        if not self.database_path.exists():
            raise KnowledgeLoadError(f"Knowledge database not found: {self.database_path}")
        if not self.database_path.is_dir():
            raise KnowledgeLoadError(f"Knowledge database path is not a directory: {self.database_path}")

        records: list[KnowledgeRecord] = []
        seen_ids: dict[str, str] = {}
        for filename in KNOWLEDGE_FILES:
            file_records = self.load_file(filename)
            for record in file_records:
                prior = seen_ids.get(record.id)
                if prior is not None:
                    raise KnowledgeSchemaError(
                        f"Duplicate knowledge id '{record.id}' in {filename} "
                        f"(already defined in {prior})"
                    )
                seen_ids[record.id] = filename
            records.extend(file_records)

        self._all_cache = records
        logger.debug(
            "Loaded %s knowledge records from %s",
            len(records),
            self.database_path,
        )
        return list(records)

    def load_file(self, filename: str) -> list[KnowledgeRecord]:
        """Load and validate a single knowledge CSV (cached).

        Args:
            filename: CSV basename under the knowledge database directory.

        Returns:
            List of records for that file (empty list allowed).

        Raises:
            KnowledgeLoadError: File missing or unreadable.
            KnowledgeSchemaError: Schema or row validation failure.
        """
        if filename in self._file_cache:
            return list(self._file_cache[filename])

        path = self.database_path / filename
        if not path.exists():
            raise KnowledgeLoadError(f"Knowledge CSV not found: {path}")

        try:
            with path.open("r", encoding="utf-8", newline="") as handle:
                reader = csv.DictReader(handle)
                self._validate_schema(reader.fieldnames, filename)
                rows = list(reader)
        except OSError as exc:
            raise KnowledgeLoadError(f"Failed to read knowledge CSV: {path}") from exc

        records: list[KnowledgeRecord] = []
        for index, row in enumerate(rows, start=2):
            if self._row_is_blank(row):
                continue
            records.append(self._parse_row(row, filename=filename, line_no=index))

        self._file_cache[filename] = records
        return list(records)

    def clear_cache(self) -> None:
        """Clear file and full-corpus caches."""
        self._file_cache.clear()
        self._all_cache = None

    def cache_size(self) -> int:
        """Return number of cached files."""
        return len(self._file_cache)

    def is_loaded(self) -> bool:
        """Return True when ``load_all`` has populated the full corpus cache."""
        return self._all_cache is not None

    def expected_files(self) -> tuple[str, ...]:
        """Return the canonical knowledge CSV filenames."""
        return KNOWLEDGE_FILES

    def _validate_schema(self, fieldnames: list[str] | None, filename: str) -> None:
        if not fieldnames:
            raise KnowledgeSchemaError(f"Missing header in {filename}")
        normalized = [name.strip() for name in fieldnames if name is not None]
        if tuple(normalized) != REQUIRED_COLUMNS:
            raise KnowledgeSchemaError(
                f"Invalid schema in {filename}: expected {list(REQUIRED_COLUMNS)}, "
                f"got {normalized}"
            )

    def _row_is_blank(self, row: dict[str, str | None]) -> bool:
        return all(not str(value or "").strip() for value in row.values())

    def _parse_row(
        self,
        row: dict[str, str | None],
        *,
        filename: str,
        line_no: int,
    ) -> KnowledgeRecord:
        record_id = str(row.get("id") or "").strip()
        if not record_id:
            raise KnowledgeSchemaError(f"Empty id in {filename} line {line_no}")

        priority_raw = str(row.get("priority") or "").strip()
        confidence_raw = str(row.get("confidence") or "").strip()
        try:
            priority = int(priority_raw) if priority_raw else 0
        except ValueError as exc:
            raise KnowledgeSchemaError(
                f"Invalid priority in {filename} line {line_no}: {priority_raw!r}"
            ) from exc
        try:
            confidence = float(confidence_raw) if confidence_raw else 0.0
        except ValueError as exc:
            raise KnowledgeSchemaError(
                f"Invalid confidence in {filename} line {line_no}: {confidence_raw!r}"
            ) from exc

        if confidence < 0.0 or confidence > 1.0:
            raise KnowledgeSchemaError(
                f"Confidence out of range in {filename} line {line_no}: {confidence}"
            )

        return KnowledgeRecord(
            id=record_id,
            topic=str(row.get("topic") or "").strip(),
            keyword=str(row.get("keyword") or "").strip(),
            condition=str(row.get("condition") or "").strip(),
            classical_text=str(row.get("classical_text") or "").strip(),
            modern_interpretation=str(row.get("modern_interpretation") or "").strip(),
            priority=priority,
            confidence=confidence,
            reference=str(row.get("reference") or "").strip(),
            source_file=filename,
        )
