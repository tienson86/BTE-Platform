from engines.strength_engine.context import StrengthContext
from engines.strength_engine.engine import StrengthEngine


def test_engine_returns_strength_result() -> None:
    ctx = StrengthContext(
        day_master="Giáp",
        day_master_element="Mộc",
        month_branch="Dần",
        month_branch_element="Mộc",
        month_branch_ten_god="Tỷ Kiên",
        month_status="Đắc lệnh",
        root_level="Thông căn 1 chi",
        support_type="Đồng hành trợ thân",
        season="spring",
        resource_elements=["Chính Ấn"],
        companion_elements=["Tỷ Kiên"],
        ten_gods_list=["Tỷ Kiên", "Chính Ấn"],
    )
    engine = StrengthEngine(database_path="database/12_strength")
    result = engine.calculate(ctx)
    assert result.success
    assert result.strength_level in {"strong", "balanced", "weak"}
    assert result.matched_rules
    assert result.strength_score >= 0.0


def test_engine_weak_chart() -> None:
    ctx = StrengthContext(
        day_master="Canh",
        day_master_element="Kim",
        month_branch="Ngọ",
        month_branch_element="Hỏa",
        month_status="Tử",
        root_level="Vô căn",
        control_type="Bị Quan Sát khắc",
        officer_elements=["Thất Sát"],
        season="summer",
    )
    engine = StrengthEngine(database_path="database/12_strength")
    result = engine.calculate(ctx)
    assert result.success
    assert result.strength_level == "weak"
