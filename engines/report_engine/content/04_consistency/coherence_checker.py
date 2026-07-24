"""Coherence checks — warn only; do not invent or rewrite content."""

from __future__ import annotations

from typing import Any

from ._text_utils import normalize
from .consistency_models import ConsistencyIssue


class CoherenceChecker:
    """
    Report coherence problems without mutating paragraph text.

    Examples: empty body, very short fragment, same-section topic jump
    after drops (informational).
    """

    def __init__(self, *, min_chars: int = 8) -> None:
        self.min_chars = min_chars

    def check(self, paragraphs: list[Any]) -> list[ConsistencyIssue]:
        """Return coherence issues (warnings)."""
        issues: list[ConsistencyIssue] = []
        previous_section = ""
        for paragraph in paragraphs:
            pid = str(getattr(paragraph, "paragraph_id", ""))
            section = str(getattr(paragraph, "section", ""))
            text = str(getattr(paragraph, "text", "") or "").strip()
            norm = normalize(text)

            if not norm:
                issues.append(
                    ConsistencyIssue(
                        kind="coherence",
                        detail="Paragraph has empty text.",
                        paragraph_id=pid,
                        section=section,
                        action="warn",
                    )
                )
            elif len(norm) < self.min_chars:
                issues.append(
                    ConsistencyIssue(
                        kind="coherence",
                        detail="Paragraph text is unusually short.",
                        paragraph_id=pid,
                        section=section,
                        action="warn",
                    )
                )

            sentences = getattr(paragraph, "sentences", None) or []
            if sentences:
                # Sentences should stay in the same section as the paragraph
                for sentence in sentences:
                    sent_section = str(getattr(sentence, "section", section))
                    if sent_section and sent_section != section:
                        issues.append(
                            ConsistencyIssue(
                                kind="coherence",
                                detail="Sentence section mismatches paragraph section.",
                                paragraph_id=pid,
                                section=section,
                                action="warn",
                            )
                        )
                        break

            if previous_section and section and previous_section != section:
                # Soft note only — transitions are handled upstream
                issues.append(
                    ConsistencyIssue(
                        kind="coherence",
                        detail=(
                            f"Section boundary {previous_section} → {section}."
                        ),
                        paragraph_id=pid,
                        section=section,
                        action="info",
                    )
                )
            previous_section = section or previous_section
        return issues
