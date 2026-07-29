from engines.pattern_engine.context import PatternContext
from engines.useful_god_engine.analyzer import UsefulGodAnalyzer
from engines.useful_god_engine.matcher import UsefulGodMatcher
from engines.useful_god_engine.utils.context_builder import build_useful_god_context


def test_analyzer_runs_all_stages() -> None:
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
        element_distribution={"Mộc": 2, "Thổ": 2},
        resource_elements=["Chính Ấn"],
        ten_gods_list=["Chính Ấn"],
    )
    ctx = build_useful_god_context(pc)
    analyzer = UsefulGodAnalyzer(UsefulGodMatcher())
    groups = {
        "strength": [{"rule_id": "a", "conditions": '[{"field":"strength_level","operator":"==","value":"weak"}]', "status": "active"}],
        "season": [],
        "temperature": [],
        "flow": [],
        "special": [],
    }
    data = analyzer.analyze(ctx, groups)
    assert "balance_summary" in data
    assert len(data["strength_candidates"]) == 1
