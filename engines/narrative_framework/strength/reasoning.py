"""Reasoning builder — grouped classified evidence. No rescoring."""

from __future__ import annotations

from engines.narrative_framework.strength.blocks import make_block
from engines.narrative_framework.strength.classify import classify_strength_evidence
from engines.narrative_framework.strength.models import (
    StrengthEvidence,
    StrengthNarrativeBlock,
    StrengthNarrativeEvidencePack,
)
from engines.strength_engine.labels import strength_level_label

_DIRECTIONAL = frozenset({"season", "root", "support", "control", "drain", "special_rules"})


def _pack(
    source: StrengthEvidence | StrengthNarrativeEvidencePack,
) -> StrengthNarrativeEvidencePack:
    if isinstance(source, StrengthNarrativeEvidencePack):
        return source
    return classify_strength_evidence(source)


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
    source: StrengthEvidence | StrengthNarrativeEvidencePack,
) -> StrengthNarrativeBlock:
    """Explain supporting vs restraining published evidence. Class stays engine-owned."""
    pack = _pack(source)
    evidence = pack.raw_evidence
    sentences: list[str] = []
    paths: list[str] = []
    if evidence.reasoning:
        sentences.append(evidence.reasoning.rstrip(".") + ".")
        paths.append("strength.reasoning")
    support_line = _group_line("Yếu tố hỗ trợ lực Nhật chủ", pack.positive_evidence)
    if support_line:
        sentences.append(support_line)
        paths.append("strength.evidence_pack.positive")
    restrain_line = _group_line("Yếu tố suy giảm lực Nhật chủ", pack.negative_evidence)
    if restrain_line:
        sentences.append(restrain_line)
        paths.append("strength.evidence_pack.negative")
    label = strength_level_label(evidence.strength_level)
    if label:
        sentences.append(f"Phân loại lực đã công bố vẫn là {label}.")
        paths.append("strength.strength_level")
    if evidence.evidence_compact:
        sentences.append(evidence.evidence_compact.rstrip(".") + ".")
        paths.append("strength.evidence_compact")
    return make_block("reasoning", tuple(sentences), tuple(paths))
