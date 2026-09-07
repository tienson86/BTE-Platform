"""Marriage snapshot builder. Select and bind Canonical Truth. No interpretation."""

from __future__ import annotations

from typing import Any, Mapping

from consulting.marriage.dto.request import CanonicalBirthInput
from consulting.marriage.exceptions import MarriageCanonicalContractError
from consulting.marriage.models.enums import FiveElement, PersonSide, TenGodVisibility
from consulting.marriage.models.person import (
    BirthDataQuality,
    CanonicalVersionReference,
    MarriagePersonReference,
)
from consulting.marriage.models.snapshot import (
    DayMasterSnapshot,
    ElementOrStemReference,
    FengShuiSnapshot,
    FiveElementSnapshot,
    LuckCycleSnapshot,
    LuckSnapshot,
    MarriageCanonicalSnapshot,
    PatternSnapshot,
    PillarSnapshot,
    PillarValue,
    ShenShaItem,
    ShenShaSnapshot,
    StrengthSnapshot,
    TenGodItem,
    TenGodSnapshot,
    UsefulGodSnapshot,
)
from consulting.marriage.runtime.canonical_labels import (
    map_five_element,
    map_yin_yang,
    try_map_five_element,
)
from consulting.marriage.runtime.phase import QUALITY_FLAG_COUNT


def build_marriage_snapshot(
    *,
    analysis: Mapping[str, Any],
    person: CanonicalBirthInput,
    analysis_id: str,
    side: PersonSide,
) -> MarriageCanonicalSnapshot:
    """Bind a marriage snapshot from a Canonical analysis envelope."""
    if side not in (PersonSide.A, PersonSide.B):
        raise MarriageCanonicalContractError("invalid_person_side")
    payload = _canonical_payload(analysis)
    hour_known = bool(analysis.get("hour_known", person.birth_time is not None))
    bazi = _require_mapping(payload, "bazi")
    return MarriageCanonicalSnapshot(
        person=_person_reference(
            person=person,
            analysis_id=analysis_id,
            payload=payload,
            hour_known=hour_known,
        ),
        pillars=_pillars(bazi, hour_known=hour_known),
        day_master=_day_master(bazi),
        five_elements=_five_elements(payload.get("five_elements")),
        strength=_strength(payload.get("strength")),
        pattern=_pattern(payload.get("pattern")),
        useful_god=_useful_god(payload.get("useful_god")),
        ten_gods=_ten_gods(payload.get("ten_gods")),
        source_analysis_id=analysis_id,
        luck=_luck(payload.get("luck")),
        shen_sha=_shen_sha(bazi),
        feng_shui=_feng_shui(payload.get("feng_shui"), payload.get("calendar")),
    )


def _canonical_payload(analysis: Mapping[str, Any]) -> Mapping[str, Any]:
    """Return the Canonical payload from a TV-01 analysis envelope."""
    nested = analysis.get("canonical")
    if isinstance(nested, Mapping):
        return nested
    if "bazi" in analysis:
        return analysis
    raise MarriageCanonicalContractError("canonical_payload_missing")


