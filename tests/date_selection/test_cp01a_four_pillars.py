"""CP-01A canonical Four Pillars contract.

Reuses Hạ Nguyên + Nạp âm element lookup already used for Day and Hour.
Does not change six-state, ranking, or Ganzhi calculation.
"""

from __future__ import annotations

from engines.date_selection.identity import pillar_contract
from engines.date_selection.service import DateSelectionService

FULL_NAP_AM_NAMES = ("Thiên Hà Thủy", "Tuyền Trung Thủy", "Lộ Bàng Thổ")
ELEMENTS = {"Mộc", "Hỏa", "Thổ", "Kim", "Thủy"}


def test_binh_ngo_pillar_is_thuy_kham() -> None:
    pillar = pillar_contract("Bính Ngọ")
    assert pillar["can_chi"] == "Bính Ngọ"
    assert pillar["nayin_element"] == "Thủy"
    assert pillar["cung_phi"] == "Khảm"
    assert pillar["nayin_element"] not in FULL_NAP_AM_NAMES


def test_nap_am_is_five_element_only() -> None:
    pillar = pillar_contract("Đinh Mùi")
    assert pillar["can_chi"] == "Đinh Mùi"
    assert pillar["nayin_element"] == "Thủy"
    assert pillar["cung_phi"] == "Ly"
    for name in FULL_NAP_AM_NAMES:
        assert name not in pillar["nayin_element"]


def test_day_payload_year_and_month_have_identity() -> None:
    payload = DateSelectionService().inspect_day(2026, 8, 27).to_dict()
    year = payload["year"]
    month = payload["month"]
    assert year["can_chi"] == "Bính Ngọ"
    assert year["nayin_element"] == "Thủy"
    assert year["cung_phi"] == "Khảm"
    assert month["can_chi"] == "Bính Thân"
    assert month["nayin_element"] == "Hỏa"
    assert month["cung_phi"] == "Khôn"
    assert "—" not in year.values()
    assert "—" not in month.values()
    assert year["nayin_element"] in ELEMENTS
    assert month["nayin_element"] in ELEMENTS


def test_day_and_hour_identity_unchanged() -> None:
    payload = DateSelectionService().inspect_day(2026, 8, 27).to_dict()
    assert payload["ganzhi"] == "Quý Dậu"
    assert payload["nayin"] == "Kim"
    assert payload["nayin_element"] == "Kim"
    assert payload["cung"] == "Đoài"
    assert payload["cung_element"] == "Kim"
    assert payload["day"]["can_chi"] == "Quý Dậu"
    assert payload["day"]["nayin_element"] == "Kim"
    assert payload["day"]["cung_phi"] == "Đoài"
    hour = next(item for item in payload["hours"] if item["window"]["branch"] == "Thìn")
    assert hour["ganzhi"] == "Bính Thìn"
    assert hour["nayin"] == "Thổ"
    assert hour["cung"] == "Ly"
    assert hour["cung_element"] == "Hỏa"
    assert hour["can_chi"] == "Bính Thìn"
    assert hour["nayin_element"] == "Thổ"
    assert hour["cung_phi"] == "Ly"


def test_four_pillars_never_empty() -> None:
    payload = DateSelectionService().inspect_day(2026, 8, 27).to_dict()
    for key in ("year", "month", "day"):
        pillar = payload[key]
        assert pillar["can_chi"]
        assert pillar["nayin_element"] in ELEMENTS
        assert pillar["cung_phi"]
        assert "—" not in pillar["can_chi"]
        assert "—" not in pillar["nayin_element"]
        assert "—" not in pillar["cung_phi"]
    for hour in payload["hours"]:
        assert hour["can_chi"]
        assert hour["nayin_element"] in ELEMENTS
        assert hour["cung_phi"]
        assert "—" not in hour["can_chi"] + hour["nayin_element"] + hour["cung_phi"]
