"""Shared snapshot readers for evidence extraction. No BaZi recalculation."""

from __future__ import annotations

from consulting.marriage.models.enums import EvidenceSignificance, FiveElement, PersonSide
from consulting.marriage.models.evidence import EvidenceSourceRef
from consulting.marriage.models.snapshot import (
    MarriageCanonicalSnapshot,
    PillarValue,
    TenGodItem,
    UsefulGodSnapshot,
)
from consulting.marriage.policy.catalog import stem_element
from consulting.marriage.policy.context import MarriagePolicyContext


PILLAR_SLOTS: tuple[str, ...] = ("year", "month", "day", "hour")


def snapshot_for(context: MarriagePolicyContext, side: PersonSide) -> MarriageCanonicalSnapshot:
    """Return the snapshot for a person side."""
    if side is PersonSide.A:
        return context.snapshot_a
    return context.snapshot_b


def analysis_id(context: MarriagePolicyContext, side: PersonSide) -> str:
    """Return the canonical analysis id for a person side."""
    if side is PersonSide.A:
        return context.source_analysis_id_a
    return context.source_analysis_id_b


def source_ref(
    context: MarriagePolicyContext,
    side: PersonSide,
    path: str,
    value: object,
) -> EvidenceSourceRef:
    """Build a canonical source reference."""
    return EvidenceSourceRef(
        analysis_id=analysis_id(context, side),
        person=side,
        path=path,
        value=value,
    )


def pillar_of(snapshot: MarriageCanonicalSnapshot, slot: str) -> PillarValue | None:
    """Return a pillar when it exists. Hour may be absent."""
    if slot == "year":
        return snapshot.pillars.year
    if slot == "month":
        return snapshot.pillars.month
    if slot == "day":
        return snapshot.pillars.day
    return snapshot.pillars.hour


def useful_elements(useful: UsefulGodSnapshot) -> tuple[FiveElement, ...]:
    """Return useful-god elements copied from the snapshot."""
    elements: list[FiveElement] = []
    for item in useful.useful or ():
        if item.element is not None and item.element not in elements:
            elements.append(item.element)
    return tuple(elements)


def favorable_elements(useful: UsefulGodSnapshot) -> tuple[FiveElement, ...]:
    """Return favorable elements copied from the snapshot."""
    elements: list[FiveElement] = []
    for item in useful.favorable or ():
        if item.element is not None and item.element not in elements:
            elements.append(item.element)
    return tuple(elements)


def unfavorable_elements(useful: UsefulGodSnapshot) -> tuple[FiveElement, ...]:
    """Return unfavorable elements copied from the snapshot."""
    elements: list[FiveElement] = []
    for item in useful.unfavorable or ():
        if item.element is not None and item.element not in elements:
            elements.append(item.element)
    return tuple(elements)


def useful_roles(useful: UsefulGodSnapshot) -> tuple[str, ...]:
    """Return useful/favorable role names."""
    names: list[str] = []
    for item in (*(useful.useful or ()), *(useful.favorable or ())):
        if item.role and item.role not in names:
            names.append(item.role)
    return tuple(names)


def unfavorable_roles(useful: UsefulGodSnapshot) -> tuple[str, ...]:
    """Return unfavorable role names."""
    names: list[str] = []
    for item in useful.unfavorable or ():
        if item.role and item.role not in names:
            names.append(item.role)
    return tuple(names)


def element_present(snapshot: MarriageCanonicalSnapshot, element: FiveElement) -> bool:
    """Return True when Canonical five-element distribution shows the element."""
    amount = snapshot.five_elements.distribution.get(element, 0.0)
    if amount > 0.0:
        return True
    if snapshot.day_master.element is element:
        return True
    if stem_element(snapshot.day_master.stem) is element:
        return True
    return False


def ten_god_items(snapshot: MarriageCanonicalSnapshot) -> tuple[TenGodItem, ...]:
    """Return visible then hidden ten-god items."""
    visible = tuple(snapshot.ten_gods.visible or ())
    hidden = tuple(snapshot.ten_gods.hidden or ())
    return visible + hidden


def significance_for_slots(*slots: str) -> EvidenceSignificance:
    """Return qualitative significance from pillar slots. Not a score."""
    if "day" in slots:
        return EvidenceSignificance.MAJOR
    if "hour" in slots:
        return EvidenceSignificance.MINOR
    return EvidenceSignificance.MODERATE
