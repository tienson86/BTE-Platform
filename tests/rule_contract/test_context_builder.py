"""
WP2B-3 unit tests — RuleContext Builder.
"""

from __future__ import annotations

import unittest

from engines.bazi_engine.engine import BaziEngine
from engines.calendar_engine.engine import CalendarEngine
from engines.pattern_engine.context import PatternContext
from engines.pattern_engine.engine import PatternEngine
from engines.rule_contract import (
    RuleConditionMatcher,
    RuleContextBuilder,
)
from engines.rule_contract.context_builder import EXPECTED_SIGNALS, REQUIRED_SECTIONS


class TestCalendarToRuleContext(unittest.TestCase):
    """Calendar → RuleContext."""

    def test_calendar_section(self) -> None:
        calendar = CalendarEngine().build(1987, 1, 21, 4, 15)
        ctx = RuleContextBuilder().build(calendar=calendar)

        self.assertIn("calendar", ctx)
        self.assertEqual(ctx["calendar"]["solar_year"], 1987)
        self.assertEqual(ctx["calendar"]["solar_month"], 1)
        self.assertEqual(ctx["calendar"]["solar_day"], 21)
        self.assertEqual(ctx["calendar"]["solar_hour"], 4)
        self.assertIsNotNone(ctx["calendar"]["julian_day"])
        self.assertIsNotNone(ctx["month"]["status"])
        self.assertEqual(ctx["wuxing"]["season"], "winter")


class TestBaziToRuleContext(unittest.TestCase):
    """Bazi → RuleContext."""

    def test_bazi_signals(self) -> None:
        calendar = CalendarEngine().build(1987, 1, 21, 4, 15)
        chart = BaziEngine().build(calendar, gender="male")
        ctx = RuleContextBuilder().build(calendar=calendar, bazi=chart)

        self.assertEqual(ctx["bazi"]["day_master"], chart.day_master)
        self.assertEqual(ctx["day_master"], chart.day_master)
        self.assertEqual(ctx["bazi"]["gender"], "male")
        self.assertIn("stem", ctx["bazi"]["year_pillar"])
        self.assertIn("branch", ctx["bazi"]["month_pillar"])
        self.assertTrue(ctx["facts"]["has_day_master"])

        # Five-element status signals
        for element in ("wood", "fire", "earth", "metal", "water"):
            self.assertIn(element, ctx["wuxing"])
            self.assertIn(
                ctx["wuxing"][element]["status"],
                {"PRESENT", "STRONG", "EXCESS", "MISSING"},
            )


class TestPatternToRuleContext(unittest.TestCase):
    """Pattern → RuleContext."""

    def test_pattern_signals(self) -> None:
        calendar = CalendarEngine().build(1987, 1, 21, 4, 15)
        chart = BaziEngine().build(calendar, gender="male")
        pctx = PatternContext(
            year_pillar=f"{chart.year_pillar.stem} {chart.year_pillar.branch}",
            month_pillar=f"{chart.month_pillar.stem} {chart.month_pillar.branch}",
            day_pillar=f"{chart.day_pillar.stem} {chart.day_pillar.branch}",
            hour_pillar=f"{chart.hour_pillar.stem} {chart.hour_pillar.branch}",
            day_master=chart.day_master,
        )
        pattern = PatternEngine().calculate(pctx)
        ctx = RuleContextBuilder().build(
            calendar=calendar,
            bazi=chart,
            pattern=pattern,
        )

        self.assertEqual(ctx["pattern"]["main_pattern"], pattern.pattern)
        self.assertEqual(ctx["pattern"]["name"], pattern.pattern)
        self.assertEqual(ctx["pattern"]["success"], pattern.success)
        if pattern.success and pattern.pattern:
            self.assertEqual(ctx["pattern"]["status"], "SUCCESS")
            self.assertTrue(ctx["facts"]["pattern_identified"])
            self.assertTrue(ctx["facts"]["pattern_success"])


class TestContextCompleteness(unittest.TestCase):
    """Context completeness / coverage."""

    def test_required_sections_always_present(self) -> None:
        ctx = RuleContextBuilder().build()
        for section in REQUIRED_SECTIONS:
            self.assertIn(section, ctx)

    def test_full_pipeline_coverage(self) -> None:
        calendar = CalendarEngine().build(1987, 1, 21, 4, 15)
        chart = BaziEngine().build(calendar, gender="male")
        pctx = PatternContext(
            day_master=chart.day_master,
            month_pillar=f"{chart.month_pillar.stem} {chart.month_pillar.branch}",
        )
        pattern = PatternEngine().calculate(pctx)

        builder = RuleContextBuilder()
        ctx = builder.build(calendar=calendar, bazi=chart, pattern=pattern)
        report = builder.completeness(ctx)

        self.assertEqual(report["missing_sections"], [])
        self.assertGreaterEqual(report["coverage_percent"], 70.0)
        self.assertTrue(
            set(report["present_signals"]).issubset(set(EXPECTED_SIGNALS))
        )

    def test_matcher_uses_rule_context_only(self) -> None:
        """Matcher can decide without touching BaziChart directly."""
        calendar = CalendarEngine().build(1987, 1, 21, 4, 15)
        chart = BaziEngine().build(calendar, gender="male")
        pattern = PatternEngine().calculate(
            PatternContext(day_master=chart.day_master)
        )
        ctx = RuleContextBuilder().build(
            calendar=calendar,
            bazi=chart,
            pattern=pattern,
        )

        matcher = RuleConditionMatcher()
        # ENUM-style rule against wuxing signal
        wood_status = ctx["wuxing"]["wood"]["status"]
        rule = {"element": "WOOD", "condition": wood_status}
        self.assertTrue(matcher.match_rule(rule, ctx))

        # Pattern status rule
        if ctx["pattern"]["status"] == "SUCCESS":
            self.assertTrue(
                matcher.match_rule(
                    {"pattern_name": "X", "condition": "Cách thành"},
                    ctx,
                )
            )


if __name__ == "__main__":
    unittest.main()
