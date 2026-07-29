import unittest

from engines.report_engine.renderer import Renderer


class TestRenderer(unittest.TestCase):

    def setUp(self):
        self.renderer = Renderer()

    def test_render(self):
        html = self.renderer.render(
            {},
            "default"
        )

        self.assertIsInstance(
            html,
            str
        )

    def test_not_none(self):
        self.assertIsNotNone(
            self.renderer.render(
                {},
                "default"
            )
        )


if __name__ == "__main__":
    unittest.main()
