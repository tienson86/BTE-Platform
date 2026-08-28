"""Reasoning builder — grouped classified Pattern evidence. No rescoring."""

from __future__ import annotations

from engines.narrative_framework.pattern.blocks import make_block
from engines.narrative_framework.pattern.classify import classify_pattern_evidence
from engines.narrative_framework.pattern.constants import (
    PUBLISHED_CLASS_PREFIX,
    RESTRAIN_GROUP_LABEL,
    SUPPORT_GROUP_LABEL,
)
from engines.narrative_framework.pattern.models import (
    PatternEvidence,
    PatternNarrativeBlock,
    PatternNarrativeEvidencePack,
)

_DIRECTIONAL = frozenset(
    {
        "winning_rule",
        "matched_rules",
        "success_reason",
        "failure_reason",
        "clash_status",
        "combination_status",
    }
)


def _pack(
    source: PatternEvidence | PatternNarrativeEvidencePack,
) -> PatternNarrativeEvidencePack:
    if isinstance(source, PatternNarrativeEvidencePack):
        return source
    return classify_pattern_evidence(source)


def _group_line(label: str, items: tuple) -> str | None:
    reasons = []
    seen: set[str] = set()
    for item in items:
        if item.component not in _DIRECTIONAL:
            continue
        reason = str(item.reason or "").strip()
        if not reason or reason in seen:
            continue
        seen.add(reason)
        reasons.append(reason)
    if not reasons:
        return None
    return f"{label}: " + ", ".join(reasons) + "."


def build_reasoning(
    source: PatternEvidence | PatternNarrativeEvidencePack,
) -> PatternNarrativeBlock:
    """Explain why the published Pattern was selected. Class stays engine-owned."""
    pack = _pack(source)
    evidence = pack.raw_evidence
    sentences: list[str] = []
    paths: list[str] = []
    if evidence.reasoning:
        sentences.append(evidence.reasoning.rstrip(".") + ".")
        paths.append("pattern.reason")
    support_line = _group_line(SUPPORT_GROUP_LABEL, pack.positive_evidence)
    if support_line:
        sentences.append(support_line)
        paths.append("pattern.evidence_pack.positive")
    restrain_line = _group_line(RESTRAIN_GROUP_LABEL, pack.negative_evidence)
    if restrain_line:
        sentences.append(restrain_line)
        paths.append("pattern.evidence_pack.negative")
    display = evidence.pattern_name or evidence.pattern_class
    if display:
        sentences.append(f"{PUBLISHED_CLASS_PREFIX} {display}.")
        paths.append("pattern.cach_cuc")
    if evidence.evidence_compact:
        sentences.append(evidence.evidence_compact.rstrip(".") + ".")
        paths.append("pattern.evidence_compact")
    return make_block("reasoning", tuple(sentences), tuple(paths))
