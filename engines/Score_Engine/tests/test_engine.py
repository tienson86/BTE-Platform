import unittest

from engines.score_engine.engine import ScoreEngine


class TestEngine(unittest.TestCase):

    def test_create(self):

        engine = ScoreEngine(None)

        self.assertIsNotNone(engine)


if __name__ == "__main__":
    unittest.main()
