"""Interpretation Formula helpers.

Observation → Reasoning → Meaning → Impact → Recommendation → Closing.

Assembles rewrite sentences. Does not invent meaning. Does not concatenate domains.
"""

from __future__ import annotations

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


def join_sentences(sentences: tuple[str, ...]) -> str:
    """Join already-complete sentences. No invented connectors."""
    cleaned = tuple(part.strip() for part in sentences if part.strip())
    return PERMITTED_JOIN.join(cleaned)


def sentence_at(sentences: tuple[str, ...], index: int) -> str | None:
    """Return one rewrite sentence by index, or None."""
    if index < 0 or index >= len(sentences):
        return None
    return sentences[index]
