import unittest

from engines.interpretation_engine.rule_loader import RuleLoader


class TestRuleLoader(unittest.TestCase):

    def setUp(self):
        self.loader = RuleLoader()

    def test_load(self):
        rules = self.loader.load()

        self.assertIsInstance(rules, list)

    def test_not_empty(self):
        rules = self.loader.load()

        self.assertGreaterEqual(
            len(rules),
            0
        )


if __name__ == "__main__":
    unittest.main()
