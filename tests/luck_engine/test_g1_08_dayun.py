"""G1-08 natal Đại vận: direction, gender, start-age, JiaZi, CASE-0001."""

from __future__ import annotations

from datetime import datetime
from types import SimpleNamespace

import pytest

from applications.api.exceptions import ValidationAPIError
from applications.api.services.five_elements_truth import ELEMENT_LABELS
from applications.api.services.luck_truth import shape_luck_payload
from applications.api.services.orchestrator import OrchestratorService
from engines.bazi_engine.engine import BaziEngine
from engines.bazi_engine.ten_god import BRANCH_META, STEM_META
from engines.calendar_engine.engine import CalendarEngine
from engines.luck_engine.dayun_validation import validate_dayun_runtime
from engines.luck_engine.engine import LuckEngine
from engines.luck_engine.exceptions import LuckContextError
from engines.luck_engine.providers._common import (
    compute_dayun_start_age,
    dayun_forward,
    gender_display_label,
    jiazi_index,
    normalize_luck_gender,
    step_jiazi,
)
from engines.luck_engine.providers.dayun import DefaultDayunProvider
from engines.rule_contract.context_builder import BRANCH_ELEMENT


CASE_0001_SEQUENCE = (
    ("Nhâm Dần", 1992, 2001, 5, 14),
    ("Quý Mão", 2002, 2011, 15, 24),
    ("Giáp Thìn", 2012, 2021, 25, 34),
    ("Ất Tỵ", 2022, 2031, 35, 44),
    ("Bính Ngọ", 2032, 2041, 45, 54),
    ("Đinh Mùi", 2042, 2051, 55, 64),
    ("Mậu Thân", 2052, 2061, 65, 74),
    ("Kỷ Dậu", 2062, 2071, 75, 84),
    ("Canh Tuất", 2072, 2081, 85, 94),
    ("Tân Hợi", 2082, 2091, 95, 104),
)


def _calendar(*, hour: int = 4, minute: int = 30) -> object:
    return CalendarEngine().build(1987, 1, 21, hour, minute, timezone_name="Asia/Bangkok")


def _chart(gender: str | None) -> object:
    return BaziEngine().build(_calendar(), gender=gender)


def _dayun(*, gender: str = "male", hour: int = 4, reference: datetime | None = None):
    calendar = _calendar(hour=hour)
    chart = BaziEngine().build(calendar, gender=gender)
    return DefaultDayunProvider(reference_dt=reference or datetime(2026, 8, 20)).provide(
        calendar=calendar,
        bazi=chart,
    )


def test_branch_meta_matches_g1_05_element_map() -> None:
    """BRANCH_META is the Vietnamese projection of canonical BRANCH_ELEMENT."""
    for branch, english in BRANCH_ELEMENT.items():
        assert BRANCH_META[branch] == ELEMENT_LABELS[english]


def test_direction_duong_nam_thuan() -> None:
    assert STEM_META["Bính"][1] == "Dương"
    assert dayun_forward("male", "Bính") is True


def test_direction_am_nam_nghich() -> None:
    assert STEM_META["Ất"][1] == "Âm"
    assert dayun_forward("male", "Ất") is False


def test_direction_duong_nu_nghich() -> None:
    assert dayun_forward("female", "Bính") is False


def test_direction_am_nu_thuan() -> None:
    assert dayun_forward("female", "Ất") is True


def test_gender_aliases_male() -> None:
    for value in ("male", "Nam", "nam", "m", "1"):
        assert normalize_luck_gender(value) == "male"
        assert dayun_forward(value, "Bính") is True


def test_gender_aliases_female() -> None:
    for value in ("female", "Nữ", "nu", "nữ", "f"):
        assert normalize_luck_gender(value) == "female"
        assert dayun_forward(value, "Bính") is False


def test_missing_gender_does_not_default_male() -> None:
    with pytest.raises(LuckContextError, match="gender_required"):
        normalize_luck_gender(None)
    with pytest.raises(LuckContextError, match="gender_required"):
        normalize_luck_gender("")
    with pytest.raises(LuckContextError, match="gender_required"):
        DefaultDayunProvider().provide(calendar=_calendar(), bazi=_chart(None))


def test_invalid_gender_does_not_default_male() -> None:
    with pytest.raises(LuckContextError, match="unsupported_gender"):
        normalize_luck_gender("unknown")
    with pytest.raises(LuckContextError, match="unsupported_gender"):
        dayun_forward("other", "Bính")


def test_luck_engine_missing_gender_sets_reason() -> None:
    luck = LuckEngine().build(calendar=_calendar(), bazi=_chart(None))
    assert luck.current_dayun is None
    assert luck.reason == "gender_required"
    payload = shape_luck_payload(luck)
    assert payload["cycles"] == []
    assert payload["reason"] == "gender_required"


