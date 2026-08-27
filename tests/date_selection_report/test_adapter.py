"""Adapter tests: SearchResult is copied, never recalculated."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from engines.date_selection.service import DateSelectionService
from engines.date_selection_report.adapter import DateSelectionReportAdapter
from engines.date_selection_report.contracts import REPORT_FOUNDATION_CONTRACT
from engines.date_selection_report.validators import validate_report_model

ADAPTER = Path(__file__).resolve().parents[2] / "engines" / "date_selection_report" / "adapter.py"


def _search():
    return DateSelectionService().search(
        full_name="Nguyễn Tiến Sơn",
        gender="male",
        birth_year=1987,
        birth_month=1,
        birth_day=21,
        target_year=2026,
        target_month=9,
    )


def test_adapter_preserves_person_and_period() -> None:
    search = _search()
    model = DateSelectionReportAdapter(
        clock=lambda: datetime(2026, 8, 27, tzinfo=timezone.utc),
        report_id="fixed-id",
    ).adapt(search)
    payload = search.to_dict()
    person = payload["person"]
    assert model.person.full_name == person["full_name"]
    assert model.person.gender == person["gender_label"]
    assert model.person.birth_solar == person["solar_label"]
    assert model.person.birth_lunar == person["lunar_label"]
    assert model.person.year_ganzhi == person["year_ganzhi"]
    assert model.person.nayin == person["nayin"]
    assert model.person.cung_phi == person["cung"]
    assert model.person.cung_element == person["cung_element"]
    assert model.search_period.year == search.target_year
    assert model.search_period.month == search.target_month
    assert model.search_period.display == "09/2026"


def test_adapter_preserves_recommendation_order() -> None:
    search = _search()
    model = DateSelectionReportAdapter().adapt(search)
    expected = [item.to_dict()["day"]["calendar"]["solar_label"] for item in search.dates]
    actual = [item.solar_date for item in model.recommendations]
    assert actual == expected
    assert [item.rank for item in model.recommendations] == list(range(1, len(actual) + 1))


def test_adapter_preserves_hours_and_positive_ke() -> None:
    search = _search()
    model = DateSelectionReportAdapter().adapt(search)
    source = search.to_dict()["dates"][0]
    report = model.recommendations[0]
    src_hours = source["compatible_hours"]
    assert [hour.branch for hour in report.compatible_hours] == [hour["branch"] for hour in src_hours]
    assert [hour.time_range for hour in report.compatible_hours] == [
        hour["full_time_range"] for hour in src_hours
    ]
    first = report.compatible_hours[0]
    src = src_hours[0]
    assert first.ganzhi == src["ganzhi"]
    assert first.cung == src["cung"]
    assert first.cung_element == src["cung_element"]
    assert [slot.result for slot in first.positive_ke] == [slot["result"] for slot in src["positive_ke"]]
    assert "hour_result" not in first.to_dict()


def test_adapter_does_not_import_calculators() -> None:
    source = ADAPTER.read_text(encoding="utf-8")
    assert "from engines.date_selection.ranking" not in source
    assert "from engines.date_selection.liu_ren" not in source
    assert "from engines.date_selection.cung_phi" not in source
    assert REPORT_FOUNDATION_CONTRACT["pack_05_contract_id"] == "bte.report.foundation.v1"


def test_guidance_is_educational_only() -> None:
    model = DateSelectionReportAdapter().adapt(_search())
    text = " ".join(item.text for item in model.guidance.items)
    assert "Đại An" in {item.label for item in model.guidance.items}
    assert "must use" not in text.lower()
    assert "bắt buộc" not in text.lower()
    validate_report_model(model)
