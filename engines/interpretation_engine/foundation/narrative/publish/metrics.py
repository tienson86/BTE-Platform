"""Editorial metrics for the published narrative. Not engine scores."""

from __future__ import annotations

from typing import Any

from engines.interpretation_engine.foundation.narrative.publish.constants import (
    DECISION_APPENDIX,
    DECISION_DROP,
    DECISION_PUBLISH,
    SECTION_LIMITS,
)
from engines.interpretation_engine.foundation.narrative.publish.criteria import (
    engine_language_hits,
    sentence_count,
    thesis_overlap,
    word_count,
)
from engines.interpretation_engine.foundation.narrative.publish.models import (
    EditorialMetrics,
    PublicationNode,
)


def build_editorial_metrics(
    nodes: list[PublicationNode],
    thesis: dict[str, Any] | None,
) -> EditorialMetrics:
    """Count publication outcomes and score commercial customer value."""
    published = [node for node in nodes if node.decision == DECISION_PUBLISH]
    dropped = [node for node in nodes if node.decision == DECISION_DROP]
    appendix = [node for node in nodes if node.decision == DECISION_APPENDIX]
    blob = " ".join(node.text for node in published)
    words = word_count(blob)
    sentences = sum(sentence_count(node.text) for node in published) or 1
    avg = words / sentences if sentences else 0.0
    leak_hits = sum(1 for node in published if engine_language_hits(node.text))
    section_published = {
        section_id: sum(1 for node in published if node.section_id == section_id)
        for section_id in SECTION_LIMITS
    }
    within_limits = all(
        section_published[section_id] <= limit
        for section_id, limit in SECTION_LIMITS.items()
    )
    total = max(len(nodes), 1)
    return EditorialMetrics(
        published_count=len(published),
        dropped_count=len(dropped),
        appendix_count=len(appendix),
        word_count=words,
        sentence_count=sentences,
        avg_words_per_sentence=round(avg, 2),
        commercial_score=_commercial_score(
            leak_hits=leak_hits,
            within_limits=within_limits,
            blob=blob,
            thesis=thesis,
            recs=section_published["sec-recommendation"],
            impact=section_published["sec-impact"],
            exec_count=section_published["sec-executive_summary"],
        ),
        readability=_readability(avg),
        customer_relevance=round(len(published) / total, 3),
        leak_hits=leak_hits,
        within_limits=within_limits,
        section_published=section_published,
    )


def _readability(avg_words: float) -> float:
    """Simple consulting readability: prefer 8–22 words per sentence."""
    if avg_words <= 0:
        return 0.0
    if 8 <= avg_words <= 22:
        return 100.0
    if avg_words < 8:
        return round(max(40.0, avg_words / 8 * 100), 1)
    return round(max(40.0, 100 - (avg_words - 22) * 3), 1)


def _commercial_score(
    *,
    leak_hits: int,
    within_limits: bool,
    blob: str,
    thesis: dict[str, Any] | None,
    recs: int,
    impact: int,
    exec_count: int,
) -> float:
    """Clarity and customer value, not knowledge completeness."""
    score = 0.0
    score += 25.0 if leak_hits == 0 else 0.0
    score += 25.0 if within_limits else 10.0
    score += 20.0 if thesis_overlap(blob, thesis) or exec_count >= 1 else 0.0
    score += 15.0 if 1 <= recs <= 5 else 5.0
    score += 15.0 if impact >= 1 else 0.0
    return round(score, 1)
