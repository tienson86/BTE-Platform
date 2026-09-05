"""Build ReportInputV1 from a stored Analyze payload. No engine recalculation."""

from __future__ import annotations

from typing import Any, Mapping

from applications.api.services.five_elements_truth import ELEMENT_KEYS
from applications.api.services.luck_truth import shape_luck_payload
from applications.api.services.result_identity import (
    CUSTOMER_USEFUL_GOD_CONTRACT,
    RELEASE_LABEL,
)
from applications.api.services.ten_gods_truth import TEN_GODS_NOTE, shape_ten_gods_payload
from engines.report_engine.contracts.report_input_v1 import (
    REPORT_INPUT_VERSION,
    ReportCalendarV1,
    ReportDiagnosticsV1,
    ReportFiveElementsV1,
    ReportInputV1,
    ReportInterpretationSectionV1,
    ReportInterpretationV1,
    ReportLuckCycleV1,
    ReportLuckCyclesV1,
    ReportMetadataV1,
    ReportPatternV1,
    ReportPillarV1,
    ReportPillarsV1,
    ReportProfileV1,
    ReportShenShaItemV1,
    ReportStrengthV1,
    ReportTenGodsV1,
    ReportUsefulGodV1,
)
from engines.report_engine.narrative_binding import (
    extract_canonical_sections,
    is_usable_narrative_result,
)
from engines.report_engine.rendering.customer_facing import strip_internal_rule_ids
from engines.useful_god_engine.presentation import (
    INSUFFICIENT_CUSTOMER_FAVORABLE_DISPLAY,
    KY_SCOPE_NOTE,
)

CUSTOMER_PRESENTATION_CONTRACT = "report.customer.PresentedReportV1@1.0"
CUSTOMER_REPORT_CONTRACT = "report.customer.v1"

_STRENGTH_LABELS = {
    "weak": "Thân nhược",
    "balanced": "Thân cân bằng",
    "strong": "Thân vượng",
    "very_weak": "Thân nhược",
    "very_strong": "Thân vượng",
}

_FORBIDDEN_PATTERN_PHRASES = (
    "Chuyên cách ưu tiên Ấn",
    "chuyên cách ưu tiên Ấn",
    "Giá Sắc tuyệt đối",
    "chuyên cách hoàn chỉnh",
    "chuyên cách quyết định Dụng",
)


def build_customer_report_input(
    *,
    analysis_id: str,
    data: Mapping[str, Any],
    birth_input: Mapping[str, Any] | None = None,
    generated_at: str = "",
) -> ReportInputV1:
    """Map a stored customer analysis dict onto ReportInputV1.

    Copies published facts only. Does not recompute Gate-1 engines.
    """
    payload = dict(data)
    birth = dict(birth_input or {})
    diagnostics = ReportDiagnosticsV1(
        source_contracts=[
            CUSTOMER_USEFUL_GOD_CONTRACT,
            CUSTOMER_PRESENTATION_CONTRACT,
            CUSTOMER_REPORT_CONTRACT,
        ],
    )
    return ReportInputV1(
        metadata=_metadata(analysis_id, payload, generated_at),
        profile=_profile(payload, birth),
        calendar=_calendar(payload, birth, diagnostics),
        pillars=_pillars(payload, diagnostics),
        five_elements=_five_elements(payload, diagnostics),
        strength=_strength(payload, diagnostics),
        ten_gods=_ten_gods(payload, diagnostics),
        pattern=_pattern(payload, diagnostics),
        useful_god=_useful_god(payload, diagnostics),
        shensha=_shensha(payload, diagnostics),
        luck_cycles=_luck(payload, diagnostics),
        interpretation=_interpretation(payload, diagnostics),
        diagnostics=diagnostics,
    )


def _metadata(analysis_id: str, data: Mapping[str, Any], generated_at: str) -> ReportMetadataV1:
    meta = _map(data.get("result_meta"))
    created = generated_at or _text(meta.get("created_at"))
    return ReportMetadataV1(
        report_version=REPORT_INPUT_VERSION,
        generated_at=created or ReportMetadataV1().generated_at,
        engine_version=RELEASE_LABEL,
        knowledge_version=CUSTOMER_REPORT_CONTRACT,
        case_id=analysis_id,
        locale="vi-VN",
        timezone=_text(data.get("timezone") or meta.get("timezone") or "Asia/Bangkok"),
    )


