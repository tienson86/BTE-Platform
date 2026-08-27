"""DS-06B Vietnamese localization and explicit identity labels."""

from __future__ import annotations

from engines.date_selection.cung_phi import trach_for_date_ganzhi
from engines.date_selection.identity import hoa_giap_view
from engines.date_selection.service import DateSelectionService


def test_person_solar_label_is_vietnamese_order() -> None:
    person = DateSelectionService().person_profile(
        full_name="Nguyễn Tiến Sơn",
        gender="male",
        birth_year=1987,
        birth_month=1,
        birth_day=21,
    )
    assert person.solar_label == "21/01/1987"
    payload = person.to_dict()
    assert payload["solar_label"] == "21/01/1987"
    assert payload["year_ganzhi"] == payload["ganzhi"]
    assert payload["nayin"]
    assert payload["cung_phi"] == payload["cung"]
    assert payload["cung_element"]
    assert payload["nayin"] != payload["cung_element"] or payload["cung"] != payload["nayin"]
    assert "Ngũ hành" not in str(payload)


def test_search_person_separates_nayin_from_hanh_cung() -> None:
    result = DateSelectionService().search(
        full_name="Nguyễn Văn A",
        gender="male",
        birth_year=1990,
        birth_month=5,
        birth_day=15,
        target_year=2026,
        target_month=9,
    )
    payload = result.to_dict()
    person = payload["person"]
    assert person["solar_label"] == "15/05/1990"
    assert "/" in person["lunar_label"]
    assert person["lunar_label"].count("/") == 2
    assert person["year_ganzhi"]
    assert person["nayin"] == "Thổ"
    assert person["cung"]
    assert person["cung_element"]
    assert person["nayin"] != person["cung_element"]
    assert payload["target_month"] == 9
    if payload["dates"]:
        card = payload["dates"][0]["day"]
        assert card["calendar"]["solar_label"].count("/") == 2
        assert card["nayin"]
        assert card["cung"]
        assert card["cung_element"]
        assert "month_ganzhi" in card["calendar"]


def test_canh_thin_and_mau_thin_remain_separate() -> None:
    canh = hoa_giap_view("Canh Thìn", trach_for_date_ganzhi("Canh Thìn"))
    assert canh["nayin"] == "Kim"
    assert canh["cung"] == "Ly"
    assert canh["cung_element"] == "Hỏa"
    mau = hoa_giap_view("Mậu Thìn", trach_for_date_ganzhi("Mậu Thìn"))
    assert mau["nayin"] == "Mộc"
    assert mau["cung"] == "Chấn"
    assert mau["cung_element"] == "Mộc"


def test_day_month_ganzhi_and_calculations_unchanged() -> None:
    day = DateSelectionService().inspect_day(2026, 8, 27)
    payload = day.to_dict()
    assert payload["calendar"]["month_ganzhi"] == "Giáp Thân"
    assert payload["calendar"]["day_ganzhi"] == "Quý Dậu"
    assert payload["six_state"]["label"] == "Tiểu Cát"
    assert payload["nayin"] == "Kim"
    assert payload["cung"] == "Đoài"
    assert payload["cung_element"] == "Kim"
