"""Published Narrative result models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class PublicationNode:
    """One narrative paragraph and its publication decision."""

    node_id: str
    section_id: str
    text: str
    decision: str
    reason: str
    order: int = 0


@dataclass(slots=True)
class EditorialMetrics:
    """Customer-facing publication counts. No engine scores."""

    published_count: int = 0
    dropped_count: int = 0
    appendix_count: int = 0
    word_count: int = 0
    sentence_count: int = 0
    avg_words_per_sentence: float = 0.0
    commercial_score: float = 0.0
    readability: float = 0.0
    customer_relevance: float = 0.0
    leak_hits: int = 0
    within_limits: bool = True
    section_published: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize metrics for metadata and product reports."""
        return {
            "published_count": self.published_count,
            "dropped_count": self.dropped_count,
            "appendix_count": self.appendix_count,
            "word_count": self.word_count,
            "sentence_count": self.sentence_count,
            "avg_words_per_sentence": self.avg_words_per_sentence,
            "commercial_score": self.commercial_score,
            "readability": self.readability,
            "customer_relevance": self.customer_relevance,
            "leak_hits": self.leak_hits,
            "within_limits": self.within_limits,
            "section_published": dict(self.section_published),
        }


@dataclass(slots=True)
class PublishedNarrative:
    """Customer-facing narrative plus the audit of every node decision."""

    sections: list[dict[str, Any]]
    summary: dict[str, Any]
    recommendations: list[dict[str, Any]]
    nodes: tuple[PublicationNode, ...]
    metrics: EditorialMetrics

    def decisions(self) -> list[dict[str, str]]:
        """Decision log without paragraph bodies (bodies stay internal)."""
        return [
            {
                "id": node.node_id,
                "section_id": node.section_id,
                "decision": node.decision,
                "reason": node.reason,
            }
            for node in self.nodes
        ]
