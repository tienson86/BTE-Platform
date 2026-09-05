"""Internal evidence candidates. Ranking happens after merge."""

from __future__ import annotations

from dataclasses import dataclass, replace

from engines.detailed_interpretation_engine.enums import PriorityTier
from engines.detailed_interpretation_engine.evidence_priority.constants import TIER_INDEX
from engines.detailed_interpretation_engine.value_objects import ConfidenceValue


@dataclass(frozen=True, slots=True)
class EvidenceCandidate:
    """One collected finding before merge and rank."""

    semantic_key: str
    source_kind: str
    source_refs: tuple[str, ...]
    domain: str
    category: str
    evidence_type: str
    tier: PriorityTier
    customer_label: str
    tier_reason: str
    confidence: ConfidenceValue
    confidence_source: str
    conditions: tuple[str, ...] = ()
    trace_ids: tuple[str, ...] = ()
    supporting_evidence: tuple[str, ...] = ()
    merge_origin: str = ""
    node_kind: str = ""
    rescued: bool = False
    filtered: bool = False


def higher_tier(left: PriorityTier, right: PriorityTier) -> PriorityTier:
    """Return the structurally higher tier. P0 beats P5."""
    if TIER_INDEX.get(left.value, 99) <= TIER_INDEX.get(right.value, 99):
        return left
    return right


def merge_candidates(left: EvidenceCandidate, right: EvidenceCandidate) -> EvidenceCandidate:
    """Merge two candidates that share a semantic cause. Keep both traces."""
    labels = [item for item in (left.customer_label, right.customer_label) if item]
    unique_labels: list[str] = []
    for label in labels:
        if label not in unique_labels:
            unique_labels.append(label)
    origins = [item for item in (left.merge_origin, right.merge_origin, left.semantic_key) if item]
    return replace(
        left,
        source_refs=_unique(left.source_refs + right.source_refs),
        supporting_evidence=_unique(left.supporting_evidence + right.supporting_evidence),
        conditions=_unique(left.conditions + right.conditions),
        trace_ids=_unique(left.trace_ids + right.trace_ids),
        tier=higher_tier(left.tier, right.tier),
        customer_label=" · ".join(unique_labels) if unique_labels else left.customer_label,
        tier_reason=left.tier_reason or right.tier_reason,
        merge_origin="+".join(_unique(tuple(origins))),
        rescued=left.rescued and right.rescued,
        filtered=left.filtered and right.filtered,
        confidence=left.confidence if left.confidence.summary else right.confidence,
        confidence_source=left.confidence_source or right.confidence_source,
    )


def _unique(values: tuple[str, ...]) -> tuple[str, ...]:
    found: list[str] = []
    for item in values:
        token = item.strip()
        if token and token not in found:
            found.append(token)
    return tuple(found)