def test_start_age_formula_boundaries() -> None:
    assert max(1, int(round(1 / 3.0))) == 1
    assert max(1, int(round(2 / 3.0))) == 1
    assert max(1, int(round(3 / 3.0))) == 1
    assert max(1, int(round(14 / 3.0))) == 5
    assert max(1, int(round(45 / 3.0))) == 15


def test_start_age_three_days_to_jie() -> None:
    age, meta = compute_dayun_start_age(1987, 2, 1, forward=True)
    assert meta["anchor_jie_date"] == "1987-02-04"
    assert meta["days_to_jie"] == 3
    assert age == 1


def test_start_age_two_days_floors_to_minimum_one() -> None:
    age, meta = compute_dayun_start_age(1987, 2, 2, forward=True)
    assert meta["days_to_jie"] == 2
    assert age == 1
    age, meta = compute_dayun_start_age(1987, 1, 21, forward=True)
    assert age == 5
    assert meta["days_to_jie"] == 14
    assert meta["anchor_jie_date"] == "1987-02-04"
    assert meta["anchor_jie_name"] == "Lập Xuân"
    assert meta["hour_used"] is False
    assert meta["same_day_jie_skipped"] == []


def test_birth_hour_does_not_change_start_age() -> None:
    morning = _dayun(hour=4)
    midnight = _dayun(hour=0)
    assert morning.metadata["sequence"][0]["start_age"] == 5
    assert midnight.metadata["sequence"][0]["start_age"] == 5
    assert morning.metadata["start_age_calc"]["days_to_jie"] == midnight.metadata[
        "start_age_calc"
    ]["days_to_jie"]


def test_same_jie_day_is_skipped_forward() -> None:
    age, meta = compute_dayun_start_age(1987, 2, 4, forward=True)
    assert "Lập Xuân 1987-02-04" in meta["same_day_jie_skipped"]
    assert meta["anchor_jie_name"] == "Kinh Trập"
    assert meta["anchor_jie_date"] == "1987-03-06"
    assert age == max(1, int(round(meta["days_to_jie"] / 3.0)))


def test_same_jie_day_is_skipped_reverse() -> None:
    _age, meta = compute_dayun_start_age(1987, 2, 4, forward=False)
    assert "Lập Xuân 1987-02-04" in meta["same_day_jie_skipped"]
    assert meta["anchor_jie_date"] < "1987-02-04"


def test_jiazi_wrap_forward_and_reverse() -> None:
    assert step_jiazi("Quý", "Hợi", 1) == ("Giáp", "Tý")
    assert step_jiazi("Giáp", "Tý", -1) == ("Quý", "Hợi")
    assert (jiazi_index("Giáp", "Tý") - jiazi_index("Quý", "Hợi")) % 60 == 1


def test_first_cycle_forward_from_month_pillar() -> None:
    current = _dayun(gender="male")
    sequence = current.metadata["sequence"]
    assert current.metadata["direction"] == "forward"
    assert sequence[0]["ganzhi"] == "Nhâm Dần"
    assert step_jiazi("Tân", "Sửu", 1) == ("Nhâm", "Dần")


def test_first_cycle_reverse_from_month_pillar() -> None:
    current = _dayun(gender="female")
    sequence = current.metadata["sequence"]
    assert current.metadata["direction"] == "reverse"
    assert step_jiazi("Tân", "Sửu", -1) == ("Canh", "Tý")
    assert sequence[0]["ganzhi"] == "Canh Tý"


def test_sequence_advances_one_jiazi_and_has_no_gap() -> None:
    current = _dayun(gender="male")
    sequence = current.metadata["sequence"]
    assert len(sequence) == 10
    for prev, nxt in zip(sequence, sequence[1:]):
        expected = step_jiazi(prev["heavenly_stem"], prev["earthly_branch"], 1)
        assert (nxt["heavenly_stem"], nxt["earthly_branch"]) == expected
        assert nxt["start_age"] == prev["end_age"] + 1
        assert nxt["start_year"] == prev["end_year"] + 1
        assert nxt["end_age"] - nxt["start_age"] == 9
        assert nxt["end_year"] - nxt["start_year"] == 9
    result = validate_dayun_runtime(current)
    assert result.ok


