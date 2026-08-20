"""G1-02R Strength correctness: drain, root, overlap, aggregation."""

from __future__ import annotations

from engines.bazi_engine.engine import BaziChart, BaziEngine, HIDDEN, Pillar
from engines.bazi_engine.ten_god import ten_god_name
from engines.calendar_engine.engine import CalendarEngine
from engines.strength_engine.engine import StrengthEngine
from engines.strength_engine.labels import strength_level_label
from engines.strength_engine.utils.context_builder import build_strength_context


def _chart_from_pillars(pillars: list[tuple[str, str]], gender: str = "female") -> BaziChart:
    parts = [Pillar(stem=stem, branch=branch) for stem, branch in pillars]
    hidden = [stem for pillar in parts for stem in HIDDEN[pillar.branch]]
    day_master = parts[2].stem
    ten_gods = [
        "Nhật Chủ" if pillar is parts[2] else ten_god_name(day_master, pillar.stem)
        for pillar in parts
    ]
    return BaziChart(*parts, gender=gender, hidden_stems=hidden, ten_gods=ten_gods)


def _strength(chart: BaziChart):
    return StrengthEngine().calculate(build_strength_context(chart))


def _son_chart() -> BaziChart:
    calendar = CalendarEngine().build(1987, 1, 21, 4, 30)
    return BaziEngine().build(calendar, gender="male")


def _dung_chart() -> BaziChart:
    return _chart_from_pillars(
        [("Nhâm", "Tuất"), ("Ất", "Tỵ"), ("Ất", "Tỵ"), ("Tân", "Tỵ")],
        gender="female",
    )


def test_control_case_son_unchanged() -> None:
    result = _strength(_son_chart())
    assert result.raw_total == 37.0
    assert abs(result.strength_score - 0.87) < 0.001
    assert result.strength_level == "strong"
    assert strength_level_label(result.strength_level) == "Thân vượng"
    assert result.drain_score == 0.0
    assert "flw_001" not in result.matched_rules
    assert "flw_005" not in result.matched_rules


def test_no_root_chart_vo_can_minus_20() -> None:
    ctx = build_strength_context(_dung_chart())
    result = _strength(_dung_chart())
    assert ctx.root_level == "Vô căn"
    assert ctx.root_count == 0
    assert "root_005" in result.matched_rules
    assert abs(result.root_score + 0.20) < 0.001


def test_repeated_output_branches_count_per_pillar() -> None:
    ctx = build_strength_context(_dung_chart())
    assert ctx.output_branch_count == 3
    assert ctx.drain_type == "Thực Thương tiết khí"
    assert ctx.drain_count >= 3


def test_strong_drain_output_chart_matches_flow_rules() -> None:
    result = _strength(_dung_chart())
    assert "flw_001" in result.matched_rules
    assert "flw_005" in result.matched_rules
    assert result.drain_score < 0
    assert abs(result.drain_score - (-0.18)) < 0.001


def test_visible_versus_hidden_drain() -> None:
    """Sơn has residual hidden output (Quý in Sửu) but no output-branch bản khí."""
    son_ctx = build_strength_context(_son_chart())
    dung_ctx = build_strength_context(_dung_chart())
    assert son_ctx.output_branch_count == 0
    assert son_ctx.drain_type is None
    assert dung_ctx.output_branch_count == 3
    assert dung_ctx.drain_type == "Thực Thương tiết khí"


def test_resource_and_resource_ten_god_overlap_provenance() -> None:
    ctx = build_strength_context(_dung_chart())
    result = _strength(_dung_chart())
    assert ctx.support_type == "Ấn tinh sinh thân"
    assert ctx.resource_elements == ["Chính Ấn"]
    assert "sup_002" in result.matched_rules
    assert "sup_006" in result.matched_rules


def test_control_and_drain_simultaneous() -> None:
    result = _strength(_dung_chart())
    assert "ctl_001" in result.matched_rules
    assert "flw_001" in result.matched_rules
    assert result.control_score < 0
    assert result.drain_score < 0


def test_dung_weak_after_drain_connected() -> None:
    result = _strength(_dung_chart())
    assert result.raw_total == -26.0
    assert abs(result.strength_score - 0.24) < 0.001
    assert result.strength_level == "weak"
    assert strength_level_label(result.strength_level) == "Thân nhược"


def test_weak_fixture_ex002_profile() -> None:
    calendar = CalendarEngine().build(1960, 7, 1, 12, 0)
    chart = BaziEngine().build(calendar, gender="male")
    ctx = build_strength_context(chart)
    result = _strength(chart)
    assert ctx.month_status == "Tử"
    assert ctx.root_level == "Vô căn"
    assert "sea_005" in result.matched_rules
    assert "root_005" in result.matched_rules
    assert result.strength_level == "weak"
    assert result.raw_total < 0


def test_balanced_fixture_not_forced() -> None:
    calendar = CalendarEngine().build(1976, 4, 12, 10, 0)
    ctx = build_strength_context(BaziEngine().build(calendar, gender="female"))
    result = StrengthEngine().calculate(ctx)
    assert result.success
    assert result.strength_level == "balanced"
    assert 0.35 < result.strength_score < 0.65
    assert ctx.root_count >= 1


def test_additional_strong_giap_dan_season() -> None:
    calendar = CalendarEngine().build(1974, 2, 12, 8, 0)
    ctx = build_strength_context(BaziEngine().build(calendar, gender="male"))
    result = StrengthEngine().calculate(ctx)
    assert ctx.month_status == "Đắc lệnh"
    assert "sea_001" in result.matched_rules
    assert result.strength_level == "strong"
    assert result.season_score > 0
