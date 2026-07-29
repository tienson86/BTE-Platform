"""
Kiểm thử nhiều lá số liên tiếp.
"""

import unittest

from engines.bazi_engine.engine import BaziEngine


class TestMultipleCases(unittest.TestCase):

    def test_many_charts(self):

        engine = BaziEngine()

        samples = [

            (1987, 1, 21, 4, 10),

            (1995, 6, 10, 12, 0),

            (2001, 11, 5, 18, 30),

        ]

        for item in samples:

            chart = engine.build(*item)

            self.assertIsNotNone(chart)
