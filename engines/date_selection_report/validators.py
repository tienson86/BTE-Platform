"""Integrity validation for Date Selection report foundation.

Validates completeness and consistency. Never checks astrological correctness.
"""

from __future__ import annotations

from typing import Any

from engines.date_selection_report.constants import (
    ALLOWED_CUNG,
    ALLOWED_ELEMENTS,
    ALLOWED_TRACH,
    DAY_RESULTS,
    NEGATIVE_KE_RESULTS,
    POSITIVE_KE_RESULTS,
    REPORT_SCHEMA_VERSION,
    REPORT_TYPE,
    TRACH_CODE_TO_LABEL,
)
from engines.date_selection_report.exceptions import DateSelectionReportValidationError
from engines.date_selection_report.models import DateSelectionReportModel


def require_text(value: object, field: str) -> str:
    """Return a non-empty stripped string or raise."""
    text = str(value or "").strip()
    if not text or text == "None":
        raise DateSelectionReportValidationError(f"missing {field}")
    return text


def trach_label(value: object, field: str) -> str:
    """Normalize Trach code/label to the customer-facing label."""
    key = require_text(value, field)
    label = TRACH_CODE_TO_LABEL.get(key)
    if label is None or label not in ALLOWED_TRACH:
        raise DateSelectionReportValidationError(f"invalid {field}: {key!r}")
    return label


def _in_set(value: str, allowed: frozenset[str], field: str) -> str:
    if value not in allowed:
        raise DateSelectionReportValidationError(f"invalid {field}: {value!r}")
    return value


def validate_search_result(payload: dict[str, Any]) -> None:
    """Layer 2: SearchResult must be a complete frozen analytical snapshot."""
    if not isinstance(payload, dict):
        raise DateSelectionReportValidationError("SearchResult must be an object")
    person = payload.get("person")
    if not isinstance(person, dict):
        raise DateSelectionReportValidationError("missing person")
    _validate_person_payload(person)
    month = payload.get("target_month")
    year = payload.get("target_year")
    if not isinstance(month, int) or month < 1 or month > 12:
        raise DateSelectionReportValidationError(f"invalid search month: {month!r}")
    if not isinstance(year, int) or year < 1900 or year > 2200:
        raise DateSelectionReportValidationError(f"invalid search year: {year!r}")
    dates = payload.get("dates")
    if not isinstance(dates, list) or not dates:
        raise DateSelectionReportValidationError("missing recommendations")
    person_trach = trach_label(
        person.get("trach_group_label") or person.get("trach_group"),
        "person.trach_group",
    )
    seen_days: set[str] = set()
    for index, item in enumerate(dates):
        _validate_ranked_payload(item, person_trach, index, seen_days)


def _validate_person_payload(person: dict[str, Any]) -> None:
    require_text(person.get("full_name"), "person.full_name")
    require_text(person.get("gender_label") or person.get("gender"), "person.gender")
    require_text(person.get("solar_label"), "person.birth_solar")
    require_text(person.get("lunar_label"), "person.birth_lunar")
    require_text(person.get("year_ganzhi") or person.get("ganzhi"), "person.year_ganzhi")
    _in_set(require_text(person.get("nayin"), "person.nayin"), ALLOWED_ELEMENTS, "person.nayin")
    _in_set(
        require_text(person.get("cung_phi") or person.get("cung"), "person.cung_phi"),
        ALLOWED_CUNG,
        "person.cung_phi",
    )
    trach_label(person.get("trach_group_label") or person.get("trach_group"), "person.trach_group")


