"""Deterministic evidence resolution. Raw evidence stays immutable."""

from __future__ import annotations

from consulting.marriage.models.enums import (
    EvidenceDirection,
    EvidenceResolutionStatus,
    EvidenceSignificance,
    MarriageEvidenceType,
)
from consulting.marriage.models.evidence import MarriageEvidence, ResolvedMarriageEvidence

_SIGNIFICANCE_ORDER: tuple[EvidenceSignificance, ...] = (
    EvidenceSignificance.MINOR,
    EvidenceSignificance.MODERATE,
    EvidenceSignificance.MAJOR,
    EvidenceSignificance.CRITICAL,
)

_POSITIVE_TYPES = frozenset(
    {
        MarriageEvidenceType.USEFUL_GOD_SUPPORT,
        MarriageEvidenceType.ELEMENT_SUPPORT,
        MarriageEvidenceType.STEM_COMBINATION,
        MarriageEvidenceType.BRANCH_COMBINATION,
        MarriageEvidenceType.BRANCH_MEETING,
        MarriageEvidenceType.TEN_GOD_SUPPORT,
        MarriageEvidenceType.ROLE_COMPLEMENT,
        MarriageEvidenceType.LUCK_ALIGNMENT,
    }
)
_NEGATIVE_TYPES = frozenset(
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
    }
)


class MarriageEvidenceResolver:
    """Normalize, deduplicate, and resolve damage/rescue without deleting atoms."""

    def resolve(self, evidence: list[MarriageEvidence]) -> list[ResolvedMarriageEvidence]:
        """Return derived resolution overlays in deterministic evidence order."""
        unique = _deduplicate(evidence)
        conflicts = _conflict_map(unique)
        rescued = _rescue_pairs(unique)
        resolved: list[ResolvedMarriageEvidence] = []
        for item in unique:
            status, reason, residual, depends = _status_for(item, conflicts, rescued)
            resolved.append(
                ResolvedMarriageEvidence(
                    evidence_id=item.evidence_id,
                    status=status,
                    significance=_residual_significance(item, status),
                    confidence=item.confidence,
                    conflicts_with=tuple(sorted(conflicts.get(item.evidence_id, ()))),
                    depends_on=depends,
                    suppression_reason=reason,
                    residual_impact=residual,
                )
            )
        return resolved


def _deduplicate(evidence: list[MarriageEvidence]) -> list[MarriageEvidence]:
    """Keep first atom per semantic key. Merge is represented by surviving id order."""
    seen: set[tuple[str, ...]] = set()
    unique: list[MarriageEvidence] = []
    for item in evidence:
        key = (
            item.domain.value,
            item.evidence_type.value,
            item.subject.value,
            item.predicate or "",
            item.direction.value,
            item.scope or "",
        )
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    return unique


def _conflict_map(evidence: list[MarriageEvidence]) -> dict[str, set[str]]:
    """Preserve opposing natal/relationship evidence as conflicts."""
    conflicts: dict[str, set[str]] = {item.evidence_id: set() for item in evidence}
    for left in evidence:
        if left.scope == "reference" or left.scope == "timing":
            continue
        for right in evidence:
            if left.evidence_id >= right.evidence_id:
                continue
            if right.scope == "reference" or right.scope == "timing":
                continue
            if left.domain is not right.domain:
                continue
            if not _opposing(left, right):
                continue
            conflicts[left.evidence_id].add(right.evidence_id)
            conflicts[right.evidence_id].add(left.evidence_id)
    return conflicts


def _opposing(left: MarriageEvidence, right: MarriageEvidence) -> bool:
    """Return True when two atoms are valid opposing evidence."""
    if left.direction is EvidenceDirection.POSITIVE and right.direction is EvidenceDirection.NEGATIVE:
        return True
    if left.direction is EvidenceDirection.NEGATIVE and right.direction is EvidenceDirection.POSITIVE:
        return True
    return (left.evidence_type in _POSITIVE_TYPES and right.evidence_type in _NEGATIVE_TYPES) or (
        left.evidence_type in _NEGATIVE_TYPES and right.evidence_type in _POSITIVE_TYPES
    )


def _rescue_pairs(evidence: list[MarriageEvidence]) -> dict[str, tuple[str, ...]]:
    """Clash/control may be rescued by combination/support. Raw atoms remain."""
    rescued: dict[str, tuple[str, ...]] = {}
    supports = [
        item
        for item in evidence
        if item.evidence_type
        in {
            MarriageEvidenceType.BRANCH_COMBINATION,
            MarriageEvidenceType.STEM_COMBINATION,
            MarriageEvidenceType.USEFUL_GOD_SUPPORT,
            MarriageEvidenceType.BRANCH_MEETING,
        }
    ]
    damaged = [
        item
        for item in evidence
        if item.evidence_type
        in {
            MarriageEvidenceType.BRANCH_CLASH,
            MarriageEvidenceType.BRANCH_HARM,
            MarriageEvidenceType.BRANCH_PUNISHMENT,
            MarriageEvidenceType.BRANCH_BREAK,
            MarriageEvidenceType.STEM_CONTROL,
            MarriageEvidenceType.UNFAVORABLE_ACTIVATION,
        }
    ]
    for negative in damaged:
        rescuers = tuple(item.evidence_id for item in supports)
        if rescuers:
            rescued[negative.evidence_id] = rescuers
    return rescued


def _status_for(
    item: MarriageEvidence,
    conflicts: dict[str, set[str]],
    rescued: dict[str, tuple[str, ...]],
) -> tuple[EvidenceResolutionStatus, str | None, str | None, tuple[str, ...]]:
    """Compute derived status without deleting the atom."""
    if item.scope == "reference":
        return EvidenceResolutionStatus.ACTIVE, None, "reference_only", ()
    rescuers = rescued.get(item.evidence_id, ())
    opposing = tuple(sorted(conflicts.get(item.evidence_id, ())))
    if rescuers:
        return EvidenceResolutionStatus.RESCUED, None, "rescued_residual", rescuers
    if opposing:
        return EvidenceResolutionStatus.CONFLICTING, None, "conflict_preserved", opposing
    return EvidenceResolutionStatus.ACTIVE, None, None, ()


def _residual_significance(
    item: MarriageEvidence,
    status: EvidenceResolutionStatus,
) -> EvidenceSignificance:
    """Reduce residual impact after rescue. Never erase the original atom."""
    if status is not EvidenceResolutionStatus.RESCUED:
        return item.significance
    index = _SIGNIFICANCE_ORDER.index(item.significance)
    return _SIGNIFICANCE_ORDER[max(0, index - 1)]
