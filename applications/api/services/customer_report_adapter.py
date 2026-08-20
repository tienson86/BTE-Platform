"""Map a stored Analyze payload onto ReportInputV1 without re-analysis.

Customer export must consume Frozen AnalysisResult JSON, never recompute
Dụng / Hỷ / Strength / Pattern. Presentation adapter only.
"""

from __future__ import annotations

from typing import Any, Mapping

from applications.api.services.five_elements_truth import ELEMENT_KEYS
from applications.api.services.luck_truth import shape_luck_payload
from applications.api.services.result_identity import (
    CUSTOMER_USEFUL_GOD_CONTRACT,
    GATE_CORE_FREEZE,
    RELEASE_LABEL,
)
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
from engines.report_engine.foundation_constants import REPORT_VERSION
from engines.useful_god_engine.presentation import (
    INSUFFICIENT_CUSTOMER_FAVORABLE_DISPLAY,
    KY_SCOPE_NOTE,
)

_OVERRIDE_CLAIM_MARKERS = (
    "chuyên cách ưu tiên ấn",
    "chuyên cách hoàn chỉnh",
    "chuyên cách quyết định dụng",
    "giá sắc tuyệt đối",
)


def build_customer_report_input(
    *,
    data: Mapping[str, Any],
    analysis_id: str,
    birth_input: Mapping[str, Any] | None = None,
    source: str = "current",
) -> ReportInputV1:
    """Build the canonical customer presentation model from stored Analyze data."""
    payload = dict(data)
    birth = dict(birth_input or {})
    diagnostics = ReportDiagnosticsV1(
        source_contracts=[
            "applications.api.analyze.data",
            CUSTOMER_USEFUL_GOD_CONTRACT,
            "pack05_narrative_result_v1",
        ]
    )
    return ReportInputV1(
        metadata=_metadata(payload, analysis_id, birth, source),
        profile=_profile(payload, birth),
        calendar=_calendar(payload, birth),
        pillars=_pillars(payload),
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


def _metadata(
    data: Mapping[str, Any],
    analysis_id: str,
    birth: Mapping[str, Any],
    source: str,
) -> ReportMetadataV1:
    meta = _as_map(data.get("result_meta"))
    timezone = str(
        birth.get("timezone")
        or _as_map(data.get("calendar")).get("timezone_name")
        or "Asia/Bangkok"
    )
    return ReportMetadataV1(
        report_version=REPORT_INPUT_VERSION,
        engine_version=REPORT_VERSION,
        knowledge_version=str(
            meta.get("release_label") or RELEASE_LABEL or GATE_CORE_FREEZE
        ),
        case_id=analysis_id,
        locale="vi-VN",
        timezone=timezone,
    )


def _profile(data: Mapping[str, Any], birth: Mapping[str, Any]) -> ReportProfileV1:
    customer = _as_map(data.get("customer"))
    year = _as_int(birth.get("year"))
    month = _as_int(birth.get("month"))
    day = _as_int(birth.get("day"))
    hour = _as_int(birth.get("hour")) or 0
    minute = _as_int(birth.get("minute")) or 0
    birth_date = ""
    if year and month and day:
        birth_date = f"{day:02d}/{month:02d}/{year:04d}"
    return ReportProfileV1(
        full_name=str(customer.get("full_name") or birth.get("full_name") or ""),
        gender=str(
            customer.get("gender")
            or birth.get("gender")
            or _as_map(data.get("bazi")).get("gender")
            or ""
        ),
        birth_date=birth_date,
        birth_time=f"{hour:02d}:{minute:02d}",
        birth_place=str(customer.get("birth_place") or birth.get("birth_place") or ""),
        timezone=str(customer.get("timezone") or birth.get("timezone") or "Asia/Bangkok"),
    )


def _calendar(data: Mapping[str, Any], birth: Mapping[str, Any]) -> ReportCalendarV1:
    calendar = _as_map(data.get("calendar"))
    lunar = _as_map(calendar.get("lunar"))
    solar = _as_map(calendar.get("solar"))
    feng = _as_map(data.get("feng_shui"))
    lunar_year = lunar.get("year", calendar.get("lunar_year"))
    lunar_month = lunar.get("month", calendar.get("lunar_month"))
    lunar_day = lunar.get("day", calendar.get("lunar_day"))
    leap = bool(
        lunar.get("is_leap_month")
        or lunar.get("leap")
        or calendar.get("is_leap_month")
        or calendar.get("leap_month")
    )
    lunar_date = str(calendar.get("lunar_date") or "")
    if not lunar_date and lunar_day is not None and lunar_month is not None and lunar_year is not None:
        lunar_date = f"{int(lunar_day):02d}/{int(lunar_month):02d}/{int(lunar_year):04d}"
        if leap:
            lunar_date = f"{lunar_date} nhuận"
    solar_date = str(calendar.get("solar_date") or calendar.get("date") or "")
    if not solar_date and solar:
        solar_date = (
            f"{int(solar.get('day') or 0):02d}/"
            f"{int(solar.get('month') or 0):02d}/"
            f"{int(solar.get('year') or 0):04d}"
        )
    if not solar_date:
        year = _as_int(birth.get("year"))
        month = _as_int(birth.get("month"))
        day = _as_int(birth.get("day"))
        if year and month and day:
            solar_date = f"{day:02d}/{month:02d}/{year:04d}"
    solar_term_raw = calendar.get("solar_term") or calendar.get("jieqi") or ""
    if isinstance(solar_term_raw, Mapping):
        solar_term = str(solar_term_raw.get("name") or "")
    else:
        solar_term = str(solar_term_raw)
    tz_payload = calendar.get("timezone")
    timezone = ""
    if isinstance(tz_payload, Mapping):
        timezone = str(tz_payload.get("name") or "")
    timezone = timezone or str(calendar.get("timezone_name") or birth.get("timezone") or "")
    lunar_can_chi = (
        calendar.get("lunar_can_chi")
        if isinstance(calendar.get("lunar_can_chi"), Mapping)
        else {}
    )
    return ReportCalendarV1(
        solar_date=solar_date,
        lunar_date=lunar_date,
        lunar_year=_as_int(lunar_year),
        lunar_month=_as_int(lunar_month),
        lunar_day=_as_int(lunar_day),
        leap_month=leap,
        lunar_year_can_chi=str(
            lunar_can_chi.get("year")
            or lunar.get("year_can_chi")
            or calendar.get("lunar_year_can_chi")
            or ""
        ),
        solar_term=solar_term,
        solar_term_datetime=str(
            calendar.get("solar_term_datetime") or calendar.get("jieqi_datetime") or ""
        ),
        calendar_mode=str(calendar.get("calendar_mode") or calendar.get("mode") or "solar_utc7"),
        timezone=timezone,
        cung_phi=str(feng.get("cung_phi") or calendar.get("cung_phi") or ""),
        menh_quai=str(feng.get("menh_quai") or calendar.get("menh_quai") or ""),
        nhom_trach=str(feng.get("nhom_trach") or calendar.get("nhom_trach") or ""),
    )


def _pillars(data: Mapping[str, Any]) -> ReportPillarsV1:
    bazi = _as_map(data.get("bazi"))
    return ReportPillarsV1(
        year=_pillar(bazi.get("year_pillar")),
        month=_pillar(bazi.get("month_pillar")),
        day=_pillar(bazi.get("day_pillar")),
        hour=_pillar(bazi.get("hour_pillar")),
    )


def _pillar(raw: Any) -> ReportPillarV1:
    payload = _as_map(raw)
    hidden = payload.get("hidden_stems") or []
    if not isinstance(hidden, list):
        hidden = []
    return ReportPillarV1(
        stem=str(payload.get("stem") or ""),
        branch=str(payload.get("branch") or ""),
        hidden_stems=[str(item) for item in hidden if item],
        na_yin=str(payload.get("nap_am") or payload.get("na_yin") or ""),
        ten_god=str(payload.get("ten_god") or ""),
        truong_sinh=str(payload.get("truong_sinh") or ""),
    )


def _five_elements(
    data: Mapping[str, Any],
    diagnostics: ReportDiagnosticsV1,
) -> ReportFiveElementsV1:
    published = _as_map(data.get("five_elements"))
    counts = published.get("counts") if isinstance(published.get("counts"), Mapping) else {}
    raw: dict[str, Any] = {}
    for key in ELEMENT_KEYS:
        value = counts.get(key) if counts else None
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
    )


