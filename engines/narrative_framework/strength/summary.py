"""Summary builder — synthesizes prior blocks. No new facts."""

from __future__ import annotations

from engines.narrative_framework.strength.blocks import make_block
from engines.narrative_framework.strength.models import StrengthNarrativeBlock


def _first_sentence(block: StrengthNarrativeBlock) -> str | None:
    if not block.available or not block.sentences:
        return None
    text = block.sentences[0].strip()
    return text or None


def build_summary(
    observation: StrengthNarrativeBlock,
    reasoning: StrengthNarrativeBlock,
    impact: StrengthNarrativeBlock,
    recommendation: StrengthNarrativeBlock,
) -> StrengthNarrativeBlock:
    """Join the first sentence of each prior block. Introduce no new facts."""
    parts: list[str] = []
    paths: list[str] = []
    for block, path in (
        (observation, "strength.narrative.observation"),
        (reasoning, "strength.narrative.reasoning"),
        (impact, "strength.narrative.impact"),
        (recommendation, "strength.narrative.recommendation"),
    ):
        sentence = _first_sentence(block)
        if sentence:
            parts.append(sentence.rstrip("."))
            paths.append(path)
    if not parts:
        return make_block("summary", (), ())
    summary = ". ".join(parts) + "."
    return make_block("summary", (summary,), tuple(paths))
