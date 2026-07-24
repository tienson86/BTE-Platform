"""Narrative Engine data models (WP7)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now() -> datetime:
    """Timezone-aware UTC timestamp."""
    return datetime.now(timezone.utc)


@dataclass(slots=True)
class NarrativeUnit:
    """One atomic narrative sentence/clause before paragraph assembly."""

    text: str
    section_id: str
    section_title: str = ""
    tone: str = "neutral"
    intent: str = "describe"
    priority: float = 0.0
    source: str = ""
    rule_id: str = ""
    is_transition: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Serialize unit."""
        return {
            "text": self.text,
            "section_id": self.section_id,
            "section_title": self.section_title,
            "tone": self.tone,
            "intent": self.intent,
            "priority": self.priority,
            "source": self.source,
            "rule_id": self.rule_id,
            "is_transition": self.is_transition,
        }


@dataclass(slots=True)
class NarrativeParagraph:
    """Coherent paragraph for one section (or transition bridge)."""

    section_id: str
    section_title: str
    text: str
    tone: str = "neutral"
    unit_count: int = 0
    is_transition: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Serialize paragraph."""
        return {
            "section_id": self.section_id,
            "section_title": self.section_title,
            "text": self.text,
            "tone": self.tone,
            "unit_count": self.unit_count,
            "is_transition": self.is_transition,
        }


@dataclass(slots=True)
class NarrativeIssue:
    """Issue found/fixed during narrative processing."""

    kind: str
    detail: str
    section_id: str = ""
    action: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize issue."""
        return {
            "kind": self.kind,
            "detail": self.detail,
            "section_id": self.section_id,
            "action": self.action,
        }


@dataclass(slots=True)
class NarrativeReport:
    """
    WP7 output: polished narrative ready for HTML / Markdown / PDF.
    """

    title: str = ""
    paragraphs: list[NarrativeParagraph] = field(default_factory=list)
    sections: list[dict[str, Any]] = field(default_factory=list)
    html: str = ""
    markdown: str = ""
    pdf_path: str = ""
    tone: str = "neutral"
    issues_fixed: list[NarrativeIssue] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)
    generated_at: datetime = field(default_factory=utc_now)

    @property
    def text(self) -> str:
        """Plain-text narrative body."""
        blocks: list[str] = []
        for paragraph in self.paragraphs:
            if paragraph.is_transition:
                blocks.append(paragraph.text)
            else:
                heading = paragraph.section_title or paragraph.section_id
                if heading:
                    blocks.append(heading)
                if paragraph.text:
                    blocks.append(paragraph.text)
            blocks.append("")
        return "\n".join(blocks).strip()

    def to_dict(self) -> dict[str, Any]:
        """Serialize NarrativeReport."""
        return {
            "title": self.title,
            "paragraphs": [item.to_dict() for item in self.paragraphs],
            "sections": self.sections,
            "html": self.html,
            "markdown": self.markdown,
            "pdf_path": self.pdf_path,
            "tone": self.tone,
            "issues_fixed": [item.to_dict() for item in self.issues_fixed],
            "metrics": self.metrics,
            "generated_at": self.generated_at.isoformat(),
            "text": self.text,
        }