def _profile(data: Mapping[str, Any], birth: Mapping[str, Any]) -> ReportProfileV1:
    customer = _map(data.get("customer"))
    year = birth.get("year")
    month = birth.get("month")
    day = birth.get("day")
    birth_date = _text(customer.get("birth_date") or birth.get("birth_date"))
    if not birth_date and year and month and day:
        birth_date = f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
    hour = birth.get("hour")
    minute = birth.get("minute")
    birth_time = _text(customer.get("birth_time") or birth.get("birth_time"))
    if not birth_time and hour is not None:
        birth_time = f"{int(hour):02d}:{int(minute or 0):02d}"
    return ReportProfileV1(
        full_name=_text(customer.get("full_name") or birth.get("full_name") or birth.get("name")),
        gender=_text(customer.get("gender") or birth.get("gender")),
        birth_date=birth_date,
        birth_time=birth_time,
        birth_place=_text(customer.get("birth_place") or birth.get("birth_place")),
        timezone=_text(customer.get("timezone") or birth.get("timezone") or "Asia/Bangkok"),
    )


def _calendar(
    data: Mapping[str, Any],
    birth: Mapping[str, Any],
    diagnostics: ReportDiagnosticsV1,
) -> ReportCalendarV1:
    payload = _map(data.get("calendar"))
    lunar = _map(payload.get("lunar"))
    solar = _map(payload.get("solar"))
    lunar_year = lunar.get("year", payload.get("lunar_year"))
    lunar_month = lunar.get("month", payload.get("lunar_month"))
    lunar_day = lunar.get("day", payload.get("lunar_day"))
    leap = bool(lunar.get("is_leap_month") or payload.get("leap_month"))
    lunar_date = _text(payload.get("lunar_date"))
    if not lunar_date and lunar_day is not None and lunar_month is not None and lunar_year is not None:
        lunar_date = f"{int(lunar_day):02d}/{int(lunar_month):02d}/{int(lunar_year):04d}"
        if leap:
            lunar_date = f"{lunar_date} nhuận"
    solar_date = _text(payload.get("solar_date") or payload.get("date"))
    if not solar_date and solar:
        solar_date = (
            f"{int(solar.get('day') or 0):02d}/"
            f"{int(solar.get('month') or 0):02d}/"
            f"{int(solar.get('year') or 0):04d}"
        )
    if not solar_date and birth.get("year"):
        solar_date = f"{int(birth['day']):02d}/{int(birth['month']):02d}/{int(birth['year']):04d}"
    solar_term_raw = payload.get("solar_term") or payload.get("jieqi") or ""
    solar_term = (
        _text(_map(solar_term_raw).get("name"))
        if isinstance(solar_term_raw, Mapping)
        else _text(solar_term_raw)
    )
    tz_payload = payload.get("timezone")
    timezone = _text(_map(tz_payload).get("name")) if isinstance(tz_payload, Mapping) else ""
    timezone = timezone or _text(payload.get("timezone_name") or birth.get("timezone"))
    lunar_can_chi = _map(payload.get("lunar_can_chi"))
    calendar = ReportCalendarV1(
        solar_date=solar_date,
        lunar_date=lunar_date,
        lunar_year=_as_int(lunar_year),
        lunar_month=_as_int(lunar_month),
        lunar_day=_as_int(lunar_day),
        leap_month=leap,
        lunar_year_can_chi=_text(
            lunar_can_chi.get("year") or lunar.get("year_can_chi") or payload.get("lunar_year_can_chi")
        ),
        solar_term=solar_term,
        solar_term_datetime=_text(payload.get("solar_term_datetime")),
        calendar_mode=_text(payload.get("calendar_mode") or "solar_utc7"),
        timezone=timezone,
        cung_phi=_text(payload.get("cung_phi")),
        menh_quai=_text(payload.get("menh_quai")),
        hanh_cung=_text(payload.get("hanh_cung")),
        nhom_trach=_text(payload.get("nhom_trach")),
    )
    if not calendar.lunar_date:
        diagnostics.missing_fields.append("calendar.lunar_date")
    return calendar


