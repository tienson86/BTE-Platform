"""
Unit Test cho RuleMatcher.
"""

import unittest

from engines.score_engine.matcher.matcher import RuleMatcher
from engines.score_engine.context import ScoreContext


class TestRuleMatcher(unittest.TestCase):

    def setUp(self):
        self.matcher = RuleMatcher()

        self.context = ScoreContext()
        self.context.strength = 75
        self.context.day_master = "Canh"

    def test_equal(self):
        self.assertTrue(
            self.matcher.evaluate(
                "day_master == 'Canh'",
                self.context
            )
        )

    def test_not_equal(self):
        self.assertFalse(
            self.matcher.evaluate(
                "day_master == 'Giáp'",
                self.context
            )
        )

    def test_greater(self):
        self.assertTrue(
            self.matcher.evaluate(
                "strength >= 70",
                self.context
            )
        )

    def test_less(self):
        self.assertFalse(
            self.matcher.evaluate(
                "strength < 50",
                self.context
            )
        )

    def test_match_rule(self):
        rule = {
            "condition": "strength >= 70"
        }

        self.assertTrue(
            self.matcher.match(
                rule,
                self.context
            )
        )


if __name__ == "__main__":
    unittest.main()
