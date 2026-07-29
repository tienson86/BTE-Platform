from engines.pattern_engine.context import PatternContext
from engines.useful_god_engine.engine import UsefulGodEngine
from engines.useful_god_engine.utils.context_builder import build_useful_god_context


def test_engine_returns_useful_god() -> None:
    pc = PatternContext(
        day_master="Giáp",
        day_master_element="Mộc",
        month_branch="Sửu",
        month_branch_element="Thổ",
        month_branch_ten_god="Chính Tài",
        strength_level="weak",
        season="winter",
        season_phase="late_winter",
        temperature_type="cold",
        element_distribution={"Mộc": 2, "Thổ": 4},
        resource_elements=["Chính Ấn"],
        ten_gods_list=["Chính Ấn", "Chính Quan"],
    )
    ctx = build_useful_god_context(pc)
    engine = UsefulGodEngine(database_path="database/13_useful_god")
    result = engine.calculate(ctx)
    assert result.success
    assert result.useful_god is not None
    assert result.matched_rules
