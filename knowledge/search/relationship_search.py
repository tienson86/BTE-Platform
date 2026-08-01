"""Relationship search over relationship documents and edges."""

from __future__ import annotations

from knowledge.search.matching import contains_match, exact_match, prefix_match
from knowledge.search.models import SearchDocument, SearchHit


class RelationshipSearch:
    """Search relationship records and ontology relationship types."""

    def __init__(self, documents: list[SearchDocument]) -> None:
        """Initialize with relationship-kind documents."""
        self.documents = [doc for doc in documents if doc.kind == "relationship"]

    def search(
        self,
        query: str,
        *,
        mode: str = "relationship",
        limit: int = 50,
    ) -> list[SearchHit]:
        """Search relationships by id/name/type."""
        hits: list[SearchHit] = []
        for doc in self.documents:
            score = 0.0
            match_type = mode
            fields = [doc.doc_id, doc.canonical_name, doc.category, doc.text, *doc.aliases]
            for field in fields:
                if not field:
                    continue
                if mode == "exact" and exact_match(query, field):
                    score = max(score, 3.0)
                    match_type = "exact"
                elif mode == "prefix" and prefix_match(query, field):
                    score = max(score, 2.0)
                    match_type = "prefix"
                elif contains_match(query, field):
                    score = max(score, 1.5)
                    match_type = "relationship"
            if score <= 0:
                continue
            hits.append(
                SearchHit(
                    doc_id=doc.doc_id,
                    kind=doc.kind,
                    canonical_name=doc.canonical_name,
                    score=score,
                    match_type=match_type,
                    path=doc.path,
                    category=doc.category,
                    snippet=doc.text or doc.canonical_name,
                )
            )
        hits.sort(key=lambda item: (-item.score, item.doc_id))
        return hits[:limit]
