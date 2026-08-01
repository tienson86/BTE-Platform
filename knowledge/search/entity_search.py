"""Entity search over Knowledge Record and ontology entity documents."""

from __future__ import annotations

from knowledge.search.matching import (
    contains_match,
    exact_match,
    fuzzy_ratio,
    prefix_match,
)
from knowledge.search.models import SearchDocument, SearchHit


class EntitySearch:
    """Search entities (KR concepts and ontology entity types)."""

    def __init__(self, documents: list[SearchDocument]) -> None:
        """Initialize with entity documents only."""
        self.documents = [
            doc for doc in documents if doc.kind in {"entity", "concept", "ontology_entity"}
        ]

    def search(
        self,
        query: str,
        *,
        mode: str = "exact",
        limit: int = 50,
        fuzzy_threshold: float = 0.72,
    ) -> list[SearchHit]:
        """Search entities by mode."""
        hits: list[SearchHit] = []
        for doc in self.documents:
            score, match_type = _score_document(
                query, doc, mode=mode, fuzzy_threshold=fuzzy_threshold
            )
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
                    snippet=doc.canonical_name,
                )
            )
        hits.sort(key=lambda item: (-item.score, item.doc_id))
        return hits[:limit]


def _score_document(
    query: str,
    doc: SearchDocument,
    *,
    mode: str,
    fuzzy_threshold: float,
) -> tuple[float, str]:
    candidates = [doc.doc_id, doc.canonical_name, *doc.aliases, doc.text]
    best = 0.0
    match_type = mode
    for candidate in candidates:
        if not candidate:
            continue
        if mode == "exact" and exact_match(query, candidate):
            best = max(best, 3.0 if exact_match(query, doc.doc_id) else 2.5)
            match_type = "exact"
        elif mode == "prefix" and prefix_match(query, candidate):
            best = max(best, 2.0)
            match_type = "prefix"
        elif mode in {"contains", "relationship", "dependency", "ontology"} and contains_match(
            query, candidate
        ):
            best = max(best, 1.5)
            match_type = "contains"
        elif mode == "fuzzy":
            ratio = fuzzy_ratio(query, candidate)
            if ratio >= fuzzy_threshold:
                best = max(best, ratio)
                match_type = "fuzzy"
    return best, match_type
