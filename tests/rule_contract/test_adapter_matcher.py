"""
WP2B-2 unit tests — Rule Adapter + Matcher V1.
"""

from __future__ import annotations

import unittest

from engines.rule_contract import (
    RuleAdapter,
    RuleConditionMatcher,
    RuleContract,
)
from engines.rule_contract.models import ConditionPredicate
from engines.score_engine.matcher import RuleMatcher as ScoreRuleMatcher


class TestRuleAdapterEnum(unittest.TestCase):
    """ENUM_TOKEN_ASCII → Contract V1."""

    def setUp(self) -> None:
        self.adapter = RuleAdapter()

    def test_present_with_element(self) -> None:
        contract = self.adapter.adapt(
            {"element": "WOOD", "condition": "PRESENT", "score": 5}
        )
        self.assertEqual(contract.source_type, "ENUM_TOKEN_ASCII")
        self.assertEqual(len(contract.conditions), 1)
        pred = contract.conditions[0]
        self.assertEqual(pred.field, "wuxing.wood.status")
        self.assertEqual(pred.normalized_operator(), "eq")
        self.assertEqual(pred.value, "PRESENT")


class TestRuleAdapterStatus(unittest.TestCase):
    """STATUS_PHRASE → Contract V1."""

    def setUp(self) -> None:
        self.adapter = RuleAdapter()

    def test_cach_thanh(self) -> None:
        contract = self.adapter.adapt(
            {
                "pattern_name": "Chính Quan Cách",
                "condition": "Cách thành",
                "score": 25,
            }
        )
        self.assertEqual(contract.source_type, "STATUS_PHRASE")
        pred = contract.conditions[0]
        self.assertEqual(pred.field, "pattern.status")
        self.assertEqual(pred.value, "SUCCESS")

    def test_hien_dien(self) -> None:
        contract = self.adapter.adapt(
            {"star_name": "Thiên Ất", "condition": "Hiện diện", "score": 3}
        )
        self.assertEqual(contract.source_type, "STATUS_PHRASE")
        pred = contract.conditions[0]
        self.assertEqual(pred.value, "PRESENT")
        self.assertTrue(pred.field.startswith("shensha."))


class TestRuleAdapterFieldCompare(unittest.TestCase):
    """FIELD_COMPARE_EXPR → Contract V1."""

    def setUp(self) -> None:
        self.adapter = RuleAdapter()

    def test_strength_score_gte(self) -> None:
        contract = self.adapter.adapt({"condition": "strength_score >= 80"})
        self.assertEqual(contract.source_type, "FIELD_COMPARE_EXPR")
        pred = contract.conditions[0]
        self.assertEqual(pred.field, "strength_score")
        self.assertEqual(pred.normalized_operator(), "gte")
        self.assertEqual(pred.value, 80)


class TestRuleAdapterEmptyCollection(unittest.TestCase):
    """EMPTY_COLLECTION → unconditional contract."""

    def setUp(self) -> None:
        self.adapter = RuleAdapter()

    def test_empty_list(self) -> None:
        contract = self.adapter.adapt({"conditions": [], "rule_id": "pattern_001"})
        self.assertEqual(contract.source_type, "EMPTY_COLLECTION")
        self.assertTrue(contract.is_unconditional)

    def test_empty_json_string(self) -> None:
        contract = self.adapter.adapt({"conditions": "[]"})
        self.assertTrue(contract.is_unconditional)


class TestRuleAdapterJsonArray(unittest.TestCase):
    """JSON_ARRAY_FIELD_OPS → Contract V1."""

    def setUp(self) -> None:
        self.adapter = RuleAdapter()

    def test_field_ops_array(self) -> None:
        contract = self.adapter.adapt(
            {
                "conditions": [
                    {
                        "condition_id": "C001",
                        "field": "context.day_master",
                        "operator": "eq",
                        "value": "Bính",
                    }
                ]
            }
        )
        self.assertEqual(contract.source_type, "JSON_ARRAY_FIELD_OPS")
        self.assertEqual(contract.conditions[0].field, "context.day_master")
        self.assertEqual(contract.conditions[0].value, "Bính")


class TestRuleAdapterJsonObject(unittest.TestCase):
    """JSON_OBJECT_MAP → Contract V1."""

    def setUp(self) -> None:
        self.adapter = RuleAdapter()

    def test_object_map(self) -> None:
        contract = self.adapter.adapt(
            {
                "conditions": {
                    "month_branch_contains": "zheng_guan",
                    "day_master_strength": ["strong", "balanced"],
                    "not_destroyed": True,
                }
            }
        )
        self.assertEqual(contract.source_type, "JSON_OBJECT_MAP")
        self.assertGreaterEqual(len(contract.conditions), 3)
        fields = {item.field for item in contract.conditions}
        self.assertIn("bazi.month_branch", fields)
        self.assertIn("strength.level", fields)


