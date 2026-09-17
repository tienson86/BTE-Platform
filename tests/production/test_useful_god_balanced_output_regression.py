"""Regression coverage for balanced charts where climate and output dominate."""

from applications.production.engine_runner import ProductionEngineRunner
from applications.production.fixtures.case_0002_readiness import CASE_0002_REQUEST
from applications.production.models import ProductionRequest
from applications.api.services.orchestrator import OrchestratorService


HUNG_REQUEST = ProductionRequest(
    case_id="HUNG-REGRESSION",
    year=1981,
    month=8,
    day=29,
    hour=4,
    minute=30,
    gender="male",
    timezone="Asia/Ho_Chi_Minh",
    full_name="Doan Quang Hung",
    birth_place="Quang Ninh, Viet Nam",
    export_pdf=False,
)

SON_REQUEST = ProductionRequest(
    case_id="SON-REGRESSION",
    year=1996,
    month=11,
    day=29,
    hour=17,
    minute=20,
    gender="male",
    timezone="Asia/Bangkok",
    full_name="Luu Hoang Son",
    birth_place="Ha Noi, Viet Nam",
    export_pdf=False,
)

KHANG_REQUEST = ProductionRequest(
    case_id="KHANG-REGRESSION",
    year=2015,
    month=8,
    day=14,
    hour=7,
    minute=22,
    gender="male",
    timezone="Asia/Ho_Chi_Minh",
    full_name="Nguyen Tien Khang",
    birth_place="Viet Nam",
    export_pdf=False,
)

DUONG_REQUEST = ProductionRequest(
    case_id="DUONG-REGRESSION",
    year=2022,
    month=8,
    day=16,
    hour=9,
    minute=24,
    gender="male",
    timezone="Asia/Ho_Chi_Minh",
    full_name="Nguyen Thanh Duong",
    birth_place="Viet Nam",
    export_pdf=False,
)

HA_REQUEST = ProductionRequest(
    case_id="HA-REGRESSION",
    year=1996,
    month=11,
    day=21,
    hour=17,
    minute=0,
    gender="male",
    timezone="Asia/Ho_Chi_Minh",
    full_name="Pham Thai Ha",
    birth_place="Viet Nam",
    export_pdf=False,
)

TRUNG_REQUEST = ProductionRequest(
    case_id="TRUNG-REGRESSION",
    year=1977,
    month=2,
    day=18,
    hour=6,
    minute=30,
    gender="male",
    timezone="Asia/Ho_Chi_Minh",
    full_name="Dinh Thanh Trung",
    birth_place="Viet Nam",
    export_pdf=False,
)

HUONG_MAI_REQUEST = ProductionRequest(
    case_id="HUONG-MAI-REGRESSION",
    year=1988,
    month=6,
    day=7,
    hour=20,
    minute=45,
    gender="female",
    timezone="Asia/Ho_Chi_Minh",
    full_name="Nguyen Thi Huong Mai",
    birth_place="Viet Nam",
    export_pdf=False,
)

NGOC_REQUEST = ProductionRequest(
    case_id="NGOC-REGRESSION",
    year=1987,
    month=9,
    day=25,
    hour=3,
    minute=31,
    gender="female",
    timezone="Asia/Ho_Chi_Minh",
    full_name="Quach Thi Ngoc",
    birth_place="Phu Tho, Viet Nam",
    export_pdf=False,
)


def test_hot_balanced_wood_output_uses_water_before_wealth_fallback() -> None:
    analysis = ProductionEngineRunner().run(CASE_0002_REQUEST).analysis

    assert analysis.strength.strength_level == "balanced"
    assert analysis.pattern.pattern == "thuong_quan"
    assert analysis.useful_god.winning_rule_id == "str_balanced_hot_wood_output"
    assert analysis.useful_god.useful_stem == "Nhâm"
    assert analysis.useful_god.useful_element == "Thủy"
    assert analysis.useful_god.favorable_display == (
        "Thủy · Quý · Chính Ấn / Mộc · Giáp · Tỷ Kiên / "
        "Mộc · Ất · Kiếp Tài / Kim · Canh · Thất Sát"
    )
    assert analysis.useful_god.unfavorable_display == (
        "Hỏa · Bính · Thực Thần / Hỏa · Đinh · Thương Quan / "
        "Thổ · Mậu · Thiên Tài / Thổ · Kỷ · Chính Tài"
    )


def test_rooster_month_balanced_earth_output_uses_fire_before_wealth_fallback() -> None:
    analysis = ProductionEngineRunner().run(HUNG_REQUEST).analysis

    assert analysis.strength.strength_level == "balanced"
    assert analysis.pattern.pattern == "thuc_than"
    assert analysis.useful_god.winning_rule_id == "str_balanced_rooster_earth_output"
    assert analysis.useful_god.useful_stem == "Đinh"
    assert analysis.useful_god.useful_element == "Hỏa"
    assert analysis.useful_god.favorable_display == (
        "Hỏa · Bính · Chính Ấn / Thổ · Mậu · Kiếp Tài / Thổ · Kỷ · Tỷ Kiên"
    )