def _strength(
    data: Mapping[str, Any],
    diagnostics: ReportDiagnosticsV1,
) -> ReportStrengthV1:
    strength = _as_map(data.get("strength"))
    bazi = _as_map(data.get("bazi"))
    if not strength:
        diagnostics.missing_fields.append("strength")
        return ReportStrengthV1(day_master=str(bazi.get("day_master") or ""))
    return ReportStrengthV1(
        day_master=str(strength.get("day_master") or bazi.get("day_master") or ""),
        score=_as_float(strength.get("strength_score")),
        level=str(strength.get("strength_level") or ""),
        classification=str(strength.get("strength_level") or ""),
        seasonal_support=_as_float(strength.get("season_score")),
        root_support=_as_float(strength.get("root_score")),
        summary=str(strength.get("reasoning") or ""),
    )


def _ten_gods(
    data: Mapping[str, Any],
    diagnostics: ReportDiagnosticsV1,
) -> ReportTenGodsV1:
    payload = _as_map(data.get("ten_gods") or data.get("ten_gods_result"))
    bazi = _as_map(data.get("bazi"))
    visible_entries = [
        dict(item) for item in (payload.get("visible") or []) if isinstance(item, Mapping)
    ]
    hidden_entries = [
        dict(item) for item in (payload.get("hidden") or []) if isinstance(item, Mapping)
    ]
    visible_labels = [
        str(item) for item in (payload.get("visible_labels") or bazi.get("ten_gods") or []) if item
    ]
    if not visible_labels and visible_entries:
        visible_labels = [
            str(item.get("ten_god") or item.get("label") or "")
            for item in visible_entries
            if item.get("ten_god") or item.get("label")
        ]
    hidden_stems = [str(item) for item in (bazi.get("hidden_stems") or []) if item]
    if hidden_entries and not hidden_stems:
        hidden_stems = [
            str(item.get("hidden_stem") or item.get("stem") or "")
            for item in hidden_entries
            if item.get("hidden_stem") or item.get("stem")
        ]
    if not visible_labels and not hidden_stems and not visible_entries:
        diagnostics.missing_fields.append("ten_gods")
    return ReportTenGodsV1(
        visible=visible_labels,
        hidden=hidden_stems,
        summary=", ".join(visible_labels) if visible_labels else "",
        visible_entries=visible_entries,
        hidden_entries=hidden_entries,
        visible_summary=str(payload.get("visible_summary") or ""),
        hidden_summary=str(payload.get("hidden_summary") or ""),
        note=str(payload.get("note") or ""),
    )


