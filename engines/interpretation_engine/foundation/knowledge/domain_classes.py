"""Semantic interpretation classes — Decision, State, Relationship.

Do not merge these classes. They use different reasoning structures.
No additional reasoning class without explicit architectural review.
"""

from __future__ import annotations

from typing import Final

INTERPRETATION_CLASS_DECISION: Final[str] = "decision"
INTERPRETATION_CLASS_STATE: Final[str] = "state"
INTERPRETATION_CLASS_RELATIONSHIP: Final[str] = "relationship"

CANONICAL_REASONING_CLASSES: Final[tuple[str, ...]] = (
    INTERPRETATION_CLASS_DECISION,
    INTERPRETATION_CLASS_STATE,
    INTERPRETATION_CLASS_RELATIONSHIP,
)

DECISION_KNOWLEDGE_DOMAINS: Final[tuple[str, ...]] = ("UsefulGod",)
STATE_KNOWLEDGE_DOMAINS: Final[tuple[str, ...]] = ("Strength",)
RELATIONSHIP_KNOWLEDGE_DOMAINS: Final[tuple[str, ...]] = (
    "Pattern",
    "TenGods",
    "ShenSha",
)


def interpretation_class_for(domain: str) -> str:
    """Return the semantic class for a knowledge domain."""
    if domain in DECISION_KNOWLEDGE_DOMAINS:
        return INTERPRETATION_CLASS_DECISION
    if domain in STATE_KNOWLEDGE_DOMAINS:
        return INTERPRETATION_CLASS_STATE
    if domain in RELATIONSHIP_KNOWLEDGE_DOMAINS:
        return INTERPRETATION_CLASS_RELATIONSHIP
    return ""
