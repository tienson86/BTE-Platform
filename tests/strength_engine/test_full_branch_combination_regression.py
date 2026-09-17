from __future__ import annotations

from applications.api.services.orchestrator import OrchestratorService
from engines.bazi_engine.engine import BaziEngine
from engines.calendar_engine.engine import CalendarEngine
from engines.strength_engine.utils.context_builder import build_strength_context


def test_huynh_fire_trine_changes_strength_and_useful_god() -> None:
    payload = OrchestratorService().analyze(
        year=1966,
        month=9,
        day=24,
        hour=4,
        minute=15,
        gender="male",
    )

    strength = payload["strength"]
    useful = payload["useful_god"]
    assert strength["strength_level"] == "strong"
    assert strength["strength_score"] == 0.82
    assert strength["combination_score"] == 0.18
    assert "Tam hợp Dần-Ngọ-Tuất thành thế Hỏa" in strength["evidence_compact"]
    assert useful["winning_rule_id"] == "str_full_fire"
    assert useful["useful_element"] == "Thủy"
    assert useful["useful_stem"] == "Nhâm"
    assert useful["climate_element"] == "Thủy"
    assert useful["climate_rule_group"] == "structural_reconciliation"
    assert "không tăng thêm hành trợ thân" in useful["climate_reason"]
    assert payload["temperature"]["recommendations"] == [useful["climate_reason"]]
    assert "Tăng dương khí" not in payload["temperature"]["recommendations"]
    assert useful["unfavorable_display"].startswith("Hỏa")


def test_strength_context_publishes_full_combination_evidence() -> None:
    calendar = CalendarEngine().build(1966, 9, 24, 4, 15)
    chart = BaziEngine().build(calendar, gender="male")
    context = build_strength_context(chart, calendar=calendar)

    assert context.self_element_full_combination is True
    assert context.dominant_combination_element == "Hỏa"
    assert context.branch_combinations == [
        {
            "kind": "tam_hop",
            "branches": ["Dần", "Ngọ", "Tuất"],
            "element": "Hỏa",
            "transformed": True,
            "reason": "đủ bộ và hành cục thấu/lâm nguyệt lệnh",
        }
    ]
