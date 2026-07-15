"""
Integration Test cho Bazi Engine.
"""

import unittest

from engines.bazi_engine.engine import BaziEngine


class TestBaziEngine(unittest.TestCase):

    def setUp(self):
        self.engine = BaziEngine()

    def test_build_chart(self):

        chart = self.engine.build(
            year=1987,
            month=1,
            day=21,
            hour=4,
            minute=10,
            gender="male"
        )

        self.assertIsNotNone(chart)

    def test_chart_has_pillars(self):

        chart = self.engine.build(
            1987, 1, 21, 4, 10
        )

        self.assertEqual(
            len(chart.pillars),
            4
        )

    def test_chart_day_master(self):

        chart = self.engine.build(
            1987, 1, 21, 4, 10
        )

        self.assertIsNotNone(chart.day_master)

    def test_chart_ten_gods(self):

        chart = self.engine.build(
            1987, 1, 21, 4, 10
        )

        self.assertGreaterEqual(
            len(chart.ten_gods),
            4
        )

    def test_chart_shensha(self):

        chart = self.engine.build(
            1987, 1, 21, 4, 10
        )

        self.assertIsNotNone(chart.shensha)


if __name__ == "__main__":
    unittest.main()
