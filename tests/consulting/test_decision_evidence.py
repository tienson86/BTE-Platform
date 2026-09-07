"""TV1-B03 evidence extraction, resolution, and traceability tests."""

from __future__ import annotations

import dataclasses

import pytest

from consulting.marriage.evidence.extractor import CanonicalEvidenceBuilder
from consulting.marriage.evidence.resolver import MarriageEvidenceResolver
from consulting.marriage.models.enums import (
    EvidenceDirection,
    EvidenceResolutionStatus,
    FiveElement,
    MarriageDomain,
    MarriageEvidenceType,
    PersonSide,
    RelationshipSubject,
)
from consulting.marriage.models.evidence import MarriageEvidence
from tests.consulting.decision_fixtures import (
    golden_pair,
    make_snapshot,
    policy_context_for,
)
from consulting.marriage.models.enums import CanonicalGender


def _extract(context=None):
    builder = CanonicalEvidenceBuilder()
    if context is None:
        snapshot_a, snapshot_b = golden_pair()
        context = policy_context_for(snapshot_a, snapshot_b)
    return builder.build_from_policy_context(context), context


def test_a_to_b_is_not_converted_to_mutual() -> None:
    """One-way useful-god support stays directional."""
    evidence, _context = _extract()
    useful = [
        item
        for item in evidence
        if item.evidence_type is MarriageEvidenceType.USEFUL_GOD_SUPPORT
    ]
    subjects = {item.subject for item in useful}
    assert RelationshipSubject.B_TO_A in subjects
    assert RelationshipSubject.MUTUAL not in subjects
    a_to_b = [item for item in useful if item.subject is RelationshipSubject.A_TO_B]
    b_to_a = [item for item in useful if item.subject is RelationshipSubject.B_TO_A]
    assert b_to_a
    for item in a_to_b:
        assert item.subject is RelationshipSubject.A_TO_B


def test_evidence_is_traceable_to_canonical_source() -> None:
    """Every evidence atom keeps a real canonical analysis_id."""
    evidence, context = _extract()
    assert evidence
    for item in evidence:
        assert item.source_refs
        analysis_ids = {ref.analysis_id for ref in item.source_refs}
        assert analysis_ids <= {
            context.source_analysis_id_a,
            context.source_analysis_id_b,
        }
        assert "MC-TEST" not in analysis_ids


def test_raw_evidence_is_immutable() -> None:
    """Raw evidence cannot be mutated after creation."""
    evidence, _context = _extract()
    atom = evidence[0]
    with pytest.raises(dataclasses.FrozenInstanceError):
        atom.confidence = 0.0  # type: ignore[misc]
    with pytest.raises(dataclasses.FrozenInstanceError):
        atom.evidence_id = "mutated"  # type: ignore[misc]


def test_semantic_deduplication_keeps_one_atom_per_meaning() -> None:
    """Duplicate semantic identity is collapsed during resolution input uniqueness."""
    evidence, _context = _extract()
    keys = [
        (
            item.domain,
            item.evidence_type,
            item.subject,
            item.predicate,
            item.direction,
            item.scope,
        )
        for item in evidence
    ]
    assert len(keys) == len(set(keys))
    resolved = MarriageEvidenceResolver().resolve(evidence)
    assert [item.evidence_id for item in resolved] == [item.evidence_id for item in evidence]


def test_conflicting_evidence_is_preserved() -> None:
    """Opposing atoms remain; resolution records the conflict."""
    evidence, _context = _extract()
    support = [
        item
        for item in evidence
        if item.evidence_type is MarriageEvidenceType.USEFUL_GOD_SUPPORT
        and item.domain is MarriageDomain.FIVE_ELEMENTS
    ]
    pressure = [
        item
        for item in evidence
        if item.evidence_type is MarriageEvidenceType.UNFAVORABLE_ACTIVATION
    ]
    assert support
    assert pressure
    resolved = {item.evidence_id: item for item in MarriageEvidenceResolver().resolve(evidence)}
    conflicted = [
        resolved[item.evidence_id]
        for item in support
        if resolved[item.evidence_id].conflicts_with
    ]
    assert conflicted
    raw_ids = {item.evidence_id for item in evidence}
    for item in conflicted:
        assert set(item.conflicts_with) <= raw_ids


def test_damage_rescue_does_not_delete_clash() -> None:
    """Clash remains after combination rescue."""
    snapshot_a = make_snapshot(
        analysis_id="MC-RESCUE-A",
        side=PersonSide.A,
        gender=CanonicalGender.MALE,
        day_stem="Canh",
        day_branch="Tý",
        day_element=FiveElement.METAL,
        useful=FiveElement.FIRE,
        month_branch="Sửu",
    )
    snapshot_b = make_snapshot(
        analysis_id="MC-RESCUE-B",
        side=PersonSide.B,
        gender=CanonicalGender.FEMALE,
        day_stem="Bính",
        day_branch="Ngọ",
        day_element=FiveElement.FIRE,
        useful=FiveElement.WOOD,
        month_branch="Sửu",
        year_branch="Sửu",
    )
    evidence, _context = _extract(policy_context_for(snapshot_a, snapshot_b))
    clashes = [item for item in evidence if item.evidence_type is MarriageEvidenceType.BRANCH_CLASH]
    combinations = [
        item for item in evidence if item.evidence_type is MarriageEvidenceType.BRANCH_COMBINATION
    ]
    assert clashes
    assert combinations
    resolved = {item.evidence_id: item for item in MarriageEvidenceResolver().resolve(evidence)}
    for clash in clashes:
        overlay = resolved[clash.evidence_id]
        assert overlay.status is EvidenceResolutionStatus.RESCUED
        assert overlay.depends_on
        assert clash.evidence_id in {item.evidence_id for item in evidence}
