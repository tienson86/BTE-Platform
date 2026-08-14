"""Build domain InterpretationFacts from canonical context and engine sources."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from engines.interpretation_engine.foundation.builders.engine_sources import EngineSources
from engines.interpretation_engine.foundation.canonical_context import CanonicalAnalysisContext
from engines.interpretation_engine.foundation import diagnostics as diag
from engines.interpretation_engine.foundation.facts.five_elements import FiveElementsInterpretationFacts
from engines.interpretation_engine.foundation.facts.luck import LuckCycleFact, LuckInterpretationFacts
from engines.interpretation_engine.foundation.facts.pattern import PatternInterpretationFacts
from engines.interpretation_engine.foundation.facts.shensha import ShenShaInterpretationFacts, ShenShaItemFact
from engines.interpretation_engine.foundation.facts.strength import StrengthInterpretationFacts
from engines.interpretation_engine.foundation.facts.temperature import TemperatureInterpretationFacts
from engines.interpretation_engine.foundation.facts.ten_gods import TenGodInterpretationFacts, TenGodPositionFact
from engines.interpretation_engine.foundation.facts.useful_god import (
    UsefulGodCandidateFact,
    UsefulGodInterpretationFacts,
)
from engines.interpretation_engine.foundation.status import DataAvailability, EvidenceStatus

_SEASON_VI: dict[str, str] = {
    "spring": "Xuân",
    "summer": "Hạ",
    "autumn": "Thu",
    "winter": "Đông",
}


@dataclass(frozen=True, slots=True)
class InterpretationFactsBundle:
    """All domain facts for one chart."""

    strength: StrengthInterpretationFacts
    pattern: PatternInterpretationFacts
    useful_god: UsefulGodInterpretationFacts
    ten_gods: TenGodInterpretationFacts
    shensha: ShenShaInterpretationFacts
    luck: LuckInterpretationFacts
    temperature: TemperatureInterpretationFacts
    five_elements: FiveElementsInterpretationFacts

    def to_dict(self) -> dict[str, Any]:
        """Serialize all domain facts."""
        return {
            "strength": self.strength.to_dict(),
            "pattern": self.pattern.to_dict(),
            "useful_god": self.useful_god.to_dict(),
            "ten_gods": self.ten_gods.to_dict(),
            "shensha": self.shensha.to_dict(),
            "luck": self.luck.to_dict(),
            "temperature": self.temperature.to_dict(),
            "five_elements": self.five_elements.to_dict(),
        }


def build_interpretation_facts(
    context: CanonicalAnalysisContext,
    *,
    luck_payload: Mapping[str, Any] | None = None,
    engine_sources: EngineSources | None = None,
    pattern_dieu_hau: str = "",
) -> InterpretationFactsBundle:
    """Project canonical context onto domain interpretation facts."""
    return InterpretationFactsBundle(
        strength=_build_strength_facts(context),
        pattern=_build_pattern_facts(context),
        useful_god=_build_useful_god_facts(context, engine_sources),
        ten_gods=_build_ten_god_facts(context, engine_sources),
        shensha=_build_shensha_facts(context, engine_sources),
        luck=_build_luck_facts(context, luck_payload),
        temperature=_build_temperature_facts(context, pattern_dieu_hau),
        five_elements=_build_five_elements_facts(context),
    )


def _build_strength_facts(context: CanonicalAnalysisContext) -> StrengthInterpretationFacts:
    """Build strength facts from StrengthEngine slice."""
    strength = context.strength
    diagnostics: list[str] = []
    if not strength.level:
        diagnostics.append(diag.STRENGTH_TRUTH_MISSING)
    status = DataAvailability.AVAILABLE if strength.level else DataAvailability.MISSING
    return StrengthInterpretationFacts(
        level=strength.level,
        score=strength.score,
        label=strength.label,
        confidence=strength.confidence,
        evidence=strength.evidence,
        rule_ids=strength.rule_ids,
        status=status,
        diagnostics=tuple(diagnostics),
    )


def _build_pattern_facts(context: CanonicalAnalysisContext) -> PatternInterpretationFacts:
    """Build pattern facts from PatternEngine slice."""
    pattern = context.pattern
    diagnostics: list[str] = []
    if not pattern.selected:
        diagnostics.append(diag.PATTERN_TRUTH_MISSING)
    status = DataAvailability.AVAILABLE if pattern.selected else DataAvailability.MISSING
    return PatternInterpretationFacts(
        selected=pattern.selected,
        label=pattern.label,
        confidence=pattern.confidence,
        evidence=pattern.evidence,
        rule_ids=pattern.rule_ids,
        status=status,
        diagnostics=tuple(diagnostics),
    )


def _build_useful_god_facts(
    context: CanonicalAnalysisContext,
    engine_sources: EngineSources | None,
) -> UsefulGodInterpretationFacts:
    """Build useful-god facts including candidates when engine source present."""
    useful = context.useful_god
    diagnostics: list[str] = []
    candidates: list[UsefulGodCandidateFact] = []
    candidate_type = ""

    pattern_ctx = engine_sources.pattern_context if engine_sources else None
    month_branch = ""
    season = ""
    if pattern_ctx is not None:
        month_branch = str(getattr(pattern_ctx, "month_branch", "") or "")
        raw_season = str(getattr(pattern_ctx, "season", "") or "")
        season = _SEASON_VI.get(raw_season, raw_season)

    ug_result = engine_sources.useful_god_result if engine_sources else None
    if ug_result is not None:
        for item in getattr(ug_result, "candidate_list", []) or []:
            if not isinstance(item, Mapping):
                item = dict(item) if hasattr(item, "__iter__") else {}
            rule_id = str(item.get("rule_id") or "")
            candidates.append(
                UsefulGodCandidateFact(
                    useful_god=str(item.get("useful_god") or ""),
                    rule_id=rule_id,
                    confidence=float(item.get("score") or 0.0),
                    reason=str(item.get("reason") or item.get("description") or ""),
                    candidate_type=str(item.get("rule_group") or ""),
                    rule_group=str(item.get("rule_group") or ""),
                )
            )
            if rule_id == "sea_004" and not candidate_type:
                candidate_type = str(item.get("rule_group") or "season")
    elif useful.candidate_count == 0:
        diagnostics.append(diag.USEFUL_GOD_CANDIDATES_MISSING)

    if not useful.selected:
        diagnostics.append(diag.USEFUL_GOD_NOT_AVAILABLE)
    if useful.selected and not useful.reason:
        diagnostics.append(diag.USEFUL_GOD_EVIDENCE_MISSING)

    presence = DataAvailability.AVAILABLE if useful.selected else DataAvailability.MISSING
    if useful.selected and diagnostics:
        status = DataAvailability.PARTIAL
    elif useful.selected:
        status = DataAvailability.AVAILABLE
    else:
        status = DataAvailability.MISSING

    five = {
        "wood": context.five_elements.wood,
        "fire": context.five_elements.fire,
        "earth": context.five_elements.earth,
        "metal": context.five_elements.metal,
        "water": context.five_elements.water,
    }

    return UsefulGodInterpretationFacts(
        selected=useful.selected,
        candidate_type=candidate_type,
        confidence=useful.confidence,
        reason=useful.reason,
        favorable_gods=useful.favorable_gods,
        unfavorable_gods=useful.unfavorable_gods,
        candidates=tuple(candidates),
        rule_ids=useful.rule_ids,
        presence=presence,
        status=status,
        day_master=context.bazi.day_master,
        day_master_element=context.bazi.day_master_element,
        month_branch=month_branch or context.bazi.month.split()[-1] if context.bazi.month else "",
        season=season,
        strength_level=context.strength.level,
        strength_score=context.strength.score,
        temperature_level=context.temperature.level,
        five_elements=five,
        diagnostics=tuple(diagnostics),
    )


def _build_ten_god_facts(
    context: CanonicalAnalysisContext,
    engine_sources: EngineSources | None,
) -> TenGodInterpretationFacts:
    """Build Ten Gods facts with positions when TenGodsEngine output available."""
    diagnostics: list[str] = []
    visible: list[TenGodPositionFact] = []
    hidden: list[TenGodPositionFact] = []
    distribution: list[dict[str, Any]] = []

    tg = engine_sources.ten_gods_result if engine_sources else None
    if tg is not None:
        for item in tg.visible:
            visible.append(
                TenGodPositionFact(
                    name=item.ten_god,
                    pillar=item.pillar,
                    stem=item.stem,
                    branch="",
                    visibility=item.visibility,
                    relation_to_day_master=item.ten_god,
                    evidence=item.evidence,
                )
            )
        for item in tg.hidden:
            hidden.append(
                TenGodPositionFact(
                    name=item.ten_god,
                    pillar=item.pillar,
                    stem=item.hidden_stem,
                    branch=item.branch,
                    visibility="hidden",
                    relation_to_day_master=item.ten_god,
                    weight=item.weight,
                    evidence=item.evidence,
                )
            )
        for entry in tg.distribution:
            distribution.append(
                {
                    "god_id": entry.god_id,
                    "label": entry.label,
                    "occurrence_count": entry.occurrence_count,
                    "weighted_contribution": entry.weighted_contribution,
                }
            )
        status = DataAvailability.AVAILABLE if visible else DataAvailability.PARTIAL
    else:
        pillar_names = ("year", "month", "day", "hour")
        labels = context.ten_gods.visible_labels
        for index, label in enumerate(labels):
            pillar = pillar_names[index] if index < len(pillar_names) else "unknown"
            visible.append(
                TenGodPositionFact(
                    name=label,
                    pillar=pillar,
                    stem="",
                    branch="",
                    visibility="visible",
                    relation_to_day_master=label,
                )
            )
        diagnostics.append(diag.TEN_GOD_POSITIONS_MISSING)
        status = DataAvailability.PARTIAL if visible else DataAvailability.MISSING

    return TenGodInterpretationFacts(
        visible=tuple(visible),
        hidden=tuple(hidden),
        distribution=tuple(distribution),
        day_master=context.bazi.day_master,
        day_master_element=context.bazi.day_master_element,
        status=status,
        diagnostics=tuple(diagnostics),
    )


def _build_shensha_facts(
    context: CanonicalAnalysisContext,
    engine_sources: EngineSources | None,
) -> ShenShaInterpretationFacts:
    """Build Shen Sha facts — never fabricate evidence."""
    items: list[ShenShaItemFact] = []
    rule_ctx = engine_sources.rule_context if engine_sources else None
    shensha_section = dict((rule_ctx or {}).get("shensha") or {}) if rule_ctx else {}

    reserved_keys = {"available", "stars", "status", "star"}
    star_names: list[str] = []
    if shensha_section.get("stars"):
        star_names = [str(name) for name in shensha_section["stars"] if name]
    elif context.bazi.shensha_names:
        star_names = list(context.bazi.shensha_names)

    if star_names:
        for name in star_names:
            detail = _shensha_detail(shensha_section, name)
            evidence = str(detail.get("evidence") or detail.get("reason") or "")
            rule_id = str(detail.get("rule_id") or "")
            evidence_status = (
                EvidenceStatus.AVAILABLE if evidence else EvidenceStatus.UNAVAILABLE
            )
            items.append(
                ShenShaItemFact(
                    name=name,
                    position=str(detail.get("position") or ""),
                    source=str(detail.get("source") or "rule_context.shensha"),
                    rule_id=rule_id,
                    evidence=evidence,
                    evidence_status=evidence_status,
                    matched_condition=str(
                        detail.get("condition") or detail.get("status") or ""
                    ),
                )
            )
    elif shensha_section:
        # Metadata-only section without star list — do not treat keys as star names.
        for key, entry in shensha_section.items():
            if key in reserved_keys or not isinstance(entry, Mapping):
                continue
            if not str(entry.get("name") or key):
                continue
            name = str(entry.get("name") or key)
            evidence = str(entry.get("evidence") or entry.get("reason") or "")
            items.append(
                ShenShaItemFact(
                    name=name,
                    position=str(entry.get("position") or ""),
                    source="rule_context.shensha",
                    rule_id=str(entry.get("rule_id") or ""),
                    evidence=evidence,
                    evidence_status=(
                        EvidenceStatus.AVAILABLE if evidence else EvidenceStatus.UNAVAILABLE
                    ),
                    matched_condition=str(entry.get("status") or ""),
                )
            )

    diagnostics: list[str] = []
    if any(item.evidence_status == EvidenceStatus.UNAVAILABLE for item in items):
        diagnostics.append(diag.SHENSHA_EVIDENCE_UNAVAILABLE)
    status = DataAvailability.AVAILABLE if items else DataAvailability.MISSING
    if items and diagnostics:
        status = DataAvailability.PARTIAL

    return ShenShaInterpretationFacts(
        items=tuple(items),
        status=status,
        diagnostics=tuple(diagnostics),
    )


def _shensha_detail(section: Mapping[str, Any], name: str) -> Mapping[str, Any]:
    """Lookup per-star detail entry inside rule_context.shensha."""
    for key, entry in section.items():
        if not isinstance(entry, Mapping):
            continue
        if str(entry.get("name") or "") == name:
            return entry
    return {}


def _build_luck_facts(
    context: CanonicalAnalysisContext,
    luck_payload: Mapping[str, Any] | None,
) -> LuckInterpretationFacts:
    """Build luck facts from shaped luck payload."""
    luck = dict(luck_payload or {})
    diagnostics: list[str] = []
    cycles_raw = luck.get("cycles") or []
    current_raw = luck.get("current_cycle") or {}
    current_gz = str(current_raw.get("gan_zhi") or context.luck.current_gan_zhi or "")

    cycles: list[LuckCycleFact] = []
    for item in cycles_raw:
        if not isinstance(item, Mapping):
            continue
        gan_zhi = str(item.get("gan_zhi") or "")
        cycles.append(
            LuckCycleFact(
                gan_zhi=gan_zhi,
                year_start=_as_int(item.get("year_start")),
                year_end=_as_int(item.get("year_end")),
                age_start=_as_int(item.get("age_start")),
                age_end=_as_int(item.get("age_end")),
                is_current=gan_zhi == current_gz and bool(current_gz),
                index=int(item.get("index") or len(cycles)),
            )
        )

    if not cycles:
        diagnostics.append(diag.LUCK_CYCLES_MISSING)

    current_cycle = None
    for cycle in cycles:
        if cycle.is_current:
            current_cycle = cycle
            break
    if current_cycle is None and cycles and current_gz:
        for cycle in cycles:
            if cycle.gan_zhi == current_gz:
                current_cycle = cycle
                break

    status = DataAvailability.AVAILABLE if cycles else DataAvailability.MISSING
    return LuckInterpretationFacts(
        available=bool(luck.get("available", context.luck.available)),
        direction=str(luck.get("direction") or context.luck.direction),
        start_age=_as_int(luck.get("start_age", context.luck.start_age)),
        current_cycle=current_cycle,
        cycles=tuple(cycles),
        status=status,
        diagnostics=tuple(diagnostics),
    )


def _build_temperature_facts(
    context: CanonicalAnalysisContext,
    pattern_dieu_hau: str,
) -> TemperatureInterpretationFacts:
    """Build temperature facts from TemperatureEngine — flag wrong-field contamination."""
    temp = context.temperature
    diagnostics: list[str] = []
    if not temp.level:
        diagnostics.append(diag.TEMPERATURE_TRUTH_MISSING)
    if pattern_dieu_hau and pattern_dieu_hau == temp.label:
        diagnostics.append(diag.TEMPERATURE_CONTAMINATED_BY_PATTERN)

    status = DataAvailability.AVAILABLE if temp.level else DataAvailability.MISSING
    return TemperatureInterpretationFacts(
        level=temp.level,
        score=temp.score,
        label=temp.label,
        recommendations=temp.recommendations,
        evidence=(temp.label,) if temp.label else (),
        rule_ids=temp.rule_ids,
        status=status,
        diagnostics=tuple(diagnostics),
    )


def _build_five_elements_facts(context: CanonicalAnalysisContext) -> FiveElementsInterpretationFacts:
    """Build five-elements facts from analytical counts."""
    five = context.five_elements
    diagnostics: list[str] = []
    counts = (five.wood, five.fire, five.earth, five.metal, five.water)
    if all(value is None for value in counts):
        diagnostics.append(diag.FIVE_ELEMENTS_TRUTH_MISSING)
        diagnostics.append(diag.ANALYTICAL_DISTRIBUTION_UNAVAILABLE)
        status = DataAvailability.MISSING
    else:
        status = DataAvailability.AVAILABLE

    return FiveElementsInterpretationFacts(
        wood=five.wood,
        fire=five.fire,
        earth=five.earth,
        metal=five.metal,
        water=five.water,
        dominant=five.dominant,
        missing=five.missing,
        status=status,
        diagnostics=tuple(diagnostics),
    )


def _as_int(value: Any) -> int | None:
    """Coerce optional int."""
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
