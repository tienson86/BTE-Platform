"""Stem and branch interaction evidence from canonical pillar identities."""

from __future__ import annotations

from consulting.marriage.evidence.draft import EvidenceDraft
from consulting.marriage.evidence.snapshot_access import (
    PILLAR_SLOTS,
    pillar_of,
    significance_for_slots,
    source_ref,
    snapshot_for,
)
from consulting.marriage.models.enums import (
    EvidenceDirection,
    MarriageDomain,
    MarriageEvidenceType,
    PersonSide,
    RelationshipSubject,
)
from consulting.marriage.models.snapshot import PillarValue
from consulting.marriage.policy.catalog import (
    BRANCH_BREAKS,
    BRANCH_CLASHES,
    BRANCH_COMBINATIONS,
    BRANCH_HARMS,
    BRANCH_MEETING_TRIADS,
    BRANCH_PUNISH_PAIRS,
    BRANCH_PUNISH_TRIADS,
    BRANCH_SELF_PUNISH,
    STEM_COMBINATIONS,
    normalize_branch,
    normalize_stem,
    pair_relation,
    stem_controls,
    stem_element,
)
from consulting.marriage.policy.context import MarriagePolicyContext


def extract_stem_branch_evidence(context: MarriagePolicyContext) -> list[EvidenceDraft]:
    """Extract D2 pair relations between Person A and Person B pillars."""
    drafts: list[EvidenceDraft] = []
    for slot_a in PILLAR_SLOTS:
        pillar_a = pillar_of(context.snapshot_a, slot_a)
        if pillar_a is None:
            continue
        for slot_b in PILLAR_SLOTS:
            pillar_b = pillar_of(context.snapshot_b, slot_b)
            if pillar_b is None:
                continue
            drafts.extend(_pair_atoms(context, slot_a, pillar_a, slot_b, pillar_b))
    drafts.extend(_triad_atoms(context, BRANCH_MEETING_TRIADS, MarriageEvidenceType.BRANCH_MEETING, "d2.branch_meeting"))
    drafts.extend(_triad_atoms(context, BRANCH_PUNISH_TRIADS, MarriageEvidenceType.BRANCH_PUNISHMENT, "d2.branch_punishment"))
    return drafts


def _pair_atoms(
    context: MarriagePolicyContext,
    slot_a: str,
    pillar_a: PillarValue,
    slot_b: str,
    pillar_b: PillarValue,
) -> list[EvidenceDraft]:
    """Emit pair-wise stem/branch atoms for one pillar pair."""
    drafts: list[EvidenceDraft] = []
    stem_a = normalize_stem(pillar_a.stem)
    stem_b = normalize_stem(pillar_b.stem)
    branch_a = normalize_branch(pillar_a.branch)
    branch_b = normalize_branch(pillar_b.branch)
    significance = significance_for_slots(slot_a, slot_b)
    refs = (
        source_ref(context, PersonSide.A, f"pillars.{slot_a}", pillar_a.can_chi),
        source_ref(context, PersonSide.B, f"pillars.{slot_b}", pillar_b.can_chi),
    )
    combination = pair_relation(STEM_COMBINATIONS, stem_a, stem_b)
    if combination:
        drafts.append(
            _shared_atom(
                MarriageEvidenceType.STEM_COMBINATION,
                EvidenceDirection.POSITIVE,
                significance,
                refs,
                f"stem_combination:{combination}:{slot_a}:{slot_b}",
                "d2.stem_combination",
                combination,
            )
        )
    clash = pair_relation(BRANCH_CLASHES, branch_a, branch_b)
    if clash:
        drafts.append(
            _shared_atom(
                MarriageEvidenceType.BRANCH_CLASH,
                EvidenceDirection.NEGATIVE,
                significance,
                refs,
                f"branch_clash:{clash}:{slot_a}:{slot_b}",
                "d2.branch_clash",
                clash,
            )
        )
    drafts.extend(_more_branch_pairs(branch_a, branch_b, significance, refs, slot_a, slot_b))
    drafts.extend(_stem_control_atoms(stem_a, stem_b, significance, refs, slot_a, slot_b))
    return drafts


def _more_branch_pairs(
    branch_a: str | None,
    branch_b: str | None,
    significance,
    refs,
    slot_a: str,
    slot_b: str,
) -> list[EvidenceDraft]:
    """Emit combination, harm, break, and pair punishment atoms."""
    drafts: list[EvidenceDraft] = []
    mapping = (
        (BRANCH_COMBINATIONS, MarriageEvidenceType.BRANCH_COMBINATION, EvidenceDirection.POSITIVE, "d2.branch_combination", "branch_combination"),
        (BRANCH_HARMS, MarriageEvidenceType.BRANCH_HARM, EvidenceDirection.NEGATIVE, "d2.branch_harm", "branch_harm"),
        (BRANCH_BREAKS, MarriageEvidenceType.BRANCH_BREAK, EvidenceDirection.NEGATIVE, "d2.branch_break", "branch_break"),
        (BRANCH_PUNISH_PAIRS, MarriageEvidenceType.BRANCH_PUNISHMENT, EvidenceDirection.NEGATIVE, "d2.branch_punishment", "branch_punishment"),
    )
    for pairs, evidence_type, direction, rule_id, prefix in mapping:
        relation = pair_relation(pairs, branch_a, branch_b)
        if relation:
            drafts.append(
                _shared_atom(
                    evidence_type,
                    direction,
                    significance,
                    refs,
                    f"{prefix}:{relation}:{slot_a}:{slot_b}",
                    rule_id,
                    relation,
                )
            )
    if branch_a and branch_a == branch_b and branch_a in BRANCH_SELF_PUNISH:
        drafts.append(
            _shared_atom(
                MarriageEvidenceType.BRANCH_PUNISHMENT,
                EvidenceDirection.NEGATIVE,
                significance,
                refs,
                f"branch_punishment:self:{branch_a}:{slot_a}:{slot_b}",
                "d2.branch_punishment",
                f"self_{branch_a}",
            )
        )
    return drafts


