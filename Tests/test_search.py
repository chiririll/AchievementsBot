import unittest
from Bot import Tools


class SearchTests(unittest.TestCase):

    TEST_REQUEST = "Hello, World!"

    def test_search(self):
        self.assertTrue(Tools.search_image(SearchTests.TEST_REQUEST) is not None)

    def test_search_all(self):
        self.assertTrue(Tools.search_image(SearchTests.TEST_REQUEST, True) is not None)
