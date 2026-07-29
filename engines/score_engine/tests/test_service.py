import unittest

from engines.score_engine.service import ScoreService


class TestService(unittest.TestCase):

    def test_create(self):

        service = ScoreService(
            "database/13_score_engine"
        )

        self.assertIsNotNone(service)


if __name__ == "__main__":
    unittest.main()
