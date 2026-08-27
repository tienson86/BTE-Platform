"""DateSelectionReportAdapter — SearchResult to DateSelectionReportModel.

Validates and normalizes. Does not calculate, rerank, or reinterpret.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Callable
from uuid import uuid4

from engines.date_selection.models import SearchResult
from engines.date_selection_report.constants import (
    ENGINE_VERSION,
    GENERATOR,
    GUIDANCE_ITEMS,
    GUIDANCE_TITLE,
    LOCALE,
    REPORT_SCHEMA_VERSION,
    REPORT_TYPE,
    SOURCE,
    TITLE,
)
from engines.date_selection_report.models import (
    CompatibleHourReportData,
    DateSelectionReportModel,
    GuidanceItem,
    GuidanceReportData,
    Metadata,
    PersonReportData,
    PositiveKeReportData,
    Provenance,
    RecommendedDateReportData,
    SearchPeriodReportData,
)
from engines.date_selection_report.validators import (
    trach_label,
    validate_report_model,
    validate_search_result,
)


class DateSelectionReportAdapter:
    """Map a frozen Date Selection SearchResult onto the report model."""

    def __init__(
        self,
        *,
        clock: Callable[[], datetime] | None = None,
        report_id: str | None = None,
        search_result_id: str | None = None,
    ) -> None:
        self._clock = clock
        self._report_id = report_id
        self._search_result_id = search_result_id

    def adapt(self, search_result: SearchResult) -> DateSelectionReportModel:
        """Validate, normalize presentation, and return an immutable report model."""
        payload = search_result.to_dict()
        validate_search_result(payload)
        generated_at = (self._clock or _utc_now)().isoformat()
        model = DateSelectionReportModel(
            metadata=_metadata(self._report_id, generated_at),
            person=_person(payload["person"]),
            search_period=_period(payload["target_month"], payload["target_year"]),
            recommendations=_recommendations(payload["dates"]),
            guidance=_guidance(),
            provenance=Provenance(
                source=SOURCE,
                search_result_id=self._search_result_id,
                generated_at=generated_at,
                engine_version=ENGINE_VERSION,
            ),
        )
        validate_report_model(model)
        return model


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _metadata(report_id: str | None, generated_at: str) -> Metadata:
    return Metadata(
        report_id=report_id or str(uuid4()),
        report_schema_version=REPORT_SCHEMA_VERSION,
        report_type=REPORT_TYPE,
        generated_at=generated_at,
        locale=LOCALE,
        title=TITLE,
        generator=GENERATOR,
    )


def _person(person: dict) -> PersonReportData:
    return PersonReportData(
        full_name=str(person["full_name"]).strip(),
        gender=str(person.get("gender_label") or person.get("gender") or "").strip(),
        birth_solar=str(person["solar_label"]).strip(),
        birth_lunar=str(person["lunar_label"]).strip(),
        year_ganzhi=str(person.get("year_ganzhi") or person.get("ganzhi") or "").strip(),
        nayin=str(person["nayin"]).strip(),
        cung_phi=str(person.get("cung_phi") or person.get("cung") or "").strip(),
        cung_element=str(person.get("cung_element") or "").strip(),
        trach_group=trach_label(
            person.get("trach_group_label") or person.get("trach_group"),
            "person.trach_group",
        ),
    )


def _period(month: int, year: int) -> SearchPeriodReportData:
    return SearchPeriodReportData(
        month=month,
        year=year,
        display=f"{month:02d}/{year}",
    )


def _recommendations(dates: list) -> tuple[RecommendedDateReportData, ...]:
    rows: list[RecommendedDateReportData] = []
    for rank, item in enumerate(dates, start=1):
        day = item["day"]
        calendar = day["calendar"]
        six = day["six_state"]
        rows.append(
            RecommendedDateReportData(
                rank=rank,
                solar_date=str(calendar["solar_label"]).strip(),
                lunar_date=str(calendar["lunar_label"]).strip(),
                year_ganzhi=str(calendar["year_ganzhi"]).strip(),
                month_ganzhi=str(calendar.get("month_ganzhi") or day.get("month_ganzhi") or "").strip(),
                day_ganzhi=str(day.get("ganzhi") or calendar.get("day_ganzhi") or "").strip(),
                day_result=str(six["label"]).strip(),
                nayin=str(day["nayin"]).strip(),
                cung=str(day["cung"]).strip(),
                cung_element=str(day.get("cung_element") or "").strip(),
                trach_group=trach_label(
                    day.get("trach_group_label") or day.get("trach_group"),
                    "recommendation.trach_group",
                ),
                compatible_hours=_hours(item["compatible_hours"]),
            )
        )
    return tuple(rows)


def _hours(hours: list) -> tuple[CompatibleHourReportData, ...]:
    rows: list[CompatibleHourReportData] = []
    for hour in hours:
        slots = tuple(
            PositiveKeReportData(
                index=int(slot["index"]),
                time_range=str(slot["time_range"]).strip(),
                result=str(slot["result"]).strip(),
            )
            for slot in hour.get("positive_ke") or []
        )
        rows.append(
            CompatibleHourReportData(
                branch=str(hour["branch"]).strip(),
                time_range=str(hour.get("full_time_range") or hour.get("time_range") or "").strip(),
                ganzhi=str(hour["ganzhi"]).strip(),
                nayin=str(hour["nayin"]).strip(),
                cung=str(hour["cung"]).strip(),
                cung_element=str(hour.get("cung_element") or "").strip(),
                trach_group=trach_label(
                    hour.get("trach_group_label") or hour.get("trach_group"),
                    "hour.trach_group",
                ),
                positive_ke=slots,
            )
        )
    return tuple(rows)


def _guidance() -> GuidanceReportData:
    return GuidanceReportData(
        title=GUIDANCE_TITLE,
        items=tuple(GuidanceItem(label=label, text=text) for label, text in GUIDANCE_ITEMS),
    )