def _validate_ranked_payload(
    item: object,
    person_trach: str,
    index: int,
    seen_days: set[str],
) -> None:
    if not isinstance(item, dict):
        raise DateSelectionReportValidationError(f"recommendation {index} is invalid")
    day = item.get("day")
    if not isinstance(day, dict):
        raise DateSelectionReportValidationError(f"recommendation {index} missing day")
    calendar = day.get("calendar") if isinstance(day.get("calendar"), dict) else {}
    solar = require_text(calendar.get("solar_label"), f"recommendation[{index}].solar_date")
    if solar in seen_days:
        raise DateSelectionReportValidationError(f"duplicate recommendation: {solar}")
    seen_days.add(solar)
    require_text(calendar.get("lunar_label"), f"recommendation[{index}].lunar_date")
    require_text(calendar.get("year_ganzhi"), f"recommendation[{index}].year_ganzhi")
    require_text(
        calendar.get("month_ganzhi") or day.get("month_ganzhi"),
        f"recommendation[{index}].month_ganzhi",
    )
    require_text(
        day.get("ganzhi") or calendar.get("day_ganzhi"),
        f"recommendation[{index}].day_ganzhi",
    )
    six = day.get("six_state") if isinstance(day.get("six_state"), dict) else {}
    _in_set(
        require_text(six.get("label"), f"recommendation[{index}].day_result"),
        DAY_RESULTS,
        f"recommendation[{index}].day_result",
    )
    _in_set(
        require_text(day.get("nayin"), f"recommendation[{index}].nayin"),
        ALLOWED_ELEMENTS,
        f"recommendation[{index}].nayin",
    )
    _in_set(
        require_text(day.get("cung"), f"recommendation[{index}].cung"),
        ALLOWED_CUNG,
        f"recommendation[{index}].cung",
    )
    day_trach = trach_label(
        day.get("trach_group_label") or day.get("trach_group"),
        f"recommendation[{index}].trach_group",
    )
    if day_trach != person_trach:
        raise DateSelectionReportValidationError(
            f"recommendation[{index}] trach {day_trach!r} != person {person_trach!r}"
        )
    hours = item.get("compatible_hours")
    if not isinstance(hours, list) or not hours:
        raise DateSelectionReportValidationError(
            f"recommendation[{index}] missing compatible_hours"
        )
    _validate_hours(hours, person_trach, index)


def _validate_hours(hours: list[Any], person_trach: str, rec_index: int) -> None:
    seen: set[str] = set()
    has_positive = False
    for hour_index, hour in enumerate(hours):
        if not isinstance(hour, dict):
            raise DateSelectionReportValidationError(
                f"recommendation[{rec_index}].hour[{hour_index}] is invalid"
            )
        branch = require_text(hour.get("branch"), f"hour[{hour_index}].branch")
        if branch in seen:
            raise DateSelectionReportValidationError(f"duplicate compatible hour: {branch}")
        seen.add(branch)
        require_text(
            hour.get("full_time_range") or hour.get("time_range"),
            f"hour[{hour_index}].time_range",
        )
        require_text(hour.get("ganzhi"), f"hour[{hour_index}].ganzhi")
        _in_set(
            require_text(hour.get("nayin"), f"hour[{hour_index}].nayin"),
            ALLOWED_ELEMENTS,
            f"hour[{hour_index}].nayin",
        )
        _in_set(
            require_text(hour.get("cung"), f"hour[{hour_index}].cung"),
            ALLOWED_CUNG,
            f"hour[{hour_index}].cung",
        )
        hour_trach = trach_label(
            hour.get("trach_group_label") or hour.get("trach_group"),
            f"hour[{hour_index}].trach_group",
        )
        if hour_trach != person_trach:
            raise DateSelectionReportValidationError(
                f"hour[{hour_index}] trach {hour_trach!r} != person {person_trach!r}"
            )
        if "hour_result" in hour:
            raise DateSelectionReportValidationError("hour_result is forbidden")
        slots = hour.get("positive_ke")
        if not isinstance(slots, list):
            raise DateSelectionReportValidationError(f"hour[{hour_index}] missing positive_ke")
        if _validate_positive_ke(slots, hour_index):
            has_positive = True
    if not has_positive:
        raise DateSelectionReportValidationError(
            f"recommendation[{rec_index}] missing positive times"
        )


