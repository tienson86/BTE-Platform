"""G1-03 canonical Pattern identification, evidence, and fallback."""

from __future__ import annotations

from applications.api.services.orchestrator import OrchestratorService
from applications.api.services.pattern_truth import build_pattern_view
from engines.bazi_engine.engine import BaziEngine
from engines.bazi_engine.ten_god import ten_god_name
from engines.calendar_engine.engine import CalendarEngine
from engines.pattern_engine.context import PatternContext
from engines.pattern_engine.engine import PatternEngine
from engines.pattern_engine.utils.context_builder import build_pattern_context


def _case_0001_chart() -> tuple[object, object]:
    calendar = CalendarEngine().build(1987, 1, 21, 4, 30)
    chart = BaziEngine().build(calendar, gender="male")
    return calendar, chart


def test_canh_ky_is_chinh_an() -> None:
    assert ten_god_name("Canh", "Kỷ") == "Chính Ấn"


def test_case_0001_canonical_context() -> None:
    calendar, chart = _case_0001_chart()
    ctx = build_pattern_context(chart, calendar=calendar)
    assert ctx.month_branch == "Sửu"
    assert ctx.month_hidden_stems == ["Kỷ", "Quý", "Tân"]
    assert ctx.month_main_qi == "Kỷ"
    assert ctx.day_master == "Canh"
    assert ctx.month_branch_ten_god == "Chính Ấn"


def test_case_0001_primary_pattern_pat_ca_01() -> None:
    calendar, chart = _case_0001_chart()
    result = PatternEngine().calculate(build_pattern_context(chart, calendar=calendar))
    assert result.success
    assert result.pattern == "chinh_an"
    assert result.cach_cuc == "Chính Ấn"
    assert result.winning_rule_id == "pat_ca_01"
    assert result.fallback_used is False
    assert result.month_main_qi == "Kỷ"
    assert result.month_main_qi_ten_god == "Chính Ấn"
    assert result.penetration_exact is False
    related_stems = [item.get("stem") for item in result.penetration_related]
    related_gods = [item.get("ten_god") for item in result.penetration_related]
    assert "Mậu" in related_stems
    assert "Thiên Ấn" in related_gods
    assert "Kỷ" not in related_stems
    assert "sat_an" not in result.validated_patterns
    assert "Nguyệt lệnh Sửu" in result.evidence_compact
    assert "khí chính Kỷ" in result.evidence_compact
    assert "Kỷ đối với Canh là Chính Ấn" in result.evidence_compact
    assert "Kỷ không thấu trực tiếp" in result.evidence_compact
    assert "Mậu" in result.evidence_compact
    assert "thành cách" not in result.evidence_compact.lower()
    assert "phá cách" not in result.evidence_compact.lower()


def test_complete_bazi_without_prebuilt_context_does_not_fallback() -> None:
    calendar, chart = _case_0001_chart()
    incomplete = PatternContext(
        day_master=chart.day_master,
        calendar=calendar,
        bazi=chart,
    )
    result = PatternEngine().calculate(incomplete)
    assert result.fallback_used is False
    assert result.pattern == "chinh_an"
    assert result.winning_rule_id == "pat_ca_01"


def test_empty_context_may_use_fallback() -> None:
    result = PatternEngine().calculate(PatternContext())
    assert result.fallback_used is True
    assert result.pattern == "chinh_quan"


def test_combination_priority_beats_main_when_both_match() -> None:
    context = PatternContext(
        day_master="Canh",
        month_branch="Sửu",
        month_main_qi="Kỷ",
        month_branch_ten_god="Chính Ấn",
        ten_gods_list=["Thất Sát", "Chính Ấn"],
        ten_gods={"list": ["Thất Sát", "Chính Ấn"]},
    )
    result = PatternEngine().calculate(context)
    assert result.priority == 85
    assert result.pattern == "sat_an"
    assert result.winning_rule_id == "com_san_01"
    assert "chinh_an" in result.candidate_patterns


def test_orchestrator_matches_engine_chinh_an() -> None:
    calendar, chart = _case_0001_chart()
    engine = PatternEngine().calculate(build_pattern_context(chart, calendar=calendar))
    payload = OrchestratorService().analyze(
        year=1987, month=1, day=21, hour=4, minute=30, gender="male"
    )
    view = build_pattern_view(engine)
    assert payload["pattern"]["cach_cuc"] == "Chính Ấn"
    assert payload["pattern"]["pattern"] == "chinh_an"
    assert payload["pattern"]["winning_rule_id"] == "pat_ca_01"
    assert payload["pattern"]["fallback_used"] is False
    assert view.cach_cuc == payload["pattern"]["cach_cuc"]
    assert payload["pattern"]["cach_cuc"] != "Chính Quan"
