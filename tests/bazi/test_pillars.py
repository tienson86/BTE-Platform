"""
Kiểm thử tính toán Tứ Trụ.
"""

import unittest

from engines.bazi_engine.engine import BaziEngine


class TestPillars(unittest.TestCase):

    def setUp(self):
        self.engine = BaziEngine()

    def test_build_four_pillars(self):

        chart = self.engine.build(
            year=1987,
            month=1,
            day=21,
            hour=4,
            minute=10,
            gender="male"
        )

        self.assertIsNotNone(chart)

        self.assertIsNotNone(chart.year_pillar)
        self.assertIsNotNone(chart.month_pillar)
        self.assertIsNotNone(chart.day_pillar)
        self.assertIsNotNone(chart.hour_pillar)

    def test_day_master_exists(self):

        chart = self.engine.build(
            1987, 1, 21, 4, 10
        )

        self.assertIsNotNone(chart.day_master)

    def test_hidden_stems_loaded(self):

        chart = self.engine.build(
            1987, 1, 21, 4, 10
        )

        self.assertGreater(
            len(chart.hidden_stems),
            0
        )


if __name__ == "__main__":
    unittest.main()
