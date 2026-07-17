"""
Test Rule Matcher

Kiểm tra:
- Khởi tạo RuleMatcher
- Match rule với Context
- Match nhiều điều kiện
- Match dữ liệu load từ RuleLoader
- Xử lý rule không hợp lệ
"""


from interpretation_engine.rule_matcher import RuleMatcher
from interpretation_engine.context import InterpretationContext
from interpretation_engine.rule_loader import RuleLoader



# ==================================================
# Khởi tạo Matcher
# ==================================================

def test_rule_matcher_create():

    matcher = RuleMatcher()

    assert matcher is not None



# ==================================================
# Match điều kiện đơn
# ==================================================

def test_match_simple_condition():

    ctx = InterpretationContext()


    ctx.set(
        "nhat_chu",
        "Canh Kim"
    )


    rule = {

        "condition":
        "nhat_chu=Canh Kim"

    }


    matcher = RuleMatcher()


    result = matcher.match(
        rule,
        ctx
    )


    assert result is True



# ==================================================
# Không match điều kiện sai
# ==================================================

def test_not_match_condition():

    ctx = InterpretationContext()


    ctx.set(
        "nhat_chu",
        "Canh Kim"
    )


    rule = {

        "condition":
        "nhat_chu=Giap Moc"

    }


    matcher = RuleMatcher()


    result = matcher.match(
        rule,
        ctx
    )


    assert result is False



# ==================================================
# Match nhiều điều kiện dạng dictionary
# ==================================================

def test_match_multiple_conditions():

    ctx = InterpretationContext()


    ctx.set(
        "nhat_chu",
        "Canh Kim"
    )


    ctx.set(
        "ngu_hanh",
        "Kim"
    )


    rule = {

        "condition":
        {

            "nhat_chu":
            "Canh Kim",

            "ngu_hanh":
            "Kim"

        }

    }


    matcher = RuleMatcher()


    result = matcher.match(
        rule,
        ctx
    )


    assert result is True



# ==================================================
# Một điều kiện đúng, một điều kiện sai
# ==================================================

def test_fail_multiple_conditions():

    ctx = InterpretationContext()


    ctx.set(
        "nhat_chu",
        "Canh Kim"
    )


    ctx.set(
        "ngu_hanh",
        "Moc"
    )


    rule = {

        "condition":
        {

            "nhat_chu":
            "Canh Kim",

            "ngu_hanh":
            "Kim"

        }

    }


    matcher = RuleMatcher()


    result = matcher.match(
        rule,
        ctx
    )


    assert result is False



# ==================================================
# Test Rule từ CSV
# ==================================================

def test_match_loaded_rule():

    loader = RuleLoader()


    rules = loader.load(
        "tests/data/test_rules.csv"
    )


    rule = rules[0]


    ctx = InterpretationContext()


    ctx.set(
        "nhat_chu",
        "Canh Kim"
    )


    matcher = RuleMatcher()


    result = matcher.match(
        rule,
        ctx
    )


    assert result is True



# ==================================================
# Test nhiều rule
# ==================================================

def test_filter_matching_rules():

    loader = RuleLoader()


    rules = loader.load(
        "tests/data/test_rules.csv"
    )


    ctx = InterpretationContext()


    ctx.set(
        "nhat_chu",
        "Canh Kim"
    )


    matcher = RuleMatcher()


    matched = []


    for rule in rules:

        if matcher.match(
            rule,
            ctx
        ):

            matched.append(rule)



    assert len(matched) >= 1



# ==================================================
# Rule không có condition
# ==================================================

def test_empty_condition():

    ctx = InterpretationContext()


    rule = {

        "rule_id":
        "TEST001"

    }


    matcher = RuleMatcher()


    result = matcher.match(
        rule,
        ctx
    )


    assert result is False



# ==================================================
# Context không có dữ liệu
# ==================================================

def test_missing_context_value():

    ctx = InterpretationContext()


    rule = {

        "condition":
        "nhat_chu=Canh Kim"

    }


    matcher = RuleMatcher()


    result = matcher.match(
        rule,
        ctx
    )


    assert result is False