def _validate_positive_ke(slots: list[Any], hour_index: int) -> bool:
    seen: set[tuple[object, object, object]] = set()
    found = False
    for slot in slots:
        if not isinstance(slot, dict):
            raise DateSelectionReportValidationError(f"hour[{hour_index}] positive_ke is invalid")
        index = slot.get("index")
        if not isinstance(index, int):
            raise DateSelectionReportValidationError(f"hour[{hour_index}] missing ke index")
        time_range = require_text(slot.get("time_range"), f"hour[{hour_index}].ke.time_range")
        result = require_text(slot.get("result"), f"hour[{hour_index}].ke.result")
        if result in NEGATIVE_KE_RESULTS:
            raise DateSelectionReportValidationError(f"negative ke exported: {result}")
        _in_set(result, POSITIVE_KE_RESULTS, f"hour[{hour_index}].ke.result")
        key = (index, time_range, result)
        if key in seen:
            raise DateSelectionReportValidationError("duplicate positive ke")
        seen.add(key)
        found = True
    return found


def validate_report_model(model: DateSelectionReportModel) -> None:
    """Layer 3: ReportModel must be complete before any renderer runs."""
    meta = model.metadata
    require_text(meta.report_id, "metadata.report_id")
    if meta.report_type != REPORT_TYPE:
        raise DateSelectionReportValidationError(f"invalid report_type: {meta.report_type!r}")
    if meta.report_schema_version != REPORT_SCHEMA_VERSION:
        raise DateSelectionReportValidationError(
            f"invalid schema_version: {meta.report_schema_version!r}"
        )
    require_text(meta.generated_at, "metadata.generated_at")
    require_text(meta.locale, "metadata.locale")
    require_text(meta.title, "metadata.title")
    require_text(meta.generator, "metadata.generator")
    person = model.person
    for field in (
        "full_name",
        "gender",
        "birth_solar",
        "birth_lunar",
        "year_ganzhi",
        "nayin",
        "cung_phi",
        "trach_group",
    ):
        require_text(getattr(person, field), f"person.{field}")
    _in_set(person.nayin, ALLOWED_ELEMENTS, "person.nayin")
    _in_set(person.cung_phi, ALLOWED_CUNG, "person.cung_phi")
    if person.cung_element:
        _in_set(person.cung_element, ALLOWED_ELEMENTS, "person.cung_element")
    _in_set(person.trach_group, ALLOWED_TRACH, "person.trach_group")
    period = model.search_period
    if period.month < 1 or period.month > 12:
        raise DateSelectionReportValidationError(f"invalid search month: {period.month}")
    require_text(period.display, "search_period.display")
    if not model.recommendations:
        raise DateSelectionReportValidationError("missing recommendations")
    for rec in model.recommendations:
        _validate_recommendation_model(rec, person.trach_group)
    if not model.guidance.items:
        raise DateSelectionReportValidationError("missing guidance")
    require_text(model.provenance.source, "provenance.source")
    require_text(model.provenance.engine_version, "provenance.engine_version")


def _validate_recommendation_model(rec: Any, person_trach: str) -> None:
    require_text(rec.solar_date, "recommendation.solar_date")
    require_text(rec.lunar_date, "recommendation.lunar_date")
    require_text(rec.year_ganzhi, "recommendation.year_ganzhi")
    require_text(rec.month_ganzhi, "recommendation.month_ganzhi")
    require_text(rec.day_ganzhi, "recommendation.day_ganzhi")
    _in_set(rec.day_result, DAY_RESULTS, "recommendation.day_result")
    _in_set(rec.nayin, ALLOWED_ELEMENTS, "recommendation.nayin")
    _in_set(rec.cung, ALLOWED_CUNG, "recommendation.cung")
    _in_set(rec.trach_group, ALLOWED_TRACH, "recommendation.trach_group")
    if rec.trach_group != person_trach:
        raise DateSelectionReportValidationError("recommendation trach mismatch")
    if not rec.compatible_hours:
        raise DateSelectionReportValidationError("missing compatible_hours")
    for hour in rec.compatible_hours:
        if hour.trach_group != person_trach:
            raise DateSelectionReportValidationError("compatible hour trach mismatch")
        if not hour.positive_ke:
            raise DateSelectionReportValidationError("missing positive times")
        for slot in hour.positive_ke:
            _in_set(slot.result, POSITIVE_KE_RESULTS, "positive_ke.result")
