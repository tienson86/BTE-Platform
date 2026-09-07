"""Finding resolution from resolved evidence. No finding without evidence."""

from __future__ import annotations

from consulting.marriage.finding.contract import MarriageFindingBuilder
from consulting.marriage.models.enums import (
    EvidenceDirection,
    EvidenceResolutionStatus,
    FindingPriority,
    FindingType,
    MarriageEvidenceType,
)
from consulting.marriage.models.evidence import MarriageEvidence, ResolvedMarriageEvidence
from consulting.marriage.models.finding import MarriageFinding
from consulting.marriage.policy.v1 import is_secondary_type
from consulting.marriage.policy.versions import FINDING_MODEL_VERSION

_SUPPORT_TYPES = frozenset(
    {
        MarriageEvidenceType.USEFUL_GOD_SUPPORT,
        MarriageEvidenceType.ELEMENT_SUPPORT,
        MarriageEvidenceType.STEM_COMBINATION,
        MarriageEvidenceType.BRANCH_COMBINATION,
        MarriageEvidenceType.BRANCH_MEETING,
        MarriageEvidenceType.TEN_GOD_SUPPORT,
        MarriageEvidenceType.ROLE_COMPLEMENT,
        MarriageEvidenceType.LUCK_ALIGNMENT,
        MarriageEvidenceType.SHEN_SHA_SUPPORT,
    }
)
_RISK_TYPES = frozenset(
    {
        MarriageEvidenceType.UNFAVORABLE_ACTIVATION,
        MarriageEvidenceType.ELEMENT_CONFLICT,
        MarriageEvidenceType.STEM_CONTROL,
        MarriageEvidenceType.BRANCH_CLASH,
        MarriageEvidenceType.BRANCH_HARM,
        MarriageEvidenceType.BRANCH_PUNISHMENT,
        MarriageEvidenceType.BRANCH_BREAK,
        MarriageEvidenceType.TEN_GOD_PRESSURE,
        MarriageEvidenceType.ROLE_CONFLICT,
        MarriageEvidenceType.LUCK_MISALIGNMENT,
        MarriageEvidenceType.SHEN_SHA_RISK,
    }
)


class CanonicalFindingBuilder(MarriageFindingBuilder):
    """Group semantically identical evidence into one finding."""

    def build(self, evidence: list[MarriageEvidence]) -> list[MarriageFinding]:
        """Create findings from raw evidence treated as active."""
        resolved = [
            ResolvedMarriageEvidence(
                evidence_id=item.evidence_id,
                status=EvidenceResolutionStatus.ACTIVE,
                significance=item.significance,
                confidence=item.confidence,
            )
            for item in evidence
        ]
        return self.build_from_resolved(evidence, resolved)

    def build_from_resolved(
        self,
        evidence: list[MarriageEvidence],
        resolved: list[ResolvedMarriageEvidence],
    ) -> list[MarriageFinding]:
        """Create findings from resolved overlays. Empty evidence yields no findings."""
        if not evidence:
            return []
        overlay = {item.evidence_id: item for item in resolved}
        groups: dict[tuple[str, str, str, str], list[MarriageEvidence]] = {}
        for item in evidence:
            if overlay.get(item.evidence_id) and overlay[item.evidence_id].status is EvidenceResolutionStatus.SUPPRESSED:
                continue
            key = (
                item.domain.value,
                item.evidence_type.value,
                _semantic_stem(item.predicate),
                item.subject.value,
            )
            groups.setdefault(key, []).append(item)
        findings: list[MarriageFinding] = []
        ordered_keys = sorted(groups)
        for index, key in enumerate(ordered_keys, start=1):
            members = groups[key]
            findings.append(_finding_from_group(f"F-{index:04d}", members, overlay))
        return findings


def _semantic_stem(predicate: str | None) -> str:
    """Group predicates that share a semantic meaning prefix."""
    if not predicate:
        return ""
    return predicate.split(":")[0]


def _finding_from_group(
    finding_id: str,
    members: list[MarriageEvidence],
    overlay: dict[str, ResolvedMarriageEvidence],
) -> MarriageFinding:
    """Build one finding from evidence that share semantic meaning."""
    first = members[0]
    evidence_ids = [item.evidence_id for item in members]
    conflicting: list[str] = []
    for item in members:
        resolved = overlay.get(item.evidence_id)
        if resolved is None:
            continue
        conflicting.extend(resolved.conflicts_with)
    conflicting = sorted(set(conflicting) - set(evidence_ids))
    directions = {item.direction for item in members}
    if EvidenceDirection.POSITIVE in directions and EvidenceDirection.NEGATIVE in directions:
        polarity = EvidenceDirection.MIXED
        finding_type = FindingType.MIXED
    else:
        polarity = first.direction
        finding_type = _finding_type(first.evidence_type, first.direction)
    confidences = [item.confidence for item in members]
    return MarriageFinding(
        finding_id=finding_id,
        domain=first.domain,
        type=finding_type,
        priority=_priority(first),
        direction=polarity,
        confidence=min(confidences),
        evidence_ids=evidence_ids,
        technical_summary=_semantic_stem(first.predicate) or first.evidence_type.value,
        semantic_key=_semantic_stem(first.predicate) or first.evidence_type.value,
        conflicting_evidence_ids=conflicting,
        conditions=["rescued"] if any(_rescued(overlay.get(item.evidence_id)) for item in members) else [],
        dependencies=_dependencies(members, overlay),
        version=FINDING_MODEL_VERSION,
    )


def _finding_type(evidence_type: MarriageEvidenceType, direction: EvidenceDirection) -> FindingType:
    """Map evidence semantics onto the frozen FindingType enum."""
    if evidence_type in {MarriageEvidenceType.LUCK_ALIGNMENT, MarriageEvidenceType.LUCK_MISALIGNMENT}:
        return FindingType.TIMING
    if is_secondary_type(evidence_type):
        return FindingType.CONDITION
    if evidence_type in _SUPPORT_TYPES or direction is EvidenceDirection.POSITIVE:
        return FindingType.SUPPORT
    if evidence_type in _RISK_TYPES or direction is EvidenceDirection.NEGATIVE:
        return FindingType.RISK
    if direction is EvidenceDirection.MIXED:
        return FindingType.MIXED
    return FindingType.CONDITION


def _priority(item: MarriageEvidence) -> FindingPriority:
    """Assign policy priority. Secondary evidence cannot be P0-P2."""
    if item.scope == "reference" or is_secondary_type(item.evidence_type):
        return FindingPriority.P5
    if item.scope == "timing":
        return FindingPriority.P3
    if item.evidence_type is MarriageEvidenceType.USEFUL_GOD_SUPPORT:
        return FindingPriority.P1
    if item.evidence_type in {
        MarriageEvidenceType.BRANCH_CLASH,
        MarriageEvidenceType.UNFAVORABLE_ACTIVATION,
        MarriageEvidenceType.TEN_GOD_PRESSURE,
    }:
        return FindingPriority.P1
    return FindingPriority.P2


def _rescued(resolved: ResolvedMarriageEvidence | None) -> bool:
    """Return True when the overlay is rescued."""
    return resolved is not None and resolved.status is EvidenceResolutionStatus.RESCUED


def _dependencies(
    members: list[MarriageEvidence],
    overlay: dict[str, ResolvedMarriageEvidence],
) -> list[str]:
    """Collect dependency ids from resolved overlays."""
    values: list[str] = []
    for item in members:
        resolved = overlay.get(item.evidence_id)
        if resolved is None:
            continue
        values.extend(resolved.depends_on)
    return sorted(set(values))
