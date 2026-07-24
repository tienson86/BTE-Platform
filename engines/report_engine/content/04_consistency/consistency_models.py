"""Consistency Layer models (WP7D)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ConsistencyIssue:
    """One consistency finding."""

    kind: str
    detail: str
    paragraph_id: str = ""
    section: str = ""
    action: str = "warn"
    related_paragraph_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize issue."""
        return {
            "kind": self.kind,
            "detail": self.detail,
            "paragraph_id": self.paragraph_id,
            "section": self.section,
            "action": self.action,
            "related_paragraph_id": self.related_paragraph_id,
        }


@dataclass(slots=True)
class ConsistentParagraphContext:
    """
    WP7D output from StyledParagraphContext.

    checked_paragraphs:
        Paragraphs retained after consistency checks (content unchanged).
    removed_duplicates:
        Texts removed as duplicates.
    contradiction_report:
        Contradiction findings (resolved by keeping higher score).
    coherence_report:
        Coherence findings / warnings.
    warnings:
        Aggregated non-fatal warnings.
    """

    checked_paragraphs: list[Any] = field(default_factory=list)
    removed_duplicates: list[str] = field(default_factory=list)
    contradiction_report: list[dict[str, Any]] = field(default_factory=list)
    coherence_report: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    tone: str = "neutral"
    emphasis_levels: dict[str, str] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize ConsistentParagraphContext."""
        paragraphs = []
        for item in self.checked_paragraphs:
            if hasattr(item, "to_dict"):
                paragraphs.append(item.to_dict())
            else:
                paragraphs.append(item)
        return {
            "checked_paragraphs": paragraphs,
            "removed_duplicates": list(self.removed_duplicates),
            "contradiction_report": list(self.contradiction_report),
            "coherence_report": list(self.coherence_report),
            "warnings": list(self.warnings),
            "tone": self.tone,
            "emphasis_levels": dict(self.emphasis_levels),
            "metadata": dict(self.metadata),
        }