def _pillars(data: Mapping[str, Any], diagnostics: ReportDiagnosticsV1) -> ReportPillarsV1:
    bazi = _map(data.get("bazi"))
    if not bazi:
        diagnostics.missing_fields.append("pillars")
        return ReportPillarsV1()
    return ReportPillarsV1(
        year=_pillar(bazi.get("year_pillar")),
        month=_pillar(bazi.get("month_pillar")),
        day=_pillar(bazi.get("day_pillar")),
        hour=_pillar(bazi.get("hour_pillar")),
    )


def _pillar(raw: Any) -> ReportPillarV1:
    item = _map(raw)
    hidden = item.get("hidden_stems") or []
    if not isinstance(hidden, list):
        hidden = []
    return ReportPillarV1(
        stem=_text(item.get("stem")),
        branch=_text(item.get("branch")),
        hidden_stems=[_text(value) for value in hidden if value],
        na_yin=_text(item.get("nap_am") or item.get("na_yin")),
        ten_god=_text(item.get("ten_god")),
        truong_sinh=_text(item.get("truong_sinh")),
    )


def _five_elements(
    data: Mapping[str, Any],
    diagnostics: ReportDiagnosticsV1,
) -> ReportFiveElementsV1:
    published = _map(data.get("five_elements"))
    counts = _map(published.get("counts"))
    raw: dict[str, Any] = {}
    for key in ELEMENT_KEYS:
        value = counts.get(key)
        if value is None:
            entry = published.get(key)
            if isinstance(entry, Mapping):
                value = entry.get("count")
            elif isinstance(entry, (int, float)):
                value = entry
        if value is not None:
            raw[key] = value
    if not raw:
        diagnostics.missing_fields.append("five_elements")
    return ReportFiveElementsV1(
        wood=_as_float(raw.get("wood")),
        fire=_as_float(raw.get("fire")),
        earth=_as_float(raw.get("earth")),
        metal=_as_float(raw.get("metal")),
        water=_as_float(raw.get("water")),
        raw={key: raw.get(key) for key in ELEMENT_KEYS},
        normalized={},
        percentages={},
    )


def _strength(data: Mapping[str, Any], diagnostics: ReportDiagnosticsV1) -> ReportStrengthV1:
    strength = _map(data.get("strength"))
    bazi = _map(data.get("bazi"))
    if not strength:
        diagnostics.missing_fields.append("strength")
        return ReportStrengthV1(day_master=_text(bazi.get("day_master")))
    level_key = _text(strength.get("strength_level")).lower()
    label = _STRENGTH_LABELS.get(level_key, _text(strength.get("strength_level")))
    return ReportStrengthV1(
        day_master=_text(bazi.get("day_master") or strength.get("day_master")),
        score=_as_float(strength.get("strength_score")),
        level=label,
        classification=label,
        seasonal_support=_as_float(strength.get("season_score")),
        root_support=_as_float(strength.get("root_score")),
        summary=_text(strength.get("evidence_compact") or strength.get("reasoning")),
    )


def _ten_gods(data: Mapping[str, Any], diagnostics: ReportDiagnosticsV1) -> ReportTenGodsV1:
    raw = data.get("ten_gods") or data.get("ten_gods_result")
    if not raw:
        diagnostics.missing_fields.append("ten_gods")
        return ReportTenGodsV1(note=TEN_GODS_NOTE)
    shaped = shape_ten_gods_payload(raw if isinstance(raw, Mapping) else {})
    visible = [dict(item) for item in (shaped.get("visible") or []) if isinstance(item, Mapping)]
    hidden = [dict(item) for item in (shaped.get("hidden") or []) if isinstance(item, Mapping)]
    return ReportTenGodsV1(
        visible=list(shaped.get("visible_labels") or []),
        hidden=list(shaped.get("hidden_labels") or []),
        summary=_text(shaped.get("summary")),
        visible_entries=visible,
        hidden_entries=hidden,
        visible_summary=_text(shaped.get("visible_summary")),
        hidden_summary=_text(shaped.get("hidden_summary")),
        note=_text(shaped.get("note")) or TEN_GODS_NOTE,
    )


