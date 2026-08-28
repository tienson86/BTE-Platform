"""Observation builder — classified Strength evidence."""

from __future__ import annotations

from engines.narrative_framework.strength.blocks import make_block
from engines.narrative_framework.strength.classify import classify_strength_evidence
from engines.narrative_framework.strength.models import (
    StrengthEvidence,
    StrengthNarrativeBlock,
    StrengthNarrativeEvidencePack,
)


def _pack(
    source: StrengthEvidence | StrengthNarrativeEvidencePack,
) -> StrengthNarrativeEvidencePack:
    if isinstance(source, StrengthNarrativeEvidencePack):
        return source
    return classify_strength_evidence(source)


def build_observation(
    source: StrengthEvidence | StrengthNarrativeEvidencePack,
) -> StrengthNarrativeBlock:
    """Name the published strength class and score from classified context items."""
    pack = _pack(source)
    sentences: list[str] = []
    paths: list[str] = []
    level = pack.item("strength_level")
    if level and level.display_value:
        sentences.append(f"Nhật chủ được đọc là {level.display_value}.")
        paths.append(level.source_path)
    score = pack.item("score")
    if score and score.value is not None:
        sentences.append(f"Điểm lực đã công bố là {score.display_value}.")
        paths.append(score.source_path)
    return make_block("observation", tuple(sentences), tuple(paths))
