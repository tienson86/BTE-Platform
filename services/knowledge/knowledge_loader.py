"""Facade Knowledge Loader orchestrating schema/record/dependency loaders."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from services.knowledge.constants import (
    DEFAULT_CANON_ROOT_RELATIVE,
    DEFAULT_SCHEMA_ROOT_RELATIVE,
)
from services.knowledge.dependency_loader import DependencyLoader
from services.knowledge.models import KnowledgeRecord, KnowledgeStats, SchemaDocument
from services.knowledge.record_loader import RecordLoader
from services.knowledge.schema_loader import SchemaLoader

logger = logging.getLogger(__name__)


class KnowledgeLoader:
    """High-level loader for Knowledge Canon infrastructure."""

    def __init__(
        self,
        *,
        project_root: str | Path | None = None,
        canon_root: str | Path | None = None,
        schema_root: str | Path | None = None,
    ) -> None:
        """Initialize loader with optional explicit roots."""
        self.project_root = (
            Path(project_root).resolve()
            if project_root is not None
            else Path.cwd().resolve()
        )
        self.canon_root = (
            Path(canon_root).resolve()
            if canon_root is not None
            else (self.project_root / DEFAULT_CANON_ROOT_RELATIVE).resolve()
        )
        self.schema_root = (
            Path(schema_root).resolve()
            if schema_root is not None
            else (self.project_root / DEFAULT_SCHEMA_ROOT_RELATIVE).resolve()
        )
        self.schema_loader = SchemaLoader(self.schema_root)
        self.record_loader = RecordLoader(self.canon_root)
        self.dependency_loader = DependencyLoader()

    def clear_cache(self) -> None:
        """Clear all nested caches."""
        self.schema_loader.clear_cache()
        self.record_loader.clear_cache()

    def load_schemas(self) -> list[SchemaDocument]:
        """Load all foundation schemas."""
        return self.schema_loader.load_all()

    def load_records(self, domain_dir: str | None = None) -> list[KnowledgeRecord]:
        """Load knowledge records, optionally filtered by domain directory."""
        if domain_dir:
            return self.record_loader.load_domain(domain_dir)
        return self.record_loader.load_all()

    def load_dependencies(
        self,
        records: list[KnowledgeRecord] | None = None,
    ) -> dict[str, list[str]]:
        """Load dependency adjacency from records."""
        payload = records if records is not None else self.load_records()
        return self.dependency_loader.load_edges(payload)

    def get_record(self, knowledge_id: str) -> KnowledgeRecord | None:
        """Return a record by knowledge_id."""
        for record in self.load_records():
            if record.knowledge_id == knowledge_id:
                return record
        return None

    def stats(self, records: list[KnowledgeRecord] | None = None) -> KnowledgeStats:
        """Compute aggregate statistics."""
        payload = records if records is not None else self.load_records()
        by_domain: dict[str, int] = {}
        by_status: dict[str, int] = {}
        for record in payload:
            by_domain[record.domain_dir] = by_domain.get(record.domain_dir, 0) + 1
            metadata = record.data.get("metadata", {})
            status = (
                str(metadata.get("status", ""))
                if isinstance(metadata, dict)
                else ""
            )
            if status:
                by_status[status] = by_status.get(status, 0) + 1
        return KnowledgeStats(
            total_records=len(payload),
            by_domain=by_domain,
            by_status=by_status,
            schema_count=len(self.load_schemas()),
            generated_at=datetime.now(timezone.utc).isoformat(),
        )

    def export_bundle(
        self,
        records: list[KnowledgeRecord] | None = None,
    ) -> dict[str, Any]:
        """Build an in-memory export bundle (no writes)."""
        payload = records if records is not None else self.load_records()
        return {
            "version": "1.1.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "schema_root": str(self.schema_root),
            "canon_root": str(self.canon_root),
            "records": [
                {
                    "knowledge_id": record.knowledge_id,
                    "domain_dir": record.domain_dir,
                    "schema_name": record.schema_name,
                    "path": record.path,
                    "data": record.data,
                }
                for record in payload
            ],
            "dependencies": self.load_dependencies(payload),
        }