def _pattern(data: Mapping[str, Any], diagnostics: ReportDiagnosticsV1) -> ReportPatternV1:
    pattern = _map(data.get("pattern"))
    if not pattern:
        diagnostics.missing_fields.append("pattern")
        return ReportPatternV1()
    primary = _text(pattern.get("cach_cuc") or pattern.get("pattern"))
    evidence = strip_internal_rule_ids(_text(pattern.get("evidence_compact")))
    for phrase in _FORBIDDEN_PATTERN_PHRASES:
        evidence = evidence.replace(phrase, "")
    override = bool(pattern.get("ug_override_eligible"))
    level = _as_int(pattern.get("qualification_level"))
    if level == 1 and not override:
        evidence = evidence.replace("ưu tiên Ấn", "").strip(" .")
    secondary: list[str] = []
    tong = _text(pattern.get("tong_cach"))
    if tong:
        secondary.append(tong)
    return ReportPatternV1(
        primary_pattern=primary,
        secondary_patterns=secondary,
        follow_pattern=tong,
        status="success" if pattern.get("success") else "unknown",
        confidence=None,
        explanation=evidence,
    )


def _useful_god(data: Mapping[str, Any], diagnostics: ReportDiagnosticsV1) -> ReportUsefulGodV1:
    useful = _map(data.get("useful_god"))
    temperature = _map(data.get("temperature"))
    if not useful:
        diagnostics.missing_fields.append("useful_god")
        return ReportUsefulGodV1(
            favorable_display=INSUFFICIENT_CUSTOMER_FAVORABLE_DISPLAY,
        )
    hy = _text(useful.get("favorable_display")) or INSUFFICIENT_CUSTOMER_FAVORABLE_DISPLAY
    return ReportUsefulGodV1(
        useful_god=_text(useful.get("useful_god")),
        useful_ten_god=_text(useful.get("useful_ten_god")),
        useful_stem=_text(useful.get("useful_stem")),
        useful_element=_text(useful.get("useful_element")),
        useful_display=_text(useful.get("useful_display")),
        favorable_gods=list(useful.get("favorable_gods") or []),
        unfavorable_gods=list(useful.get("unfavorable_gods") or []),
        favorable_roles=[dict(item) for item in (useful.get("favorable_roles") or []) if isinstance(item, Mapping)],
        unfavorable_roles=[
            dict(item) for item in (useful.get("unfavorable_roles") or []) if isinstance(item, Mapping)
        ],
        favorable_display=hy,
        unfavorable_display=_text(useful.get("unfavorable_display")),
        winning_rule_id=_text(useful.get("winning_rule_id")),
        winning_rule_group=_text(useful.get("winning_rule_group")),
        overall_incomplete=bool(useful.get("overall_incomplete")),
        climate_preference_label=_text(useful.get("climate_preference_label")),
        climate_candidate=_text(useful.get("climate_candidate")),
        climate_display=_text(useful.get("climate_display")),
        climate_rule_id=_text(useful.get("climate_rule_id")),
        climate_rule_group=_text(useful.get("climate_rule_group")),
        short_reason=_text(useful.get("short_reason")),
        reason_archetype=_text(useful.get("reason_archetype")),
        hy_role_status=_text(useful.get("hy_role_status")),
        ky_scope_note=_text(useful.get("ky_scope_note")) or KY_SCOPE_NOTE,
        temperature_adjustment=_text(temperature.get("climate_state") or temperature.get("temperature_level")),
        balancing_need=_text(temperature.get("balancing_need")),
        climate_evidence=_text(temperature.get("evidence_compact")),
        reasoning=_text(useful.get("short_reason") or useful.get("reasoning")),
    )


