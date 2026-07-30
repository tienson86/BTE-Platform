"""Primary Knowledge Index over loaded records."""

from __future__ import annotations

from services.knowledge.models import KnowledgeRecord


class KnowledgeIndex:
    """In-memory index of knowledge records by common keys."""

    def __init__(self) -> None:
        """Initialize empty index."""
        self.by_id: dict[str, KnowledgeRecord] = {}
        self.by_domain: dict[str, list[str]] = {}
        self.by_status: dict[str, list[str]] = {}
        self.by_canonical_name: dict[str, list[str]] = {}

    def clear(self) -> None:
        """Reset all index maps."""
        self.by_id.clear()
        self.by_domain.clear()
        self.by_status.clear()
        self.by_canonical_name.clear()

    def build(self, records: list[KnowledgeRecord]) -> KnowledgeIndex:
        """Rebuild indexes from records."""
        self.clear()
        for record in records:
            if not record.knowledge_id:
                continue
            self.by_id[record.knowledge_id] = record
            self.by_domain.setdefault(record.domain_dir, []).append(record.knowledge_id)
            metadata = record.data.get("metadata", {})
            status = (
                str(metadata.get("status", ""))
                if isinstance(metadata, dict)
                else ""
            )
            if status:
                self.by_status.setdefault(status, []).append(record.knowledge_id)
            identity = record.data.get("identity", {})
            name = (
                str(identity.get("canonical_name", "")).strip().lower()
                if isinstance(identity, dict)
                else ""
            )
            if name:
                self.by_canonical_name.setdefault(name, []).append(record.knowledge_id)
        return self

    def get(self, knowledge_id: str) -> KnowledgeRecord | None:
        """Lookup by knowledge_id."""
        return self.by_id.get(knowledge_id)

    def list_ids(
        self,
        *,
        domain_dir: str | None = None,
        status: str | None = None,
    ) -> list[str]:
        """List knowledge IDs with optional filters."""
        ids = list(self.by_id.keys())
        if domain_dir:
            allowed = set(self.by_domain.get(domain_dir, []))
            ids = [item for item in ids if item in allowed]
        if status:
            allowed = set(self.by_status.get(status, []))
            ids = [item for item in ids if item in allowed]
        return sorted(ids)
