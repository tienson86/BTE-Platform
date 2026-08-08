"""Executive Summary Composer — Sprint D2."""

from __future__ import annotations

from statistics import fmean

from engines.narrative_engine.runtime.models import ComponentType

from .constants import INSUFFICIENT_EVIDENCE_NARRATIVE
from .models import NarrativeSection, NarrativeSummary


class ExecutiveSummaryComposer:
    """
    Build NarrativeSummary from composed sections.

    Does not invent slots — uses section texts or insufficient narrative.
    """

    def compose(self, sections: tuple[NarrativeSection, ...]) -> NarrativeSummary:
        """Derive executive summary from body sections."""
        by_intent = {section.intent: section for section in sections}
        by_id = {section.id: section for section in sections}

        identity = _slot_text(
            by_id.get("sec-observation") or by_intent.get("observation")
        )
        strengths = _list_slot(
            by_id.get("sec-observation"),
            fallback_section=by_id.get("sec-impact"),
        )
        weaknesses = _list_slot(by_id.get("sec-warning"))
        priority = _recommendation_action(by_id.get("sec-recommendation"))
        next_action = priority

        flags: list[str] = []
        if identity == INSUFFICIENT_EVIDENCE_NARRATIVE:
            flags.append("identity")
        if not strengths or strengths == (INSUFFICIENT_EVIDENCE_NARRATIVE,):
            flags.append("strengths")
            strengths = (INSUFFICIENT_EVIDENCE_NARRATIVE,)
        if not weaknesses or weaknesses == (INSUFFICIENT_EVIDENCE_NARRATIVE,):
            flags.append("weaknesses")
            weaknesses = (INSUFFICIENT_EVIDENCE_NARRATIVE,)
        if priority == INSUFFICIENT_EVIDENCE_NARRATIVE:
            flags.append("priority_recommendation")
            flags.append("next_action")

        confidences = [section.confidence for section in sections if section.confidence > 0]
        overall = round(fmean(confidences), 4) if confidences else 0.0

        return NarrativeSummary(
            identity=identity,
            strengths=strengths,
            weaknesses=weaknesses,
            priority_recommendation=priority,
            next_action=next_action,
            overall_confidence=overall,
            insufficient_flags=tuple(dict.fromkeys(flags)),
        )


def _slot_text(section: NarrativeSection | None) -> str:
    """Extract first paragraph text or insufficient narrative."""
    if section is None or not section.paragraphs:
        return INSUFFICIENT_EVIDENCE_NARRATIVE
    paragraph = section.paragraphs[0]
    if paragraph.insufficient_data or not paragraph.text.strip():
        return INSUFFICIENT_EVIDENCE_NARRATIVE
    return paragraph.text.strip()


def _list_slot(
    section: NarrativeSection | None,
    fallback_section: NarrativeSection | None = None,
) -> tuple[str, ...]:
    """Build a short list slot from section paragraph text."""
    target = section
    if target is None or target.insufficient_data:
        target = fallback_section
    if target is None or not target.paragraphs:
        return (INSUFFICIENT_EVIDENCE_NARRATIVE,)
    texts = [
        paragraph.text.strip()
        for paragraph in target.paragraphs
        if paragraph.text.strip() and not paragraph.insufficient_data
    ]
    if not texts:
        return (INSUFFICIENT_EVIDENCE_NARRATIVE,)
    return tuple(texts[:2])


def _recommendation_action(section: NarrativeSection | None) -> str:
    """Extract primary recommendation action text."""
    if section is None:
        return INSUFFICIENT_EVIDENCE_NARRATIVE
    for item in section.recommendations:
        if item.insufficient_data or not item.action.strip():
            continue
        return item.action.strip()
    return _slot_text(section)
