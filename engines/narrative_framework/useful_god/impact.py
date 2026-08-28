"""Impact builder — published Useful God, optionally enriched by classification."""

from __future__ import annotations

from engines.narrative_framework.useful_god.blocks import make_block
from engines.narrative_framework.useful_god.classify import classify_useful_god_evidence
from engines.narrative_framework.useful_god.constants import IMPACT_COPY
from engines.narrative_framework.useful_god.models import (
    UsefulGodEvidence,
    UsefulGodNarrativeBlock,
    UsefulGodNarrativeEvidencePack,
)


def _pack(
    source: UsefulGodEvidence | UsefulGodNarrativeEvidencePack,
) -> UsefulGodNarrativeEvidencePack:
    if isinstance(source, UsefulGodNarrativeEvidencePack):
        return source
    return classify_useful_god_evidence(source)


def build_impact(
    source: UsefulGodEvidence | UsefulGodNarrativeEvidencePack,
) -> UsefulGodNarrativeBlock:
    """Describe consequence of the published Useful God. Classification cannot change it."""
    pack = _pack(source)
    display = pack.raw_evidence.useful_display or pack.raw_evidence.useful_god
    if not display:
        return make_block("impact", (), ())
    sentences = [IMPACT_COPY.format(useful_display=display)]
    paths = ["useful_god.useful_display"]
    support = [item.reason for item in pack.positive_evidence if item.reason]
    if support:
        unique = list(dict.fromkeys(support))
        sentences.append("Hỗ trợ Dụng thần đã công bố: " + ", ".join(unique) + ".")
        paths.append("useful_god.evidence_pack.positive")
    return make_block("impact", tuple(sentences), tuple(paths))
