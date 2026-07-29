from engines.strength_engine.context import StrengthContext
from engines.strength_engine.matcher import StrengthMatcher


def test_matcher_equality() -> None:
    ctx = StrengthContext(month_status="Đắc lệnh")
    matcher = StrengthMatcher()
    rule = {
        "conditions": '[{"field": "month_status", "operator": "==", "value": "Đắc lệnh"}]',
    }
    assert matcher.match(ctx, rule)


def test_matcher_contains() -> None:
    ctx = StrengthContext(resource_elements=["Chính Ấn"])
    matcher = StrengthMatcher()
    rule = {
        "conditions": '[{"field": "resource_elements", "operator": "contains", "value": "Chính Ấn"}]',
    }
    assert matcher.match(ctx, rule)


def test_matcher_numeric_gte() -> None:
    ctx = StrengthContext(drain_count=3)
    matcher = StrengthMatcher()
    rule = {
        "conditions": '[{"field": "drain_count", "operator": ">=", "value": 3}]',
    }
    assert matcher.match(ctx, rule)
