"""Language asset status model."""

from __future__ import annotations

STATUS_DRAFT = "draft"
STATUS_REVIEW = "review"
STATUS_APPROVED = "approved"
STATUS_DEPRECATED = "deprecated"

CUSTOMER_ELIGIBLE = frozenset({STATUS_APPROVED})

SENTENCE_LIBRARY_VERSION = "1.0.0"

CATEGORIES: tuple[str, ...] = (
    "headline",
    "observation",
    "reasoning",
    "meaning",
    "impact",
    "recommendation",
    "transition",
    "closing",
    "decision",
    "action",
    "warning",
)

MEANING_CATEGORIES: frozenset[str] = frozenset(
    {
        "headline",
        "observation",
        "reasoning",
        "meaning",
        "impact",
        "recommendation",
        "transition",
        "closing",
    }
)

TASK_CATEGORIES: frozenset[str] = frozenset({"decision", "action", "warning"})
