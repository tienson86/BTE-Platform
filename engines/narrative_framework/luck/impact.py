"""Impact builder — published Luck stage, optionally enriched by classification."""

from __future__ import annotations

from engines.narrative_framework.luck.blocks import make_block
from engines.narrative_framework.luck.classify import classify_luck_evidence
from engines.narrative_framework.luck.constants import IMPACT_COPY
from engines.narrative_framework.luck.models import (
    LuckEvidence,
    LuckNarrativeBlock,
    LuckNarrativeEvidencePack,
)


def _pack(
    source: LuckEvidence | LuckNarrativeEvidencePack,
) -> LuckNarrativeEvidencePack:
    if isinstance(source, LuckNarrativeEvidencePack):
        return source
    return classify_luck_evidence(source)


def build_impact(
    source: LuckEvidence | LuckNarrativeEvidencePack,
) -> LuckNarrativeBlock:
    """Describe the current published stage. No prediction."""
    pack = _pack(source)
    stage = pack.raw_evidence.luck_stage or pack.raw_evidence.current_cycle
    if not stage:
        return make_block("impact", (), ())
    sentences = [IMPACT_COPY.format(stage=stage)]
    paths = ["luck.luck_stage" if pack.raw_evidence.luck_stage else "luck.current_dayun"]
    support = [item.reason for item in pack.positive_evidence if item.reason]
    if support:
        unique = list(dict.fromkeys(support))
        sentences.append("Hỗ trợ vận đã công bố: " + ", ".join(unique) + ".")
        paths.append("luck.evidence_pack.positive")
    return make_block("impact", tuple(sentences), tuple(paths))
