"""Impact builder — published Strength class, optionally enriched by classification."""

from __future__ import annotations

from engines.narrative_framework.strength.blocks import make_block
from engines.narrative_framework.strength.classify import classify_strength_evidence
from engines.narrative_framework.strength.constants import IMPACT_BY_LEVEL
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


def build_impact(
    source: StrengthEvidence | StrengthNarrativeEvidencePack,
) -> StrengthNarrativeBlock:
    """Describe consequence of the published class. Classification cannot change it."""
    pack = _pack(source)
    level = pack.raw_evidence.strength_level
    text = IMPACT_BY_LEVEL.get(level, "")
    if not text:
        return make_block("impact", (), ())
    sentences = [text]
    paths = ["strength.strength_level"]
    support = [item.reason for item in pack.positive_evidence if item.reason]
    if support:
        unique = list(dict.fromkeys(support))
        sentences.append("Hỗ trợ lực đã công bố: " + ", ".join(unique) + ".")
        paths.append("strength.evidence_pack.positive")
    return make_block("impact", tuple(sentences), tuple(paths))
