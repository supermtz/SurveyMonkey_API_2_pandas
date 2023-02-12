import unittest
from src.utils import html_parser


class TestHtmlParser(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(html_parser.get_text("<strong>Hello</strong>"), "Hello")


if __name__ == "__main__":
    unittest.main()
