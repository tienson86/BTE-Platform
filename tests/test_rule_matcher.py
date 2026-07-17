"""
Test Rule Matcher

Kiểm tra:
- Khởi tạo RuleMatcher
- So khớp điều kiện rule với Context
- Xử lý nhiều điều kiện
- Xử lý rule lỗi
"""


import pytest


from interpretation_engine.rule_matcher import RuleMatcher
from interpretation_engine.context import InterpretationContext



# ==================================================
# Test khởi tạo
# ==================================================

def test_rule_matcher_create():

    matcher = RuleMatcher()

    assert matcher is not None



# ==================================================
# Test match điều kiện đơn giản
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
# Test không match
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
# Test nhiều điều kiện
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
# Test nhiều điều kiện nhưng sai một phần
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
# Test rule không có condition
# ==================================================

def test_empty_condition():

    ctx = InterpretationContext()


    rule = {

        "rule_id":
        "R001"

    }


    matcher = RuleMatcher()


    result = matcher.match(
        rule,
        ctx
    )


    assert result is False



# ==================================================
# Test context thiếu dữ liệu
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
