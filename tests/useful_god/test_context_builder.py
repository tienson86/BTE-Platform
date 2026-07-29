from engines.pattern_engine.context import PatternContext
from engines.useful_god_engine.utils.context_builder import build_useful_god_context


def test_context_builder_maps_fields() -> None:
    pc = PatternContext(
        day_master="Giáp",
        day_master_element="Mộc",
        day_master_yin_yang="Dương",
        month_branch="Sửu",
        month_branch_element="Thổ",
        month_branch_ten_god="Chính Tài",
        strength_level="weak",
        season="winter",
        season_phase="late_winter",
        temperature_type="cold",
        element_distribution={"Mộc": 2, "Thổ": 4},
        resource_elements=["Chính Ấn"],
        officer_elements=["Chính Quan"],
        ten_gods_list=["Chính Ấn", "Chính Quan"],
    )
    ctx = build_useful_god_context(pc)
    assert ctx.day_master == "Giáp"
    assert ctx.month_branch_ten_god == "Chính Tài"
    assert ctx.element_distribution["Thổ"] == 4