def test_case_0001_full_sequence_and_current() -> None:
    current = _dayun(gender="male", reference=datetime(2026, 8, 20))
    payload = shape_luck_payload(
        SimpleNamespace(
            to_dict=lambda: {
                "current_dayun": current.to_dict(),
                "available": True,
                "reason": None,
                "metadata": {},
            }
        )
    )
    assert payload["direction"] == "forward"
    assert payload["direction_label"] == "Thuận"
    assert payload["start_age"] == 5
    assert payload["evidence"] == "Nam · Niên can Bính Dương · Thuận"
    assert payload["precision"] == "year_level"
    assert payload["current_age_basis"] == "current_year - birth_year"
    assert payload["current_cycle"]["gan_zhi"] == "Ất Tỵ"
    assert payload["current_cycle"]["year_start"] == 2022
    assert payload["current_cycle"]["year_end"] == 2031
    assert payload["current_cycle"]["age_start"] == 35
    assert payload["current_cycle"]["age_end"] == 44
    assert payload["current_cycle"]["stem_element"] == "Mộc"
    assert payload["current_cycle"]["branch_element"] == "Hỏa"
    for index, (gan_zhi, year_start, year_end, age_start, age_end) in enumerate(
        CASE_0001_SEQUENCE
    ):
        cycle = payload["cycles"][index]
        assert cycle["index"] == index
        assert cycle["gan_zhi"] == gan_zhi
        assert cycle["year_start"] == year_start
        assert cycle["year_end"] == year_end
        assert cycle["age_start"] == age_start
        assert cycle["age_end"] == age_end


def test_orchestrator_case_0001_matches_engine() -> None:
    payload = OrchestratorService().analyze(
        year=1987, month=1, day=21, hour=4, minute=30, gender="male"
    )
    luck = payload["luck"]
    engine = _dayun(gender="male", reference=datetime(2026, 8, 20))
    assert luck["direction"] == "forward"
    assert luck["start_age"] == 5
    assert luck["current_cycle"]["gan_zhi"] == f"{engine.heavenly_stem} {engine.earthly_branch}"
    assert luck["cycles"][0]["gan_zhi"] == "Nhâm Dần"
    assert luck["cycles"][3]["gan_zhi"] == "Ất Tỵ"
    assert luck["cycles"][3]["year_start"] == 2022
    assert luck["current_cycle"]["year_start"] == 2022


def test_internal_gender_maps_to_vietnamese_display() -> None:
    assert gender_display_label("male") == "Nam"
    assert gender_display_label("female") == "Nữ"


def test_missing_gender_display_is_empty() -> None:
    assert gender_display_label(None) == ""
    assert gender_display_label("") == ""
    assert gender_display_label("unknown") == ""


def test_missing_gender_never_becomes_male() -> None:
    luck = LuckEngine().build(calendar=_calendar(), bazi=_chart(None))
    payload = shape_luck_payload(luck)
    assert luck.reason == "gender_required"
    assert payload["gender"] != "male"
    assert payload["gender_label"] != "Nam"
    assert payload["direction"] in ("", None)
    assert payload["cycles"] == []


def test_analyze_missing_gender_is_validation_failure() -> None:
    with pytest.raises(ValidationAPIError) as exc:
        OrchestratorService().analyze(
            year=1987, month=1, day=21, hour=4, minute=30, gender=None
        )
    assert exc.value.status_code == 422
    assert exc.value.code == "validation_error"
    assert exc.value.details["code"] == "gender_required"
    assert exc.value.details["field"] == "gender"


def test_analyze_invalid_gender_is_validation_failure() -> None:
    with pytest.raises(ValidationAPIError) as exc:
        OrchestratorService().analyze(
            year=1987, month=1, day=21, hour=4, minute=30, gender="unknown"
        )
    assert exc.value.status_code == 422
    assert exc.value.details["code"] == "unsupported_gender"


def test_analyze_missing_gender_does_not_compute_dayun_as_male() -> None:
    with pytest.raises(ValidationAPIError):
        OrchestratorService().analyze(
            year=1987, month=1, day=21, hour=4, minute=30, gender=""
        )


def test_case_0001_payload_gender_label_nam() -> None:
    from applications.api.routes._helpers import customer_metadata_from_request
    from applications.api.schemas.common import BirthRequest

    payload = OrchestratorService().analyze(
        year=1987, month=1, day=21, hour=4, minute=30, gender="male"
    )
    assert payload["luck"]["gender"] == "male"
    assert payload["luck"]["gender_label"] == "Nam"
    assert payload["luck"]["evidence"] == "Nam · Niên can Bính Dương · Thuận"
    assert payload["luck"]["direction_label"] == "Thuận"
    meta = customer_metadata_from_request(
        BirthRequest(year=1987, month=1, day=21, hour=4, minute=30, gender="male")
    )
    assert meta["gender"] == "male"
    assert meta["gender_label"] == "Nam"
