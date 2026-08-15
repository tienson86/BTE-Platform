"""Semantic interpretation classes — Decision vs State.

Do not merge these classes. They use different reasoning structures.
"""

from __future__ import annotations

from typing import Final

INTERPRETATION_CLASS_DECISION: Final[str] = "decision"
INTERPRETATION_CLASS_STATE: Final[str] = "state"

DECISION_KNOWLEDGE_DOMAINS: Final[tuple[str, ...]] = ("UsefulGod",)
STATE_KNOWLEDGE_DOMAINS: Final[tuple[str, ...]] = ("Strength",)


def interpretation_class_for(domain: str) -> str:
    """Return the semantic class for a knowledge domain."""
    if domain in DECISION_KNOWLEDGE_DOMAINS:
        return INTERPRETATION_CLASS_DECISION
    if domain in STATE_KNOWLEDGE_DOMAINS:
        return INTERPRETATION_CLASS_STATE
    return ""
