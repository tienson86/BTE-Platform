"""Read natal domains and upstream Đại Vận. Does not rebuild luck pillars."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from engines.bazi_engine.ten_god import ten_god_name
from engines.detailed_interpretation_engine.context_layers import CanonicalAnalysisContext
from engines.detailed_interpretation_engine.domains import DomainInterpretationResult, DomainSection
from engines.detailed_interpretation_engine.luck_activation.constants import GOD_TO_FAMILY
from engines.detailed_interpretation_engine.ten_gods.constants import LABEL_TO_GOD_ID


@dataclass(frozen=True, slots=True)
class LuckCycleFacts:
    """Canonical current/selected Đại Vận identity from LuckEngine."""

    cycle_id: str
    gan_zhi: str
    stem: str
    branch: str
    stem_element: str
    branch_element: str
    year_start: str
    year_end: str
    time_window: str
    index: int


@dataclass(frozen=True, slots=True)
class LuckActivationFacts:
    """Inputs Luck Activation may explain. Natal objects are copied, not mutated."""

    analysis_id: str
    cycle: LuckCycleFacts | None
    day_master: str
    temporal_ten_god_label: str
    temporal_god_id: str
    temporal_family: str
    useful_god_element: str
    useful_god_match: bool
    support_elements: tuple[str, ...]
    attack_elements: tuple[str, ...]
    damage_types: tuple[str, ...]
    has_rescue: bool
    domains: DomainSection
    natal: dict[str, DomainInterpretationResult]


def collect_luck_activation_facts(
    context: CanonicalAnalysisContext,
    payload: Mapping[str, Any] | None,
) -> LuckActivationFacts:
    """Copy LuckEngine current cycle plus natal domain snapshots."""
    data = _as_map(payload)
    luck = _as_map(data.get("luck"))
    cycle = _cycle(luck)
    day_master = _day_master(data)
    label = ten_god_name(day_master, cycle.stem) if cycle and day_master and cycle.stem else ""
    god_id = LABEL_TO_GOD_ID.get(label, "")
    family = GOD_TO_FAMILY.get(god_id, "")
    useful = _useful_element(data)
    luck_elements = (cycle.stem_element, cycle.branch_element) if cycle else ()
    match = bool(useful and any(item == useful for item in luck_elements if item))
    section = context.runtime.domains
    natal = _natal_map(section)
    damage = _damage(data)
    rescue = _rescue(data)
    return LuckActivationFacts(
        analysis_id=context.analysis_id,
        cycle=cycle,
        day_master=day_master,
        temporal_ten_god_label=label,
        temporal_god_id=god_id,
        temporal_family=family,
        useful_god_element=useful,
        useful_god_match=match,
        support_elements=_string_tuple(luck.get("support_elements")),
        attack_elements=_string_tuple(luck.get("attack_elements")),
        damage_types=damage,
        has_rescue=bool(rescue),
        domains=section,
        natal=natal,
    )


def _cycle(luck: Mapping[str, Any]) -> LuckCycleFacts | None:
    raw = luck.get("selected_cycle")
    if not isinstance(raw, Mapping):
        raw = luck.get("current_cycle")
    if not isinstance(raw, Mapping):
        return None
    stem = str(raw.get("stem") or raw.get("heavenly_stem") or "").strip()
    branch = str(raw.get("branch") or raw.get("earthly_branch") or "").strip()
    gan_zhi = str(raw.get("gan_zhi") or raw.get("ganzhi") or "").strip() or f"{stem} {branch}".strip()
    if not gan_zhi:
        return None
    year_start = str(raw.get("year_start") or raw.get("start_year") or "").strip()
    year_end = str(raw.get("year_end") or raw.get("end_year") or "").strip()
    window = f"{year_start}–{year_end}" if year_start and year_end else ""
    index = int(raw.get("index") or 0)
    return LuckCycleFacts(
        cycle_id=f"dai_van:{index}:{gan_zhi.replace(' ', '')}",
        gan_zhi=gan_zhi,
        stem=stem,
        branch=branch,
        stem_element=str(raw.get("stem_element") or "").strip(),
        branch_element=str(raw.get("branch_element") or "").strip(),
        year_start=year_start,
        year_end=year_end,
        time_window=window,
        index=index,
    )


def _day_master(payload: Mapping[str, Any]) -> str:
    pattern = _as_map(payload.get("pattern"))
    stem = str(pattern.get("day_master") or pattern.get("day_stem") or "").strip()
    if stem:
        return stem
    identity = _as_map(payload.get("identity"))
    pillars = _as_map(identity.get("four_pillars"))
    day = _as_map(pillars.get("day"))
    stem = str(day.get("stem") or "").strip()
    if stem:
        return stem
    bazi = _as_map(payload.get("bazi"))
    day = _as_map(bazi.get("day"))
    if not day:
        day = _as_map(bazi.get("day_pillar"))
    return str(day.get("stem") or bazi.get("day_master") or "").strip()


_ELEMENT_TOKENS: tuple[str, ...] = ("Kim", "Mộc", "Thủy", "Hỏa", "Thổ")


def _useful_element(payload: Mapping[str, Any]) -> str:
    useful = _as_map(payload.get("useful_god"))
    text = str(
        useful.get("useful_element")
        or useful.get("element")
        or useful.get("useful_display")
        or ""
    ).strip()
    for token in _ELEMENT_TOKENS:
        if token in text:
            return token
    return text


def _natal_map(section: DomainSection) -> dict[str, DomainInterpretationResult]:
    items: dict[str, DomainInterpretationResult] = {
        "authority": section.authority.natal,
        "career": section.career.natal,
        "wealth": section.wealth.natal,
        "relationship": section.relationship.natal,
        "legacy": section.legacy.natal,
        "vitality": section.vitality.natal,
    }
    items.update(section.supporting)
    return items


def _damage(payload: Mapping[str, Any]) -> tuple[str, ...]:
    mingju = _as_map(payload.get("mingju"))
    raw = mingju.get("damage") or payload.get("damage_ids") or ()
    if isinstance(raw, str):
        return (raw,)
    items: list[str] = []
    for item in raw:
        if isinstance(item, Mapping):
            value = str(item.get("damage_type") or item.get("id") or "").strip()
        else:
            value = str(item).strip()
        if value:
            items.append(value)
    return tuple(items)


def _rescue(payload: Mapping[str, Any]) -> tuple[str, ...]:
    mingju = _as_map(payload.get("mingju"))
    raw = mingju.get("rescue") or payload.get("rescue_ids") or ()
    if isinstance(raw, str):
        return (raw,) if raw else ()
    items: list[str] = []
    for item in raw:
        if isinstance(item, Mapping):
            value = str(item.get("rescue_type") or item.get("id") or "").strip()
        else:
            value = str(item).strip()
        if value:
            items.append(value)
    return tuple(items)


def _as_map(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _string_tuple(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,) if value.strip() else ()
    return tuple(str(item) for item in value if str(item).strip())