def _shensha(data: Mapping[str, Any], diagnostics: ReportDiagnosticsV1) -> list[ReportShenShaItemV1]:
    bazi = _map(data.get("bazi"))
    matches = bazi.get("shensha_matches") or []
    items: list[ReportShenShaItemV1] = []
    if isinstance(matches, list):
        for match in matches:
            if not isinstance(match, Mapping):
                continue
            name = _text(match.get("canonical_name") or match.get("name"))
            if not name:
                continue
            items.append(
                ReportShenShaItemV1(
                    id=_text(match.get("id")),
                    name=name,
                    category="shensha",
                    present=True,
                    evidence=_text(match.get("evidence_text")),
                    source_type=_text(match.get("source_type")),
                    source_value=_text(match.get("source_value")),
                    target_type=_text(match.get("target_type")),
                    target_value=_text(match.get("target_value")),
                    pillar=_text(match.get("pillar")),
                    location=_text(match.get("location")),
                    presence_label=_text(match.get("presence_label")),
                    aliases=[],
                    rule_source=_text(match.get("rule_source")),
                    occurrences=[
                        dict(item)
                        for item in (match.get("occurrences") or [])
                        if isinstance(item, Mapping)
                    ],
                )
            )
    if not items:
        names = bazi.get("shensha") or []
        if isinstance(names, list):
            items = [
                ReportShenShaItemV1(
                    id=f"shensha_{index + 1}",
                    name=_text(name),
                    category="shensha",
                    present=True,
                )
                for index, name in enumerate(names)
                if _text(name)
            ]
    if not items:
        diagnostics.missing_fields.append("shensha")
    return items


def _luck(data: Mapping[str, Any], diagnostics: ReportDiagnosticsV1) -> ReportLuckCyclesV1:
    payload = _map(data.get("luck"))
    if not payload:
        diagnostics.missing_fields.append("luck_cycles")
        return ReportLuckCyclesV1()
    shaped = payload if "cycles" in payload else shape_luck_payload(payload)
    cycles_raw = shaped.get("cycles") or []
    cycles: list[ReportLuckCycleV1] = []
    if isinstance(cycles_raw, list):
        for item in cycles_raw:
            if not isinstance(item, Mapping):
                continue
            cycles.append(
                ReportLuckCycleV1(
                    index=int(item.get("index") or 0),
                    start_year=_as_int(item.get("year_start") or item.get("start_year")),
                    end_year=_as_int(item.get("year_end") or item.get("end_year")),
                    stem=_text(item.get("stem") or item.get("heavenly_stem")),
                    branch=_text(item.get("branch") or item.get("earthly_branch")),
                    age_start=_as_int(item.get("age_start") or item.get("start_age")),
                    age_end=_as_int(item.get("age_end") or item.get("end_age")),
                    summary=_text(item.get("gan_zhi") or item.get("ganzhi") or item.get("summary")),
                )
            )
    if not cycles:
        diagnostics.missing_fields.append("luck_cycles.cycles")
    current = _map(shaped.get("current_cycle"))
    return ReportLuckCyclesV1(
        direction=_text(shaped.get("direction")),
        start_age=_as_int(shaped.get("start_age")),
        start_date=_text(shaped.get("start_date")),
        cycles=cycles,
        evidence=_text(shaped.get("evidence")),
        method_note=_text(shaped.get("method_note")),
        precision=_text(shaped.get("precision")),
        current_gan_zhi=_text(current.get("gan_zhi") or current.get("summary")),
        current_year_start=_as_int(current.get("year_start")),
        current_year_end=_as_int(current.get("year_end")),
        current_age_start=_as_int(current.get("age_start")),
        current_age_end=_as_int(current.get("age_end")),
    )


def _interpretation(
    data: Mapping[str, Any],
    diagnostics: ReportDiagnosticsV1,
) -> ReportInterpretationV1:
    narrative = data.get("narrative_result")
    if not is_usable_narrative_result(narrative):
        diagnostics.missing_fields.append("narrative_result")
        return ReportInterpretationV1()
    extracted = extract_canonical_sections(dict(narrative))
    sections = [
        ReportInterpretationSectionV1(
            id=_text(item.get("id")),
            title=_text(item.get("title")),
            content=_text(item.get("body")),
            priority=index + 1,
        )
        for index, item in enumerate(extracted)
    ]
    by_id = {item.id: item for item in sections}
    recommendation = by_id.get("sec-recommendation")
    warning = by_id.get("sec-warning")
    recs = [
        paragraph.strip()
        for paragraph in (recommendation.content.split("\n\n") if recommendation else [])
        if paragraph.strip()
    ]
    return ReportInterpretationV1(
        executive_summary=_text(by_id["sec-executive_summary"].content)
        if "sec-executive_summary" in by_id
        else "",
        sections=sections,
        conclusion=_text(by_id["sec-conclusion"].content) if "sec-conclusion" in by_id else "",
        recommendations=recs,
        warnings=[warning.content] if warning and warning.content else [],
    )


def _map(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


def _text(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def _as_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _as_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