def _pattern(
    data: Mapping[str, Any],
    diagnostics: ReportDiagnosticsV1,
) -> ReportPatternV1:
    pattern = _as_map(data.get("pattern"))
    if not pattern:
        diagnostics.missing_fields.append("pattern")
        return ReportPatternV1()
    primary = str(pattern.get("cach_cuc") or pattern.get("pattern") or "")
    tong = str(pattern.get("tong_cach") or "")
    follow = tong if _is_follow_pattern_label(tong) else ""
    override = bool(pattern.get("ug_override_eligible"))
    explanation = str(pattern.get("success_reason") or pattern.get("evidence_compact") or "")
    if not override and _claims_special_override(explanation):
        explanation = primary
    elif not explanation:
        explanation = primary
    return ReportPatternV1(
        primary_pattern=primary,
        secondary_patterns=[tong] if tong and tong != primary else [],
        follow_pattern=follow,
        status="success" if pattern.get("success") else "unknown",
        confidence=_as_float(pattern.get("score")),
        explanation=explanation,
    )


def _useful_god(
    data: Mapping[str, Any],
    diagnostics: ReportDiagnosticsV1,
) -> ReportUsefulGodV1:
    useful = _as_map(data.get("useful_god"))
    temperature = _as_map(data.get("temperature"))
    if not useful:
        diagnostics.missing_fields.append("useful_god")
        return ReportUsefulGodV1()
    hy_status = str(useful.get("hy_role_status") or "")
    favorable_display = str(useful.get("favorable_display") or "")
    if not favorable_display and hy_status and hy_status != "SUPPORTED_INDEPENDENT_ROLE":
        favorable_display = INSUFFICIENT_CUSTOMER_FAVORABLE_DISPLAY
    return ReportUsefulGodV1(
        useful_god=str(useful.get("useful_god") or ""),
        useful_ten_god=str(useful.get("useful_ten_god") or ""),
        useful_stem=str(useful.get("useful_stem") or ""),
        useful_element=str(useful.get("useful_element") or ""),
        useful_display=str(useful.get("useful_display") or useful.get("useful_god") or ""),
        favorable_gods=list(useful.get("favorable_gods") or []),
        unfavorable_gods=list(useful.get("unfavorable_gods") or []),
        favorable_roles=[
            dict(item) for item in (useful.get("favorable_roles") or []) if isinstance(item, Mapping)
        ],
        unfavorable_roles=[
            dict(item)
            for item in (useful.get("unfavorable_roles") or [])
            if isinstance(item, Mapping)
        ],
        favorable_display=favorable_display or INSUFFICIENT_CUSTOMER_FAVORABLE_DISPLAY,
        unfavorable_display=str(
            useful.get("unfavorable_display")
            or ", ".join(str(item) for item in (useful.get("unfavorable_gods") or []) if item)
        ),
        winning_rule_id=str(useful.get("winning_rule_id") or ""),
        winning_rule_group=str(useful.get("winning_rule_group") or ""),
        overall_incomplete=bool(useful.get("overall_incomplete")),
        climate_preference_label=str(useful.get("climate_preference_label") or ""),
        climate_candidate=str(useful.get("climate_candidate") or ""),
        climate_display=str(useful.get("climate_display") or ""),
        climate_rule_id=str(useful.get("climate_rule_id") or ""),
        climate_rule_group=str(useful.get("climate_rule_group") or ""),
        short_reason=str(useful.get("short_reason") or ""),
        reason_archetype=str(useful.get("reason_archetype") or ""),
        hy_role_status=hy_status,
        ky_scope_note=str(useful.get("ky_scope_note") or KY_SCOPE_NOTE),
        temperature_adjustment=str(
            temperature.get("climate_state") or temperature.get("temperature_level") or ""
        ),
        balancing_need=str(temperature.get("balancing_need") or ""),
        climate_evidence=str(temperature.get("evidence_compact") or ""),
        reasoning=str(useful.get("short_reason") or useful.get("reasoning") or ""),
    )


