import unittest
import image_parser

class SearchTests(unittest.TestCase):

    def test_search(self):
        self.assertTrue(image_parser.get_google("amogus") is not None)

    def test_search_all(self):
        self.assertTrue(image_parser.get_google("amogus", True) is not None)
