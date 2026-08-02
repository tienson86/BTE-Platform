"""Indexed repository over loaded knowledge records."""

from __future__ import annotations

from collections import defaultdict

from engines.knowledge_engine.loader import KnowledgeLoader
from engines.knowledge_engine.models import KnowledgeRecord


class KnowledgeRepository:
    """In-memory index for knowledge lookup by id, topic, and keyword.

    Loading and indexing only — no reasoning.
    """

    def __init__(self, loader: KnowledgeLoader | None = None) -> None:
        """Create a repository backed by a knowledge loader.

        Args:
            loader: Optional loader. Defaults to ``KnowledgeLoader()``.
        """
        self._loader = loader or KnowledgeLoader()
        self._records: list[KnowledgeRecord] = []
        self._by_id: dict[str, KnowledgeRecord] = {}
        self._by_topic: dict[str, list[KnowledgeRecord]] = defaultdict(list)
        self._by_keyword: dict[str, list[KnowledgeRecord]] = defaultdict(list)
        self._indexed = False

    @property
    def loader(self) -> KnowledgeLoader:
        """Return the bound loader."""
        return self._loader

    def load(self) -> KnowledgeRepository:
        """Load all CSVs via the loader and rebuild indexes.

        Returns:
            ``self`` for fluent chaining.
        """
        records = self._loader.load_all()
        self._build_indexes(records)
        return self

    def reload(self) -> KnowledgeRepository:
        """Clear loader cache, reload CSVs, and rebuild indexes."""
        self._loader.clear_cache()
        self._indexed = False
        return self.load()

    def is_indexed(self) -> bool:
        """Return True when indexes have been built."""
        return self._indexed

    def all(self) -> list[KnowledgeRecord]:
        """Return all loaded records (ensures load)."""
        self._ensure_indexed()
        return list(self._records)

    def count(self) -> int:
        """Return number of indexed records."""
        self._ensure_indexed()
        return len(self._records)

    def get_by_id(self, record_id: str) -> KnowledgeRecord | None:
        """Return a record by exact id, or ``None`` if missing."""
        self._ensure_indexed()
        key = str(record_id or "").strip()
        if not key:
            return None
        return self._by_id.get(key)

    def find_by_topic(self, topic: str, *, exact: bool = False) -> list[KnowledgeRecord]:
        """Find records matching a topic.

        Args:
            topic: Topic query.
            exact: When True, require case-insensitive exact topic equality.
                When False, also match topic substrings.

        Returns:
            Matching records sorted by priority desc, then id.
        """
        self._ensure_indexed()
        query = str(topic or "").strip().lower()
        if not query:
            return []

        if exact:
            matches = list(self._by_topic.get(query, []))
        else:
            matches = []
            seen: set[str] = set()
            for key, rows in self._by_topic.items():
                if query == key or query in key or key in query:
                    for row in rows:
                        if row.id not in seen:
                            seen.add(row.id)
                            matches.append(row)
        return self._sort(matches)

    def find_by_keyword(self, keyword: str) -> list[KnowledgeRecord]:
        """Find records whose keyword tokens contain the query (case-insensitive).

        Also matches when the query appears as a substring of the raw keyword field.
        """
        self._ensure_indexed()
        query = str(keyword or "").strip().lower()
        if not query:
            return []

        matches: list[KnowledgeRecord] = []
        seen: set[str] = set()

        for token, rows in self._by_keyword.items():
            if query == token or query in token or token in query:
                for row in rows:
                    if row.id not in seen:
                        seen.add(row.id)
                        matches.append(row)

        for row in self._records:
            if row.id in seen:
                continue
            if query in (row.keyword or "").lower():
                seen.add(row.id)
                matches.append(row)

        return self._sort(matches)

    def search(
        self,
        *,
        record_id: str | None = None,
        topic: str | None = None,
        keyword: str | None = None,
    ) -> list[KnowledgeRecord]:
        """Search by id and/or topic and/or keyword.

        When multiple filters are provided, results are the intersection.
        When only ``record_id`` is provided, returns a 0–1 element list.
        """
        self._ensure_indexed()

        if record_id is not None and str(record_id).strip():
            found = self.get_by_id(record_id)
            candidates = [found] if found else []
        else:
            candidates = list(self._records)

        if topic is not None and str(topic).strip():
            topic_ids = {row.id for row in self.find_by_topic(topic)}
            candidates = [row for row in candidates if row.id in topic_ids]

        if keyword is not None and str(keyword).strip():
            keyword_ids = {row.id for row in self.find_by_keyword(keyword)}
            candidates = [row for row in candidates if row.id in keyword_ids]

        return self._sort(candidates)

    def _ensure_indexed(self) -> None:
        if not self._indexed:
            self.load()

    def _build_indexes(self, records: list[KnowledgeRecord]) -> None:
        self._records = list(records)
        self._by_id = {}
        self._by_topic = defaultdict(list)
        self._by_keyword = defaultdict(list)

        for record in self._records:
            self._by_id[record.id] = record
            topic_key = (record.topic or "").strip().lower()
            if topic_key:
                self._by_topic[topic_key].append(record)
            for token in record.keyword_tokens():
                self._by_keyword[token].append(record)

        self._indexed = True

    def _sort(self, records: list[KnowledgeRecord]) -> list[KnowledgeRecord]:
        return sorted(records, key=lambda row: (-row.priority, row.id))