def _shensha(
    data: Mapping[str, Any],
    diagnostics: ReportDiagnosticsV1,
) -> list[ReportShenShaItemV1]:
    bazi = _as_map(data.get("bazi"))
    matches = bazi.get("shensha_matches") or data.get("shensha_matches") or []
    names = bazi.get("shensha") or []
    if not matches and not names:
        diagnostics.missing_fields.append("shensha")
        return []
    if isinstance(matches, list) and matches:
        items: list[ReportShenShaItemV1] = []
        for item in matches:
            payload = _as_map(item)
            items.append(
                ReportShenShaItemV1(
                    id=str(payload.get("id") or ""),
                    name=str(payload.get("canonical_name") or payload.get("name") or ""),
                    category="shensha",
                    present=True,
                    evidence=str(payload.get("evidence_text") or ""),
                    source_type=str(payload.get("source_type") or ""),
                    source_value=str(payload.get("source_value") or ""),
                    target_type=str(payload.get("target_type") or ""),
                    target_value=str(payload.get("target_value") or ""),
                    pillar=str(payload.get("pillar") or ""),
                    location=str(payload.get("location") or ""),
                    presence_label=str(payload.get("presence_label") or ""),
                    aliases=[str(alias) for alias in (payload.get("aliases") or []) if alias],
                    rule_source=str(payload.get("rule_source") or ""),
                    occurrences=[
                        dict(occ)
                        for occ in (payload.get("occurrences") or [])
                        if isinstance(occ, dict)
                    ],
                )
            )
        return items
    return [
        ReportShenShaItemV1(
            id=f"shensha_{index + 1}",
            name=str(name),
            category="shensha",
            present=True,
        )
        for index, name in enumerate(names)
        if name
    ]


