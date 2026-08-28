"""Impact builder — published Pattern, optionally enriched by classification."""

from __future__ import annotations

from engines.narrative_framework.pattern.blocks import make_block
from engines.narrative_framework.pattern.classify import classify_pattern_evidence
from engines.narrative_framework.pattern.constants import IMPACT_COPY
from engines.narrative_framework.pattern.models import (
    PatternEvidence,
    PatternNarrativeBlock,
    PatternNarrativeEvidencePack,
)


def _pack(
    source: PatternEvidence | PatternNarrativeEvidencePack,
) -> PatternNarrativeEvidencePack:
    if isinstance(source, PatternNarrativeEvidencePack):
        return source
    return classify_pattern_evidence(source)


def build_impact(
    source: PatternEvidence | PatternNarrativeEvidencePack,
) -> PatternNarrativeBlock:
    """Describe implication of the published Pattern. Classification cannot change it."""
    pack = _pack(source)
    display = pack.raw_evidence.pattern_name or pack.raw_evidence.pattern_class
    if not display:
        return make_block("impact", (), ())
    sentences = [IMPACT_COPY.format(pattern_name=display)]
    paths = ["pattern.cach_cuc"]
    support = [item.reason for item in pack.positive_evidence if item.reason]
    if support:
        unique = list(dict.fromkeys(support))
        sentences.append("Hỗ trợ cách cục đã công bố: " + ", ".join(unique) + ".")
        paths.append("pattern.evidence_pack.positive")
    return make_block("impact", tuple(sentences), tuple(paths))
