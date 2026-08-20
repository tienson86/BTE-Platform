"""G1-X01 Useful God follow-token normalization and Tuyền spc_001 guard."""

from __future__ import annotations

from applications.api.services.orchestrator import OrchestratorService
from engines.bazi_engine.engine import BaziEngine
from engines.calendar_engine.engine import CalendarEngine
from engines.pattern_engine.context import PatternContext
from engines.pattern_engine.engine import PatternEngine, PatternResult
from engines.pattern_engine.utils.context_builder import build_pattern_context
from engines.useful_god_engine.context import UsefulGodContext
from engines.useful_god_engine.engine import UsefulGodEngine
from engines.useful_god_engine.matcher import UsefulGodMatcher
from engines.useful_god_engine.utils.context_builder import build_useful_god_context


def _calculate(context: UsefulGodContext):
    return UsefulGodEngine().calculate(context)


def test_builder_normalizes_display_label_to_canonical_token() -> None:
    result = PatternResult(pattern="tong_tai", follow_type="Tòng Tài")
    ctx = build_useful_god_context(PatternContext(day_master="Mậu"), result)
    assert ctx.follow_pattern == "tong_tai"


def test_spc_001_matches_token_not_vietnamese_label() -> None:
    with_token = _calculate(
        UsefulGodContext(day_master="Mậu", follow_pattern="tong_tai")
    )
    assert with_token.winning_rule_id == "spc_001"
    with_label = _calculate(
        UsefulGodContext(
            day_master="Mậu",
            follow_pattern="Tòng Tài",
            strength_level="weak",
            season="summer",
            temperature_type="hot",
        )
    )
    assert with_label.winning_rule_id != "spc_001"


def test_legitimate_engine_tong_tai_still_reaches_spc_001() -> None:
    gods = ["Chính Tài"] * 6 + ["Tỷ Kiên"]
    pattern_context = PatternContext(
        day_master="Giáp",
        strength_level="weak",
        ten_gods={"list": list(gods)},
        ten_gods_list=list(gods),
        month_branch_ten_god="Chính Tài",
        season="spring",
        temperature_type="warm",
    )
    pattern = PatternEngine().calculate(pattern_context)
    assert pattern.follow_type == "tong_tai"
    useful = _calculate(build_useful_god_context(pattern_context, pattern))
    assert useful.winning_rule_id == "spc_001"


def test_tuyen_does_not_win_spc_001_after_strength_gate() -> None:
    payload = OrchestratorService().analyze(
        year=1984, month=7, day=13, hour=21, minute=1, gender="female"
    )
    useful = payload["useful_god"]
    assert useful["winning_rule_id"] != "spc_001"
    ids = [str(item.get("rule_id") or "") for item in useful.get("candidate_list") or []]
    assert "spc_001" not in ids


def test_tuyen_flo_004_uses_unique_maximum_not_key_presence() -> None:
    matcher = UsefulGodMatcher()
    calendar = CalendarEngine().build(1984, 7, 13, 21, 1)
    chart = BaziEngine().build(calendar, gender="female")
    pattern_context = build_pattern_context(chart, calendar=calendar)
    dist = dict(pattern_context.element_distribution or {})
    unique_max = matcher.evaluate(dist, "contains", "Thủy")
    payload = OrchestratorService().analyze(
        year=1984, month=7, day=13, hour=21, minute=1, gender="female"
    )
    ids = [
        str(item.get("rule_id") or "")
        for item in (payload["useful_god"].get("candidate_list") or [])
    ]
    assert matcher.evaluate(
        {"Mộc": 2, "Hỏa": 4, "Thổ": 5, "Kim": 3, "Thủy": 1}, "contains", "Thủy"
    ) is False
    if unique_max:
        assert "flo_004" in ids
    else:
        assert "flo_004" not in ids
