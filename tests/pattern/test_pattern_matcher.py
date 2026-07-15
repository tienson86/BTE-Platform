import unittest

from engines.pattern.matcher import PatternMatcher
from engines.pattern.context import PatternContext


class TestPatternMatcher(unittest.TestCase):

    def setUp(self):
        self.matcher = PatternMatcher()
        self.context = PatternContext()

    def test_create(self):
        self.assertIsNotNone(self.matcher)

    def test_match(self):
        result = self.matcher.match(self.context)
        self.assertIsInstance(result, list)

    def test_empty(self):
        result = self.matcher.match(None)
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
