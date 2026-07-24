"""Select transitions between paragraphs (no new sentence generation)."""

from __future__ import annotations

from typing import Any, Iterable, Mapping

from .paragraph_models import Paragraph, Transition


class TransitionSelector:
    """
    Insert transition markers only between consecutive paragraphs.

    Never invents narrative sentences. Optionally anchors to an existing
    repeated topic from ContentContext when sections differ.
    """

    def select(
        self,
        paragraphs: list[Paragraph],
        *,
        repeated_topics: Iterable[Mapping[str, Any]] | None = None,
    ) -> list[Transition]:
        """Build transitions for each adjacent paragraph pair."""
        topics = list(repeated_topics or [])
        transitions: list[Transition] = []
        if len(paragraphs) < 2:
            return transitions

        for index in range(len(paragraphs) - 1):
            left = paragraphs[index]
            right = paragraphs[index + 1]
            # Only between paragraphs (always adjacent in final order)
            kind = (
                "section_boundary"
                if left.section != right.section
                else "polarity_or_topic_boundary"
            )
            anchor = self._anchor_topic(
                left.section,
                right.section,
                topics,
            )
            transitions.append(
                Transition(
                    transition_id=f"T{index + 1:03d}",
                    after_paragraph_id=left.paragraph_id,
                    before_paragraph_id=right.paragraph_id,
                    from_section=left.section,
                    to_section=right.section,
                    kind=kind,
                    anchor_topic=anchor,
                )
            )
        return transitions

    @staticmethod
    def _anchor_topic(
        from_section: str,
        to_section: str,
        repeated_topics: list[Mapping[str, Any]],
    ) -> str:
        """Pick an existing repeated topic shared by both sections, if any."""
        if from_section == to_section:
            return ""
        for item in repeated_topics:
            sections = {str(section) for section in (item.get("sections") or [])}
            if from_section in sections and to_section in sections:
                return str(item.get("topic") or "")
        return ""
