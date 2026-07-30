"""Search index for Knowledge Records."""

from __future__ import annotations

from services.knowledge.exceptions import KnowledgeQueryError
from services.knowledge.models import KnowledgeRecord, SearchHit


class SearchIndex:
    """Simple substring search over indexed knowledge fields."""

    def __init__(self) -> None:
        """Initialize empty search corpus."""
        self._records: list[KnowledgeRecord] = []

    def build(self, records: list[KnowledgeRecord]) -> SearchIndex:
        """Replace search corpus."""
        self._records = list(records)
        return self

    def search(self, query: str, *, limit: int = 50) -> list[SearchHit]:
        """Case-insensitive substring search."""
        needle = query.strip().lower()
        if not needle:
            raise KnowledgeQueryError("Search query must not be empty")

        hits: list[SearchHit] = []
        for record in self._records:
            identity = record.data.get("identity", {})
            metadata = record.data.get("metadata", {})
            classification = record.data.get("classification", {})
            if not isinstance(identity, dict):
                continue
            haystacks = [
                record.knowledge_id,
                str(identity.get("canonical_name", "")),
                str(identity.get("english_name", "")),
                str(identity.get("chinese", "")),
                str(identity.get("pinyin", "")),
                record.domain_dir,
                str(classification.get("domain", ""))
                if isinstance(classification, dict)
                else "",
                str(classification.get("category", ""))
                if isinstance(classification, dict)
                else "",
                str(record.data.get("definition", "")),
            ]
            aliases = identity.get("aliases", [])
            if isinstance(aliases, list):
                haystacks.extend(str(item) for item in aliases)
            blob = " ".join(haystacks).lower()
            if needle not in blob:
                continue
            score = 2.0 if needle in record.knowledge_id.lower() else 1.0
            if needle == str(identity.get("canonical_name", "")).lower():
                score = 3.0
            hits.append(
                SearchHit(
                    knowledge_id=record.knowledge_id,
                    domain=record.domain_dir,
                    canonical_name=str(identity.get("canonical_name", "")),
                    status=(
                        str(metadata.get("status", ""))
                        if isinstance(metadata, dict)
                        else ""
                    ),
                    score=score,
                    path=record.path,
                )
            )
        hits.sort(key=lambda item: (-item.score, item.knowledge_id))
        return hits[:limit]
