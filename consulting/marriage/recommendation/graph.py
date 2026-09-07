"""Recommendation graph helpers. Deterministic, acyclic, no orphans."""

from __future__ import annotations

from consulting.marriage.exceptions import MarriageRecommendationError
from consulting.marriage.models.enums import RecommendationType
from consulting.marriage.models.recommendation import MarriageRecommendation


def apply_dependencies(recommendations: list[MarriageRecommendation]) -> None:
    """Attach explicit finance dependencies. Do not invent long chains."""
    conflict_ids = [
        item.recommendation_id
        for item in recommendations
        if item.action_type is RecommendationType.REDUCE_CONFLICT
    ]
    role_ids = [
        item.recommendation_id
        for item in recommendations
        if item.action_type is RecommendationType.ROLE_BALANCE
    ]
    for item in recommendations:
        if item.action_type is not RecommendationType.FINANCIAL_STRUCTURE:
            continue
        item.depends_on = sorted({*conflict_ids, *role_ids})


def assert_graph(recommendations: list[MarriageRecommendation]) -> None:
    """Reject missing dependency targets and cycles."""
    ids = {item.recommendation_id for item in recommendations}
    for item in recommendations:
        if not item.source_finding_ids:
            raise MarriageRecommendationError(f"orphan_recommendation:{item.recommendation_id}")
        for dep in item.depends_on:
            if dep not in ids:
                raise MarriageRecommendationError(f"orphan_dependency:{item.recommendation_id}:{dep}")
    _assert_acyclic(recommendations)


def _assert_acyclic(recommendations: list[MarriageRecommendation]) -> None:
    """Fail when the recommendation graph contains a cycle."""
    edges = {item.recommendation_id: list(item.depends_on) for item in recommendations}
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visited:
            return
        if node in visiting:
            raise MarriageRecommendationError(f"recommendation_cycle:{node}")
        visiting.add(node)
        for nxt in edges.get(node, ()):
            visit(nxt)
        visiting.remove(node)
        visited.add(node)

    for rec_id in sorted(edges):
        visit(rec_id)
