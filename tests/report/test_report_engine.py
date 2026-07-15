import unittest

from engines.report_engine.engine import ReportEngine


class TestReportEngine(unittest.TestCase):

    def setUp(self):
        self.engine = ReportEngine()

    def test_generate(self):
        report = self.engine.generate(
            {}
        )

        self.assertTrue(report.success)

    def test_content(self):
        report = self.engine.generate(
            {}
        )

        self.assertGreater(
            len(report.content),
            0
        )


if __name__ == "__main__":
    unittest.main()
