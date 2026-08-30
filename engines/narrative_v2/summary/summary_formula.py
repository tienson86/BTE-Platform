"""Executive Summary Formula helpers.

Rewrite Units → Insight Selection → Summary Assembly.
Does not invent meaning. Does not join all domains.
"""

from __future__ import annotations

from engines.narrative_v2.summary.summary_model import HEADLINE_WORD_LIMIT

CORE_SEMANTIC_PRIORITY: tuple[str, ...] = (
    "core.pattern_context",
    "core.useful_god_context",
    "core.temperature_balancing_context",
    "core.pattern_ten_gods_relation",
    "core.luck_temporal_context",
)

DOMAIN_PRIORITY: tuple[str, ...] = (
    "pattern",
    "strength",
    "useful_god",
    "temperature",
    "ten_gods",
    "luck",
    "shensha",
)

PERMITTED_JOIN = " "


def split_sentences(text: str) -> tuple[str, ...]:
    """Split a rewrite unit into sentence units. No new wording."""
    parts: list[str] = []
    current: list[str] = []
    for char in text.strip():
        current.append(char)
        if char in ".!?":
            sentence = "".join(current).strip()
            if sentence:
                parts.append(sentence)
            current = []
    tail = "".join(current).strip()
    if tail:
        parts.append(tail)
    return tuple(parts)


def word_count(text: str) -> int:
    """Count whitespace-separated words."""
    return len(text.split())


def headline_from_insight(text: str) -> str | None:
    """Return the first sentence if it is a customer-safe headline."""
    sentences = split_sentences(text)
    if not sentences:
        return None
    first = sentences[0]
    if word_count(first) > HEADLINE_WORD_LIMIT:
        return None
    return first


def join_sentences(sentences: tuple[str, ...]) -> str:
    """Join already-complete sentences. No invented connectors."""
    cleaned = tuple(part.strip() for part in sentences if part.strip())
    return PERMITTED_JOIN.join(cleaned)
