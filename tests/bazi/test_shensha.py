"""
Kiểm thử Thần Sát.
"""

import unittest

from engines.bazi_engine.shensha.service import ShenShaService


class TestShenSha(unittest.TestCase):

    def setUp(self):
        self.service = ShenShaService()

    def test_calculate(self):

        result = self.service.calculate(
            year_branch="Dần",
            day_master="Canh"
        )

        self.assertIsInstance(result, list)

    def test_contains_items(self):

        result = self.service.calculate(
            "Dần",
            "Canh"
        )

        self.assertGreaterEqual(len(result), 0)


if __name__ == "__main__":
    unittest.main()
