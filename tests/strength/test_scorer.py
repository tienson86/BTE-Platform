from engines.strength_engine.analyzer import StrengthAnalyzer
from engines.strength_engine.context import StrengthContext
from engines.strength_engine.loader import StrengthLoader
from engines.strength_engine.matcher import StrengthMatcher
from engines.strength_engine.priority import StrengthPriorityResolver
from engines.strength_engine.scorer import StrengthScorer


def test_scorer_aggregates_component_scores() -> None:
    ctx = StrengthContext(month_status="Đắc lệnh", root_level="Thông căn 2 chi")
    loader = StrengthLoader("database/12_strength")
    grouped = loader.load_rule_groups()
    analyzer = StrengthAnalyzer(StrengthMatcher())
    analysis = analyzer.analyze(ctx, grouped)
    config = loader.load_config()
    level_rules = loader.load_level_rules()
    resolver = StrengthPriorityResolver(loader.load_priority_rules())
    scored = StrengthScorer().score(ctx, analysis, config, level_rules, StrengthMatcher(), resolver)
    assert scored["season_score"] != 0.0 or scored["root_score"] != 0.0
    assert 0.0 <= scored["strength_score"] <= 1.0