class TestRuleAdapterImplicit(unittest.TestCase):
    """Files without condition → implicit metadata."""

    def setUp(self) -> None:
        self.adapter = RuleAdapter()

    def test_month_status(self) -> None:
        contract = self.adapter.adapt(
            {
                "rule_code": "IN_SEASON",
                "month_status": "Đắc lệnh",
                "score": 35,
            }
        )
        self.assertEqual(contract.source_type, "IMPLICIT_COLUMN_SCHEMA")
        pred = contract.conditions[0]
        self.assertEqual(pred.field, "strength.month_status")
        self.assertEqual(pred.value, "Đắc lệnh")

    def test_score_range(self) -> None:
        contract = self.adapter.adapt(
            {"grade": "A", "min_score": 80, "max_score": 84}
        )
        self.assertEqual(contract.source_type, "IMPLICIT_COLUMN_SCHEMA")
        pred = contract.conditions[0]
        self.assertEqual(pred.normalized_operator(), "between")
        self.assertEqual(pred.value, [80, 84])


class TestRuleConditionMatcher(unittest.TestCase):
    """Matcher V1 — no eval."""

    def setUp(self) -> None:
        self.matcher = RuleConditionMatcher()

    def test_enum_match(self) -> None:
        rule = {"element": "WOOD", "condition": "PRESENT"}
        ctx = {"wuxing": {"wood": {"status": "PRESENT"}}}
        self.assertTrue(self.matcher.match_rule(rule, ctx))
        ctx_miss = {"wuxing": {"wood": {"status": "MISSING"}}}
        self.assertFalse(self.matcher.match_rule(rule, ctx_miss))

    def test_status_match(self) -> None:
        rule = {"pattern_name": "Chính Quan", "condition": "Cách thành"}
        self.assertTrue(
            self.matcher.match_rule(rule, {"pattern": {"status": "SUCCESS"}})
        )
        self.assertFalse(
            self.matcher.match_rule(rule, {"pattern": {"status": "DESTROYED"}})
        )

    def test_field_compare(self) -> None:
        rule = {"condition": "strength_score >= 80"}
        self.assertTrue(self.matcher.match_rule(rule, {"strength_score": 90}))
        self.assertFalse(self.matcher.match_rule(rule, {"strength_score": 10}))

    def test_empty_collection_always_true(self) -> None:
        rule = {"conditions": []}
        self.assertTrue(self.matcher.match_rule(rule, {}))

    def test_json_array(self) -> None:
        rule = {
            "conditions": [
                {
                    "condition_id": "C001",
                    "field": "day_master",
                    "operator": "eq",
                    "value": "Bính",
                }
            ]
        }
        self.assertTrue(self.matcher.match_rule(rule, {"day_master": "Bính"}))
        self.assertFalse(self.matcher.match_rule(rule, {"day_master": "Canh"}))

    def test_json_object_map(self) -> None:
        rule = {
            "conditions": {
                "month_branch_contains": "zheng_guan",
                "not_destroyed": True,
            }
        }
        ctx = {
            "bazi": {"month_branch": "has_zheng_guan_token"},
            "pattern": {"not_destroyed": True},
        }
        # contains checks substring
        ctx["bazi"]["month_branch"] = "xx_zheng_guan_yy"
        self.assertTrue(self.matcher.match_rule(rule, ctx))

    def test_operators_between_contains_any(self) -> None:
        contract = RuleContract(
            conditions=[
                ConditionPredicate("C1", "score.total_score", "between", [10, 20]),
                ConditionPredicate(
                    "C2", "tags", "contains_any", ["a", "z"]
                ),
            ]
        )
        self.assertTrue(
            self.matcher.match_contract(
                contract,
                {"score": {"total_score": 15}, "tags": ["x", "a"]},
            )
        )

    def test_no_eval_in_score_matcher_source(self) -> None:
        import ast
        import inspect
        from engines.score_engine.matcher import matcher as matcher_mod

        tree = ast.parse(inspect.getsource(matcher_mod))
        calls = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "eval"
        ]
        self.assertEqual(calls, [])

class TestScoreRuleMatcherFacade(unittest.TestCase):
    """Score Engine RuleMatcher facade uses V1."""

    def test_match_dataframe_like_list(self) -> None:
        matcher = ScoreRuleMatcher()
        rules = [
            {"element": "FIRE", "condition": "PRESENT", "score": 5},
            {"element": "WATER", "condition": "PRESENT", "score": 5},
        ]
        ctx = {
            "wuxing": {
                "fire": {"status": "PRESENT"},
                "water": {"status": "MISSING"},
            }
        }
        matched = matcher.match(rules, ctx)
        self.assertEqual(len(matched), 1)
        self.assertEqual(matched[0]["element"], "FIRE")


if __name__ == "__main__":
    unittest.main()
