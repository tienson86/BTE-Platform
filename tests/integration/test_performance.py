"""
Kiểm thử hiệu năng.
"""

import time
import unittest

from engines.bazi_engine.engine import BaziEngine


class TestPerformance(unittest.TestCase):

    def test_speed(self):

        engine = BaziEngine()

        start = time.perf_counter()

        for _ in range(100):

            engine.build(
                1987,
                1,
                21,
                4,
                10
            )

        elapsed = time.perf_counter() - start

        self.assertLess(elapsed, 10.0)
