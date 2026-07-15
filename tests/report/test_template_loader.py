import unittest

from engines.report_engine.template_loader import (
    TemplateLoader,
)


class TestTemplateLoader(unittest.TestCase):

    def setUp(self):
        self.loader = TemplateLoader()

    def test_load(self):
        template = self.loader.load(
            "default"
        )

        self.assertIsNotNone(template)

    def test_list(self):
        templates = self.loader.list()

        self.assertIsInstance(
            templates,
            list
        )


if __name__ == "__main__":
    unittest.main()
