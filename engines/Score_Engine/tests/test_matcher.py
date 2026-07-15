import unittest

from engines.score_engine.utils.matcher import RuleMatcher


class TestRuleMatcher(unittest.TestCase):

    def test_create_matcher(self):

        matcher = RuleMatcher()

        self.assertIsNotNone(matcher)

    def test_match_empty(self):

        matcher = RuleMatcher()

        self.assertEqual(
            matcher.match([], {}),
            []
        )


if __name__ == "__main__":
    unittest.main()