def _luck(
    data: Mapping[str, Any],
    diagnostics: ReportDiagnosticsV1,
) -> ReportLuckCyclesV1:
    payload = _as_map(data.get("luck"))
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
                    stem=str(item.get("stem") or item.get("heavenly_stem") or ""),
                    branch=str(item.get("branch") or item.get("earthly_branch") or ""),
                    age_start=_as_int(item.get("age_start") or item.get("start_age")),
                    age_end=_as_int(item.get("age_end") or item.get("end_age")),
                    summary=str(item.get("gan_zhi") or item.get("ganzhi") or item.get("summary") or ""),
                )
            )
    if not cycles:
        diagnostics.missing_fields.append("luck_cycles.cycles")
    current = shaped.get("current_cycle") or {}
    if not isinstance(current, Mapping):
        current = {}
    return ReportLuckCyclesV1(
        direction=str(shaped.get("direction") or ""),
        start_age=_as_int(shaped.get("start_age")),
        start_date=str(shaped.get("start_date") or ""),
        cycles=cycles,
        evidence=str(shaped.get("evidence") or ""),
        method_note=str(shaped.get("method_note") or ""),
        precision=str(shaped.get("precision") or ""),
        current_gan_zhi=str(current.get("gan_zhi") or ""),
        current_year_start=_as_int(current.get("year_start")),
        current_year_end=_as_int(current.get("year_end")),
        current_age_start=_as_int(current.get("age_start")),
        current_age_end=_as_int(current.get("age_end")),
    )


def _interpretation(
    data: Mapping[str, Any],
    diagnostics: ReportDiagnosticsV1,
) -> ReportInterpretationV1:
    narrative = _as_map(data.get("narrative_result"))
    if not narrative:
        diagnostics.missing_fields.append("narrative_result")
        return ReportInterpretationV1()
    summary = _as_map(narrative.get("summary"))
    exec_sum = _as_map(narrative.get("commercial_executive_summary"))
    executive = (
        str(exec_sum.get("composed_text") or "")
        or str(summary.get("identity") or "")
        or str(exec_sum.get("central_message") or "")
    )
    sections: list[ReportInterpretationSectionV1] = []
    for item in narrative.get("sections") or []:
        if not isinstance(item, Mapping):
            continue
        paragraphs: list[str] = []
        for para in item.get("paragraphs") or []:
            if isinstance(para, Mapping):
                paragraphs.append(str(para.get("text") or ""))
            else:
                paragraphs.append(str(para))
        content = "\n".join(part for part in paragraphs if part)
        sections.append(
            ReportInterpretationSectionV1(
                id=str(item.get("id") or ""),
                title=str(item.get("title") or ""),
                content=content,
            )
        )
    recommendations: list[str] = []
    for rec in narrative.get("recommendations") or []:
        if isinstance(rec, Mapping):
            text = str(rec.get("action") or rec.get("text") or "")
        else:
            text = str(rec)
        if text:
            recommendations.append(text)
    conclusion = ""
    warnings: list[str] = []
    for section in sections:
        title = section.title.lower()
        sid = section.id.lower()
        if not conclusion and ("kết luận" in title or sid == "conclusion"):
            conclusion = section.content
        if "lưu ý" in title or "warning" in sid:
            warnings.append(section.content)
    if not executive and not sections:
        diagnostics.missing_fields.append("narrative_result.content")
    return ReportInterpretationV1(
        executive_summary=executive,
        sections=sections,
        conclusion=conclusion or str(exec_sum.get("conclusion") or ""),
        recommendations=recommendations,
        warnings=warnings,
    )


def _is_follow_pattern_label(value: str) -> bool:
    token = value.strip().lower()
    return token.startswith("tòng") or token.startswith("tong")


def _claims_special_override(text: str) -> bool:
    lowered = text.lower()
    return any(marker in lowered for marker in _OVERRIDE_CLAIM_MARKERS)


def _as_map(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


def _as_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _as_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
