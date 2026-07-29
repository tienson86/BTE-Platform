"""
Kiểm thử lập đầy đủ một lá số.
"""

import unittest

from engines.bazi_engine.engine import BaziEngine


class TestFullChart(unittest.TestCase):

    def setUp(self):

        self.engine = BaziEngine()

    def test_chart_complete(self):

        chart = self.engine.build(
            year=1987,
            month=1,
            day=21,
            hour=4,
            minute=10,
            gender="male"
        )

        self.assertEqual(len(chart.pillars), 4)

        self.assertIsNotNone(chart.day_master)

        self.assertGreater(len(chart.ten_gods), 0)

        self.assertGreater(len(chart.hidden_stems), 0)

        self.assertGreaterEqual(len(chart.shensha), 0)


if __name__ == "__main__":
    unittest.main()
