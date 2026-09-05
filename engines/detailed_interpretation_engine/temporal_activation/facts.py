"""Read canonical annual identity plus luck envelope. Does not rebuild Gan-Zhi."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from engines.bazi_engine.ten_god import ten_god_name
from engines.detailed_interpretation_engine.context_layers import CanonicalAnalysisContext
from engines.detailed_interpretation_engine.domains import DomainInterpretationResult, DomainSection
from engines.detailed_interpretation_engine.evidence import EvidencePriorityResult
from engines.detailed_interpretation_engine.luck_activation.constants import GOD_TO_FAMILY
from engines.detailed_interpretation_engine.luck_activation.facts import (
    _as_map,
    _damage,
    _day_master,
    _natal_map,
    _rescue,
    _string_tuple,
    _useful_element,
)
from engines.detailed_interpretation_engine.temporal import LuckActivationResult, LuckInteractionResult
from engines.detailed_interpretation_engine.temporal_activation.constants import (
    ANNUAL_SOURCE_PATH,
    RELATION_KINDS,
)
from engines.detailed_interpretation_engine.ten_gods.constants import LABEL_TO_GOD_ID


@dataclass(frozen=True, slots=True)
class AnnualLayerFacts:
    """Canonical current-year identity from LuckEngine Liunian. Not a Pack 07 recalculation."""

    year: str
    civil_year: str
    gan_zhi: str
    stem: str
    branch: str
    stem_element: str
    branch_element: str
    ten_god_label: str
    god_id: str
    family: str
    source_identity: str
    relations: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class TemporalActivationContext:
    """Inputs Temporal Activation may explain. Upstream objects are copied, not mutated."""

    analysis_id: str
    natal_domains: DomainSection
    luck_cycle_result: LuckActivationResult
    luck_interaction_result: LuckInteractionResult
    annual: AnnualLayerFacts | None
    natal: dict[str, DomainInterpretationResult]
    evidence_priority: EvidencePriorityResult
    day_master: str
    useful_god_element: str
    useful_god_match: bool
    element_action: str
    damage_types: tuple[str, ...]
    has_rescue: bool
    requested_layers: tuple[str, ...]
    active_ruleset: str
    source_versions: tuple[str, ...]


def collect_temporal_activation_facts(
    context: CanonicalAnalysisContext,
    payload: Mapping[str, Any] | None,
) -> TemporalActivationContext:
    """Copy LuckEngine annual identity plus natal/luck snapshots."""
    data = _as_map(payload)
    luck = _as_map(data.get("luck"))
    annual = _annual(luck, _as_map(data.get("_luck_raw")))
    day_master = _day_master(data)
    useful = _useful_element(data)
    label = ""
    god_id = ""
    family = ""
    match = False
    element_action = ""
    if annual is not None:
        label = (
            ten_god_name(day_master, annual.stem)
            if day_master and annual.stem
            else annual.ten_god_label
        )
        god_id = LABEL_TO_GOD_ID.get(label, "")
        family = GOD_TO_FAMILY.get(god_id, "")
        annual_elements = tuple(item for item in (annual.stem_element, annual.branch_element) if item)
        match = bool(useful and any(item == useful for item in annual_elements))
        element_action = _element_action(annual_elements, useful)
        annual = AnnualLayerFacts(
            year=annual.year,
            civil_year=annual.civil_year,
            gan_zhi=annual.gan_zhi,
            stem=annual.stem,
            branch=annual.branch,
            stem_element=annual.stem_element,
            branch_element=annual.branch_element,
            ten_god_label=label or annual.ten_god_label,
            god_id=god_id,
            family=family,
            source_identity=annual.source_identity or ANNUAL_SOURCE_PATH,
            relations=annual.relations,
        )
    section = context.runtime.domains
    return TemporalActivationContext(
        analysis_id=context.analysis_id,
        natal_domains=section,
        luck_cycle_result=context.runtime.temporal.luck_activation,
        luck_interaction_result=context.runtime.temporal.luck_interaction,
        annual=annual,
        natal=_natal_map(section),
        evidence_priority=context.runtime.interpretation.evidence_priority,
        day_master=day_master,
        useful_god_element=useful,
        useful_god_match=match,
        element_action=element_action,
        damage_types=_damage(data),
        has_rescue=bool(_rescue(data)),
        requested_layers=("luck_cycle", "annual"),
        active_ruleset="temporal_activation",
        source_versions=(ANNUAL_SOURCE_PATH,),
    )


def _annual(luck: Mapping[str, Any], raw: Mapping[str, Any]) -> AnnualLayerFacts | None:
    for candidate in (
        luck.get("annual_identity"),
        luck.get("current_liunian"),
        raw.get("current_liunian"),
        luck.get("annual"),
    ):
        parsed = _annual_from_mapping(candidate)
        if parsed is not None:
            return parsed
    return None


def _annual_from_mapping(candidate: Any) -> AnnualLayerFacts | None:
    if not isinstance(candidate, Mapping):
        return None
    stem = str(candidate.get("stem") or candidate.get("heavenly_stem") or "").strip()
    branch = str(candidate.get("branch") or candidate.get("earthly_branch") or "").strip()
    gan_zhi = str(candidate.get("gan_zhi") or candidate.get("ganzhi") or "").strip()
    if not gan_zhi:
        gan_zhi = f"{stem} {branch}".strip()
    if not stem and gan_zhi:
        parts = gan_zhi.split()
        if len(parts) >= 2:
            stem, branch = parts[0], parts[1]
            gan_zhi = f"{stem} {branch}"
    if not gan_zhi:
        return None
    raw_meta = candidate.get("metadata")
    metadata: Mapping[str, Any] = raw_meta if isinstance(raw_meta, Mapping) else {}
    year = str(candidate.get("year") or metadata.get("bazi_year") or "").strip()
    civil = str(candidate.get("civil_year") or metadata.get("civil_year") or year).strip()
    if not year and not civil:
        return None
    relations = _relations(candidate.get("relations") or metadata.get("relations"))
    return AnnualLayerFacts(
        year=year or civil,
        civil_year=civil or year,
        gan_zhi=gan_zhi,
        stem=stem,
        branch=branch,
        stem_element=str(candidate.get("stem_element") or candidate.get("element") or "").strip(),
        branch_element=str(candidate.get("branch_element") or "").strip(),
        ten_god_label=str(candidate.get("ten_god") or "").strip(),
        god_id="",
        family="",
        source_identity=str(candidate.get("source") or ANNUAL_SOURCE_PATH).strip() or ANNUAL_SOURCE_PATH,
        relations=relations,
    )


def _relations(value: Any) -> tuple[str, ...]:
    items = _string_tuple(value)
    return tuple(item for item in items if item in RELATION_KINDS)


def _element_action(annual_elements: tuple[str, ...], useful: str) -> str:
    if not useful:
        return ""
    from engines.detailed_interpretation_engine.temporal_activation.constants import (
        ELEMENT_CONTROLS,
        ELEMENT_GENERATES,
    )

    for element in annual_elements:
        if element == useful:
            return "support"
        if ELEMENT_GENERATES.get(element) == useful:
            return "generate"
        if ELEMENT_GENERATES.get(useful) == element:
            return "drain"
        if ELEMENT_CONTROLS.get(element) == useful:
            return "control"
        if ELEMENT_CONTROLS.get(useful) == element:
            return "stress"
    return ""