def test_cold_balanced_metal_sat_resource_uses_fire_before_wealth_fallback() -> None:
    analysis = ProductionEngineRunner().run(SON_REQUEST).analysis

    assert analysis.strength.strength_level == "balanced"
    assert analysis.pattern.pattern == "sat_an"
    assert analysis.temperature.temperature_level == "cold"
    assert analysis.useful_god.winning_rule_id == (
        "str_balanced_cold_metal_sat_resource"
    )
    assert analysis.useful_god.useful_stem == "Bính"
    assert analysis.useful_god.useful_element == "Hỏa"
    assert analysis.useful_god.favorable_display == (
        "Thổ · Mậu · Thiên Ấn / Thổ · Kỷ · Chính Ấn / "
        "Kim · Canh · Tỷ Kiên / Kim · Tân · Kiếp Tài"
    )
    assert analysis.useful_god.unfavorable_display == (
        "Thủy · Nhâm · Thực Thần / Thủy · Quý · Thương Quan"
    )


def test_uncovered_balanced_chart_uses_controlled_climate_fallback() -> None:
    request = ProductionRequest(
        case_id="BALANCED-SAFETY-GATE",
        year=1984,
        month=5,
        day=7,
        hour=10,
        minute=30,
        gender="male",
        timezone="Asia/Ho_Chi_Minh",
        full_name="Balanced Safety Gate",
        birth_place="Viet Nam",
        export_pdf=False,
    )
    analysis = ProductionEngineRunner().run(request).analysis

    assert analysis.strength.strength_level == "balanced"
    assert analysis.useful_god.success is True
    assert analysis.useful_god.overall_incomplete is False
    assert analysis.useful_god.winning_rule_id in {
        "str_balanced_cold_cool_climate_fallback",
        "str_balanced_warm_hot_climate_fallback",
    }
    assert "str_005" not in analysis.useful_god.matched_rules


def test_cool_monkey_month_strong_water_uses_fire_not_more_earth() -> None:
    analysis = ProductionEngineRunner().run(KHANG_REQUEST).analysis

    assert analysis.strength.strength_level == "strong"
    assert analysis.bazi.day_master_element == "Thủy"
    assert analysis.bazi.month_pillar.branch == "Thân"
    assert analysis.temperature.temperature_level == "cool"
    assert analysis.useful_god.winning_rule_id == "str_cool_monkey_strong_water"
    assert analysis.useful_god.useful_display == "Hỏa · Đinh · Chính Tài"
    assert analysis.useful_god.favorable_display == (
        "Hỏa · Bính · Thiên Tài / Mộc · Giáp · Thực Thần / "
        "Mộc · Ất · Thương Quan"
    )
    assert analysis.useful_god.unfavorable_display == (
        "Thổ · Mậu · Thất Sát / Thổ · Kỷ · Chính Quan / "
        "Kim · Canh · Thiên Ấn / Kim · Tân · Chính Ấn / "
        "Thủy · Nhâm · Tỷ Kiên / Thủy · Quý · Kiếp Tài"
    )


def test_cool_monkey_month_strong_metal_uses_fire_and_wood_not_water() -> None:
    analysis = ProductionEngineRunner().run(DUONG_REQUEST).analysis

    assert analysis.strength.strength_level == "strong"
    assert analysis.bazi.day_master_element == "Kim"
    assert analysis.bazi.month_pillar.branch == "Thân"
    assert analysis.temperature.temperature_level == "cool"
    assert analysis.useful_god.winning_rule_id == "str_cool_monkey_strong_metal"
    assert analysis.useful_god.useful_display == "Hỏa · Bính · Chính Quan"
    assert analysis.useful_god.favorable_display == (
        "Hỏa · Đinh · Thất Sát / Mộc · Giáp · Chính Tài / "
        "Mộc · Ất · Thiên Tài"
    )
    assert "Thủy" not in analysis.useful_god.favorable_display


def test_cold_pig_month_strong_water_uses_fire_and_wood_not_earth() -> None:
    analysis = ProductionEngineRunner().run(HA_REQUEST).analysis

    assert analysis.strength.strength_level == "strong"
    assert analysis.bazi.day_master_element == "Thủy"
    assert analysis.bazi.month_pillar.branch == "Hợi"
    assert analysis.temperature.temperature_level == "cold"
    assert analysis.useful_god.winning_rule_id == "str_cold_pig_strong_water"
    assert analysis.useful_god.useful_display == "Hỏa · Bính · Thiên Tài"
    assert analysis.useful_god.favorable_display == (
        "Hỏa · Đinh · Chính Tài / Mộc · Giáp · Thực Thần / "
        "Mộc · Ất · Thương Quan"
    )
    assert "Thổ" not in analysis.useful_god.favorable_display


