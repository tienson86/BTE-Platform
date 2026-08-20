"""G1-02R2: drain and support paths must work for all five Day Master elements."""

from __future__ import annotations

from engines.bazi_engine.engine import BaziChart, HIDDEN, Pillar
from engines.bazi_engine.ten_god import ten_god_name
from engines.strength_engine.engine import StrengthEngine
from engines.strength_engine.utils.context_builder import build_strength_context

_OUTPUT_DRAIN = "Thực Thương tiết khí"
_PEER_SUPPORT = "Đồng hành trợ thân"
_RESOURCE_SUPPORT = "Ấn tinh sinh thân"


def _chart(pillars: list[tuple[str, str]], gender: str = "male") -> BaziChart:
    parts = [Pillar(stem=stem, branch=branch) for stem, branch in pillars]
    hidden = [stem for pillar in parts for stem in HIDDEN[pillar.branch]]
    day_master = parts[2].stem
    ten_gods = [
        "Nhật Chủ" if pillar is parts[2] else ten_god_name(day_master, pillar.stem)
        for pillar in parts
    ]
    return BaziChart(*parts, gender=gender, hidden_stems=hidden, ten_gods=ten_gods)


def _ctx_result(pillars: list[tuple[str, str]]):
    chart = _chart(pillars)
    ctx = build_strength_context(chart)
    result = StrengthEngine().calculate(ctx)
    return ctx, result


def test_wood_drains_to_fire_via_ty_branch() -> None:
    ctx, result = _ctx_result(
        [("Nhâm", "Tý"), ("Quý", "Tỵ"), ("Ất", "Hợi"), ("Giáp", "Hợi")]
    )
    assert ctx.day_master_element == "Mộc"
    assert ctx.output_branch_count >= 1
    assert ctx.drain_type == _OUTPUT_DRAIN
    assert "flw_001" in result.matched_rules


def test_fire_drains_to_earth_via_tuat_branch() -> None:
    ctx, result = _ctx_result(
        [("Giáp", "Dần"), ("Ất", "Mão"), ("Bính", "Tuất"), ("Đinh", "Dần")]
    )
    assert ctx.day_master_element == "Hỏa"
    assert ctx.output_branch_count >= 1
    assert ctx.drain_type == _OUTPUT_DRAIN
    assert "flw_001" in result.matched_rules


def test_earth_drains_to_metal_via_dau_branch() -> None:
    ctx, result = _ctx_result(
        [("Bính", "Ngọ"), ("Đinh", "Tỵ"), ("Mậu", "Thìn"), ("Kỷ", "Dậu")]
    )
    assert ctx.day_master_element == "Thổ"
    assert ctx.output_branch_count >= 1
    assert ctx.drain_type == _OUTPUT_DRAIN
    assert "flw_001" in result.matched_rules


def test_metal_drains_to_water_via_hoi_branch() -> None:
    ctx, result = _ctx_result(
        [("Mậu", "Tuất"), ("Kỷ", "Sửu"), ("Canh", "Thân"), ("Tân", "Hợi")]
    )
    assert ctx.day_master_element == "Kim"
    assert ctx.output_branch_count >= 1
    assert ctx.drain_type == _OUTPUT_DRAIN
    assert "flw_001" in result.matched_rules


def test_water_drains_to_wood_via_dan_branch() -> None:
    ctx, result = _ctx_result(
        [("Canh", "Thân"), ("Tân", "Dậu"), ("Nhâm", "Tý"), ("Quý", "Dần")]
    )
    assert ctx.day_master_element == "Thủy"
    assert ctx.output_branch_count >= 1
    assert ctx.drain_type == _OUTPUT_DRAIN
    assert "flw_001" in result.matched_rules


def test_wood_peer_support_path() -> None:
    ctx, result = _ctx_result(
        [("Giáp", "Tý"), ("Ất", "Hợi"), ("Ất", "Hợi"), ("Nhâm", "Tý")]
    )
    assert ctx.support_type == _PEER_SUPPORT
    assert "sup_001" in result.matched_rules


def test_wood_resource_support_path() -> None:
    ctx, result = _ctx_result(
        [("Nhâm", "Tý"), ("Quý", "Hợi"), ("Ất", "Hợi"), ("Canh", "Thân")]
    )
    assert ctx.support_type == _RESOURCE_SUPPORT
    assert "sup_002" in result.matched_rules


def test_fire_peer_support_path() -> None:
    ctx, result = _ctx_result(
        [("Bính", "Dần"), ("Đinh", "Mão"), ("Bính", "Dần"), ("Giáp", "Dần")]
    )
    assert ctx.support_type == _PEER_SUPPORT
    assert "sup_001" in result.matched_rules


def test_fire_resource_support_path() -> None:
    ctx, result = _ctx_result(
        [("Giáp", "Dần"), ("Ất", "Mão"), ("Bính", "Dần"), ("Giáp", "Mão")]
    )
    assert ctx.support_type == _RESOURCE_SUPPORT
    assert "sup_002" in result.matched_rules


def test_live_cases_unchanged_by_symmetry_coverage() -> None:
    """Symmetry tests must not imply a retune of the three frozen charts."""
    from engines.bazi_engine.engine import BaziEngine
    from engines.calendar_engine.engine import CalendarEngine

    son = BaziEngine().build(CalendarEngine().build(1987, 1, 21, 4, 30), gender="male")
    huynh = BaziEngine().build(CalendarEngine().build(1966, 9, 24, 4, 15), gender="male")
    dung = _chart(
        [("Nhâm", "Tuất"), ("Ất", "Tỵ"), ("Ất", "Tỵ"), ("Tân", "Tỵ")],
        gender="female",
    )
    son_r = StrengthEngine().calculate(build_strength_context(son))
    huynh_r = StrengthEngine().calculate(build_strength_context(huynh))
    dung_r = StrengthEngine().calculate(build_strength_context(dung))
    assert son_r.raw_total == 37.0
    assert abs(son_r.strength_score - 0.87) < 0.001
    assert son_r.strength_level == "strong"
    assert huynh_r.raw_total == 14.0
    assert abs(huynh_r.strength_score - 0.64) < 0.001
    assert huynh_r.strength_level == "balanced"
    assert dung_r.raw_total == -26.0
    assert abs(dung_r.strength_score - 0.24) < 0.001
    assert dung_r.strength_level == "weak"
