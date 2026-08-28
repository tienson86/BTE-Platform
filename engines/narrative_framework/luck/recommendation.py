"""Recommendation builder — copy published Luck recommendations only."""

from __future__ import annotations

from engines.narrative_framework.luck.blocks import make_block
from engines.narrative_framework.luck.models import LuckEvidence, LuckNarrativeBlock


def build_recommendation(evidence: LuckEvidence) -> LuckNarrativeBlock:
    """Restate published Luck recommendations. No invented advice."""
    sentences: list[str] = []
    paths: list[str] = []
    for item in evidence.recommendations:
        text = item if item.endswith(".") else item + "."
        sentences.append(text)
        paths.append("luck.recommendations")
    return make_block("recommendation", tuple(sentences), tuple(paths))
