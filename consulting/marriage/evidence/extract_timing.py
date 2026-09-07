"""Luck activation evidence. Does not rewrite natal structure."""

from __future__ import annotations

from consulting.marriage.evidence.draft import EvidenceDraft
from consulting.marriage.evidence.snapshot_access import (
    favorable_elements,
    source_ref,
    snapshot_for,
    unfavorable_elements,
    useful_elements,
)
from consulting.marriage.models.enums import (
    EvidenceDirection,
    EvidenceSignificance,
    MarriageDomain,
    MarriageEvidenceType,
    PersonSide,
    RelationshipSubject,
)
from consulting.marriage.models.snapshot import LuckCycleSnapshot
from consulting.marriage.policy.catalog import stem_element
from consulting.marriage.policy.context import MarriagePolicyContext


def extract_luck_evidence(context: MarriagePolicyContext) -> list[EvidenceDraft]:
    """Extract D8 alignment only when Canonical luck and options allow it."""
    if context.options.include_luck is False:
        return []
    drafts: list[EvidenceDraft] = []
    drafts.extend(_person_luck(context, PersonSide.A))
    drafts.extend(_person_luck(context, PersonSide.B))
    return drafts


def _person_luck(context: MarriagePolicyContext, side: PersonSide) -> list[EvidenceDraft]:
    """Compare one person's current luck cycle against their useful/unfavorable."""
    snapshot = snapshot_for(context, side)
    cycle = snapshot.luck.current_cycle if snapshot.luck is not None else None
    if cycle is None:
        return []
    if not _cycle_in_window(cycle, context):
        return []
    luck_element = stem_element(cycle.stem)
    if luck_element is None:
        return []
    drafts: list[EvidenceDraft] = []
    if luck_element in useful_elements(snapshot.useful_god) or luck_element in favorable_elements(
        snapshot.useful_god
    ):
        drafts.append(
            _luck_atom(
                context,
                side,
                cycle,
                luck_element.value,
                MarriageEvidenceType.LUCK_ALIGNMENT,
                EvidenceDirection.POSITIVE,
                "luck_alignment",
            )
        )
    if luck_element in unfavorable_elements(snapshot.useful_god):
        drafts.append(
            _luck_atom(
                context,
                side,
                cycle,
                luck_element.value,
                MarriageEvidenceType.LUCK_MISALIGNMENT,
                EvidenceDirection.NEGATIVE,
                "luck_misalignment",
            )
        )
    return drafts


def _cycle_in_window(cycle: LuckCycleSnapshot, context: MarriagePolicyContext) -> bool:
    """Honor an explicit luck window. Unset window means the current cycle is used."""
    window = context.options.luck_window
    if window is None:
        return True
    return not (cycle.end_year < window.start_year or cycle.start_year > window.end_year)


def _luck_atom(
    context: MarriagePolicyContext,
    side: PersonSide,
    cycle: LuckCycleSnapshot,
    element: str,
    evidence_type: MarriageEvidenceType,
    direction: EvidenceDirection,
    predicate: str,
) -> EvidenceDraft:
    """Build one D8 activation atom. Scope stays timing."""
    return EvidenceDraft(
        domain=MarriageDomain.LUCK,
        evidence_type=evidence_type,
        direction=direction,
        significance=EvidenceSignificance.MINOR,
        confidence=0.65,
        subject=RelationshipSubject.SHARED,
        source_refs=(
            source_ref(context, side, "luck.current_cycle", cycle.can_chi),
            source_ref(context, side, "useful_god", element),
        ),
        predicate=f"{predicate}:{side.value}:{element}",
        scope="timing",
        rule_id="d8.luck_activation",
        payload={"side": side.value, "element": element, "cycle": cycle.can_chi},
    )
