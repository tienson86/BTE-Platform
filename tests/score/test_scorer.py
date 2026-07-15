"""
Unit Test cho RuleScorer.
"""

import unittest

from engines.score_engine.utils.scorer import RuleScorer


class TestRuleScorer(unittest.TestCase):

    def setUp(self):
        self.scorer = RuleScorer()

    def test_initial_score(self):
        self.assertEqual(
            self.scorer.score,
            0
        )

    def test_add_score(self):
        self.scorer.add(
            20,
            "R001",
            "Test"
        )

        self.assertEqual(
            self.scorer.score,
            20
        )

    def test_subtract_score(self):
        self.scorer.add(30)
        self.scorer.subtract(10)

        self.assertEqual(
            self.scorer.score,
            20
        )

    def test_reset(self):
        self.scorer.add(50)

        self.scorer.reset()

        self.assertEqual(
            self.scorer.score,
            0
        )

    def test_history(self):
        self.scorer.add(
            10,
            "R001",
            "Positive"
        )

        self.scorer.subtract(
            5,
            "R002",
            "Negative"
        )

        self.assertEqual(
            len(self.scorer.history),
            2
        )


if __name__ == "__main__":
    unittest.main()