def _stem_control_atoms(
    stem_a: str | None,
    stem_b: str | None,
    significance,
    refs,
    slot_a: str,
    slot_b: str,
) -> list[EvidenceDraft]:
    """Emit directional stem control when the five-element cycle supports it."""
    element_a = stem_element(stem_a)
    element_b = stem_element(stem_b)
    drafts: list[EvidenceDraft] = []
    if stem_controls(element_a, element_b):
        drafts.append(
            EvidenceDraft(
                domain=MarriageDomain.STEM_BRANCH,
                evidence_type=MarriageEvidenceType.STEM_CONTROL,
                direction=EvidenceDirection.NEGATIVE,
                significance=significance,
                confidence=0.8,
                subject=RelationshipSubject.A_TO_B,
                source_refs=refs,
                predicate=f"stem_control:{stem_a}:{stem_b}:{slot_a}:{slot_b}",
                scope="relationship",
                rule_id="d2.stem_control",
                payload={"relation_id": f"{stem_a}_controls_{stem_b}"},
            )
        )
    if stem_controls(element_b, element_a):
        drafts.append(
            EvidenceDraft(
                domain=MarriageDomain.STEM_BRANCH,
                evidence_type=MarriageEvidenceType.STEM_CONTROL,
                direction=EvidenceDirection.NEGATIVE,
                significance=significance,
                confidence=0.8,
                subject=RelationshipSubject.B_TO_A,
                source_refs=refs,
                predicate=f"stem_control:{stem_b}:{stem_a}:{slot_b}:{slot_a}",
                scope="relationship",
                rule_id="d2.stem_control",
                payload={"relation_id": f"{stem_b}_controls_{stem_a}"},
            )
        )
    return drafts


def _shared_atom(
    evidence_type: MarriageEvidenceType,
    direction: EvidenceDirection,
    significance,
    refs,
    predicate: str,
    rule_id: str,
    relation_id: str,
) -> EvidenceDraft:
    """Build a SHARED stem/branch atom."""
    return EvidenceDraft(
        domain=MarriageDomain.STEM_BRANCH,
        evidence_type=evidence_type,
        direction=direction,
        significance=significance,
        confidence=0.85,
        subject=RelationshipSubject.SHARED,
        source_refs=refs,
        predicate=predicate,
        scope="relationship",
        rule_id=rule_id,
        payload={"relation_id": relation_id},
    )


def _triad_atoms(
    context: MarriagePolicyContext,
    triads: tuple,
    evidence_type: MarriageEvidenceType,
    rule_id: str,
) -> list[EvidenceDraft]:
    """Emit triad evidence when both charts jointly complete a canonical triad."""
    branches_a = _branch_set(context, PersonSide.A)
    branches_b = _branch_set(context, PersonSide.B)
    combined = branches_a | branches_b
    drafts: list[EvidenceDraft] = []
    for members, relation_id in triads:
        if not members <= combined:
            continue
        if not (members & branches_a) or not (members & branches_b):
            continue
        drafts.append(
            EvidenceDraft(
                domain=MarriageDomain.STEM_BRANCH,
                evidence_type=evidence_type,
                direction=(
                    EvidenceDirection.POSITIVE
                    if evidence_type is MarriageEvidenceType.BRANCH_MEETING
                    else EvidenceDirection.NEGATIVE
                ),
                significance=significance_for_slots("day"),
                confidence=0.8,
                subject=RelationshipSubject.SHARED,
                source_refs=(
                    source_ref(context, PersonSide.A, "pillars.branches", sorted(branches_a)),
                    source_ref(context, PersonSide.B, "pillars.branches", sorted(branches_b)),
                ),
                predicate=f"{evidence_type.value}:{relation_id}",
                scope="relationship",
                rule_id=rule_id,
                payload={"relation_id": relation_id},
            )
        )
    return drafts


def _branch_set(context: MarriagePolicyContext, side: PersonSide) -> set[str]:
    """Collect canonical branches from one snapshot."""
    snapshot = snapshot_for(context, side)
    values: set[str] = set()
    for slot in PILLAR_SLOTS:
        pillar = pillar_of(snapshot, slot)
        if pillar is None:
            continue
        branch = normalize_branch(pillar.branch)
        if branch:
            values.add(branch)
    return values
