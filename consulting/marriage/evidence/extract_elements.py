"""Five-element and useful-god evidence. Snapshot comparison only."""

from __future__ import annotations

from consulting.marriage.evidence.draft import EvidenceDraft
from consulting.marriage.evidence.snapshot_access import (
    element_present,
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
from consulting.marriage.models.snapshot import MarriageCanonicalSnapshot
from consulting.marriage.policy.context import MarriagePolicyContext


def extract_element_evidence(context: MarriagePolicyContext) -> list[EvidenceDraft]:
    """Extract D1 evidence from useful/favorable/unfavorable snapshot fields."""
    drafts: list[EvidenceDraft] = []
    drafts.extend(_directed_need(context, PersonSide.A, PersonSide.B, RelationshipSubject.B_TO_A))
    drafts.extend(_directed_need(context, PersonSide.B, PersonSide.A, RelationshipSubject.A_TO_B))
    return drafts


def _directed_need(
    context: MarriagePolicyContext,
    need_side: PersonSide,
    offer_side: PersonSide,
    subject: RelationshipSubject,
) -> list[EvidenceDraft]:
    """Emit one-way support/pressure from offer_side toward need_side."""
    need = snapshot_for(context, need_side)
    offer = snapshot_for(context, offer_side)
    drafts: list[EvidenceDraft] = []
    useful = useful_elements(need.useful_god)
    if not useful:
        return drafts
    drafts.extend(
        _match_elements(
            context=context,
            need=need,
            offer=offer,
            need_side=need_side,
            offer_side=offer_side,
            subject=subject,
            elements=useful,
            evidence_type=MarriageEvidenceType.USEFUL_GOD_SUPPORT,
            direction=EvidenceDirection.POSITIVE,
            rule_id="d1.useful_god_support",
            predicate_prefix="useful_god_support",
        )
    )
    drafts.extend(
        _match_elements(
            context=context,
            need=need,
            offer=offer,
            need_side=need_side,
            offer_side=offer_side,
            subject=subject,
            elements=favorable_elements(need.useful_god),
            evidence_type=MarriageEvidenceType.ELEMENT_SUPPORT,
            direction=EvidenceDirection.POSITIVE,
            rule_id="d1.favorable_support",
            predicate_prefix="favorable_support",
        )
    )
    drafts.extend(
        _match_elements(
            context=context,
            need=need,
            offer=offer,
            need_side=need_side,
            offer_side=offer_side,
            subject=subject,
            elements=unfavorable_elements(need.useful_god),
            evidence_type=MarriageEvidenceType.UNFAVORABLE_ACTIVATION,
            direction=EvidenceDirection.NEGATIVE,
            rule_id="d1.unfavorable_activation",
            predicate_prefix="unfavorable_activation",
        )
    )
    return drafts


def _match_elements(
    *,
    context: MarriagePolicyContext,
    need: MarriageCanonicalSnapshot,
    offer: MarriageCanonicalSnapshot,
    need_side: PersonSide,
    offer_side: PersonSide,
    subject: RelationshipSubject,
    elements: tuple,
    evidence_type: MarriageEvidenceType,
    direction: EvidenceDirection,
    rule_id: str,
    predicate_prefix: str,
) -> list[EvidenceDraft]:
    """Create atoms when the offering snapshot presents a needed element."""
    drafts: list[EvidenceDraft] = []
    confidence = min(_useful_confidence(need), _useful_confidence(offer))
    for element in elements:
        if not element_present(offer, element):
            continue
        drafts.append(
            EvidenceDraft(
                domain=MarriageDomain.FIVE_ELEMENTS,
                evidence_type=evidence_type,
                direction=direction,
                significance=EvidenceSignificance.MAJOR,
                confidence=confidence,
                subject=subject,
                source_refs=(
                    source_ref(context, need_side, "useful_god", element.value),
                    source_ref(
                        context,
                        offer_side,
                        "five_elements.distribution",
                        offer.five_elements.distribution.get(element),
                    ),
                    source_ref(
                        context,
                        offer_side,
                        "day_master.element",
                        offer.day_master.element.value,
                    ),
                ),
                predicate=f"{predicate_prefix}:{element.value}",
                scope="natal",
                rule_id=rule_id,
                payload={"element": element.value, "need_side": need_side.value},
            )
        )
    return drafts


def _useful_confidence(snapshot: MarriageCanonicalSnapshot) -> float:
    """Use Canonical useful-god confidence when published."""
    value = snapshot.useful_god.confidence
    if value is None:
        return 0.7
    return max(0.0, min(1.0, value))
