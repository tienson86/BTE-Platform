"""
Kiểm thử Tàng Can.
"""

import unittest

from engines.bazi_engine.hidden_stems.service import HiddenStemService


class TestHiddenStems(unittest.TestCase):

    def setUp(self):
        self.service = HiddenStemService()

    def test_hidden_stem_of_zi(self):

        stems = self.service.get("Tý")

        self.assertGreater(len(stems), 0)

    def test_hidden_stem_of_wu(self):

        stems = self.service.get("Ngọ")

        self.assertGreater(len(stems), 0)

    def test_hidden_stem_type(self):

        stems = self.service.get("Dần")

        self.assertIsInstance(stems, list)


if __name__ == "__main__":
    unittest.main()
