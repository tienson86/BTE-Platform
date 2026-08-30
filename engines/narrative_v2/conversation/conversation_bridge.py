"""Duplicate merge and remainder bridging. Does not invent sentences."""

from __future__ import annotations

from engines.narrative_v2.conversation.conversation_flow import split_sentences


def is_duplicate(left: str | None, right: str | None) -> bool:
    """True when two fields carry identical wording."""
    if left is None or right is None:
        return False
    return left.strip() == right.strip()


def novel_sentences(text: str, already: tuple[str, ...]) -> tuple[str, ...]:
    """Return sentences in text that have not already been spoken."""
    known = set(already)
    return tuple(
        sentence for sentence in split_sentences(text) if sentence not in known
    )
