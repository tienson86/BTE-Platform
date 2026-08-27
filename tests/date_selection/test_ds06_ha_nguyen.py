"""DS-06 Hạ Nguyên date/hour Cung table and Calendar day-Ganzhi payload."""

from __future__ import annotations

from engines.bazi_engine.engine import BaziEngine
from engines.calendar_engine.engine import CalendarEngine
from engines.date_selection.constants import (
    CUNG_ELEMENT,
    DONG_TU_TRACH,
    JIAZI_LABELS,
    TAY_TU_TRACH,
)
from engines.date_selection.cung_phi import cung_for_date_ganzhi, trach_for_date_ganzhi, trach_for_person
from engines.date_selection.loader import load_ha_nguyen_cung
from engines.date_selection.service import DateSelectionService
from engines.date_selection.trach import trach_from_cung


def test_a_ha_nguyen_table_integrity() -> None:
    table = load_ha_nguyen_cung()
    assert len(table) == 60
    assert set(table) == set(JIAZI_LABELS)
    for ganzhi, row in table.items():
        cung = row["ha_nguyen_cung"]
        assert cung in CUNG_ELEMENT
        info = trach_from_cung(cung)
        assert row["cung_element"] == info.element_label
        assert row["trach_group"] == info.trach_group_code
        if cung in DONG_TU_TRACH:
            assert info.trach_group_code == "dong"
        if cung in TAY_TU_TRACH:
            assert info.trach_group_code == "tay"


def test_b_quy_dau_doai_kim_tay() -> None:
    info = trach_for_date_ganzhi("Quý Dậu")
    assert cung_for_date_ganzhi("Quý Dậu") == "Đoài"
    assert info.cung == "Đoài"
    assert info.element_label == "Kim"
    assert info.trach_group_code == "tay"
    assert info.trach_group_label == "Tây Tứ Trạch"


def test_c_tan_dau_ton_moc_dong() -> None:
    info = trach_for_date_ganzhi("Tân Dậu")
    assert cung_for_date_ganzhi("Tân Dậu") == "Tốn"
    assert info.cung == "Tốn"
    assert info.element_label == "Mộc"
    assert info.trach_group_code == "dong"
    assert info.trach_group_label == "Đông Tứ Trạch"


def test_d_day_cung_gender_invariant() -> None:
    service = DateSelectionService()
    male = service.inspect_day(2026, 8, 27, gender="male")
    female = service.inspect_day(2026, 8, 27, gender="female")
    assert male.trach is not None and female.trach is not None
    assert male.calendar.day_ganzhi == female.calendar.day_ganzhi == "Quý Dậu"
    assert male.trach.cung == female.trach.cung == "Đoài"
    assert male.trach.element_label == female.trach.element_label
    assert male.trach.trach_group_code == female.trach.trach_group_code


def test_e_hour_cung_gender_invariant() -> None:
    service = DateSelectionService()
    male = service.inspect_day(2026, 8, 27, gender="male")
    female = service.inspect_day(2026, 8, 27, gender="female")
    male_thin = next(item for item in male.hours if item.window.branch == "Thìn")
    female_thin = next(item for item in female.hours if item.window.branch == "Thìn")
    assert male_thin.ganzhi == female_thin.ganzhi
    assert male_thin.trach is not None and female_thin.trach is not None
    assert male_thin.trach.cung == female_thin.trach.cung
    assert male_thin.trach.trach_group_code == female_thin.trach.trach_group_code


def test_f_person_cung_depends_on_gender() -> None:
    male = trach_for_person(lunar_year=1990, gender="male")
    female = trach_for_person(lunar_year=1990, gender="female")
    assert male.cung == "Khảm"
    assert female.cung == "Cấn"
    assert male.cung != female.cung


def test_g_known_date_27_aug_2026() -> None:
    day = DateSelectionService().inspect_day(2026, 8, 27)
    assert day.calendar.solar_label == "27/08/2026"
    assert day.calendar.lunar_day == 15
    assert day.calendar.lunar_month == 7
    assert day.calendar.year_ganzhi == "Bính Ngọ"
    assert day.calendar.day_ganzhi == "Quý Dậu"
    assert day.trach is not None
    assert day.trach.cung == "Đoài"
    assert day.trach.element_label == "Kim"
    assert day.trach.trach_group_label == "Tây Tứ Trạch"
    assert day.six_state.label == "Tiểu Cát"


def test_h_calendar_to_dict_day_ganzhi_matches_bazi() -> None:
    calendar = CalendarEngine().build(2026, 8, 27)
    chart = BaziEngine().build(2026, 8, 27, 12, 0)
    payload_day = calendar.to_dict()["lunar_can_chi"]["day"]
    bazi_day = f"{chart.day_pillar.stem} {chart.day_pillar.branch}"
    ds_day = DateSelectionService().inspect_day(2026, 8, 27).calendar.day_ganzhi
    assert payload_day == bazi_day == ds_day == "Quý Dậu"


def test_i_golden_1987_01_21_canh_ngo() -> None:
    calendar = CalendarEngine().build(1987, 1, 21, 3, 30)
    chart = BaziEngine().build(1987, 1, 21, 3, 30)
    assert calendar.to_dict()["lunar_can_chi"]["day"] == "Canh Ngọ"
    assert f"{chart.day_pillar.stem} {chart.day_pillar.branch}" == "Canh Ngọ"
    assert DateSelectionService().inspect_day(1987, 1, 21).calendar.day_ganzhi == "Canh Ngọ"


def test_jkl_personalized_top5_matches_trach() -> None:
    result = DateSelectionService().search(
        full_name="Nguyễn Văn A",
        gender="male",
        birth_year=1990,
        birth_month=5,
        birth_day=15,
        target_year=2026,
        target_month=8,
    )
    assert 1 <= len(result.dates) <= 5
    person_group = result.person.trach.trach_group_code
    for item in result.dates:
        assert item.day.trach is not None
        assert item.day.trach.trach_group_code == person_group
        assert item.day.six_state.code in {"dai_an", "toc_hy", "tieu_cat"}
        assert item.recommendations
        for rec in item.recommendations:
            hour = next(
                hour for hour in item.day.hours if hour.window.branch == rec.branch
            )
            assert hour.trach is not None
            assert hour.trach.trach_group_code == person_group
            assert rec.classification not in {"Xích Khẩu", "Không Vong"}
