"""Draft evidence atoms before deterministic id assignment."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from consulting.marriage.models.enums import (
    EvidenceDirection,
    EvidenceSignificance,
    MarriageDomain,
    MarriageEvidenceType,
    RelationshipSubject,
)
from consulting.marriage.models.evidence import EvidenceSourceRef, MarriageEvidence
from consulting.marriage.policy.versions import EVIDENCE_MODEL_VERSION, policy_version_token


@dataclass(frozen=True, slots=True)
class EvidenceDraft:
    """One evidence atom before stable id assignment."""

    domain: MarriageDomain
    evidence_type: MarriageEvidenceType
    direction: EvidenceDirection
    significance: EvidenceSignificance
    confidence: float
    subject: RelationshipSubject
    source_refs: tuple[EvidenceSourceRef, ...]
    predicate: str
    scope: str
    rule_id: str
    payload: Mapping[str, Any]


def sort_key(draft: EvidenceDraft) -> tuple[str, ...]:
    """Return a deterministic sort key for evidence drafts."""
    paths = ",".join(ref.path for ref in draft.source_refs)
    return (
        draft.domain.value,
        draft.evidence_type.value,
        draft.subject.value,
        draft.predicate,
        draft.direction.value,
        paths,
    )


def semantic_key(draft: EvidenceDraft) -> tuple[str, ...]:
    """Return the semantic identity used for deduplication."""
    return (
        draft.domain.value,
        draft.evidence_type.value,
        draft.subject.value,
        draft.predicate,
        draft.direction.value,
        draft.scope,
    )


def assign_ids(drafts: list[EvidenceDraft]) -> list[MarriageEvidence]:
    """Merge semantic duplicates, then assign stable evidence ids."""
    merged: dict[tuple[str, ...], EvidenceDraft] = {}
    for draft in sorted(drafts, key=sort_key):
        key = semantic_key(draft)
        existing = merged.get(key)
        if existing is None:
            merged[key] = draft
            continue
        refs = tuple(dict.fromkeys((*existing.source_refs, *draft.source_refs)))
        significance = existing.significance
        if _rank(draft.significance) > _rank(existing.significance):
            significance = draft.significance
        merged[key] = EvidenceDraft(
            domain=existing.domain,
            evidence_type=existing.evidence_type,
            direction=existing.direction,
            significance=significance,
            confidence=min(existing.confidence, draft.confidence),
            subject=existing.subject,
            source_refs=refs,
            predicate=existing.predicate,
            scope=existing.scope,
            rule_id=existing.rule_id,
            payload=existing.payload,
        )
    assigned: list[MarriageEvidence] = []
    for index, draft in enumerate(sorted(merged.values(), key=sort_key), start=1):
        assigned.append(
            MarriageEvidence(
                evidence_id=f"EV-{index:04d}",
                domain=draft.domain,
                evidence_type=draft.evidence_type,
                direction=draft.direction,
                significance=draft.significance,
                confidence=draft.confidence,
                subject=draft.subject,
                source_refs=draft.source_refs,
                rule_id=draft.rule_id,
                technical_payload=dict(draft.payload),
                predicate=draft.predicate,
                scope=draft.scope,
                version=EVIDENCE_MODEL_VERSION,
                policy_ref=policy_version_token(),
            )
        )
    return assigned


def _rank(value: EvidenceSignificance) -> int:
    """Order significance for merge. Not a score."""
    return {
        EvidenceSignificance.MINOR: 0,
        EvidenceSignificance.MODERATE: 1,
        EvidenceSignificance.MAJOR: 2,
        EvidenceSignificance.CRITICAL: 3,
    }[value]
