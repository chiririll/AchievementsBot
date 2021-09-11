import unittest
from io import BytesIO

from Achievement import *


class AchievementTests(unittest.TestCase):

    def test_Default(self):
        self.__test_style("Default.achst", "Default", description="Test default achievement style")

    def test_Magical(self):
        self.__test_style("Magical.achst", "Magical", description="Test magical achievement style")

    def test_Layout(self):
        self.__test_style("Layout.achs")

    def __test_style(self, ach_style: str, name="Testing", icon=None, description=None, lang="ENG"):
        st = Style(open(f"Styles/{ach_style}", 'rb'), lang)
        ach = Achievement(st, name, icon, description)
        f = ach.generate()

        self.assertIs(type(f), BytesIO)

        saver = open(f"Images/styles/{ach_style.split('.', 1)[0].lower()}.png", 'wb')
        saver.write(f.read())
        saver.close()


if __name__ == '__main__':
    unittest.main()
