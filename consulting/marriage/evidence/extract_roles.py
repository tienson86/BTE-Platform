"""Ten-god role evidence from Canonical role lists. No gender stereotypes."""

from __future__ import annotations

from consulting.marriage.evidence.draft import EvidenceDraft
from consulting.marriage.evidence.snapshot_access import (
    source_ref,
    snapshot_for,
    ten_god_items,
    unfavorable_roles,
    useful_roles,
)
from consulting.marriage.models.enums import (
    EvidenceDirection,
    EvidenceSignificance,
    MarriageDomain,
    MarriageEvidenceType,
    PersonSide,
    RelationshipSubject,
)
from consulting.marriage.models.snapshot import TenGodItem
from consulting.marriage.policy.catalog import is_wealth_pressure_role, is_wealth_role, normalize_role
from consulting.marriage.policy.context import MarriagePolicyContext


def extract_ten_god_evidence(context: MarriagePolicyContext) -> list[EvidenceDraft]:
    """Extract D3 role support/pressure and D5 wealth-role evidence."""
    drafts: list[EvidenceDraft] = []
    drafts.extend(_role_direction(context, PersonSide.A, PersonSide.B, RelationshipSubject.B_TO_A))
    drafts.extend(_role_direction(context, PersonSide.B, PersonSide.A, RelationshipSubject.A_TO_B))
    return drafts


def _role_direction(
    context: MarriagePolicyContext,
    need_side: PersonSide,
    offer_side: PersonSide,
    subject: RelationshipSubject,
) -> list[EvidenceDraft]:
    """Emit role atoms from offer_side toward need_side."""
    need = snapshot_for(context, need_side)
    offer = snapshot_for(context, offer_side)
    offer_items = ten_god_items(offer)
    drafts: list[EvidenceDraft] = []
    drafts.extend(
        _role_matches(
            context=context,
            need_side=need_side,
            offer_side=offer_side,
            subject=subject,
            offer_items=offer_items,
            wanted=useful_roles(need.useful_god),
            evidence_type=MarriageEvidenceType.TEN_GOD_SUPPORT,
            direction=EvidenceDirection.POSITIVE,
            rule_id="d3.role_support",
            predicate_prefix="role_support",
            domain=MarriageDomain.TEN_GODS,
        )
    )
    drafts.extend(
        _role_matches(
            context=context,
            need_side=need_side,
            offer_side=offer_side,
            subject=subject,
            offer_items=offer_items,
            wanted=unfavorable_roles(need.useful_god),
            evidence_type=MarriageEvidenceType.TEN_GOD_PRESSURE,
            direction=EvidenceDirection.NEGATIVE,
            rule_id="d3.role_pressure",
            predicate_prefix="role_pressure",
            domain=MarriageDomain.TEN_GODS,
        )
    )
    drafts.extend(_wealth_atoms(context, offer_side, subject, offer_items))
    return drafts


def _role_matches(
    *,
    context: MarriagePolicyContext,
    need_side: PersonSide,
    offer_side: PersonSide,
    subject: RelationshipSubject,
    offer_items: tuple[TenGodItem, ...],
    wanted: tuple[str, ...],
    evidence_type: MarriageEvidenceType,
    direction: EvidenceDirection,
    rule_id: str,
    predicate_prefix: str,
    domain: MarriageDomain,
) -> list[EvidenceDraft]:
    """Match wanted role names against the offering snapshot's ten gods."""
    wanted_folded = {normalize_role(name) for name in wanted if name}
    drafts: list[EvidenceDraft] = []
    seen: set[str] = set()
    for item in offer_items:
        folded = normalize_role(item.name)
        if folded not in wanted_folded or folded in seen:
            continue
        seen.add(folded)
        drafts.append(
            EvidenceDraft(
                domain=domain,
                evidence_type=evidence_type,
                direction=direction,
                significance=EvidenceSignificance.MAJOR,
                confidence=0.75,
                subject=subject,
                source_refs=(
                    source_ref(context, need_side, "useful_god.roles", sorted(wanted_folded)),
                    source_ref(context, offer_side, "ten_gods", item.name),
                ),
                predicate=f"{predicate_prefix}:{folded}",
                scope="natal",
                rule_id=rule_id,
                payload={"role": item.name, "need_side": need_side.value},
            )
        )
    return drafts


def _wealth_atoms(
    context: MarriagePolicyContext,
    offer_side: PersonSide,
    subject: RelationshipSubject,
    offer_items: tuple[TenGodItem, ...],
) -> list[EvidenceDraft]:
    """Emit D5 evidence only from explicit wealth-role identities."""
    drafts: list[EvidenceDraft] = []
    for item in offer_items:
        if is_wealth_role(item.name):
            drafts.append(
                EvidenceDraft(
                    domain=MarriageDomain.FINANCE,
                    evidence_type=MarriageEvidenceType.ROLE_COMPLEMENT,
                    direction=EvidenceDirection.POSITIVE,
                    significance=EvidenceSignificance.MODERATE,
                    confidence=0.7,
                    subject=subject,
                    source_refs=(source_ref(context, offer_side, "ten_gods", item.name),),
                    predicate=f"wealth_support:{normalize_role(item.name)}",
                    scope="finance",
                    rule_id="d5.wealth_support",
                    payload={"role": item.name},
                )
            )
        if is_wealth_pressure_role(item.name):
            drafts.append(
                EvidenceDraft(
                    domain=MarriageDomain.FINANCE,
                    evidence_type=MarriageEvidenceType.ROLE_CONFLICT,
                    direction=EvidenceDirection.NEGATIVE,
                    significance=EvidenceSignificance.MODERATE,
                    confidence=0.7,
                    subject=subject,
                    source_refs=(source_ref(context, offer_side, "ten_gods", item.name),),
                    predicate=f"wealth_pressure:{normalize_role(item.name)}",
                    scope="finance",
                    rule_id="d5.resource_competition",
                    payload={"role": item.name},
                )
            )
    return drafts
