"""Rule search over validation/compiler/rule registry documents."""

from __future__ import annotations

from knowledge.search.matching import contains_match, exact_match, fuzzy_ratio, prefix_match
from knowledge.search.models import SearchDocument, SearchHit


class RuleSearch:
    """Search rule documents."""

    def __init__(self, documents: list[SearchDocument]) -> None:
        """Initialize with rule-kind documents."""
        self.documents = [doc for doc in documents if doc.kind == "rule"]

    def search(
        self,
        query: str,
        *,
        mode: str = "exact",
        limit: int = 50,
        fuzzy_threshold: float = 0.72,
    ) -> list[SearchHit]:
        """Search rules by code/title/text."""
        hits: list[SearchHit] = []
        for doc in self.documents:
            score = 0.0
            match_type = mode
            fields = [doc.doc_id, doc.canonical_name, doc.text, *doc.aliases]
            for field in fields:
                if not field:
                    continue
                if mode == "exact" and exact_match(query, field):
                    score = max(score, 3.0)
                    match_type = "exact"
                elif mode == "prefix" and prefix_match(query, field):
                    score = max(score, 2.0)
                    match_type = "prefix"
                elif mode == "fuzzy":
                    ratio = fuzzy_ratio(query, field)
                    if ratio >= fuzzy_threshold:
                        score = max(score, ratio)
                        match_type = "fuzzy"
                elif contains_match(query, field):
                    score = max(score, 1.4)
                    match_type = "contains"
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
