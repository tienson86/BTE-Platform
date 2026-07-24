"""ContentContext — output of the Report Content Analysis Layer (WP7A)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ContentContext:
    """
    Analysis result derived from InterpretationResult.

    Fields
    ------
    section_scores:
        section_id → importance score (0..100).
    important_sections:
        Sections ranked above the importance threshold, high → low.
    keywords:
        Extracted topic keywords with frequencies.
    grouped_rules:
        section_id → list of rule payloads grouped for narrative/report use.
    repeated_topics:
        Topics / keywords that recur across multiple sections.
    suggested_order:
        Recommended section render order after optimization.
    """

    section_scores: dict[str, float] = field(default_factory=dict)
    important_sections: list[str] = field(default_factory=list)
    keywords: list[dict[str, Any]] = field(default_factory=list)
    grouped_rules: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    repeated_topics: list[dict[str, Any]] = field(default_factory=list)
    suggested_order: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize ContentContext for tests / downstream consumers."""
        return {
            "section_scores": dict(self.section_scores),
            "important_sections": list(self.important_sections),
            "keywords": list(self.keywords),
            "grouped_rules": {
                key: [dict(item) for item in value]
                for key, value in self.grouped_rules.items()
            },
            "repeated_topics": list(self.repeated_topics),
            "suggested_order": list(self.suggested_order),
            "metadata": dict(self.metadata),
        }
