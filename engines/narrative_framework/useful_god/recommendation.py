"""Recommendation builder — copy published Useful God guidance only."""

from __future__ import annotations

from engines.narrative_framework.useful_god.blocks import make_block
from engines.narrative_framework.useful_god.models import UsefulGodEvidence, UsefulGodNarrativeBlock


def build_recommendation(evidence: UsefulGodEvidence) -> UsefulGodNarrativeBlock:
    """Restate published Useful God / Hỷ / Kỵ / climate guidance. No new advice."""
    sentences: list[str] = []
    paths: list[str] = []
    display = evidence.useful_display or evidence.useful_god
    if display:
        sentences.append(f"Ưu tiên hướng Dụng thần đã công bố: {display}.")
        paths.append("useful_god.useful_display")
    if evidence.favorable_display:
        sentences.append(f"Hỷ thần đã công bố: {evidence.favorable_display}.")
        paths.append("useful_god.favorable_display")
    if evidence.unfavorable_display:
        sentences.append(f"Hạn chế Kỵ thần đã công bố: {evidence.unfavorable_display}.")
        paths.append("useful_god.unfavorable_display")
    if evidence.climate_preference_label:
        sentences.append(
            f"Hướng điều hậu đã công bố: {evidence.climate_preference_label}."
        )
        paths.append("useful_god.climate_preference_label")
    for item in evidence.recommendations:
        text = item if item.endswith(".") else item + "."
        sentences.append(text)
        paths.append("useful_god.recommendations")
    return make_block("recommendation", tuple(sentences), tuple(paths))