def _require_mapping(payload: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    """Return a required mapping field."""
    value = payload.get(key)
    if not isinstance(value, Mapping):
        raise MarriageCanonicalContractError(f"canonical_field_missing:{key}")
    return value


def _person_reference(
    *,
    person: CanonicalBirthInput,
    analysis_id: str,
    payload: Mapping[str, Any],
    hour_known: bool,
) -> MarriagePersonReference:
    """Build a person reference. Completeness is input quality, not score."""
    place_known = person.birth_place is not None
    timezone_resolved = person.timezone is not None
    flags = (True, hour_known, place_known, timezone_resolved)
    limitations: list[str] = []
    if not hour_known:
        limitations.append("birth_time_unknown")
    if not place_known:
        limitations.append("birth_place_unknown")
    if not timezone_resolved:
        limitations.append("timezone_unspecified")
    versions = CanonicalVersionReference(
        calendar_version=_source_token(payload.get("calendar")),
        bazi_version=_source_token(payload.get("bazi_source")),
        strength_version=_source_token(payload.get("strength_source")),
        pattern_version=_source_token(payload.get("pattern_source")),
        useful_god_version=_source_token(payload.get("useful_god_source")),
        ten_gods_version=_source_token(payload.get("ten_gods_source")),
        luck_version=_source_token(payload.get("luck")),
    )
    return MarriagePersonReference(
        analysis_id=analysis_id,
        gender=person.gender,
        birth_data_quality=BirthDataQuality(
            birth_date_known=True,
            birth_time_known=hour_known,
            birth_place_known=place_known,
            timezone_resolved=timezone_resolved,
            completeness_score=sum(1 for flag in flags if flag) / QUALITY_FLAG_COUNT,
            limitations=limitations,
        ),
        canonical_version=versions,
        display_name=person.full_name,
    )


def _source_token(value: Any) -> str | None:
    """Extract a version/source token when Canonical published one."""
    if isinstance(value, Mapping):
        for key in ("contract", "engine", "version"):
            token = value.get(key)
            if token:
                return str(token)
        return None
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _pillars(bazi: Mapping[str, Any], *, hour_known: bool) -> PillarSnapshot:
    """Copy four pillars. Hour is omitted when birth time was unknown."""
    return PillarSnapshot(
        year=_pillar(bazi, "year_pillar"),
        month=_pillar(bazi, "month_pillar"),
        day=_pillar(bazi, "day_pillar"),
        hour=_pillar(bazi, "hour_pillar") if hour_known else None,
    )


def _pillar(bazi: Mapping[str, Any], key: str) -> PillarValue:
    """Copy one Canonical pillar."""
    raw = bazi.get(key)
    if not isinstance(raw, Mapping):
        raise MarriageCanonicalContractError(f"canonical_pillar_missing:{key}")
    stem = str(raw.get("stem") or "")
    branch = str(raw.get("branch") or "")
    if not stem or not branch:
        raise MarriageCanonicalContractError(f"canonical_pillar_incomplete:{key}")
    hidden = raw.get("hidden_stems")
    hidden_stems = [str(item) for item in hidden] if isinstance(hidden, list) else None
    return PillarValue(
        stem=stem,
        branch=branch,
        can_chi=f"{stem} {branch}".strip(),
        hidden_stems=hidden_stems,
        ten_god=str(raw.get("ten_god") or "") or None,
        growth_stage=str(raw.get("truong_sinh") or "") or None,
        na_yin=str(raw.get("nap_am") or "") or None,
    )


def _day_master(bazi: Mapping[str, Any]) -> DayMasterSnapshot:
    """Copy day master from Canonical BaZi."""
    stem = str(bazi.get("day_master") or "")
    if not stem:
        raise MarriageCanonicalContractError("canonical_day_master_missing")
    return DayMasterSnapshot(
        stem=stem,
        element=map_five_element(str(bazi.get("day_master_element") or "")),
        yin_yang=map_yin_yang(str(bazi.get("day_master_yin_yang") or "")),
    )


def _five_elements(raw: Any) -> FiveElementSnapshot:
    """Copy five-element distribution. Does not classify dominant/weak/absent."""
    payload = raw if isinstance(raw, Mapping) else {}
    counts = payload.get("counts") if isinstance(payload.get("counts"), Mapping) else payload
    distribution = {}
    for element in FiveElement:
        value = counts.get(element.value) if isinstance(counts, Mapping) else None
        distribution[element] = float(value) if value is not None else 0.0
    return FiveElementSnapshot(distribution=distribution)


def _strength(raw: Any) -> StrengthSnapshot:
    """Copy Canonical strength classification."""
    payload = raw if isinstance(raw, Mapping) else {}
    classification = str(payload.get("strength_level") or payload.get("classification") or "")
    if not classification:
        raise MarriageCanonicalContractError("canonical_strength_missing")
    score = payload.get("strength_score", payload.get("score"))
    confidence = payload.get("confidence")
    return StrengthSnapshot(
        classification=classification,
        score=float(score) if score is not None else None,
        confidence=float(confidence) if confidence is not None else None,
    )


def _pattern(raw: Any) -> PatternSnapshot:
    """Copy Canonical pattern identity. Does not reinterpret."""
    payload = raw if isinstance(raw, Mapping) else {}
    return PatternSnapshot(
        pattern_id=str(payload.get("pattern") or "") or None,
        pattern_name=str(payload.get("cach_cuc") or payload.get("pattern_name") or "") or None,
        grade=str(payload.get("qualification_level") or "") or None,
        purity=str(payload.get("tong_cach") or "") or None,
        status=str(payload.get("success_reason") or "") or None,
    )


def _useful_god(raw: Any) -> UsefulGodSnapshot:
    """Copy Useful / Favorable / Unfavorable references. Roles stay separate."""
    payload = raw if isinstance(raw, Mapping) else {}
    useful = [
        ElementOrStemReference(
            element=try_map_five_element(str(payload.get("useful_element") or "")),
            stem=str(payload.get("useful_stem") or "") or None,
            role=str(payload.get("useful_god") or payload.get("useful_ten_god") or "") or None,
        )
    ]
    return UsefulGodSnapshot(
        useful=useful,
        favorable=_role_refs(payload.get("favorable_roles")),
        unfavorable=_role_refs(payload.get("unfavorable_roles")),
        temperature_need=str(payload.get("climate_preference_label") or "") or None,
        confidence=float(payload["confidence"]) if payload.get("confidence") is not None else None,
    )


def _role_refs(raw: Any) -> list[ElementOrStemReference] | None:
    """Copy Canonical role lists without collapsing them."""
    if not isinstance(raw, list):
        return None
    refs: list[ElementOrStemReference] = []
    for item in raw:
        if not isinstance(item, Mapping):
            continue
        refs.append(
            ElementOrStemReference(
                element=try_map_five_element(str(item.get("element") or "")),
                stem=str(item.get("stem") or "") or None,
                role=str(item.get("ten_god") or item.get("role") or "") or None,
            )
        )
    return refs


def _ten_gods(raw: Any) -> TenGodSnapshot:
    """Copy Canonical ten-god items."""
    payload = raw if isinstance(raw, Mapping) else {}
    return TenGodSnapshot(
        visible=_ten_god_items(payload.get("visible"), TenGodVisibility.VISIBLE),
        hidden=_ten_god_items(payload.get("hidden"), TenGodVisibility.HIDDEN),
    )


def _ten_god_items(raw: Any, visibility: TenGodVisibility) -> list[TenGodItem] | None:
    """Copy one ten-god list."""
    if not isinstance(raw, list):
        return None
    items: list[TenGodItem] = []
    for item in raw:
        if not isinstance(item, Mapping):
            continue
        name = str(item.get("ten_god") or item.get("name") or "")
        if not name:
            continue
        items.append(
            TenGodItem(
                name=name,
                source_pillar=str(item.get("pillar") or "") or None,
                source_stem=str(item.get("stem") or item.get("hidden_stem") or "") or None,
                visibility=visibility,
            )
        )
    return items


def _luck(raw: Any) -> LuckSnapshot | None:
    """Copy luck cycles when Canonical published them. Does not recalculate."""
    if not isinstance(raw, Mapping):
        return None
    cycles: list[LuckCycleSnapshot] = []
    for item in raw.get("cycles") or []:
        cycle = _luck_cycle(item)
        if cycle is not None:
            cycles.append(cycle)
    current = _luck_cycle(raw.get("current_cycle"))
    if not cycles and current is None:
        return LuckSnapshot(cycles=[], current_cycle=None)
    return LuckSnapshot(cycles=cycles, current_cycle=current)


def _luck_cycle(raw: Any) -> LuckCycleSnapshot | None:
    """Copy one luck cycle when year bounds exist."""
    if not isinstance(raw, Mapping):
        return None
    start = raw.get("year_start", raw.get("start_year"))
    end = raw.get("year_end", raw.get("end_year"))
    stem = str(raw.get("stem") or "")
    branch = str(raw.get("branch") or "")
    can_chi = str(raw.get("gan_zhi") or raw.get("can_chi") or f"{stem} {branch}").strip()
    if start is None or end is None or not can_chi:
        return None
    return LuckCycleSnapshot(
        index=int(raw.get("index") or 0),
        start_year=int(start),
        end_year=int(end),
        can_chi=can_chi,
        stem=stem,
        branch=branch,
    )


def _shen_sha(bazi: Mapping[str, Any]) -> ShenShaSnapshot | None:
    """Copy Shen Sha names. Secondary evidence only."""
    matches = bazi.get("shensha_matches")
    items: list[ShenShaItem] = []
    if isinstance(matches, list):
        for item in matches:
            if not isinstance(item, Mapping):
                continue
            name = str(item.get("canonical_name") or item.get("name") or "")
            if not name:
                continue
            items.append(
                ShenShaItem(
                    name=name,
                    id=str(item.get("id") or "") or None,
                    pillar=str(item.get("pillar") or "") or None,
                )
            )
    names = bazi.get("shensha")
    if not items and isinstance(names, list):
        items = [ShenShaItem(name=str(name)) for name in names if str(name)]
    if not items:
        return None
    return ShenShaSnapshot(items=items)


def _feng_shui(feng: Any, calendar: Any) -> FengShuiSnapshot | None:
    """Copy Feng Shui reference fields. Not primary evidence."""
    payload = feng if isinstance(feng, Mapping) else {}
    calendar_payload = calendar if isinstance(calendar, Mapping) else {}
    cung = str(payload.get("cung_phi") or calendar_payload.get("cung_phi") or "") or None
    group = str(
        payload.get("nhom_trach")
        or payload.get("house_group")
        or calendar_payload.get("nhom_trach")
        or calendar_payload.get("house_group")
        or ""
    ) or None
    element = try_map_five_element(str(payload.get("element") or payload.get("hanh") or ""))
    if cung is None and group is None and element is None:
        return None
    return FengShuiSnapshot(cung_phi=cung, element=element, group=group)
