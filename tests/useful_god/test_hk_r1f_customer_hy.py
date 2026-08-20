"""HK-R1F: customer Hỷ omits exact Dụng; internal favorable set unchanged."""

from __future__ import annotations

from applications.api.services.orchestrator import OrchestratorService
from applications.api.services.useful_god_truth import build_useful_god_view
from engines.bazi_engine.engine import BaziChart, HIDDEN, Pillar
from engines.bazi_engine.ten_god import ten_god_name
from engines.pattern_engine.engine import PatternEngine
from engines.pattern_engine.utils.context_builder import build_pattern_context
from engines.useful_god_engine.engine import UsefulGodEngine
from engines.useful_god_engine.presentation import (
    EMPTY_CUSTOMER_FAVORABLE_DISPLAY,
    customer_favorable_display,
    customer_favorable_roles,
    is_exact_dung_duplicate,
)
from engines.useful_god_engine.utils.context_builder import build_useful_god_context


def _dung_chart() -> BaziChart:
    year = Pillar(stem="Ất", branch="Sửu")
    month = Pillar(stem="Ất", branch="Dậu")
    day = Pillar(stem="Canh", branch="Thân")
    hour = Pillar(stem="Canh", branch="Thìn")
    pillars = [year, month, day, hour]
    hidden = [stem for pillar in pillars for stem in HIDDEN[pillar.branch]]
    dm = day.stem
    ten_gods = [
        "Nhật Chủ" if pillar is day else ten_god_name(dm, pillar.stem) for pillar in pillars
    ]
    return BaziChart(*pillars, gender="male", hidden_stems=hidden, ten_gods=ten_gods)


def test_exact_duplicate_requires_all_three_fields() -> None:
    dung = {"element": "Thủy", "stem": "Nhâm", "ten_god": "Thực Thần"}
    assert is_exact_dung_duplicate(dung, dung) is True
    assert (
        is_exact_dung_duplicate(
            {"element": "Thủy", "stem": "Quý", "ten_god": "Thương Quan"},
            dung,
        )
        is False
    )
    assert (
        is_exact_dung_duplicate(
            {"element": "Thủy", "stem": "", "ten_god": "Thực Thần"},
            dung,
        )
        is False
    )


def test_empty_remainder_does_not_reinsert_dung() -> None:
    dung = {"element": "Thủy", "stem": "Nhâm", "ten_god": "Thực Thần"}
    remaining = customer_favorable_roles(dung, [dung])
    assert remaining == []
    assert customer_favorable_display(dung, [dung]) == EMPTY_CUSTOMER_FAVORABLE_DISPLAY


def test_dung_customer_hy_omits_exact_dung_keeps_same_element() -> None:
    chart = _dung_chart()
    context = build_pattern_context(chart)
    context.strength_level = "strong"
    context.strength_score = 1.0
    pattern = PatternEngine().calculate(context)
    engine = UsefulGodEngine().calculate(build_useful_god_context(context, pattern))
    view = build_useful_god_view(engine)

    assert engine.useful_display == "Thủy · Nhâm · Thực Thần"
    assert engine.favorable_gods == ["Thực Thần", "Thương Quan"]
    assert engine.favorable_display.startswith("Thủy · Nhâm · Thực Thần")
    assert view.favorable_gods == engine.favorable_gods
    assert view.canonical_favorable_display == engine.favorable_display
    assert view.favorable_display == "Thủy · Quý · Thương Quan"
    assert "Nhâm" not in view.favorable_display
    assert view.unfavorable_display == engine.unfavorable_display
    assert view.useful_display == engine.useful_display
    assert view.winning_rule_id == engine.winning_rule_id


def test_api_tuyen_customer_hy_is_canh_thuc_than() -> None:
    payload = OrchestratorService().analyze(
        year=1984, month=7, day=13, hour=21, minute=1, gender="female"
    )
    useful = payload["useful_god"]
    assert useful["useful_display"] == "Mộc · Ất · Chính Quan"
    assert useful["favorable_gods"] == ["Chính Quan", "Thực Thần"]
    assert useful["canonical_favorable_display"].startswith("Mộc · Ất · Chính Quan")
    assert useful["favorable_display"] == "Kim · Canh · Thực Thần"
    assert useful["unfavorable_display"].startswith("Thổ · Mậu · Tỷ Kiên")
    assert payload["pattern"]["hy_than"] == "Thực Thần"
    assert "Chính Quan" not in useful["favorable_display"]


def test_api_dung_customer_hy_is_quy_thuong_quan() -> None:
    payload = OrchestratorService().analyze(
        year=1985,
        month=9,
        day=18,
        hour=8,
        minute=0,
        gender="male",
        timezone="Asia/Bangkok",
    )
    useful = payload["useful_god"]
    assert useful["useful_display"] == "Thủy · Nhâm · Thực Thần"
    assert useful["favorable_gods"] == ["Thực Thần", "Thương Quan"]
    assert useful["favorable_display"] == "Thủy · Quý · Thương Quan"
    assert useful["unfavorable_display"].startswith("Kim · Canh · Tỷ Kiên")
    assert payload["pattern"]["hy_than"] == "Thương Quan"