def test_warm_tiger_month_strong_fire_uses_water_with_metal_and_earth_support() -> None:
    analysis = ProductionEngineRunner().run(TRUNG_REQUEST).analysis

    assert analysis.strength.strength_level == "strong"
    assert analysis.bazi.day_master_element == "Hỏa"
    assert analysis.bazi.month_pillar.branch == "Dần"
    assert analysis.temperature.temperature_level == "warm"
    assert analysis.useful_god.winning_rule_id == "str_warm_tiger_strong_fire"
    assert analysis.useful_god.useful_display == "Thủy · Nhâm · Thất Sát"
    assert analysis.useful_god.favorable_display == (
        "Thủy · Quý · Chính Quan / Kim · Canh · Thiên Tài / "
        "Kim · Tân · Chính Tài / Thổ · Mậu · Thực Thần / "
        "Thổ · Kỷ · Thương Quan"
    )
    assert "Hỏa" not in analysis.useful_god.favorable_display
    assert "Mộc" not in analysis.useful_god.favorable_display


def test_hot_snake_month_balanced_water_has_specific_useful_god() -> None:
    analysis = ProductionEngineRunner().run(HUONG_MAI_REQUEST).analysis

    assert analysis.strength.strength_level == "balanced"
    assert analysis.bazi.day_master_element == "Thủy"
    assert analysis.bazi.month_pillar.branch == "Tỵ"
    assert analysis.temperature.temperature_level == "hot"
    assert analysis.pattern.pattern == "chinh_tai"
    assert analysis.useful_god.winning_rule_id == "str_balanced_hot_snake_water"
    assert analysis.useful_god.overall_incomplete is False
    assert analysis.useful_god.useful_display == "Thủy · Nhâm · Kiếp Tài"
    assert analysis.useful_god.favorable_display == (
        "Thủy · Quý · Tỷ Kiên / Kim · Canh · Chính Ấn / "
        "Kim · Tân · Thiên Ấn"
    )


def test_cool_rooster_month_balanced_fire_wealth_uses_wood_then_fire() -> None:
    result = ProductionEngineRunner().run(NGOC_REQUEST)
    analysis = result.analysis

    assert analysis.strength.strength_level == "balanced"
    assert analysis.bazi.day_master_element == "Hỏa"
    assert analysis.bazi.month_pillar.branch == "Dậu"
    assert analysis.temperature.temperature_level == "cool"
    assert analysis.pattern.pattern == "thien_tai"
    assert analysis.useful_god.winning_rule_id == (
        "str_balanced_cool_rooster_fire_wealth"
    )
    assert analysis.useful_god.overall_incomplete is False
    assert analysis.useful_god.useful_display == "Mộc · Giáp · Chính Ấn"
    assert analysis.useful_god.favorable_display == (
        "Mộc · Ất · Thiên Ấn / Hỏa · Bính · Kiếp Tài / "
        "Hỏa · Đinh · Tỷ Kiên"
    )
    assert analysis.useful_god.unfavorable_display == (
        "Kim · Canh · Chính Tài / Kim · Tân · Thiên Tài / "
        "Thủy · Nhâm · Chính Quan / Thủy · Quý · Thất Sát / "
        "Thổ · Mậu · Thương Quan / Thổ · Kỷ · Thực Thần"
    )


def test_1987_female_year_row_publishes_personal_khon_cung_phi() -> None:
    payload = OrchestratorService().analyze(
        year=1987,
        month=9,
        day=25,
        hour=3,
        minute=31,
        gender="female",
        timezone="Asia/Ho_Chi_Minh",
    )
    year = payload["bazi"]["year_pillar"]

    assert payload["calendar"]["cung_phi"] == "Khôn"
    assert year["cung_phi"] == "Khôn"
    assert year["ganzhi_cung_phi"] == "Tốn"
    assert year["cung_phi_basis"] == "personal_birth_year_gender"
    assert payload["identity"]["four_pillars"]["year"]["cung_phi"] == "Khôn"


def test_pre_tet_1987_male_publishes_lunar_1986_khon_everywhere() -> None:
    payload = OrchestratorService().analyze(
        year=1987,
        month=1,
        day=21,
        hour=4,
        minute=31,
        gender="male",
        timezone="Asia/Ho_Chi_Minh",
    )
    year = payload["bazi"]["year_pillar"]

    assert payload["calendar"]["lunar_year"] == 1986
    assert payload["calendar"]["cung_phi"] == "Khôn"
    assert year["cung_phi"] == "Khôn"
    assert year["ganzhi_cung_phi"] == "Khôn"
    assert payload["identity"]["four_pillars"]["year"]["cung_phi"] == "Khôn"
