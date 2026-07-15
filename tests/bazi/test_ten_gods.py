"""
Kiểm thử Thập Thần.
"""

import unittest

from engines.bazi_engine.ten_gods.service import TenGodService


class TestTenGods(unittest.TestCase):

    def setUp(self):
        self.service = TenGodService()

    def test_compare_stems(self):

        god = self.service.calculate(
            day_master="Canh",
            target="Giáp"
        )

        self.assertIsNotNone(god)

    def test_same_element(self):

        god = self.service.calculate(
            "Canh",
            "Tân"
        )

        self.assertIsNotNone(god)

    def test_different_element(self):

        god = self.service.calculate(
            "Canh",
            "Bính"
        )

        self.assertIsNotNone(god)


if __name__ == "__main__":
    unittest.main()
