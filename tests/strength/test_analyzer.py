from engines.strength_engine.analyzer import StrengthAnalyzer
from engines.strength_engine.context import StrengthContext
from engines.strength_engine.loader import StrengthLoader
from engines.strength_engine.matcher import StrengthMatcher


def test_analyzer_matches_season_rules() -> None:
    ctx = StrengthContext(month_status="Đắc lệnh", root_level="Thông căn 1 chi")
    loader = StrengthLoader("database/12_strength")
    grouped = loader.load_rule_groups()
    analyzer = StrengthAnalyzer(StrengthMatcher())
    result = analyzer.analyze(ctx, grouped)
    assert result["season_matches"]
    assert any(m["rule_id"] == "sea_001" for m in result["season_matches"])
