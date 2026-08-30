"""G1-10C: published Year/Month Cung Phi follow birth Tam Nguyên, not Hạ Nguyên."""

from __future__ import annotations

from fastapi.testclient import TestClient

from applications.api.app import create_app
from engines.calendar_engine.cung_phi import cung_for_ganzhi, ha_nguyen_cung_for_ganzhi
from engines.calendar_engine.tam_nguyen import TRUNG_NGUYEN
from engines.date_selection.service import DateSelectionService

_YEAR = 1966
_MONTH = 9
_DAY = 24
_HOUR = 4
_MINUTE = 15


def _analyze() -> dict:
    client = TestClient(create_app())
    response = client.post(
        "/api/v1/analyze",
        json={
            "year": _YEAR,
            "month": _MONTH,
            "day": _DAY,
            "hour": _HOUR,
            "minute": _MINUTE,
            "gender": "male",
            "full_name": "G1-10C",
            "birth_place": "Ha Noi",
        },
    )
    assert response.status_code == 200
    return response.json()["data"]


def test_1966_api_pillar_cung_phi_matches_tam_nguyen_tables() -> None:
    data = _analyze()
    calendar = data["calendar"]
    identity = data["identity"]["four_pillars"]
    bazi = data["bazi"]
    routing = calendar["ganzhi_routing"]

    assert calendar["tam_nguyen"] == TRUNG_NGUYEN
    assert bazi["year_pillar"]["stem"] == "Bính"
    assert bazi["year_pillar"]["branch"] == "Ngọ"
    assert bazi["month_pillar"]["stem"] == "Đinh"
    assert bazi["month_pillar"]["branch"] == "Dậu"
    assert bazi["day_pillar"]["stem"] == "Bính"
    assert bazi["day_pillar"]["branch"] == "Tuất"
    assert bazi["hour_pillar"]["stem"] == "Canh"
    assert bazi["hour_pillar"]["branch"] == "Dần"

    expected_year = cung_for_ganzhi(
        "Bính Ngọ",
        tam_nguyen=TRUNG_NGUYEN,
        reference_year=_YEAR,
        gender="male",
    )
    expected_month = cung_for_ganzhi(
        "Đinh Dậu",
        tam_nguyen=TRUNG_NGUYEN,
        reference_year=_YEAR,
        gender="male",
    )
    expected_day = ha_nguyen_cung_for_ganzhi("Bính Tuất", reference_year=_YEAR)
    expected_hour = ha_nguyen_cung_for_ganzhi("Canh Dần", reference_year=_YEAR)

    assert expected_year == "Đoài"
    assert expected_month == "Đoài"
    assert expected_day == "Chấn"
    assert expected_hour == "Cấn"
    assert expected_year != ha_nguyen_cung_for_ganzhi("Bính Ngọ", reference_year=_YEAR)
    assert expected_month != ha_nguyen_cung_for_ganzhi("Đinh Dậu", reference_year=_YEAR)

    for source in (identity["year"], bazi["year_pillar"], routing["year"]):
        assert source["cung_phi"] == "Đoài"
    for source in (identity["month"], bazi["month_pillar"], routing["month"]):
        assert source["cung_phi"] == "Đoài"
    for source in (identity["day"], bazi["day_pillar"], routing["day"]):
        assert source["cung_phi"] == "Chấn"
    for source in (identity["hour"], bazi["hour_pillar"], routing["hour"]):
        assert source["cung_phi"] == "Cấn"


def test_1966_homepage_ket_qua_ngay_year_month_cung() -> None:
    payload = DateSelectionService().inspect_day(_YEAR, _MONTH, _DAY).to_dict()
    assert payload["year"]["can_chi"] == "Bính Ngọ"
    assert payload["year"]["cung_phi"] == "Đoài"
    assert payload["month"]["can_chi"] == "Đinh Dậu"
    assert payload["month"]["cung_phi"] == "Đoài"
    assert payload["day"]["can_chi"] == "Bính Tuất"
    assert payload["day"]["cung_phi"] == "Chấn"
    hour = next(
        item
        for item in payload["hours"]
        if item.get("ganzhi") == "Canh Dần" or (item.get("window") or {}).get("branch") == "Dần"
    )
    assert (hour.get("cung_phi") or hour.get("cung")) == "Cấn"
