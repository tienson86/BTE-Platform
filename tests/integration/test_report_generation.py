"""
Kiểm thử sinh báo cáo.
"""

import unittest

from engines.report_engine.engine import ReportEngine


class TestReportGeneration(unittest.TestCase):

    def test_generate(self):

        engine = ReportEngine()

        report = engine.generate({})

        self.assertTrue(report.success)

        self.assertGreater(
            len(report.content),
            0
        )


if __name__ == "__main__":
    unittest.main()
